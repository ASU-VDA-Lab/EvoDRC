## Observed Operation Outcomes on M1

### Trial Acceptance Summary

All four measured trials that touched M1 (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00) were accepted with `decision: gated_in`, `conn_preserved: true`, and zero new M1 DRC violations introduced in-crop or out-of-crop. No M1 rule (M1.W.1, M1.S.1, M1.S.2, M1.S.3, M1.S.4, M1.S.5, M1.S.6, M1.A.1, M1.R.0, V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1) fired as a new violation in any accepted trial.

---

### M1 Polygon Resize Operations

**X-axis high-end extensions** of +128 dbu on M1 polygons p951 and p955 were accepted without triggering M1.W.1, M1.S.1, M1.S.2, M1.S.3, M1.A.1, or V1.M1.EN.1 (trial:i05.ug.whole_design.00). Extending the high end of an M1 polygon along the x-axis by this magnitude is a viable repair action when connectivity is preserved.

**Y-axis high-end extensions** of +48 dbu on polygon p879 and +20 dbu on polygon p910 were both accepted without new M1 violations (trial:i01.ug.whole_design.00). Small y-axis extensions on the high end of M1 polygons do not introduce M1 width, spacing, or area violations at these magnitudes.

**X-axis positional move** of +8 dbu on polygon p910 (combined with the y-axis resize on the same polygon in the same trial) was accepted without new M1 violations (trial:i01.ug.whole_design.00). Combined translate-and-extend operations on a single M1 polygon are safe when the enclosure relationships to V0 and V1 are maintained.

Do not shrink M1 polygons along an enclosure axis without verifying V0.M1.EN.1 and V1.M1.EN.1 remain satisfied: the measured trials only extend M1 polygon ends, never shrink them, and all enclosure checks passed across every trial (trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00).

---

### Instance Move Ranges That Were Accepted

**X-axis instance moves** in the range −36 dbu to +136 dbu were applied across many instances and accepted without new M1 violations:
- ±36 dbu moves across multiple instances (trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00)
- +72 dbu moves across multiple instances (trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00)
- +136 dbu (i0012) and −28 dbu (i0103) moves (trial:i01.ug.whole_design.00)

**Y-axis instance moves** in the range −48 dbu to +96 dbu were applied across multiple instances and accepted without new M1 violations (trial:i01.ug.whole_design.00): moves of +72, −48, +24, +96, −24, and +48 dbu all cleared every M1 check.

When moving instances, prefer increments that are multiples of 24 dbu or 36 dbu, as all accepted instance moves in the measured history use these increments or their multiples (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). Moves at these granularities did not create M1.S.1, M1.S.2, M1.S.3, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, or V1.M1.EN.1 violations in any measured trial.

---

### Instance Deletion Touching M1

Deleting seven instances (i0098, i0105, i0075, i0076, i0099, i0002, i0070) in a single trial that listed M1 as a touched layer was accepted with connectivity preserved and zero new M1 violations (trial:i05.ug.whole_design.00). Instance deletion is a viable M1-touching operation provided connectivity is verified; the measured result confirms no M1 area, spacing, or enclosure rule was newly triggered by removing these instances.

---

### V0.M1.EN.1 and V0.M1.AUX.3 Enclosure Behavior

V0.M1.EN.1 requires M1 to enclose V0 by at least 5 nm on two opposite sides (either 5 & 5 nm or 5 & 0 nm on a projection basis). V0.M1.AUX.3 requires V0 to be exactly the same width as M1 along the direction perpendicular to M1 length. No new violations of either rule were observed across any of the four measured trials (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). All operations that extended M1 polygon ends or moved instances containing V0 maintained these enclosure relationships.

When resizing M1 polygon ends (as with p879, p910 in trial:i01.ug.whole_design.00 and p951, p955 in trial:i05.ug.whole_design.00), use resize_end on the M1 polygon's high end to extend enclosure rather than moving the via, to avoid disturbing V0.M1.AUX.3 width-match requirements.

---

### V1.M1.EN.1 Enclosure Behavior

V1.M1.EN.1 requires M1 to enclose V1 by 5 nm on one opposite pair of sides and 2 nm on the other. All four measured trials that listed M1 as a touched layer (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00) were accepted with no new V1.M1.EN.1 violations. The x-axis high-end extensions of +128 dbu on M1 polygons in trial:i05.ug.whole_design.00 confirm that large extensions of M1 along the enclosure axis do not themselves violate V1.M1.EN.1, provided the extension moves outward from the via.

---

### M1 Width, Spacing, and Area Rules

No violation of M1.W.1 (minimum 18 nm width), M1.S.1 (side-to-side 18 nm), M1.S.2 (tip-to-side 25 nm), M1.S.3 (tip-to-tip for 24–36 nm edges: 27 nm), M1.S.4, M1.S.5, M1.S.6 (corner-to-corner 20 nm), or M1.A.1 (minimum area 504 nm²) was recorded as newly introduced in any of the four measured trials (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00).

Extending M1 polygon ends by +128 dbu in the x-direction (trial:i05.ug.whole_design.00) did not cause M1.S.1 or M1.S.2 violations, indicating that the neighboring M1 geometry had sufficient clearance to accommodate these extensions at this design location.

Avoid shrinking M1 polygon ends below the minimum width of 18 nm (M1.W.1) or below the 504 nm² area threshold (M1.A.1): no measured trial tests any shrink operation on M1 polygons, so no safe shrink magnitude has been established.

---

### M1.R.0 Redundant Island Rule

M1.R.0 flags M1 islands that enclose exactly one small V0 via when located near a large empty M1 region (≥ 500 nm wide, area > 2.5 µm², expanded by 400 nm). No new M1.R.0 violations were introduced in any measured trial (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). The seven instance deletions in trial:i05.ug.whole_design.00 did not create new M1 islands triggering this rule, confirming that instance removal in the measured locus did not produce isolated single-via M1 fragments near large empty regions.