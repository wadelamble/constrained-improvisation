# Tip-to-tail with A as the phase reference

This standalone side-conversation experiment isolates the phasor pane of
`symmetry-many-slit-paths-phasors-interference.mp4` and removes its subtraction
of the straight A–B path length. Existing films and generators are preserved.

The only mathematical change is from `theta_j = k (L_j - AB)` to
`theta_j = k L_j`. The original 49 slit positions, spherical path lengths,
geometric-spreading weights, top-to-bottom addition order, and 18.5-second
timeline are reused directly from the original generator. This retains that
film's illustrative path model; it does not add a normalized propagation
kernel or substitute the later progressive animation's model.

The complex-plane origin, scale, and axes remain fixed throughout. Playback
first builds the chain at central B, then follows the original detector sweep
and final hold. No temporal carrier rotation is added; playback reveals sums
and varies B with the source phase held at zero. At the central B, AB is exactly
18 wavelengths, so removing the subtraction leaves the starting orientation
unchanged modulo a full turn.

- Source: `scripts/generate_symmetry_tip_to_tail_source_phase.py`.
- Film: `content/drafts/animations/symmetry-tip-to-tail-source-phase.mp4`.
- Stills: the same prefix followed by `-check-<seconds>.png`.
- Generate: `python scripts/generate_symmetry_tip_to_tail_source_phase.py --render`.

The generator checks that each new arrow equals the corresponding old arrow
multiplied by the common factor `exp(i k AB)`, that intensity is preserved, and
that all complete chains stay within the fixed plot throughout playback. It
also verifies the encoded frame count and duration and decodes the complete MP4.

Validation: the common-rotation identity agreed to 1.89e-14 per arrow and the
largest absolute intensity difference was 1.53e-12. Every full chain retained
at least 29.9 pixels of plot margin. The finished H.264/yuv420p film is 960 by
840 at 24 fps, 444 frames, 18.5 seconds. Full decode passed; nine encoded frames
covering buildup, center hold, sweep, and final hold were inspected for layout.
