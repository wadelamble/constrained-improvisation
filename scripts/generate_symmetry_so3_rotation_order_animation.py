from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from symmetry_d3_rendering import (
    BG,
    COORD,
    INK,
    RUST,
    TEAL,
    Projection,
    Renderer,
    ease,
    mul,
    normalize,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_so3_rotation_order_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1200
HEIGHT = 700
SCALE = 2
FPS = 24
FRAMES = 192

LEFT_ORIGIN = (315.0, 408.0)
RIGHT_ORIGIN = (885.0, 408.0)
PANEL_SCALE = 128.0

BLUE = (44, 103, 142)
GOLD = (190, 130, 38)
GREEN = (57, 126, 95)
MUTED = (112, 112, 112)
FAINT = (224, 224, 224)

SPHERE_RADIUS = 1.22
MARKER_DIRECTION = (0.0, 0.0, 1.0)
MARKER_POINT = mul(SPHERE_RADIUS, MARKER_DIRECTION)


def rotate_x(v: tuple[float, float, float], degrees: float) -> tuple[float, float, float]:
    theta = math.radians(degrees)
    c = math.cos(theta)
    s = math.sin(theta)
    return (v[0], c * v[1] - s * v[2], s * v[1] + c * v[2])


def rotate_y(v: tuple[float, float, float], degrees: float) -> tuple[float, float, float]:
    theta = math.radians(degrees)
    c = math.cos(theta)
    s = math.sin(theta)
    return (c * v[0] + s * v[2], v[1], -s * v[0] + c * v[2])


def transform(v: tuple[float, float, float], order: str, first_angle: float, second_angle: float) -> tuple[float, float, float]:
    if order == "xy":
        return rotate_y(rotate_x(v, first_angle), second_angle)
    return rotate_x(rotate_y(v, first_angle), second_angle)


def timeline(frame: int) -> tuple[float, float, int]:
    u = frame / (FRAMES - 1)
    if u < 0.10:
        return 0.0, 0.0, 0
    if u < 0.38:
        return 90.0 * ease((u - 0.10) / 0.28), 0.0, 1
    if u < 0.48:
        return 90.0, 0.0, 1
    if u < 0.76:
        return 90.0, 90.0 * ease((u - 0.48) / 0.28), 2
    return 90.0, 90.0, 3


def projected(projection: Projection, point: tuple[float, float, float]) -> tuple[float, float]:
    p = projection.project(point)
    return (p[0], p[1])


def draw_axes(renderer: Renderer, projection: Projection, active_axis: str | None) -> None:
    axes = {
        "x": ((1.0, 0.0, 0.0), RUST),
        "y": ((0.0, 1.0, 0.0), GOLD),
        "z": ((0.0, 0.0, 1.0), BLUE),
    }
    for label, (axis, color) in axes.items():
        is_active = label == active_axis
        renderer.arrow(
            mul(-0.18, axis),
            mul(2.15, axis),
            projection,
            color if is_active else COORD,
            3.6 if is_active else 1.8,
            1.0 if is_active else 0.78,
            head=13.0 if is_active else 9.0,
        )
        endpoint = projection.project(mul(2.30, axis))
        renderer.text(label, (endpoint[0], endpoint[1]), 16, color if is_active else MUTED, 1.0, bold=is_active)


def draw_sphere_disc(renderer: Renderer, projection: Projection) -> None:
    center = projection.project((0.0, 0.0, 0.0))
    radius = SPHERE_RADIUS * projection.scale
    box = (
        round((center[0] - radius) * renderer.scale),
        round((center[1] - radius) * renderer.scale),
        round((center[0] + radius) * renderer.scale),
        round((center[1] + radius) * renderer.scale),
    )
    renderer.draw.ellipse(
        box,
        fill=renderer.blend((241, 247, 249), 0.82),
        outline=renderer.blend((134, 164, 174), 0.72),
        width=max(1, round(2.0 * renderer.scale)),
    )


def draw_surface_curve(
    renderer: Renderer,
    projection: Projection,
    points: list[tuple[float, float, float]],
    color: tuple[int, int, int] = (132, 157, 166),
    width: float = 1.15,
    front_alpha: float = 0.52,
    back_alpha: float = 0.12,
) -> None:
    for index in range(len(points) - 1):
        p0 = projection.project(points[index])
        p1 = projection.project(points[index + 1])
        alpha = front_alpha if (p0[2] + p1[2]) * 0.5 >= 0.0 else back_alpha
        renderer.line([(p0[0], p0[1]), (p1[0], p1[1])], color, width, alpha)


def draw_sphere_grid(
    renderer: Renderer,
    projection: Projection,
    order: str,
    first_angle: float,
    second_angle: float,
) -> None:
    # Latitude/longitude lines are fixed to the sphere and therefore reveal its rotation.
    for latitude_degrees in (-50.0, -25.0, 0.0, 25.0, 50.0):
        latitude = math.radians(latitude_degrees)
        points: list[tuple[float, float, float]] = []
        for index in range(97):
            longitude = 2.0 * math.pi * index / 96
            body_point = (
                SPHERE_RADIUS * math.cos(latitude) * math.cos(longitude),
                SPHERE_RADIUS * math.cos(latitude) * math.sin(longitude),
                SPHERE_RADIUS * math.sin(latitude),
            )
            points.append(transform(body_point, order, first_angle, second_angle))
        draw_surface_curve(renderer, projection, points)

    for longitude_degrees in (0.0, 45.0, 90.0, 135.0):
        longitude = math.radians(longitude_degrees)
        points = []
        for index in range(97):
            latitude = -math.pi / 2 + math.pi * index / 96
            body_point = (
                SPHERE_RADIUS * math.cos(latitude) * math.cos(longitude),
                SPHERE_RADIUS * math.cos(latitude) * math.sin(longitude),
                SPHERE_RADIUS * math.sin(latitude),
            )
            points.append(transform(body_point, order, first_angle, second_angle))
        draw_surface_curve(renderer, projection, points)

    # One distinguished body-fixed meridian makes a quarter turn easy to track.
    points = []
    longitude = math.radians(-45.0)
    for index in range(97):
        latitude = -math.pi / 2 + math.pi * index / 96
        body_point = (
            SPHERE_RADIUS * math.cos(latitude) * math.cos(longitude),
            SPHERE_RADIUS * math.cos(latitude) * math.sin(longitude),
            SPHERE_RADIUS * math.sin(latitude),
        )
        points.append(transform(body_point, order, first_angle, second_angle))
    draw_surface_curve(renderer, projection, points, BLUE, 1.7, 0.66, 0.10)


def draw_rotation_arc(renderer: Renderer, projection: Projection, axis: str, progress_degrees: float) -> None:
    if progress_degrees <= 0.0:
        return
    radius = 0.48
    points: list[tuple[float, float]] = []
    for index in range(32):
        angle = progress_degrees * index / 31
        if axis == "x":
            point = rotate_x((0.0, 0.0, radius), angle)
            color = RUST
        else:
            point = rotate_y((0.0, 0.0, radius), angle)
            color = GOLD
        points.append(projected(projection, point))
    renderer.line(points, color, 3.0, 0.82)


def draw_marker(renderer: Renderer, projection: Projection, order: str, first_angle: float, second_angle: float, alpha: float = 1.0) -> None:
    base = transform(MARKER_POINT, order, first_angle, second_angle)
    base_2d = projection.project(base)
    renderer.circle((base_2d[0], base_2d[1]), 8.0, TEAL, alpha)


def trace_points(order: str, first_angle: float, second_angle: float) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    first: list[tuple[float, float, float]] = []
    second: list[tuple[float, float, float]] = []
    if first_angle > 0.0:
        for index in range(42):
            angle = first_angle * index / 41
            first.append(transform(MARKER_POINT, order, angle, 0.0))
    if second_angle > 0.0:
        for index in range(42):
            angle = second_angle * index / 41
            second.append(transform(MARKER_POINT, order, 90.0, angle))
    return first, second


def draw_trace(renderer: Renderer, projection: Projection, order: str, first_angle: float, second_angle: float) -> None:
    first, second = trace_points(order, first_angle, second_angle)
    if len(first) > 1:
        renderer.line([projected(projection, point) for point in first], RUST, 2.5, 0.55)
    if len(second) > 1:
        renderer.line([projected(projection, point) for point in second], GOLD, 2.5, 0.66)


def active_axis(order: str, stage: int) -> str | None:
    if stage == 0 or stage == 3:
        return None
    if order == "xy":
        return "x" if stage == 1 else "y"
    return "y" if stage == 1 else "x"


def draw_panel(
    renderer: Renderer,
    origin: tuple[float, float],
    order: str,
    first_angle: float,
    second_angle: float,
    stage: int,
) -> None:
    projection = Projection.from_view(origin, PANEL_SCALE)
    draw_sphere_disc(renderer, projection)
    draw_sphere_grid(renderer, projection, order, first_angle, second_angle)
    draw_axes(renderer, projection, active_axis(order, stage))

    # The common initial surface point remains as a faint reference after motion begins.
    if first_angle > 0.1:
        draw_marker(renderer, projection, order, 0.0, 0.0, 0.18)

    draw_trace(renderer, projection, order, first_angle, second_angle)
    draw_marker(renderer, projection, order, first_angle, second_angle)

    if stage == 1:
        axis = "x" if order == "xy" else "y"
        draw_rotation_arc(renderer, projection, axis, first_angle)
    elif stage == 2:
        axis = "y" if order == "xy" else "x"
        draw_rotation_arc(renderer, projection, axis, second_angle)


def draw_frame(frame: int) -> Image.Image:
    first_angle, second_angle, stage = timeline(frame)
    renderer = Renderer(WIDTH, HEIGHT, SCALE)

    renderer.text("Rotations in three dimensions do not commute", (WIDTH / 2, 38.0), 27, INK, 0.96, bold=True)
    renderer.line([(WIDTH / 2, 70.0), (WIDTH / 2, HEIGHT - 70.0)], FAINT, 1.3, 1.0)

    renderer.text("x first, then y", (WIDTH * 0.25, 78.0), 22, INK, 0.94, bold=True)
    renderer.text("y first, then x", (WIDTH * 0.75, 78.0), 22, INK, 0.94, bold=True)
    renderer.text("Rᵧ Rₓ f₀", (WIDTH * 0.25, 111.0), 18, MUTED, 0.96)
    renderer.text("Rₓ Rᵧ f₀", (WIDTH * 0.75, 111.0), 18, MUTED, 0.96)

    draw_panel(renderer, LEFT_ORIGIN, "xy", first_angle, second_angle, stage)
    draw_panel(renderer, RIGHT_ORIGIN, "yx", first_angle, second_angle, stage)

    if stage == 0:
        status_left = status_right = "start:  f₀ = (0, 0, 1)"
        color_left = color_right = MUTED
    elif stage == 1:
        status_left = "first rotation:  Rₓ(90°)"
        status_right = "first rotation:  Rᵧ(90°)"
        color_left = color_right = RUST
    elif stage == 2:
        status_left = "second rotation:  Rᵧ(90°)"
        status_right = "second rotation:  Rₓ(90°)"
        color_left = color_right = GOLD
    else:
        status_left = "final:  (0, −1, 0)"
        status_right = "final:  (1, 0, 0)"
        color_left = color_right = GREEN

    renderer.text(status_left, (WIDTH * 0.25, 606.0), 17, color_left, 1.0, bold=stage == 3)
    renderer.text(status_right, (WIDTH * 0.75, 606.0), 17, color_right, 1.0, bold=stage == 3)

    footer_alpha = ease((frame / (FRAMES - 1) - 0.76) / 0.12)
    renderer.text("RᵧRₓ f₀  ≠  RₓRᵧ f₀", (WIDTH / 2, 661.0), 22, INK, footer_alpha, bold=True)
    return renderer.output()


def make_contact_sheet(video_stem: str) -> Path:
    samples = [0, 38, 72, 108, 145, 191]
    thumb_w = 400
    thumb_h = 233
    label_h = 25
    margin = 16
    cols = 3
    rows = 2
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text((x + 6, y + thumb_h + 5), f"frame {frame:03d}", fill=MUTED)
    output = OUTPUT_DIR / f"{video_stem}-contact-sheet.png"
    sheet.save(output)
    return output


def render() -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video_stem = "symmetry-so3-rotation-order"
    video = OUTPUT_DIR / f"{video_stem}.mp4"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(SCRATCH / f"frame_{index:04d}.png")
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
                "-crf",
                "18",
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
        return video, make_contact_sheet(video_stem)
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


def main() -> None:
    for path in render():
        print(path)


if __name__ == "__main__":
    main()
