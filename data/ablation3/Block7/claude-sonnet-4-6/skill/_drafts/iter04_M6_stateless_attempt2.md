**Track alignment (M6.AUX.2) — y-axis moves**

AUX.2 enforces that minimum-width M6 shapes have their horizontal centerlines on the routing track grid (`(cl - 64) mod 256 == 0` dbu, restricted to polygons whose bottom and top coordinates are both divisible by 128 dbu). In trial:i01.ug.whole_design.00, six M6 polygons (p3801–p3806) were corrected with y-axis move operations under the `m6_snap` group, using deltas from {−64, −32, −16, +16, +32, +64} dbu. Every polygon move in that trial was paired with y-axis moves of the same magnitude on the associated instances. The trial was accepted with zero new DRC violations inside and outside the crop (conn_preserved=true, n_new_in_crop=0, n_new_out_of_crop=0).

**X-axis moves**

In trial:i04.ug.whole_design.00, three pairs of M6 polygons were moved along the x-axis: p2213 and p2216 by +32 dbu, p2212 and p2215 by −16 dbu, and p2211 and p2214 by −64 dbu. Both polygons within each pair received the same x-delta. That trial also carried a large set of instance moves with mixed x- and y-components, and was accepted with zero new violations.

**Move delta set across both accepted trials**

All M6 polygon move deltas observed across trial:i01.ug.whole_design.00 and trial:i04.ug.whole_design.00 are drawn from {−64, −32, −16, +16, +32, +64} dbu, on both the x- and y-axes. No other magnitude appears in the measured history for M6 polygon moves.

**Paired polygon moves**

In trial:i04.ug.whole_design.00, polygons moved in pairs (p2213/p2216, p2212/p2215, p2211/p2214), each pair sharing an identical x-delta. Geometrically related M6 shapes travel together in this data.

**No resize operations in the measured history**

Neither trial:i01.ug.whole_design.00 nor trial:i04.ug.whole_design.00 contains any resize operation on M6 polygons. All shape modifications are pure move operations. No measured basis exists for any prescriptive resize strategy for M6 rules including M6.W.3 and M6.W.4.

**Connectivity and co-moved layers**

Both trials preserved all connectivity. Trial:i01.ug.whole_design.00 touched M5, M6, and V5. Trial:i04.ug.whole_design.00 touched M3, M4, M5, M6, V3, V4, and V5. In both cases, moving M6 polygons was accompanied by moves of the co-located via instances.