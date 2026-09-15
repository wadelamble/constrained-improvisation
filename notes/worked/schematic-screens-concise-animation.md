# Schematic screens: shorter pacing

The user found that the 52-second v3 construction took too long to reach its
point. The concise version retains every stage and the same calculated image
layers, while reducing the lead-in and giving more of its time to additional
screens and the recovered plane wave.

- Script: `scripts/retime_symmetry_schematic_screens.py`
- MP4: `content/drafts/animations/symmetry-schematic-screens-v3-concise.mp4`
- Poster, decoded contact sheet, final frame, and validation share that prefix.
- Rebuild: `python scripts/retime_symmetry_schematic_screens.py`
- Original model and movie: see `schematic-screens-v3-animation.md`.

The retime is continuous, monotone, and applied to each complete original
frame. No cross-fades or interpolated pictures are introduced. Both line layers
retain their common phase at every displayed configuration. Playback speed
changes between portions of the story; some original frames are omitted.

| Source time | Presentation time |
|---|---|
| 0 s | 0 s |
| 2 s: first screen | 1 s |
| 22 s: second screen | 7 s |
| 42 s: finer slits | 17 s |
| 48 s: open slices | 21 s |
| 52 s: end | 24 s |

The first dense screen arrives at 5.8 seconds, and fifteen screens at 15 seconds.
The original file is preserved. Only the MP4 and poster references in ccr-2
change; the prose and the propagation model are untouched.

All 576 output frames decoded successfully at 1280 by 720 and 24 fps. Twelve
samples from the encoded MP4 were visually inspected across all portions of
the progression. At the fastest retime, successive output frames advance at
most four source frames, corresponding to 20 degrees of the shared wave
phase; there is no temporal phase reversal. The validation records both file
hashes and the exact time mapping.
