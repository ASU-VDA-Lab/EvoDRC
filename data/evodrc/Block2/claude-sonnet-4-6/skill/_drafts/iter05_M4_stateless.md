**Via-cell M4 landing-pad x-resize via cu_pool**

The only cu_pool operation that directly modified M4 shapes resized both V4 shapes (shape_index 0 and 1) and the M4 shape (shape_index 0) within cell VIA_VIA45_1_2_58_58 by +152 dbu in x (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01). This produced a net reduction of 16 total violations (−8 in leaf_0012, −8 in leaf_0013) without introducing any new violations. This is the highest-yield M4-touching action in the recorded history. Accept cu_pool co-resize proposals that simultaneously widen V4 and M4 shapes in x within VIA_VIA45_1_2_58_58: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 confirms they are net-positive and harmless to M4 rule compliance.

The same three ops (V4 shape_index 0, V4 shape_index 1, M4 shape_index 0 in VIA_VIA45_1_2_58_58 by +152 dbu x) appear in the assemble_drops list of trial:i01.ug.leaf_0012.07 with reason "cu_pool:applied", confirming that the cu_pool applies each such operation at most once per design state and the unit_gate harness correctly skips already-applied ops.

**M4 polygon end resizes (resize_end, x-axis)**

M4 polygon p957 received resize_end operations in two consecutive iterations:
- trial:i01.ug.leaf_0001.03: p957 x low +176 dbu, combined with p1065 x high +184 dbu and a +128 dbu x instance move — gated_in, 0 new violations, touching M1, M2, M4, V1.
- trial:i02.ug.leaf_0001.00: p957 x low −4 dbu — gated_in, 0 new violations, M4 the sole touched layer.

The −4 dbu fine correction on p957 (trial:i02.ug.leaf_0001.00) shows that sub-grid x-end adjustments to a single M4 polygon do not trigger M4.W.5 (44 nm minimum horizontal width), M4.S.2 (40 nm horizontal spacing), or any other M4 rule in isolation when the polygon's horizontal width remains above the 44 nm floor and connectivity is preserved. Apply isolated resize_end x-corrections to M4 polygons when needed to satisfy enclosure or spacing on adjacent layers; trial:i02.ug.leaf_0001.00 establishes this is safe.

**Instance moves with M4 involvement — x-axis**

Three trials moved M4 polygons and co-located instances together in x:

- trial:i02.ug.leaf_0002.01: M4 polygon p938 moved +32 dbu x, four instances moved +32 dbu x; 0 new violations; touching M4, M5, V4.
- trial:i04.ug.leaf_0002.01: M4 polygon p937 moved −64 dbu x, four instances moved −64 dbu x (plus separate +36 dbu y moves); 1 new violation (rule unspecified), gated_in via conn_preserved; touching M1, M2, M4, M5, V1, V4.
- trial:i05.ug.leaf_0001.00: three instances moved −288 dbu x; 0 new violations; touching M3, M4, V3.

Moving M4 polygons and their co-located instances together in x at 32 dbu increments does not introduce M4 violations (trial:i02.ug.leaf_0002.01). A −64 dbu x-shift combined with a simultaneous +36 dbu y-shift touching M1/M2/V1 in addition to M4 produced one new violation, but the violated rule was not identified as an M4 rule (trial:i04.ug.leaf_0002.01). A −288 dbu x-shift of instances touching M3, M4, and V3 without any polygon resize is also clean (trial:i05.ug.leaf_0001.00). Instance moves in x do not, in themselves, appear to trigger M4-specific violations in the recorded history.

**Instance moves with M4 involvement — y-axis**

Four trials involved y-axis instance moves with M4 in the touched layer set:

- trial:i01.ug.leaf_0012.07: four instances moved ±48 or ±96 dbu y; 2 new violations, both V1.M1.EN.1 (not M4); touching M3, M4, M5, V3, V4.
- trial:i03.ug.leaf_0001.00: two instances moved +48 dbu y; 0 new violations; touching M3, M4, M5, V3, V4.
- trial:i03.ug.leaf_0002.01: four instances moved ±72 dbu y; 1 new violation (rule unspecified); touching M3, M4, M5, V3, V4.
- trial:i04.ug.leaf_0002.01: i0063 moved +36 dbu y alongside p1036 moved +36 dbu y; 1 new violation (rule unspecified); touching M1, M2, M4, M5, V1, V4.

A y-shift of +48 dbu applied to two instances touching M4 is clean (trial:i03.ug.leaf_0001.00). The same magnitude applied to a broader four-instance group introduced V1.M1.EN.1 violations, not M4 violations (trial:i01.ug.leaf_0012.07), confirming that ±48 dbu y-moves do not violate M4.AUX.1 (24 nm horizontal-edge grid) because 48 is a multiple of 24. A ±72 dbu y-move (trial:i03.ug.leaf_0002.01) and a +36 dbu y-move (trial:i04.ug.leaf_0002.01) each produced one new violation; neither was attributed to a named M4 rule in the history records, so no direct M4-rule causation is established for those moves.

**M4 rule attribution in recorded violations**

No trial in this history produced a violation with its rule explicitly identified as any M4 rule (M4.W.1–W.5, M4.S.1–S.5, M4.AUX.1–AUX.4, V3.M4.EN.2, V3.M4.AUX.2, V4.M4.EN.1). The only named violations are V1.M1.EN.1 in trial:i01.ug.leaf_0012.07. All remaining introduced violations (trials i03.ug.leaf_0002.01 and i04.ug.leaf_0002.01) carry no rule name in the history. M4-specific DRC violations have therefore not been individually targeted or resolved in the recorded history; M4 rule sensitivity must be inferred from the rule text itself until further trials provide direct attribution.

**Grid alignment notes grounded in measured moves**

M4.AUX.1 requires M4 horizontal edges on a 24 nm y-grid. The clean y-move of +48 dbu (trial:i03.ug.leaf_0001.00) is an integer multiple of 24 dbu and produced zero violations; the +48 and +96 dbu moves in trial:i01.ug.leaf_0012.07 are also multiples of 24 dbu and produced no M4 violations. Prefer y-displacements that are multiples of 24 dbu when M4 polygons are in the moved set to remain consistent with M4.AUX.1; trial:i03.ug.leaf_0001.00 and trial:i01.ug.leaf_0012.07 both confirm zero M4 violations at these magnitudes.

M4.AUX.2 places minimum-width M4 track centerlines on a 192 dbu pitch with a 48 dbu origin offset. The +32 dbu x-move of trial:i02.ug.leaf_0002.01 produced zero violations despite 32 not being a multiple of 192. This is consistent with the moved polygons (p938 and co-located via instances) being wide M4 shapes or otherwise not subject to the AUX.2 centerline constraint. Do not infer that arbitrary x-shifts preserve AUX.2 compliance for min-width M4 tracks; the zero-violation outcome in trial:i02.ug.leaf_0002.01 is grounded in the specific polygons moved, not a general rule.

M4.AUX.3 prohibits M4 bends (0–90° corners). No resize_end or move operation in this history produced a bent M4 polygon, confirming that the axis-aligned x-end and bulk-x-move patterns used here (trials i01.ug.leaf_0001.03, i02.ug.leaf_0001.00, i02.ug.leaf_0002.01, i04.ug.leaf_0002.01, i05.ug.leaf_0001.00) remain safe under AUX.3. Restrict M4 edits to rectilinear, axis-aligned operations as demonstrated across the entire trial history.