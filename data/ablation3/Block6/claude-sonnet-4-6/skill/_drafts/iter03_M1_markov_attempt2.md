## Per-rule recipes

### Family A: M1-via cluster (V0.M1.AUX.3, M1.S.2, M1.S.6, V1.M1.EN.1)

These four rules often cluster around a VIA_VIA12 instance placed where local M1 geometry fails width-matching, spacing, or enclosure constraints (seed). A single site usually fires one to three of them, not necessarily all four; the 37-violation example block assigns 18 of 37 violations to this family.

Rule semantics (ASAP7 rule deck):
- V0.M1.AUX.3: V0 must exactly match M1 width perpendicular to M1 length; the V0 y-extent must equal the M1 y-extent at the landing location (seed).
- V1.M1.EN.1 (deck hgood/vgood construction; description "5 & 2 nm"): on ONE pair of opposite sides -- either the x-pair or the y-pair -- BOTH sides must be >= 2 nm (8 dbu) AND at least ONE of the two >= 5 nm (20 dbu) (seed). Fires when NEITHER pair achieves this on the merged M1.
- M1.S.2: Tip-to-side spacing >= 25 nm (100 dbu) when one edge is <= 36 nm and the other > 36 nm (seed).
- M1.S.6: Corner-to-corner spacing >= 20 nm (80 dbu) (seed).

Root cause pattern: A VIA_VIA12 (cell = M1 land + M2 land + V1 cut; it does NOT contain V0 -- V0 (layer 18) is the std-cell contact level below, and V0.M1.AUX.3 is checked on the MERGED M1 around it) is placed at a coordinate where the merged M1 has an edge mismatch or insufficient extension. Moving the via to a nearby M1-valid position clears multiple rules of this family at once (reference-design-verified). Observed move shapes: pure-x single-instance (e.g. +136 dbu, examples A2/A3); pure-y single-instance (e.g. +68 dbu, example A4); two-axis single-instance (e.g. (+72,-108) dbu); pure-x fleet move of 8 instances at +96 dbu each (trial:i03.ug.whole_design.00).

Recipe -- Co-lateral via-and-pad slide:

Step 1. For each violation in this family, locate the VIA_VIA12 instance whose bounding box overlaps or abuts the violation bbox (seed).

Step 2. Determine the required lateral delta. The VIA_VIA12 cell's own M1 land supplies exactly 8 dbu on both y-sides (land y = +/-44 vs cut +/-36) but 0 on x, so on the y-pair BOTH sides supply 8 dbu but neither reaches 20 dbu; the merged M1 at the new location must either lift one y-side to >= 20 dbu, or achieve the x-pair with >= 8 dbu on both sides and >= 20 dbu on at least one (seed). Repairs in this lineage aimed for >= 20 dbu on BOTH x-sides, a conservative working target that exceeds the rule minimum. M1.S.2 and M1.S.6 clear when the via moves away from the neighbor that was causing tip/corner proximity (reference-design-verified).

Step 3. Apply the delta to VIA_VIA12 and verify V0.M1.AUX.3 is cleared. A uniform fleet move of [+96, 0] dbu across 8 via instances produced conn_preserved=true and n_new_in_crop=0 (trial:i03.ug.whole_design.00). Single-instance moves of +136 dbu in x (examples A2, A3) and +68 dbu in y (example A4) were each verified DRC-clean (reference-design-verified).

Step 4. If a VIA_VIA23 is co-located at the same (x, y) (stacked via), decide PER LEVEL -- co-located vias do not always travel together (reference-design-verified):
  (a) COUPLED case: if the M2 landing must move with the V1 fix (the M2 polygon itself is co-moved), move VIA23 by the same delta. Verified: the stacked pair at (5652,5220) both moved +64 in x, together with the associated TOP-LEVEL M2 pad and M3 routing polygons; the vias' own M1/M2 lands travel inside the instances -- no top-level M1 was involved.
  (b) ANCHOR case: if VIA23's own levels (M2-M3) remain correctly aligned at the ORIGINAL coordinate, leave VIA23 in place and move only VIA12. Verified: VIA12 (3204,1980)->(3340,1980) +136 while the co-located VIA23 stayed at (3204,1980) as the M2-M3 anchor.
  (c) PARTIAL case: the two may share one axis and split the other. Verified: at (6228,2340) both took +8 in y, but VIA12 took +36 in x while VIA23 took 0.
  The deciding question: after moving VIA12, does the V2 level at the OLD position still need VIA23 there to reach M3, and does VIA23's own alignment stay legal? If yes to both -> anchor case, leave VIA23 in place. The final clean pair shows this anchor pattern explicitly (reference-design-verified).

