from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_d3_r2_sa_equals_sc_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 960
HEIGHT = 620
SCALE = 2
FPS = 24

BG = (255, 255, 255)
INK = (12, 12, 12)
REFERENCE = (226, 226, 226)
AXIS_A = (85, 85, 85)
AXIS_C = (160, 160, 160)
LABEL_COLORS = {
    "A": (30, 105, 125),
    "B": (176, 83, 52),
    "C": (88, 88, 150),
}

CENTER = (480.0, 260.0)
RADIUS = 170.0
ORDER = ["A", "B", "C"]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_LABEL = font(34, True)
FONT_TEXT = font(28, True)


Vec2 = tuple[float, float]


BASE: dict[str, Vec2] = {
    "A": (0.0, RADIUS),
    "B": (-RADIUS * math.cos(math.radians(30)), -RADIUS * 0.5),
    "C": (RADIUS * math.cos(math.radians(30)), -RADIUS * 0.5),
}


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def screen(point: Vec2) -> Vec2:
    return (CENTER[0] + point[0], CENTER[1] - point[1])


def rotate(point: Vec2, degrees: float) -> Vec2:
    theta = math.radians(degrees)
    x, y = point
    return (
        math.cos(theta) * x - math.sin(theta) * y,
        math.sin(theta) * x + math.cos(theta) * y,
    )


def reflect_about_a_axis(point: Vec2, progress: float) -> Vec2:
    x, y = point
    return (x * math.cos(math.pi * ease(progress)), y)


def reflect_about_axis(point: Vec2, axis_angle_degrees: float) -> Vec2:
    theta = math.radians(axis_angle_degrees)
    ux = math.cos(theta)
    uy = math.sin(theta)
    along = point[0] * ux + point[1] * uy
    parallel = (along * ux, along * uy)
    perpendicular = (point[0] - parallel[0], point[1] - parallel[1])
    return (parallel[0] - perpendicular[0], parallel[1] - perpendicular[1])


def positions_after_r(degrees: float) -> dict[str, Vec2]:
    return {label: rotate(point, degrees) for label, point in BASE.items()}


def positions_after_r2_then_sa(progress: float) -> dict[str, Vec2]:
    r2 = positions_after_r(240.0)
    return {label: reflect_about_a_axis(point, progress) for label, point in r2.items()}


def positions_after_sc() -> dict[str, Vec2]:
    axis_angle = math.atan2(BASE["C"][1], BASE["C"][0])
    return {label: reflect_about_axis(point, math.degrees(axis_angle)) for label, point in BASE.items()}


def text_size(draw: ImageDraw.ImageDraw, text: str, chosen_font: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=chosen_font)
    return (box[2] - box[0], box[3] - box[1])


def draw_centered_text(draw: ImageDraw.ImageDraw, text: str, y: float, alpha: float = 1.0) -> None:
    if not text or alpha <= 0.0:
        return
    w, _h = text_size(draw, text, FONT_TEXT)
    color = blend(INK, alpha)
    draw.text(((WIDTH * SCALE - w * SCALE) / 2, y * SCALE), text, fill=color, font=scaled_font(FONT_TEXT))


def blend(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int]:
    alpha = max(0.0, min(1.0, alpha))
    return (
        round(BG[0] * (1.0 - alpha) + color[0] * alpha),
        round(BG[1] * (1.0 - alpha) + color[1] * alpha),
        round(BG[2] * (1.0 - alpha) + color[2] * alpha),
    )


def scaled_font(base_font: ImageFont.ImageFont) -> ImageFont.ImageFont:
    # The chosen font objects are already raster fonts; recreate TrueType at scale
    # for sharper downsampling when possible.
    size = getattr(base_font, "size", 28)
    return font(size * SCALE, True)


def draw_line(
    draw: ImageDraw.ImageDraw,
    points: list[Vec2],
    color: tuple[int, int, int],
    width: float,
    alpha: float = 1.0,
    joint: str | None = "curve",
) -> None:
    if alpha <= 0.0:
        return
    draw.line(
        [(round(x * SCALE), round(y * SCALE)) for x, y in points],
        fill=blend(color, alpha),
        width=max(1, round(width * SCALE)),
        joint=joint,
    )


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    p0: Vec2,
    p1: Vec2,
    color: tuple[int, int, int],
    width: float,
    alpha: float,
    dash: float = 16.0,
    gap: float = 10.0,
) -> None:
    if alpha <= 0.0:
        return
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    length = math.hypot(dx, dy)
    if length <= 0:
        return
    ux = dx / length
    uy = dy / length
    distance = 0.0
    while distance < length:
        segment_end = min(distance + dash, length)
        start = (p0[0] + ux * distance, p0[1] + uy * distance)
        end = (p0[0] + ux * segment_end, p0[1] + uy * segment_end)
        draw_line(draw, [start, end], color, width, alpha, joint=None)
        distance += dash + gap


