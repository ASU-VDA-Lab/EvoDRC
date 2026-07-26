**V2.M2.EN.1 enclosure violations in via cells**

Extending M2 in the y-axis by +64 dbu on the enclosing shape inside a VIA_VIA23 via cell, simultaneously with a matching +64 dbu y-axis resize of all co-located V2 shapes, removes V2.M2.EN.1 violations and preserves connectivity. The cu_pool channel applied this four-operation repair to cell VIA_VIA23_1_3_36_36 and eliminated 8 violations with conn_preserved=true (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**M2 resize in via cell must track V2 resize**

When V2 shapes inside a via cell are resized in y to satisfy V2.M2.EN.1, the M2 shape in the same cell must also be resized in the same axis and by the same delta to avoid introducing new M2 width, spacing, or area violations; in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 a single M2 y-resize of +64 dbu accompanied three V2 y-resizes of +64 dbu each with no residual M2 violations.

**Via cell shape operations via resize_via_shape**

The op type `resize_via_shape` acting on layer M2 within a named via cell (here VIA_VIA23_1_3_36_36) is a valid, connection-preserving repair path for enclosure defects; the applied record at trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 confirms net negative violation delta (-8) and conn_preserved=true for this op type on M2.