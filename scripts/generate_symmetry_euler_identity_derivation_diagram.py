from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-euler-identity-derivation.png"

WIDTH = 1280
HEIGHT = 820
SCALE = 2

BG = (255, 252, 246, 255)
PANEL = (250, 246, 238, 255)
PANEL_EDGE = (224, 216, 204, 255)
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


TITLE = font(22, True)
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


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float], title: str) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in box), radius=s(14), fill=PANEL, outline=PANEL_EDGE, width=s(2))
    draw_text(draw, (box[0] + 28, box[1] + 24), title, font_obj=TITLE)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int, int],
    width: int = 5,
    head: float = 17,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def point(cx: float, cy: float, r: float, theta: float) -> tuple[float, float]:
    return cx + r * math.cos(theta), cy - r * math.sin(theta)


def draw_axes(draw: ImageDraw.ImageDraw, cx: float, cy: float, extent: float) -> None:
    draw.line((s(cx - extent), s(cy), s(cx + extent), s(cy)), fill=MUTED, width=s(2))
    draw.line((s(cx), s(cy + extent), s(cx), s(cy - extent)), fill=MUTED, width=s(2))


def draw_arc(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    start: float,
    end: float,
    color: tuple[int, int, int, int],
    width: int = 4,
    arrow: bool = False,
) -> None:
    draw.arc(
        (s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)),
        start=-math.degrees(end),
        end=-math.degrees(start),
        fill=color,
        width=s(width),
    )
    if arrow:
        ax, ay = point(cx, cy, radius, end)
        tangent = end + math.pi / 2
        for offset in (-2.55, 2.55):
            bx = ax - 12 * math.cos(tangent + offset)
            by = ay + 12 * math.sin(tangent + offset)
            draw.line((s(ax), s(ay), s(bx), s(by)), fill=color, width=s(3))


def constants_panel(draw: ImageDraw.ImageDraw) -> None:
    box = (44, 48, 612, 360)
    draw_panel(draw, box, "Define the constants")
    x = box[0] + 44
    y = box[1] + 86
    draw_text(draw, (x, y), "i:     i^2 = -1", font_obj=LABEL)
    draw_text(draw, (x, y + 52), "\u03c0:    C = 2\u03c0r", font_obj=LABEL)
    draw_text(draw, (x, y + 104), "e:    d(e^x)/dx = e^x", font_obj=LABEL)
    draw_text(draw, (x, y + 172), "Goal: show  e^{i\u03c0} = -1", fill=RED, font_obj=TITLE)


def i_rotation_panel(draw: ImageDraw.ImageDraw) -> None:
    box = (668, 48, 1236, 360)
    draw_panel(draw, box, "Multiplication by i is a 90° rotation")
    draw_text(draw, (box[0] + 44, box[1] + 78), "iz = i(x+iy) = ix+i^2y = -y+ix", fill=RED, font_obj=LABEL)
    draw_text(draw, (box[0] + 44, box[1] + 116), "(x,y) \u2192 (-y,x)", fill=INK, font_obj=LABEL)

    cx, cy = 960.0, 248.0
    draw_axes(draw, cx, cy, 120)
    length = 95
    theta = math.radians(45)
    z = point(cx, cy, length, theta)
    iz = point(cx, cy, length, theta + math.pi / 2)
    draw_arrow(draw, (cx, cy), z, BLUE, width=5)
    draw_arrow(draw, (cx, cy), iz, RED, width=5)
    draw_arc(draw, cx, cy, 46, theta, theta + math.pi / 2, GOLD, width=4, arrow=True)
    draw_text(draw, (z[0] + 14, z[1] - 18), "(\u221a2,\u221a2)", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (iz[0] - 14, iz[1] - 18), "(-\u221a2,\u221a2)", fill=RED, font_obj=SMALL, anchor="rm")


def unit_circle_panel(draw: ImageDraw.ImageDraw) -> None:
    box = (44, 404, 612, 772)
    draw_panel(draw, box, "Represent points by z(\u03b8)")
    cx, cy = 300.0, 605.0
    r = 118.0
    draw_axes(draw, cx, cy, 160)
    draw.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), outline=(64, 91, 104, 255), width=s(5))
    theta = math.radians(55)
    z = point(cx, cy, r, theta)
    draw_arrow(draw, (cx, cy), z, BLUE, width=5)
    draw_arc(draw, cx, cy, 45, 0, theta, GOLD, width=4, arrow=True)
    draw_text(draw, (z[0] + 16, z[1] - 12), "z", fill=BLUE, font_obj=LABEL)
    draw_text(draw, (cx + 58, cy - 22), "\u03b8", fill=GOLD, font_obj=LABEL)
    draw_text(draw, (box[0] + 328, box[1] + 100), "z(x,y) \u2192 z(\u03b8)", font_obj=LABEL)
    draw_text(draw, (box[0] + 328, box[1] + 142), "on the unit circle", fill=(93, 88, 82, 255), font_obj=SMALL)


def tangent_panel(draw: ImageDraw.ImageDraw) -> None:
    box = (668, 404, 1236, 772)
    draw_panel(draw, box, "The tangent is iz")
    cx, cy = 946.0, 588.0
    r = 112.0
    draw_axes(draw, cx, cy, 152)
    draw.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), outline=(64, 91, 104, 255), width=s(5))

    # Cardinal tangent arrows echo the handwritten sketch.
    tangents = [
        (0, (0, -64), "(0,1)", RED),
        (math.pi / 2, (-64, 0), "(-1,0)", RED),
        (math.pi, (0, 64), "(0,-1)", RED),
        (3 * math.pi / 2, (64, 0), "(1,0)", RED),
    ]
    for angle, vec, label, color in tangents:
        p = point(cx, cy, r, angle)
        end = (p[0] + vec[0], p[1] + vec[1])
        draw_arrow(draw, p, end, color, width=4, head=14)
        lx = end[0] + (12 if vec[0] >= 0 else -12)
        ly = end[1] + (-8 if vec[1] <= 0 else 18)
        anchor = "lm" if vec[0] >= 0 else "rm"
        draw_text(draw, (lx, ly), label, fill=color, font_obj=SMALL, anchor=anchor)

    draw_arc(draw, cx, cy, r + 35, 0, math.pi, GOLD, width=4, arrow=True)
    draw_text(draw, (cx, cy - r - 56), "\u03c0", fill=GOLD, font_obj=LABEL, anchor="mm")
    draw_text(draw, (box[0] + 42, box[1] + 88), "dz/d\u03b8 = iz(\u03b8)", fill=RED, font_obj=LABEL)
    draw_text(draw, (box[0] + 42, box[1] + 128), "z(\u03b8) = e^{i\u03b8}", font_obj=LABEL)
    draw_text(draw, (box[0] + 42, box[1] + 304), "at \u03b8=\u03c0:  e^{i\u03c0} = -1", fill=RED, font_obj=TITLE)


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")
    constants_panel(draw)
    i_rotation_panel(draw)
    unit_circle_panel(draw)
    tangent_panel(draw)
    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
