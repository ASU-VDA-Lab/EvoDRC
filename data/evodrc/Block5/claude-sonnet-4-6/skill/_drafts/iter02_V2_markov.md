**V2/M3 Co-Operation Pattern (Resize and Move)**

Coordinated operations touching V2, M3, and M2 together are required when correcting V2 spacing or enclosure violations. In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 simultaneous y-axis resizes on V2 (-40 dbu) and four adjacent M3 strips (-64 dbu each) reduced violations in unit:leaf_0009 by 8. In trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 an x-axis move of the V2 shape (+144 dbu, move_via_shape) reduced violations across unit:leaf_0002 (-4) and unit:leaf_0003 (-3) with M2, M3, and V2 all listed in touched_layers. Both repairs preserved connectivity. V2.M3.AUX.2 requires V2 width to exactly match M3 width perpendicular to M3 length; any V2 reposition that shifts its footprint relative to M3 requires a matching M3 adjustment on the same axis.

**Asymmetric Resize Magnitudes Between V2 and M3**

In trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 the V2 via shape was shrunk by 40 dbu on y while each of the four M3 strip polygons was shrunk by 64 dbu on y—a 24 dbu difference. V2.M3.EN.2 mandates that M3 enclose V2 by at least 5 nm on two opposite sides; the larger M3 delta relative to the V2 delta preserves or restores that enclosure margin after the via shrink. Do not assume equal deltas for V2 and M3; size M3 to maintain V2.M3.EN.2 enclosure after any V2 change (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00).

**M2 Is Also Touched During Via Resize or Move**

Both repair records list M2 in touched_layers alongside M3 and V2: a y-axis resize in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 and an x-axis move in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01. V2.M2.EN.1 requires M2 to enclose V2 by at least 5 nm on two opposite sides. Verify and adjust M2 enclosure whenever any V2 positional change (resize or move) is applied on any axis (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

**Axis-Aligned Operations Avoid NONORTHOGONAL Violations**

Trial:i01.cu.def:VIA_VIA23_1_3_36_36.00 used y-axis resize and trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 used an x-axis move; both are strictly axis-aligned and neither introduced NONORTHOGONAL violations—connectivity was preserved in both cases. The NONORTHOGONAL rule fires on any V2 edge with an angle outside 0° and 90°. Restrict all V2 resize and move operations to strictly axis-aligned directions (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

**Single Via Move Can Affect Multiple Windows Simultaneously**

The x-axis move in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01 reduced violations in two distinct windows: unit:leaf_0002 by 4 (17→13) and unit:leaf_0003 by 3 (25→22), with a single n_ops:1 operation. A V2 via position influences DRC checks in overlapping or adjacent windows; a single positional correction can yield non-uniform delta contributions across those windows (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

**Move vs. Resize as Repair Strategies**

Two distinct operation types have been recorded for V2 violation repair: resize (y-axis, trial:i01.cu.def:VIA_VIA23_1_3_36_36.00) and move_via_shape (x-axis, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01). The move operation repositioned the via shape by 144 dbu along x without changing its dimensions, while the resize changed via and M3 dimensions without translating the via center. Both are valid repair strategies; the applicable type depends on whether the violation source is an absolute position conflict (spacing to a neighbor on the same axis) or an enclosure dimension mismatch (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).

**Partial Violation Reduction Per Window**

After the repair in trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, unit:leaf_0009 retained 17 violations despite a reduction of 8, and unit:leaf_0010 remained at 25 violations unchanged. After the repair in trial:i02.cu.def:VIA_VIA23_1_3_36_36.01, unit:leaf_0002 retained 13 violations and unit:leaf_0003 retained 22 violations. A single operation addressing one V2 instance does not clear all violations in a window. Expect multiple independent V2 violation sources per unit window and do not stop after a single repair if the window count remains nonzero (trial:i01.cu.def:VIA_VIA23_1_3_36_36.00, trial:i02.cu.def:VIA_VIA23_1_3_36_36.01).