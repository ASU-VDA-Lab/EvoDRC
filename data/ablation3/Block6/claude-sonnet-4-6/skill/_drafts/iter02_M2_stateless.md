## Via Enclosure Repair on M2 (V2.M2.EN.1)

The only completed repair recorded for iteration 2 on layer M2 is trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, which targeted cell `VIA_VIA23_1_3_36_36` and reduced whole-design violations from 159 to 81 (delta −78). The decision was `applied` and connectivity was preserved (`conn_preserved: true`). All five operations acted exclusively on V2 shapes within the via cell; M2 itself was listed as a touched layer but received no direct edits, meaning the M2-rule relief came from adjusting via geometry to conform to existing M2 geometry rather than modifying M2 shapes.

### Operation pattern that succeeded

The five ops in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 follow a paired move-then-resize pattern on the x-axis across three V2 shape indices:

- Shape 0: move −144 dbu, then resize +288 dbu → net lateral shift left by 144 dbu while widening 288 dbu.
- Shape 1: resize +288 dbu only (no move) → symmetric widening.
- Shape 2: move +144 dbu, then resize +288 dbu → net lateral shift right by 144 dbu while widening 288 dbu.

This paired offset-and-expand on shapes 0 and 2 with a center-only expand on shape 1 produced a balanced adjustment that satisfied the enclosure requirement without violating spacing constraints on the M2 side, as evidenced by the net −78 violation reduction and the `applied` outcome in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00.

### Rule V2.M2.EN.1 context

Rule V2.M2.EN.1 requires V2 to be enclosed by M2 by at least 5 nm on at least two opposite sides (x or y). The repair in trial:i02.cu.def:VIA_VIA23_1_3_36_36.00 operated exclusively in x, indicating the enclosure deficiency was in the horizontal direction. Resizing V2 shapes toward both ends simultaneously (as seen in shapes 0 and 2) brings V2 edges closer to M2 boundaries on opposing sides without requiring M2 edits, which preserves all M2 spacing rules.

### Residual violations

After applying trial:i02.cu.def:VIA_VIA23_1_3_36_36.00, 81 violations remain in the whole design. This single trial addressed only one via cell definition; M2-related violations tied to other cells or to M2's own width, spacing, area, or tip-to-tip proximity rules (M2.W.1, M2.S.1–M2.S.8, M2.A.1) are not yet covered by any measured repair in this layer's history. No prescriptive guidance on those rules can be offered without additional measured trials.