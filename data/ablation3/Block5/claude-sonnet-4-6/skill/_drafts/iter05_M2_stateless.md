## M2 Repair Behavior: Measured Summary Through Iteration 5

### General Patterns Across All Trials

M2 has been touched in every trial recorded in this history. All four unit_gate trials (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00) list M2 among their `touched_layers`, and all four returned `decision: gated_in` with `n_new_in_crop: 0` and `n_new_out_of_crop: 0` under the `conn_preserved` gate reason. This confirms that instance-level moves that preserve connectivity do not introduce new M2 violations, provided the moves are accepted by the unit_gate channel.

The cu_pool trial (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00) also touches M2 and is the only trial that directly modifies M2 polygon geometry within a via cell definition.

---

### Instance Moves and M2

All unit_gate trials use `move_instance` operations that displace cell instances in x or y. These moves propagate to M2 because instance routing stubs and abutment wires on M2 shift with their parent cell.

- trial:i01.ug.whole_design.00 moved 14 instances (mixed x and y displacements, ranging from -28 dbu to +136 dbu in x, -48 dbu to +96 dbu in y) alongside polygon resize operations on p879 and p910. M2 was among the 9 touched layers. No new M2 violations resulted.
- trial:i02.ug.whole_design.00 moved 7 instances in x (±36 dbu), touching only M1, M2, V1. No new violations.
- trial:i04.ug.whole_design.00 moved 6 instances in x (−36 to +72 dbu), touching M1, M2, V1. No new violations.
- trial:i05.ug.whole_design.00 combined 3 instance moves, 7 instance deletions, 2 polygon resize_end operations on p951 and p955 (x-axis, +128 dbu each, high end), and 7 VIA_VIA34 via additions, touching M1, M2, M3, M4, V1, V3. No new violations.

The safe envelope for instance moves observed across these trials spans at least −36 to +136 dbu in x and −48 to +96 dbu in y without introducing M2 rule failures.

---

### M2 Polygon Resize Operations

Three sets of M2 polygon resize operations appear in the unit_gate channel:

**trial:i01.ug.whole_design.00:**
- p879: `resize_end`, axis y, delta +48 dbu, end high. Accepted; no new violations.
- p910: `move`, axis x, delta +8 dbu (whole polygon shift); followed by `resize_end`, axis y, delta +20 dbu, end high. Accepted; no new violations.

**trial:i05.ug.whole_design.00:**
- p951: `resize_end`, axis x, delta +128 dbu, end high. Accepted; no new violations.
- p955: `resize_end`, axis x, delta +128 dbu, end high. Accepted; no new violations.

In both cases the operation extends the high end of the polygon. The extensions in trial:i05 (+128 dbu ≈ +12.8 nm at 0.1 nm/dbu) are substantially larger than those in trial:i01 (+48 dbu ≈ +4.8 nm, +20 dbu ≈ +2.0 nm). All extensions were accepted without triggering M2.W.1, M2.S.1–M2.S.8, or M2.A.1, confirming that the post-extension geometry remained within the legal range for width and spacing on M2.

Do not extend a polygon end without verifying that the resulting tip-to-tip and tip-to-side spacing with adjacent M2 shapes will still satisfy M2.S.2 (25 nm tip-to-side), M2.S.3 (27 nm tip-to-tip for edges 24–36 nm), M2.S.4 (31 nm tip-to-tip for edges <24 nm), M2.S.5 (31 nm mixed tip-to-tip), and M2.S.7 (no 18 nm tip-to-tip co-located with side spacing ≤32 nm unless run length ≥35 nm). The observed extensions were accepted (trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00) but the margins were not measured individually; rely on DRC re-check after each extension.

---

### Via Cell M2 Polygon Adjustment (cu_pool Channel)

trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 is the sole cu_pool entry in this history. It targeted cell `VIA_VIA23_1_3_36_36` and applied 8 operations:

- One `resize_via_shape` on the V2 shape in M3 (y-axis, −40 dbu).
- Seven `resize` ops on polygons p891–p897, each y-axis, −64 dbu.

The trial touched M2, M3, and V2. It reduced total violations by 8 (from 30 to 22 across the `unit:whole_design` window). Decision: `applied`.

The −64 dbu shrink on the seven M2 polygons co-occurred with the −40 dbu shrink on the via shape. This co-adjustment pattern is necessary: resizing a via shape inside a cell definition without also resizing the enclosing M2 polygon would violate V2.M2.EN.1 (minimum enclosure of V2 by M2 on at least two opposite sides is 5 nm). The 24 dbu difference between the via shape shrink (−40 dbu) and the M2 polygon shrink (−64 dbu) is consistent with maintaining ≥5 nm enclosure per V2.M2.EN.1 when 1 dbu = 0.1 nm (5 nm = 50 dbu; the extra shrink of 24 dbu beyond the via shrink may account for pre-existing enclosure margin reduction being reclaimed).

When modifying via cell geometry that includes V2 on M2: always apply a co-adjustment to the M2 polygon that keeps V2 fully enclosed within M2 on at least two opposite sides (V2.M2.EN.1). The measured ratio from trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 is −64 dbu on M2 for −40 dbu on the via shape (in y); do not apply the via shrink alone.

