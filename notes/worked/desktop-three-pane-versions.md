# Desktop three-pane animation: current version and archives

The canonical asset remains:

[symmetry-many-slit-paths-phasors-interference.mp4](../../content/drafts/animations/symmetry-many-slit-paths-phasors-interference.mp4)

Version 7 retains 49 physical slits with opaque gaps in every view and
calculation. It contains the centered, amplitude-scaled tip-to-tail diagram
in pane two. Pane one uses the matching slit geometry, and pane three uses
the intensity from the same corrected contributions. The phase
reference is the completed sum at central B, fixed throughout the film.
The gray phasor comparison is omitted; the gray no-screen intensity curve
remains. The 1280 by 720 layout and 24 fps are retained. The four-second wave
introduction uses color strength to show local intensity throughout the
travelling field, with hue showing phase. It has no added detector strip or
curve. The 18.5-second version 5 body follows unchanged. There is no closing
wave segment: the complete current film is 22.5 seconds long.

The canonical contact sheet and final PNG are updated to match the video.

## Saved versions

- [Version 1: original desktop animation](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v1-original.mp4).
  The original final PNG and contact sheet have the same `-v1-original`
  prefix. Its generator source was copied, before editing, to
  `scripts/iterations/generate_symmetry_many_slit_paths_phasors_interference-v1-original.py`.
- [Version 2: centered corrected desktop animation](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v2-centered.mp4).
  Its final PNG, contact sheet, and validation record share that prefix.
  The renderer and model source snapshots are also saved under
  `scripts/iterations/` with a `-v2-centered.py` suffix.
- [Version 3: matching wave bookends](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v3-wave-bookends.mp4).
  Its wave uses the same source, aperture, propagation kernel, amplitude
  units, and fixed display phase as the arrows. Its final PNG, contact
  sheet, and validation record share that prefix. Timestamped generator
  snapshots are saved under `scripts/iterations/` with a `-v3.py` suffix.
- [Version 4: softer waves and visible screen](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v4-soft-wave-bookends.mp4).
  Muted red and blue blend continuously through purple, without black
  contour bands. The view is pulled back slightly and the physical screen,
  opening edges, and detector are drawn clearly. Physics and timing are
  unchanged. Its validation record and previews share the same prefix;
  source snapshots have a `-v4.py` suffix.
- [Version 5: 49 physical slits throughout](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v5-49-physical-slits.mp4).
  Corrects the continuous-opening substitution in versions 2 through 4.
  All waves, arrows, and intensities now integrate over 49 disjoint finite
  openings with opaque gaps, and both screen drawings use those same
  bounds. Soft colors and 24.5-second timing remain. Source snapshots use
  a `-v5.py` suffix.
- [Version 6: wave and intensity introduction](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v6-wave-and-intensity-intro.mp4).
  Four seconds of blue/red waves on warm paper, with a projection strip
  whose brightness follows the arriving intensity and the same blue
  profile as pane three. The checked version 5 body is preserved frame
  for frame; there is no closing wave. Total duration is 22.5 seconds.
- [Version 7: intensity in the wave itself](../../content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v7-intensity-in-the-wave.mp4).
  Removes the added strip and curve. The local intensity of the actual
  complex field controls the strength of the wave colors everywhere; phase
  changes their hue. The detector variation remains linear and unclipped.
  The four-second intro and checked body retain the 22.5-second timing.

The separately named corrected and centered experiments are preserved too.
Version 2 is a byte-identical copy of the validated
`symmetry-many-slit-corrected-centered.mp4`, not a new physical calculation.
The explicit phase adjustment is described in
[the centered presentation note](tip-to-tail-centered-presentation.md).
The wave calculation, timing, and checks are described in
[the wave bookends note](desktop-wave-bookends.md).
The current mask and corresponding recalculation are documented in
[the 49-slit correction](desktop-49-physical-slits.md).
The current wave design is described in
[the intensity-in-the-wave note](desktop-wave-intensity-field.md). The
[four-second introduction note](desktop-wave-intro.md) records version 6.

## Regeneration

The established generator entry point now delegates to the approved
renderer and wave-introduction assembler:

```powershell
python -B scripts/generate_symmetry_many_slit_paths_phasors_interference.py
```

It saves the current video and preview assets under a timestamped prefix in
`content/drafts/animations/iterations/`, renders a separate new version,
checks it, and then updates the canonical filenames. Future renders thus
retain the centered treatment and four-second wave introduction and preserve
the previous media. Regeneration builds a fresh 18.5-second 49-slit body
before adding the introduction; it never adds to an already extended movie.

Legacy geometry, timing, and raw-model helper functions remain in the old
module for existing reel derivatives. Its original `draw_frame` helper
remains historical; the canonical CLI output uses the corrected renderer.
Archived Python files are source snapshots rather than separate standalone
entry points. Current regeneration uses the files in `scripts/`.
