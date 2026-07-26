## Operation Repertoire

All repairs in the history apply one or more of five distinct operation types to M1 and its associated via layers. Every trial in the full history (46 records, iterations 1–5) carries conn_preserved=true and decision=gated_in, confirming that each strategy below was safe for connectivity.

**move_instance** translates all M1 shapes belonging to an instance by a signed (x, y) delta. Trials that rely exclusively on this operation include trial:i01.ug.Block7_union_row11.01 (two instances moved +36 dbu in x), trial:i01.ug.Block7_union_row9.21 (five instances each moved +40 dbu in x), and trial:i01.ug.leaf_0001.22 (single instance moved +108 dbu in x).

**resize_end** extends or retracts one tip of an M1 polygon along one axis. It is applied when instance placement alone leaves insufficient enclosure over a via or a spacing gap remains after the instance shifts. trial:i01.ug.Block7_union_row12.02 combines a +36 dbu instance move with a +56 dbu resize_end on the high-x end of polygon p3273. trial:i02.ug.Block7_union_row9.06 pairs a +56 dbu instance move with a +112 dbu resize_end on the high-x end of polygon p3683.

**resize** (no end specifier) resizes a polygon body symmetrically along one axis. trial:i01.ug.Block7_union_row15.05 applies a +160 dbu x-axis resize to polygon p3586. trial:i02.ug.Block7_union_row15.03 applies a +96 dbu y-axis resize to polygon p3592.

**move** (polygon body) translates an entire polygon without altering its dimensions. trial:i01.ug.Block7_union_row16.06 moves polygon p3516 by −12 dbu in y. trial:i02.ug.leaf_0014.08 moves polygon p3515 by −12 dbu in y.

**add_polygon** inserts a new shape on a layer. The add_polygon in trial:i01.ug.Block7_union_row20.10 creates a 56×72 dbu M2 rectangle; the 72 dbu minor dimension matches the M1.W.1 minimum width threshold (18 nm) when compared against rule-specified geometry. The add_polygon in trial:i03.ug.leaf_0002.04 creates a 244×72 dbu M3 shape. No add_polygon targeting M1 itself appears in any record.

---

## Instance Move Direction and Magnitude

Instance moves in x dominate across all four active repair iterations. The most common single-step x deltas are 36 dbu and 40 dbu, appearing across trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row14.04, trial:i01.ug.Block7_union_row17.07, trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row12.01, trial:i02.ug.Block7_union_row13.02, and trial:i03.ug.Block7_union_row13.01. Larger x deltas of 108 dbu appear in trial:i01.ug.leaf_0001.22, trial:i01.ug.leaf_0008.24, trial:i01.ug.Block7_union_row7.19, and trial:i03.ug.leaf_0008.06. Deltas of 136 dbu appear in trial:i01.ug.Block7_union_row13.03 and trial:i01.ug.Block7_union_row24.14.

Negative x instance moves are applied when the repair requires compressing space on the high-x side. trial:i01.ug.Block7_union_row3.15 moves instance i1891 by −36 dbu. trial:i01.ug.leaf_0024.25 moves one instance −24 dbu and a second −108 dbu in x. trial:i04.ug.leaf_0004.03 moves instance i1140 by −56 dbu in x.

Vertical (y-axis) instance moves appear in repairs that target y-direction enclosure or spacing. trial:i01.ug.Block7_union_row16.06 moves two instances −12 dbu in y alongside a polygon move of −12 dbu in y. trial:i01.ug.leaf_0095.26 moves two instances +48 dbu in y with polygon resize_end extensions of +68 and +48 dbu on the high-y end. trial:i02.ug.Block7_union_row15.03 moves instance i1062 −84 dbu in y and applies a +96 dbu y-axis polygon resize. trial:i04.ug.leaf_0005.04 moves instance i1062 −44 dbu in y, and trial:i04.ug.leaf_0007.06 moves instance i0177 +48 dbu in y.

---

## Multi-Instance Coordinated Moves

When a repair must clear spacing across M1 shapes belonging to multiple instances, all affected instances move by the same or closely matched delta in the same direction. trial:i01.ug.Block7_union_row9.21 moves five instances (i1117, i1398, i1215, i1178, i1885) each by +40 dbu in x. trial:i01.ug.Block7_union_row6.18 moves six instances by +28 or +36 dbu in x. trial:i02.ug.Block7_union_row22.05 moves five instances by +32 or +36 dbu in x together with a single resize_end on polygon p3527.

