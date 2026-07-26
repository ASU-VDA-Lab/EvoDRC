## M5 Repair Patterns (Iteration 1)

### Via-Cell Y-Axis Shrink Reduces Violations

Shrinking the M5 shape along the y-axis inside a VIA_VIA45 cell is an effective repair operation that reduces DRC violations while preserving connectivity. A single `resize_via_shape` on axis `y` with delta_dbu `-88` inside cell `VIA_VIA45_1_2_58_58` reduced the total violation count by 52 (−26 per affected window) with `conn_preserved: true` (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

### Repair Scope and Symmetry

The −52 reduction was split evenly across two distinct design windows (`unit:leaf_0034` and `unit:leaf_0035`, each −26), indicating that the oversized M5 shape in the shared via cell contributed violations symmetrically to both contexts. When a single cell edit resolves violations in multiple windows simultaneously, prefer editing that cell rather than per-instance geometry, as seen in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01.

### Y-Direction Sizing Rules to Target

The following M5 rules govern vertical (y-axis) geometry and are the primary candidates implicated by a y-shrink repair:

- **M5.W.5** requires minimum vertical width ≥ 44 nm. A shrink of 88 dbu removes excess vertical extent without approaching this floor, provided the post-repair height remains ≥ 44 nm.
- **M5.S.2** requires minimum vertical spacing ≥ 40 nm between M5 edges. An oversized M5 in a via cell can encroach on neighboring M5 polygons vertically; shrinking by 88 dbu is consistent with opening spacing headroom (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).
- **M5.S.3** and **M5.S.4** govern tip-to-tip spacing (≥ 40 nm) on adjacent tracks; excess y-extent generates short tip-to-tip distances that a y-shrink directly resolves.

### Via Enclosure Constraints Are the Primary Sizing Bound

Rules **V4.M5.EN.2** and **V4.M5.AUX.2** constrain how tightly M5 may be shrunk around V4:

- V4.M5.EN.2 requires M5 to enclose V4 by ≥ 11 nm on two opposite sides (both x and y). Any y-axis shrink of M5 in a via cell must leave ≥ 11 nm of M5 overhanging the V4 extent on both the top and bottom edges.
- V4.M5.AUX.2 requires V4 to match M5 width exactly in the direction perpendicular to M5 length. For a horizontal M5 wire, V4 width in x must equal M5 width in x; a y-axis shrink does not affect this constraint but a mistaken x-axis shrink would violate it.

The successful −88 dbu y-shrink in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 confirms that these enclosure bounds were not violated at this delta, meaning the pre-repair M5 y-extent in `VIA_VIA45_1_2_58_58` exceeded the via plus 11 nm enclosure by at least 88 nm on one side (or split across both sides).

### Grid and Routing Track Alignment Must Be Maintained

- **M5.AUX.1** requires all M5 vertical edges to lie on a 24 nm grid. Any resize delta must be a multiple of 24 nm to preserve grid compliance. Note that 88 dbu is not a multiple of 24 (88 = 3×24 + 16), so the post-repair shape must have been grid-aligned through the original placement, not through the delta alone. Verify grid compliance after any y-axis resize that uses a non-multiple-of-24 delta (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 was accepted, confirming the net result was grid-legal).
- **M5.AUX.2** requires minimum-width M5 tracks to lie on x-routing tracks spaced at 192 dbu pitch with 48 dbu offset (base 96 dbu). This is an x-centerline rule and is not directly affected by y-axis resize operations.
- **M5.AUX.3** prohibits M5 bends (no corners with angles 0–90°). Via cell edits must not introduce non-rectilinear outlines. The shape_index=0 resize in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 operated on a rectangle and did not violate this rule.
- **M5.AUX.4** prohibits wide M5 polygon outer y-edges from touching routing track edges. Y-shrinks of wide M5 shapes must not land the resulting edge exactly on a track boundary.

### Width Rules Constrain Horizontal Dimension Only

Rules M5.W.1 through M5.W.4 govern horizontal (x-axis) width exclusively:

- M5.W.1: minimum horizontal width ≥ 24 nm.
- M5.W.2: maximum horizontal width ≤ 480 nm.
- M5.W.3: horizontal width must not be an even integer multiple of 24 nm (i.e., not 48, 96, 144, … 480 nm).
- M5.W.4: horizontal widths of 72, 168, 264, 360, or 456 nm are prohibited.

These rules are unaffected by a pure y-axis resize. The single measured trial (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) involved only a y-axis op, so no x-width constraint interaction has been measured yet.

### M5.S.1 Is Orthogonal to Y-Shrink

**M5.S.1** (minimum horizontal spacing ≥ 24 nm) is governed by x-axis separation between parallel M5 wires. A y-axis shrink does not directly affect horizontal spacing between adjacent tracks, though it can alter which portions of M5 edges are co-planar and thus subject to parallel-run-length checks (M5.S.5 requires parallel run length ≥ 44 nm where two M5 edges on adjacent tracks are within 24 nm of each other).

### Operation Classification

The sole measured operation type is `resize_via_shape` applied to layer M5 within a via cell definition (`def:VIA_VIA45_1_2_58_58`). This op class edits the cell master, propagating the fix to all instances. The `cu_pool` channel was used (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). No instance-level ops, no x-axis ops, and no non-via-cell M5 ops have been measured in iteration 1.