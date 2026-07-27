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

"""Optional gate rejecting a trial edit that increases local DRC violations.

Off by default. When enabled it renders the layout before and after the edit,
runs the rule deck over each, and counts the violations that land inside the
leaf; the edit is accepted when that count holds or falls. Only the case
input and the public rule deck are used, never the reference report, so this
measures the work rather than the score.

Unlike the connectivity gate, this one fails open: if the measurement cannot
be made, the edit is let through instead of blocked, since new violations are
already covered by the cheaper checks that run by default and this gate only
refines them. The measurement itself raises NotImplementedError, so today the
gate lets every edit through.
"""


import os
import subprocess
import tempfile
from .logging_setup import get_logger, stage_extra

log = get_logger()


def _drc_gate_enabled(ctx):
    return bool(getattr(ctx, "drc_gate", 0))


def drc_non_increasing(trial_text, prev_text, leaf, ctx):
    if not _drc_gate_enabled(ctx):
        return True
    try:
        before = _count_local_drc(prev_text, leaf, ctx)
        after = _count_local_drc(trial_text, leaf, ctx)
    except Exception:
        log.warning("drc_oracle unavailable; degrading to connectivity-only "
                    "gate (fail-OPEN)", extra=stage_extra("S10"))
        return True            # unavailable: allow rather than block
    return after <= before


def _count_local_drc(text, leaf, ctx):
    """Count the violations a layout script produces inside one leaf.

    Intended to render the text to a temporary GDS, run KLayout with the
    trimmed deck held in the context or the rule deck on disk, parse the
    report, and count the violations whose bounding box meets the leaf. Any
    failure raises, which the caller treats as the gate being unavailable.
    """
    raise NotImplementedError("L3 measured-upgrade; default-OFF")
