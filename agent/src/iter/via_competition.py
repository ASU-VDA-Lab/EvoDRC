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

"""Contest that picks one unit's edit of a shared via cell definition.

Via operations are keyed by cell name and rewrite the global cell definition,
so when two or more accepted units edit the same via cell, assembly can keep
only one version. This module chooses it by scoring each contender in
isolation: it renders a layout containing just that via cell with the
contender's via operations applied, instantiates it at every real placement
transform the cell has in the input layout, runs the DRC deck and counts the
resulting violations.

Placing the instances at their real coordinates matters because some grid
rules are defined in absolute coordinates, and placing everything at the origin
would score all contenders alike. Fewest violations wins, a contender that
fails to score ranks last, and ties break to the lexicographically smallest
leaf id, so the outcome is deterministic.
"""

import json
import os
import re
import subprocess

from ..patch_apply import apply_patch_to_text, _find_polygon_def
from ..patch_parser import parse_patch_from_file_text

_FAIL_SCORE = 10 ** 9   # rank given to a contender that failed to score


def _parse_dbu(text):
    """Return the ``layout.dbu`` literal from the layout script, verbatim as a
    string, falling back to the usual default when it is absent."""
    m = re.search(r"^layout\.dbu\s*=\s*([0-9.eE+\-]+)\s*$", text, re.MULTILINE)
    if m:
        return m.group(1)
    return "0.00025"


def _real_transforms(text, cell_name):
    """Return every placement transform of ``cell_name`` in the layout text.

    Matches the cell-instance inserts anywhere in the text and returns
    ``[[rot, mirror, x, y], ...]`` in file order."""
    pat = (r"\.insert\(pya\.CellInstArray\(cell_%s\.cell_index\(\),\s*"
           r"pya\.Trans\((\d+),\s*(True|False),\s*"
           r"pya\.Vector\((-?\d+),\s*(-?\d+)\)\)\)\)" % re.escape(cell_name))
    out = []
    for m in re.finditer(pat, text):
        out.append([int(m.group(1)), m.group(2) == "True",
                    int(m.group(3)), int(m.group(4))])
    return out


def _cell_shapes(text, cell_name):
    """Return the cell's ``(layer_num, polygon_id)`` inserts in file order,
    which is also shape-index order.

    Only datatype 0 is matched; marker shapes live on the top cell and never
    inside a via cell definition."""
    pat = (r"^cell_%s\.shapes\(layout\.layer\(pya\.LayerInfo\(\s*(\d+)\s*,"
           r"\s*0\s*\)\)\)\.insert\(\s*(p\w+)\s*\)\s*$" % re.escape(cell_name))
    return [(int(m.group(1)), m.group(2))
            for m in re.finditer(pat, text, re.MULTILINE)]


def _cell_def_text(text, cell_name):
    """Extract the standalone cell-definition lines for ``cell_name`` -- the
    polygon definitions and their shape inserts -- from the layout text, which
    may already have a patch applied."""
    shapes = _cell_shapes(text, cell_name)
    if not shapes:
        raise ValueError("no datatype-0 shapes found for cell %s" % cell_name)
    out = []
    for lyr, pid in shapes:
        m = _find_polygon_def(text, pid)
        if m is None:
            raise ValueError("polygon def not found: %s" % pid)
        out.append(m.group(0).strip())
        out.append("cell_%s.shapes(layout.layer(pya.LayerInfo(%d, 0)))"
                   ".insert(%s)" % (cell_name, lyr, pid))
    return "\n".join(out)


def _render_script(cell_name, dbu, cell_def, transforms, out_gds):
    """Build a standalone layout script holding the cell definition and one
    instance per placement transform."""
    lines = [
        "import pya",
        "layout = pya.Layout()",
        "layout.dbu = %s" % dbu,
        'cell_%s = layout.create_cell("%s")' % (cell_name, cell_name),
        cell_def,
        'cell_TOP = layout.create_cell("TOP")',
    ]
    for tr in transforms:
        lines.append(
            "cell_TOP.insert(pya.CellInstArray(cell_%s.cell_index(), "
            "pya.Trans(%d, %s, pya.Vector(%d, %d))))"
            % (cell_name, tr[0], "True" if tr[1] else "False", tr[2], tr[3]))
    lines.append('layout.write("%s")' % out_gds)
    lines.append("")
    return "\n".join(lines)


def _ws_root():
    """Return the directory above the agent package; this file lives at
    ``<root>/agent/src/iter/``."""
    here = os.path.dirname(os.path.abspath(__file__))
    agent_dir = os.path.dirname(os.path.dirname(here))
    return os.path.dirname(agent_dir)


def _klayout(args, scratch_dir, log_path, timeout):
    """Run ``klayout -b`` with the given arguments and return its exit code.

    The working directory is ``scratch_dir``, so relative artifact names in the
    scripts resolve there. Output goes to ``log_path``."""
    cmd = ["klayout", "-b"] + list(args)
    with open(log_path, "w", encoding="utf-8") as log:
        r = subprocess.run(cmd, cwd=scratch_dir, stdout=log,
                           stderr=subprocess.STDOUT,
                           universal_newlines=True, timeout=timeout)
    return r.returncode


