## Repair Operation Vocabulary

Every V1 DRC repair in the measured history co-touches M1, M2, and V1 simultaneously; no trial isolated changes to V1 alone (trial:i01.ug.Block7_union_row10.00 through trial:i03.ug.leaf_0011.07). The complete repair vocabulary observed is:

- **move_instance**: shifts a cell instance and all its child geometry by a signed x or y delta in dbu.
- **resize_end**: extends or contracts one end (high or low) of a polygon along axis x or y.
- **resize**: shifts both ends of a polygon by a net delta along one axis.
- **move**: translates an entire polygon without changing its shape.
- **add_polygon**: inserts a new rectangle on a specified layer to restore connectivity after a via is displaced.

## Lateral (X-Axis) Instance Moves Are the Primary Fix

The dominant repair action across all 42 trials is `move_instance` with a nonzero x delta. Lateral moves re-space via instances along M2 tracks to satisfy V1.S.1 projection-spacing requirements. The most frequent move increment is 36 dbu, appearing in trial:i01.ug.Block7_union_row11.01, trial:i01.ug.Block7_union_row12.02, trial:i01.ug.Block7_union_row6.18, trial:i01.ug.Block7_union_row17.07, trial:i03.ug.Block7_union_row13.01, and many others. Moves of 72 dbu and 108 dbu (double and triple of 36) are also common (trial:i01.ug.Block7_union_row7.19 x+108, trial:i01.ug.leaf_0001.22 x+108, trial:i03.ug.leaf_0008.06 x+108). Larger moves of 136 dbu appear when violations are severe (trial:i01.ug.Block7_union_row13.03, trial:i01.ug.Block7_union_row15.05, trial:i01.ug.Block7_union_row24.14).

## M2 Polygon Resizing Accompanies Instance Moves

When an instance is moved laterally, adjacent M2 polygons must be resized to maintain their wire extents and preserve V1 enclosure by M2 (V1.M2.EN.2). The standard pattern pairs a `move_instance` with one or more `resize_end` operations on neighboring M2 polygons. Trial:i01.ug.Block7_union_row10.00 moves instance i1140 by x+52 and extends polygon p3286 high end by x+308; trial:i01.ug.Block7_union_row3.15 moves i1623 by x-36 and adjusts the low end of p3384 by x+56. The resize_end delta is not equal to the move delta in general—it compensates for the net geometry change needed at the polygon endpoint.

A `resize` (full-polygon shift) applied to an M2 polygon moves it bodily without changing its length (trial:i01.ug.Block7_union_row15.05 x+160 on p3586, trial:i01.ug.Block7_union_row19.09 x+40 on p3619 and x-72 on p3654). This is used when the polygon must track its connected via exactly rather than stretch to meet it.

## M2 Patch Polygons Restore Enclosure After Via Displacement

When a V1 via is displaced far enough that it exits the boundary of its original M2 segment, a new M2 rectangle is added via `add_polygon` to re-cover the via. Trial:i01.ug.Block7_union_row20.10 moves instance i0753 by x-36 and then inserts an M2 patch at [5992,22824]–[6048,22896] (56 dbu wide, 72 dbu tall) to restore V1.AUX.1 and V1.M2.EN.2 compliance. This strategy avoids extending the original M2 segment when doing so would create a new spacing violation with a neighboring segment.

## Y-Axis Adjustments Address Cross-Track and Vertical Violations

Violations involving V1 instances on adjacent or parallel M2 tracks (V1.S.1 parallel-track cases, or V1.S.2/S.3/S.4 corner-to-corner rules) require vertical (y-axis) moves in addition to or instead of lateral moves. Trial:i01.ug.Block7_union_row16.06 moves two instances y-12 and also shifts an M3 polygon by y-12. Trial:i02.ug.Block7_union_row15.03 moves instance i1062 y-84 and applies a y+96 polygon resize on p3592. Trial:i03.ug.leaf_0007.05 moves i1062 y+84 and then shrinks both ends of p3592 along y by 48 dbu each (resize_end low y-48 and high y-48). The net result in these cases is that the via is repositioned vertically and the M2 polygon is trimmed to prevent the extended footprint from creating new violations with neighbors.

## Multi-Layer Repairs Involve M3 and V2

Five trials also touch M3 and V2 layers alongside V1: trial:i01.ug.Block7_union_row16.06, trial:i01.ug.leaf_0095.26, trial:i02.ug.leaf_0014.08, trial:i03.ug.leaf_0002.04, trial:i03.ug.leaf_0011.07. Moving a V1/M2 instance in these cases requires adjusting the M3 segment and V2 via above it to preserve the vertical stack. Trial:i03.ug.leaf_0002.04 adds an M3 polygon at [11664,11756]–[11908,11828] after moving instances x+68 and x+172 and resizing an M2 polygon low end x-88, showing that M3 patch insertion is a required repair action when moving the M2/V1 stack displaces the stacked V2 outside its original M3 coverage. Trial:i03.ug.leaf_0011.07 trims the high end of polygon p3537 by y-48 after moving two instances by y-48 and y-48/-16, keeping the M3 footprint aligned with the shifted M2/V1 stack.

