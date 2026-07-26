**Movement direction and axis constraints**

All ten accepted unit_gate trials that touch M2 apply displacement exclusively along the x-axis: trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0001.01, trial:i02.ug.leaf_0002.02, and trial:i03.ug.leaf_0002.01. No y-axis unit_gate displacement on M2 has been accepted across three iterations. Never apply y-axis instance moves targeting M2 spacing correction; the x-axis is the operative direction for all M2 fixes observed.

**Common move magnitudes**

X-axis displacement magnitudes in accepted unit_gate trials on M2 are: 4 dbu (trial:i01.ug.Block5_union_row6.01), 8 dbu (trial:i02.ug.leaf_0001.01), 36 dbu (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i03.ug.leaf_0002.01), 72 dbu (trial:i02.ug.leaf_0002.02), and 104 dbu (trial:i02.ug.Block5_union_row6.00). All values are multiples of 4 dbu. The 36 dbu step appears in six of the ten accepted unit_gate trials and is the most prevalent M2 repair displacement observed.

**Resize operations on M2 polygons**

Three accepted trials include a resize_end on an M2 polygon, all targeting the high end of the x-axis: trial:i01.ug.Block5_union_row3.00 (p967, axis=x, end=high, +36 dbu), trial:i01.ug.leaf_0001.02 (p974, axis=x, end=high, +72 dbu), and trial:i02.ug.Block5_union_row6.00 (p955, axis=x, end=high, +20 dbu). Every M2 polygon resize observed expands the high end; no M2 low-end resize has been accepted. Do not apply resize_end to the x-axis low end of M2 polygons without a distinct measured basis beyond what is recorded here.

**Opposing instance moves**

Trial trial:i01.ug.leaf_0002.03 pairs two instance moves in opposite x-directions: i0056 at [+36, 0] and i0103 at [-36, 0], both accepted as a single gated_in trial. When two M2 polygons on adjacent instances are too close, moving the bounding instances symmetrically apart along x is a valid repair pattern.

**Acceptance with new in-crop violations**

Trial trial:i03.ug.leaf_0002.01 was accepted (decision=gated_in) despite introducing n_new_in_crop=1. The acceptance criterion was conn_preserved=true with n_new_out_of_crop=0. The gate does not block a trial that introduces one new in-crop violation when connectivity is preserved and no out-of-crop violations are added. Do not treat n_new_in_crop=1 as an automatic rejection condition when conn_preserved=true and n_new_out_of_crop=0.

**cu_pool trials touching M2 via V2/M3**

Three cu_pool trials targeted VIA_VIA23_1_3_36_36 and touched M2 indirectly through the V2/M3 interface:

- trial:i02.cu.def:VIA_VIA23_1_3_36_36.00: single op resize_via_shape M3 y-axis -40 dbu; rejected (delta_total=0, rejected_net_positive).
- trial:i02.cu.def:VIA_VIA23_1_3_36_36.01: ten ops across M3, V3, M4, and bilateral y-shrinks on M2 polygon ends p891/p892/p893 (-32 dbu each end); rejected (delta_total=+5, net increase).
- trial:i03.cu.def:VIA_VIA23_1_3_36_36.00: same single op as trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 (resize_via_shape M3 y/-40 dbu); applied (delta_total=-8).

The identical single-op move was rejected in iter 2 (design_state c5292a...) and applied in iter 3 (design_state d7ef52...). The intervening unit_gate repairs altered the layout sufficiently that the same via resize became net-beneficial. Do not permanently discard a single-op via resize because it failed in a prior design state; re-evaluate it after other repairs have been applied.

The multi-op trial trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 applied bilateral y-axis shrinks of 32 dbu on both ends of M2 polygons p891, p892, and p893 and produced a net increase of 5 violations. Avoid simultaneous bilateral y-shrink on M2 polygon ends when targeting V2/M2 enclosure violations; the measured outcome is net-positive DRC count.

**V2.M2.EN.1 enclosure: repair via M3 resize, not direct M2 resize**

V2.M2.EN.1 requires V2 to be enclosed by M2 by at least 5 nm on at least two opposite sides. The only applied cure in the history for V2-adjacent M2 violations is a y-axis resize of the M3 via shape by -40 dbu (trial:i03.cu.def:VIA_VIA23_1_3_36_36.00), with no direct modification to M2. Resizing the via cell from the layer above without touching M2 directly achieved a delta_total of -8. Prefer resizing the adjacent via cell over resizing M2 directly for V2.M2.EN.1 violations.

**V1.M2.EN.2 and V1.M2.AUX.2 compatibility with instance moves**

V1.M2.EN.2 requires M2 to enclose V1 by 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). V1.M2.AUX.2 requires V1 to have exactly the same width as M2 in the direction perpendicular to M2 length. All accepted unit_gate trials that move instances on M2 also list V1 in touched_layers (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.Block5_union_row6.01, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i02.ug.Block5_union_row6.00, trial:i02.ug.leaf_0002.02, trial:i03.ug.leaf_0002.01). Instance moves translate M2 and V1 together, preserving the M2/V1 width correspondence required by V1.M2.AUX.2. Do not resize M2 without co-resizing the associated V1, as that would violate V1.M2.AUX.2.

**M2.W.1 and M2.A.1 constraints on resize**

M2.W.1 sets minimum width at 18 nm. M2.A.1 sets minimum area at 504 nm². All M2 resize_end operations in the history expand the polygon (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i02.ug.Block5_union_row6.00), consistent with preserving these minimums. Do not shrink an M2 polygon to width < 18 nm or area < 504 nm².

**M2 spacing rules: key thresholds**

M2.S.1 (side-to-side, both edges > 36 nm): minimum 18 nm. M2.S.2 (tip-to-side, tip <= 36 nm, side > 36 nm): minimum 25 nm. M2.S.3 (tip-to-tip, both edges 24–36 nm): minimum 27 nm. M2.S.4 (tip-to-tip, both edges < 24 nm): minimum 31 nm. M2.S.5 (tip-to-tip, one 24–36 nm, other < 24 nm): minimum 31 nm. M2.S.6 (corner-to-corner, euclidian): minimum 20 nm.

The x-axis moves in accepted trials correct spacing violations governed primarily by M2.S.1. A 4 dbu move (trial:i01.ug.Block5_union_row6.01) resolved one context while 36 dbu was required in six others (trial:i01.ug.Block5_union_row3.00, trial:i01.ug.leaf_0001.02, trial:i01.ug.leaf_0002.03, trial:i01.ug.leaf_0005.04, trial:i01.ug.leaf_0006.05, trial:i03.ug.leaf_0002.01). The required displacement is proportional to the initial gap deficit; always verify the post-move spacing satisfies the applicable rule for the specific edge-length combination present.

**M2.S.7 and M2.S.8 compound spacing rules**

M2.S.7 forbids a tip-to-tip gap of 18 nm co-located with side-to-side spacing <= 32 nm; parallel run length must be >= 35 nm when side spacing <= 32 nm. M2.S.8 requires the euclidian center-to-center distance between 18 nm tip-to-tip gaps on different M2 tracks to be >= 80 nm. No trial in the history directly targeted isolated M2.S.7 or M2.S.8 violations. When applying x-axis instance moves to correct M2.S.1, verify that tip-to-tip gaps on adjacent tracks remain >= 80 nm center-to-center so that M2.S.8 is not introduced.