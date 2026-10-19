# Symmetry to Waves — offline first cuts

Open `index.html` to review the ordered series. Titles and captions come from
`notes/reels/symmetry-series/reel-text.md`; edit that document, then rerun
`scripts/symmetry_reels/render.py --package`. Title changes also require new
video and cover renders. No account, upload, or publishing code is present.

The source is `content/drafts/symmetry-draft.md`, stopping before “The Fourier
Structure of Waves.” The manuscript and Waves to Quanta series are preserved.
Masters: 1080×1920, 30 fps, silent H.264/yuv420p, fast-start. The gallery plays
the MP4 masters directly; optional 720×1280 WebM previews are used if generated.
Captions use the Buffer-adjusted UTF-16 count, limited to 2196.
The gallery and manifest explicitly identify missing media during production.

Production commands use the available scientific Python runtime:
`render.py --review --render --package` (add `--episodes 1 2` for a subset).
Use `render.py --previews --package` only to make optional WebM previews.
The review contact sheets initially come from
the renderer. Final motion QA must also inspect dense frames decoded from MP4s.
