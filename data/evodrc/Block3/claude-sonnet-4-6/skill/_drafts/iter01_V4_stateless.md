## General Repair Orientation

Only one measured trial exists for V4 at iteration 1: trial:i01.cu.def:VIA_VIA45_1_2_58_58.01. All prescriptive guidance below is grounded exclusively in that record.

## Multi-Shape, Multi-Layer Compound Repairs

The single accepted repair (trial:i01.cu.def:VIA_VIA45_1_2_58_58.01) consisted of five operations across three layers (M4, M5, V4) applied to cell `VIA_VIA45_1_2_58_58`. Do not attempt to fix V4 violations by editing V4 geometry alone; the winning op sequence also included an M4 x-axis resize alongside the V4 moves and resizes. Isolating the repair to V4 only is unverified and inconsistent with the recorded approach.

## Symmetric Outward Move + Resize on X Is an Effective Pattern

In trial:i01.cu.def:VIA_VIA45_1_2_58_58.01, two V4 shapes within the same via cell were moved symmetrically outward along the x-axis (shape 0 by −116 dbu, shape 1 by +116 dbu) and each was simultaneously resized by +384 dbu on x. This compound move-then-resize sequence on both shapes reduced the violation count by 18 across two neighboring DRC windows (leaf_0018: −10, leaf_0019: −8) while preserving connectivity. Apply symmetric outward displacement paired with x-axis enlargement when two V4 shapes in the same via cell are involved and x-axis spacing or enclosure is the suspected driver.

## M4 Co-Resize Is Required When V4 Is Resized on X

The accepted repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 included an M4 shape resize of +152 dbu on x in addition to the V4 shape changes. Rules V4.M4.EN.1 (≥11 nm enclosure on two opposite sides by M4) and V4.AUX.1 (V4 must lie inside both M4 and M5) both constrain the relationship between V4 geometry and M4 geometry. Expanding V4 on x without co-expanding M4 risks creating or worsening V4.M4.EN.1 or V4.AUX.1 violations. Always include an M4 resize step when V4 shapes are resized in x.

## Width and Enclosure Thresholds to Respect

V4.W.1 requires a minimum V4 width of 24 nm. V4.M4.EN.1 requires M4 to enclose V4 by at least 11 nm on two opposite sides along the M5 length direction. V4.M5.EN.2 requires M5 to enclose V4 by at least 11 nm on two opposite sides. V4.M5.AUX.2 requires V4 width to exactly match M5 width in the direction perpendicular to M5 length. The repair in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 expanded V4 shapes by 384 dbu on x while preserving connectivity, confirming that substantial x-axis enlargement is compatible with clean rule checks when M4 is co-resized.

## Spacing: All Spacing Rules Use 33 nm and Apply Projection or Euclidean

V4.S.1 and V4.S.2 enforce 33 nm minimum spacing under projection; V4.S.3 enforces 33 nm corner-to-corner under Euclidean distance. The symmetric outward movement of +116/−116 dbu (11.6 nm in a 10 dbu/nm grid, or another scale depending on DBU) applied in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 increased inter-shape separation. When the net effect of a move+resize changes the projected or Euclidean gap between V4 instances, verify the 33 nm threshold under all three spacing rules before committing the repair.

## Orthogonality Must Be Preserved

The NONORTHOGONAL rule applies globally to all drawing layers including V4. All move and resize operations in trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 acted exclusively on the x-axis, producing only rectilinear shapes. Never introduce diagonal edges into V4 geometry during repair; restrict all move and resize deltas to axis-aligned (x or y) operations.

## Connectivity Preservation Is Achievable With Compound Repairs

trial:i01.cu.def:VIA_VIA45_1_2_58_58.01 records `conn_preserved: true` despite modifying five shapes across three layers. Symmetric outward moves of V4 shapes combined with proportional resizes do not sever connectivity when the via still overlaps both M4 and M5 after the operation.