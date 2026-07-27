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

"""End-of-iteration snapshot of every repair unit's context directory.

At the end of each iteration the context each unit was given -- crops, DRC
results, connectivity data -- is copied to

    <PERSIST_ROOT>/crop_history/iter{N}/<UNIT>/ctx/

so that evidence survives the next iteration, which re-decomposes the repaired
layout and produces different crops. Union and whole-design units sit at the
same level as plain leaves, so a single scan covers all three kinds.

The snapshot is a record rather than a result, so it is best-effort: a failure
on one unit is logged and skipped, and the caller guards the whole call so a
snapshot problem cannot discard a completed iteration.
"""

import os
import shutil

from ..logging_setup import get_logger, stage_extra


def snapshot(persist_root, iter_dir, iter_index):
    """Archive each unit's ``ctx/`` into ``crop_history/iter{N}/<UNIT>/ctx``.

    Returns the number of context directories archived, or 0 without raising
    when the iteration produced no ``leaf/`` directory, which happens when the
    controller stops early."""
    log = get_logger()
    leaf_root = os.path.join(iter_dir, "leaf")
    if not os.path.isdir(leaf_root):
        return 0
    n = 0
    try:
        unit_ids = sorted(os.listdir(leaf_root))
    except OSError as exc:
        log.warning("crop_history: cannot list %s: %r", leaf_root, exc,
                    extra=stage_extra("S0"))
        return 0
    for unit_id in unit_ids:
        src = os.path.join(leaf_root, unit_id, "ctx")
        if not os.path.isdir(src):
            continue
        dest = os.path.join(persist_root, "crop_history",
                            "iter{0}".format(iter_index), unit_id, "ctx")
        try:
            # Replace rather than merge, so a repeated iteration cannot leave
            # a stale crop from an earlier decomposition behind.
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copytree(src, dest)
            n += 1
        except OSError as exc:
            log.warning("crop_history: copy failed for %s: %r", unit_id, exc,
                        extra=stage_extra("S0"))
    log.info("crop_history: iter%d -> %d ctx dir(s) archived",
             iter_index, n, extra=stage_extra("S0"))
    return n
