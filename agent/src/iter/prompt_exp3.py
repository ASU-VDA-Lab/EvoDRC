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

"""Opening sections of the exp3 repair prompt, and the whole-design data block.

The prompt is assembled in two halves. ``prompt_format.build_leaf_prompt``
renders sections S4 to S7; this module supplies S1 (mission and task), S2
(resources and paths) and S3 (subagent roles and repair workflow), plus the
block-wide facts injected into S6 for shared targets and for whole-design mode.

Paths are resolved at build time: the technology directory and case name
arrive as arguments, and the knowledge-file paths in the templates are
re-pointed onto the staged injection directory.

Note the formatting convention in the templates: they are expanded by one
positional ``%`` pass with four arguments, and every literal percent sign is
escaped as ``%%``. Introducing a named ``%(name)s`` field would make the whole
expansion fail.
"""

import os


# --------------------------------------------------------------------------
# Prompt sections rendered here
#
# S1 states the mission and task, S2 lists the resources and their paths, and
# S3 describes the subagent roles and the repair workflow. The remaining
# sections -- verification and tools, edit rules, data and output -- come from
# prompt_format.build_leaf_prompt, and the banner strings must match the ones
# it uses.
#
# The three constants below are expanded together by one positional % pass
# with the arguments (tools, leaf_id, tc_dir, tc_dir): S1 carries the first
# two placeholders and S2 the last two.
# --------------------------------------------------------------------------
S1 = (
    "=== S1: MISSION & TASK ===\n\n"
    "- You are an EDA engineer specializing in ASAP7 PDK block-level DRC "
    "repair.\n"
    "- You repair ONE cropped block-level layout. Inlined below: the crop "
    "(S6 '## Crop'), its violations (S6 '# === violations to fix ==='), "
    "the patch grammar v2 (S5), and the output envelope (S7). %s\n"
    "- The leaf id is %s.\n\n"
    "TASK -- for each violation:\n"
    "- Decide whether a minimal, safe, legal repair exists using ONLY "
    "editable polygons / allowed instance ops.\n"
    "- PREFER repairs that introduce NO new violation.\n"
    "- A candidate that cannot avoid collateral is still submittable when "
    "the window preview shows NET DRC reduction (violations cleared "
    "strictly greater than violations introduced) AND connectivity "
    "preserved -- declare every introduced violation (rule + bbox) in the "
    "trace as DECLARED DEBT.\n"
    "- Stay legal and on-grid: manufacturing grid 1 dbu; respect each "
    "layer's own routing-grid AUX rules.\n"
    "- Fewer ops better. If no net-reducing legal fix exists, leave it out "
    "(empty ops is valid).\n\n"
    "SUBMISSION STANDARD:\n"
    "- Follow the final ## Output section (S7) exactly.\n"
    "- The patch JSON explanation field: 1-2 sentences naming the "
    "violation(s) addressed and the polygon(s) edited.\n"
    "- The validator is deterministic Python; if your patch is malformed, "
    "the leaf is silently skipped.\n\n"
    "FINAL OUTPUT: see S7 (output requirements are centralized there).\n\n")

