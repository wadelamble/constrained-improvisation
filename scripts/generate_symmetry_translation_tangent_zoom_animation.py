from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 168

BG = (255, 252, 246)
PANEL = (250, 246, 238)
PANEL_EDGE = (224, 216, 204)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (196, 132, 42)
GREEN = (71, 130, 101)


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


TITLE = font(25, True)
LABEL = font(18)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 4,
    head: float = 14,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def f(x: float) -> float:
    return 0.48 + 0.20 * x + 0.22 * x * x - 0.035 * x * x * x


def fp(x: float) -> float:
    return 0.20 + 0.44 * x - 0.105 * x * x


def tangent(x: float, x0: float) -> float:
    return f(x0) + fp(x0) * (x - x0)


def make_mapper(x_min: float, x_max: float, y_min: float, y_max: float):
    left, top, right, bottom = 92, 106, 914, 610

    def to_screen(x: float, y: float) -> tuple[float, float]:
        px = left + (x - x_min) / (x_max - x_min) * (right - left)
        py = bottom - (y - y_min) / (y_max - y_min) * (bottom - top)
        return px, py

    return to_screen


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    t = frame / (FRAMES - 1)
    zoom = ease((t - 0.22) / 0.70)
    span = lerp(4.8, 0.72, zoom)
    x0 = 0.0
    x_min = x0 - 0.52 * span
    x_max = x0 + 0.48 * span
    y_center = f(x0)
    y_span = lerp(2.50, 0.46, zoom)
    y_min = y_center - 0.43 * y_span
    y_max = y_center + 0.57 * y_span
    to_screen = make_mapper(x_min, x_max, y_min, y_max)

    draw_text(draw, (58, 42), "A tangent is a local copy of the function", font_obj=TITLE)

    # Axes.
    axis_y = to_screen(0, 0)[1]
    axis_x = to_screen(0, 0)[0]
    draw.line((s(72), s(axis_y), s(934), s(axis_y)), fill=rgba(MUTED, 0.75), width=s(2))
    draw.line((s(axis_x), s(92), s(axis_x), s(630)), fill=rgba(MUTED, 0.45), width=s(2))

    # Function and tangent.
    curve = []
    tan_line = []
    samples = 360
    for i in range(samples):
        x = x_min + (x_max - x_min) * i / (samples - 1)
        curve.append(tuple(s(v) for v in to_screen(x, f(x))))
        tan_line.append(tuple(s(v) for v in to_screen(x, tangent(x, x0))))
    draw.line(tan_line, fill=GOLD, width=s(5))
    draw.line(curve, fill=BLUE, width=s(5))

    # The represented translation shrinks as the view becomes local.
    a = 0.34 * span
    x_shift = x0 - a
    p0 = to_screen(x0, f(x0))
    p_actual = to_screen(x_shift, f(x_shift))
    p_tan = to_screen(x_shift, tangent(x_shift, x0))

    bracket_y = min(598, max(p0[1], p_actual[1], p_tan[1]) + 58)
    draw.line((s(p0[0]), s(p0[1]), s(p0[0]), s(bracket_y)), fill=rgba(BLUE, 0.45), width=s(2))
    draw.line((s(p_actual[0]), s(min(p_actual[1], p_tan[1])), s(p_actual[0]), s(bracket_y)), fill=rgba(RED, 0.45), width=s(2))
    draw.ellipse((s(p0[0] - 7), s(p0[1] - 7), s(p0[0] + 7), s(p0[1] + 7)), fill=BLUE)
    draw.ellipse((s(p_actual[0] - 7), s(p_actual[1] - 7), s(p_actual[0] + 7), s(p_actual[1] + 7)), fill=RED)
    draw.ellipse((s(p_tan[0] - 6), s(p_tan[1] - 6), s(p_tan[0] + 6), s(p_tan[1] + 6)), fill=GOLD)

    if abs(p_tan[1] - p_actual[1]) > 12:
        draw.line((s(p_actual[0]), s(p_actual[1]), s(p_tan[0]), s(p_tan[1])), fill=GREEN, width=s(4))
        draw_text(draw, (p_actual[0] - 16, (p_actual[1] + p_tan[1]) / 2), "error", fill=GREEN, font_obj=SMALL, anchor="rm")

    draw_arrow(draw, (p0[0] - 8, bracket_y - 22), (p_actual[0] + 8, bracket_y - 22), RED, width=3)
    draw_text(draw, ((p0[0] + p_actual[0]) / 2, bracket_y - 50), "a", fill=RED, font_obj=SMALL, anchor="mm")
    draw_text(draw, (p0[0] + 12, p0[1] - 28), "x", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (p_actual[0], bracket_y + 22), "x-a", fill=RED, font_obj=SMALL, anchor="mm")

    # Equation panel.
    draw.rounded_rectangle((s(970), s(170), s(1198), s(392)), radius=s(12), fill=PANEL, outline=PANEL_EDGE, width=s(2))
    draw_text(draw, (994, 202), "near x", font_obj=LABEL)
    draw_text(draw, (994, 252), "f(x-a)", fill=RED, font_obj=LABEL)
    draw_text(draw, (994, 294), "\u2248 f(x) - a f'(x)", fill=INK, font_obj=LABEL)
    draw_text(draw, (994, 348), "zoom makes", fill=(91, 87, 81), font_obj=SMALL)
    draw_text(draw, (994, 374), "near become true", fill=(91, 87, 81), font_obj=SMALL)

    # Small zoom indicator.
    bar_x, bar_y, bar_w = 970, 456, 218
    draw.line((s(bar_x), s(bar_y), s(bar_x + bar_w), s(bar_y)), fill=rgba(MUTED, 0.8), width=s(4))
    knob_x = bar_x + bar_w * zoom
    draw.ellipse((s(knob_x - 8), s(bar_y - 8), s(knob_x + 8), s(bar_y + 8)), fill=BLUE)
    draw_text(draw, (bar_x, bar_y - 32), "local zoom", fill=(91, 87, 81), font_obj=SMALL)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    samples = [0, 28, 56, 84, 112, 140]
    thumb_w = 400
    thumb_h = 225
    label_h = 28
    margin = 18
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
        draw.text((x + 8, y + thumb_h + 6), f"{round(frame / (FRAMES - 1) * 100)}%", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(out)
    return out


def render() -> tuple[Path, Path]:
    name = "symmetry-translation-tangent-zoom"
    scratch = OUTPUT_DIR / f"_{name}_frames"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
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
        contact = make_contact_sheet(name)
        return video, contact
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact = render()
    print(video)
    print(contact)


if __name__ == "__main__":
    main()
