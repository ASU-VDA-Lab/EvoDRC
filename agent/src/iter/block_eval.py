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

"""Whole-block DRC and connectivity measurement for one iteration.

The iteration's assembled layout is rendered to GDS, checked against the DRC
deck with KLayout, and the report is converted into a ``.drc.json`` that uses
the same schema as the reference report, so the next iteration's
decomposition can read it directly.

Block connectivity is then checked against the golden net list, and the
repaired violation multiset is compared with the iteration's input to derive
the repair rate and the count of newly introduced violations. Everything runs
from KLayout plus the agent's own post-processing and connectivity helpers.
"""

import json
import os
import re
import shutil
import subprocess
from collections import OrderedDict

from ..connectivity import is_connectivity_preserved
from ..drc_check import _multiset_from_drc_json


def _ws_root():
    here = os.path.dirname(os.path.abspath(__file__))
    agent_dir = os.path.dirname(os.path.dirname(here))
    return os.path.dirname(agent_dir)


def _make_render_script(layout_py_text, gds_path):
    """Point the layout script at ``gds_path``, rewriting its existing
    ``layout.write(...)`` call or appending one when there is none."""
    replacement = "layout.write({0})".format(json.dumps(gds_path))
    updated, count = re.subn(
        r"layout\.write\(\s*(['\"]).*?\1\s*\)", replacement, layout_py_text)
    if count == 0:
        if updated and not updated.endswith("\n"):
            updated += "\n"
        updated += "\n{0}\n".format(replacement)
    return updated


def _klayout(args, timeout=1800):
    """Run ``klayout -b`` with the given arguments and return the combined
    stdout and stderr; a timeout or failure is reported in the returned text
    rather than raised."""
    try:
        proc = subprocess.run(
            ["klayout", "-b"] + args,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, timeout=timeout)
        return proc.stdout or ""
    except subprocess.TimeoutExpired as exc:
        return "TIMEOUT: {0}".format(exc)
    except Exception as exc:                          # noqa: BLE001
        return "ERROR: {0}".format(exc)


def render_block_drc(repaired_py, case_name, design_type, rule_path, out_dir,
                     timeout=1800):
    """Render the layout, run the DRC deck and post-process the report.

    Returns ``(drc_json_path, log)``, with the path None when no report was
    produced."""
    work = out_dir
    os.makedirs(work, exist_ok=True)
    with open(repaired_py, "r", encoding="utf-8") as fh:
        layout_text = fh.read()
    gds = os.path.join(work, "{0}.gds".format(case_name))
    render_py = os.path.join(work, "{0}_render.py".format(case_name))
    lyrpt = os.path.join(work, "{0}.lyrpt".format(case_name))
    drcjson = os.path.join(work, "{0}.drc.json".format(case_name))
    with open(render_py, "w", encoding="utf-8") as fh:
        fh.write(_make_render_script(layout_text, gds))

    logs = []
    logs.append(_klayout(["-r", render_py], timeout=timeout))
    if rule_path and os.path.isfile(rule_path):
        logs.append(_klayout(
            ["-r", rule_path, "-rd", "in_gds=" + gds,
             "-rd", "report_file=" + lyrpt], timeout=timeout))
    if os.path.isfile(lyrpt):
        ws = _ws_root()
        env = dict(os.environ)
        pp = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = os.pathsep.join(
            [ws, os.path.join(ws, "src")] + ([pp] if pp else []))
        try:
            proc = subprocess.run(
                ["python3", "-m", "agent.src.drc_postprocess",
                 "--lyrpt", lyrpt, "--output", drcjson,
                 "--case_name", case_name, "--design_type", design_type,
                 "--layout-script", render_py],
                cwd=ws, env=env, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, universal_newlines=True,
                timeout=timeout)
            logs.append(proc.stdout or "")
        except Exception as exc:                      # noqa: BLE001
            logs.append("postprocess error: {0}".format(exc))
    raw_log = "\n".join(logs)
    if not os.path.isfile(drcjson):
        return None, raw_log
    return drcjson, raw_log


