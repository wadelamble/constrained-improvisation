from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"

SCALE = 3
W, H = 1400, 900

BG = "#fbfaf7"
PANEL = "#ffffff"
INK = "#2f2f2f"
MUTED = "#6f675e"
BORDER = "#d6cec1"
BLUE_BG = "#e8f3fa"
ORANGE_BG = "#f8eadc"
BLUE = "#245e91"
ORANGE = "#b85c38"
GRAY = "#8b8278"


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
FONT_SMALL = load_font("segoeui.ttf", 23)
FONT_TINY = load_font("segoeui.ttf", 20)
FONT_BOLD = load_font("segoeuib.ttf", 42)
FONT_LABEL = load_font("segoeuib.ttf", 36)
FONT_EQ = load_font("segoeui.ttf", 32)


def draw_text(
    draw: ImageDraw.ImageDraw,
    point: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str = INK,
    anchor: str | None = None,
) -> None:
    draw.text(xy(point), text, font=font, fill=fill, anchor=anchor)


def draw_line(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: str,
    width: int = 4,
) -> None:
    draw.line([xy(p) for p in points], fill=fill, width=s(width), joint="curve")


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    fill: str,
    width: int = 3,
    dash: float = 16,
    gap: float = 11,
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
        draw_line(
            draw,
            [(x1 + ux * t, y1 + uy * t), (x1 + ux * end, y1 + uy * end)],
            fill,
            width,
        )
        t += dash + gap


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    fill: str,
    width: int = 4,
    head: float = 18,
) -> None:
    draw_line(draw, [p1, p2], fill, width)
    vx, vy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(vx, vy)
    if length == 0:
        return
    ux, uy = vx / length, vy / length
    px, py = -uy, ux
    base = (p2[0] - ux * head, p2[1] - uy * head)
    left = (base[0] + px * head * 0.45, base[1] + py * head * 0.45)
    right = (base[0] - px * head * 0.45, base[1] - py * head * 0.45)
    draw.polygon([xy(p2), xy(left), xy(right)], fill=fill)


def draw_double_arrow(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    fill: str,
    width: int = 3,
) -> None:
    draw_arrow(draw, p1, p2, fill, width, head=14)
    draw_arrow(draw, p2, p1, fill, width, head=14)


def draw_point(draw: ImageDraw.ImageDraw, point: tuple[float, float], label: str, label_pos: tuple[float, float]) -> None:
    r = 13
    draw.ellipse([s(point[0] - r - 3), s(point[1] - r - 3), s(point[0] + r + 3), s(point[1] + r + 3)], fill="#ffffff")
    draw.ellipse([s(point[0] - r), s(point[1] - r), s(point[0] + r), s(point[1] + r)], fill=INK)
    draw_text(draw, label_pos, label, FONT_LABEL, INK, "mm")


def draw_angle_arc(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    start: float,
    end: float,
    radius: float,
    label: str,
    label_angle: float,
    label_radius: float,
    color: str,
) -> None:
    steps = 36
    points = []
    for i in range(steps + 1):
        a = start + (end - start) * i / steps
        points.append((center[0] + radius * math.cos(a), center[1] + radius * math.sin(a)))
    draw_line(draw, points, color, 4)
    draw_text(
        draw,
        (
            center[0] + label_radius * math.cos(label_angle),
            center[1] + label_radius * math.sin(label_angle),
        ),
        label,
        FONT,
        color,
        "mm",
    )


def right_angle_marker(
    draw: ImageDraw.ImageDraw,
    corner: tuple[float, float],
    u: tuple[float, float],
    v: tuple[float, float],
    color: str,
    size: float = 28,
) -> None:
    p1 = (corner[0] + u[0] * size, corner[1] + u[1] * size)
    p2 = (p1[0] + v[0] * size, p1[1] + v[1] * size)
    p3 = (corner[0] + v[0] * size, corner[1] + v[1] * size)
    draw_line(draw, [p1, p2, p3], color, 3)


