**Instance translation on M1: X-axis shifts in the range ±36 to ±72 dbu preserve all M1 DRC rules**

In trial:i03.ug.whole_design.00, 32 instance moves used ±64 dbu X displacements. In trial:i05.ug.whole_design.00, 22 operations used a wider range of X displacements: instance moves at +48, +44, and +36 dbu (positive direction) and −72, −72, and −64 dbu (negative direction). Both trials were accepted with `conn_preserved=true`, `n_new_in_crop=0`, and `n_new_out_of_crop=0`, confirming no new violations under any active M1 rule (V0.M1.EN.1, V0.M1.AUX.3, M1.W.1, M1.S.1 through M1.S.6, M1.A.1, M1.R.0, V1.M1.EN.1, and GEOMETRY.NONORTHOGONAL). The observed safe range of X translation magnitudes now spans 36–72 dbu in both directions; displacements outside this range are untested.

**Asymmetric move sets (mixed +/− X, variable magnitudes) do not inherently break M1 enclosure or spacing**

trial:i03.ug.whole_design.00 demonstrated a 32-instance mixed-direction X translation at ±64 dbu with zero new enclosure violations. trial:i05.ug.whole_design.00 extended this to a 22-operation mixed set with positive moves at 36, 44, and 48 dbu and negative moves at −64 and −72 dbu, also producing zero new violations. Do not assume asymmetric multi-instance translations at variable magnitudes are unsafe for M1 enclosure — both trials confirm this pattern is clean.

**resize_end (polygon endpoint extension) on the M1 x-axis high end at +44 dbu is safe under all M1 DRC rules**

trial:i05.ug.whole_design.00 introduced a new operation type not seen in prior iterations: `resize_end` on polygons p1255, p1270, p1295, p1309, and p1320, each extending the high end of the x-axis by 44 dbu. These five resize operations were interleaved with instance moves in the same 22-operation batch. The trial was accepted with zero new violations, confirming that extending M1 polygon endpoints by 44 dbu in the +X direction does not violate M1.W.1, M1.S.1–M1.S.6, M1.A.1, V0.M1.EN.1, V0.M1.AUX.3, V1.M1.EN.1, M1.R.0, or GEOMETRY.NONORTHOGONAL. Only +44 dbu high-end X extensions have been measured; other axes, ends, or magnitudes for resize_end are untested.

**Combining instance moves and polygon resize_end in a single operation batch is safe for M1**

trial:i05.ug.whole_design.00 applied 17 move_instance operations and 5 resize_end operations in a single batch across the whole design. The batch was accepted with no new violations. Mixed batches of moves and resizes do not inherently introduce M1 rule conflicts, as confirmed by trial:i05.ug.whole_design.00.

**No M1 area or width regressions from instance-level X translations or +44 dbu high-end X resizes**

M1.W.1 (minimum width 18 nm) and M1.A.1 (minimum area 504 nm²) both remained violation-free after the 32-move operation in trial:i03.ug.whole_design.00 and after the 22-operation mixed batch (including 5 resize_end at +44 dbu) in trial:i05.ug.whole_design.00. Instance translations that preserve internal cell geometry do not alter intra-cell M1 widths or areas; high-end X extensions increase polygon area and width, moving them further from the minimum thresholds. Only reductions in M1 width or area are at risk for these rules.

**M1 spacing rules (M1.S.1 through M1.S.6) survived mixed ±36–72 dbu X translations and +44 dbu resizes**

All tip-to-side (M1.S.2, 25 nm minimum), tip-to-tip (M1.S.3, 27 nm; M1.S.4, 31 nm; M1.S.5, 31 nm), side-to-side (M1.S.1, 18 nm), and corner-to-corner (M1.S.6, 20 nm) spacing rules remained clean in trial:i03.ug.whole_design.00 and trial:i05.ug.whole_design.00. The observed displacement range (36–72 dbu) and the +44 dbu high-end resize were each insufficient to close inter-cell or inter-polygon M1 gaps below any spacing threshold when starting from a clean baseline. A safe lower bound on translation or resize magnitude has not been established by these two trials.

**V0.M1.EN.1 and V1.M1.EN.1 (enclosure rules) are not disturbed by pure X-axis instance moves or X-axis high-end resizes**

In trial:i03.ug.whole_design.00, all 32 operations were X-axis translations and produced no new enclosure violations. In trial:i05.ug.whole_design.00, the 17 instance moves (X-axis only) and 5 resize_end operations (X-axis, high end, +44 dbu) also produced no new enclosure violations under V0.M1.EN.1 or V1.M1.EN.1. Preserve instance orientation and internal cell geometry; do not rotate or resize in the Y direction when the goal is translation-only or X-end-only repair.

**V0.M1.AUX.3 (V0 width matching) is not disturbed by pure X-axis instance moves or X-axis high-end polygon resizes**

V0.M1.AUX.3 requires that V0 width exactly match M1 width in the direction perpendicular to M1 length. trial:i03.ug.whole_design.00 confirmed this with 32 X-axis instance moves. trial:i05.ug.whole_design.00 confirmed this with 17 X-axis instance moves and 5 X-axis high-end resizes, none of which altered the perpendicular (Y-axis) dimension of any M1 polygon. Operations confined to the X axis do not affect the M1 Y-dimension and therefore do not risk V0.M1.AUX.3.

**M1.R.0 (redundant island detection) was not triggered by whole-design move-and-resize batches**

M1.R.0 flags M1 islands enclosing exactly one small V0 near large empty M1 regions. Neither trial:i03.ug.whole_design.00 nor trial:i05.ug.whole_design.00 created new M1.R.0 violations. Translations and X-axis high-end polygon extensions preserve the relative spatial relationship between M1 islands and surrounding empty regions. Do not generalize to arbitrary resize directions; only the tested operations (X-axis moves and +X high-end resizes) are confirmed clean.

**GEOMETRY.NONORTHOGONAL: all-orthogonal moves and axis-aligned resizes produce no nonorthogonal edges**

All operations in trial:i03.ug.whole_design.00 (32 rectilinear X translations) and trial:i05.ug.whole_design.00 (17 rectilinear X translations, 5 X-axis high-end resizes) were axis-aligned. No GEOMETRY.NONORTHOGONAL violations were introduced on M1 in either trial. Use only axis-aligned (0°/90°) translations and axis-aligned resize_end operations when repairing M1; any rotation or diagonal displacement risks GEOMETRY.NONORTHOGONAL on M1 edges.