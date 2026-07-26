Working from the inline data provided. Writing the knowledge section now.

---

## Effective repair strategies observed

Both recorded trials for V1 were accepted with `decision: gated_in`, `conn_preserved: true`, and zero net new violations (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`), establishing that all described operation patterns are confirmed-effective for this layer.

---

## V1.M2.EN.2 — M2 end-cap enclosure repair

V1.M2.EN.2 requires M2 to enclose V1 by at least 5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm along each projection axis). When the M2 end-cap on the high-x side is too short, the confirmed repair is to extend the M2 polygon's high-x end while simultaneously moving the V1 instance in the same direction to preserve M2 width matching required by V1.M2.AUX.2.

In trial:i03.ug.whole_design.00, this was applied to eight distinct M2 polygons (p2071, p2020, p2072, p2086, p1946, p1903, p1991) using `resize_end(axis=x, end=high)` with deltas of either 116 dbu or 152 dbu, paired with `move_instance(+96 dbu, x)` on the co-located V1-bearing instances (i0536, i0410, i0446, i0361, i0239, i0093, i0015, i0404, i0471). The net end-cap gain on the M2 side past the via is the difference between the polygon extension and the instance shift (116 − 96 = 20 dbu = 2 nm; 152 − 96 = 56 dbu ≈ 5.6 nm). The fact that a 20 dbu net gain (2 nm) closed the violation while the via was also translated indicates that the violation was marginal and the combined effect of more M2 material plus re-centering the via brought both sides of the enclosure into compliance simultaneously.

Do not extend M2 on one end in isolation without moving the associated V1 instance by a matching or smaller offset: doing so risks violating V1.M2.AUX.2 (V1 must exactly match M2 width perpendicular to M2 length) if the via is no longer flush with the shifted M2 boundary.

---

## V1.M2.AUX.2 — width matching constraint governs all M2 edits

V1.M2.AUX.2 requires that V1's dimension perpendicular to the M2 run direction exactly equals the M2 width at that location. This means that any symmetric resize of the M2 polygon along the axis perpendicular to the M2 run direction must be accompanied by an equivalent resize or replacement of the V1 instance.

In trial:i04.ug.whole_design.00, symmetric `resize(axis=x, delta=+10 dbu)` operations on polygons p1990, p1923, and p1920 were each accepted with no new V1.M2.AUX.2 violations. These 10 dbu (1 nm) expansions stayed within compliance because the resize was symmetric (both x edges moved outward equally) and the M1 enclosure (V1.M1.EN.1) was not violated, as confirmed by the trial's clean acceptance.

---

## V1.AUX.1 and V1.M1.EN.1 — M1 enclosure must follow all V1 translations

V1.AUX.1 requires V1 to lie inside both M1 and M2. V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on two opposite sides (minimum 2 nm on the other pair). Both rules fire if V1 is translated without the surrounding M1 polygon tracking the move.

In trial:i03.ug.whole_design.00, every `move_instance` operation that shifted a V1-containing instance was accompanied by modifications to both M1 and M2 polygons in the same op list, and the trial accepted cleanly. The touched-layers field confirms M1, M2, and V1 were all adjusted together (trial:i03.ug.whole_design.00). Do not move a V1 instance without verifying that the M1 polygon it sits inside is either also translated or large enough to maintain the 5 & 2 nm enclosure after the shift.

In trial:i04.ug.whole_design.00, a subset of instances (i0112, i0152) were moved −96 dbu in x while others (i0319, i0213) were moved +96 dbu in x, with no new V1.AUX.1 or V1.M1.EN.1 violations, indicating that the underlying M1 footprints at those locations already provided sufficient margin for a 96 dbu shift in either direction.

---

## V1.S.1 — spacing repairs via whole-polygon translation

V1.S.1 enforces minimum projection spacing between V1 instances (18 nm same track, 27 nm parallel unaligned, 18 nm parallel aligned), evaluated on the derived v1_mask geometry which extends M2 end-caps by 5 nm into the inter-via gap. Spacing violations are therefore sensitive to the M2 end geometry, not just the bare V1 footprint.

In trial:i04.ug.whole_design.00, the M2 polygon p1684 was moved +80 dbu in x as a whole (`op: move`), and ten associated instances (i0025, i0040, i0108, i0126, i0409, i0412, i0530, i0031, i0538 at +80 dbu, and i0015, i0471 at −48 dbu) were repositioned in the same trial. This compound translation — moving M2 and its via instances together while adjusting neighbor instances in the opposite direction — resolved spacing conflicts without introducing new violations. The asymmetric shift of i0015 and i0471 (−48 dbu rather than +80 dbu) indicates that relaxing one via-to-via gap is balanced against tightening another; the solver chose values that kept all spacings above the 18 nm / 27 nm thresholds.

When a V1.S.1 violation exists between two specific instances, moving the M2 wire and its hosted V1 together (rigid body translation) is preferred over resizing the via or adjusting only one endpoint, as confirmed in trial:i04.ug.whole_design.00.

---

## Operation sizing reference (confirmed values)

From trial:i03.ug.whole_design.00 and trial:i04.ug.whole_design.00, the following move deltas were used and accepted:

- **+96 dbu** instance moves (x): used in both i03 and i04 for standard via re-centering after M2 end extension.
- **−96 dbu** instance moves (x): used in i04 for instances i0112, i0152 moving toward lower x.
- **+80 dbu** polygon and instance moves (x): used in i04 for rigid-body track relocation of p1684 and associated instances.
- **−48 dbu** instance moves (x): used in i04 for i0015, i0471 as counter-correction after a conflicting neighbor shifted +80 dbu.
- **+116 dbu, +152 dbu** resize_end(x-high) on M2 polygons: used in i03 for end-cap extension.
- **+10 dbu** symmetric resize(x) on M1/M2 polygons: used in i04 for marginal enclosure correction.

All of these values were confirmed clean by the respective trial acceptances.

---

## GEOMETRY.NONORTHOGONAL constraint

The nonorthogonal block applies to V1: all V1 edges must have angles of exactly 0° or 90°. Neither recorded trial introduced diagonal edges; all resize and move operations were constrained to orthogonal axes (axis=x only, with signed integer dbu deltas), confirming that axis-aligned moves and end-resizes do not risk this violation (trial:i03.ug.whole_design.00, trial:i04.ug.whole_design.00).