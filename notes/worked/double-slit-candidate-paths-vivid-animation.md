# Two contributions at B: visual refresh

The ccr-2 point-source/two-path animation uses the vivid signed red/blue field
on black. An ideal source A replaces the former plane-wave strip and first
source screen. Captions are outside the wave field. On review, the user asked
to restore the explicit spherical-component arcs; they are present in the
current revision. Earlier versions remain available.

- Generator: `scripts/generate_symmetry_double_slit_candidate_paths_vivid.py`
- MP4: `content/drafts/animations/symmetry-double-slit-candidate-paths-shortwave-arcs.mp4`
- Poster, source/decoded contact sheets, and validation reports share its prefix.
- Rebuild: `python scripts/generate_symmetry_double_slit_candidate_paths_vivid.py --check --preview --render --encoded-check`.

The geometry remains A=(-3.2,0), C=(0,1), D=(0,-1), B=(5.2,0.55), with wavelength
0.5, matching the opening wavelength of the preceding short-wave-beams movie.
Path lengths remain 8.57204576 and 8.77870528, giving relative phase
2.59696017 radians. The outgoing phases are k(AC+rC)−ωt and k(AD+rD)−ωt. The old
common phase reference k*A.x is removed, without changing their difference.
Both contributions are present throughout. Only their dashed route guides are
revealed sequentially, beginning at 1.6 and 3.8 seconds. There are no moving
particles or highlighted beads that would imply an object takes a route.

This preserves the original phase-only point-aperture illustration, including
its softened source falloff and shared outgoing amplitude falloff. It is not a
finite-aperture boundary calculation or quantitative spherical-wave irradiance
model. The companion still uses equal normalized contributions and the same
relative phase: `content/drafts/diagrams/symmetry-double-slit-two-path-phasor-sum-shortwave.png`.
Its generator is `scripts/generate_symmetry_two_path_phasor_shortwave.py`.
A common phase places the resultant on the real axis; its normalized magnitude
is 0.53792609. The original still remains available.
One fixed signed color scale is used throughout, with no local/frame gain.

Thin white source fronts and cyan/gold C/D fronts satisfy
k*(incoming path length + radius)−ωt = 2πn. They mark equal phase of each
component, including its source-to-slit phase, rather than contours of the
sum. They were checked against that phase condition (maximum complex residual
1.91e−14) and clipped separately to the appropriate side of the screen.

The user found that the saturated red/blue palette works better when the
wavelength is short: fine stripes read as texture, whereas long-wavelength
bands become broad, visually forceful masses. At the user's request, this
revision shortens the wavelength from 1.25 to 0.5 while retaining the component
arcs and the same color map.

The 10-second movie is 1440×810 at 30 fps, with equal physical x/y scales and
period 1.6 seconds. The algebraic sum was checked against the original real
cosine expression (maximum discrepancy 6.23e−15). All 300 encoded frames decode
successfully; source/decoded sample mean RGB errors with arcs are 2.56–2.75 out of 255.
Source and decoded contact sheets were visually checked for slit visibility,
route legibility, circular fronts, and label placement.
