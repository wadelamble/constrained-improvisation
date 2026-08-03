from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-complex-plane-phase.png"

WIDTH = 1100
HEIGHT = 560
SCALE = 2

BG = (255, 252, 246, 255)
INK = (35, 36, 38, 255)
MUTED = (174, 168, 158, 220)
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
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - 0.45), end[1] - head * math.sin(angle - 0.45))
    right = (end[0] - head * math.cos(angle + 0.45), end[1] - head * math.sin(angle + 0.45))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def arc_points(cx: float, cy: float, radius: float, a0: float, a1: float, steps: int = 48) -> list[tuple[int, int]]:
    pts = []
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        pts.append((s(cx + radius * math.cos(t)), s(cy - radius * math.sin(t))))
    return pts


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 42), "Phase as rotation in the complex plane", font_obj=TITLE)

    cx, cy = 420, 316
    radius = 168
    theta = math.radians(42)
    px = cx + radius * math.cos(theta)
    py = cy - radius * math.sin(theta)
    foot = (px, cy)

    # Grid.
    for k in range(-3, 4):
        x = cx + k * radius / 2
        y = cy + k * radius / 2
        draw.line((s(x), s(96), s(x), s(492)), fill=FAINT, width=s(1))
        draw.line((s(144), s(y), s(706), s(y)), fill=FAINT, width=s(1))

    # Unit circle and axes.
    draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=MUTED, width=s(3))
    draw_arrow(draw, (130, cy), (732, cy), MUTED, width=3, head=13)
    draw_arrow(draw, (cx, 502), (cx, 82), MUTED, width=3, head=13)
    draw_text(draw, (744, cy + 20), "real", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (cx + 14, 78), "imaginary", fill=MUTED, font_obj=SMALL)

    # Reference radius at 1.
    draw_arrow(draw, (cx, cy), (cx + radius, cy), (174, 168, 158, 120), width=4, head=12)
    draw_text(draw, (cx + radius + 12, cy + 28), "1", fill=MUTED, font_obj=SMALL)

    # Component guides.
    draw.line((s(px), s(py), s(px), s(cy)), fill=(184, 72, 48, 120), width=s(3))
    draw.line((s(cx), s(py), s(px), s(py)), fill=(57, 103, 157, 120), width=s(3))
    draw_arrow(draw, (cx, cy), foot, BLUE, width=5)
    draw_arrow(draw, foot, (px, py), RED, width=5)

    # Rotation vector and point.
    draw_arrow(draw, (cx, cy), (px, py), GREEN, width=6, head=18)
    draw.ellipse((s(px - 8), s(py - 8), s(px + 8), s(py + 8)), fill=GREEN)

    # Angle arc.
    pts = arc_points(cx, cy, 70, 0, theta)
    draw.line(pts, fill=GOLD, width=s(4))
    end_angle = theta
    arc_end = (cx + 70 * math.cos(end_angle), cy - 70 * math.sin(end_angle))
    draw_arrow(draw, (arc_end[0] - 1, arc_end[1] + 1), arc_end, GOLD, width=1, head=11)
    draw_text(draw, (cx + 86, cy - 30), "θ", fill=GOLD, font_obj=LABEL)

    # Labels.
    draw_text(draw, ((cx + foot[0]) / 2, cy + 34), "cos θ", fill=BLUE, font_obj=LABEL, anchor="mm")
    draw_text(draw, (foot[0] + 20, (cy + py) / 2), "sin θ", fill=RED, font_obj=LABEL, anchor="lm")
    draw_text(draw, (px + 24, py - 18), "e^{iθ}", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (px + 24, py + 12), "= cos θ + i sin θ", fill=GREEN, font_obj=SMALL)
    draw_text(draw, (cx - 110, cy - radius - 22), "|e^{iθ}| = 1", fill=INK, font_obj=LABEL)
    draw_text(draw, (cx - 112, cy + radius + 30), "phase θ rotates the unit vector", fill=(91, 87, 81, 255), font_obj=SMALL)

    # Summary panel.
    draw.rounded_rectangle((s(780), s(150), s(1032), s(378)), radius=s(12), fill=(250, 246, 238, 255), outline=(224, 216, 204, 255), width=s(2))
    draw_text(draw, (806, 184), "one complex number", font_obj=LABEL)
    draw_text(draw, (806, 228), "z = e^{iθ}", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (806, 284), "two real components", font_obj=LABEL)
    draw_text(draw, (806, 326), "(cos θ, sin θ)", fill=INK, font_obj=LABEL)
    draw_text(draw, (806, 356), "same rotation", fill=(91, 87, 81, 255), font_obj=SMALL)

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
