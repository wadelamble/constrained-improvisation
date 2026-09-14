# Normalized dense path diamond

This version implements the request to apply physical propagation weights to
every contribution and every partial sum. It keeps the previous dense film's
point-source geometry, the same 20,001 midpoint crossing positions, the two
panes, and the three wavelengths 0.5, 0.05, and 0.005. The original raw film
and generator remain available for comparison.

## Normalization and scope

Reuse the complete one-transverse-coordinate scalar propagation model from
`scripts/corrected_tip_to_tail_model.py`, with wavelength parameterized:

\[
G(z,y)=H_0^{(1)}(k\sqrt{z^2+y^2}),\qquad
K(z,y)=\frac{ikz}{2\sqrt{z^2+y^2}}H_1^{(1)}(k\sqrt{z^2+y^2}),
\]

\[
v_j=\Delta y\,\frac{G(4.5,y_j)K(4.5,-y_j)}{G(9,0)}.
\]

Here k = 2π/λ, Δy = 5.6/20,001, and y_j are the same top-to-bottom
midpoint samples in [-2.8,2.8] as the raw version. The time convention is
exp(-iωt). The point source is cylindrical in this two-dimensional scalar
model. Polarization, material-screen response, and multiple scattering are
outside the approximation.

The denominator is independently known unobstructed propagation from A to B.
It is not the computed finite-screen sum. The propagation rule is normalized
before restricting the transverse span: K(z₂) convolved with G(z₁) equals
G(z₁+z₂). The angular-spectrum factors multiply to give this identity,
including evanescent components. A direct numerical reconstruction over a
wide transparent plane checks it independently.

This restores both wavelength-dependent and position-dependent weights. The
previous equal-length arrows were an approximation; complete source and
propagator weights vary over this relatively broad geometry. At λ=.005,
individual contribution magnitudes range from about .001903 to .002640.
All 20,001 terms are still added explicitly. No rescaling of the completed
resultant is used.

The full kernel retains the actual geometric distances. A pure Fresnel
version would additionally replace the geometric path-length phase by its
quadratic approximation, which is not uniformly accurate across this full
diamond. This version avoids that additional approximation.

The dense sampling represents a finite permitted transverse span. The dotted
screen is a schematic glyph, not 20,001 separately resolved finite holes with
an invented width or opaque fill fraction. No finite-width hole mask from the
older 49-slit experiment is silently inferred. The blue paint represents
added candidate routes; it is not a wave field, intensity, or probability.

## Display and results

The lower pane uses one fixed scale, 620 pixels per unit of free-field
amplitude, and one fixed origin. Unobstructed A-to-B propagation is always
the complex reference 1. There is no additional presentation rotation to
make the first or any later finite-screen sum horizontal. All phase and
amplitude factors are included in each blue term before summation.

| Wavelength | Completed sum | Magnitude |
|---|---|---|
| 0.5 | 1.043704936 − 0.092377071i | 1.047785053 |
| 0.05 | 0.977039241 − 0.022825500i | 0.977305828 |
| 0.005 | 0.992716825 − 0.007278913i | 0.992743511 |

The finite-span result approaches the free-field reference in the resolved
short-wavelength regime, without being forced to equal 1. This comparison
does not assert probability-one arrival at B. The distinction between routes
connecting fixed endpoints and the distribution across possible endpoints
remains essential for the later quantum-mechanical narrative.

The original uniform timing is retained: each pass has 0.8 seconds before
accumulation, a 9.6-second top-to-bottom scan, and a 1.6-second final hold.
The movie is 36 seconds at 60 fps and 1440 × 1080. Every displayed prefix
uses the same index in the diamond and the tip-to-tail pane.

## Validation and regeneration

Checks cover the unchanged path set, symmetry, vector-to-prefix identity,
kernel agreement with independent angular-spectrum integration, transparent
plane reconstruction, threefold sampling refinement over every prefix, and
six adaptive prefix integrals per wavelength. The maximum adaptive error is
5.92e-5 of the free-field amplitude. The largest neighboring phase increment
is 21.299°. The wide-plane reconstruction errors are at most 2.32e-5, with
the remaining discrepancy attributable to the |y| ≤ 256 truncation.

The encoded video is decoded completely. Representative frames are compared
with the source rendering, and the gold tip is checked against its actual
mathematical prefix. Source and encoded contact sheets support visual review.

- Generator: `scripts/generate_symmetry_normalized_path_diamond.py`
- Shared drawing: `scripts/generate_symmetry_dense_path_diamond.py`
- Movie: `content/drafts/animations/symmetry-normalized-path-diamond-wavelength-scan.mp4`
- Validation files: the same movie stem with `-validation.json` and
  `-encoded-validation.json` suffixes.

```powershell
python -B scripts/generate_symmetry_normalized_path_diamond.py --check --preview --render --encoded-check
```

The normalized generator configures the shared renderer only within its own
process and writes to its own output stem. All paths resolve from the repo.
