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

"""Container-local work root, and the lease on the shared scratch dirs.

The persist root sits on a bind mount, so anything written there is copied to
the host and becomes part of the published run record. Working files -- token
dumps, decomposition scratch, knowledge staging, the model's raw patch, runner
logs -- do not belong in that record, so this module places them under a work
root outside every bind mount (``/tmp/evodrc_work/<digest>`` by default),
where they are discarded with the container.

``_inject/`` stays under the persist root on purpose: the rendered prompt
names the injected files by absolute path, so relocating it would change the
prompt bytes. ``EVODRC_WORK_BASE`` is an environment variable rather than a
config key, so the work base cannot be pointed back at the bind mount.
"""

import hashlib
import os
import re
import shutil
import sys
import tempfile

from . import paths as _paths


# Outside every bind mount the container sets up.
DEFAULT_WORK_BASE = "/tmp/evodrc_work"

# The only entries a finished unit dir may contain; everything else at depth 1
# is swept into the work dir. ``ctx`` is kept whole and never recursed into.
UNIT_KEEP = ("ctx", "patch.json", "prompt.txt")

# Host-visible prefixes a work root may never live under.
_BLOCKED = ("/workspace/temp", "/workspace/result", "/workspace/score",
            "/workspace/logs", "/workspace/agent")

# Scratch dirs the rendered prompt names at the benchmark temp root. They are
# leased by atomic mkdir, and only what this process created is released.
_SCRATCH = ("conn", "drc")

# resolve_work_root refuses to remove anything whose basename is not one of
# these 12-hex-char digests, so the removal target cannot be work_base()
# itself, '/', or a hand-typed path.
_DIGEST_RE = re.compile(r"^[0-9a-f]{12}$")


def _warn(msg):
    try:
        sys.stderr.write(msg if msg.endswith("\n") else msg + "\n")
        sys.stderr.flush()
    except Exception:                                      # noqa: BLE001
        pass


def work_base():
    """Return the container-local base directory for all working files."""
    override = os.environ.get("EVODRC_WORK_BASE", "").strip()
    if override:
        return override
    return DEFAULT_WORK_BASE


def _norm(path):
    return os.path.abspath(path).rstrip(os.sep) or os.sep


def _is_under(child, parent):
    """True if ``child`` lies under ``parent`` on a path-component boundary."""
    c = _norm(child)
    p = _norm(parent)
    if c == p:
        return True
    return c.startswith(p + os.sep if p != os.sep else os.sep)


def assert_disjoint(work_path, published_path):
    """Raise unless the two trees are strictly disjoint.

    Equality, work-under-published and published-under-work are all fatal:
    each would either put working files back inside the published record, or
    put the published record inside a tree that later gets removed.
    """
    w = _norm(work_path)
    p = _norm(published_path)
    if w == p:
        raise RuntimeError(
            "work path and published path are the SAME dir: {0}".format(w))
    if _is_under(w, p):
        raise RuntimeError(
            "work path {0} is INSIDE the published tree {1} -- internal files "
            "would be dumped to the host".format(w, p))
    if _is_under(p, w):
        raise RuntimeError(
            "published tree {0} is INSIDE the work path {1} -- the published "
            "record would be wiped with the work root".format(p, w))


def work_root_for(persist_root):
    """Return the work root matching ``persist_root``.

    Pure: it creates and removes nothing, so the path can be recomputed after
    a run to inspect what was swept there.
    """
    digest = hashlib.sha1(
        os.path.realpath(persist_root).encode("utf-8")).hexdigest()[:12]
    return os.path.join(work_base(), digest)


def resolve_work_root(persist_root):
    """Create and return a fresh work root for this run.

    Guards, in order: the base may not sit under a bind mount; the work root
    and the persist root must be disjoint; and the directory about to be
    removed must carry a 12-hex-char digest name.
    """
    base = work_base()
    nbase = _norm(base)
    for bad in _BLOCKED:
        if _is_under(nbase, bad):
            raise RuntimeError(
                "EVODRC_WORK_BASE={0} is inside the host-visible mount {1} -- "
                "working files would be dumped to the host".format(base, bad))
    root = work_root_for(persist_root)
    assert_disjoint(root, persist_root)
    leaf = os.path.basename(_norm(root))
    if not _DIGEST_RE.match(leaf):
        raise RuntimeError(
            "refusing to reset work root {0}: its basename {1!r} is not a "
            "12-hex-char digest".format(root, leaf))
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    return root


def iter_work_dir(work_root, iter_index):
    """Create and return ``<work_root>/iter{i}``."""
    d = os.path.join(work_root, "iter{0}".format(iter_index))
    if not os.path.isdir(d):
        os.makedirs(d)
    return d


