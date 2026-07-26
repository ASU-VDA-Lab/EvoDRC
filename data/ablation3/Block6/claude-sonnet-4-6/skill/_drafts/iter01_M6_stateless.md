## Via-cell V5 y-axis resize reduces M6 violations without breaking connectivity

Resizing all four V5 shapes inside cell `VIA_VIA56_2_2_66_58` along the y-axis by +248 dbu reduced the total violation count by 32 with connectivity preserved (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). The repair was routed through the `cu_pool` channel and touched layers M5, M6, and V5 together, confirming that a single via-cell y-resize can simultaneously resolve violations across multiple layers including M6 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## All shapes in the via cell must be resized together

The applied operation modified all four V5 shape indices (0, 1, 2, 3) inside `VIA_VIA56_2_2_66_58` with the same delta of 248 dbu on the y-axis (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Partial application to a subset of shapes in the same via cell was not attempted, and the full-cell simultaneous resize is the form that produced a net reduction of 32 violations (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## Effective repair scope is design-wide through via cell definition

The delta of −32 violations was measured across the `unit:whole_design` window with a locus spanning the full 16944 × 16944 dbu extent (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). Because the target is a cell definition (`def:VIA_VIA56_2_2_66_58`), the repair propagates to every instance of that via cell in the design, producing a large aggregate violation reduction from a compact four-operation fix (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

## M6 enclosure and width rules are sensitive to V5 y-dimension

The only repair type observed that resolved M6-layer violations is a y-axis resize of V5 shapes in the V5-M6 via cell (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01). No M6 polygon geometry was directly modified; the M6 violation count changed as a consequence of adjusting V5 dimensions, which directly governs the enclosure relationships checked by V5.M6.EN.2 and the width-matching relationship checked by V5.M6.AUX.2 (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).