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

"""Run configuration and ablation semantics.

The agent tree is bind-mounted read-only into the container and only a few
environment variables are forwarded to it, so the ablation switch cannot
travel in through the environment. It lives instead in a plain key/value file
shipped alongside the code, ``agent/evodrc.conf``.

Every key resolves in the order: a non-empty ``os.environ`` entry, then a
non-empty ``evodrc.conf`` entry, then the built-in default. A run with no
config file resolves every key to those defaults, the production settings.
``resolve()`` writes each resolved key back into ``os.environ``, which is how
the values reach modules that read the environment directly and how every
leaf_runner subprocess inherits them.
"""

import os


CONF_BASENAME = "evodrc.conf"

# The single source for the evolution-policy vocabulary. Producers and
# consumers compare against these constants rather than bare strings, so a
# typo raises AttributeError instead of selecting the wrong ablation.
EVOLUTION_ON = "on"
EVOLUTION_FROZEN = "frozen"

PROMPT_EXP3 = "exp3"
PROMPT_LEGACY = "legacy"

_KEYS = ("ABLATION", "MAX_ITERS", "LEAF_CONCURRENCY", "EVODRC_PROMPT_MODE",
         "KNOW_CONCURRENCY", "KNOW_ATTEMPTS",
         "MAX_CONCURRENT_CALLS", "CALL_COOLDOWN_SECONDS",
         "CU_DRC", "CU_DELTA_LE0", "VIA_COMPETITION")

# These match seed.CLA_PROVENANCE and seed.COLD_START_PROVENANCE. They are
# spelled out again here rather than imported so this module stays free of
# intra-package dependencies.
_CLA_PROVENANCE = "cla seed"
_COLD_START_PROVENANCE = "cold-start ablation seed"

# The ablation table. Keys are the ABLATION values; each row is
#   seed_subdir | evolution | default max_iters | provenance | whole_design
_ABLATION_TABLE = {
    "":  ("cla",        EVOLUTION_ON,     5, _CLA_PROVENANCE,        False),
    "1": ("cold_start", EVOLUTION_ON,     5, _COLD_START_PROVENANCE, False),
    "2": ("cla",        EVOLUTION_FROZEN, 5, _CLA_PROVENANCE,        False),
    "3": ("cla",        EVOLUTION_ON,     5, _CLA_PROVENANCE,        True),
}

_DEFAULTS = {
    "ABLATION": "",
    "MAX_ITERS": "",                 # empty means derived from ABLATION
    "LEAF_CONCURRENCY": "5",
    "EVODRC_PROMPT_MODE": PROMPT_EXP3,
    "KNOW_CONCURRENCY": "2",
    "KNOW_ATTEMPTS": "2",
    # --- Global model-call throttle (agent/src/iter/throttle.py) ------------
    # A single gate covers unit repair and every knowledge call. 5 is the
    # concurrency the published experiments ran at; 0 means unlimited.
    "MAX_CONCURRENT_CALLS": "5",
    # Seconds a freed slot stays closed after a call completes; 0 disables the
    # cooldown. Two seconds is light in-container spacing.
    "CALL_COOLDOWN_SECONDS": "2",
    # Contested-unit DRC tournament (cu_drc.run_pool). '1' enables it.
    "CU_DRC": "1",
    # '1' loosens the tournament acceptance threshold from delta_total < 0
    # (strict improvement only) to delta_total <= 0, so a neutral candidate
    # also qualifies. The connectivity-preserved requirement is unchanged.
    "CU_DELTA_LE0": "1",
    # N-way isolated-cell DRC competition for shared via cells.
    "VIA_COMPETITION": "1",
}

_TRUE = ("1", "true", "yes", "on")
_FALSE = ("0", "false", "no", "off")


