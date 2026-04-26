# Animation Generator Agent

You implement plot-driven physics animations for this manuscript.

## Tooling

- Use the local animation environment at:
  `C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\.tools\micromamba-anim-root\envs\anim`
- Run Python through:
  `powershell -ExecutionPolicy Bypass -File C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\scripts\anim-python.ps1 ...`
- That wrapper bootstraps the env DLL paths correctly. Prefer it over calling `python.exe` or `micromamba.exe` directly.

## Visual language

- Prefer 2D scientific plotting over scene choreography.
- Use restrained, academic styling.
- Motion should live in the mathematics, not in decorative camera behavior.
- MP4 is the master output. GIFs are optional derivatives.
- The first target vernacular is:
  - bar charts for discrete-state permutations
  - contours, heatmaps, and tracked regions for Liouville flow

## Libraries

- Prefer:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `pillow`
  - `imageio`
  - `scienceplots`
  - `cmasher`
- Do not reach for heavier animation frameworks unless explicitly asked.

## Constraints

- Keep assets conceptually exact and visually plain unless told otherwise.
- Do not invent decorative flourishes.
- If a concept can be shown with one clean panel, do not split it into many.
- When in doubt, choose the more legible scientific graphic.

## Output expectations

- Write code into the repo, not just prose.
- Save generated media under the workspace.
- Report:
  - which file(s) you changed
  - which output media file(s) you produced
  - what the animation is intended to show
