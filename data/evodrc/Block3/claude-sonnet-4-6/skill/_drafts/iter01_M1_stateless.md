All ten history trials share the same outcome: decision `gated_in`, `conn_preserved: true`, and zero new violations both inside and outside the crop window. The knowledge below is distilled exclusively from those records.

---

## Repair operation patterns observed on M1

### Paired move-instance + resize_end (x-axis, high end) is the dominant repair idiom

Six of the ten accepted trials combine one or more `move_instance` ops (positive x direction) with a `resize_end` on axis x, end `high`, applied to the M1 polygon that hosts the moved instance. In every such pairing the resize delta exceeds the move delta: trial:i01.ug.Block3_union_row1.00 moved instances by 136 dbu while extending three M1 polygons by 192 dbu each; trial:i01.ug.Block3_union_row8.03 showed four pairs with move/resize ratios of 108/164, 72/128, 72/128, and 72/92; trial:i01.ug.leaf_0012.08 moved 72 dbu and extended by 108 dbu; trial:i01.ug.leaf_0007.05 moved 36 dbu and extended by 56 dbu on two polygons; trial:i01.ug.leaf_0008.06 moved 136 dbu and extended by 92 dbu (x) alongside a 4 dbu x-move with no paired resize and a separate 20 dbu y-high resize. Always extend the high-end of the M1 polygon by more than the instance displacement when the via must remain enclosed: the extra margin beyond the move delta directly adds to the enclosure that V0.M1.EN.1 (5 nm minimum on two opposite sides) and V1.M1.EN.1 (5 & 2 nm) require.

### Pure move-instance sequences (no resize) are safe when no enclosure change is needed

Four trials applied only `move_instance` ops and introduced zero new violations: trial:i01.ug.Block3_union_row2.01 (two instances moved +36 dbu x), trial:i01.ug.leaf_0006.04 (two instances moved +36 dbu x), trial:i01.ug.leaf_0009.07 (one instance moved +36 dbu x), trial:i01.ug.leaf_0013.09 (one instance moved −36 dbu x). Use move-only when the associated M1 polygon already provides sufficient enclosure on both the moved axis and the opposite side after displacement, so that V0.M1.EN.1 and V1.M1.EN.1 are not degraded.

### Negative x displacement is safe at −36 dbu

trial:i01.ug.leaf_0013.09 is the only record with a leftward move (−36 dbu x) and it was accepted with zero new violations. Do not assume the high-end resize idiom is required for leftward moves; use it only when the enclosure on the low side drops below the 5 nm threshold.

### y-axis resize is rare and small

The only y-axis resize in the dataset is a +20 dbu high-end extension in trial:i01.ug.leaf_0008.06, applied to polygon p1159 while other ops in the same trial handled x-direction corrections. This trial was accepted with zero new violations. Limit y-axis resizes to the minimum needed to satisfy enclosure on the perpendicular pair required by V0.M1.EN.1 and V1.M1.EN.1.

---

## Enclosure rules: V0.M1.EN.1 and V1.M1.EN.1

**V0.M1.EN.1** flags a V0 when M1 does not enclose it by at least 5 nm on one of two opposite sides (horizontal or vertical), with the relaxation that one side may be 0 nm provided the other is 5 nm. The resize_end high deltas in trial:i01.ug.Block3_union_row1.00 (192 dbu beyond a 136 dbu instance shift) and trial:i01.ug.Block3_union_row8.03 (164, 128, 128, 92 dbu extensions) all cleared this check: the net M1 extension beyond the via position on the high side exceeded 5 nm in each case.

**V1.M1.EN.1** is stricter on the asymmetric pair: 5 nm on the longer side and 2 nm on the shorter side. All trials that touched V1 (every trial touched V1 per `touched_layers`) were accepted. The consistent pattern is that resize deltas larger than the instance move delta preserve both the 5 nm and 2 nm sides simultaneously.

**V0.M1.AUX.3** requires V0 to be exactly the same width as M1 perpendicular to the M1 length direction. No trial applied a width change to M1 that would alter this relationship; all accepted ops either moved instances (which carry both V0 and the containing M1 together) or extended the M1 length-direction endpoint only. Do not apply a y-direction resize that narrows M1 to be narrower than V0 in that axis.

---

## Width and spacing headroom

**M1.W.1** (minimum 18 nm width) was not violated in any trial. The smallest resize delta applied was +20 dbu (y-axis, trial:i01.ug.leaf_0008.06); the smallest x-axis move was 36 dbu. Both are well above the 18 nm threshold. Avoid shrinking M1 width below 18 nm when resizing the low end inward.

**M1.S.1** (minimum 18 nm side-to-side spacing when both edges > 36 nm) and **M1.S.2** (minimum 25 nm tip-to-side when one edge ≤ 36 nm and the other > 36 nm) were not triggered in any trial. All accepted high-end extensions moved the tip away from neighboring polygons, increasing spacing rather than decreasing it.

**M1.S.3** (minimum 27 nm tip-to-tip when both edges are 24–36 nm), **M1.S.4** (minimum 31 nm tip-to-tip when both edges < 24 nm), and **M1.S.5** (minimum 31 nm tip-to-tip when one edge is 24–36 nm and the other < 24 nm) are all tip-based. The resize_end high operations observed in trials i01.ug.Block3_union_row1.00 through i01.ug.leaf_0012.08 extended tips outward into open space (zero new violations result confirms no adjacent tip was close enough to form a new violation). Before applying a high-end extension, verify that the extended tip does not approach a neighboring polygon's tip or side within 27–31 nm depending on the tip widths involved.

**M1.S.6** (minimum 20 nm corner-to-corner between M1 polygons) was not violated in any trial. Extensions along the x high-end pull corners away from neighbors in that direction.

**M1.A.1** (minimum area 504 nm²) was not triggered. All resize ops increased M1 area. Do not shrink M1 area below 504 nm²; the measured ops are all area-increasing or area-neutral.

---

## Connectivity preservation is a gate condition

Every accepted trial reports `conn_preserved: true` and `reason: conn_preserved`. The harness gates on this: a repair that breaks connectivity is not applied regardless of DRC outcome. All observed ops move instances and extend their host polygons together, preserving the M1–V0–M1 and M1–V1–M1 stack continuity. When constructing a repair, ensure that every V0 or V1 that was inside M1 before the op remains inside M1 after the op.

---

## Multi-layer coupling

All ten trials touched M1, M2, and V1 simultaneously. Trial:i01.ug.leaf_0008.06 additionally touched M3. M1 ops do not occur in isolation: instance moves propagate to all layers attached to that instance. Coordinate M1 polygon resizes with the V1 and M2 state above to avoid introducing spacing or enclosure violations on those layers when extending M1.

---

## M1.R.0 (redundant island) avoidance

M1.R.0 flags an M1 island that encloses exactly one small V0 when that island sits near a large empty M1 region (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm). No trial triggered this rule. The observed pattern of extending existing M1 polygons rather than inserting new isolated M1 shapes avoids creating new islands. Do not introduce a standalone M1 polygon to resolve an enclosure violation when the polygon would be isolated near a large empty area; instead extend the existing M1 endpoint as shown in trial:i01.ug.Block3_union_row1.00 and trial:i01.ug.Block3_union_row8.03.

---

## Non-orthogonal geometry

The NONORTHOGONAL rule applies to M1. No trial introduced non-orthogonal edges: all `resize_end` ops were axis-aligned (x or y) and all `move_instance` ops preserved the Manhattan geometry of the moved polygons. Restrict all M1 polygon modifications to horizontal and vertical edges only.