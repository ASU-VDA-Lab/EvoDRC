## V4.M5.AUX.2 — Width-match between V4 and M5

Rule V4.M5.AUX.2 requires that each V4 instance is exactly the same width as the M5 shape it sits inside, measured along the direction perpendicular to M5's length. Violations arise when the M5 shape extends beyond the V4 footprint (or vice versa) on one or both transverse edges.

The confirmed repair strategy for V4.M5.AUX.2 is to resize the M5 shape rather than the V4 shape. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a `resize_via_shape` operation was applied to M5 along the y-axis (delta_dbu = -88), shrinking the M5 extent to match the V4 width. The repair was accepted and reduced violations by 56 across two witness windows (unit:leaf_0019: −30, unit:leaf_0020: −26). Do not resize V4 directly to fix V4.M5.AUX.2; the measured fix operates on M5.

The operation group label is `v4_m5_aux2_fix`. When selecting the axis for the resize, use the axis perpendicular to M5's routing direction — in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 this was the y-axis for a cell named VIA_VIA45_1_2_58_58, touching layers M4, M5, and V4.

## V4.AUX.1 — V4 must be inside both M4 and M5

V4.AUX.1 flags any V4 instance not fully contained within the intersection of M4 and M5. Repairs to M5 shape size that bring M5 into alignment with V4 (as in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00) simultaneously affect V4.AUX.1 exposure: shrinking an oversized M5 along one axis can clear or introduce AUX.1 violations depending on the direction. Always verify AUX.1 DRC count after applying a V4.M5.AUX.2 resize, since both rules share M5 geometry as their constraint surface.

## V4.M4.EN.1 and V4.M5.EN.2 — Enclosure constraints

V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides. V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. Any M5 resize applied for V4.M5.AUX.2 compliance changes the M5 overlap available for enclosure; in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 the M5 shape was shrunk by 88 dbu on the y-axis and the repair was accepted without triggering EN.2 regressions, confirming that the pre-existing M5 extent had sufficient margin on both sides before the trim. When computing the resize delta, ensure the resulting M5 dimension still provides ≥11 nm enclosure on both opposite sides after the adjustment.

## V4.W.1 — Minimum width

V4.W.1 sets a 24 nm minimum width for V4 instances along the M5 length direction. No V4.W.1 violation or width-targeted repair appears in the measured history; do not resize V4 shapes below 24 nm when making any geometric adjustment.

## V4.S.1, V4.S.2, V4.S.3 — Spacing rules

All three spacing rules enforce a 33 nm minimum between V4 instances (same-net, different-net, and corner-to-corner respectively). No spacing violations or spacing-targeted repairs appear in the measured history. When resizing M5 to fix V4.M5.AUX.2, monitor V4 placement relative to neighboring V4 instances; an M5 extension that was previously out-of-DRC-scope could become a new shadow under projection spacing after geometry changes.

## Repair applicability

The single accepted repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00 operated on a via cell (VIA_VIA45_1_2_58_58) in channel cu_pool, Block6, touching M4, M5, and V4 together. The locus bounding box was [1728, 2068, 15336, 15216] dbu. The net violation reduction was 56 violations across two leaf windows, with the repair applied at iteration 1. This confirms that a single-operation M5 y-axis resize is sufficient to achieve meaningful violation reduction in this via cell class without requiring multi-step or multi-layer edits.