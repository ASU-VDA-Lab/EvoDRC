## Via Cell VIA_VIA23_1_3_36_36: Coordinated M2 and V2 Y-Axis Resize

Resizing the M2 via shape in y (+64 dbu) together with all three co-located V2 via shapes in y (+64 dbu each) inside cell `VIA_VIA23_1_3_36_36` produced a net reduction of 8 total violations (68 → 60) with connectivity preserved (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). Apply y-axis resizes to M2 and every V2 shape within this cell together; partial resizing of only the V2 shapes or only the M2 shape is untested by the measured history and leaves the enclosure relationship between M2 and V2 in an unverified state.

V2.M2.EN.1 requires M2 to enclose V2 by ≥ 5 nm on two opposite sides; V2.M2.AUX.2 requires V2 width to match M2 width along the direction perpendicular to M2 length. The co-resize strategy of +64 dbu on both M2 and V2 in the same axis satisfies both constraints simultaneously because the enclosure margin is unchanged while the overlap footprint grows, confirming the via body and the M2 landing pad expand in lock-step (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## Unit-Gate Whole-Design X-Axis Displacement: M2 Wire Extension Pattern

### Instance Move Requires Over-Extended M2 High-End

In both unit_gate iterations, instances were translated in +x and M2 polygon high-ends (the downstream terminus facing the moved instance) were extended in +x by a delta strictly larger than the instance displacement (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00). In trial:i02.ug.whole_design.00, instances moved +32 dbu while M2 high-ends extended +80 to +116 dbu. In trial:i03.ug.whole_design.00, instances moved +72 dbu while M2 high-ends extended +36 to +128 dbu. Do not set the M2 resize delta equal to the instance move delta; the surplus absorption (up to 56 dbu in iter 2 and 56 dbu in iter 3) maintains V1 enclosure margins under V1.M2.EN.2 (≥ 5 nm on two opposite sides) and prevents tip-to-side shortfalls under M2.S.2 (≥ 25 nm when one edge is a tip ≤ 36 nm and the opposing edge is > 36 nm). Both trials gated in with zero new violations inside or outside the crop window and with connectivity preserved (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00).

### Extend the High End Only; Do Not Resize the Low End

In both unit_gate trials every M2 resize_end operation targeted only the high-x end of the affected polygon (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00). The low-x end was never shortened or moved. Shortening the low end is untested in the measured history and would reduce enclosure on the opposite side of any V1 or V2 landing on that terminus.

### Y-Axis M2 Position Was Not Altered in Unit-Gate Operations

No M2 polygon y-axis move or y-axis resize_end appears in trial:i02.ug.whole_design.00 or trial:i03.ug.whole_design.00. Y-axis polygon moves in iter 2 apply to other-layer polygons only. Confine whole-design x-displacement repairs to x-axis instance moves and x-axis M2 high-end extensions; do not introduce y-axis M2 movement as part of the unit_gate repair strategy, as it is unvalidated in the measured history.

## Spacing and Width: No Violations Introduced Across All Trials

M2.W.1 sets a minimum wire width of 18 nm. All M2 operations in the measured history used resize_end to extend the wire in x or resize the via landing pad in y; no cross-section narrowing occurred, and no M2.W.1 violations appeared in any trial (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00).

M2.S.1 (side-to-side ≥ 18 nm for edges > 36 nm), M2.S.2 (tip-to-side ≥ 25 nm), M2.S.3 (tip-to-tip ≥ 27 nm when both tips 24–36 nm), M2.S.4 (tip-to-tip ≥ 31 nm when both tips < 24 nm), and M2.S.5 (tip-to-tip ≥ 31 nm, mixed narrow/wide tips) were all unviolated after unit_gate operations. The x-only extension of M2 high-ends with per-polygon surplus deltas absorbed differential displacement between adjacent wires without collapsing any gap below the applicable minimum. No new spacing violations of any class were introduced (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00).

M2.S.7 forbids co-location of an 18 nm tip-to-tip gap with a side-to-side spacing ≤ 32 nm unless the parallel run length is ≥ 35 nm. Extending M2 high-ends in the direction of instance travel preserves the existing run length along the wire and does not create new facing-tip conditions on the same track; no M2.S.7 violations appeared in either unit_gate trial (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00).

M2.A.1 sets a minimum M2 area of 504 nm². Extension of M2 polygon ends strictly increases polygon area; no M2.A.1 violation was created by any M2 resize in the measured history (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00).

## Connectivity and Gating

All three trials preserved connectivity (conn_preserved: true). The cu_pool trial was accepted as `applied`; both unit_gate trials were accepted as `gated_in`. In all cases, operations on M2 did not break nets. When resizing M2 via landing pads in y alongside V2 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) or extending M2 wire termini in x alongside instance moves (trial:i02.ug.whole_design.00, trial:i03.ug.whole_design.00), connectivity is preserved provided the resize keeps the M2 polygon fully covering the associated via footprint on all required sides.