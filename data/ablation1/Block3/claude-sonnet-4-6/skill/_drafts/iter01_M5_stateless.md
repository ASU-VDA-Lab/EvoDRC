## Effective Repairs

**M5 vertical shrink in via cells resolves multi-window violations.** A single y-axis resize of -88 dbu on M5 shape_index 0 in cell VIA_VIA45_1_2_58_58 was applied and reduced the combined violation count by 20 (leaf_0018: -11, leaf_0019: -9) (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02). Prefer a single-op M5 y-resize over multi-op cross-layer sequences when both target the same via-cell locus.

**A single-op M5 edit outperforms a five-op V4/M4 sequence on the same locus.** The five-operation sequence touching V4 (two move + two resize) and M4 (one resize) achieved only a -18 combined delta and lost the tournament (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01), while the single M5 y-resize achieved -20 and was applied (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02). Do not prefer V4/M4 reshaping over direct M5 resizing for violations that manifest in M5-containing windows at this locus.

## Via Enclosure and M5 Vertical Extent

**Reducing M5 vertical extent addresses enclosure-related violations in via cells.** Rule V4.M5.EN.2 requires V4 to be enclosed by M5 by at least 11 nm on two opposite sides; rule V5.M5.EN.1 imposes the same 11 nm two-sided enclosure requirement for V5. Rule V4.M5.AUX.2 requires V4 width to exactly match M5 width along the direction perpendicular to M5 length. In cell VIA_VIA45_1_2_58_58, a y-axis shrink of M5 by 88 dbu cleared violations tracked across two windows without breaking connectivity (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02, conn_preserved: true). Shrinking M5 vertically in via cells is safe with respect to connectivity provided the enclosure floor (11 nm each side) is respected.

**The minimum vertical width constraint (M5.W.5 = 44 nm) bounds how far M5 may be shrunk vertically.** Any y-axis resize applied to M5 must leave vertical width at or above 44 nm. The successful -88 dbu shrink (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02) was applied without triggering M5.W.5, confirming the pre-repair vertical extent in this via cell exceeded 132 nm.

## Locus and Window Scope

**Both leaf windows (leaf_0018, leaf_0019) at locus [1728, 2068, 11016, 10892] respond to M5 y-resize.** The applied repair (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02) reduced violations in both windows simultaneously with one operation, indicating that a single M5 geometry change propagates improvement across co-located DRC windows for this via cell. When repairing violations in multiple windows sharing this locus, target M5 directly rather than distributing ops across V4 and M4.

## Op-Count and Tournament Outcomes

**More operations do not guarantee a tournament win.** Five ops across V4 and M4 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, decision: lost_tournament) were outscored by one op on M5 (trial:i01.cu.def:VIA_VIA45_1_2_58_58.02, decision: applied). Minimize op count and layer count when targeting M5-window violations; the tournament scorer favors repair efficiency.