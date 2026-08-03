from __future__ import annotations

import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 240

BG = (255, 252, 246)
PANEL = (248, 244, 235)
PANEL_ALT = (242, 238, 229)
INK = (37, 39, 42)
MUTED = (105, 104, 100)
FAINT = (220, 215, 206)
GRID = (167, 177, 177)
TEAL = (36, 122, 127)
RUST = (181, 78, 55)
GOLD = (201, 148, 49)
ARCADE_BG = (18, 24, 30)
ARCADE_LINE = (226, 239, 236)

FLAT_LEFT = 145.0
FLAT_RIGHT = 1135.0
FLAT_TOP = 185.0
FLAT_BOTTOM = 590.0
FLAT_WIDTH = FLAT_RIGHT - FLAT_LEFT
FLAT_HEIGHT = FLAT_BOTTOM - FLAT_TOP
CYLINDER_CENTER = (640.0, (FLAT_TOP + FLAT_BOTTOM) / 2)
CYLINDER_RADIUS = 232.0
CYLINDER_HEIGHT = 350.0


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
SUBTITLE = font(17)
LABEL = font(16)
LABEL_BOLD = font(16, True)
SMALL = font(13)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def interval(value: float, start: float, end: float) -> float:
    return smoothstep((value - start) / (end - start))


def text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str = "mm",
) -> None:
    draw.text((s(xy[0]), s(xy[1])), value, fill=fill, font=font_obj, anchor=anchor)


def material_point(u: float, v: float, flatten: float) -> tuple[float, float, float]:
    """Map the same material point from a closed cylinder to an open strip."""
    theta = 2.0 * math.pi * u - math.pi / 2.0
    depth = CYLINDER_RADIUS * math.cos(theta)
    cylinder_x = CYLINDER_CENTER[0] + CYLINDER_RADIUS * math.sin(theta) + 0.30 * depth
    cylinder_y = CYLINDER_CENTER[1] + v * CYLINDER_HEIGHT / 2.0 - 0.12 * depth

    flat_x = FLAT_LEFT + u * FLAT_WIDTH
    flat_y = CYLINDER_CENTER[1] + v * FLAT_HEIGHT / 2.0
    return (
        cylinder_x + (flat_x - cylinder_x) * flatten,
        cylinder_y + (flat_y - cylinder_y) * flatten,
        depth * (1.0 - flatten),
    )


def draw_arrowhead(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], color, size: float = 10.0) -> None:
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    right = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_strip(image: Image.Image, flatten: float, stage_progress: float) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    columns = 28
    rows = 10
    cells: list[tuple[float, int, int]] = []
    for row in range(rows):
        for column in range(columns):
            center_u = (column + 0.5) / columns
            depth = material_point(center_u, 0.0, flatten)[2]
            cells.append((depth, row, column))
    cells.sort(key=lambda item: item[0])

    for depth, row, column in cells:
        u0 = column / columns
        u1 = (column + 1) / columns
        v0 = -1.0 + 2.0 * row / rows
        v1 = -1.0 + 2.0 * (row + 1) / rows
        points = [
            material_point(u0, v0, flatten),
            material_point(u1, v0, flatten),
            material_point(u1, v1, flatten),
            material_point(u0, v1, flatten),
        ]
        front = 0.5 + 0.5 * max(-1.0, min(1.0, depth / max(1.0, CYLINDER_RADIUS)))
        base = PANEL if (row + column) % 2 == 0 else PANEL_ALT
        shade = tuple(max(0, min(255, round(channel * (0.94 + 0.06 * front)))) for channel in base)
        draw.polygon([(s(x), s(y)) for x, y, _ in points], fill=rgba(shade, 0.94))

    # Grid curves. Back-facing segments are visible but faint until the strip opens.
    for row in range(rows + 1):
        v = -1.0 + 2.0 * row / rows
        for column in range(columns):
            u0 = column / columns
            u1 = (column + 1) / columns
            p0 = material_point(u0, v, flatten)
            p1 = material_point(u1, v, flatten)
            avg_depth = 0.5 * (p0[2] + p1[2])
            front_alpha = 0.26 + 0.42 * (0.5 + 0.5 * max(-1.0, min(1.0, avg_depth / max(1.0, CYLINDER_RADIUS))))
            alpha = front_alpha + (0.58 - front_alpha) * flatten
            draw.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=rgba(GRID, alpha), width=s(1.3))

    for column in range(columns + 1):
        u = column / columns
        points = [material_point(u, -1.0 + 2.0 * row / 80.0, flatten) for row in range(81)]
        depth = material_point(u, 0.0, flatten)[2]
        front_alpha = 0.25 + 0.48 * (0.5 + 0.5 * max(-1.0, min(1.0, depth / max(1.0, CYLINDER_RADIUS))))
        alpha = front_alpha + (0.62 - front_alpha) * flatten
        draw.line([(s(x), s(y)) for x, y, _ in points], fill=rgba(GRID, alpha), width=s(1.2))

    # The coincident edges of the cylinder separate into the two identified edges.
    for u in (0.0, 1.0):
        points = [material_point(u, -1.0 + 2.0 * row / 80.0, flatten) for row in range(81)]
        draw.line([(s(x), s(y)) for x, y, _ in points], fill=rgba(RUST, 0.78), width=s(3.0))

    # A material marker makes it clear that the surface is changing presentation, not identity.
    marker = material_point(0.18, -0.14, flatten)
    draw.ellipse(
        (s(marker[0] - 8), s(marker[1] - 8), s(marker[0] + 8), s(marker[1] + 8)),
        fill=TEAL,
        outline=rgba(BG, 0.9),
        width=s(2),
    )

    if flatten < 0.16:
        # A short tangent arrow around the circumference indicates the periodic translation.
        samples = [material_point(0.09 + 0.14 * index / 30.0, -0.14, flatten) for index in range(31)]
        path = [(s(x), s(y)) for x, y, _ in samples]
        draw.line(path, fill=rgba(TEAL, 0.68), width=s(3))
        draw_arrowhead(draw, (samples[-2][0], samples[-2][1]), (samples[-1][0], samples[-1][1]), rgba(TEAL, 0.76), 9)

    seam_alpha = interval(stage_progress, 0.18, 0.32) * (1.0 - interval(stage_progress, 0.52, 0.60))
    if seam_alpha > 0.0:
        text(draw, (640, 628), "cut one seam and unroll", rgba(RUST, seam_alpha), LABEL_BOLD)


