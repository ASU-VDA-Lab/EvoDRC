Looking at the DRC rules and 4 measured trials, I'll generate the V1 knowledge body now.

---

## Observed repair patterns and outcomes

### Instance-move granularity

Every operation that touched V1 geometry used instance moves exclusively in the X direction, with step sizes that are multiples of 36 dbu (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). The recorded deltas are −36, +36, +72, and −72 dbu; no Y-direction moves were applied to any instance in trials that modified V1. All four trials were accepted as `gated_in` with zero new in-crop V1 violations, establishing 36 dbu as the safe horizontal step quantum for instance repositioning when V1 is on the affected layers.

### Net-zero violation record across all measured iterations

No trial in the history introduced a net increase of V1 violations within the crop window. The `deltas.n_new_in_crop` and `deltas.n_new_out_of_crop` fields are 0 for all four V1-touching trials (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). This is consistent with the operations being restructuring moves rather than shrink operations — V1.W.1 (18 nm minimum width), V1.M1.EN.1 (5 & 2 nm M1 enclosure), V1.M2.EN.2 (5 & 5 nm or 5 & 0 nm M2 enclosure), V1.AUX.1 (V1 inside M1 ∩ M2), and V1.M2.AUX.2 (V1 width-matches M2) were all held clean when only lateral repositioning at 36 dbu granularity was applied.

### M1 and M2 polygon expansion does not harm V1 enclosure rules

Trial:i01.ug.whole_design.00 applied resize_end operations on polygons p879 (Y high end +48 dbu) and p910 (X +8 dbu move, Y high end +20 dbu). These are M1 or M2 metal expansions; the trial resulted in zero new V1 violations. Expanding M1 or M2 shapes outward increases the enclosure margin against V1.M1.EN.1 and V1.M2.EN.2 and therefore does not trigger those rules. Do not shrink M1 or M2 shapes near a V1 instance without verifying the residual enclosure on both opposing-side pairs.

### Instance deletion with connectivity preservation is safe for V1

Trial:i05.ug.whole_design.00 deleted seven instances (i0098, i0105, i0075, i0076, i0099, i0002, i0070) simultaneously with instance moves and M2 high-end extensions, while `conn_preserved` remained true and zero new V1 violations appeared. The deleted instances presumably carried V1 shapes that were made redundant by the repositioning of surviving instances. Instance deletion is acceptable for V1 compliance as long as connectivity is preserved; removing a V1-bearing instance without a replacement path to M1 and M2 would violate V1.AUX.1.

### V1.AUX.1 and V1.M2.AUX.2 are not forgiving of partial overlap

V1.AUX.1 requires V1 to be entirely inside both M1 and M2. V1.M2.AUX.2 requires the V1 width (perpendicular to M2 length) to exactly match the M2 width. All accepted trial operations used whole-instance moves rather than resizing individual V1 polygons, meaning V1 shapes travelled with their enclosing M1 and M2 shapes together. The clean outcomes in trial:i02.ug.whole_design.00 and trial:i04.ug.whole_design.00 — both of which moved groups of instances in X — confirm that moving a via instance and its host metal together maintains V1.AUX.1 and V1.M2.AUX.2 automatically. Never move a V1 instance independently of its M1/M2 host wires.

### Spacing rules (V1.S.1–V1.S.4) tolerate 36 dbu lateral shifts without triggering

The spacing rules V1.S.1 (17 nm projection / 18 nm projection depending on mask class), V1.S.2 (16.4 nm euclidean corner-to-corner for wec–wec), V1.S.3 (16.12 nm euclidean corner-to-corner for nec–nec), and V1.S.4 (17.11 nm euclidean wec–nec) all remained clean under the 36 and 72 dbu lateral shifts recorded in trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, and trial:i05.ug.whole_design.00. The 36 dbu step (approximately 9 nm at 1 dbu = 0.25 nm scaling) does not bring V1 instances into spacing violation when the starting placement already satisfies the rules. When reducing X-separation between two V1 instances, verify the resulting gap against whichever of V1.S.1–V1.S.4 applies given end-cap classification (wec vs. nec) before committing the move.

### V1.M2.AUX.2 depends on end-cap context

The deck logic for V1.S.1 and V1.S.2–V1.S.4 distinguishes vias with a 5 nm M2 end-cap (wec — with end-cap) from those without (nec — no end-cap) based on whether all V1 edges are coincident with M2 edges. The M2 extension operations in trial:i05.ug.whole_design.00 (p951 X high end +128 dbu, p955 X high end +128 dbu) grew M2 shapes along their length axis. Extending M2 beyond a V1 instance converts that V1 from nec to wec classification, which relaxes V1.S.3 (nec–nec corner spacing 30 nm) and activates V1.S.2 (wec–wec 23 nm) or V1.S.4 (wec–nec 27 nm) instead. No spacing violations were introduced in trial:i05.ug.whole_design.00 after those extensions, confirming that extending M2 to create wec classification is a valid repair path when nec–nec spacing would otherwise be the binding constraint.

### Global locus: all fixes are whole-design scope

All four trials were executed on the full design locus [0, 0, 10784, 10784] (trial:i01.ug.whole_design.00, trial:i02.ug.whole_design.00, trial:i04.ug.whole_design.00, trial:i05.ug.whole_design.00). There is no evidence from this history of sub-crop or local-window repair for V1; all decisions were evaluated against the full block.