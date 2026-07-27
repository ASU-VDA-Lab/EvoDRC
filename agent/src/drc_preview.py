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

"""Command-line DRC preview for one candidate set of edits.

The caller passes a candidate ``{"ops": [...]}`` and the per-leaf context file
prepared for it; the leaf comes from the context, not the candidate. This tool
re-runs the deterministic decomposition of the case, selects that leaf, applies
the ops to a deep copy of the geometry model, and runs the crop DRC on the
result.

It prints a single line of JSON saying which of the leaf's target violations
cleared, which remain, and whether new ones appeared inside the window;
KLayout's own report reaches the caller only through those fields. The exit
code is 0 when every target cleared, 1 when some remain, and 2 on an error.
"""


import argparse
import copy
import json
import os
import sys
import tempfile
from collections import Counter

from . import drc_check
from . import drc_context


# ---------------------------------------------------------------------------
# Decomposition
# ---------------------------------------------------------------------------
def _decompose(case_name, design_type, layout_path, rule_path,
               drc_path="", connectivity_path=""):
    """Run the decomposition pipeline for a case and return its context.

    The global leaf counter is reset first, so the leaf ids produced here match
    the ones the production run assigned.

    drc_path must point at the reference DRC report. Its violations are what
    seeds ctx.violations, and the split stage bisects those into leaves, so an
    empty drc_path yields no violations, no leaves, and no way to find the leaf
    the caller asked for.
    """
    from .calibrate import stage_calibrate
    from .clips import stage_build_clips, stage_merge_clips
    from .hrd_split import stage_hrd_split
    from .model import stage_model
    from .scheduler import stage_schedule
    from .strap_compact import stage_strap_compact
    from .types import CaseContext, CaseInfo, RuleDB
    from . import hrd_split as _hrd
    try:
        _hrd._global_leaf_counter()[0] = 0
    except Exception:
        try:
            _hrd._LEAF_COUNTER[0] = 0
        except Exception:
            pass
    tdir = tempfile.mkdtemp(prefix="drcprev_dec_")
    info = CaseInfo(case_name=case_name, design_type=design_type,
                    task_type="repair", layout_path=layout_path,
                    drc_path=(drc_path or ""),
                    connectivity_path=(connectivity_path or ""),
                    rule_path=(rule_path if rule_path and os.path.isfile(rule_path)
                               else ""),
                    skill_path="", output_path="", model_name="drc-preview")
    ctx = CaseContext(prompt_path="", output_path="", temp_dir=tdir,
                      workspace="", case_info=info, rule_db=RuleDB())
    for stg in (stage_model, stage_calibrate, stage_build_clips,
                stage_merge_clips, stage_hrd_split, stage_strap_compact,
                stage_schedule):
        stg(ctx)
    return ctx


def _leaf_targets(leaf, ctx):
    """Return the leaf's target violations as [(rule_id, (x1,y1,x2,y2)), ...]."""
    vby = {v.violation_id: v for v in ctx.violations}
    out = []
    for vid in leaf.violations:
        v = vby.get(vid)
        if v is None:
            continue
        out.append((getattr(v, "rule_id", "?"), tuple(v.bbox_dbu)))
    return out


