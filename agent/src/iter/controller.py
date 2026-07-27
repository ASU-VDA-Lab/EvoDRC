#BSD 3-Clause License
#
#Copyright (c) 2026, ASU-VDA-Lab
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################

"""Iterative block-repair orchestrator.

``run_iterative_block_repair(ctx)`` runs up to MAX_ITERS rounds, configured by
``agent/evodrc.conf``. Each round decomposes the current block into repair
units, repairs every repairable unit with one model call apiece, gates the
resulting patches on connectivity, assembles the ones that pass, re-measures
block DRC and connectivity, and evolves the per-layer knowledge store. It stops
early when the block is DRC-clean or nothing is repairable. Artifacts are
persisted under a deterministic root, the last connectivity-preserving repair
is copied to ``output_path``, and the function returns ``(status, error)``.
"""

import json
import os
import shutil
import sys

from .. import hrd_split as _hrd
from ..logging_setup import get_logger, stage_extra
from . import assemble as _assemble
from . import block_eval as _block_eval
from . import conf as _conf
from . import crop_history as _crop_history
from . import cu_drc as _cu_drc
from . import decompose as _decompose
from . import evolve as _evolve
from . import gate as _gate
from . import inject as _inject
from . import layerdb as _layerdb
from . import paths as _paths
from . import plan as _plan
from . import schedule as _schedule
from . import seed as _seed
from . import workdir as _workdir


def _hard_assert_startup(info):
    """Check the preconditions the run cannot recover from, raising on any."""
    # Per-leaf token capture requires RECORD_TOKENS=1 and AGENT_CALLS_DIR.
    if os.environ.get("RECORD_TOKENS") != "1" \
            or not os.environ.get("AGENT_CALLS_DIR", "").strip():
        raise RuntimeError(
            "RECORD_TOKENS!=1 or AGENT_CALLS_DIR empty: per-leaf token capture "
            "disabled -- relaunch with `RECORD_TOKENS=1 bash "
            "src/evaluate_claude.sh` from the DAC26_DRC_Benchmark root (the "
            "Dockerfile ENV bake is overridden by evaluate_claude.sh's "
            "`docker exec -e RECORD_TOKENS`).")
    # The connectivity helper must be importable: on an import error the gate
    # returns False for everything and silently rejects every leaf.
    from ..connectivity import _resolve_check_connectivity
    try:
        _resolve_check_connectivity()
    except Exception as exc:                          # noqa: BLE001
        raise RuntimeError(
            "check_connectivity not importable (connectivity gate would "
            "silently reject every leaf): {0}".format(exc))
    if not (info.rule_path and os.path.isfile(info.rule_path)):
        raise RuntimeError("rule_path missing: {0}".format(info.rule_path))
    if not (info.connectivity_path and os.path.isfile(info.connectivity_path)):
        raise RuntimeError(
            "connectivity_path missing: {0}".format(info.connectivity_path))
    if not (info.layout_path and os.path.isfile(info.layout_path)):
        raise RuntimeError("layout_path missing: {0}".format(info.layout_path))
    if not (info.drc_path and os.path.isfile(info.drc_path)):
        raise RuntimeError(
            "drc_path (golden DRC report) missing: {0}".format(info.drc_path))


def _emit_output(src_py, output_path):
    """Atomically copy ``src_py`` to ``output_path``, the file the scorer
    reads."""
    if not (src_py and os.path.isfile(src_py) and output_path):
        return False
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)),
                    exist_ok=True)
    except OSError:
        pass
    tmp = output_path + ".iter_tmp"
    try:
        shutil.copyfile(src_py, tmp)
        os.replace(tmp, output_path)
        return True
    except OSError:
        try:
            if os.path.isfile(tmp):
                os.remove(tmp)
        except OSError:
            pass
        return False


def _max_iters():
    try:
        return int(os.environ.get("MAX_ITERS", "5"))
    except (TypeError, ValueError):
        return 5


