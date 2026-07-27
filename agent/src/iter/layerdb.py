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

"""Per-layer knowledge database backed by plain files.

Each framework layer (M1..M7, V0..V6) owns a branch under ``<root>/db/layerdb``
holding an immutable ``rules.txt`` rendered once from the deck map, an
append-only ``history.jsonl`` of measured records, and a ``_meta.json``. A
layer's current knowledge text lives separately as ``<LAYER>.md`` and is
rewritten with the rules section re-pasted, so generated text can never
overwrite the rules. ``main.md`` indexes the branches and ``build_injection``
stages the whole set where the prompts read it. No model calls, only files.
"""

import json
import hashlib
import os
import re
import sys
import tempfile
from datetime import datetime, timezone

# agent/src/iter/layerdb.py -> the agent directory, mounted read-only.
_AGENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# Writable state root. The agent directory is mounted read-only, so the store
# roots come from a module-level cell the controller sets at startup. The last
# fallback is the system temp dir, so no resolution path can land inside the
# read-only mount.
# ---------------------------------------------------------------------------
_STORE_ROOT = [None]


def set_store_root(path):
    """Point the layer database and the skill store at ``path``."""
    _STORE_ROOT[0] = path


def store_root():
    return (os.environ.get("EVODRC_KNOWLEDGE_ROOT")
            or _STORE_ROOT[0]
            or os.path.join(tempfile.gettempdir(), "evodrc_knowledge"))


# The framework layer universe; branches exist only for these.
METALS = tuple("M%d" % i for i in range(1, 8))
CUTS = tuple("V%d" % i for i in range(0, 7))
UNIVERSE = METALS + CUTS

# The directory the INDEX lines point at. A settable cell, so the index can
# name the stable injection directory the leaf prompts reference by absolute
# path.
_INDEX_PREFIX = ["/work/in/knowledge"]


def set_index_prefix(path):
    """Set the absolute directory the INDEX lines point at.

    Called once, before seeding, so the index lines main.md is born with are
    already final; rebuilding main.md later under a different prefix would
    change bytes that are expected to stay fixed."""
    _INDEX_PREFIX[0] = str(path).rstrip("/")


def index_prefix():
    return os.environ.get("EVODRC_INDEX_PREFIX") or _INDEX_PREFIX[0]


INDEX_LINE_FMT = "- %s -> %s/%s.md  ops:%d  updated:%s"


def index_line_re():
    """The INDEX line grammar, compiled against the current prefix."""
    return re.compile(
        r"^- (M[1-7]|V[0-6]) -> " + re.escape(index_prefix())
        + r"/(M[1-7]|V[0-6])\.md  ops:\d+  updated:(seed|iter\d+)$")

_UPDATED_TAG_RE = re.compile(r"<!-- layerdb: updated=(seed|iter\d+) ")
_ITER_IN_PROV_RE = re.compile(r"\biter(\d+)\b")

# The fixed three-step navigation instruction; never generated text.
NAVIGATION_TEXT = (
    "1. Map each violation's rule name to its layers: the layer tokens "
    "(M*/V*) in the rule name -- at most 2; both appear in the crop's rule "
    "descriptions.\n"
    "2. Read ONLY those layers' knowledge files at the INDEX paths above.\n"
    "3. No other knowledge discovery: the INDEX paths are the complete "
    "navigation.")

# The only top-level files build_injection stages, alongside the per-branch
# copies under knowledge/.
INJECTION_WHITELIST = ("skill_official.md", "main.md", "knowledge.md")

# The run scripts only check that knowledge.md exists and pass it as
# --knowledge, so a short pointer file is enough to keep them working.
def alias_stub_text():
    """The pointer-file text, resolved against the current injection prefix."""
    return ("# DEPRECATED alias (layerdb cutover, LAYERDB_PLAN_v1 1.7)\n"
            "Knowledge now lives at %s; see its LAYER INDEX for the\n"
            "per-layer files under %s/.\n"
            % (os.path.join(os.path.dirname(index_prefix()), "main.md"),
               index_prefix()))


def _skill_md():
    """The skill file staged as ``skill_official.md``: the EVODRC_SKILL_MD
    environment variable when set, otherwise ``<agent>/skill.md``."""
    return (os.environ.get("EVODRC_SKILL_MD")
            or os.path.join(_AGENT_DIR, "skill.md"))


