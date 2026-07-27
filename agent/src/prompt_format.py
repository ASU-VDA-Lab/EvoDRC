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

"""Builds the prompt that is sent to the model for one leaf.

The fixed parts of the prompt -- the role preamble, the patch grammar, the
editing rules and the output envelope -- are string constants in this module,
so this source file is the only place that text lives. The variable parts are
rendered per leaf: the crop of layout to repair, the violations inside it, the
rules those violations come from, and the paths the model must write to.
Assembly happens entirely in memory; this module reads and writes no files.
"""


import json
import os
import re
from typing import List  # noqa: F401  (used in a type-comment annotation)

from . import crop_body
# Re-exported for callers that import these names from this module; re-export
# is the only use they have here.
from .types import CaseContext, Leaf, Polygon, SubcellInstance, Violation  # noqa: F401


def _via_edit_enabled():
    """Whether the prompt offers ops that edit the internals of a via cell.

    Controlled by the VIA_STRUCT_EDIT environment variable, enabled by
    default. When disabled, resize_via_shape and move_via_shape are dropped
    from the grammar, the subcell rules and the self-critique checklist. Read
    on every call so the setting can be toggled without a restart. The
    matching validator flag must agree, or the model is offered an op that is
    then rejected.
    """
    return os.environ.get("VIA_STRUCT_EDIT", "1") == "1"


def _via_add_enabled():
    """Whether the prompt offers the add_via op.

    Controlled by the VIA_ADD environment variable, enabled by default, and
    independent of VIA_STRUCT_EDIT. When disabled, the add_via grammar
    fragment and the placeable-via catalog are both left out.
    """
    return os.environ.get("VIA_ADD", "1") == "1"


def _exp3_prompt():
    """Whether to render the prompt in its seven-section layout.

    Controlled by the EXP3_PROMPT environment variable, off by default, in
    which case the older flat layout is produced instead.
    """
    return os.environ.get("EXP3_PROMPT", "0") == "1"


# ---------------------------------------------------------------------------
# Fixed prompt text
# ---------------------------------------------------------------------------

_SYSTEM_PREAMBLE = """\
You are an EDA engineer specializing in ASAP7 PDK block-level DRC repair.
You receive ONE cropped block layout in this prompt. Follow the final
## Output section exactly. The patch JSON explanation field must be 1-2
sentences naming the violation(s) addressed and the polygon(s) edited.
The validator is deterministic Python; if your patch is malformed, the
leaf is silently skipped.
"""


_INPUT_RESOURCES = """\
## Input resources

You have access to the following resources. Read each one carefully before
proceeding.
- Cropped block layout -- inlined below in "## Crop" (the layout to repair
  via patch ops).
- Violations to fix -- inlined below in "# === violations to fix ===".
- Design Rule Document (Path): /workspace/testcase/asap7/asap7.lydrc.
  The KLayout DRC rule file (.lydrc) that defines every design rule
  checked. Use this to understand the exact rule semantics, numeric
  thresholds, and layer references for each violation category.
- Design Rule Manual (DRM) Images (Path):
  /workspace/testcase/asap7/drm_jpg/<rule>.jpg. Per-rule JPGs named after
  the rule (e.g. M1.S.4.jpg); use alongside the rule file to see each
  rule's geometric intent.
- Accumulated repair knowledge (Path): /work/in/knowledge.md. Read it
  yourself with the Read tool; cross-iteration, generalizable DRC-repair
  heuristics distilled from prior iterations (may be empty on iteration 1).
"""


# ---------------------------------------------------------------------------
# Seven-section prompt layout
# ---------------------------------------------------------------------------
# Sections S1 to S3 are rendered by the caller that runs a leaf repair; this
# module renders S4 to S7. The list below fixes the canonical order and is
# read by callers that need to check a prompt is well formed. Only the
# sectioned layout emits these banners; the flat layout has none.
# ---------------------------------------------------------------------------
EXP3_SECTION_BANNERS = [
    "=== S1: MISSION & TASK ===",
    "=== S2: RESOURCES & PATHS ===",
    "=== S3: SUBAGENT ROLES & REPAIR WORKFLOW ===",
    "=== S4: VERIFICATION & TOOLS ===",
    "=== S5: EDIT RULES ===",
    "=== S6: DATA ===",
    "=== S7: OUTPUT ===",
]


# The review standards the model is asked to apply to its own patch: when a
# candidate is good enough to submit, how coupled edits are grouped, when an
# edit to a shared cell definition may be attempted, and which preview tools
# must be run first. Kept here as the one place this text is defined, and
# interpolated by concatenation rather than %-formatting so literal percent
# signs need no escaping.
_S4_STANDARDS = """\
VERIFICATION STANDARDS -- applied by BOTH reviewer roles (S3 step 2 to the
PLAN, S3 step 5 to the CONCRETE ops):

NET-REDUCTION BAR:
- APPROVE when the previews show NET DRC reduction (cleared > introduced)
  AND connectivity preserved AND every op legal/on-grid.
- PREFER a zero-new-violation candidate when one exists.
- Any introduced violations MUST be listed in the trace (rule + bbox) as
  declared debt.

HIERARCHY OF STANDARDS:
- The net-reduction bar above governs ALL ordinary edits.
- ONE exception: a def edit ADMITTED by the (=100%) shared-target test.
  Your window cannot price a block-wide edit -- do NOT self-reject it on
  secondary in-window preview noise; such a candidate may carry declared
  debt and MUST be submitted for the harness's block-wide combined
  measurement (doctrine G4), which is the binding judge.

ATOMIC GROUPS (coupled edits, part of the hierarchy above):
- When a def edit needs coupled companion edits (e.g. coupled resizes on
  multiple shared definitions, or a def resize plus a die-spanning polygon
  resize): mark EVERY coupled op with the same {"group": "<name>"} key.
- Group WITH at least one def-level or die-spanning-resize member: the
  harness measures and applies it as ONE atomic candidate over the pooled
  targets' block-wide coverage windows PLUS, when the group carries
  regional members, your unit's own window (those members are priced in
  your window; effects outside all measured windows are NOT priced -- keep
  coupled edits near the group's targets).
- All-regional group: the group key is ignored and the ops flow through
  normal per-unit gating.
- Group members MUST use only resize / resize_end / move / delete /
  move_instance / delete_instance / resize_via_shape / move_via_shape /
  add_via.
- A group WITH at least one def-level or die-spanning-resize member that
  also contains add_polygon or add_jog is rejected unmeasured;
  all-regional groups are exempt from that rejection (their key is simply
  ignored).

MANDATORY SHARED-TARGET CHECK:
- Trigger: the plan or patch contains resize_via_shape / move_via_shape
  (or a full-edge op on a die-spanning polygon).
- Look up the motivating rule for that cell in '## Shared-target context'
  (S6: DATA).
- Unless that rule is marked (=100%) there: REJECT; demand a regional fix
  (move/delete) or leaving the violation unfixed.
- An in-window 'all placements look broken' impression NEVER overrides the
  injected block-wide fraction.

PREVIEW-TOOL VERIFICATION -- the reviewer MUST verify using the three
preview tools available in THIS run:
- drc_preview: do all target violations clear / are there new in-window
  violations?
- conn_preview: is connectivity preserved on the full design?
- conn_impact_preview: what does each edited object physically touch?
- Protocol: write the candidate {"ops":[...]} to a scratch file; run each
  tool against the pre-filled --context path (the three tool directives
  below); treat their one-line JSON verdicts as ground truth.
"""


