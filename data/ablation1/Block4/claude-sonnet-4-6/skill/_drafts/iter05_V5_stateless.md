## Repair Patterns

### Enclosure repairs: coordinated M5 expansion + V5 move-and-resize (y-axis)

Both applied trials targeted via cells of the VIA_VIA56_2_x family and resolved enclosure violations (V5.M5.EN.1, V5.M6.EN.2) using a three-step sequence applied uniformly to every V5 shape in the cell:

1. Expand M5 on the y-axis by +248 dbu (resize only, no move).
2. Move each V5 shape outward along y: shapes indexed toward the negative-y edge move by −132 dbu; shapes indexed toward the positive-y edge move by +132 dbu.
3. Resize every V5 shape on the y-axis by +512 dbu.

For a 2-via cell (VIA_VIA56_2_1_66_58, 2 V5 shapes), shape_index=0 received move −132 dbu then resize +512 dbu, and shape_index=1 received move +132 dbu then resize +512 dbu (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00, delta_total −2, applied).

For a 4-via cell (VIA_VIA56_2_2_66_58, 4 V5 shapes), shapes at indices 0 and 1 received move −132 dbu then resize +512 dbu, and shapes at indices 2 and 3 received move +132 dbu then resize +512 dbu (trial:i04.cu.def:VIA_VIA56_2_2_66_58.01, delta_total −4, applied).

The move step spreads each V5 shape away from the cell's y-axis center before the resize, preventing the grown V5 geometry from violating V5.S.1 / V5.S.2 / V5.S.3 spacing rules against neighboring instances. The M5 resize of +248 dbu accommodates the enlarged V5 footprint without leaving V5 outside M5, preserving V5.AUX.1 compliance.

### M6-only expansion without V5 adjustment increases violations

Resizing M6 by +128 dbu on the y-axis across both via cells (VIA_VIA56_2_1_66_58 and VIA_VIA56_2_2_66_58) and a standalone polygon (p1402, group g_v0056_m6aux1), without any corresponding move or resize of V5 shapes, produced a net increase of +5 violations (trial:i05.cu.def:VIA_VIA56_2_1_66_58.00, delta_total +5, rejected_net_positive). Do not apply M6-only resizes to fix V5 enclosure violations; the V5.M6.AUX.2 rule requires V5 width to match M6 width perpendicular to the M6 length, so expanding M6 without adjusting V5 creates or widens the mismatch detected by that rule.

### Operation sequencing within a via cell

In both applied trials the repair engine issued operations in this order: M5 resize first, then interleaved move+resize pairs for each V5 shape. Connectivity was preserved across all applied repairs (conn_preserved: true in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00 and trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). Apply the M5 expansion before V5 shape adjustments so that intermediate states do not temporarily push V5 outside M5, which would trigger V5.AUX.1.

### Scaling move magnitude by via count

In both applied trials the absolute move magnitude per V5 shape is 132 dbu regardless of whether the cell contains 2 or 4 V5 shapes (trial:i04.cu.def:VIA_VIA56_2_1_66_58.00; trial:i04.cu.def:VIA_VIA56_2_2_66_58.01). The resize magnitude is likewise 512 dbu per shape in both cases. These values are uniform across via-count variants of the VIA_VIA56_2_x cell family and need not be scaled by the number of shapes.

### M5 and M6 are co-touched layers; V5 repairs affect both metal layers

Every trial in the history touches M5, M6, and V5 together (touched_layers in trial:i04.cu.def:VIA_VIA56_2_1_66_58.00; trial:i04.cu.def:VIA_VIA56_2_2_66_58.01; trial:i05.cu.def:VIA_VIA56_2_1_66_58.00). Isolating V5 shape changes to a single metal layer while leaving the other unchanged is not sufficient to close violations; repairs to V5 enclosure require corresponding adjustments on at least M5.