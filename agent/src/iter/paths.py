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

"""Persist-root resolution, iteration directories, ASCII sanitize and clamp.

Iteration artifacts are written under the ``/workspace/temp`` bind-mount so
they survive the pipeline script's cleanup of its own temp directory. The
resolved root is ``<base>/data/<EXP>/<CASE>/<MODEL>/``, matching the layout of
the published experiment data; ``<EXP>`` comes from the ABLATION setting
('' -> evodrc, '1' -> ablation1, and so on).

The path is deterministic -- no timestamp, no process id -- so re-running the
same case overwrites the previous run. ``resolve_persist_root`` clears the
whole root and ``ensure_fresh_iter_dir`` clears each ``iter{i}/``; copy a run
aside to keep it. Nothing is written under the read-only agent tree.
"""

import os
import re
import shutil
import tempfile


# Default clamp for persisted free text: leaf_runner passes trace.md through
# clamp_text so a runaway narration cannot bloat the persisted directory. It
# bounds persisted text only; injected knowledge reaches the prompt by path
# rather than inlined, and arrives whole.
KNOWLEDGE_MAX_CHARS = 3800


def _persist_base():
    """Resolve the base directory that lands on the host bind-mount.

    Tried in order: the EVODRC_PERSIST_BASE environment override, the
    ``/workspace/temp`` bind-mount, then the system temp directory as a
    fallback for running outside a container.
    """
    override = os.environ.get("EVODRC_PERSIST_BASE", "").strip()
    if override:
        return override
    if os.path.isdir("/workspace/temp"):
        return "/workspace/temp"
    return tempfile.gettempdir()


def persist_base():
    """Public alias for the resolved persist base.

    The controller needs it to lease the ``conn`` and ``drc`` scratch dirs
    that the rendered prompt places at the benchmark temp root, one level
    above the persist root.
    """
    return _persist_base()


# ABLATION value -> the experiment folder name used by the published data tree.
_EXP_BY_ABLATION = {
    "": "evodrc",
    "1": "ablation1",
    "2": "ablation2",
    "3": "ablation3",
}

_SAFE_COMPONENT_RE = re.compile(r"[^A-Za-z0-9._-]+")


def experiment_name(ablation):
    """Map an ABLATION value to its published experiment folder name.

    Raises RuntimeError on an unknown key rather than defaulting to
    ``evodrc``, which would file an ablation run's results under the main
    experiment. conf.resolve() rejects unknown values too, so this is a
    second, independent guard."""
    key = "" if ablation is None else str(ablation).strip()
    if key not in _EXP_BY_ABLATION:
        raise RuntimeError(
            "ABLATION={0!r} has no experiment folder name (expected one of "
            "'', '1', '2', '3')".format(ablation))
    return _EXP_BY_ABLATION[key]


def _safe_component(value, fallback):
    """Reduce ``value`` to a single safe path component.

    Everything outside ``[A-Za-z0-9._-]`` collapses to ``_``, and the result
    is never ``''``, ``'.'`` or ``'..'``, so an odd case or model name cannot
    escape the data root or resolve to its parent directory, which
    ``resolve_persist_root`` would then remove."""
    token = _SAFE_COMPONENT_RE.sub("_", str(value if value is not None else ""))
    token = token.strip()
    if token in ("", ".", ".."):
        return fallback
    return token


def resolve_persist_root(case_name, model_name, ablation, reset=True):
    """Create and return the persist root for this run.

    The path is ``<base>/data/<EXP>/<CASE>/<MODEL>``, matching the published
    experiment data. It carries no run tag, so repeating a case lands in the
    same folder.

    With ``reset`` (the default) the whole root is removed first. A partial
    wipe would be incorrect: ``seed.ensure_seed`` skips seeding whenever the
    knowledge store already exists, so leaving ``db/`` behind would resume the
    previous run's evolved knowledge, and leaving ``iter{N}/`` behind would
    strand iterations from a longer prior run in this run's record. The
    ``!= base`` guard prevents removing the bind-mount itself."""
    base = _persist_base()
    root = os.path.join(base, "data", experiment_name(ablation),
                        _safe_component(case_name, "case"),
                        _safe_component(model_name, "model"))
    if reset and os.path.isdir(root) and \
            os.path.abspath(root) != os.path.abspath(base):
        shutil.rmtree(root)
    os.makedirs(root, exist_ok=True)
    return root


def ensure_fresh_iter_dir(persist_root, iter_index):
    """Return an empty ``<persist_root>/iter{i}`` along with its ``input/``
    subdirectory.

    An existing directory is replaced rather than refused: because the persist
    root is deterministic, refusing would make every repeat run of a case
    fail."""
    d = os.path.join(persist_root, "iter{0}".format(iter_index))
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    os.makedirs(os.path.join(d, "input"))
    return d


def leaf_dir(iter_dir, leaf_id):
    """Create and return ``<iter_dir>/leaf/<leaf_id>``.

    The ``leaf/`` level matches the published tree, which nests every repair
    unit -- leaf, union and whole-design alike -- beneath it. ``leaf_id``
    already carries its own prefix (for example ``leaf_0006``,
    ``Block5_union_row3``, ``whole_design``), so the folder takes that name
    verbatim.

    This directory is published, so nothing else is created here; per-call
    token capture stays container-local under the work dir (iter/workdir.py)."""
    d = os.path.join(iter_dir, "leaf", leaf_id)
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# ASCII sanitize and size clamp
# ---------------------------------------------------------------------------

# A few common Unicode -> ASCII transliterations so the sanitizer keeps the
# meaning of a symbol instead of dropping it. Everything else falls through to
# the ascii('replace') pass below.
_UNICODE_MAP = {
    "–": "-", "—": "--", "−": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "…": "...", "±": "+/-", "µ": "u", "μ": "u",
    "δ": "delta", "Ω": "ohm", "°": "deg", "×": "x",
    "≤": "<=", "≥": ">=", "≠": "!=", "→": "->",
    " ": " ",
}


def ascii_sanitize(text):
    """Return an ASCII-only version of ``text``.

    Known symbols are transliterated; any remaining non-ASCII byte becomes a
    single space, so the result is pure 7-bit ASCII.

    Note that encode('ascii', 'replace') marks non-ASCII as '?' and the final
    replacement of '?' is unconditional, so a question mark already present in
    the input also becomes a space. Use textutil.ascii_sanitize where that
    matters."""
    if not text:
        return ""
    s = str(text)
    for k, v in _UNICODE_MAP.items():
        if k in s:
            s = s.replace(k, v)
    # Replace any leftover non-ASCII with a space.
    out = s.encode("ascii", "replace").decode("ascii").replace("?", " ")
    return out


def clamp_text(text, max_chars=KNOWLEDGE_MAX_CHARS):
    """Clamp ``text`` to at most ``max_chars``, counting the single trailing
    newline it always appends.

    One character is reserved for that newline, and the cut prefers a line
    boundary so the result stays readable."""
    body = (text or "").rstrip()
    limit = max_chars - 1
    if len(body) > limit:
        cut = body[:limit]
        nl = cut.rfind("\n")
        if nl > 0:
            cut = cut[:nl]
        body = cut.rstrip()
    doc = body + "\n"
    if len(doc) > max_chars:        # safety net; the slice above already fits
        doc = doc[:max_chars]
    return doc
