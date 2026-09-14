# Schematic screens v3: continuous buildup and complete grouped sums

The user asked for a two-second baseline, evenly paced story steps, and one
screen that remains present while its slit count rises. New screens should
arrive already densely slitted. Every visible opening must contribute a
wavelet; the old three-source subset is no longer used for dense columns.

- Model and timeline: `scripts/schematic_screens_v3_model.py`.
- Renderer: `scripts/generate_symmetry_schematic_screens_v3.py`.
- Media prefix: `content/drafts/animations/symmetry-schematic-screens-v3`.
- Generate: `python scripts/generate_symmetry_schematic_screens_v3.py --preview --render`.

All prior files and media remain preserved. The normalized scalar propagator,
wavelength 0.72, uniform incident plane, 1280 x 720 geometry, and 24 fps clock
are unchanged. The sequence still lasts 52 seconds, but its internal timing
and aperture states are new.

## Progression

After two seconds of plane wave, new story steps begin every four seconds.
Most mask transitions take 1.4 seconds, leaving a clear hold in each step.
The first screen is never removed between the coarse and dense slit stages.

| Starts | Configuration |
|---|---|
| 2 s | One screen, one slit |
| 6 s | One screen, three slits |
| 10 s | One screen, seven slits |
| 14 s | One screen, fifteen slits |
| 18 s | The same screen, dense slits |
| 22 s | Two dense screens |
| 26 s | Three dense screens |
| 30 s | Five dense screens |
| 34 s | Nine dense screens |
| 38 s | Fifteen dense screens |
| 42 s | Fifteen screens with finer slits |
| 46 s | Remaining material opens away over two seconds |
| 48-52 s | Open imaginary slices and the recovered plane wave |

Dense screens use pitch 0.225 and open fraction 0.995 from the moment they
arrive. The finer stage uses pitch 0.1125 and open fraction 0.9995. Their real
opaque strips are enlarged only for display, with the same centered,
gap-preserving method as v2. No enlarged dimension enters the wave equation.

## What is actually summed

At each chosen plane, visible transverse bins and one outside-view remainder
partition every numerical cell exactly once. In coarse steady states, opaque
cells are zero, so each visible bin contains a complete physical slit. Dense
states have 33 visible groups; the finer state has 65. The entire set is used
at every column, including partially transmitting cells. No small nonzero
physical contributions are silently discarded.

Each visible group's propagated field is computed by summing the normalized
circulant Green-response columns weighted by that group's actual post-mask
complex field. The outside-view remainder is propagated directly by the same
angular-spectrum FFT operator. The gold array is then formed by adding all
these group fields and the remainder, slab by slab. It is not supplied by a
separate full-field answer or a geometrically drawn envelope.

The blue lines and gold lines retain the common physical clock and inherited
input phase. There is no per-screen phase reset or independent amplitude
normalization. Gold shows positive-real phase contours of the complete sum,
using the same fixed 0.003 magnitude cutoff as earlier versions. Blue uses the
fixed 1e-5 contour cutoff. These are phase lines, not an intensity plot.

## Local curves and complete fields

Drawing every complete dense group field produced illegible blue hatching.
For 33 groups, each blue contour is therefore displayed only within 0.45
transverse units of its own source center; for 65 groups the half-width is
0.225. Every visible opening is still represented. Only the drawn curve is
cropped: the group's complete field remains in the gold sum everywhere in the
slab. The full outside-view remainder is included numerically and is not drawn
as another broad blue field. The legend states "local wavelet arcs" and
"full fields summed."

Coarse groups retain their full displayed curves. Blue display opacity is
chosen for legibility; it does not encode amplitude. The drawn arcs do not
geometrically morph into the gold front. The gold front is a new contour of
their actual complex sum. During refinement, a short fade of the blue
annotations hides a change of partition or slab boundary; the complete gold
field continues unchanged by that explanatory choice. At screen insertion,
partially transmitting background belongs to the visible bins, so a
transitional bin is not yet solely an isolated slit contribution.

## Efficiency and validation

Normalized Green responses and distance kernels are cached by slab geometry.
Two complete static grouped scenes are retained at most; a finer scene takes
about 150 MB for its visible component fields across all slabs. During each
transition, every mask is affine in the common transition amount. A grouped
complex field is therefore a polynomial of degree at most the number of
changing masks. Exact Chebyshev interpolation of that many plus one directly
solved scenes avoids solving every frame from scratch. Each visible group
and the outside-view remainder are interpolated separately; the gold field
is then explicitly summed from those arrays. Only the current transition's
nodes are retained, and its final node becomes the following static scene.
The shared phase clock and contour extraction are evaluated afresh per frame.
The renderer does not build a separate full-domain movie for every source.

Dense local contour grids are batched per slab with masked separator rows.
Each returned curve is translated back into its own physical coordinates.
Comparison against separate contour extraction gives maximum coordinate
discrepancy 5.33e-15. This changes computational overhead, not the geometry.

Independent validation of the rendered grouped sums against direct full FFT
propagation at eleven states and transition samples gives maximum complex
error 8.7e-15, including non-node samples after exact transition caching.
Re-adding the stored component arrays and remainder reproduces
the gold arrays to better than 2.2e-15. Model checks verify the exact partition,
complete plane-wave recovery, continuous presence of the first screen, and
dense construction of every additional screen.

The completed MP4 is 52.0 seconds, 1,248 frames at 24 fps, 1280 x 720,
H.264 High profile with yuv420p pixels, and 21,724,897 bytes. A full decode
reported no errors. Visual review covered 104 half-second samples across the
entire encoded movie, full-size dense-stage frames, and 48 adjacent frames
around the first dense partition, the second screen, finer slits, and final
recovery. The first screen remains visible continuously until its final
opening, the annotation fades hide partition changes, and the gold phase
fronts remain continuous through those fades. Headers and the two line-layer
labels remain clear of the field. No further render changes were needed.
