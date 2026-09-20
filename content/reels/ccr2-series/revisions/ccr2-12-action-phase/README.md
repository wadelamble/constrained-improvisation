# Reel 12 action and phase revision

Approved and published on September 20, 2026 as https://www.instagram.com/reel/Ddg_MPFDskC/. Reel 13 was reposted immediately after it to preserve the series order. Both superseded Instagram copies were removed after verification. The current publication receipt is `notes/reels/ccr2-series/publication-20260920-action-phase.json`.

- 0–8 seconds. Change the displayed frame on the lowest shell. The worldline event stays at the origin. Proper time is not labeled yet.
- 8–24 seconds. Three equal passes use successively higher shells. Each pass advances the same proper-time interval, from 0 to 12 fs, on the same straight worldline.
- The phase dial rotates clockwise according to `phi = -kappa * tau`, without a numeric counter.
- The action bar uses a fixed 0–36 eV fs scale. Its three endpoints are 12, 24 and 36 eV fs. Its numerical readout gives the action magnitude; the signed convention is `S = -m * tau`.
- Numerical masses appear in the action tile only, through `m = hbar * kappa`. The upper tile is titled “Wave-number shell.”

Units are `c = 1`, time in femtoseconds, spatial distance in light-femtoseconds, mass in eV and action in eV fs. The masses 1, 2 and 3 eV are illustrative values, not claims about named particle species. The displayed phase uses these values directly, with no separate phase-speed adjustment. One femtosecond is 10^-15 seconds.

Generator, relative to the repository root: `scripts/ccr2_reels/revise_action_phase.py`. Running it creates review stills and numerical validation. Add `--render` to generate the MP4 and WebM. It does not rebuild captions, manifests, publication receipts or the main gallery.

The caption retains its previous wording except for removal of the obsolete sentence “The calibration plot is schematic.”
