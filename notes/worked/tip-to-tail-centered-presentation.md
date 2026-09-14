# Central sum aligned for presentation

This note records the original continuous-opening presentation. The current
49-slit desktop movie keeps the same fixed-reference convention but uses the
new mask's +1.87341523-degree offset. See
[the physical-slit correction](desktop-49-physical-slits.md).

The user requested removal of the slight initial tilt, permitting a
documented presentation adjustment. This version applies one constant
rotation to the displayed phasors:

```math
a_j^{\mathrm{display}}(B)=e^{-i\arg S(0)}a_j(B),\qquad
S(0)=\sum_j a_j(0).
```

The angle is approximately +5.058 degrees. It is applied to every arrow,
partial sum, and complete sum for the entire movie. The completed sum at
symmetric B is horizontal. Later spinning, relative arrow angles, arrow
lengths, and intensity are preserved. There is no time-dependent easing or
detector-dependent straightening, and only rotating the green resultant
would be incorrect because it would break the tip-to-tail addition.

This chooses the finite-aperture central sum as the display's phase zero.
It does not remove the physical phase difference from the unobstructed
wave. The gray no-screen phasor is omitted from this presentation copy;
otherwise that same relative difference would remain visible. The gray
no-screen intensity curve in the third pane remains. The frame's phase
reference caption is updated to match the actual convention.

The underlying model and unadjusted videos are preserved. See
[the corrected model notes](tip-to-tail-corrected.md) for physical scope.

New videos, each 18.5 seconds at 24 fps:

- `content/drafts/animations/symmetry-tip-to-tail-corrected-centered.mp4`
- `content/drafts/animations/symmetry-many-slit-corrected-centered.mp4`

The implementation is the documented `center_presentation()` function and
the `--center-phase` option in
`scripts/generate_symmetry_tip_to_tail_corrected.py`. No change is made to
`scripts/corrected_tip_to_tail_model.py`.

```powershell
python -B scripts/generate_symmetry_tip_to_tail_corrected.py --center-phase --preview --render
```

The centered validation report records the rotation, central sum, fixed
plot margins, and encoded video checks. The existing physics validation
continues to describe the unchanged physical model.

This treatment is now installed at the canonical desktop filename,
`symmetry-many-slit-paths-phasors-interference.mp4`. The original and revised
videos, preview images, and source snapshots are recorded in
[the desktop version history](desktop-three-pane-versions.md).
