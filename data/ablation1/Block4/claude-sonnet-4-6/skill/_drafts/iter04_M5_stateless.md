## M5 Repair Knowledge — Iteration 4

### Effective repair pattern for VIA_VIA56 cells: M5 y-axis resize + V5 repositioning

Both measured trials address VIA_VIA56 via cells in Block4 at locus [1728, 2068, 13168, 13052]. In both cases the engine applied a y-axis resize of the M5 shape by +248 dbu (shape\_index 0), coupled with coordinated V5 shape moves and resizes on the same y axis. Both trials preserved connectivity (`conn_preserved: true`) and were accepted (`decision: applied`). The combined pattern is the only repair strategy in this layer's history and it succeeds on every attempt recorded.

**M5 resize magnitude.** The M5 shape at shape\_index 0 is always resized on the y axis by +248 dbu. This single magnitude appears in both trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01. Do not use a different delta for the M5 y-resize on VIA_VIA56 cells until a measured record supersedes this value.

**V5 shape pairing pattern.** Each V5 cut shape receives two operations: a move of ±132 dbu (outward from center along y) followed by a resize of +512 dbu along y. In the single-pair cell (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, 2 V5 shapes), shape\_index 0 is moved −132 dbu then resized +512 dbu, and shape\_index 1 is moved +132 dbu then resized +512 dbu. In the double-pair cell (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, 4 V5 shapes), the same ±132 / +512 pattern repeats for all four shapes: indices 0 and 1 receive −132 and +132 moves respectively, as do indices 2 and 3. Apply this pairing rule uniformly regardless of the number of V5 cuts; the move magnitude (132 dbu) and resize magnitude (512 dbu) are consistent across both records.

**Violation yield scales with V5 cut count.** The single-pair cell reduced violations by −2 (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00); the double-pair cell reduced violations by −4 (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). The per-cut contribution is 1 violation eliminated per V5 shape pair treated. This ratio holds across both records and can be used to estimate expected yield for untreated cells with known V5 cut counts.

**Operation ordering.** In both trials the M5 resize is applied first (op index 0), followed by the V5 move/resize pairs in ascending shape\_index order. Maintain this ordering; reordering has no measured support.

**Layers touched.** Every applied trial touches M5, M6, and V5 simultaneously (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Repairs scoped only to M5 or only to V5 have no support in this history; treat the three-layer bundle as the atomic repair unit.

**Rule context for the M5 y-resize.** Rules V5.M5.EN.1 and V4.M5.EN.2 each require a minimum 11 nm enclosure of the via by M5 on two opposite sides. The +248 dbu M5 y-expansion directly extends enclosure margin on the vertical axis. Rule M5.W.5 sets the minimum vertical width at 44 nm (44 dbu); the +248 dbu expansion increases vertical extent and must not reduce it below this floor — both trials satisfy this implicitly, as both were accepted. Rule M5.AUX.3 prohibits bends in M5; a pure y-axis resize of a rectilinear shape cannot introduce a bend, which is consistent with acceptance in both trials.

**Connectivity safety.** All recorded repairs preserve connectivity (`conn_preserved: true` in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). The M5 y-expansion and V5 repositioning do not disconnect nets for this via type and locus.

**Scope limitation.** The two records both originate from Block4, locus [1728, 2068, 13168, 13052], cell family VIA_VIA56. No M5 repairs at other loci or for other via families appear in this history. Do not generalize the specific delta values (248 dbu M5 resize, ±132 dbu V5 move, 512 dbu V5 resize) to other cell types or loci without additional measured support.