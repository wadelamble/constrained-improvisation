from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

from symmetry_d3_rendering import (
    AXIS,
    BG,
    INK,
    RUST,
    TEAL,
    U,
    E1,
    E2,
    Projection,
    Renderer,
    add,
    dot,
    ease,
    mul,
    orbit,
    reflect_in_a_plane,
    reflect_progress,
    rotate_about_axis,
    state_vector,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_d3_rotations_vs_flips_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
if not FFMPEG.is_file():
    from imageio_ffmpeg import get_ffmpeg_exe

    FFMPEG = Path(get_ffmpeg_exe())

WIDTH = 1200
HEIGHT = 700
SCALE = 2
FPS = 24

LEFT_ORIGIN = (320.0, 405.0)
RIGHT_ORIGIN = (920.0, 405.0)
PANEL_SCALE = 128.0
ROT_STATE = state_vector(1.34, 1.04, 45.0)
FLIP_STATE = state_vector(1.34, 1.04, 125.0)
SLICE_HEIGHT = dot(U, ROT_STATE)
SLICE_RADIUS = 1.25
SLICE_FILL = (247, 237, 213)
SLICE_EDGE = (181, 151, 90)


def slice_point(a: float, b: float):
    """The invariant affine plane through both illustrated vector tips."""
    return add(mul(SLICE_HEIGHT, U), add(mul(a, E1), mul(b, E2)))


def draw_tip_plane(renderer: Renderer, projection: Projection) -> None:
    r = SLICE_RADIUS
    corners = [slice_point(a, b) for a, b in ((-r, -r), (r, -r), (r, r), (-r, r))]
    projected = [projection.project(p)[:2] for p in corners]
    renderer.polygon(projected, SLICE_FILL, 0.52, SLICE_EDGE, 0.45)
    for value in (-0.8, -0.4, 0.0, 0.4, 0.8):
        for ends in ((slice_point(-r, value), slice_point(r, value)),
                     (slice_point(value, -r), slice_point(value, r))):
            renderer.line([projection.project(p)[:2] for p in ends], SLICE_EDGE, 0.8, 0.22)


def validate_tip_plane() -> None:
    assert abs(dot(U, FLIP_STATE) - SLICE_HEIGHT) < 1e-12
    for angle, _ in rotation_timeline():
        assert abs(dot(U, rotate_about_axis(ROT_STATE, angle)) - SLICE_HEIGHT) < 1e-12
    for i in range(157):
        assert abs(dot(U, reflect_progress(FLIP_STATE, i / 156)) - SLICE_HEIGHT) < 1e-12


def rotation_timeline() -> list[tuple[float, float]]:
    timeline: list[tuple[float, float]] = []
    timeline.extend([(0.0, 0.0)] * 14)

    for step in range(3):
        for index in range(30):
            t = ease(index / 29)
            angle = 120.0 * (step + t)
            trace = (step + t) / 3.0
            timeline.append((angle, trace))
        timeline.extend([(120.0 * (step + 1), (step + 1) / 3.0)] * 8)

    timeline.extend([(360.0, 1.0)] * 28)
    return timeline


def draw_rotation_panel(renderer: Renderer, angle: float, trace: float) -> None:
    projection = Projection.from_view(LEFT_ORIGIN, PANEL_SCALE)
    draw_tip_plane(renderer, projection)
    renderer.coordinate_axes(projection, 1.0)
    renderer.diagonal_axis(projection, 1.0)
    renderer.orbit_trace(orbit(ROT_STATE), projection, RUST, 0.88, progress=trace, width=2.8)
    renderer.vector(rotate_about_axis(ROT_STATE, angle), projection, TEAL, 1.0)
    renderer.component_axis_labels(projection)


def draw_flip_trace(renderer: Renderer, projection: Projection, progress: float, global_progress: float) -> None:
    reflected = reflect_in_a_plane(FLIP_STATE)
    p0 = projection.project(FLIP_STATE)
    p1 = projection.project(reflected)
    trace_alpha = 0.42 + 0.35 * min(1.0, global_progress * 2.0)
    renderer.line([(p0[0], p0[1]), (p1[0], p1[1])], RUST, 2.6, trace_alpha)
    renderer.circle((p0[0], p0[1]), 4.5, RUST, 0.64)
    renderer.circle((p1[0], p1[1]), 4.5, RUST, 0.64)
    renderer.arrow((0.0, 0.0, 0.0), FLIP_STATE, projection, RUST, 1.8, 0.26, head=11.0)

    state = reflect_progress(FLIP_STATE, progress)
    renderer.vector(state, projection, TEAL, 1.0)


def draw_flip_panel(renderer: Renderer, progress: float, global_progress: float) -> None:
    projection = Projection.from_view(RIGHT_ORIGIN, PANEL_SCALE)
    renderer.reflection_plane(projection, 0.20)
    draw_tip_plane(renderer, projection)
    renderer.coordinate_axes(projection, 1.0)
    renderer.diagonal_axis(projection, 1.0)
    draw_flip_trace(renderer, projection, progress, global_progress)
    renderer.component_axis_labels(projection)


def draw_frame(angle: float, trace: float, index: int, total: int) -> Image.Image:
    renderer = Renderer(WIDTH, HEIGHT, SCALE)
    renderer.line([(WIDTH / 2, 46.0), (WIDTH / 2, HEIGHT - 42.0)], (235, 235, 235), 1.2, 1.0)
    renderer.text("rotations", (WIDTH * 0.25, 52.0), 24, INK, 0.92, bold=True)
    renderer.text("flips", (WIDTH * 0.75, 52.0), 24, INK, 0.92, bold=True)
    renderer.equal_components_key((180.0, 112.0))
    renderer.equal_components_key((780.0, 112.0))

    draw_rotation_panel(renderer, angle, trace)

    global_progress = index / max(1, total - 1)
    flip_progress = global_progress * 2.0 if global_progress <= 0.5 else (1.0 - global_progress) * 2.0
    draw_flip_panel(renderer, flip_progress, global_progress)

    return renderer.output()


def build_frames() -> list[Image.Image]:
    validate_tip_plane()
    timeline = rotation_timeline()
    total = len(timeline)
    return [draw_frame(angle, trace, index, total) for index, (angle, trace) in enumerate(timeline)]


def encode(frames: list[Image.Image]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    assert SCRATCH.resolve().parent == OUTPUT_DIR.resolve()
    assert SCRATCH.name == "_symmetry_d3_rotations_vs_flips_frames"
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    try:
        for index, image in enumerate(frames):
            image.save(SCRATCH / f"frame_{index:04d}.png")

        video = OUTPUT_DIR / "symmetry-d3-rotations-vs-flips.mp4"
        subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(SCRATCH / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        poster = OUTPUT_DIR / "symmetry-d3-rotations-vs-flips-poster.png"
        frames[-1].save(poster)
        return video, poster
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


def main() -> None:
    video, poster = encode(build_frames())
    print(video)
    print(poster)


if __name__ == "__main__":
    main()