# S2 collects every resource path and the rules for reading them; the rule
# deck is named here and nowhere else, and the two placeholders take the
# technology directory. The forbidden-reads sentence carries a case-name
# literal that build_header rewrites for other cases.
S2 = (
    "=== S2: RESOURCES & PATHS ===\n\n"
    "Reference resources, in PRIORITY ORDER (all staged read-only; "
    "SUBAGENT-READ per CONTEXT HYGIENE below):\n"
    "1. Living repair knowledge -- PRIMARY rule source: /work/in/main.md "
    "(Read it FIRST: gating doctrine (PART A, binding) + LAYER INDEX) plus "
    "the per-layer knowledge files under /work/in/knowledge/.\n"
    "   - Each layer file's [DRC RULES] section carries that layer's "
    "verbatim deck rules (implementation + derivations); [KNOWLEDGE] "
    "carries the distilled repair heuristics.\n"
    "   - START with the layers that have violations in YOUR crop: map "
    "each violation's rule name to its layers -- the layer tokens (M*/V*) "
    "in the rule name, at most 2; both appear in the crop's rule "
    "descriptions -- and have your PLANNER and CODER subagents Read those "
    "violated layers' files FIRST at the INDEX paths.\n"
    "   - Add a layer's file ONLY when you plan to edit geometry on it.\n"
    "2. Per-rule DRM images: %s/drm_jpg/<rule>.jpg (e.g. M1.S.4.jpg) -- "
    "each rule's geometric intent, alongside the layer files' "
    "[DRC RULES].\n"
    "3. Full rule deck -- FALLBACK ONLY: %s/asap7.lydrc; consult it only "
    "for a layer you plan to EDIT that has no staged knowledge file, or "
    "for cross-layer derivations not visible in the layer files.\n\n"
    "Background reference: /work/in/skill_official.md (base reference "
    "skill).\n"
    "On any conflict: main.md's gating doctrine and THIS prompt win.\n\n"
    "FORBIDDEN READS: do NOT read the full Block5 layout script, other "
    "crops/leaves, the agent source, or scoring files.\n\n"
    "CONTEXT HYGIENE:\n"
    "- You are the MAIN agent: do NOT read the reference resources into "
    "your OWN context; they are NOT inlined here.\n"
    "- When a role needs a reference, have that PLANNER or CODER subagent "
    "Read it; spread the reads across your subagents.\n\n"
    "PAGING GUARD (applies to EVERY file Read in this task, by any "
    "agent):\n"
    "- First check the file's line count (e.g. wc -l via Bash, or a "
    "probing Read).\n"
    "- If it may exceed 1800 lines OR ~20k tokens (the Read tool truncates "
    "near 25k tokens -- the rule deck does), Read it in pages with "
    "offset/limit.\n"
    "- NEVER assume a single Read returned the whole file.\n\n")

