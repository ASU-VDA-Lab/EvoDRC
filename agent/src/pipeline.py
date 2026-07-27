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

"""Run the repair pipeline for one case, stage by stage.

`run_pipeline(ctx)` calls all eleven stages back to back on a single case
context: parse the case, build the geometry model, calibrate, group the
violations into clips, split those into leaves, schedule and dispatch them,
mount the patches that come back, and write out the patched layout. Every
stage reads and writes the same in-memory context; nothing intermediate is
persisted to disk.
"""


import os
from typing import Optional

from .calibrate import stage_calibrate
from .clips import stage_build_clips, stage_merge_clips
from .connectivity import is_connectivity_preserved
from .dispatch import stage_dispatch
from .hrd_split import stage_hrd_split
from .logging_setup import get_logger, setup_logger, stage_extra
from .model import stage_model
from .mount import stage_mount
from .parse_case import stage_parse_case
from .pdn_prepass import stage_pdn_prepass
from .scheduler import stage_schedule
from .strap_compact import stage_strap_compact
from .types import CaseContext


class PipelineFailure(Exception):
    """Raised by a stage to abort the pipeline with a known reason."""

    def __init__(self, stage_idx: int, message: str):
        super().__init__(message)
        self.stage_idx = stage_idx
        self.message = message


def run_pipeline(ctx: CaseContext) -> None:
    """Run every stage in order on `ctx`."""
    setup_logger("INFO")
    log = get_logger()
    log.info("pipeline start case=%s",
             ctx.case_info.case_name, extra=stage_extra("S0"))

    _safe("S1", 1, log, lambda: stage_parse_case(ctx))
    _safe("S2", 2, log, lambda: stage_model(ctx))
    _safe("S3", 3, log, lambda: stage_calibrate(ctx))
    _safe("S4", 4, log, lambda: stage_build_clips(ctx))
    _safe("S4.5", 45, log, lambda: stage_pdn_prepass(ctx))
    _safe("S5", 5, log, lambda: stage_merge_clips(ctx))
    _safe("S6", 6, log, lambda: stage_hrd_split(ctx))
    _safe("S7", 7, log, lambda: stage_strap_compact(ctx))
    _safe("S8", 8, log, lambda: stage_schedule(ctx))
    _safe("S9", 9, log, lambda: stage_dispatch(ctx))
    _safe("S10", 10, log, lambda: stage_mount(ctx))
    _safe("S11", 11, log, lambda: stage_emit(ctx))

    log.info("pipeline end", extra=stage_extra("S0"))


def stage_emit(ctx: CaseContext) -> None:
    """Write the patched layout text to the configured output path.

    The text goes to a temporary file, is checked once more against the
    reference connectivity, and only then replaces the output file. A failed
    check leaves whatever is already there untouched.
    """
    log = get_logger()
    log.info("start", extra=stage_extra("S11"))
    out = ctx.case_info.output_path or ctx.output_path
    if not out:
        log.warning("no output_path; skip emit", extra=stage_extra("S11"))
        return
    text = ctx.patched_layout_text
    if text is None:
        # Nothing was patched: leave whatever already sits at the output path.
        log.info("no patched text; skip", extra=stage_extra("S11"))
        return
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    except OSError:
        pass
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    info = ctx.case_info
    if info.connectivity_path and os.path.isfile(info.connectivity_path):
        ok = is_connectivity_preserved(
            info.connectivity_path, tmp, info.design_type or "block")
        if not ok:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            log.warning("emit rejected: connectivity broken",
                        extra=stage_extra("S11"))
            return
    # Atomic swap, unlinking first so it also works on overlay filesystems.
    try:
        os.unlink(out)
    except FileNotFoundError:
        pass
    except OSError:
        pass
    try:
        os.replace(tmp, out)
    except OSError as exc:
        log.warning("os.replace failed: %s", exc, extra=stage_extra("S11"))
    log.info("end", extra=stage_extra("S11"))


def _safe(name: str, idx: int, log, fn) -> None:
    try:
        fn()
    except PipelineFailure:
        raise
    except Exception as exc:
        log.error("%s failed: %s", name, exc, extra=stage_extra(name))
        raise PipelineFailure(idx, "{0} failed: {1}".format(name, exc))
