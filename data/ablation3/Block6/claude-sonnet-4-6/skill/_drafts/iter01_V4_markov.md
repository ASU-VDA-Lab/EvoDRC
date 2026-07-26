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

**V4 violations are resolved by M5 y-axis resize within VIA_VIA45 cells.**
In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a `resize_via_shape` op on the M5
layer (axis y, delta_dbu -88) inside cell VIA_VIA45_1_2_58_58 reduced the
whole-design DRC count by 56 (before 247, after 191). Touched layers were M4,
M5, and V4; connection was preserved. This confirms that M5 shape extent in the
y-direction inside a VIA_VIA45 cell directly governs V4 enclosure and width
compliance (rules V4.M5.EN.2, V4.M5.AUX.2, V4.W.1).

**The repair axis for M5-driven V4 violations is y, not x, inside VIA_VIA45 cells.**
The single op in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 uses axis y with
delta -88 dbu on M5; no x-component was required. Do not conflate this with the
x-shift anti-pattern AP-2 (stripe-level x-batch from the seed): that pattern
applies to M5 stripe x-relocations at the top level, whereas this repair is a
y-resize of the M5 shape internal to a VIA_VIA45 subcell.

**A single resize_via_shape op is sufficient when the violation is isolated to
one VIA_VIA45 instance.** trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 records
n_ops=1 with decision=applied and conn_preserved=true, yielding a net delta of
-56 violations. No secondary moves on M4 or V4 shapes were required in this
case, distinguishing it from the seed's coupled-delta pattern where M4 y-move
and VIA45 x+y combined deltas were both needed.