_PROCEDURE = """\
## Procedure

Follow these steps in order.
Step 1 - Parse the violations: read the inlined "# === violations to fix
  ===" block; for each, note its violation type (rule) and bounding box.
Step 2 - Understand each violated rule: Read the design rule file at
  /workspace/testcase/asap7/asap7.lydrc thoroughly. For each violation
  type, study its check logic (KLayout Ruby DRC API, layer derivations,
  measurement ops), the layer(s) involved, the geometric constraint (min
  width / spacing / enclosure, exact pitch, forbidden bend, area, ...), and
  the numeric threshold + unit (nanometers in ASAP7; crop coords are raw
  integers in dbu, 1 dbu = 0.00025 um = 0.25 nm -- confirm the scale from
  the crop header). Also view the DRM image
  /workspace/testcase/asap7/drm_jpg/<rule>.jpg. Cross-reference the
  accumulated repair knowledge you Read from /work/in/knowledge.md. Do not
  guess thresholds or rule semantics.
Step 3 - Locate the offending geometry: in the inlined "## Crop" snippet,
  map each violation bbox to the editable polygon(s) / instance(s) listed
  below.
Step 4 - Determine and apply the MINIMAL repair as patch ops (smallest
  geometric tweak that clears the violation without introducing new ones).
Step 5 - Verify internal consistency: edits stay within block_bounds_dbu,
  only touch editable polygons / allowed instance ops, introduce no new
  spacing / width / enclosure violations, and the JSON matches the patch
  grammar.
"""


_PATCH_GRAMMAR_REFERENCE = """\
## Patch grammar (v2)

Polygon ops (target = polygon_id in editable_polygons OR bridge_polygons[ownership=self]):
  {"op": "add_polygon", "layer_name": "M1", "points": [[x1,y1], ...]}
     - The new polygon is inserted into the block's top cell
       (cell_<case_name>). Additive repair is a first-class strategy
       (enclosure patches, extensions, tie-in geometry).
  {"op": "resize",  "polygon_id": "pNNN", "axis": "x|y", "delta_dbu": <int>}
     - SYMMETRIC grow/shrink along the chosen axis: delta_dbu/2 on the lower
       edge and delta_dbu - delta_dbu/2 on the upper edge; the polygon's
       centre stays put. Negative delta_dbu shrinks. D-SECTION
       polygons (fully-contained editable); ONE C-section exception: a
       stripe marked WIDTH ONLY (both ends display-cut) accepts resize on
       its PERPENDICULAR (width) axis only.
  {"op": "resize_end", "polygon_id": "pNNN", "axis": "x|y", "end": "low|high", "delta_dbu": <int>}
     - SINGLE-END move: moves ONLY the chosen end's edge along axis. end="low"
       moves the min-coord edge to min - delta_dbu; end="high" moves the
       max-coord edge to max + delta_dbu. delta_dbu>0 ELONGATES that end
       (away from centre), delta_dbu<0 SHORTENS it. The OTHER end stays put.
     - C-SECTION ONLY: use on a partially-editable stripe to move ONLY a
       real (in-crop) end. A display-cut end is FROZEN -- resize_end on a
       frozen end, or move / add_jog on a C-section stripe, are REJECTED;
       symmetric resize on a C-section stripe is REJECTED except the
       WIDTH-ONLY perpendicular case under "resize" above.
  {"op": "move",    "polygon_id": "pNNN", "axis": "x|y", "delta_dbu": <int>}
  {"op": "delete",  "polygon_id": "pNNN"}
  {"op": "add_jog", "polygon_id": "pNNN", "jog_pts": [[x1,y1], ...]}
     - APPENDS the listed vertices to that polygon's vertex outline (a
       jog/notch). Each jog point is an absolute on-grid integer dbu pair
       inside the block bounds; at least one point required. REJECTED on a
       C-section stripe. Example with placeholder id
       (always use the real ids from YOUR crop): {"op": "add_jog",
       "polygon_id": "pA", "jog_pts": [[x1,y1], [x2,y2]]}

Instance ops (target = inst_id in subcell_instances; op must be in allowed_ops):
  {"op": "move_instance",   "inst_id": "iNNNN", "delta_dbu": [<int>, <int>]}
  {"op": "delete_instance", "inst_id": "iNNNN"}

Via-structure ops (target = a SHARED via cell's internal shape; edits the cell
DEFINITION so ALL instances of that via type change together):
  {"op":"resize_via_shape","cell_name":"VIA_VIA12","layer_name":"M1","shape_index":0,"axis":"x|y","delta_dbu":<int>}
     - SYMMETRIC grow/shrink of that land/cut about its centre (grow a land to
       fix an EN enclosure, widen/narrow the cut for a via width/spacing rule).
  {"op":"move_via_shape","cell_name":"VIA_VIA12","layer_name":"M1","shape_index":0,"axis":"x|y","delta_dbu":<int>}
     - TRANSLATE that land/cut. NOTE: shifts the shape for EVERY instance of the
       type (may realign some, misalign others) -- prefer resize_via_shape.
   cell_name = a via you OWN in section A; layer_name = a land (M*) or cut (V*)
   shown in that cell's A1 structure; shape_index (default 0) picks the Nth
   shape on that layer (needed only for array/strap vias with repeated cuts).
   REJECTED if cell_name is a std cell, not owned/movable here, or the layer /
   shape_index does not exist.

All delta_dbu values must be integers (MANUFACTURING_GRID_DBU = 1).
"""


# Variant used when via-structure editing is disabled: the "Via-structure ops"
# block is dropped, leaving a via editable only as a whole instance.
_PATCH_GRAMMAR_REFERENCE_NOVIA = """\
## Patch grammar (v2)

Polygon ops (target = polygon_id in editable_polygons OR bridge_polygons[ownership=self]):
  {"op": "add_polygon", "layer_name": "M1", "points": [[x1,y1], ...]}
     - The new polygon is inserted into the block's top cell
       (cell_<case_name>). Additive repair is a first-class strategy
       (enclosure patches, extensions, tie-in geometry).
  {"op": "resize",  "polygon_id": "pNNN", "axis": "x|y", "delta_dbu": <int>}
     - SYMMETRIC grow/shrink along the chosen axis: delta_dbu/2 on the lower
       edge and delta_dbu - delta_dbu/2 on the upper edge; the polygon's
       centre stays put. Negative delta_dbu shrinks. D-SECTION
       polygons (fully-contained editable); ONE C-section exception: a
       stripe marked WIDTH ONLY (both ends display-cut) accepts resize on
       its PERPENDICULAR (width) axis only.
  {"op": "resize_end", "polygon_id": "pNNN", "axis": "x|y", "end": "low|high", "delta_dbu": <int>}
     - SINGLE-END move: moves ONLY the chosen end's edge along axis. end="low"
       moves the min-coord edge to min - delta_dbu; end="high" moves the
       max-coord edge to max + delta_dbu. delta_dbu>0 ELONGATES that end
       (away from centre), delta_dbu<0 SHORTENS it. The OTHER end stays put.
     - C-SECTION ONLY: use on a partially-editable stripe to move ONLY a
       real (in-crop) end. A display-cut end is FROZEN -- resize_end on a
       frozen end, or move / add_jog on a C-section stripe, are REJECTED;
       symmetric resize on a C-section stripe is REJECTED except the
       WIDTH-ONLY perpendicular case under "resize" above.
  {"op": "move",    "polygon_id": "pNNN", "axis": "x|y", "delta_dbu": <int>}
  {"op": "delete",  "polygon_id": "pNNN"}
  {"op": "add_jog", "polygon_id": "pNNN", "jog_pts": [[x1,y1], ...]}
     - APPENDS the listed vertices to that polygon's vertex outline (a
       jog/notch). Each jog point is an absolute on-grid integer dbu pair
       inside the block bounds; at least one point required. REJECTED on a
       C-section stripe. Example with placeholder id
       (always use the real ids from YOUR crop): {"op": "add_jog",
       "polygon_id": "pA", "jog_pts": [[x1,y1], [x2,y2]]}

Instance ops (target = inst_id in subcell_instances; op must be in allowed_ops):
  {"op": "move_instance",   "inst_id": "iNNNN", "delta_dbu": [<int>, <int>]}
  {"op": "delete_instance", "inst_id": "iNNNN"}

All delta_dbu values must be integers (MANUFACTURING_GRID_DBU = 1).
"""


