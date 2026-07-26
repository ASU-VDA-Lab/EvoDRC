The inputs are already provided inline in the prompt. I have everything I need to generate the knowledge section directly.

---

## Rule Summary and Geometry Constraints

V3 instances must satisfy eight geometric rules. Four rules govern the V3 shape itself; four govern its relationship with the bounding M3 and M4 metal layers.

**Width.** V3.W.1 requires a minimum width of 18 nm measured along the length of the M4 track.

**Projection spacing.** V3.S.1 encodes three sub-cases based on track alignment and is evaluated on derived mask geometry that classifies each V3 instance as either "with end-cap" (v3\_wec: at least one edge coincides with an M4 edge) or "no end-cap" (v3\_nec: all edges flush with M4). For v3\_nec instances the mask is the via sized by 5 nm; for v3\_wec instances the mask is the union of the via and the M4-coincident edges extended by 5 nm. Three minimum projection spacings apply: 18 nm (same M4 track), 27 nm (parallel M4 tracks, not aligned), and 18 nm (parallel M4 tracks, aligned). There is also an auxiliary projection-space check of 1 nm on the merged mask, and an 18 nm projection check on the non-M4-coincident edges of the v3\_maskav layer.

**Corner-to-corner (Euclidean) spacing.** V3.S.2 (23 nm), V3.S.3 (30 nm), and V3.S.4 (27 nm) apply when the projection-space check passes but the Euclidean check fails, i.e., the violation polygon does not interact with its projection counterpart. V3.S.2 fires when both vias carry the 5 nm M4 end-cap (v3\_wec pair, Euclidean threshold 16.4 nm before mask expansion). V3.S.3 fires when neither via carries the end-cap (v3\_nec pair, Euclidean threshold 16.12 nm before mask expansion). V3.S.4 fires on a mixed pair (v3\_wec vs. v3\_nec mask, separation check at 17.11 nm Euclidean).

**M3 enclosure.** V3.M3.EN.1 requires M3 to enclose V3 by at least 5 nm on at least two opposite sides. The check passes if the via fits inside m3.sized(-5 nm, 0) (left–right pair) or inside m3.sized(0, -5 nm) (top–bottom pair). Failure is the union of vias satisfying neither condition and vias falling entirely outside M3.

**M4 enclosure.** V3.M4.EN.2 requires M4 to enclose V3 by at least 11 nm on at least two opposite sides.

**Containment.** V3.AUX.1 requires every V3 instance to lie fully inside the intersection of M3 and M4. V3.M4.AUX.2 further requires that the via width perpendicular to the M4 length exactly matches the M4 width at that location: the via must share at least two coincident edges with M4 on opposite sides.

**Non-orthogonal geometry.** The global GEOMETRY.NONORTHOGONAL block applies to V3. All V3 edges must be strictly orthogonal (0° or 90°); edges at any angle in the ranges 1°–89°, 91°–179°, −179° to −91°, and −89° to −1° are flagged.

---

## Observations from Measured Trial

Trial `i01.ug.whole_design.00` is the sole measured record for this layer and iteration. It operated on Block5 under the unit\_gate channel, applied 19 operations across layers M1–M5 and V1–V4, and was accepted (`decision: gated_in`, `conn_preserved: true`).

The operation set included 14 instance moves and 3 polygon-level edits. Instance displacements ranged from −48 to +136 dbu on the x-axis and −48 to +96 dbu on the y-axis. Two polygon operations targeted specific shapes: polygon p879 received a y-axis high-end resize of +48 dbu; polygon p910 was translated +8 dbu on x and then received a y-axis high-end resize of +20 dbu. The mix of instance moves with targeted polygon end-resizes, applied together in a single gated pass, produced a connectivity-preserving accepted outcome in trial `i01.ug.whole_design.00`.

No trial in this history isolates a single V3 DRC rule violation and its repair in isolation. The single accepted trial demonstrates that simultaneous adjustment of multiple instances across several metal and via layers, combined with localized polygon resize operations, is a viable repair strategy, but the history does not yet identify which specific rule or rules drove the V3-touching changes in trial `i01.ug.whole_design.00`, nor does it record a rejected trial. Rule-specific repair heuristics for V3.W.1, V3.S.1–S.4, V3.M3.EN.1, V3.M4.EN.2, V3.AUX.1, V3.M4.AUX.2, and GEOMETRY.NONORTHOGONAL cannot be derived from one accepted multi-layer pass; additional measured history with per-rule attribution is needed before rule-specific guidance can be asserted.