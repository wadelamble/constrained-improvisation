# Fixed candidate paths and literal contribution arrows

[Movie](../../content/drafts/animations/symmetry-fixed-path-count-scan.mp4) ·
[Stills](../../content/drafts/animations/symmetry-fixed-path-count-scan-contact-sheet.png) ·
[Generator](../../scripts/generate_symmetry_fixed_path_count_scan.py)

Every pass uses **the same 121 midpoint paths**, in the same spatial order,
with the same quadrature weights. Each selected path contributes exactly
one blue vector to the polygon below. Its index is displayed in both
panels, its physical path is blue, and its newly added vector is thicker.
All previous vectors remain present. No analytic curve, tangent heads,
grouping, or per-pass drawing samples substitute for those vectors.

The three wavelengths are λ₀, λ₀/4, and λ₀/9, giving Fresnel numbers
F = 1, 4, and 9. This deliberately moderate range keeps a fixed, countable
set of arrows while resolving the shortest wavelength. It is a separate
version of the earlier continuous-curve movie.

Each pass has a one-second establishment, 121 additions at five frames
per path, and a one-second hold. The first and last midpoint additions
are exactly ten seconds apart. The complete MP4 is 36.25 seconds,
1440 × 960, at 60 fps. Selection advances in equal steps at the same
cadence in every pass; it does not depict propagation time.

## Model

The aperture has uniform incident plane-wave amplitude and phase. The
observer B is on axis. With s = y/a and F = a²/(λz), the fixed rule is

```text
N = 121
Δs = 2/N
s_j = -1 + (j - 1/2) Δs,       j = 1,...,N
v_j(F) = sqrt(F) exp(-iπ/4) exp(iπF s_j²) Δs
P_m(F) = sum(j=1,...,m) v_j(F).
```

The blue arrow j runs from P_(j−1) to P_j. The gold arrow runs from
zero to the actual P_m. The unobstructed plane wave exp(ikz) supplies
the phase reference. Its normalized one-dimensional Fresnel prefactor
is retained: individual vector lengths increase by factors 1, 2, and 3
as wavelength decreases. This is physical prefactor dependence; the
drawing scale stays at 640 pixels per complex-amplitude unit throughout.
No resultant is rotated, normalized, or forced to be horizontal.

Each midpoint stands for an equal-width aperture bin. Its vector is the
midpoint approximation to that bin's integral, not its exact integrated
contribution and not a finite amplitude assigned to a zero-width path.
The finite polygon approaches the continuous Fresnel integral as this
quadrature is refined.

The blue aperture band marks the phase scale |y| ≤ sqrt(λz). Its width
shrinks by a factor of three across the movie. It does not remove any
outer paths or enclose the whole final amplitude. The familiar completed
Cornu-like polygon need not straighten: the intended comparison is the
physical interval in which the scan builds the principal advance of the
sum. A stationary neighborhood supplies that advance; one exact path
does not supply a finite continuum amplitude by itself.

The upper geometry is schematic. Taking fixed z/a = 1000 makes the
maximum neglected quartic phase about 7.07 × 10⁻⁶ radians for F = 9.

## Validation

The analytic Fresnel integral is used only as an independent benchmark,
evaluated at every aperture-bin boundary. The actual displayed endpoints
are the sums of the 121 midpoint vectors.

| F | Finite final sum | Maximum absolute prefix error | Final relative error |
|---:|---:|---:|---:|
| 1 | 1.242965 + 0.185182i | 0.0001431 | 0.0114% |
| 4 | 0.882775 − 0.108464i | 0.0011502 | 0.1292% |
| 9 | 1.079084 + 0.076434i | 0.0039631 | 0.3674% |

At the shortest wavelength the largest adjacent unwrapped phase change
is 0.919 radians, below π/3. The longest-wavelength arrows are 10.58 pixels
long; the shortest-wavelength arrows are 31.74 pixels. Every vector has
one actual endpoint arrowhead. Coils can overlap geometrically, but no
vector is omitted or replaced.

Checks cover identical position/weight hashes in all passes, 121 vectors
per complete polygon, prefix-difference agreement with each vector,
constant magnitude within each pass, exact addition cadence, fixed
scale, and containment of every polygon vertex. The video is fully
decoded to check its frame count; representative encoded frames are
compared with source renders and checked for the active aperture marker.
Rendered stills and decoded contact sheets are inspected for collisions,
clipping, and correspondence between the selected path and added arrow.

[Model checks](../../content/drafts/animations/symmetry-fixed-path-count-scan-validation.json) ·
[Encoded-video checks](../../content/drafts/animations/symmetry-fixed-path-count-scan-encoded-validation.json) ·
[Decoded contact sheet](../../content/drafts/animations/symmetry-fixed-path-count-scan-encoded-contact-sheet.png)

```text
python -B scripts/generate_symmetry_fixed_path_count_scan.py --check --preview --render --encoded-check
```

Only the new generator, this note, and this version's media and validation
files are added. Earlier variants and manuscript material are preserved.
