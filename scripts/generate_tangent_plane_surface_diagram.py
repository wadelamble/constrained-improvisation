from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "tangent-plane-curved-surface.png"

WIDTH = 1200
HEIGHT = 780
SCALE = 2

BG = (255, 252, 246, 255)
INK = (42, 43, 45, 255)
MESH = (91, 132, 125, 155)
SURFACE = (196, 224, 214, 122)
PLANE = (238, 196, 118, 145)
PLANE_EDGE = (171, 112, 36, 220)
RED = (184, 72, 48, 255)
BLUE = (50, 99, 164, 255)
POINT = (30, 32, 34, 255)


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


TITLE = font(27, True)
LABEL = font(18)
SMALL = font(15)


def surface_z(x: float, y: float) -> float:
    return 0.78 - 0.15 * x * x - 0.10 * y * y


def dzdx(x: float, y: float) -> float:
    return -0.30 * x


def dzdy(x: float, y: float) -> float:
    return -0.20 * y


def normalize(v: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    return (v[0] / length, v[1] / length, v[2] / length)


def cross(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def add(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(v: tuple[float, float, float], factor: float) -> tuple[float, float, float]:
    return (v[0] * factor, v[1] * factor, v[2] * factor)


VIEW_Z = math.radians(-36)
VIEW_X = math.radians(59)
COS_Z = math.cos(VIEW_Z)
SIN_Z = math.sin(VIEW_Z)
COS_X = math.cos(VIEW_X)
SIN_X = math.sin(VIEW_X)


def rotate(p: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = p
    x1 = COS_Z * x - SIN_Z * y
    y1 = SIN_Z * x + COS_Z * y
    return (
        x1,
        COS_X * y1 + SIN_X * z,
        -SIN_X * y1 + COS_X * z,
    )


def project(p: tuple[float, float, float]) -> tuple[float, float]:
    x, y, _depth = rotate(p)
    scale = 146 * SCALE
    return (WIDTH * SCALE * 0.51 + scale * x, HEIGHT * SCALE * 0.50 - scale * y)


def depth(p: tuple[float, float, float]) -> float:
    return rotate(p)[2]


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((xy[0] * SCALE, xy[1] * SCALE), text, fill=fill, font=font_obj, anchor=anchor)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int, int],
    width: int = 5,
) -> None:
    draw.line((*start, *end), fill=color, width=width * SCALE)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 17 * SCALE
    left = (
        end[0] - size * math.cos(angle - math.pi / 7),
        end[1] - size * math.sin(angle - math.pi / 7),
    )
    right = (
        end[0] - size * math.cos(angle + math.pi / 7),
        end[1] - size * math.sin(angle + math.pi / 7),
    )
    draw.polygon([end, left, right], fill=color)


def draw_poly(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float, float]],
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int] | None = None,
    width: int = 1,
) -> None:
    xy = [project(p) for p in points]
    draw.polygon(xy, fill=fill)
    if outline:
        draw.line(xy + [xy[0]], fill=outline, width=width * SCALE, joint="curve")


def main() -> None:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (64, 52), "Curved surface, tangent plane, tangent vectors", font_obj=TITLE)

    xs = [v / 10 for v in range(-24, 25, 4)]
    ys = [v / 10 for v in range(-18, 19, 4)]
    cells = []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            quad = [
                (xs[i], ys[j], surface_z(xs[i], ys[j])),
                (xs[i + 1], ys[j], surface_z(xs[i + 1], ys[j])),
                (xs[i + 1], ys[j + 1], surface_z(xs[i + 1], ys[j + 1])),
                (xs[i], ys[j + 1], surface_z(xs[i], ys[j + 1])),
            ]
            cells.append((sum(depth(p) for p in quad) / 4, quad))

    for _z, quad in sorted(cells):
        draw_poly(draw, quad, SURFACE)

    for y in ys:
        line = [(x, y, surface_z(x, y)) for x in xs]
        draw.line([project(p) for p in line], fill=MESH, width=2 * SCALE, joint="curve")
    for x in xs:
        line = [(x, y, surface_z(x, y)) for y in ys]
        draw.line([project(p) for p in line], fill=MESH, width=2 * SCALE, joint="curve")

    p0 = (0.25, -0.25, surface_z(0.25, -0.25))
    zx = dzdx(0.25, -0.25)
    zy = dzdy(0.25, -0.25)
    normal = normalize((-zx, -zy, 1.0))
    e1 = normalize((1.0, 0.0, zx))
    e2 = normalize(cross(normal, e1))

    plane_radius = 0.82
    plane = [
        add(p0, add(mul(e1, -plane_radius), mul(e2, -plane_radius))),
        add(p0, add(mul(e1, plane_radius), mul(e2, -plane_radius))),
        add(p0, add(mul(e1, plane_radius), mul(e2, plane_radius))),
        add(p0, add(mul(e1, -plane_radius), mul(e2, plane_radius))),
    ]
    draw_poly(draw, plane, PLANE, PLANE_EDGE, width=2)

    origin = project(p0)
    e1_end = project(add(p0, mul(e1, 0.98)))
    e2_end = project(add(p0, mul(e2, 0.98)))
    draw_arrow(draw, origin, e1_end, RED, width=5)
    draw_arrow(draw, origin, e2_end, BLUE, width=5)

    marker_size = 0.18
    marker = [
        add(p0, mul(e1, marker_size)),
        add(p0, add(mul(e1, marker_size), mul(e2, marker_size))),
        add(p0, mul(e2, marker_size)),
    ]
    draw.line([project(p) for p in marker], fill=(46, 47, 48, 230), width=3 * SCALE)

    px, py = origin
    r = 8 * SCALE
    draw.ellipse((px - r, py - r, px + r, py + r), fill=POINT)

    draw_text(draw, (780, 160), "tangent plane", fill=PLANE_EDGE, font_obj=LABEL)
    plane_label_anchor = project(add(p0, add(mul(e1, 0.72), mul(e2, 0.58))))
    draw.line(
        (780 * SCALE, 190 * SCALE, plane_label_anchor[0], plane_label_anchor[1]),
        fill=PLANE_EDGE,
        width=2 * SCALE,
    )

    draw_text(draw, (820, 560), "orthogonal tangent vectors", fill=(44, 58, 78, 255), font_obj=LABEL)
    draw.line(
        (820 * SCALE, 590 * SCALE, origin[0] + 22 * SCALE, origin[1] + 4 * SCALE),
        fill=(44, 58, 78, 200),
        width=2 * SCALE,
    )

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
