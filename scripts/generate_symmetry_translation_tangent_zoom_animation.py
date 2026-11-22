from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
sys.path.insert(0, str(ROOT / ".tools" / "animation-python-packages"))
import imageio_ffmpeg
import matplotlib
matplotlib.use("Agg")
from matplotlib.mathtext import math_to_image

NAME = "symmetry-translation-tangent-zoom"
PREVIEW_DIR = ROOT / ".tools" / "taylor-zoom-review"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 432
X_REF = 0.2
PLOT = (80, 150, 1200, 605)

BG = (255, 252, 246)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
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


TITLE = font(32, True)
LABEL = font(23)
SMALL = font(20)


def s(value: float) -> int:
    return int(round(value * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def log_lerp(a: float, b: float, t: float) -> float:
    return a * ((b / a) ** t)


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
    bounds = draw.textbbox((s(xy[0]), s(xy[1])), text, font=font_obj, anchor=anchor)
    assert bounds[0] >= 20 * SCALE and bounds[1] >= 20 * SCALE, (text, bounds)
    assert bounds[2] <= (WIDTH - 20) * SCALE and bounds[3] <= (HEIGHT - 20) * SCALE, (text, bounds)
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def faded(color, alpha):
    return tuple(round(b + alpha * (c - b)) for b, c in zip(BG, color))


@lru_cache(20)
def math_image(tex, size=25, color=INK):
    buffer = BytesIO()
    with matplotlib.rc_context({"mathtext.fontset": "stix", "savefig.transparent": True}):
        math_to_image("$" + tex + "$", buffer, format="png", dpi=144,
                      prop=matplotlib.font_manager.FontProperties(size=size),
                      color=tuple(c / 255 for c in color))
    buffer.seek(0)
    return Image.open(buffer).convert("RGBA")


def put_math(image, tex, xy, size=25, color=INK, alpha=1.0, anchor="mm"):
    mark = math_image(tex, size, color).copy()
    if alpha < 1:
        mark.putalpha(mark.getchannel("A").point(lambda value: round(value * alpha)))
    x, y = s(xy[0]), s(xy[1])
    if anchor[0] == "m":
        x -= mark.width // 2
    elif anchor[0] == "r":
        x -= mark.width
    if anchor[1] == "m":
        y -= mark.height // 2
    assert 20 * SCALE <= x and 20 * SCALE <= y, (tex, x, y)
    assert x + mark.width <= (WIDTH - 20) * SCALE and y + mark.height <= (HEIGHT - 20) * SCALE, tex
    image.paste(mark, (x, y), mark)


def arrow(draw, start, end, color):
    draw.line(tuple(s(v) for point in (start, end) for v in point), fill=color, width=s(2))
    theta = math.atan2(end[1] - start[1], end[0] - start[0])
    tip = [end]
    for offset in (-0.48, 0.48):
        tip.append((end[0] - 10 * math.cos(theta + offset), end[1] - 10 * math.sin(theta + offset)))
    draw.polygon([(s(x), s(y)) for x, y in tip], fill=color)


def f(x: float) -> float:
    """A deliberately irregular but smooth function."""
    return (
        0.46 * math.sin(0.72 * x + 0.35)
        + 0.24 * math.sin(1.65 * x - 0.60)
        + 0.13 * math.sin(3.35 * x + 1.10)
        + 0.04 * x
    )


def fp(x: float) -> float:
    return (
        0.46 * 0.72 * math.cos(0.72 * x + 0.35)
        + 0.24 * 1.65 * math.cos(1.65 * x - 0.60)
        + 0.13 * 3.35 * math.cos(3.35 * x + 1.10)
        + 0.04
    )


def tangent(x: float, x0: float) -> float:
    return f(x0) + fp(x0) * (x - x0)


def make_mapper(x_min: float, x_max: float, y_min: float, y_max: float):
    left, top, right, bottom = PLOT

    def to_screen(x: float, y: float) -> tuple[float, float]:
        px = left + (x - x_min) / (x_max - x_min) * (right - left)
        py = bottom - (y - y_min) / (y_max - y_min) * (bottom - top)
        return px, py

    return to_screen


def geometry(frame):
    seconds = frame / FPS
    progress = ease((seconds - 3.0) / 10.5)
    x_span = log_lerp(8.0, 0.02, progress)
    left, top, right, bottom = PLOT
    y_span = x_span * (bottom - top) / (right - left)
    # A true uniform zoom about a fixed point on the curve. The displacement
    # shrinks with the view, so the first-order remainder vanishes on screen.
    x_min = X_REF - (860 - left) / (right - left) * x_span
    y_max = f(X_REF) + (290 - top) / (bottom - top) * y_span
    mapper = make_mapper(x_min, x_min + x_span, y_max - y_span, y_max)
    return seconds, x_span, x_min, mapper, 0.28 * x_span


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    seconds, x_span, x_min, to_screen, displacement = geometry(frame)
    tangent_alpha = ease((seconds - 1.4) / 1.4)
    detail_alpha = ease((0.19 - displacement) / 0.09)
    draw_text(draw, (64, 36), "Visualizing the Taylor expansion", font_obj=TITLE)
    draw_text(draw, (1196, 105), f"Zoom ×{8.0 / x_span:.0f}", font_obj=SMALL, anchor="rm")
    draw.line((s(66), s(110), s(106), s(110)), fill=BLUE, width=s(4))
    draw_text(draw, (119, 110), "Function", font_obj=SMALL, anchor="lm")
    draw.line((s(260), s(110), s(300), s(110)), fill=faded(GOLD, tangent_alpha), width=s(3))
    draw_text(draw, (313, 110), "Tangent", fill=faded(INK, tangent_alpha), font_obj=SMALL, anchor="lm")

    plot = Image.new("RGB", image.size, BG)
    pd = ImageDraw.Draw(plot)
    curve = []
    for i in range(850):
        x = x_min + x_span * i / 849
        curve.append(tuple(s(v) for v in to_screen(x, f(x))))
    pd.line(curve, fill=BLUE, width=s(4), joint="curve")
    pd.line([tuple(s(v) for v in to_screen(x, tangent(x, X_REF)))
             for x in (x_min, x_min + x_span)], fill=faded(GOLD, tangent_alpha), width=s(2.5))
    box = tuple(s(v) for v in PLOT)
    image.paste(plot.crop(box), box[:2])

    ref = to_screen(X_REF, f(X_REF))
    shifted = to_screen(X_REF - displacement, f(X_REF - displacement))
    estimate = to_screen(X_REF - displacement, tangent(X_REF - displacement, X_REF))
    corner = (estimate[0], ref[1])
    if detail_alpha > 0:
        tone = faded(GOLD, detail_alpha)
        arrow(draw, ref, corner, tone)
        arrow(draw, corner, estimate, tone)
        pdx, pdy = corner
        draw.line([(s(pdx + 13), s(pdy)), (s(pdx + 13), s(pdy + 13)),
                   (s(pdx), s(pdy + 13))], fill=tone, width=s(1))
        put_math(image, r"-a", ((ref[0] + corner[0]) / 2, ref[1] - 24), alpha=detail_alpha)
        put_math(image, r"-a f'(x)", (corner[0] - 22, (corner[1] + estimate[1]) / 2),
                 alpha=detail_alpha, anchor="rm")
        draw.line([tuple(s(v) for v in estimate), tuple(s(v) for v in shifted)],
                  fill=faded(RED, detail_alpha), width=s(3))
        px, py = shifted
        draw.ellipse((s(px-5), s(py-5), s(px+5), s(py+5)), fill=faded(BLUE, detail_alpha))
        px, py = estimate
        draw.ellipse((s(px-7), s(py-7), s(px+7), s(py+7)), outline=tone, width=s(2))
        put_math(image, r"f(x-a)", (shifted[0] + 24, shifted[1] + 28),
                 color=BLUE, alpha=detail_alpha, anchor="lm")
        put_math(image, r"f(x-a)\approx f(x)-a f'(x)", (640, 657), size=33, alpha=detail_alpha)
    px, py = ref
    draw.ellipse((s(px-6), s(py-6), s(px+6), s(py+6)), fill=INK, outline=BG, width=s(1.5))
    put_math(image, r"f(x)", (ref[0]+20, ref[1]+24), anchor="lm")
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str, directory=OUTPUT_DIR) -> Path:
    samples = [0, 72, 144, 216, 288, 408]
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
        draw.text((x + 8, y + thumb_h + 4), f"{frame / FPS:.1f} s", fill=(96, 92, 86), font=font(8))
    out = directory / f"{name}-contact-sheet.png"
    sheet.save(out)
    return out


def validate_geometry():
    samples = []
    for a in (0.1, 0.05, 0.025, 0.01, 0.0056):
        error = f(X_REF-a) - tangent(X_REF-a, X_REF)
        samples.append({"a": a, "error": error, "error_over_a_squared": error/a**2,
                        "screen_error_pixels": abs(error) * (PLOT[2]-PLOT[0]) / (a/0.28)})
    assert all(abs(b["error"]) < abs(a["error"]) for a,b in zip(samples,samples[1:]))
    assert samples[-1]["screen_error_pixels"] < 1.3
    for frame in range(FRAMES):
        _, span, _, mapper, a = geometry(frame)
        p = mapper(X_REF, f(X_REF))
        q = mapper(X_REF-a, tangent(X_REF-a, X_REF))
        assert abs(p[0]-860) < 1e-8 and abs(p[1]-290) < 1e-8
        assert abs((q[1]-p[1])/(p[0]-q[0])-fp(X_REF)) < 1e-8
        assert abs(a/span-0.28) < 1e-12
    return {"reference_x": X_REF, "slope": fp(X_REF), "taylor_remainders": samples,
            "uniform_zoom_and_fixed_tangent_slope": "checked on every frame"}


def render():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = validate_geometry()
    video = OUTPUT_DIR / f"{NAME}.mp4"
    writer = imageio_ffmpeg.write_frames(str(video), (WIDTH, HEIGHT), fps=FPS,
            codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p", quality=None,
            output_params=["-crf", "18", "-movflags", "+faststart", "-threads", "2"])
    writer.send(None)
    try:
        for index in range(FRAMES):
            writer.send(draw_frame(index).tobytes())
            if index % 96 == 0:
                print(f"Rendered {index}/{FRAMES}", flush=True)
    finally:
        writer.close()
    make_contact_sheet(NAME)
    draw_frame(384).save(OUTPUT_DIR / f"{NAME}-poster.png")
    count, seconds = imageio_ffmpeg.count_frames_and_secs(str(video))
    assert count == FRAMES and abs(seconds-FRAMES/FPS) < 0.1
    report.update({"frame_count": count, "duration_seconds": seconds, "fps": FPS,
                   "width": WIDTH, "height": HEIGHT,
                   "video_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
                   "source_sha256": hashlib.sha256(Path(__file__).read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
                   "source_hash_normalization": "UTF-8 source with LF line endings",
                   "text_bounds": "checked on every rendered frame"})
    (OUTPUT_DIR / f"{NAME}-validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(video, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    if args.preview:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        validate_geometry()
        make_contact_sheet(NAME, PREVIEW_DIR)
        draw_frame(240).save(PREVIEW_DIR / "middle.png")
        draw_frame(408).save(PREVIEW_DIR / "end.png")
        print(PREVIEW_DIR)
    else:
        render()


if __name__ == "__main__":
    main()