# S3 describes the four-role loop: planner, plan reviewer, coder, patch
# reviewer. The reviewer steps stay short and point at the verification
# standards in S4 rather than restating them.
S3 = (
    "=== S3: SUBAGENT ROLES & REPAIR WORKFLOW ===\n\n"
    "REPAIR WORKFLOW -- you are the MAIN agent and you MUST divide the work "
    "across subagents in a FOUR-ROLE loop: PLANNER -> PLAN-REVIEWER -> CODER "
    "-> PATCH-REVIEWER. Do NOT write a one-shot patch. Every subagent you "
    "spawn inherits this model and effort.\n"
    "1. PLANNER: spawn a planner subagent. Give it the block/crop, its "
    "target violations, the connectivity constraint to preserve, the patch "
    "grammar, and the skill. It returns ONE concrete candidate repair PLAN "
    "(which polygons / via structures / instances to edit, and how) that is "
    "minimal, safe, and legal. Planner sub-steps:\n"
    "   1a. Parse the violations from '# === violations to fix ===' (S6): "
    "note each violation type (rule) and bounding box.\n"
    "   1b. Study each violated rule per the S2 priority order (violated "
    "layers' [DRC RULES] sections first; DRM image; full deck as FALLBACK "
    "ONLY): the check logic (KLayout Ruby DRC API, layer derivations, "
    "measurement ops), the layer(s) involved, the geometric constraint "
    "(min width / spacing / enclosure, exact pitch, forbidden bend, "
    "area, ...), and the numeric threshold + unit. Units: nanometers in "
    "ASAP7; crop coords are raw integers in dbu, 1 dbu = 0.00025 um = "
    "0.25 nm -- confirm the scale from the crop header. Do NOT guess "
    "thresholds or rule semantics.\n"
    "   1c. Locate the offending geometry: in the '## Crop' snippet (S6), "
    "map each violation bbox to the editable polygon(s) / instance(s) "
    "listed there.\n"
    "   REPAIR ORDER (mandatory, REGIONAL before GLOBAL):\n"
    "   - FIRST try the REGIONAL ops for each violation: move_instance / "
    "guarded delete_instance, or a top-level polygon op (resize / "
    "resize_end / move / delete / add_jog / add_polygon / add_via) -- "
    "effect stays local to this crop's neighborhood.\n"
    "   - ONLY IF no regional op can clear it: escalate to editing the VIA "
    "STRUCTURE via resize_via_shape / move_via_shape. That escalation is "
    "GLOBAL (see '## Shared-target context' (S6) for admissibility and how "
    "the harness measures def-level candidates block-wide).\n"
    "   - A via-structure plan MUST state the expected effect at the OTHER "
    "placements of that via type, not just the in-crop ones.\n"
    "   - COUPLED edits (spanning multiple shared definitions, or a def "
    "edit plus companion polygon/instance edits): plan them as ONE atomic "
    "candidate -- mark every coupled op with the same "
    "{\"group\": \"<name>\"} key (full spec in S4). A def edit that "
    "measures non-negative SOLO can become net-negative when measured WITH "
    "its coupled companions.\n"
    "2. PLAN-REVIEWER: spawn a SEPARATE subagent and give it ONLY the "
    "planner's PLAN. It ADVERSARIALLY reviews the plan, applying the "
    "VERIFICATION STANDARDS & TOOLS (S4) -- NET-reduction bar, HIERARCHY "
    "OF STANDARDS, atomic-group rules, MANDATORY SHARED-TARGET CHECK, and "
    "preview-tool verification -- to the PLAN. Any resize_via_shape / "
    "move_via_shape whose motivating rule is not marked (=100%%) in "
    "'## Shared-target context' (S6) is an automatic REJECT. It returns "
    "APPROVE, or REJECT with specific, actionable reasons.\n"
    "3. PLAN LOOP: while the plan-reviewer REJECTS, spawn a FRESH planner "
    "subagent carrying the reviewer's critique verbatim, and repeat 1->2. "
    "There is NO fixed iteration cap -- continue until the plan is APPROVED "
    "(if you exhaust your budget, carry the best-reviewed plan forward).\n"
    "4. CODER: once the PLAN is APPROVED, spawn a coder subagent. Give it "
    "the approved plan plus the patch grammar; it implements the plan into "
    "the CONCRETE patch -- the exact EvoDRC ops JSON: a flat list of op "
    "dicts drawn ONLY from the op vocabulary (S5), referencing the real ids "
    "exactly as they appear. Coder rules:\n"
    "   - Apply the MINIMAL repair: the smallest geometric tweak that "
    "clears the violation, per the NET-reduction standard (S4); declare "
    "any introduced violation as DEBT in the trace.\n"
    "   - Verify internal consistency before handing off: edits stay "
    "within block_bounds_dbu; targets and grid legality follow the TASK "
    "(S1); the JSON matches the patch grammar (S5).\n"
    "   - If the approved plan declares an atomic group, every op of that "
    "group must carry the same {\"group\": \"<name>\"} key in the final "
    "ops JSON.\n"
    "5. PATCH-REVIEWER: spawn a SEPARATE subagent and give it the coder's "
    "FINAL PATCH. It ADVERSARIALLY reviews the concrete patch, applying "
    "the SAME VERIFICATION STANDARDS & TOOLS (S4) to the CONCRETE ops. It "
    "re-runs the MANDATORY SHARED-TARGET CHECK (S4): any resize_via_shape "
    "/ move_via_shape whose motivating rule is not marked (=100%%) in "
    "'## Shared-target context' (S6) is an automatic REJECT. It returns "
    "APPROVE, or REJECT with specific reasons.\n"
    "6. PATCH LOOP + ESCALATION: while the patch-reviewer REJECTS, spawn a "
    "FRESH coder subagent carrying the critique and repeat 4->5 (no fixed "
    "cap). HOWEVER, if the patch-reviewer concludes the PLAN ITSELF is "
    "flawed (no legal patch can satisfy it), it MUST escalate: discard the "
    "plan and RESTART FROM STEP 1 with a fresh planner carrying the "
    "escalation critique.\n"
    "7. FINALIZE: only once the patch-reviewer APPROVES, you (the MAIN "
    "agent) aggregate and emit the final approved patch plus a concise "
    "reasoning trace, exactly per the ## Output section (S7). Stop only "
    "when the patch-reviewer has APPROVED.\n\n")


