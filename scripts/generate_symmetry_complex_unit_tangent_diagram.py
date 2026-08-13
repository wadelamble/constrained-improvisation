from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-complex-unit-tangent.png"

WIDTH = 1100
HEIGHT = 620
SCALE = 2

BG = (255, 252, 246, 255)
INK = (35, 36, 38, 255)
MUTED = (174, 168, 158, 220)
FAINT = (226, 219, 209, 255)
CIRCLE = (64, 91, 104, 255)
BLUE = (57, 103, 157, 255)
RED = (184, 72, 48, 255)


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
    head: float = 17,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 42), "The unit tangent at the identity", font_obj=TITLE)

    cx, cy = 455.0, 370.0
    radius = 170.0
    identity = (cx + radius, cy)
    tangent_end = (identity[0], identity[1] - radius)

    # Coordinate grid and complex-plane axes.
    for offset in range(-2, 3):
        x = cx + offset * radius
        y = cy + offset * radius
        draw.line((s(x), s(104), s(x), s(566)), fill=FAINT, width=s(1))
        draw.line((s(112), s(y), s(820), s(y)), fill=FAINT, width=s(1))
    draw_arrow(draw, (112, cy), (835, cy), MUTED, width=3, head=13)
    draw_arrow(draw, (cx, 566), (cx, 94), MUTED, width=3, head=13)
    draw_text(draw, (848, cy + 18), "real", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (cx + 16, 88), "imaginary", fill=MUTED, font_obj=SMALL)

    # Unit circle.
    draw.ellipse(
        (s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)),
        outline=CIRCLE,
        width=s(5),
    )
    draw_text(draw, (cx - 112, cy - 116), "unit circle", fill=CIRCLE, font_obj=SMALL)

    # The identity vector and the equally long tangent vector at its tip.
    draw_arrow(draw, (cx, cy), identity, BLUE, width=6)
    draw_arrow(draw, identity, tangent_end, RED, width=6)
    draw.ellipse(
        (s(identity[0] - 7), s(identity[1] - 7), s(identity[0] + 7), s(identity[1] + 7)),
        fill=INK,
    )

    # Right-angle marker at the identity.
    marker = 20
    draw.line(
        (
            s(identity[0] - marker),
            s(identity[1]),
            s(identity[0] - marker),
            s(identity[1] - marker),
            s(identity[0]),
            s(identity[1] - marker),
        ),
        fill=MUTED,
        width=s(2),
    )

    draw_text(draw, ((cx + identity[0]) / 2, cy + 32), "1", fill=BLUE, font_obj=LABEL, anchor="mm")
    draw_text(draw, (identity[0] + 24, cy + 22), "identity  1", font_obj=LABEL)
    draw_text(draw, (identity[0] + 24, (identity[1] + tangent_end[1]) / 2), "unit tangent  i", fill=RED, font_obj=LABEL)
    draw_text(draw, (cx - 12, cy + 16), "0", fill=MUTED, font_obj=SMALL, anchor="ra")

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
