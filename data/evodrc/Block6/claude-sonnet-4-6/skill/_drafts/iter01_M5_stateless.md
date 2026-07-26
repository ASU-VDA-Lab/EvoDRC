## Via Enclosure Repairs: Adjust Via Geometry, Not M5

Both measured trials on M5 involved via enclosure violations repaired entirely through via-side geometry changes, with no M5 shape operations performed. M5 was listed in `touched_layers` for both trials but received zero ops, confirming that M5 geometry was compliant and the source of violations was via placement and sizing within the existing M5 context.

**V4.M5.EN.2 and V4.M5.AUX.2 — via re-centering and width match (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01)**

Rule V4.M5.EN.2 requires 11 nm enclosure of V4 by M5 on two opposite sides. Rule V4.M5.AUX.2 additionally requires V4 to be exactly the same width as M5 along the direction perpendicular to M5 length. In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, both conditions were violated due to off-center V4 sub-shape placement. The repair moved V4 sub-shapes by ±116 dbu on the x-axis to re-center them within the M5 track, then resized each V4 sub-shape by +384 dbu on the x-axis to bring its width into exact agreement with the M5 track width as required by V4.M5.AUX.2. An M4 shape was also resized (+152 dbu, x-axis) as a co-adjustment. This set of 5 ops reduced total violations by 52 (−28 in unit:leaf_0019, −24 in unit:leaf_0020) and was applied.

Do not attempt to widen M5 to resolve V4.M5.EN.2 or V4.M5.AUX.2 violations: M5 width changes risk triggering M5.W.1 (24 nm minimum horizontal width), M5.W.2 (480 nm maximum horizontal width), M5.W.3 (even-multiple-of-minimum-width prohibition), M5.W.4 (even-number-of-minimum-tracks prohibition), and M5.AUX.4 (wide M5 outside edge must not touch a routing track edge). trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 demonstrates that re-centering and resizing the via is sufficient.

**V5.M5.EN.1 — V5 re-centering and resizing (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02)**

Rule V5.M5.EN.1 requires 11 nm enclosure of V5 by M5 on at least two opposite sides. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, a 4-cut V5 via cell (VIA_VIA56_2_2_66_58) violated this rule. The repair applied the same pattern: all four V5 sub-shapes were moved by ±116 dbu on the x-axis to re-center them, and all four were resized by +320 dbu on the x-axis. No M5 or M6 ops were issued despite both appearing in `touched_layers`. The 8-op repair reduced total violations by 16 (−8 in unit:leaf_0019, −8 in unit:leaf_0020) and was applied.

The ±116 dbu centering offset and the +320 dbu / +384 dbu resize amounts differ between the V4 and V5 via cells, reflecting cell-specific cut geometry rather than any difference in the underlying M5 track width requirement. The ±116 dbu lateral displacement is the consistent signature of an off-center via placement that breaks the two-sided enclosure check.

**Grid and routing track constraints on M5**

M5 vertical edges must lie on a 24 nm horizontal grid (M5.AUX.1). Minimum-width (24 nm) M5 tracks must be centered on vertical routing tracks spaced at 192 dbu pitch with a 48 dbu offset from the origin (M5.AUX.2). M5 may not contain any bend or corner (M5.AUX.3). These constraints apply to any M5 shape that might be introduced or modified during via repair; neither trial modified M5, so no grid or routing-track violations were introduced.

**Parallel run length and spacing**

M5.S.5 requires a minimum parallel run length of 44 nm between M5 polygons on adjacent tracks. M5.S.1 and M5.S.2 set minimum horizontal (24 nm) and vertical (40 nm) spacing. M5.S.3 sets minimum tip-to-tip spacing of 40 nm on adjacent tracks without shared parallel run length; M5.S.4 sets the same 40 nm minimum for polygons that do share parallel run length. Neither trial triggered or resolved any of these rules, and no M5 moves were made, so no spacing relationships were altered.