# The add_via grammar fragment is spliced in after the delete_instance line of
# whichever grammar variant is in use. That line occurs exactly once in each
# variant, so the fragment always lands inside the "Instance ops" block.
_DELETE_INSTANCE_LINE = "  {\"op\": \"delete_instance\", \"inst_id\": \"iNNNN\"}\n"
_ADD_VIA_GRAMMAR = """\
  {"op": "add_via", "cell_name": "VIA_*", "origin_dbu": [x, y]}
     - Creates ONE NEW instance of a DESIGN-PRESENT via cell def at that
       origin (rotation 0, no mirror). NEVER invent a cell name: pick one
       from this crop's "via cell types placeable with add_via" catalog.
       FREE placement -- no metal-overlap precondition (preview the result;
       the gate judges outcomes). Constraints: the cell's cut layer must be
       a via layer in THIS crop's editable band; the instance bbox must lie
       inside this crop window; REJECTED if its M1 land would overlap
       std-cell M1 geometry; disabled when VIA_ADD=0.
"""


_SUBCELL_PROTECTION_CLAUSE = """\
## Subcell instance protection rule

Block-level layout contains TWO categories of geometry:

(1) top_level polygons -- directly inserted by cell_<top>.shapes(...).insert(p).
    You MAY edit these via polygon ops: resize, move, delete.
    Target polygon_id MUST be in editable_polygons or bridge_polygons[ownership=self].

(2) subcell instances -- emitted as cell_<top>.insert(pya.CellInstArray(...)).
    Two kinds with DIFFERENT permissions:

    (2a) kind="via" -- PDK via cells (VIA_VIA12, VIA_VIA23, VIA_VIA34, VIA_VIA45,
         and parameterized variants like VIA_VIA12_1_3_36_36).
         allowed_ops = ["move_instance", "delete_instance"].
         NO rotate_instance (vias are symmetric).
         NO swap_instance (changing via type alters electrical impedance).
         Via INTERNAL structure IS editable via resize_via_shape / move_via_shape
         (see patch grammar): you may resize/move the metal lands (M*) and the
         V-cut (V*). This edits the SHARED VIA_* cell definition, so EVERY
         instance of that via type changes together -- weigh that same-type
         impact; the whole-block DRC + connectivity gate is the backstop.

    (2b) kind="stdcell" -- ASAP7 standard cells (INVx1_*, BUFx2_*, AND2x2_*,
         HAxp5_*, TAPCELL_*, DECAPx*_*, FILLER*_*).
         allowed_ops = [] -- COMPLETELY FROZEN. You MUST NOT emit any
         instance op targeting a stdcell. Placement is fixed by P&R timing
         closure; moving a stdcell breaks setup/hold timing.

You MUST NOT edit a polygon inside a STD-CELL definition
(cell_INVx1_ASAP7_75t_R.shapes(...), etc.) -- std-cell internals stay FROZEN
(fab signoff / PDK compliance). Via cell internals are the ONLY subcell shapes
you may edit, and ONLY through resize_via_shape / move_via_shape (never a raw
polygon op).

Sub-M1 layers (V0, LISD, LIG, SDT, ACTIVE, GATE, FIN, WELL, NSELECT,
PSELECT, SLVT, LVT, SRAMVT) are NEVER exposed at block top level -- they
live exclusively inside stdcell internals. You will not see them in any
leaf JSON field; do not reference them.

All of the above are rejected at validator check 1 (provenance); the
entire patch is discarded and the leaf is marked skipped_invalid_patch
(no retry this iteration).
"""


# Variant used when via-structure editing is disabled: the via section and the
# closing paragraph declare via internals frozen.
_SUBCELL_PROTECTION_CLAUSE_NOVIA = """\
## Subcell instance protection rule

Block-level layout contains TWO categories of geometry:

(1) top_level polygons -- directly inserted by cell_<top>.shapes(...).insert(p).
    You MAY edit these via polygon ops: resize, move, delete.
    Target polygon_id MUST be in editable_polygons or bridge_polygons[ownership=self].

(2) subcell instances -- emitted as cell_<top>.insert(pya.CellInstArray(...)).
    Two kinds with DIFFERENT permissions:

    (2a) kind="via" -- PDK via cells (VIA_VIA12, VIA_VIA23, VIA_VIA34, VIA_VIA45,
         and parameterized variants like VIA_VIA12_1_3_36_36).
         allowed_ops = ["move_instance", "delete_instance"].
         NO rotate_instance (vias are symmetric).
         NO swap_instance (changing via type alters electrical impedance).
         A via is editable ONLY as a WHOLE instance (move_instance /
         delete_instance); its INTERNAL structure (metal lands M*, V-cut V*) is
         FROZEN -- the shared VIA_* cell definition must not be edited.

    (2b) kind="stdcell" -- ASAP7 standard cells (INVx1_*, BUFx2_*, AND2x2_*,
         HAxp5_*, TAPCELL_*, DECAPx*_*, FILLER*_*).
         allowed_ops = [] -- COMPLETELY FROZEN. You MUST NOT emit any
         instance op targeting a stdcell. Placement is fixed by P&R timing
         closure; moving a stdcell breaks setup/hold timing.

You MUST NOT edit a polygon inside a STD-CELL definition
(cell_INVx1_ASAP7_75t_R.shapes(...), etc.) -- std-cell internals stay FROZEN
(fab signoff / PDK compliance). Via cell internals are FROZEN too; a via is
editable ONLY as a whole instance (move_instance / delete_instance).

Sub-M1 layers (V0, LISD, LIG, SDT, ACTIVE, GATE, FIN, WELL, NSELECT,
PSELECT, SLVT, LVT, SRAMVT) are NEVER exposed at block top level -- they
live exclusively inside stdcell internals. You will not see them in any
leaf JSON field; do not reference them.

All of the above are rejected at validator check 1 (provenance); the
entire patch is discarded and the leaf is marked skipped_invalid_patch
(no retry this iteration).
"""


_SELF_CRITIQUE_CHECKLIST = """\
## Pre-output self-critique (adjustment-aware)

Before writing your patch, verify each:
1. Every targeted polygon_id is an editable polygon -- it appears under the
   `# --- D.` (editable) or `# --- C.` (partially editable, near end only)
   section, NOT under `# --- B.` background (neither a `_ptemp_` B(i) flattened
   polygon nor a real-pNNN B(ii) read-only/out-of-band neighbour); every
   instance op targets an owned, mobile via in `# --- A.` (NOT a std cell, NOT
   V0, NOT a non-owned via). Any via-structure op (resize_via_shape /
   move_via_shape) names a via you OWN in section A and a land/cut layer shown
   in its A1 structure.
2. Edits stay on the violation's layer band; you did not touch a background
   layer.
3. For a long stripe, you only shorten/elongate the OPEN end along its long
   axis and did not cross the leaf border.
4. For a via move, you stayed inside the stated move-freedom interval so the
   via still overlaps every tied land and respects spacing.
5. Fewer ops is better -- a 1-op fix beats a 6-op fix that risks new
   violations.
6. If EVERY candidate op risks a new violation, write an empty ops list. A
   skipped leaf (0 new violations) is strictly better than a regression.
"""


