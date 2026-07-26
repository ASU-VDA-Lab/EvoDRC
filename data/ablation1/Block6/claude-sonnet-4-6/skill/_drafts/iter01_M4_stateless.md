## Layer M4 — Repair Knowledge (Iteration 1)

### Coverage note

Only one measured trial exists for this iteration. That trial's primary operation targeted M5 geometry inside a via cell; M4 appears as a touched layer, not the direct operand. All assertions below are grounded exclusively in trial:i01.cu.def:VIA_VIA45_1_2_58_58.00.

---

### Via-cell y-axis shrink on M5 touches M4 and yields net M4-region violation reduction

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.00, a single `resize_via_shape` operation on M5 (axis: y, delta: −88 dbu) inside cell `VIA_VIA45_1_2_58_58` listed M4 among its touched layers alongside M5 and V4. The repair was accepted (decision: applied) and produced a combined reduction of 56 DRC violations across the two affected windows (unit:leaf_0019: −30; unit:leaf_0020: −26). Connectivity was preserved throughout (conn_preserved: true, trial:i01.cu.def:VIA_VIA45_1_2_58_58.00).

When a via cell's M5 shape is shortened in y, the adjacent M4 enclosure geometry is renegotiated in the same deck evaluation pass. Do not treat M4 as an isolated layer when repairing V4- or M5-touching via cells; the enclosure check V4.M4.EN.1 (minimum 11 nm enclosure of V4 by M4 on at least two opposite sides) and the width/spacing rules evaluated over the via cell's M4 extent are co-evaluated and will move together (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00).

---

### Key dimensional constraints with no directly measured repair data yet

The following rules have not yet been exercised by any repair trial on this layer. No prescriptive repair guidance can be cited for them; they are listed here as uncharted territory so future iterations can prioritize measurement:

- **M4.W.1 / M4.W.2 / M4.W.3 / M4.W.4**: vertical width must be ≥ 24 nm, ≤ 480 nm, must not be an even-integer multiple of 24 nm, and must not be 72, 168, 264, 360, or 456 nm.
- **M4.W.5**: horizontal width ≥ 44 nm.
- **M4.S.1 – M4.S.5**: vertical spacing ≥ 24 nm; horizontal spacing ≥ 40 nm; tip-to-tip spacing ≥ 40 nm; parallel run length ≥ 44 nm.
- **M4.AUX.1**: horizontal edges must land on a 24 nm grid.
- **M4.AUX.2**: minimum-width M4 track centerlines must align to a 192 dbu pitch with 48 dbu offset from origin.
- **M4.AUX.3**: M4 shapes must not bend (no corners between 0° and 90°).
- **M4.AUX.4**: the outside horizontal edge of a wide M4 polygon must not coincide with a routing-track edge defined by neighboring 1× M4 tracks.
- **V3.M4.EN.2**: V3 vias must be enclosed by M4 by at least 11 nm on two opposite sides.
- **V3.M4.AUX.2**: V3 width must exactly equal M4 width in the direction perpendicular to M4 length.

---

### Repair scope and connectivity safety

The single applied trial confirms that multi-layer via-cell repairs touching M4 can be executed without breaking connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.00). Always verify conn_preserved after any operation that simultaneously adjusts M4, V4, or M5 dimensions within a shared via cell; the geometry coupling between those layers means a fix to one enclosure can perturb another.