Step 5. Re-establish LANDING coverage at the via's NEW position. The via's own M1/M2 lands travel inside the instance; what may need editing are the TOP-LEVEL M2 (layer 20) landing/routing polygons (and M3 for the VIA23 level, Step 6) -- in the reference-design repair ZERO top-level M1 (layer 19) polygons were touched. In trial:i03.ug.whole_design.00, 7 of 8 via moves at +96 dbu in x were each paired with a resize_end on the polygon high-x edge: extension delta was +116 dbu (polygons p2020, p1946, p1903, p1991) or +152 dbu (polygons p2071, p2072, p2086), both larger than the via's +96 dbu move, leaving a 20-56 dbu overhang beyond the new via position. The remaining 2 instances (i0404, i0471) received no dedicated polygon resize, indicating their metal already covered the new position. An isolated landing pad can translate by the same delta; a pad attached to a routing stub is typically end-extended instead, and its delta need not equal the via's (observed: via at (6228,2340) moved (+36,+8) while its M2 pad moved (+92,+8), reference-design-verified).

Step 6. VIA_VIA23 is the M2-M3 via: after any VIA23 move, BOTH levels need coverage (reference-design-verified). If it now falls outside the M2 routing polygon (layer M2), move or extend the M2 polygon to cover it; likewise verify the M3 side still covers the via at its new location (M3 coverage loss is a connectivity break the window DRC does not flag).
  Two modes observed, on whichever affected level (top-level M2 or M3):
  (a) Co-move: the polygon translates by the same delta as the via (observed on both an M2 pad and an M3 routing polygon in worked example A1, reference-design-verified).
  (b) Extend: one edge is stretched to reach the new via position (observed on M2 in example A2 and on M3 in example A4, reference-design-verified).

