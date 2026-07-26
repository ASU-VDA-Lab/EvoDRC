The inputs are fully embedded in the prompt. I'll compose the output directly from the provided records.

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


## Cell-definition resize of VIA_VIA45 (iteration 1 measured)

V4 violations in units sharing the same VIA_VIA45 cell definition can be resolved
by resizing the V4 shapes inside that cell definition rather than moving
instances. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 the cu_pool channel
applied resize_via_shape ops to both V4 shape_index 0 and shape_index 1 inside
cell VIA_VIA45_1_2_58_58, each with axis=x delta_dbu=+152. The same trial
simultaneously resized the M4 shape_index 0 in the same cell by axis=x
delta_dbu=+152. The result was delta_total=-16 violations, with -8 per
affected unit (leaf_0012 and leaf_0013 each dropped from 27-28 violations to
19-20). This confirms that a single cell-definition edit propagates the fix to
every instantiation simultaneously.

When VIA_VIA45_1_2_58_58 contains two V4 shapes, both must receive the identical
x-delta; a partial resize (only one shape index) would leave one V4 shape
under-sized relative to M5 and re-trigger V4.M5.AUX.2 or V4.W.1. The measured
record trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 shows shape_index 0 and
shape_index 1 both taking +152 with no exception.

The M4 shape inside the same cell takes the same axis=x delta as the V4 shapes
(trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, M4 shape_index 0 delta_dbu=+152).
This is the intra-cell expression of the broader M4/V4 coupling documented in
the seed evidence above; the delta magnitude need not match the stripe-level M5
x-shift and in this case it does not (-88 dbu at stripe level vs. +152 dbu at
cell level).


## cu_pool vs. unit_gate ordering and assemble_drops

The cu_pool channel applies cell-definition resizes before unit_gate instance
moves are assembled. In trial:i01.ug.leaf_0012.07 (unit_gate, gated_in), the
assemble_drops list records the three VIA_VIA45_1_2_58_58 resize ops with
reason="cu_pool:applied", confirming they were already committed by
trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and must not be re-applied by the
unit_gate path. Any unit_gate trial operating on a locus that overlaps an
already-applied cu_pool cell edit must treat those shape ops as absorbed; do not
double-count or re-issue them.

trial:i01.ug.leaf_0012.07 was gated_in (not applied) despite conn_preserved=true
because it introduced 2 new V1.M1.EN.1 violations in-crop. V4 is listed in
touched_layers for that trial (instance moves on i0097, i0092 at dy=-48 and
i0064, i0072 at dy=+96), so asymmetric y-moves across the via stack can expose
M1 enclosure violations even when V4 itself is the repair target layer. When
evaluating a candidate move_instance set that touches V4, verify the full
touched_layers stack (M3, M4, M5, V3, V4 in this case) for downstream rule
interactions before committing.