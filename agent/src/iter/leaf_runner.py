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

"""Per-unit repair runner, executed as a module in its own process.

``schedule.py`` starts one process per unit. The runner re-decomposes the
iteration input deterministically, selects the requested unit, builds its
prompt from the shared context carriers, makes a single model call, and writes
``prompt.txt``, ``patch.json``, ``trace.md`` and the recorded token JSON. The
published output directory ends up holding only ``ctx/``, ``patch.json`` and
``prompt.txt``; everything else stays in the container-local work directory.
The process always exits 0 and the controller reads the folder for the outcome.
"""

import argparse
import importlib
import json
import os
import shutil
import sys
import tempfile


# ---------------------------------------------------------------------------
# sys.path bootstrap, so ``agent.*`` and ``agent_backend`` both resolve: the
# parent of the agent directory is the workspace root, and its ``src`` sibling
# holds ``agent_backend``.
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))            # .../agent/src/iter
_AGENT_DIR = os.path.dirname(os.path.dirname(_HERE))          # .../agent
_WS = os.path.dirname(_AGENT_DIR)                             # /workspace
_SRC = os.path.join(_WS, "src")
for _p in (_WS, _SRC):
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

from agent.src.iter import decompose as _decompose          # noqa: E402
from agent.src.prompt_format import build_leaf_prompt        # noqa: E402
from agent.src.patch_parser import parse_patch_from_file_text  # noqa: E402
from agent.src import conn_context, drc_context              # noqa: E402
from agent.src.hrd_split import (WHOLE_UNIT_ID, build_union_leaf,  # noqa: E402,E501
                                 build_whole_design_leaf)
from agent.src.iter import paths as _paths                   # noqa: E402
from agent.src.iter import prompt_exp3 as _prompt_exp3       # noqa: E402
from agent.src.iter import workdir as _workdir               # noqa: E402

try:
    from agent.src import conn_impact_context as _ci_context  # noqa: E402
except Exception:                                                    # noqa: BLE001
    _ci_context = None


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _write_patch_json(out_dir, leaf_id, ops, explanation):
    obj = {"leaf_id": leaf_id, "ops": ops or [],
           "explanation": _paths.ascii_sanitize(explanation or "")}
    with open(os.path.join(out_dir, "patch.json"), "w",
              encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)


def _write_trace(out_dir, leaf_id, call_id, status, n_ops, explanation,
                 narration, error):
    lines = []
    lines.append("# Leaf {0} repair trace".format(leaf_id))
    lines.append("")
    lines.append("- call_id: {0}".format(call_id))
    lines.append("- claude status: {0}".format(status))
    lines.append("- ops emitted: {0}".format(n_ops))
    if error:
        lines.append("- error: {0}".format(
            _paths.ascii_sanitize(str(error))[:400]))
    lines.append("")
    lines.append("## Patch explanation (agent's own)")
    lines.append(_paths.ascii_sanitize(explanation or "(none)"))
    lines.append("")
    lines.append("## Agent narration excerpt (agent's own trace)")
    lines.append(_paths.ascii_sanitize(narration or "(no narration captured)"))
    body = "\n".join(lines)
    # Clamp the trace so a runaway narration cannot bloat the persisted dir.
    body = _paths.clamp_text(body, max_chars=8000)
    _write(os.path.join(out_dir, "trace.md"), body)


def _place_tokens(call_id, score_calls_dir, *, work_dir):
    """Copy ``_calls/<call_id>.json`` to ``tokens.json`` and to
    ``score_calls_dir``.

    ``work_dir`` is keyword-only and required, and together with
    ``score_calls_dir`` it is the only place this writes, which keeps the
    published unit directory out of reach. The ``score_calls_dir`` copy is the
    run-level calls directory that ``agent.src.tokens.aggregate`` reads. A
    missing source file, which happens when the backend recorded nothing, is
    tolerated: a ``tokens.json`` stub notes that no tokens were captured."""
    src = os.path.join(work_dir, "_calls", "{0}.json".format(call_id))
    dst = os.path.join(work_dir, "tokens.json")
    try:
        os.makedirs(work_dir, exist_ok=True)
    except OSError:
        pass
    if os.path.isfile(src):
        try:
            shutil.copyfile(src, dst)
        except OSError:
            pass
        if score_calls_dir:
            try:
                os.makedirs(score_calls_dir, exist_ok=True)
                shutil.copyfile(
                    src, os.path.join(score_calls_dir,
                                      "{0}.json".format(call_id)))
            except OSError:
                pass
        return
    stub = {"recorded": False,
            "reason": "no per-call token file (claude CLI failed or "
                      "RECORD_TOKENS!=1)",
            "call_id": call_id, "num_calls": 0,
            "input_tokens": 0, "output_tokens": 0,
            "cache_read_tokens": 0, "cache_write_tokens": 0}
    try:
        with open(dst, "w", encoding="utf-8") as fh:
            json.dump(stub, fh, indent=2)
    except OSError:
        pass


