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

"""Connectivity check that decides whether a leaf's patch is applied.

For each leaf, the candidate patch is applied to a rendered copy of the
iteration's input layout, leaving the canonical input as the benchmark
shipped it, and the result is compared against the golden net list.
Connectivity is the only criterion: a missing, empty or unparseable patch is
rejected, and so is one that breaks connectivity. New DRC violations are
counted later, at block level, after assembly.

The connectivity check itself runs through an external helper provided by the
evaluation environment. This stage is the connectivity verdict alone; model
calls and scoring belong to other stages.
"""

import json
import os

from ..connectivity import is_connectivity_preserved
from ..patch_apply import apply_patch_to_text
from ..patch_parser import parse_patch_from_file_text


def _load_patch_obj(patch_json_path):
    """Return ``(obj, n_ops)``, with ``obj`` None when the file is missing,
    empty or does not parse into a dict with an ``ops`` list."""
    if not patch_json_path or not os.path.isfile(patch_json_path):
        return None, 0
    if os.path.getsize(patch_json_path) == 0:
        return None, 0
    try:
        with open(patch_json_path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, ValueError):
        return None, 0
    if not isinstance(obj, dict):
        return None, 0
    ops = obj.get("ops")
    if not isinstance(ops, list):
        return None, 0
    return obj, len(ops)


def gate_leaf(ctx, leaf_id, patch_json_path, input_layout_text,
              golden_conn_path, design_type, scratch_dir):
    """Decide the connectivity verdict for one leaf.

    Returns a dict with the keys ``leaf_id``, ``gated_in``,
    ``connectivity_preserved``, ``n_ops`` and ``reason``. ``ctx`` is the
    decomposed case context for this iteration, so ``ctx.leaves[leaf_id]``
    corresponds to the patch's leaf."""
    obj, n_ops = _load_patch_obj(patch_json_path)
    if obj is None or n_ops == 0:
        return {"leaf_id": leaf_id, "gated_in": False,
                "connectivity_preserved": None, "n_ops": n_ops,
                "reason": "empty_or_missing_patch"}

    leaf = ctx.leaves.get(leaf_id)
    if leaf is None:
        return {"leaf_id": leaf_id, "gated_in": False,
                "connectivity_preserved": None, "n_ops": n_ops,
                "reason": "leaf_not_found"}

    patch = parse_patch_from_file_text(json.dumps(obj), leaf_id)
    if patch is None or not patch.ops:
        return {"leaf_id": leaf_id, "gated_in": False,
                "connectivity_preserved": None, "n_ops": n_ops,
                "reason": "unparseable_patch"}

    # Apply to a rendered copy of the iteration input, never the input itself.
    try:
        rendered = apply_patch_to_text(input_layout_text, patch, leaf)
    except Exception as exc:                          # noqa: BLE001
        return {"leaf_id": leaf_id, "gated_in": False,
                "connectivity_preserved": None, "n_ops": n_ops,
                "reason": "apply_failed:{0}".format(exc)}

    os.makedirs(scratch_dir, exist_ok=True)
    render_py = os.path.join(scratch_dir, "{0}_render.py".format(leaf_id))
    with open(render_py, "w", encoding="utf-8") as fh:
        fh.write(rendered)

    preserved = bool(is_connectivity_preserved(
        golden_conn_path, render_py, design_type or "block"))
    return {"leaf_id": leaf_id, "gated_in": preserved,
            "connectivity_preserved": preserved, "n_ops": n_ops,
            "reason": ("conn_preserved" if preserved else "conn_broken")}
