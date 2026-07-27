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

"""Shared data shapes that every pipeline stage passes around.

The pipeline reads a layout and a DRC report, breaks the violations into small
regions that can be repaired independently, sends each region to a model, and
mounts the accepted edits back into the layout. The classes here describe that
data at each step: geometry primitives, the per-block statistics that bound a
region, the clips and leaves produced by decomposition, and the case-wide
context object that accumulates all of it.
"""


from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# --- Layer enumeration ---
# Maps ASAP7 layer names to the integer index used by the spatial-extent check.
# Metal and via layers interleave, so a difference of indices measures how far
# a shape group spans up the stack. Layers below M1 live inside subcells and
# are never edited, so the map starts at M1.
LAYER_INDEX_MAP: Dict[str, int] = {
    "M1": 0, "V1": 1, "M2": 2, "V2": 3, "M3": 4, "V3": 5,
    "M4": 6, "V4": 7, "M5": 8, "V5": 9, "M6": 10, "V6": 11, "M7": 12,
}

# Inverse lookup, used to name a layer index in log output.
LAYER_NAME_BY_INDEX: Dict[int, str] = {v: k for k, v in LAYER_INDEX_MAP.items()}

# GDS layer number (the first LayerInfo argument) to the metal or via name it
# denotes in the ASAP7 stack.
LAYER_NUM_TO_NAME: Dict[int, str] = {
    19: "M1", 21: "V1", 20: "M2", 25: "V2", 30: "M3", 35: "V3",
    40: "M4", 45: "V4", 50: "M5", 55: "V5", 60: "M6", 65: "V6",
    70: "M7", 75: "V7", 80: "M8", 85: "V8", 90: "M9", 95: "V9",
    96: "M9",
}


# --- Geometry primitives ---------------------------------------------------

@dataclass
class Polygon:
    """One physical polygon on the layout.

    Deliberately mutable: validation applies a patch to a deep copy of the
    model and updates the copied polygons in place.
    """
    polygon_id: str                       # "p<NNNN>", assigned when the model is built
    layer_name: str                       # "M1", "V2", etc.
    layer_index: int                      # LAYER_INDEX_MAP[layer_name]
    bbox_dbu: Tuple[int, int, int, int]   # (x_min, y_min, x_max, y_max)
    points_dbu: Tuple[Tuple[int, int], ...]  # outline; first==last not required
    net_id: Optional[str] = None          # from connectivity.json; None if not on any net
    owner_kind: str = "editable"          # "editable" | "bridge" | "subcell_via" | "subcell_stdcell"
    bridge_owner_leaf_id: Optional[str] = None  # set when bridge ownership is assigned


@dataclass
class SubcellInstance:
    """One CellInstArray reference inside the top cell."""
    instance_id: str                      # "i<NNNN>"
    cell_name: str                        # "VIA_VIA12", "INVx1_ASAP7_75t_R", ...
    kind: str                             # "via" | "stdcell"
    allowed_ops: Tuple[str, ...]          # () for stdcell; ("move_instance","delete_instance") for via
    origin_dbu: Tuple[int, int]           # (x, y)
    rot_code: int = 0                     # KLayout transform rotation code: 0/2/4/6
    mirror: bool = False                  # KLayout transform mirror flag


@dataclass
class CellDef:
    """Internal geometry of one cell type, in cell-local coordinates.

    A definition carries no instance transform, so its shapes are shared by
    every instance of that type. Crops use this to render a subcell's internal
    structure once per cell type rather than once per instance.
    """
    cell_name: str
    kind: str                             # "via" | "stdcell"
    # each shape: (gds_layer_num, local_points, is_via_cut)
    shapes: List[Tuple[int, Tuple[Tuple[int, int], ...], bool]] = field(
        default_factory=list)
    is_strap: bool = False                # via-cut count >= 4 (VIA cells only)
    via_cut_count: int = 0
    extent_dbu: Tuple[int, int] = (0, 0)  # (width, height) of the local bbox


@dataclass
class Violation:
    """One DRC violation row from drc.json."""
    violation_id: str                     # "v<NNNN>"
    rule_id: str                          # e.g., "M1.S.2"
    rule_family: str                      # e.g., "M_SPACING"
    bbox_dbu: Tuple[int, int, int, int]
    involves: Tuple[str, ...]             # polygon_id refs (drc.json "involves" field)
    description: str = ""                 # rule text carried over from the DRC report


# --- Block-level state -----------------------------------------------------

@dataclass
class GeometryModel:
    polygons: Dict[str, Polygon]          # by polygon_id
    instances: Dict[str, SubcellInstance]
    block_bounds_dbu: Tuple[int, int, int, int]  # x_min, y_min, x_max, y_max
    cell_defs: Dict[str, "CellDef"] = field(default_factory=dict)  # by cell_name


