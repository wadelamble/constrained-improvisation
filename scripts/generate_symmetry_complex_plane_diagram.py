from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-complex-plane-vector.png"

WIDTH = 1100
HEIGHT = 560
SCALE = 2

BG = (255, 252, 246, 255)
INK = (35, 36, 38, 255)
MUTED = (174, 168, 158, 220)
FAINT = (226, 219, 209, 255)
BLUE = (57, 103, 157, 255)
RED = (184, 72, 48, 255)
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


TITLE = font(26, True)
LABEL = font(18)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 5,
    head: float = 16,
) -> None:
    import math

    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - 0.45), end[1] - head * math.sin(angle - 0.45))
    right = (end[0] - head * math.cos(angle + 0.45), end[1] - head * math.sin(angle + 0.45))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 42), "A complex number is a two-component vector", font_obj=TITLE)

    ox, oy = 455, 410
    x_len = 270
    y_len = 190
    z_end = (ox + x_len, oy - y_len)

    # Grid and axes.
    for k in range(-4, 5):
        x = ox + k * 70
        y = oy + k * 70
        draw.line((s(x), s(110), s(x), s(474)), fill=FAINT, width=s(1))
        draw.line((s(120), s(y), s(790), s(y)), fill=FAINT, width=s(1))
    draw_arrow(draw, (120, oy), (810, oy), MUTED, width=3, head=13)
    draw_arrow(draw, (ox, 474), (ox, 92), MUTED, width=3, head=13)
    draw_text(draw, (818, oy + 20), "real", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (ox + 16, 88), "imaginary", fill=MUTED, font_obj=SMALL)

    # Component guides.
    dash = 12
    x0, y0 = z_end
    y = oy
    while y > y0:
        draw.line((s(x0), s(y), s(x0), s(max(y - dash, y0))), fill=(184, 72, 48, 115), width=s(2))
        y -= 2 * dash
    x = ox
    while x < x0:
        draw.line((s(x), s(y0), s(min(x + dash, x0)), s(y0)), fill=(57, 103, 157, 115), width=s(2))
        x += 2 * dash

    # Components and vector.
    draw_arrow(draw, (ox, oy), (ox + x_len, oy), BLUE, width=5)
    draw_arrow(draw, (ox + x_len, oy), z_end, RED, width=5)
    draw_arrow(draw, (ox, oy), z_end, GREEN, width=6)

    draw.ellipse((s(z_end[0] - 7), s(z_end[1] - 7), s(z_end[0] + 7), s(z_end[1] + 7)), fill=GREEN)
    draw_text(draw, (ox + x_len / 2, oy + 32), "x", fill=BLUE, font_obj=LABEL, anchor="mm")
    draw_text(draw, (ox + x_len + 22, oy - y_len / 2), "iy", fill=RED, font_obj=LABEL, anchor="lm")
    draw_text(draw, (z_end[0] + 22, z_end[1] - 20), "z = x + iy", fill=GREEN, font_obj=LABEL)

    # Small coordinate version.
    draw.rounded_rectangle((s(840), s(166), s(1038), s(352)), radius=s(12), fill=(250, 246, 238, 255), outline=(224, 216, 204, 255), width=s(2))
    draw_text(draw, (864, 196), "complex form", font_obj=LABEL)
    draw_text(draw, (864, 238), "z = x + iy", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (864, 292), "vector form", font_obj=LABEL)
    draw_text(draw, (864, 328), "(x, y)", fill=INK, font_obj=LABEL)

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
