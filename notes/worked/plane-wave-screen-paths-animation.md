# Plane-wave screens: companion path view

[Play the path view](../../content/drafts/animations/symmetry-plane-wave-screen-paths.mp4)

This standalone file accompanies the
[wave-field view](plane-wave-screens-animation.md). Both import
`scripts/plane_wave_screens_model.py`: the same uniform incident field,
wavelength, screen masks, exact angular-spectrum propagation, stage timeline,
and temporal phase. Both are 1280 × 720, 24 frames per second, and 52 seconds
(1,248 frames). Their physical plot rectangle is `(40, 80, 1240, 680)`.

The input is a unit plane wave on the whole transverse numerical domain at
x = 0. The fixed endpoint is B = (14.4, 0). The viewport shows y = −3.6 to
+3.6; the numerical domain is much wider. The input is not a point source.

## What is drawn

The blue lines show representative candidate paths to B. The gold line
identifies the central candidate. A finite selection can show how crossing
sequences pass through openings, but does not enumerate the path expansion.
The line colors and their brightness are not complex path amplitudes.
Blocked paths disappear because the screen transmission is zero, not because
interference is being represented by fading.

Each stage has a deterministic bank of routes on the shared transverse grid.
The renderer crossfades these representative banks during the shared mask
transition and applies the actual masks to all their screen crossings. There
is no random resampling from frame to frame. The routes illustrate a choice
of crossing sequence, not a particle trajectory. In particular, a plane wave
still has nonparallel candidate paths to a chosen endpoint.

The green arrow gives the full complex field at B, with a fixed unit circle
and the shared factor exp(−iωt). It uses neither per-stage normalization nor
an extra phase rotation. The right-edge strip gives the entire output field
in the wave animation's red/blue instantaneous-amplitude palette. The left
edge shows the incident field's common phase. These exact field displays
include all numerical source and screen points, including points beyond the
visible path window.

As in the wave animation, the changing masks depict successive monochromatic
steady states. This is not a simulation of the transient caused by physically
inserting a screen. Thin transmission screens omit reflected waves. The
final masks are identity: only then do the faint imaginary-slice marks appear.

## Exact path-sum connection

For each propagation distance d, the finite-grid transfer matrix is

```math
U(d) = F^{-1}\operatorname{diag}
\left(e^{i d\sqrt{k^2-q^2}}\right)F.
```

The square root has nonnegative imaginary part, giving evanescent decay.
The inverse Fourier transform includes normalization. Each mask multiplies
the field before the next propagation. This is the same kernel as the wave
view, including its complex phase.

The renderer computes the displayed resultant independently as a grouped
path sum at the last screen. If f is the incident field after that screen,
then each last-crossing contribution is U(B, j) f(j), and their sum is the
amplitude at B. The field f already sums every preceding source and screen
choice. The route sample drawn in blue is not used to estimate this sum.

The normalized matrix-element product was also checked by explicitly
enumerating all 2,401 terms on a seven-point input plane with three
intermediate screens. That expansion and sequential propagation agree to
9.51 × 10⁻¹⁶. Across representative holds and mask transitions, the grouped
sum agrees with the shared wave field at B to 2.38 × 10⁻¹⁶. The initial and
fully opened final states agree with exp(ikX) to 1.38 × 10⁻¹⁵ before applying
the shared clock. The wave-view note records spatial-convergence checks.

## Regeneration

```powershell
python scripts/generate_symmetry_plane_wave_screen_paths.py --check --preview --render --qa
```

The script uses the same optional repository-local animation dependencies
as the wave renderer. It writes only the new
`symmetry-plane-wave-screen-paths` media family and leaves older animations
intact. The master is the MP4; the contact sheet and inspection PNGs support
review before folding this view into a larger panel layout.
The QA option decodes the finished MP4 and saves two encoded frames per
second in review grids under the ignored `.tools/plane-wave-paths-qa` folder.
