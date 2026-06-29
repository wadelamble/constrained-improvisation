from __future__ import annotations

from pathlib import Path
from math import pi, sin

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "drafts" / "animations" / "lm-possible-spacetime-paths.png"
SCALE = 2


def font(size: int, italic: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/segoeuii.ttf" if italic else "C:/Windows/Fonts/segoeui.ttf"
    return ImageFont.truetype(path, size)


def cubic(p0, p1, p2, p3, steps: int = 90) -> list[tuple[float, float]]:
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def polyline(points: list[tuple[float, float]], samples_per_segment: int = 70) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for p0, p1 in zip(points, points[1:]):
        for i in range(samples_per_segment):
            t = i / samples_per_segment
            out.append((p0[0] * (1 - t) + p1[0] * t, p0[1] * (1 - t) + p1[1] * t))
    out.append(points[-1])
    return out


def sampled_path(start: tuple[float, float], end: tuple[float, float], offset, steps: int = 360) -> list[tuple[float, float]]:
    pts = []
    for i in range(steps + 1):
        s = i / steps
        x = start[0] * (1 - s) + end[0] * s + offset(s)
        t = start[1] * (1 - s) + end[1] * s
        pts.append((x, t))
    return pts


def data_to_px(point: tuple[float, float]) -> tuple[int, int]:
    x, t = point
    x_min, x_max = -3.0, 3.8
    t_min, t_max = -0.05, 5.05
    left, top, right, bottom = 58, 70, 860, 700
    px = left + (x - x_min) / (x_max - x_min) * (right - left)
    py = bottom - (t - t_min) / (t_max - t_min) * (bottom - top)
    return round(px), round(py)


def draw_path(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], color: str, width: int) -> None:
    draw.line([(x * SCALE, y * SCALE) for x, y in (data_to_px(p) for p in points)], fill=color, width=width, joint="curve")


def main() -> None:
    width, height = 900, 760
    im = Image.new("RGB", (width * SCALE, height * SCALE), "#F7F3EC")
    draw = ImageDraw.Draw(im)

    def sxy(x: int, y: int) -> tuple[int, int]:
        return x * SCALE, y * SCALE

    def srect(rect):
        return tuple(v * SCALE for v in rect)

    title_font = font(31 * SCALE)
    label_font = font(22 * SCALE)
    small_font = font(21 * SCALE)
    italic_font = font(24 * SCALE, italic=True)

    plot = (52, 70, 860, 700)
    draw.rectangle(srect(plot), outline="#BBA88F", width=2 * SCALE)

    title = "Possible paths between fixed spacetime events"
    title_box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(sxy((width - (title_box[2] - title_box[0]) // SCALE) // 2, 12), title, fill="#2F2F2F", font=title_font)

    arrow = "#7E7468"
    draw.line([sxy(70, 690), sxy(846, 690)], fill=arrow, width=3 * SCALE)
    draw.polygon([sxy(846, 690), sxy(834, 682), sxy(834, 698)], fill=arrow)
    draw.line([sxy(86, 686), sxy(86, 100)], fill=arrow, width=3 * SCALE)
    draw.polygon([sxy(86, 100), sxy(78, 113), sxy(94, 113)], fill=arrow)

    draw.text(sxy(836, 710), "x", fill="#4B463F", font=italic_font)
    draw.text(sxy(58, 102), "t", fill="#4B463F", font=italic_font)
    draw.text(sxy(432, 712), "space", fill="#000000", font=label_font)
    draw.text(sxy(17, 378), "time", fill="#000000", font=label_font)

    start = (-1.55, 0.35)
    end = (1.45, 4.45)

    left_overshoot = sampled_path(
        start,
        end,
        lambda s: -1.35 * sin(pi * s) - 0.28 * sin(2 * pi * s) + 0.18 * sin(3 * pi * s),
    )
    right_overshoot = sampled_path(
        start,
        end,
        lambda s: 1.95 * sin(pi * s) ** 1.1 + 0.58 * sin(2 * pi * s),
    )
    wild = sampled_path(
        start,
        end,
        lambda s: 0.95 * sin(pi * s) * sin(5.4 * pi * s) + 0.44 * sin(pi * s) * sin(2 * pi * s),
    )
    smooth = cubic(start, (-1.02, 1.26), (0.78, 3.45), end, 180)

    draw_path(draw, left_overshoot, "#BDB4A7", 6 * SCALE)
    draw_path(draw, right_overshoot, "#BDB4A7", 6 * SCALE)
    draw_path(draw, wild, "#A8B5C6", 6 * SCALE)
    draw_path(draw, smooth, "#B85C38", 7 * SCALE)

    for point in [start, end]:
        x, y = data_to_px(point)
        draw.ellipse(srect((x - 11, y - 11, x + 11, y + 11)), fill="#2F2F2F", outline="#FFFFFF", width=2 * SCALE)

    draw.text(sxy(120, 612), "fixed start", fill="#4B463F", font=small_font)
    draw.text(sxy(612, 125), "fixed end", fill="#4B463F", font=small_font)

    im = im.resize((width, height), Image.Resampling.LANCZOS)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    im.save(OUTPUT)


if __name__ == "__main__":
    main()