# ---------------------------------------------------------------------------
# Candidate op application
# ---------------------------------------------------------------------------
def _apply_ops_to_geom(ctx, leaf, ops):
    from .validator import (_apply_resize_bbox, _apply_move_bbox,
                            _apply_resize_end_bbox)
    polys = ctx.geometry_model.polygons
    insts = ctx.geometry_model.instances

    def _bbox_pts(bb):
        x1, y1, x2, y2 = bb
        return ((x1, y1), (x1, y2), (x2, y2), (x2, y1))

    for op in ops:
        k = op.get("op")
        if k in ("resize", "move", "resize_end"):
            pid = op.get("polygon_id")
            p = polys.get(pid)
            if p is None:
                continue
            axis = op.get("axis", "x")
            dd = op.get("delta_dbu", 0)
            if k == "resize":
                nb = _apply_resize_bbox(p.bbox_dbu, axis, dd)
            elif k == "move":
                nb = _apply_move_bbox(p.bbox_dbu, axis, dd)
            else:
                nb = _apply_resize_end_bbox(p.bbox_dbu, axis,
                                            op.get("end", "low"), dd)
            p.bbox_dbu = nb
            p.points_dbu = _bbox_pts(nb)
        elif k == "delete":
            polys.pop(op.get("polygon_id"), None)
        elif k == "move_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            inst = insts.get(iid)
            if inst is None:
                continue
            delta = op.get("delta_dbu", [0, 0])
            try:
                dx, dy = delta
            except (TypeError, ValueError):
                dx, dy = 0, 0
            inst.origin_dbu = (inst.origin_dbu[0] + int(dx),
                               inst.origin_dbu[1] + int(dy))
        elif k == "delete_instance":
            iid = op.get("inst_id") or op.get("instance_id")
            insts.pop(iid, None)
            if iid in leaf.subcell_instances:
                leaf.subcell_instances.remove(iid)
        elif k == "add_via":
            # Register one new instance of a via definition that already exists
            # in the design. The crop render flattens every instance listed on
            # the leaf, so the new via is measured without further bookkeeping.
            from .subcell_protection import allowed_ops_for
            from .types import SubcellInstance
            cn = op.get("cell_name")
            cdef = ctx.geometry_model.cell_defs.get(cn)
            if cdef is None or cdef.kind != "via":
                continue                     # only via defs can be added
            org = op.get("origin_dbu") or [op.get("x"), op.get("y")]
            try:
                ox, oy = int(org[0]), int(org[1])
            except (TypeError, ValueError, IndexError):
                continue
            seq = 0
            while ("iprev_add_%d" % seq) in insts:
                seq += 1
            iid = "iprev_add_%d" % seq
            insts[iid] = SubcellInstance(
                instance_id=iid, cell_name=cn, kind="via",
                allowed_ops=allowed_ops_for("via"), origin_dbu=(ox, oy),
                rot_code=0, mirror=False)
            if iid not in leaf.subcell_instances:
                leaf.subcell_instances.append(iid)
        elif k in ("resize_via_shape", "move_via_shape"):
            # Edit the shape inside the shared via cell definition, so every
            # instance of that via type re-renders. The flattening helper is
            # memoized on the shape tuple, so replacing it drops the old cache
            # entry by itself.
            from .patch_apply import (_resize_points, _move_points,
                                      _LAYER_NAME_TO_NUM)
            from .crop_body import _layer_name_for_gds
            # Via-shape ops are legal only on via definitions; standard-cell
            # definitions cannot be edited, and the preview must not promise an
            # effect the real apply step would refuse.
            if not str(op.get("cell_name") or "").startswith("VIA_"):
                continue
            cdef = ctx.geometry_model.cell_defs.get(op.get("cell_name"))
            if cdef is None:
                continue
            lname = op.get("layer_name")
            # The real apply step resolves via layers through the same table,
            # which covers M1..M9 and V1..V9 but not V0, so a V0 via op does
            # nothing there. Skip it here as well.
            if _LAYER_NAME_TO_NUM.get(lname) is None:
                continue
            try:
                si = int(op.get("shape_index", 0) or 0)
            except (TypeError, ValueError):
                si = 0
            occ = -1
            target = None
            for idx, sh in enumerate(cdef.shapes):
                if _layer_name_for_gds(sh[0]) == lname:
                    occ += 1
                    if occ == si:
                        target = idx
                        break
            if target is None:
                continue
            lyr, pts, cut = cdef.shapes[target]
            axis = op.get("axis", "x")
            dd = int(op.get("delta_dbu", 0) or 0)
            if k == "resize_via_shape":
                new_pts = _resize_points(list(pts), axis, dd)
            else:
                new_pts = _move_points(list(pts), axis, dd)
            cdef.shapes[target] = (
                lyr, tuple((int(x), int(y)) for (x, y) in new_pts), cut)


