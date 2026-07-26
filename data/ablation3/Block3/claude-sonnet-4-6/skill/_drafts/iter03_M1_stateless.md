## Repair Operations Observed

The single measured trial for M1 at iteration 3 used two operation types: `move_instance` (+x direction only) and `resize_end` (axis=x, end=high). All 16 polygon resize operations extended the high-x end of M1 polygons; no low-end, y-axis, or shrink operations were applied. All 20 instance moves displaced instances by either 64 dbu or 136 dbu in the +x direction. No operations acted on the low-x end or either y-axis end of any polygon in this trial (trial:i03.ug.whole_design.00).

## Outcome

Trial `i03.ug.whole_design.00` was accepted as `gated_in` with `conn_preserved=true` and zero new violations introduced either inside or outside the crop region (`n_new_in_crop=0`, `n_new_out_of_crop=0`). This confirms that the combination of +x instance moves and +x high-end polygon extensions can resolve M1 DRC violations without breaking connectivity or creating secondary violations in the same pass (trial:i03.ug.whole_design.00).

## Layer Interaction

Repairs in trial:i03.ug.whole_design.00 touched layers M1, M2, and V1 together. M1 polygon extensions therefore require coordinated changes on V1 and M2 to maintain enclosure compliance. Specifically, rules V0.M1.EN.1, V1.M1.EN.1, and V0.M1.AUX.3 constrain how M1 must surround vias; extending an M1 polygon end can satisfy or violate these rules depending on orientation relative to the via. The measured trial resolved these jointly by also adjusting V1, confirming that isolated M1-only edits are insufficient when vias are present (trial:i03.ug.whole_design.00).

## Resize Delta Range

Polygon end extensions in the measured trial ranged from 84 dbu to 192 dbu (polygons p1189 and p1223 at 84 dbu; p1226 at 156 dbu; p1267, p1261, p1255, p1270 at 192 dbu; the majority at 120 dbu). The spread across this range within a single accepted repair pass indicates that different M1 segments required different extension amounts to satisfy enclosure and spacing rules simultaneously (trial:i03.ug.whole_design.00).

## Spacing and Width Rules

Rules M1.W.1 (min width 18 nm), M1.S.1 (min side-to-side 18 nm for edges >36 nm), M1.S.2 (min tip-to-side 25 nm), M1.S.3 (min tip-to-tip 27 nm for edges 24–36 nm), M1.S.4 (min tip-to-tip 31 nm for edges <24 nm), M1.S.5 (31 nm mixed), and M1.S.6 (corner-to-corner 20 nm) all depend on M1 edge length classification. Extending a tip edge (≤36 nm) converts it to a side edge (>36 nm), shifting the applicable spacing rule from M1.S.2/S.3/S.4/S.5 to M1.S.1. The successful +x extensions in trial:i03.ug.whole_design.00 produced no new spacing violations, confirming that the applied delta values kept all resulting edges clear of their respective spacing minimums after reclassification.

## Area Rule

Rule M1.A.1 requires minimum M1 area of 504 nm². Extending M1 polygon ends increases area, so resize_end operations as applied in trial:i03.ug.whole_design.00 move polygons away from M1.A.1 violations rather than toward them. No area violations were introduced by the measured repairs (trial:i03.ug.whole_design.00).

## Redundancy Rule

Rule M1.R.0 flags M1 islands enclosing exactly one small V0 near large empty M1 regions. The measured trial did not trigger this rule, consistent with the repair strategy of extending existing M1 shapes rather than creating new isolated islands (trial:i03.ug.whole_design.00).

## Non-Orthogonal Geometry

The NONORTHOGONAL rule applies to M1. All resize_end and move_instance operations in the measured trial were strictly axis-aligned (x-axis moves and extensions only), producing no non-orthogonal edges. Any repair operation that introduces diagonal edges or non-rectilinear geometry will trigger GEOMETRY.NONORTHOGONAL on M1. The measured repair set avoided this by restricting all edits to axis-aligned movements and rectangular end extensions (trial:i03.ug.whole_design.00).