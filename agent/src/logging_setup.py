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

"""Process-wide logger for the agent pipeline.

Log records go to stderr in a human-readable format, one line per key event,
tagged with the pipeline stage that emitted it. The surrounding host script
reads the same stream looking for three exact-prefix markers (``STATUS=``,
``TOKENS_JSON=``, ``RUNTIME_SECONDS=``) and ignores every other line, so
ordinary log output cannot interfere with them.
"""


import logging
import sys
from typing import Optional

_LOGGER_NAME = "src"


class _StageDefaultFilter(logging.Filter):
    """Give every record a ``stage`` attribute so the format string resolves."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "stage"):
            record.stage = "-"
        return True


def setup_logger(level: str = "INFO") -> logging.Logger:
    """Configure the shared stderr logger; later calls return the same one."""
    logger = logging.getLogger(_LOGGER_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, str(level).upper(), logging.INFO))
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(name)s.%(stage)s] %(message)s",
        datefmt="%H:%M:%S",
    ))
    h.addFilter(_StageDefaultFilter())
    logger.addHandler(h)
    logger.propagate = False
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(_LOGGER_NAME)


def stage_extra(stage: str) -> dict:
    """Build the ``extra`` mapping that tags a log record with a stage name."""
    return {"stage": stage}
