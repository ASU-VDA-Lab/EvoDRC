Both measured records are fully provided in the prompt. I'll write the knowledge section from the DRC rules and the two history records.

---

## V3 Layer: Measured Repair Knowledge

### Rule Dependency on Co-Layers M3 and M4

V3 instances exist at the interface of M3 (below) and M4 (above). Rules V3.AUX.1, V3.M3.EN.1, V3.M4.EN.2, and V3.M4.AUX.2 all require geometric alignment with both enclosing metal layers simultaneously. Both trials that touched V3 also touched M3 and M4 in the same op set (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). Repairing any V3 rule in isolation from M3 and M4 is not observed in the history; all accepted moves co-operated on these three layers together.

### Move-Instance as the Primary V3 Repair Mechanism

The dominant operation type in both V3-touching trials is `move_instance`, displacing via cell instances along X and/or Y. In trial:i02.ug.whole_design.00, over 50 `move_instance` ops on instances such as i0379, i0527, i0333 and many others were applied alongside polygon moves on M3/M4 shapes, with the result that V3 accumulated zero new in-crop violations. In trial:i05.ug.whole_design.00, a second wave of `move_instance` ops (e.g., i0137, i0162, i0177, i0225, and others shifted by +37 or +13 dbu in X) again yielded zero new V3 violations. Do not attempt to repair V3 violations solely via polygon edge resizing without accompanying instance moves; the history does not contain an accepted example of resize-only V3 repair.

### Enclosure by M3 (V3.M3.EN.1): 5 nm on Opposite Sides

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least two opposite sides (either left+right, or top+bottom). The DRC kernel checks this via `v3.inside(m3.sized(-5.nm, 0))` and `v3.inside(m3.sized(0, -5.nm))`; a V3 instance that fails both tests raises a violation. Both trials touched M3 while touching V3 (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00) and neither introduced new V3 enclosure violations. When moving a V3 instance, the enclosing M3 shape must move by the same delta or must be resized to maintain 5 nm overlap on the relevant pair of edges.

### Enclosure by M4 (V3.M4.EN.2): 11 nm on Opposite Sides

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least two opposite sides. The threshold is higher than V3.M3.EN.1 (11 nm vs 5 nm), making M4 the tighter enclosure constraint. In trial:i02.ug.whole_design.00, polygons p1831, p1786, and p1806 received `resize_end` operations (axis x, delta +20 dbu, end high) alongside Y-axis endpoint adjustments. These resizes extended M4 shapes to maintain or recover enclosure of the co-moved V3 instances. In trial:i05.ug.whole_design.00, the same polygons p1831, p1786, p1806 received `resize_end` at axis x, delta −20 dbu, end high, partially reversing the prior resize while maintaining zero new V3 violations. This pair of trials demonstrates that M4 endpoint extensions of order 20 dbu (~2 nm at 0.1 nm/dbu) are within tolerance for maintaining V3.M4.EN.2 compliance, and that symmetric undo of such resizes does not itself trigger violations.

### Width Match Rule (V3.M4.AUX.2): V3 Must Match M4 Width Perpendicularly

V3.M4.AUX.2 requires that V3 be exactly the same width as M4 along the axis perpendicular to the M4 run direction. The DRC checks for two coincident edges between V3 and M4 boundaries. Neither trial introduced a new V3.M4.AUX.2 violation (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). When co-moving V3 instances with M4 polygons using paired `move_instance` + polygon `move` operations (as observed in both trials), this width-match constraint is automatically preserved because the via cell's transverse extent and the M4 shape move as a unit.

### Containment (V3.AUX.1): V3 Must Lie Inside Both M3 and M4

V3.AUX.1 is the strictest containment rule: V3 must fall entirely within the intersection of M3 and M4. Displacement of a V3 instance without a matching displacement of the relevant M3 and M4 shapes risks violation. Both accepted trials co-moved M3, M4, and V3 in the same op set (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). Never move a V3 instance without simultaneously moving or verifying the extents of its enclosing M3 and M4 shapes.

### Spacing Rules (V3.S.1 Through V3.S.4): End-Cap Context Determines Threshold

The spacing rules distinguish V3 instances by whether they have a 5 nm M4 end-cap (WEC: wide end-cap) or not (NEC: no end-cap):

- V3.S.1: Minimum projection spacing between NEC-type V3 edge masks is 17 nm; between maskav non-M4-coincident edges is 18 nm; between any v3_mask pair is 1 nm (effectively a merge guard).
- V3.S.2: Corner-to-corner Euclidean spacing for two WEC instances is 23 nm.
- V3.S.3: Corner-to-corner Euclidean spacing for two NEC instances is 30 nm (NEC masks are sized +5 nm, raising the effective kernel threshold).
- V3.S.4: Corner-to-corner separation between one WEC and one NEC instance is 27 nm.

Neither trial:i02.ug.whole_design.00 nor trial:i05.ug.whole_design.00 introduced new V3 spacing violations despite displacing many V3 instances. The instance moves in both trials involve X-axis deltas of 12–48 dbu (1.2–4.8 nm at 0.1 nm/dbu) and Y-axis deltas up to 96 dbu (9.6 nm). Moves of this magnitude did not produce V3.S.1–S.4 violations in either accepted trial, indicating that the pre-existing layout already had spacing margin beyond the minimum thresholds after those deltas.

### Minimum Width (V3.W.1): 18 nm Along M4 Length

V3.W.1 requires a minimum V3 width of 18 nm along the length of M4. Width along M4 is controlled by the via cell geometry, not by polygon edge edits in the assembled layout. Neither trial modified V3 cell geometry directly (all ops were `move_instance` or co-metal polygon moves), and neither trial produced a V3.W.1 violation (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). Do not resize a V3 via shape in the dimension parallel to M4 without verifying the resulting width is at least 18 nm.

### Connectivity Preservation Under V3 Moves

Both trials report `conn_preserved: true` and `decision: gated_in` (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). V3 is a via and therefore a connectivity-critical element. Any displacement of a V3 instance must maintain physical overlap with both the M3 shape below and the M4 shape above; losing that overlap severs a net. The co-move strategy observed in both trials (moving the via instance and its enclosing metal shapes together by matched deltas) is the only repair pattern in the history that has been accepted without connectivity loss.

### Orthogonality Constraint (GEOMETRY.NONORTHOGONAL)

All V3 edges must be axis-aligned (0° or 90°). The nonorthogonal block fires on any edge with angle in (1°–89°) or (91°–179°) or the negative equivalents. All polygon operations in both V3-touching trials are `move`, `move_instance`, or `resize_end` along a single named axis (x or y), which preserves orthogonality by construction (trial:i02.ug.whole_design.00, trial:i05.ug.whole_design.00). Never apply diagonal or rotational transforms to V3 shapes.