Worked example A1 (V0.M1.AUX.3 at [5580,5220,5652,5292], reference-design-verified):
  Via at (5652,5220); violation at boundary where V0 width != M1 width.
  Delta: (+64, 0) dbu = 16 nm in +x.
  VIA12 moves (5652,5220)->(5716,5220); VIA23 co-moves same delta.
  M2 landing pad polygon (92x72 dbu, layer 20 = M2) moves (5560,5184)->(5624,5184), same delta (this is VIA23's lower land level / VIA12's upper).
  M3 routing polygon (72x3156 dbu, layer 30 = M3) moves (5616,5184)->(5680,5184), same delta (VIA23's upper level).

Worked example A2 (multi-rule single-move, delta +136 dbu in x, reference-design-verified):
  VIA12 at (3204,1980) moves to (3340,1980).
  This single move clears:
    V0.M1.AUX.3 at [3204,1980,3276,2052]
    V1.M1.EN.1 at [3168,1944,3240,2016]
    M1.S.2 at [3072,1936,3168,2024] -- the marker ends exactly at the old M1
      land's left edge (3168, land y 1936..2024); the +136 move carries the
      land away from the tip-to-side conflict.
  M2 routing polygon (layer 20 = M2, at (2880,1944)-(3240,2016)) extended: right edge from x=3240 to x=3336 (+96 dbu = 24 nm) -- this re-covers the via's M2 land at its new x. NO top-level M1 polygon was edited: the V1.M1.EN.1 side closes because the RELOCATED via's own M1 land merges with the M1 already present at the new position. Enclosure is checked on MERGED metal; enclosure must not be re-derived from any single polygon alone (reference-design-verified).

Worked example A3 (three-rule single-move, delta +136 dbu in x, reference-design-verified):
  VIA12 at (2340,3060) moves to (2476,3060).
  This single move clears:
    V0.M1.AUX.3 at [2340,3060,2412,3132]
    V1.M1.EN.1 at [2304,3024,2376,3096]
    M1.S.2 at [2208,3016,2304,3104]

Worked example A4 (V1.M1.EN.1 + M3 extend, delta (0,+68) dbu, reference-design-verified):
  VIA12 at (5364,5724) moves to (5364,5792); VIA23 co-moves same.
  Clears V1.M1.EN.1 at [5328,5688,5400,5760].
  M3 polygon (layer 30 = M3, at (5328,4896)-(5400,5760)) TOP edge extended from y=5760 to y=5816 to cover the via's M3 level at its new y (VIA23 is M2-M3).

Worked example A5 (M1.S.2 + V1.M1.EN.1 near x=6228, coordinated multi-object, reference-design-verified):
  M2 polygon (92x72 dbu, layer 20 = M2) at (6136,2304) moves to (6228,2312), delta (+92,+8).
  VIA12 at (6228,2340) moves to (6264,2348), delta (+36,+8).
  VIA23 at (6228,2340) moves to (6228,2348), delta (0,+8).
  Clears M1.S.2 at [6120,2296,6192,2384] and V1.M1.EN.1 at [6192,2304,6264,2376].
  Note: VIA12 and VIA23 were co-located (stacked) at (6228,2340) BEFORE the repair; the repair deliberately split them in x (+36 vs 0) while both shared the +8 y-delta -- the PARTIAL case of Step 4(c). Co-location before a repair does not imply co-movement during it.

Worked example A6 (fleet pure-x move, 8 instances, trial:i03.ug.whole_design.00):
  8 via instances (i0536, i0410, i0446, i0361, i0239, i0093, i0015, i0404, i0471) moved by [+96, 0] dbu.
  7 of 8 were paired with a resize_end on a top-level polygon's high-x edge: +116 dbu on polygons p2020, p1946, p1903, p1991; +152 dbu on polygons p2071, p2072, p2086.
  2 instances (i0404, i0471) received no paired resize_end, indicating their covering metal already reached the new position.
  Layers touched: M1, M2, V1. conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0.
  Extension delta (116 or 152 dbu) exceeded via move delta (96 dbu) in all 7 paired cases, leaving a 20-56 dbu overhang beyond the new via center.

Connectivity preservation (Family A): the via's own M1/M2 lands travel with the instance, so the V1 cut stays within its lands (reference-design-verified). Top-level M2 pads/routing are co-moved or end-extended so the via's M2 land stays merged with its net; the VIA23 level likewise keeps M2 and M3 coverage. Via cell definitions are not touched; only instance placements and top-level M2/M3 polygons change.

---


## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference design's initial layout against its repaired final layout, plus the BEFORE and AFTER DRC reports. Every coordinate and delta cited in this document is quoted inline from that pair; the layout files themselves are not needed and are not shipped with this skill.

- Moving via instances without touching cell definitions is sufficient to clear V0.M1.AUX.3, V1.M1.EN.1, M1.S.2, and M1.S.6, provided metal polygons are co-moved or extended to maintain coverage (reference-design-verified).

- A single via move can simultaneously clear violations under 3 different rules (confirmed by example A3: one VIA12 move clears V0.M1.AUX.3, V1.M1.EN.1, and M1.S.2 at once, reference-design-verified).

- A fleet of 8 via instances moved by uniform [+96, 0] dbu, with per-instance polygon resize_end operations at +116 or +152 dbu on the high-x edge, produced conn_preserved=true and n_new_in_crop=0 across the whole design (trial:i03.ug.whole_design.00).


## Case notes

Multi-rule single-fix frequency: in the reference-design block, 3 out of 12 VIA12 moves each cleared violations from 2-3 distinct rules (reference-design-verified). When spatial clustering shows overlapping violation bboxes from different rules at the same location, treat them as one compound fix. A single rule can also double-report one physical site through deck rule variants: the two M1.S.6 markers [6408,3457,6480,3499] and [6405,3464,6483,3492] outline the same corner pair, so marker count can exceed physical site count (reference-design-verified).