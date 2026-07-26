## V5.M6.AUX.2 — Width-match repair via y-axis resize

V5.M6.AUX.2 requires each V5 shape to span the full width of the enclosing M6 stripe in the direction perpendicular to M6 length. The only applied fix in this layer's history addresses that violation by resizing V5 shapes along the y-axis. In trial:i01.cu.def:VIA_VIA56_2_2_66_58.02, all four shapes of cell VIA_VIA56_2_2_66_58 were resized in y by +248 dbu under group label `v5_m6_aux2_fix`, yielding delta_total=-32 (16 violations cleared per affected unit: leaf_0019 139→123, leaf_0020 154→138) with conn_preserved=true. That trial was applied.

Do not use x-axis move plus x-axis resize to address V5.M6.AUX.2. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.01 applied eight ops pairing move_via_shape (axis=x, ±116 dbu) and resize_via_shape (axis=x, +320 dbu) across the same four shapes and achieved only delta_total=-16 before losing the tournament. The y-axis pure-resize approach (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02) produced twice the violation reduction and was selected.

## V5.M6.AUX.2 repair pattern (shape-level)

Apply resize_via_shape on axis=y to every shape in the via cell simultaneously. Trial:i01.cu.def:VIA_VIA56_2_2_66_58.02 operated on shape_index 0 through 3 with identical delta_dbu=+248, showing that all shapes in a multi-cut via cell must be updated together for the rule to clear. Partial updates (a subset of shapes) are not recorded as successful in this layer's history and should not be attempted.

## Interaction between cu_pool M5 fixes and V5 enclosure

Adjustments to M5 geometry affect V5 enclosure rules (V5.M5.EN.1, V5.AUX.1). In trial:i05.cu.def:VIA_VIA45_1_2_58_58.00, the cu_pool channel applied m5_fix group ops — moving M5 polygons p1683 (+32 dbu x) and p1682 (-16 dbu x) and resizing M5 via shapes for both VIA_VIA45_1_2_58_58 and VIA_VIA56_2_2_66_58 (-64 dbu x) — with V5 listed among touched_layers and conn_preserved=true, delta_total=-2.

The corresponding unit_gate trial:i05.ug.leaf_0003.01 dropped the identical m5_fix ops (polygon p1683, p1682, and both via M5 resize ops) under reason "cu_pool:applied", confirming that cu_pool M5 moves are the primary channel for these fixes and unit_gate assembles must not re-issue them. When constructing a unit_gate repair that also involves M5 geometry, check whether cu_pool has already applied the relevant M5 ops; if so, exclude them from the unit_gate op list to avoid assemble_drops.

## V5 shape moves through instance placement

Trial:i05.ug.leaf_0003.01 moved multiple instances (inst_id values i0384, i0528, i0173, i0027, i0367, i0366, i0362, i0360, i0177, i0168, i0426, i0435, i0424, i0411, i0030, i0026) along the y-axis by ±24 or ±32 dbu, with V5 among touched_layers and gated_in as the decision. No direct V5 shape ops appeared; the V5 geometry moved implicitly as part of the via cells referenced by the displaced instances. This trial introduced 68 new in-crop violations across M1.A.1 (27), M4.W.5 (2), and V1.M1.EN.1 (39) as recorded in the debt field, but those are on other layers and do not invalidate the gate decision for this locus.

## Rule reminders grounded in history

**V5.M6.AUX.2**: Y-axis resize of all V5 shapes within a via cell is the confirmed repair action (trial:i01.cu.def:VIA_VIA56_2_2_66_58.02). X-axis moves and resizes in the same context lose tournament (trial:i01.cu.def:VIA_VIA56_2_2_66_58.01).

**V5.AUX.1 and V5.M5.EN.1**: M5 geometry adjustments (moves and via-shape resizes) are the lever for these rules. Apply them through cu_pool before unit_gate to avoid redundant op assembly, as shown by the assemble_drops in trial:i05.ug.leaf_0003.01 that traced back to trial:i05.cu.def:VIA_VIA45_1_2_58_58.00.

**Connectivity**: All four applied or gated-in trials in this layer's history preserved connectivity (conn_preserved=true). V5 shape resizes and via-cell instance moves in the recorded repair range do not break nets.