def _warn(msg):
    print("[layerdb] WARNING: %s" % msg, file=sys.stderr, flush=True)


def layerdb_root():
    """Storage root: the LAYERDB_DIR variable, else ``store_root()/db``."""
    return os.environ.get("LAYERDB_DIR") or os.path.join(store_root(), "db")


def skill_root():
    """Per-layer knowledge store: the SKILL_STORE_DIR variable, else
    ``store_root()/skill``."""
    return (os.environ.get("SKILL_STORE_DIR")
            or os.path.join(store_root(), "skill"))


def default_deck_map_path():
    """The deck map shipped inside the agent directory. It is read from a
    read-only mount and is never written."""
    return os.path.join(_AGENT_DIR, "knowledge", "deck_map.json")


def load_deck_map(path=None):
    p = path or default_deck_map_path()
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _layer_sort_key(layer):
    """Sort key placing M1..M7 first, then V0..V6."""
    return (0 if layer.startswith("M") else 1, int(layer[1:]))


def branch_dir(layer):
    return os.path.join(layerdb_root(), "layerdb", layer)


def history_path(layer):
    return os.path.join(branch_dir(layer), "history.jsonl")


def rules_path(layer):
    return os.path.join(branch_dir(layer), "rules.txt")


def knowledge_path(layer):
    return os.path.join(skill_root(), "%s.md" % layer)


# ---------------------------------------------------------------------------
# rules.txt rendering, lazy and write-once
# ---------------------------------------------------------------------------
def render_rules(layer, deck_map):
    """Render the rule text for one layer.

    Emits the layer's rule stanzas verbatim in deck order, each headed by
    ``# RULE <name> (deck lines a-b)``, adds the helper definitions when a
    stanza calls offgrid_cl or ongrid_ep, and always appends the
    nonorthogonal block. Blocks are ordered by their deck start line."""
    blocks = []          # (start_lineno, text)
    needs_helper = False
    for name in sorted(deck_map["rules"]):
        entry = deck_map["rules"][name]
        if layer not in entry.get("layers", []):
            continue
        lines = entry["lines"]
        start = lines[0]["lineno"]
        end = lines[-1]["lineno"]
        stanza = ["# RULE %s (deck lines %d-%d)" % (name, start, end)]
        stanza += [o["text"] for o in lines]
        blocks.append((start, "\n".join(stanza)))
        if entry.get("needs_helper_defs"):
            needs_helper = True
    if needs_helper:
        h = deck_map["snippets"]["helper_defs"]
        blocks.append((h["start"],
                       "# HELPER DEFS (deck lines %d-%d) -- offgrid_cl / "
                       "ongrid_ep definitions required by AUX rules\n%s"
                       % (h["start"], h["end"], h["text"])))
    nb = deck_map["snippets"]["nonortho_block"]
    blocks.append((nb["start"],
                   "# NONORTHOGONAL BLOCK (deck lines %d-%d) -- applies to "
                   "every layer\n%s" % (nb["start"], nb["end"], nb["text"])))
    blocks.sort(key=lambda b: b[0])
    return "\n\n".join(t for _s, t in blocks) + "\n"


def ensure_branch(layer, deck_map_path=None):
    """Create the branch for ``layer`` if it does not exist and return its
    directory.

    Idempotent: an existing rules.txt is never rewritten. A deck change is
    detected through the deck hash in _meta.json and only warned about. An
    empty knowledge file is bootstrapped when none is present, so every
    existing branch always has one."""
    if layer not in UNIVERSE:
        raise ValueError("layer %r outside framework universe %s"
                         % (layer, ",".join(UNIVERSE)))
    bdir = branch_dir(layer)
    rp = rules_path(layer)
    meta_p = os.path.join(bdir, "_meta.json")
    deck_map = load_deck_map(deck_map_path)
    if os.path.isfile(rp):
        try:
            with open(meta_p, "r", encoding="utf-8") as fh:
                meta = json.load(fh)
        except (OSError, ValueError):
            meta = {}
        have = meta.get("deck_sha256")
        cur = deck_map.get("deck_sha256")
        if have and cur and have != cur:
            _warn("deck sha mismatch for branch %s: rules.txt was rendered "
                  "from deck %s but deck_map.json now says %s -- rules.txt "
                  "NOT rewritten (immutable); regenerate the layerdb in a "
                  "fresh STATE_DIR if the deck really changed"
                  % (layer, have[:12], cur[:12]))
    else:
        os.makedirs(bdir, exist_ok=True)
        rules_text = render_rules(layer, deck_map)
        with open(rp, "w", encoding="utf-8") as fh:
            fh.write(rules_text)
        meta = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "rules_sha256": hashlib.sha256(
                rules_text.encode("utf-8")).hexdigest(),
            "deck_sha256": deck_map.get("deck_sha256", ""),
        }
        with open(meta_p, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2, sort_keys=True)
            fh.write("\n")
    # Every existing branch always has a knowledge file.
    if not os.path.isfile(knowledge_path(layer)):
        write_knowledge(layer, "", "bootstrap")
    return bdir


