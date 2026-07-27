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

# Unified EvoDRC dispatcher.
#
# Selects a model backend (claude / codex / cursor) and routes the run by
# (design_type, task_type):
#   - block + repair          -> src.agent_entry.run_src_block_repair()
#   - cell / polygon + repair -> one single-shot call through the backend
#   - detection (any design)  -> one single-shot call through the backend
#
# Four invariants hold on every route, because the host wrapper depends on
# them: unknown command-line flags are tolerated rather than rejected, the
# output path is pre-populated from --fallback before any pipeline work
# begins, the three stderr markers (STATUS, TOKENS_JSON, RUNTIME_SECONDS)
# are written on every exit path, and the process always exits 0 since the
# wrapper reads the outcome from STATUS= rather than from the exit code.

import argparse
import importlib
import json
import os
import shutil
import sys


# ---------------------------------------------------------------------------
# sys.path bootstrap: make ``agent.*`` and ``agent_backend.*`` importable
# no matter which directory the process was started from. The container
# image installs agent_backend into the ``src`` directory next to this one,
# so both the parent directory and that sibling go onto sys.path.
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)
_SRC = os.path.join(_PARENT, "src")
for _p in (_PARENT, _SRC):
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)


_VALID_BACKENDS = ("claude", "codex", "cursor")


def _zero_tokens():
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
    }


def _emit_markers(stderr, status, tokens, runtime_seconds):
    """Write the STATUS, TOKENS_JSON and RUNTIME_SECONDS markers to stderr."""
    stderr.write("STATUS={0}\n".format(status))
    stderr.write("TOKENS_JSON={0}\n".format(json.dumps(tokens)))
    stderr.write("RUNTIME_SECONDS={0:.3f}\n".format(runtime_seconds))


def _dump_raw(raw_json_out, status, raw_data, error):
    """Persist the raw backend JSON so a finished run can be inspected later.

    The pipeline path reports status="success" only after its evidence
    checks pass (at least one leaf mounted, the mount was not rejected, and
    the patched text differs from the original). That path issues many
    per-leaf calls rather than one, so it can succeed with raw_data unset;
    write a minimal success stub in that case instead of a failure payload.
    """
    if not raw_json_out:
        return
    if status == "success":
        payload = raw_data if raw_data is not None else {"status": "success"}
    else:
        payload = {"status": "fail", "error": error or "unknown"}
    try:
        os.makedirs(os.path.dirname(os.path.abspath(raw_json_out)),
                    exist_ok=True)
        with open(raw_json_out, "w") as fh:
            json.dump(payload, fh, indent=2, default=str)
    except Exception as exc:
        sys.stderr.write(
            "WARNING: failed to dump raw JSON to {0}: {1}\n".format(
                raw_json_out, exc))


def _resolve_backend(cli_value):
    if cli_value:
        return cli_value
    env_value = os.environ.get("AGENT_BACKEND", "").strip().lower()
    if env_value:
        return env_value
    return None


def _derive_design_and_case(args):
    """Recover design_type and case_name from the output path, best effort.

    Benchmark output paths follow the layout
        result/<run_id>/<design_type>/<task_type>/<case>/<case>_*.py
    so both names can normally be read off positionally, with the file name
    and the prompt path as fallbacks. Either value comes back empty when
    nothing in the paths identifies it.
    """
    output_path = args.output_file or ""
    design_type = ""
    case_name = ""
    try:
        parts = os.path.abspath(output_path).split(os.sep)
    except (TypeError, ValueError):
        parts = []
    if "result" in parts:
        try:
            idx = parts.index("result")
            # parts[idx+1] = run_id ; parts[idx+2] = design_type ;
            # parts[idx+3] = task_type ; parts[idx+4] = case_name
            if idx + 2 < len(parts):
                design_type = parts[idx + 2]
            if idx + 4 < len(parts):
                case_name = parts[idx + 4]
        except ValueError:
            pass
    if not case_name and output_path:
        base = os.path.basename(output_path)
        if base.endswith("_repaired.py"):
            case_name = base[: -len("_repaired.py")]
        elif base.endswith("_detection.json"):
            case_name = base[: -len("_detection.json")]
    if not design_type:
        # Fall back to a design-type directory named in the prompt path.
        prompt_lower = (args.prompt_file or "").lower()
        for cand in ("block", "cell", "polygon"):
            if "/" + cand + "/" in prompt_lower:
                design_type = cand
                break
    return design_type, case_name


