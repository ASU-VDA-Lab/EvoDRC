## Spacing Hierarchy

M3 enforces five distinct spacing checks that depend on the classified length of each interacting edge pair. Side edges (length > 36 nm) require only 18 nm between them (M3.S.1). When one edge is a tip (≤ 36 nm) and the other is a side, the required clearance rises to 25 nm (M3.S.2). Wide tips (24–36 nm) meeting each other need 27 nm tip-to-tip (M3.S.3). A wide tip facing a narrow tip (< 24 nm) needs 31 nm (M3.S.5), and two narrow tips also need 31 nm (M3.S.4). No measured trial has yet directly isolated these individual spacing classes, so the ordering is rule-derived only; cite trial evidence as it accumulates.

## Corner Spacing

M3.S.6 is measured euclidean, not projection, and fires on shapes that clear the 20 nm projection check but fail at corners. The rule catches diagonal proximity that M3.S.1 through M3.S.5 miss. No trial has yet isolated a pure M3.S.6 fix; do not confuse this rule with the side/tip spacing rules above when diagnosing violations.

## Minimum Width and Area

M3.W.1 requires a minimum wire width of 18 nm. M3.A.1 requires minimum area of 504 nm². A rectangle at minimum width (18 nm) requires a length of at least 28 nm to satisfy area (18 × 28 = 504). These two rules interact: any width-reducing operation that brings a segment to or below 18 nm may simultaneously create an area violation if the segment is short. No trial has yet targeted a standalone M3.W.1 or M3.A.1 violation.

## V2 Enclosure and Alignment (V2.M3.EN.2, V2.M3.AUX.2)

V2.M3.EN.2 requires M3 to enclose each V2 on two opposite sides by at least 5 nm (both sides ≥ 5 nm, or one side ≥ 5 nm and the opposite exactly 0 nm via coincident edges). V2.M3.AUX.2 further constrains V2 to match M3's width exactly in the direction perpendicular to the M3 wire's length — V2 must not protrude beyond M3 edges, and it must share exactly two coincident edges with M3 on the narrow dimension.

Via cell VIA_VIA23_1_3_36_36 carries both V2 and its surrounding M3 context. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, resizing V2 shapes within that cell along the x-axis (shape_index 0: move −144 dbu then expand +288 dbu; shape_index 1: expand +288 dbu; shape_index 2: move +144 dbu then expand +288 dbu) reduced the total DRC violation count by 27 across units leaf_0018 (−15) and leaf_0019 (−12). This confirms that V2-side geometry adjustments within via cell definitions are an effective lever for clearing V2/M3 enclosure and alignment violations on M3 when the same via cell instance appears in multiple units.

When the same via cell drives violations in multiple units simultaneously, modifying the cell definition propagates the fix everywhere the cell is instantiated, yielding outsized DRC reduction per operation, as demonstrated by trial:i01.cu.def:VIA_VIA23_1_3_36_36.00.

## V3 Enclosure (V3.M3.EN.1)

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides (either left+right or top+bottom). The M3 polygon must extend ≥ 5 nm beyond the V3 boundary in both directions of at least one axis. No trial has yet directly fixed a V3.M3.EN.1 violation; when encountered, extending M3 along the axis where enclosure is short is the rule-implied repair direction.

## Non-Orthogonal Geometry

M3 edges must be strictly horizontal or vertical. The NONORTHOGONAL rule flags any edge with angle not a multiple of 90 degrees. No non-orthogonal M3 edges have appeared in the measured trial history. Resize and move operations used in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and trial:i01.ug.leaf_0008.06 operated on rectilinear shapes and did not introduce diagonal edges.

## Unit-Gate Channel Behavior on M3

Trial:i01.ug.leaf_0008.06 touched M3 (among M1, M2, V1) via a resize_end on polygon p1159 (y-axis high end, +20 dbu) and a resize_end on polygon p1261 (x-axis high end, +92 dbu), combined with two instance moves. The trial was recorded with decision gated_in and reason conn_preserved, with n_new_in_crop = 0 and n_new_out_of_crop = 0, indicating that the set of operations introduced no net new DRC violations in the crop window. Unit-gate channel trials touching M3 can therefore complete connectivity-preserving moves and end-resizes without introducing M3 violations, at least in configurations similar to leaf_0008.