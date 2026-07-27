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

"""Per-leaf context file for the connectivity impact preview tool.

Structured like the other context carriers, except that the payload holds the
geometry itself rather than paths to it: every object in the block, as rings
per layer in world coordinates, together with how editable each one is from
this leaf's point of view. That tool only reads and intersects those rings, so
it runs from this file alone.

The file is written next to the other per-leaf contexts, named after the leaf,
and ``EVODRC_CONN_IMPACT_CTX`` points at the most recent one for running the
tool by hand. The dispatcher passes the path explicitly, so every leaf running
at the same time reads its own file.
"""


import json
import os
import tempfile


ENV_VAR = "EVODRC_CONN_IMPACT_CTX"


def _conn_impact_dir(base):
    """Return ``<base>/connimpact`` (created best-effort), falling back to the
    system temp dir if base is unwritable."""
    ci = os.path.join(base, "connimpact")
    try:
        os.makedirs(ci, exist_ok=True)
        return ci
    except OSError:
        ci = os.path.join(tempfile.gettempdir(), "connimpact")
        try:
            os.makedirs(ci, exist_ok=True)
        except OSError:
            pass
        return ci


def build_context(ctx, leaf):
    """Build the per-leaf context dict; nothing is written.

    crop_body is imported inside the function to keep this module free of any
    import cycle.
    """
    from . import crop_body
    info = ctx.case_info
    return {
        "case_name": info.case_name,
        "leaf_id": leaf.leaf_id,
        "objects": crop_body.object_geometries_by_layer(leaf, ctx),
    }


def write_context(ctx, leaf):
    """Write the per-leaf context JSON and point the env var at it.

    The file goes to ``<temp_dir>/connimpact/context_<leaf_id>.json``, or under
    the system temp dir when the context has no temp dir of its own. Returns
    the path that was written.
    """
    base = ctx.temp_dir or tempfile.gettempdir()
    ci = _conn_impact_dir(base)
    path = os.path.join(ci, "context_{0}.json".format(leaf.leaf_id))
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
        raise ValueError("no connectivity-impact context path (set --context "
                         "or " + ENV_VAR + ")")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
