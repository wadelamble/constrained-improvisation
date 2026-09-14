# Short wavelength: link the paths to the running sum

[Animation](../../content/drafts/animations/symmetry-short-wavelength-path-scan.mp4)

[Contact sheet](../../content/drafts/animations/symmetry-short-wavelength-path-scan-contact-sheet.png)

[Generator](../../scripts/generate_symmetry_short_wavelength_path_scan.py)

The upper view scans a uniformly illuminated aperture from left to right.
The blue line joins the current aperture point to an on-axis observer.
The lower view draws the corresponding ordered cumulative tip-to-tail
curve. The gold arrow joins its origin to its current endpoint. Both blue
markers refer to the same aperture coordinate at every frame.

Three passes use wavelength ratios 1, 1/16, and 1/256. Geometry, aperture
extent, scan speed, and complex-amplitude scale remain fixed. Each pass
has one second to establish the view, a ten-second linear scan, and a
one-second final hold. The MP4 is 36 seconds, 1440 × 960, at 60 fps.
The scan represents the order of addition, not propagation time or a
particle moving between the candidate paths.

## What changes

Shortening the wavelength confines the main advance of the sum to a
narrower neighborhood of the stationary path. Before and after that
crossing, additional contributions curl around the two endpoint regions.
Their individual directions are retained in the drawing.

The finished cumulative curve need not straighten. Its familiar shape
persists because the variable y/sqrt(λz) resolves the shrinking physical
neighborhood. Linking the curve to the aperture coordinate exposes this
localization, which a finished, unlabelled Cornu curve hides.

The blue aperture band marks |y| ≤ sqrt(λz), the stationary-phase scale
(the first Fresnel zone for this quadratic phase). Its width decreases
by a factor of four per pass, sixteen overall. This is **not** a boundary
outside which contributions vanish. The normalized contribution of this
band is about 1.242864 + 0.185081i; the outer zones still correct that sum.
Every contribution across the finite aperture remains in the calculation
and in the accumulated trace.

In the final pass the scan crosses the marked band in 0.442 seconds,
approximately 27 video frames. The camera and scan do not slow down at
the center. The apparent concentration in scan time follows from the
shrinking region in the aperture.

## Calculation

Let s = y/a, with aperture -1 ≤ s ≤ 1, and F = a²/(λz). The cumulative
amplitude, relative to the unobstructed plane wave exp(ikz), is

```text
C_F(s) = sqrt(F) exp(-iπ/4) ∫[-1,s] exp(iπ F t²) dt.
```

The normalized one-transverse-coordinate Fresnel prefactor is retained,
including its -π/4 phase. The analytic integral uses the Fresnel C and S
functions. No frame is rotated to align its resultant, and no total is
rescaled to unit length. All passes use 650 pixels per incident-field
amplitude unit. Their finite-aperture final amplitudes are:

| F | λ/λ₀ | Final amplitude |
|---:|---:|---:|
| 2 | 1 | 0.831669 − 0.144838i |
| 32 | 1/16 | 0.960016 − 0.039588i |
| 512 | 1/256 | 0.990050 − 0.009944i |

The top geometry is schematic. The model can use fixed z/a = 1000;
then the maximum omitted quartic phase is below 0.000403 radians even
in the shortest-wavelength pass. This is a scalar paraxial construction.

The trace is sampled independently of frame rate, with at most 0.45 pixels
of arc length per drawing segment. Each frame appends its exact current
integral endpoint. Small tangent arrowheads indicate the direction of
addition; they do not replace sections of the curve with grouped arrows.
The unresolved center of a tightly packed coil remains accumulated blue
ink, rather than disappearing through a visual fade.

## Validation and reproduction

Independent composite Gauss–Legendre quadrature checks all 601 scan-frame
positions in each pass against the analytic cumulative integral. Maximum
absolute discrepancy: 4.4 × 10⁻¹⁴. Checks also cover constant scan speed,
fixed drawing scale, sampling resolution, and curve containment.

[Calculation checks](../../content/drafts/animations/symmetry-short-wavelength-path-scan-validation.json)

The finished H.264 video decoded successfully at the intended resolution,
duration, and frame rate. Both blue marker positions were checked against
the model in 31 decoded frames, including the final central crossing at
0.1-second intervals. Rendered stills and encoded-frame contact sheets were
visually inspected for curve clipping, text collisions, and the narrowing
interval of net advance.

[Encoded-video checks](../../content/drafts/animations/symmetry-short-wavelength-path-scan-encoded-validation.json)

```text
python -B scripts/generate_symmetry_short_wavelength_path_scan.py --check --preview --render
```

This is a separate artifact. It preserves the earlier two-limit movie,
the raw short-wavelength still, and the grouped still, and does not change
the manuscript or deploy a website.

The normalization and stationary-phase scaling follow the
[Huygens–Fresnel derivation](https://farside.ph.utexas.edu/teaching/315/Waves/node99.html)
and the [stationary-phase discussion](https://farside.ph.utexas.edu/teaching/jk1/lectures/node78.html).
