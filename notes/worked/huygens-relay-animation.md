# Continuous Huygens relay — schematic prototype

The user found the preceding Huygens field animation accurate but insufficient:
one finite reconstruction did not convey wavelets continually recombining and
regenerating. The user then explicitly suggested abandoning the realistic-looking
waves in favor of schematic lines. This supersedes the red/blue field requirement
for this relay prototype; it is not a blanket change to other project visuals.
All previous generators and finished media remain preserved.

## Visual mechanism

A following camera stays with one upward-advancing plane wavefront. Its gold
horizontal line remains fixed in the image, while earlier construction rows
recede downward. At regularly chosen reconstruction steps, a new set of points
on the current front seeds forward semicircular wavelets. Three generations
remain visible together. Each expanding family has the same current gold line
as its forward common tangent. The next generation therefore begins on the
newly constructed front without a pause or a return to an initial scene.

Successive rows are staggered by half a source spacing, making their handoff
legible. Blue arcs are construction wavelets, small blue points are their
construction centers, and pale dashed rows are earlier fronts. Older construction
annotations fade out to keep the drawing readable. That fading does not portray
physical amplitude decay or interference cancellation.

The film contains eight reconstruction steps and loops. Following the front
allows the process to continue indefinitely without resetting the physical
construction inside the visible scene. The upward arrow and camera caption make
the otherwise stationary envelope's motion convention explicit.

## Mathematical meaning and limits

Let the physical front height be h(t) = ct. Generation g is constructed at
t_g = g Δt, from the plane h_g = c t_g. Its wavelet radius is

    r_g(t) = c(t − t_g).

Consequently every retained generation has the same forward tangent:

    h_g + r_g(t) = ct.

In the following camera its source row lies r_g below the fixed envelope. The
semicircles remain circular because both drawing axes have the same scale.

The plotted points sample a continuous wavefront. The gold line is the common
tangent of the displayed circles and the exact forward envelope of the
continuous family; it is not asserted to be the scalloped outer boundary of a
finite union of disks.

This is a geometric Huygens construction. It does not display complex phase,
finite-wavelength interference, or a normalized amplitude sum. Its reconstruction
times are choices in the construction, not physical emission flashes or time
steps imposed on the wave. The previous signed-field models remain available for
those quantitative questions.

## Files and settings

- Geometry: `scripts/huygens_relay_model.py`.
- Renderer: `scripts/generate_symmetry_huygens_relay.py`.
- Media prefix: `content/drafts/animations/symmetry-huygens-relay`.
- Preview: `python scripts/generate_symmetry_huygens_relay.py --preview`.
- Render: `python scripts/generate_symmetry_huygens_relay.py --render`.
- Looping GIF: `python scripts/generate_symmetry_huygens_relay.py --gif`.
- Checks: `python scripts/huygens_relay_model.py`.

The prototype is 12 seconds at 24 fps, 1280 × 720. Reconstruction steps are
1.5 seconds apart. Three generations are retained; annotations of the oldest
fade smoothly before removal. The drawing uses the established desktop palette:
ivory background, restrained blue lines, and a gold envelope. Twofold supersampling
keeps the thin circles and moving points clean.

## Validation

Across 1,201 sample times, the maximum common-tangent error is 4.44 × 10⁻¹⁶.
Following-camera geometry repeats after 12 seconds to the same tolerance, and
the alternating row offsets repeat exactly because the loop contains an even
number of reconstruction steps. Rendered frames at 0 and 12 seconds are
pixel-identical. Early full-size stills and a contact sheet were inspected before
encoding.

The finished MP4 contains 288 frames at 24 fps and lasts exactly 12.0 seconds.
It decodes completely without errors. Encoded frames spanning the entire loop,
both staggered handoffs at 1.5 and 3 seconds, and the transition from the final
frame back to the start were inspected. The next small semicircles appear at the
new construction points while the prior generations remain visible; the seam
has the same normal handoff as the interior of the movie.

The companion GIF contains the three-second fundamental cycle: two construction
steps, so the row stagger also returns to its initial configuration. It is
960 × 540, 60 frames at exactly 50 ms per frame, with GIF loop count zero
(repeat indefinitely). One fixed palette avoids frame-to-frame palette changes.
Its line quality, source-point motion, and handoff frames were inspected after
encoding. This GIF makes continued regeneration visible even when an MP4 player
would stop at the end of the twelve-second file.