def _pick_union_leaf(ctx, leaf_id, member_ids, host_union_path):
    """Resolve a union unit, the merged-union counterpart of a plain
    ``ctx.leaves`` lookup.

    Validates the merge built here against the caller-prepared
    ``host_union.json`` (leaf_id, case, member_leaf_ids, bbox_dbu,
    violation_ids) and returns ``(leaf, None)``. Every member must be a real
    decompose leaf, the member set must match, and the merged violation set and
    union bbox must equal the recorded ones.

    Any drift returns ``(None, reason)`` rather than aborting: the caller
    records the reason with an empty patch and exits 0, so a single drifting
    unit cannot kill the whole iteration."""
    try:
        with open(host_union_path, "r", encoding="utf-8") as fh:
            host = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, "host_union.json unreadable ({0}): {1}".format(
            host_union_path, exc)
    if host.get("leaf_id") != leaf_id:
        return None, "host_union.json leaf_id {0} != requested {1}".format(
            host.get("leaf_id"), leaf_id)
    missing = [m for m in member_ids if m not in ctx.leaves]
    if missing:
        return None, ("union members not in container decompose: {0}; "
                      "have {1}".format(missing, sorted(ctx.leaves)))
    if sorted(member_ids) != sorted(host.get("member_leaf_ids") or []):
        return None, "union member set {0} != host {1}".format(
            sorted(member_ids), sorted(host.get("member_leaf_ids") or []))
    merged = build_union_leaf(ctx, member_ids, leaf_id)
    c_viol = sorted(merged.violations or [])
    c_bbox = list(merged.bbox_dbu)
    h_viol = sorted(host.get("violation_ids") or [])
    h_bbox = list(host.get("bbox_dbu") or [])
    if c_viol != h_viol or c_bbox != h_bbox:
        return None, ("container viol={0} bbox={1} != host viol={2} "
                      "bbox={3}".format(c_viol, c_bbox, h_viol, h_bbox))
    return merged, None


def main(argv=None):
    ap = argparse.ArgumentParser(description="EvoDRC iterative leaf runner")
    ap.add_argument("--input-layout", required=True)
    ap.add_argument("--input-drc", required=True)
    ap.add_argument("--leaf-id", required=True)
    ap.add_argument("--out-dir", required=True)
    # Required: schedule.py passes the container-local work dir holding every
    # file that must not reach the published run record.
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--call-id", required=True)
    ap.add_argument("--case-name", required=True)
    ap.add_argument("--design-type", default="block")
    ap.add_argument("--conn-path", default="")
    ap.add_argument("--rule-path", default="")
    ap.add_argument("--skill-path", default="")
    ap.add_argument("--model", required=True)
    ap.add_argument("--workspace", default="")
    ap.add_argument("--score-calls-dir", default="")
    # ---- knowledge-injection and mode flags, passed by schedule.py ---------
    ap.add_argument("--inject-main", default="",
                    help="absolute path of the staged main.md (LAYER INDEX)")
    ap.add_argument("--inject-official", default="",
                    help="absolute path of the staged skill_official.md")
    ap.add_argument("--inject-kdir", default="",
                    help="absolute path of the staged knowledge/ dir")
    ap.add_argument("--tc-dir", default="",
                    help="shared technology dir (deck + drm_jpg)")
    ap.add_argument("--ablation", default="",
                    help="'' | 1 | 2 | 3 (informational for the leaf)")
    ap.add_argument("--prompt-mode", default="exp3",
                    help="exp3 (default) | legacy")
    # ---- union unit dispatch; schedule.py passes both or neither ----------
    ap.add_argument("--union-members", default="",
                    help="comma-separated member leaf ids of a UNION unit")
    ap.add_argument("--host-union", default="",
                    help="absolute path of the answer-free "
                         "host_union.<unit>.json projection")
    args = ap.parse_args(argv)

    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    try:
        return _run_unit(args)
    finally:
        # Relocate everything the unit dir must not keep. This tidy-up must
        # never fail a leaf that repaired successfully, hence the broad catch:
        # the scheduler treats any exception escaping here as a failed run.
        try:
            _workdir.sweep_unit(out_dir, unit_work=args.work_dir)
        except Exception as exc:                      # noqa: BLE001
            sys.stderr.write("leaf {0} sweep failed: {1}\n".format(
                args.leaf_id, exc))


