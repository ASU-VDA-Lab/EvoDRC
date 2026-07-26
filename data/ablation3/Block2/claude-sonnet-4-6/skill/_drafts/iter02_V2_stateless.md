**Via cell y-axis growth reduces V2 violations**

Growing all three V2 shapes within a via cell along the y-axis by 64 dbu, paired with a matching y-axis resize of the co-located M2 shape, produced a net reduction of 8 total violations and preserved connectivity (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00). When a via cell such as VIA_VIA23_1_3_36_36 is the violation locus, resize both the V2 shapes and the enclosing M2 shape together rather than resizing V2 alone; the single-axis (y) resize satisfied V2.M2.EN.1 and V2.AUX.1 without introducing new enclosure or spacing errors on M3 (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Coordinated multi-layer repositioning is safe for V2**

A 45-operation unit_gate sweep covering M1–M5 and V1–V4, including V2, was accepted with zero new violations introduced inside or outside the crop region and connectivity fully preserved (trial:i02.ug.whole_design.00). When V2 instances are moved as part of a coordinated block that shifts the surrounding M2 and M3 geometries by the same delta, V2.AUX.1 (V2 must be inside M2 and M3) and V2.M3.AUX.2 (V2 width must match M3 width perpendicular to M3 length) are not violated, because the relative positions of V2 with respect to its enclosing metal layers do not change (trial:i02.ug.whole_design.00).

**Do not resize V2 without co-resizing M2**

The successful repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 resized M2 alongside V2; V2.M2.EN.1 requires at least 5 nm enclosure of V2 by M2 on two opposite sides. Resizing V2 outward without a matching M2 extension would shrink the effective enclosure margin and risk triggering V2.M2.EN.1. The only repair in the history that touched V2 sizing always included an M2 resize in the same operation set (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Prefer y-axis resizes in via cells on the same M3 track**

The V2.S.1 spacing rule has its tightest projection-based threshold (18 nm) for via instances on the same M3 track. The repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 applied y-axis growth (perpendicular to the M3 length direction for horizontal M3 tracks), which expands the via along the M3 direction and does not close the same-track projection spacing. Net violations decreased by 8 without introducing new V2.S.1 errors (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**Instance moves on V2 require simultaneous moves of all connected metal**

In trial:i02.ug.whole_design.00, every V2-containing via instance was moved with its surrounding M2, M3, and adjacent vias within the same operation batch. No new V2.S.1, V2.S.2, V2.S.3, or V2.S.4 violations were introduced (delta n_new_in_crop = 0), confirming that moving V2 instances without altering inter-via spacing—because all neighboring vias shift by the same delta—keeps mask-derived spacing metrics intact (trial:i02.ug.whole_design.00).