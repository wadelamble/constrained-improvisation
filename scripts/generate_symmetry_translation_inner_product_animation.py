from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_translation_inner_product_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 192

BG = (255, 252, 246)
INK = (35, 36, 38)
TEXT_MUTED = (91, 87, 81)
GRID = (226, 219, 209)
GRID_MAJOR = (205, 198, 188)
AXIS = (158, 151, 141)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (196, 132, 42)


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
LABEL = font(18)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 6,
    head: float = 20.0,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (
        end[0] - head * math.cos(angle - math.pi / 7),
        end[1] - head * math.sin(angle - math.pi / 7),
    )
    right = (
        end[0] - head * math.cos(angle + math.pi / 7),
        end[1] - head * math.sin(angle + math.pi / 7),
    )
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


def point_at(origin: tuple[float, float], length: float, angle_degrees: float) -> tuple[float, float]:
    angle = math.radians(angle_degrees)
    return origin[0] + length * math.cos(angle), origin[1] - length * math.sin(angle)


def motion_for_frame(frame: int) -> float:
    # Brief holds make the unchanged vector pair easy to compare before and after.
    t = frame / (FRAMES - 1)
    return smoothstep((t - 0.12) / 0.76)


def draw_grid(draw: ImageDraw.ImageDraw, motion: float) -> None:
    left, top, right, bottom = 58.0, 138.0, 1222.0, 616.0
    spacing = 82.0
    half_spacing = spacing / 2.0
    origin_x = 1040.0 - 680.0 * motion
    origin_y = 526.0

    # Minor and major horizontal lines remain fixed under a horizontal translation.
    first_minor_y = origin_y - math.ceil((origin_y - top) / half_spacing) * half_spacing
    y = first_minor_y
    while y <= bottom:
        index = round((origin_y - y) / half_spacing)
        color = GRID_MAJOR if index % 2 == 0 else GRID
        width = 2 if index % 2 == 0 else 1
        draw.line((s(left), s(y), s(right), s(y)), fill=color, width=s(width))
        y += half_spacing

    # Vertical grid lines, tick labels, and the y-axis all slide left.
    first_minor_x = origin_x - math.ceil((origin_x - left) / half_spacing) * half_spacing
    x = first_minor_x
    while x <= right:
        index = round((x - origin_x) / half_spacing)
        color = GRID_MAJOR if index % 2 == 0 else GRID
        width = 2 if index % 2 == 0 else 1
        draw.line((s(x), s(top), s(x), s(bottom)), fill=color, width=s(width))
        x += half_spacing

    draw.line((s(left), s(origin_y), s(right), s(origin_y)), fill=AXIS, width=s(3))
    if left <= origin_x <= right:
        draw.line((s(origin_x), s(top), s(origin_x), s(bottom)), fill=AXIS, width=s(3))
        draw_text(draw, (origin_x - 13, top + 16), "y", fill=TEXT_MUTED, font_obj=SMALL, anchor="rm")

    # Integer x-coordinate labels make the movement of the background unmistakable.
    first_index = math.ceil((left - origin_x) / spacing)
    last_index = math.floor((right - origin_x) / spacing)
    for index in range(first_index, last_index + 1):
        x = origin_x + index * spacing
        draw.line((s(x), s(origin_y - 7), s(x), s(origin_y + 7)), fill=AXIS, width=s(2))
        if index != 0:
            draw_text(draw, (x, origin_y + 25), str(index), fill=TEXT_MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, (right - 10, origin_y - 18), "x", fill=TEXT_MUTED, font_obj=SMALL, anchor="rm")


def draw_angle_arc(draw: ImageDraw.ImageDraw, origin: tuple[float, float]) -> None:
    radius = 67.0
    box = (
        s(origin[0] - radius),
        s(origin[1] - radius),
        s(origin[0] + radius),
        s(origin[1] + radius),
    )
    draw.arc(box, start=-60, end=0, fill=GOLD, width=s(5))
    label = point_at(origin, 96.0, 30.0)
    draw_text(draw, label, "60°", fill=GOLD, font_obj=LABEL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    motion = motion_for_frame(frame)
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)

    draw_text(draw, (58, 46), "Translation preserves the dot product", font_obj=TITLE)
    draw_text(
        draw,
        (58, 88),
        "The coordinate grid moves; the vectors' lengths and relative angle do not",
        fill=TEXT_MUTED,
        font_obj=LABEL,
    )

    # A quiet motion key, separate from the geometric content.
    draw_arrow(draw, (1130, 108), (965, 108), GOLD, width=4, head=15)
    draw_text(draw, (1048, 82), "grid translation", fill=GOLD, font_obj=SMALL, anchor="mm")

    draw_grid(draw, motion)

    origin = (610.0, 410.0)
    long_end = point_at(origin, 250.0, 0.0)
    short_end = point_at(origin, 195.0, 60.0)

    draw_arrow(draw, origin, long_end, BLUE, width=7, head=22)
    draw_arrow(draw, origin, short_end, RED, width=7, head=22)
    draw_angle_arc(draw, origin)
    draw.ellipse((s(origin[0] - 7), s(origin[1] - 7), s(origin[0] + 7), s(origin[1] + 7)), fill=INK)

    draw_text(draw, (long_end[0] + 25, long_end[1] - 5), "u", fill=BLUE, font_obj=LABEL, anchor="lm")
    draw_text(draw, (short_end[0] + 8, short_end[1] - 18), "v", fill=RED, font_obj=LABEL, anchor="lm")

    draw_text(
        draw,
        (WIDTH / 2, 669),
        "u · v = |u||v| cos 60° remains unchanged",
        fill=TEXT_MUTED,
        font_obj=LABEL,
        anchor="mm",
    )

    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet() -> Path:
    samples = [0, 38, 76, 114, 152, 191]
    thumb_w = 400
    thumb_h = 225
    label_h = 28
    margin = 18
    cols = 3
    rows = 2
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text(
            (x + 8, y + thumb_h + 6),
            f"{round(frame / (FRAMES - 1) * 100)}%",
            fill=(96, 92, 86),
            font=SMALL,
        )
    output = OUTPUT_DIR / "symmetry-translation-inner-product-contact-sheet.png"
    sheet.save(output)
    return output


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video = OUTPUT_DIR / "symmetry-translation-inner-product.mp4"

    try:
        for index in range(FRAMES):
            draw_frame(index).save(SCRATCH / f"frame_{index:04d}.png")
        subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(SCRATCH / "frame_%04d.png"),
                "-c:v",
                "libx264",
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
        print(video)
        print(make_contact_sheet())
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


if __name__ == "__main__":
    main()
