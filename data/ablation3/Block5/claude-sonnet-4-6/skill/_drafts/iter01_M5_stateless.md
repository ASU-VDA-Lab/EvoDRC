## Width Constraints

**M5.W.1 — Minimum horizontal width: 24 nm.**
M5 horizontal widths are checked in projection mode against 90-degree (vertical) edges. Never reduce the horizontal span of an M5 polygon below 24 nm. Instance x-moves applied in trial:i01.ug.whole_design.00 (e.g., i0012 +136 dbu, i0103 -28 dbu) adjusted inter-polygon horizontal separation without narrowing wires.

**M5.W.2 — Maximum horizontal width: 480 nm.**
Horizontal widths above 480 nm are illegal. Do not resize M5 polygons wider than 480 nm in x.

**M5.W.3 — Forbidden even-multiple horizontal widths.**
Widths that are exact even integer multiples of 24 nm are illegal: 48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm. When correcting a width to clear M5.W.1, skip past these values; valid target widths include 24, 72, 120, 168, 216, 264, 312, 360, 408, 456 nm among odd multiples of 24 nm.

**M5.W.4 — Forbidden even-track-spanning horizontal widths.**
Widths of 72, 168, 264, 360, and 456 nm are additionally forbidden because they span an even number of minimum-width routing tracks. These overlap with part of the M5.W.3 odd-multiple set and must also be avoided when targeting a corrective width.

**M5.W.5 — Minimum vertical width: 44 nm.**
Vertical (y-direction) widths below 44 nm trigger M5.W.5. In trial:i01.ug.whole_design.00, polygon p910 received a `resize_end` of +20 dbu on its high-y end, extending the vertical span of the polygon. Apply vertical end-extension (high or low end) when correcting M5.W.5 violations; the target span must reach at least 44 dbu.

## Spacing Constraints

**M5.S.1 — Minimum horizontal spacing: 24 nm.**
Horizontal gaps between any two M5 polygons must be at least 24 nm, measured in projection mode against vertical edges. The rule is also enforced Euclidean (1 nm gap catches all near-touching cases). Instance x-moves in trial:i01.ug.whole_design.00 (i0012 +136 dbu, i0103 -28 dbu, i0061 +8 dbu, i0104 +8 dbu) were the primary horizontal-separation corrections; use instance moves to open horizontal gaps when M5.S.1 is violated by net-level congestion.

**M5.S.2 — Minimum vertical spacing: 40 nm.**
Vertical gaps between M5 polygon edges must be at least 40 nm. In trial:i01.ug.whole_design.00, polygon p879 received a `resize_end` of +48 dbu on its high-y end, and multiple instances were displaced vertically (i0113 +72 dbu, i0099 +72 dbu, i0112 -48 dbu, i0105 -48 dbu, i0067 -24 dbu, i0070 -24 dbu, i0062 +48 dbu, i0076 +48 dbu, i0001 +24 dbu, i0002 +24 dbu, i0073 +96 dbu, i0075 +96 dbu). Both instance moves and direct polygon end-extension resolved vertical crowding; prefer instance moves when several nets need coordinated vertical separation, and reserve direct polygon resize for isolated single-polygon adjustments.

**M5.S.3 — Adjacent-track tip-to-tip spacing (no shared parallel run): 40 nm.**
When two M5 polygons on adjacent horizontal tracks do not share any parallel run length, their tip-to-tip clearance must be at least 40 nm. The checker internally sizes the polygon +48 dbu in x before testing, so effective susceptibility extends 48 dbu beyond the literal tip. Do not position M5 polygon tips within 40 nm of a neighboring tip on an adjacent track.

**M5.S.4 — Adjacent-track tip-to-tip spacing (shared parallel run): 40 nm.**
When two M5 polygons sharing a parallel run on adjacent tracks have their horizontal (0-degree) tip edges within 30 dbu of each other (the tip extension region), the facing-tip gap must be at least 40 nm. Apply the same 40 nm clearance target as M5.S.3.

