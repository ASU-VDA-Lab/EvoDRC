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

"""Two-pass ownership enforcement for polygons and instances shared by leaves.

A polygon that ends up in more than one leaf is a bridge, and an instance can
likewise be referenced by several leaves. Both need exactly one owner before
the leaves can be repaired in parallel. Called once from the split stage after
the recursion has finished. The first pass scans the leaves in leaf id order
and records the first leaf that references each shared object as its owner; the
second pass rewrites each leaf's polygon channels, or fills in its owned
instance list, from that record.
"""


from typing import Dict, List

from .model import is_pdn_editable_pid
from .types import Leaf, Polygon


def enforce_bridge_ownership(leaves: List[Leaf],
                             polygons_by_id: Dict[str, Polygon]) -> List[Leaf]:
    """Give every bridge polygon a single owning leaf.

    ``polygons_by_id`` is the master polygon dict from ``ctx.geometry_model``.
    Polygons are mutated in place to set ``bridge_owner_leaf_id``, so the
    ownership predicate still holds when the graph is rebuilt from scratch.
    """
    # Pass 1: record an owner for each bridge, in deterministic order.
    bridge_owner_dict: Dict[str, str] = {}
    for leaf in sorted(leaves, key=lambda L: L.leaf_id):
        for pid in (list(leaf.editable_polygons) + list(leaf.bridge_polygons)):
            poly = polygons_by_id.get(pid)
            if poly is None or poly.owner_kind != "bridge":
                continue
            if pid not in bridge_owner_dict:
                bridge_owner_dict[pid] = leaf.leaf_id

    # Pass 2: re-sort each leaf's polygons into the right channel.
    for leaf in leaves:
        owned_polys = list(dict.fromkeys(
            list(leaf.editable_polygons) + list(leaf.bridge_polygons)
            + list(leaf.context_readonly)))
        new_editable: List[str] = []
        new_context: List[str] = []
        new_bridge: List[str] = []
        for pid in owned_polys:
            poly = polygons_by_id.get(pid)
            if poly is None:
                # unknown polygon: drop silently
                continue
            if poly.owner_kind == "subcell_via" \
                    or poly.owner_kind == "subcell_stdcell":
                # Subcell polygons never appear in editable lists.
                new_context.append(pid)
                continue
            if is_pdn_editable_pid(pid):
                # A PDN power-net polygon is editable only in its own power
                # crop, which is spliced in later. In every other leaf, whether
                # it arrived as a plain editable polygon or as a cross-leaf
                # bridge, it stays view-only context, so no power polygon is
                # ever co-owned by a non-power leaf.
                new_context.append(pid)
                continue
            if poly.owner_kind != "bridge":
                # Plain editable polygon.
                new_editable.append(pid)
                continue
            # Bridge polygon. Membership here is provisional:
            # longstripe.classify, re-run on every merged or relocated bbox, is
            # the final router. It keeps a bridge partially editable -- a
            # resize_end on the in-crop open end only -- when this crop contains
            # at least one real end of the wire, and demotes every crop without
            # an in-crop end to read-only context. A bridge is therefore never
            # fully editable outside an open-end crop. bridge_owner_leaf_id is
            # still stamped in pass 1 so a single deterministic owner is
            # recorded for logging and the ownership predicate, while classify
            # alone decides editability.
            owner = bridge_owner_dict.get(pid)
            if poly.bridge_owner_leaf_id is None and owner is not None:
                poly.bridge_owner_leaf_id = owner
            new_bridge.append(pid)
            new_editable.append(pid)
        leaf.editable_polygons = new_editable
        leaf.bridge_polygons = new_bridge
        leaf.context_readonly = new_context
    return leaves


def assign_instance_owners(leaves, instances_by_id, exclude_iids=()):
    """Give every shared mobile instance a single owning leaf.

    An instance with a non-empty ``allowed_ops`` is owned by the first leaf, in
    leaf id order, that references it, and each leaf's ``owned_instances`` is
    set to its share. Frozen instances are skipped, since they are read-only
    context in any case. This mirrors the bridge two-pass, and the only field
    it writes is each leaf's ``owned_instances``.

    ``exclude_iids`` names instances a regular leaf must never own because a
    later stage assigns them a dedicated owner. The PDN power crops are spliced
    in after this pass already carrying their net's power vias as owned
    instances. Those same power vias are also referenced as read-only context by
    nearby regular leaves, so without this exclusion a power via would end up
    owned by both, and single ownership would be broken. Excluding them here
    hands each power via cleanly to its PDN leaf; it still renders as view-only
    background in the regular crop, since it stays in that leaf's
    subcell_instances while ownership rests with the PDN leaf alone.
    """
    exclude = set(exclude_iids or ())
    owner_of = {}
    for leaf in sorted(leaves, key=lambda L: L.leaf_id):
        for iid in leaf.subcell_instances:
            if iid in exclude:
                continue
            inst = instances_by_id.get(iid)
            if inst is None or not inst.allowed_ops:
                continue
            if iid not in owner_of:
                owner_of[iid] = leaf.leaf_id
    for leaf in leaves:
        owned = []
        for iid in leaf.subcell_instances:
            if owner_of.get(iid) == leaf.leaf_id:
                owned.append(iid)
        leaf.owned_instances = tuple(owned)
    return leaves