class RunConfig(object):
    """Resolved run configuration, held in a plain class so the config path
    depends on nothing beyond the standard library."""

    __slots__ = ("ablation", "max_iters", "leaf_concurrency", "prompt_mode",
                 "know_concurrency", "know_attempts", "seed_dir", "evolution",
                 "provenance", "whole_design", "conf_path",
                 "cu_drc", "cu_delta_le0", "via_competition",
                 "max_concurrent_calls", "call_cooldown_seconds")

    def __init__(self, ablation, max_iters, leaf_concurrency, prompt_mode,
                 know_concurrency, know_attempts, seed_dir, evolution,
                 provenance, whole_design, conf_path,
                 cu_drc=True, cu_delta_le0=True, via_competition=True,
                 max_concurrent_calls=5, call_cooldown_seconds=2.0):
        self.ablation = ablation
        self.max_iters = max_iters
        self.leaf_concurrency = leaf_concurrency
        self.prompt_mode = prompt_mode
        self.know_concurrency = know_concurrency
        self.know_attempts = know_attempts
        self.seed_dir = seed_dir
        self.evolution = evolution
        self.provenance = provenance
        self.whole_design = whole_design
        self.conf_path = conf_path
        self.cu_drc = cu_drc
        self.cu_delta_le0 = cu_delta_le0
        self.via_competition = via_competition
        self.max_concurrent_calls = max_concurrent_calls
        self.call_cooldown_seconds = call_cooldown_seconds

    def as_dict(self):
        return dict((k, getattr(self, k)) for k in self.__slots__)

    def __repr__(self):
        return "RunConfig({0})".format(self.as_dict())


def agent_dir():
    """Return the ``agent`` directory; this file lives at
    ``agent/src/iter/conf.py``."""
    here = os.path.dirname(os.path.abspath(__file__))       # agent/src/iter
    return os.path.dirname(os.path.dirname(here))           # agent


def conf_path():
    return os.path.join(agent_dir(), CONF_BASENAME)


def parse_conf_file(path):
    """Parse ``KEY=VALUE`` lines; a missing file returns ``{}`` rather than
    raising.

    ``#`` starts a comment and blank lines are ignored. There is no ``${VAR}``
    expansion -- the config is a flat, auditable list of keys."""
    out = {}
    if not (path and os.path.isfile(path)):
        return out
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh.read().splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            if key:
                out[key] = val.strip()
    return out


def _get(key, file_cfg):
    """Resolve one key: non-empty environment value, else non-empty file
    value, else the built-in default."""
    env_val = (os.environ.get(key) or "").strip()
    if env_val:
        return env_val
    file_val = (file_cfg.get(key) or "").strip()
    if file_val:
        return file_val
    return _DEFAULTS.get(key, "")


def _int(value, default):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _float(value, default):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _int_nonneg(value, default):
    """Parse an integer, treating a negative value as invalid rather than as a
    request for 'unlimited'.

    Clamping to 0 would fail open: for MAX_CONCURRENT_CALLS, 0 means
    unlimited, so a typo such as ``-1`` would disable the call cap. A negative
    value falls back to the default; only an explicit 0 keeps its meaning."""
    n = _int(value, default)
    return default if n < 0 else n


def _float_nonneg(value, default):
    """Float counterpart of :func:`_int_nonneg`; a negative value falls back
    to the default."""
    x = _float(value, default)
    return default if x < 0 else x


def _bool(value, default):
    """Accept 1/0, true/false, yes/no, on/off, case-insensitively.

    An unrecognised value falls back to ``default`` rather than raising: these
    keys are feature switches, and a typo should not abort a run that was
    meant to use the default anyway."""
    token = str(value if value is not None else "").strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    return default


