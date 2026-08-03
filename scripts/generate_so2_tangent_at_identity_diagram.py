from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "so2-tangent-at-identity.png"

WIDTH = 980
HEIGHT = 620
SCALE = 2

BG = (255, 252, 246, 255)
INK = (36, 38, 40, 255)
AXIS = (174, 168, 158, 190)
CIRCLE = (64, 91, 104, 255)
TANGENT = (184, 72, 48, 255)
POINT = (32, 34, 36, 255)
ARC = (196, 105, 52, 230)


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


TITLE = font(26, True)
LABEL = font(18)
SMALL = font(15)


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


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int, int],
    width: int = 5,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 18
    left = (end[0] - size * math.cos(angle - math.pi / 7), end[1] - size * math.sin(angle - math.pi / 7))
    right = (end[0] - size * math.cos(angle + math.pi / 7), end[1] - size * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 48), "Tangent generator at \u03b8 = 0", font_obj=TITLE)

    cx, cy = 395, 330
    r = 170

    # Coordinate axes.
    draw.line((s(cx - 245), s(cy), s(cx + 285), s(cy)), fill=AXIS, width=s(2))
    draw.line((s(cx), s(cy + 230), s(cx), s(cy - 245)), fill=AXIS, width=s(2))
    draw_text(draw, (cx + 302, cy - 6), "x", fill=(110, 105, 98, 255), font_obj=SMALL)
    draw_text(draw, (cx + 10, cy - 258), "y", fill=(110, 105, 98, 255), font_obj=SMALL)

    # Circle.
    draw.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), outline=CIRCLE, width=s(5))

    # Small positive-angle arc, kept inside the circle so it does not compete
    # with the tangent vector at the boundary.
    arc_r = 58
    draw.arc((s(cx - arc_r), s(cy - arc_r), s(cx + arc_r), s(cy + arc_r)), start=-118, end=-12, fill=ARC, width=s(4))
    end_angle = math.radians(-118)
    ax = cx + arc_r * math.cos(end_angle)
    ay = cy + arc_r * math.sin(end_angle)
    tangent_angle = end_angle - math.pi / 2
    for offset in (-2.55, 2.55):
        bx = ax + 12 * math.cos(tangent_angle + offset)
        by = ay + 12 * math.sin(tangent_angle + offset)
        draw.line((s(ax), s(ay), s(bx), s(by)), fill=ARC, width=s(3))

    # Point at theta=0 and tangent vector.
    p = (cx + r, cy)
    draw.ellipse((s(p[0] - 8), s(p[1] - 8), s(p[0] + 8), s(p[1] + 8)), fill=POINT)
    draw_arrow(draw, p, (p[0], p[1] - 132), TANGENT, width=5)

    draw_text(draw, (p[0] + 24, p[1] + 18), "\u03b8 = 0", fill=INK, font_obj=LABEL)
    draw_text(draw, (p[0] + 20, p[1] - 102), "tangent vector", fill=TANGENT, font_obj=LABEL)
    draw_text(draw, (cx - 9, cy + 12), "0", fill=(110, 105, 98, 255), font_obj=SMALL, anchor="ra")
    draw_text(draw, (p[0], p[1] + 48), "(1,0)", fill=INK, font_obj=SMALL, anchor="mm")

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