def render(path: Path) -> None:
    img = Image.new("RGB", (s(W), s(H)), BG)
    draw = ImageDraw.Draw(img)

    panel = (90, 105, 1310, 745)
    boundary_y = 410
    draw.rounded_rectangle(
        [s(panel[0]), s(panel[1]), s(panel[2]), s(panel[3])],
        radius=s(5),
        fill=PANEL,
        outline=BORDER,
        width=s(2),
    )
    draw.rectangle([s(panel[0]), s(panel[1]), s(panel[2]), s(boundary_y)], fill=BLUE_BG)
    draw.rectangle([s(panel[0]), s(boundary_y), s(panel[2]), s(panel[3])], fill=ORANGE_BG)
    draw_line(draw, [(panel[0], boundary_y), (panel[2], boundary_y)], INK, 4)

    draw_text(draw, (700, 55), "Huygens construction gives Snell's law", FONT_BOLD, INK, "mm")
    draw_text(draw, (210, 165), "medium 1, speed v\u2081", FONT_SMALL, BLUE, "mm")
    draw_text(draw, (210, 700), "medium 2, speed v\u2082", FONT_SMALL, ORANGE, "mm")

    a = (390, boundary_y)
    b = (850, boundary_y)
    theta1 = math.radians(36)
    theta2 = math.radians(21)
    ab = b[0] - a[0]

    # Incoming front at the later time, and the perpendicular advance from A.
    # Image coordinates have y increasing downward, so the upper triangle uses
    # a negative y component.
    f1 = (-math.cos(theta1), -math.sin(theta1))
    c1 = (b[0] + ab * math.cos(theta1) * f1[0], b[1] + ab * math.cos(theta1) * f1[1])
    f1_start = (b[0] + f1[0] * 320, b[1] + f1[1] * 320)
    f1_end = (b[0] - f1[0] * 155, b[1] - f1[1] * 155)
    draw_line(draw, [f1_start, f1_end], BLUE, 6)
    draw_text(draw, (780, 225), "incoming front\nafter \u0394t", FONT_SMALL, BLUE, "mm")
    draw_arrow(draw, a, c1, BLUE, 4)
    draw_text(draw, ((a[0] + c1[0]) / 2 - 50, (a[1] + c1[1]) / 2 - 20), "v\u2081\u0394t", FONT, BLUE, "mm")
    right_angle_marker(draw, c1, (math.sin(theta1), -math.cos(theta1)), f1, BLUE, size=20)

    # Huygens wavelet and refracted front tangent to it.
    f2 = (-math.cos(theta2), math.sin(theta2))
    t = (b[0] + ab * math.cos(theta2) * f2[0], b[1] + ab * math.cos(theta2) * f2[1])
    radius = math.hypot(t[0] - a[0], t[1] - a[1])
    draw.arc(
        [s(a[0] - radius), s(a[1] - radius), s(a[0] + radius), s(a[1] + radius)],
        start=0,
        end=180,
        fill=ORANGE,
        width=s(5),
    )
    f2_start = (b[0] + f2[0] * 435, b[1] + f2[1] * 435)
    f2_end = (b[0] - f2[0] * 160, b[1] - f2[1] * 160)
    draw_line(draw, [f2_start, f2_end], ORANGE, 6)
    draw_text(draw, (825, 595), "refracted front\ntangent to wavelet", FONT_SMALL, ORANGE, "mm")
    draw_arrow(draw, a, t, ORANGE, 4)
    draw_text(draw, ((a[0] + t[0]) / 2 - 18, (a[1] + t[1]) / 2 + 28), "v\u2082\u0394t", FONT, ORANGE, "mm")
    right_angle_marker(draw, t, (math.sin(theta2), math.cos(theta2)), f2, ORANGE, size=20)

    # Boundary distance and points.
    draw_double_arrow(draw, (a[0], boundary_y - 36), (b[0], boundary_y - 36), GRAY, 3)
    draw_text(draw, ((a[0] + b[0]) / 2, boundary_y - 72), "AB", FONT, GRAY, "mm")
    draw_point(draw, a, "A", (a[0] - 38, a[1] + 43))
    draw_point(draw, b, "B", (b[0] + 38, b[1] + 43))
    draw_text(draw, (a[0], boundary_y + 72), "first point hit", FONT_TINY, MUTED, "mm")
    draw_text(draw, (b[0] + 8, boundary_y + 72), "point hit after \u0394t", FONT_TINY, MUTED, "mm")

    # Angle arcs. The front angle with the boundary equals the ray angle with the normal.
    draw_angle_arc(draw, b, math.pi, math.pi + theta1, 82, "\u03b8\u2081", math.pi + theta1 / 2, 118, BLUE)
    draw_angle_arc(draw, b, math.pi - theta2, math.pi, 102, "\u03b8\u2082", math.pi - theta2 / 2, 140, ORANGE)

    # Formula callout.
    box = (910, 130, 1270, 285)
    draw.rounded_rectangle([s(box[0]), s(box[1]), s(box[2]), s(box[3])], radius=s(12), fill="#fffdf8", outline=BORDER, width=s(2))
    draw_text(draw, (1090, 175), "sin \u03b8\u2081 = v\u2081\u0394t / AB", FONT_EQ, INK, "mm")
    draw_text(draw, (1090, 240), "sin \u03b8\u2082 = v\u2082\u0394t / AB", FONT_EQ, INK, "mm")

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main() -> None:
    render(OUT / "lm-huygens-snell-two-point-construction.png")
    render(OUT / "lm-huygens-snell-two-point-construction-review.png")


if __name__ == "__main__":
    main()
