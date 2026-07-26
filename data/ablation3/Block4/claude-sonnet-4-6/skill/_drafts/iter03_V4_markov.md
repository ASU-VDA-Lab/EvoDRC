(seed, reference-design-verified)
<!-- migrated from repair_skill_v0.md (md5 4c50681f3667b5cf80cd134b67b23d8e) by migrate_seed_v0.py; family slice(s): none (tail evidence only) -->


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


## Cell-definition resize (iteration 3 measured)

Trial trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 demonstrates that V4 violations can be resolved by resizing shapes inside the VIA_VIA45 cell definition rather than by moving cell instances. In that trial the fix targeted `def:VIA_VIA45_1_2_58_58`: both V4 shapes (shape_index 0 and 1) were widened by +152 dbu on the x-axis, and the M4 shape (shape_index 0) in the same cell was widened by the same +152 dbu on the x-axis. All three ops shared the identical delta and axis (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, n_ops=3). The fix reduced whole-design violations from 89 to 61 (delta_total -28) and preserved connectivity (conn_preserved=true).

Apply the same delta to every V4 shape and the enclosing M4 shape inside the cell definition when resizing a VIA_VIA45 cell for V4.W.1 relief; mismatched deltas between V4 and M4 shapes inside the same cell definition violate V4.M4.EN.1 enclosure (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). Because V4.M5.AUX.2 requires V4 width to exactly match M5 width perpendicular to the M5 run direction, verify that the x-axis resize delta is consistent with the M5 stripe width already in place before committing the cell-definition edit (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

Cell-definition edits propagate to every instance of that cell across the full design. The locus for trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 covers the whole design (0,0)-(14672,14672), and touched_layers includes M5 even though no M5 op appears in the op list, confirming that M5 interaction is evaluated globally after the cell-def change. Do not apply a cell-definition resize when only a subset of that cell's instances require the fix; instance-level ops must be used in that case.