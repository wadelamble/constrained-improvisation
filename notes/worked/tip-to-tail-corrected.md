# Tip-to-tail with complete propagation phases and weights

Historical note: this describes the continuous-opening experiment used in
desktop versions 2 through 4. The current desktop movie restores 49 separate
physical slits; see [the slit correction](desktop-49-physical-slits.md).
The propagation kernel below remains shared, but the aperture bounds and
resulting amplitudes in this note are not the current slit-mask values.

Separate outputs preserve the earlier films:

- `content/drafts/animations/symmetry-tip-to-tail-corrected.mp4`: isolated spinning phasor diagram, 960 by 840.
- `content/drafts/animations/symmetry-many-slit-corrected.mp4`: matching three-pane diagram, 1280 by 720.

Both retain the 18.5-second, 24-fps sequence: build the chain at central B,
then sweep B while keeping the complex-plane axes, phase reference, and
amplitude scale fixed. Blue arrows are individual aperture contributions,
gold adds the current contribution, and green is the sum. The gray dashed
arrow is the amplitude with no screen at the current B. Its value at central
B defines phase zero and amplitude one for the entire movie.

This is a physical reference convention, not a claim that the isolated
stationary-path summand has zero phase. The corrected contributions are not
assigned phase kL alone. No frame-dependent rotation is used to straighten
the sum, and the sum is not forced to agree with the no-screen reference.

## Model

The previous 49-arrow diagram used exact Euclidean route lengths but
illustrative weights. This version keeps the A/screen/B distances and the
wavelength, using a complete **two-dimensional scalar** wave model. A is an
outgoing cylindrical source. It is not a three-dimensional spherical-wave
calculation and does not silently substitute a plane-wave or Gaussian input.

With time dependence exp(-i omega t), source distance z1=4.5, onward distance
z2=4.5, and wavelength 0.5, define

```math
G(z,y)=H_0^{(1)}\!\left(k\sqrt{z^2+y^2}\right),\qquad
P(z,y)=\frac{ikz}{2\sqrt{z^2+y^2}}
H_1^{(1)}\!\left(k\sqrt{z^2+y^2}\right).
```

P is the one-transverse-coordinate Rayleigh--Sommerfeld propagator. Its
Fourier multiplier is exp(i z sqrt(k^2-q^2)), with the outgoing/decaying
branch. Equivalently, P=-(i/2) partial_z G. Its phase, spreading, and angular
weight are all retained; no hand-applied 45-degree rotation is appended.
This is nonparaxial scalar propagation. The screen is still represented by
an ideal thin transmission mask, not by a full electromagnetic solution for
finite-thickness material and polarization.

The aperture [-2.8,2.8] is divided into 49 adjacent finite elements. Each
displayed arrow is

```math
a_j(B)=\frac{1}{G(9,0)}\int_{\text{element }j}
G(4.5,y)\,P(4.5,B-y)\,dy.
```

Each integral uses 12-point Gauss--Legendre quadrature. The element centers
are displayed in the path pane, ordered from top to bottom. This explicitly
represents a finely divided opening, not 49 zero-width physical holes.
The former model already described its 49 samples as a finely divided
aperture rather than a grating. A continuous aperture opening in the new
path pane makes that interpretation visible instead of drawing opaque bars
between the quadrature samples. A genuinely perforated mask with finite
opaque gaps would be a distinct physical setup.

The detector uses |sum_j a_j|^2 from exactly these terms. A single fixed
intensity scale accommodates both the full detector profile and intermediate
partial sums during construction. Arrows have their calculated magnitudes;
neither individual terms nor frame totals are normalized to equal length.

The no-screen reference is G(9,B)/G(9,0). At central B it is exactly 1.
The finite-aperture sum is about 5.058 degrees clockwise from it, with
intensity 1.09785 relative to the unobstructed central intensity. This
residual is retained. The old approximately 43-degree raw-sum tilt is not
merely rotated by a manually chosen number.

The underlying angular-spectrum propagation and its connection to the
Helmholtz equation are described in [TU Delft's wavefield propagation
notes](https://qiweb.tudelft.nl/aoi/wavefieldpropagation/wavefieldpropagation/).
The one-dimensional transverse Hankel kernel is also stated as equation
2.19 in this [UPC optics thesis](https://upcommons.upc.edu/server/api/core/bitstreams/e7e22c64-7e3e-45d3-a09d-551728bbc273/content).

## Validation and regeneration

The model checks:

- 12 versus 24 quadrature points per element and an independent adaptive
  integral over the complete finite aperture.
- The Hankel kernel against independent angular-spectrum integration,
  including the evanescent part.
- Repropagation of the unblocked cylindrical source from several imaginary
  planes against the direct source field. The spatial check truncates the
  infinite plane at |y|=2048 and retains its measured truncation error.
- Spectral composition over 1, 2, 7, and 63 steps, including a plane wave.
- Symmetry under B -> -B and the fixed central phase reference.

The renderer checks the complete chains against fixed plot bounds over
every animation frame. It checks encoded frame count, duration, and full
MP4 decoding. Representative generated and encoded frames are inspected.

Results are saved in
`content/drafts/animations/symmetry-tip-to-tail-corrected-validation.json`.

Sources:

- `scripts/corrected_tip_to_tail_model.py`
- `scripts/generate_symmetry_tip_to_tail_corrected.py`

Dependencies are NumPy, SciPy, Pillow, and imageio-ffmpeg. The existing
animation packages are reused; SciPy was installed in the separate ignored
directory `.tools/tip-to-tail-corrected-python-packages` on this machine.
The scripts detect these repository-local package directories when present.

```powershell
python -B scripts/generate_symmetry_tip_to_tail_corrected.py --check --preview --render
```

The later progressive many-screen animation has its own normalized paraxial
model. This correction does not modify that generator or any earlier media.
