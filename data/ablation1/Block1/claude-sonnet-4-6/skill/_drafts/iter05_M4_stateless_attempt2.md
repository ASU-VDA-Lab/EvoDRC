**X-axis end-resize is the validated repair primitive for M4 in the unit_gate channel.**

Both accepted M4 outcomes used `resize_end` operations on the x-axis. In trial:i02 the high end of p1216 was extended by 132 dbu; in trial:i05 the low end of p1187 was extended by 44 dbu. Both were gated in with `conn_preserved` true and zero new violations inside or outside the crop region. X-axis `resize_end` operations in the unit_gate channel have a clean acceptance record across the two unit_gate trials observed (trial:i02, trial:i05).

**Use extension steps of at least 44 dbu when growing M4 horizontally.**

The 44 dbu horizontal extension applied to p1187 in trial:i05 aligns with M4.W.5's 44 nm minimum horizontal width floor. The trial:i05 repair was gated in with zero new crop violations. Applying an extension step below 44 dbu risks leaving the modified polygon in violation of M4.W.5; 44 dbu is the smallest step confirmed safe by trial:i05.

**Combine polygon deletion with neighbor extension as a composite M4 repair.**

Trial:i05 deleted p1211 and simultaneously extended the low end of p1187 by 44 dbu. The composite was gated in with connectivity preserved and no new violations in the crop window. When a polygon on M4 is to be removed, extend an adjacent M4 polygon in the same operation rather than leaving the space unoccupied; trial:i05 demonstrates this pattern produces a clean outcome.

**Do not commit M4 moves in the cu_pool channel when the aggregate violation delta across windows is positive.**

Trial:i03 moved p1143 by +32 dbu and p1142 by −16 dbu on the x-axis in a cu_pool operation. Unit leaf_0007 improved by 2 violations (175 → 173) while unit leaf_0008 worsened by 18 (113 → 131), yielding an aggregate delta of +16. The decision was `rejected_net_positive`. Per-window improvement does not override a positive aggregate; evaluate the sum across all affected windows before committing any M4 repositioning in the cu_pool channel (trial:i03).

**Multi-layer cu_pool operations that include M4 moves are still subject to net-delta rejection.**

Trial:i03 resized via shapes in M5 (VIA_VIA45\_1\_2\_58\_58 and VIA\_VIA56\_2\_2\_66\_58) alongside the M4 moves, touching layers M4, M5, M6, V4, and V5. The cross-layer operation was rejected on the aggregate delta. Spanning additional layers does not relax the net-positive rejection criterion; all windows affected by the combined M4-and-via operation must be evaluated together (trial:i03).