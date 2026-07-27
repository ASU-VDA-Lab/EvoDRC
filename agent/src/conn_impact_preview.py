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

"""Command-line lookup of which objects touch a given one electrically.

The caller names one object, a top-level polygon or a via instance, plus the
per-leaf context file. That context, written by conn_impact_context, carries
every object in the block as per-layer rings in world coordinates along with
how editable each one is, so no geometry has to be recomputed here.

The tool lists every other object that shares a layer with the named one and
overlaps it there with positive area; a via participates through the lands it
has on each layer. It takes overlapping interiors to be listed: a shared edge
or corner encloses zero area. Rings are only ever compared within the same
layer, so every result names a layer both objects occupy. The output is one
line of JSON on stdout, and the exit code is 0 whenever the lookup succeeded,
whatever it found: this reports what an edit might disturb, it decides nothing.
"""


import argparse
import json
import sys

from . import conn_impact_context


try:
    from shapely.geometry import Polygon as _SPoly
    _HAVE_SHAPELY = True
except Exception:                      # pragma: no cover - host-only path
    _SPoly = None
    _HAVE_SHAPELY = False


def _ring_to_shape(ring):
    """Turn a ring of [x, y] pairs into a valid polygon of positive area.

    Returns None when the ring is degenerate. A zero-width buffer is used to
    repair rings that touch themselves, which older shapely releases offer no
    other way to fix.
    """
    if ring is None or len(ring) < 3:
        return None
    sp = _SPoly([(float(x), float(y)) for (x, y) in ring])
    if not sp.is_valid:
        sp = sp.buffer(0)
    if sp.is_empty or sp.area <= 0:
        return None
    return sp


def _layers_overlap(a_rings, b_rings):
    """True if any ring in one list overlaps any ring in the other with
    positive area, which takes a shared interior rather than a shared edge or
    corner."""
    for a in a_rings:
        if a is None:
            continue
        for b in b_rings:
            if b is None:
                continue
            inter = a.intersection(b)
            if (not inter.is_empty) and inter.area > 0.0:
                return True
    return False


def _overlapping(object_id, objects_by_layer, kind_of, editability_by_id):
    """List the objects that overlap object_id on a layer they both occupy.

    Each overlapping object appears once, reported against the first shared
    layer on which the overlap was found, and the list is sorted by id.
    """
    src = objects_by_layer.get(object_id, {})
    results = []
    for oid in sorted(objects_by_layer):
        if oid == object_id:
            continue
        other = objects_by_layer[oid]
        hit_layer = None
        for lname in sorted(set(src) & set(other)):
            if _layers_overlap(src[lname], other[lname]):
                hit_layer = lname
                break
        if hit_layer is not None:
            results.append({"id": oid, "kind": kind_of.get(oid, "?"),
                            "layer": hit_layer,
                            "editability": editability_by_id.get(oid, "?")})
    return results


def _emit(obj, code):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()
    return code


def _error_verdict(object_id, reason):
    return {"object": object_id, "overlapping": [], "error": reason}


def _build_parser():
    p = argparse.ArgumentParser(
        prog="conn_impact_preview",
        description="List every other object that is connectivity-overlapping "
                    "the given object (same layer, positive-area polygon "
                    "overlap). LIST-only; grants no permissions.")
    p.add_argument("--object", required=True, dest="object_id",
                   help="ONE object id: a top-level polygon id (pNNN) OR a via "
                        "instance id (iNNNN).")
    p.add_argument("--context", default=None,
                   help="Per-leaf context path supplied by the harness "
                        "(falls back to env EVODRC_CONN_IMPACT_CTX).")
    return p


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    object_id = args.object_id

    if not _HAVE_SHAPELY:
        return _emit(_error_verdict(object_id, "shapely unavailable"), 2)

    # 1. Load the context, which supplies both geometry and editability.
    try:
        ctx = conn_impact_context.read_context(args.context)
    except Exception as exc:
        return _emit(_error_verdict(
            object_id, "context resolution failed: " + str(exc)), 2)

    leaf_id = ctx.get("leaf_id")
    objects = ctx.get("objects")
    case_name = ctx.get("case_name")
    if case_name:
        sys.stderr.write("conn_impact_preview: case_name=" + str(case_name)
                         + " leaf_id=" + str(leaf_id) + "\n")
    if leaf_id is None or not isinstance(objects, list):
        return _emit(_error_verdict(
            object_id, "context missing leaf_id/objects"), 2)

    # 2. Index the objects by id and turn their rings into polygons.
    objects_by_layer = {}
    kind_of = {}
    editability_by_id = {}
    for entry in objects:
        oid = entry.get("id")
        if oid is None:
            continue
        kind_of[oid] = entry.get("kind", "?")
        editability_by_id[oid] = entry.get("editability", "?")
        by_layer = {}
        for lname, rings in (entry.get("layers") or {}).items():
            shapes = []
            for r in (rings or []):
                sp = _ring_to_shape(r)
                if sp is not None:
                    shapes.append(sp)
            if shapes:
                by_layer[lname] = shapes
        objects_by_layer[oid] = by_layer

    # 3. Reject an id the context does not know about.
    if object_id not in objects_by_layer:
        return _emit(_error_verdict(
            object_id, "object id not found in context"), 2)

    # 4. Emit the list. Every overlap found is included and the step exits 0.
    overlapping = _overlapping(object_id, objects_by_layer, kind_of,
                               editability_by_id)
    return _emit({"object": object_id, "overlapping": overlapping}, 0)


if __name__ == "__main__":
    sys.exit(main())
