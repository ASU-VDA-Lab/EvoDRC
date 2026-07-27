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

"""Scheduler that dispatches one repair subprocess per leaf.

Each leaf is handled by a ``leaf_runner`` subprocess, and at most
``LEAF_CONCURRENCY`` of them run at once; 0 means all leaves at once. A
worker's stdout and stderr go to a per-leaf file rather than an in-memory
pipe, so file-descriptor and process pressure stays bounded.

That setting is only a per-phase sub-cap. The binding limit is the
process-wide gate in ``throttle``: ``_run_one`` spawns its subprocess inside
``throttle.call_slot``, so the global concurrency cap and the post-call
cooldown apply to repair calls exactly as they do to knowledge calls. Each
child makes one model call, so holding the slot for the child's lifetime
bounds the in-flight calls conservatively.
"""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import paths as _paths
from . import throttle
# Bound as a module rather than importing sweep_unit directly, so this file
# and leaf_runner.py both reach the sweep through the same module attribute.
from . import workdir as _workdir


def _concurrency(n_leaves):
    """Resolve the worker cap from LEAF_CONCURRENCY; 0 means all leaves at
    once, and an invalid value falls back to 5."""
    raw = os.environ.get("LEAF_CONCURRENCY", "5")
    try:
        k = int(raw)
    except (TypeError, ValueError):
        k = 5
    if k == 0:
        return max(1, n_leaves)
    if k < 0:
        k = 5
    return max(1, k)


def _ws_root():
    """Return the directory above the agent package, which the child needs as
    its working directory for ``-m agent...`` to resolve."""
    here = os.path.dirname(os.path.abspath(__file__))      # .../agent/src/iter
    agent_dir = os.path.dirname(os.path.dirname(here))     # .../agent
    return os.path.dirname(agent_dir)                      # /workspace


def _run_one(leaf_id, iter_index, common, *, iter_work):
    """Spawn one leaf_runner subprocess and return ``(leaf_id, returncode)``.

    ``iter_work`` names the container-local work directory for this iteration,
    from which the unit's own work directory is derived. It is required and
    keyword-only so it can never be silently defaulted.
    """
    out_dir = _paths.leaf_dir(common["iter_dir"], leaf_id)
    unit_work = _workdir.unit_work_dir(iter_work, leaf_id)
    call_id = "{0}_iter{1}_{2}".format(
        common["case_name"], iter_index, leaf_id)
    cmd = [
        sys.executable, "-m", "agent.src.iter.leaf_runner",
        "--input-layout", common["input_layout"],
        "--input-drc", common["input_drc"],
        "--leaf-id", leaf_id,
        "--out-dir", out_dir,
        "--work-dir", unit_work,
        "--call-id", call_id,
        "--case-name", common["case_name"],
        "--design-type", common["design_type"],
        "--conn-path", common["conn_path"] or "",
        "--rule-path", common["rule_path"] or "",
        "--skill-path", common["skill_path"] or "",
        "--model", common["model"],
        "--workspace", common["workspace"] or "",
        "--score-calls-dir", common["score_calls_dir"] or "",
        # ---- knowledge injection paths and prompt mode ---------------------
        "--inject-main", (common.get("inject") or {}).get("main", "") or "",
        "--inject-official",
        (common.get("inject") or {}).get("official", "") or "",
        "--inject-kdir",
        (common.get("inject") or {}).get("knowledge_dir", "") or "",
        "--tc-dir", common.get("tc_dir", "") or "",
        "--ablation", common.get("ablation", "") or "",
        "--prompt-mode", common.get("prompt_mode", "exp3") or "exp3",
    ]
    # ---- union units: member list plus the solution-free metadata file ------
    # plan_units wrote host_union.<unit>.json into <iter_dir>/input, which is
    # the directory holding the input layout.
    members = (common.get("unions_map") or {}).get(leaf_id)
    if members:
        cmd += [
            "--union-members", ",".join(members),
            "--host-union",
            os.path.join(os.path.dirname(common["input_layout"]),
                         "host_union.{0}.json".format(leaf_id)),
        ]
    ws = _ws_root()
    env = dict(os.environ)
    # Let the child resolve both the ``agent`` package and ``agent_backend``.
    pp = env.get("PYTHONPATH", "")
    parts = [ws, os.path.join(ws, "src")]
    if pp:
        parts.append(pp)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    env["PYTHONHASHSEED"] = "0"
    env["RECORD_TOKENS"] = "1"
    # runner.log is container-local: it exists only for debugging inside the
    # container, so it goes straight to the work dir instead of being written
    # to the unit dir and swept afterwards.
    log_path = os.path.join(unit_work, "runner.log")
    try:
        with open(log_path, "w", encoding="utf-8") as logfh:
            # The global gate. call_slot returns the credit even if the spawn
            # itself raises, so a broken child cannot leak a slot.
            with throttle.call_slot("leaf:" + leaf_id):
                proc = subprocess.run(cmd, cwd=ws, env=env,
                                      stdout=logfh, stderr=subprocess.STDOUT)
    finally:
        # The child sweeps its own unit dir, but one killed before its cleanup
        # runs would leave the unit dirty, so sweep again here; the move is
        # idempotent, making a second sweep harmless.
        #
        # This sits outside the call_slot context, so the concurrency credit is
        # already back before the sweep starts, and it swallows every
        # exception: run_leaves records rc=-1 for anything raised out of the
        # future, and a tidy-up failure leaves a successful repair intact.
        try:
            _workdir.sweep_unit(out_dir, unit_work=unit_work)
        except Exception as exc:                      # noqa: BLE001
            sys.stderr.write(
                "leaf {0} sweep failed: {1}\n".format(leaf_id, exc))
    return leaf_id, proc.returncode


def run_leaves(iter_index, leaf_ids, common, *, iter_work):
    """Run every leaf under the concurrency cap, returning ``{leaf_id: rc}``.

    ``iter_work`` is the container-local work directory for this iteration and
    is forwarded unchanged to every ``_run_one``.

    ``common`` carries the settings shared by all leaves: iter_dir,
    input_layout, input_drc, case_name, design_type, conn_path, rule_path,
    skill_path, model, workspace, score_calls_dir, inject (the staged
    knowledge paths), tc_dir, ablation, prompt_mode, and unions_map, whose
    entries mark which units are dispatched as unions.

    The concurrency cap is read from the environment, which ``conf.resolve()``
    has already populated; the same environment is handed to every child.
    """
    leaf_ids = list(leaf_ids)
    if not leaf_ids:
        return {}
    k = _concurrency(len(leaf_ids))
    results = {}
    with ThreadPoolExecutor(max_workers=k) as pool:
        futs = {pool.submit(_run_one, lid, iter_index, common,
                            iter_work=iter_work): lid
                for lid in leaf_ids}
        for fut in as_completed(futs):
            lid = futs[fut]
            try:
                _lid, rc = fut.result()
            except Exception as exc:                  # noqa: BLE001
                rc = -1
                sys.stderr.write(
                    "leaf {0} runner crashed: {1}\n".format(lid, exc))
            results[lid] = rc
    return results
