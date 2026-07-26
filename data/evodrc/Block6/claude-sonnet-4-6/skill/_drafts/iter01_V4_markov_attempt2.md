The two rejected prescriptions need `reference-design-verified` tokens (they are seed-era claims) and the new trial record needs to be folded in. Here is the corrected body:

---

## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity
  (center_y mod 192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves.
  No object add/delete was needed in either of these cases -- a property of
  these repairs, not a universal rule. (reference-design-verified)


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL VIA_VIA45
instances associated with that shifted stripe must be applied as one complete
batch (reference-design-verified). The final diff shows two M5 stripes shifted
-88 dbu in x, and all seven repaired VIA45 instances also take dx=-88.
VIA_VIA34 is NOT part of that x-batch (it keeps x and re-centers in y with the
M4 reshape -- see Family B (-> see M4.md / V3.md) Step 5).
From a local crop, do not submit a partial stripe migration unless the complete
VIA45 target set for that stripe is known (reference-design-verified).

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move.
VIA45 must track both, producing combined deltas such as (-88, -48) or
(-88, +120) (reference-design-verified). Compute the x and y components
separately, then sum.


## Iteration 1 measured facts

**trial:i01.cu.def:VIA_VIA45_1_2_58_58.01** — Block6, cu_pool channel, locus
[1728, 2068, 15336, 15216]. Applied; total violation delta -52 (-28 in
unit:leaf_0019, -24 in unit:leaf_0020). 5 ops on cell VIA_VIA45_1_2_58_58
touching layers V4 and M4:

- V4 shape_index 0: move_via_shape x -116 dbu, then resize_via_shape x +384 dbu.
- V4 shape_index 1: move_via_shape x +116 dbu, then resize_via_shape x +384 dbu.
- M4 shape_index 0: resize_via_shape x +152 dbu.

The two V4 shapes within the cell are moved symmetrically outward (±116 dbu)
and each widened (+384 dbu x) in the same operation set; M4 is widened (+152 dbu
x) alongside them (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). Connectivity is
preserved (conn_preserved: true). No y-axis operations were applied in this
repair; all adjustments were x-axis only (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).

When both V4 shapes in a VIA_VIA45 cell require x-repositioning, the moves are
opposite in sign and equal in magnitude, with resize applied independently to
each shape; the accompanying M4 resize is smaller in magnitude than the V4
resize (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01).