Not all instances in a repair need the same delta. trial:i01.ug.Block7_union_row14.04 moves eight instances with x deltas of +36, +52, +72, and +108 dbu across different instance positions, while also extending polygon p3539's high-x end by +16 dbu. trial:i01.ug.Block7_union_row13.03 moves three instances by +136 dbu while polygon p3526 receives an asymmetric resize (−56 dbu on the low-x end, +100 dbu on the high-x end) and polygon p3525 receives a +192 dbu high-x extension.

---

## Polygon Resize and End-Extension Patterns

resize_end operations extend one tip of an M1 polygon in the direction required to cover a via or satisfy a spacing rule. The axis and end always correspond to the dimension being expanded. trial:i01.ug.Block7_union_row24.14 extends the high-x ends of polygons p3058, p3635, and p3564 by +136, +120, and +128 dbu respectively, alongside three instance moves of +64–136 dbu. trial:i01.ug.leaf_0095.26 extends the high-y end of polygon p3537 by +48 dbu and the high-y end of polygon p2432 by +68 dbu.

resize_end on the low end repositions the near tip of a polygon, expanding it toward lower coordinates. trial:i01.ug.Block7_union_row3.15 applies a +56 dbu resize_end on the low-x end of polygon p3384 (expanding the polygon toward −x) alongside a −36 dbu instance move. trial:i01.ug.Block7_union_row17.07 applies a +56 dbu resize_end on the low-x end of polygon p3187 alongside four +36 dbu instance moves.

Both ends of a polygon may be modified in the same repair. trial:i01.ug.Block7_union_row13.03 extends polygon p3526 with −56 dbu on the low-x end and +100 dbu on the high-x end. trial:i03.ug.leaf_0007.05 applies a +72 dbu x-low resize_end and −48 dbu on both y-low and y-high ends of polygon p3592, changing both the horizontal position and vertical extent simultaneously.

---

## Via Enclosure Repairs (V0.M1.EN.1, V1.M1.EN.1)

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm per the projection variant). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one axis and at least 2 nm on the other. Both rules check edges in the horizontal and vertical directions independently.

Enclosure repairs combine instance moves with selective polygon end extensions. trial:i01.ug.Block7_union_row8.20 moves instance i1891 −36 dbu in x and applies a +56 dbu resize_end on the low-x end of polygon p3430, expanding M1 coverage over the via while adjusting spacing on the other side. trial:i02.ug.Block7_union_row9.06 moves instance i1150 +56 dbu in x and extends polygon p3683's high-x end by +112 dbu.

Vertical enclosure repairs use y-direction moves and y-axis polygon extensions. trial:i01.ug.leaf_0095.26 moves two instances +48 dbu in y and extends y-high polygon ends by +48 and +68 dbu. trial:i02.ug.leaf_0014.08 moves two instances −12 dbu in y and moves polygon p3515 −12 dbu in y. trial:i03.ug.leaf_0011.07 moves instances −48 dbu in y and retracts the y-high end of polygon p3537 by −48 dbu, partially reversing the y-extension applied in trial:i01.ug.leaf_0095.26 on the same unit. trial:i04.ug.leaf_0007.06 moves instance i0177 +48 dbu in y.

---

## Spacing Rule Repairs (M1.S.1, M1.S.2, M1.S.3)

M1.S.1 governs minimum side-to-side spacing (18 nm) between M1 edges longer than 36 nm. M1.S.2 governs tip-to-side spacing (25 nm) between a short edge (≤36 nm) and a long edge (>36 nm). M1.S.3 governs tip-to-tip spacing (27 nm) between two edges each 24–36 nm long.

Side-to-side spacing repairs combine instance moves with selective polygon extensions. trial:i01.ug.Block7_union_row14.04 moves eight instances with x deltas of 36–108 dbu and extends polygon p3539's high-x end by +16 dbu. trial:i01.ug.Block7_union_row18.08 moves instances by +72 or −72 dbu in x, extends polygon p3532's high-x end by +60 dbu, and expands polygon p3096's low-x end by +92 dbu.

For tip-related spacing violations, the repair moves the tip away or extends the M1 end. trial:i01.ug.Block7_union_row7.19 moves instance i1446 by +108 dbu in x and extends polygon p3317's high-x end by +128 dbu, a combined displacement well above the 27 nm M1.S.3 minimum. trial:i01.ug.Block7_union_row24.14 extends three polygon high-x ends by 120–136 dbu alongside instance moves of 64–136 dbu.