# Variant used when via-structure editing is disabled: item 1 loses its
# closing sentence about via-shape ops. Item 4 stays, since moving a whole via
# instance is still allowed.
_SELF_CRITIQUE_CHECKLIST_NOVIA = """\
## Pre-output self-critique (adjustment-aware)

Before writing your patch, verify each:
1. Every targeted polygon_id is an editable polygon -- it appears under the
   `# --- D.` (editable) or `# --- C.` (partially editable, near end only)
   section, NOT under `# --- B.` background (neither a `_ptemp_` B(i) flattened
   polygon nor a real-pNNN B(ii) read-only/out-of-band neighbour); every
   instance op targets an owned, mobile via in `# --- A.` (NOT a std cell, NOT
   V0, NOT a non-owned via).
2. Edits stay on the violation's layer band; you did not touch a background
   layer.
3. For a long stripe, you only shorten/elongate the OPEN end along its long
   axis and did not cross the leaf border.
4. For a via move, you stayed inside the stated move-freedom interval so the
   via still overlaps every tied land and respects spacing.
5. Fewer ops is better -- a 1-op fix beats a 6-op fix that risks new
   violations.
6. If EVERY candidate op risks a new violation, write an empty ops list. A
   skipped leaf (0 new violations) is strictly better than a regression.
"""


_OUTPUT_ENVELOPE_DIRECTIVE = """\
## Output envelope

Your patch file must contain a JSON object of the form (pure JSON, NO
fences):

{
  "leaf_id": "<must-match-leaf-id-from-the-crop-header>",
  "ops": [
    {"op": "resize", "polygon_id": "pA", "axis": "x", "delta_dbu": -96},
    {"op": "move_instance", "inst_id": "iA", "delta_dbu": [18, 0]}
  ],
  "explanation": "Short human-readable rationale (one or two sentences)."
}

Example: to fix an Mk spacing violation between two neighboring polygons pA
and pB (placeholder ids -- always use the real ids from YOUR crop), shrink
pA on the violating axis: {"op": "resize", "polygon_id": "pA", "axis": "x",
"delta_dbu": -96}.

If you cannot determine a fix, write an empty ops list:

{"leaf_id": "<leaf-id>", "ops": [], "explanation": "no safe fix"}

An empty patch is treated as "skip this leaf"; the next iteration's DRC
will catch the unfixed violations.
"""


# ---------------------------------------------------------------------------
# Rule cards
# ---------------------------------------------------------------------------

# Category code to a short description, used as a fallback when the rule id
# matches the "<LAYER>.<CATEGORY>.<N>" pattern but the rule database has no
# specific description for it.
_CATEGORY_BLURBS = {
    "S": ("spacing", "minimum spacing between {layer} shapes",
          "Fix by widening the gap; resize or move one shape."),
    "W": ("width", "minimum width on {layer} shapes",
          "Fix by resizing along the short axis."),
    "EN": ("enclosure", "{layer} enclosure constraint",
           "Fix by extending the enclosing shape."),
    "EX": ("extension", "{layer} extension constraint",
           "Fix by extending the polygon along the constrained axis."),
    "A": ("area", "minimum area on {layer} shapes",
          "Fix by resizing to gain area without breaking spacing."),
    "EOL": ("end-of-line", "end-of-line constraint on {layer}",
            "Fix by lengthening / blunting the EOL via resize."),
    "AUX": ("auxiliary", "auxiliary geometric constraint on {layer}",
            "Consult the rule_db / skill excerpt for specifics; "
            "minimal geometric tweak."),
}

# Family name to a short description, used when the leaf names a known rule
# family but no rule id in the canonical form is available.
_FAMILY_CARDS = {
    "spacing": ("Spacing rules require a minimum dbu distance between two "
                "shapes on the same or adjacent layers. Resize or jog one "
                "shape away; do not delete unless redundant."),
    "width":   ("Width rules enforce a minimum dbu width on a single shape. "
                "Resize the offending shape by delta_dbu along the short axis."),
    "enclosure": ("Enclosure rules require an outer layer to cover an inner "
                  "layer by N dbu on all sides. Resize the outer shape."),
    "area":    ("Area rules enforce a minimum polygon area. Resize the shape "
                "along its short axis to gain area without creating new "
                "spacing violations."),
    "eol":     ("End-of-line rules constrain the end of a metal segment. "
                "Use resize-axis to lengthen / blunt the EOL."),
    "min_size": ("Minimum size rules enforce a per-dimension minimum on the "
                 "shape. Resize along the offending axis."),
    "other":   ("Generic rule -- inspect the rule family in the rule_db and "
                "apply the minimal geometric fix."),
}

# Optional inner layer, then outer layer, category and number. For example
# M1.S.2, M5.AUX.1, V4.M5.AUX.2 and V0.M1.AUX.3.
_RULE_ID_RE = re.compile(
    r"^(?:(?P<inner>[A-Z]+\d*)\.)?(?P<layer>[A-Z]+\d*)\.(?P<cat>[A-Z]+)\.(?P<num>\d+)$"
)


def _classify_rule_family(rule_id):
    """Map a rule id to a coarse family name.

    Returns one of "spacing", "width", "enclosure", "area", "eol",
    "min_size", "other" or "unknown". Recognises the same token set as the
    classifier in the geometry model, so the two stay consistent.
    """
    if not rule_id:
        return "unknown"
    for part in str(rule_id).split("."):
        p = part.upper()
        if p in ("S", "SPACE", "SPACING"):
            return "spacing"
        if p in ("W", "WIDTH"):
            return "width"
        if p in ("EN", "ENC", "ENCLOSURE"):
            return "enclosure"
        if p in ("A", "AREA"):
            return "area"
        if p == "EOL":
            return "eol"
        if p in ("MIN", "SIZE"):
            return "min_size"
    return "other"


def _rule_db_lookup(rule_db, rule_id):
    """Pull a numeric threshold in dbu and a description out of a rule entry.

    Accepts several shapes of rule database -- mapping or object, with the
    value under any of a few key names -- and returns (None, None) when
    nothing usable is found.
    """
    if rule_db is None or not rule_id:
        return (None, None)
    # First try a .get() that returns a dict-like entry.
    entry = None
    getter = getattr(rule_db, "get", None)
    if callable(getter):
        try:
            entry = getter(rule_id)
        except Exception:
            entry = None
    if entry is None:
        # Then try subscripting the rule database directly.
        try:
            entry = rule_db[rule_id]  # type: ignore[index]
        except Exception:
            entry = None
    if entry is None:
        return (None, None)
    desc = None
    target = None
    if isinstance(entry, dict):
        desc = entry.get("description") or entry.get("desc")
        for key in ("min_dbu", "min_value", "value_dbu", "value"):
            val = entry.get(key)
            if isinstance(val, (int, float)):
                target = int(val)
                break
    else:
        desc = getattr(entry, "description", None) or getattr(entry, "desc", None)
        for key in ("min_dbu", "min_value", "value_dbu", "value"):
            val = getattr(entry, key, None)
            if isinstance(val, (int, float)):
                target = int(val)
                break
    return (target, desc)


