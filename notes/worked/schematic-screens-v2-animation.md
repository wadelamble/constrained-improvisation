# Schematic screens v2: visible barriers at every column

The user wanted recognizable screens with slits rather than columns that read
as dots. This revision changes the late drawing layer while preserving the
52-second progression, physical masks, normalized wave calculation, phase
clock, and selected-cell contributions. It does not introduce a new
recombination animation. All earlier sources and media remain preserved.

- Renderer: `scripts/generate_symmetry_schematic_screens_v2.py`.
- Media prefix: `content/drafts/animations/symmetry-schematic-screens-v2`.
- Generate: `python scripts/generate_symmetry_schematic_screens_v2.py --preview --render`.
- Shared physics and earlier explanation: `plane-wave-screens-animation.md` and
  `schematic-screens-animation.md` in this directory.

The first 24 seconds call the preserved v1 frame renderer directly. The
23-second preview is pixel-identical to its prior counterpart. From 24 to 29
seconds, drawing style changes continuously: late blue opacity is capped at
45/255 and source-point dots disappear. Gold remains the complete field's
phase fronts, while blue remains a sparse sample of true cell contributions.

For the three many-screen targets, the real comb pitches remain 0.45, 0.225,
and 0.1125. Every opening is retained. Dark material strips are enlarged only
in the drawing, symmetrically around their real half-pitch centers; slit
centers remain at integer multiples of the pitch. Display thickness is the
larger of the real transverse thickness and 12 pixels, capped at 55% of the
pitch. This yields strip heights of 12, 10.3125, and 5.15625 pixels, with a
3-pixel horizontal stroke width. The remaining visible gap is always positive.
Exact display-pixel coverage keeps the smallest gaps legible.

The enlarged display targets interpolate with exactly the same eased amount
as the physical masks. Added columns appear continuously; changing combs
crossfade their correctly centered strips; all physical screen strokes fade
to zero over 42-46 seconds as the actual masks become identity. These enlarged
dimensions never enter the propagated field. The screen layer is drawn over
both wave layers, and the late legend states "screen strips enlarged."

The late legend distinguishes "total wavefronts (all sources)" from "sample
wavelets." After 46 seconds the remaining faint columns are explicitly
"imaginary slices" with no material strokes. Blue constructions persist at
reduced opacity and without source dots, while the gold plane fronts continue.

## Validation

The six full-size previews at 23, 33, 37, 41, 44, and 48 seconds were inspected
for barrier/gap visibility, visual hierarchy, and text placement. The early
23-second preview exactly matches v1. The unchanged propagation solver and
cell responses inherit the checks documented for v1; this drawing-only
revision does not require a new physical-model validation.

The finished MP4 is H.264 High, yuv420p, 1280 x 720 at 24 fps: 1,248 frames,
52.0 seconds, and 25,014,747 bytes. Full decoding reported no errors. Twenty-one
encoded frames were inspected, including full-size 33, 37, and 41 second views,
the changing comb stages, and half-second samples throughout the 42-46 second
screen fade. Screen segments and gaps remain distinct, gold remains dominant,
and the late legend is clear. Python compilation passes.

The unchanged first 24 seconds refer to source frames, which use the same
renderer directly. Encoded comparisons at 2 and 13 seconds were also
pixel-identical to v1. The 23-second source preview was pixel-identical, while
the re-encoded 23-second movie sample differed by a mean absolute 0.796 channel
levels out of 255 (maximum 34); this is a compression difference, not a change
to the early drawing or physics. Thus the two MP4 prefixes are not claimed to
be byte-identical.
