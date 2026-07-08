from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image

from _make_contact_sheets import make_contact_sheet
from symmetry_d3_rendering import (
    AXIS,
    BG,
    INK,
    RUST,
    TEAL,
    Projection,
    Renderer,
    ease,
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

WIDTH = 1200
HEIGHT = 700
SCALE = 2
FPS = 24

LEFT_ORIGIN = (320.0, 405.0)
RIGHT_ORIGIN = (920.0, 405.0)
PANEL_SCALE = 128.0
ROT_STATE = state_vector(1.34, 1.04, 45.0)
FLIP_STATE = state_vector(1.34, 1.04, 125.0)


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
    renderer.coordinate_axes(projection, 1.0)
    renderer.diagonal_axis(projection, 1.0)
    renderer.orbit_trace(orbit(ROT_STATE), projection, RUST, 0.88, progress=trace, width=2.8)
    renderer.vector(rotate_about_axis(ROT_STATE, angle), projection, TEAL, 1.0)


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
    renderer.coordinate_axes(projection, 1.0)
    renderer.reflection_plane(projection, 0.28)
    renderer.diagonal_axis(projection, 1.0)
    draw_flip_trace(renderer, projection, progress, global_progress)


def draw_frame(angle: float, trace: float, index: int, total: int) -> Image.Image:
    renderer = Renderer(WIDTH, HEIGHT, SCALE)
    renderer.line([(WIDTH / 2, 46.0), (WIDTH / 2, HEIGHT - 42.0)], (235, 235, 235), 1.2, 1.0)
    renderer.text("rotations", (WIDTH * 0.25, 52.0), 24, INK, 0.92, bold=True)
    renderer.text("flips", (WIDTH * 0.75, 52.0), 24, INK, 0.92, bold=True)

    draw_rotation_panel(renderer, angle, trace)

    global_progress = index / max(1, total - 1)
    flip_progress = global_progress * 2.0 if global_progress <= 0.5 else (1.0 - global_progress) * 2.0
    draw_flip_panel(renderer, flip_progress, global_progress)

    return renderer.output()


def build_frames() -> list[Image.Image]:
    timeline = rotation_timeline()
    total = len(timeline)
    return [draw_frame(angle, trace, index, total) for index, (angle, trace) in enumerate(timeline)]


def encode(frames: list[Image.Image]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
        sheet = make_contact_sheet(video.name)
        return video, sheet
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)
        contact_scratch = OUTPUT_DIR / "_contact_sheet_frames"
        for path in contact_scratch.glob("symmetry-d3-rotations-vs-flips-*.png"):
            path.unlink()


def main() -> None:
    video, sheet = encode(build_frames())
    print(video)
    print(sheet)


if __name__ == "__main__":
    main()
