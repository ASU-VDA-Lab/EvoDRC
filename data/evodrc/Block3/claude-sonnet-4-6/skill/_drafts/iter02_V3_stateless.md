## Repair Approach: Coordinated Multi-Layer Instance Moves

Both measured trials moved V3 instances as part of multi-layer operation bundles, not in isolation. Trial i02.ug.leaf_0003.02 applied six move_instance operations (i0177, i0152, i0079, i0102, i0078, i0101) with pure y-axis displacements (−48, −48, +96, +96, +48, +48 dbu), touching M3, M4, M5, V3, and V4 simultaneously, and was accepted (gated_in, n_new_in_crop=0). Trial i02.ug.leaf_0004.03 applied thirteen operations—eight move_instance calls plus five polygon-level resize_end and move operations (p1059 x-axis +32 dbu; p1104, p1103 high-end y extensions; p1102, p1101 low-end y extensions)—across the same layer set and was accepted (gated_in, n_new_in_crop=2). Move V3 instances together with their enclosing M3, M4, and adjacent via/metal layers; both trials demonstrate that this coordinated approach yields accepted outcomes.

## Connectivity Is the Primary Acceptance Condition

Both trials were accepted (gated_in) with conn_preserved=true. Trial i02.ug.leaf_0004.03 introduced two new violations in crop (n_new_in_crop=2) and was still accepted because the reason field is conn_preserved. Trial i02.ug.leaf_0003.02 introduced zero new violations (n_new_in_crop=0). Construct all V3 repair operations so that electrical connectivity is preserved; both accepted outcomes across trial:i02.ug.leaf_0003.02 and trial:i02.ug.leaf_0004.03 share conn_preserved=true as a necessary condition.

## M4 End-Cap Classification Governs Spacing Rule Selection

V3.S.1 through V3.S.4 select the applicable spacing check based on whether each V3 instance has a 5 nm M4 end-cap (wec = end-cap present; nec = M4 flush with V3 edge):

- Same M4 track, projection: 18 nm minimum (V3.S.1)
- Parallel M4 tracks, not aligned, projection: 27 nm minimum (V3.S.1)
- Parallel M4 tracks, aligned, projection: 18 nm minimum (V3.S.1)
- Both wec, corner-to-corner euclidian: 23 nm minimum (V3.S.2)
- Both nec, corner-to-corner euclidian: 30 nm minimum (V3.S.3)
- Mixed wec/nec, corner-to-corner euclidian: 27 nm minimum (V3.S.4)

Trial i02.ug.leaf_0003.02 moved instances along y by up to 96 dbu, shifting inter-instance y-separation on M4 tracks and therefore the applicable spacing category. Trial i02.ug.leaf_0004.03 moved instances along both x (32 dbu) and y (up to 72 dbu). After any instance repositioning that changes the relative track position of two V3 instances, verify post-move spacing against the correct end-cap category; both trials achieved accepted outcomes through such repositioning.

## Enclosure Constraints: Extend Bounding Polygons Concurrently With Instance Moves

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides. V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. V3.AUX.1 requires V3 to lie entirely inside both M3 and M4. Trial i02.ug.leaf_0004.03 demonstrates that when instance moves are large enough to risk enclosure violations, resize_end operations on the bounding metal polygons (p1104, p1103 extended at their high y-end; p1102, p1101 extended at their low y-end; p1059 shifted along x) must be applied in the same operation bundle. That trial was accepted (gated_in) with conn_preserved=true. Trial i02.ug.leaf_0003.02 applied only move_instance operations with no polygon resizes and introduced no new violations (n_new_in_crop=0), indicating that smaller displacements within existing enclosure margins do not require concurrent polygon extension.

## Width Matching and Orthogonality

V3.M4.AUX.2 requires V3 width perpendicular to M4 length to exactly equal M4 width. Neither trial independently resized V3 polygon widths; both used move_instance operations that preserve the internal geometry of V3 cells and thereby maintain the exact-match constraint. Avoid standalone V3 polygon resizes on the axis perpendicular to M4 length; use only instance moves or joint M4+V3 operations that keep V3 width identical to M4 width, consistent with both accepted trials (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03).

V3.W.1 requires minimum 18 nm width along the M4 length direction; this is maintained automatically when V3 instance geometry is not altered independently. All displacements in both trials are axis-aligned (trial:i02.ug.leaf_0003.02: y-only deltas of ±48 and +96 dbu; trial:i02.ug.leaf_0004.03: x deltas of 32 dbu and y deltas of ±24 and ±72 dbu), producing no diagonal edges. Keep all V3 move and resize deltas on the orthogonal grid; the NONORTHOGONAL block flags any edge at 1°–89° or 91°–179°, and both accepted trials avoided this by using exclusively axis-aligned operations.