@dataclass
class BlockStats:
    """Size bounds calibrated at runtime from the block's own violations."""
    safety_bound_p90: int                 # p90 of max(dx, dy, dz_layer_index)
    geom_degree_p95: int                  # p95 of polygon's adjacency count in violation graph
    cell_poly_p95: int                    # p95 of polygons-per-violation-cluster


# --- Decomposition products ------------------------------------------------

@dataclass
class Clip:
    clip_id: str
    violation_ids: Tuple[str, ...]
    polygon_ids: Tuple[str, ...]
    depth: int = 0                        # recursion depth; 0 for an initial clip
    # Subcell instances whose world bounding box touches this clip's violation
    # bbox. Clips that share an instance are merged, so this acts as the merge
    # key; sub-clips produced later during recursion leave it empty because
    # merging has already happened by then.
    instance_ids: Tuple[str, ...] = ()


@dataclass
class Leaf:
    leaf_id: str                          # "leaf_<NNNN>"
    editable_polygons: List[str]          # polygon_ids inside the leaf, mutable
    bridge_polygons: List[str]            # polygon_ids on leaf boundary, owned but read-mostly
    subcell_instances: List[str]          # instance_ids referenced
    violations: List[str]                 # violation_ids assigned to this leaf
    net_to_polygons: Dict[str, List[str]] = field(default_factory=dict)
    block_bounds_dbu: Tuple[int, int, int, int] = (0, 0, 0, 0)
    bbox_dbu: Tuple[int, int, int, int] = (0, 0, 0, 0)
    strap_class: Optional[str] = None     # filled in by strap classification (S7)
    depth: int = 0
    rule_families: Tuple[str, ...] = ()
    context_readonly: List[str] = field(default_factory=list)
    warn_depth_exceeded: bool = False
    # Neighbouring top-level polygons shown to the model as `# ro` comment
    # lines only. They are never editable and never form a conflict edge, so
    # the scheduler and validator visibility sets leave them out.
    ro_neighbor_ids: List[str] = field(default_factory=list)
    # Instances pulled in because their world bbox intersects a violation
    # bbox; these are exempt from the crop's instance count cap.
    seed_instance_ids: List[str] = field(default_factory=list)
    # Layer band for this leaf: the layer names it may edit and the ones it
    # only sees. band_background holds top-level polygons demoted out of the
    # editable lists, rendered as `# band-bg` comment lines.
    editable_layers: Tuple[str, ...] = ()
    background_layers: Tuple[str, ...] = ()
    band_background: List[str] = field(default_factory=list)
    # Frozen standard-cell pin shapes in top-level coordinates, rendered as
    # `# stdpin` comment lines. Each entry is (cell_name, gds_layer_num,
    # world_points).
    stdcell_pin_polys: List[Tuple[str, int, Tuple[Tuple[int, int], ...]]] = field(
        default_factory=list)
    # One-hop geometric neighbours rendered as `# bg-via` / `# bg` comment
    # lines; holds a mix of instance ids and polygon ids.
    frozen_context: List[str] = field(default_factory=list)
    # For long stripes, which ends run off the edge of the crop:
    #   polygon_id -> {"axis": "x"|"y", "open_low": bool, "open_high": bool}.
    long_open_ends: Dict[str, Dict[str, object]] = field(default_factory=dict)
    # Instances this leaf may move or delete. When leaves run in parallel this
    # is the subset owned by exactly one leaf; run sequentially it is every
    # movable instance.
    owned_instances: Tuple[str, ...] = ()
    # Union of the band layer names across the whole case, recorded so a
    # trimmed rule deck can be traced back to the layers it was trimmed for.
    case_deck_layers: Tuple[str, ...] = ()
    # None means the leaf is dispatchable; "skipped_empty_crop" marks a leaf
    # whose crop came out empty, which is dropped before scheduling.
    skip_status: Optional[str] = None
    # True for a power-distribution-network crop, where editable_polygons is
    # exactly one power net's traced top-level shapes and everything else in
    # the bbox is view-only background. Crop rendering and the connectivity
    # gate use this to tell editable PDN geometry from background.
    is_pdn: bool = False
    # Rail label for the two power-net crops, "VDD" or "VSS", empty on every
    # other leaf. Net names are not available at this point, so which crop is
    # which follows a deterministic geometric tie-break rather than any
    # electrical information.
    pdn_rail: str = ""
    # True when this leaf covers the whole design instead of a decomposed
    # region. Prompt and preview code reads it through getattr, so leaves
    # built without the flag still work.
    whole_design: bool = False


@dataclass
class Patch:
    leaf_id: str
    ops: List[Dict[str, object]]          # one entry per edit operation
    explanation: str = ""


@dataclass
class Verdict:
    ok: bool
    check_name: str = ""
    reason: str = ""