def unit_work_dir(iter_work, unit_id):
    """Create and return ``<iter_work>/unit/<unit_id>`` plus its ``_calls``
    subdirectory.

    ``unit_id`` goes through the same sanitizer the persist tree uses, so an
    odd unit id cannot escape the directory via ``..``.
    """
    token = _paths._safe_component(unit_id, "unit")
    d = os.path.join(iter_work, "unit", token)
    calls = os.path.join(d, "_calls")
    if not os.path.isdir(calls):
        os.makedirs(calls)
    return d


def _collision_free(dest):
    """Return ``dest``, or ``dest.1`` / ``dest.2`` / ... if it is taken."""
    if not os.path.exists(dest) and not os.path.islink(dest):
        return dest
    i = 1
    while True:
        cand = "{0}.{1}".format(dest, i)
        if not os.path.exists(cand) and not os.path.islink(cand):
            return cand
        i += 1


def sweep_unit(out_dir, *, unit_work):
    """Move every depth-1 entry of ``out_dir`` that is not in UNIT_KEEP.

    ``unit_work`` is keyword-only with no default because both arguments are
    directory paths of the same type, making omission or transposition easy
    and a defaulted value unsafe.

    Entries move to ``<unit_work>/swept/`` rather than being deleted: the
    model can create arbitrary files, and losing one would be worse than
    finding it in an unexpected place. ``ctx/`` is kept whole and never
    recursed into, and colliding names are renamed. The operation is
    idempotent, so running it twice is harmless.

    Returns the list of moved basenames.
    """
    if not unit_work:
        raise RuntimeError(
            "sweep_unit requires an explicit unit_work dir; refusing to "
            "guess (a defaulted safety knob fails open)")
    assert_disjoint(unit_work, out_dir)
    if not os.path.isdir(out_dir):
        return []
    moved = []
    dest_root = os.path.join(unit_work, "swept")
    for name in sorted(os.listdir(out_dir)):
        if name in UNIT_KEEP:
            continue
        src = os.path.join(out_dir, name)
        if not os.path.isdir(dest_root):
            os.makedirs(dest_root)
        shutil.move(src, _collision_free(os.path.join(dest_root, name)))
        moved.append(name)
    return moved


# ---------------------------------------------------------------------------
# Base-scratch lease
#
# The rendered prompt names <benchmark temp>/conn and <benchmark temp>/drc to
# the model, so those two directories sit at the shared benchmark temp root,
# outside the persist tree. They are claimed by atomic os.mkdir and only what
# this process created is released, so a concurrent run's directories and
# files stay exactly where they are.
# ---------------------------------------------------------------------------

def base_scratch_allowed(base):
    """True if scratch dirs may be leased at ``base``.

    The machine's shared temp directory is refused first and unconditionally:
    with EVODRC_PERSIST_BASE unset and no ``/workspace/temp``, the persist base
    resolves to ``tempfile.gettempdir()``, and claiming names as generic as
    ``conn`` and ``drc`` in the shared temp dir would collide with other
    software.
    """
    b = os.path.abspath(base)
    if b == os.path.abspath(tempfile.gettempdir()):
        return False
    if b == "/workspace/temp" and os.path.isdir("/workspace/temp"):
        return True
    override = os.environ.get("EVODRC_PERSIST_BASE", "").strip()
    return bool(override) and os.path.abspath(override) == b


def claim_base_scratch(base):
    """Atomically claim ``conn`` and ``drc`` at ``base``, returning the names
    this call created.

    ``os.mkdir`` fails when another run -- or an earlier killed one -- got
    there first, in which case the name belongs to that run and this one leaves
    it alone. Exactly one process can win each name.
    """
    if not base_scratch_allowed(base):
        return ()
    owned = []
    for name in _SCRATCH:
        try:
            os.mkdir(os.path.join(base, name))
        except OSError:
            continue
        owned.append(name)
    return tuple(owned)


def release_base_scratch(base, owned, *, dest):
    """Move the owned directories out of ``base`` and into ``dest``.

    Only names in ``owned`` are touched, so directories and files belonging to
    a concurrent run survive. A symlink where the owned directory was expected
    is left alone.

    Returns the list of released names.
    """
    if not owned:
        return []
    if not dest:
        raise RuntimeError(
            "release_base_scratch requires an explicit dest dir; refusing to "
            "guess")
    released = []
    for name in owned:
        src = os.path.join(base, name)
        if os.path.islink(src) or not os.path.isdir(src):
            continue
        if not os.path.isdir(dest):
            os.makedirs(dest)
        try:
            shutil.move(src, _collision_free(os.path.join(dest, name)))
        except Exception as exc:                           # noqa: BLE001
            _warn("evodrc: could not release base scratch {0}: {1}".format(
                src, exc))
            continue
        released.append(name)
    return released
