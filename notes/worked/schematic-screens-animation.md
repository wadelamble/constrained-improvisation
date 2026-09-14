# Schematic screens, slits, and wavelets

The user requested the **same screens and slits being added**, with schematic
arcs replacing the realistic signed-field treatment. This is the operative
correction for this version. The intervening no-barrier Huygens relay remains
preserved as a separate experiment. This film returns to the original
left-to-right, 52-second screen/slit progression.

## Files and regeneration

- Renderer: `scripts/generate_symmetry_schematic_screens.py`.
- Unchanged physical model: `scripts/plane_wave_screens_model.py`.
- Reused complete-field cache: `scripts/generate_symmetry_plane_wave_screens.py`.
- Media prefix: `content/drafts/animations/symmetry-schematic-screens`.
- Generate: `python scripts/generate_symmetry_schematic_screens.py --preview --render`.
- Selected previews: add `--times 8.5,13,33,41,48`.

The script uses the existing optional `.tools/animation-python-packages`
directory for NumPy, Pillow, ContourPy, and imageio-ffmpeg. All project paths
are relative to the script. Existing generators and outputs are preserved.

## What the lines mean

Gold **combined wavefronts** are constant-phase contours of the actual complete
complex field U, after normalized angular-spectrum propagation through the
current masks. The extraction is Im(U exp(-i omega t)) = 0 with positive real
part. This avoids an argument-function branch cut. The fixed magnitude cutoff
is 0.003 on the incident-unit scale; it prevents assigning visible phase lines
to near-zero fields. Line thickness does not represent amplitude or intensity.

Blue **selected wavelets** are the same phase contours of representative
single-cell contributions. In the early 1, 3, 7, and 15 slit stages, one cell at
each slit center visibly seeds its own wavelet. The nearest mesh cell supplies
each source. In the dense multi-screen stages a sparse subset at transverse
coordinates -0.9, 0, and +0.9 keeps the repeated local construction readable.
A cell is shown only when its actual transmission and actual post-mask field
are nonzero. These selected transmitting elements are not whole slit
apertures and do not form the complete summed field alone. Dense sets use paler
construction lines to preserve the visibility of the gold combined fronts.

For a source cell j on a screen, the displayed contribution at downstream cell
i and distance d is

    U_after_mask[j] * ifft(exp(i d sqrt(k^2 - q^2)))[(i-j) mod n].

This is exactly one column of the same discrete normalized propagator. It
retains the actual local complex phase at later screens; there is no new
per-screen phase origin, independent normalization, or raw exp(i k L) shortcut.
The fixed blue numerical-zero cutoff is 1e-5. Blue and gold contours share the
same exp(-2 pi i t / 3) clock. Chosen line weights identify layers; they do not
claim that a tiny cell carries the same physical amplitude as the whole wave.

Blue contributions are drawn only in the slab ending at the next active
physical screen. The field is then decomposed anew from transmitting cells on
that screen. The gold field is computed from every aperture cell, including
those outside the displayed view. No geometric shadow mask is applied to the
downstream field; diffraction can enter regions behind opaque material.

After 46 seconds all physical masks are identity. The same fifteen positions
remain as faint imaginary construction slices and the blue decomposition is
retained between them. Segmentation there is an explanatory choice, not
physical interception. The gold total remains the original continuous plane
wave in both amplitude and phase. This final simultaneous view makes ongoing
wavelet reconstruction visible without changing the recovered field.

## Geometry and progression

The original shared model controls every wavelength, mask, screen position,
time, and phase: 1280 x 720, 24 fps, 52 seconds; x=0..14.4 and y=-3.6..3.6;
equal physical axis scale in pixel rectangle (40,80,1240,680). The new palette
is restrained ivory, blue, and gold, with dark barrier strokes.

The sequence is plane wave; one screen with 1, 3, 7, then 15 slits; the first
barrier opening away; 3, 7, then 15 increasingly transparent perforated screens;
and finally identity masks at every screen. Physical strokes use the actual
cell-averaged opacity. Small exterior ticks keep screen positions visible when
opaque remnants fall below pixel scale, without changing numerical masks.

As in the original, mask changes are successive monochromatic configurations,
not a causal simulation of a barrier-insertion transient. The finite-wavelength
phase contours are derived from the wave equation model, rather than being
purely geometric circle envelopes. See `plane-wave-screens-animation.md` for
the physical model, padding and mesh checks, and unchanged propagation limits.

Construction annotations fade with the visibility of newly introduced or
removed screens. In particular the first screen's blue guides fade throughout
24.5-28 seconds instead of vanishing abruptly. This fade changes annotation
visibility only. At the final recovery the guides remain visible as the
material opens away, because the same construction continues on imaginary
slices.

At 34 and 38 seconds the newly introduced planes subdivide the previous local
decomposition. The blue layer fades to zero over 0.4 seconds before each
boundary and returns over 0.4 seconds afterward, so changed clip endpoints
never pop into view. Individual selected-source visibility also follows its
actual transmission. These are annotation fades; the gold total and physical
mask sequence continue unchanged throughout.

## Validation

The complete field and transition interpolation are reused unchanged from the
reviewed wave renderer. Its full plane-wave reconstruction and phase-composition
checks remain applicable. The new cell-response layer is checked against a
fresh direct propagation of a vector containing only its selected source cell.
Representative stills and frames decoded from the final MP4 are inspected for
screen/opening visibility, line continuity, temporal motion, and label spacing.

An independent audit compared selected-cell fields against separately
propagated weighted impulses; maximum complex discrepancy was 3.56e-16.
Every selected cell transmitted, and every contribution stopped at the next
chosen plane. The 8.5, 33, 41, and 48 second states contained respectively
1, 9, 45, and 45 selected cell contributions. Contour extraction recovered
the expected twenty positive plane-wave fronts at four clock phases, with
maximum interpolation phase error 6.25e-5 radians (far below one pixel).

The finished MP4 is H.264 High, yuv420p, 1280 x 720 at 24 fps: 1,248 frames,
exactly 52.0 seconds, and 29,514,654 bytes. A full decode reported no errors.
All 104 encoded frames sampled at exact half-second intervals were inspected,
together with full-size encoded stills and 48 adjacent-frame samples across
the 28, 34, 38, and 46 second handoffs. The blue construction fades smoothly
when local slabs change, and persists through final recovery. Gold fronts
continue without an annotation-induced discontinuity; labels and frame edges
remain clear. Frames at exactly 34 and 38 seconds were also verified to be
pixel-identical with the blue-component layer disabled. The renderer passes
Python compilation.
