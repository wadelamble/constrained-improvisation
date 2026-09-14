# Blue/red wave bookends for the desktop animation

The current version 7 has a four-second wave introduction and no closing
wave segment. Local intensity controls color strength throughout the wave,
without an added detector strip or curve. See
[the current wave encoding](desktop-wave-intensity-field.md). The 49-slit physical
model from version 5 is retained; see
[the physical-slit correction](desktop-49-physical-slits.md).

## Historical versions 3 and 4

Versions 3 and 4 opened and closed with three seconds of a
full-frame signed wave field. At 24 fps, the sequence is 72 wave frames,
444 accepted three-pane frames, and 72 wave frames: 24.5 seconds in total.

The field comes from `scripts/corrected_tip_to_tail_model.py`, the same
calculation used by the corrected arrows. Source A remains an outgoing
cylindrical source at (-4.5, 0), the wavelength is 0.5, and the aperture at
x = 0 extends from y = -2.8 to 2.8. The 49 adjacent aperture elements are
integration intervals; the wave picture therefore adds no opaque bars
between them. Detector B is at x = 4.5, y = 0 in the opening, and y = 0.94
in the closing, matching the middle sequence's initial and final B.

Before the aperture, the field is the original source field. Beyond it,
the renderer integrates that field against the same normalized outgoing
propagation kernel over all 49 elements. Both sides use the same amplitude
reference and the same fixed +5.057997625773197-degree display rotation
described in `tip-to-tail-centered-presentation.md`. The sum at central B
is consequently horizontal in the diagram and positive real at the
adjacent wave frame. The presentation phase adjustment is retained
explicitly; the field is not recalibrated separately for the closing B.

Each bookend advances the optical carrier by one cycle per three seconds.
The opening's last frame and the closing's first frame have carrier phase
zero. The intervening arrows represent complex amplitudes, without a
running optical clock. The color is the instantaneous real part: positive
red, negative blue, and zero muted purple. Version 4 uses one continuous,
low-contrast color map everywhere and at every time:
`mix(blue, red, (1 + tanh(real(field) / 1.3)) / 2)`. The endpoints are muted
slate blue (88, 121, 158) and dusty red (166, 109, 117); their midpoint is
purple (127, 115, 137.5). Purple marks a zero crossing of the signed field,
not a third component of the wave. There are no dark contour bands or
wave outlines. A smooth color transfer replaces version 3's near-black
zero and sublinear contrast curve; the complex field is unchanged.

The view is pulled back equally in both directions to make the opaque
screen ends clearly visible. Solid graphite bars mark the screen outside
the finite opening, with pale end caps and an offset opening bracket.
The detector line is also visible. These are drawing changes; they do not
introduce another barrier or change the aperture. The source and detector
labels use the restrained colors of the middle diagram.

The complex field is calculated at 640 by 360 sample centers, with equal
horizontal and vertical physical scales, then interpolated to 1280 by 720
before coloring. Quadrature is refined near the aperture, where the
propagation kernel becomes sharply localized. Checks compare the wave at
129 detector positions with the complete arrow sums, compare near-screen
quadrature with a finer rule, and check sampled field columns against the
same propagation integral.

The 18.5-second middle is stream-copied into the combined MP4. All 444
decoded middle-frame hashes must match the accepted source. The complete
movie is decoded, counted, and sampled for its contact sheet before the
canonical filename is replaced. Previous assets and generator snapshots
are retained under the corresponding `iterations/` directories.

## Regeneration

The usual entry point produces the entire movie, including both bookends:

```powershell
python -B scripts/generate_symmetry_many_slit_paths_phasors_interference.py
```

The dedicated implementation is
`scripts/generate_symmetry_desktop_wave_bookends.py`. Its `--preview`
option produces wave stills and numerical checks without replacing the
canonical movie. The current generator recalculates a 49-slit body by
default. Its `--reuse-middle` option requires a matching model fingerprint
and video hash in the body's `.model.json` file. The old version 2
continuous-opening body cannot be reused in the current slit-mask movie.

The original v1 and centered v2 movies remain available. The first extended
movie is saved as
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v3-wave-bookends.mp4`.
The softened revision with the visible screen and opening is saved as
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v4-soft-wave-bookends.mp4`.
The corrected 49-slit revision is saved as
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v5-49-physical-slits.mp4`.
The canonical and versioned validation JSON files record timing, hashes,
field agreement, and the locations of the previous assets.