## Units Requiring Multiple Iterations

Several units returned V1 violations after the first repair pass and required second and third iterations:

- Block7_union_row13 was repaired in all three iterations (trial:i01.ug.Block7_union_row13.03, trial:i02.ug.Block7_union_row13.02, trial:i03.ug.Block7_union_row13.01), with the locus shrinking from the full row span (3520–26640 dbu) to a 1.5 µm sub-segment (14200–15696 dbu) by iteration 3. Early coarse moves expose secondary violations at neighboring via sites that the next iteration targets at a tighter locus.
- Block7_union_row20 required three iterations (trial:i01.ug.Block7_union_row20.10, trial:i02.ug.Block7_union_row20.04, trial:i03.ug.Block7_union_row20.02), each with a narrowing locus, confirming the same convergence behavior.
- Block7_union_row12 required iterations 1 and 2 (trial:i01.ug.Block7_union_row12.02, trial:i02.ug.Block7_union_row12.01); Block7_union_row15 required iterations 1 and 2 (trial:i01.ug.Block7_union_row15.05, trial:i02.ug.Block7_union_row15.03); Block7_union_row9 required iterations 1 and 2 (trial:i01.ug.Block7_union_row9.21, trial:i02.ug.Block7_union_row9.06); leaf_0002 required iterations 1 and 3 (trial:i01.ug.leaf_0002.23, trial:i03.ug.leaf_0002.04).

## New In-Crop Violations Introduced by Accepted Repairs

Multiple accepted repairs introduced new V1 violations within the crop region (n_new_in_crop > 0) and were still gated in because connectivity was preserved (conn_preserved=true). The highest count was 9 new in-crop violations for trial:i01.ug.Block7_union_row21.11, which used only two move_instance operations with x+36 each. Trials trial:i02.ug.leaf_0017.09, trial:i02.ug.leaf_0022.10, and trial:i03.ug.leaf_0007.05 each introduced 3 new in-crop violations. Single-step instance moves on dense V1 tracks produce secondary V1.S.1 violations at immediately adjacent via sites; those sites become the target of the subsequent iteration.

## Geometry Constraints Inferred from Rule Interaction

**V1.W.1 and V1.M2.AUX.2 interact**: V1.M2.AUX.2 requires V1 to be exactly the same width as M2 in the direction perpendicular to M2 length. Because M2 runs horizontally, the perpendicular direction is y. Y-axis resize_end operations on M2 polygons (trial:i02.ug.Block7_union_row15.03 y+96 resize, trial:i03.ug.leaf_0007.05 y-48 on both ends of p3592) bring M2 y-extents into alignment with repositioned V1 y-positions, satisfying both rules simultaneously. Any M2 y-extent below 18 dbu would simultaneously violate V1.W.1 and must be resized to at least 18 dbu.

**V1.M2.EN.2 and the 5&0 nm end-cap distinction**: The rule allows either 5&5 nm or 5&0 nm enclosure. The 5&0 nm option (via edge coincident with M2 edge) is the flush condition tested by v1_full_flush_m2 in V1.S.1 and determines which spacing mask (v1_nec vs v1_wec path) applies to a given via. Trials consistently resize M2 ends in multiples of 4 dbu (trial:i01.ug.Block7_union_row10.00 x+308, trial:i02.ug.Block7_union_row9.06 x+112, trial:i02.ug.Block7_union_row22.05 x+92), maintaining the net enclosure above the 5 nm threshold.

**V1.M1.EN.1 is satisfied through instance-level moves**: All instance moves carry M1 with them as a rigid body (M1 is in touched_layers for every trial). No standalone M1 resize_end operations appear in the history. M1 enclosure compliance is maintained automatically when the entire instance is moved, not through direct M1 polygon edits.

**V1.AUX.1 is restored by M2 patch addition**: The add_polygon strategy in trial:i01.ug.Block7_union_row20.10 is the only observed direct fix for a V1 falling outside M2. Moving an instance without also extending or patching M2 violates V1.AUX.1; the inserted patch polygon re-establishes the M1 ∩ M2 intersection condition required by the rule.

## NONORTHOGONAL Constraint

No nonorthogonal geometry was introduced in any trial. All add_polygon operations use axis-aligned rectangles (trial:i01.ug.Block7_union_row20.10 M2 patch, trial:i03.ug.leaf_0002.04 M3 patch), and all resize operations use axis-constrained directions (x or y only, never diagonal). The NONORTHOGONAL rule is satisfied automatically when all V1 repair geometry remains axis-aligned.