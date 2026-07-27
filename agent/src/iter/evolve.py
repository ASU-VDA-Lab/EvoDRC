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

"""Knowledge evolution: measured records to layer store to per-layer update.

``build_records`` turns an iteration's gate verdicts and patches into measured
records, maps each record's operations onto framework layers (M1..M7 / V0..V6)
and appends them to the matching branches, without any model call.
``update_layer`` then runs a two-generator plus judge pipeline for one touched
layer and writes the winner back through ``layerdb.write_knowledge``.
``update_all`` orchestrates both and rebuilds ``main.md``; when evolution is
frozen it stops after the records, leaving the layer store untouched.
"""

import hashlib
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import conf
from . import layerdb
from . import throttle


# ===========================================================================
# Model backend
# ===========================================================================
_BACKEND = [None]


def set_backend(obj):
    """Install an object exposing ``call_agent`` as the backend override."""
    _BACKEND[0] = obj


def _resolve_backend():
    """Return the backend override if one is installed, else the default."""
    if _BACKEND[0] is not None:
        return _BACKEND[0]
    import importlib
    return (sys.modules.get("agent_backend.claude")
            or importlib.import_module("agent_backend.claude"))


def _call_backend(prompt, model, workspace, call_id, stage_dir, label):
    """The single ``call_agent`` invocation in this module; the markov,
    stateless and judge stages all route through here.

    The call sits inside ``throttle.call_slot``, the process-wide gate that
    also governs the leaf-repair subprocesses in ``schedule.py``, so the
    concurrency cap and the post-completion cooldown bind across both classes
    of call. The slot is released even when the backend raises.

    Returns the raw response text, with code fences left in place. Whatever the
    backend raises propagates; callers decide how to degrade."""
    backend = _resolve_backend()
    with throttle.call_slot(label):
        try:
            res = backend.call_agent(
                prompt_text=prompt, output_path=None, model=model,
                workspace=(workspace or None),
                effort=(os.environ.get("CLAUDE_EFFORT") or None),
                call_id=call_id, temp_dir=stage_dir)
        except TypeError:
            res = backend.call_agent(
                prompt, None, model, workspace=(workspace or None),
                effort=(os.environ.get("CLAUDE_EFFORT") or None),
                call_id=call_id, temp_dir=stage_dir)
    raw = (res or {}).get("raw_data") or {}
    return raw.get("result", "") if isinstance(raw, dict) else ""


def _log(msg):
    sys.stderr.write("[evolve] %s\n" % msg)


# ===========================================================================
# Part 1 -- record building
# ===========================================================================
SCHEMA_VERSION = 1
_LAYER_TOKEN_RE = re.compile(r"^(M[1-9]|V[0-9])$")
_INPUT_LINE_RE = re.compile(r"^(\w+) = input\((\d+), (\d+)\)")
_VIA_NAME_RE = re.compile(r"^VIA(\d)(\d)$")

_POLYGON_OPS = ("resize", "move", "resize_end", "delete", "add_jog")
_VIA_SHAPE_OPS = ("resize_via_shape", "move_via_shape")
_INSTANCE_OPS = ("move_instance", "delete_instance")


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _write(path, text):
    d = os.path.dirname(path)
    if d:
        try:
            os.makedirs(d, exist_ok=True)
        except OSError:
            pass
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_json_or_empty(path):
    try:
        return _load_json(path)
    except (OSError, ValueError):
        return {}


def _load_cu_verdicts(iter_dir):
    """Load ``<iter_dir>/cu_verdicts.json``; returns {} when absent or corrupt.

    Always returns a mapping: the cu_pool channel only enriches the analysis,
    so a missing or damaged artifact degrades to "no cu records" while the
    iteration's unit_gate evidence still comes through."""
    path = os.path.join(iter_dir, "cu_verdicts.json")
    if not os.path.isfile(path):
        return {}
    doc = _load_json_or_empty(path)
    if not isinstance(doc, dict):
        _log("cu_verdicts.json is not an object -- cu_pool channel skipped")
        return {}
    return doc


def _window_bbox(window, unit_bboxes):
    """Resolve a cu window key to a bounding box. ``synth:x0,y0,x1,y1`` parses
    directly, ``unit:<id>`` goes through the unit bbox map, and anything else
    returns None."""
    if not isinstance(window, str):
        return None
    if window.startswith("synth:"):
        parts = window[len("synth:"):].split(",")
        if len(parts) != 4:
            return None
        try:
            return [int(p) for p in parts]
        except (TypeError, ValueError):
            return None
    if window.startswith("unit:"):
        bb = unit_bboxes.get(window[len("unit:"):])
        return list(bb) if bb else None
    return None


def _windows_locus(windows, unit_bboxes):
    """Bounding-box union of a cu verdict's windows; a single unresolvable
    window yields None, so a box that is returned spans every window."""
    boxes = []
    for w in windows or []:
        if not isinstance(w, dict):
            return None
        b = _window_bbox(w.get("window"), unit_bboxes)
        if b is None:
            return None
        boxes.append(b)
    if not boxes:
        return None
    return [min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)]


def _build_cu_records(cu, i, case, design_state, unit_bboxes, geom,
                      gds2fw, name2fw):
    """Build one ``channel="cu_pool"`` record per verdict in
    ``cu_verdicts.json``.

    ``unit_id`` is None because a pool candidate belongs to a target rather
    than to a unit; its proposers are recorded inside the verdict itself. A
    malformed verdict is skipped and logged; the usable ones are returned."""
    records = []
    verdicts = cu.get("verdicts")
    if not isinstance(verdicts, list):
        _log("cu_verdicts.json verdicts is not a list -- cu_pool skipped")
        return records
    for idx, v in enumerate(verdicts):
        if not isinstance(v, dict):
            _log("cu verdict %d is not an object -- skipped" % idx)
            continue
        try:
            target = v.get("target")
            ops = [op for op in (v.get("ops") or []) if isinstance(op, dict)]
            windows = [w for w in (v.get("windows") or [])
                       if isinstance(w, dict)]
            records.append({
                "trial_id": "i%02d.cu.%s.%02d" % (i, target, idx),
                "schema": SCHEMA_VERSION, "iter": i, "case": case,
                "channel": "cu_pool", "design_state": design_state,
                "unit_id": None, "target": target,
                "decision": v.get("decision"),
                "conn_preserved": v.get("conn_preserved"),
                "ops": ops, "n_ops": len(ops),
                "deltas": {"delta_total": v.get("delta_total"),
                           "windows": windows},
                "locus": _windows_locus(windows, unit_bboxes),
                "touched_layers": group_layers(ops, geom, gds2fw, name2fw),
            })
        except Exception as exc:                      # noqa: BLE001
            _log("cu verdict %d unusable (%r) -- skipped" % (idx, exc))
    return records