# --------------------------------------------------------------------------
# Whole-design header variants
#
# Used when the entire block is one repair unit. They follow the same
# formatting convention as the crop-mode versions. Facts that depend on the
# staged files -- sizes and counts -- arrive as <TOKEN> placeholders that are
# substituted after the single % pass. S3 is the standard S3 with two planner
# sub-steps re-pointed at the layout and DRC files.
# --------------------------------------------------------------------------
S1_WHOLE = (
    "=== S1: MISSION & TASK ===\n\n"
    "- You are an EDA engineer specializing in ASAP7 PDK block-level DRC "
    "repair.\n"
    "- You repair the WHOLE block design as ONE unit -- there is NO "
    "window/crop decomposition. The design layout script and the full DRC "
    "violation list are staged BY PATH (S2/S6); they are NOT inlined. "
    "Inlined below: the patch grammar v2 (S5) and the output envelope "
    "(S7). %s\n"
    "- The unit id is %s.\n\n"
    "TASK -- for each violation:\n"
    "- Decide whether a minimal, safe, legal repair exists using ONLY "
    "editable polygons / allowed instance ops.\n"
    "- PREFER repairs that introduce NO new violation.\n"
    "- A candidate that cannot avoid collateral is still submittable when "
    "the window preview shows NET DRC reduction (violations cleared "
    "strictly greater than violations introduced) AND connectivity "
    "preserved -- declare every introduced violation (rule + bbox) in the "
    "trace as DECLARED DEBT.\n"
    "- Stay legal and on-grid: manufacturing grid 1 dbu; respect each "
    "layer's own routing-grid AUX rules.\n"
    "- Fewer ops better. If no net-reducing legal fix exists, leave it out "
    "(empty ops is valid).\n\n"
    "SUBMISSION STANDARD:\n"
    "- Follow the final ## Output section (S7) exactly.\n"
    "- The patch JSON explanation field: 1-2 sentences naming the "
    "violation(s) addressed and the polygon(s) edited.\n"
    "- The validator is deterministic Python; if your patch is malformed, "
    "the leaf is silently skipped.\n\n"
    "FINAL OUTPUT: see S7 (output requirements are centralized there).\n\n")

