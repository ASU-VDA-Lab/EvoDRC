**Accepted operations on M2**

In trial:i01.ug.whole_design.00, two M2 polygon modifications were accepted (decision: gated_in, conn_preserved=true): polygon p879 received a y-axis high-end extension of +48 dbu, and polygon p910 received a +8 dbu x-axis translation combined with a +20 dbu y-axis high-end extension. Apply y-axis end-extension and x-axis polygon translation as M2 repair primitives when connectivity must be preserved (trial:i01.ug.whole_design.00).

In trial:i02.ug.whole_design.00, seven instances affecting M1, M2, and V1 were translated ±36 dbu along the x-axis. The trial was accepted (gated_in, conn_preserved=true). Use ±36 dbu as a tested x-axis step granularity for instance moves that modulate M2 spacing (trial:i02.ug.whole_design.00).

**Rule thresholds for spacing and geometry**

M2.W.1 requires minimum width 18 nm. M2.S.1 requires minimum side-to-side spacing 18 nm when both opposing edges exceed 36 nm in length. M2.S.2 requires minimum tip-to-side spacing 25 nm when the tip edge is ≤36 nm and the side edge is >36 nm. M2.S.3 requires minimum tip-to-tip spacing 27 nm when both tip edges are in the range 24–36 nm. M2.S.4 requires minimum tip-to-tip spacing 31 nm when both tip edges are <24 nm. M2.S.5 requires minimum tip-to-tip spacing 31 nm when one tip is in the range 24–36 nm and the other is <24 nm. M2.S.6 requires minimum corner-to-corner (euclidean) spacing 20 nm. M2.A.1 requires minimum polygon area 504 nm².

M2.S.7 forbids the combination of an 18 nm tip-to-tip gap and side-to-side spacing ≤32 nm on co-located tracks; parallel run length must be ≥35 nm whenever side spacing is ≤32 nm. M2.S.8 requires minimum diagonal (euclidean) center-to-center spacing of 80 nm between tip-to-tip gaps on different tracks; gap centers are defined by shrinking each gap polygon 8.5 nm per side.

**Via enclosure thresholds**

V1.M2.EN.2 requires M2 to enclose V1 by ≥5 nm on two opposite sides (5 & 5 nm or 5 & 0 nm). V1.M2.AUX.2 requires V1 to match M2 width along the direction perpendicular to M2 length; V1 edges must coincide with M2 edges on exactly two sides. V2.M2.EN.1 requires M2 to enclose V2 by ≥5 nm on at least two opposite sides.

**Connectivity preservation is required for acceptance**

Both accepted trials recorded conn_preserved=true. Never apply M2 polygon resizes or instance moves that sever routed connections; the accepted end-extensions and translations in trial:i01.ug.whole_design.00 and trial:i02.ug.whole_design.00 maintained all connectivity, and both were gated_in as a result.