from __future__ import annotations

import math
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
FRAMES = 216

BG = (255, 252, 246)
INK = (37, 39, 42)
MUTED = (112, 107, 99)
FAINT = (224, 217, 207)
BLUE = (51, 121, 183)
RUST = (220, 107, 47)
GREEN = (74, 168, 103)
LIGHT_GREEN = (188, 231, 199)

ROWS = 5
COLUMNS = 16


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


TITLE = font(25, True)
LABEL = font(16)
LABEL_BOLD = font(16, True)
SMALL = font(13)
TINY = font(11)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    *,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def original_point(t: float) -> tuple[float, float]:
    return (
        145.0 + 940.0 * t,
        494.0 - 160.0 * t + 43.0 * math.sin(2.0 * math.pi * t),
    )


def varied_point(t: float) -> tuple[float, float]:
    x, y = original_point(t)
    envelope = math.sin(math.pi * t)
    return (
        x + 39.0 * envelope * math.sin(2.0 * math.pi * t),
        y - 126.0 * envelope * (0.82 + 0.12 * math.sin(4.0 * math.pi * t)),
    )


def between_point(t: float, across: float) -> tuple[float, float]:
    ox, oy = original_point(t)
    vx, vy = varied_point(t)
    return (
        ox + across * (vx - ox),
        oy + across * (vy - oy),
    )


def curve_points(across: float, samples: int = 180) -> list[tuple[float, float]]:
    return [between_point(index / samples, across) for index in range(samples + 1)]


def scaled_points(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(s(x), s(y)) for x, y in points]


def partial_curve(points: list[tuple[float, float]], progress: float) -> list[tuple[float, float]]:
    if progress <= 0.0:
        return []
    if progress >= 1.0:
        return points
    exact = progress * (len(points) - 1)
    whole = int(math.floor(exact))
    fraction = exact - whole
    result = points[: whole + 1]
    x0, y0 = points[whole]
    x1, y1 = points[whole + 1]
    result.append((x0 + fraction * (x1 - x0), y0 + fraction * (y1 - y0)))
    return result


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    *,
    width: float = 3.0,
    head: float = 11.0,
) -> None:
    x0, y0 = start
    x1, y1 = end
    draw.line((s(x0), s(y0), s(x1), s(y1)), fill=color, width=s(width))
    angle = math.atan2(y1 - y0, x1 - x0)
    left = (
        x1 - head * math.cos(angle - math.pi / 6.0),
        y1 - head * math.sin(angle - math.pi / 6.0),
    )
    right = (
        x1 - head * math.cos(angle + math.pi / 6.0),
        y1 - head * math.sin(angle + math.pi / 6.0),
    )
    draw.polygon(scaled_points([(x1, y1), left, right]), fill=color)


def cell_points(column: int, row: int) -> list[tuple[float, float]]:
    t0 = column / COLUMNS
    t1 = (column + 1) / COLUMNS
    a0 = row / ROWS
    a1 = (row + 1) / ROWS
    return [
        between_point(t0, a0),
        between_point(t1, a0),
        between_point(t1, a1),
        between_point(t0, a1),
    ]


def point_around_polygon(points: list[tuple[float, float]], progress: float) -> tuple[float, float]:
    closed = points + [points[0]]
    lengths: list[float] = []
    total = 0.0
    for index in range(len(closed) - 1):
        x0, y0 = closed[index]
        x1, y1 = closed[index + 1]
        length = math.hypot(x1 - x0, y1 - y0)
        lengths.append(length)
        total += length
    target = (progress % 1.0) * total
    passed = 0.0
    for index, length in enumerate(lengths):
        if target <= passed + length:
            local = 0.0 if length == 0.0 else (target - passed) / length
            x0, y0 = closed[index]
            x1, y1 = closed[index + 1]
            return x0 + local * (x1 - x0), y0 + local * (y1 - y0)
        passed += length
    return points[0]