def resolve(env_writeback=True):
    """Resolve the run configuration and, by default, write it back into
    ``os.environ`` so that modules reading the environment directly and every
    leaf subprocess observe the resolved values.

    Raises RuntimeError for an unknown ABLATION and for the ``legacy`` prompt
    mode combined with ``ABLATION=3``, since the legacy prompt branch ignores
    the whole-design data section and would inline the entire block."""
    cp = conf_path()
    file_cfg = parse_conf_file(cp)

    ablation = _get("ABLATION", file_cfg)
    if ablation not in _ABLATION_TABLE:
        raise RuntimeError(
            "ABLATION={0!r} is not one of '', '1', '2', '3' "
            "(config file: {1})".format(ablation, cp))
    seed_subdir, evolution, default_iters, provenance, whole = \
        _ABLATION_TABLE[ablation]

    prompt_mode = _get("EVODRC_PROMPT_MODE", file_cfg)
    if prompt_mode not in (PROMPT_EXP3, PROMPT_LEGACY):
        raise RuntimeError(
            "EVODRC_PROMPT_MODE={0!r} is not one of {1!r}, {2!r} "
            "(config file: {3})".format(prompt_mode, PROMPT_EXP3,
                                        PROMPT_LEGACY, cp))
    if prompt_mode == PROMPT_LEGACY and ablation == "3":
        raise RuntimeError(
            "EVODRC_PROMPT_MODE=legacy with ABLATION=3 is refused: the legacy "
            "prompt branch ignores the whole-design data section and would "
            "inline the ENTIRE block layout into the leaf prompt.")

    max_iters_raw = _get("MAX_ITERS", file_cfg)
    max_iters = _int(max_iters_raw, default_iters) if max_iters_raw \
        else default_iters
    if max_iters < 1:
        raise RuntimeError("MAX_ITERS must be >= 1, got {0!r}"
                           .format(max_iters_raw))

    leaf_conc = _int_nonneg(_get("LEAF_CONCURRENCY", file_cfg), 5)
    know_conc = max(1, _int_nonneg(_get("KNOW_CONCURRENCY", file_cfg), 2))
    know_attempts = max(1, _int_nonneg(_get("KNOW_ATTEMPTS", file_cfg), 2))

    # A negative value for either throttle key is invalid and falls back to
    # the default, never to "unlimited" or "no cooldown". An explicit 0 still
    # means unlimited calls, or no cooldown, respectively.
    max_calls = _int_nonneg(_get("MAX_CONCURRENT_CALLS", file_cfg), 5)
    cooldown = _float_nonneg(_get("CALL_COOLDOWN_SECONDS", file_cfg), 2.0)

    cu_drc = _bool(_get("CU_DRC", file_cfg), True)
    cu_delta_le0 = _bool(_get("CU_DELTA_LE0", file_cfg), True)
    via_comp = _bool(_get("VIA_COMPETITION", file_cfg), True)

    seed_dir = os.path.join(agent_dir(), "knowledge", seed_subdir)

    cfg = RunConfig(ablation=ablation, max_iters=max_iters,
                    leaf_concurrency=leaf_conc, prompt_mode=prompt_mode,
                    know_concurrency=know_conc, know_attempts=know_attempts,
                    seed_dir=seed_dir, evolution=evolution,
                    provenance=provenance, whole_design=whole, conf_path=cp,
                    cu_drc=cu_drc, cu_delta_le0=cu_delta_le0,
                    via_competition=via_comp,
                    max_concurrent_calls=max_calls,
                    call_cooldown_seconds=cooldown)

    if env_writeback:
        os.environ["ABLATION"] = cfg.ablation
        os.environ["MAX_ITERS"] = str(cfg.max_iters)
        os.environ["LEAF_CONCURRENCY"] = str(cfg.leaf_concurrency)
        os.environ["EVODRC_PROMPT_MODE"] = cfg.prompt_mode
        os.environ["KNOW_CONCURRENCY"] = str(cfg.know_concurrency)
        os.environ["KNOW_ATTEMPTS"] = str(cfg.know_attempts)
        # throttle.get_gate() builds the process-wide gate from os.environ and
        # schedule._run_one passes the whole environment to every leaf
        # subprocess, so this writeback is how the resolved throttle reaches
        # both.
        os.environ["MAX_CONCURRENT_CALLS"] = str(cfg.max_concurrent_calls)
        os.environ["CALL_COOLDOWN_SECONDS"] = repr(cfg.call_cooldown_seconds)
        # cu_drc.run_pool reads CU_DRC and CU_DELTA_LE0 from os.environ
        # directly, so the normalised '1'/'0' spelling below is how the
        # resolved values reach the tournament.
        os.environ["CU_DRC"] = "1" if cfg.cu_drc else "0"
        os.environ["CU_DELTA_LE0"] = "1" if cfg.cu_delta_le0 else "0"
        os.environ["VIA_COMPETITION"] = "1" if cfg.via_competition else "0"
    return cfg
