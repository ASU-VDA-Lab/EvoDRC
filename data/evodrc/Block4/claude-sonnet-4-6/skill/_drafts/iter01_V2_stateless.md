## Repair Operation Outcomes

**resize_via_shape on M3 (y-axis) is ineffective for this via cell configuration.**
Trial trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied a `resize_via_shape` operation shrinking the M3 shape component of cell `VIA_VIA23_1_3_36_36` by −40 dbu along the y-axis. The DRC window counts were unchanged before and after (88 violations in `unit:leaf_0025`, 35 in `unit:leaf_0026`, delta_total=0 in both), and the operation was rejected as not net-positive. Do not apply a y-axis M3 shrink of −40 dbu to this via cell as a standalone V2 repair action.

**Resizing the M3 layer within a via cell simultaneously touches M2, M3, and V2.**
The touched_layers list from trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 is `["M2","M3","V2"]`, confirming that a single `resize_via_shape` on M3 inside a via cell has cross-layer DRC implications. Any attempted repair must account for V2.AUX.1 (V2 must be inside M2 and M3), V2.M2.EN.1 (5 nm enclosure of V2 by M2 on two opposite sides), V2.M3.EN.2 (5 nm enclosure of V2 by M3 on two opposite sides), and V2.M3.AUX.2 (V2 width must match M3 width perpendicular to M3 length) simultaneously — changing M3 bounds risks violating any of these on both M2 and V2 simultaneously.

## Rule Application Notes

**V2.AUX.1 and V2.M3.AUX.2 jointly constrain via shape sizing.**
V2.AUX.1 requires V2 to be entirely inside the intersection of M2 and M3. V2.M3.AUX.2 requires that V2 exactly matches M3 width in the direction perpendicular to M3 length. A shrink of M3 in the y-axis (as attempted in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) risks either pulling M3 inside V2 (AUX.1 violation) or creating a width mismatch (AUX.2 violation) without resolving any existing spacing violations.

**V2.M3.EN.2 requires enclosure on two opposite sides (5 & 5 nm or 5 & 0 nm).**
The rule accepts a zero-enclosure on one side only if the opposite side has at least 5 nm. A y-axis resize that reduces M3 extension beyond V2 on one side below 5 nm while the opposite side is already at or near 0 nm will trigger V2.M3.EN.2. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 shows that a −40 dbu y-shrink on M3 in this cell did not clear any violations, consistent with the enclosure and width-matching constraints leaving no net improvement.

**V2.S.1 spacing depends on M3 track alignment and via end-cap class.**
The rule distinguishes three cases: same M3 track (18 nm), parallel tracks not aligned (27 nm), parallel tracks aligned (18 nm). The computation separates vias with full M3 flush edges (no-end-cap class, `v2_nec`) from those without (`v2_wec`), and applies different mask extensions. No trial in this iteration successfully modified V2 spacing violations, so the relative strictness of the 27 nm not-aligned case remains unverified as a repair target from measured data.

**V2.S.2 and V2.S.3 apply Euclidean (corner-to-corner) spacing, not projection.**
V2.S.2 (23 nm Euclidean between two with-end-cap vias) and V2.S.3 (30 nm Euclidean between two no-end-cap vias) fire only on edge pairs whose violation is detected in Euclidean but not projection. No trial in this iteration targeted these rules; no effective repair approach for them is available from measured data.

**V2.M2.EN.1 requires 5 nm enclosure by M2 on at least two opposite sides.**
This is checked via `m2.sized(-5.nm, 0)` in both x and y. A resize that moves M3 without correspondingly moving M2 or repositioning V2 will leave M2 enclosure unchanged; if V2 is already marginal on M2 enclosure, such a resize may newly trigger V2.M2.EN.1. Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 touched M2 (in the touched_layers list) yet produced no improvement, indicating that the M2 geometry was not the limiting factor but remains a co-constraint.

## Rejected Operations

| Trial | Operation | Delta | Outcome |
|---|---|---|---|
| trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 | resize_via_shape, M3, y, −40 dbu | 0 | rejected_net_positive |