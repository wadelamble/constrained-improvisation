# State and evolution reels

Five portrait adaptations of the desktop animations added after the previous Instagram batch. The approved titles are in [reel-text.md](reel-text.md).

## Review and edit

- [Editable captions](reel-text.md)
- [Local review gallery](../../../content/reels/symmetry-evolution/index.html)
- [Output manifest](../../../content/reels/symmetry-evolution/manifest.json)

Edit each **Caption** in `reel-text.md`. Captions are separate from the MP4s. Refresh the plain-text exports and gallery with:

```powershell
python scripts/symmetry_evolution_reels/render.py --package
```

Titles and on-screen wording are baked into the videos. Their lists in the Markdown document are references, not live renderer inputs. A title change is deliberately rejected by the packager until the renderer is updated and the affected reel is rerendered.

```powershell
python scripts/symmetry_evolution_reels/render.py --reels 3 --preview --render --validate
python scripts/symmetry_evolution_reels/render.py --package
```

The script uses packages under `.tools/animation-python-packages`. Use the project Python environment, not the Windows Store Python alias. These commands have no posting, scheduling, committing, or deployment behavior.

## Contents

| Reel | Title | Duration |
| --- | --- | --- |
| 1 | Reversible evolution preserves information | 24 s |
| 2 | Unitary evolution preserves overlap | 24 s |
| 3 | Transforming an operator | 23 s |
| 4 | Commuting operators | 17 s |
| 5 | Information preservation and state-space geometry | 42 s |

Exports are 1080 × 1920, 30 fps, H.264 MP4 with AAC audio. The soundtrack uses the previously supplied Philip Glass / Kronos Quartet recording and existing soft music bed, with consecutive excerpts and gentle fades. The local recording is not copied into this folder.

Each reel includes a poster, a portrait cover, a caption `.txt`, and a decoded-video contact sheet. Mathematical model checks are recorded in `model-validation.json`. Individual reports in `review/` verify dimensions, duration, frame count, audio signal, and source hashes.

The desktop animations and manuscript were not modified. The two histories compare separate states. The grid in Reel 5 maps a selected wave-packet family to its averages and does not count quantum states.

## Instagram publication

Published to **@symmetryphysics** on November 20, 2026 (Pacific time). All five posts were confirmed sent, with exact caption, video URL, and selected-thumbnail matches.

- [1. Reversible evolution preserves information](https://www.instagram.com/reel/Df_GXoblLnh/)
- [2. Unitary evolution preserves overlap](https://www.instagram.com/reel/Df_GkarkvXO/)
- [3. Transforming an operator](https://www.instagram.com/reel/Df_GuPuFKsa/)
- [4. Commuting operators](https://www.instagram.com/reel/Df_G62eFCoE/)
- [5. Information preservation and state-space geometry](https://www.instagram.com/reel/Df_HMBmlnKG/)

[Publication receipt](publication-20261120.json).
