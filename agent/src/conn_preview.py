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

"""Command-line connectivity preview for one candidate set of edits.

The caller passes a candidate ``{"ops": [...]}`` and the per-leaf context file
prepared for it; the leaf comes from the context, not the candidate. The ops
are merged into a temporary copy of the full design layout script, which is
then handed to the connectivity checker.

The result is printed as a single line of JSON: whether connectivity is
preserved, how many seeds were checked, and which ones broke. The exit code is
0 when connectivity holds, 1 when it does not, and 2 on an error.
"""


import argparse
import json
import os
import sys
import tempfile

from . import conn_check
from . import conn_context
from .patch_apply import apply_patch_to_text
from .types import Leaf, Patch


def _verdict(result):
    """Condense a checker result into the verdict printed to stdout.

    The detail lists are indexed directly rather than with ``get``: each loop
    reads only the list the checker produced for it, so a KeyError would mean
    the two sides have gone out of step and should not be swallowed.
    """
    broken = []
    for e in result.get("missing_seeds", []):
        broken.append({"kind": "missing_seed",
                       "seed_layer": e["layer"], "seed_points": e["points"]})
    for e in result.get("pin_mismatches_detail", []):
        broken.append({"kind": "pin_endpoint",
                       "seed_layer": e["seed_layer"],
                       "seed_points": e["seed_points"],
                       "endpoint_layer": e["endpoint_layer"]})
    for e in result.get("layer_mismatches_detail", []):
        broken.append({"kind": "layer_count",
                       "seed_layer": e["seed_layer"],
                       "seed_points": e["seed_points"],
                       "endpoint_layer": e["endpoint_layer"]})
    return {"preserved": result.get("connectivity_preserved"),
            "summary": result.get("details", ""),
            "seeds_checked": result.get("seeds_checked", 0),
            "seeds_missing": result.get("seeds_missing", 0),
            "broken_seeds": broken}


def _error_verdict(reason):
    return {"preserved": None, "summary": reason,
            "seeds_checked": 0, "seeds_missing": 0, "broken_seeds": []}


def _empty_verdict(seeds_checked):
    return {"preserved": True,
            "summary": "empty patch (no ops) -> connectivity unchanged",
            "seeds_checked": seeds_checked, "seeds_missing": 0,
            "broken_seeds": []}


def _exit_code(verdict):
    preserved = verdict.get("preserved")
    if preserved is None:
        return 2
    if preserved is True:
        return 0
    return 1


def _build_parser():
    p = argparse.ArgumentParser(
        prog="conn_preview",
        description="Merge candidate ops into the full design and report "
                    "whether block connectivity is preserved.")
    p.add_argument("--candidate", required=True,
                   help="JSON file holding {\"ops\":[...]} (leaf_id OPTIONAL "
                        "and never required).")
    p.add_argument("--context", default=None,
                   help="Per-leaf context path supplied by the harness "
                        "(falls back to env EVODRC_CONN_CTX).")
    return p


def _conn_dir_for(ctx_path, ctx_temp_dir):
    """Pick a writable directory to hold the merged layout script.

    The directory holding the context file is preferred, then the context's
    own temp dir, then the system temp dir. The agent's source directory is
    mounted read-only, so it is never a candidate.
    """
    if ctx_path:
        d = os.path.dirname(os.path.abspath(ctx_path))
        if os.path.isdir(d) and os.access(d, os.W_OK):
            return d
    if ctx_temp_dir and os.path.isdir(ctx_temp_dir) and os.access(ctx_temp_dir, os.W_OK):
        return ctx_temp_dir
    return tempfile.gettempdir()


def _emit(verdict):
    sys.stdout.write(json.dumps(verdict) + "\n")
    sys.stdout.flush()
    return _exit_code(verdict)


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    # 1. Resolve the context file: design type, layout, reference connectivity
    #    report, and the leaf id. The case name is only used for logging.
    try:
        ctx = conn_context.read_context(args.context)
    except Exception as exc:
        return _emit(_error_verdict("context resolution failed: " + str(exc)))

    design_type = ctx.get("design_type") or "block"
    layout_path = ctx.get("layout_path")
    connectivity_path = ctx.get("connectivity_path")
    ctx_leaf_id = ctx.get("leaf_id")
    case_name = ctx.get("case_name")
    if case_name:
        sys.stderr.write("conn_preview: case_name=" + str(case_name)
                         + " leaf_id=" + str(ctx_leaf_id) + "\n")
    if not layout_path or not connectivity_path or not ctx_leaf_id:
        return _emit(_error_verdict(
            "context missing layout_path/connectivity_path/leaf_id"))

    # 2. Load the candidate. Only its ops are used; any leaf_id is ignored.
    try:
        with open(args.candidate, "r", encoding="utf-8") as fh:
            cand = json.load(fh)
    except Exception as exc:
        return _emit(_error_verdict("candidate unreadable/malformed: "
                                    + str(exc)))
    if not isinstance(cand, dict):
        return _emit(_error_verdict("candidate JSON is not an object"))

    cand_leaf = cand.get("leaf_id")
    if cand_leaf is not None and cand_leaf != ctx_leaf_id:
        sys.stderr.write(
            "conn_preview: candidate leaf_id %r ignored; using context "
            "leaf_id %r\n" % (cand_leaf, ctx_leaf_id))

    ops = cand.get("ops", [])
    if not isinstance(ops, list):
        return _emit(_error_verdict("candidate 'ops' is not a list"))

    # 3. An empty candidate cannot change connectivity, so skip the checker.
    if not ops:
        return _emit(_empty_verdict(0))

    # 4. Read the full design layout script.
    try:
        with open(layout_path, "r", encoding="utf-8") as fh:
            full_text = fh.read()
    except Exception as exc:
        return _emit(_error_verdict("layout unreadable: " + str(exc)))

    # 5. Build the patch straight from the context leaf id and the candidate
    #    ops. The empty Leaf passed alongside it is a placeholder: the merge is
    #    driven entirely by text anchors in the layout script.
    patch = Patch(leaf_id=ctx_leaf_id, ops=ops,
                  explanation=cand.get("explanation", ""))
    try:
        merged = apply_patch_to_text(
            full_text, patch, Leaf(ctx_leaf_id, [], [], [], []))
    except Exception as exc:
        return _emit(_error_verdict("patch merge failed: " + str(exc)))

    # 6. Write the merged script to a writable scratch directory.
    conn_dir = _conn_dir_for(args.context, None)
    fd, mpath = tempfile.mkstemp(prefix="conn_preview_", suffix=".py",
                                 dir=conn_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(merged)
        # 7. Compare the merged script against the reference connectivity.
        try:
            result = conn_check.check_connectivity(
                connectivity_path, mpath, design_type)
        except Exception as exc:
            return _emit(_error_verdict("check_connectivity raised: "
                                        + str(exc)))
    finally:
        # 8. Always remove the scratch file.
        try:
            os.unlink(mpath)
        except OSError:
            pass

    if not isinstance(result, dict):
        return _emit(_error_verdict("check_connectivity returned non-dict"))

    # 9. Print the verdict and exit accordingly.
    return _emit(_verdict(result))


if __name__ == "__main__":
    sys.exit(main())