# The whole-design S2 adds the task data to the resource list as entries 0 and
# 0b, referenced by path. The crop-mode ban on reading the full layout is
# dropped here, since the layout and the DRC list are now the task data
# itself; the context and paging guidance is unchanged.
S2_WHOLE = (
    "=== S2: RESOURCES & PATHS ===\n\n"
    "Reference resources, in PRIORITY ORDER (all staged read-only; "
    "SUBAGENT-READ per CONTEXT HYGIENE below):\n"
    "0. <LAYOUT_PATH> -- the FULL design layout script (~<LAYOUT_BYTES> "
    "bytes, <LAYOUT_LINES> lines): SUBAGENT paged reads MANDATORY per the "
    "PAGING GUARD below; NEVER read it into your MAIN context.\n"
    "0b. <DRC_PATH> -- the FULL violation list (<N_VIOL> violations, "
    "<N_RULES> rules): have a PLANNER subagent Read it (paged).\n"
    "1. Living repair knowledge -- PRIMARY rule source: /work/in/main.md "
    "(Read it FIRST: gating doctrine (PART A, binding) + LAYER INDEX) plus "
    "the per-layer knowledge files under /work/in/knowledge/.\n"
    "   - Each layer file's [DRC RULES] section carries that layer's "
    "verbatim deck rules (implementation + derivations); [KNOWLEDGE] "
    "carries the distilled repair heuristics.\n"
    "   - START with the layers that have violations in YOUR crop: map "
    "each violation's rule name to its layers -- the layer tokens (M*/V*) "
    "in the rule name, at most 2; both appear in the crop's rule "
    "descriptions -- and have your PLANNER and CODER subagents Read those "
    "violated layers' files FIRST at the INDEX paths.\n"
    "   - Add a layer's file ONLY when you plan to edit geometry on it.\n"
    "2. Per-rule DRM images: %s/drm_jpg/<rule>.jpg (e.g. M1.S.4.jpg) -- "
    "each rule's geometric intent, alongside the layer files' "
    "[DRC RULES].\n"
    "3. Full rule deck -- FALLBACK ONLY: %s/asap7.lydrc; consult it only "
    "for a layer you plan to EDIT that has no staged knowledge file, or "
    "for cross-layer derivations not visible in the layer files.\n\n"
    "Background reference: /work/in/skill_official.md (base reference "
    "skill).\n"
    "On any conflict: main.md's gating doctrine and THIS prompt win.\n\n"
    "FORBIDDEN READS: do NOT read the agent source, scoring files, or "
    "other runs' /out directories.\n\n"
    "CONTEXT HYGIENE:\n"
    "- You are the MAIN agent: do NOT read the reference resources into "
    "your OWN context; they are NOT inlined here.\n"
    "- When a role needs a reference, have that PLANNER or CODER subagent "
    "Read it; spread the reads across your subagents.\n\n"
    "PAGING GUARD (applies to EVERY file Read in this task, by any "
    "agent):\n"
    "- First check the file's line count (e.g. wc -l via Bash, or a "
    "probing Read).\n"
    "- If it may exceed 1800 lines OR ~20k tokens (the Read tool truncates "
    "near 25k tokens -- the rule deck does), Read it in pages with "
    "offset/limit.\n"
    "- NEVER assume a single Read returned the whole file.\n\n")

# The two planner sub-steps that change in whole-design mode, where the data
# is referenced by path rather than inlined.
_S3_1A_LEGACY = (
    "   1a. Parse the violations from '# === violations to fix ===' (S6): "
    "note each violation type (rule) and bounding box.\n")
_S3_1A_WHOLE = (
    "   1a. Parse the violations from <DRC_PATH> (S6 gives the path + "
    "per-rule counts): have a PLANNER subagent Read it (paged); note each "
    "violation type (rule) and bounding box.\n")
_S3_1C_LEGACY = (
    "   1c. Locate the offending geometry: in the '## Crop' snippet (S6), "
    "map each violation bbox to the editable polygon(s) / instance(s) "
    "listed there.\n")
_S3_1C_WHOLE = (
    "   1c. Locate the offending geometry: have a PLANNER subagent Read "
    "the layout script <LAYOUT_PATH> (paged, per the PAGING GUARD) and map "
    "each violation bbox to the editable polygon(s) / instance(s); the "
    "static '## Repair order by DRC degree' table (S6) ranks the top "
    "editable objects.\n")


def s3_whole():
    """Return S3 with the two whole-design planner sub-steps substituted in.

    The assertion catches the case where S3 has been edited such that the
    sentences being replaced no longer exist."""
    assert _S3_1A_LEGACY in S3 and _S3_1C_LEGACY in S3, \
        "S3 drift: whole-design sub-step swap anchors missing"
    return (S3.replace(_S3_1A_LEGACY, _S3_1A_WHOLE)
            .replace(_S3_1C_LEGACY, _S3_1C_WHOLE))


def _cell_extent(geom, cell_name):
    """Cell-local bounding box of a definition's shapes, or None when the
    definition is unknown or has no shapes."""
    cd = geom.cell_defs.get(cell_name)
    xs, ys = [], []
    for _lyr, pts, _cut in (cd.shapes if cd else []):
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def _bbox_overlap(a, b, margin=8):
    return not (a[2] + margin <= b[0] or b[2] <= a[0] - margin
                or a[3] + margin <= b[1] or b[3] <= a[1] - margin)


