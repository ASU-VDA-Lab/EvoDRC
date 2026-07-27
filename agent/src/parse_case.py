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

"""First pipeline stage: read case metadata out of the rendered prompt file.

The prompt handed to the model carries the names and file paths that describe
a single repair case. This stage parses those fields and copies them into the
shared ``CaseContext``, falling back to whatever value the context already
holds. A missing case name is derived from the layout script filename; if it
still cannot be determined the stage raises, because every later stage keys
its outputs off that name.
"""


import os
from typing import Optional

from .agent_entry import parse_case_info_from_prompt
from .logging_setup import get_logger, stage_extra
from .types import CaseContext, CaseInfo


def stage_parse_case(ctx: CaseContext) -> None:
    """Fill in ``ctx.case_info`` from the fields found in the rendered prompt."""
    log = get_logger()
    log.info("start", extra=stage_extra("S1"))
    raw = parse_case_info_from_prompt(ctx.prompt_path)
    info = ctx.case_info
    info.case_name = str(raw.get("case_name") or info.case_name or "")
    info.design_type = str(raw.get("design_type") or info.design_type or "block")
    info.task_type = str(raw.get("task_type") or info.task_type or "repair")
    info.layout_path = str(raw.get("path_to_layout_script") or info.layout_path or "")
    info.drc_path = str(raw.get("path_to_drc_report") or info.drc_path or "")
    info.connectivity_path = str(
        raw.get("path_to_connectivity_file") or info.connectivity_path or "")
    info.rule_path = str(raw.get("path_to_design_rule") or info.rule_path or "")
    info.skill_path = str(raw.get("path_to_skill") or info.skill_path or "")
    info.output_path = str(
        raw.get("output_path") or info.output_path or ctx.output_path or "")
    info.model_name = str(raw.get("model_name") or info.model_name or "")
    if not info.case_name and info.layout_path:
        info.case_name = os.path.basename(info.layout_path).rsplit(".py", 1)[0]
    if not info.case_name:
        raise ValueError("case_name not derivable from prompt or layout path")
    log.info("end case=%s", info.case_name, extra=stage_extra("S1"))