def run_iterative_block_repair(ctx):
    log = get_logger()
    info = ctx.case_info
    case_name = info.case_name or "Block5"
    design_type = info.design_type or "block"
    output_path = info.output_path or ctx.output_path
    score_calls_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()

    # Resolve the config first: it writes MAX_ITERS, LEAF_CONCURRENCY and the
    # rest back into os.environ, which is what _max_iters(),
    # schedule._concurrency() and every leaf subprocess read.
    cfg = _conf.resolve()

    _hard_assert_startup(info)

    max_iters = _max_iters()
    # Deterministic root, <base>/data/<EXP>/<CASE>/<MODEL>. Re-running the same
    # case replaces its previous results.
    persist_root = _paths.resolve_persist_root(case_name, info.model_name,
                                               cfg.ablation)

    # ---- container-local work root ------------------------------------------
    # Everything under persist_root is bind-mounted out and forms the published
    # run record. Internal working files go here instead, outside every bind
    # mount, and are discarded with the container.
    work_root = _workdir.resolve_work_root(persist_root)
    # The benchmark temp root sits one level above persist_root, and the
    # rendered prompt names <base>/conn and <base>/drc, so those two dirs are
    # claimed by atomic mkdir and only the ones created here are released.
    temp_base = _paths.persist_base()
    owned_scratch = _workdir.claim_base_scratch(temp_base)
    try:

        # ---- knowledge store wiring -----------------------------------------
        # Both roots are set once, before seeding, so the main.md the seed
        # builds already carries its final index paths. They resolve to
        # <persist_root>/db and <persist_root>/skill, with the stable injection
        # dir at <persist_root>/_inject; nothing is ever written inside the
        # read-only agent mount.
        _layerdb.set_store_root(persist_root)
        _layerdb.set_index_prefix(
            os.path.join(persist_root, "_inject", "knowledge"))
        if info.skill_path and os.path.isfile(info.skill_path):
            os.environ.setdefault("EVODRC_SKILL_MD", info.skill_path)
        _seed.ensure_seed(cfg.seed_dir, provenance=cfg.provenance,
                          label=(cfg.ablation or "cla"))

        # Surface the host-visible artifact root so the operator can find it.
        sys.stderr.write(
            "EVODRC_ITER persist_root={0} ablation={1} evolution={2} "
            "max_iters={3}\n".format(persist_root,
                                     cfg.ablation or "(production)",
                                     cfg.evolution, max_iters))
        log.info("iterative repair persist_root=%s max_iters=%d ablation=%s "
                 "evolution=%s whole_design=%s", persist_root, max_iters,
                 cfg.ablation or "(production)", cfg.evolution, cfg.whole_design,
                 extra=stage_extra("S0"))

        # Keep the untouched original, to check later that the output differs.
        try:
            with open(info.layout_path, "r", encoding="utf-8") as fh:
                original_text = fh.read()
        except OSError:
            original_text = None

        current_layout = info.layout_path
        current_drc = info.drc_path
        any_applied = False
        last_good_py = None

        for i in range(1, max_iters + 1):
            iter_dir = _paths.ensure_fresh_iter_dir(persist_root, i)
            # This iteration's container-local work dir.
            iter_work = _workdir.iter_work_dir(work_root, i)
            # Refresh the stable injection dir from the current layer store and
            # record its manifest in this iteration dir. A pure copy: main.md is
            # never rebuilt here.
            inject_d = _inject.stage(persist_root, iter_dir,
                                     work_dir=iter_work)
            in_layout = os.path.join(iter_dir, "input",
                                     "{0}.py".format(case_name))
            in_drc = os.path.join(iter_dir, "input",
                                  "{0}.drc.json".format(case_name))
            shutil.copyfile(current_layout, in_layout)
            shutil.copyfile(current_drc, in_drc)
            # The reference connectivity net list, kept alongside the layout
            # and the DRC report in this iteration's input/ directory.
            if info.connectivity_path and os.path.isfile(info.connectivity_path):
                try:
                    shutil.copyfile(
                        info.connectivity_path,
                        os.path.join(iter_dir, "input",
                                     "{0}.json".format(case_name)))
                except OSError:
                    pass

            # ---- decompose (controller's own ctx for gate + assemble) ----------
            dctx = _decompose.decompose_ctx(
                layout_path=in_layout, drc_path=in_drc, case_name=case_name,
                design_type=design_type, connectivity_path=info.connectivity_path,
                rule_path=info.rule_path, skill_path=info.skill_path,
                model_name=info.model_name,
                temp_dir=os.path.join(iter_work, "_dec_ctrl"))
            leaves_doc = _decompose.leaves_json(dctx, i)
            with open(os.path.join(iter_dir, "leaves.json"), "w",
                      encoding="utf-8") as fh:
                json.dump(leaves_doc, fh, indent=2)
            # ---- unit planning: leaves -> repair units -------------------------
            # A repair unit can span many leaves. plan_units merges single-row
            # crops sharing a standard-cell row band into row unions, keeps
            # multi-row and PDN crops standalone, quarantines the rest, and
            # writes unions.json plus a per-union projection. Whole-design mode
            # replaces the grouping with one unit instead. Both register their
            # non-leaf units into dctx.leaves, which gate, assemble and cu_drc
            # need.
            if cfg.whole_design:
                plan_doc = _plan.plan_whole(dctx, case_name, iter_dir, _hrd)
            else:
                plan_doc = _plan.plan_units(dctx, case_name, iter_dir, _hrd)
            units = plan_doc["units"]
            rep_ids = plan_doc["repairable"]
            unions_map = plan_doc["unions_map"]
            log.info("iter%d leaves=%d units=%d repairable=%d union=%d", i,
                     len(leaves_doc.get("leaves", []) or []), len(units),
                     len(rep_ids), len(unions_map), extra=stage_extra("S0"))

            # Decompose has rewritten in_layout with anchor comments, so it is
            # read afterwards, giving patch_apply anchors that resolve.
            with open(in_layout, "r", encoding="utf-8") as fh:
                input_text = fh.read()

            # ---- early stop: nothing repairable (block is DRC-clean) -----------
            if not rep_ids:
                n_v = len(dctx.violations)
                result = {"iter": i, "start_violations": n_v,
                          "end_violations": n_v,
                          "repair_rate": 0.0, "new_violation_count": 0,
                          "connectivity": "preserved",
                          "drc_total_after": n_v,
                          "input_drc": in_drc, "repaired_drc": "",
                          "note": "no repairable leaves (block DRC-clean)"}
                log.info("iter%d no repairable leaves (violations=%d); early stop",
                         i, n_v, extra=stage_extra("S0"))
                # The same projection the main path writes: the file gets the
                # fixed keys and ``note`` stays on the dict handed to evolve.
                _block_eval.write_block_result(iter_dir, result)
                # The loop that fills gated_in / patch_objs is below.
                _evolve.update_all(iter_dir, i, case_name, dctx,
                                   rep_ids=[], gated_in=[], patch_objs={},
                                   result=result, cfg=cfg,
                                   work_dir=iter_work)
                break

            # ---- repair every unit, scheduled under LEAF_CONCURRENCY ----------
            common = {
                "iter_dir": iter_dir,
                "input_layout": in_layout,
                "input_drc": in_drc,
                "case_name": case_name,
                "design_type": design_type,
                "conn_path": info.connectivity_path,
                "rule_path": info.rule_path,
                "skill_path": info.skill_path,
                "model": info.model_name,
                "workspace": ctx.workspace or "",
                "score_calls_dir": score_calls_dir,
                "inject": inject_d,
                "tc_dir": os.path.dirname(info.rule_path or "") or "",
                "ablation": cfg.ablation,
                "prompt_mode": cfg.prompt_mode,
                "unions_map": unions_map,
            }
            _schedule.run_leaves(i, rep_ids, common, iter_work=iter_work)

            # ---- connectivity gate; no model calls -----------------------------
            gated_dir = os.path.join(iter_dir, "gated")
            os.makedirs(gated_dir, exist_ok=True)
            gate_scratch = os.path.join(iter_dir, "_gate")
            gated_in = []
            patch_objs = {}
            for leaf_id in rep_ids:
                # A plain join rather than paths.leaf_dir: this loop is
                # read-only and must not create a directory for a unit the
                # scheduler never produced.
                ld = os.path.join(iter_dir, "leaf", leaf_id)
                patch_json = os.path.join(ld, "patch.json")
                verdict = _gate.gate_leaf(
                    dctx, leaf_id, patch_json, input_text,
                    info.connectivity_path, design_type, gate_scratch)
                # The .verdict extension keeps these files distinct from the
                # <UNIT>.assembled.json files assemble writes to the same dir.
                with open(os.path.join(gated_dir, "{0}.verdict".format(leaf_id)),
                          "w", encoding="utf-8") as fh:
                    json.dump(verdict, fh, indent=2)
                try:
                    with open(patch_json, "r", encoding="utf-8") as fh:
                        patch_objs[leaf_id] = json.load(fh)
                except (OSError, ValueError):
                    pass
                if verdict.get("gated_in"):
                    gated_in.append(leaf_id)
            log.info("iter%d gated_in=%d/%d", i, len(gated_in), len(rep_ids),
                     extra=stage_extra("S0"))

            # ---- contested-unit DRC tournament --------------------------------
            # When several units propose ops on one shared target, such as a via
            # cell definition or a die-spanning polygon, no proposer's own window
            # can price the result. run_pool measures each candidate over a
            # coverage window set and elects at most one winner per conflict
            # component, writing cu_verdicts.json. A failure here is caught and
            # the iteration continues with first-wins assembly.
            pool = None
            if cfg.cu_drc:
                try:
                    pool = _cu_drc.run_pool(iter_dir, case_name, unions_map,
                                            units=units, ctx=dctx,
                                            golden_conn_path=info.connectivity_path,
                                            work_dir=iter_work)
                except Exception as exc:                  # noqa: BLE001
                    log.warning("iter%d cu_drc pool failed (%r) -- legacy "
                                "assembly", i, exc, extra=stage_extra("S0"))
                    pool = None

            # ---- shared via-cell competition config ---------------------------
            # Only used when two or more units edit the same via cell; assembly
            # stays free of KLayout otherwise.
            comp_cfg = None
            if cfg.via_competition:
                comp_cfg = {"deck": info.rule_path,
                            "scratch": os.path.join(iter_work, "_via_comp"),
                            "case": case_name}

            # ---- assemble gated-IN patches -> repaired/{case}.py ---------------
            repaired_dir = os.path.join(iter_dir, "repaired")
            os.makedirs(repaired_dir, exist_ok=True)
            out_py = os.path.join(repaired_dir, "{0}.py".format(case_name))
            _assemble.assemble(dctx, gated_in, patch_objs, input_text, out_py,
                               comp_cfg=comp_cfg, pool=pool,
                               records_dir=gated_dir)
            if gated_in:
                any_applied = True

            # ---- block DRC and connectivity ------------------------------------
            # Render artifacts go under repaired/_blockeval/, with the DRC report
            # copied up to repaired/<case>.drc.json.
            result, new_drc = _block_eval.run_block_drc_nested(
                repaired_py=out_py, input_drc_path=in_drc, case_name=case_name,
                design_type=design_type, rule_path=info.rule_path,
                golden_conn_path=info.connectivity_path,
                repaired_dir=repaired_dir, iter_index=i)

            # ---- the iteration's headline numbers -> block_result.json ---------
            # Written on both loop exits, so every iteration directory carries
            # this file.
            _block_eval.write_block_result(iter_dir, result)

            # ---- knowledge evolution -------------------------------------------
            _evolve.update_all(iter_dir, i, case_name, dctx,
                               rep_ids=rep_ids, gated_in=gated_in,
                               patch_objs=patch_objs, result=result, cfg=cfg,
                               work_dir=iter_work)

            # ---- archive each unit's ctx/ for the record -----------------------
            # Wrapped, so a snapshot failure leaves the completed iteration
            # intact.
            try:
                _crop_history.snapshot(persist_root, iter_dir, i)
            except Exception as exc:                      # noqa: BLE001
                log.warning("iter%d crop_history snapshot failed (%r)", i, exc,
                            extra=stage_extra("S0"))

            # ---- emit the best repaired .py so far to output_path --------------
            # Only overwrite when block connectivity is intact, so output_path
            # keeps the last assembly whose connectivity held.
            if result.get("connectivity") != "broken":
                if _emit_output(out_py, output_path):
                    last_good_py = out_py

            # ---- early stop: block DRC-clean -----------------------------------
            end_v = result.get("end_violations")
            if isinstance(end_v, int) and end_v == 0:
                log.info("iter%d block DRC-clean; early stop", i,
                         extra=stage_extra("S0"))
                break

            # ---- prepare next iteration ----------------------------------------
            if not (new_drc and os.path.isfile(new_drc)):
                log.warning("iter%d produced no block drc.json; stopping", i,
                            extra=stage_extra("S0"))
                break
            current_layout = out_py
            current_drc = new_drc

        # Final emit guard: ensure output_path holds the best repaired .py.
        if last_good_py and os.path.isfile(last_good_py):
            _emit_output(last_good_py, output_path)

        # ---- final verdict -------------------------------------------------------
        if any_applied and last_good_py and os.path.isfile(output_path):
            differs = True
            if original_text is not None:
                try:
                    with open(output_path, "r", encoding="utf-8") as fh:
                        differs = (fh.read() != original_text)
                except OSError:
                    differs = True
            if differs:
                return ("success", None)
            return ("fail",
                    "src_iter_no_op:patches mounted but output equals "
                    "original")
        return ("fail",
                "src_iter_no_patches_mounted:no leaf patch passed the "
                "connectivity gate across the iterations")
    finally:
        # Release the claimed scratch dirs. Every exception is swallowed: this
        # tidy-up must never turn a completed repair into a crash.
        try:
            _workdir.release_base_scratch(
                temp_base, owned_scratch,
                dest=os.path.join(work_root, "base_scratch"))
        except Exception as exc:                      # noqa: BLE001
            sys.stderr.write(
                "evodrc: base scratch release failed: {0}\n".format(exc))
