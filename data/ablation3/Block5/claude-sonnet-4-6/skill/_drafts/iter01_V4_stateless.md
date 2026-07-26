## Summary of Available Evidence

The layer V4 repair history contains exactly one completed trial: trial:i01.ug.whole_design.00 (Block5, whole-design unit, channel unit_gate, iteration 1). That trial was accepted with decision gated_in, reason conn_preserved, and zero new violations introduced in or out of the crop region (n_new_in_crop: 0, n_new_out_of_crop: 0). V4 is one of nine touched layers (M1–M5, V1–V4). All claims below are grounded solely in that record.

---

## Operation Mix

The accepted repair used 19 operations: 16 move_instance ops and 3 direct polygon edits (trial:i01.ug.whole_design.00). The polygon edits targeted two polygons:

- **p879**: high-Y end extended by +48 dbu (resize_end, axis y, end high).
- **p910**: translated +8 dbu along X (move, axis x), then high-Y end extended by +20 dbu (resize_end, axis y, end high).

No low-end resizes, X-axis resizes, or polygon deletions appeared in this repair (trial:i01.ug.whole_design.00).

---

## Instance Move Displacements

All 16 instance moves in trial:i01.ug.whole_design.00 are listed below with their axes and magnitudes:

| Instance | Axis | Delta (dbu) |
|----------|------|-------------|
| i0012 | X | +136 |
| i0103 | X | −28 |
| i0113 | Y | +72 |
| i0099 | Y | +72 |
| i0112 | Y | −48 |
| i0105 | Y | −48 |
| i0001 | Y | +24 |
| i0002 | Y | +24 |
| i0073 | Y | +96 |
| i0075 | Y | +96 |
| i0067 | Y | −24 |
| i0070 | Y | −24 |
| i0062 | Y | +48 |
| i0076 | Y | +48 |
| i0061 | X | +8 |
| i0104 | X | +8 |

Y-axis displacements ranged from −48 to +96 dbu; X-axis displacements ranged from −28 to +136 dbu. Several instances were moved in coordinated pairs sharing identical displacement vectors: (i0113, i0099) at +72 Y, (i0112, i0105) at −48 Y, (i0001, i0002) at +24 Y, (i0073, i0075) at +96 Y, (i0067, i0070) at −24 Y, (i0062, i0076) at +48 Y, and (i0061, i0104) at +8 X (trial:i01.ug.whole_design.00). Moving a logically coupled pair with the same vector preserves their relative geometry and is the pattern used in the only repair that was accepted.

---

## Connectivity Outcome

The trial was accepted under the conn_preserved condition. All 16 instance moves and both polygon end-extensions in trial:i01.ug.whole_design.00 left routing connectivity intact across M1–M5 and V1–V4. The largest single-instance Y displacement used was 96 dbu (i0073, i0075) and the largest X displacement was 136 dbu (i0012); these magnitudes did not break connectivity in this block configuration (trial:i01.ug.whole_design.00).

---

## No-New-Violation Outcome

The repair introduced zero new violations in-crop and zero new violations out-of-crop (trial:i01.ug.whole_design.00). The combination of pair-coordinated instance moves and high-end polygon extension on p879 and p910 achieved this without adding V4.W.1, V4.S.1, V4.S.2, V4.S.3, V4.M4.EN.1, V4.M5.EN.2, V4.AUX.1, or V4.M5.AUX.2 violations elsewhere in the design.

---

## Polygon End Extension Direction

Both direct polygon edits in the accepted repair grew the high-Y end of the target polygon (p879: +48 dbu; p910: +20 dbu) rather than shrinking or moving the low end (trial:i01.ug.whole_design.00). Neither edit caused a new violation. Do not apply low-end shrinks or X-axis resizes to V4-adjacent polygons without additional measured evidence, as no such operation appears in any accepted trial.

---

## Rule-Specific Constraints (for Reference During Repair)

The following minimum dimensions are enforced by the DRC deck and must not be violated when placing or resizing V4 shapes:

- **V4.W.1**: minimum via width 24 nm along M5 length direction.
- **V4.S.1 / V4.S.2 / V4.S.3**: minimum spacing 33 nm between any two V4 instances (same net projection, different net projection, and corner-to-corner euclidean).
- **V4.M4.EN.1**: M4 must enclose V4 by at least 11 nm on at least two opposite sides.
- **V4.M5.EN.2**: M5 must enclose V4 by at least 11 nm on two opposite sides.
- **V4.AUX.1**: every V4 shape must lie fully inside both M4 and M5.
- **V4.M5.AUX.2**: V4 width in the direction perpendicular to M5 length must exactly equal the M5 width at that location.

These thresholds bound acceptable resize deltas: any high-end extension that causes a neighboring V4 shape to fall within 33 nm (projected or corner-to-corner) will create a new spacing violation. The one accepted repair avoided this (trial:i01.ug.whole_design.00).