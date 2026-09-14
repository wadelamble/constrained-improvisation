# A fixed spectrum links the paths to the ungrouped sum

This standalone variant adds the user's requested physical-position colors
to the normalized, ungrouped two-pane film. It preserves the original movie
and the subsequently rejected grouped experiment.

## Correspondence

Each of the same 20,001 crossing positions receives a fixed color from
`t = 1 - abs(y)/2.8`: blue at both outer edges, then cyan, green, yellow,
orange, and red at the center. The mapping is independent of wavelength,
phase, contribution magnitude, and the current scan prefix. Symmetric paths
receive the same color because they have the same distance from the center.

The exact contribution of path j is drawn in that color between cumulative
vertices j and j+1. All original vertices remain in the tip-to-tail trace.
Adjacent segments with identical 8-bit RGB values share a drawing call;
this is a rendering optimization, not a sum over a region or replacement
of a curved subchain by its chord.

The upper diamond retains the dense painted-path idiom. A pixel is mapped
to the nearest original crossing position of the route passing through it.
The unresolved family is translucent; the current physical route is drawn
at full color, matching the corresponding tip-to-tail segment. A ring of
that color surrounds the current cumulative tip, with the gold total still
ending at its center. The dotted screen and a fixed edge-to-center key show
the same palette. Paint opacity marks scan progress, not physical weight.

This exposes which physical paths produce each part of the trace. In the
shorter-wavelength passes the large sweep becomes increasingly red, while
colors farther from the stationary crossing occupy tight endpoint coils.
The full ungrouped curve is retained; it is not forced into a straight line.

## Preserved mathematics and timing

`generate_symmetry_normalized_path_diamond.py` supplies the unchanged scalar
source and propagation weights, normalized by independent free A-to-B
propagation. Its vectors, cumulative vertices, phase reference, and endpoints
are reused directly. Geometry stays A=(-4.5,0), screen x=0, B=(4.5,0), sampled
screen span [-2.8,2.8]. The model's scope and normalization are documented in
`normalized-path-diamond-wavelength-scan.md`.

The wavelengths remain 0.5, 0.05, and 0.005. The scale stays 620 pixels per
unit of reference amplitude. Each 12-second pass has a 0.8-second prelude,
9.6-second uniform top-to-bottom scan, and 1.6-second final hold. At prefix n,
the highlighted physical path is n-1, the highlighted segment joins vertices
n-1 and n, and the gold subtotal ends at vertex n. There are 2,160 frames at
60 fps, 1440 × 1080, totaling 36 seconds.

## Files and verification

- Generator: `scripts/generate_symmetry_spectrum_path_diamond.py`
- Movie: `content/drafts/animations/symmetry-spectrum-path-diamond-wavelength-scan.mp4`
- Three final stills, source/encoded contact sheets, and two validation JSON
  files use the same movie stem.

Focused checks cover palette symmetry and endpoint colors, full coverage of
the original segments, identical colors within drawing runs, correspondence
between the fan raster and physical paths, and matching path/segment/subtotal
indices at representative scan times. The per-wavelength vector hashes and
unchanged endpoints are recorded. The scalar model was already independently
validated in the normalized version.

Encoded verification decodes all frames, compares representative frames
against the source rendering, and checks active-path color and gold-tip
position. Inspect both the final stills and intermediate contact-sheet frames
to assess the correspondence; final geometry alone does not show scan timing.

```powershell
python -B scripts/generate_symmetry_spectrum_path_diamond.py --check --preview --render --encoded-check
```
