## Final-pair measured facts (reference-design tail evidence)

Provenance: these facts come from the final-pair comparison of the reference
design's initial layout against its repaired final layout, plus the BEFORE and
AFTER DRC reports. Every coordinate and delta cited in this document is quoted
inline from that pair; the layout files themselves are not needed and are not
shipped with this skill.

- M5.AUX.1 is resolved by coordinate snapping (x-shift of the stripe), with the
  M5.AUX.2 track parity (center_x mod 192 == 48) picking the snap direction.
  The M4 grid fixes are NOT mere snapping: they combine y-edge snapping
  (M4.AUX.1), height normalization to the V3 height, track parity (center_y mod
  192 == 48, M4.AUX.2), and the coupled VIA34/VIA45 moves. No object add/delete
  was needed in either of these cases -- a property of these repairs, not a
  universal rule.


## Case notes (reference-design tail evidence)

Anti-pattern AP-2 (atomic stripe batch): an M5 stripe x-shift and ALL V4
instances associated with that shifted stripe must be applied as one complete
batch. The final diff shows two M5 stripes shifted -88 dbu in x, and all seven
repaired V4 instances also take dx=-88. Trial i04.ug.leaf_0002.01 independently
confirms this: M5 polygon p1341 shifts +32 dbu in x, and all five associated V4
instances (i0239, i0223, i0141, i0150, i0138) also take dx=+32. Do not submit a
partial stripe migration unless the complete V4 target set for that stripe is
known.

V4 instances track both x and y independently, then sum the components.
In trial i04.ug.leaf_0002.01, the x-component (+32) comes from the M5 stripe
shift and is uniform across all five V4 instances; the y-components (+72, +24,
-24, +24, -24) come from the M4 y-reshape and differ per instance. Compute the x
and y components separately, then sum: the resulting per-instance deltas are
[+32,+72], [+32,+24], [+32,-24], [+32,+24], [+32,-24].

V3/VIA34 instances are NOT part of the M5 x-batch. In trial i04.ug.leaf_0002.01,
five additional instances (i0237, i0214, i0103, i0104, i0134) carry dx=0 with
the same y-deltas (+72, +24, -24, +24, -24) as their V4 counterparts. This
confirms that VIA34 tracks only the M4 y-reshape, never the M5 x-shift; the
dx=0 group is a reliable membership signal for the VIA34 tier.

M5 and M4 are tightly coupled: M5.AUX.1 drives M5 x-shift. That shift forces
V4 x-move. V4 x-move forces a top-level M4 x-extent adjustment (to keep the
MERGED M4 valid around V4). M4.AUX.1 independently forces M4 y-move. V4 must
track both, producing combined deltas such as (-88, -48), (-88, +120), or
(+32, +72) as measured in trial i04.ug.leaf_0002.01.