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

"""Deterministic re-decomposition of the current block.

Runs the geometry, calibration, clipping, splitting and scheduling stages over
an explicit (layout, DRC) pair, so the controller can re-decompose the block at
the start of every iteration as repairs accumulate.

The leaf counter is reset before the stages run, so leaf ids always start at
leaf_0001 and match between the controller process and each leaf_runner
subprocess; both also pin the hash seed. The module also builds the
per-iteration leaves.json record and lists which leaves are worth repairing.
"""

import os
import tempfile
from collections import Counter

from ..types import CaseContext, CaseInfo, RuleDB
from ..calibrate import stage_calibrate
from ..clips import stage_build_clips, stage_merge_clips
from ..hrd_split import stage_hrd_split
from ..model import stage_model
from .. import model as _model
from ..scheduler import stage_schedule
from ..strap_compact import stage_strap_compact
from .. import hrd_split as _hrd


def _reset_leaf_counter():
    """Reset the module-level leaf counter so leaf ids start at leaf_0001."""
    try:
        _hrd._global_leaf_counter()[0] = 0
    except Exception:                              # noqa: BLE001
        try:
            _hrd._LEAF_COUNTER[0] = 0
        except Exception:                          # noqa: BLE001
            pass


def decompose_ctx(layout_path, drc_path, case_name, design_type,
                  connectivity_path, rule_path, skill_path, model_name,
                  temp_dir=None):
    """Run the decomposition stages over ``(layout_path, drc_path)``.

    Returns a populated CaseContext holding the geometry model, violations and
    leaves. Stage scratch goes to a fresh temp directory, and the inputs are
    left alone apart from the anchor-comment pass, which must run on a
    per-iteration copy of the layout rather than the read-only original.

    That requirement is checked up front: passing a frozen benchmark layout
    raises immediately and names the path. Copying it into scratch instead
    would return a context whose layout path points at the copy, and that path
    is written into the context files the model reads, so it would alter
    prompt-visible content while hiding the caller's mistake.
    """
    _model.assert_layout_not_frozen(layout_path, "decompose_ctx")
    _reset_leaf_counter()
    tdir = temp_dir or tempfile.mkdtemp(prefix="iterdec_")
    info = CaseInfo(
        case_name=case_name,
        design_type=design_type or "block",
        task_type="repair",
        layout_path=layout_path,
        drc_path=drc_path,
        connectivity_path=connectivity_path,
        rule_path=(rule_path if (rule_path and os.path.isfile(rule_path))
                   else ""),
        skill_path=skill_path or "",
        output_path="",
        model_name=model_name or "iter",
    )
    ctx = CaseContext(prompt_path="", output_path="", temp_dir=tdir,
                      workspace="", case_info=info, rule_db=RuleDB())
    for stg in (stage_model, stage_calibrate, stage_build_clips,
                stage_merge_clips, stage_hrd_split, stage_strap_compact,
                stage_schedule):
        stg(ctx)
    return ctx


def _block_bounds(ctx):
    geom = getattr(ctx, "geometry_model", None)
    if geom is not None and getattr(geom, "block_bounds_dbu", None):
        return list(geom.block_bounds_dbu)
    xs1 = []; ys1 = []; xs2 = []; ys2 = []
    for lf in ctx.leaves.values():
        b = list(lf.bbox_dbu)
        xs1.append(b[0]); ys1.append(b[1]); xs2.append(b[2]); ys2.append(b[3])
    if not xs1:
        return [0, 0, 0, 0]
    return [min(xs1), min(ys1), max(xs2), max(ys2)]


def leaves_json(ctx, iter_index):
    """Build the deterministic per-iteration leaves.json dict, listing every
    violation and every leaf with its bounding box and rule counts."""
    vby = {v.violation_id: v for v in ctx.violations}
    violations = []
    for v in ctx.violations:
        violations.append({
            "violation_id": v.violation_id,
            "rule_id": getattr(v, "rule_id", "?"),
            "bbox": list(v.bbox_dbu),
        })
    entries = []
    for leaf_id in sorted(ctx.leaves.keys()):
        lf = ctx.leaves[leaf_id]
        vids = list(lf.violations or [])
        rc = Counter()
        for vid in vids:
            v = vby.get(vid)
            if v is not None:
                rc[getattr(v, "rule_id", "?")] += 1
        entries.append({
            "leaf_id": leaf_id,
            "bbox_dbu": list(lf.bbox_dbu),
            "violation_ids": vids,
            "rule_counts": dict(rc),
            "n_viol": len(vids),
        })
    return {
        "iter": iter_index,
        "block_bounds_dbu": _block_bounds(ctx),
        "violations": violations,
        "leaves": entries,
        "count": len(entries),
    }


def repairable_leaf_ids(ctx):
    """Return the ids of leaves owning at least one violation, sorted
    ascending."""
    out = []
    for leaf_id in sorted(ctx.leaves.keys()):
        lf = ctx.leaves[leaf_id]
        if len(lf.violations or []) > 0:
            out.append(leaf_id)
    return out
