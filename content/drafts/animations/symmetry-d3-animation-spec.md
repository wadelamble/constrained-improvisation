# D3 Animation Spec

Working scope: only the two D3 representation animations below.

## Rotations / Flips

- Two panes.
- Both panes show 3D coordinate axes.
- The origin sits near the lower left, with the axes extending a little into the negative sectors.
- The rotation axis is drawn.
- A state vector is drawn from the origin.
- Rotation pane: the state vector rotates in three clicks, traces a triangle, and returns where it began.
- Flip pane: similar visual grammar for a flip.

## 3D / 2D

- Single pane.
- Stage 1 is like the rotation side of the rotations/flips animation.
- Instead of showing one vector rotating, show one vector, then a second different vector, then a third.
- Stage 2 stacks the three triangle orbits "Towers of Hanoi style."
- Then collapse the stacked triangle orbits to a plane.

The spec is directional. Intelligent choices are allowed when they better serve clarity, visual quality, or the manuscript's explanation.