# ---------------------------------------------------------------------------
# history.jsonl, append-only and immutable
# ---------------------------------------------------------------------------
def append_records(layer, records):
    """Append one compact JSON line per record, then flush and fsync.

    The same record dict is passed for every layer it touches; sorted-key
    serialisation makes the per-branch copies byte-identical."""
    if not records:
        return 0
    ensure_branch(layer)
    hp = history_path(layer)
    with open(hp, "a", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, sort_keys=True,
                                separators=(",", ":")) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return len(records)


def read_history(layer):
    """Parse the branch's history.jsonl. An unparsable line raises, because in
    an append-only file it means corruption rather than schema drift."""
    hp = history_path(layer)
    if not os.path.isfile(hp):
        return []
    out = []
    with open(hp, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            try:
                out.append(json.loads(line))
            except ValueError:
                raise ValueError(
                    "corrupt history.jsonl (%s line %d): %r"
                    % (hp, n, line[:120]))
    return out


def read_iter_records(layer, iter_i):
    return [r for r in read_history(layer) if r.get("iter") == iter_i]


def trial_ids(layer):
    return {r.get("trial_id") for r in read_history(layer)}


# ---------------------------------------------------------------------------
# Applied loci and staleness annotation
# ---------------------------------------------------------------------------
def loci_path():
    return os.path.join(layerdb_root(), "loci.jsonl")


def read_loci():
    lp = loci_path()
    if not os.path.isfile(lp):
        return []
    out = []
    with open(lp, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh.read().splitlines(), 1):
            try:
                out.append(json.loads(line))
            except ValueError:
                raise ValueError("corrupt loci.jsonl line %d: %r"
                                 % (n, line[:120]))
    return out


def record_applied_loci(iter_i, loci):
    """Append one line per iteration, ``{"iter": i, "loci": [[x0,y0,x1,y1],
    ...]}``. Idempotent on resume: an iteration already recorded is never
    appended twice."""
    if any(e.get("iter") == iter_i for e in read_loci()):
        return False
    os.makedirs(layerdb_root(), exist_ok=True)
    entry = {"iter": iter_i,
             "loci": [[int(v) for v in b] for b in (loci or [])]}
    with open(loci_path(), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True,
                            separators=(",", ":")) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return True


def _bbox_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def annotate_staleness(records):
    """Return copies of the records carrying a ``locus_status`` field.

    The stored history is never rewritten; the field is added when records are
    read::

      UNTOUCHED       no later iteration's applied locus intersects this one
      SINCE-MODIFIED  a later applied locus overlaps this record's locus
      UNKNOWN         the record has no locus
    """
    loci_entries = read_loci()
    out = []
    for rec in records:
        r = dict(rec)
        locus = rec.get("locus")
        if not locus:
            r["locus_status"] = "UNKNOWN"
        else:
            later = [b for e in loci_entries
                     if e.get("iter", 0) > rec.get("iter", 0)
                     for b in e.get("loci", [])]
            r["locus_status"] = ("SINCE-MODIFIED"
                                 if any(_bbox_overlap(locus, b)
                                        for b in later) else "UNTOUCHED")
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Quarantine for records with no mappable framework layer
# ---------------------------------------------------------------------------
def unmapped_path():
    return os.path.join(layerdb_root(), "_unmapped.jsonl")


def append_unmapped(record):
    """Append a record that maps to no framework layer.

    It lands beside the branches rather than inside one, so it has no branch
    directory, no rules.txt, no index line and no staged copy, and stays
    invisible to the per-layer counts, ``layers_present`` and
    ``build_injection``."""
    os.makedirs(layerdb_root(), exist_ok=True)
    with open(unmapped_path(), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True,
                            separators=(",", ":")) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


# ---------------------------------------------------------------------------
# Knowledge files
# ---------------------------------------------------------------------------
def _updated_tag(provenance):
    m = _ITER_IN_PROV_RE.search(provenance or "")
    return "iter%d" % int(m.group(1)) if m else "seed"


def write_knowledge(layer, knowledge_body, provenance):
    """Write the layer's knowledge file: the [DRC RULES] section re-pasted
    from the branch's rules.txt, followed by the given [KNOWLEDGE] body.

    A body containing a [DRC RULES] heading is refused, so generated text can
    never overwrite the rules section."""
    body = knowledge_body or ""
    if "[DRC RULES]" in body:
        raise ValueError(
            "knowledge body for %s contains a [DRC RULES] heading -- "
            "assembly refuses (rules are harness-pasted only)" % layer)
    rp = rules_path(layer)
    if not os.path.isfile(rp):
        raise FileNotFoundError(
            "rules.txt missing for %s -- ensure_branch first" % layer)
    with open(rp, "r", encoding="utf-8") as fh:
        rules_text = fh.read()
    prov = " ".join((provenance or "").split()).replace("-->", "-]")
    tag = _updated_tag(prov)
    text = ("[DRC RULES]\n" + rules_text
            + ("" if rules_text.endswith("\n") else "\n")
            + "[KNOWLEDGE]\n"
            + "<!-- layerdb: updated=%s provenance=%s -->\n" % (tag, prov)
            + body
            + ("" if (not body or body.endswith("\n")) else "\n"))
    kp = knowledge_path(layer)
    os.makedirs(os.path.dirname(kp), exist_ok=True)
    tmp = kp + ".tmp"                     # Write then rename, so a reader
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)                    # always sees either the old file
    os.replace(tmp, kp)                   # or the complete new one.
    return kp


