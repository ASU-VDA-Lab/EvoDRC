**V2.M3.AUX.2 — coordinated via-cell plus line resize**

V2.M3.AUX.2 requires each V2 to share the same width as the enclosing M3 stripe along the axis perpendicular to the M3 run direction; any mismatch between the V2 edge and the M3 edge on either side flags as a violation. In iter 4, 8 violations were cleared (window count 30 → 22) by a two-part operation grouped under label `v2m3aux2_fix`, targeting via cell `VIA_VIA23_1_3_36_36` (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00). The repair applied two distinct resize deltas: the M3 enclosure shape internal to the via cell was reduced by 40 dbu in y, and each of the seven connected M3 line polygons (p891–p897) was reduced by 64 dbu in y. Connectivity was preserved throughout (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

The 24 dbu difference between the via-cell delta (40 dbu) and the line-polygon delta (64 dbu) reflects the fact that the via cell's M3 shape and the abutting line polygons originate at different absolute y coordinates; both endpoints must land at the same y edge for the AUX.2 coincidence condition to be satisfied. Applying the via-cell resize alone, or the line resize alone, would leave a y-step at the junction that recreates the violation (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

The cu_pool channel was used to deliver this fix (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00). The target field `def:VIA_VIA23_1_3_36_36` identifies the via cell definition as the repair anchor; line polygons sharing the same via instance group were co-resized in the same operation batch.

**Unit-gate channel — gating despite connectivity preservation**

In iter 1, a 19-operation unit-gate trial spanning M1–M5 and V1–V4 was assigned `decision: gated_in` even though all connections were preserved (trial:i01.ug.whole_design.00). Because the trial was not applied to the design, no M3 geometry change from that trial entered the layout; the design state used as the base for the iter-4 cu_pool fix (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00) reflects a different prior state. No M3-specific outcome can be attributed to trial:i01.ug.whole_design.00.

**M3 geometry inside via cells**

The via cell `VIA_VIA23_1_3_36_36` contains an M3 shape that participates in both V2.M3.AUX.2 (V2 width matching) and V2.M3.EN.2 (minimum two-sided enclosure of V2 by M3 ≥ 5 nm on at least one pair of opposite sides). Resizing the M3 shape inside the via cell in y by −40 dbu did not introduce new V2.M3.EN.2 or V2.M3.AUX.2 violations on the resized side — the repair was net-negative in total violation count — confirming that 40 dbu of y reduction from the pre-fix geometry remained within enclosure headroom on the affected axis (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).

**V3.M3.EN.1 — no recorded violations**

V3.M3.EN.1 requires V3 to be enclosed by M3 by at least 5 nm on at least one pair of opposite sides. No V3.M3.EN.1 violations appear in the repair history and no operations targeting V3 enclosure by M3 were performed. The layer touched set for the only applied trial is M2, M3, V2 (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00); V3 was not involved.

**M3 width, area, and spacing rules — no recorded violations**

Rules M3.W.1 (minimum width 18 nm), M3.A.1 (minimum area 504 nm²), M3.S.1 through M3.S.6, and M3.GEOMETRY.NONORTHOGONAL generated no recorded violations and no repair operations in the two available trials. The resize operations applied to M3 polygons in iter 4 were y-axis shrinks on what appear to be vertical stripes; no evidence in the history suggests that these shrinks approached the 18 nm minimum width or the 504 nm² area floor (trial:i04.cu.def:VIA_VIA23_1_3_36_36.00).