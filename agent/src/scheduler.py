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

"""Group the leaves into waves that can be repaired in parallel.

Two leaves conflict when they share a polygon, either a bridge polygon or an
editable one, because repairing both at once would mean two edits to the same
line of the layout source. The leaves are coloured greedily in descending order
of conflict degree, and each colour becomes one wave, so the leaves inside a
wave share no polygon and can be dispatched together.
"""


from typing import Dict, List

from .logging_setup import get_logger, stage_extra
from .types import CaseContext, Leaf


def assert_editable_disjoint(leaves: List[Leaf]) -> None:
    """Check that no power crop shares an editable polygon with another leaf.

    A power crop repairs a whole power net as one unit, so every polygon it may
    edit -- the straps and their rails -- has to belong to it alone. Power crops
    may overlap other leaves in bbox, but never in the set of polygons they
    edit, and this raises AssertionError when they do.

    Two ordinary leaves sharing an editable polygon is fine and happens when a
    long top-level polygon spans two crops. The conflict edges built below put
    such leaves in different waves, so they are never dispatched together.
    """
    owner_of: Dict[str, tuple] = {}        # pid -> (leaf_id, owner_is_power)
    for leaf in leaves:
        lp = bool(getattr(leaf, "is_pdn", False))
        for pid in leaf.editable_polygons:
            prev = owner_of.get(pid)
            if prev is not None and prev[0] != leaf.leaf_id:
                if lp or prev[1]:
                    raise AssertionError(
                        "PDN editable polygon %s shared by leaves %s and %s "
                        "(parallel-unsafe)" % (pid, prev[0], leaf.leaf_id))
                continue                   # both ordinary: the waves separate them
            owner_of[pid] = (leaf.leaf_id, lp or (prev[1] if prev else False))


def stage_schedule(ctx: CaseContext) -> None:
    log = get_logger()
    log.info("start", extra=stage_extra("S8"))
    leaves: List[Leaf] = [L for L in ctx.leaves.values()
                          if getattr(L, "skip_status", None) is None]
    if not leaves:
        ctx.waves = []
        log.info("no leaves", extra=stage_extra("S8"))
        return

    # Checked here so a broken ownership rule surfaces while the case is being
    # decomposed rather than silently during repair. It holds by construction:
    # a bridge polygon has one owner, and power-net polygons are kept out of
    # every leaf but their own.
    assert_editable_disjoint(leaves)

    # Build conflict graph keyed by leaf_id.
    bridge_owners: Dict[str, List[str]] = {}
    for leaf in leaves:
        for pid in leaf.bridge_polygons:
            bridge_owners.setdefault(pid, []).append(leaf.leaf_id)
        # Only bridge polygons are counted: read-only context shapes cannot be
        # edited by anyone, so they cannot be raced on.
    # Edges from shared editable polygons. Power leaves carry no bridges, so
    # without these they would never conflict with anything. When ownership is
    # right the editable sets are disjoint and this adds no edges at all; if two
    # leaves do share one, they can no longer land in the same wave.
    editable_owners: Dict[str, List[str]] = {}
    for leaf in leaves:
        for pid in leaf.editable_polygons:
            editable_owners.setdefault(pid, []).append(leaf.leaf_id)
    conflict: Dict[str, set] = {leaf.leaf_id: set() for leaf in leaves}
    for owners in list(bridge_owners.values()) + list(editable_owners.values()):
        for i in range(len(owners)):
            for j in range(i + 1, len(owners)):
                conflict[owners[i]].add(owners[j])
                conflict[owners[j]].add(owners[i])

    # Welsh-Powell: sort by descending degree, then greedy colour.
    ordered = sorted(leaves, key=lambda L: (-len(conflict[L.leaf_id]),
                                            L.leaf_id))
    colour_of: Dict[str, int] = {}
    for leaf in ordered:
        used = {colour_of[c] for c in conflict[leaf.leaf_id]
                if c in colour_of}
        colour = 0
        while colour in used:
            colour += 1
        colour_of[leaf.leaf_id] = colour

    # Stash each leaf's wave index and conflict degree; the mount stage orders
    # its candidates by them.
    ctx.leaf_wave = dict(colour_of)
    ctx.leaf_conflict_degree = {lid: len(conflict.get(lid, ()))
                                for lid in colour_of}

    max_colour = max(colour_of.values()) if colour_of else 0
    waves: List[List[str]] = [[] for _ in range(max_colour + 1)]
    for leaf_id in sorted(colour_of.keys()):
        waves[colour_of[leaf_id]].append(leaf_id)
    ctx.waves = [w for w in waves if w]
    log.info("end waves=%d", len(ctx.waves), extra=stage_extra("S8"))
