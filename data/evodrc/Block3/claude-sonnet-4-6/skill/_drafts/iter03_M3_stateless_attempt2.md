## Unit-Gate Operations on M3

All four unit_gate channel trials touching M3 carry `decision=gated_in` with `reason=conn_preserved`: trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i03.ug.leaf_0001.00. The conn_preserved reason was sufficient for acceptance in every case recorded in this history.

New in-crop violations do not block acceptance when conn_preserved is the stated gate reason. Trial:i02.ug.leaf_0004.03 introduced 2 new in-crop violations and was accepted; trial:i03.ug.leaf_0001.00 introduced 1 new in-crop violation and was accepted. Both carry `decision=gated_in`.

Every gated_in unit_gate trial recorded `n_new_out_of_crop=0`: trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i03.ug.leaf_0001.00. No trial in the measured history introduced out-of-crop violations alongside an M3 touch.

## Unit-Gate Move and Resize Deltas Observed on M3

Instance move deltas in unit_gate trials that touch M3 take the following x-axis values in the measured history: -16 dbu (trial:i03.ug.leaf_0001.00), +4 dbu and +136 dbu (trial:i01.ug.leaf_0008.06), and +32 dbu (trial:i02.ug.leaf_0004.03). Y-axis instance move values observed are ±24 dbu, ±48 dbu, ±72 dbu, and ±96 dbu (trial:i02.ug.leaf_0004.03, trial:i02.ug.leaf_0003.02).

Resize-end operations on M3 polygons are present in two trials. Trial:i01.ug.leaf_0008.06 carries a y-axis `resize_end` of +20 dbu (high end, polygon p1159) and an x-axis `resize_end` of +92 dbu (high end, polygon p1261). Trial:i02.ug.leaf_0004.03 carries four y-axis `resize_end` operations on polygons p1101–p1104, with deltas of ±24 dbu and ±72 dbu. All six resize operations are paired with instance moves in the same trial and all were accepted.

## cu_pool V2/M3 Via Sizing

The one cu_pool trial touching M3, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, applied five via-shape operations entirely on V2 shapes within cell VIA_VIA23_1_3_36_36: three `resize_via_shape` ops of +288 dbu along x and two `move_via_shape` ops of -144 dbu and +144 dbu along x. This yielded a net reduction of 27 DRC violations across two units (leaf_0018: -15, leaf_0019: -12), with `decision=applied`. V2 shape resizing of this kind directly affects M3 geometry compliance because V2.M3.EN.2 requires M3 to enclose V2 by at least 5 nm on two opposite sides, and V2.M3.AUX.2 requires V2 width to equal M3 width in the direction perpendicular to M3 length.

## M3 Spacing and Width Rules as Applied in Measured Trials

M3.W.1 sets minimum M3 width at 18 nm. The resize operations in trial:i01.ug.leaf_0008.06 and trial:i02.ug.leaf_0004.03 enlarged or shifted M3 polygon ends without producing a rejected outcome, consistent with M3.W.1 compliance being maintained through those operations.

M3.S.1 requires 18 nm side-to-side spacing for edges longer than 36 nm. M3.S.2 raises the tip-to-side minimum to 25 nm when one edge is a tip (≤36 nm). M3.S.3 requires 27 nm tip-to-tip when both tips are in the 24–36 nm range. M3.S.4 requires 31 nm tip-to-tip when both tips are shorter than 24 nm. M3.S.5 requires 31 nm when one tip is 24–36 nm and the other is shorter than 24 nm. M3.S.6 adds a Euclidean corner-to-corner floor of 20 nm independent of edge classification. M3.A.1 requires a minimum polygon area of 504 nm². The polygon geometry alterations across trial:i01.ug.leaf_0008.06, trial:i02.ug.leaf_0004.03, and trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 each resulted in an accepted outcome, confirming that those specific operations did not push any M3 geometry below these thresholds.

## V3 Enclosure Interactions with M3 Instance Moves

V3.M3.EN.1 requires V3 to be enclosed by M3 by at least 5 nm on two opposite sides. Three accepted unit_gate trials list V3 among their touched layers alongside M3: trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, and trial:i03.ug.leaf_0001.00. In all three, the primary ops are instance moves; the V3.M3.EN.1 constraint was not violated by those moves, as all three carry `decision=gated_in`. When selecting instance move deltas for M3-touching cells that also include V3, the deltas observed in this history (y-axis: ±48 and ±96 dbu in trial:i02.ug.leaf_0003.02; x-axis: -16 dbu in trial:i03.ug.leaf_0001.00) preserved V3.M3.EN.1 compliance.