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

"""Apply the accepted patches to the layout and keep the ones that hold up.

Each leaf's patch is applied on its own to a working copy of the layout script.
A patch is kept when the result still passes the block-level connectivity
check, and, when that gate is enabled, when it does not raise the local DRC
count either. The resulting text is stored on the case context and each leaf's
result records whether its patch was mounted, skipped as a no-op, or rejected.
"""


import os
import tempfile

from .connectivity import is_connectivity_preserved
from .logging_setup import get_logger, stage_extra
from .patch_apply import apply_patch_to_text
from .types import CaseContext


def _connectivity_ok(text, tmp_dir, info):
    """Write the text to a temporary script and run the connectivity check.

    Returns True when connectivity is preserved, and also when no reference
    connectivity file is configured, so a missing reference blocks nothing."""
    if not info.connectivity_path or not os.path.isfile(info.connectivity_path):
        return True
    fd, path = tempfile.mkstemp(prefix="src_inc_", suffix=".py",
                                dir=tmp_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        return is_connectivity_preserved(
            info.connectivity_path, path, info.design_type or "block")
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def stage_mount(ctx: CaseContext) -> None:
    """Mount the leaf patches one at a time, keeping only those that hold.

    The per-leaf validator only sees its own leaf and cannot judge interactions
    between nets, so patches are tried individually: applying them all at once
    and rolling everything back on a single failure threw away the good repairs
    along with the bad one. Leaves are tried in wave order, then by descending
    conflict degree, then by id.

    Side effects on ``ctx.leaf_results``:
      - an accepted patch keeps ``status == "mounted"``.
      - a patch that breaks block-level connectivity becomes
        ``status == "mount_rejected_connectivity"`` with ``error`` set.
      - a patch that raises the local DRC count, when that gate is on,
        becomes ``status == "mount_rejected_drc"``.
      - a patch that changes nothing becomes
        ``status == "mount_skipped_noop"``.
    """
    log = get_logger()
    log.info("start", extra=stage_extra("S10"))
    info = ctx.case_info
    if not info.layout_path or not os.path.isfile(info.layout_path):
        ctx.mount_rejected_reason = "no_layout"
        return

    tmp_dir = ctx.temp_dir or tempfile.gettempdir()
    try:
        os.makedirs(tmp_dir, exist_ok=True)
    except OSError:
        tmp_dir = tempfile.gettempdir()

    with open(info.layout_path, encoding="utf-8") as fh:
        layout_text = fh.read()

    # The unmodified layout must pass connectivity; if it does not, stop here.
    if not _connectivity_ok(layout_text, tmp_dir, info):
        ctx.patched_layout_text = layout_text
        ctx.mount_rejected_reason = "original_layout_already_broken"
        log.warning("original layout fails connectivity; aborting mount",
                    extra=stage_extra("S10"))
        return

    accepted = 0
    no_op = 0
    rejected = 0
    def _d6_key(lid):
        return (ctx.leaf_wave.get(lid, 0),
                -ctx.leaf_conflict_degree.get(lid, 0),
                lid)
    candidate_lids = [lid for lid in sorted(ctx.leaf_results.keys(), key=_d6_key)
                      if ctx.leaf_results[lid].status == "mounted"
                      and ctx.leaf_results[lid].patch is not None]
    log.info("incremental mount over %d candidate leaves",
             len(candidate_lids), extra=stage_extra("S10"))

    for lid in candidate_lids:
        res = ctx.leaf_results[lid]
        leaf = ctx.leaves.get(lid)
        if leaf is None:
            continue
        trial = apply_patch_to_text(layout_text, res.patch, leaf)
        if trial == layout_text:
            res.status = "mount_skipped_noop"
            res.error = "apply_patch_to_text produced no diff"
            no_op += 1
            log.info("leaf %s skipped (no-op)", lid, extra=stage_extra("S10"))
            continue
        if _connectivity_ok(trial, tmp_dir, info):
            # Optional extra gate, off by default: reject a patch that raises
            # the local DRC count. The oracle fails open, letting the patch
            # through whenever it cannot decide, which is the opposite of the
            # connectivity check above.
            if ctx.drc_gate:
                from . import drc_oracle
                if not drc_oracle.drc_non_increasing(trial, layout_text, leaf, ctx):
                    res.status = "mount_rejected_drc"
                    res.error = "patch increased local DRC count"
                    rejected += 1
                    continue
            layout_text = trial
            accepted += 1
            log.info("leaf %s mounted (ok=%d/rej=%d/noop=%d)",
                     lid, accepted, rejected, no_op,
                     extra=stage_extra("S10"))
        else:
            res.status = "mount_rejected_connectivity"
            res.error = "patch broke block-level connectivity"
            rejected += 1
            log.info("leaf %s rejected (connectivity broken)",
                     lid, extra=stage_extra("S10"))

    ctx.patched_layout_text = layout_text
    _assert_context_integrity(ctx, layout_text)
    log.info("end accepted=%d rejected=%d no_op=%d",
             accepted, rejected, no_op, extra=stage_extra("S10"))
    if accepted == 0 and (rejected > 0 or no_op > 0):
        ctx.mount_rejected_reason = (
            "all_patches_rejected_or_noop:acc=0 rej={0} noop={1}"
            .format(rejected, no_op))


def _assert_context_integrity(ctx, final_text):
    """Warn if the mount changed something it was never allowed to change.

    Compares the set of standard-cell instances in the final text against the
    original file and logs a warning on any difference. The mounted text stands
    either way: this checks an invariant that should already hold."""
    log = get_logger()
    info = ctx.case_info
    try:
        with open(info.layout_path, encoding="utf-8") as fh:
            original = fh.read()
    except OSError:
        return
    # The set of standard-cell instance inserts must be unchanged.
    import re as _re
    def _stdcell_inserts(text):
        out = []
        for m in _re.finditer(
                r"insert\(\s*pya\.CellInstArray\(\s*cell_([A-Za-z0-9_]*_ASAP7_[A-Za-z0-9_]*)\.",
                text):
            out.append(m.group(1))
        return sorted(out)
    if _stdcell_inserts(original) != _stdcell_inserts(final_text):
        log.warning("mount_context_corruption: std-cell instance set changed",
                    extra=stage_extra("S10"))