def _artifact_paths(scratch_dir, cell_name, uid):
    base = os.path.join(scratch_dir, "%s__%s" % (cell_name, uid))
    return {"script": base + ".py",
            "gds": base + ".gds",
            "lyrdb": base + ".lyrdb",
            "drc_json": base + ".drc.json",
            "render_log": base + ".render.log",
            "drc_log": base + ".drc.log"}


def _score_contender(input_layout_text, cell_name, uid, ops, transforms, dbu,
                     deck_path, scratch_dir, case_name, timeout, art):
    """Build, render, DRC and post-process one contender's isolated cell.

    Returns the violation count, or None if any step fails; a contender that
    cannot be scored simply ranks last and assembly carries on."""
    # Artifact names are deterministic, so drop stale outputs first: otherwise
    # a failed stage could leave an old artifact behind and score it.
    for k in ("gds", "lyrdb", "drc_json"):
        if os.path.exists(art[k]):
            os.remove(art[k])

    # The sandbox is the untouched iteration input plus only this contender's
    # via operations for this cell. Passing no leaf is fine here: via ops are
    # keyed by cell name rather than scoped to a crop.
    patch = parse_patch_from_file_text(
        json.dumps({"leaf_id": uid, "ops": ops, "explanation": ""}), uid)
    if patch is None:
        return None
    sandbox_text = apply_patch_to_text(input_layout_text, patch, None)
    cell_def = _cell_def_text(sandbox_text, cell_name)
    with open(art["script"], "w", encoding="utf-8") as fh:
        fh.write(_render_script(cell_name, dbu, cell_def, transforms,
                                art["gds"]))

    # Render the isolated cell to GDS.
    rc = _klayout(["-r", art["script"]], scratch_dir, art["render_log"],
                  timeout)
    if rc != 0 or not os.path.isfile(art["gds"]) \
            or os.path.getsize(art["gds"]) == 0:
        return None

    # DRC with the benchmark deck.
    rc = _klayout(["-r", deck_path,
                   "-rd", "in_gds=%s" % art["gds"],
                   "-rd", "report_file=%s" % art["lyrdb"]],
                  scratch_dir, art["drc_log"], timeout)
    if rc != 0 or not os.path.isfile(art["lyrdb"]) \
            or os.path.getsize(art["lyrdb"]) == 0:
        return None

    # Count violations with the benchmark post-processor, so the numbers match
    # the reference report. Running it as a module from the repository root
    # puts that root on the import path, so the package-relative imports inside
    # the post-processor resolve.
    ws = _ws_root()
    env = dict(os.environ)
    pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(
        [ws, os.path.join(ws, "src")] + ([pp] if pp else []))
    cmd = ["python3", "-m", "agent.src.drc_postprocess",
           "--lyrpt", art["lyrdb"], "--output", art["drc_json"],
           "--case_name", case_name, "--design_type", "block",
           "--layout-script", art["script"]]
    r = subprocess.run(cmd, cwd=ws, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,
                       universal_newlines=True, timeout=timeout)
    if r.returncode != 0 or not os.path.isfile(art["drc_json"]):
        return None
    with open(art["drc_json"], "r", encoding="utf-8") as fh:
        d = json.load(fh)
    tv = d.get("total_violations")
    if not isinstance(tv, int):
        return None
    return tv


def run_competition(input_layout_text, cell_name, contenders, deck_path,
                    scratch_dir, case_name, timeout=600):
    """Score every contender for one shared via cell and pick a winner.

    ``contenders`` maps each leaf id to its via operations for this cell, in
    patch order, and must hold at least two entries. Returns a dict with the
    winning leaf id, the per-contender scores, the artifact paths, the
    placement transforms and the cell name.

    The winner is the contender with the fewest violations; an unscored
    contender ranks last, and any tie -- including the cases where no
    placement was found or every contender failed -- breaks to the
    lexicographically smallest leaf id."""
    uids = sorted(contenders.keys())
    if len(uids) < 2:
        raise ValueError("competition needs >= 2 contenders, got %d"
                         % len(uids))
    os.makedirs(scratch_dir, exist_ok=True)

    dbu = _parse_dbu(input_layout_text)
    transforms = _real_transforms(input_layout_text, cell_name)
    result = {"cell_name": cell_name, "transforms": transforms,
              "scores": {}, "artifacts": {}}

    if not transforms:
        # With no placement found there is nothing meaningful to score, so
        # pick the lexicographic winner without running KLayout at all.
        result["no_transforms"] = True
        for uid in uids:
            result["scores"][uid] = None
        result["winner"] = uids[0]
        return result

    for uid in uids:
        art = _artifact_paths(scratch_dir, cell_name, uid)
        try:
            score = _score_contender(
                input_layout_text, cell_name, uid, contenders[uid],
                transforms, dbu, deck_path, scratch_dir,
                case_name, timeout, art)
        except Exception:                                  # noqa: BLE001
            score = None
        result["scores"][uid] = score
        result["artifacts"][uid] = art

    def _rank(uid):
        s = result["scores"][uid]
        if s is None:
            s = _FAIL_SCORE
        return (s, uid)

    result["winner"] = min(uids, key=_rank)
    return result
