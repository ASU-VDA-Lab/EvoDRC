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

"""Per-block statistics derived from the block's own violations.

Later stages need a sense of how large and how entangled the violations in
this particular block are. Three things are measured over the violation set:
the spatial and layer extent of each violation, how many other violations
share a polygon with it, and how many polygons each connected cluster of
violations covers. High percentiles of those measures are stored on the
context as BlockStats, defaulting to 1 when there is nothing to measure.
"""


from typing import Dict, List, Set

from .logging_setup import get_logger, stage_extra
from .types import BlockStats, CaseContext


def stage_calibrate(ctx: CaseContext) -> None:
    log = get_logger()
    log.info("start", extra=stage_extra("S3"))

    if ctx.geometry_model is None:
        ctx.block_stats = BlockStats(safety_bound_p90=1,
                                     geom_degree_p95=1, cell_poly_p95=1)
        log.info("no geometry; defaults", extra=stage_extra("S3"))
        return

    polys = ctx.geometry_model.polygons
    violations = ctx.violations
    if not violations:
        ctx.block_stats = BlockStats(safety_bound_p90=1,
                                     geom_degree_p95=1, cell_poly_p95=1)
        log.info("no violations; defaults", extra=stage_extra("S3"))
        return

    # Extent of each violation: the largest of width, height and layer span.
    diameters: List[int] = []
    for v in violations:
        ps = [polys[pid] for pid in v.involves if pid in polys]
        if not ps:
            # No polygon resolved, so use the violation's own bounding box.
            x_min, y_min, x_max, y_max = v.bbox_dbu
            diameters.append(max(x_max - x_min, y_max - y_min, 1))
            continue
        x_min = min(p.bbox_dbu[0] for p in ps)
        y_min = min(p.bbox_dbu[1] for p in ps)
        x_max = max(p.bbox_dbu[2] for p in ps)
        y_max = max(p.bbox_dbu[3] for p in ps)
        z_min = min(p.layer_index for p in ps)
        z_max = max(p.layer_index for p in ps)
        diameters.append(max(x_max - x_min, y_max - y_min, z_max - z_min))

    # Degree of each violation in the graph where a shared polygon is an edge.
    poly_to_viols: Dict[str, Set[str]] = {}
    for v in violations:
        for pid in v.involves:
            poly_to_viols.setdefault(pid, set()).add(v.violation_id)
    degree: List[int] = []
    for v in violations:
        neigh: Set[str] = set()
        for pid in v.involves:
            neigh |= poly_to_viols.get(pid, set())
        neigh.discard(v.violation_id)
        degree.append(len(neigh))

    # Distinct polygons per connected cluster, found by walking that graph.
    viol_by_id = {v.violation_id: v for v in violations}
    seen: Set[str] = set()
    cluster_poly_counts: List[int] = []
    for v in violations:
        if v.violation_id in seen:
            continue
        stack = [v.violation_id]
        component: Set[str] = set()
        while stack:
            vid = stack.pop()
            if vid in seen:
                continue
            seen.add(vid)
            component.add(vid)
            for pid in viol_by_id[vid].involves:
                for nxt in poly_to_viols.get(pid, ()):
                    if nxt not in seen:
                        stack.append(nxt)
        polys_in_component = {pid for vid in component
                              for pid in viol_by_id[vid].involves}
        cluster_poly_counts.append(len(polys_in_component))

    ctx.block_stats = BlockStats(
        safety_bound_p90=max(1, _quantile(diameters, 0.90)),
        geom_degree_p95=max(1, _quantile(degree, 0.95)),
        cell_poly_p95=max(1, _quantile(cluster_poly_counts, 0.95)),
    )
    log.info("p90=%d deg95=%d poly95=%d",
             ctx.block_stats.safety_bound_p90,
             ctx.block_stats.geom_degree_p95,
             ctx.block_stats.cell_poly_p95,
             extra=stage_extra("S3"))


def _quantile(xs: List[int], q: float) -> int:
    if not xs:
        return 1
    xs = sorted(xs)
    k = max(0, min(len(xs) - 1, int(round(q * (len(xs) - 1)))))
    return int(xs[k])
