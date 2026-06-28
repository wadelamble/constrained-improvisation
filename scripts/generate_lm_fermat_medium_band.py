from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations" / "lm-fermat-medium-band.png"

SCALE = 3
W, H = 1400, 900

BG = "#fbfaf7"
INK = "#2f2f2f"
MUTED = "#6f675e"
PANEL = "#ffffff"
BORDER = "#d6cec1"
BAND = "#dceff5"
BAND_EDGE = "#7fb0c1"
BLUE = "#245e91"
GRAY = "#b7ada0"
ANGLE = "#a65331"


def s(value: float) -> int:
    return int(round(value * SCALE))


def xy(point: tuple[float, float]) -> tuple[int, int]:
    return (s(point[0]), s(point[1]))


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    font_dir = Path("C:/Windows/Fonts")
    candidates = [
        font_dir / name,
        font_dir / "segoeui.ttf",
        font_dir / "arial.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), s(size))
    return ImageFont.load_default()


FONT = load_font("segoeui.ttf", 27)
FONT_SMALL = load_font("segoeui.ttf", 22)
FONT_TINY = load_font("segoeui.ttf", 19)
FONT_BOLD = load_font("segoeuib.ttf", 36)
FONT_LABEL = load_font("segoeuib.ttf", 38)
FONT_EQ = load_font("segoeui.ttf", 35)


def draw_text(
    draw: ImageDraw.ImageDraw,
    point: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str = INK,
    anchor: str | None = None,
) -> None:
    draw.text(xy(point), text, font=font, fill=fill, anchor=anchor)


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    fill: str,
    width: int,
    dash: float = 18,
    gap: float = 13,
) -> None:
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    t = 0.0
    while t < length:
        end = min(t + dash, length)
        a = (x1 + ux * t, y1 + uy * t)
        b = (x1 + ux * end, y1 + uy * end)
        draw.line([xy(a), xy(b)], fill=fill, width=s(width))
        t += dash + gap


def draw_polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: str,
    width: int,
) -> None:
    scaled = [xy(p) for p in points]
    draw.line(scaled, fill=fill, width=s(width), joint="curve")
    r = width / 2
    for p in points[1:-1]:
        draw.ellipse(
            [s(p[0] - r), s(p[1] - r), s(p[0] + r), s(p[1] + r)],
            fill=fill,
        )


def draw_arrowhead(
    draw: ImageDraw.ImageDraw,
    tip: tuple[float, float],
    tail: tuple[float, float],
    fill: str,
    size: float = 34,
) -> None:
    vx, vy = tip[0] - tail[0], tip[1] - tail[1]
    length = math.hypot(vx, vy)
    if length == 0:
        return
    ux, uy = vx / length, vy / length
    px, py = -uy, ux
    base = (tip[0] - ux * size, tip[1] - uy * size)
    left = (base[0] + px * size * 0.43, base[1] + py * size * 0.43)
    right = (base[0] - px * size * 0.43, base[1] - py * size * 0.43)
    draw.polygon([xy(tip), xy(left), xy(right)], fill=fill)


