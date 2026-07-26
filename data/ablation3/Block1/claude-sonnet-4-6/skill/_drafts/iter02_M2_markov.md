**M2 in VIA_VIA23_1_3_36_36: y-axis extension co-repairs V2.M2 auxiliary violations**

Resizing the M2 shape in cell `VIA_VIA23_1_3_36_36` by +64 dbu on the y-axis, simultaneous with matching y-axis expansions of all three V2 shapes in the same cell, eliminated 24 violations and preserved connectivity (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, group `v2m3aux2_fix`, decision `applied`). The M2 extension is a co-traveler of the V2 resize: the DRC engine requires M2 to track the V2 boundary change to keep the via flush with its enclosing metal in the perpendicular direction (V1.M2.AUX.2 analogue applied to the V2/M2 interface at this cell).

**M2 resize axis must match the via resize axis**

When a via-cell fix drives M2, the M2 delta axis must equal the via delta axis. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, all four ops (three V2, one M2) used `axis:"y"` and `delta_dbu:64`. Mismatched axes would reintroduce width/enclosure asymmetry and regenerate violations.

**64 dbu y-expansion sufficient to clear 24-violation cluster in VIA_VIA23_1_3_36_36**

A single uniform +64 dbu y-expansion applied to shape_index 0 of M2 (alongside all V2 shapes at indices 0–2) cleared the full 24-violation delta in the `unit:whole_design` window (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00). No secondary M2 spacing or width violations were introduced, confirming that this magnitude does not push M2 edges into neighboring geometries within this cell's pitch environment.

**Co-repair scope: M2 + V2 shapes must move together**

Applying the `v2m3aux2_fix` group with only V2 ops and omitting the M2 op, or vice versa, is not supported by any measured record; the single successful repair (trial:i02.cu.def:VIA_VIA23_1_3_36_36.00) bundled all four ops atomically. Do not split the M2 and V2 ops into separate passes for this cell type.