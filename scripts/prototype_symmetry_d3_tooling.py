from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations" / "_prototypes"

WIDTH = 1200
HEIGHT = 720
SCALE = 2
BG = (255, 255, 255)
INK = (14, 14, 14)
COORD = (176, 176, 176)
AXIS = (16, 16, 16)
TEAL = (34, 107, 128)
RUST = (176, 83, 52)
PURPLE = (91, 92, 154)
PLANE = (232, 240, 242)
PLANE_EDGE = (150, 174, 181)

Vec3 = tuple[float, float, float]
Vec2 = tuple[float, float]


def add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(s: float, v: Vec3) -> Vec3:
    return (s * v[0], s * v[1], s * v[2])


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(v: Vec3) -> float:
    return math.sqrt(dot(v, v))


def normalize(v: Vec3) -> Vec3:
    size = length(v)
    return (v[0] / size, v[1] / size, v[2] / size)


def mix(a: Vec3, b: Vec3, t: float) -> Vec3:
    return (
        a[0] * (1.0 - t) + b[0] * t,
        a[1] * (1.0 - t) + b[1] * t,
        a[2] * (1.0 - t) + b[2] * t,
    )


def blend(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int]:
    alpha = max(0.0, min(1.0, alpha))
    return (
        round(BG[0] * (1.0 - alpha) + color[0] * alpha),
        round(BG[1] * (1.0 - alpha) + color[1] * alpha),
        round(BG[2] * (1.0 - alpha) + color[2] * alpha),
    )


U = normalize((1.0, 1.0, 1.0))
E1 = normalize((1.0, -1.0, 0.0))
E2 = normalize(cross(U, E1))
VIEW = normalize((3.8, -2.8, 3.2))
RIGHT = normalize(cross(VIEW, (0.0, 0.0, 1.0)))
UP = normalize(cross(VIEW, RIGHT))


def rotate_about_axis(v: Vec3, degrees: float) -> Vec3:
    theta = math.radians(degrees)
    return add(
        add(mul(math.cos(theta), v), mul(math.sin(theta), cross(U, v))),
        mul(dot(U, v) * (1.0 - math.cos(theta)), U),
    )


def reflect_in_plane(v: Vec3) -> Vec3:
    normal = normalize(cross(U, (1.0, 0.0, 0.0)))
    return sub(v, mul(2.0 * dot(v, normal), normal))


def sample(h: float, radius: float, phase: float) -> Vec3:
    return add(mul(h, U), add(mul(radius * math.cos(phase), E1), mul(radius * math.sin(phase), E2)))


def orbit(v: Vec3) -> list[Vec3]:
    return [rotate_about_axis(v, angle) for angle in (0.0, 120.0, 240.0)]


def project(v: Vec3, origin: Vec2, scale: float) -> tuple[float, float, float]:
    return (origin[0] + dot(v, RIGHT) * scale, origin[1] - dot(v, UP) * scale, dot(v, VIEW))


def xy(p: Vec2) -> tuple[int, int]:
    return (round(p[0] * SCALE), round(p[1] * SCALE))


def line(draw: ImageDraw.ImageDraw, points: list[Vec2], color: tuple[int, int, int], width: float, alpha: float = 1.0) -> None:
    if alpha <= 0:
        return
    draw.line([xy(p) for p in points], fill=blend(color, alpha), width=max(1, round(width * SCALE)), joint="curve")


def circle(draw: ImageDraw.ImageDraw, p: Vec2, radius: float, color: tuple[int, int, int], alpha: float = 1.0) -> None:
    if alpha <= 0:
        return
    x, y = xy(p)
    r = round(radius * SCALE)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=blend(color, alpha))


def arrow(draw: ImageDraw.ImageDraw, a: Vec3, b: Vec3, origin: Vec2, scale: float, color: tuple[int, int, int], width: float, alpha: float = 1.0) -> None:
    p0 = project(a, origin, scale)
    p1 = project(b, origin, scale)
    a2 = (p0[0], p0[1])
    b2 = (p1[0], p1[1])
    line(draw, [a2, b2], color, width, alpha)
    dx = b2[0] - a2[0]
    dy = b2[1] - a2[1]
    size = math.hypot(dx, dy)
    if size < 4:
        return
    angle = math.atan2(dy, dx)
    spread = 2.62
    head = 15.0
    pts = [
        b2,
        (b2[0] + math.cos(angle + spread) * head, b2[1] + math.sin(angle + spread) * head),
        (b2[0] + math.cos(angle - spread) * head, b2[1] + math.sin(angle - spread) * head),
    ]
    draw.polygon([xy(p) for p in pts], fill=blend(color, alpha))


def draw_axes(draw: ImageDraw.ImageDraw, origin: Vec2, scale: float) -> None:
    for endpoint in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)):
        arrow(draw, mul(-0.16, endpoint), mul(2.45, endpoint), origin, scale, COORD, 1.8, 1.0)
    arrow(draw, mul(-0.10, U), mul(2.35, U), origin, scale, AXIS, 3.2, 1.0)
    o = project((0.0, 0.0, 0.0), origin, scale)
    circle(draw, (o[0], o[1]), 4.0, AXIS, 1.0)


def draw_orbit(draw: ImageDraw.ImageDraw, v: Vec3, origin: Vec2, scale: float, color: tuple[int, int, int], alpha: float = 1.0) -> None:
    pts3 = orbit(v)
    pts2 = [(project(p, origin, scale)[0], project(p, origin, scale)[1]) for p in pts3]
    line(draw, pts2 + [pts2[0]], color, 2.8, alpha)
    for p in pts2:
        circle(draw, p, 4.4, color, alpha)