def build_norm_maps(deck_map):
    """Return (gds number -> framework name, spelled name -> framework name),
    covering the "M5", "m5", "V4", "VIA45" and 45 spellings."""
    gds2fw, name2fw = {}, {}
    for sym_up, entry in deck_map["layers"].items():
        m = _INPUT_LINE_RE.match(entry["input_line"])
        if not m:
            continue
        if _LAYER_TOKEN_RE.match(sym_up):
            gds = int(m.group(2))
            gds2fw[gds] = sym_up
            name2fw[sym_up] = sym_up
            name2fw[sym_up.lower()] = sym_up
    return gds2fw, name2fw


def normalize_layer(token, gds2fw, name2fw):
    """Map one spelled or numbered layer token to a framework name, or None."""
    if token is None:
        return None
    if isinstance(token, int):
        return gds2fw.get(token)
    s = str(token).strip()
    if s.isdigit():
        return gds2fw.get(int(s))
    if s in name2fw:
        return name2fw[s]
    up = s.upper()
    if up in name2fw:
        return name2fw[up]
    m = _VIA_NAME_RE.match(up)
    if m and int(m.group(2)) == int(m.group(1)) + 1:
        return name2fw.get("V%s" % m.group(1))
    return None


def _cell_layers(geom, cell_name, gds2fw):
    """All framework layers used by a cell definition's shapes: a via cell
    expands to its three layers, a standard cell to its own shape layers."""
    cd = geom.cell_defs.get(cell_name)
    if cd is None:
        return set()
    out = set()
    for lyr, _pts, _cut in cd.shapes:
        fw = gds2fw.get(lyr)
        if fw:
            out.add(fw)
    return out


def op_layers(op, geom, gds2fw, name2fw):
    """The framework layers one op touches; an empty set when unmappable."""
    if not isinstance(op, dict):
        return set()
    kind = op.get("op") or op.get("type") or op.get("kind")
    if kind in ("add_polygon", "add"):
        fw = normalize_layer(op.get("layer_name") or op.get("layer"),
                             gds2fw, name2fw)
        return {fw} if fw else set()
    if kind in _VIA_SHAPE_OPS:
        return _cell_layers(geom, op.get("cell_name"), gds2fw)
    if kind == "add_via":
        # Same three-layer via expansion as the shape and instance ops,
        # e.g. VIA_VIA23 -> {M2, V2, M3}.
        return _cell_layers(geom, op.get("cell_name"), gds2fw)
    if kind in _INSTANCE_OPS:
        iid = op.get("instance_id") or op.get("inst_id")
        ins = geom.instances.get(iid) if iid else None
        if ins is None:
            return set()
        return _cell_layers(geom, ins.cell_name, gds2fw)
    pid = op.get("polygon_id")
    if pid is not None:
        p = geom.polygons.get(pid)
        if p is None:
            return set()
        fw = normalize_layer(p.layer_name, gds2fw, name2fw)
        return {fw} if fw else set()
    # Unrecognised op shape: fall back to the instance, else report unmappable.
    iid = op.get("instance_id") or op.get("inst_id")
    if iid and iid in geom.instances:
        return _cell_layers(geom, geom.instances[iid].cell_name, gds2fw)
    return set()


def group_layers(ops, geom, gds2fw, name2fw):
    out = set()
    for op in ops or []:
        out |= op_layers(op, geom, gds2fw, name2fw)
    return sorted(out & set(layerdb.UNIVERSE), key=layerdb._layer_sort_key)


def rule_layers(rule_name, deck_map):
    """The framework layers a violation rule names.

    Uses the deck map's mapping when the rule appears there, and otherwise
    derives the layers from the rule name's own tokens, which covers the
    ``<dwg>.GEOMETRY.NONORTHOGONAL`` style names the map holds only as a
    snippet."""
    entry = deck_map["rules"].get(rule_name)
    if entry is not None:
        toks = entry.get("layers") or []
    else:
        toks = [t.upper() for t in rule_name.split(".")
                if _LAYER_TOKEN_RE.match(t.upper())]
    return sorted(set(toks) & set(layerdb.UNIVERSE),
                  key=layerdb._layer_sort_key)


