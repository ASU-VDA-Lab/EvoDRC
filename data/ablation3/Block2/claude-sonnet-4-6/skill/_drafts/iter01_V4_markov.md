The record is already provided inline. Composing the updated knowledge body now.

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
  these repairs, not a universal rule.


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

**Cell-definition resize is a valid V4 repair path.**
trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 (decision: applied, conn_preserved:
true) resolved 16 V4-related DRC violations (68 → 52) by resizing V4 shapes
inside the cell definition of VIA_VIA45_1_2_58_58 along the x-axis by +152 dbu.
Both V4 shape_index 0 and shape_index 1 were resized by the identical delta.
The repair does NOT move the cell instance; it modifies the cell master geometry
directly.

**M4 co-resize is mandatory in V4 cell-definition repairs.**
In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 the M4 shape (shape_index 0) inside
the same VIA_VIA45 cell was also resized by +152 dbu on the x-axis as part of
the same atomic op group ("V4M5_fix"). All three ops (V4 shape 0, V4 shape 1,
M4 shape 0) shared the same delta and were committed together. Do not resize V4
cell shapes without resizing the co-located M4 shape by the same delta on the
same axis.

**Both V4 shapes in a VIA_VIA45 cell must be resized together.**
trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 applied the x-axis resize to
shape_index 0 and shape_index 1 on V4 with identical delta (+152 dbu). Resizing
only one of the two V4 shapes would leave the cell geometry inconsistent;
always apply the matching delta to all V4 shapes in the cell master when the
repair targets the cell definition.

**M5 layer appears in touched_layers but receives no explicit resize op.**
In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 "touched_layers" includes M5, yet
the three recorded ops address only V4 (×2) and M4 (×1). M5 is read for
interaction checks (V4.M5.AUX.2, V4.M5.EN.2 enclosure rules) but is not
directly modified by the cell-definition resize. Do not add a spurious M5 op
when reproducing this repair class.

**Cell-definition resize and instance-placement shift are distinct repair
classes; do not conflate them.**
The reference-design tail evidence (seed) describes instance-level x-shifts
applied to VIA45 instances (e.g., dx=-88). trial:i01.cu.def:VIA_VIA45_1_2_58_58.01
describes a cell-master geometry resize (+152 dbu in x) with no instance move.
When the group tag is "V4M5_fix" and the target is a "def:" URI, apply the
resize-cell-master path. When the target is an instance URI and the context is
an M5 stripe shift, apply the instance-placement path from AP-2.