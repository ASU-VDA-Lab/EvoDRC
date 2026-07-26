## Measured repair summary (iteration 3)

One repair trial exists for M4 in iteration 3: `trial:i03.cu.def:VIA_VIA45_1_2_58_58.00`.

## Via landing-pad X-axis resize

In `trial:i03.cu.def:VIA_VIA45_1_2_58_58.00` the solver applied three coordinated resize operations on cell `VIA_VIA45_1_2_58_58`, all along the horizontal (x) axis: two V4 shapes each resized +152 dbu in x, and the co-located M4 landing-pad shape (shape_index 0) resized +152 dbu in x. The repair was accepted (`decision: applied`), connectivity was preserved (`conn_preserved: true`), and the whole-design violation count dropped from 89 to 61, a reduction of 28 (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

When the M4 landing pad of a via cell is undersized in the horizontal direction, growing the M4 shape in x together with its V4 stack closes the horizontal enclosure gap. The relevant enclosure rule for this layer pair is V4.M4.EN.1 (minimum enclosure of V4 by M4 on at least two opposite sides is 11 nm); a simultaneous x-resize on both the V4 shapes and the M4 pad is the pattern that resolved 28 violations in a single application (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Resize magnitude and grid compliance

The applied M4 x-resize was +152 dbu (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). Rule M4.AUX.1 requires M4 horizontal edges to lie on a 24 nm grid; rule M4.W.5 requires a minimum horizontal width of 44 nm; rule M4.S.2 requires a minimum horizontal spacing of 40 nm between vertical edges. The trial was accepted without introducing new violations, confirming that a +152 dbu x-extension of the landing pad satisfies these constraints in the context of `VIA_VIA45_1_2_58_58` as instantiated in Block4.

## Layer scope of the repair

The touched layers were M4, M5, and V4 (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). No M4-only shape operations (width, spacing, or track-alignment edits unrelated to a via pad) appear in the measured history. All repair evidence for M4 in iteration 3 is scoped to via-cell landing-pad resizes driven by the V4.M4.EN.1 enclosure requirement.

## No bending, wide-metal, or off-track evidence

Rules M4.AUX.3 (no bends), M4.AUX.4 (wide polygon outside-edge must not touch a routing track edge), M4.AUX.2 (minimum-width tracks must lie on the 2N × 24 nm + 48 nm horizontal grid), M4.W.2/W.3/W.4 (maximum and forbidden vertical widths), M4.S.1/S.3/S.4/S.5 (vertical spacing and tip-to-tip rules), and V3.M4.EN.2/V3.M4.AUX.2 (V3 enclosure and width-match rules) produced no repair operations in the measured history. No prescriptive guidance for those rules can be grounded in iteration 3 trial evidence.