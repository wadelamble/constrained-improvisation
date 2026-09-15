# Narrow openings and the short-wavelength limit

Standalone trial of the user's chosen option 1: fix two narrow apertures,
shorten the wavelength, and change from signed wave crests to intensity before
the spatial carrier becomes too fine to draw. The widening-apertures movie is
preserved for comparison. No manuscript links are changed by this generator.

- Generator: `scripts/generate_symmetry_short_wave_beams.py`
- Movie: `content/drafts/animations/symmetry-short-wave-beams.mp4`
- Stills, contact sheets, and validation reports share that prefix.
- Rebuild with `python scripts/generate_symmetry_short_wave_beams.py --check --preview --render --encoded-check`.
- The generator imports fonts, the signed-wave palette, and coordinate helpers
  from `scripts/generate_symmetry_widening_apertures.py`.

## Visible sequence

The camera, unit incident plane-wave amplitude, aperture width 0.5, and aperture
centers y = ±2.4 remain fixed. The wavelength decreases through 0.5, 0.2, 0.08,
0.015, and 0.001. The opening therefore changes from one to 500 wavelengths wide
without moving its edges. Plot scales are equal, 100 pixels per unit.

The 20-second, 1440 × 1120, 30 fps movie holds the first state for two seconds,
uses four three-second transitions, and holds each intermediate state for one
second and the final state for three. The fixed playback phase clock has a
1.2-second period. This clock is chosen for legibility, not as a physical
dispersion relation or model of changing the illumination frequency in time.

The original vivid red/blue colors show Re U. As wavelength decreases from
0.30 to 0.18, the picture explicitly changes to
|U|², labeled intensity averaged over a wave cycle. This is a change of
observable. Averaging the red/blue colors would not give intensity. A fixed
black/plum/red/gold/pale-yellow intensity map applies to both sides of the
barrier throughout; there is no beam-dependent or frame-dependent gain.
Computed diffraction remains visible in the final beam edges.

The display change begins before spatial crests become unresolvable: reducing
the wavelength also moves crests between movie frames. To avoid apparent
backward motion from temporal aliasing, global phase is referenced to x = 3.5
and the visible carrier is faded before its maximum step exceeds half a cycle.
The measured maximum while any signed field remains is 2.54 radians per frame,
below π. This phase reference does not change the computed intensity.

## Calculation and validation

Each frame is a separate monochromatic steady state in a scalar forward
angular-spectrum model. Reflection, polarization, screen thickness, and
frequency-change transients are not modeled. Exact finite-interval Fourier
coefficients describe the two openings. The angular spectrum includes
evanescent decay. Factoring out exp(ikx) allows the envelope to be calculated
when the wavelength itself is far smaller than a display pixel. The carrier
is restored at full display resolution whenever Re U is shown.

The production transverse period is 128 with 16384 samples. There are 301 axial
samples; interpolation of the complex envelope was checked against propagation
at the precise display coordinates (maximum sampled error 0.00481). The final
display integrates about 95.9% of visible |U|² within the two geometrical
aperture-width strips. An independent, much finer calculation gives about
95.4%; remaining differences concern fine Fresnel fringes, not beam position
or width. There is no enforced ray mask in the calculation or renderer.

The finished H.264 movie was decoded through all 600 frames. Dimensions, frame
rate, and duration match the specification. Six source/decoded frame comparisons
gave mean RGB errors between 1.12 and 2.11 on a 0–255 scale; the decoded contact
sheet was inspected for geometry, palette, and readable labels.

## User's fallback

If this trial is not preferred, use the existing widening-apertures version
with incoming ray arrows and one outgoing arrow down the center of each beam
once propagation is sufficiently ray-like. That fallback has not been applied
while the separate trial is being evaluated.
