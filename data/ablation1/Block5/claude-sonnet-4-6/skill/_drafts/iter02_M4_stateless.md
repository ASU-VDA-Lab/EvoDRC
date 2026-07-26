**Via enclosure and coordinated chain resizing**

The only applied repair in this layer's history (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00) used a `chain_fix` group that simultaneously grew the M4 via-bar shape on VIA_VIA45_1_2_58_58 by +88 dbu in the y-axis alongside matching +88 dbu growth on both V4 shapes in the same cell and both V3 shapes in VIA_VIA34_1_2_58_52. That coordinated resize reduced the total DRC count by 13 (unit:leaf_0009 fell from 25 to 18; unit:leaf_0010 fell from 25 to 19). Resize operations on M4 that target V3.M4.EN.2 (minimum 11 nm enclosure of V3 on two opposite sides) and V3.M4.AUX.2 (V3 width must equal M4 width perpendicular to M4 length) must therefore keep V3 and M4 y-dimensions synchronized; resizing M4 alone without the paired V3 resize leaves V3.M4.AUX.2 unsatisfied.

**Shrink operations on adjacent via structures increase M4 violations**

The rejected trial (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01) applied negative y-deltas to M3 and V3 shapes in adjacent via cells (VIA_VIA34_1_2_58_52 and VIA_VIA23_1_3_36_36) along with symmetric shrinks of −32 dbu on both ends of M4-adjacent polygons p891, p892, and p893, while M4 was listed in `touched_layers`. The net result was +5 total DRC violations (unit:leaf_0005 rose from 20 to 28, partially offset by unit:leaf_0006 falling from 16 to 13), and the trial was rejected. Shrink operations that reduce enclosing metal on all sides simultaneously drive M4 into V3.M4.EN.2 failure; the asymmetry between the one window that worsened (+8) and the one that improved (−3) confirms that bilateral symmetric shrinks of the enclosing bar do not satisfy the two-opposite-sides enclosure requirement.

**Width rules constrain delta magnitudes**

Rule M4.W.1 sets 24 nm as the minimum vertical width. Rule M4.W.2 caps vertical width at 480 nm. Rules M4.W.3 and M4.W.4 prohibit vertical widths that are exact even integer multiples of 24 nm (48, 96, 144, 192, 240, 288, 336, 384, 432, 480 nm) or that correspond to an even number of minimum-width routing tracks (72, 168, 264, 360, 456 nm). The +88 dbu growth applied in trial:i01.cu.def:VIA_VIA34_1_2_58_52.00 was accepted without triggering M4.W.3 or M4.W.4 violations, establishing that a delta of +88 dbu on the via-bar shape in that geometry did not land on a prohibited width. Any proposed y-axis delta must be checked against the post-resize absolute width to confirm it does not equal 48, 72, 96, 144, 168, 192, 240, 264, 288, 336, 360, 384, 432, 456, or 480 nm.

**Grid alignment of horizontal edges**

Rule M4.AUX.1 requires all M4 horizontal edges to lie on a 24 nm vertical grid. Rule M4.AUX.2 requires minimum-width M4 tracks (those not surviving a ±13 dbu sized erosion) to have their centerlines on the routing track grid (pitch 192 dbu, offset 48 dbu from the origin). The applied trial (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00) grew the M4 shape by +88 dbu and was not rejected for grid violations, so the pre-existing edge positions combined with a +88 dbu shift remained on the 24 nm grid in that specific geometry. No repair should be proposed that moves a horizontal M4 edge to a position not divisible by 24 dbu, and no minimum-width track centerline should be moved off the 192 dbu pitch / 48 dbu offset grid.

**No-bend and no-nonorthogonal constraints**

Rule M4.AUX.3 prohibits any M4 polygon from having bends (corners in the 0–90° range trigger a violation). The GEOMETRY.NONORTHOGONAL block prohibits any edge with angle outside {0°, 90°, 180°, 270°}. All ops in both trials used axis-aligned y-direction resizes, consistent with these constraints. Resize operations must remain strictly axis-aligned and must not introduce new corners into M4 shapes.

**Horizontal spacing and tip rules**

Rules M4.S.2 (40 nm minimum horizontal spacing between vertical M4 edges), M4.S.3 (40 nm minimum tip-to-tip spacing for polygons not sharing parallel run length on adjacent tracks), and M4.S.4 (40 nm minimum tip-to-tip spacing for polygons sharing parallel run length) were not cited as the direct violation target in either trial but are active constraints. Rule M4.S.1 sets 24 nm minimum vertical spacing. Rule M4.S.5 sets 44 nm minimum parallel run length on adjacent tracks. The shrink trial (trial:i02.cu.def:VIA_VIA23_1_3_36_36.01) reduced run lengths and enclosure margins simultaneously; the net violation increase is consistent with M4.S.5 or enclosure rules tightening as bars shorten.

**V4 enclosure**

Rule V4.M4.EN.1 requires V4 to be enclosed by M4 by at least 11 nm on two opposite sides. The applied trial (trial:i01.cu.def:VIA_VIA34_1_2_58_52.00) resized both V4 shapes in VIA_VIA45_1_2_58_58 by +88 dbu in y alongside the M4 resize; this joint growth was the construct that achieved net violation reduction. Growing V4 without growing M4 by at least the same amount would erode the V4.M4.EN.1 margin; growing M4 without growing V4 by the same amount would violate V3.M4.AUX.2 if V3 is also present and synchronized to V4 height.