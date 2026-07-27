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

"""Initial population of the layered knowledge store from a source directory.

A source directory holds a ``main.md`` carrying the shared doctrine text plus
one ``<LAYER>.md`` file per layer. Two pre-built directories ship with the
agent: ``knowledge/cla``, which contains layers with accumulated repair
experience and is used by the main experiment and by ablations 2 and 3, and
``knowledge/cold_start``, which contains rules only and is used by ablation 1.

``ensure_seed()`` is the entry point the controller calls once per run, before
the iteration loop. Everything here is plain file work with no model calls;
source directories are only read, and a re-run of the same seed produces
byte-identical output.
"""

import os
import re
import sys

from . import layerdb

DOCTRINE_BEGIN = "<!-- BEGIN GATING-DOCTRINE"
DOCTRINE_END = "<!-- END GATING-DOCTRINE -->"

DEFAULT_CLA_DIR = os.path.join(layerdb._AGENT_DIR, "knowledge", "cla")
CLA_PROVENANCE = "cla seed"

DEFAULT_COLD_START_DIR = os.path.join(layerdb._AGENT_DIR, "knowledge",
                                      "cold_start")
COLD_START_PROVENANCE = "cold-start ablation seed"


def _log(msg):
    print("[seed] %s" % msg, flush=True)


def _fail(msg):
    """Log an error and raise RuntimeError rather than calling sys.exit, since
    the caller's top-level handler would read a SystemExit as a clean
    shutdown."""
    print("[seed] ERROR: %s" % msg, file=sys.stderr, flush=True)
    raise RuntimeError(msg)


_COLD_KNOWLEDGE_HEAD_RE = re.compile(r"^\[KNOWLEDGE\][ \t]*$", re.M)


def parse_cold_start_knowledge(text):
    """Return the ``[KNOWLEDGE]`` body of a source layer file, meaning
    everything after the first ``[KNOWLEDGE]`` heading line.

    Returns '' when the section is absent, which is the normal case for the
    cold-start set: it carries DRC rules and no prior experience."""
    m = _COLD_KNOWLEDGE_HEAD_RE.search(text or "")
    if not m:
        return ""
    return text[m.end():].lstrip("\n")


