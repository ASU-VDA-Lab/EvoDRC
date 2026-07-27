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

# Token accounting for each model call.
#
# Every model call writes one JSON file, ``${AGENT_CALLS_DIR}/<call_id>.json``,
# holding four flat token counts. The backend performs that write. Two readers
# then consume the same set of files: :func:`aggregate` below sums them
# in-process for the ``TOKENS_JSON=`` marker printed on stderr, and the host's
# own aggregator globs them into its score file, de-duplicating by file name.
# Because both read the same files, the two totals always agree.

import json
import os


# The four token counters, named exactly as the host aggregator expects them.
TOKEN_KEYS = (
    "input_tokens",
    "output_tokens",
    "cache_read_tokens",
    "cache_write_tokens",
)


def _zero_tokens():
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
    }


def _canonical_payload(call_id, raw_data):
    """Build the flat per-call payload from a raw response dict.

    The key set is the one the host aggregator reads without translation:
    ``call_id``, ``case_name``, ``model``, ``schema_version``, the four token
    counts, and ``by_model``.
    """
    usage = (raw_data or {}).get("usage") or {}
    model_name = ((raw_data or {}).get("model")
                  or os.environ.get("AGENT_MODEL_NAME", "")
                  or "")
    by_model_inner = {
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
        # The API reports these as *_input_tokens; flatten to the host's keys.
        "cache_read_tokens": int(usage.get("cache_read_input_tokens", 0) or 0),
        "cache_write_tokens": int(
            usage.get("cache_creation_input_tokens", 0) or 0),
    }
    payload = {
        "call_id": str(call_id),
        "case_name": os.environ.get("AGENT_CASE_NAME", "") or "unknown",
        "model": str(model_name),
        "schema_version": "1",
        "input_tokens": by_model_inner["input_tokens"],
        "output_tokens": by_model_inner["output_tokens"],
        "cache_read_tokens": by_model_inner["cache_read_tokens"],
        "cache_write_tokens": by_model_inner["cache_write_tokens"],
        "by_model": {str(model_name) or "unknown": by_model_inner},
    }
    return payload


def _atomic_write_json(target_path, payload):
    """Write JSON atomically, through a temporary file and os.replace."""
    parent = os.path.dirname(target_path)
    if parent:
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            pass
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    os.replace(tmp_path, target_path)


def record_call(call_id, raw_data, temp_dir):
    # type: (str, dict, str) -> None
    """Write one per-call token file at ``${AGENT_CALLS_DIR}/<call_id>.json``.

    The dispatch path does not use this, since the backend performs that write
    itself; the function exists so a caller outside that path still produces a
    file in the expected schema. Nothing is written when ``AGENT_CALLS_DIR`` is
    unset, which is how token recording is turned off. ``temp_dir`` is accepted
    only to keep the signature stable.
    """
    del temp_dir  # signature only: the target comes from AGENT_CALLS_DIR
    host_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    if not host_dir:
        return
    host_target = os.path.join(host_dir, call_id + ".json")
    try:
        _atomic_write_json(host_target, _canonical_payload(call_id, raw_data))
    except Exception:
        # Bookkeeping must never bring down the caller.
        pass


def aggregate(temp_dir):
    # type: (str) -> dict
    """Sum token usage across the per-call files belonging to this case.

    Reads ``${AGENT_CALLS_DIR}/${AGENT_CASE_NAME}_*.json``, the same files the
    host aggregator reads, so the stderr ``TOKENS_JSON=`` marker and the host's
    own totals come from one set of files.

    Args:
        temp_dir: Accepted to keep the signature stable; the files live under
            AGENT_CALLS_DIR rather than here.

    Returns:
        Dict with the four token keys. Zeros when ``AGENT_CALLS_DIR`` is
        unset, is not a directory, or cannot be listed -- the marker is only
        meaningful when the host asks for token recording and sets it.
    """
    del temp_dir  # the per-call files live under AGENT_CALLS_DIR
    totals = _zero_tokens()
    calls_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    if not calls_dir or not os.path.isdir(calls_dir):
        return totals
    case_name = os.environ.get("AGENT_CASE_NAME", "").strip()
    prefix = (case_name + "_") if case_name else None
    try:
        entries = os.listdir(calls_dir)
    except OSError:
        return totals
    for fn in entries:
        if not fn.endswith(".json") or fn.endswith(".tmp"):
            continue
        # Only this case's files, the same filter the host aggregator uses.
        # With no case name known, sum every per-call file in the directory.
        if prefix is not None and not fn.startswith(prefix):
            continue
        full = os.path.join(calls_dir, fn)
        try:
            with open(full, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            # Corrupt or half-written file: skip it and carry on.
            continue
        if not isinstance(data, dict):
            continue
        for k in TOKEN_KEYS:
            try:
                totals[k] += int(data.get(k, 0) or 0)
            except (TypeError, ValueError):
                continue
    return totals