def build_shared_target_context(ctx, leaf):
    """Build the prompt section describing targets this crop shares with the
    rest of the block.

    The prompt builder sees the whole block, so it can compute facts the model
    cannot derive from its crop alone. For every shared target visible in the
    crop it reports:
      * via definitions: total placements, the split by owning net, how many
        this crop owns, and the fraction of placements violating each of the
        crop's rules -- a fraction of 100% means the defect is inherent to the
        definition, so editing the structure is justified;
      * polygons claimed by more than one unit;
      * editable polygons whose footprint spans much of the die.

    These are statistics over the input layout and input DRC report only.
    """
    geom = ctx.geometry_model
    out = []
    out.append("## Shared-target context (block-wide, input-derived)")
    out.append(
        "How to read: a structure edit on a shared definition re-renders at "
        "EVERY placement block-wide. It is admissible ONLY for a rule marked "
        "(=100%) below -- any smaller fraction proves compliant siblings "
        "exist, so the defect is POSITIONAL: fix by move/delete or leave "
        "unfixed. Your own window is violation-biased by construction and "
        "NEVER overrides these fractions. The harness measures every "
        "def-level candidate across coverage windows spanning its whole "
        "footprint and rejects it unless the combined DRC amount drops and "
        "connectivity holds.")

    # --- instance ownership, taken from the per-net power-grid crops ---------
    own_sets = {}
    for lid in sorted(ctx.leaves):
        L = ctx.leaves[lid]
        if getattr(L, "is_pdn", False):
            label = str(getattr(L, "pdn_rail", "") or "PDN").upper() or "PDN"
            own_sets.setdefault(label, set()).update(L.subcell_instances or [])

    mine = set(leaf.subcell_instances or [])
    vlist = list(getattr(ctx, "violations", None) or [])
    vmap = {v.violation_id: v for v in vlist}
    crop_rules = sorted({vmap[vid].rule_id for vid in (leaf.violations or [])
                         if vid in vmap})

    defs_here = sorted({geom.instances[i].cell_name for i in mine
                        if i in geom.instances
                        and str(geom.instances[i].cell_name).startswith("VIA")})
    for cn in defs_here:
        ex = _cell_extent(geom, cn)
        if ex is None:
            continue
        ids = [(iid, ins) for iid, ins in geom.instances.items()
               if ins.cell_name == cn]
        total = len(ids)
        split_cnt = {}
        pboxes = []
        own_k = 0
        for iid, ins in ids:
            dom = "SIGNAL"
            for label in sorted(own_sets):
                if iid in own_sets[label]:
                    dom = label
                    break
            split_cnt[dom] = split_cnt.get(dom, 0) + 1
            if iid in mine:
                own_k += 1
            ox, oy = ins.origin_dbu
            pboxes.append((ox + ex[0], oy + ex[1], ox + ex[2], oy + ex[3]))
        rule_bits = []
        for r in crop_rules:
            vbs = [v.bbox_dbu for v in vlist if v.rule_id == r]
            if not vbs:
                continue
            vr = sum(1 for p in pboxes if any(_bbox_overlap(p, b) for b in vbs))
            if vr:
                rule_bits.append("%s: %d/%d violating%s"
                                 % (r, vr, total,
                                    " (=100%)" if vr == total else ""))
        split_txt = " + ".join("%d %s" % (split_cnt[k], k)
                               for k in sorted(split_cnt))
        out.append("- %s: %d placements = %s; this crop owns %d (your preview "
                   "tools cover ONLY the owned/in-window ones); %s"
                   % (cn, total, split_txt, own_k,
                      "; ".join(rule_bits)
                      if rule_bits else "no crop-rule violations attributed"))

    # --- bridge polygons claimed by more than one unit ----------------------
    for pid in sorted(set(leaf.bridge_polygons or [])):
        k = 0
        for L in ctx.leaves.values():
            if pid in (L.editable_polygons or []) \
                    or pid in (L.bridge_polygons or []):
                k += 1
        if k > 1:
            out.append("- polygon %s: shared with %d units in total; edit ONLY "
                       "your in-crop open end -- same-end conflicts are "
                       "settled by the harness's measured arbitration."
                       % (pid, k))

    # --- editable polygons whose footprint dwarfs this window ---------------
    bb = geom.block_bounds_dbu
    die_w = max(1, int(bb[2]) - int(bb[0]))
    die_h = max(1, int(bb[3]) - int(bb[1]))
    for pid in sorted(set(leaf.editable_polygons or [])):
        p = geom.polygons.get(pid)
        if p is None:
            continue
        px = p.bbox_dbu
        if (px[2] - px[0]) >= 0.6 * die_w or (px[3] - px[1]) >= 0.6 * die_h:
            n_along = sum(1 for v in vlist if _bbox_overlap(px, v.bbox_dbu))
            out.append("- polygon %s spans ~%d%% of the die (footprint far "
                       "beyond this window); %d violations touch it "
                       "block-wide. A full-edge resize is a GLOBAL op: same "
                       "admissibility and harness measurement as a via-def "
                       "edit." % (pid,
                                  int(100.0 * max((px[2]-px[0]) / float(die_w),
                                                  (px[3]-px[1]) / float(die_h))),
                                  n_along))
    if len(out) <= 2:
        return ""
    return "\n".join(out) + "\n\n"


