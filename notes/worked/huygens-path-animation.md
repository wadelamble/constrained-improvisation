# Huygens construction: paths and amplitudes

[Play the path companion](../../content/drafts/animations/symmetry-huygens-paths.mp4)

This standalone animation accompanies the Huygens wave-field animation.
Both use `scripts/huygens_construction_model.py`, including the same source,
smooth wavefront elements, remaining-wavefront term, absolute complex
propagator, selection coefficients, clock, geometry and 40-second timeline.
Earlier screen/slit animations remain separate and unchanged.

The construction selects parts of one existing plane wave. There is no
barrier, no slit opening, and no change to the underlying complete wave.
The partial pictures show selected terms in a mathematical decomposition.

## What the paths represent

The imaginary construction plane is x = 3.2. The fixed observation point is
B = (14.4, 0). Eleven visible elements are centered from y = −3.2 to +3.2 in
steps of 0.64. The shared model forms nonnegative normalized Gaussian
weights, with sigma 0.20, and includes the entire remaining wavefront.
The twelve weights sum to one throughout the numerical transverse domain.
The Gaussian elements overlap; they are weighted groups, not exclusive slits.

Each line connects an element's center to B. The small surrounding fan and
the profile on the construction plane identify its finite transverse extent.
The corresponding arrow is the exact integrated contribution

```math
C_j(B)=\sum_a K(B,a)\,w_j(a)\,U(a).
```

Here K is the normalized finite-grid propagation matrix. Its inverse Fourier
transform already includes the quadrature normalization. The arrow's angle
is not calculated from the center-line length, and the few drawn lines are
not the samples used to estimate the sum. The full model integrates every
sample of each weighted element, including its tails.

The path view follows the wave view's selection: the central element,
the pair at y = ±1.92, the other neighboring pairs, then the remaining
wavefront. Each route and its arrow receive the same selection coefficient.
The purple arrow explicitly includes the remaining-wavefront contribution.
Its magnitude at B is approximately 0.264, so omitting it would materially
change the result. It is calculated from the remaining weight function,
not substituted for an unexplained final jump to an analytic plane wave.

## Phase convention

The small phasor diagram is labelled **Phase relative to the plane wave at B**.
Every complex contribution is divided by the same unit complex reference

```math
R_B(t)=\exp(ikx_B)\exp(-i\omega t).
```

This is a phase-only change of coordinates. It removes the common clock
rotation and leaves the complete plane field horizontal with unit magnitude.
It does not rotate individual groups independently, change their relative
phases, or normalize a partial sum to unit length. The faint green reference
arrow stays fixed; the bright green resultant changes as groups are selected.

The color sample at B uses the absolute selected amplitude, including the
same time phase as the wave film. Initial and final wave bands also use
that absolute phase. The ending brackets follow the identical positive
crest as the wave companion.

## Validation and regeneration

Across 81 times covering holds and transitions, the selected path sum agrees
with the shared wave amplitude at B to 4.58 × 10⁻¹⁶. Transforming the displayed
phasors back from their labelled reference agrees to the same tolerance.
An independent real-space convolution of every weighted group agrees with
the spectral endpoint calculation to 3.68 × 10⁻¹⁵. The full sum agrees with
the absolute complex plane field to 2.25 × 10⁻¹⁷.

Both films are 1280 × 720, 24 frames per second, and 40 seconds (960 frames).
They share plot rectangle `(40, 80, 1240, 680)`, x = 0 to 14.4, and
y = −3.6 to +3.6. The numerical field uses a wider periodic transverse
domain; the shared wave-model notes describe that approximation.

```powershell
python scripts/generate_symmetry_huygens_paths.py --check --preview --render --qa
```

The generator uses the existing optional repository-local animation
dependencies. It writes only the new `symmetry-huygens-paths` media family.
The QA option decodes the finished MP4 and saves two actual encoded frames
per second in contact grids under the ignored `.tools/huygens-paths-qa` folder.
