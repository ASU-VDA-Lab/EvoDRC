## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height
  normalization to the V3 height, track parity (center_y mod 192 == 48,
  M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed
  in either of these cases -- a property of these repairs, not a universal
  rule.


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven
repaired VIA45 instances also take dx=-88. VIA_VIA34 is NOT part of that x-batch
(it keeps x and re-centers in y with the M4 reshape -- see Family B (-> see M4.md / V3.md) Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
VIA45 target set for that stripe is known.

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. VIA45
must track both, producing combined deltas such as (-88, -48) or (-88, +120).
Compute the x and y components separately, then sum.


## Iteration 1 measured facts

### V4 intra-cell move+resize pattern (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01)

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (Block3, cu_pool channel, locus [1728, 2068, 11016, 10892]), five ops were applied to cell VIA_VIA45_1_2_58_58 and the repair was accepted (decision: applied), reducing DRC-window error counts by 10 in unit:leaf_0018 (32→22) and by 8 in unit:leaf_0019 (35→27), for a total delta of -18. Connectivity was preserved throughout (conn_preserved: true).

The five ops break into three groups:

1. **V4 shape_index=0**: move x by -116 dbu, then resize x by +384 dbu. Net effect: the shape's left edge shifts -116 dbu while its right edge shifts -116+384 = +268 dbu, expanding the shape to the right and re-centering it leftward.

2. **V4 shape_index=1**: move x by +116 dbu, then resize x by +384 dbu. Net effect: the shape's left edge shifts +116 dbu and its right edge shifts +116+384 = +500 dbu, expanding the shape to the right and pulling the left edge inward.

3. **M4 shape_index=0**: resize x by +152 dbu, widening M4 in x to accommodate the expanded V4 footprint and maintain V4.AUX.1 (V4 must be inside M4 & M5) and V4.M4.EN.1 (minimum 11 nm enclosure on two opposite sides).

The two V4 shapes are moved in opposite x directions (−116, +116) -- symmetric divergence -- before both receive the same +384 resize. This pattern simultaneously increases the x-extent of each V4 shape (addressing V4.W.1 or V4.M4.EN.1 / V4.M5.EN.2 enclosure shortfalls) while moving the shapes apart from each other (addressing V4.S.1 / V4.S.2 / V4.S.3 spacing violations). The accompanying M4 x-resize (+152) is smaller than the V4 x-resize (+384) per shape, consistent with M4 needing only to cover the outer envelope of the repositioned V4 pair rather than tracking each V4 shape individually (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

Do not apply the V4 move or resize in isolation: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 shows all five ops were submitted together and accepted as a unit. Partial application (e.g., move without resize, or V4 ops without the M4 resize) risks leaving V4.AUX.1 or V4.M4.EN.1 violations open.

When a VIA_VIA45 cell contains two V4 shapes, treat the repair as a symmetric diverge-and-expand: compute the move magnitude for spacing relief, apply it with opposite sign to each shape, then apply an equal resize to both shapes for enclosure/width relief, and widen M4 by the net outer-envelope growth needed to maintain enclosure (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).