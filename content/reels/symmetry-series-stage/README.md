# Local staged reels

Open `index.html` through the project HTTP server. The series contains 27 reels numbered consecutively. Original reel 20 is omitted. Original 24a becomes staged reel 24. The latest commutator and Casimir animations are staged reels 16 and 17.

Titles, numbering, covers, captions, and next-reel pointers come from the current editable text. Scientific motion is preserved from the latest reviewed MP4s. The source snapshot and mechanical edit record are in `source/`. Original reel labels remain in the editable source to avoid disrupting ongoing review.

## Music

All 27 MP4s include String Quartet No. 5, movement I (Philip Glass · Kronos Quartet). Consecutive excerpts play at a soft background level, with gentle fades on each reel and 2-second crossfades when the recording loops. Video streams are copied without reencoding. The preview plays the embedded audio, without an external music player.

The supplied recording and silent backups remain under the ignored `.tools/reel-audio/` directory. Nothing has been uploaded or scheduled.

## Rebuild

Run `scripts/symmetry_reels_v2/stage.py` with the project Python runtime from the repository root. It reads `notes/reels/symmetry-series-v2/reel-text.md`, preserves the earlier previews, and caches videos when their source footage and title overlays are unchanged. The CSV is a local inventory, not a social-platform import template.

To change only the audio mix, run `scripts/symmetry_reels_v2/stage_audio.py`. The local source is configured in `source/music.json`.
