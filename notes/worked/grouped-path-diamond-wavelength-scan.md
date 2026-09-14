# Fixed groups of neighboring paths

This standalone version answers the request to see grouping: replace the
tip-to-tail chain from each fixed region of the screen by its net arrow.
It uses the same 20,001 paths and complete scalar propagation model as
`normalized-path-diamond-wavelength-scan.md`, without changing any term.
All earlier films and generators remain available.

## What changes in the drawing

Split the permitted screen span [-2.8, 2.8] into seven equal physical regions,
width 0.8. Their boundaries are fixed across wavelengths, independent of
phase. The central region is [-0.4, 0.4]. Group the existing midpoint samples
by their crossing positions; counts run 2,857, 2,858, 2,857, 2,857, 2,857,
2,858, 2,857 from top to bottom. These are regions of the existing sampling
plane, not seven new holes or a new physical transmission mask.

For each region, the displayed blue arrow is the exact sum of its original
contributions: the chord between the endpoints of that region's subchain.
It is not a representative path. The gold arrow is the complete sum of all
20,001 contributions throughout the regrouping. Blue chord endpoints agree
with the original cumulative chain to floating-point accuracy.

There are three equal eight-second passes, at wavelengths 0.5, 0.05, 0.005.
Each begins with the old raw chain for 0.6 seconds, replaces the seven groups
in top-to-bottom order at 0.7 seconds per group, and holds the grouped result
for 2.5 seconds. A brief chord reveal and removal of its original subchain
are explicitly a change of representation at fixed wavelength. They do not
depict a change in physical contributions or cancellation by fading. The
highlight in the diamond identifies the group being replaced; it does not
encode probability or intensity. During the final hold it marks region 4.

The reference remains independent unobstructed A-to-B propagation, and the
scale stays 620 pixels per unit. The result is not divided by its endpoint.
The three gold endpoints therefore remain exactly those of the previous
normalized film. The centered path belongs to region 4 at every wavelength.

## What this finite example shows

| Wavelength | Central-region magnitude | Largest outer-region magnitude |
|---|---:|---:|
| 0.5 | 0.745611 | 0.410091 |
| 0.05 | 0.922531 | 0.167256 |
| 0.005 | 0.987134 | 0.040454 |

The grouped chain approaches one dominant arrow, with finite exterior
residuals still visible. These numbers are amplitude magnitudes, not
probabilities of arrival. Every fixed exterior region is nonstationary, so
its normalized resultant tends to zero in the short-wavelength asymptotic
limit. The central region contains the shrinking stationary neighborhood.
Convergence need not be monotone at every intermediate wavelength because
finite-boundary terms oscillate. The ungrouped curve is not asserted to
straighten: grouping is the essential change in what an arrow represents.

## Validation and outputs

Focused checks verify exhaustive symmetric grouping, fixed sample positions,
every grouped prefix against the original cumulative chain, unchanged total,
symmetry, drawing bounds, and threefold quadrature refinement. Maximum
regrouping discrepancy is 6.72e-15; maximum refinement error per region is
3.13e-5. The unchanged physical propagator was validated separately in the
previous normalized version.

The video is 24 seconds at 1440 × 1080, 30 fps. Encoded verification decodes
all 720 frames and compares 15 representative frames with source renders,
including visible gold-tip positions. Source and encoded contact sheets
are generated for visual inspection.

- Generator: `scripts/generate_symmetry_grouped_path_diamond.py`
- Movie: `content/drafts/animations/symmetry-grouped-path-diamond-wavelength-scan.mp4`
- Stills: the same stem with `-lambda-1.png` through `-lambda-3.png`.
- Checks and contact sheets: the same stem with `-validation.json`,
  `-encoded-validation.json`, `-contact-sheet.png`, and `-encoded-contact-sheet.png`.

```powershell
python -B scripts/generate_symmetry_grouped_path_diamond.py --check --preview --render --encoded-check
```