def _rule_card_for_rule_id(rule_id, rule_db):
    """Return a one-line description of what a rule id constrains."""
    target, desc = _rule_db_lookup(rule_db, rule_id)
    if desc:
        if target is not None:
            return "{0} ({1} dbu). Fix per the rule_db description.".format(
                desc.rstrip(". "), target)
        return desc.rstrip(". ") + "."
    m = _RULE_ID_RE.match(str(rule_id or ""))
    if m:
        layer = m.group("layer")
        cat = m.group("cat")
        inner = m.group("inner")
        cat_entry = _CATEGORY_BLURBS.get(cat)
        if cat_entry is not None:
            _fam, what, fix = cat_entry
            if cat == "AUX" and inner:
                what = "{0} interaction with {1}".format(inner, layer)
            elif cat == "EN" and inner:
                what = "{0} enclosure of {1}".format(layer, inner)
            elif inner and cat in ("S", "W", "A"):
                what = what.format(layer=layer) + " (in context of " + inner + ")"
            else:
                what = what.format(layer=layer)
            if target is not None:
                return "{0}: minimum {1} dbu. {2}".format(what, target, fix)
            return what + ". " + fix
    # Nothing matched: echo the rule id back.
    return "rule {0} (no canonical category match; consult rule_db / skill).".format(
        rule_id)


def _rule_cards_for_leaf(leaf, ctx):
    """Build the rule cards section of the prompt for one leaf.

    Lists the rule ids that the leaf's violations refer to and points the
    model at the authoritative sources -- the rule deck and the per-rule
    drawing -- rather than paraphrasing the rules here, so it reads the real
    definitions itself. Returns a multi-line string.
    """
    lines = ["## Rule cards (active in this leaf)"]
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    rule_ids_in_leaf = []  # de-duplicated, first-seen order preserved
    for vid in leaf.violations:
        v = viol_by_id.get(vid)
        if v is None:
            continue
        rid = v.rule_id
        if rid and rid not in rule_ids_in_leaf:
            rule_ids_in_leaf.append(rid)
    if rule_ids_in_leaf:
        lines.append("Rule IDs active in this leaf: {0}.".format(
            ", ".join(rule_ids_in_leaf)))
    else:
        lines.append("No specific rule IDs resolved for this leaf; treat the "
                     "violations below as generic and inspect their layers.")
    if _exp3_prompt():
        # In the sectioned layout every file path is stated once, in S2, so
        # this wording points at that section instead of repeating them.
        lines.append(
            "Look up each rule's exact definition and numeric threshold per "
            "the S2 resource priority (the violated layers' [DRC RULES] "
            "sections first; full deck as FALLBACK ONLY), and view its DRM "
            "image (paths in S2). DRC rules interact -- before committing a "
            "fix, also check neighbouring rules on the same layers so your "
            "edit does not introduce a new violation.")
    else:
        lines.append(
            "Look up each rule's exact definition and numeric threshold in "
            "/workspace/testcase/asap7/asap7.lydrc (Step 2), and view its DRM "
            "image drm_jpg/<rule>.jpg. DRC rules interact -- before committing "
            "a fix, also check neighbouring rules on the same layers so your "
            "edit does not introduce a new violation.")
    return "\n".join(lines)


