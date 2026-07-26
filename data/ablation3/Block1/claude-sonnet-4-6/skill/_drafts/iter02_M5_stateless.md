**Via-cell M5 shape resize: y-axis shrink yields improvement; x-axis shrink does not**

Shrinking M5 in the y-axis on a via cell produced a net violation reduction of 52 with connectivity preserved (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00: -88 dbu y-axis resize on M5 in cell VIA_VIA45_1_2_58_58, touching M4, M5, V4, decision applied). Shrinking M5 in the x-axis on a via cell produced zero improvement and was rejected (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01: -96 dbu x-axis resize on M5 in cell VIA_VIA56_2_2_66_58, touching M5, M6, V5, delta_total 0, decision rejected_net_positive). When targeting via cells that overlap M5, apply y-axis resizes before x-axis resizes.

**x-axis M5 resize in via cells carries enclosure and width risk**

The x-axis (horizontal) dimension of M5 is constrained by M5.W.1 (minimum 24 nm horizontal width), M5.W.3/M5.W.4 (forbidden even-multiple widths), M5.S.1 (minimum 24 nm horizontal spacing), and V4.M5.AUX.2 / V5.M5.EN.1 enclosure rules. The rejected x-axis shrink of -96 dbu in trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 produced no net gain. Do not apply x-axis M5 shrinks in via cells without confirming the resulting horizontal extent satisfies all width and enclosure constraints.

**Gated-in unit-gate decisions do not guarantee M5 DRC cleanliness**

A large 57-op unit-gate trial (trial:i02.ug.whole_design.00) touching M3, M4, M5, M6, V3, V4, and V5 was accepted with decision gated_in solely because connectivity was preserved (conn_preserved true), despite introducing 48 new V1.M2.AUX.2 violations. The gated_in criterion is connectivity preservation, not zero new violations. Do not treat a gated_in result as a DRC-clean outcome for M5 or any other touched layer.

**M5 polygon x-axis move deltas of -16 dbu and +32 dbu risk M5.AUX.1 off-grid violations**

In trial:i02.ug.whole_design.00, M5 polygons p1142 and p1144 were moved -16 dbu in x, and p1143 and p1145 were moved +32 dbu in x. M5.AUX.1 requires M5 vertical edges to lie on a 24 nm grid. Neither 16 dbu nor 32 dbu is a multiple of 24 dbu, so these moves risk placing vertical M5 edges off the required grid. Verify M5.AUX.1 grid compliance after any polygon or instance move with x-delta not divisible by 24 dbu.

**M5 polygon y-axis moves: deltas observed in unit-gate trial**

In trial:i02.ug.whole_design.00, M5 polygons p1561 and p1562 were moved +32 dbu and +16 dbu in y respectively, and p1563 was moved -64 dbu in y. M5.W.5 sets the minimum vertical width at 44 nm, and M5.S.2 sets minimum vertical spacing at 40 nm. Y-axis moves must be verified against these constraints after application; the gated_in decision in trial:i02.ug.whole_design.00 does not confirm these constraints are satisfied.

**M5.AUX.2 routing track alignment must be rechecked after any x-axis polygon or instance move**

M5.AUX.2 requires minimum-width M5 tracks to lie on vertical routing tracks at pitch 192 dbu with offset 48 dbu from the origin. The x-axis polygon deltas of -16 and +32 dbu applied in trial:i02.ug.whole_design.00 are not multiples of 192 dbu and are not aligned to the 48 dbu offset pattern, so minimum-width M5 polygons moved by these amounts can violate M5.AUX.2. Confirm routing track alignment independently after each x-axis move.

**M5.AUX.3 no-bend constraint must be preserved across all move operations**

M5.AUX.3 prohibits any bend in M5 geometry. The 57-op move set in trial:i02.ug.whole_design.00 included both x-axis and y-axis displacements applied to distinct polygons within the same design state. Moving polygons independently in x and y does not by itself create bends within a single polygon, but merging M5 shapes after moves can produce L-shaped or bent outlines that violate M5.AUX.3. Verify that no merged M5 region contains corner angles in the 0–90 degree range after any batch of polygon or instance moves.