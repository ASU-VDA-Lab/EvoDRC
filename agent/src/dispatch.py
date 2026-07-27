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

"""Dispatch of repair leaves to the model backend.

A leaf is one bounded editing task: a small group of polygons together with
the violations that touch them. For each leaf this module builds a prompt,
makes a single model call, reads back the patch JSON the model wrote to a
per-leaf file, runs the patch through the validator, and records a
LeafResult saying whether it was mounted or skipped. Leaves inside one wave
are dispatched in parallel; the waves themselves run in order.
"""


import dataclasses
import importlib
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from .logging_setup import get_logger, stage_extra
from .patch_parser import (parse_patch_json, parse_patch_from_file_text,
                           _coerce_text)
from .prompt_format import build_leaf_prompt
from .types import CaseContext, Leaf, LeafResult
from . import conn_context
from . import drc_context
from . import validator


def dispatch_leaf(leaf: Leaf, ctx: CaseContext,
                  wave_idx: int, leaf_idx: int) -> LeafResult:
    """Run one model call for a leaf, validate the patch, and mount or skip it."""
    from ._invariant import SKIP_STATUS
    if getattr(leaf, "skip_status", None) == SKIP_STATUS:
        return LeafResult(leaf_id=leaf.leaf_id, status=SKIP_STATUS,
                          failed_check="invariant",
                          error="C1/C2 invariant failed; not dispatched")
    # Prefer a backend module that is already registered over a fresh import.
    backend = (sys.modules.get("agent_backend.claude")
               or importlib.import_module("agent_backend.claude"))

    call_id = "{0}_w{1:03d}_l{2:04d}".format(
        ctx.case_info.case_name or "case", wave_idx, leaf_idx)

    # The backend does not carry the model name into its per-call record, so
    # publish it through the environment for the token accounting to read and
    # key its per-model totals on.
    if ctx.case_info.model_name:
        os.environ["AGENT_MODEL_NAME"] = ctx.case_info.model_name

    # Patches are delivered through files rather than stdout: each leaf gets
    # its own path under the scratch directory, the prompt tells the agent to
    # write its patch JSON there, and the file is read back after the call.
    # The system temp directory is used when no scratch directory is set.
    base = ctx.temp_dir or tempfile.gettempdir()
    patches_dir = os.path.join(base, "patches")
    try:
        os.makedirs(patches_dir, exist_ok=True)
    except OSError:
        base = tempfile.gettempdir()
        patches_dir = os.path.join(base, "patches")
        try:
            os.makedirs(patches_dir, exist_ok=True)
        except OSError:
            pass
    patch_path = os.path.join(patches_dir, "{0}.json".format(leaf.leaf_id))
    # Remove any file left behind by an earlier wave, so a stale patch can
    # never be read back as this call's result.
    try:
        os.remove(patch_path)
    except OSError:
        pass

    # Connectivity-preview context for this leaf: written to the scratch
    # directory and named in the prompt, so the dispatched agent can preview
    # connectivity without access to any state held in this process.
    conn_ctx_path = conn_context.write_context(ctx, leaf)
    # DRC-preview context, carried into the prompt the same way.
    drc_ctx_path = drc_context.write_context(ctx, leaf)
    prompt_text = build_leaf_prompt(leaf, ctx, patch_path=patch_path,
                                    conn_ctx_path=conn_ctx_path,
                                    drc_ctx_path=drc_ctx_path)
    _dump_prompt(leaf, prompt_text, ctx)
    try:
        result = backend.call_agent(
            prompt_text=prompt_text,
            output_path=None,
            model=ctx.case_info.model_name,
            workspace=ctx.workspace or None,
            effort=None,
            call_id=call_id,
            temp_dir=ctx.temp_dir or None,
        )
    except TypeError:
        # Older backends take the first three arguments positionally.
        result = backend.call_agent(
            prompt_text, None, ctx.case_info.model_name,
            workspace=ctx.workspace or None, effort=None,
            call_id=call_id, temp_dir=ctx.temp_dir or None)

    if not isinstance(result, dict) or result.get("status") != "success":
        return LeafResult(
            leaf_id=leaf.leaf_id,
            status="dispatch_fail",
            error=(result or {}).get("error"),
            call_id=call_id,
        )

    # Read back the patch file. A missing, unreadable or malformed file
    # marks the leaf patch_parse_fail and leaves the layout untouched.
    file_text = None
    try:
        with open(patch_path, "r", encoding="utf-8") as fh:
            file_text = fh.read()
    except (FileNotFoundError, OSError):
        file_text = None

    patch = parse_patch_from_file_text(file_text, leaf.leaf_id)
    if patch is None:
        lr = LeafResult(
            leaf_id=leaf.leaf_id, status="patch_parse_fail",
            call_id=call_id)
        # Keep the complete raw output so the parse failure can be diagnosed
        # from the per-leaf dump: the file content when there was one,
        # otherwise whatever the backend returned.
        try:
            lr.raw_result_preview = (
                file_text or _coerce_text(result.get("raw_data")) or "")
        except Exception:
            pass
        return lr

    if not patch.ops:
        # An empty patch means the model chose to leave this leaf alone.
        return LeafResult(
            leaf_id=leaf.leaf_id, status="skipped_invalid_patch",
            patch=patch, call_id=call_id,
            failed_check="empty_patch", error="empty patch")

    verdict = validator.validate(patch, leaf, ctx)
    if not verdict.ok:
        return LeafResult(
            leaf_id=leaf.leaf_id, status="skipped_invalid_patch",
            patch=patch, verdict=verdict, call_id=call_id,
            failed_check=verdict.check_name, error=verdict.reason)

    return LeafResult(
        leaf_id=leaf.leaf_id, status="mounted",
        patch=patch, verdict=verdict, call_id=call_id)


