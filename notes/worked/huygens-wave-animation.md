# Huygens as a coherent wave construction

This standalone animation replaces the screen-count progression as the current
Huygens exploration. All previous media and source files are preserved. The
user asked for a beautiful Huygens animation in the confirmed red/blue wave
style from the portrait reel, with artistic judgment delegated to the animator.

**Durable design correction:** the user rejected the previous progression of
denser slits across increasing numbers of screens because it became visually
redundant: one sufficiently open, densely sampled screen had already recovered
the plane wave. Adding further screens contributed no useful visual development.
The new direction is the coherent Huygens construction itself, with discernible
secondary contributions and a reconstructed advancing wavefront, rather than
another screen-count limit. Earlier generators and media remain preserved.

## Files

- Shared model: `scripts/huygens_construction_model.py`.
- Wave renderer: `scripts/generate_symmetry_huygens_wave.py`.
- Wave media prefix: `content/drafts/animations/symmetry-huygens-wave`.
- Rebuild: `python scripts/generate_symmetry_huygens_wave.py --preview --render`.
- Model checks: `python scripts/huygens_construction_model.py`.

The model is separate from both the wave renderer and its path companion. It
exports the partition, source geometry, coefficients, labels, clock, frame rate,
duration, and final moving-crest cue. Companion views consume the same complex
contributions. The earlier many-screen files are not dependencies.

## What the construction shows

The incoming field is one unit plane wave. A mathematical plane at x = 3.2
divides its description into localized contributions. Small gold marks identify
elements of that plane; they do not represent holes, material, or physical
emitters being switched on. All elements retain the same incident phase.

The movie first shows the complete wave, then selects one secondary
contribution. It includes two other separated elements so that their curved
fronts and coherent interference are discernible, then fills the intervening
elements and the remaining wavefront. The complex sum recovers the original
plane wave. Finally, two small marks outside the image follow one actual red
crest as it advances.

The reveal is a decomposition of one unchanged free field. During selection,
the right side shows a partial sum of that field's contributions, not the total
physical field after blocking the unselected contributions. The full incoming
field stays visible to the left, all element marks remain present, and the
footer identifies the partial-sum view. There is no barrier or slit sequence.

## Exact meaning of a secondary contribution

Write the incident plane wave as exp(ikx), with time convention exp(−iωt).
At the construction plane, smooth nonnegative functions w_j(y) partition the
field into localized elements. Visible elements have centers j × 0.64 for
j = −5,...,5 and Gaussian width 0.20. Each Gaussian is divided by the sum of
the complete periodic Gaussian lattice. These are weighted finite elements,
not literal point sources with independently chosen unit amplitudes.

The visible eleven elements are supplemented by one grouped remainder:

    w_remaining(y) = 1 − sum_visible w_j(y).

All twelve weights are nonnegative and sum to one across the entire numerical
plane. The remainder includes the other lattice elements, whose tails can reach
into the visible interval; it is therefore called the remaining wavefront rather
than a contribution supported strictly outside the picture.

For x ≥ x_c = 3.2, the complex contribution of element j is

    U_j(x,y) = P_(x−x_c)[exp(ik x_c) w_j](y).

The propagation operator multiplies transverse Fourier mode q by

    H_d(q) = exp(i d sqrt(k² − q²)),   k = 2π / 0.9.

The root has nonnegative imaginary part, so evanescent modes decay. FFT and
inverse FFT supply the consistent normalization; the longitudinal carrier phase
is included. This is forward scalar angular-spectrum propagation on a periodic
transverse domain, with one transverse coordinate. It is not a model of
reflections, polarization, material screens, or finite-thickness scattering.
It also does not replace the normalized contributions with equal-amplitude
spherical waves or apply a small-wavelength stationary-phase approximation.

Linearity gives the complete reconstruction exactly:

    sum_j U_j(x,y) = exp(ikx).

The renderer calculates the selected complex sum first, multiplies by the common
clock exp(−2πit/3), then applies the fixed signed-amplitude color map once.
It never adds separately color-mapped fields or intensities. There is no
per-element or per-frame renormalization and no separate phase at reveal time.

## Timing and visual contract

The movie is 40 seconds, 24 fps, 1280 × 720. Its field rectangle is
(40, 80, 1240, 680), covering x = 0 to 14.4 and y = −3.6 to 3.6 with equal
physical axis scale. It uses the reel's colors: positive RGB (255,42,91),
negative (37,137,255), and zero (3,3,8). Display strength is the fixed function
|Re U|^0.72 after clipping to [−1,1]. The dark nodes remain visible.

| Time | Construction |
|---|---|
| 0–4 s | Complete plane wave |
| 4–6 s | Identify one mathematical wavefront plane |
| 6–8 s | Select its central localized contribution |
| 8–11 s | Hold the single curved wavelet |
| 11–13 s | Add elements j = ±3 coherently |
| 13–16 s | Hold their interference |
| 16–23 s | Include the remaining visible elements |
| 23–28 s | Include the grouped remaining wavefront |
| 28–32 s | Hold the complete reconstruction; element marks recede |
| 32–40 s | Follow one advancing positive crest |

The final tracked crest satisfies kx−ωt = −12π. Its position is
x(t) = 0.9(t/3 − 6), advancing at 0.3 plot units per second. The marker is a
visual annotation outside the field and does not modify its amplitude.

## Numerical validation

The production transverse grid has 16,384 points across a period of 512,
spacing 0.03125. The complete periodic lattice has 800 elements. The renderer
precomputes the twelve grouped fields in small longitudinal chunks rather than
allocating a dense global transfer matrix.

Independent checks found:

- Complete reconstruction over the full transverse plane: maximum complex
  error 5.63 × 10⁻¹⁶.
- Off-grid endpoint positions and clock phases: maximum error 3.49 × 10⁻¹⁵.
- Explicit Fourier-mode matrix on a separate 512-point check grid versus the
  grouped endpoint calculation: 1.48 × 10⁻¹⁵.
- Partial reveals evaluated directly from their weighted initial fields versus
  the sum of separately propagated groups: at most 3.47 × 10⁻¹⁶.
- Doubled mesh: component sums change by approximately 10⁻¹⁶.
- Doubled padded period, 512 to 1024: individual endpoint contributions change
  by at most 0.000303, and sampled partial sums by at most 0.000710, on the unit
  incident-amplitude scale.

The remaining-wavefront contribution at the central endpoint has magnitude
about 0.264. It is substantial and is explicitly included and acknowledged
during 23–28 seconds. A finite visible patch alone is not substituted for the
complete plane.

The single-wavelet, three-wavelet interference, and reconstruction previews were
inspected at full size before final encoding. Baseline and reconstructed PNGs
are supplied at the same clock phase for direct comparison.

The finished MP4 is H.264 High, yuv420p, 1280 × 720, 24 fps: 960 frames and
exactly 40.0 seconds. It decodes completely without errors. All 80 encoded
frames sampled at 2 fps were inspected, plus full-size encoded reconstruction
and advancing-crest frames. Labels fit, the remaining-wavefront caption appears
at the correct stage, and the final brackets follow a positive crest without
modifying the field. No visible encoding defects or unintended discontinuities
were found. The same-phase baseline and reconstructed wave rectangles are
pixel-identical.