def read_knowledge(layer):
    kp = knowledge_path(layer)
    if not os.path.isfile(kp):
        return None
    with open(kp, "r", encoding="utf-8") as fh:
        return fh.read()


def reset_knowledge_bootstrap(layer):
    """Rewrite the layer's knowledge file to the bootstrap template: the rules
    re-pasted from the branch plus an empty [KNOWLEDGE] section, exactly the
    bytes ensure_branch writes at branch creation. The branch's own files are
    left untouched, and the branch must already exist."""
    return write_knowledge(layer, "", "bootstrap")


def split_knowledge(text):
    """Split an assembled file into (rules section, knowledge section). The
    rules section is byte-equal to the branch's rules.txt by construction."""
    if not text.startswith("[DRC RULES]\n"):
        raise ValueError("knowledge file does not start with [DRC RULES]")
    rest = text[len("[DRC RULES]\n"):]
    idx = rest.find("[KNOWLEDGE]\n")
    if idx < 0:
        raise ValueError("knowledge file has no [KNOWLEDGE] section")
    return rest[:idx], rest[idx + len("[KNOWLEDGE]\n"):]


def _knowledge_updated_tag(layer):
    text = read_knowledge(layer)
    if not text:
        return "seed"
    m = _UPDATED_TAG_RE.search(text)
    return m.group(1) if m else "seed"


# ---------------------------------------------------------------------------
# Index inputs and the main.md builder
# ---------------------------------------------------------------------------
def layers_present():
    """Existing branches, sorted M1..M7 then V0..V6."""
    dbdir = os.path.join(layerdb_root(), "layerdb")
    if not os.path.isdir(dbdir):
        return []
    out = [d for d in os.listdir(dbdir)
           if d in UNIVERSE and os.path.isdir(os.path.join(dbdir, d))]
    return sorted(out, key=_layer_sort_key)


def branch_stats(layer):
    recs = read_history(layer)
    iters = [r.get("iter") for r in recs if isinstance(r.get("iter"), int)]
    return {"n_records": len(recs), "last_iter": max(iters) if iters else None}


def main_part_a_path():
    return os.path.join(layerdb_root(), "main_part_a.md")


def main_md_path():
    return os.path.join(layerdb_root(), "main.md")


