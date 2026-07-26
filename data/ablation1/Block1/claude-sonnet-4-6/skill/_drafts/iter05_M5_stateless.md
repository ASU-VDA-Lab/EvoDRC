## VIA_VIA56_2_2_66_58: Y-Axis Displacement of M6 Shape Increases Violations in Both Directions

Moving the M6 shape in cell VIA_VIA56_2_2_66_58 along the y-axis increases total DRC violations regardless of polarity. A +32 dbu y-move produced a net +19 increase (leaf_0007: +20, leaf_0008: -1) and was rejected (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01). A -96 dbu y-move produced a net +33 increase (leaf_0004: +26, leaf_0005: +7) and was rejected (trial:i05.cu.def:VIA_VIA56_2_2_66_58.00). Do not attempt y-axis displacement of the M6 shape in VIA_VIA56_2_2_66_58; both directions across a range spanning at least 128 dbu have been measured to worsen violations (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA56_2_2_66_58.00).

The -96 dbu move (trial:i05.cu.def:VIA_VIA56_2_2_66_58.00) operated from a different design state (65d3c7f4…) than the +32 dbu move (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, state f1b04dbd…), confirming the failure is not specific to a single design snapshot but persists across states. Both trials list M5 in touched_layers despite the sole operation being on M6; moving M6 without co-moving M5 and V5 within the via cell creates M5/V5 enclosure misalignment relevant to V5.M5.EN.1 (minimum 11 nm M5 enclosure of V5 on two opposite sides). Never move the M6 shape in VIA_VIA56_2_2_66_58 on y without co-moving the M5 and V5 shapes by the same delta (trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA56_2_2_66_58.00).

## VIA_VIA45_1_2_58_58: M5 X-Axis Resize Combined with Polygon Moves Causes Cross-Window Harm

Applying a -32 dbu x-resize to the M5 shapes in VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 simultaneously with x-axis moves of polygons p1143 (+32 dbu) and p1142 (-16 dbu) yielded a net +16 DRC increase: leaf_0007 improved by 2 violations but leaf_0008 worsened by 18 violations, and the trial was rejected (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00). Avoid bundling M5 via-shape x-resizes with adjacent metal polygon moves when those moves interact with distinct leaf windows at the same locus; the improvement concentrates in the directly targeted window while harm spreads to other windows (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

The ops in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 resize both the VIA_VIA45 M5 shape and the VIA_VIA56 M5 shape by -32 dbu on x but do not include any corresponding resize of V4 or V5 cuts. V4.M5.AUX.2 requires V4 to exactly match M5 width in the direction perpendicular to the M5 run; resizing M5 on x without an equal V4 resize on x violates this exact-match requirement wherever M5 runs vertically. Do not resize M5 via shapes on x without simultaneously applying the same delta to the co-located V4 or V5 shape on x (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Grid Alignment: X-Axis Resizes Must Be Multiples of 24 dbu

M5.AUX.1 requires all M5 vertical edges to lie on a 24 nm grid. A resize of -32 dbu on x is not divisible by 24, so it moves at least one vertical edge off the 24 nm grid from any on-grid starting position. The -32 dbu x-resize applied to M5 shapes in VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 is a resize of this type; that trial was rejected with net +16. Apply only x-axis resizes that are multiples of 24 dbu to M5 shapes to preserve M5.AUX.1 grid compliance (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Routing Track Alignment: X-Axis Moves on Minimum-Width M5 Shapes Must Be Multiples of 192 dbu

M5.AUX.2 requires minimum-width M5 tracks (shapes narrower than 26 nm on x, i.e., those that survive a ±13 nm x-erosion) to have x-centerlines satisfying (centerline_x − 48) mod 192 = 0. An x-axis move or resize by any amount not divisible by 192 dbu shifts the centerline away from the required routing grid positions. The -32 dbu x-resize in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 (rejected, net +16) is not a multiple of 192 dbu. Do not apply x-axis moves or resizes of amounts not divisible by 192 dbu to minimum-width M5 shapes (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Width Constraint: Avoid Even-Multiple and Forbidden-Track Widths After Any X-Resize

M5.W.3 forbids horizontal widths equal to any even integer multiple of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm). M5.W.4 forbids widths of 72, 168, 264, 360, or 456 nm (widths spanning an even number of minimum-width routing tracks). Any x-axis resize must be checked to ensure the resulting M5 width does not land on any of these values. The -32 dbu x-resize applied in trial:i03.cu.def:VIA_VIA45_1_2_58_58.00 (rejected) alters the M5 shape width; verify the post-resize width clears all M5.W.3 and M5.W.4 forbidden values before committing any x-resize to M5 shapes (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00).

## Locus Coupling: Evaluate All Overlapping Leaf Windows Before Accepting Any Operation

All three measured trials target locus [1728, 2068, 14256, 14132]. In every case, one leaf window improved while another worsened, producing a net-positive total:

- trial:i03.cu.def:VIA_VIA45_1_2_58_58.00: leaf_0007 −2, leaf_0008 +18, net +16
- trial:i03.cu.def:VIA_VIA56_2_2_66_58.01: leaf_0007 +20, leaf_0008 −1, net +19
- trial:i05.cu.def:VIA_VIA56_2_2_66_58.00: leaf_0004 +26, leaf_0005 +7, net +33

Never evaluate or score a proposed M5 repair using only the targeted leaf window's delta; compute the net delta across all windows overlapping the locus and reject any operation with a positive net total (trial:i03.cu.def:VIA_VIA45_1_2_58_58.00, trial:i03.cu.def:VIA_VIA56_2_2_66_58.01, trial:i05.cu.def:VIA_VIA56_2_2_66_58.00).