def _run_unit(args):
    """The unit body. Split out of main() so main() can own the sweep."""
    out_dir = args.out_dir
    work_dir = args.work_dir
    os.makedirs(os.path.join(work_dir, "_calls"), exist_ok=True)
    leaf_id = args.leaf_id
    call_id = args.call_id

    # Per-leaf token isolation: the backend records to
    # ${AGENT_CALLS_DIR}/<call_id>.json only when RECORD_TOKENS is 1, so point
    # it at this leaf's own _calls folder.
    os.environ["RECORD_TOKENS"] = "1"
    os.environ["AGENT_CALLS_DIR"] = os.path.join(work_dir, "_calls")
    os.environ["AGENT_CASE_NAME"] = args.case_name
    os.environ["AGENT_MODEL_NAME"] = args.model
    # Where hrd_split.dump_crops writes. It has to be derived from out_dir,
    # since ctx does not exist yet, and set before decompose_ctx below, which
    # is what triggers the dump. Left unset, the crops land beside the calls
    # folder instead of under ctx/.
    os.environ["EVODRC_CROPS_DIR"] = os.path.join(out_dir, "ctx", "crops")

    # ---- re-decompose + select the leaf -------------------------------------
    dec_scratch = os.path.join(work_dir, "_dec")
    try:
        os.makedirs(dec_scratch, exist_ok=True)
    except OSError:
        dec_scratch = tempfile.mkdtemp(prefix="leafdec_")
    try:
        ctx = _decompose.decompose_ctx(
            layout_path=args.input_layout,
            drc_path=args.input_drc,
            case_name=args.case_name,
            design_type=args.design_type,
            connectivity_path=args.conn_path,
            rule_path=args.rule_path,
            skill_path=args.skill_path,
            model_name=args.model,
            temp_dir=dec_scratch,
        )
    except Exception as exc:                          # noqa: BLE001
        _write_patch_json(out_dir, leaf_id, [], "decompose failed")
        _write_trace(out_dir, leaf_id, call_id, "fail", 0, "",
                     "", "decompose failed: {0}".format(exc))
        _place_tokens(call_id, args.score_calls_dir, work_dir=work_dir)
        return 0

    # Three-way unit selection. A whole-design unit and a row union unit are
    # both absent from ctx.leaves; both ends call the same shared builder, so
    # with a fixed hash seed the controller's unit and this one are identical.
    if leaf_id == WHOLE_UNIT_ID:
        leaf = build_whole_design_leaf(ctx)
    elif args.union_members:
        members = [m for m in args.union_members.split(",") if m]
        leaf, parity_err = _pick_union_leaf(ctx, leaf_id, members,
                                           args.host_union)
        if leaf is None:
            # One drifting unit must not kill the iteration: record the reason
            # and return an empty patch, which the controller's gate rejects.
            _write_patch_json(out_dir, leaf_id, [], "union parity failed")
            _write_trace(out_dir, leaf_id, call_id, "skip", 0, "",
                         "union_parity_fail:{0}".format(parity_err), None)
            _place_tokens(call_id, args.score_calls_dir, work_dir=work_dir)
            return 0
    else:
        leaf = ctx.leaves.get(leaf_id)
    if leaf is None:
        _write_patch_json(out_dir, leaf_id, [], "leaf not present this iter")
        _write_trace(out_dir, leaf_id, call_id, "skip", 0, "",
                     "leaf {0} not in this iteration's decomposition".format(
                         leaf_id), None)
        _place_tokens(call_id, args.score_calls_dir, work_dir=work_dir)
        return 0

    # The context carriers write their scratch files under ctx.temp_dir, so
    # point it at <out_dir>/ctx and they land together in the published
    # per-unit ctx/ folder, alongside the crops directed there above. Once
    # main()'s finally has swept the unit dir it holds only prompt.txt,
    # patch.json and ctx/; patch_raw.json and trace.md are written into it
    # first because the prompt names those exact paths to the model, and are
    # relocated afterwards.
    ctx_dir = os.path.join(out_dir, "ctx")
    os.makedirs(ctx_dir, exist_ok=True)
    ctx.temp_dir = ctx_dir

    patch_path = os.path.join(out_dir, "patch_raw.json")
    try:
        os.remove(patch_path)
    except OSError:
        pass

    conn_ctx_path = conn_context.write_context(ctx, leaf)
    drc_ctx_path = drc_context.write_context(ctx, leaf)
    ci_ctx_path = None
    if _ci_context is not None:
        try:
            ci_ctx_path = _ci_context.write_context(ctx, leaf)
        except Exception:                             # noqa: BLE001
            ci_ctx_path = None

    # Knowledge reaches the prompt by path, never inlined: main.md's layer
    # index names the per-layer files and the model reads only the layers its
    # own violations touch.
    if args.inject_main:
        # The legacy prompt renders its accumulated-knowledge section from this
        # path; exp3 takes its knowledge paths from the header injection.
        ctx.case_info.skill_path = args.inject_main

    trace_path = os.path.join(out_dir, "trace.md")
    if args.prompt_mode == "exp3":
        os.environ["EXP3_PROMPT"] = "1"       # prompt_format.py reads this
        inj = {"main": args.inject_main,
               "official": args.inject_official,
               "knowledge_dir": args.inject_kdir}
        whole = None
        whole_data = None
        if leaf_id == WHOLE_UNIT_ID:
            whole = _prompt_exp3.whole_header_info(
                ctx, args.input_layout, args.input_drc)
            whole_data = _prompt_exp3.build_whole_data_section(
                ctx, leaf, args.input_layout, args.input_drc)
        header = _prompt_exp3.build_header(
            leaf_id, inj, args.tc_dir, args.case_name, whole=whole)
        shared = _prompt_exp3.build_shared_target_context(ctx, leaf)
        body = build_leaf_prompt(
            leaf, ctx, patch_path=patch_path,
            conn_ctx_path=conn_ctx_path, drc_ctx_path=drc_ctx_path,
            repair_order=True, ci_ctx_path=ci_ctx_path,
            trace_path=trace_path, shared_ctx=shared, whole_data=whole_data)
        prompt_text = header + body
    else:
        os.environ.pop("EXP3_PROMPT", None)
        prompt_text = build_leaf_prompt(
            leaf, ctx, patch_path=patch_path,
            conn_ctx_path=conn_ctx_path, drc_ctx_path=drc_ctx_path,
            repair_order=True, ci_ctx_path=ci_ctx_path,
            trace_path=trace_path)
    _write(os.path.join(out_dir, "prompt.txt"), prompt_text)

    # ---- one backend call ---------------------------------------------------
    backend = (sys.modules.get("agent_backend.claude")
               or importlib.import_module("agent_backend.claude"))
    try:
        result = backend.call_agent(
            prompt_text=prompt_text, output_path=None, model=args.model,
            workspace=(args.workspace or None),
            effort=(os.environ.get("CLAUDE_EFFORT") or None),
            call_id=call_id, temp_dir=out_dir)
    except TypeError:
        result = backend.call_agent(
            prompt_text, None, args.model,
            workspace=(args.workspace or None),
            effort=(os.environ.get("CLAUDE_EFFORT") or None),
            call_id=call_id, temp_dir=out_dir)
    except Exception as exc:                          # noqa: BLE001
        result = {"status": "fail", "error": str(exc), "raw_data": None}

    status = (result or {}).get("status", "fail")
    error = (result or {}).get("error")
    raw = (result or {}).get("raw_data") or {}
    narration = ""
    if isinstance(raw, dict):
        narration = str(raw.get("result") or "")[:4000]

    # ---- parse the patch the model wrote ------------------------------------
    file_text = None
    try:
        with open(patch_path, "r", encoding="utf-8") as fh:
            file_text = fh.read()
    except (OSError, IOError):
        file_text = None

    ops = []
    explanation = ""
    if status == "success" and file_text:
        patch = parse_patch_from_file_text(file_text, leaf_id)
        if patch is not None:
            ops = list(patch.ops or [])
            explanation = patch.explanation or ""

    _write_patch_json(out_dir, leaf_id, ops, explanation)
    _write_trace(out_dir, leaf_id, call_id, status, len(ops),
                 explanation, narration, error)
    _place_tokens(call_id, args.score_calls_dir, work_dir=work_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
