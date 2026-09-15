# Widening apertures: wave propagation toward rays

Standalone candidate for the introductory animation in `symmetry-ccr-2.md`.
The earlier two-pane movies remain available. This version uses one physical
setup and the vivid red/blue-on-black palette confirmed from the portrait reel.

## Files

- Generator: `scripts/generate_symmetry_widening_apertures.py`
- Movie: `content/drafts/animations/symmetry-widening-apertures.mp4`
- Stills, contact sheets, and numerical/encoded reports share that prefix.
- Rebuild with `python scripts/generate_symmetry_widening_apertures.py --check --preview --render --encoded-check`.
- Intermediate propagation kernels live in the ignored `.tools/animation-review`
  directory. The cache key includes all geometric and numerical parameters.

## Visible sequence

One normally incident plane wave illuminates two openings. Its wavelength is
fixed at 0.2 in plot units. Both openings widen from 0.12 to 3.4, or from 0.6 to
17 wavelengths. Centers remain at y = ±2.7, leaving a final opaque divider ten
wavelengths wide. Equal screen scales represent x = −3 to 10 and y = −4.8 to 4.8.

The 20-second movie uses 1440 × 1120 pixels and 30 fps. After two seconds at the
narrowest width, five two-second transitions reach successive widths, with a
one-second hold after each intermediate transition. The broad final beams
receive four seconds. The wave clock advances continuously with period 1.2 s.
Gold guides appear near the end and are labeled “Ray approximation.” The actual
wave field remains visible, including all computed edge diffraction.

Colors show the real part of the wave: positive (255,42,91), negative (37,137,255),
zero (3,3,8). One fixed |Re U|^0.72 display curve is used for both incident and
transmitted fields at every width. Colors are not intensity; no frame-dependent
normalization or transmitted-side gain is applied.

## Calculation

The full finite width of each opening contributes. This is forward scalar
angular-spectrum propagation from an ideal thin transmission mask, with carrier
phase and evanescent decay included. The changing widths depict successive
monochromatic steady states, not the transient caused by physically moving an
edge. Reflection, polarization, and screen thickness are not modeled.

For each downstream distance, the propagator is H(q) = exp(i x sqrt(k²−q²)).
Its transverse antiderivative is computed spectrally, omitting q = 0. An opening
[a,b] then gives G(y−a)−G(y−b)+(b−a)H(0)/L. The two interval contributions are
summed before the common time phase and color map are applied. Aperture edges
move in this actual integral; endpoint images are not crossfaded.

The production periodic extent is 512 with 131072 samples (spacing 0.00390625).
Only the central strip needed for shifted evaluations is cached. Comparison
with direct analytic-rectangle Fourier propagation gave maximum complex error
0.000171 across sampled widths/distances. Constant plane-wave propagation is
preserved to floating-point accuracy. Independent padding checks with doubled
extent changed narrow-opening visible fields by at most 0.215% relative RMS.
At the final far edge, mean core intensity is about 1.18 versus 0.091 in the
central shadow interval used by the generator's validation.

The final H.264 movie decodes to all 600 frames at the intended dimensions and
frame rate. Six timestamp-matched comparisons gave maximum mean RGB error 5.72
on a 0–255 scale, mostly from the browser-compatible 4:2:0 color subsampling.
After matching that color conversion, maximum mean compression error was 2.45.
The decoded contact sheet and final frame were visually checked for wave
geometry, interference, color, and label clarity. The preview stills use a
fixed carrier phase for width comparisons; use the saved encoded-reference
frame for a phase-matched comparison with the decoded final sample.
