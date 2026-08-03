from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_continuous_so2_translation_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 620
SCALE = 2
FPS = 24
FRAMES = 120
END_HOLD = 14
TRANSLATION_SPACINGS = 17

BG = (255, 252, 246)
PANEL = (249, 245, 237)
PANEL_EDGE = (223, 214, 201)
INK = (35, 36, 38)
MUTED = (184, 177, 166)
ACCENT = (193, 88, 55)
BLUE = (56, 105, 163)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "seguisb.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size * SCALE)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = font(22, True)
LABEL = font(15)
SMALL = font(13)


def s(value: float) -> int:
    return int(round(value * SCALE))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(v) for v in box),
        radius=s(18),
        fill=PANEL,
        outline=PANEL_EDGE,
        width=s(2),
    )


def tick_on_circle(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    angle: float,
    color: tuple[int, int, int],
    width: int,
    length: float,
) -> None:
    ux = math.cos(angle)
    uy = math.sin(angle)
    x1 = center[0] + (radius - length / 2) * ux
    y1 = center[1] + (radius - length / 2) * uy
    x2 = center[0] + (radius + length / 2) * ux
    y2 = center[1] + (radius + length / 2) * uy
    draw.line((s(x1), s(y1), s(x2), s(y2)), fill=color, width=s(width))


def draw_rotation_panel(draw: ImageDraw.ImageDraw, phase: float) -> None:
    left = (46, 54, 616, 566)
    draw_panel(draw, left)
    draw_text(draw, (86, 84), "SO(2): rotation", font_obj=TITLE)

    cx, cy = 331.0, 320.0
    radius = 150.0
    draw.ellipse(
        (s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)),
        outline=(87, 93, 99),
        width=s(4),
    )

    tick_count = 11
    tick_length = 34.0
    angle = 2 * math.pi * phase
    for index in range(tick_count):
        base = 2 * math.pi * index / tick_count
        tick_on_circle(draw, (cx, cy), radius, base, MUTED, 4, tick_length)
    for index in range(tick_count):
        base = 2 * math.pi * index / tick_count
        tick_on_circle(draw, (cx, cy), radius, base + angle, ACCENT, 4, tick_length)

    arc_radius = radius + 44
    start = -88
    end = start + 315 * phase
    if phase > 0.02:
        draw.arc(
            (s(cx - arc_radius), s(cy - arc_radius), s(cx + arc_radius), s(cy + arc_radius)),
            start=start,
            end=end,
            fill=ACCENT,
            width=s(3),
        )
        arrow_angle = math.radians(end)
        ax = cx + arc_radius * math.cos(arrow_angle)
        ay = cy + arc_radius * math.sin(arrow_angle)
        tangent = arrow_angle + math.pi / 2
        for offset in (-2.55, 2.55):
            bx = ax + 12 * math.cos(tangent + offset)
            by = ay + 12 * math.sin(tangent + offset)
            draw.line((s(ax), s(ay), s(bx), s(by)), fill=ACCENT, width=s(3))


def draw_line_ticks(
    draw: ImageDraw.ImageDraw,
    y: float,
    x_min: float,
    x_max: float,
    spacing: float,
    offset: float,
    color: tuple[int, int, int],
    width: int,
    length: float,
) -> None:
    start = x_min - 3 * spacing + offset
    end = x_max + 3 * spacing
    count = int((end - start) / spacing) + 1
    for index in range(count):
        x = start + index * spacing
        if x_min <= x <= x_max:
            draw.line((s(x), s(y - length / 2), s(x), s(y + length / 2)), fill=color, width=s(width))


def draw_translation_panel(draw: ImageDraw.ImageDraw, phase: float) -> None:
    right = (664, 54, 1234, 566)
    draw_panel(draw, right)
    draw_text(draw, (704, 84), "(R,+): translation", font_obj=TITLE)

    y = 322.0
    line_x1 = 665.0
    line_x2 = 1233.0
    x_min = line_x1 + 26.0
    x_max = line_x2 - 26.0
    draw.line((s(line_x1), s(y), s(line_x2), s(y)), fill=(87, 93, 99), width=s(4))
    # Small edge arrows suggest the line continues beyond the pane.
    draw.polygon([(s(line_x1), s(y)), (s(line_x1 + 16), s(y - 8)), (s(line_x1 + 16), s(y + 8))], fill=(87, 93, 99))
    draw.polygon([(s(line_x2), s(y)), (s(line_x2 - 16), s(y - 8)), (s(line_x2 - 16), s(y + 8))], fill=(87, 93, 99))

    spacing = 54.0
    offset = (phase * TRANSLATION_SPACINGS * spacing) % spacing
    draw_line_ticks(draw, y, x_min, x_max, spacing, 0.0, MUTED, 4, 46.0)
    draw_line_ticks(draw, y, x_min, x_max, spacing, offset, BLUE, 4, 46.0)


def draw_frame(frame_index: int) -> Image.Image:
    moving_frames = FRAMES - END_HOLD
    if frame_index >= moving_frames:
        phase = 1.0
    else:
        phase = frame_index / (moving_frames - 1)
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    draw_rotation_panel(draw, phase)
    draw_translation_panel(draw, phase)
    image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video = OUTPUT_DIR / "symmetry-continuous-so2-translation.mp4"

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
        print(video)
        print(make_contact_sheet(video.name))
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


if __name__ == "__main__":
    main()
