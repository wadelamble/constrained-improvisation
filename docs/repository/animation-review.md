# Reviewing Wave Symmetry and its animations

The public `/animation-review/` page accompanies the Wave Symmetry chapter
(`notes/worked/symmetry-ccr-2.md`). Each of its 14 animations links to a review
page through **Code and frames**. The other chapters are outside this packet.

The packet provides chapter text, surrounding passages, decoded frames, source
files and their dependencies, and existing generator reports where available.
It contains no previous critiques, grades, private project memory, or chats.
The ZIP excludes the MP4s and links to the published movies instead.

For an outside review, supply the review page or its downloadable ZIP to a new
reviewer. Read `review.md` first. A fresh chat is not itself a guarantee that a
service's memory or account instructions are disabled; configure those controls
separately or use an account with no project history.

## What the evidence establishes

Frames come from the delivered MP4s, not a fresh rendering of the generator.
Each movie has twelve evenly spaced sampled frame indices, including the first
and last, with timestamps read from the decoder. Full-resolution JPEGs accompany
the contact sheets. Sampling is systematic rather than a selection of favorable
moments, but cannot establish continuous motion or capture every transition.

Hashes tie each frame set to a specific movie and identify the exact delivered
source bytes. The source mapping describes the generation pipeline and its
known limits. It is not a reproducible-build attestation. Existing generator
reports are author-produced checks, not independent certification, and the
site builder does not rerun them.

Assess the chapter's physical and mathematical correctness, the support for its
conclusions, explanatory clarity for its intended reader, and fidelity of the
visuals. Separate errors from ambiguities and preferences. Cite passages,
equations, frames or code; distinguish direct observations from inferences.
Properties not examined should remain unassessed.

## Updating the packet

The site build needs only Python's standard library. Frame extraction needs
Pillow and `imageio-ffmpeg`. The extraction script also checks the project's
existing `.tools/animation-python-packages` installation.

1. Update the explicit source mapping in `site_src/animation-sources.json` if a
   generator, dependency or output changes.
2. After changing an MP4, extract its frames. Unchanged movie/frame hashes reuse
   the existing files.

   ```powershell
   python scripts/prepare_animation_review.py
   # Or just one animation
   python scripts/prepare_animation_review.py --only symmetry-action-phase-desktop.mp4
   ```

3. Build and check the site.

   ```powershell
   python scripts/build_site.py
   python scripts/check_animation_review.py --site site
   ```

   When using `SITE_BASE_PATH`, pass the same prefix to the checker with
   `--base-path /constrained-improvisation`.

4. Inspect representative full-size frames and rendered review pages. Commit
   the source mapping and `content/review/animation-frames/` files with the
   changed movie. The generated `site/` directory remains ignored.

The build fails on a missing source mapping, a changed movie without fresh
frames, or a frame hash mismatch. The checker also checks published links,
source/report hashes and the exact ZIP contents. It does not grade the physics.
