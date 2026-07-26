## V3 Layer DRC Repair Knowledge — Iteration 2

### Summary of measured evidence

One accepted trial exists for this layer at iteration 2: trial:i02.ug.whole_design.00 (Block2, whole_design unit, gated_in, conn_preserved). That trial touched layers M1, M2, M3, M4, M5, V1, V2, V3, V4 and applied 45 ops: x-axis moves and resize_end operations on V3 polygons p937, p938, p958–p965 alongside coordinated instance moves for M3/M4 cells.

---

### V3.W.1 — Minimum width 18 nm along M4 length

V3 width along the M4-length axis must be at least 18 nm. In trial:i02.ug.whole_design.00, resize_end operations on V3 polygons (e.g., p958–p965, all axis=x end=high) extended the high x-edge by 32 dbu while the corresponding instance groups were moved by [32,0]. Applying resize_end only to the trailing edge while the leading edge moves with the instance preserves the absolute x-span of each V3 shape; do not shrink the x-dimension of a V3 polygon when co-moving it with an M4 instance, as doing so risks violating the 18 nm floor (trial:i02.ug.whole_design.00).

---

### V3.S.1 — Minimum projection spacing between V3 instances

The rule enforces three spacing regimes: 18 nm on the same M4 track, 27 nm between parallel tracks not aligned, and 18 nm between parallel tracks aligned. The mask geometry distinguishes "full-flush" (NEC) from "with-end-cap" (WEC) V3 instances and applies 5 nm extensions before checking projection spacing.

In trial:i02.ug.whole_design.00, V3 polygons were moved with x-deltas of +32 dbu alongside their owning M4 instance groups, and y-positions were adjusted in discrete steps (±48, ±72, ±96 dbu) for different instance clusters. The trial was accepted (gated_in) with conn_preserved, confirming that co-moving V3 with its M4 host by identical x/y deltas does not open new S.1 violations provided the inter-V3 spacing on the M4 track is unchanged (trial:i02.ug.whole_design.00). When moving a group of V3 instances on the same track, apply the same delta to all members of that track group; partial moves that close the intra-track gap below 18 nm will trigger S.1 (trial:i02.ug.whole_design.00).

---

### V3.S.2 — Corner-to-corner spacing 23 nm (both with 5 nm M4 end-cap)

The euclidean check fires when a corner-to-corner distance between two WEC V3 instances (both carrying a 5 nm M4 end-cap extension) falls below 23 nm, provided no projection violation is already flagged for that pair. In trial:i02.ug.whole_design.00, the y-offset increments used for adjacent instance clusters (48, 72 dbu) are large relative to the 23 nm threshold, and the trial passed without S.2 violations. Maintain y-separations between WEC V3 clusters at the coarse grid steps used in that trial; finer y-compressions that bring corners closer than 23 nm will trigger S.2 (trial:i02.ug.whole_design.00).

---

### V3.S.3 — Corner-to-corner spacing 30 nm (both without 5 nm M4 end-cap)

For NEC V3 pairs (both flush with M4, no end-cap), the euclidean corner-to-corner minimum is 30 nm after the 5 nm symmetric sizing. In trial:i02.ug.whole_design.00, NEC V3 polygons were moved in the same x-direction as their M4 hosts with no independent y-compression, keeping diagonal neighbors at the same relative separation. Do not reduce the y-pitch of NEC V3 instances relative to their M4 track pitch when fixing x-direction violations; the 30 nm diagonal clearance is the binding constraint for NEC–NEC pairs (trial:i02.ug.whole_design.00).

---

### V3.S.4 — Corner-to-corner spacing 27 nm (mixed WEC/NEC pair)

When one V3 is WEC and the other NEC, the euclidean corner-to-corner minimum is 27 nm. The asymmetry (17.11 nm euclidean check against the WEC mask separated from the NEC mask) means the binding corner is the WEC end-cap extension. In trial:i02.ug.whole_design.00, moves that adjusted y-position by ±72 or ±48 dbu for mixed-type neighbor groups were accepted without S.4 errors, confirming those separations clear the 27 nm bound (trial:i02.ug.whole_design.00). When resolving S.1 by moving a WEC V3 along x, verify that the resulting diagonal to any NEC neighbor does not close below 27 nm (trial:i02.ug.whole_design.00).

