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

"""Per-leaf context file for the DRC preview tool.

The preview tool is a separate process that submits only candidate ops, so
everything it needs to identify the leaf and rebuild it from the case has to
be handed over out of band. This module writes that as a small JSON file and
points the ``EVODRC_DRC_CTX`` environment variable at it, which child
processes inherit.

The file carries the case name for logging, the design type, the paths to the
layout script, the reference DRC and connectivity reports and the rule deck,
and the leaf id. The DRC report path matters most: the violations it holds are
what the decomposition splits into leaves, so without it no leaf exists to be
found.

Each leaf gets its own file, named after the leaf, and the dispatcher passes
the path explicitly, so several leaves can be previewed at once without the
shared environment variable getting in the way. That variable remains a
fallback for running the tool by hand.
"""


import json
import os
import tempfile


ENV_VAR = "EVODRC_DRC_CTX"


def _drc_dir(base):
    """Return ``<base>/drc`` (created best-effort), falling back to the system
    temp dir if base is unwritable."""
    drc = os.path.join(base, "drc")
    try:
        os.makedirs(drc, exist_ok=True)
        return drc
    except OSError:
        drc = os.path.join(tempfile.gettempdir(), "drc")
        try:
            os.makedirs(drc, exist_ok=True)
        except OSError:
            pass
        return drc


def build_context(ctx, leaf):
    """Build the per-leaf context dict (no side effects)."""
    info = ctx.case_info
    data = {
        "case_name": info.case_name,
        "design_type": info.design_type or "block",
        "layout_path": info.layout_path,
        # The DRC report seeds the violations that the decomposition splits
        # into leaves, so an empty path here leaves the preview with no leaf
        # to find.
        "drc_path": info.drc_path,
        "connectivity_path": info.connectivity_path,
        "rule_path": info.rule_path,
        "leaf_id": leaf.leaf_id,
        # For a merged leaf, the ids it was built from, so the preview can
        # rebuild it. An ordinary leaf writes an empty list here.
        "union_members": list(getattr(leaf, "union_members", []) or []),
    }
    # Only the whole-design leaf carries this flag; the preview uses it to
    # rebuild that leaf instead of looking for it in the decomposition.
    if getattr(leaf, "whole_design", False):
        data["whole_design"] = True
    return data


def write_context(ctx, leaf):
    """Write the per-leaf context JSON and point the env var at it.

    The file goes to ``<temp_dir>/drc/context_<leaf_id>.json``, or under the
    system temp dir when the context has no temp dir of its own. Returns the
    path that was written.
    """
    base = ctx.temp_dir or tempfile.gettempdir()
    drc = _drc_dir(base)
    path = os.path.join(drc, "context_{0}.json".format(leaf.leaf_id))
    data = build_context(ctx, leaf)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    os.environ[ENV_VAR] = path
    return path


def set_path(path):
    """Point the env var at an existing context file."""
    os.environ[ENV_VAR] = path


def clear():
    """Remove the env var pointing at the context file."""
    os.environ.pop(ENV_VAR, None)


def read_context(path=None):
    """Load the context JSON, from an explicit path or from the env var.

    Raises when neither resolves or the file cannot be read; the preview tool
    turns that into an error verdict.
    """
    if path is None:
        path = os.environ.get(ENV_VAR)
    if not path:
        raise ValueError("no DRC context path (set --context or "
                         + ENV_VAR + ")")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
