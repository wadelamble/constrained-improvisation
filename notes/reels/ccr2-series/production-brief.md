# CCR-2: Waves to Quanta

Production decision: thirteen silent, cumulative portrait reels, 30–60 seconds
each. Animations and equations are in the video; verbal explanation belongs in
the accompanying post caption. No Instagram account is needed to stage these.
The source manuscript remains untouched.

1. Translate a function in position and wave number.
2. Translate two functions together: overlap is preserved.
3. Rotate the complex function: global phase versus position.
4. Close an x/k loop: a phase remains; the commutation relations close.
5. Fourier localization and uncertainty.
6. Travelling waves, apertures, and the short-wave ray limit.
7. Multiply along a route; add across routes.
8. Many routes, one complex sum, one intensity.
9. Huygens: wavelets recombine; dense transmitting screens recover free space.
10. Short wavelengths: match the path position to the colored phasor chain.
11. The quantum import: amplitudes encode measurement probabilities.
12. Preview of spacetime: mass shells, proper time, action and phase.
13. Momentum, the canonical commutator, and uncertainty in physical units.

## Shared visual contract

1080×1920, 24 fps, H.264 MP4, no audio. Dark background, ivory text, cyan/red
complex waves, gold envelope/phase, green resultants. Essential content inside
x=70…950 and y=160…1620. Shared core owns title and progress footer. Artwork
begins at y=480. Keep text ≥30 px, equations ≥42 px where practicable. In-frame
prose is brief; captions explain the argument. Do not shrink a landscape movie
into an unreadable portrait rectangle.

Each episode module exports `EPISODES`: integer keys with `title`, `duration`,
`render` (function of seconds returning RGB PIL Image), `caption`, `checkpoints`
(seconds for review), and optionally `validation` (numerical facts/checks).
Use `from core import *` (the renderer adds this directory to sys.path).
Core exposes Scene, helix, phasor, spectrum_color, np, Image, ImageDraw, ease,
window, and the shared colors. `Scene(n,title,stage,t,duration)` creates header;
`s.im` is the final frame. Panels: x70…950, y480…1430. Equations/notes can occupy
1450…1630. Test every math string in real frames; matplotlib mathtext is used.

## Mathematical contract

Transforms: Tx(a)ψ(x)=ψ(x−a), Tk(b)ψ(x)=exp(ibx)ψ(x).
Chronological loop +k,+x,−k,−x leaves exp(−iab)ψ. Global phase preserves |ψ|.
Fourier transform is unitary; normalized Gaussian widths obey σxσk=1/2.
No manufactured cancellation, per-frame phasor rescaling, or deleting unwanted
contributions. Candidate paths are calculation terms, not observed trajectories.
Reuse the accepted dense-path normalized model if showing its stationary limit.
The Born rule, physical dynamics, and empirical ħ calibration are physical input,
not consequences of the commutator alone. Spacetime/proper time is a preview;
state c=1 when using S=−mτ. Mass labels a mass shell, not a standalone Newtonian
parameter introduced without context.

## Deliverables

One cover JPEG and caption TXT per video; ordered JSON and CSV manifests;
local HTML gallery; production/readme and research sources; renderable code and
focused numerical checks. Publishing remains a later account-connected step.
Original project videos and manuscript are preserved.