# ---------------------------------------------------------------------------
# Verdict construction
# ---------------------------------------------------------------------------
def _make_verdict(leaf_id, n_ops, tgt_list, crop_ms):
    """Compare the leaf's targets against the violations the crop DRC found.

    A target counts as cleared when the crop no longer reports it at least as
    often as before; anything the crop reports beyond the targets is new.
    """
    target_ms = Counter(tgt_list)
    cleared, remaining = [], []
    for kk, cnt in target_ms.items():
        present = crop_ms.get(kk, 0) >= cnt
        (remaining if present else cleared).append(
            {"rule_id": kk[0], "bbox": list(kk[1])})
    new = []
    for kk, cnt in crop_ms.items():
        extra = cnt - target_ms.get(kk, 0)
        for _ in range(max(0, extra)):
            new.append({"rule_id": kk[0], "bbox": list(kk[1])})
    return {
        "leaf_id": leaf_id,
        "n_ops": n_ops,
        "targets_total": len(tgt_list),
        "cleared": cleared,
        "remaining": remaining,
        "new_in_window": new,
        "all_targets_cleared": len(cleared) == len(tgt_list),
        "introduced_new": len(new) > 0,
    }


def _error_verdict(reason):
    return {"verdict": None, "error": reason,
            "cleared": [], "remaining": [], "new_in_window": []}


def _exit_code(verdict):
    if verdict.get("verdict", "ok") is None or "error" in verdict:
        return 2
    return 0 if verdict.get("all_targets_cleared") else 1


def _emit(verdict):
    sys.stdout.write(json.dumps(verdict) + "\n")
    sys.stdout.flush()
    return _exit_code(verdict)


