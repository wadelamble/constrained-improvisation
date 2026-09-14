# Standalone plane-wave / screens animation

This is a separate wave-only companion to the progressive path animation. The
user confirmed the red/blue continuous field in the existing portrait reel's
top pane as the reference. The input is deliberately a plane wave, replacing
the earlier localized spherical source. Existing assets are preserved.

## Files and regeneration

- Model and shared timeline: `scripts/plane_wave_screens_model.py`.
- Wave renderer: `scripts/generate_symmetry_plane_wave_screens.py`.
- Media prefix: `content/drafts/animations/symmetry-plane-wave-screens`.
- Render with `python scripts/generate_symmetry_plane_wave_screens.py --preview --render`.
- Numerical checks: `python scripts/plane_wave_screens_model.py`.

The scripts use NumPy, Pillow, and imageio-ffmpeg from the existing animation
requirements. They also recognize the optional repository-local
`.tools/animation-python-packages` directory. Paths are portable.

## Sequence and visual contract

The 52-second, 24 fps, 1280 × 720 sequence starts with five seconds of an
unobstructed plane wave. It introduces one screen with one slit, then three,
seven, and fifteen slits. The remaining barrier opens away. It then introduces
three, seven, and fifteen increasingly open screens, before their transmission
reaches one everywhere. Only then do faint imaginary-slice marks appear.

The shared model exports `TRANSITIONS`, `state_at(t)`, `masks_at(t)`, `FPS`,
`DURATION`, `temporal_phase(t)`, source/endpoint coordinates, and screen positions.
Companion path renderers must consume these rather than copying a separate
schedule or independently choosing propagation phases.

The field view covers x = 0 to 14.4 and y = −3.6 to 3.6, with equal physical
axis scale. The pixel rectangle is (40, 80, 1240, 680). Red is positive real
amplitude, blue negative, and near-black zero. Exact reel colors are RGB
(255, 42, 91), (37, 137, 255), and (3, 3, 8); display strength is the fixed
function |Re ψ|^0.72 after clipping to [−1, 1]. This is one mapping for every
stage. No output field is independently brightened or phase-rotated.

Small ticks outside the field identify physical screen positions even as the
opaque remnants become too narrow to see clearly. These ticks do not thicken
the masks used in the calculation. Final slice markers are bookkeeping marks.

## Physical model and the limit

At x = 0 the complex field is identically one over the complete transverse
computational domain. The wavelength is 0.72. With time convention exp(−iωt),
each transverse Fourier mode q propagates through distance d by

    H_d(q) = exp(i d sqrt(k² − q²)),   k = 2π / wavelength.

The square-root branch has nonnegative imaginary part, so modes |q| > k decay.
FFT and inverse FFT supply the consistent continuum-discretization factors;
the carrier phase is retained. This is exact forward scalar angular-spectrum
propagation on the finite periodic grid, rather than a paraxial approximation.
Thin real transmission masks multiply the complex field at each screen. The
model does not calculate reflected waves, polarization, or scattering inside
material of finite thickness.

The first four slit masks have opening width 0.24. The many-screen targets use
3 screens with pitch 0.45 and open fraction 0.86; 7 screens with pitch 0.225 and
open fraction 0.97; and 15 screens with pitch 0.1125 and open fraction 0.995.
Masks use exact aperture overlap averaged over each grid cell. The grating
phase is centered on y = 0 and does not depend on the padding domain.

Transitions interpolate transmission masks continuously, so the material can
pass through partial transparency. Every displayed field is recalculated from
its actual current masks. These are successive monochromatic steady states,
not a causal simulation of the transient when a barrier is suddenly inserted.
Motion within each state uses one uninterrupted exp(−2πit/3) clock.

For rendering efficiency the field during a transition is evaluated as its
exact polynomial in the interpolated mask amount. With N changing screens,
each mask is affine in that amount, so the propagated field has degree at most
N. Barycentric interpolation at N + 1 Chebyshev nodes evaluates that polynomial;
this is not a two-image crossfade. Fresh full-field solves at nine interior
transition amounts agree to a maximum complex error of 2.02 × 10⁻¹⁵.

Increasing the number of perforated barriers alone does not recover free
propagation. Here their transmission explicitly tends to identity. The final
field is exp(ikx), with the same amplitude and phase as the initial plane wave,
and inserting further identity masks leaves it unchanged. Finite stages retain
real attenuation; for example the three-screen output amplitude is about 0.64.

## Numerical and visual validation

The production grid has 16,384 transverse cells across a period of 512,
spacing 0.03125. The much smaller visible interval is centered in that domain.
Propagation is evaluated in longitudinal sections to avoid allocating full
screen-to-screen dense transfer matrices.

An initial period of 64 was rejected after doubling it changed the one-slit
output substantially. At the selected period of 512, comparison to period
1024 at unchanged spacing gives these errors in the complex output field
at x = 14.4, |y| ≤ 3.6:

| Stage | Maximum absolute error | Relative L2 error |
|---|---:|---:|
| 1 slit | 0.00050345 | 0.4383% |
| 7 slits | 0.00050487 | 0.1066% |
| 15 slits | 0.00050268 | 0.0721% |
| 3 screens | 0.00017577 | 0.0193% |
| 7 screens | 0.00001615 | 0.00142% |
| 15 screens | 0.000000175 | 0.0000134% |

Doubling the mesh at fixed period gives at most 0.001429 absolute and 0.1254%
relative L2 error across these targets. The one-slit mesh errors are 0.00003343
absolute and 0.0202% relative L2.

The built-in checks verify full complex plane-wave recovery, the q = 0 phase,
the propagation composition law, valid transmission bounds, and identical
initial/final masks. They do not require norm conservation for arbitrary fields:
evanescent decay and real absorptive masks intentionally reduce it.

Previews include one frame per important state, a contact sheet, and baseline
and recovered PNGs at exactly the same clock phase. The latter permit a direct
visual comparison without confusing elapsed carrier phase with an added offset.
Their wave rectangles are pixel-identical. The complete-recovery caption starts
only at 46 seconds, after all physical masks reach identity.

The finished MP4 decodes completely without errors: H.264 High, yuv420p,
1280 × 720, 24 fps, 1,248 frames, and exactly 52.0 seconds. All 104 encoded
frames sampled at 2 fps were inspected in contact grids, together with full-size
encoded one-slit, opening, and recovered-wave frames. No clipped labels,
unexplained discontinuities, or visible encoding defects were found.
