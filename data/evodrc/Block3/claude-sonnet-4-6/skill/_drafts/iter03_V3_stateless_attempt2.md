The history is already provided inline. I have everything I need to write the knowledge body.

---

## Operation outcomes

Three trials are on record for layer V3. All three preserved connectivity (conn_preserved=true) and received a gated_in decision; the solver accepts trials that preserve connectivity even when new violations appear within the crop window.

- trial:i02.ug.leaf_0003.02 -- n_new_in_crop=0, n_new_out_of_crop=0 (zero new violations)
- trial:i02.ug.leaf_0004.03 -- n_new_in_crop=2, n_new_out_of_crop=0 (two new violations)
- trial:i03.ug.leaf_0001.00 -- n_new_in_crop=1, n_new_out_of_crop=0 (one new violation)

## Operation type and violation count

Prefer coordinated Y-axis move_instance operations with no resize steps. Trial:i02.ug.leaf_0003.02 applied six Y-axis move_instance operations in symmetric pairs (delta_dbu values 0,+-48 and 0,+-96), touching M3, M4, M5, V3, and V4, and introduced zero new violations -- the only zero-violation outcome in the history.

Do not combine move_instance with resize_end in a single operation set on V3-bearing M4 segments without verifying post-repair enclosure margins. Trial:i02.ug.leaf_0004.03 combined move_instance operations (including X+Y deltas) with resize_end operations on M4 Y endpoints (deltas of 24 and 72 dbu applied to both high and low ends) and introduced 2 new violations -- the highest per-trial count in the history.

Avoid applying a lateral (X-axis only) move_instance to a single V3-connected instance in isolation. Trial:i03.ug.leaf_0001.00 applied one move_instance with delta_dbu=[-16,0] across M3, M4, and V3 and introduced 1 new violation.

## V3.AUX.1: containment inside M3 and M4

V3 must lie inside M3 and M4. Connectivity preservation (conn_preserved=true) does not imply geometric containment; trial:i03.ug.leaf_0001.00 preserved connectivity and still introduced a new violation. Any move that displaces V3 beyond either M3 or M4 boundaries fires this rule before enclosure rules are evaluated.

## V3.M4.AUX.2: exact width match

V3 must match M4's width exactly in the direction perpendicular to M4 length (no tolerance). Move V3 and its M4 host together laterally to preserve this match; trial:i03.ug.leaf_0001.00 moved a single V3-connected instance laterally by delta_dbu=[-16,0] and introduced a new violation, showing that a lone lateral move without a matching M4 displacement is sufficient to violate the exact-width requirement.

## V3.M3.EN.1: M3 enclosure

M3 must enclose V3 by at least 5 nm on at least two opposite sides. The rule evaluates two independent axis-aligned pairs (X-pair: v3.inside(m3.sized(-5.nm, 0)); Y-pair: v3.inside(m3.sized(0, -5.nm))); V3 passes if it satisfies either pair. Symmetric group moves that shift V3 and its surrounding M3 together preserve both pairs. Trial:i02.ug.leaf_0003.02 applied symmetric Y-axis group moves and produced zero new violations. Moving a single instance without its surrounding M3 context breaks the enclosure pair balance; trial:i03.ug.leaf_0001.00 applied exactly this pattern and introduced a new violation.

## V3.M4.EN.2: M4 enclosure

M4 must enclose V3 by at least 11 nm on at least two opposite sides. The 11 nm threshold is large relative to common move deltas; resize_end operations that shorten M4 endpoints directly consume this margin. Do not apply resize_end to M4 endpoints adjacent to V3 without confirming the 11 nm margin is preserved on the remaining opposite sides; trial:i02.ug.leaf_0004.03 applied resize_end deltas of 24 and 72 dbu to M4 Y endpoints in the same operation set that introduced 2 new violations.

## V3.S.1: projection-based spacing via NEC/WEC masks

V3.S.1 classifies each V3 instance as NEC (no-end-cap) or WEC (with-end-cap). A NEC instance has all of its edges fully coincident with M4 edges; a WEC instance has at least one non-coincident edge. The mask for WEC instances is extended 5 nm along the M4 direction before spacing is measured. This means a move that breaks full-flush edge coincidence between V3 and M4 reclassifies a NEC instance as WEC, changing the effective spacing geometry without any change in raw V3-to-V3 distance. Do not apply lateral moves to V3 instances without verifying that the resulting NEC or WEC classification satisfies all projection spacing thresholds; trial:i03.ug.leaf_0001.00 applied a lateral move (delta_dbu=[-16,0]) to a V3-connected instance and introduced a new violation.

The projection spacing minimums under V3.S.1 are: 17 nm on NEC-mask non-M4 edges (v3_nec_mask_nm4_nte check), 18 nm on maskav non-M4 edges (v3_maskav_nciem check), and 1 nm on v3_mask to v3_mask (floor check). A reclassification from NEC to WEC that moves a V3 instance within the 5 nm mask extension of a neighbor can produce an 18 nm maskav violation even when the raw V3-to-V3 gap is larger.

## V3.S.2, V3.S.3, V3.S.4: corner-to-corner euclidean spacing

These three rules enforce euclidean corner-to-corner minimums between pairs of V3 instances based on end-cap configuration: 23 nm between two WEC instances (V3.S.2), 30 nm between two NEC instances (V3.S.3), and 27 nm between one WEC and one NEC instance (V3.S.4). Each rule fires only on euclidean violations not also caught by a projection check (not_interacting with projection-based polygon results).

Operations that displace V3 in both X and Y simultaneously alter euclidean corner distances independently of projection distances. Trial:i02.ug.leaf_0004.03 is the only operation set in the history that applied combined X and Y displacement (move_instance with non-zero X delta alongside Y resize_end on M4) and is also the only trial that introduced more than one new violation. Use trial:i02.ug.leaf_0004.03 as the reference case when evaluating whether a multi-axis move requires an explicit corner-spacing check against V3.S.2, V3.S.3, and V3.S.4.

## V3.W.1: minimum width

V3 minimum width along the M4 length direction is 18 nm. No trial in the history applied a resize operation directly to V3 geometry; all resize operations were on M4 (trial:i02.ug.leaf_0004.03, resize_end on M4 Y endpoints). V3.M4.AUX.2 requires V3 to match M4 width exactly perpendicular to M4 length; a resize_end that narrows M4 below 18 nm in that direction would force a V3 resize that violates V3.W.1.

## Move delta magnitudes and geometry

All move deltas in the history are multiples of 8 dbu: 16, 24, 32, 48, 72, 96 dbu (trial:i02.ug.leaf_0003.02, trial:i02.ug.leaf_0004.03, trial:i03.ug.leaf_0001.00). All three trials used strictly axis-aligned operations and none introduced V3.GEOMETRY.NONORTHOGONAL violations. The nonorthogonal rule fires on any V3 edge with angle outside 0 and 90 degrees; keep all V3 moves and resizes axis-aligned to avoid it.