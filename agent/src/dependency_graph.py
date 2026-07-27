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

"""Dependency graph over individual polygons.

Each node is one polygon, and an edge joins two polygons that appear together
in the same violation. Edges carry no weights, so adjacency is a plain set of
neighbours. A graph can be built either from raw polygon and violation lists
or from a single clip. Later stages use it to work out which polygons have to
be repaired together and where a clip can be split.
"""


from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple

from .types import Polygon, Violation


@dataclass
class Graph:
    """Undirected graph over polygons, the input to the minimum-cut search.

    Vertices are polygon id strings, and adjacency is a plain set, so every
    edge implicitly has weight 1. The Polygon and Violation objects are kept
    alongside, so callers can inspect bounding boxes, owner kinds and similar
    attributes without a second lookup table.
    """
    nodes: Set[str] = field(default_factory=set)
    adj: Dict[str, Set[str]] = field(default_factory=dict)
    polygons_by_id: Dict[str, Polygon] = field(default_factory=dict)
    violations: List[Violation] = field(default_factory=list)

    def add_node(self, polygon: Polygon) -> None:
        self.nodes.add(polygon.polygon_id)
        self.adj.setdefault(polygon.polygon_id, set())
        self.polygons_by_id[polygon.polygon_id] = polygon

    def add_edge(self, a: str, b: str) -> None:
        if a == b:
            return
        self.adj.setdefault(a, set()).add(b)
        self.adj.setdefault(b, set()).add(a)

    # convenience views used by predicates ----------------------------------

    @property
    def polygon_nodes(self) -> Iterable[Polygon]:
        for pid in self.nodes:
            poly = self.polygons_by_id.get(pid)
            if poly is not None:
                yield poly

    @property
    def violation_nodes(self) -> Iterable[Violation]:
        nodes = self.nodes
        for v in self.violations:
            if any(pid in nodes for pid in v.involves):
                yield v

    def degrees(self) -> Dict[str, int]:
        return {n: len(self.adj.get(n, ())) for n in self.nodes}


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_polygon_graph_from_pieces(polygons: List[Polygon],
                                    violations: List[Violation]) -> Graph:
    """Build a graph from raw polygon and violation lists.

    Two polygons are joined whenever at least one violation names them both.
    """
    g = Graph()
    for poly in polygons:
        g.add_node(poly)
    g.violations = list(violations)
    poly_id_set = g.nodes
    for v in violations:
        involves = [pid for pid in v.involves if pid in poly_id_set]
        for i in range(len(involves)):
            for j in range(i + 1, len(involves)):
                g.add_edge(involves[i], involves[j])
    return g


def build_polygon_graph(clip,
                        polygons_by_id: Dict[str, Polygon],
                        violations_by_id: Dict[str, Violation]) -> Graph:
    """Build the polygon graph for a single clip.

    `clip` only has to expose `polygon_ids` and `violation_ids`, so a leaf or
    a similar wrapper works just as well.
    """
    polys: List[Polygon] = []
    for pid in clip.polygon_ids:
        p = polygons_by_id.get(pid)
        if p is not None:
            polys.append(p)
    viols: List[Violation] = []
    for vid in clip.violation_ids:
        v = violations_by_id.get(vid)
        if v is not None:
            viols.append(v)
    return build_polygon_graph_from_pieces(polys, viols)
