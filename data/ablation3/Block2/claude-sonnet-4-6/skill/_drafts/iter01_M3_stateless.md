## Via-cell repairs on M3-adjacent vias

The only completed repair touching M3 in this iteration targeted the via cell `VIA_VIA23_1_3_36_36` (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). The four operations all acted on V2 shapes (three shape indices in the via cell) and the M2 shape inside that same cell; no M3 polygon was directly moved or resized, yet M3 appears in `touched_layers`. This establishes that M3 DRC state can change as a side effect of V2/M2 geometry changes inside a via cell, without any direct M3 edit.

The repair was accepted (`decision: applied`, `conn_preserved: true`) and reduced the whole-design violation count by 8 (from 68 to 60) (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). All four resize operations used `axis: y` with `delta_dbu: +64`, meaning every V2 shape and the M2 shape were extended 64 dbu in the y-direction.

## V2.M3.EN.2 and V2.M3.AUX.2 are the rules implicated by y-axis V2 resizes

Rule V2.M3.EN.2 requires that V2 be enclosed by M3 on two opposite sides by at least 5 nm (with the 5 & 0 nm asymmetric form also allowed, provided one opposite side is fully coincident). Rule V2.M3.AUX.2 requires V2 to match M3's width exactly in the direction perpendicular to M3's length. A y-axis extension of V2 shapes directly affects both of these enclosure and width-matching checks. The trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 repair, by growing V2 in y while leaving M3 unchanged, brought the V2 footprint into better alignment with the enclosing M3 geometry as measured by both rules.

When a via cell such as `VIA_VIA23_1_3_36_36` triggers M3 violations (V2.M3.EN.2 or V2.M3.AUX.2), resizing V2 shapes in the axis of the enclosure deficit — here y — is a valid repair path that preserves connectivity (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

## M3 intrinsic spacing and width rules: no repairs observed yet

Rules M3.W.1 (minimum width 18 nm), M3.S.1 (minimum side-to-side spacing 18 nm for edges longer than 36 nm), M3.S.2 (tip-to-side 25 nm), M3.S.3 (tip-to-tip 27 nm when both tips are 24–36 nm), M3.S.4 (tip-to-tip 31 nm when both tips are narrower than 24 nm), M3.S.5 (tip-to-tip 31 nm mixed-width case), M3.S.6 (corner-to-corner 20 nm euclidean), and M3.A.1 (minimum area 504 nm²) have no direct repair records in iteration 1. No prescriptive repair guidance for these rules can be derived from the measured history at this stage.

## V3.M3.EN.1: no repairs observed yet

Rule V3.M3.EN.1 (V3 must be enclosed by M3 on at least two opposite sides by 5 nm) has no repair records in iteration 1. No repair guidance for this rule is available from the measured history.

## NONORTHOGONAL: no violations repaired on M3

The NONORTHOGONAL block flags any non-axis-aligned edge on M3. No repair in iteration 1 addressed a NONORTHOGONAL violation on M3. No repair guidance for this rule is available from the measured history.

## Repair bookkeeping

One trial was executed and applied for M3-adjacent work in iteration 1: trial:i01.cu.def:VIA_VIA23_1_3_36_36.00. All prescriptive statements in this file are grounded in that single record. Rules M3.W.1, M3.S.1–M3.S.6, M3.A.1, V3.M3.EN.1, and NONORTHOGONAL have no measured repair history and therefore carry no derived repair guidance.