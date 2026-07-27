#!/usr/bin/env python3
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

"""Render a prompt template into finished prompt text on stdout.

The script takes two positional arguments, the case-info JSON first and the
prompt template JSON second, and the calling shell redirects stdout into a
prompt file. The template's directive body carries an {{INFO_JSON}}
placeholder, which is replaced with the subset of case-info keys that the
template lists in info_keys_to_embed. Templates use schema version
"src/v1", whose keys are schema_version, task, mode, info_keys_to_embed,
directive_body and output_format.
"""


import json
import sys


CASE_INFO_OPEN = "<!-- EVODRC_CASE_INFO -->"
CASE_INFO_CLOSE = "<!-- /EVODRC_CASE_INFO -->"


def render(template, info):
    schema = template.get("schema_version")
    if schema != "src/v1":
        raise ValueError(
            "Bad schema_version: {0!r} (expected 'src/v1')".format(
                schema))
    keys = template.get("info_keys_to_embed") or []
    filtered = {k: info[k] for k in keys if k in info}
    info_json_str = json.dumps(filtered, indent=2)
    body = template.get("directive_body", "")
    if "{{INFO_JSON}}" not in body:
        raise ValueError("directive_body missing {{INFO_JSON}} placeholder")
    rendered = body.replace("{{INFO_JSON}}", info_json_str)
    # Detection templates also carry a ${mode} placeholder.
    mode = template.get("mode") or info.get("design_type", "")
    if "${mode}" in rendered and mode:
        rendered = rendered.replace("${mode}", mode)
    return rendered


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(
            "usage: {0} <case_info_json> <template_json>\n".format(sys.argv[0]))
        sys.exit(2)
    info_path = sys.argv[1]       # case info comes first
    template_path = sys.argv[2]   # then the prompt template
    with open(info_path, encoding="utf-8") as fh:
        info = json.load(fh)
    with open(template_path, encoding="utf-8") as fh:
        template = json.load(fh)
    sys.stdout.write(render(template, info))
    if not sys.stdout.isatty():
        sys.stdout.flush()


if __name__ == "__main__":
    main()