def build_records(iter_dir, i, case, dctx, rep_ids, gated_in, patch_objs,
                  result, deck_map, append=True):
    """Build this iteration's measured records, optionally appending them to
    the layerdb branches.

    Returns::

        {"n_records":      int,          # mapped + unmapped, both channels
         "touched_layers": [str, ...],   # sorted union over mapped records
         "n_unmapped":     int,
         "n_appended":     {layer: int}, # {} when append is False
         "n_cu_pool":      int,          # records from cu_verdicts.json
         "ledger_path":    str,          # <iter_dir>/ledger_summary.json
         "append":         bool}

    Records come from two channels: ``unit_gate``, one per repairable unit
    carrying a connectivity-only verdict with the ops cu_drc pooled away
    subtracted, and ``cu_pool``, one per ``cu_verdicts.json`` verdict carrying
    the measured ``deltas.delta_total`` and ``deltas.windows``. Each record
    also carries its own ``touched_layers`` list alongside the run-level union
    returned above. Note that ``n_appended`` here is a per-layer map while the
    written file's ``n_appended_new`` is a plain integer sum.

    Every write to ``db/`` sits behind ``append``. ``ledger_summary.json`` is
    written either way and holds the record bodies, so skipping the appends
    keeps the full analysis data and drops only the ``db/`` side effects."""
    gds2fw, name2fw = build_norm_maps(deck_map)

    # (1) Every layer named by the input violations gets a branch even when no
    #     op touches it. Gated on append, since ensure_branch writes rules.txt,
    #     _meta.json and knowledge.md into db/.
    if append:
        in_drc = os.path.join(iter_dir, "input", "%s.drc.json" % case)
        viol_layers = set()
        if os.path.isfile(in_drc):
            for rname in (_load_json_or_empty(in_drc).get("rules") or {}):
                viol_layers.update(rule_layers(rname, deck_map))
        for layer in sorted(viol_layers, key=layerdb._layer_sort_key):
            layerdb.ensure_branch(layer)

    # (2) Build the records; identical whether or not appending is enabled.
    in_py = os.path.join(iter_dir, "input", "%s.py" % case)
    design_state = _sha256_file(in_py) if os.path.isfile(in_py) else ""
    geom = getattr(dctx, "geometry_model", None)
    cu = _load_cu_verdicts(iter_dir)
    strip_map = cu.get("strip") or {}
    unit_bboxes = {}
    records = []
    for seq, leaf_id in enumerate(rep_ids or []):
        verdict = _load_json_or_empty(
            os.path.join(iter_dir, "gated", "%s.verdict" % leaf_id))
        ops_raw = (patch_objs.get(leaf_id) or {}).get("ops", []) or []
        # Ops cu_drc pooled away were measured and decided in the cu_pool
        # channel below, so leaving them here would weight one experiment
        # twice.
        strip_set = set(x for x in (strip_map.get(leaf_id) or [])
                        if isinstance(x, str))
        ops = [op for op in ops_raw
               if json.dumps([op], sort_keys=True) not in strip_set]
        leaf = (dctx.leaves or {}).get(leaf_id)
        if leaf is not None:
            unit_bboxes[leaf_id] = list(leaf.bbox_dbu)
        records.append({
            "trial_id": "i%02d.ug.%s.%02d" % (i, leaf_id, seq),
            "schema": SCHEMA_VERSION, "iter": i, "case": case,
            "channel": "unit_gate", "design_state": design_state,
            "unit_id": leaf_id, "target": None,
            "decision": ("gated_in" if leaf_id in (gated_in or [])
                         else "gated_out"),
            "conn_preserved": verdict.get("connectivity_preserved"),
            "ops": ops, "n_ops": len(ops),
            "deltas": {"reason": verdict.get("reason"),
                       "block_start": (result or {}).get("start_violations"),
                       "block_end": (result or {}).get("end_violations"),
                       # The unit-gate channel is connectivity-only, so its
                       # per-window collateral counts stay None. Measured
                       # per-window deltas live in the cu_pool channel,
                       # written by cu_drc.run_pool.
                       "n_new_in_crop": None,
                       "n_new_out_of_crop": None},
            "locus": (list(leaf.bbox_dbu) if leaf is not None else None),
            "touched_layers": group_layers(ops, geom, gds2fw, name2fw),
        })

    # (2b) The cu_pool channel: one record per cu_drc verdict.
    n_cu = 0
    if cu:
        cu_records = _build_cu_records(cu, i, case, design_state, unit_bboxes,
                                       geom, gds2fw, name2fw)
        n_cu = len(cu_records)
        records.extend(cu_records)

    mapped = [r for r in records if r["touched_layers"]]
    unmapped = [r for r in records if not r["touched_layers"]]
    touched = sorted({L for r in mapped for L in r["touched_layers"]},
                     key=layerdb._layer_sort_key)

    n_appended = {}
    if append:
        # (4) Per-layer append, skipping trial ids the branch already holds.
        for layer in touched:
            layerdb.ensure_branch(layer)
            existing = layerdb.trial_ids(layer)
            new = [r for r in mapped
                   if layer in r["touched_layers"]
                   and r["trial_id"] not in existing]
            layerdb.append_records(layer, new)
            n_appended[layer] = len(new)
        # (5) Records with no mapped layer are quarantined in
        #     db/_unmapped.jsonl.
        for r in unmapped:
            r2 = dict(r)
            r2["reason"] = ("empty_patch" if not r["ops"] else "unmappable_ops")
            layerdb.append_unmapped(r2)
        # (6) Applied loci -> db/loci.jsonl, the input to staleness annotation.
        loci = []
        for lid in (gated_in or []):
            lf = (dctx.leaves or {}).get(lid)
            if lf is not None:
                loci.append(list(lf.bbox_dbu))
        layerdb.record_applied_loci(i, loci)

    # (7) Always write the summary file; it is the only sink when appending is
    #     disabled. Written last so ``per_layer`` reports what actually landed
    #     in each branch, and it keeps the record bodies because nothing else
    #     stores them once the appends are skipped.
    per_layer = {}
    if append:
        per_layer = dict((L, len(layerdb.read_iter_records(L, i)))
                         for L in touched)
    summary_doc = {
        "iter": i,
        "case": case,
        "design_state": design_state,
        "n_records": len(records),
        "n_unit_gate": len(records) - n_cu,
        "n_cu_pool": n_cu,
        # Present for schema parity only: there is no failed-trial channel.
        "n_failed_trials": 0,
        "failed_trials": [],
        "n_unmapped": len(unmapped),
        # An integer sum, not the per-layer map; the map stays on the returned
        # object under its own "n_appended" key, which the caller reads.
        "n_appended_new": sum(n_appended.values()) if append else 0,
        "per_layer": per_layer,
        "touched_layers": touched,
        "trial_ids": sorted(r["trial_id"] for r in records),
        "records": records,
    }
    ledger_path = os.path.join(iter_dir, "ledger_summary.json")
    with open(ledger_path, "w", encoding="utf-8") as fh:
        json.dump(summary_doc, fh, indent=2, sort_keys=True)
        fh.write("\n")

    return {"n_records": len(records), "touched_layers": touched,
            "n_unmapped": len(unmapped), "n_appended": n_appended,
            "n_cu_pool": n_cu,
            "ledger_path": ledger_path, "append": bool(append)}


# ===========================================================================
# Part 2 -- the per-layer dual-generator and judge pipeline
# ===========================================================================
SEED_TOKEN = "(seed, reference-design-verified)"
SOFT_CAP_CHARS = 30000

# The exact set of files each call kind may read. ``_stage_dir`` raises on any
# deviation, so the record of what a call could see cannot drift.
STAGE_WHITELIST = {
    "markov": ("rules.txt", "knowledge_current.md", "new_records.jsonl"),
    "stateless": ("rules.txt", "history.jsonl"),
    "judge": ("rules.txt", "candidate_A.md", "candidate_B.md",
              "history_excerpt.jsonl"),
}

CITE_RE = re.compile(r"trial:[A-Za-z0-9._:-]+")
HYPOTHESIS_RE = re.compile(
    r"\b(probably|likely|maybe|perhaps|possibly|might|may be|could be|"
    r"hypothes\w*|suspect\w*|presum\w*|appears? to|seems? to|unclear|"
    r"unverified|untested|I think|worth trying)\b", re.IGNORECASE)
PRESCRIPTIVE_START_RE = re.compile(
    r"^[\s\-\*\d\.\)>#]*(do not|don't|never|always|prefer|use|avoid|apply|"
    r"move|resize|snap)\b", re.IGNORECASE)
