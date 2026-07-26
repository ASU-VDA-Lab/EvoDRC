## Via Enclosure: V4.M4.EN.1 and V3.M4 Rules

**V4 enclosure by M4** violations at via cells are repaired by resizing M4 horizontally within the via cell definition. Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 applied a +152 dbu x-resize to the M4 shape (shape_index 0) inside cell `VIA_VIA45_1_2_58_58`, simultaneously with ±116 dbu V4 repositioning and +384 dbu V4 resizing on both V4 shapes, reducing total violations by 52 across two unit windows (leaf_0019: −28, leaf_0020: −24). The 11 nm minimum enclosure required by V4.M4.EN.1 is achieved by expanding M4 laterally in x while repositioning the V4 shapes relative to the new M4 boundary.

**V3/M4 enclosure** violations (V3.M4.EN.2, V3.M4.AUX.2) are repaired by small horizontal instance moves of −16 dbu in x. Trial:i02.ug.leaf_0003.03 moved instance i0358 by [−16, 0], resolving 2 in-crop violations in leaf_0003 while touching M3, M4, and V3 with connectivity preserved. Trial:i04.ug.leaf_0001.00 moved instance i0193 by [−16, 0], resolving 1 violation in leaf_0001 on the same layer set. Both operations were accepted with `conn_preserved: true`.

## M4 Track Alignment: M4.AUX.1 and M4.AUX.2

M4 horizontal edges must land on a 24 dbu grid (M4.AUX.1). Every y-direction move recorded in the history is an integer multiple of 24 dbu. Trial:i02.ug.leaf_0010.06 applies y-deltas of ±24 and ±72 dbu across 24 move_instance operations and 12 resize_end operations on M4 polygons. Trial:i03.ug.leaf_0002.01 applies y-deltas of ±48 and ±96 dbu across 20 move_instance operations. All deltas divide exactly by 24 dbu.

Minimum-width M4 tracks must follow the horizontal routing grid at 192 dbu pitch with a 48 dbu origin offset (M4.AUX.2). The y-deltas of 24, 48, 72, and 96 dbu used in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01 are all representable as N×24 dbu (N = 1, 2, 3, 4), which keeps relocated track centerlines on valid grid positions.

## Horizontal Track Spacing: M4.S.2

M4 vertical edges are adjusted by applying opposing x-direction moves to two polygon groups: one group shifts +32 dbu and the other shifts −16 dbu, producing a net 48 dbu increase in separation between the two M4 track sets, exceeding the 40 dbu minimum horizontal spacing required by M4.S.2. Trial:i03.ug.leaf_0003.02 applied this pattern to polygon p1683 (+32 dbu, with eight associated instances) and polygon p1682 (−16 dbu, with eight instances), resolving 26 in-crop violations in leaf_0003 while touching M4, M5, M6, V4, V5. Trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 applied the same ±32/−16 pattern to polygons p1685 and p1684 on M4, reducing violations in leaf_0002 by 14.

## Single-Axis Geometry Constraint: M4.AUX.3

M4.AUX.3 prohibits bending. All M4 geometry operations in the history are strictly single-axis. The resize_end operations in trial:i02.ug.leaf_0010.06 use only `axis:"y"`. The polygon moves in trial:i03.ug.leaf_0003.02 use only `axis:"x"` for all M4-touching polygon ops. Trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 likewise applies x-only moves to M4 polygons p1685 and p1684. No mixed-axis or diagonal M4 shape edits appear anywhere in the history.

## Repair Channel Behavior and Outcomes

Two channels act on M4. The `cu_pool` channel edits via cell definitions directly, modifying named cell geometry (resize_via_shape, move_via_shape). Trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 both used this channel to resize M4 metal while adjusting V4 or V5 shapes within the same via cell, and both were accepted with `decision: applied`. The `unit_gate` channel operates at the instance level using move_instance and resize_end. All five unit_gate trials (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, trial:i03.ug.leaf_0003.02, trial:i04.ug.leaf_0001.00) were accepted with `decision: gated_in` and `conn_preserved: true`. No trial in the full history was rejected.

## Scale of Repairs

Large coordinated repairs touching M4 fix dozens of violations in a single trial. Trial:i02.ug.leaf_0010.06 used 36 operations to resolve 26 in-crop violations across a locus covering nearly the full block height (y: 3072–14720 dbu). Trial:i03.ug.leaf_0002.01 used 20 operations to resolve 35 violations over a similar large locus (y: 2068–15216 dbu). Isolated residual violations are handled by single-instance repairs: trial:i02.ug.leaf_0003.03 (1 op, 2 violations) and trial:i04.ug.leaf_0001.00 (1 op, 1 violation). When multiple M4 tracks and their associated instances must shift together, grouping is used: trial:i04.cu.def:VIA_VIA56_2_2_66_58.00 assigns all 30 operations to `group:"g1"`, ensuring the combined M4 and via adjustment is applied atomically.