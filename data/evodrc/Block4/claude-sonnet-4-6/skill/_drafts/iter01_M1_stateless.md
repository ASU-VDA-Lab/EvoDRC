## Repair Operation Patterns Observed on M1 (Iteration 1)

### Instance-Move Step Size

Single-instance moves of exactly 36 dbu (+x direction) are the minimal safe displacement for M1-touching cells. Trials trial:i01.ug.Block4_union_row3.03, trial:i01.ug.Block4_union_row6.05, trial:i01.ug.leaf_0008.08, trial:i01.ug.leaf_0020.09, and trial:i01.ug.leaf_0021.10 each applied one `move_instance` of [36, 0] dbu and were accepted with `n_new_in_crop: 0`. At the 1 dbu = 1 nm scale implied by the rules (M1.W.1 minimum 18 nm, M1.S.1 minimum 18 nm), 36 nm equals exactly two minimum-width/spacing pitches, making it the smallest move that cannot create a new M1.W.1 or M1.S.1 violation when the surrounding geometry is already rule-clean. Do not use sub-36 nm moves for M1-touching instances; the only sub-36 move in the dataset (−28 dbu, trial:i01.ug.Block4_union_row7.06) was paired with compensating resize_end operations on multiple M1 polygons in the same locus.

Larger moves — 64 dbu (trial:i01.ug.Block4_union_row5.04), 108 dbu (trial:i01.ug.Block4_union_row1.00, trial:i01.ug.Block4_union_row7.06) — also passed without new violations when combined with appropriate resize_end steps. All moves in the dataset are strictly +x or −x; no +y / −y instance moves appear on M1-touching units in iteration 1.

### resize_end on M1 Polygon Endpoints

`resize_end` on the x-axis is the primary mechanism for satisfying V0.M1.EN.1 and V1.M1.EN.1 enclosure requirements. The operation extends a single endpoint of a specific polygon along the x-axis; positive `delta_dbu` on `end: high` pushes the right edge rightward, positive `delta_dbu` on `end: low` pushes the left edge leftward, both increasing enclosure. All resize_end calls in the dataset are positive-delta extensions — never retractions. Observed deltas: 56, 64, 72, 92, 92, 120, 120, 128, 164, 172 dbu across trials trial:i01.ug.Block4_union_row10.01, trial:i01.ug.Block4_union_row2.02, trial:i01.ug.Block4_union_row5.04, trial:i01.ug.Block4_union_row7.06. All passed with `n_new_in_crop: 0`, confirming extensions up to 172 nm on M1 tip ends do not introduce M1.S.2 (tip-to-side ≥ 25 nm) or M1.S.3 (wide-tip-to-tip ≥ 27 nm) violations in these block configurations.

V0.M1.EN.1 requires ≥5 nm enclosure on two opposite sides (or 5 & 0 nm with one flush edge). V1.M1.EN.1 requires ≥5 nm on one side and ≥2 nm on the other. `resize_end` targets the side that falls short of its required projection. Resize only the deficient end; the non-deficient end must not be moved (all trials leave one endpoint unchanged per resize_end call).

### Coupled Move-then-Resize Pattern

Multi-operation repairs consistently pair `move_instance` with one or more `resize_end` calls on M1 polygons in the same locus. The move shifts the via or connecting instance to relieve a spacing or alignment conflict; the resize_end then re-establishes the enclosure margin that the move would otherwise reduce. This two-step pattern appears in trial:i01.ug.Block4_union_row2.02 (move + 2 resizes), trial:i01.ug.Block4_union_row5.04 (3 moves + 2 resizes), trial:i01.ug.Block4_union_row7.06 (4 moves + 4 resizes), and trial:i01.ug.Block4_union_row10.01 (3 moves + 4 resizes). Applying the move without the compensating resize risks creating a new V0.M1.EN.1 or V1.M1.EN.1 violation; the dataset contains no successful single-move trial in a multi-op locus, supporting this as a firm coupling requirement.

### V0.M1.AUX.3 Axis Constraint

All `resize_end` operations target the x-axis only (`axis: "x"`). V0.M1.AUX.3 requires that V0 width exactly matches M1 width along the direction perpendicular to M1 length — modifying the y-extent of an M1 polygon that covers a V0 without also resizing V0 would violate this rule. The absence of y-axis resize_end calls in any successful trial confirms that y-axis M1 endpoint changes are avoided entirely on M1-touching polygons that contain V0. Apply resize_end only on the x-axis for M1 polygons that carry V0 vias.

### M2 add_polygon as an Alternative to M1 Edits

Trial trial:i01.ug.Block4_union_row1.00 resolved connectivity on a locus touching M1, M2, and V1 by adding two M2 rectangles ([9252,3024]→[9444,3096] and [12132,3024]→[12224,3096]) rather than editing any M1 polygon. The result was accepted with `conn_preserved: true` and `n_new_in_crop: 0`. When M1 enclosure is already adequate and the violation is a broken net continuity rather than a DRC geometry failure, prefer adding a short M2 bridge over resizing M1; this avoids perturbing M1 spacing relationships.

### M1.A.1 and M1.R.0 — No Observed Violations or Repairs

No trial in the dataset includes polygon deletions, polygon splits, or area-increasing fills on standalone M1 islands. M1.A.1 (minimum area 504 nm²) and M1.R.0 (redundant island near large empty region) did not trigger any repair operation in iteration 1. Avoid creating M1 fragments smaller than 504 nm² as a side effect of resize_end; at the minimum width of 18 nm, a polygon must be ≥ 28 nm long to meet this area floor.

### M1.S.1 / M1.S.3 / M1.S.4 / M1.S.5 Spacing — Empirical Margin

M1.S.1 forbids side-to-side spacing < 18 nm between edges longer than 36 nm. M1.S.3 forbids tip-to-tip spacing < 27 nm when both tips are 24–36 nm wide. All resize_end extensions in the dataset landed cleanly (zero new violations), but the extended polygons are in block-level contexts where surrounding M1 geometry already satisfies these spacing rules. Before applying a resize_end delta larger than 36 nm, verify that the extended tip will not encroach within 18 nm of an adjacent M1 side edge (M1.S.1) or within 27 nm of an adjacent M1 wide tip (M1.S.3). The safe set of observed deltas (56–172 nm) assumes the nearest neighbor M1 edge is not within closing distance.

### GEOMETRY.NONORTHOGONAL — Implicit Constraint

All operations (move_instance, resize_end, add_polygon) produce axis-aligned displacements and rectilinear polygons. No diagonal moves or angled edges appear anywhere in the history. The NONORTHOGONAL rule applies to M1 edges at any non-0/90-degree angle. All repair actions for M1 must use strictly orthogonal geometry; tile all polygons to Manhattan boundaries and restrict move_instance deltas to [Δx, 0] or [0, Δy] form, as confirmed by every trial in this layer's history.