def angle_of(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw_angle_arc(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    start_angle: float,
    end_angle: float,
    radius: float,
    label: str,
    label_radius: float,
) -> None:
    delta = (end_angle - start_angle + math.pi) % (2 * math.pi) - math.pi
    steps = 28
    points = []
    for i in range(steps + 1):
        a = start_angle + delta * i / steps
        points.append((center[0] + radius * math.cos(a), center[1] + radius * math.sin(a)))
    draw.line([xy(p) for p in points], fill=ANGLE, width=s(4), joint="curve")
    mid = start_angle + delta / 2
    draw_text(
        draw,
        (center[0] + label_radius * math.cos(mid), center[1] + label_radius * math.sin(mid)),
        label,
        FONT,
        ANGLE,
        "mm",
    )


def draw_point(
    draw: ImageDraw.ImageDraw,
    p: tuple[float, float],
    label: str,
    label_pos: tuple[float, float],
) -> None:
    r = 16
    draw.ellipse([s(p[0] - r - 3), s(p[1] - r - 3), s(p[0] + r + 3), s(p[1] + r + 3)], fill="#ffffff")
    draw.ellipse([s(p[0] - r), s(p[1] - r), s(p[0] + r), s(p[1] + r)], fill=INK)
    draw_text(draw, label_pos, label, FONT_LABEL, INK, "mm")


def main() -> None:
    img = Image.new("RGB", (s(W), s(H)), BG)
    draw = ImageDraw.Draw(img)

    panel = (100, 115, 1300, 740)
    band_top, band_bottom = 335, 535

    draw.rounded_rectangle([s(panel[0]), s(panel[1]), s(panel[2]), s(panel[3])], radius=s(4), fill=PANEL, outline=BORDER, width=s(2))
    draw.rectangle([s(panel[0]), s(band_top), s(panel[2]), s(band_bottom)], fill=BAND)
    draw.line([(s(panel[0]), s(band_top)), (s(panel[2]), s(band_top))], fill=BAND_EDGE, width=s(4))
    draw.line([(s(panel[0]), s(band_bottom)), (s(panel[2]), s(band_bottom))], fill=BAND_EDGE, width=s(4))

    draw_text(draw, (700, 58), "Fermat path through a slower medium", FONT_BOLD, "#403a34", "mm")
    draw_text(draw, (1135, 205), "outside medium, speed v\u2081", FONT_SMALL, "#4b463f", "mm")
    draw_text(draw, (1025, 435), "slower medium band, speed v\u2082 < v\u2081", FONT_SMALL, "#335766", "mm")
    draw_text(draw, (285, 680), "outside medium, speed v\u2081", FONT_SMALL, "#4b463f", "mm")

    a = (205, 245)
    b = (470, band_top)
    c = (700, band_bottom)
    d = (1060, 655)
    path = [a, b, c, d]

    draw_dashed_line(draw, a, d, GRAY, 4, dash=23, gap=16)
    draw_text(draw, (815, 405), "direct geometric path", FONT_TINY, "#8a8379", "mm")

    normal_specs = [
        (b[0], band_top - 105, band_top + 118, (b[0] + 62, band_top - 92)),
        (c[0], band_bottom - 118, band_bottom + 112, (c[0] - 70, band_bottom + 96)),
    ]
    for x, y1, y2, label_point in normal_specs:
        draw_dashed_line(draw, (x, y1), (x, y2), "#928b82", 3, dash=15, gap=12)
        draw_text(draw, label_point, "normal", FONT_TINY, MUTED, "mm")

    draw_polyline(draw, path, BLUE, 10)
    draw_arrowhead(draw, (1042, 649), c, BLUE)

    theta1 = "\u03b8\u2081"
    theta2 = "\u03b8\u2082"
    draw_angle_arc(draw, b, -math.pi / 2, angle_of(b, a), 74, theta1, 103)
    draw_angle_arc(draw, b, math.pi / 2, angle_of(b, c), 63, theta2, 91)
    draw_angle_arc(draw, c, -math.pi / 2, angle_of(c, b), 63, theta2, 90)
    draw_angle_arc(draw, c, math.pi / 2, angle_of(c, d), 74, theta1, 104)

    draw_point(draw, a, "A", (172, 203))
    draw_point(draw, b, "B", (522, 303))
    draw_point(draw, c, "C", (778, 503))
    draw_point(draw, d, "D", (1198, 676))

    draw_text(draw, (700, 800), "Snell:  sin \u03b8\u2081 / v\u2081 = sin \u03b8\u2082 / v\u2082", FONT_EQ, "#403a34", "mm")
    draw_text(draw, (700, 842), "the ray bends toward the normal on entry, then away on exit", FONT_SMALL, MUTED, "mm")

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
