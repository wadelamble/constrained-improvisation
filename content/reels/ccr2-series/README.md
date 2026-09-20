<!-- action-phase-20260920 completed -->
# Current publication — September 20, 2026

Reel 12 action-phase replacement and unchanged Reel 13 repost verified live; both superseded posts removed. Other eleven posts unchanged. Latest order: 13 down to 1.

Only reels 12 and 13 were updated in this publication run. Reel 12 uses the approved 24-second action-phase animation and omits the obsolete calibration-plot sentence from its caption; Reel 13 was reposted unchanged. Current receipt: `notes/reels/ccr2-series/publication-20260920-action-phase.json`. Earlier dated receipts and production notes below are historical.

---

# Current publication — September 19, 2026

All 13 replacements are live on @symmetryphysics, published in order 1–13; the old copies were removed. Local titles and captions match the final live set. Canonical receipt: `notes/reels/ccr2-series/publication-20260919.json`. Reproduce title layouts with `scripts/ccr2_reels/retitle_live.py --titles notes/reels/ccr2-series/publication-20260919.json --prepare` using a fresh `--run-id`. Earlier production notes below are historical.

---

# Waves to Quanta — review and publishing package

Open `index.html` to review thirteen reels in order. Each video has a matching
cover JPEG and UTF-8 post-caption TXT. `manifest.json` and `manifest.csv` retain
the ordering and exact pairings. Captions are post text, not narration.

Recorded for @symmetryphysics: 12/13 current videos hosted; 13/13 current Instagram reels published; 0/13 Buffer drafts. Reel 5 uploaded directly through Instagram web and verified 2026-09-17T18:31:11.526Z.

The manifest includes public media URLs, Buffer post IDs, Instagram links, and
publication timestamps only when the recorded video and caption hashes match
this package. Any remaining Buffer drafts require a separate scheduling or
publishing action. Publishing receipts remain in
`notes/reels/ccr2-series/buffer-staging-status.json`; the website build copies
only the MP4 media, not these receipts or this review package.
The CSV is our portable manifest, not a claim that Instagram directly imports CSV.

All MP4s are 1080×1920, 42 fps, H.264/yuv420p, fast-start, and silent.
Playback is 1.75× the original pace. Reel 5 uses the approved extended finite-width rendering; the other twelve videos retain their original frames.
The gallery
uses lighter 720×1280 WebM previews; the Video link provides the full MP4. Preview
framing leaves margins for player controls. Platforms can change overlays, so
check the first draft in the destination app before posting the series.

Source: `notes/worked/symmetry-ccr-2.md`. Production source:
`scripts/ccr2_reels/`. Original chapter and existing animations are preserved.
Run `render.py --review`, `render.py --render --episodes 1 2`, or
`render.py --previews --package --bundle` with the project Python runtime to
regenerate the review and portable publishing package.

Equations and simulations are original renderings. The final spacetime/action
episodes are a compact preview, with physical assumptions identified in captions.
The series does not claim to derive dynamics or the Born rule from the CCR alone.

Reel 5 was replaced on Instagram on 2026-09-17 with the author's exact Slide 5 caption. Its current files are in this directory. The portable ZIP predates this targeted replacement.

Title refresh. Reels 4, 5 and 7–13 have revised headers and covers. Animation frames and 1.75× timing are preserved. These revisions are local only. Caption text and publishing receipts are unchanged. Run `retitle.py --prepare` then `retitle.py --render` to reproduce from the preserved inputs. The portable ZIP predates these revisions.