def stage_dispatch(ctx: CaseContext) -> None:
    log = get_logger()
    log.info("start waves=%d", len(ctx.waves), extra=stage_extra("S9"))
    ctx.leaf_results = {}
    outer = _get_outer_workers()
    dump_dir = _maybe_dump_dir(ctx)
    _ctx_holder["ctx"] = ctx  # _dump_leaf reads ctx.violations from here
    for wave_idx, wave_ids in enumerate(ctx.waves):
        wave_leaves = [ctx.leaves[lid] for lid in wave_ids if lid in ctx.leaves]
        if not wave_leaves:
            continue
        if outer <= 1 or len(wave_leaves) == 1:
            # Serial path, easier to follow when debugging.
            for lidx, leaf in enumerate(wave_leaves):
                res = dispatch_leaf(leaf, ctx, wave_idx, lidx)
                ctx.leaf_results[res.leaf_id] = res
                _log_leaf(log, res)
                _dump_leaf(dump_dir, leaf, res)
            continue
        with ThreadPoolExecutor(max_workers=outer) as pool:
            futures = {pool.submit(dispatch_leaf, leaf, ctx, wave_idx, lidx):
                       leaf for lidx, leaf in enumerate(wave_leaves)}
            for fut in as_completed(futures):
                res = fut.result()
                ctx.leaf_results[res.leaf_id] = res
                _log_leaf(log, res)
                _dump_leaf(dump_dir, futures[fut], res)
    log.info("end leaf_results=%d", len(ctx.leaf_results),
             extra=stage_extra("S9"))


def _log_leaf(log, res: LeafResult) -> None:
    n_ops = len(res.patch.ops) if (res.patch is not None) else 0
    log.info("leaf %s verdict=%s call=%s ops=%d failed=%s err=%s",
             res.leaf_id, res.status, res.call_id or "-",
             n_ops, (res.failed_check or "-"), (res.error or "-"),
             extra=stage_extra("S9"))


def _maybe_dump_dir(ctx: CaseContext):
    """Return a directory path for per-leaf JSON dumps, or None if disabled.

    Dumping is on unless ``EVODRC_DUMP_LEAVES=0``. The preferred location is
    a ``leaves`` directory next to the calls directory named by
    ``AGENT_CALLS_DIR``, which outlives the scratch directory; without that
    variable, ``<temp_dir>/leaves`` is used instead.
    """
    if os.environ.get("EVODRC_DUMP_LEAVES", "1") == "0":
        return None
    # Prefer the location that outlives the scratch directory.
    calls_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    candidate = None
    if calls_dir:
        candidate = os.path.join(os.path.dirname(calls_dir), "leaves")
    elif ctx.temp_dir:
        candidate = os.path.join(ctx.temp_dir, "leaves")
    if candidate is None:
        return None
    try:
        os.makedirs(candidate, exist_ok=True)
    except OSError:
        return None
    return candidate


