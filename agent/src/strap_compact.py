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

"""Detection of power-strap patterns in a leaf's geometry.

A leaf whose editable geometry contains a run of axis-aligned polygons that
share a metal layer, an orientation and a width is very likely part of a power
strap. This stage walks every leaf in the context and, where it finds such a
run, stamps a short descriptor of the layer, orientation and width onto
``leaf.strap_class``. The stage is an annotation only: the leaf is still handed
to a repair agent in full, with the descriptor as extra context.
"""


from collections import Counter
from typing import Dict, List, Optional

from .logging_setup import get_logger, stage_extra
from .types import CaseContext, Leaf, Polygon


def stage_strap_compact(ctx: CaseContext) -> None:
    log = get_logger()
    log.info("start", extra=stage_extra("S7"))
    if not ctx.leaves:
        log.info("no leaves", extra=stage_extra("S7"))
        return
    polys = ctx.geometry_model.polygons if ctx.geometry_model else {}
    annotated = 0
    for leaf in ctx.leaves.values():
        sclass = _classify_strap(leaf, polys)
        if sclass is not None:
            leaf.strap_class = sclass
            annotated += 1
    log.info("end annotated=%d", annotated, extra=stage_extra("S7"))


def _classify_strap(leaf: Leaf, polys: Dict[str, Polygon]) -> Optional[str]:
    """Return a strap descriptor when at least four of the leaf's polygons share
    a layer, an orientation and a width, otherwise None."""
    pids = list(leaf.editable_polygons) + list(leaf.bridge_polygons)
    sigs: Counter = Counter()
    for pid in pids:
        poly = polys.get(pid)
        if poly is None:
            continue
        w = poly.bbox_dbu[2] - poly.bbox_dbu[0]
        h = poly.bbox_dbu[3] - poly.bbox_dbu[1]
        if w == 0 or h == 0:
            continue
        if w > h:
            sigs[(poly.layer_name, "horizontal", h)] += 1
        else:
            sigs[(poly.layer_name, "vertical", w)] += 1
    if not sigs:
        return None
    (key, count) = max(sigs.items(), key=lambda kv: kv[1])
    if count >= 4:
        layer, axis, width = key
        return "{0}_{1}_w{2}".format(layer, axis, width)
    return None
