# Intensity carried by the travelling wave itself

Version 7 removes the detector brightness strip and the added intensity
curve from the introduction. One large wave view shows A, the 49 physical
slits, and a thin line marking the detector. The four-second introduction,
18.5-second checked body, and absence of a closing wave remain: 540 frames
at 24 fps, lasting 22.5 seconds.

Every wave pixel uses its own calculated complex field E(x,y). Phase
changes the red/gray/blue hue. Color strength against the warm paper follows
the local intensity, `abs(E(x,y))**2`, throughout the image. No detector
profile is copied, extended, or imposed on any part of the travelling wave.
The wave is the same 49-slit scalar propagation calculation as version 5;
only its visual encoding changes.

The prior signed-field coloring let optical zero crossings erase the
apparent local intensity. Version 7 separates those two displayed
quantities. The phase colors have the same Rec.709-weighted RGB luma, so
the carrier changes hue without changing the contrast assigned to intensity.
Their strength against paper is `min(1.6 * abs(E)**2, 0.90)`. One global
exposure applies on both sides of the slit screen, with no subtraction of
a minimum or local normalization. The brightest source and near-mask
regions reach the finite display range. The detector range of approximately
0.27 to 0.45 is below that limit, so its variations remain linear and are
not clipped. Stronger ink means greater intensity; this is a scientific
phase/intensity color encoding, not a literal picture of light's color.

This makes the interference envelope visible in the travelling field,
including the region immediately before the detector. Phase colors continue
moving through that steady envelope. The physics is not altered to create
the effect. The rendered caption states: color is wave phase; color strength
is local intensity.

Checks cover the original slit integrals, agreement with the schematic's
intensity profile, and proportionality of the color encoding to intensity
at multiple carrier phases. The detector range is explicitly checked to be
unclipped. All 444 body frames must match the version 5 input. The completed
movie is decoded, counted, and checked through encoded frames.

The implementation remains `scripts/generate_symmetry_desktop_wave_bookends.py`.
The canonical entry point is:

```powershell
python -B scripts/generate_symmetry_many_slit_paths_phasors_interference.py
```

Version 7 is saved as
`content/drafts/animations/iterations/symmetry-many-slit-paths-phasors-interference-v7-intensity-in-the-wave.mp4`.
The canonical `content/drafts/animations/symmetry-many-slit-paths-phasors-interference.mp4`
is updated to match. Earlier films and source snapshots are preserved.
