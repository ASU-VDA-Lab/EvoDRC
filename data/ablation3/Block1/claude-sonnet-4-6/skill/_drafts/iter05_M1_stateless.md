## Observed Operation Outcomes

**Accepted trial inventory.** Both recorded trials for M1 were accepted (decision: "gated\_in") with zero net new violations introduced (n\_new\_in\_crop: 0, n\_new\_out\_of\_crop: 0): trial:i03.ug.whole\_design.00 (iter 3, 32 ops) and trial:i05.ug.whole\_design.00 (iter 5, 22 ops).

---

## Axis Coverage

All instance moves in both accepted trials operated exclusively on the x-axis (delta\_dbu y-component = 0 in every move\_instance entry; resize\_end operations specify axis: "x" throughout). No y-axis moves or y-axis resize operations appear in the measured history (trial:i03.ug.whole\_design.00, trial:i05.ug.whole\_design.00). Do not extrapolate y-axis behavior from these records; it is unmeasured.

---

## Instance Move Magnitudes and Sign

In trial:i03.ug.whole\_design.00, 32 move\_instance operations applied uniform magnitudes of +64 dbu (30 instances) and −64 dbu (2 instances: i0455, i0079) in x, all accepted without new violations. In trial:i05.ug.whole\_design.00, move magnitudes varied: +48 dbu (instances i0041, i0244, i0290, i0300, i0434, i0438, i0492), +44 dbu (i0060, i0188, i0294, i0485, i0507), +36 dbu (i0078, i0463), −72 dbu (i0433, i0082), and −64 dbu (i0258), also accepted. Mixing positive and negative x-displacements in the same operation set does not in itself introduce new M1 violations, as confirmed by both trials.

---

## resize\_end Operations on M1 Polygons

Trial:i05.ug.whole\_design.00 introduced five resize\_end operations extending the high end of the x-axis on M1 polygons p1255, p1270, p1295, p1309, and p1320, each by +44 dbu. Each of these polygon extensions accompanied a move\_instance on an adjacent instance that shifted by +44 dbu (instances i0060, i0188, i0294, i0485, i0507 at +44 dbu). Instances paired with resize\_end operations moved at +44 dbu while other nearby instances not paired with a resize moved at +48 dbu (trial:i05.ug.whole\_design.00). The combination of per-instance moves at different magnitudes with selective M1 polygon edge extensions was accepted with no new violations. Apply resize\_end on the M1 high-x edge by the same delta as the paired instance move when the instance displacement matches the polygon extension delta, as demonstrated in trial:i05.ug.whole\_design.00.

---

## Enclosure Rules: V0.M1.EN.1 and V1.M1.EN.1

V0.M1.EN.1 requires that M1 encloses V0 by at least 5 nm on two opposite sides (5 & 5 nm, or 5 & 0 nm permitted). V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm and 2 nm on two opposite sides. Both trials touch layers M1, M2, and V1 (touched\_layers field), meaning V1 enclosure by M1 is actively affected. The resize\_end operations in trial:i05.ug.whole\_design.00 extend the M1 polygon's high-x edge to follow the displaced via, maintaining enclosure without generating new V1.M1.EN.1 violations. When a move\_instance shifts a cell containing V1 (or V0) and the M1 polygon does not automatically extend with it, apply resize\_end on the appropriate M1 edge by the instance move delta to preserve enclosure compliance, as confirmed by trial:i05.ug.whole\_design.00.

---

## V0.M1.AUX.3: Width Matching

V0.M1.AUX.3 requires that V0 exactly matches M1 width in the direction perpendicular to M1 length. The resize\_end operations in trial:i05.ug.whole\_design.00 extend only one end of M1 polygons (the high-x edge). No symmetric resize or width-adjustment operations appear in either trial. Both trials were accepted with no new violations, meaning the single-end extension at +44 dbu did not break V0.M1.AUX.3 in the measured cases. Avoid extending only one edge of an M1 polygon in a way that causes M1 to exceed or diverge from the V0 width in the perpendicular direction; the measured acceptance in trial:i05.ug.whole\_design.00 covers the specific instances listed (p1255, p1270, p1295, p1309, p1320) and their particular geometric context.

---

## Connectivity Preservation

Both accepted trials record conn\_preserved: true. Operate instance moves and M1 edge extensions together as a coordinated set (as done in trial:i03.ug.whole\_design.00 and trial:i05.ug.whole\_design.00) rather than adjusting M1 polygons independently of their associated cell instances, to preserve connectivity.

---

## Spacing Rules: Observed Bounds

M1.S.1 prohibits side-to-side spacing below 18 nm when both edges exceed 36 nm. M1.S.2 sets tip-to-side minimum at 25 nm. M1.S.3 sets tip-to-tip minimum at 27 nm when both edges are 24–36 nm. M1.S.4 and M1.S.5 set tip-to-tip minimums at 31 nm for edges below 24 nm. M1.S.6 sets corner-to-corner minimum at 20 nm. Both accepted trials operated exclusively via instance moves and single-end polygon extensions in x; no explicit spacing-targeted edits appear. The acceptance of both trials without new spacing violations confirms that the x-displacements applied (36–72 dbu in magnitude) did not close any previously compliant spacing below its threshold for the specific geometries involved (trial:i03.ug.whole\_design.00, trial:i05.ug.whole\_design.00). Do not infer that arbitrary x-displacements of these magnitudes are universally safe; both trials reflect the specific design state hashes d3918cc01cdd3a72b920a56bb4134c32dba21ba75cc816cc33aad0b5beb59ec0 and 3c70b52c7b36cb9889dd6cab3814e4103d463e5a5446f6e996b1892edac64ef2, respectively.

---

## Width and Area Rules

M1.W.1 requires minimum M1 width of 18 nm. M1.A.1 requires minimum M1 area of 504 nm-sq. The resize\_end operations in trial:i05.ug.whole\_design.00 increased the high-x extent of M1 polygons by +44 dbu, which increases polygon area and does not reduce width. No resize operations that shrink M1 appear in either trial. The accepted outcome in trial:i05.ug.whole\_design.00 confirms that adding length to M1 polygons in x does not introduce M1.W.1 or M1.A.1 violations.

---

## M1.R.0: Redundant Island Avoidance

M1.R.0 flags M1 polygons enclosing exactly one small V0 via when located near a large empty M1 region. Neither trial contains operations that create isolated single-via M1 islands; all instance moves are coordinated cluster relocations (trial:i03.ug.whole\_design.00, trial:i05.ug.whole\_design.00). When moving instances, move the full cluster of associated cells together rather than moving individual cells in isolation, to avoid creating M1 islands that satisfy the M1.R.0 flagging conditions.

---

## Nonorthogonal Geometry

The NONORTHOGONAL rule prohibits any M1 edge with an angle other than 0 or 90 degrees. All resize\_end operations in the measured history specify axis: "x" with integer dbu deltas, and all move\_instance operations use integer dbu vectors on orthogonal axes (trial:i05.ug.whole\_design.00, trial:i03.ug.whole\_design.00). Never introduce diagonal cuts or non-integer snap positions when adjusting M1 polygons or moving M1-touching instances.