def main():
    parser = argparse.ArgumentParser(
        description="EvoDRC unified LLM agent dispatcher")
    parser.add_argument("prompt_file",
                        help="Path to formatted prompt file")
    parser.add_argument("output_file",
                        help="Expected output file path")
    parser.add_argument("--backend", choices=_VALID_BACKENDS, default=None,
                        help="Backend to dispatch to (claude|codex|cursor)")
    parser.add_argument("--model", required=True,
                        help="Model name forwarded to the backend CLI")
    parser.add_argument("--task_type", default="repair",
                        choices=["repair", "detection"],
                        help="Task type drives fallback semantics")
    parser.add_argument("--fallback", default=None,
                        help="For repair: original layout copied to "
                             "output_file before agent runs")
    parser.add_argument("--workspace", default=None,
                        help="Workspace dir forwarded to backend")
    parser.add_argument("--effort", default=None,
                        help="Reasoning-effort level (high/medium/low)")
    parser.add_argument("--temp_dir", default=None,
                        help="Directory for intermediate / scratch files")
    parser.add_argument("--raw-json-out", dest="raw_json_out",
                        default=None,
                        help="Path to dump raw backend JSON")

    # Tolerate unknown flags so a newer host wrapper can pass extra options.
    args, _unknown = parser.parse_known_args()

    backend_name = _resolve_backend(args.backend)
    if backend_name is None:
        sys.stderr.write(
            "ERROR: --backend is required (claude|codex|cursor)\n")
        _emit_markers(sys.stderr, "fail", _zero_tokens(), 0.0)
        sys.exit(0)
    if backend_name not in _VALID_BACKENDS:
        sys.stderr.write(
            "ERROR: unknown backend '{0}'. Valid: {1}\n".format(
                backend_name, ", ".join(_VALID_BACKENDS)))
        _emit_markers(sys.stderr, "fail", _zero_tokens(), 0.0)
        sys.exit(0)

    # ------ Ensure temp_dir exists, then pre-populate the output ----------
    if args.temp_dir:
        try:
            os.makedirs(args.temp_dir, exist_ok=True)
        except OSError:
            pass
        # The pipeline writes into these subdirectories.
        for sub in ("calls", "stages", "checkpoint"):
            try:
                os.makedirs(os.path.join(args.temp_dir, sub), exist_ok=True)
            except OSError:
                pass
        sys.stdout.write("Temp dir: {0}\n".format(args.temp_dir))

    if args.task_type == "repair" and args.fallback:
        if os.path.isfile(args.fallback):
            try:
                os.makedirs(
                    os.path.dirname(os.path.abspath(args.output_file)),
                    exist_ok=True)
            except OSError:
                pass
            try:
                shutil.copy2(args.fallback, args.output_file)
                sys.stdout.write(
                    "Fallback: copied original to {0}\n".format(
                        args.output_file))
            except OSError as exc:
                sys.stderr.write(
                    "WARNING: failed to pre-populate fallback: {0}\n".format(
                        exc))
        else:
            sys.stderr.write(
                "WARNING: fallback file not found: {0}\n".format(
                    args.fallback))
    elif args.task_type == "detection":
        try:
            os.makedirs(
                os.path.dirname(os.path.abspath(args.output_file)),
                exist_ok=True)
        except OSError:
            pass
        try:
            with open(args.output_file, "w") as fh:
                fh.write("[]")
            sys.stdout.write(
                "Fallback: wrote empty detection JSON to {0}\n".format(
                    args.output_file))
        except OSError as exc:
            sys.stderr.write(
                "WARNING: failed to pre-populate detection []: {0}\n".format(
                    exc))

    # ------ Read formatted prompt -------------------------------------------
    prompt_text = ""
    try:
        with open(args.prompt_file) as fh:
            prompt_text = fh.read()
    except OSError as exc:
        sys.stderr.write(
            "ERROR: cannot read prompt file {0}: {1}\n".format(
                args.prompt_file, exc))
        _emit_markers(sys.stderr, "fail", _zero_tokens(), 0.0)
        _dump_raw(args.raw_json_out, "fail", None, str(exc))
        sys.exit(0)

    sys.stdout.write("Backend: {0}\n".format(backend_name))
    sys.stdout.write("Calling model: {0}\n".format(args.model))
    if args.effort:
        sys.stdout.write("Reasoning effort: {0}\n".format(args.effort))

    # ------ Lazy-load the backend ------------------------------------------
    try:
        backend = importlib.import_module("agent_backend." + backend_name)
    except Exception as exc:
        sys.stderr.write(
            "ERROR: failed to import backend '{0}': {1}\n".format(
                backend_name, exc))
        _emit_markers(sys.stderr, "fail", _zero_tokens(), 0.0)
        _dump_raw(args.raw_json_out, "fail", None, str(exc))
        sys.exit(0)
    if not hasattr(backend, "call_agent"):
        sys.stderr.write(
            "ERROR: backend '{0}' has no call_agent()\n".format(
                backend_name))
        _emit_markers(sys.stderr, "fail", _zero_tokens(), 0.0)
        sys.exit(0)

    # ------ Route on (design_type, task_type) -------------------------------
    design_type, case_name = _derive_design_and_case(args)
    use_src = (
        design_type == "block"
        and args.task_type == "repair"
        and os.environ.get("EVODRC_FORCE_FALLBACK", "0") != "1"
    )

    status = "fail"
    tokens = _zero_tokens()
    runtime_seconds = 0.0
    raw_data = None
    error = None

    if use_src:
        # ---- EvoDRC pipeline path -------------------------------------
        import time as _time
        t0 = _time.monotonic()
        try:
            from agent.src.agent_entry import (
                run_src_block_repair)
            from agent.src import tokens as tokens_mod

            ret = run_src_block_repair(
                prompt_path=args.prompt_file,
                output_path=args.output_file,
                temp_dir=args.temp_dir or "",
                workspace=args.workspace,
                model_name=args.model,
            )
            # The entry point returns either a bare status string or a
            # (status, error) pair.
            if isinstance(ret, tuple) and len(ret) == 2:
                status, error = ret
            else:
                status = ret
                error = None
            # Token counts always come from the per-call aggregator, so
            # every route reports the same totals.
            tokens = tokens_mod.aggregate(args.temp_dir or "")
            runtime_seconds = _time.monotonic() - t0
        except Exception as exc:
            runtime_seconds = _time.monotonic() - t0
            status = "fail"
            error = "src_unexpected:" + str(exc)
            sys.stderr.write("ERROR: {0}\n".format(error))
            try:
                from agent.src import tokens as tokens_mod
                tokens = tokens_mod.aggregate(args.temp_dir or "")
            except Exception:
                tokens = _zero_tokens()
    else:
        # ---- Single-shot path ---------------------------------------------
        call_id = "{0}_singleshot".format(case_name or "case") \
            if args.task_type == "repair" \
            else "{0}_detect".format(case_name or "case")
        try:
            result = backend.call_agent(
                prompt_text, args.output_file, args.model,
                workspace=args.workspace, effort=args.effort,
                call_id=call_id, temp_dir=args.temp_dir)
        except TypeError:
            # Older backends do not accept the extra keyword arguments.
            result = backend.call_agent(
                prompt_text, args.output_file, args.model,
                workspace=args.workspace, effort=args.effort)
        status = result.get("status", "fail")
        runtime_seconds = float(result.get("runtime_seconds", 0.0) or 0.0)
        raw_data = result.get("raw_data")
        error = result.get("error")
        # Prefer the aggregator so both routes count tokens the same way.
        try:
            from agent.src import tokens as tokens_mod
            tokens = tokens_mod.aggregate(args.temp_dir or "")
        except Exception:
            tokens = result.get("tokens") or _zero_tokens()

    if error:
        sys.stderr.write("ERROR: {0}\n".format(error))

    _emit_markers(sys.stderr, status, tokens, runtime_seconds)
    _dump_raw(args.raw_json_out, status, raw_data, error)

    if os.path.isfile(args.output_file):
        sys.stdout.write(
            "Output file exists: {0}\n".format(args.output_file))
    else:
        sys.stdout.write(
            "WARNING: Output file not found: {0}\n".format(args.output_file))

    sys.exit(0)


if __name__ == "__main__":
    main()
