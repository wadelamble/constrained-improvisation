# Wave introduction with a visible detector pattern

Historical version 6: the current version 7 removes the strip and extra
curve and carries intensity in the wave colors themselves. See
[the current wave encoding](desktop-wave-intensity-field.md).

Version 6 opens with four seconds of the wave and then shows the checked
18.5-second three-pane sequence. There is no closing wave segment. The
complete movie has 540 frames at 24 fps and lasts 22.5 seconds.

The scene uses the same warm paper background and restrained graphical
language as the schematic. Blue and red show the instantaneous signed
field; zero is warm paper. Color opacity is
`.84 * abs(tanh(real(field) / 1.4))`, with one fixed map everywhere and no
separate gain for the transmitted wave. Two slow carrier cycles run during
the introduction, ending at the established display phase zero.

Source A, all 49 separate slits, the projection screen, and B are visible.
The wave is cropped with equal horizontal and vertical physical scales.
Both the screen drawing and the propagation integrals use the unchanged
finite slit bounds from `perforated_tip_to_tail_model.py`.

The projection screen now has two linked representations:

- A 22-pixel strip whose brightness is proportional to `abs(total(B))**2`.
  One fixed exposure makes its maximum visible. It multiplies all values
  equally, with no subtraction of the minimum, retaining bright/dim ratios.
  The strip stays constant as the red/blue optical carrier moves.
- The same blue detector profile as pane three, plotted beside the strip
  with the same absolute intensity axis range, starting at zero. The gray
  no-screen reference remains. A gold guide and green marker identify the
  value at central B.

The strip, profile, and wave share their vertical coordinate, so bright
regions line up with intensity peaks. The approximately 0.27-to-0.45
variation is not stretched to black and white by subtracting a background.
The caption distinguishes moving wave phase from the steady intensity.

The version 5 body is reused with its matching model fingerprint and video
hash, then stream-copied after the intro. All 444 decoded body frames must
remain identical. The completed movie is decoded, counted, and inspected
through encoded preview frames. Previous media and source are preserved.

## Regeneration

```powershell
python -B scripts/generate_symmetry_many_slit_paths_phasors_interference.py
```

The historical implementation filename,
`scripts/generate_symmetry_desktop_wave_bookends.py`, now produces the intro
and body only. Its `--preview` option generates stills without replacing the
movie. `--reuse-middle` accepts a matching 49-slit body with its `.model.json`
record; otherwise regeneration builds a fresh body from the shared model.

The saved version is
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v6-wave-and-intensity-intro.mp4`.
It is also copied to the canonical
`content/drafts/animations/symmetry-many-slit-paths-phasors-interference.mp4`.
Validation JSON and a contact sheet accompany the versioned film.
