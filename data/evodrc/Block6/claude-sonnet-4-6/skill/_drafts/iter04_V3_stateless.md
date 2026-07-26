## V3 layer topology and co-layer constraints

V3 is a via layer connecting M3 (below) and M4 (above). Rule V3.AUX.1 requires every V3 polygon to lie fully inside the intersection of M3 and M4. Rule V3.M4.AUX.2 additionally constrains V3 to exactly match M4's width in the direction perpendicular to M4's run — V3 must not undercut or overhang M4 laterally on either side.

Every accepted repair that touched V3 also modified M3 and M4 simultaneously. This holds for single-instance moves (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00) and for large multi-instance coordinated operations (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). Never attempt to reposition V3 geometry without verifying the corresponding M3 and M4 geometry; all four accepted operations co-modified both enclosing metal layers (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00).

When inter-layer adjustments propagate upward from M4 into M5, V4 appears in the touched-layers list alongside V3 (trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01). Upward propagation is not required for repairs confined to the M3/M4/V3 stack (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00).

## V3 width rule (V3.W.1)

The minimum V3 width along the M4 run direction is 18 nm. Because V3.M4.AUX.2 forces V3 to exactly match M4's width in the perpendicular direction, the only free width dimension is the one parallel to M4's axis. Resize_end operations on M4 polygon ends (trial:i02.ug.leaf_0010.06) that lengthen or shorten M4 along its run extend V3's effective footprint in that direction and must keep the parallel dimension at or above 18 nm.

## Enclosure rules

**V3.M3.EN.1** requires M3 to enclose V3 by at least 5 nm on at least one pair of opposite sides (left+right or top+bottom). A V3 shifted so that M3 enclosure falls below 5 nm on both ends of both axes simultaneously violates this rule. Y-axis group moves of ±24 dbu and ±72 dbu were accepted and kept all moved instances inside their enclosing M3 polygons (trial:i02.ug.leaf_0010.06). Y-axis moves of ±48 dbu and ±96 dbu were likewise accepted without M3 enclosure violations (trial:i03.ug.leaf_0002.01).

**V3.M4.EN.2** requires M4 to enclose V3 by at least 11 nm on at least one pair of opposite sides. The 11 nm threshold exceeds the 5 nm M3 enclosure threshold, making V3.M4.EN.2 the binding enclosure constraint when the M4 segment is short. X-axis moves of -16 dbu were accepted in two independent single-instance repairs without producing M4 enclosure violations (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00), confirming that the available M4 segments accommodated that displacement.

## End-cap classification: WEC vs NEC

The V3 spacing rules V3.S.1 through V3.S.4 depend on whether each V3 instance has a 5 nm M4 end-cap. The classification is derived purely from geometric edge coincidence:

- **NEC** (no end-cap): every V3 edge is coincident with an M4 edge — the via reaches all four sides of its M4 bounding box. The DRC mask for NEC instances is the V3 polygon sized outward by 5 nm.
- **WEC** (with end-cap): at least one V3 edge is not coincident with M4. The DRC mask extends only the coincident M4 edges by 5 nm outward along the M4 run direction.

Because V3.M4.AUX.2 forces the two lateral (perpendicular-to-run) V3 edges to exactly coincide with M4 edges, the non-coincident edges, when present, are exclusively the two ends along the M4 run direction. A V3 that sits away from both tips of its M4 segment is WEC; a V3 whose end edges align with M4 tips is NEC.

## Spacing rules (V3.S.1 through V3.S.4)

**V3.S.1** uses projection-based spacing on the combined v3_mask geometry. Three effective thresholds apply:

- Same M4 track (v3_nec_mask_nm4 vertical edges, 90° angle): 17 nm minimum projection spacing.
- v3_maskav non-M4 edges: 18 nm minimum projection spacing.
- v3_mask general: 1 nm minimum projection spacing (catches mask self-intersection artifacts).

The 5 nm mask extension means the effective keep-out around each V3 instance extends beyond the drawn outline before the spacing check fires.

**V3.S.2** (23 nm corner-to-corner): fires when both V3 instances are WEC. The euclidean check catches only those edge pairs not already covered by the projection check — true diagonal corner-to-corner scenarios. The 16.4 nm euclidean threshold on the WEC mask geometry corresponds to a 23 nm corner-to-corner spacing on drawn V3.

**V3.S.3** (30 nm corner-to-corner): fires when both V3 instances are NEC. The 16.12 nm euclidean threshold on the NEC-sized-by-5 nm mask corresponds to 30 nm on drawn V3. This is the most restrictive corner-to-corner threshold.

**V3.S.4** (27 nm corner-to-corner): fires for one WEC and one NEC instance. The 17.11 nm euclidean separation threshold on the respective masks corresponds to 27 nm on drawn V3.

Group y-axis moves used in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01 adjusted inter-instance spacing along the M4 run direction across multiple instances simultaneously while preserving connectivity, confirming that coordinated group moves are the correct mechanism when multiple V3 instances on the same or adjacent tracks are in violation.

## Move magnitudes in accepted repairs

**Single-instance x-axis moves:** A displacement of -16 dbu was accepted in two independent leaf repairs that each touched only M3, M4, and V3 (trial:i02.ug.leaf_0003.03, trial:i04.ug.leaf_0001.00). Both operations moved exactly one instance with n_ops = 1 and introduced one new in-crop DRC reduction each, confirming the displacement is sufficient to clear the violation without creating new ones.

**Multi-instance y-axis moves:** Four step sizes were accepted across the two large coordinated operations:
- ±24 dbu: accepted in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01.
- ±48 dbu: accepted in trial:i03.ug.leaf_0002.01.
- ±72 dbu: accepted in trial:i02.ug.leaf_0010.06 and trial:i03.ug.leaf_0002.01.
- ±96 dbu: accepted in trial:i03.ug.leaf_0002.01.

In trial:i02.ug.leaf_0010.06, instance moves were paired with resize_end operations on enclosing polygon ends (y-axis, both high and low ends), keeping M3/M4 enclosure valid as the V3-bearing instances shifted. Use resize_end operations on the enclosing metal end that moves with the instance to preserve enclosure when the instance displacement is large enough to shrink M3 or M4 coverage below the V3.M3.EN.1 or V3.M4.EN.2 thresholds (trial:i02.ug.leaf_0010.06).

## Operation types and geometry orthogonality

The NONORTHOGONAL rule prohibits any V3 edge at angles other than 0° or 90°. All operation types used across accepted repairs are move_instance and resize_end; both produce only axis-aligned geometry by construction. Every accepted trial applied exclusively these two operation types (trial:i02.ug.leaf_0003.03, trial:i02.ug.leaf_0010.06, trial:i03.ug.leaf_0002.01, trial:i04.ug.leaf_0001.00). No operation type that could introduce a diagonal edge appeared in any accepted repair.