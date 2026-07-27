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

"""Staging of the knowledge files the prompts point at, plus an audit manifest.

Prompts name the knowledge files by absolute path rather than inlining them,
so that path has to stay the same across iterations. A single directory,
``<PERSIST_ROOT>/_inject``, is refreshed in place from the current knowledge
store at the start of every iteration. It is kept separate from the store's
own ``skill`` and ``db`` directories, whose file names would collide and whose
contents are hashed as a change-detection handle.

Each iteration also gets a copy under ``<iter_dir>/input/`` for the record,
but prompts keep pointing at ``_inject``. Staging only copies files: it never
rebuilds main.md or changes the index prefix, so a frozen knowledge store
produces byte-identical staged output every iteration.
"""

import hashlib
import json
import os
import shutil

from . import layerdb


def inject_dir(persist_root):
    """Return the injection directory, which is the same for every iteration
    of a run."""
    return os.path.join(persist_root, "_inject")


def _sha256_bytes(data):
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _file_entry(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return {"sha256": None, "bytes": None, "missing": True}
    return {"sha256": _sha256_bytes(data), "bytes": len(data)}


def db_tree_sha256(persist_root):
    """Hash the whole ``<PERSIST_ROOT>/db`` tree into one string.

    The hash covers a sorted listing of ``<relpath>\\0<file sha256>`` entries,
    so it moves both when any file's bytes change and when a file appears or
    disappears. That makes it a single handle for checking whether the
    knowledge store stayed frozen across a run."""
    root = os.path.join(persist_root, "db")
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root)
            try:
                with open(p, "rb") as fh:
                    rows.append(rel + "\0" + _sha256_bytes(fh.read()))
            except OSError:
                rows.append(rel + "\0<unreadable>")
    return _sha256_bytes("\n".join(sorted(rows)).encode("utf-8"))


def _write_manifest(persist_root, info, *, work_dir):
    """Write ``<work_dir>/inject_manifest.json``, recording the hashes of the
    staged files and of the knowledge store.

    This is an internal audit artifact and stays out of the published run
    record, which is why ``work_dir`` is required and keyword-only rather than
    defaulting to the published iteration directory.
    """
    kdir = info.get("knowledge_dir") or ""
    knowledge = {}
    for layer in (info.get("layers") or []):
        knowledge[layer] = _file_entry(os.path.join(kdir, "%s.md" % layer))
    doc = {
        "main": _file_entry(info.get("main") or ""),
        "official": _file_entry(info.get("official") or ""),
        "alias": _file_entry(info.get("alias") or ""),
        "knowledge": knowledge,
        "knowledge_dir": kdir,
        "index_prefix": layerdb.index_prefix(),
        "db_tree_sha256": db_tree_sha256(persist_root),
    }
    path = os.path.join(work_dir, "inject_manifest.json")
    try:
        os.makedirs(work_dir, exist_ok=True)
    except OSError:
        pass
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return path


def _mirror_into_input(iter_dir, info):
    """Copy the staged injection into ``<iter_dir>/input/`` for the record.

    The published tree carries the staged main.md, skill file and per-layer
    knowledge files in every iteration's ``input/``. These copies are records
    only: prompt paths keep pointing at ``_inject``, because main.md's layer
    index embeds absolute paths that must not move between iterations."""
    in_dir = os.path.join(iter_dir, "input")
    try:
        os.makedirs(in_dir, exist_ok=True)
    except OSError:
        return
    for key in ("official", "main", "alias"):
        src = info.get(key) or ""
        if src and os.path.isfile(src):
            try:
                shutil.copyfile(src, os.path.join(in_dir,
                                                  os.path.basename(src)))
            except OSError:
                pass
    kdir = info.get("knowledge_dir") or ""
    if kdir and os.path.isdir(kdir):
        dest = os.path.join(in_dir, "knowledge")
        try:
            os.makedirs(dest, exist_ok=True)
        except OSError:
            return
        for layer in (info.get("layers") or []):
            src = os.path.join(kdir, "%s.md" % layer)
            if os.path.isfile(src):
                try:
                    shutil.copyfile(src, os.path.join(dest, "%s.md" % layer))
                except OSError:
                    pass


def stage(persist_root, iter_dir, *, work_dir):
    """Refresh the injection directory from the current knowledge store, copy
    it into ``<iter_dir>/input/`` for the record and write the audit manifest.

    Returns ``layerdb.build_injection``'s dict of staged paths, extended with
    ``manifest`` and ``dir``. Every path in it refers to the stable ``_inject``
    directory, never to the per-iteration copy.

    ``_inject`` stays at the persist root even though it is a staging area,
    because the rendered prompt names its files by absolute path and moving it
    would change the prompt text. ``work_dir`` receives only the manifest,
    which no prompt reads."""
    d = inject_dir(persist_root)
    os.makedirs(d, exist_ok=True)
    info = layerdb.build_injection(d)          # copies only; never rebuilds main.md
    info = dict(info)
    info["dir"] = d
    _mirror_into_input(iter_dir, info)
    info["manifest"] = _write_manifest(persist_root, info, work_dir=work_dir)
    return info