def _rule_cards_for(families):
    """Build rule cards from family names alone, without any rule ids."""
    lines = ["## Rule cards"]
    seen = []  # type: List[str]
    for f in families:
        if f in seen:
            continue
        seen.append(f)
        lines.append("- {0}: {1}".format(f, _FAMILY_CARDS.get(f, "")))
    if len(lines) == 1:
        lines.append("- (no rule families resolved; treat as generic)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Leaf JSON serializer (used by tooling; the prompt uses the KLayout crop)
# ---------------------------------------------------------------------------

def _serialize_leaf_json(leaf, ctx):
    polys = ctx.geometry_model.polygons if ctx.geometry_model else {}
    insts = ctx.geometry_model.instances if ctx.geometry_model else {}

    def poly_view(pid):
        p = polys.get(pid)
        if p is None:
            return {"polygon_id": pid, "missing": True}
        return {
            "polygon_id": p.polygon_id,
            "layer_name": p.layer_name,
            "layer_index": p.layer_index,
            "bbox_dbu": list(p.bbox_dbu),
            "owner_kind": p.owner_kind,
            "bridge_owner_leaf_id": p.bridge_owner_leaf_id,
        }

    def inst_view(iid):
        inst = insts.get(iid)
        if inst is None:
            return {"inst_id": iid, "missing": True}
        return {
            "inst_id": inst.instance_id,
            "cell_name": inst.cell_name,
            "kind": inst.kind,
            "allowed_ops": list(inst.allowed_ops),
            "origin_dbu": list(inst.origin_dbu),
        }

    payload = {
        "leaf_id": leaf.leaf_id,
        "violations": list(leaf.violations),
        "rule_families": list(leaf.rule_families),
        "strap_class": leaf.strap_class,
        "block_bounds_dbu": list(leaf.block_bounds_dbu),
        "bbox_dbu": list(leaf.bbox_dbu),
        "manufacturing_grid_dbu": 1,
        "editable_polygons": [poly_view(p) for p in leaf.editable_polygons],
        "bridge_polygons": [poly_view(p) for p in leaf.bridge_polygons],
        "context_readonly": [poly_view(p) for p in leaf.context_readonly],
        "subcell_instances": [inst_view(i) for i in leaf.subcell_instances],
    }
    return "## Leaf JSON\n\n```json\n" + json.dumps(payload, indent=2) + "\n```"


# ---------------------------------------------------------------------------
# Leaf serializer: the crop as a runnable KLayout Python snippet
# ---------------------------------------------------------------------------

def _resolve_top_cell_var(ctx):
    """Pick the variable name used for the top cell in the emitted snippet.

    Prefers ``ctx.geometry_model.top_cell_var`` when it is set, otherwise
    derives ``cell_<case_name>`` from the case, and falls back to
    ``cell_top``.
    """
    geom = getattr(ctx, "geometry_model", None)
    if geom is not None:
        tcv = getattr(geom, "top_cell_var", None)
        if tcv:
            return tcv
    case_info = getattr(ctx, "case_info", None)
    case_name = getattr(case_info, "case_name", "") if case_info else ""
    if case_name:
        return "cell_{0}".format(case_name)
    return "cell_top"


def _points_for(poly):
    """Return the (x, y) tuples that make up a polygon's outline.

    Falls back to the four corners of its bounding box when the stored
    outline is empty or has fewer than three points.
    """
    pts = tuple(poly.points_dbu) if poly.points_dbu else ()
    if len(pts) < 3:
        x1, y1, x2, y2 = poly.bbox_dbu
        return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    return [(int(x), int(y)) for (x, y) in pts]


def _format_points(pts):
    return ", ".join("pya.Point({0}, {1})".format(x, y) for (x, y) in pts)


def _emit_instance_block(iid, insts, top_cell_var):
    """Emit the comment header and the insert call for one instance."""
    lines = []
    inst = insts.get(iid)
    lines.append("# instance_id: {0}".format(iid))
    if inst is None:
        lines.append("# cell_name: <missing>  kind: <unknown>  allowed_ops: []")
        lines.append("# (instance not found in geometry_model -- skipped)")
        return lines
    lines.append(
        "# cell_name: {0}  kind: {1}  allowed_ops: {2}".format(
            inst.cell_name, inst.kind, list(inst.allowed_ops)))
    origin = inst.origin_dbu if inst.origin_dbu else (0, 0)
    ox, oy = int(origin[0]), int(origin[1])
    lines.append(
        "{0}.insert(pya.CellInstArray(cell_{1}.cell_index(), "
        "pya.Trans(0, False, pya.Vector({2}, {3}))))".format(
            top_cell_var, inst.cell_name, ox, oy))
    return lines


def _emit_instance_block_compact(iid, insts):
    """Emit a read-only instance as a single comment line, with no insert."""
    lines = []
    inst = insts.get(iid)
    if inst is None:
        lines.append("# instance_id: {0}  (missing from geometry_model)".format(iid))
        return lines
    origin = inst.origin_dbu if inst.origin_dbu else (0, 0)
    ox, oy = int(origin[0]), int(origin[1])
    lines.append(
        "# instance_id: {0}  cell={1}  origin=({2}, {3})".format(
            iid, inst.cell_name, ox, oy))
    return lines


def _violations_table_lines(leaf, ctx):
    """Return one comment line per violation in this leaf.

    Each line carries the violation id, its rule and its bounding box, for
    example::

      # v0001 violation type=M5.S.2 violation_bounding_box_in_dbu=(...)
    """
    viol_by_id = {v.violation_id: v for v in (ctx.violations or [])}
    n = len(leaf.violations)
    out = ["# === violations to fix (n={0}) ===".format(n)]
    if n == 0:
        return out
    # Emit the violations in the same order the rest of the crop uses:
    # clustered by via group or strip, then sorted by lowest metal and
    # position. The ordering is a permutation of the same ids, so the count
    # printed above still matches.
    for vid in crop_body._ordered_violations(leaf, ctx):
        v = viol_by_id.get(vid)
        if v is None:
            out.append("# {0}  (violation not found in ctx.violations)".format(vid))
            continue
        rule = (v.rule_id or "?")
        bbox = v.bbox_dbu if v.bbox_dbu else (0, 0, 0, 0)
        out.append(
            "# {0} violation type={1} "
            "violation_bounding_box_in_dbu=({2}, {3}, {4}, {5})".format(
                vid, rule,
                int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))
    return out


def _build_klayout_snippet_body(leaf, ctx):
    """Build the runnable KLayout Python body of a crop.

    Returns the lines that go inside the fenced code block, without the fence
    markers or the metadata comments that precede it. The body has four
    sections: owned vias, read-only background, partially editable stripes and
    fully editable polygons. The same builder produces the crop files written
    to disk, so the two can never drift apart.
    """
    return crop_body.build_body(leaf, ctx)


def _build_klayout_header_lines(leaf, ctx):
    """Metadata comments that precede the crop's fenced code block.

    The same lines appear at the top of an in-prompt snippet and of a crop
    file written to disk; only the section heading above them differs.
    """
    out = [
        "# leaf_id: {0}".format(leaf.leaf_id),
        "# rule_families: {0}".format(", ".join(leaf.rule_families)),
        "# bbox_dbu: ({0}, {1}, {2}, {3})".format(*leaf.bbox_dbu),
        "# block_bounds_dbu: ({0}, {1}, {2}, {3})".format(
            *leaf.block_bounds_dbu),
        "# manufacturing_grid_dbu: 1",
        "# Edits MUST keep all polygon vertices inside block_bounds_dbu;",
        "# the validator (check 2) rejects any op that moves a vertex outside.",
    ]
    out.extend(_violations_table_lines(leaf, ctx))
    return out


def _serialize_leaf_as_klayout(leaf, ctx):
    """Emit the crop section that goes into the prompt.

    The section is a heading, the metadata comments, and the crop body inside
    a fenced Python block.
    """
    header = _build_klayout_header_lines(leaf, ctx)
    body = _build_klayout_snippet_body(leaf, ctx)
    parts = ["## Crop (runnable KLayout snippet)", ""]
    parts.extend(header)
    parts.append("")
    parts.append("```python")
    parts.extend(body)
    parts.append("```")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Knowledge document handling
# ---------------------------------------------------------------------------

def _trim_skill_excerpt(text, hard_cap=4000):
    """Return the knowledge text unchanged; ``hard_cap`` is ignored.

    The knowledge document is no longer inlined into the prompt -- the prompt
    gives its path and the model reads it -- so there is nothing to truncate.
    """
    if not text:
        return ""
    return text


# ---------------------------------------------------------------------------
# Public entry: build the per-leaf prompt
# ---------------------------------------------------------------------------

def _output_section(leaf, patch_path, trace_path):
    """Build the closing ``## Output`` section of the prompt.

    This is the only place the prompt states what the model must produce: the
    two files to write, the JSON envelope for the patch, the empty-ops form
    when no safe fix exists, and what the reasoning trace must contain.

    ``patch_path`` and ``trace_path`` are the absolute paths generated for this
    leaf; neutral defaults keep the prompt well formed for callers that are not
    dispatching a real run. The section is built by concatenation rather than
    formatting so the literal JSON braces need no escaping, and because it
    embeds the leaf id it must stay at the end of the prompt, where a per-leaf
    value cannot break the shared cached prefix.
    """
    patch = patch_path if patch_path else "/out/patch.json"
    trace = trace_path if trace_path else "/out/trace.md"
    leaf_id = leaf.leaf_id
    s = (
        "## Output\n\n"
        "Write exactly these two output files using the Write tool, and do "
        "not modify any other file:\n"
        "  " + patch + "\n"
        "  " + trace + "\n\n"
        + patch + " must be pure JSON with NO markdown fences and exactly "
        "this envelope:\n"
        "{\n"
        "  \"leaf_id\": \"" + leaf_id + "\",\n"
        "  \"ops\": [\n"
        "    {\"op\": \"resize\", \"polygon_id\": \"pA\", \"axis\": \"x\", "
        "\"delta_dbu\": -96},\n"
        "    {\"op\": \"move_instance\", \"inst_id\": \"iA\", "
        "\"delta_dbu\": [18, 0]}\n"
        "  ],\n"
        "  \"explanation\": \"Short human-readable rationale in 1-2 "
        "sentences.\"\n"
        "}\n\n"
        "The two ops above are format examples with placeholder ids (pA / "
        "iA) -- always use the real ids from YOUR crop.\n\n"
        "If no safe fix exists, write this to " + patch + ":\n"
        "{\"leaf_id\": \"" + leaf_id + "\", \"ops\": [], "
        "\"explanation\": \"no safe fix\"}\n\n"
        + trace + " must contain the full reasoning trace: each violation, "
        "rule+threshold, candidates considered and why, op effect, "
        "self-critique, repair order followed, and whether/how the "
        "connectivity-, DRC-, and connectivity-impact-preview tools were "
        "used.")
    if _exp3_prompt():
        # Also require any newly introduced violation to be declared.
        s = s.replace(
            "connectivity-impact-preview tools were used.",
            "connectivity-impact-preview tools were used, and, if your patch "
            "introduces any violation, a DECLARED-DEBT list (rule + bbox) for "
            "each.")
    return s


def _conn_preview_directive(conn_ctx_path):
    """Build the ``## Connectivity preview`` section of the prompt.

    Because it embeds the per-leaf context path it is a function rather than a
    constant, and it belongs after the shared cached prefix. A placeholder
    stands in when no path is supplied.
    """
    target = conn_ctx_path if conn_ctx_path else \
        "<the --context path supplied by the harness>"
    return (
        "## Connectivity preview (call BEFORE risky ops)\n\n"
        "Before you finalize any patch that contains delete_instance or "
        "move_instance\n"
        "(these most often break a net), CHECK it first:\n"
        "  1. Write your candidate ops JSON to a temp file (use the Write "
        "tool), e.g.\n"
        "     /workspace/temp/conn/candidate.json. The file needs ONLY "
        "{{\"ops\":[...]}};\n"
        "     you do NOT include a leaf_id -- the tool supplies it from "
        "context.\n"
        "  2. Run:\n"
        "     python3 -m agent.src.conn_preview --candidate "
        "<that_path> --context {0}\n"
        "  3. Read the one-line JSON verdict. If \"preserved\" is false, your "
        "ops break\n"
        "     block connectivity (see \"broken_seeds\"): drop or revise the "
        "offending op\n"
        "     and re-check. Only write your FINAL patch (per \"## Output\") "
        "once the\n"
        "     preview says \"preserved\": true (or you removed the risky "
        "op).\n"
        "You do NOT need to know the leaf id, case, layout path, or golden "
        "file -- the\n"
        "tool already has them. Pass ONLY --candidate (and the --context "
        "value above).".format(target))


def _drc_preview_directive(drc_ctx_path):
    """Build the ``## DRC preview`` section of the prompt.

    Because it embeds the per-leaf context path it is a function rather than a
    constant, and it belongs after the shared cached prefix. A placeholder
    stands in when no path is supplied.
    """
    target = drc_ctx_path if drc_ctx_path else \
        "<the --context path supplied by the harness>"
    s = (
        "## DRC preview (check candidate ops BEFORE writing your final patch)\n\n"
        "To verify a candidate patch actually clears your target violations "
        "without\n"
        "introducing new in-window ones, CHECK it first:\n"
        "  1. Write your candidate ops JSON to a temp file, e.g.\n"
        "     /workspace/temp/drc/candidate.json. The file needs ONLY "
        "{{\"ops\":[...]}};\n"
        "     you do NOT include a leaf_id -- the tool supplies it from "
        "context.\n"
        "  2. Run:\n"
        "     python3 -m agent.src.drc_preview --candidate "
        "<that_path> --context {0}\n"
        "  3. Read the one-line JSON verdict: \"cleared\" / \"remaining\" "
        "target violations\n"
        "     and \"new_in_window\" (NEW violations your ops introduced inside "
        "this crop).\n"
        "     Only write your FINAL patch (per \"## Output\") once "
        "\"remaining\" shrinks and\n"
        "     \"new_in_window\" is empty.\n"
        "You do NOT need the leaf id, case, layout path, or deck -- the tool "
        "has them.\n"
        "Pass ONLY --candidate (and the --context value above).".format(target))
    if _exp3_prompt():
        # Raise the bar for a final patch: net violation reduction rather
        # than merely no new violations in the window.
        s = s.replace(
            "     Only write your FINAL patch (per \"## Output\") once "
            "\"remaining\" shrinks and\n"
            "     \"new_in_window\" is empty.\n",
            "     Only write your FINAL patch once ALL of:\n"
            "       - \"remaining\" shrinks;\n"
            "       - connectivity preserved;\n"
            "       - \"new_in_window\" strictly SMALLER than the set you "
            "cleared (net\n"
            "         reduction; prefer empty when achievable).\n"
            "     Every entry left in \"new_in_window\" MUST be declared in "
            "your trace\n"
            "     with rule + bbox.\n")
    return s


def _conn_impact_directive(ci_ctx_path):
    """Build the ``## Connectivity-impact preview`` section of the prompt.

    Because it embeds the per-leaf context path it is a function rather than a
    constant, and it belongs after the shared cached prefix. A placeholder
    stands in when no path is supplied.
    """
    target = ci_ctx_path if ci_ctx_path else \
        "<the --context path supplied by the harness>"
    s = (
        "## Connectivity-impact preview (which objects you are electrically "
        "touching)\n\n"
        "Before you move/delete a via, resize/move a via land/cut, or resize a "
        "metal, see\nEVERY other object that is CONNECTIVITY-OVERLAPPING it "
        "(same layer, real polygons "
        "overlap with positive\narea; a via participates through its per-layer "
        "lands). This is LIST-ONLY -- it\ngrants no permissions; it shows what "
        "you may break.\n"
        "  Run:\n"
        "     python3 -m agent.src.conn_impact_preview --object <id> "
        "--context {0}\n"
        "  <id> is ONE object id: a top-level polygon id (pNNN) OR a via "
        "instance id (iNNNN).\n"
        "  Read the one-line JSON {{\"object\":<id>,\"overlapping\":[{{id,kind,"
        "layer,editability}}...]}}:\n"
        "  each listed object shares a layer and physically overlaps yours. An "
        "[editability]\n"
        "  of [D editable]/[C partial-editable] = you may edit it; [movable, "
        "owned] = you may\n  move/delete that via OR resize/move its lands/cut "
        "(resize_via_shape/move_via_shape);\n  anything else is frozen. Use this "
        "to keep every land covered when you move or\n  resize a via, and to "
        "spot a metal you would short.\n"
        "You do NOT need the leaf id, case, or layout path -- the tool has the "
        "geometry.\n"
        "Pass ONLY --object (and the --context value above).".format(target))
    # With via-structure editing off, drop the wording about editing via
    # lands and cuts; whole-instance moves and metal resizes still apply.
    if not _via_edit_enabled():
        s = s.replace(
            "move/delete a via, resize/move a via land/cut, or resize a metal",
            "move/delete a via or resize a metal")
        s = s.replace(
            "move/delete that via OR resize/move its lands/cut "
            "(resize_via_shape/move_via_shape);",
            "move/delete that via;")
    if _exp3_prompt():
        # Reformat the same guidance as bullet lists. The text being matched
        # is the via-editing wording, so with that feature off these
        # replacements find nothing and the variant above is kept.
        s = s.replace(
            "Before you move/delete a via, resize/move a via land/cut, or "
            "resize a metal, see\nEVERY other object that is "
            "CONNECTIVITY-OVERLAPPING it (same layer, real polygons "
            "overlap with positive\narea; a via participates through its "
            "per-layer lands). This is LIST-ONLY -- it\ngrants no "
            "permissions; it shows what you may break.\n",
            "Before you move/delete a via, resize/move a via land/cut, or "
            "resize a metal:\n"
            "  - See EVERY other object that is CONNECTIVITY-OVERLAPPING "
            "it (same layer,\n"
            "    real polygons overlap with positive area; a via "
            "participates through its\n"
            "    per-layer lands).\n"
            "  - LIST-ONLY: grants no permissions; shows what you may "
            "break.\n")
        s = s.replace(
            "  each listed object shares a layer and physically overlaps "
            "yours. An [editability]\n"
            "  of [D editable]/[C partial-editable] = you may edit it; "
            "[movable, owned] = you may\n"
            "  move/delete that via OR resize/move its lands/cut "
            "(resize_via_shape/move_via_shape);\n"
            "  anything else is frozen. Use this to keep every land "
            "covered when you move or\n"
            "  resize a via, and to spot a metal you would short.",
            "  (each listed object shares a layer and physically overlaps "
            "yours):\n"
            "    - [D editable] / [C partial-editable] = you may edit "
            "it;\n"
            "    - [movable, owned] = you may move/delete that via OR "
            "resize/move its\n"
            "      lands/cut (resize_via_shape/move_via_shape);\n"
            "    - anything else = FROZEN.\n"
            "  Use it to keep every land covered when you move/resize a "
            "via, and to spot\n"
            "  a metal you would short.")
    return s


def build_leaf_prompt(leaf, ctx, patch_path=None, conn_ctx_path=None,
                      drc_ctx_path=None, repair_order=False, ci_ctx_path=None,
                      trace_path=None, shared_ctx=None, whole_data=None):
    """Assemble the prompt for one leaf and return it as a string.

    Two layouts are produced. The flat layout, used by default, runs preamble,
    input resources, procedure, patch grammar, subcell protection and
    self-critique, then the crop with its violation table, the rule cards, the
    preview-tool directives, and finally the output section. The model gets the
    data it needs first, with the rules and the write target repeated
    immediately before it has to commit to an answer.

    The sectioned layout, selected by EXP3_PROMPT, renders sections S4 to S7 --
    verification standards and tools, edit rules, data, and output -- while the
    caller supplies sections S1 to S3 ahead of them.

    ``patch_path`` and ``trace_path`` are the absolute paths the model must
    write its patch JSON and its reasoning trace to. ``conn_ctx_path``,
    ``drc_ctx_path`` and ``ci_ctx_path`` are per-leaf context paths for the
    three preview tools; each directive is only emitted if its path is given.
    All of them default to None so callers that are not dispatching a real run
    still get a well-formed prompt.

    ``shared_ctx`` is pre-rendered shared-target context. It is placed at the
    head of the data section in the sectioned layout and ignored in the flat
    one, where the caller positions it itself.

    ``whole_data`` is a pre-rendered compact data section for whole-design
    mode. When given, it replaces the inline crop and the per-violation
    highlight, and the repair-order table is rendered with row caps.
    """
    # Everything that is identical across the leaves of one case goes first, so
    # the model provider can cache that prefix; anything derived from this leaf
    # goes last. Moving a constant earlier only lengthens the shared prefix.
    _via_on = _via_edit_enabled()
    _exp3 = _exp3_prompt()
    _sc = _SELF_CRITIQUE_CHECKLIST if _via_on else _SELF_CRITIQUE_CHECKLIST_NOVIA
    if _exp3:
        # Rewrite item 6 against whichever base string was chosen, rather than
        # keeping four near-identical constants. The standard it refers to is
        # stated once, in the verification standards above.
        _sc = _sc.replace(
            "6. If EVERY candidate op risks a new violation, write an empty "
            "ops list. A\n   skipped leaf (0 new violations) is strictly "
            "better than a regression.\n",
            "6. If every candidate previews net-negative or breaks "
            "connectivity, write\n   an empty ops list. Otherwise submit the "
            "best NET-REDUCING patch per\n   the NET-reduction standard "
            "above (declared debt in your trace).\n")
    _pg = _PATCH_GRAMMAR_REFERENCE if _via_on else _PATCH_GRAMMAR_REFERENCE_NOVIA
    if _exp3:
        # Mention the atomic-group key in the grammar itself so it is
        # discoverable there. The mechanism is described in full in the
        # verification standards; ops sharing a group name are pooled into a
        # single candidate and measured together.
        _pg = _pg.replace(
            "All delta_dbu values must be integers "
            "(MANUFACTURING_GRID_DBU = 1).\n",
            "All delta_dbu values must be integers "
            "(MANUFACTURING_GRID_DBU = 1).\n\n"
            "Optional key on ANY op: \"group\": \"<name>\" -- ops sharing a "
            "group name are\npooled by the harness and measured/applied as "
            "ONE atomic candidate (used\nfor coupled multi-def or def+polygon "
            "repairs; see the atomic-group\nspec in S4).\n")
    if _via_add_enabled():
        # Splice the add_via fragment into the "Instance ops" block of
        # whichever grammar variant is in use. This flag is independent of
        # both the via-structure flag and the layout choice.
        _pg = _pg.replace(_DELETE_INSTANCE_LINE,
                          _DELETE_INSTANCE_LINE + _ADD_VIA_GRAMMAR)
    _sp = _SUBCELL_PROTECTION_CLAUSE if _via_on else _SUBCELL_PROTECTION_CLAUSE_NOVIA
    if _exp3:
        # The consequences of editing a shared cell definition are explained
        # once, in the shared-target context section, so this passage points
        # there instead. The variant without via editing has no such passage
        # and is left untouched.
        _sp = _sp.replace(
            "changes together -- weigh that same-type\n"
            "         impact; the whole-block DRC + connectivity gate is the "
            "backstop.",
            "changes together -- admissibility and\n"
            "         block-wide measurement per '## Shared-target context'.")
    if _exp3:
        # Sections S4 to S7: verification standards and preview tools, then
        # edit rules, then the data for this leaf, then the output contract.
        # The caller has already emitted S1 to S3, which is where the input
        # resources, the procedure and every file path are stated.
        parts = [
            EXP3_SECTION_BANNERS[3],                  # === S4 ===
            _S4_STANDARDS,
            _conn_preview_directive(conn_ctx_path),
            _drc_preview_directive(drc_ctx_path),
        ]
        if ci_ctx_path is not None:                   # optional section
            parts.append(_conn_impact_directive(ci_ctx_path))
        parts.extend([
            _sc,
            EXP3_SECTION_BANNERS[4],                  # === S5 ===
            _pg,
            _sp,
            EXP3_SECTION_BANNERS[5],                  # === S6 ===
        ])
        if shared_ctx:
            parts.append(shared_ctx.rstrip("\n"))
        if whole_data is not None:
            # Whole-design mode: the data is referenced by path instead of
            # inlined, so the compact section replaces the crop and the
            # highlight, and the repair-order table is capped.
            parts.append(whole_data.rstrip("\n"))
            if repair_order:                          # optional section
                _ro = crop_body.build_repair_order_section(
                    leaf, ctx, max_rows=60, max_touch_ids=6)
                if _ro:
                    parts.append(_ro)
        else:
            parts.append(_serialize_leaf_as_klayout(leaf, ctx))
            _hl = crop_body.build_highlight_section(leaf, ctx)
            if _hl:
                parts.append(_hl)
            if repair_order:                          # optional section
                _ro = crop_body.build_repair_order_section(leaf, ctx)
                if _ro:
                    parts.append(_ro)
        parts.extend([
            _rule_cards_for_leaf(leaf, ctx),
            EXP3_SECTION_BANNERS[6],                  # === S7 ===
            _output_section(leaf, patch_path, trace_path),
        ])
        return "\n\n".join(parts)
    # ---- Flat assembly (the default layout) --------------------------------
    prefix = [
        _SYSTEM_PREAMBLE,
        _INPUT_RESOURCES,
        _PROCEDURE,
        _pg,
        _sp,
        _sc,
    ]
    # The accumulated repair knowledge is referenced by path and read by the
    # model itself, so the prompt carries just the path, at constant size, and
    # the model sees the whole file. The section is emitted whenever a path
    # exists, even if the file is still empty on the first iteration.
    _kpath = getattr(getattr(ctx, "case_info", None), "skill_path", "") or ""
    if _kpath:
        prefix.append(
            "## Accumulated repair knowledge (READ THIS FILE YOURSELF)\n\n"
            "Read `%s` with the Read tool for cross-iteration, generalizable "
            "DRC-repair heuristics distilled from prior iterations (negative "
            "lessons included). It may be empty on iteration 1. Use it; do not "
            "guess thresholds or rule semantics." % _kpath)
    suffix = [
        _serialize_leaf_as_klayout(leaf, ctx),
    ]
    _hl = crop_body.build_highlight_section(leaf, ctx)
    if _hl:
        suffix.append(_hl)
    if repair_order:                                  # optional section
        _ro = crop_body.build_repair_order_section(leaf, ctx)
        if _ro:
            suffix.append(_ro)
    # The output envelope lives only in the closing section below, so the
    # write requirements are stated once, right before the model answers.
    suffix.extend([
        _rule_cards_for_leaf(leaf, ctx),
        _conn_preview_directive(conn_ctx_path),
        _drc_preview_directive(drc_ctx_path),
    ])
    if ci_ctx_path is not None:                       # optional section
        suffix.append(_conn_impact_directive(ci_ctx_path))
    suffix.append(_output_section(leaf, patch_path, trace_path))
    return "\n\n".join(prefix + suffix)
