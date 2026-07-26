## Via Enclosure and Via-Metal Matching

**V4.M4.EN.1 and resize coordination.** The applied fix trial:i05.cu.def:VIA_VIA45_1_2_58_58.01 resolved enclosure violations by enlarging both V4 and M4 in the x-axis simultaneously: each V4 shape was repositioned (±116 dbu) and resized (+384 dbu), while the M4 via shape was resized +152 dbu in x. The net result was -38 total violations across leaf_0001 and leaf_0002. This confirms that correcting V4.M4.EN.1 requires M4 to grow in the same axis as the via expansion; resizing the via alone without a corresponding M4 extension leaves the enclosure margin insufficient (11 nm minimum on at least two opposite sides).

**V3.M4.AUX.2 and V3.M4.EN.2 — do not shrink via shapes in y without matching M4.** trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 was rejected_net_positive (+34 new violations) after attempting to shrink the VIA_VIA34 cell shapes in y: M3 shape shrank -64 dbu and both V3 shapes shrank -24 dbu in y, with no M4 operation performed. Despite M4 appearing in touched_layers, no M4 resize accompanied the V3 shrink. V3.M4.AUX.2 requires V3 to be exactly the same width as M4 in the direction perpendicular to M4 length; reducing V3 height while leaving M4 unchanged breaks this flush-edge requirement. V3.M4.EN.2 (11 nm minimum enclosure on two opposite sides) is simultaneously at risk when V3 shrinks toward an M4 edge. Never shrink a via shape in y without a matching y-resize on the enclosing M4 shape (trial:i01.cu.def:VIA_VIA34_1_2_58_52.01).

## M4 Horizontal (x-axis) Resize Operations

**Extending M4 endpoints in x is consistently safe.** Four independent trials performed positive x-axis resize_end operations on M4 polygons and were all accepted with zero new violations introduced in the crop window:

- trial:i01.ug.Block4_union_row10.01: p1551 +128 high, p1589 +72 low, p1605 +92 high, p1379 +64 low — gated_in.
- trial:i01.ug.Block4_union_row7.06: p1595 +164 high, p1577 +92 high, p1556 +56 high, p1395 +172 high — gated_in.
- trial:i01.ug.leaf_0001.07: p1374 +96 high — gated_in (M4-only operation).
- trial:i05.cu.def:VIA_VIA45_1_2_58_58.01: M4 via shape +152 in x — applied.

The observed delta range is +56 to +172 dbu for unit_gate operations and +152 dbu for the via cell fix. All were at least the M4.W.5 minimum horizontal width (44 nm). None triggered M4.S.2 (40 nm minimum horizontal spacing between vertical edges) or M4.S.3/M4.S.4 tip-to-tip rules, indicating the surrounding horizontal clearance was sufficient at these loci.

**x-axis resizes do not perturb M4.AUX.1 or M4.AUX.2.** M4.AUX.1 constrains horizontal edge y-positions to a 24 nm grid; M4.AUX.2 constrains minimum-width track centerlines to a 192 dbu pitch with 48 dbu offset. Neither rule is affected by extending M4 ends in x, consistent with zero y-coordinate changes in all four trials above.

## Instance Moves Combined with M4 Resize

**Coordinated instance moves and M4 resize_end are accepted together.** trials i01.ug.Block4_union_row10.01 and i01.ug.Block4_union_row7.06 paired move_instance operations (x-axis, ±28 to +108 dbu) with M4 resize_end operations and were gated_in without introducing violations. The move_instance operations adjust M1/V1 connections while the M4 resize_end compensates horizontal reach, preserving connectivity. This joint pattern avoids open-net violations that a resize-only or move-only approach would create.

**y-axis instance moves at ±24 dbu multiples are accepted.** trial:i04.ug.leaf_0002.01 (iter 4) moved multiple instances by ±24 dbu and +72 dbu in y (and +32 dbu in x for a group), touching M3, M4, M5, V3, V4, and was gated_in with 2 new in-crop violations that remained in-crop (n_new_out_of_crop=0). The ±24 dbu y increments are consistent with the M4.AUX.1 24 nm horizontal-edge grid and the M4.AUX.2 192 dbu track pitch subdivision; moves at these increments keep track-aligned M4 shapes on valid grid positions.

## Via Cell Repair Strategy (cu_pool channel)

**Enlarging via cell shapes in x reduces violations; shrinking in y without M4 adjustment increases them.** The two cu_pool trials on M4-touching via cells show opposite outcomes:

- trial:i05.cu.def:VIA_VIA45_1_2_58_58.01 (applied): enlarged V4 and M4 shapes in x → -38 total violations.
- trial:i01.cu.def:VIA_VIA34_1_2_58_52.01 (rejected_net_positive): shrunk V3 and M3 shapes in y without touching M4 → +34 total violations.

When repairing a via cell definition, resize M4 in the same axis and direction as the via resize. For x-axis enclosure fixes, the M4 extension need not match the via extension exactly (trial:i05 used +152 dbu on M4 vs. +384 dbu on V4 per shape) but must be sufficient to satisfy the 11 nm minimum enclosure margin on both sides after the via repositioning.