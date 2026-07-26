## Repair History Summary

One trial has been measured for M2 in iteration 2. All prescriptive claims below are grounded exclusively in that record.

---

## V2 Via Resize as a Path to M2 Violation Reduction

Resizing the V2 via shape in the x-axis direction within cell `VIA_VIA23_1_3_36_36` by +144 dbu reduced the total design DRC violation count from 140 to 89 (delta: −51) while preserving all connectivity and receiving a final `applied` decision (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). M2 was one of the three touched layers in that operation (alongside M3 and V2), confirming that geometry changes to V2 via cells propagate into M2-relevant rule checks. When a via cell resize operation spans M2, apply the change only after verifying that the resize direction (here: x-axis) does not reduce any existing M2 enclosure margin below the thresholds required by V2.M2.EN.1 (minimum 5 nm enclosure on at least two opposite sides); the measured trial shows that expanding in x is safe in this configuration (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00).

---

## V2.M2.EN.1 Enclosure Constraint

V2.M2.EN.1 requires that M2 encloses V2 by at least 5 nm on at least two opposite sides. A via resize that enlarges the V2 footprint in one axis without a corresponding enlargement of the enclosing M2 shape will tighten or violate this enclosure. The single measured repair (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) demonstrates that an x-axis V2 expansion of 144 dbu in `VIA_VIA23_1_3_36_36` produces a net improvement in the violation count without introducing new M2 failures, so the M2 landing geometry in that cell is sufficient to accommodate the enlarged via in the x direction.

---

## Rule Applicability Notes (Rule-Derived, No Additional Trials)

The following are direct restatements of the DRC rules, included to support triage when new violations appear. No measured repairs beyond trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 exist yet to ground strategy claims for these rules.

**Width (M2.W.1):** Any M2 polygon edge pair on opposite sides must be separated by at least 18 nm. Shapes narrower than 18 nm in any direction are illegal.

**Side-to-side spacing (M2.S.1):** When both interacting edges each exceed 36 nm in length, the minimum gap between those edges is 18 nm.

**Tip-to-side spacing (M2.S.2):** When one edge is ≤ 36 nm (a "tip") and the opposing edge is > 36 nm (a "side"), the minimum projection-measured separation is 25 nm. This is 7 nm more restrictive than M2.S.1 and must be accounted for whenever a short endpoint faces a long side.

**Tip-to-tip spacing — wide tips (M2.S.3):** Two edges each in the 24–36 nm range require a minimum tip-to-tip spacing of 27 nm (projection).

**Tip-to-tip spacing — mixed tips (M2.S.5):** One edge in the 24–36 nm range opposite an edge shorter than 24 nm requires a minimum tip-to-tip spacing of 31 nm (projection).

**Tip-to-tip spacing — narrow tips (M2.S.4):** Two edges each shorter than 24 nm require a minimum tip-to-tip spacing of 31 nm (projection).

**Corner-to-corner spacing (M2.S.6):** Euclidean corner-to-corner distance between any two M2 polygons must be ≥ 20 nm. This applies to diagonal proximity that projection-based checks do not flag.

**Minimum area (M2.A.1):** No M2 polygon may have an area below 504 nm². Sliver or stub shapes produced as side effects of geometry edits must be checked for area compliance.

**Compound spacing (M2.S.7):** A tip-to-tip gap of 18 nm co-located with a side-to-side spacing of ≤ 32 nm is forbidden. When side spacing is ≤ 32 nm, the parallel run length of the adjacent M2 edges must be ≥ 35 nm. Short stubs or line-ends placed near parallel neighbors with tight side spacing will trigger this rule even when M2.S.1 and individual tip rules pass.

**Diagonal gap spacing (M2.S.8):** Tip-to-tip gaps (each approximately 18 nm wide, on parallel tracks) whose shrunk centers are closer than 80 nm in euclidean distance are forbidden. Staggered line-end arrangements on adjacent tracks must maintain at least 80 nm center-to-center diagonal clearance between the gap regions.

**V1 enclosure by M2 (V1.M2.EN.2):** M2 must enclose each V1 via by at least 5 nm on two opposite sides; one of those sides may be 0 nm only when the other is 5 nm (the "5 & 0" asymmetric case is permitted, but 0 on both sides of any axis is not). V1 edges must not protrude past M2 on any side that lacks the required enclosure.

**V1 width matching (V1.M2.AUX.2):** V1 must be exactly the same width as its enclosing M2 shape in the direction perpendicular to the M2 routing direction. Any M2 resize that changes the transverse dimension of the metal must be accompanied by a matching resize of all enclosed V1 vias, or this rule will fire.

**Non-orthogonal geometry:** All M2 edges must be strictly horizontal (0°) or vertical (90°). Any repair operation that rounds corners, introduces diagonal cuts, or produces off-axis edges will produce a `M2.GEOMETRY.NONORTHOGONAL` violation. Only rectilinear edits are legal on M2.