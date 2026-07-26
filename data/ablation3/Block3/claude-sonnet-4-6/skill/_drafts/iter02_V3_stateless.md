## Width and Sizing

Rule V3.W.1 requires every V3 instance to be at least 18 nm wide measured along the M4 length direction. No trial in this iteration attempted to shrink a V3 below that threshold; trial:i02.ug.whole_design.00 moved V3-touching instances by 32 dbu in X and varying offsets in Y and introduced zero new in-crop violations, confirming that rigid translation of properly-sized vias does not trigger V3.W.1 as long as the underlying via dimensions are unchanged.

## Spacing (V3.S.1 through V3.S.4)

The spacing rules distinguish three via populations based on M4 end-cap presence. Vias whose edges are entirely coincident with M4 edges (no-end-cap, NEC class) are sized by 5 nm before the projection check; vias with at least one non-coincident edge (with-end-cap, WEC class) get a 5 nm extension on the M4-coincident edge before the mask is formed. The minimum projection spacings are 18 nm (same-track or aligned parallel-track), 27 nm (non-aligned parallel-track), and the euclidean corner-to-corner minimums are 23 nm (WEC–WEC, V3.S.2), 30 nm (NEC–NEC, V3.S.3), and 27 nm (mixed WEC–NEC, V3.S.4).

Trial:i02.ug.whole_design.00 applied 32 dbu X-translations and mixed Y-offsets (±24, ±48, ±72, ±96 dbu) across eighteen instance moves touching V3 and produced `n_new_in_crop: 0` and an empty `new_out_of_crop_by_rule` map. This demonstrates that bulk rigid translations that preserve relative via-to-via distances do not perturb spacing compliance. No spacing violation was induced or repaired in this iteration, so no spacing-specific repair heuristic is yet grounded by measured data.

## M3 Enclosure (V3.M3.EN.1)

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least two opposite sides (left+right OR top+bottom). Trial:i02.ug.whole_design.00 moved instances touching M3 (confirmed by `touched_layers` including "M3") by up to 32 dbu in X without introducing new violations, meaning the M3 geometry co-moved with the via instances and the enclosure relationship was maintained. Repairs that translate a via must carry the enclosing M3 shape with it, or separately verify that the post-move enclosure still satisfies the 5 nm bilateral minimum.

## M4 Enclosure (V3.M4.EN.2)

V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least two opposite sides. In trial:i02.ug.whole_design.00 several M4 resize and move operations were dropped by the assembler (`cu_pool:rejected_net_positive`) while the corresponding instance moves on V3-touching cells were retained. Despite those M4 assemble-drops the trial was accepted with `n_new_in_crop: 0`, indicating the retained instance-level moves were sufficient to keep V3 within compliant M4 enclosure. Do not assume dropped M4 resizes are harmless in all cases; the zero-violation outcome here is specific to the geometry of trial:i02.ug.whole_design.00 where the M4 shapes were already large enough after the instance translations.

## Alignment with M4 Width (V3.M4.AUX.2)

V3.M4.AUX.2 demands that a V3 shape be exactly as wide as the M4 shape in the direction perpendicular to M4's length, with the V3 sharing at least two coincident M4 edges. Trial:i02.ug.whole_design.00 moved polygon shapes p1059 and p1060 by 32 dbu in X alongside associated instance moves and produced no AUX.2 violations. Pure X-translation of both the V3 polygon and the M4 container preserves the perpendicular width coincidence. Any repair that moves a V3 in the M4-perpendicular direction without an equal move of the enclosing M4 would break AUX.2 and is not supported by observed evidence.

## Placement Inside M3 and M4 (V3.AUX.1)

V3.AUX.1 requires every V3 to lie entirely inside the intersection of M3 and M4. Trial:i02.ug.whole_design.00 co-moved V3-touching instances with both their M3 and M4 context (all three layers appear in `touched_layers`) and produced no AUX.1 violations. Moving a via instance without simultaneously moving its enclosing M3 and M4 context risks creating an out-of-intersection condition; the safe pattern observed in trial:i02.ug.whole_design.00 is instance-level translation that carries all participating layers together.

## Connectivity and Acceptance Gate

Trial:i02.ug.whole_design.00 was accepted (`decision: gated_in`) with `conn_preserved: true` and zero new violations in or out of crop. The 18-operation move set, which included translations of 32 dbu in X and offsets from −72 to +96 dbu in Y across eleven distinct instances, is the only repair event recorded for V3 in this iteration. All knowledge above is grounded solely in that single trial.