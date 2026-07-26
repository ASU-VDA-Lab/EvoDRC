## Effective repair pattern: opposite-direction Y moves followed by uniform Y resize

The two applied cu_pool trials establish the dominant repair pattern for V5 enclosure violations. In trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, shape_index 0 was moved Y -132 dbu and shape_index 1 was moved Y +132 dbu — opposite directions — before both were resized Y +512 dbu. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.01, a four-shape cell followed the same scheme: shape_indices 0 and 1 received move Y -132 dbu and shape_indices 2 and 3 received move Y +132 dbu, then all four were resized Y +512 dbu. Applying the same move delta to every shape in a cell (all negative or all positive) did not appear in any applied record; the recorded repairs in trial:i01.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 consistently spread shapes outward from the cell center before resizing.

## Move magnitude and resize magnitude

Both applied trials used a move magnitude of 132 dbu on the Y axis and a resize magnitude of +512 dbu on the Y axis (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). No other move or resize magnitudes appear in the recorded applied operations for layer V5.

## Shapes per cell and op ordering

For a two-shape via cell (VIA_VIA56_2_1_66_58), the repair required 4 ops: move then resize for shape_index 0, move then resize for shape_index 1 (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00). For a four-shape via cell (VIA_VIA56_2_2_66_58), 8 ops were required following the same per-shape move-then-resize order (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). In both cases the move operation precedes the resize for each shape.

## Violation reduction per applied trial

Trial:i01.cu.def:VIA_VIA56_2_1_66_58.00 reduced whole_design violations by 2 (147 → 145). Trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 reduced them by 4 (147 → 143, measured after the first trial had already applied). The four-shape cell produced twice the reduction of the two-shape cell, consistent with a per-shape contribution to the enclosure violation count.

## Connectivity preservation

Both applied cu_pool trials report conn_preserved: true (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). The Y-axis spread-and-resize sequence did not break connectivity in either case.

## Touched layers

All three recorded trials — trial:i01.ug.whole_design.00, trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 — list touched_layers as M5, M6, and V5 together. V5 repair ops consistently co-modify the enclosing metal layers.

## unit_gate channel and DRC violation count

Trial:i01.ug.whole_design.00 operated through the unit_gate channel with decision "gated_in" and moved polygon p1402 and instances i0234 and i0305 by +64 dbu on Y. The cu_pool trials that followed both recorded a starting violation count of 147, which is identical to what was present before trial:i01.ug.whole_design.00 executed. The unit_gate channel produces no per-rule DRC delta record and the violation baseline remained at 147 after it applied (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00 shows "before":147). A "gated_in" decision in the unit_gate channel does not indicate V5 DRC violations were cleared; the cu_pool channel trials are the records that show measurable violation reduction for V5.

## Rule-to-operation mapping from observed repairs

Rules V5.M5.EN.1 and V5.M6.EN.2 both require 11 nm enclosure of V5 on at least two opposite sides. The recorded repair action — spreading via shapes outward on the Y axis (trial:i01.cu.def:VIA_VIA56_2_1_66_58.00, trial:i01.cu.def:VIA_VIA56_2_2_66_58.01) — extends the via shape toward each enclosing metal edge on opposing sides, directly addressing the two-opposite-sides enclosure requirement. Rule V5.M6.AUX.2 requires V5 to match M6 width exactly in the direction perpendicular to M6 length; the Y resize of +512 dbu in both applied trials adjusts the via extent to satisfy width-matching under this constraint without violating connectivity. No ops targeting X-axis enclosure appear in the history; all measured V5 repair ops operated exclusively on the Y axis.