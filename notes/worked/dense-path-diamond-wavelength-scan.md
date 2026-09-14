# Dense path diamond and wavelength scan

This standalone iteration follows the decision to retain one screen and the
point-source A-to-B diamond, replace the arbitrary 49-path count with a fixed
dense family, and omit the detector-intensity pane. It preserves earlier
assets rather than replacing the canonical desktop animation.

## Model

A = (-4.5, 0), screen x = 0, and B = (4.5, 0). There are 20,001 uniformly
spaced midpoint samples across y in [-2.8, 2.8]. The odd count includes the
exact central crossing. The same positions and equal weights are retained
at wavelengths 0.5, 0.05, and 0.005.

For each position y, the total length is L(y) = 2 sqrt(4.5² + y²). Its
contribution is exp(i 2π[L(y)-9]/λ) / 20,001. The cumulative trace includes
every contribution, in top-to-bottom order, without grouping or fitting a
replacement curve. Each frame's diamond sweep and gold sum use the same
prefix index. A frame advances roughly 35 contributions; those sub-frame
contributions remain present in the drawn cumulative polyline.

These are equal-weight geometric path phasors. They are not the absolute
scalar propagation field of the former 49 finite-width slits. No transmitted
intensity, finite-width slit integral, or omitted propagator normalization is
implicitly inferred from their magnitudes. This is the point-path model
agreed during the discussion of choosing sufficiently fine spacing once for
the whole wavelength range.

## Display

The upper pane paints the envelope of the unresolved A-to-screen-to-B rays.
The blue region represents the paths already added. It is not intensity,
probability, or a signed wave field. The diamond's aspect ratio and dotted
screen glyph are schematic; the dots are not a literal count of the 20,001
positions. The moving blue boundary is an actual selected center path.

The lower pane uses a fixed 4,300 pixels per phasor unit. Each individual
contribution is about 0.215 pixels long, so the blue arrows resolve as a
continuous trace. The gold arrow always runs from the origin to the actual
prefix sum. No artificial endpoint knots or straight connecting segment are
inserted. The shortest-wavelength result is smaller on this fixed scale.

As in the earlier desktop presentation, the completed first sum sets phase
zero. This applies one constant rotation of -38.3259163282 degrees to every
contribution and every partial sum in the entire movie. The reference is
stated in the image. There is no independent rotation or normalization for
later wavelengths. Relative to the bare straight-path phase, the resultant
angles are approximately 38.326°, 43.145°, and 44.417°; the stationary-phase
offset has not been claimed to disappear.

Each wavelength gets exactly 12 seconds: 0.8 seconds before accumulation,
9.6 seconds for a uniform scan, and 1.6 seconds holding the completed sum.
Total duration is 36 seconds at 60 fps, 1440 × 1080. At shorter wavelengths,
the significant advance occurs during a narrower part of that same scan.

## Checks and files

Checks verify fixed positions and weights, central-path inclusion, symmetry,
the identical scan/prefix link, scalar sums evaluated independently, adaptive
integrals at six prefixes per wavelength, and plot containment. The largest
adjacent phase step is 21.299° at λ = 0.005. The maximum checked discrepancy
from the continuous integral is 1.56e-6 phasor units. The exact finite sum is
what is drawn; the continuous integral is an independent resolution check.

The encoded MP4 is decoded in full, with representative image and gold-tip
checks. Preview and encoded contact sheets accompany the output.

- Generator: `scripts/generate_symmetry_dense_path_diamond.py`
- Movie: `content/drafts/animations/symmetry-dense-path-diamond-wavelength-scan.mp4`
- Mathematical checks: `content/drafts/animations/symmetry-dense-path-diamond-wavelength-scan-validation.json`
- Encoded checks: `content/drafts/animations/symmetry-dense-path-diamond-wavelength-scan-encoded-validation.json`

```powershell
python -B scripts/generate_symmetry_dense_path_diamond.py --check --preview --render --encoded-check
```

The generator resolves the repository root and dependency folders relative
to its source file, preserving portability across machines.
