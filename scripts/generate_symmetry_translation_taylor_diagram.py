from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-translation-taylor-slope.png"

WIDTH = 1100
HEIGHT = 560
SCALE = 2

BG = (255, 252, 246, 255)
INK = (35, 36, 38, 255)
MUTED = (174, 168, 158, 210)
FAINT = (226, 219, 209, 255)
BLUE = (57, 103, 157, 255)
RED = (184, 72, 48, 255)
GOLD = (196, 132, 42, 255)
GREEN = (71, 130, 101, 255)


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


TITLE = font(24, True)
LABEL = font(17)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def f(x: float) -> float:
    return 0.56 + 0.20 * math.sin(1.25 * x - 0.35) + 0.13 * math.sin(3.15 * x + 0.1)


def fp(x: float) -> float:
    return 0.20 * 1.25 * math.cos(1.25 * x - 0.35) + 0.13 * 3.15 * math.cos(3.15 * x + 0.1)


def to_screen(x: float, y: float) -> tuple[float, float]:
    x_min, x_max = -3.2, 3.4
    y_min, y_max = 0.02, 1.1
    left, top, right, bottom = 92, 92, 804, 472
    px = left + (x - x_min) / (x_max - x_min) * (right - left)
    py = bottom - (y - y_min) / (y_max - y_min) * (bottom - top)
    return px, py


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int, int],
    width: int = 4,
    head: float = 14,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 40), "A tiny translation is measured by the slope", font_obj=TITLE)

    # Axes.
    x_axis_y = to_screen(0, 0.08)[1]
    y_axis_x = to_screen(0, 0)[0]
    draw.line((s(72), s(x_axis_y), s(835), s(x_axis_y)), fill=MUTED, width=s(2))
    draw.line((s(y_axis_x), s(70), s(y_axis_x), s(492)), fill=(174, 168, 158, 120), width=s(2))
    draw_text(draw, (846, x_axis_y - 8), "x", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (y_axis_x + 10, 70), "f(x)", fill=MUTED, font_obj=SMALL)

    # Curve.
    points = []
    for i in range(320):
        x = -3.1 + 6.3 * i / 319
        points.append(tuple(s(v) for v in to_screen(x, f(x))))
    draw.line(points, fill=BLUE, width=s(5))

    x0 = 0.20
    a = 0.36
    x_left = x0 - a
    y0 = f(x0)
    y_left = f(x_left)
    y_tangent_left = y0 + fp(x0) * (x_left - x0)

    p0 = to_screen(x0, y0)
    p_left = to_screen(x_left, y_left)
    p_tangent_left = to_screen(x_left, y_tangent_left)

    # Tangent line at x.
    slope = fp(x0)
    tangent_points = []
    for i in range(80):
        x = x_left - 0.05 + 0.72 * i / 79
        y = y0 + slope * (x - x0)
        tangent_points.append(tuple(s(v) for v in to_screen(x, y)))
    draw.line(tangent_points, fill=GOLD, width=s(4))

    # Mark the two function values.
    draw.line((s(p0[0]), s(p0[1]), s(p0[0]), s(x_axis_y)), fill=(57, 103, 157, 105), width=s(2))
    draw.line((s(p_left[0]), s(p_left[1]), s(p_left[0]), s(x_axis_y)), fill=(184, 72, 48, 105), width=s(2))
    draw.ellipse((s(p0[0] - 7), s(p0[1] - 7), s(p0[0] + 7), s(p0[1] + 7)), fill=BLUE)
    draw.ellipse((s(p_left[0] - 7), s(p_left[1] - 7), s(p_left[0] + 7), s(p_left[1] + 7)), fill=RED)
    draw.ellipse((s(p_tangent_left[0] - 5), s(p_tangent_left[1] - 5), s(p_tangent_left[0] + 5), s(p_tangent_left[1] + 5)), fill=GOLD)

    draw_text(draw, (p0[0] + 12, p0[1] - 28), "f(x)", fill=BLUE, font_obj=LABEL)
    draw_text(draw, (p_left[0] - 12, p_left[1] - 28), "f(x-a)", fill=RED, font_obj=LABEL, anchor="rm")
    draw_text(draw, (p0[0], x_axis_y + 26), "x", fill=BLUE, font_obj=SMALL, anchor="mm")
    draw_text(draw, (p_left[0], x_axis_y + 26), "x-a", fill=RED, font_obj=SMALL, anchor="mm")

    # Horizontal shift and vertical correction.
    draw_arrow(draw, (p0[0] - 4, x_axis_y - 28), (p_left[0] + 4, x_axis_y - 28), RED, width=3)
    draw_text(draw, ((p0[0] + p_left[0]) / 2, x_axis_y - 58), "shift by a", fill=RED, font_obj=SMALL, anchor="mm")
    draw.line((s(p_left[0]), s(p0[1]), s(p_left[0]), s(p_tangent_left[1])), fill=GREEN, width=s(4))
    draw_text(draw, (p_left[0] - 14, (p0[1] + p_tangent_left[1]) / 2), "tangent estimate", fill=GREEN, font_obj=SMALL, anchor="rm")

    # Equation panel.
    draw.rounded_rectangle((s(850), s(152), s(1042), s(396)), radius=s(12), fill=(250, 246, 238, 255), outline=(224, 216, 204, 255), width=s(2))
    draw_text(draw, (874, 178), "near x:", font_obj=LABEL)
    draw_text(draw, (874, 226), "f(x-a)", fill=RED, font_obj=LABEL)
    draw_text(draw, (874, 268), "\u2248 f(x) - a f'(x)", fill=INK, font_obj=LABEL)
    draw_text(draw, (874, 326), "slope gives the", fill=(91, 87, 81, 255), font_obj=SMALL)
    draw_text(draw, (874, 352), "first correction", fill=(91, 87, 81, 255), font_obj=SMALL)

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
