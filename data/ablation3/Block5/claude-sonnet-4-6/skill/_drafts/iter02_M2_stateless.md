## Observed Operation Outcomes

Both recorded trials for M2 on this block were accepted (`gated_in`) with connectivity preserved and zero net change in DRC markers within the crop (`n_new_in_crop: 0`, `n_new_out_of_crop: 0`).

### Trial i01 — Mixed polygon resize and instance moves (iter 1)

trial:i01.ug.whole_design.00 performed 19 operations touching M1, M2, M3, M4, M5, V1, V2, V3, V4. The M2-relevant subset included:

- Resize of polygon p879: high-end Y extension of +48 dbu.
- Translation of polygon p910: +8 dbu in X.
- Resize of polygon p910: high-end Y extension of +20 dbu.
- Instance moves ranging from −28 to +136 dbu in X and −48 to +96 dbu in Y across multiple instances.

All of these were accepted without introducing new M2 DRC violations (trial:i01.ug.whole_design.00). The Y-extension on p879 and p910 did not trigger M2.W.1 (minimum width 18 nm), M2.S.1 (minimum side-to-side spacing 18 nm for edges > 36 nm), or M2.A.1 (minimum area 504 nm²) violations. The X translation of p910 by 8 dbu alongside V1/V2 touching layers did not cause V1.M2.EN.2, V1.M2.AUX.2, or V2.M2.EN.1 violations (trial:i01.ug.whole_design.00).

### Trial i02 — Pure X-axis instance moves (iter 2)

trial:i02.ug.whole_design.00 performed 7 instance moves, all in X, touching only M1, M2, and V1:

| Instance | Delta X (dbu) |
|----------|--------------|
| i0011    | −36          |
| i0017    | +36          |
| i0019    | +36          |
| i0025    | +36          |
| i0056    | +36          |
| i0111    | +36          |
| i0131    | −36          |

X-axis instance displacements of ±36 dbu applied to instances whose geometry spans M1, M2, and V1 did not introduce M2 spacing, width, area, or via-enclosure violations (trial:i02.ug.whole_design.00). The symmetric pattern — one instance moving −36 dbu while a cluster moves +36 dbu — preserved inter-polygon spacings and V1 enclosure on M2.

### Via enclosure rules — no violations observed

Neither trial produced violations of V1.M2.EN.2 (minimum enclosure of V1 by M2 on two opposite sides: 5 nm & 5 nm or 5 nm & 0 nm), V1.M2.AUX.2 (V1 width must match M2 width in the perpendicular direction), or V2.M2.EN.1 (minimum enclosure of V2 by M2 on at least two opposite sides: 5 nm). The polygon resize operations in trial:i01.ug.whole_design.00 and the instance shifts in trial:i02.ug.whole_design.00 both preserved these enclosure relationships.

### Rule thresholds active for this layer

The following rule boundaries are operative; no measured violation of any of these was recorded in either trial, so the operations performed remained within safe margins:

- **M2.W.1**: minimum M2 width 18 nm. Polygon extensions observed in trial:i01.ug.whole_design.00 did not narrow any edge below this.
- **M2.S.1**: side-to-side spacing ≥ 18 nm when both edges exceed 36 nm. Instance shifts of ±36 dbu in trial:i02.ug.whole_design.00 did not compress side-to-side gaps below threshold.
- **M2.S.2**: tip-to-side spacing ≥ 25 nm (tip ≤ 36 nm, side > 36 nm).
- **M2.S.3**: tip-to-tip spacing ≥ 27 nm when both tips are 24–36 nm.
- **M2.S.4**: tip-to-tip spacing ≥ 31 nm when both tips are < 24 nm.
- **M2.S.5**: tip-to-tip spacing ≥ 31 nm when one tip is 24–36 nm and the other is < 24 nm.
- **M2.S.6**: corner-to-corner (euclidean) spacing ≥ 20 nm.
- **M2.A.1**: polygon area ≥ 504 nm². The +48 dbu Y resize on p879 and +20 dbu Y resize on p910 in trial:i01.ug.whole_design.00 increased or maintained area, so area-minimum was not at risk from those operations.
- **M2.S.7**: tip-to-tip gap of 18 nm co-located with side-to-side spacing ≤ 32 nm is forbidden; parallel run length must be ≥ 35 nm when side spacing ≤ 32 nm.
- **M2.S.8**: diagonal center-to-center spacing between tip-to-tip gaps on different tracks must be ≥ 80 nm (euclidean).
- **GEOMETRY.NONORTHOGONAL**: all M2 edges must be axis-aligned (0° or 90°). No diagonal geometry was introduced in either trial.

### Summary of grounded safe operation patterns

X-axis instance moves of ±36 dbu across instances whose geometries include M2 wires and V1 cuts were accepted without M2 DRC impact (trial:i02.ug.whole_design.00). Y-axis polygon end extensions of +48 dbu and +20 dbu, combined with an 8 dbu X translation, were accepted without M2 DRC impact (trial:i01.ug.whole_design.00). The measured history contains no M2 DRC failures; no failure-grounded avoidance rules can be stated beyond what the rule thresholds themselves define.