def _total_violations(drc_json_path):
    try:
        with open(drc_json_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    tv = data.get("total_violations")
    if isinstance(tv, int):
        return tv
    ms, total = _multiset_from_drc_json(drc_json_path)
    return total


def run_block_drc(repaired_py, input_drc_path, case_name, design_type,
                  rule_path, golden_conn_path, out_dir, iter_index,
                  timeout=1800):
    """Measure the repaired block and return ``(result, drc_json_path)``.

    The returned report becomes the next iteration's input DRC file and uses
    the same schema as the reference report. Render artifacts -- GDS, raw
    report, drc.json, the render script and the KLayout log -- are written flat
    into ``out_dir``; serialising the result is the caller's job."""
    drcjson, log = render_block_drc(
        repaired_py, case_name, design_type, rule_path, out_dir,
        timeout=timeout)

    # Connectivity is checked on the repaired layout against the golden nets.
    connectivity = "unknown"
    if golden_conn_path and os.path.isfile(golden_conn_path):
        ok = is_connectivity_preserved(
            golden_conn_path, repaired_py, design_type or "block")
        connectivity = "preserved" if ok else "broken"

    start_total = _total_violations(input_drc_path)
    end_total = _total_violations(drcjson) if drcjson else None

    new_violation_count = None
    repair_rate = None
    if drcjson and os.path.isfile(input_drc_path):
        try:
            in_ms, _it = _multiset_from_drc_json(input_drc_path)
            af_ms, _at = _multiset_from_drc_json(drcjson)
            new_violation_count = 0
            for k, cnt in af_ms.items():
                new_violation_count += max(0, cnt - in_ms.get(k, 0))
        except Exception:                             # noqa: BLE001
            new_violation_count = None
    if isinstance(start_total, int) and isinstance(end_total, int):
        repair_rate = (((start_total - end_total) / start_total)
                       if start_total else 0.0)

    result = {
        "iter": iter_index,
        "start_violations": start_total,
        "end_violations": end_total,
        "repair_rate": repair_rate,
        "new_violation_count": new_violation_count,
        "connectivity": connectivity,
        "drc_total_after": end_total,
        "drc_rendered": bool(drcjson),
        "input_drc": input_drc_path,
        "repaired_drc": drcjson or "",
    }
    # Keep a tail of the KLayout log on disk for diagnosis; the result dict
    # carries only the measured values and the artifact paths.
    try:
        with open(os.path.join(out_dir, "klayout.log"), "w",
                  encoding="utf-8") as fh:
            fh.write(log[-20000:])
    except OSError:
        pass
    return result, drcjson


def run_block_drc_nested(repaired_py, input_drc_path, case_name, design_type,
                         rule_path, golden_conn_path, repaired_dir,
                         iter_index, timeout=1800):
    """:func:`run_block_drc` with the artifact layout used in published runs.

    Render artifacts go to ``<repaired_dir>/_blockeval/`` and the DRC report is
    additionally copied to ``<repaired_dir>/<case>.drc.json``, which is the
    path returned and the one named by ``result["repaired_drc"]``.

    The nesting lives here rather than in ``run_block_drc`` so that a caller
    passing its own ``out_dir`` gets the artifacts in that directory itself."""
    be_out = os.path.join(repaired_dir, "_blockeval")
    try:
        os.makedirs(be_out, exist_ok=True)
    except OSError:
        pass
    result, drcjson = run_block_drc(
        repaired_py=repaired_py, input_drc_path=input_drc_path,
        case_name=case_name, design_type=design_type, rule_path=rule_path,
        golden_conn_path=golden_conn_path, out_dir=be_out,
        iter_index=iter_index, timeout=timeout)

    final_drc = drcjson
    if drcjson and os.path.isfile(drcjson):
        dest = os.path.join(repaired_dir, "{0}.drc.json".format(case_name))
        try:
            shutil.copyfile(drcjson, dest)
            final_drc = dest
        except OSError:
            # If the copy fails, keep pointing at the _blockeval path.
            final_drc = drcjson
    result["repaired_drc"] = final_drc or ""
    return result, final_drc


# The ``block_result.json`` schema: these keys, in this order. run_block_drc
# also produces ``drc_rendered``, and the early-stop path adds a ``note``;
# both are dropped when the file is written.
BLOCK_RESULT_KEYS = (
    "iter", "start_violations", "end_violations", "repair_rate",
    "new_violation_count", "connectivity", "drc_total_after",
    "input_drc", "repaired_drc",
)


def write_block_result(iter_dir, result):
    """Write ``result`` to ``<iter_dir>/block_result.json`` and return the path.

    Only the keys in :data:`BLOCK_RESULT_KEYS` are written, in that order, so
    the file always has the same schema. The keys are copied into a fresh dict,
    so the controller and the knowledge update still see every extra key
    ``result`` carries.

    The controller calls this on both loop exits, the normal one and the early
    stop taken when the block is already DRC-clean."""
    doc = OrderedDict()
    for key in BLOCK_RESULT_KEYS:
        doc[key] = result.get(key)
    path = os.path.join(iter_dir, "block_result.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
    return path
