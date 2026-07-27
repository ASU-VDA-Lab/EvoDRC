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

"""Yes-or-no access to the evaluator's connectivity checker.

The checker ships with the benchmark's evaluator directory, which is mounted
into place rather than installed as a package, so it has to be found on disk
and imported at runtime. This module tries a fixed list of locations, memoizes
the function it finds, and exposes one call returning a plain bool. The other
fields of the checker's result are dropped; callers that want the detail go
through the checker directly.
"""


import os
import sys
from typing import Optional


_CHECK_FUNC = None  # cached once resolved


def _resolve_check_connectivity():
    """Find the evaluator's check_connectivity() and import it once."""
    global _CHECK_FUNC
    if _CHECK_FUNC is not None:
        return _CHECK_FUNC
    candidates = [
        "/workspace/evaluator_helpers",  # where the container mounts it
        os.path.normpath(os.path.join(  # alongside the benchmark checkout
            # realpath rather than abspath: the agent directory may be reached
            # through a symlink, and only the resolved location has the
            # benchmark next to it.
            os.path.dirname(os.path.realpath(__file__)),
            "..", "..", "DAC26_DRC_Benchmark", "evaluator",
        )),
        os.environ.get("EVALUATOR_DIR", ""),  # explicit override
        os.path.normpath(os.path.join(  # when this package has been copied
            # into the benchmark itself, the evaluator sits two levels up.
            os.path.dirname(os.path.realpath(__file__)),
            "..", "..", "evaluator",
        )),
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(c, "check_connectivity.py")):
            if c not in sys.path:
                sys.path.insert(0, c)
            from check_connectivity import check_connectivity as _cc  # type: ignore
            _CHECK_FUNC = _cc
            return _cc
    raise ImportError(
        "check_connectivity.py not found in any of: " + ", ".join(candidates))


def is_connectivity_preserved(golden_json_path: str,
                              modified_script_path: str,
                              design_type: str) -> bool:
    """True when the checker reports that connectivity is preserved.

    The argument order matches check_connectivity() itself. Anything else,
    including a missing checker, a raised exception, or an unexpected result
    shape, is reported as False.
    """
    try:
        cc = _resolve_check_connectivity()
    except ImportError:
        return False
    try:
        result = cc(golden_json_path, modified_script_path, design_type)
    except Exception:
        return False
    if not isinstance(result, dict):
        return False
    return bool(result.get("connectivity_preserved", False))