def build_main_md():
    """Rebuild main.md from three parts: the verbatim bytes of
    main_part_a.md, one LAYER INDEX line per existing branch, and the fixed
    NAVIGATION text. None of it is generated text."""
    pa_path = main_part_a_path()
    if not os.path.isfile(pa_path):
        raise FileNotFoundError(
            "%s missing -- run the dir seeding (migrate_seed_v0.py) "
            "before building main.md" % pa_path)
    with open(pa_path, "r", encoding="utf-8") as fh:
        part_a = fh.read()
    index_lines = []
    for layer in layers_present():
        if not os.path.isfile(knowledge_path(layer)):   # should already exist
            write_knowledge(layer, "", "bootstrap")
        st = branch_stats(layer)
        index_lines.append(INDEX_LINE_FMT
                           % (layer, index_prefix(), layer, st["n_records"],
                              _knowledge_updated_tag(layer)))
    text = (part_a + ("" if part_a.endswith("\n") else "\n")
            + "\n## LAYER INDEX\n"
            + ("\n".join(index_lines) + "\n" if index_lines else "")
            + "\n## NAVIGATION\n" + NAVIGATION_TEXT + "\n")
    mp = main_md_path()
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    with open(mp, "w", encoding="utf-8") as fh:
        fh.write(text)
    return mp


# ---------------------------------------------------------------------------
# Injection staging. ``dest`` is the stable directory the leaf prompts
# reference by absolute path, so re-staging every iteration needs no prompt
# change.
# ---------------------------------------------------------------------------
def build_injection(dest):
    """Stage the knowledge injection into the stable injection directory.

    ``dest`` may be the directory itself or a ``.../knowledge.md`` path, in
    which case its dirname is used. Everything below is written on every call
    and is non-empty by construction, which is how the container side detects
    that the injection is present::

      * ``skill_official.md``    verbatim bytes of the configured skill file;
      * ``main.md``              a sanitized copy whose INDEX carries the
                                 absolute per-layer paths the leaf prompts
                                 reference;
      * ``knowledge/<LAYER>.md`` a sanitized copy for every existing branch.
                                 Quarantined records have no branch and so no
                                 staged copy;
      * ``knowledge.md``         a pointer to main.md, kept because the run
                                 scripts check that this file exists.

    Returns {"official", "main", "alias", "knowledge_dir", "layers"}.
    """
    # Imported here rather than at module level to avoid import-time side
    # effects; the function is the identity on ASCII input.
    from .textutil import ascii_sanitize
    in_dir = os.path.dirname(dest) if dest.endswith(".md") else dest
    os.makedirs(in_dir, exist_ok=True)

    skill_md = _skill_md()
    if not (skill_md and os.path.isfile(skill_md)):
        raise FileNotFoundError(
            "skill.md missing/unset (%r) -- cannot stage "
            "skill_official.md" % skill_md)
    with open(skill_md, "r", encoding="utf-8") as fh:
        official_text = fh.read()
    official = os.path.join(in_dir, INJECTION_WHITELIST[0])
    with open(official, "w", encoding="utf-8") as fh:
        fh.write(official_text)

    mp = main_md_path()
    if not os.path.isfile(mp):
        raise FileNotFoundError(
            "%s missing -- run the dir seeding (migrate_seed_v0.py) / "
            "build_main_md() before staging the injection" % mp)
    with open(mp, "r", encoding="utf-8") as fh:
        main_text = ascii_sanitize(fh.read())
    main_staged = os.path.join(in_dir, INJECTION_WHITELIST[1])
    with open(main_staged, "w", encoding="utf-8") as fh:
        fh.write(main_text)

    kdir = os.path.join(in_dir, "knowledge")
    os.makedirs(kdir, exist_ok=True)
    layers = layers_present()
    for layer in layers:
        if not os.path.isfile(knowledge_path(layer)):   # should already exist
            write_knowledge(layer, "", "bootstrap")
        with open(knowledge_path(layer), "r", encoding="utf-8") as fh:
            body = ascii_sanitize(fh.read())
        with open(os.path.join(kdir, "%s.md" % layer), "w",
                  encoding="utf-8") as fh:
            fh.write(body)

    alias = os.path.join(in_dir, INJECTION_WHITELIST[2])
    with open(alias, "w", encoding="utf-8") as fh:
        fh.write(alias_stub_text())
    return {"official": official, "main": main_staged, "alias": alias,
            "knowledge_dir": kdir, "layers": layers}
