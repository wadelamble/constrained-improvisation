# Two tip-to-tail limits

Standalone comparison, preserving all previous animations:

- [MP4](../../content/drafts/animations/symmetry-two-tip-to-tail-limits.mp4)
- [Final frame](../../content/drafts/animations/symmetry-two-tip-to-tail-limits-final.png)
- [Contact sheet](../../content/drafts/animations/symmetry-two-tip-to-tail-limits-contact-sheet.png)
- [Generator](../../scripts/generate_symmetry_two_tip_to_tail_limits.py)

Two panes begin with the same complete chain and change continuously. The
left increases propagation distance at fixed wavelength; the right shortens
wavelength at fixed distance. Both use the same finite, uniformly illuminated
opening, an on-axis observation point, and a plane-wave input. Blue shows
aperture contributions; gold is their actual complex sum in every frame.

The 26-second film holds the starting state for 1.5 seconds, changes the
parameters for 22 seconds, and holds the final states for 2.5 seconds. A short
velocity ramp softens only the beginning and end of the parameter sweep.
The left distance grows exponentially, distributing the visible unwinding
through the movie. The right phase spread grows linearly, keeping its outer
arrows turning at an approximately steady rate.

## Calculation and reference

Write the aperture as [-a,a] and F=a²/(λz). The one-transverse-coordinate
normalized Fresnel propagator is

```math
K_z(y)=\frac{e^{ikz-i\pi/4}}{\sqrt{\lambda z}}
       \exp\!\left(\frac{i\pi y^2}{\lambda z}\right).
```

The display divides the entire field by the unobstructed wave exp(ikz) at
the observation point. That declared reference removes the common travel
phase as z or λ changes; it retains the -π/4 kernel phase and all physical
amplitude factors. No rotation aligns the resultant with an axis. No
per-frame amplitude fitting or equal-length normalization is used. Both
panes have the same fixed 355 pixels per incident-field amplitude unit.

Each arrow is the integral of K over one aperture element, evaluated with
the analytic Fresnel functions. The underlying partition has 256 elements.
When individual arrows would be shorter than 3 pixels, exact groups of
eight adjacent elements provide visible arrows; a fine cumulative trace
still shows the full within-group curvature. On the right, all 256 arrows
remain individually drawn throughout. All groupings give the same endpoint.

Both panes start at F=2. The left ends at F=.05 (z/z₀=40); the right ends at
F=24 (λ/λ₀=1/12). These are finite approaches to the limits, not literal
infinity or zero. One possible physical realization is a=1 unit, z₀=100
units, λ₀=.005 unit, keeping the geometry paraxial throughout.

The left chain straightens because a fixed finite aperture increasingly
contributes in phase; its magnitude also decreases with distance and that
decrease is retained. This is not the claim that the complete infinite-plane
Cornu curve straightens. The right retains curling tails, while the stationary
region gives the net displacement. The gold chord is the resultant, not a
replacement for the curved chain or a literal individual path contribution.

The Fresnel propagation phase and normalization follow the
[Huygens–Fresnel derivation](https://farside.ph.utexas.edu/teaching/315/Waves/node99.html).

## Validation

The generator compares every element against independent 24-point
Gauss–Legendre quadrature at 250 parameter values. It also checks common
initial conditions and a dense sampling of each curve against the fixed
plot bounds. Results are in
[validation JSON](../../content/drafts/animations/symmetry-two-tip-to-tail-limits-validation.json).
Representative frames and the encoded MP4 are inspected before delivery.

Regenerate using the configured Python runtime with NumPy, SciPy, Pillow,
and imageio-ffmpeg available:

```text
python -B scripts/generate_symmetry_two_tip_to_tail_limits.py --check --preview --render
```
