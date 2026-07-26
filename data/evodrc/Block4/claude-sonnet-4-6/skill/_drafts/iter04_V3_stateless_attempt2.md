## Repair Behavior Observed in V3

### Shrinking V3 on the Y-Axis Introduces Net Violations

In trial:i01.cu.def:VIA_VIA34_1_2_58_52.01, two V3 shapes in cell `VIA_VIA34_1_2_58_52` were each resized −24 dbu on the y-axis, simultaneously with an M3 y-axis shrink of −64 dbu on the same cell. The trial was rejected with `decision: rejected_net_positive`: the total DRC delta across reported windows was +34 (window `unit:leaf_0025` went from 88 to 112; window `unit:leaf_0026` went from 35 to 45). Do not apply negative y-axis resizes to V3 shapes in tandem with negative M3 y-axis resizes; the combined reduction degrades enclosure margins (V3.M3.EN.1 requires ≥5 nm enclosure on at least two opposite sides) and can violate spacing rules simultaneously.

### Multi-Instance Moves Touching V3 Can Pass When Connectivity Is Preserved

In trial:i04.ug.leaf_0002.01, eleven operations (moves of one polygon and ten instances) touched layers M3, M4, M5, V3, and V4. The trial was accepted (`decision: gated_in`) with `conn_preserved: true` and only 2 new in-crop violations and 0 new out-of-crop violations. Instance-level moves that maintain connectivity across V3-bearing cells are viable repair candidates and are not categorically blocked by V3 spacing or enclosure rules.

### Rule Reference Summary (no prescriptive extension beyond measured evidence)

The following rules are active for V3 and inform interpretation of the two measured trials above. No repair recipe is asserted for rules not yet exercised in the measured history.

- **V3.W.1**: Minimum width of a V3 shape along the M4 length direction is 18 nm.
- **V3.S.1**: Minimum projected spacing between V3 instances varies by track relationship: 18 nm on the same M4 track, 27 nm between parallel non-aligned tracks, 18 nm between parallel aligned tracks.
- **V3.S.2**: Minimum euclidean corner-to-corner spacing between two V3 instances both carrying a 5 nm M4 end-cap is 23 nm.
- **V3.S.3**: Minimum euclidean corner-to-corner spacing between two V3 instances both without a 5 nm M4 end-cap is 30 nm.
- **V3.S.4**: Minimum euclidean corner-to-corner spacing between one V3 with and one V3 without a 5 nm M4 end-cap is 27 nm.
- **V3.M3.EN.1**: M3 must enclose V3 by at least 5 nm on at least two opposite sides.
- **V3.M4.EN.2**: M4 must enclose V3 by at least 11 nm on at least two opposite sides.
- **V3.AUX.1**: V3 must reside within the intersection of M3 and M4.
- **V3.M4.AUX.2**: V3 width perpendicular to the M4 length direction must exactly match the M4 width in that direction.