def draw_triangle(
    draw: ImageDraw.ImageDraw,
    positions: dict[str, Vec2],
    color: tuple[int, int, int],
    width: float,
    alpha: float = 1.0,
) -> None:
    points = [screen(positions[label]) for label in ORDER]
    draw_line(draw, points + [points[0]], color, width, alpha)


def draw_labels(draw: ImageDraw.ImageDraw, positions: dict[str, Vec2], alpha: float = 1.0) -> None:
    for label in ORDER:
        point = positions[label]
        size = math.hypot(point[0], point[1])
        offset = (point[0] / size * 30.0, point[1] / size * 30.0)
        sx, sy = screen((point[0] + offset[0], point[1] + offset[1]))
        chosen_font = scaled_font(FONT_LABEL)
        w, h = text_size(draw, label, chosen_font)
        draw.text(
            (sx * SCALE - w / 2, sy * SCALE - h / 2),
            label,
            fill=blend(LABEL_COLORS[label], alpha),
            font=chosen_font,
        )


def draw_axis_through_vertex(
    draw: ImageDraw.ImageDraw,
    vertex_label: str,
    color: tuple[int, int, int],
    alpha: float,
    width: float = 2.0,
) -> None:
    direction = BASE[vertex_label]
    size = math.hypot(direction[0], direction[1])
    unit = (direction[0] / size, direction[1] / size)
    p0 = screen((-unit[0] * 245.0, -unit[1] * 245.0))
    p1 = screen((unit[0] * 245.0, unit[1] * 245.0))
    draw_dashed_line(draw, p0, p1, color, width, alpha)


def draw_direct_sc_overlay(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0.0:
        return
    direct = positions_after_sc()
    draw_triangle(draw, direct, AXIS_C, 2.0, alpha * 0.7)
    draw_labels(draw, direct, alpha * 0.7)


def draw_frame(
    positions: dict[str, Vec2],
    text: str,
    axis_a_alpha: float = 0.0,
    axis_c_alpha: float = 0.0,
    direct_sc_alpha: float = 0.0,
) -> Image.Image:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)

    draw_triangle(draw, BASE, REFERENCE, 2.0, 1.0)
    if axis_a_alpha > 0.0:
        draw_axis_through_vertex(draw, "A", AXIS_A, axis_a_alpha)
    if axis_c_alpha > 0.0:
        draw_axis_through_vertex(draw, "C", AXIS_C, axis_c_alpha)
    draw_direct_sc_overlay(draw, direct_sc_alpha)

    draw_triangle(draw, positions, INK, 4.0, 1.0)
    draw_labels(draw, positions, 1.0)
    draw_centered_text(draw, text, 520.0)

    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def hold(frames: list[Image.Image], count: int, **kwargs: object) -> None:
    for _ in range(count):
        frames.append(draw_frame(**kwargs))


def build_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []
    hold(frames, 18, positions=BASE, text="")

    for index in range(46):
        t = ease(index / 45)
        frames.append(draw_frame(positions_after_r(120.0 * t), "r"))
    hold(frames, 12, positions=positions_after_r(120.0), text="r")

    for index in range(46):
        t = ease(index / 45)
        frames.append(draw_frame(positions_after_r(120.0 + 120.0 * t), "r^2"))
    hold(frames, 16, positions=positions_after_r(240.0), text="r^2")

    for index in range(14):
        t = ease(index / 13)
        frames.append(draw_frame(positions_after_r(240.0), "r^2 then s_A", axis_a_alpha=t))

    for index in range(54):
        t = index / 53
        frames.append(
            draw_frame(
                positions_after_r2_then_sa(t),
                "r^2 then s_A",
                axis_a_alpha=1.0,
            )
        )

    final_positions = positions_after_r2_then_sa(1.0)
    hold(frames, 16, positions=final_positions, text="r^2 then s_A", axis_a_alpha=1.0)

    for index in range(32):
        t = ease(index / 31)
        frames.append(
            draw_frame(
                final_positions,
                "r^2 then s_A = s_C",
                axis_a_alpha=1.0 - 0.55 * t,
                axis_c_alpha=t,
                direct_sc_alpha=t,
            )
        )

    hold(
        frames,
        34,
        positions=final_positions,
        text="r^2 then s_A = s_C",
        axis_a_alpha=0.45,
        axis_c_alpha=1.0,
        direct_sc_alpha=1.0,
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

        video = OUTPUT_DIR / "symmetry-d3-r2-sa-equals-sc.mp4"
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
        for path in contact_scratch.glob("symmetry-d3-r2-sa-equals-sc-*.png"):
            path.unlink()


def main() -> None:
    video, sheet = encode(build_frames())
    print(video)
    print(sheet)


if __name__ == "__main__":
    main()
