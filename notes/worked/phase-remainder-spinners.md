# Phase left over after complete turns

Standalone insert requested after the color-linked path diamond. It uses two
complex arrows and three trials for increasing path lengths. Each trial
continues from the previous stopping position, starting at zero in trial 1.
The left arrow advances 30 degrees each time, accumulating one quarter turn
over all three trials; the right completes many turns. Previous stopping
positions stay visible as ghost arrows, numbered only on the right.

## Proposed manuscript blurb

For a path of length $L$, the accumulated phase can be written as

\[
\phi=\frac{2\pi L}{\lambda}=2\pi n+\theta,
\qquad 0\leq\theta<2\pi.
\]

Each complete turn brings the arrow back to the same direction. Its final
orientation therefore depends only on the remainder $\theta$. The shorter
the wavelength, the more sensitively this remainder responds to a change in
path length: nearby paths can finish at widely different angles after their
complete turns are removed. Across a family of nonstationary paths, these
varying directions largely cancel in the sum. Near a stationary path, the
phase varies more slowly and a net contribution survives.

The remainders are calculated, not randomly chosen. The spinner insert
illustrates their sensitivity to small path-length changes; its three
examples are not themselves a demonstration of full interference cancellation.

## Model and visible values

Use illustrative lengths 1, 2, 3 in the same arbitrary length unit.
The increment is 1 on both sides. Wavelengths are 12 and 5/47. The full
phase is exactly $2\pi L/\lambda$ in this schematic propagation-phase example.
No wavelength-dependent amplitude or diffraction-field claim is made.

| Run | Slow: full phase advance | Fast: full turns + remainder |
|---|---|---|
| 1 | 30° | 9 + 144° |
| 2 | 60° | 18 + 288° |
| 3 | 90° | 28 + 72° |

Each trial adds 30° on the left and 9.4 complete revolutions on the right.
The right stopping direction therefore advances 144° modulo one turn. These are deterministic
values, with no random-number generator or independently chosen final angles.
The left displays its full phase advance without a remainder sector or
complete-turn counter. Its previous endpoints are clearly separated. The right
shows its complete-turn counter and a gold sector marking the final positive
counterclockwise remainder from the real axis, in [0,360°).

This is three trials, not exactly three revolutions per spinner. Each trial
takes 3.6 seconds and holds for 1.8 seconds; the initial prelude is 0.8 seconds.
Total duration is 17 seconds, 1,020 frames, 60 fps, 1440 × 870. Smooth display
pacing makes starts and stops readable. Playback depicts accumulated phase,
not physical optical time. The fastest sampled advance is about 23.50° per
frame, below the 180° per-frame rotation-aliasing boundary.

## Files and checks

- Generator: `scripts/generate_symmetry_phase_remainder_spinners.py`
- Movie: `content/drafts/animations/symmetry-phase-remainder-spinners.mp4`
- Three stopped-run PNGs, source and encoded contact sheets, and source and
  encoded validation JSON files share the movie stem.
- The prior movie and companions are preserved in
  `content/drafts/animations/iterations/phase-remainder-v1/`; its generator is
  `scripts/iterations/generate_symmetry_phase_remainder_spinners-v1.py`.
- The next version, with nearly coincident left endpoints, is preserved in
  `content/drafts/animations/iterations/phase-remainder-v2/` and
  `scripts/iterations/generate_symmetry_phase_remainder_spinners-v2.py`.

Checks verify the equal path-length increment, phase ratio, full-phase versus
remainder complex-exponential identity, the six endpoint angles, playback
sampling, stopped states, and uninterrupted forward motion across trial
boundaries. Encoded verification decodes all 1,020 frames
and checks representative images and both spinner tips against source renders.
Rendered stills are inspected for numeral and axis-label collisions.

```powershell
python -B scripts/generate_symmetry_phase_remainder_spinners.py --check --preview --render --encoded-check
```