---

### V3.M3.EN.1 — M3 must enclose V3 by ≥5 nm on at least two opposite sides

A V3 shape fails this rule if it is not covered with 5 nm margin on both the left+right pair or both the top+bottom pair by M3. In trial:i02.ug.whole_design.00, M3 was among the touched layers and M3 instance groups were co-moved with V3 polygons using identical x-deltas ([32,0] for the main cluster). Co-moving V3 and M3 by the same vector preserves the enclosure margin on both axes; moving V3 without also moving the enclosing M3 shape will erode the enclosure and trigger EN.1 (trial:i02.ug.whole_design.00). The two resize_end operations on p1065 (x +116 dbu) and p1036 (x +80 dbu) at the end of the trial extended M3/M4 shapes beyond the V3 move delta, which is consistent with maintaining or increasing the x-direction enclosure margin (trial:i02.ug.whole_design.00).

---

### V3.M4.EN.2 — M4 must enclose V3 by ≥11 nm on at least two opposite sides

M4 enclosure is checked symmetrically: V3 must sit at least 11 nm inside the M4 boundary on both left+right or both top+bottom. In trial:i02.ug.whole_design.00, M4 instance moves and V3 polygon moves used the same x-delta (+32 dbu), keeping the x-direction enclosure unchanged. The larger resize_end values on p1065 (+116 dbu) and p1036 (+80 dbu) extend the M4 end beyond the V3 trailing edge, ensuring the 11 nm margin is not lost at the high-x end after the move (trial:i02.ug.whole_design.00). When moving V3 in x, extend the high-x end of the enclosing M4 shape by at least the V3 move delta to preserve the 11 nm enclosure; do not move V3 alone without a corresponding M4 adjustment (trial:i02.ug.whole_design.00).

---

### V3.AUX.1 — V3 must be inside both M3 and M4

V3 must be entirely contained within the intersection of M3 and M4. In trial:i02.ug.whole_design.00, V3 polygon moves and M3/M4 instance moves were applied with matching x-deltas, and the trial was accepted with conn_preserved, confirming containment was maintained (trial:i02.ug.whole_design.00). Moving a V3 polygon without simultaneously moving or extending the M3 and M4 shapes that contain it will cause V3 to exit the M3∩M4 region and trigger AUX.1; always co-move the enclosing M3 and M4 geometry when translating a V3 shape (trial:i02.ug.whole_design.00).

---

### V3.M4.AUX.2 — V3 must exactly match M4 width perpendicular to M4 length

V3 must span the full width of M4 in the direction perpendicular to the M4 wire, with exactly two coincident edges shared with M4. In trial:i02.ug.whole_design.00, V3 polygon resize_end operations on the x-axis (p958–p965 each extended by +32 dbu high-x end) were paired with M4 instance moves of [32,0], preserving the exact width match between V3 and M4 in the perpendicular direction (trial:i02.ug.whole_design.00). Do not apply an independent resize to the V3 perpendicular dimension; any change in M4 width in that direction must be mirrored exactly by a corresponding V3 resize, and any translation of V3 must be accompanied by the same translation of the enclosing M4 instance to keep the two coincident edges aligned (trial:i02.ug.whole_design.00).

---

### Interaction notes

The ops pattern in trial:i02.ug.whole_design.00 shows that V3, M3, and M4 must be treated as a coupled unit during any x-direction move: V3 polygon move + V3 resize_end + M4 instance move at the same delta, with larger resize_end on the M3/M4 boundary shapes to preserve both EN.1 and EN.2 margins. Decoupling any of these three components produces violations across AUX.1, M4.AUX.2, M3.EN.1, and M4.EN.2 simultaneously (trial:i02.ug.whole_design.00).