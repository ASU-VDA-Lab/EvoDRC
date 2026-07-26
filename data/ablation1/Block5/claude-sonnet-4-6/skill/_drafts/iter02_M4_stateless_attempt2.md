## M4 Repair Knowledge — Iteration 2

### Enclosure violations (V3.M4.EN.2, V4.M4.EN.1)

Both enclosure rules require M4 to surround its via on at least two opposite sides by a minimum of 11 nm. The only successful repair in this layer's history addressed exactly this class of violation by growing the M4 metal shape in the y-axis via `resize_via_shape` (+88 dbu) on the containing VIA cell (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00, `conn_preserved=true`, `delta_total=-13`). Expand M4 in the enclosure-deficient axis first; the measured reduction of 13 violations in a single pass confirms this is the high-leverage action.

V4.M4.EN.1 and V3.M4.EN.2 share the same 11 nm threshold and the same two-opposite-sides requirement. When the via cell is shared across both V3 and V4 stacks (as in trial:i01 where `VIA_VIA45_1_2_58_58` carries both V4 and M4 shapes and `VIA_VIA34_1_2_58_52` carries V3), a single y-axis resize on the M4 shape inside the cell simultaneously resolves both enclosure checks; trial:i01 confirms this chain-fix approach produced the net-negative delta.

### Shrinking M4 in the y-axis worsens the violation count

Trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 applied `resize_end` operations at -32 dbu on both the low and high y-ends of three polygons (p891, p892, p893) while M4 was in `touched_layers`. The trial was `rejected_net_positive` (`delta_total=+5`). Do not shrink M4 polygon extents in the y-axis as a repair strategy; trial:i02 confirms this increases net violations even when a subset of windows improves.

### Width constraints (M4.W.1 – M4.W.4) and grid alignment (M4.AUX.1, M4.AUX.2)

M4.W.1 sets 24 nm as the minimum vertical width. M4.W.3 and M4.W.4 together prohibit vertical widths that are exact even-integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm per M4.W.3) and additionally prohibit widths 72, 168, 264, 360, and 456 nm (M4.W.4). M4.W.2 caps vertical width at 480 nm. After any y-axis resize, verify the resulting vertical dimension does not land on any of these forbidden values. The +88 dbu resize in trial:i01 was applied without triggering M4.W.3 or M4.W.4, consistent with the starting shape having a vertical width that, after expansion, remained off the forbidden list.

M4.AUX.1 requires M4 horizontal edges to sit on a 24 nm grid. M4.AUX.2 requires minimum-width M4 tracks to lie on the horizontal routing grid with 192 dbu pitch and 48 dbu offset. Any `resize_end` or `resize_via_shape` operation that shifts a horizontal edge must land on a multiple of 24 nm; the successful repair in trial:i01 used a delta of 88 dbu, which is not a multiple of 24. The 88 dbu delta acted on a shape inside a VIA cell where the edge was repositioned relative to the cell origin, so the absolute post-move coordinate must be grid-checked at placement, not at the delta value alone.

### Non-bending constraint (M4.AUX.3) and axis-aligned repair

M4.AUX.3 prohibits any bend in M4 (corners between 0° and 90°). Every operation recorded in the history uses `axis="y"` with orthogonal resize operations (`resize_via_shape`, `resize_end`), preserving the rectilinear shape of M4 (trial:i01, trial:i02). Apply only axis-aligned resize operations to M4; trial:i01 demonstrates that y-axis `resize_via_shape` on the VIA cell is the correct mechanism for enclosure repair without introducing non-orthogonal geometry.

### Spacing rules (M4.S.1 – M4.S.5) interaction with enclosure repair

Expanding M4 to satisfy enclosure must be checked against M4.S.1 (24 nm minimum vertical spacing) and M4.S.2 (40 nm minimum horizontal spacing) with neighboring M4 shapes. Trial:i01 expanded M4 by 88 dbu and was accepted (`conn_preserved=true`, `decision=applied`), indicating the expanded shape did not violate spacing rules in that locus. When expanding M4 in a dense region, verify both the new enclosure margin and the resulting spacing to the nearest neighbor before committing; the trial:i02 rejection (`rejected_net_positive`) shows that operations touching M4 in adjacent loci can increase violations despite locally reducing them in one window (window `unit:leaf_0005` worsened from 20→28 while `unit:leaf_0006` improved from 16→13).

### V3.M4.AUX.2: via width matching

V3.M4.AUX.2 requires V3 to be exactly the same width as M4 in the direction perpendicular to M4's length. When M4 is resized in y to close an enclosure gap, V3 shapes must be co-resized to maintain this constraint. Trial:i01 resized both M4 (via `resize_via_shape` on `VIA_VIA45_1_2_58_58` layer M4) and V3 (via `resize_via_shape` on `VIA_VIA34_1_2_58_52` layers V3 shape_index 0 and 1) by the same +88 dbu, and the trial was accepted with no V3.M4.AUX.2 violations added. Always co-resize the V3 shapes inside the same VIA cell by the same delta when adjusting M4 y-extent; trial:i01 confirms this paired approach clears both the enclosure and the width-match constraint simultaneously.

### Chain-fix grouping

Trial:i01 bundled six operations across M3, M4, V3, and V4 under the `"chain_fix"` group in a single applied trial, yielding -13 total violations across two windows. Trial:i02 bundled ten operations under `"V2M3_corrected"` across M2, M3, V2, V3, and M4 (indirect) and was rejected net positive. Group all co-dependent via-stack resizes into one chain-fix submission; do not split M4 and its immediately adjacent via layers across separate trials. Trial:i01 is the only accepted example in this layer's history and it used exactly this co-grouped approach.