def _file_size_lines(path):
    """Return ``(bytes, line count)`` for a staged file, or ``(0, 0)`` if it
    cannot be read."""
    try:
        nbytes = int(os.path.getsize(path))
        n = 0
        with open(path, "rb") as fh:
            for _ in fh:
                n += 1
        return nbytes, n
    except Exception:  # noqa: BLE001
        return 0, 0


def whole_header_info(ctx, layout_path, drc_path):
    """Collect the whole-design facts that fill the <TOKEN> placeholders in S2.

    The caller passes the paths of the actually staged layout and DRC report,
    so the prompt names files the model can read and the size and count facts
    are measured on those same files."""
    nbytes, nlines = _file_size_lines(layout_path)
    vlist = list(getattr(ctx, "violations", None) or [])
    return {"layout_disp": layout_path,
            "drc_disp": drc_path,
            "layout_bytes": nbytes, "layout_lines": nlines,
            "n_viol": len(vlist),
            "n_rules": len({v.rule_id for v in vlist})}


def build_whole_data_section(ctx, leaf, layout_path, drc_path):
    """Build the whole-design data section of the prompt.

    It names the layout and DRC files by path rather than inlining them, and
    adds the per-rule violation counts, the block bounds and a catalog of via
    definitions. This replaces the inlined crop and per-violation detail that
    the prompt body emits in crop mode."""
    from ..crop_body import _layer_name_for_gds
    geom = ctx.geometry_model
    info = whole_header_info(ctx, layout_path, drc_path)
    vlist = list(getattr(ctx, "violations", None) or [])
    counts = {}
    for v in vlist:
        counts[v.rule_id] = counts.get(v.rule_id, 0) + 1
    bb = geom.block_bounds_dbu
    out = []
    out.append("## Design data (whole-design mode)")
    out.append("")
    out.append("- Layout script (FULL design): %s (~%d bytes, %d lines). "
               "NOT inlined -- SUBAGENT paged reads MANDATORY per the "
               "PAGING GUARD (S2)."
               % (info["layout_disp"], info["layout_bytes"],
                  info["layout_lines"]))
    out.append("- DRC violation list (FULL): %s -- %d violations across %d "
               "rules. NOT inlined -- have a PLANNER subagent Read it "
               "(paged)." % (info["drc_disp"], info["n_viol"],
                             info["n_rules"]))
    out.append("- Block bounds (dbu): [%d, %d, %d, %d]; every edit must "
               "stay inside them."
               % (int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])))
    out.append("- Coordinate scale: raw integers in dbu, 1 dbu = 0.00025 um "
               "= 0.25 nm.")
    out.append("")
    out.append("Per-rule violation counts (from %s):" % info["drc_disp"])
    out.append("")
    out.append("| rule | count |")
    out.append("|------|-------|")
    for rid in sorted(counts, key=lambda r: (-counts[r], r)):
        out.append("| %s | %d |" % (rid, counts[rid]))
    out.append("")
    out.append("## Via-def catalog (all design defs)")
    out.append("")
    out.append("Every via cell definition in the design (a via-structure "
               "edit re-renders at EVERY placement; see '## Shared-target "
               "context' above for admissibility):")
    n_place = {}
    for _iid, ins in geom.instances.items():
        n_place[ins.cell_name] = n_place.get(ins.cell_name, 0) + 1
    for cn in sorted(geom.cell_defs):
        cd = geom.cell_defs[cn]
        if cd.kind != "via":
            continue
        shp = []
        for (gds, pts, cut) in cd.shapes:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            shp.append("%s (%d,%d,%d,%d) %s"
                       % (_layer_name_for_gds(gds), min(xs), min(ys),
                          max(xs), max(ys), "cut" if cut else "land"))
        out.append("- %s: %d placement(s); shapes: %s"
                   % (cn, n_place.get(cn, 0), "; ".join(shp)))
    return "\n".join(out) + "\n"


