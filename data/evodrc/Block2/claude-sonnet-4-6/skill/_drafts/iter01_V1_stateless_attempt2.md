## Observed Repair Patterns for V1 (Iteration 1)

### Co-repair of V1, M1, and M2

Every accepted fix in this iteration touched V1 together with M1 and M2 in the same operation set (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06). Do not plan V1 repair ops in isolation from M1 and M2; the rules V1.AUX.1, V1.M1.EN.1, V1.M2.EN.2, and V1.M2.AUX.2 couple V1 geometry to both adjacent metal layers by construction, so always include M1 and M2 in the touched-layer set when moving or resizing to fix a V1 violation.

### Move-Only Sufficiency

A repair consisting solely of move_instance ops, with no polygon resize, cleared violations in three units. Trial:i01.ug.Block2_union_row1.00 used two move_instance ops (both +36 dbu in x). Trial:i01.ug.leaf_0004.04 and trial:i01.ug.leaf_0007.05 each used a single move_instance (+36 dbu in x). All three were accepted with conn_preserved=true and no new violations in or out of crop. Prefer move_instance before adding resize_end when the locus contains no M2 polygon that must be stretched to maintain enclosure or width.

### Move Combined with Resize

Four units required at least one resize_end op in addition to move_instance. Trial:i01.ug.Block2_union_row3.01 combined two move_instance ops (+36 dbu x) with one resize_end on the high-x end of polygon p1040 (+36 dbu). Trial:i01.ug.Block2_union_row5.02 combined two move_instance ops (+64 dbu x) with two resize_end ops on the high-x ends of polygons p1059 and p1057 (+64 dbu each). Trial:i01.ug.leaf_0001.03 combined one move_instance (+128 dbu x) with a high-end resize of p1065 (+184 dbu) and a low-end resize of p957 (+176 dbu). Trial:i01.ug.leaf_0011.06 combined one move_instance (+36 dbu x) with one high-end resize of p1052 (+36 dbu). Apply resize_end when the moved instance would otherwise violate V1.M2.EN.2 or V1.M2.AUX.2 by leaving an M2 polygon too short to maintain enclosure or width-match against the repositioned V1.

### Move Magnitudes

Three distinct x-displacement magnitudes appear in accepted fixes: 36 dbu (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06), 64 dbu (trial:i01.ug.Block2_union_row5.02), and 128 dbu (trial:i01.ug.leaf_0001.03). Do not use a smaller move than the spacing or enclosure shortfall requires; the accepted records show that the repair engine selected move magnitudes matched to the measured violation gap in each locus.

### Axis Directionality

All move_instance deltas in this iteration are in the x-direction only, with a y-component of zero (trial:i01.ug.Block2_union_row1.00 [36,0], trial:i01.ug.Block2_union_row3.01 [36,0], trial:i01.ug.Block2_union_row5.02 [64,0], trial:i01.ug.leaf_0001.03 [128,0], trial:i01.ug.leaf_0004.04 [36,0], trial:i01.ug.leaf_0007.05 [36,0], trial:i01.ug.leaf_0011.06 [36,0]). All resize_end ops recorded this iteration specify axis:"x" (trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0011.06). V1.S.1 and V1.S.2/S.3/S.4 are projection-based checks along and perpendicular to M2 tracks; moving along x resolves projection-spacing violations without disturbing orthogonal track assignments, consistent with the NONORTHOGONAL rule that forbids non-90-degree edges.

### Resize End Selection

The resize_end end parameter was "high" in all cases except one. Trial:i01.ug.leaf_0001.03 applied end:"high" to p1065 (+184 dbu) and end:"low" to p957 (+176 dbu) in the same fix, indicating that a fix locus can contain M2 polygons on both sides of the moved instance, each requiring its nearer end extended toward the new instance position. Do not assume a single end direction covers all polygons in a multi-instance locus; use end:"low" on polygons whose high end is already flush and whose low end faces the repositioned V1.

### Connectivity and Violation Budget

Every accepted fix preserved connectivity (conn_preserved=true) and introduced zero new violations inside or outside the crop window (n_new_in_crop=0, n_new_out_of_crop=0) across all seven trials. Discard any candidate fix for a V1 violation that breaks connectivity or propagates new violations, consistent with the gated_in acceptance criterion applied in trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0011.06.

### M2 Enclosure and Width-Match Context

V1.M2.EN.2 requires M2 to enclose V1 on two opposite sides by 5 & 5 nm or 5 & 0 nm, and V1.M2.AUX.2 requires V1 to match M2 width exactly in the direction perpendicular to M2 length. When move_instance is paired with resize_end, as in trial:i01.ug.leaf_0001.03 where p1065 was extended by 184 dbu and p957 by 176 dbu (larger than the 128 dbu instance move), the resize magnitudes exceeded the move delta. Apply additional length to the M2 resize beyond the instance displacement only when needed to restore the minimum enclosure required by V1.M2.EN.2 at the new instance position.