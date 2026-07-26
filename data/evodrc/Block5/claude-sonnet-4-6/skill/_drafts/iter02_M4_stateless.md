## M4 Grid and Move Quantization

All instance moves that touch M4 must use vertical deltas that are integer multiples of 24 dbu to comply with M4.AUX.1 (horizontal edges on a 24 nm grid) and M4.AUX.2 (minimum-width M4 tracks centered on 192 dbu pitch, 48 dbu offset). In trial:i01.ug.leaf_0010.07 every vertical delta applied was a multiple of 24 dbu (values ±24 and ±72 observed), and the trial was accepted as gated_in with conn_preserved=true. Non-multiple moves risk landing M4 horizontal edges off-grid and violating M4.AUX.1 or displacing a min-width track off its routing centerline and violating M4.AUX.2.

## Connectivity Preservation Overrides New In-Crop Violations

A repair that introduces new in-crop DRC violations on M4 (or co-touched layers) is still accepted when conn_preserved=true. Trial:i01.ug.leaf_0010.07 produced n_new_in_crop=3 violations (across M3, M4, M5, V3, V4) yet received decision=gated_in solely because connectivity was preserved. Do not treat new in-crop violations as a disqualifying condition when the connectivity invariant holds; the gate logic applies the conn_preserved flag first.

## Cu_Pool Channel Reservations Block Unit_Gate M4 Polygon Moves

When cu_pool has reserved a specific M4 polygon in the same iteration, unit_gate ops targeting the same polygon are dropped at assemble time. In trial:i02.ug.leaf_0002.01, the op moving polygon p879 by +32 dbu in x was tagged reason="reserved_by_cu_pool_winner" (conflict_with_leaf="cu_pool:leaf_0002") and removed from the applied set. Two additional ops on p879 — a y-axis resize of +96 dbu and a V2 via-shape x-move of +144 dbu — were instead applied by cu_pool itself (reason="cu_pool:applied"). Never propose unit_gate x-axis moves on M4 polygons that cu_pool has already claimed in the current iteration; the move will be silently dropped, potentially leaving M4 geometry in a state the unit_gate agent did not anticipate.

## Via Cell Y-Resize as the Primary M4/V4 Enclosure Relief Lever

Resizing the M5 shape of a V4 via cell in the y-axis is an effective mechanism for resolving V4.M4.EN.1 enclosure violations (minimum 11 nm enclosure of V4 by M4 on at least two opposite sides). Trial:i02.cu.def:VIA_VIA45_1_2_58_58.02 applied a y-axis resize of -88 dbu to the M5 layer of VIA_VIA45_1_2_58_58 (cu_pool channel), touching M4 and V4, and reduced the total violation count by 15 across two units (leaf_0002: 17→8, leaf_0003: 25→19). Because M4 is a passive participant in this operation (the resize acts on the via cell definition, not on the M4 polygon directly), the M4 geometry itself need not be moved to resolve V4.M4.EN.1; adjusting the via cell's M5 extent in y is sufficient.

## Assemble Drop Ordering: Cu_Pool Wins Over Unit_Gate on Shared Polygons

The drop records in trial:i02.ug.leaf_0002.01 show a deterministic ordering: the cu_pool:applied variant of a conflicting op supersedes the unit_gate variant. The unit_gate x-move on p879 was dropped first, then cu_pool applied its own y-resize on p879 and its V2 via-shape move. When constructing repair ops for M4 polygons, assume cu_pool claims take precedence and plan unit_gate edits only on polygons not already in the cu_pool reservation set for that iteration.

## M4-Touching Trials Span Multiple Co-Layers

Every M4-touching trial in the measured history also touched M3, M5, V3, and V4 simultaneously (trial:i01.ug.leaf_0010.07, trial:i02.ug.leaf_0002.01, trial:i02.cu.def:VIA_VIA45_1_2_58_58.02). Repairs proposed for M4 violations must be evaluated for their effect on V3.M4.EN.2 (11 nm V3 enclosure by M4), V3.M4.AUX.2 (V3 width exactly matching M4 perpendicular width), and V4.M4.EN.1 (11 nm V4 enclosure by M4), as any vertical shift of M4 directly perturbs via enclosure margins on both the V3 and V4 interfaces.