def pil_rotation_flip() -> Image.Image:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    left_origin = (265.0, 560.0)
    right_origin = (865.0, 560.0)
    scale = 150.0
    v = sample(1.28, 1.06, math.radians(15.0))
    draw.line([(WIDTH * SCALE // 2, 46 * SCALE), (WIDTH * SCALE // 2, (HEIGHT - 44) * SCALE)], fill=(235, 235, 235), width=2)
    for origin in (left_origin, right_origin):
        draw_axes(draw, origin, scale)
    draw_orbit(draw, v, left_origin, scale, RUST, 0.9)
    arrow(draw, (0.0, 0.0, 0.0), rotate_about_axis(v, 120.0), left_origin, scale, TEAL, 4.0, 1.0)

    reflected = reflect_in_plane(v)
    p0 = project(v, right_origin, scale)
    p1 = project(reflected, right_origin, scale)
    line(draw, [(p0[0], p0[1]), (p1[0], p1[1])], RUST, 2.6, 0.8)
    circle(draw, (p0[0], p0[1]), 4.5, RUST, 0.75)
    circle(draw, (p1[0], p1[1]), 4.5, RUST, 0.75)
    arrow(draw, (0.0, 0.0, 0.0), reflected, right_origin, scale, TEAL, 4.0, 1.0)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def pil_stack_collapse() -> Image.Image:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    origin = (360.0, 570.0)
    scale = 155.0
    draw_axes(draw, origin, scale)
    samples = [
        (sample(2.00, 1.08, math.radians(15.0)), TEAL),
        (sample(1.40, 0.78, math.radians(15.0)), RUST),
        (sample(0.85, 0.52, math.radians(15.0)), PURPLE),
    ]
    for v, color in samples:
        draw_orbit(draw, v, origin, scale, color, 0.9)
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def mpl_rotation_flip() -> Image.Image | None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception:
        return None

    fig = plt.figure(figsize=(12, 7.2), dpi=120)
    v = np.array(sample(1.28, 1.06, math.radians(15.0)))
    axes = [fig.add_subplot(1, 2, 1, projection="3d"), fig.add_subplot(1, 2, 2, projection="3d")]
    for ax in axes:
        ax.view_init(elev=23, azim=-42)
        ax.set_xlim(-0.25, 2.5)
        ax.set_ylim(-0.25, 2.5)
        ax.set_zlim(-0.25, 2.5)
        ax.set_axis_off()
        for endpoint in np.eye(3):
            ax.quiver(0, 0, 0, endpoint[0] * 2.3, endpoint[1] * 2.3, endpoint[2] * 2.3, color="#BBBBBB", arrow_length_ratio=0.06, linewidth=1.3)
        ax.quiver(0, 0, 0, U[0] * 2.25, U[1] * 2.25, U[2] * 2.25, color="#111111", arrow_length_ratio=0.06, linewidth=2.5)
    pts = np.array(orbit(tuple(v)))
    axes[0].plot([*pts[:, 0], pts[0, 0]], [*pts[:, 1], pts[0, 1]], [*pts[:, 2], pts[0, 2]], color="#B05334", linewidth=2.2)
    rv = np.array(rotate_about_axis(tuple(v), 120.0))
    axes[0].quiver(0, 0, 0, rv[0], rv[1], rv[2], color="#226B80", arrow_length_ratio=0.10, linewidth=2.5)
    fv = np.array(reflect_in_plane(tuple(v)))
    axes[1].plot([v[0], fv[0]], [v[1], fv[1]], [v[2], fv[2]], color="#B05334", linewidth=2.2)
    axes[1].quiver(0, 0, 0, fv[0], fv[1], fv[2], color="#226B80", arrow_length_ratio=0.10, linewidth=2.5)

    OUT.mkdir(parents=True, exist_ok=True)
    temp = OUT / "_mpl_rotation_flip.png"
    fig.savefig(temp, facecolor="white", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    return Image.open(temp).convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_comparison() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    pil_a = pil_rotation_flip()
    pil_b = pil_stack_collapse()
    mpl = mpl_rotation_flip()

    pil_a.save(OUT / "prototype-pil-rotations-flips.png")
    pil_b.save(OUT / "prototype-pil-stack.png")
    if mpl is not None:
        mpl.save(OUT / "prototype-mpl-rotations-flips.png")

    images = [pil_a, pil_b]
    labels = ["PIL custom projection: rotations/flips still", "PIL custom projection: stack still"]
    if mpl is not None:
        images.append(mpl)
        labels.append("matplotlib mplot3d: rotations/flips still")

    thumb_w, thumb_h = 520, 330
    sheet = Image.new("RGB", (thumb_w * len(images), thumb_h + 36), (246, 246, 246))
    draw = ImageDraw.Draw(sheet)
    for idx, img in enumerate(images):
        thumb = img.copy()
        thumb.thumbnail((thumb_w - 20, thumb_h - 20), Image.Resampling.LANCZOS)
        x = idx * thumb_w + (thumb_w - thumb.width) // 2
        y = 10
        sheet.paste(thumb, (x, y))
        draw.text((idx * thumb_w + 14, thumb_h + 8), labels[idx], fill=(70, 70, 70))
    output = OUT / "tooling-comparison.png"
    sheet.save(output)
    return output


def main() -> None:
    print(make_comparison())


if __name__ == "__main__":
    main()
