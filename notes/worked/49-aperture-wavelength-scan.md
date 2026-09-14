# Wavelength comparison with the original 49 openings

[Movie](../../content/drafts/animations/symmetry-49-aperture-wavelength-scan.mp4) ·
[Contact sheet](../../content/drafts/animations/symmetry-49-aperture-wavelength-scan-contact-sheet.png) ·
[Generator](../../scripts/generate_symmetry_49_aperture_wavelength_scan.py)

This version restores **one screen with 49 distinct openings, 49 candidate
paths, and 49 literal contribution arrows**. The same opening centers,
weights, spatial order, and arrow scale are used in every pass. Only
wavelength changes. Opening j and arrow j are identified together while
the sum is built. Every completed polygon contains exactly 49 arrows.

The original screen geometry is retained: centers span −2.8 to +2.8,
with pitch 0.1166667, opening width 0.07, and opaque gap width 0.0466667.
The on-axis observation point is 4.5 units beyond the screen. The drawing
is schematic, but all 49 openings and 48 intervening opaque bars are
distinct. Illumination at the screen has uniform plane-wave phase.

## Explicit amplitude and phase conventions

This is a **finite, equal-weight path phasor model**, displayed in
normalized phasor units. Assign magnitude one to each path and divide
every vector by the fixed number 49. Thus an all-in-phase sum would have
magnitude one. This same division applies in all frames and passes; it
never depends on the resultant.

The frame states both “normalized phasor units” and |vⱼ| = 1/49. It also
states “Phase relative to the straight path.” The equations are

```text
y_j = -2.8 + (j-1) (5.6/48),          j = 1,...,49
z = 4.5
L_j = sqrt(z² + y_j²)
φ_j(λ) = (2π/λ) (L_j - z)
v_j(λ) = exp(iφ_j)/49
P_m(λ) = sum(j=1,...,m) v_j(λ).
```

The phase reference removes the straight path's carrier exp(ikz).
Opening 25 lies at y = 0, so its vector points along the positive real
axis in every pass. No completed sum is rotated to align it with an axis.
The blue arrow j runs from P_(j−1) to P_j; gold joins zero to P_m.

The model uses exact geometric lengths, not their quadratic expansion.
It does **not** calculate complete physical propagation amplitudes,
slit transmission, obliquity, or diffraction within each opening. No
Fresnel prefactor is silently treated as an absolute physical amplitude.
The assigned equal magnitudes are the stated phasor convention, not a
claim that the complete scalar propagator has magnitude 1/49. Each
opening supplies one central path; it is neither subdivided nor replaced
by a numerical integral over subsidiary paths.

This is therefore distinct from the existing physically integrated
49-slit asset and from the continuous-opening Fresnel movies. Their
absolute amplitude claims do not carry over to this finite comparison.

## Wavelengths and timing

The wavelengths are 6.9688889, 1.7422222, and 0.4355556 in the same length
units as the geometry: λ₀, λ₀/4, and λ₀/16. The bookkeeping parameter
a²/(λz), using a = 2.8, is respectively 0.25, 1, and 4; the calculation
still uses the exact lengths above.

| λ/λ₀ | Final finite sum | Magnitude | Largest adjacent phase difference |
|---:|---:|---:|---:|
| 1 | 0.942715 + 0.247843i | 0.974750 | 0.054726 rad |
| 1/4 | 0.381356 + 0.523494i | 0.647672 | 0.218905 rad |
| 1/16 | 0.145514 + 0.135905i | 0.199110 | 0.875621 rad |

All arrows have length 14.2857 pixels, using 700 pixels per phasor unit.
The smaller final sum in these three examples follows from cancellation
among the same 49 equal arrows. The range was chosen to keep neighboring
phase changes below π/3 and individual arrows legible. This is not an
error estimate against a continuum integral: the finite sum is the model.

There is no claim that this fixed set approaches a stationary-path limit
as λ tends to zero. At shorter wavelengths the sampled phases can wrap,
rephase, and produce revivals; monotonic cancellation is not guaranteed.
Replacing 49 paths by a refining continuum would be another model change.

Each pass has one second to establish the scene, 49 additions at 0.2
seconds per path, and a one-second final hold. All passes receive the
same 11.8 seconds. The complete movie is **35.4 seconds, 1440 × 960,
60 fps**. The scan depicts spatial addition order, not propagation time.

## Validation

Checks confirm 49 disjoint openings, 49 positions and weights, and exactly
49 executed blue-vector draws per complete polygon. Position/weight
hashes match in every pass. All vector lengths match, each polygon edge
equals its assigned vector, and opening 25 has precisely zero relative
phase. An independent scalar calculation using direct geometric length
subtraction agrees with every finite prefix to within 5.6 × 10⁻¹⁶.
The checks also verify identical selection cadence, fixed scale, and
containment of every vertex.

The complete MP4 is decoded, its frame count and dimensions checked,
and 25 representative decoded frames compared against source renders.
Selected-opening pixels are checked against the corresponding path
index. Final stills and decoded contact sheets are visually inspected
for literal openings, arrow correspondence, clipping, and text collisions.

[Model validation](../../content/drafts/animations/symmetry-49-aperture-wavelength-scan-validation.json) ·
[Video validation](../../content/drafts/animations/symmetry-49-aperture-wavelength-scan-encoded-validation.json) ·
[Decoded contact sheet](../../content/drafts/animations/symmetry-49-aperture-wavelength-scan-encoded-contact-sheet.png)

```text
python -B scripts/generate_symmetry_49_aperture_wavelength_scan.py --check --preview --render --encoded-check
```

The 121-path prototype, earlier media, and manuscript files are preserved.