def _repoint_paths(s, inject):
    """Rewrite the placeholder knowledge-mount paths in the template onto the
    staged injection directory.

    Both the crop-mode and whole-design S2 carry the same navigation block, so
    both are rewritten; leaving one alone would ship a dead path. This runs
    after the single ``%`` expansion, so it cannot disturb the positional
    format arguments."""
    s = s.replace("/work/in/main.md", inject["main"])
    s = s.replace("/work/in/knowledge/",
                  inject["knowledge_dir"].rstrip("/") + "/")
    s = s.replace("/work/in/skill_official.md", inject["official"])
    assert "/work/in/" not in s, "unreplaced harness mount path in EXP3 header"
    return s


def build_header(leaf_id, inject, tc_dir, case_name, whole=None):
    """Render sections S1 to S3 of the prompt; the body supplies S4 to S7.

    ``inject``    the absolute paths of the staged knowledge files, as
                  returned by ``inject.stage()``.
    ``tc_dir``    the shared technology directory holding the rule deck and
                  the per-rule images; callers pass the directory containing
                  the rule deck.
    ``case_name`` replaces the one case-specific literal in the template.
    ``whole``     None for crop mode; otherwise the ``whole_header_info`` dict,
                  which selects the whole-design S1 and S2, applies the two S3
                  sub-step swaps and fills the <TOKEN> placeholders."""
    tools = ("The three preview-tool directives (Connectivity / DRC / "
             "Connectivity-impact) and the pre-output self-critique are in "
             "S4; the static '## Repair order by DRC degree' table is in "
             "S6.")
    if whole is not None:
        s = S1_WHOLE + S2_WHOLE + s3_whole()
    else:
        s = S1 + S2 + S3
    s = s % (tools, leaf_id, tc_dir, tc_dir)
    if whole is not None:
        s = (s.replace("<LAYOUT_PATH>", whole["layout_disp"])
             .replace("<DRC_PATH>", whole["drc_disp"])
             .replace("<LAYOUT_BYTES>", str(whole["layout_bytes"]))
             .replace("<LAYOUT_LINES>", str(whole["layout_lines"]))
             .replace("<N_VIOL>", str(whole["n_viol"]))
             .replace("<N_RULES>", str(whole["n_rules"])))
    s = _repoint_paths(s, inject)
    if case_name != "Block5":
        s = s.replace("full Block5 layout", "full %s layout" % case_name)
    return s
