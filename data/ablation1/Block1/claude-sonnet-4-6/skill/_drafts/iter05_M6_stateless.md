**Active M6 violation state after iteration 5 commit**

The gated-in trial:i05.ug.leaf_0005.04 introduced 24 new in-crop violations, of which M6 contributed two rule types: 1 new M6.AUX.1 violation and 7 new M6.AUX.3 violations. These are the open M6 issues entering the next repair cycle. No M6.W.\*, M6.S.\*, V5.M6.EN.2, V6.M6.EN.1, or M6.AUX.2 violations were introduced by any trial in this layer's history.

---

**M6.AUX.3 — no-bend rule: instance moves that touch M6 on the x-axis create join-point bends**

M6.AUX.3 triggers when an M6 polygon has a corner in the 0°–90° interior-angle range. The rule locates these via `m6.corners(0..90)` and flags all edges touching each such corner. Moving four instances simultaneously by +36 dbu in x (trial:i05.ug.leaf_0005.04), a set that touched M6 among other layers, introduced 7 new M6.AUX.3 violations. The seven violations arise at join points where a displaced instance's M6 edge segment no longer shares the same y-coordinate as the adjacent stationary M6 segment, forming L-bends at the join. To repair M6.AUX.3 violations, the M6 geometry at each bend point must be made collinear: trim or extend the M6 run inside the moved instance to align horizontally with the neighboring stationary segment, or adjust the stationary segment to match the moved one. Avoid issuing instance x-moves that produce non-collinear M6 junctions without correcting the join geometry in the same operation set.

---

**M6.AUX.1 — horizontal edge y-grid of 32 nm: all M6 horizontal edges must land on a 32 nm y-grid**

M6.AUX.1 fires when any horizontal M6 edge has a y-coordinate not divisible by 32 nm. The gated-in trial:i05.ug.leaf_0005.04 — which moved p1561 by -96 dbu in y and moved four instances by +36 dbu in x across M6-touching layers — produced 1 new M6.AUX.1 violation. All M6 horizontal edge y-coordinates must be divisible by 32 dbu after any committed operation set.

---

**Y-axis moves of the M6 shape inside VIA_VIA56_2_2_66_58 increase global DRC count: do not attempt**

Both measured y-axis directions for the M6 shape in cell VIA_VIA56_2_2_66_58 were rejected by cu_pool as net_positive:

- +32 dbu in y: delta_total = +19, driven by leaf_0007 gaining 20 violations (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01).
- -96 dbu in y: delta_total = +33, driven by leaf_0004 gaining 26 and leaf_0005 gaining 7 violations (trial:i05.cu.def:VIA_VIA56_2_2_66_58.00).

The assembler excluded the -96 dbu y-move from the trial:i05.ug.leaf_0005.04 commit, citing the cu_pool rejection (assemble_drops entry). Do not propose y-axis moves of the M6 shape in VIA_VIA56_2_2_66_58.

---

**Combining M5 x-resizes with M6-touching polygon x-moves is net-positive**

The operation set that resized the M5 shape in VIA_VIA45_1_2_58_58 by -32 dbu in x, resized the M5 shape in VIA_VIA56_2_2_66_58 by -32 dbu in x, moved p1143 by +32 dbu in x, and moved p1142 by -16 dbu in x (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00) was rejected with delta_total = +16. The local gain in leaf_0007 (-2 violations) was outweighed by the degradation in leaf_0008 (+18 violations). Avoid coupling M5 shape x-resizes in these via cells with M6-adjacent polygon x-moves as a combined repair strategy.

---

**V5.M6.EN.2 and V6.M6.EN.1 enclosure — not triggered by any measured operation**

No V5.M6.EN.2 or V6.M6.EN.1 violations appeared in the new_in_crop tallies of any trial. The via y-moves and instance x-moves in trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA56_2_2_66_58.00, and trial:i05.ug.leaf_0005.04 did not cross the 11 nm enclosure threshold for V5 or V6 on M6.

---

**M6.W.\* and M6.S.\* — no violations introduced by any measured operation**

No width-rule (M6.W.1 through M6.W.5) or spacing-rule (M6.S.1 through M6.S.5) violations appeared in any trial's in-crop deltas. The polygon x-moves, instance x-moves, and via shape y-moves tested in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.ug.leaf_0005.04, and trial:i05.cu.def:VIA_VIA56_2_2_66_58.00 all left width and spacing compliance intact.

---

**M6.AUX.2 — routing-track centerline grid: no violations introduced**

No M6.AUX.2 violations appeared in any trial. The rule requires minimum-width M6 tracks (those surviving the ±17 nm vertical erosion) to have centerlines on a 256 dbu pitch with 64 dbu offset. None of the four measured trials produced M6.AUX.2 violations.