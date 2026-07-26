## VIA_VIA56 Via Cell Repairs Are the Sole M6 Repair Activity This Iteration

All two trials in this iteration targeted VIA_VIA56 via cells. Both were applied and both reduced violations in the unit:leaf\_0002 window. M6 appears in the `touched_layers` field of both trials despite no op in either ops list directly naming M6; V5 and M5 shape adjustments within the via cell propagate to M6 rule checks (trial:i04.cu.def:VIA\_VIA56\_2\_1\_66\_58.00, trial:i04.cu.def:VIA\_VIA56\_2\_2\_66\_58.01).

## V5 Resize-After-Move Pattern Resolves M6-Coupled Violations

Each V5 shape index in both applied trials received a y-axis move (±132 dbu) followed immediately by a y-axis resize of +512 dbu. The M5 shape at index 0 received a y-axis resize of +248 dbu with no accompanying move. Connectivity was preserved in both cases (conn\_preserved=true). This sequence — reposition then enlarge each V5 shape, enlarge M5 — was sufficient to close M6-related violations without introducing new ones (trial:i04.cu.def:VIA\_VIA56\_2\_1\_66\_58.00, trial:i04.cu.def:VIA\_VIA56\_2\_2\_66\_58.01).

## Violation Reduction Scales Proportionally with Via Array Population

The 2x1 cell (VIA\_VIA56\_2\_1\_66\_58) carried 2 V5 shape indices, required 5 operations, and yielded a reduction of 2 violations (51→49). The 2x2 cell (VIA\_VIA56\_2\_2\_66\_58) carried 4 V5 shape indices, required 9 operations, and yielded a reduction of 4 violations (51→47). The ratio of ops to violation reduction is consistent across both variants, suggesting the per-shape operation cost and per-shape violation count are uniform across the array (trial:i04.cu.def:VIA\_VIA56\_2\_1\_66\_58.00, trial:i04.cu.def:VIA\_VIA56\_2\_2\_66\_58.01).

## Both Trials Are Co-Located and Share the Same Baseline Design State

Both trials share locus [1728, 2068, 13168, 13052] and design\_state hash `ed567ea8ed9532055b9f2d9d79f033adb07cdfa59d71df85f27c47b9ae6a365e`, confirming they were evaluated against the same unmodified baseline and address the same spatial region of the layout (trial:i04.cu.def:VIA\_VIA56\_2\_1\_66\_58.00, trial:i04.cu.def:VIA\_VIA56\_2\_2\_66\_58.01).