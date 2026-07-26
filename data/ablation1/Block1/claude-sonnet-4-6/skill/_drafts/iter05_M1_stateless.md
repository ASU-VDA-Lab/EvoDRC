**Connectivity is the binding gate criterion; DRC violation count is not.**

All accepted trials have `conn_preserved=true` regardless of how many new in-crop DRC violations they introduce. trial:i04.ug.leaf_0004.03 introduced 80 new in-crop violations yet was gated_in because `conn_preserved=true`. trial:i05.ug.leaf_0001.00 was gated_out with 0 new violations because `conn_preserved=false`. Do not use `n_new_in_crop` to predict acceptance or rejection.

---

**Move-instance deltas and the 36 dbu grid.**

Every accepted move_instance uses a `delta_dbu` that is a nonzero multiple of 36 in each axis (±36, ±72, ±108) with two exceptions: instance i0455 moved −32 dbu in trial:i01.ug.Block1_union_row6.06 (1 new violation, gated_in) and instance i0060 moved +4 dbu in trial:i04.ug.leaf_0004.03 (80 new in-crop violations, gated_in). Use multiples of 36 dbu for move_instance deltas when possible; the off-grid 4 dbu move in trial:i04.ug.leaf_0004.03 produced the highest new-violation count observed across all five iterations.

---

**Repeated instance i0453: delta escalation broke connectivity.**

Instance i0453 was moved +36 dbu in x at trial:i03.ug.Block1_union_row3.00 (gated_in, 0 new violations), moved +36 dbu again at trial:i04.ug.leaf_0001.00 (gated_in, 0 new violations), and then moved +72 dbu at trial:i05.ug.leaf_0001.00, which was gated_out (`conn_broken`). Do not double the per-trial delta for an instance that has already been moved in a prior iteration; a larger single-step displacement of a cumulated instance can sever connectivity even in a direction that was previously safe.

---

**resize_end operations on M1 polygons.**

resize_end on the x-axis at the high end has been accepted with deltas of +36, +52, +72, +92, and +128 dbu across multiple trials (trial:i01.ug.Block1_union_row1.00 applied +128 dbu to p1320 and +92 dbu to p1321; trial:i01.ug.Block1_union_row3.03 applied +92 dbu to p1370; trial:i01.ug.Block1_union_row4.04 applied +52 dbu to p1238; trial:i03.ug.leaf_0004.01 applied +72 dbu to p1295). resize_end at the low end with +36 dbu was also accepted for p1253 in trial:i01.ug.leaf_0020.10 and for p1301 in trial:i01.ug.Block1_union_row5.05. Simultaneous resize_end on both the high end of one polygon and the low end of another within the same trial is safe (trial:i01.ug.Block1_union_row5.05, p1297 high +36, p1301 low +36, 0 new violations).

---

**V1.M1.EN.1: enclosure violations introduced by large-locus multi-instance moves.**

In trial:i05.ug.leaf_0005.04, a large-locus trial (x: 1728–14256 dbu, y: 3148–14132 dbu) with four +36 dbu x-moves of distinct instances plus a y-displacement of polygon p1561 (−96 dbu) produced 15 new V1.M1.EN.1 in-crop violations — the largest single-rule violation count in iteration 5 for M1-adjacent rules. V1.M1.EN.1 requires M1 to enclose V1 by at least 5 nm on one horizontal-or-vertical opposite-side pair and at least 2 nm on the other pair (per the asymmetric 5 & 2 nm rule). Wide-locus trials that displace multiple instances in the same direction shift M1 endpoints away from their enclosing V1 edges; after such moves, verify that M1 still satisfies both the 5 nm and 2 nm projection enclosures on every V1 the moved M1 touches.

---

**M1.A.1: small M1 fragments produced by multi-instance moves.**

trial:i05.ug.leaf_0005.04 introduced 7 new M1.A.1 violations (minimum area 504 nm-sq) in the same wide-locus trial that produced the V1.M1.EN.1 violations above. Instance moves that shrink or sever M1 geometries can leave sub-504 nm-sq fragments; verify M1 polygon area after any displacement that reduces local M1 coverage, particularly in wide-locus trials with multiple simultaneous moves.

---

**add_via as a zero-violation substitute for a misplaced instance.**

trial:i02.ug.leaf_0004.02 paired `delete_instance` (i0300) with `add_via` placing a VIA_VIA12 cell at origin [5904, 6300], touching M1, M2, and V1, with 0 new in-crop violations and gated_in. Via replacement is a clean substitute for a misplaced instance in the M1/V0 stack.

---

**assemble_drops do not block gating.**

trial:i05.ug.leaf_0005.04 logged one assemble_drop — a V56 via shape y-move rejected by the copper pool with reason `cu_pool:rejected_net_positive` — but was still gated_in with conn_preserved=true. Assemble_drops represent post-assembly optimizations rejected at the copper-pool stage, not a DRC or connectivity failure, and do not prevent a trial from being accepted.

---

**Touched-layer scope of M1 operations.**

Every trial in the full history touches M1, M2, and V1 as a minimum set. trial:i05.ug.leaf_0005.04 additionally touches M6. No trial touches M1 in isolation: resize_end and move_instance operations on M1 polygons and instances containing M1 geometry uniformly register V1 and M2 as co-touched layers, confirming that M1 adjustments propagate through the via stack above and below.