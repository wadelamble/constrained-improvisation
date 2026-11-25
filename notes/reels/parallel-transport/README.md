# Parallel transport reel

A standalone portrait adaptation of the Symmetry chapter's current parallel-transport commutator animation. The desktop original is unchanged.

- Renderer: `scripts/parallel_transport_reel.py`
- Exact geometry and drawing primitives: `scripts/generate_symmetry_parallel_transport_commutator.py` and `scripts/parallel_transport_geometry.py`
- Editable caption: `notes/reels/parallel-transport/reel-text.md`
- Package: `content/reels/parallel-transport/`
- Format: 1080 × 1920, 30 fps, 34 seconds, H.264 video and AAC stereo audio
- Music: the supplied Herbie Hancock *Maiden Voyage (Remastered 2012)* recording, 130–164 seconds, −4 dB, 1.5-second fade-in and 2-second fade-out

With the project animation dependencies available, run:

```powershell
python scripts/parallel_transport_reel.py --preview --render --validate --package --music-source '<supplied FLAC path>'
```

After editing only the caption:

```powershell
python scripts/parallel_transport_reel.py --package
```

Validation checks the transported vectors' norm and tangency, common endpoint, exact tangent-plane subtraction, and convergence to the small-step generator bracket. Text bounds and pairwise text collisions are checked on every rendered frame. The encoded MP4 is fully decoded; duration, frame count, dimensions, audio presence, peak and RMS are checked. The decoded contact sheet and poster are used for visual review.

Blue is x then y, represented by TᵧTₓ. Gold is y then x, represented by TₓTᵧ. Green is gold minus blue. The finite commutator is exact; the generator-bracket expression is explicitly a small-step approximation. Coordinate steps are not presented as physical arc lengths.

The renderer never publishes. Publication receipts are maintained separately.
