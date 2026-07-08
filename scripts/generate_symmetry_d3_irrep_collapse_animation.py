from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from _make_contact_sheets import make_contact_sheet
from symmetry_d3_rendering import (
    AXIS,
    RUST,
    TEAL,
    PURPLE,
    Projection,
    Renderer,
    Vec3,
    add,
    ease,
    mix2,
    mul,
    orbit,
    rotate_about_axis,
    state_vector,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_d3_irrep_collapse_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1200
HEIGHT = 720
SCALE = 2
FPS = 24

START_ORIGIN = (410.0, 420.0)
END_ORIGIN = (WIDTH / 2, HEIGHT / 2 - 8.0)
START_SCALE = 136.0
END_SCALE = 190.0
PHASE = 45.0


@dataclass(frozen=True)
class Sample:
    height: float
    radius: float
    color: tuple[int, int, int]


SAMPLES = [
    Sample(1.96, 1.06, TEAL),
    Sample(1.38, 0.78, RUST),
    Sample(0.86, 0.54, PURPLE),
]


def sample_state(sample: Sample, collapse: float = 0.0) -> Vec3:
    return state_vector(sample.height, sample.radius, PHASE, collapse)


def projection(camera_blend: float) -> Projection:
    t = ease(camera_blend)
    origin = mix2(START_ORIGIN, END_ORIGIN, t)
    scale = START_SCALE * (1.0 - t) + END_SCALE * t
    return Projection.from_blend(origin, scale, camera_blend)


def reveal_tuple(active_index: int | None = None, active_value: float = 0.0, completed: int = 0) -> tuple[float, float, float]:
    values = [1.0 if index < completed else 0.0 for index in range(len(SAMPLES))]
    if active_index is not None:
        values[active_index] = active_value
    return (values[0], values[1], values[2])


def angle_tuple(active_index: int | None = None, active_angle: float = 0.0) -> tuple[float, float, float]:
    values = [0.0, 0.0, 0.0]
    if active_index is not None:
        values[active_index] = active_angle
    return (values[0], values[1], values[2])


def draw_orbits(
    renderer: Renderer,
    proj: Projection,
    reveals: tuple[float, float, float],
    collapse: float,
    fill_alpha: float,
    width: float,
    orbit_alpha: float,
) -> None:
    entries = []
    for index, sample in enumerate(SAMPLES):
        reveal = max(0.0, min(1.0, reveals[index]))
        if reveal <= 0.0:
            continue
        points = orbit(sample_state(sample, collapse))
        entries.append((sample.radius, sample, points, reveal))

    for _radius, sample, points, reveal in sorted(entries, key=lambda item: item[0], reverse=True):
        renderer.orbit_trace(
            points,
            proj,
            sample.color,
            alpha=orbit_alpha,
            progress=reveal,
            width=width,
            dots=True,
            fill_alpha=fill_alpha * ease(max(0.0, reveal - 0.72) / 0.28),
        )


def draw_vectors(
    renderer: Renderer,
    proj: Projection,
    reveals: tuple[float, float, float],
    angles: tuple[float, float, float],
    collapse: float,
    alpha: float,
) -> None:
    if alpha <= 0.0:
        return
    vectors = []
    for index, sample in enumerate(SAMPLES):
        reveal = max(0.0, min(1.0, reveals[index]))
        if reveal <= 0.0:
            continue
        point = rotate_about_axis(sample_state(sample, collapse), angles[index])
        vectors.append((proj.project(point)[2], sample, point, reveal))

    for _depth, sample, point, reveal in sorted(vectors, key=lambda item: item[0]):
        renderer.vector(point, proj, sample.color, alpha * reveal)


def draw_frame(
    reveals: tuple[float, float, float],
    angles: tuple[float, float, float],
    vector_reveals: tuple[float, float, float],
    collapse: float = 0.0,
    camera_blend: float = 0.0,
    axes_alpha: float = 1.0,
    axis_alpha: float = 1.0,
    vector_alpha: float = 1.0,
    plane_alpha: float = 0.0,
    fill_alpha: float = 0.045,
    orbit_width: float = 2.9,
    orbit_alpha: float = 0.68,
) -> Image.Image:
    renderer = Renderer(WIDTH, HEIGHT, SCALE)
    proj = projection(camera_blend)

    if plane_alpha > 0.0:
        renderer.sum_zero_plane(proj, plane_alpha)

    if axes_alpha > 0.0:
        renderer.coordinate_axes(proj, axes_alpha)

    draw_orbits(renderer, proj, reveals, collapse, fill_alpha, orbit_width, orbit_alpha)

    if axis_alpha > 0.0:
        renderer.diagonal_axis(proj, axis_alpha)

    draw_vectors(renderer, proj, vector_reveals, angles, collapse, vector_alpha)

    return renderer.output()


def add_hold(frames: list[Image.Image], count: int, **kwargs: object) -> None:
    for _ in range(count):
        frames.append(draw_frame(**kwargs))


def build_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []

    add_hold(
        frames,
        14,
        reveals=(0.0, 0.0, 0.0),
        angles=(0.0, 0.0, 0.0),
        vector_reveals=(1.0, 0.0, 0.0),
        fill_alpha=0.0,
    )

    for sample_index in range(len(SAMPLES)):
        for turn in range(3):
            for frame_index in range(28):
                t = ease(frame_index / 27)
                angle = 120.0 * (turn + t)
                progress = (turn + t) / 3.0
                frames.append(
                    draw_frame(
                        reveals=reveal_tuple(sample_index, progress, sample_index),
                        angles=angle_tuple(sample_index, angle),
                        vector_reveals=reveal_tuple(sample_index, 1.0, sample_index),
                        fill_alpha=0.035,
                    )
                )
            add_hold(
                frames,
                6,
                reveals=reveal_tuple(sample_index, (turn + 1) / 3.0, sample_index),
                angles=angle_tuple(sample_index, 120.0 * (turn + 1)),
                vector_reveals=reveal_tuple(sample_index, 1.0, sample_index),
                fill_alpha=0.035,
            )

        add_hold(
            frames,
            10,
            reveals=reveal_tuple(sample_index, 1.0, sample_index),
            angles=angle_tuple(sample_index, 360.0),
            vector_reveals=reveal_tuple(sample_index, 0.45, sample_index),
            vector_alpha=0.8,
            fill_alpha=0.05,
        )

    for frame_index in range(28):
        t = ease(frame_index / 27)
        frames.append(
            draw_frame(
                reveals=(1.0, 1.0, 1.0),
                angles=(0.0, 0.0, 0.0),
                vector_reveals=(0.45, 0.45, 0.45),
                vector_alpha=1.0 - t,
                fill_alpha=0.055,
                orbit_width=3.1,
            )
        )

    add_hold(
        frames,
        24,
        reveals=(1.0, 1.0, 1.0),
        angles=(0.0, 0.0, 0.0),
        vector_reveals=(0.0, 0.0, 0.0),
        vector_alpha=0.0,
        fill_alpha=0.055,
        orbit_width=3.1,
    )

    for frame_index in range(68):
        t = ease(frame_index / 67)
        frames.append(
            draw_frame(
                reveals=(1.0, 1.0, 1.0),
                angles=(0.0, 0.0, 0.0),
                vector_reveals=(0.0, 0.0, 0.0),
                vector_alpha=0.0,
                collapse=t,
                axes_alpha=1.0 - 0.28 * t,
                axis_alpha=1.0 - 0.18 * t,
                fill_alpha=0.055,
                orbit_width=3.1,
            )
        )

    for frame_index in range(62):
        t = ease(frame_index / 61)
        frames.append(
            draw_frame(
                reveals=(1.0, 1.0, 1.0),
                angles=(0.0, 0.0, 0.0),
                vector_reveals=(0.0, 0.0, 0.0),
                vector_alpha=0.0,
                collapse=1.0,
                camera_blend=t,
                axes_alpha=0.72 * (1.0 - t),
                axis_alpha=0.82 * (1.0 - t),
                plane_alpha=0.10 * t,
                fill_alpha=0.045,
                orbit_width=3.3,
                orbit_alpha=0.68 + 0.24 * t,
            )
        )

    add_hold(
        frames,
        38,
        reveals=(1.0, 1.0, 1.0),
        angles=(0.0, 0.0, 0.0),
        vector_reveals=(0.0, 0.0, 0.0),
        vector_alpha=0.0,
        collapse=1.0,
        camera_blend=1.0,
        axes_alpha=0.0,
        axis_alpha=0.0,
        plane_alpha=0.10,
        fill_alpha=0.045,
        orbit_width=3.3,
        orbit_alpha=0.92,
    )

    return frames


def encode(frames: list[Image.Image]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    try:
        for index, image in enumerate(frames):
            image.save(SCRATCH / f"frame_{index:04d}.png")

        video = OUTPUT_DIR / "symmetry-d3-irrep-collapse.mp4"
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
        for path in contact_scratch.glob("symmetry-d3-irrep-collapse-*.png"):
            path.unlink()


def main() -> None:
    video, sheet = encode(build_frames())
    print(video)
    print(sheet)


if __name__ == "__main__":
    main()