MUST_RE = re.compile(r"\bmust\b", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?;:])\s+|\n+")
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n|\n```\s*$")
_LAYERDB_COMMENT_RE = re.compile(r"^<!-- layerdb:[^\n]*-->\n?")


def _env_int(name, default):
    try:
        return int(os.environ.get(name) or default)
    except ValueError:
        return default


def _attempts():
    return max(1, _env_int("KNOW_ATTEMPTS", 2))


def _sha12(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _strip_fence(text):
    return _FENCE_RE.sub("", (text or "").strip()).strip()


def _mask_code_spans(paragraph):
    """Blank out fenced-code lines and inline `...` spans, so the lexicon and
    structural scans ignore code; citations are searched on the original
    text."""
    out, in_fence = [], False
    for ln in paragraph.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", " ", ln))
    return "\n".join(out)


def _paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def mech_check(candidate, known_trial_ids, lineage):
    """Check a candidate body against the mechanical output rules.

    Returns a list of violation strings, empty when the candidate passes.
    ``lineage`` is "markov" or "stateless"; the seed token counts as a
    citation for markov candidates only."""
    if lineage not in ("markov", "stateless"):
        raise ValueError("lineage must be markov|stateless, got %r" % lineage)
    violations = []
    text = candidate or ""
    if not text.strip():
        return ["EMPTY: candidate is empty"]
    if "[DRC RULES]" in text:
        violations.append("RULES-HEADING: candidate contains a [DRC RULES] "
                          "heading (rules are harness-pasted only)")
    if "<!-- layerdb:" in text:
        violations.append("LAYERDB-COMMENT: candidate contains a "
                          "'<!-- layerdb:' line (harness provenance "
                          "comments are assembly-written only)")
    if lineage == "stateless" and SEED_TOKEN in text:
        violations.append("SEED-TOKEN-IN-STATELESS: %r may appear only in "
                          "markov-lineage candidates" % SEED_TOKEN)
    known = {t for t in (known_trial_ids or ()) if t}
    for m in CITE_RE.finditer(text):
        tok = m.group(0)[len("trial:"):]
        if tok not in known and tok.rstrip(".:-") not in known:
            violations.append("CITE-NONEXISTENT: trial:%s not in this "
                              "layer's history" % tok)
    for para in _paragraphs(text):
        clean = _mask_code_spans(para)
        for m in HYPOTHESIS_RE.finditer(clean):
            violations.append("HYPOTHESIS-LEXICON: %r in: %s"
                              % (m.group(0), " ".join(para.split())[:100]))
        cited = bool(CITE_RE.search(para)) or (lineage == "markov"
                                               and SEED_TOKEN in para)
        if cited:
            continue
        for sent in _SENTENCE_SPLIT_RE.split(clean):
            if not sent.strip():
                continue
            if PRESCRIPTIVE_START_RE.match(sent) or MUST_RE.search(sent):
                violations.append(
                    "PRESCRIPTION-WITHOUT-CITATION: %s"
                    % " ".join(sent.split())[:120])
                break
    return violations


_OUTPUT_RULES = (
    "OUTPUT RULES (hard):\n"
    "- Output ONLY the [KNOWLEDGE] section BODY for layer %(layer)s: "
    "markdown, English, ASCII.\n"
    "- Do NOT output a '[KNOWLEDGE]' heading line.\n"
    "- NEVER output a '[DRC RULES]' heading or any copy of the rules "
    "text -- the harness re-pastes the rules at assembly.\n"
    "- Every prescriptive claim (do not / never / always / prefer / use / "
    "avoid / apply / move / resize / snap / must) needs at least one "
    "measured citation, literal form trial:<id>, INSIDE the same "
    "paragraph.\n"
    "- Every cited id MUST exist in this layer's history records. NEVER "
    "fabricate ids.\n"
    "- NO hypothesis language (probably, likely, maybe, perhaps, possibly, "
    "might, may be, could be, hypothesize, suspect, presume, appears to, "
    "seems to, unclear, unverified, untested, I think, worth trying). "
    "Assert only what the measured records ground.\n"
    "- SOFT CAP ~%(soft)d chars: prefer dropping superseded or "
    "SINCE-MODIFIED-grounded prose first; keep it lean -- there is no "
    "hard cap.\n"
    "- Body only: no preamble, no fences, no commentary, no "
    "'<!-- layerdb:' comment lines.\n")

_MARKOV_SEED_RULE = (
    "- Seed-derived prose (present in the CURRENT KNOWLEDGE below) may keep "
    "the literal token %s as its citation equivalent; keep it in any seed "
    "paragraph you retain.\n" % SEED_TOKEN)

# This rule tells the stateless generator it has no seed at all: its prompt
# withholds both the knowledge file and the seed, and mech_check disqualifies
# a candidate that claims any provenance other than a trial citation.
_STATELESS_SEED_RULE = (
    "- You have NO prior knowledge file and NO seed: your ONLY sources are "
    "the DRC rules and the measured history records below.\n"
    "- Cite trial:<id> ONLY -- NEVER claim any other provenance.\n")

_RETRY_HEADER = ("\n\nPREVIOUS ATTEMPT REJECTED by the mechanical checks. "
                 "Fix ALL of the following and re-output the complete "
                 "body:\n")

_JUDGE_RETRY = ("\n\nPREVIOUS OUTPUT VIOLATED THE CONTRACT. Reply with "
                "EXACTLY one line of JSON, winner = majority of your three "
                "votes, no tie anywhere:\n"
                '{"winner":"A"|"B", "evidence_fidelity":"A"|"B", '
                '"coverage":"A"|"B", "knowledge_quality":"A"|"B", '
                '"reason":"<=200 chars"}\n')


def _embed_or_read(payload, staged_name, stage_dir):
    """Embed the payload when it fits KNOW_EMBED_MAX (default 200000 chars),
    otherwise write it to ``<stage_dir>/<staged_name>`` and return a pointer
    telling the model to read that path instead."""
    if len(payload) <= _env_int("KNOW_EMBED_MAX", 200000):
        return payload
    p = os.path.join(stage_dir, staged_name)
    _write(p, payload)
    return ("(too large to embed -- Read the staged file %s for the full "
            "content)" % p)


def build_markov_prompt(layer, i, rules_text, current_body, new_records_text,
                        stage_dir):
    return (
        "=== MARKOV KNOWLEDGE GENERATOR (lineage update) ===\n"
        "Role: maintain the [KNOWLEDGE] section of the per-layer DRC repair "
        "knowledge file for layer %s (iteration %d).\n"
        "Task -- update the CURRENT KNOWLEDGE with THIS ITERATION'S new "
        "measured records:\n"
        "- fold in new conclusions\n"
        "- drop anything the new records contradict\n"
        "- keep what still holds\n\n" % (layer, i)
        + _OUTPUT_RULES % {"layer": layer, "soft": SOFT_CAP_CHARS}
        + _MARKOV_SEED_RULE
        + "\nStaged read-only under %s: rules.txt, knowledge_current.md, "
          "new_records.jsonl (same inputs as below).\n" % stage_dir
        + "\n[DRC RULES] (hardcoded, layer %s)\n%s\n" % (layer, rules_text)
        + "\nCURRENT KNOWLEDGE (your lineage; body only):\n%s\n"
          % (current_body if current_body.strip()
             else "(empty -- first knowledge for this layer)")
        + "\nNEW MEASURED RECORDS (iteration %d; one JSON per line):\n%s\n"
          % (i, _embed_or_read(new_records_text, "new_records.jsonl",
                               stage_dir)))


def build_stateless_prompt(layer, i, rules_text, history_text, stage_dir):
    """Prompt for the second lineage: the rules plus the entire branch history
    and nothing else. Withholding the knowledge file and the seed is what makes
    this candidate an independent reading of the run evidence rather than a
    rewrite of the previous document."""
    return (
        "=== STATELESS KNOWLEDGE GENERATOR (from measured history only) ===\n"
        "Role: write the [KNOWLEDGE] section of the per-layer DRC repair "
        "knowledge file for layer %s (iteration %d) FROM SCRATCH.\n"
        "- Use ONLY the hardcoded DRC rules and the layer's complete "
        "measured operation history below.\n\n" % (layer, i)
        + _OUTPUT_RULES % {"layer": layer, "soft": SOFT_CAP_CHARS}
        + _STATELESS_SEED_RULE
        + "\nStaged read-only under %s: rules.txt, history.jsonl "
          "(same inputs as below).\n" % stage_dir
        + "\n[DRC RULES] (hardcoded, layer %s)\n%s\n" % (layer, rules_text)
        + "\nFULL MEASURED HISTORY (chronological; one JSON per line):\n%s\n"
          % _embed_or_read(history_text, "history.jsonl", stage_dir))


def build_judge_prompt(layer, i, rules_text, cand_a, cand_b, excerpt_text,
                       stage_dir):
    """Prompt for the judge. A is the markov candidate and B the stateless one,
    in that fixed order, and neither lineage is revealed."""
    return (
        "=== KNOWLEDGE JUDGE ===\n"
        "Task: select the better [KNOWLEDGE] candidate for layer %s "
        "(iteration %d). Both were produced from this layer's measured "
        "record; you are not told how.\n\n" % (layer, i)
        + "DECISION PROCEDURE (fixed):\n"
          "- Vote A or B on EACH criterion separately -- no tie anywhere.\n"
          "- The three axes are deliberately orthogonal; judge each on its "
          "own evidence.\n"
          "- evidence_fidelity: spot-check each candidate's citations "
          "against the history excerpt AND whether its claims stay within "
          "the cited evidence (claims resting on SINCE-MODIFIED loci are "
          "discounted as current-state assertions); better-verified wins.\n"
          "- coverage: accounts for more of this layer's measured record "
          "(newest records weigh most).\n"
          "- knowledge_quality: the better-crafted document overall -- "
          "less redundancy, clearer wording, better organization, fewer "
          "internal contradictions.\n"
          "- winner = the majority of your three votes (mechanically "
          "checked).\n\n"
        + "OUTPUT CONTRACT (hard): EXACTLY one line and nothing else:\n"
          '{"winner":"A"|"B", "evidence_fidelity":"A"|"B", '
          '"coverage":"A"|"B", "knowledge_quality":"A"|"B", '
          '"reason":"<=200 chars"}\n\n'
        + "Staged read-only under %s: rules.txt, candidate_A.md, "
          "candidate_B.md, history_excerpt.jsonl (same inputs as below).\n"
          % stage_dir
        + "\n[DRC RULES] (hardcoded, layer %s)\n%s\n" % (layer, rules_text)
        + "\nCANDIDATE A:\n%s\n" % cand_a
        + "\nCANDIDATE B:\n%s\n" % cand_b
        + "\nHISTORY EXCERPT (context lines first, then records "
          "newest-first, staleness-annotated):\n%s\n"
          % _embed_or_read(excerpt_text, "history_excerpt.jsonl", stage_dir))


def parse_judge_verdict(raw):
    """Parse the judge's reply, which must be exactly one line of
    ``{"winner":"A"|"B","evidence_fidelity":"A"|"B","coverage":"A"|"B",
    "knowledge_quality":"A"|"B","reason":"<=200 chars"}``.

    ``winner`` must equal the majority of the three per-criterion votes. With
    three binary votes a majority always exists, so a mismatch means the
    verdict contradicts itself. Anything else returns None, and the caller
    retries and then carries the current knowledge forward."""
    s = _strip_fence(raw)
    if not s or "\n" in s:
        return None
    try:
        d = json.loads(s)
    except ValueError:
        return None
    if not isinstance(d, dict):
        return None
    crit = []
    for k in ("evidence_fidelity", "coverage", "knowledge_quality"):
        v = d.get(k)
        if v not in ("A", "B"):
            return None
        crit.append(v)
    w = d.get("winner")
    if w not in ("A", "B"):
        return None
    if w != ("A" if crit.count("A") >= 2 else "B"):
        return None                      # self-contradictory verdict
    reason = d.get("reason")
    if reason is not None and (not isinstance(reason, str)
                               or len(reason) > 200):
        return None
    return w


# ---------------------------------------------------------------------------
# Judge context
# ---------------------------------------------------------------------------
def _drc_rule_counts(path):
    """Read a DRC json into {rule name: violation count}, or None when the file
    is absent or unparsable. None means "not measured", which the histogram
    reports differently from a measured zero."""
    if not (path and os.path.isfile(path)):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            rules = (json.load(fh).get("rules") or {})
    except (OSError, ValueError):
        return None
    out = {}
    for name, v in rules.items():
        if isinstance(v, dict):
            out[name] = v.get("violation_count",
                              len(v.get("violations") or []))
        elif isinstance(v, list):
            out[name] = len(v)
    return out


def repaired_drc_path(iter_dir, case, repaired_drc=None):
    """Locate the repaired-block DRC json for this iteration.

    Prefers the measured path the caller passed down (``result["repaired_drc"]``,
    which ``block_eval.run_block_drc_nested`` sets) and otherwise falls back to
    ``<iter_dir>/repaired/<CASE>.drc.json``. A wrong path fails silently --
    every histogram would report ``repaired: None`` instead of raising -- so
    the fallback has to stay in step with controller.py's ``repaired_dir``."""
    if repaired_drc and os.path.isfile(repaired_drc):
        return repaired_drc
    p = os.path.join(iter_dir, "repaired", "%s.drc.json" % case)
    return p if os.path.isfile(p) else None


def block_histogram(layer, iter_dir, case, deck_map, repaired_drc=None):
    """Per-layer block DRC histogram, rule -> {input, repaired}, restricted to
    rules that name this layer. ``repaired`` is None when the repaired DRC was
    never measured, for instance because the render failed, never a silent 0."""
    n_in = _drc_rule_counts(
        os.path.join(iter_dir, "input", "%s.drc.json" % case)) or {}
    n_out = _drc_rule_counts(repaired_drc_path(iter_dir, case, repaired_drc))
    hist = {}
    for rule in sorted(set(n_in) | set(n_out or {})):
        if layer not in rule_layers(rule, deck_map):
            continue
        hist[rule] = {"input": n_in.get(rule, 0),
                      "repaired": None if n_out is None
                      else (n_out or {}).get(rule, 0)}
    return hist


def unmapped_layer_context(layer, deck_map):
    """Quarantined records from ``db/_unmapped.jsonl`` whose per-rule delta or
    debt names this layer, offered to the judge as context only.

    This reads ``deltas.per_rule`` and ``debt``, which the current
    connectivity-only gate leaves unset, so in practice it returns an empty
    list and stays in place for a future per-rule gate. Unparsable lines are
    skipped."""
    up = layerdb.unmapped_path()
    if not os.path.isfile(up):
        return []
    out = []
    with open(up, "r", encoding="utf-8") as fh:
        for line in fh.read().splitlines():
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if not isinstance(rec, dict):
                continue
            rules = set()
            pr = (rec.get("deltas") or {}).get("per_rule") or {}
            for key in ("new_in_crop_by_rule", "new_out_of_crop_by_rule"):
                rules |= set((pr.get(key) or {}).keys())
            rules |= set(((rec.get("debt") or {})
                          .get("new_out_of_crop_by_rule") or {}).keys())
            if any(layer in rule_layers(r, deck_map) for r in rules):
                out.append(rec)
    return out


def build_history_excerpt(layer, iter_dir, i, case, deck_map,
                          repaired_drc=None):
    """Assemble the judge's evidence: the context lines first (block histogram,
    then any quarantined-gate context), then the staleness-annotated branch
    records newest-first, all of them unless KNOW_EXCERPT_MAX_RECORDS is
    positive. Oversized excerpts are handed off as a staged file by
    ``_embed_or_read``; the full text is always staged as
    history_excerpt.jsonl."""
    cap = _env_int("KNOW_EXCERPT_MAX_RECORDS", 0)
    annotated = layerdb.annotate_staleness(layerdb.read_history(layer))
    annotated.reverse()                    # newest first
    lines = [json.dumps(
        {"context": "block_histogram", "layer": layer, "iter": i,
         "rules": block_histogram(layer, iter_dir, case, deck_map,
                                  repaired_drc)},
        sort_keys=True, separators=(",", ":"))]
    for rec in unmapped_layer_context(layer, deck_map):
        lines.append(json.dumps(
            {"context": "unmapped_gate_record",
             "note": "quarantined record (no op-derived layer) whose "
                     "per-rule delta names this layer; context only, not "
                     "part of this branch's history",
             "record": rec}, sort_keys=True, separators=(",", ":")))
    lines += [json.dumps(r, sort_keys=True, separators=(",", ":"))
              for r in (annotated[:cap] if cap > 0 else annotated)]
    return "\n".join(lines) + "\n"


def _stage_dir(kind, layer, contents, *, work_dir):
    """Create ``<work_dir>/_know/<layer>/<kind>/`` holding exactly the
    whitelisted files for this call kind, and return its path.

    The location is deterministic rather than a temporary directory, so any
    call can be reconstructed afterwards from what it was allowed to read. The
    staging area is internal to the run rather than part of the published
    record, which is why ``work_dir`` is keyword-only and required: the caller
    always says where the staging tree goes. The path is interpolated into all
    three prompts, so moving it changes the prompt text."""
    if set(contents) != set(STAGE_WHITELIST[kind]):
        raise ValueError("staging for %s must be exactly %s, got %s"
                         % (kind, STAGE_WHITELIST[kind], sorted(contents)))
    d = os.path.join(work_dir, "_know", layer, kind)
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        pass
    for name, data in contents.items():
        _write(os.path.join(d, name), data or "")
    return d


def _save_draft(text, i, layer, kind, attempt):
    """Write a rejected candidate to ``<skill root>/_drafts/`` as
    ``iter{i}_{LAYER}_{kind}.md``; a failed write is logged as a warning."""
    try:
        d = os.path.join(layerdb.skill_root(), "_drafts")
        os.makedirs(d, exist_ok=True)
        name = "iter%02d_%s_%s%s.md" % (
            i, layer, kind, "" if attempt <= 1 else "_attempt%d" % attempt)
        _write(os.path.join(d, name), text)
    except Exception as exc:                          # noqa: BLE001
        _log("WARNING: draft save failed: %r" % exc)


def _current_body(layer):
    """The layer's current [KNOWLEDGE] body, with the leading provenance
    comment line stripped."""
    text = layerdb.read_knowledge(layer)
    if not text:
        return ""
    try:
        _rules, body = layerdb.split_knowledge(text)
    except ValueError:
        return ""
    return _LAYERDB_COMMENT_RE.sub("", body, count=1)


def _records_text(records):
    return "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n"
                   for r in (records or []))


def _call_id(case, i, layer, kind, attempt):
    """Build the identifier for one knowledge call.

    ``tokens.aggregate`` filters the recorded per-call files by the
    ``"<case>_"`` prefix, so the id has to start with it or the call's cost is
    never counted."""
    return "%s_iter%d_know_%s_%s_a%d" % (case, i, layer, kind, attempt)


def _generate(kind, layer, i, case, base_prompt, stage_dir, known_ids,
              model, workspace, score_calls_dir, calls_log):
    """Run one generator lineage: call, strip fences, ``mech_check``, retried
    up to KNOW_ATTEMPTS times with the violation lines quoted back.

    Returns the surviving candidate text, or None when every attempt was
    disqualified or the backend failed; rejected bodies are saved as drafts.
    ``calls_log`` belongs to this call alone -- the layer thread merges the
    per-generator lists afterwards, so no lock is needed."""
    prompt = base_prompt
    for attempt in range(1, _attempts() + 1):
        call_id = _call_id(case, i, layer, kind, attempt)
        _write(os.path.join(stage_dir, "prompt.txt"), prompt)
        t0 = time.time()
        try:
            raw = _call_backend(prompt, model, workspace, call_id, stage_dir,
                                "know:%s:%s:i%d" % (layer, kind, i))
        except Exception as exc:                      # noqa: BLE001
            calls_log.append({"kind": kind, "attempt": attempt,
                              "wall_s": round(time.time() - t0, 2),
                              "ok": False, "error": repr(exc)[:200]})
            _log("%s %s attempt %d: call failed: %r"
                 % (layer, kind, attempt, exc))
            continue
        _copy_call_tokens(stage_dir, call_id, score_calls_dir)
        out = _strip_fence(raw)
        viol = mech_check(out, known_ids, kind)
        calls_log.append({"kind": kind, "attempt": attempt,
                          "wall_s": round(time.time() - t0, 2),
                          "ok": not viol, "n_violations": len(viol)})
        if not viol:
            return out
        for v in viol[:10]:
            _log("%s %s attempt %d MECH-CHECK violation: %s"
                 % (layer, kind, attempt, v))
        if out:
            _save_draft(out, i, layer, kind, attempt)
        if attempt < _attempts():
            prompt = (base_prompt + _RETRY_HEADER
                      + "\n".join("> " + v for v in viol) + "\n")
    return None


def _run_generators(layer, i, case, gen_specs, known_ids, model, workspace,
                    score_calls_dir):
    """Run the generator lineages concurrently, one thread per
    ``(kind, base_prompt, stage_dir)`` spec.

    The retry loops stay inside ``_generate`` and the global
    ``throttle.CallGate`` still governs the real call rate, so these threads
    add no unbounded parallelism. Returns
    ``{kind: (candidate_or_None, call_records)}``. A crash in a generator
    thread is re-raised in the calling layer thread, where ``_safe_result``
    contains it, leaving per-layer isolation intact."""
    out, errs = {}, {}

    def _one(kind, base_prompt, stage_dir):
        log = []
        cand = None
        try:
            cand = _generate(kind, layer, i, case, base_prompt, stage_dir,
                             known_ids, model, workspace, score_calls_dir,
                             log)
        except BaseException as exc:              # noqa: BLE001 (re-raised)
            errs[kind] = exc
        out[kind] = (cand, log)

    threads = [threading.Thread(target=_one, args=spec,
                                name="know_%s_%s" % (layer, spec[0]))
               for spec in gen_specs]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    if errs:
        raise errs[sorted(errs)[0]]
    return out


def _judge(layer, iter_dir, i, case, rules_text, cand_markov, cand_stateless,
           deck_map, model, workspace, score_calls_dir, repaired_drc, res,
           *, work_dir):
    """Run the A/B judge, with A the markov candidate and B the stateless one
    in that fixed order and the judge never told which is which.

    Returns the verdict ``"A"`` or ``"B"``, or None when the one-line JSON
    contract was still violated after KNOW_ATTEMPTS tries, in which case the
    caller carries the current knowledge file forward verbatim."""
    excerpt_text = build_history_excerpt(layer, iter_dir, i, case, deck_map,
                                         repaired_drc)
    stage = _stage_dir("judge", layer, {
        "rules.txt": rules_text,
        "candidate_A.md": cand_markov,
        "candidate_B.md": cand_stateless,
        "history_excerpt.jsonl": excerpt_text,
    }, work_dir=work_dir)
    base_prompt = build_judge_prompt(layer, i, rules_text, cand_markov,
                                     cand_stateless, excerpt_text, stage)
    prompt = base_prompt
    for attempt in range(1, _attempts() + 1):
        call_id = _call_id(case, i, layer, "judge", attempt)
        _write(os.path.join(stage, "prompt.txt"), prompt)
        t0 = time.time()
        try:
            raw = _call_backend(prompt, model, workspace, call_id, stage,
                                "know:%s:judge:i%d" % (layer, i))
        except Exception as exc:                      # noqa: BLE001
            res["calls"].append({"kind": "judge", "attempt": attempt,
                                 "wall_s": round(time.time() - t0, 2),
                                 "ok": False, "error": repr(exc)[:200]})
            _log("%s judge attempt %d: call failed: %r" % (layer, attempt,
                                                           exc))
            continue
        _copy_call_tokens(stage, call_id, score_calls_dir)
        verdict = parse_judge_verdict(raw)
        res["calls"].append({"kind": "judge", "attempt": attempt,
                             "wall_s": round(time.time() - t0, 2),
                             "ok": verdict is not None,
                             "raw": (raw or "")[:240]})
        if verdict is not None:
            return verdict
        prompt = base_prompt + _JUDGE_RETRY
    return None


def update_layer(layer, iter_dir, i, case, model, workspace, score_calls_dir,
                 deck_map=None, result=None, *, work_dir):
    """Run the two-generator and judge pipeline for one triggered layer.

    The knowledge file is rewritten only when a candidate wins. Every failure
    mode -- both candidates disqualified, a judge that never honours its output
    contract, a backend that keeps raising -- carries the current file forward
    byte for byte and lets the other layers and the iteration finish."""
    res = {"layer": layer, "status": "carried", "outcome": "carry_forward",
           "winner": None, "judged": False, "calls": [], "verdict": None}
    deck_map = deck_map or layerdb.load_deck_map()
    new_records = layerdb.read_iter_records(layer, i)
    if not new_records:
        res["status"] = "skipped_no_records"
        res["outcome"] = "skipped_no_records"
        return res
    res["n_new_records"] = len(new_records)
    known_ids = layerdb.trial_ids(layer)
    rules_text = _read(layerdb.rules_path(layer))
    current_file = layerdb.read_knowledge(layer) or ""
    current_body = _current_body(layer)
    new_records_text = _records_text(new_records)

    # Markov lineage: rules, the current knowledge file, this iteration's
    # records.
    mk_stage = _stage_dir("markov", layer, {
        "rules.txt": rules_text,
        "knowledge_current.md": current_file,
        "new_records.jsonl": new_records_text,
    }, work_dir=work_dir)
    mk_prompt = build_markov_prompt(layer, i, rules_text, current_body,
                                    new_records_text, mk_stage)

    # Stateless lineage: rules and the entire history, no knowledge file and
    # no seed.
    history_text = _read(layerdb.history_path(layer))
    sl_stage = _stage_dir("stateless", layer, {
        "rules.txt": rules_text,
        "history.jsonl": history_text,
    }, work_dir=work_dir)
    sl_prompt = build_stateless_prompt(layer, i, rules_text, history_text,
                                       sl_stage)

    gen_out = _run_generators(
        layer, i, case,
        (("markov", mk_prompt, mk_stage), ("stateless", sl_prompt, sl_stage)),
        known_ids, model, workspace, score_calls_dir)
    cand_markov, mk_calls = gen_out["markov"]
    cand_stateless, sl_calls = gen_out["stateless"]
    res["calls"].extend(mk_calls)
    res["calls"].extend(sl_calls)

    survivors = [(name, cand) for name, cand in
                 (("markov", cand_markov), ("stateless", cand_stateless))
                 if cand is not None]
    hash_a = _sha12(cand_markov) if cand_markov is not None else "dq"
    hash_b = _sha12(cand_stateless) if cand_stateless is not None else "dq"

    if not survivors:
        _log("%s: both candidates disqualified -> CARRY FORWARD current "
             "file verbatim" % layer)
        return res

    if len(survivors) == 1:
        # A single survivor wins without a judge call: there is nothing to
        # compare it against.
        winner, body = survivors[0]
    else:
        verdict = _judge(layer, iter_dir, i, case, rules_text, cand_markov,
                         cand_stateless, deck_map, model, workspace,
                         score_calls_dir,
                         (result or {}).get("repaired_drc"), res,
                         work_dir=work_dir)
        res["judged"] = True
        res["verdict"] = verdict
        if verdict is None:
            _log("%s: judge contract violated after retries -> CARRY "
                 "FORWARD previous knowledge" % layer)
            return res
        winner = "markov" if verdict == "A" else "stateless"
        body = cand_markov if verdict == "A" else cand_stateless

    provenance = ("iter%d knowledge_pipeline winner=%s judged=%s "
                  "markov=%s stateless=%s"
                  % (i, winner, "true" if res["judged"] else "false",
                     hash_a, hash_b))
    layerdb.write_knowledge(layer, body, provenance)
    res["status"] = "updated"
    res["outcome"] = "updated"
    res["winner"] = winner
    res["sha12"] = _sha12(body)
    res["chars"] = len(body)
    _log("%s: winner=%s judged=%s -> knowledge file rewritten"
         % (layer, winner, res["judged"]))
    return res


def _copy_call_tokens(stage_dir, call_id, score_calls_dir):
    """Copy the recorded per-call token JSON next to the staged inputs.

    The original already lands in AGENT_CALLS_DIR, which is what
    ``agent.src.tokens.aggregate`` counts; this copy exists only so the cost of
    a knowledge call can be inspected beside the inputs it was made with."""
    src_dir = os.environ.get("AGENT_CALLS_DIR", "").strip()
    if not src_dir:
        return
    src = os.path.join(src_dir, "%s.json" % call_id)
    if not os.path.isfile(src):
        return
    try:
        import shutil
        shutil.copyfile(src, os.path.join(stage_dir, "tokens.json"))
    except OSError:
        pass


# ===========================================================================
# Part 3 -- orchestration
# ===========================================================================
def _model(dctx):
    info = getattr(dctx, "case_info", None)
    return (getattr(info, "model_name", "") or
            os.environ.get("AGENT_MODEL_NAME", "") or "claude-sonnet-4-6")


def _workspace(dctx):
    return getattr(dctx, "workspace", "") or ""


def _calls_dir():
    return os.environ.get("AGENT_CALLS_DIR", "").strip()


def _safe_result(fut):
    try:
        return fut.result()
    except Exception as exc:                          # noqa: BLE001
        return {"status": "error", "outcome": "error", "error": str(exc)}


def _write_audit(iter_dir, i, summary, cfg, per_layer=None, skipped=None):
    doc = {"iter": i,
           "evolution": cfg.evolution,
           "ablation": cfg.ablation,
           "skipped": skipped,
           "n_records": summary["n_records"],
           "n_cu_pool": summary.get("n_cu_pool", 0),
           "touched_layers": summary["touched_layers"],
           "n_appended": summary["n_appended"],
           "n_unmapped": summary["n_unmapped"],
           "ledger_path": summary["ledger_path"],
           "per_layer": per_layer or {}}
    path = os.path.join(iter_dir, "knowledge_update.json")
    try:
        os.makedirs(iter_dir, exist_ok=True)
    except OSError:
        pass
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return path


def update_all(iter_dir, i, case, dctx, rep_ids, gated_in, patch_objs,
               result, cfg, *, work_dir):
    """Build this iteration's records and, unless evolution is frozen, update
    the per-layer knowledge. Returns ``build_records``' summary dict.

    ``iter_dir`` addresses the published outputs -- ledger_summary.json,
    knowledge_update.json and the repaired DRC the history excerpt reads --
    while ``work_dir`` is keyword-only and required and carries only the
    internal ``_know/`` staging tree."""
    deck_map = layerdb.load_deck_map()
    summary = build_records(iter_dir, i, case, dctx, rep_ids, gated_in,
                            patch_objs, result, deck_map,
                            append=(cfg.evolution == conf.EVOLUTION_ON))
    if cfg.evolution == conf.EVOLUTION_FROZEN:
        # Return before resolving a backend and before rebuilding main.md.
        _write_audit(iter_dir, i, summary, cfg, skipped="ablation2_frozen")
        return summary

    per_layer = {}
    triggered = summary["touched_layers"]
    if triggered:
        # A per-phase sub-cap only: every model call still passes through the
        # global throttle.CallGate that also governs the leaf subprocesses.
        workers = max(1, int(getattr(cfg, "know_concurrency", 2) or 1))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = {}
            for layer in triggered:
                futs[pool.submit(update_layer, layer, iter_dir, i, case,
                                 _model(dctx), _workspace(dctx),
                                 _calls_dir(), deck_map, result,
                                 work_dir=work_dir)] = layer
            for fut in as_completed(futs):
                per_layer[futs[fut]] = _safe_result(fut)
    # Rebuilt after the appends and the knowledge writes so the index ops
    # counts and updated tags reflect them.
    layerdb.build_main_md()
    _write_audit(iter_dir, i, summary, cfg, per_layer=per_layer)
    return summary
