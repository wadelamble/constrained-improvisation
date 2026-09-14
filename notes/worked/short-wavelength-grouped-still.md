# Very short wavelength: grouped tip-to-tail still

[Still diagram](../../content/drafts/animations/symmetry-short-wavelength-grouped-limit.png)

[Generator](../../scripts/generate_symmetry_short_wavelength_grouped_still.py)

The user requested a still to agree on the short-wavelength endpoint before
any new animation. The many-slit pane is abandoned for this request. This
asset preserves all earlier files and does not modify the manuscript.

The uniformly illuminated aperture [-a,a] is partitioned into 21 **fixed**
equal regions. The middle region includes y=0, the stationary path to the
on-axis observation point. The diagram shows the integrated complex
amplitude of each region as an arrow, in spatial order. It does not plot the
complete microscopic Cornu curve and then deform that curve to a line.
The central grouping is not identified with the first Fresnel zone or with
one isolated candidate path.

The dimensionless Fresnel number is F=a²/(λz)=10⁸. Group coefficients are
analytic integrals of the normalized one-transverse-coordinate Fresnel
kernel, using the unobstructed plane wave exp(ikz) as the phase reference.
The -π/4 kernel phase and magnitude prefactor are retained. The generator
reuses the cumulative integral from the two-pane source.

For this finite example:

- Central group: 0.9997546802 + 0.0006218075 i.
- Other 20 groups combined: 0.0002228119 − 0.0006443154 i.
- Complete sum: 0.9999774921 − 0.0000225079 i.
- Magnitude of the combined outer contribution / magnitude of total:
  0.0006817686, or 0.06817686%. This is an amplitude ratio, not a probability.

All arrows have their true computed direction and magnitude at 910 pixels
per incident-field amplitude unit. Each outer group is less than one pixel
long. The gold resultant is translated down for comparison, retaining the
same scale and angle. Neither the central arrow nor the gold total is forced
horizontal. Thin leader lines identify the outer endpoint clusters.

At fixed grouping, every noncentral interval's integrated contribution
tends to zero as λ tends to zero; the central interval's contribution tends
to one. This uses cancellation within each fixed interval. Finite-λ
corrections oscillate and need not decrease monotonically at every step.

The calculation is the paraxial scalar model. Short wavelength alone does
not ensure that approximation is accurate for exact free propagation.
For example, fixed z/a=10⁶ keeps the maximum neglected quartic phase term
below 8×10⁻⁵ radians at the plotted F.

The propagation and scaling follow the
[Huygens–Fresnel derivation](https://farside.ph.utexas.edu/teaching/315/Waves/node99.html).

Validation compares every group against a separate three-term endpoint
expansion from integration by parts: maximum absolute discrepancy
1.24×10⁻¹². It also verifies the group sums, central-plus-outer decomposition,
and residual size. The rendered PNG was visually inspected for clipping,
text collisions, and consistent arrow scales.

[Validation data](../../content/drafts/animations/symmetry-short-wavelength-grouped-limit-validation.json)

```text
python -B scripts/generate_symmetry_short_wavelength_grouped_still.py
```
