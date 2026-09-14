# Restore 49 physical slits throughout the desktop movie

This records the version 5 physical correction. Version 6 retains this
model and body, with revised wave styling and timing described in
[the four-second introduction note](desktop-wave-intro.md).

Version 5 corrects the geometry error in versions 2 through 4: those versions
integrated 49 adjacent pieces of one continuous opening. The intended screen
has 49 separate openings with opaque material between them. Version 5 uses
that perforated mask in the wave calculation, individual arrows, intensity
curve, and both screen drawings.

## Shared geometry and calculation

Source A is at (-4.5, 0), the screen is at x = 0, and B lies on x = 4.5.
Wavelength remains 0.5. The original 49 slit centers are restored, equally
spaced between y = -2.8 and +2.8. The old drawing did not specify finite
physical slit widths. For this revision, each opening is 60% of the pitch:

- Center spacing: 0.1166666667.
- Slit width: 0.07.
- Opaque gap between adjacent slits: 0.0466666667.
- 49 disjoint open intervals, 48 internal opaque bars, and two outer opaque
  screen portions.

`scripts/perforated_tip_to_tail_model.py` defines `SLIT_BOUNDS`. Both screen
renderers draw its opaque complement, and both numerical integrations use
the same bounds. Each arrow is the integral of the incident source times
the complete outgoing propagation kernel over one finite slit. The field
beyond the screen is the sum of these same integrals evaluated across the
image. No light is transmitted through the opaque gaps in the mask, and
bars are not painted onto an independently calculated continuous opening.

The outgoing cylindrical source, scalar Rayleigh--Sommerfeld kernel,
wavelength, and amplitude reference G(9, 0) are reused from the validated
`corrected_tip_to_tail_model.py`. That earlier continuous-opening model is
preserved for its historical experiments. The physical scope remains an
ideal thin scalar transmission mask.

At central B, the slit-mask intensity is approximately 0.43627772 relative
to the unobstructed center. The amplitude therefore decreases visibly; the
wave does not receive a separate gain on its transmitted side. Its phase
relative to the unobstructed central field is approximately -1.87341523
degrees. The user-requested fixed display convention is retained by applying
+1.87341523 degrees to every phasor and the entire complex wave field.
The completed central sum is horizontal; later rotation and all relative
angles remain. This replaces the old continuous-opening offset of +5.058
degrees because the physical mask has changed.

## Drawing and timing

Both wave segments retain the muted blue-purple-red palette of version 4,
with purple at zero signed field and no black wave outlines. Each lasts
three seconds. The recalculated three-pane body lasts 18.5 seconds, for a
24.5-second film at 24 fps. The centered and final B positions remain 0 and
0.94, respectively.

Pane one draws the 49 finite openings and routes through their centers.
The gold completed route goes through the slit center closest to the
unconstrained stationary route; it never crosses an opaque bar. Each
centerline represents one slit integral rather than a zero-width hole.
Pane two uses amplitude-scaled arrows and one fixed plot scale across the
entire film. Pane three uses the squared magnitude of the same sum, with
the gray unobstructed intensity curve for comparison.

## Checks and regeneration

Numerical checks verify 49 nonoverlapping slits, zero transmission at every
gap center, correct opaque complements, 12 versus 24 quadrature points per
slit, independent adaptive integration over all 49 slits, and B symmetry.
They also confirm that the central result differs from one continuous
opening, preventing a repeat of this mistake.

The wave is checked against the arrow sums at 129 detector positions in
complex amplitude, phase, and intensity. Near-screen integration is checked
against a higher-order rule. Plot bounds are checked over every frame.
The assembled video is fully decoded and counted; its body frames must
match the freshly recalculated body exactly. Reusing a body requires a
matching model fingerprint and video hash in its `.model.json` file, so a
version 2 continuous-opening body cannot silently reappear in this movie.

```powershell
python -B scripts/generate_symmetry_many_slit_paths_phasors_interference.py
```

The usual generator delegates to `generate_symmetry_desktop_wave_bookends.py`,
which now uses `generate_symmetry_slit_tip_to_tail.py` and
`perforated_tip_to_tail_model.py`. Use the bookend generator's `--preview`
option to inspect wave and body stills without replacing the canonical film.

The canonical asset is
`content/drafts/animations/symmetry-many-slit-paths-phasors-interference.mp4`.
Version 5 is also saved as
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v5-49-physical-slits.mp4`.
Earlier media and source snapshots are retained under the respective
`iterations/` directories. Validation JSON accompanies the new film.