def seed_from_dir(src_dir, deck_map_path=None, layerdb_dir=None,
                  skill_dir=None, provenance=None, label="seed"):
    """Seed the layered knowledge store from a source directory.

      * ``main.md`` supplies the fixed doctrine section and must contain the
        gating-doctrine markers. Generated trailing sections (layer index,
        navigation, the cold-start comment) are stripped, so both a bare
        template and an already-served main.md are accepted;
      * one branch is created per ``<src_dir>/<LAYER>.md``; the filename stem
        names the layer and must be in ``layerdb.UNIVERSE``;
      * ``ensure_branch`` renders each layer's rules.txt from the deck map,
        and ``layerdb.write_knowledge`` re-pastes the rules section from that
        rules.txt, so the deck map is the sole source of the rules text;
      * the knowledge body comes from ``parse_cold_start_knowledge``;
      * main.md is rebuilt with an index covering every seeded layer.

    Source files are only read. The operation is deterministic and
    idempotent: repeating it produces byte-identical output, and rules.txt is
    never rewritten."""
    src_dir = os.path.abspath(src_dir)
    if layerdb_dir:
        os.environ["LAYERDB_DIR"] = os.path.abspath(layerdb_dir)
    if skill_dir:
        os.environ["SKILL_STORE_DIR"] = os.path.abspath(skill_dir)
    elif layerdb_dir and "SKILL_STORE_DIR" not in os.environ:
        os.environ["SKILL_STORE_DIR"] = os.path.join(
            os.path.dirname(os.path.abspath(layerdb_dir)), "skill")

    if not os.path.isdir(src_dir):
        _fail("%s dir not found: %s" % (label, src_dir))
    main_source = os.path.join(src_dir, "main.md")
    if not os.path.isfile(main_source):
        _fail("%s main.md not found: %s" % (label, main_source))
    files = sorted(f for f in os.listdir(src_dir)
                   if f.endswith(".md") and f != "main.md")
    if not files:
        _fail("%s dir %s contains no *.md layer files" % (label, src_dir))
    pairs = []                     # (layer, filename), validated against UNIVERSE
    for f in files:
        stem = f[:-3]
        if stem not in layerdb.UNIVERSE:
            _fail("%s file %s: stem %r is outside the framework "
                  "universe %s" % (label, f, stem, ",".join(layerdb.UNIVERSE)))
        pairs.append((stem, f))
    pairs.sort(key=lambda p: layerdb._layer_sort_key(p[0]))

    # -- doctrine section from the source main.md ----------------------------
    with open(main_source, "r", encoding="utf-8") as fh:
        part_a_text = fh.read()
    if not (part_a_text.startswith(DOCTRINE_BEGIN)
            and DOCTRINE_END in part_a_text):
        _fail("%s main.md must contain the complete gating-doctrine "
              "marker block" % label)
    # Strip template-provided trailing sections. "## LAYER INDEX" and
    # "## NAVIGATION" are placeholders for sections build_main_md regenerates
    # on every rebuild from live counts and the current layer set, so keeping
    # a static copy would duplicate them and let it go stale as knowledge
    # evolves.
    cut = len(part_a_text)
    for marker in ("\n<!-- Cold-start global knowledge",
                   "\n## LAYER INDEX", "\n## NAVIGATION"):
        idx = part_a_text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    part_a_text = part_a_text[:cut].rstrip("\n") + "\n"
    os.makedirs(layerdb.layerdb_root(), exist_ok=True)
    with open(layerdb.main_part_a_path(), "w", encoding="utf-8") as fh:
        fh.write(part_a_text)

    # Validate the deck map up front so a bad path fails before any branch is
    # written; ensure_branch re-reads it below.
    layerdb.load_deck_map(deck_map_path)

    # -- per-layer knowledge --------------------------------------------------
    written = {}
    for layer, fname in pairs:
        with open(os.path.join(src_dir, fname), "r",
                  encoding="utf-8") as fh:
            body = parse_cold_start_knowledge(fh.read())
        layerdb.ensure_branch(layer, deck_map_path=deck_map_path)
        kp = layerdb.write_knowledge(layer, body, provenance)
        written[layer] = kp
        _log("%s seeded %s (from %s; [KNOWLEDGE] body %d chars%s)"
             % (label, kp, fname, len(body), "" if body else " -- rules only"))

    main_md = layerdb.build_main_md()
    _log("rebuilt %s (INDEX lines updated:seed)" % main_md)

    layers = sorted(written, key=layerdb._layer_sort_key)
    _log("%s DONE: %d layer(s) seeded from %s: %s"
         % (label.upper(), len(layers), src_dir, ", ".join(layers)))
    return {"layers": layers,
            "main_part_a": layerdb.main_part_a_path(),
            "main_md": main_md,
            "src_main": main_source,
            "src_dir": src_dir}


def seed_cla(cla_dir=None, deck_map_path=None, layerdb_dir=None,
             skill_dir=None):
    """Seed from the pre-built starting-knowledge directory used by the main
    experiment and by ablations 2 and 3.

    It mixes layers derived from earlier repair experience with rules-only
    layers that fill in the rest of the universe."""
    return seed_from_dir(cla_dir or DEFAULT_CLA_DIR, deck_map_path,
                         layerdb_dir, skill_dir=skill_dir,
                         provenance=CLA_PROVENANCE, label="cla")


def seed_cold_start(cold_start_dir=None, deck_map_path=None,
                    layerdb_dir=None, skill_dir=None):
    """Seed ablation 1 from the cold-start directory, which supplies DRC rules
    and no prior repair experience."""
    return seed_from_dir(cold_start_dir or DEFAULT_COLD_START_DIR,
                         deck_map_path, layerdb_dir, skill_dir=skill_dir,
                         provenance=COLD_START_PROVENANCE, label="cold-start")


def ensure_seed(seed_dir, provenance, label="seed"):
    """Seed the store once at controller startup, doing nothing if it is
    already seeded.

    A store whose ``main.md`` exists is left untouched, because re-seeding
    would rewrite every knowledge file back to its seed body and discard the
    knowledge accumulated so far. Returns a dict describing what was done,
    with ``{"skipped": True}`` when the store was already seeded."""
    if os.path.isfile(layerdb.main_md_path()):
        _log("layerdb already seeded at %s -- skipping"
             % layerdb.main_md_path())
        return {"skipped": True, "main_md": layerdb.main_md_path(),
                "layers": layerdb.layers_present(), "src_dir": seed_dir}
    out = seed_from_dir(seed_dir,
                        deck_map_path=layerdb.default_deck_map_path(),
                        layerdb_dir=layerdb.layerdb_root(),
                        skill_dir=layerdb.skill_root(),
                        provenance=provenance, label=label)
    out["skipped"] = False
    return out