def _build_parser():
    p = argparse.ArgumentParser(
        prog="drc_preview",
        description="Apply candidate ops to this leaf's crop, run faithful "
                    "KLayout DRC, and report which target violations clear / "
                    "remain and whether new in-window ones appear.")
    p.add_argument("--candidate", required=True,
                   help="JSON file holding {\"ops\":[...]} (leaf_id OPTIONAL "
                        "and never required).")
    p.add_argument("--context", default=None,
                   help="Per-leaf context path supplied by the harness "
                        "(falls back to env EVODRC_DRC_CTX).")
    return p


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    # 1. Resolve the context file: case, layout, rule deck, and the leaf id.
    try:
        ctxinfo = drc_context.read_context(args.context)
    except Exception as exc:
        return _emit(_error_verdict("context resolution failed: " + str(exc)))

    case_name = ctxinfo.get("case_name") or "case"
    design_type = ctxinfo.get("design_type") or "block"
    layout_path = ctxinfo.get("layout_path")
    rule_path = ctxinfo.get("rule_path")
    drc_path = ctxinfo.get("drc_path") or ""
    connectivity_path = ctxinfo.get("connectivity_path") or ""
    ctx_leaf_id = ctxinfo.get("leaf_id")
    sys.stderr.write("drc_preview: case_name=" + str(case_name)
                     + " leaf_id=" + str(ctx_leaf_id)
                     + " drc_path=" + str(drc_path) + "\n")
    if not layout_path or not ctx_leaf_id:
        return _emit(_error_verdict("context missing layout_path/leaf_id"))
    if not drc_path:
        # Without the reference DRC report the decomposition produces no leaves
        # at all, so report the missing path rather than the confusing
        # "leaf not found" that would follow.
        return _emit(_error_verdict(
            "context missing drc_path (golden DRC report); cannot decompose"))

    # 2. Load the candidate. Only its ops are used; any leaf_id is ignored.
    try:
        with open(args.candidate, "r", encoding="utf-8") as fh:
            cand = json.load(fh)
    except Exception as exc:
        return _emit(_error_verdict("candidate unreadable/malformed: "
                                    + str(exc)))
    if not isinstance(cand, dict):
        return _emit(_error_verdict("candidate JSON is not an object"))
    cand_leaf = cand.get("leaf_id")
    if cand_leaf is not None and cand_leaf != ctx_leaf_id:
        sys.stderr.write(
            "drc_preview: candidate leaf_id %r ignored; using context "
            "leaf_id %r\n" % (cand_leaf, ctx_leaf_id))
    ops = cand.get("ops", [])
    if not isinstance(ops, list):
        return _emit(_error_verdict("candidate 'ops' is not a list"))

    # 3. Decompose the case and select the leaf. The report paths determine
    #    which violations, and therefore which leaves, exist.
    try:
        base_ctx = _decompose(case_name, design_type, layout_path, rule_path,
                              drc_path=drc_path,
                              connectivity_path=connectivity_path)
    except Exception as exc:
        return _emit(_error_verdict("decomposition failed: " + str(exc)))
    if ctx_leaf_id not in base_ctx.leaves \
            and ctxinfo.get("whole_design"):
        # The whole-design leaf id is reserved and never comes out of a fresh
        # decomposition, so rebuild it here. The single-leaf path below then
        # runs unchanged, with the window covering the whole block.
        try:
            from .hrd_split import build_whole_design_leaf
            base_ctx.leaves[ctx_leaf_id] = build_whole_design_leaf(
                base_ctx, ctx_leaf_id)
        except Exception as exc:
            return _emit(_error_verdict(
                "whole-design reconstruction failed: " + str(exc)))
    if ctx_leaf_id not in base_ctx.leaves:
        # A merged-union leaf id is synthetic and likewise never comes out of a
        # fresh decomposition. When the context names the leaves it was built
        # from, rebuild the same merged leaf and register it under that id, so
        # the single-leaf path below runs on the correct merged window.
        union_members = ctxinfo.get("union_members") or []
        if not union_members:
            return _emit(_error_verdict(
                "leaf %r not found after decomposition" % ctx_leaf_id))
        missing = [m for m in union_members if m not in base_ctx.leaves]
        if missing:
            return _emit(_error_verdict(
                "union member(s) %r not found after decomposition"
                % (missing,)))
        try:
            from .hrd_split import build_union_leaf
            base_ctx.leaves[ctx_leaf_id] = build_union_leaf(
                base_ctx, union_members, ctx_leaf_id)
        except Exception as exc:
            return _emit(_error_verdict(
                "union reconstruction failed: " + str(exc)))

    # 4. Work on a deep copy so the ops cannot disturb the decomposed context.
    work_ctx = copy.deepcopy(base_ctx)
    leaf = work_ctx.leaves[ctx_leaf_id]
    tgt_list = _leaf_targets(leaf, work_ctx)

    # 5. An empty candidate is a request for the baseline: DRC the crop as it
    #    stands, with nothing applied.
    if not ops:
        try:
            crop_ms = drc_check.run_faithful_crop_drc(leaf, work_ctx)
        except Exception as exc:
            return _emit(_error_verdict("baseline crop DRC failed: "
                                        + str(exc)))
        return _emit(_make_verdict(ctx_leaf_id, 0, tgt_list, crop_ms))

    # 6. Apply the ops to the copied geometry, then re-render and re-check.
    try:
        _apply_ops_to_geom(work_ctx, leaf, ops)
    except Exception as exc:
        return _emit(_error_verdict("apply ops failed: " + str(exc)))
    try:
        crop_ms = drc_check.run_faithful_crop_drc(leaf, work_ctx)
    except Exception as exc:
        return _emit(_error_verdict("crop DRC failed: " + str(exc)))

    # 7. Compare what is left against the targets.
    return _emit(_make_verdict(ctx_leaf_id, len(ops), tgt_list, crop_ms))


if __name__ == "__main__":
    sys.exit(main())
