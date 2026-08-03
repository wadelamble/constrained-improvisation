from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_function_translation_shape_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 620
SCALE = 2
FPS = 24
FRAMES = 132

BG = (255, 252, 246)
PANEL = (250, 246, 238)
PANEL_EDGE = (224, 216, 204)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (226, 219, 209)
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


TITLE = font(24, True)
LABEL = font(17)
SMALL = font(13)


def s(value: float) -> int:
    return int(round(value * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in box), radius=s(16), fill=PANEL, outline=PANEL_EDGE, width=s(2))


def graph_point(box: tuple[float, float, float, float], x: float, y: float) -> tuple[int, int]:
    x_min, x_max = -3.4, 3.8
    y_min, y_max = -0.18, 1.38
    px = box[0] + (x - x_min) / (x_max - x_min) * (box[2] - box[0])
    py = box[3] - (y - y_min) / (y_max - y_min) * (box[3] - box[1])
    return s(px), s(py)


def base_shape(x: float) -> float:
    return (
        0.82 * math.exp(-((x + 1.18) ** 2) / 0.42)
        + 0.48 * math.exp(-((x - 0.35) ** 2) / 0.15)
        + 0.26 * math.exp(-((x - 1.18) ** 2) / 0.28)
    )


def distorted_shape(x: float, amount: float) -> float:
    stretch = 1.0 + 0.42 * amount
    skew = 0.28 * amount
    height = 1.0 - 0.28 * amount
    wobble = 0.12 * amount * math.exp(-((x - 0.5) ** 2) / 1.8) * math.sin(3.2 * x)
    return max(0.0, height * base_shape((x - skew) / stretch) + wobble)


def draw_axes(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    y0 = graph_point(box, 0, 0)[1]
    x0 = graph_point(box, 0, 0)[0]
    draw.line((s(box[0]), y0, s(box[2]), y0), fill=MUTED, width=s(2))
    draw.line((x0, s(box[1]), x0, s(box[3])), fill=rgba(MUTED, 0.45), width=s(2))


def draw_curve(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fn,
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 5,
) -> None:
    points = []
    for index in range(280):
        x = -3.4 + 7.2 * index / 279
        points.append(graph_point(box, x, fn(x)))
    draw.line(points, fill=color, width=s(width), joint="curve")


def shifted_shape(shift: float):
    return lambda x: base_shape(x - shift)


def shifted_distorted_shape(shift: float, amount: float):
    return lambda x: distorted_shape(x - shift, amount)


def draw_frame(frame: int) -> Image.Image:
    phase = ease(frame / (FRAMES - 1))
    shift = 2.1 * phase

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    left_panel = (48, 58, 618, 554)
    right_panel = (662, 58, 1232, 554)
    left_graph = (82, 176, 584, 494)
    right_graph = (696, 176, 1198, 494)
    draw_panel(draw, left_panel)
    draw_panel(draw, right_panel)

    draw_text(draw, (82, 92), "translation symmetry", font_obj=TITLE)
    draw_text(draw, (82, 128), "shape preserved", fill=BLUE, font_obj=LABEL)
    draw_text(draw, (696, 92), "not a translation symmetry", font_obj=TITLE)
    draw_text(draw, (696, 128), "shape distorted", fill=RED, font_obj=LABEL)

    draw_axes(draw, left_graph)
    draw_axes(draw, right_graph)

    # Ghosts show the starting shape.
    draw_curve(draw, left_graph, base_shape, rgba(BLUE, 0.22), width=4)
    draw_curve(draw, right_graph, base_shape, rgba(RED, 0.22), width=4)

    draw_curve(draw, left_graph, shifted_shape(shift), BLUE, width=5)
    draw_curve(draw, right_graph, shifted_distorted_shape(shift, phase), RED, width=5)

    draw_text(draw, (318, 522), "same values, new position", fill=BLUE, font_obj=SMALL, anchor="mm")
    draw_text(draw, (932, 522), "new position and new shape", fill=RED, font_obj=SMALL, anchor="mm")

    # Small motion arrows.
    arrow_y = 154
    draw.line((s(212), s(arrow_y), s(378), s(arrow_y)), fill=GOLD, width=s(3))
    draw.polygon([(s(378), s(arrow_y)), (s(362), s(arrow_y - 8)), (s(362), s(arrow_y + 8))], fill=GOLD)
    draw.line((s(826), s(arrow_y), s(992), s(arrow_y)), fill=GOLD, width=s(3))
    draw.polygon([(s(992), s(arrow_y)), (s(976), s(arrow_y - 8)), (s(976), s(arrow_y + 8))], fill=GOLD)

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    samples = [0, 26, 52, 78, 104, 131]
    thumb_w = 400
    thumb_h = 194
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
        draw.text((x + 8, y + thumb_h + 6), f"{round(frame / (FRAMES - 1) * 100)}%", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / "symmetry-function-translation-shape-contact-sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video = OUTPUT_DIR / "symmetry-function-translation-shape.mp4"

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