---

## V0.M1.AUX.3 (Via Width Match)

V0.M1.AUX.3 requires V0 to be exactly as wide as the enclosing M1 strip in the direction perpendicular to M1 length. When M1 polygon ends are extended past the via boundary, new convex corner edges of V0 may no longer coincide with M1 edges, triggering this rule. The strategy observed in the history is to move the via-containing instance rather than resize the M1 polygon when the via-side M1 edge must remain fixed. trial:i01.ug.Block7_union_row11.01 moves two instances +36 dbu in x with no polygon resize, preserving the V0-to-M1 width alignment. trial:i01.ug.Block7_union_row17.07 moves four instances +36 dbu each and applies a single resize_end only on the far-side polygon end (low-x of p3187), leaving the via-adjacent M1 edge unchanged.

---

## Non-Orthogonal Geometry (GEOMETRY.NONORTHOGONAL)

The NONORTHOGONAL check fires on any M1 edge whose angle lies between 1–89°, 91–179°, or the equivalent negative-angle ranges. No trial in the history introduces non-orthogonal M1 edges. All observed move_instance, resize_end, resize, move, and add_polygon operations translate or extend M1 shapes exclusively along the x or y axis, preserving axis-aligned geometry. trial:i01.ug.Block7_union_row19.09 applies both x and y instance moves (one instance moves y −48 dbu while others move x +36–72 dbu) but each individual shape retains orthogonal edges.

---

## M1.R.0 (Redundant Island)

M1.R.0 flags an M1 island enclosing exactly one small V0 via when that island lies near a large empty M1 region (≥500 nm wide, area >2.5 µm², expanded by 400 nm). No trial in the history creates a standalone M1 island over a single V0. The add_polygon operations in trial:i01.ug.Block7_union_row20.10 and trial:i03.ug.leaf_0002.04 target M2 and M3 respectively, not M1, so they do not produce M1 shapes subject to M1.R.0.

---

## M1.W.1 and M1.A.1 (Width and Area)

M1.W.1 requires a minimum width of 18 nm. The M2 add_polygon in trial:i01.ug.Block7_union_row20.10 has a 72 dbu minor dimension; the M3 add_polygon in trial:i03.ug.leaf_0002.04 also has a 72 dbu height. These 72 dbu dimensions match the M1.W.1 minimum-width threshold at the scale of the design, establishing 72 dbu as the minimum viable M1 stripe width in this technology. No resize or move operation in the history produces an M1 polygon narrower than this dimension.

M1.A.1 requires minimum M1 area of 504 nm². All polygon bodies after resize_end operations in the history remain substantially above this minimum. The smallest resize_end deltas observed (e.g., +16 dbu in trial:i01.ug.Block7_union_row14.04) extend existing polygons rather than creating new minimum-size shapes, so area compliance is maintained through the parent polygon's existing geometry.

---

## Iteration Convergence Pattern

Units that appear across multiple iterations show progressive repair convergence: op count and delta magnitude decrease as residual violations shrink. Block7_union_row10 appears in iter 1 (trial:i01.ug.Block7_union_row10.00, six ops including a +308 dbu resize_end and +288 dbu instance move) and iter 3 (trial:i03.ug.Block7_union_row10.00, two ops: +56 dbu instance move and +52 dbu resize_end) with a much smaller locus in iter 3.

Block7_union_row13 appears in iter 1 (trial:i01.ug.Block7_union_row13.03, six ops with deltas up to +192 dbu), iter 2 (trial:i02.ug.Block7_union_row13.02, three ops with deltas of +36, −72, +36 dbu), and iter 3 (trial:i03.ug.Block7_union_row13.01, two ops each +36 dbu), confirming that large initial moves leave progressively smaller residuals.

Block7_union_row20 appears in iter 1 (trial:i01.ug.Block7_union_row20.10, two ops including an M2 add_polygon), iter 2 (trial:i02.ug.Block7_union_row20.04, three ops), and iter 3 (trial:i03.ug.Block7_union_row20.02, single +36 dbu instance move).

leaf_0004 is repaired in iter 4 (trial:i04.ug.leaf_0004.03, −56 dbu in x) and re-addressed in iter 5 (trial:i05.ug.leaf_0004.03, −96 dbu in x and −48 dbu in y), indicating that a prior x-only repair introduced or left a y-direction violation requiring a combined two-axis move on the next pass.