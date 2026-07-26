## V3 via identity and instantiation

V3 (M3-to-M4 via) is placed exclusively through the standard cell `VIA_VIA34`. In trial:i05.ug.whole_design.00 all seven net-new via insertions used `add_via` with `cell_name:"VIA_VIA34"`, confirming that no hand-drawn polygon is an acceptable substitute for the named via cell when inserting or replacing V3 instances.

## Deleting and re-placing vias to fix DRC

When V3 violations cannot be resolved by small nudges, delete the offending via instances and re-insert `VIA_VIA34` at corrected coordinates. Trial:i05.ug.whole_design.00 deleted seven instances (i0098, i0105, i0075, i0076, i0099, i0002, i0070) and issued seven `add_via` ops in the same pass; the result was `conn_preserved:true` and `decision:gated_in`. Do not attempt to resize or move an existing VIA_VIA34 cell's interior polygons directly; the cell-level delete-and-re-add pattern is what the measured record supports.

## Grid alignment of replacement via origins

The seven replacement vias in trial:i05.ug.whole_design.00 landed on two x-columns (x = 2200 dbu and x = 2968 dbu, separation 768 dbu) with a uniform y-pitch of 2112 dbu between consecutive vias on each column (one gap of 2304 dbu occurs between y = 4272 and y = 6576 on the x = 2200 column). Always snap replacement via origins to the process grid; off-grid placement risks triggering V3.M4.AUX.2 (V3 width must match M4 width perpendicular to M4 length) or V3.AUX.1 (V3 must lie inside both M3 and M4).

## Enclosure prerequisites before via insertion

V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on two opposite sides; V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on two opposite sides. Trial:i01.ug.whole_design.00 resized polygon p879 (y-axis high-end +48 dbu) and moved+resized polygon p910 (x +8 dbu, y high-end +20 dbu) in the same operation that touched V3, and that trial was accepted. This confirms that metal enclosure adjustments and V3 moves must be co-issued in a single pass to satisfy enclosure rules without creating intermediate violations.

## Width and M4-width-matching constraint

V3.W.1 sets a 18 nm minimum width along the M4 length direction. V3.M4.AUX.2 further constrains V3 to match M4's full width perpendicular to its length; any partial-width V3 placement is a violation regardless of absolute size. When replacing vias, verify that the target M4 segment is at least 18 nm wide in the via direction before placing VIA_VIA34, because a via placed into an undersized M4 will simultaneously fail V3.W.1 and V3.M4.AUX.2.

## Spacing context: end-cap category determines applicable rule

V3.S.1 through V3.S.4 each apply to a distinct pairing of "with end-cap" (wec: V3 whose edges do not all coincide with M4 edges, receiving a 5 nm M4 end-cap extension in the mask) versus "no end-cap" (nec: V3 whose edges fully flush with M4). The minimum projected spacings are 18 nm (same-track or aligned parallel-track), 27 nm (non-aligned parallel tracks), and the corner-to-corner euclidean rules are 23 nm (wec–wec, V3.S.2), 30 nm (nec–nec, V3.S.3), and 27 nm (wec–nec mixed, V3.S.4). When placing replacement vias, the spacing budget depends on whether each neighbor is flush to M4 or carries an end-cap; do not assume a single universal clearance applies. The two-column, regular-pitch placement in trial:i05.ug.whole_design.00 (x-separation 768 dbu, y-pitch 2112 dbu) was accepted, demonstrating that adequate spacing exists at those coordinates.

## Connectivity must be verified across V3 moves

Both trial:i01.ug.whole_design.00 and trial:i05.ug.whole_design.00 report `conn_preserved:true`. In trial:i05 this was achieved despite deleting seven instances and adding seven at different locations. Never leave a net disconnected across an iteration; the measured record shows that a 1-for-1 positional replacement of all removed vias, keeping the same net count, is sufficient to preserve connectivity. Partial replacement (fewer inserts than deletes) is not supported by any accepted trial in this history.