## Move-Instance Operations

Instance moves in 36 dbu x-axis increments are the primary repair vehicle for M1 violations in this design. Across seven accepted trials (trial:i01.ug.Block2_union_row1.00, trial:i01.ug.Block2_union_row3.01, trial:i01.ug.Block2_union_row5.02, trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0007.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0013.08), move_instance ops at delta_dbu [36,0] produced zero new in-crop DRC violations and were accepted as gated_in. One trial used delta [12,0] (trial:i01.ug.leaf_0001.03) and one used [37,0] (trial:i01.ug.leaf_0004.04); both were also accepted with zero new violations. All recorded move_instance deltas are x-axis only (y=0), consistent with the NONORTHOGONAL prohibition on non-axis-aligned M1 geometry.

## M1.A.1: Minimum Area Risk from Instance Moves

Instance moves can introduce new M1.A.1 violations without blocking acceptance. trial:i01.ug.leaf_0013.08 moved a single instance (delta [36,0]) and produced one new in-crop M1.A.1 violation; the trial was nonetheless accepted because conn_preserved=true. M1.A.1 requires a minimum M1 area of 504 nm². Connectivity preservation takes priority over eliminating M1.A.1 violations in the unit_gate channel, but new M1.A.1 violations introduced by instance moves must be recorded: they are not automatically self-correcting and may accumulate across iterations.

## M1 Polygon Resize and resize_end

Resizing an M1 polygon in x by +184 dbu (trial:i01.ug.Block2_union_row1.00) produced no new violations. Resizing the low x-end of M1 polygon p957 by +172 dbu, paired with a VIA_VIA12 add at [5472,2340] (trial:i02.ug.leaf_0001.00), also produced no new violations. Both operations remained axis-aligned and introduced no M1.W.1, M1.S.1/S.2/S.3, V0.M1.EN.1, or V1.M1.EN.1 violations. Resize magnitudes in the 172–184 dbu range are safe for the loci encountered in these trials.

## V0 and V1 Enclosure by M1

When adding VIA_VIA12 at [5472,2340] in trial:i02.ug.leaf_0001.00, the paired resize_end of p957 by 172 dbu on the low-x end was sufficient to satisfy both V0.M1.EN.1 (5 nm minimum enclosure on two opposite sides, with 0 nm permitted on the complementary pair) and V1.M1.EN.1 (5 & 2 nm on opposite sides) without generating new violations. Extending an M1 polygon end toward a new via location by a resize_end satisfies enclosure requirements; trial:i02.ug.leaf_0001.00 confirms this pattern produces a clean result.

## V0.M1.AUX.3: Width Matching Preserved by Instance Moves

V0.M1.AUX.3 requires V0 to exactly match M1 width in the direction perpendicular to M1 length. All move_instance operations across iteration 1 (trial:i01.ug.Block2_union_row1.00 through trial:i01.ug.leaf_0013.08) preserved this constraint, producing zero new V0.M1.AUX.3 violations in every accepted trial. Instance-level moves keep V0-M1 perpendicular width alignment intact. Direct M1 polygon width changes that do not move the via must be separately verified against V0.M1.AUX.3, as no such isolated M1-width change without a paired via adjustment appears in this history.

## add_polygon Approach Superseded for leaf_0001

An M1 polygon added at [[5332,2340],[5532,2340],[5532,2448],[5332,2448]] (200×108 dbu) in trial:i01.ug.leaf_0001.03 was deleted in trial:i02.ug.leaf_0001.00, together with the deletion of instance i0086. The resolved state for leaf_0001 uses resize_end of p957 (+172 dbu, low-x end) paired with VIA_VIA12. Do not reinstate the add_polygon path for this unit; it was explicitly replaced and the delete-and-rebuild sequence in trial:i02.ug.leaf_0001.00 produced zero new violations.

## M1.S Spacing Rules: No Violations Introduced

No M1.S.1 through M1.S.6 violations were newly introduced in any trial across iterations 1 and 2. M1 resize operations of 172–184 dbu in x (trial:i01.ug.Block2_union_row1.00, trial:i02.ug.leaf_0001.00) and instance moves of 12–37 dbu (trial:i01.ug.leaf_0001.03, trial:i01.ug.leaf_0004.04, trial:i01.ug.leaf_0013.08) maintained the required side-to-side spacing of 18 nm (M1.S.1), tip-to-side spacing of 25 nm (M1.S.2), wide-tip-to-tip spacing of 27 nm (M1.S.3), narrow-tip-to-tip spacings of 31 nm (M1.S.4, M1.S.5), and corner-to-corner spacing of 20 nm (M1.S.6) across all loci examined.

## Non-Orthogonal Geometry

No non-axis-aligned M1 operations appear in any trial. All polygon additions and resizes in this history are rectilinear: the add_polygon in trial:i01.ug.leaf_0001.03 used only right-angle vertices, and the resize and resize_end ops in trial:i01.ug.Block2_union_row1.00 and trial:i02.ug.leaf_0001.00 are single-axis adjustments. The NONORTHOGONAL rule disqualifies any M1 edge at angles other than 0 or 90 degrees; avoid any operation that would introduce diagonal M1 geometry.