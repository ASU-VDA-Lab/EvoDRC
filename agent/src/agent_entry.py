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

"""Entry point for block repair runs, called by the top-level dispatcher.

The rendered prompt file carries the case description as JSON inside an
EVODRC_CASE_INFO comment block. This module extracts that JSON, turns it
into a CaseContext holding the input paths, the output path and the per-run
scratch directory, then hands the context to the iterative repair
controller and returns the controller's (status, error) pair unchanged.
"""


import json
import os
import sys
from typing import Any, Dict, Optional

from .logging_setup import get_logger, setup_logger, stage_extra
from .types import CaseContext, CaseInfo, RuleDB


_OPEN = "<!-- EVODRC_CASE_INFO -->"
_CLOSE = "<!-- /EVODRC_CASE_INFO -->"
_FENCE = "```"


def parse_case_info_from_prompt(prompt_md_path: str) -> Dict[str, Any]:
    """Extract the case-info JSON from a rendered prompt file.

    Brace counting is used rather than a non-greedy regex, so the match ends
    at the brace that closes the outermost object.
    """
    with open(prompt_md_path, encoding="utf-8") as fh:
        text = fh.read()
    i = text.find(_OPEN)
    j = text.find(_CLOSE, i + 1)
    if i < 0 or j < 0:
        raise ValueError(
            "EVODRC_CASE_INFO markers not found in {0}".format(prompt_md_path))
    segment = text[i + len(_OPEN):j]
    # Find the JSON fence boundaries inside the segment.
    f1 = segment.find(_FENCE)
    if f1 < 0:
        # Fallback: scan for first '{' and brace-count to closing '}'.
        return _brace_count_json(segment)
    nl = segment.find("\n", f1)
    if nl < 0:
        raise ValueError("Malformed JSON fence inside EVODRC_CASE_INFO block")
    f1_end = nl + 1
    f2 = segment.rfind(_FENCE)
    if f2 <= f1_end:
        # Closing fence missing or ahead of the content.
        return _brace_count_json(segment[f1_end:])
    raw = segment[f1_end:f2].strip()
    return json.loads(raw)


def _brace_count_json(segment: str) -> Dict[str, Any]:
    """Extract the first complete JSON object from a block with no code fence."""
    start = segment.find("{")
    if start < 0:
        raise ValueError("No JSON object found in EVODRC_CASE_INFO segment")
    depth = 0
    in_str = False
    escape = False
    for k in range(start, len(segment)):
        ch = segment[k]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(segment[start:k + 1])
    raise ValueError("Unbalanced braces in EVODRC_CASE_INFO segment")


def build_case_context(prompt_path: str, output_path: str,
                       temp_dir: str, workspace: Optional[str],
                       model_name: str) -> CaseContext:
    raw = parse_case_info_from_prompt(prompt_path)
    info = CaseInfo(
        case_name=str(raw.get("case_name") or ""),
        design_type=str(raw.get("design_type") or "block"),
        task_type=str(raw.get("task_type") or "repair"),
        layout_path=str(raw.get("path_to_layout_script") or ""),
        drc_path=str(raw.get("path_to_drc_report") or ""),
        connectivity_path=str(raw.get("path_to_connectivity_file") or ""),
        rule_path=str(raw.get("path_to_design_rule") or ""),
        skill_path=str(raw.get("path_to_skill") or ""),
        output_path=str(raw.get("output_path") or output_path),
        model_name=str(raw.get("model_name") or model_name),
    )
    if not info.case_name:
        # Derive the case name from the layout file name instead.
        if info.layout_path:
            info.case_name = os.path.basename(info.layout_path).rsplit(".py", 1)[0]
    ctx = CaseContext(
        prompt_path=prompt_path,
        output_path=output_path,
        temp_dir=temp_dir,
        workspace=workspace or "",
        case_info=info,
        rule_db=RuleDB(),
    )
    # Optional feature switches, read once here and off unless set.
    ctx.drc_gate = 1 if str(os.environ.get("EVODRC_DRC_GATE", "0")).strip() \
        in ("1", "true", "True") else 0
    ctx.via_metal_coupling = 1 if str(
        os.environ.get("EVODRC_VIA_METAL_COUPLING", "0")).strip() \
        in ("1", "true", "True") else 0
    return ctx


def run_src_block_repair(prompt_path, output_path,
                                temp_dir, workspace, model_name):
    """Parse the prompt, build the case context and run the iterative repair.

    Returns a ``(status, error)`` tuple. ``status`` is ``"success"`` or
    ``"fail"``; ``error`` is a short reason tag, or None on success.

    Exceptions propagate rather than being caught here, so the caller sees
    the real exception text. The full traceback is additionally written to
    ``<temp_dir>/src_error.txt`` when a temp_dir was given.

    The status comes straight from the iterative controller: ``"success"``
    requires at least one connectivity-gated patch to have been assembled
    and the emitted output to differ from the original layout.
    """
    import traceback
    setup_logger("INFO")
    log = get_logger()
    log.info("agent_entry start prompt=%s output=%s",
             prompt_path, output_path, extra=stage_extra("S0"))

    def _persist_traceback(exc):
        """Write the current traceback to stderr and, if possible, to disk."""
        tb = traceback.format_exc()
        sys.stderr.write(tb)
        if temp_dir:
            try:
                with open(os.path.join(temp_dir, "src_error.txt"),
                          "w", encoding="utf-8") as fh:
                    fh.write(tb)
            except Exception:
                pass

    try:
        ctx = build_case_context(prompt_path, output_path,
                                 temp_dir or "", workspace, model_name)
    except Exception as exc:
        log.error("S1 build_case_context failed: %s", exc,
                  extra=stage_extra("S1"))
        _persist_traceback(exc)
        raise

    log.info("case=%s design=%s task=%s",
             ctx.case_info.case_name,
             ctx.case_info.design_type,
             ctx.case_info.task_type,
             extra=stage_extra("S0"))
    try:
        from .iter.controller import run_iterative_block_repair
        status, error = run_iterative_block_repair(ctx)
    except Exception as exc:
        log.error("pipeline failed: %s", exc, extra=stage_extra("S0"))
        _persist_traceback(exc)
        raise

    log.info("agent_entry end status=%s error=%s",
             status, (error or "-"), extra=stage_extra("S0"))
    return (status, error)