def _dump_leaf(dump_dir, leaf: Leaf, res: LeafResult):
    if dump_dir is None:
        return
    payload = {
        "leaf": _leaf_summary(leaf, _ctx_holder.get("ctx")),
        "result": _result_summary(res),
    }
    out = os.path.join(dump_dir, "{0}.json".format(res.leaf_id))
    try:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, default=str)
    except OSError:
        pass


_ctx_holder = {}  # populated by stage_dispatch for _dump_leaf to read


def _leaf_summary(leaf: Leaf, ctx=None):
    summary = {
        "leaf_id": leaf.leaf_id,
        "editable_polygons": list(leaf.editable_polygons),
        "bridge_polygons": list(leaf.bridge_polygons),
        "subcell_instances": list(leaf.subcell_instances),
        "violations": list(leaf.violations),
        "violation_count": len(leaf.violations),
        "block_bounds_dbu": list(leaf.block_bounds_dbu),
        "bbox_dbu": list(leaf.bbox_dbu),
    }
    # Map each violation id to its rule id and count per rule, so the dump
    # shows e.g. {"M1.S.2": 3, "V2.M3.AUX.2": 5} beside the raw ids.
    if ctx is not None and getattr(ctx, "violations", None):
        viol_by_id = {v.violation_id: v for v in ctx.violations}
        by_type = {}
        for vid in leaf.violations:
            v = viol_by_id.get(vid)
            rule = getattr(v, "rule_id", None) if v is not None else None
            if rule:
                by_type[rule] = by_type.get(rule, 0) + 1
        summary["violations_by_type"] = by_type
    return summary


def _result_summary(res: LeafResult):
    out = {
        "leaf_id": res.leaf_id,
        "status": res.status,
        "call_id": res.call_id,
        "failed_check": res.failed_check,
        "error": res.error,
    }
    if res.patch is not None:
        out["patch_ops"] = res.patch.ops
        out["patch_explanation"] = res.patch.explanation
    # Raw model output, recorded only for leaves whose patch failed to parse.
    preview = getattr(res, "raw_result_preview", None)
    if preview:
        out["raw_result_preview"] = preview
    return out


def _get_outer_workers() -> int:
    try:
        return max(1, int(os.environ.get("EVODRC_RATE_LIMIT_OUTER", "4")))
    except (TypeError, ValueError):
        return 4


def _resolve_prompts_dir(ctx):
    """Resolve a persistent directory for per-leaf prompt dumps.

    Candidates, in order:
      1. ``<AGENT_CALLS_DIR>/../prompts``, when that variable is set;
      2. a score directory derived from the case output path, which persists
         without needing any environment variable;
      3. ``<temp_dir>/prompts``, which is discarded when the run ends.
    Returns an empty string when none of them apply.
    """
    calls_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    if calls_dir:
        return os.path.join(os.path.dirname(calls_dir), "prompts")
    ci = getattr(ctx, "case_info", None)
    out_path = getattr(ci, "output_path", "") if ci else ""
    if out_path and "/result/" in out_path:
        score_root = os.path.dirname(os.path.dirname(out_path))
        score_root = score_root.replace("/result/", "/score/", 1)
        return os.path.join(score_root, "prompts")
    if getattr(ctx, "temp_dir", ""):
        return os.path.join(ctx.temp_dir, "prompts")
    return ""


def _dump_prompt(leaf, prompt_text, ctx):
    """Write the exact prompt sent to the model for one leaf as a .md file.

    The file lands at ``<prompts_dir>/<leaf_id>.md``. Directory and write
    failures are ignored, since the dump is only for inspection."""
    prompts_dir = _resolve_prompts_dir(ctx)
    if not prompts_dir:
        return
    try:
        os.makedirs(prompts_dir, exist_ok=True)
    except OSError:
        if not os.path.isdir(prompts_dir):
            return
    target = os.path.join(prompts_dir, "{0}.md".format(leaf.leaf_id))
    try:
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(prompt_text)
    except OSError:
        pass