def asteroid_points(cx: float, cy: float, radius: float, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    count = 11
    points: list[tuple[int, int]] = []
    for index in range(count):
        angle = 2.0 * math.pi * index / count
        local_radius = radius * rng.uniform(0.72, 1.12)
        points.append((s(cx + local_radius * math.cos(angle)), s(cy + local_radius * math.sin(angle))))
    return points


def draw_asteroid(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float, seed: int, color, alpha: float, width: float = 2.0) -> None:
    points = asteroid_points(cx, cy, radius, seed)
    draw.line(points + [points[0]], fill=rgba(color, alpha), width=s(width), joint="curve")
    # Two angular inner facets preserve the hand-drawn vector-game look.
    draw.line((s(cx - 0.25 * radius), s(cy - 0.20 * radius), s(cx + 0.18 * radius), s(cy + 0.08 * radius)), fill=rgba(color, alpha * 0.72), width=s(1.2))
    draw.line((s(cx + 0.18 * radius), s(cy + 0.08 * radius), s(cx - 0.05 * radius), s(cy + 0.34 * radius)), fill=rgba(color, alpha * 0.72), width=s(1.2))


def draw_ship(draw: ImageDraw.ImageDraw, cx: float, cy: float, angle: float, alpha: float) -> None:
    local = [(22.0, 0.0), (-15.0, -13.0), (-9.0, 0.0), (-15.0, 13.0)]
    c = math.cos(angle)
    si = math.sin(angle)
    points = [(s(cx + c * x - si * y), s(cy + si * x + c * y)) for x, y in local]
    draw.line(points + [points[0]], fill=rgba(ARCADE_LINE, alpha), width=s(2.0), joint="curve")
    flame = [(-15.0, -6.0), (-27.0, 0.0), (-15.0, 6.0)]
    flame_points = [(s(cx + c * x - si * y), s(cy + si * x + c * y)) for x, y in flame]
    draw.line(flame_points, fill=rgba(GOLD, alpha * 0.9), width=s(1.6))


def make_arcade_screen(progress: float, alpha: float) -> Image.Image:
    logical_width = int(round(FLAT_WIDTH))
    logical_height = int(round(FLAT_HEIGHT))
    screen = Image.new("RGBA", (logical_width * SCALE, logical_height * SCALE), rgba(ARCADE_BG, alpha))
    draw = ImageDraw.Draw(screen, "RGBA")

    rng = random.Random(7321)
    for _ in range(50):
        x = rng.uniform(12.0, logical_width - 12.0)
        y = rng.uniform(12.0, logical_height - 12.0)
        radius = rng.choice((0.9, 1.2, 1.6))
        draw.ellipse((s(x - radius), s(y - radius), s(x + radius), s(y + radius)), fill=rgba(ARCADE_LINE, alpha * rng.uniform(0.32, 0.72)))

    drift = 18.0 * progress
    draw_asteroid(draw, 165.0 + 0.25 * drift, 90.0, 34.0, 4, ARCADE_LINE, alpha * 0.70)
    draw_asteroid(draw, 310.0 - 0.18 * drift, 315.0, 25.0, 8, ARCADE_LINE, alpha * 0.62)
    draw_asteroid(draw, 660.0 + 0.12 * drift, 78.0, 28.0, 11, ARCADE_LINE, alpha * 0.66)
    draw_asteroid(draw, 775.0 - 0.20 * drift, 330.0, 40.0, 21, ARCADE_LINE, alpha * 0.58)
    draw_ship(draw, 500.0, 226.0, -0.18, alpha)

    # This asteroid crosses the identified right edge and appears at the left edge.
    unwrapped_x = 820.0 + 390.0 * progress
    for x in (unwrapped_x, unwrapped_x - logical_width, unwrapped_x + logical_width):
        if -48.0 <= x <= logical_width + 48.0:
            draw_asteroid(draw, x, 155.0, 33.0, 93, GOLD, alpha, 2.8)

    return screen


def draw_arcade(image: Image.Image, stage_progress: float, alpha: float) -> None:
    if alpha <= 0.0:
        return
    arcade_progress = interval(stage_progress, 0.72, 0.98)
    screen = make_arcade_screen(arcade_progress, alpha)
    image.alpha_composite(screen, (s(FLAT_LEFT), s(FLAT_TOP)))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle(
        (s(FLAT_LEFT), s(FLAT_TOP), s(FLAT_RIGHT), s(FLAT_BOTTOM)),
        outline=rgba(ARCADE_LINE, alpha * 0.9),
        width=s(2.2),
    )

    # Identified horizontal edges are named directly above the playfield.
    label_alpha = alpha * interval(stage_progress, 0.66, 0.75)
    text(draw, (FLAT_LEFT, 158), "left edge", rgba(RUST, label_alpha), SMALL, "lm")
    text(draw, (FLAT_RIGHT, 158), "right edge", rgba(RUST, label_alpha), SMALL, "rm")
    draw.line((s(FLAT_LEFT + 72), s(158), s(FLAT_RIGHT - 82), s(158)), fill=rgba(RUST, label_alpha * 0.75), width=s(1.5))
    draw_arrowhead(draw, (FLAT_LEFT + 92, 158), (FLAT_LEFT + 72, 158), rgba(RUST, label_alpha), 8)
    draw_arrowhead(draw, (FLAT_RIGHT - 102, 158), (FLAT_RIGHT - 82, 158), rgba(RUST, label_alpha), 8)


def draw_frame(frame: int) -> Image.Image:
    progress = frame / (FRAMES - 1)
    flatten = interval(progress, 0.18, 0.52)
    arcade_alpha = interval(progress, 0.60, 0.72)

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    text(draw, (640, 48), "Unrolling a cylinder reveals its wraparound topology", INK, TITLE)
    text(draw, (640, 82), "The identified seam becomes the left and right edges of a flat screen", MUTED, SUBTITLE)

    draw_strip(image, flatten, progress)
    draw_arcade(image, progress, arcade_alpha)

    footer_alpha = interval(progress, 0.74, 0.83)
    if footer_alpha > 0.02:
        text(draw, (640, 657), "Local translations commute; the global identification is extra information.", INK, LABEL_BOLD)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    samples = [0, 54, 92, 124, 174, 239]
    thumb_width = 400
    thumb_height = 225
    label_height = 24
    margin = 15
    sheet = Image.new("RGB", (3 * thumb_width + 4 * margin, 2 * (thumb_height + label_height) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        column = index % 3
        row = index // 3
        x = margin + column * (thumb_width + margin)
        y = margin + row * (thumb_height + label_height + margin)
        thumb = draw_frame(frame).resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 5, y + thumb_height + 4), f"frame {frame:03d}", fill=MUTED)
    output = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(output)
    return output


def render() -> tuple[Path, Path]:
    name = "symmetry-cylinder-topology-wrap"
    scratch = OUTPUT_DIR / f"_{name}_frames"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return video, make_contact_sheet(name)
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    for output in render():
        print(output)


if __name__ == "__main__":
    main()