**M5.S.5 — Minimum parallel run length: 44 nm.**
When two M5 polygons on adjacent tracks are within 24 nm of each other horizontally, the vertical overlap (parallel run length) must be at least 44 nm. In trial:i01.ug.whole_design.00, p879 was extended +48 dbu vertically (high end) and p910 was extended +20 dbu vertically (high end); vertical end-extension is effective for increasing parallel run length to clear M5.S.5.

## Grid and Routing-Track Alignment

**M5.AUX.1 — Vertical edges on 24 nm x-grid.**
All M5 vertical edges must lie at x-coordinates that are multiples of 24 nm (24 dbu if 1 dbu = 1 nm). After any x-axis move or horizontal resize of an M5 polygon, verify that all resulting vertical edge x-coordinates satisfy `x mod 24 == 0`. In trial:i01.ug.whole_design.00, polygon p910 was moved +8 dbu in x alongside multiple instance moves; the trial resolved with conn_preserved=true and no new DRC crop violations, so the net absolute position remained AUX.1-compliant within the instance coordinate context.

**M5.AUX.2 — Minimum-width track centerlines on routing-track grid.**
1x (minimum-width) M5 tracks — those not covered by an erosion-then-dilation at 13 nm — must have their x-centerlines at positions satisfying `(centerline - 48) mod 192 == 0 dbu`, subject to base-width qualification at 96 dbu. Do not move minimum-width M5 polygons to x positions that violate this alignment. The instance moves in trial:i01.ug.whole_design.00 preserved routing-track alignment, as connectivity and crop-boundary validity were maintained (conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0).

**M5.AUX.3 — M5 may not bend.**
M5 polygons with any corner angle between 0 and 90 degrees trigger M5.AUX.3. Never introduce L-shapes, T-shapes, or any non-rectilinear routing bends in M5. All operations in trial:i01.ug.whole_design.00 used linear moves and single-axis end-extensions, which preserve the rectilinear shape of M5 polygons.

**M5.AUX.4 — Wide M5 outside edges must not touch routing-track edges.**
Wide M5 polygons (horizontal width > 24 nm, i.e., those that survive a 13 nm x-erosion) must not have their vertical edges coincide with any 1x-track boundary from the AUX.2 grid. When resizing or moving wide M5 polygons horizontally, avoid placing their left or right edges on AUX.2 routing-track x-positions.

## Via Enclosure

**V4.M5.EN.2 — V4 enclosed by M5 at least 11 nm on two opposite sides.**
V4 vias inside M5 must be enclosed by at least 11 nm in both x and y. When instance moves or polygon resizes shift M5 relative to V4 positions, preserve the 11 nm two-sided enclosure. In trial:i01.ug.whole_design.00, V4 was among the touched layers and the result was conn_preserved=true; the coordinate moves applied (including y-axis end-extensions and x-axis instance shifts) maintained valid V4.M5.EN.2 enclosure throughout.

**V4.M5.AUX.2 — V4 width must exactly match M5 width in the perpendicular direction.**
Each V4 via must be exactly as wide as the M5 it sits on in the direction perpendicular to M5's length (i.e., perpendicular to the run direction). Resizing an M5 polygon's horizontal span without correspondingly adjusting V4 horizontal extent will trigger this rule. In trial:i01.ug.whole_design.00, all M5 resize operations were on the y-axis (vertical end-extensions on p879 and p910); no x-axis M5 width changes were made to M5 polygons carrying V4 vias, keeping V4 and M5 width-matched in the perpendicular direction.

**V5.M5.EN.1 — V5 enclosed by M5 at least 11 nm on two opposite sides.**
V5 vias inside M5 must also be enclosed by at least 11 nm on two opposite sides in both x and y. Apply the same enclosure-preservation check as V4.M5.EN.2 for any M5 move or resize that could shift M5 relative to resident V5 vias.

## Non-Orthogonal Geometry

M5 edges must be strictly horizontal (0 degrees) or vertical (90 degrees); any edge at 1–89, 91–179, or their negative equivalents triggers `M5.GEOMETRY.NONORTHOGONAL`. Never produce non-rectilinear M5 shapes. The repair operations in trial:i01.ug.whole_design.00 — linear instance moves and single-axis `resize_end` — produce only axis-aligned geometry and preserve polygon orthogonality.