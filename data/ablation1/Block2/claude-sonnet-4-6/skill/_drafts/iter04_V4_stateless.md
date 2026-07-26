Scanning the two history records and extracting grounded knowledge now.

**Via-cell M5 resize is the only repair channel that applied successfully for V4.**

The single applied fix touching V4 was a `resize_via_shape` operation on layer M5 (y-axis, delta −88 dbu) inside cell `def:VIA_VIA45_1_2_58_58`, executed by the `cu_pool` channel (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00). That one operation reduced total in-crop violations by 16 (from 23 to 15 in `unit:leaf_0002` and from 14 to 6 in `unit:leaf_0003`). Connectivity was preserved and the fix was committed. No unit_gate or other channel fix targeting V4 was applied across the full history.

**Shrinking M5 along its short axis (y) inside a via cell resolves multi-unit V4 violations simultaneously.**

The `cu_pool` repair in trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 propagated relief to two separate units (leaf_0002, leaf_0003) from a single via-cell edit. When the same via cell is instantiated across multiple units, a y-axis M5 shrink at the cell definition level repairs enclosure or width-matching violations wherever that cell appears. Prefer editing shared via cell definitions over per-instance operations when the same violation pattern recurs across units.

**V4.M5.AUX.2 and V4.M5.EN.2 are the rules most likely addressed by y-axis M5 resizing in a via cell.**

V4.M5.AUX.2 requires that V4 exactly match M5 width along the direction perpendicular to M5 length; V4.M5.EN.2 requires at least 11 nm enclosure on two opposite sides. A y-axis M5 shrink of 88 dbu within the via cell changes the M5 footprint perpendicular to its run direction, directly adjusting the enclosure margin and the width-matching relationship governed by these two rules. The −88 dbu (−8.8 nm in a 10 dbu/nm grid) correction at trial:i04.cu.def:VIA_VIA45_1_2_58_58.00 produced the only net-positive outcome in this history.

**Instance moves in the unit_gate channel introduce new V4 violations and must not be applied without post-move DRC gating.**

Both unit_gate trials that touched V4 were blocked (`gated_in`) because they introduced 2 new in-crop violations despite preserving connectivity. In trial:i03.ug.leaf_0002.01, eight instance moves (y-axis, ±24 to ±72 dbu) combined with an asymmetric x-axis resize of polygon p937 (+64 dbu low end, +320 dbu high end) disturbed M3/M4/M5/V3/V4 geometry and created new violations. In trial:i04.ug.leaf_0003.02, three smaller instance moves (y-axis, ±24 dbu on i0089, i0090, i0110) touching M2 through V4 also introduced 2 new in-crop violations. Both were suppressed. Do not commit unit_gate moves that touch V4 without confirming zero net increase in in-crop violations; the gating criterion is strict.

**Asymmetric polygon resizes on metal layers adjacent to V4 risk new spacing or enclosure violations.**

In trial:i03.ug.leaf_0002.01, polygon p937 was resized with unequal deltas on its two x-axis ends (+64 dbu low, +320 dbu high), a 5:1 asymmetry. This operation touched M5 along with the instance moves and contributed to the 2 new in-crop violations that caused gating. Asymmetric end-resizes on M5 polygons change the projection footprint seen by V4.S.1, V4.S.2, and V4.S.3 (all using projection spacing at 33 nm) in ways that are not symmetric about the via centerline. Prefer balanced resizes or via-cell-level edits (as in trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) over asymmetric polygon end-pulls when V4 spacing rules are at risk.

**V4.AUX.1 constrains any M4 or M5 move that shifts a via out of the intersection region.**

V4.AUX.1 fires whenever a V4 polygon is not fully contained within both M4 and M5. Instance moves of ±24 to ±72 dbu seen in trial:i03.ug.leaf_0002.01 and trial:i04.ug.leaf_0003.02 shift M4 and M5 relative to V4 shapes. If the move displaces M4 or M5 so that any part of a V4 polygon escapes their overlap, V4.AUX.1 will fire. The enclosure floors (V4.M4.EN.1, V4.M5.EN.2: 11 nm each on two opposite sides) must remain satisfied after every instance move; the observed ±24 dbu (2.4 nm) and ±72 dbu (7.2 nm) moves are sub-enclosure-margin but close enough to the 11 nm floor that stacked moves in the same direction can violate it.

**The same locus [1728,3148,10368,9812] in Block2 was targeted by both unit_gate trials without resolution.**

Trials i03.ug.leaf_0002.01 and i04.ug.leaf_0003.02 share the same crop window and the same Block2 case. Neither was applied. The cu_pool repair (trial:i04.cu.def:VIA_VIA45_1_2_58_58.00) used a wider locus [1632,2068,10368,9812] and was the one that succeeded. When unit_gate moves in a given locus repeatedly fail for V4, switch to cu_pool via-cell repair targeting the shared via definition rather than retrying instance moves.