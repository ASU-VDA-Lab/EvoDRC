All nine iteration-1 trials on layer M2 were accepted (decision: gated_in) with connectivity preserved and zero new violations introduced inside or outside the crop window (n_new_in_crop=0, n_new_out_of_crop=0 in every case: trial:i01.ug.Block6_union_row3.00, trial:i01.ug.Block6_union_row4.01, trial:i01.ug.Block6_union_row5.02, trial:i01.ug.Block6_union_row7.03, trial:i01.ug.Block6_union_row8.04, trial:i01.ug.leaf_0001.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0015.07, trial:i01.ug.leaf_0018.08).

**Repair operations on M2 and co-touched layers**

All accepted repairs touch M2 together with M1 and V1; no trial in this iteration isolated M2 alone. Multi-instance moves (2–3 instances per trial) are consistently accepted when connectivity is preserved, as demonstrated in trial:i01.ug.Block6_union_row4.01 (2 ops), trial:i01.ug.Block6_union_row5.02 (2 ops), trial:i01.ug.Block6_union_row7.03 (3 ops), trial:i01.ug.Block6_union_row8.04 (3 ops), and trial:i01.ug.leaf_0015.07 (3 ops). Single-instance moves are also accepted: trial:i01.ug.Block6_union_row3.00, trial:i01.ug.leaf_0001.05, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0018.08.

**Accepted move magnitudes — x-axis**

The following x-direction instance move deltas were each accepted without introducing new M2 violations: 4 dbu (trial:i01.ug.leaf_0001.05, trial:i01.ug.Block6_union_row5.02), 12 dbu (trial:i01.ug.Block6_union_row7.03), 28 dbu (trial:i01.ug.leaf_0015.07), 36 dbu (trial:i01.ug.Block6_union_row4.01, trial:i01.ug.Block6_union_row8.04, trial:i01.ug.leaf_0011.06, trial:i01.ug.leaf_0018.06), and −40 dbu (trial:i01.ug.Block6_union_row7.03). Use x-axis moves in the range −40 to +36 dbu when other constraints allow; avoid larger untested magnitudes until records exist to support them.

**Accepted move magnitudes — y-axis**

A y-direction move of 48 dbu (trial:i01.ug.Block6_union_row3.00) and a combined y-move of 48 dbu paired with a 4 dbu x-move (trial:i01.ug.Block6_union_row5.02) were each accepted without new M2 violations. No other y magnitudes appear in iteration-1 records.

**Accepted resize_end operations on M2 polygons**

Resizing the x-axis low end of an M2 polygon by +60 dbu (trial:i01.ug.Block6_union_row7.03, polygon p1920) and resizing the x-axis high end by +36 dbu (trial:i01.ug.Block6_union_row8.04, polygon p1907) and +48 dbu (trial:i01.ug.leaf_0015.07, polygon p1923) were each accepted without new violations. Apply resize_end to M2 polygon ends when an instance-only move is insufficient and a stretch is needed to satisfy enclosure or spacing rules; the accepted range for x-axis end extension is 36–60 dbu per these records.

**Connectivity preservation as a gate**

Every accepted trial reports conn_preserved=true. Preserve connectivity across M1, M2, and V1 when selecting move or resize targets; moves that break connectivity are not represented among the accepted records and are not a supported strategy based on this iteration.