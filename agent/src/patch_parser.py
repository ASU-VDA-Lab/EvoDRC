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

"""Parse the patch JSON produced for one leaf.

The expected envelope has exactly three keys, ``{leaf_id, ops, explanation}``.
There are two entry points. ``parse_patch_from_file_text`` reads a patch that
was written to a per-leaf file, trying plain JSON first and falling back to a
fenced block. ``parse_patch_json`` reads a patch out of a model's stdout, where
it is expected inside a fenced ```json block. Neither raises: anything that
cannot be turned into a patch comes back as None.
"""


import json
from typing import Any, Optional

from .types import Patch


_FENCE = "```"


def _dict_to_patch(obj, expected_leaf_id):
    """Validate a decoded JSON object into a ``Patch``, or return None.

    Both entry points go through this, so the envelope rules stay identical:
    the leaf id has to match the expected one, ``ops`` has to be a list, and
    ``patch`` is accepted as an alias for it.
    """
    if not isinstance(obj, dict):
        return None
    if obj.get("leaf_id") != expected_leaf_id:
        return None
    ops = obj.get("ops")
    # "patch" is tolerated as an alias for "ops".
    if ops is None:
        ops = obj.get("patch")
    if not isinstance(ops, list):
        return None
    return Patch(
        leaf_id=str(obj["leaf_id"]),
        ops=list(ops),
        explanation=str(obj.get("explanation", "")),
    )


def parse_patch_from_file_text(file_text, expected_leaf_id):
    # type: (Optional[str], str) -> Optional[Patch]
    """Parse a patch out of the per-leaf file it was written to.

    Plain JSON is tried first, since that is the unfenced form the prompt asks
    for. Failing that, the fenced-block extraction runs, so a file that still
    wraps the JSON in a ```json block parses too. Missing, empty or malformed
    input returns None, which dispatch records as a parse failure.
    """
    if not file_text:
        return None
    try:
        obj = json.loads(file_text)
    except (ValueError, TypeError):
        # Not plain JSON: it may still be wrapped in a fence.
        return parse_patch_json(file_text, expected_leaf_id)
    patch = _dict_to_patch(obj, expected_leaf_id)
    if patch is not None:
        return patch
    # Decoded, but unusable as a patch, for instance a wrong leaf id or a JSON
    # list. Try the fenced fallback, in case a valid block sits inside a string.
    return parse_patch_json(file_text, expected_leaf_id)


def parse_patch_json(stdout: Any, expected_leaf_id: str) -> Optional[Patch]:
    """Extract the first fenced ```json block from `stdout` and parse it.

    Accepts either a raw string or an already-decoded response dict; in the
    dict case the text is taken from the ``result`` field.
    """
    text = _coerce_text(stdout)
    if not text:
        return None

    i = text.find(_FENCE + "json")
    if i < 0:
        i = text.find(_FENCE)
        if i < 0:
            return None
    # Move past the opening fence line (```json\n  or ```\n).
    i_open_end = text.find("\n", i)
    if i_open_end < 0:
        return None
    i_open_end += 1
    j = text.find(_FENCE, i_open_end)
    if j < 0:
        return None
    raw = text[i_open_end:j].strip()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return _dict_to_patch(obj, expected_leaf_id)


def _coerce_text(stdout: Any) -> str:
    if stdout is None:
        return ""
    if isinstance(stdout, str):
        return stdout
    if isinstance(stdout, dict):
        # Decoded response object: prefer the ``result`` text, then any other
        # plain content field.
        for key in ("result", "text", "content"):
            v = stdout.get(key)
            if isinstance(v, str) and v:
                return v
        return json.dumps(stdout)
    return str(stdout)