def draw_grid(
    draw: ImageDraw.ImageDraw,
    *,
    reveal: float,
    sweep: float,
    interior_alpha: float,
) -> tuple[int, int]:
    active_exact = max(0.0, min(1.0, sweep)) * COLUMNS
    active_column = min(COLUMNS - 1, int(math.floor(active_exact)))

    for column in range(COLUMNS):
        column_reveal = smoothstep((reveal * COLUMNS - column) / 1.25)
        for row in range(ROWS):
            points = cell_points(column, row)
            if sweep <= 0.0:
                fill_alpha = 0.045 * column_reveal
            elif column < active_column:
                fill_alpha = 0.22
            elif column == active_column:
                fill_alpha = 0.46
            else:
                fill_alpha = 0.045
            draw.polygon(scaled_points(points), fill=rgba(GREEN, fill_alpha))

    grid_alpha = max(0.0, min(1.0, reveal)) * interior_alpha
    if grid_alpha > 0.001:
        for row in range(1, ROWS):
            draw.line(
                scaled_points(curve_points(row / ROWS)),
                fill=rgba(MUTED, 0.46 * grid_alpha),
                width=s(1.0),
                joint="curve",
            )
        for column in range(1, COLUMNS):
            t = column / COLUMNS
            draw.line(
                scaled_points([between_point(t, 0.0), between_point(t, 1.0)]),
                fill=rgba(MUTED, 0.46 * grid_alpha),
                width=s(1.0),
            )

    return active_column, min(ROWS - 1, ROWS // 2)


def stage_values(u: float) -> tuple[float, float, float, float, str]:
    if u < 0.16:
        return smoothstep(u / 0.16), 0.0, 0.0, 1.0, "Begin with one candidate history."
    if u < 0.32:
        return 1.0, smoothstep((u - 0.16) / 0.16), 0.0, 1.0, "Vary it while keeping the same endpoints."
    if u < 0.46:
        return 1.0, 1.0, smoothstep((u - 0.32) / 0.14), 1.0, "Tile the enclosed ribbon in both directions."
    if u < 0.84:
        sweep = smoothstep((u - 0.46) / 0.38)
        return 1.0, 1.0, 1.0, 1.0, "Each local commutator loop contributes a phase shift."
    fade = smoothstep((u - 0.84) / 0.16)
    return 1.0, 1.0, 1.0, 1.0 - 0.88 * fade, "The local contributions add to the total variation."


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    u = frame / (FRAMES - 1)

    original_progress, varied_progress, grid_reveal, interior_alpha, caption = stage_values(u)
    sweep = 0.0 if u < 0.46 else smoothstep((u - 0.46) / 0.38)

    draw_text(draw, (56, 42), "A path variation is a ribbon of local commutator loops", font_obj=TITLE)

    axis_left = 104.0
    axis_bottom = 553.0
    draw.line((s(axis_left), s(axis_bottom), s(1162), s(axis_bottom)), fill=FAINT, width=s(2))
    draw.line((s(axis_left), s(axis_bottom), s(axis_left), s(92)), fill=FAINT, width=s(2))
    draw_text(draw, (1174, axis_bottom + 5), "x", fill=MUTED, font_obj=LABEL)
    draw_text(draw, (axis_left - 10, 78), "k", fill=MUTED, font_obj=LABEL)

    if grid_reveal > 0.0:
        active_column, active_row = draw_grid(
            draw,
            reveal=grid_reveal,
            sweep=sweep,
            interior_alpha=interior_alpha,
        )
    else:
        active_column, active_row = 7, 2

    original = curve_points(0.0)
    varied = curve_points(1.0)
    original_partial = partial_curve(original, original_progress)
    varied_partial = partial_curve(varied, varied_progress)
    if len(original_partial) > 1:
        draw.line(scaled_points(original_partial), fill=BLUE, width=s(4), joint="curve")
    if len(varied_partial) > 1:
        draw.line(scaled_points(varied_partial), fill=RUST, width=s(4), joint="curve")

    if original_progress >= 0.99:
        draw_arrow(draw, original_point(0.91), original_point(0.985), BLUE, width=3.2, head=12.0)
        label_point = original_point(0.72)
        draw_text(
            draw,
            (label_point[0] + 20, label_point[1] + 28),
            "candidate history",
            fill=BLUE,
            font_obj=SMALL,
        )
    if varied_progress >= 0.99:
        draw_arrow(draw, varied_point(0.085), varied_point(0.012), RUST, width=3.2, head=12.0)
        label_point = varied_point(0.72)
        draw_text(
            draw,
            (label_point[0] + 16, label_point[1] - 22),
            "nearby varied history",
            fill=RUST,
            font_obj=SMALL,
        )

    start = original_point(0.0)
    end = original_point(1.0)
    if original_progress > 0.02:
        draw.ellipse(
            (s(start[0] - 6), s(start[1] - 6), s(start[0] + 6), s(start[1] + 6)),
            fill=INK,
        )
    if original_progress >= 0.99:
        draw.ellipse(
            (s(end[0] - 6), s(end[1] - 6), s(end[0] + 6), s(end[1] + 6)),
            fill=INK,
        )

    if 0.34 <= u < 0.90:
        focus_column = active_column if u >= 0.46 else 7
        points = cell_points(focus_column, active_row)
        draw.line(
            scaled_points(points + [points[0]]),
            fill=rgba(GREEN, 0.95),
            width=s(3),
            joint="curve",
        )
        dot_progress = ((u - 0.34) * 8.0) % 1.0
        dot = point_around_polygon(points, dot_progress)
        draw.ellipse(
            (s(dot[0] - 5), s(dot[1] - 5), s(dot[0] + 5), s(dot[1] + 5)),
            fill=GREEN,
            outline=BG,
            width=s(2),
        )
        center_x = sum(point[0] for point in points) / 4.0
        center_y = sum(point[1] for point in points) / 4.0
        label_x = min(790.0, center_x + 80.0)
        label_y = 130.0
        draw.line(
            (s(center_x), s(center_y), s(label_x - 12), s(label_y + 5)),
            fill=rgba(MUTED, 0.72),
            width=s(1),
        )
        draw_text(draw, (label_x, label_y), "one closed local loop", fill=INK, font_obj=SMALL)

    meter_left = 218.0
    meter_top = 606.0
    meter_width = 844.0
    segment_width = meter_width / COLUMNS
    draw_text(draw, (meter_left, meter_top - 24), "accumulated local phase contribution", fill=MUTED, font_obj=SMALL)
    for column in range(COLUMNS):
        x0 = meter_left + column * segment_width
        x1 = x0 + segment_width - 3.0
        draw.rectangle(
            (s(x0), s(meter_top), s(x1), s(meter_top + 17)),
            fill=rgba(FAINT, 0.88),
        )
        if u >= 0.46:
            exact = sweep * COLUMNS
            fill_fraction = max(0.0, min(1.0, exact - column))
            if fill_fraction > 0.0:
                draw.rectangle(
                    (s(x0), s(meter_top), s(x0 + (x1 - x0) * fill_fraction), s(meter_top + 17)),
                    fill=rgba(GREEN, 0.88),
                )

    if u >= 0.84:
        final_alpha = smoothstep((u - 0.84) / 0.16)
        draw_text(
            draw,
            (meter_left + meter_width, meter_top + 43),
            "sum = phase variation between histories",
            fill=rgba(GREEN, final_alpha),
            font_obj=LABEL_BOLD,
            anchor="rs",
        )

    draw_text(draw, (WIDTH / 2, 687), caption, fill=INK, font_obj=LABEL, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_sheet(name: str, dense: bool) -> Path:
    samples = list(range(0, FRAMES, 18)) if dense else [0, 35, 70, 105, 155, 215]
    cols = 4 if dense else 3
    thumb_w = 320 if dense else 400
    thumb_h = 180 if dense else 225
    label_h = 23
    margin = 14
    rows = math.ceil(len(samples) / cols)
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 5, y + thumb_h + 4), f"frame {frame:03d}", fill=MUTED)
    suffix = "dense-motion-qa" if dense else "contact-sheet"
    output = OUTPUT_DIR / f"{name}-{suffix}.png"
    sheet.save(output)
    return output


def render() -> tuple[Path, Path, Path]:
    name = "symmetry-ccr-action-variation"
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
        return video, make_sheet(name, dense=False), make_sheet(name, dense=True)
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    for path in render():
        print(path)


if __name__ == "__main__":
    main()