@dataclass
class LeafResult:
    leaf_id: str
    status: str                           # "mounted" | "skipped_invalid_patch" | "dispatch_fail" | "patch_parse_fail" | "skipped_empty_crop"; mounting may replace it with a "mount_*" value
    patch: Optional[Patch] = None
    verdict: Optional[Verdict] = None
    call_id: Optional[str] = None
    failed_check: Optional[str] = None
    error: Optional[str] = None


# --- Case-level state ------------------------------------------------------

@dataclass
class CaseInfo:
    """Case metadata read out of the case-info block of the prompt."""
    case_name: str = ""
    design_type: str = "block"
    task_type: str = "repair"
    layout_path: str = ""
    drc_path: str = ""
    connectivity_path: str = ""
    rule_path: str = ""
    skill_path: str = ""
    output_path: str = ""
    model_name: str = "claude-opus-4-7"


@dataclass
class CaseContext:
    prompt_path: str                      # positional arg from agent.py
    output_path: str                      # positional arg from agent.py
    temp_dir: str                         # --temp_dir
    workspace: str                        # --workspace
    case_info: CaseInfo = field(default_factory=CaseInfo)
    skill_excerpt: str = ""               # full knowledge document; the prompt points at its path rather than inlining it
    geometry_model: Optional[GeometryModel] = None  # S2
    violations: List[Violation] = field(default_factory=list)  # S2
    block_stats: Optional[BlockStats] = None        # S3
    clips: List[Clip] = field(default_factory=list)             # S4
    merged_clips: List[Clip] = field(default_factory=list)      # S5
    leaves: Dict[str, Leaf] = field(default_factory=dict)       # S6, keyed by leaf_id
    waves: List[List[str]] = field(default_factory=list)        # S8, each wave is a list of leaf_ids
    leaf_results: Dict[str, LeafResult] = field(default_factory=dict)  # S9
    patched_layout_text: Optional[str] = None       # S10
    mount_rejected_reason: Optional[str] = None     # S10
    rule_db: Optional[object] = None                # rule family lookup, set by S2/S3
    # Rule deck text trimmed to the layers this case touches, computed once.
    trimmed_deck_text: Optional[str] = None
    # Per-leaf wave index and conflict degree recorded by the scheduler and
    # reused to order mounting. Left empty, mounting falls back to leaf order.
    leaf_wave: Dict[str, int] = field(default_factory=dict)
    leaf_conflict_degree: Dict[str, int] = field(default_factory=dict)
    # Optional feature dials, read from the environment and clamped once when
    # the context is built. 0 turns the feature off, which is the default.
    drc_gate: int = 0
    via_metal_coupling: int = 0
    # --- Power-distribution-network pre-pass state ---
    # pdn_done: set once the pre-pass has run; a second call returns at once.
    # pdn_global_polys: the polygon set frozen before power nets are carved
    #   out, so later merging sees the same picture it did before the carve.
    # pdn_leaves: the per-net power crops, spliced into the leaf list just
    #   before leaves are renumbered.
    # pdn_editable_pids: every polygon promoted into a power crop; these are
    #   removed from the editable set of all other leaves.
    # pdn_net_pids / pdn_net_violations: traced polygons and carved violation
    #   ids, per net.
    # pdn_net_vias: net key -> the via instances attached to that net.
    # pdn_owned_via_iids: union of the above. Each via belongs to a single
    #   net, which keeps leaves running in parallel off the same instance.
    # pdn_detect_report: per-net detection lines kept for reporting.
    pdn_done: bool = False
    pdn_global_polys: Optional[set] = None
    pdn_leaves: List["Leaf"] = field(default_factory=list)
    pdn_editable_pids: set = field(default_factory=set)
    pdn_net_pids: Dict[object, List[str]] = field(default_factory=dict)
    pdn_net_violations: Dict[object, List[str]] = field(default_factory=dict)
    pdn_net_vias: Dict[object, List[str]] = field(default_factory=dict)
    pdn_owned_via_iids: set = field(default_factory=set)
    pdn_detect_report: List[str] = field(default_factory=list)


class RuleDB:
    """Maps a DRC rule id to a coarse rule family.

    ``family_of("M1.S.4")`` returns "spacing". The leaf predicates use the
    family label to decide whether a group of violations is homogeneous enough
    to repair together.
    """

    _FAMILY_TOKENS = {
        "S": "spacing", "SPACE": "spacing", "SPACING": "spacing",
        "W": "width", "WIDTH": "width",
        "EN": "enclosure", "ENC": "enclosure", "ENCLOSURE": "enclosure",
        "A": "area", "AREA": "area",
        "EOL": "eol", "MIN": "min_size", "SIZE": "min_size",
    }

    def family_of(self, rule_id: str) -> str:
        if not rule_id:
            return "unknown"
        for part in str(rule_id).split("."):
            f = self._FAMILY_TOKENS.get(part.upper())
            if f is not None:
                return f
        return "other"
