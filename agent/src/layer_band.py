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

"""Layer-band membership for a DRC rule or a leaf.

A rule names one or more metal and via layers. The band around those layers
decides what a repair agent may edit and what it may only look at: layers
within two steps of a named layer are editable, layers three steps away are
background, and V0 is never editable because it is the device floor. This
module holds its own interleaved stack order including V0, rather than reusing
the map in ``types``, and is the single place band membership is decided.
"""


import re
from typing import List, Set, Tuple


# Interleaved electrical stack, with V0 as the lowest entry.
_BAND_ORDER = ("V0", "M1", "V1", "M2", "V2", "M3", "V3", "M4", "V4", "M5",
               "V5", "M6", "V6", "M7", "V7", "M8", "V8", "M9", "V9")
_BAND_IDX = dict((n, i) for i, n in enumerate(_BAND_ORDER))
_RE_LAYER_TOK = re.compile(r"^[MV]\d$")


def layers_of_rule(rule_id):
    """Return the layer names a rule id mentions.

    The dotted rule id is split into tokens and the ones matching ``M<d>`` or
    ``V<d>`` are kept, in order and without duplicates."""
    out = []
    for tok in str(rule_id or "").split("."):
        if _RE_LAYER_TOK.match(tok) and tok not in out:
            out.append(tok)
    return out


def band_for_layers(nset):
    """Expand a set of layer names into an editable band and a background band.

    Editable covers the named layers and everything within two steps of them in
    the stack; background is what sits exactly three steps away, minus the
    editable band. V0 is removed from editable, since it is the electrical
    floor, but may still appear in background. Editable wins over background,
    because background has editable subtracted from it only after every named
    layer has been expanded. Returns (editable_set, background_set) of names.
    """
    editable = set()
    background = set()
    for n in nset:
        i = _BAND_IDX.get(n)
        if i is None:
            continue
        editable.add(n)
        for d in (-2, -1, 1, 2):
            j = i + d
            if 0 <= j < len(_BAND_ORDER):
                editable.add(_BAND_ORDER[j])
    for n in nset:
        i = _BAND_IDX.get(n)
        if i is None:
            continue
        for d in (-3, 3):
            j = i + d
            if 0 <= j < len(_BAND_ORDER):
                background.add(_BAND_ORDER[j])
    editable.discard("V0")          # V0 is the electrical floor
    background -= editable          # after the discard, so a V0 three steps
                                    # away stays in background as view-only
    return editable, background


def band_for_leaf(leaf, violations_by_id):
    """A leaf's band, expanded from the layers named by all of its violations.

    ``violations_by_id`` maps a violation id to a Violation, which carries the
    rule id. Returns sorted tuples, ready to assign to Leaf.editable_layers and
    Leaf.background_layers.
    """
    nset = set()
    for vid in leaf.violations:
        v = violations_by_id.get(vid)
        if v is None:
            continue
        for lyr in layers_of_rule(v.rule_id):
            nset.add(lyr)
    editable, background = band_for_layers(nset)
    return tuple(sorted(editable)), tuple(sorted(background))
