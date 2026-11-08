from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"

WIDTH = 1280
HEIGHT = 620
SCALE = 2
FPS = 24
FRAMES = 192
X_MIN, X_MAX = -3.4, 5.4
SHIFT = 2.1

BG = (255, 252, 246)
PANEL = (250, 246, 238)
PANEL_EDGE = (224, 216, 204)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
REFERENCE = (158, 154, 147)
BLUE = (57, 103, 157)
GOLD = (196, 132, 42)


def find_ffmpeg() -> str:
    configured = os.environ.get("FFMPEG_BINARY")
    if configured and Path(configured).is_file():
        return str(Path(configured))
    system = shutil.which("ffmpeg")
    if system:
        return system
    candidates = sorted((ROOT / ".tools" / "animation-python-packages" /
                         "imageio_ffmpeg" / "binaries").glob("ffmpeg*"))
    for candidate in candidates:
        if candidate.is_file() and candidate.suffix in ("", ".exe"):
            return str(candidate)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError("Install ffmpeg or set FFMPEG_BINARY to its executable.") from exc


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
EQUATION = font(27)
LABEL = font(20)
SMALL = font(17)


def s(value: float) -> int:
    return int(round(value * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


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
    y_min, y_max = -0.12, 1.05
    px = box[0] + (x - X_MIN) / (X_MAX - X_MIN) * (box[2] - box[0])
    py = box[3] - (y - y_min) / (y_max - y_min) * (box[3] - box[1])
    return s(px), s(py)


def base_shape(x: float) -> float:
    return (
        0.82 * math.exp(-((x + 1.18) ** 2) / 0.42)
        + 0.48 * math.exp(-((x - 0.35) ** 2) / 0.15)
        + 0.26 * math.exp(-((x - 1.18) ** 2) / 0.28)
    )


def draw_axes(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    y0 = graph_point(box, 0, 0)[1]
    x0 = graph_point(box, 0, 0)[0]
    draw.line((s(box[0]), y0, s(box[2]), y0), fill=MUTED, width=s(2))
    draw.line((x0, s(box[1]), x0, s(box[3])), fill=PANEL_EDGE, width=s(1))
    draw_text(draw, (x0 / SCALE - 12, y0 / SCALE + 16), "0", fill=MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, (box[2] + 14, y0 / SCALE), "x", fill=INK, font_obj=LABEL, anchor="mm")


def draw_curve(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fn,
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 5,
) -> None:
    points = []
    for index in range(800):
        x = X_MIN + (X_MAX - X_MIN) * index / 799
        points.append(graph_point(box, x, fn(x)))
    draw.line(points, fill=color, width=s(width), joint="curve")


def shifted_shape(shift: float):
    return lambda x: base_shape(x - shift)


def draw_frame(frame: int) -> Image.Image:
    # A short opening hold, one translation, then a final hold. This parameter
    # advances the group action; the animation does not assert an equation of motion.
    shift = SHIFT * ease((frame / FPS - 0.75) / 5.75)

    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)

    panel = (48, 58, 1232, 562)
    graph = (96, 232, 1184, 500)
    draw_panel(draw, panel)

    draw_text(draw, (96, 92), "Translation", font_obj=TITLE)
    draw_text(draw, (1184, 110), "(Tₐ f)(x) = f(x − a)", font_obj=EQUATION, anchor="rm")

    for x, text, color in ((96, "f(x)", REFERENCE), (268, "(Tₐ f)(x)", BLUE)):
        draw.line((s(x), s(165), s(x + 38), s(165)), fill=color, width=s(3))
        draw_text(draw, (x + 50, 165), text, fill=color, font_obj=LABEL, anchor="lm")

    draw_axes(draw, graph)
    draw_curve(draw, graph, base_shape, REFERENCE, width=3)
    draw_curve(draw, graph, shifted_shape(shift), BLUE, width=4)

    # The arrow measures the same displacement as every point of the curve.
    start = graph_point(graph, -1.18, 0)[0]
    end = graph_point(graph, -1.18 + shift, 0)[0]
    if end - start > s(24):
        arrow_y = s(226)
        draw.line((start, arrow_y, end, arrow_y), fill=GOLD, width=s(2))
        draw.polygon([(end, arrow_y), (end - s(10), arrow_y - s(5)), (end - s(10), arrow_y + s(5))], fill=GOLD)
        draw_text(draw, ((start + end) / (2 * SCALE), 210), "a", fill=GOLD, font_obj=LABEL, anchor="mm")

    image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    samples = [0, 36, 72, 108, 144, FRAMES - 1]
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
        draw.text((x + 8, y + thumb_h + 6), f"{frame / FPS:.1f} s", fill=(96, 92, 86), font=font(8))
    out = OUTPUT_DIR / "symmetry-function-translation-shape-contact-sheet.png"
    sheet.save(out)
    return out


def make_poster() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "symmetry-function-translation-shape-poster.png"
    draw_frame(FRAMES - 1).save(out)
    return out


def main() -> None:
    ffmpeg = find_ffmpeg()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video = OUTPUT_DIR / "symmetry-function-translation-shape.mp4"
    temporary_video = video.with_suffix(".rendering.mp4")
    process = subprocess.Popen(
        [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
         "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporary_video)],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for index in range(FRAMES):
            process.stdin.write(draw_frame(index).tobytes())
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError("FFmpeg failed to encode the translation animation.")
        temporary_video.replace(video)
        print(video)
        print(make_contact_sheet())
        print(make_poster())
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        temporary_video.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render one translation acting on a function.")
    parser.add_argument("--poster-only", action="store_true", help="Write the final-frame poster without rendering video.")
    args = parser.parse_args()
    if args.poster_only:
        print(make_poster())
    else:
        main()
