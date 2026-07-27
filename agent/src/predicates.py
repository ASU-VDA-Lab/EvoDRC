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

"""Tests that decide whether a violation subgraph can be repaired on its own.

A subgraph is a "natural leaf" when it is self-contained enough to hand to the
repair step directly instead of splitting it further: one connected component,
a single rule family, bounded vertex degree, bounded spatial extent and a
bounded polygon count. Bridge polygons shared between leaves are checked by a
separate clause, once ownership has been assigned. Every predicate here is
pure and reads only the graph and the calibrated per-block statistics.
"""


from typing import Optional

from .dependency_graph import Graph


MANUFACTURING_GRID_DBU = 1  # Offsets are snapped to whole database units.


def is_natural_leaf(graph: Graph, block_stats, rule_db,
                    *, check_p5e: bool = False) -> bool:
    """Return True when every leaf predicate holds for this subgraph.

    ``check_p5e`` stays False while the decomposition is still recursing,
    since bridge ownership is only assigned once recursion has terminated. A
    later enforcer pass re-checks that clause against the final set of leaves.
    """
    base_ok = (
        _p1_single_component(graph)
        and _p2_one_colorable_family_hypergraph(graph, rule_db)
        and _p3_geom_degree_ok(graph, block_stats)
        and _p5_bbox_diameter_ok(graph, block_stats)
        and _p5d_polygon_count_ok(graph, block_stats)
    )
    if not base_ok:
        return False
    if check_p5e:
        return _p5e_bridge_ownership_pure(graph)
    return True


# ---------------------------------------------------------------------------
# Individual clauses
# ---------------------------------------------------------------------------

def _p1_single_component(graph: Graph) -> bool:
    """True when a traversal from an arbitrary node reaches every other node."""
    if not graph.nodes:
        return True
    start = next(iter(graph.nodes))
    seen = set()
    stack = [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(graph.adj.get(n, ()))
    return seen == graph.nodes


def _p2_one_colorable_family_hypergraph(graph: Graph, rule_db) -> bool:
    """True when the violations in the subgraph all share one rule family."""
    families = set()
    for v in graph.violation_nodes:
        if rule_db is None:
            families.add(getattr(v, "rule_family", "") or "")
        else:
            families.add(rule_db.family_of(v.rule_id))
    return len(families) <= 1


def _p3_geom_degree_ok(graph: Graph, block_stats) -> bool:
    """True when the largest vertex degree fits the calibrated degree bound."""
    if not graph.nodes:
        return True
    max_deg = max(len(graph.adj.get(n, ())) for n in graph.nodes)
    return max_deg <= block_stats.geom_degree_p95


def _p5_bbox_diameter_ok(graph: Graph, block_stats) -> bool:
    """True when the subgraph's spatial extent stays within the safety bound.

    The extent is the largest single-axis span over x, y and layer index, not
    the Euclidean diagonal. Calibration derives ``safety_bound_p90`` with the
    same metric, so the two are directly comparable.
    """
    polys = list(graph.polygon_nodes)
    if not polys:
        return True
    x_min = min(p.bbox_dbu[0] for p in polys)
    y_min = min(p.bbox_dbu[1] for p in polys)
    x_max = max(p.bbox_dbu[2] for p in polys)
    y_max = max(p.bbox_dbu[3] for p in polys)
    z_min = min(p.layer_index for p in polys)
    z_max = max(p.layer_index for p in polys)
    diameter = max(x_max - x_min, y_max - y_min, z_max - z_min)
    return diameter <= block_stats.safety_bound_p90


def _p5d_polygon_count_ok(graph: Graph, block_stats) -> bool:
    """True when the polygon count fits both the absolute and per-violation caps."""
    n_poly = sum(1 for _ in graph.polygon_nodes)
    n_viol = max(1, sum(1 for _ in graph.violation_nodes))
    cap_abs = block_stats.cell_poly_p95
    cap_ratio = block_stats.geom_degree_p95 * n_viol
    return n_poly <= min(cap_abs, cap_ratio)


def _p5e_bridge_ownership_pure(graph: Graph) -> bool:
    """True when every polygon marked as a bridge has an owning leaf recorded."""
    for p in graph.polygon_nodes:
        if p.owner_kind != "bridge":
            continue
        if getattr(p, "bridge_owner_leaf_id", None) is None:
            return False
    return True
