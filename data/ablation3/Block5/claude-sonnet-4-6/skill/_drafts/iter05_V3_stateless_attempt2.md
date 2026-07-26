## Via Instantiation

V3 vias are placed by instantiating the cell `VIA_VIA34` via `add_via` operations, not by editing raw polygons. In trial:i05.ug.whole_design.00, seven new vias were placed using `add_via` with `cell_name:"VIA_VIA34"` at explicit `origin_dbu` coordinates. Do not attempt to construct V3 geometry from scratch as a freestanding polygon; always use `VIA_VIA34` cell placements.

When replacing a via, the stale instance must be removed before the new one is placed. In trial:i05.ug.whole_design.00 seven `delete_instance` operations (i0098, i0105, i0075, i0076, i0099, i0002, i0070) were issued in the same op batch as the seven `add_via` operations. Leaving a displaced old instance in place while adding a replacement risks V3.S.1 and V3.S.2 spacing violations between the old and new placements.

## Metal Enclosure and Via Placement Must Be Co-Issued

In trial:i05.ug.whole_design.00, `resize_end` operations extending polygons p951 and p955 by 128 dbu in the x-axis (high end) were included in the same 19-op batch as the `add_via` placements. V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides, and V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. Because these enclosure constraints must be satisfied at the time DRC is evaluated, issue enclosing metal `resize_end` operations in the same batch as the corresponding `add_via` operations, as was done in trial:i05.ug.whole_design.00.

## Touched Layers

Both successful trials modified V3 together with M3 and M4 in a single batch. trial:i01.ug.whole_design.00 touched M1, M2, M3, M4, M5, V1, V2, V3, V4; trial:i05.ug.whole_design.00 touched M1, M2, M3, M4, V1, V3. Repairs to V3 placement consistently require concurrent changes to the bounding metal layers (at minimum M3 and M4) to satisfy V3.M3.EN.1, V3.M4.EN.2, V3.AUX.1, and V3.M4.AUX.2.

## V3.M4.AUX.2 — Width Match with M4

V3.M4.AUX.2 requires that V3 width exactly match the M4 width in the direction perpendicular to M4 length. In trial:i05.ug.whole_design.00, the `resize_end` ops on p951 and p955 extended M4 metal before via addition, establishing the correct M4 span before the VIA_VIA34 cell was dropped in. Placing a VIA_VIA34 instance without first confirming (or adjusting) M4 width in the perpendicular direction will produce V3.M4.AUX.2 violations.

## Spacing Rules — V3.S.1, V3.S.2, V3.S.3, V3.S.4

V3.S.1 encodes three spacing thresholds depending on M4 track alignment: 18 nm on the same M4 track, 27 nm between parallel non-aligned tracks, and 18 nm between aligned parallel tracks. V3.S.2 adds a 23 nm Euclidean corner-to-corner floor when both vias carry a 5 nm M4 end-cap (WEC classification in the DRC deck). V3.S.3 sets 30 nm corner-to-corner for two vias both lacking end-caps (NEC), and V3.S.4 sets 27 nm corner-to-corner for one WEC and one NEC pair.

In trial:i05.ug.whole_design.00 the seven `add_via` origin coordinates span y-values of 2160, 3312, 4272, 5424, 6576, 7536, and 8688 dbu at x-columns 2200 and 2968. The interleaved two-column placement pattern was retained across both the delete and re-add steps in a single batch, which preserved connectivity (conn_preserved: true) and passed DRC (decision: gated_in). When selecting origin coordinates for new VIA_VIA34 placements, respect the spacing floors above; the multi-column y-interleave pattern demonstrated in trial:i05.ug.whole_design.00 is a viable arrangement.

## V3.W.1 — Minimum Width

V3.W.1 requires at least 18 nm width along the M4 length direction. VIA_VIA34 cell geometry is fixed at instantiation time; if a V3.W.1 violation exists, it indicates the VIA_VIA34 cell itself is undersized or is being placed on an M4 segment that is narrower than 18 nm, which would also trigger V3.M4.AUX.2. Correct M4 width before via placement as demonstrated in trial:i05.ug.whole_design.00 (resize_end on p951, p955 before add_via).

## V3.AUX.1 — Containment in M3 and M4

V3.AUX.1 flags any V3 shape not fully inside the intersection of M3 and M4. In both trials, M3 and M4 modifications were issued alongside V3 changes and connectivity was preserved (trial:i01.ug.whole_design.00, trial:i05.ug.whole_design.00). Place VIA_VIA34 only at origins where the full cell footprint falls within both the M3 and M4 coverage areas after any enclosure-extending resize operations.

## Connectivity Preservation

Both trials achieved `conn_preserved: true` and `decision: gated_in`. In trial:i05.ug.whole_design.00, seven via deletions paired with seven new via placements at updated coordinates maintained full connectivity. When relocating a via, the new `add_via` origin must land on a coordinate where M3 and M4 overlap so that the net connections on both layers are maintained; the delete-then-re-add pattern within a single op batch, as used in trial:i05.ug.whole_design.00, satisfies this requirement.