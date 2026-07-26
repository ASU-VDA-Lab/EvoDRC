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


## Iteration 2 measured facts

**V4 shape edits in VIA_VIA45_1_2_58_58 via isolated cu_pool trial are ineffective.**
The cu_pool trial trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 attempted to widen V4 shapes
inside cell VIA_VIA45_1_2_58_58 by moving shape_index=0 by +38 dbu in x and
shape_index=1 by -38 dbu in x, each followed by a +76 dbu x-resize, plus a +152 dbu
x-resize of the M4 shape. The result was delta_total=0 (62 violations before, 62 after)
and decision=rejected_net_positive. These five ops produced zero net DRC improvement
for this cell definition.

**Dropped V4 ops in the assembled whole-design batch confirm the same result.**
Trial trial:i02.ug.whole_design.00 was gated_in (decision=gated_in, conn_preserved=true,
18 ops accepted), but all five V4/M4 shape ops targeting VIA_VIA45_1_2_58_58 were
listed in assemble_drops with reason=cu_pool:rejected_net_positive. The accepted batch
moved M5 polygons p1059 and p1060 each by dx=+32 and moved ten VIA45 instances
(varying y-deltas, all dx=+32) and six VIA instances (dx=0, varying y-deltas). No V4
shape edits survived into the assembled commit.

**Isolating V4 shape widening within a via cell definition does not clear spacing or
enclosure violations when the surrounding M4/M5 context is not co-moved.**
The rejected trial trial:i02.cu.def:VIA_VIA45_1_2_58_58.00 operated on the cell
definition in isolation; the M4 resize it included (+152 dbu, shape_index=0) was
insufficient to remove violations without the corresponding M5 stripe x-shift and
VIA45 instance translations that the whole-design trial (trial:i02.ug.whole_design.00)
carries. V4 shape changes must therefore be co-committed with the full M5+VIA45
instance batch, not submitted as a standalone cell-definition patch.

**The accepted whole-design batch (trial:i02.ug.whole_design.00) touches V4 only
indirectly through instance moves, not through shape edits.**
The 18 accepted ops in trial:i02.ug.whole_design.00 are all move_instance or M5
polygon moves; none directly edit a V4 shape. V4 shapes inside VIA_VIA45_1_2_58_58
instances move because their parent instance moves -- they do not receive independent
shape-level edits. This is consistent with the seed observation that no object
add/delete was needed in the reference design repairs.