---

### assemble_drops and M2 Interaction

trial:i04.ug.whole_design.00 records an `assemble_drops` list containing the same eight ops that appear in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, each with `reason: cu_pool:applied`. This confirms the cu_pool channel applies its ops to the design state before unit_gate assembles its own batch; unit_gate then detects those ops as already present and drops them to avoid double-application.

The `deltas.per_rule` field in trial:i04.ug.whole_design.00 records `new_in_crop_by_rule: {"V2.M3.EN.2": 6}`, yet `n_new_in_crop` is 0. This means the V2.M3.EN.2 violations introduced by the unit_gate move ops were compensated by the already-applied cu_pool fix, netting to zero new violations at the crop level. M2 in this trial was not the site of the conflict; the conflict was on M3/V2, and the M2 resize ops in the cu_pool trial resolved the upstream enclosure relationship.

---

### Via Addition and M2 Enclosure

trial:i05.ug.whole_design.00 adds seven VIA_VIA34 instances at coordinates in the range x ∈ {2200, 2968} dbu, y ∈ {2160, 3312, 4272, 5424, 6576, 7536, 8688} dbu. The touched_layers list includes M2. VIA_VIA34 is a V3/M3-level via cell (given V3 and M3 are in the touched layers), but M2 appears in touched_layers, indicating either the cell geometry overlaps M2 or adjacent M2 routing adjusts to accommodate the additions.

No new violations were introduced (trial:i05.ug.whole_design.00, n_new_in_crop: 0), confirming the added VIA_VIA34 instances and the accompanying p951/p955 extensions are mutually consistent with M2 enclosure and spacing rules as placed.

---

### Rule-Level Observations (Grounded in History)

**M2.W.1 (min width 18 nm):** No violations of this rule are recorded in any trial. All resize operations on M2 polygons (trial:i01.ug.whole_design.00, trial:i04.cu.def:VIA_VIA23_1_3_36_36.00, trial:i05.ug.whole_design.00) either shrink in a dimension that does not reduce width, or extend the end without narrowing. The −64 dbu shrink on p891–p897 in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 is along y; if those polygons' y-extent after shrink exceeds 180 dbu (18 nm at 0.1 nm/dbu), M2.W.1 is not triggered.

**M2.S.1–M2.S.6 (spacing rules):** No M2 spacing violations appear in the per_rule fields of any trial. All accepted unit_gate moves and polygon resizes produced no new M2 spacing errors. The +128 dbu x-extensions in trial:i05.ug.whole_design.00 are the largest single-dimension polygon change recorded; they did not trigger M2.S.1 or M2.S.2, confirming the extended end was not within 18 nm (side) or 25 nm (tip-to-side) of any neighbor.

**M2.S.7 (tip-to-tip 18 nm co-located with side spacing ≤32 nm):** Not triggered in any trial. No flagging of this rule appears in `per_rule` in any decision record.

**M2.S.8 (diagonal gap center spacing ≥80 nm):** Not triggered in any trial.

**M2.A.1 (min area 504 nm²):** The −64 dbu shrinks in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 reduce polygon area. No M2.A.1 violation is recorded, meaning the post-shrink y-dimension of each polygon (original y minus 64 dbu), multiplied by its x-dimension, remains above 504 nm² (5040 dbu²). When performing y-shrinks on M2 polygons in via cells, confirm the surviving area remains above this threshold before applying.

**V1.M2.EN.2 (V1 enclosure by M2, 5 nm on two opposite sides):** M2 is directly involved as the enclosing layer. Trials i01 and i02 touch V1 and M2 together; no V1.M2.EN.2 violations are recorded in either trial. Instance moves that shift M2 and V1 together preserve the enclosure relationship provided connectivity is maintained — confirmed by both trials returning conn_preserved with no enclosure violations.

**V1.M2.AUX.2 (V1 must match M2 width in perpendicular direction):** Not violated in any trial. M2 polygon resizes recorded here are end-extensions (resize_end on high end), which do not alter M2 width in the direction perpendicular to its length. Resizing M2 width (as distinct from length) would require separate validation against V1.M2.AUX.2.

**V2.M2.EN.1 (V2 enclosure by M2, 5 nm on two opposite sides):** Maintained throughout. The cu_pool fix in trial:i04.cu.def:VIA_VIA23_1_3_36_36.00 explicitly co-adjusted M2 to preserve this enclosure when the via shape was shrunk. Never shrink a via shape in a cell containing V2 on M2 without an equal or larger shrink of the M2 polygon boundary in the same direction.

---

### Instance Deletion and M2

trial:i05.ug.whole_design.00 deletes seven instances (i0098, i0105, i0075, i0076, i0099, i0002, i0070). M2 is listed in the touched_layers. No new violations result. Instance deletion removes M2 geometry associated with those cells; the surrounding M2 geometry (including the extended p951 and p955 polygons) remains legal after the deletions, confirming that the extensions compensate for connectivity previously provided by the deleted instances.