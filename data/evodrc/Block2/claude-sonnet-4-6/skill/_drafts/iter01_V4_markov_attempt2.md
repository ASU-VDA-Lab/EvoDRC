Looking at the rejection reasons, I need to either add trial citations to the two prescriptive claims or remove them. Let me check what the new records actually support before rewriting.

The new records provide:
- `i01.cu.def:VIA_VIA45_1_2_58_58.01`: resize_via_shape on both V4 shapes and M4 shape simultaneously (n_ops=3, x-axis delta_dbu=152, cu_pool:applied)
- `i01.ug.leaf_0012.07`: move_instance on 4 instances with [0,-48]/[0,96] deltas, gated_in, touching M3/M4/M5/V3/V4

The "all instances on a stripe" batch claim and the specific "(-88,-48) or (-88,+120)" combined-delta claims have no trial-id support in any record. I'll rephrase to what is measurably grounded.

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
  (M4.AUX.1), height
  normalization to the V3 height, track parity (center_y mod 192 == 48,
  M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete was needed
  in either of these cases -- a property of these repairs, not a universal
  rule. (seed, reference-design-verified)


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (partial stripe migration): the final diff shows two M5 stripes
shifted -88 dbu in x, and all seven repaired VIA45 instances in those stripes
also took dx=-88. VIA_VIA34 is NOT part of that x-batch (it keeps x and
re-centers in y with the M4 reshape -- see Family B Step 5). (seed, reference-design-verified)

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
VIA45 x-move. VIA45 x-move forces a top-level M4 x-extent adjustment (to keep
the MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. Compute
the x and y components of any VIA45 displacement separately before summing.
(seed, reference-design-verified)


## VIA_VIA45 cell-definition resize (V4 layer)

In trial i01.cu.def:VIA_VIA45_1_2_58_58.01, a cu_pool:applied decision resized the
VIA_VIA45_1_2_58_58 cell definition: both V4 shapes (shape_index 0 and 1) and the
M4 shape (shape_index 0) each received delta_dbu=152 on the x-axis in a single
3-op batch; touched_layers were M4, M5, V4. The V4 resize and M4 resize inside
the same VIA45 cell definition were applied together, not split across separate
cu_pool submissions.

The same trial i01.cu.def:VIA_VIA45_1_2_58_58.01 records delta_dbu=152 on the x-axis
for both V4 shape indices (0 and 1) within VIA_VIA45_1_2_58_58. This is the only
measured x-axis resize for a VIA45 cell definition in this iteration; no y-axis
resize of a VIA45 cell definition appears in these records.


## Instance-move interactions touching V4

In trial i01.ug.leaf_0012.07, four move_instance operations were issued:
i0097 and i0092 each moved [0, -48] dbu; i0064 and i0072 each moved [0, +96] dbu.
The operation touched layers M3, M4, M5, V3, V4. The decision was gated_in
(not directly applied to the design): it introduced 2 new V1.M1.EN.1 violations
inside the crop window (n_new_in_crop=2) while producing no new out-of-crop
bounding-box excursions; connectivity was preserved (conn_preserved=true).
The assemble_drops for that trial include the cu_pool:applied ops from
i01.cu.def:VIA_VIA45_1_2_58_58.01 (x-axis resizes) plus y-axis resizes on M3
shapes (p962--p965, delta_dbu=-64 each) and a y-axis resize on a VIA_VIA23
M3 shape (delta_dbu=-40).