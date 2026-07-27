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

"""Classification of subcell instances and the edits allowed on each kind.

The cell name decides what may be done to an instance, matched
case-insensitively. A name starting with VIA_VIA0 is a device via and is
frozen; any other VIA_ name is a routing via, which may be moved or deleted;
a name matching the standard-cell library pattern is a cell placed by place
and route and is frozen as well. A name matching none of these raises
ValueError, which the pipeline treats as a reason to abandon the staged
repair and fall back to a single model call.
"""


import re
from typing import Tuple


VIA_PATTERN = re.compile(r"^VIA_.*", re.IGNORECASE)
STDCELL_PATTERN = re.compile(r"^.*_ASAP7_.*", re.IGNORECASE)
# A V0 device via sits below M1 and connects M1 to a device pin. Its geometry
# resembles a routing via but it must stay frozen, so this pattern is tested
# before VIA_PATTERN, which would otherwise match the same names first.
_V0_VIA_PATTERN = re.compile(r"^VIA_VIA0", re.IGNORECASE)


def detect_subcell_kind(cell_name: str) -> str:
    """Return 'via_v0', 'via' or 'stdcell', or raise ValueError if unrecognised."""
    if cell_name is None:
        raise ValueError("Unknown subcell kind: None")
    name = str(cell_name)
    if _V0_VIA_PATTERN.match(name):
        return "via_v0"
    if VIA_PATTERN.match(name):
        return "via"
    if STDCELL_PATTERN.match(name):
        return "stdcell"
    raise ValueError("Unknown subcell kind: {0}".format(cell_name))


def allowed_ops_for(kind: str) -> Tuple[str, ...]:
    """Return the tuple of ops that are legal for this subcell kind."""
    if kind == "via_v0":
        return ()          # device via: read-only background
    if kind == "via":
        return ("move_instance", "delete_instance")
    if kind == "stdcell":
        return ()
    raise ValueError("Unknown kind: {0}".format(kind))


def owner_kind_for(kind: str) -> str:
    """Map subcell `kind` to the owner_kind string used on polygon objects."""
    if kind == "via_v0":
        return "subcell_via"   # rendered as a via stamp; read-only
    if kind == "via":
        return "subcell_via"
    if kind == "stdcell":
        return "subcell_stdcell"
    raise ValueError("Unknown kind: {0}".format(kind))
