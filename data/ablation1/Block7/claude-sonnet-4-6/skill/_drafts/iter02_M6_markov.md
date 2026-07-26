**Via cell M6 vertical trim combined with V5 repositioning resolves multi-instance violations**

Shrinking the M6 shape in the y-axis (vertical) within a via cell definition, together with coordinated V5 move and resize operations in the same cell, reduced violations across all instances of that cell simultaneously. In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, a single M6 y-axis resize of −384 dbu applied at the cell definition level (def:VIA_VIA56_2_2_66_58) propagated the fix to four instantiation windows, reducing the total violation count by 39 (units leaf_0045 −18, leaf_0046 −18, leaf_0038 −2, Block7_union_row21 −1) while preserving connectivity.

**M6 y-resize must be paired with V5 adjustments when operating inside a via cell**

When M6 is trimmed vertically inside a via cell, the V5 shapes that land inside M6 require compensating moves and resizes to maintain valid V5.M6.EN.2 enclosure (≥11 nm on two opposite sides) and to satisfy V5.M6.AUX.2 (V5 width must exactly match M6 width perpendicular to M6 length). In trial:i02.cu.def:VIA_VIA56_2_2_66_58.01, each of the four V5 shapes in VIA_VIA56_2_2_66_58 received a y-move of ±132 dbu (outer pair inward, inner pair outward) and a y-resize of +128 dbu; this was sufficient to satisfy both enclosure and width-matching constraints after the M6 −384 dbu y-shrink.

**Cell-definition-level M6 edits are high-leverage when violations cluster across many instances of the same via cell**

When the same via cell type (e.g., VIA_VIA56_2_2_66_58) contributes violations in multiple leaf units, editing the shared cell definition rather than individual instance shapes eliminates violations in all affected windows in a single repair. Trial:i02.cu.def:VIA_VIA56_2_2_66_58.01 demonstrated that 9 ops at the definition level cleared 39 violations spanning 4 distinct windows in the cu_pool channel.