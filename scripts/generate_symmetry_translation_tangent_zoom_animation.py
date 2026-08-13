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
FRAMES = 360

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


TITLE = font(25, True)
LABEL = font(18)
SMALL = font(15)


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
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


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
    left, top, right, bottom = 66, 104, 1214, 650

    def to_screen(x: float, y: float) -> tuple[float, float]:
        px = left + (x - x_min) / (x_max - x_min) * (right - left)
        py = bottom - (y - y_min) / (y_max - y_min) * (bottom - top)
        return px, py

    return to_screen


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    t = frame / (FRAMES - 1)
    zoom = ease(ease((t - 0.14) / 0.68))

    # The two marked arguments are genuinely close on the original graph. The
    # camera closes in on that fixed pair, making their local segment readable.
    x_ref = 1.92
    displacement = 0.035
    x_shift = x_ref - displacement
    x_center = 0.5 * (x_ref + x_shift)
    y_center = 0.5 * (f(x_ref) + f(x_shift))

    x_span = log_lerp(10.5, 0.105, zoom)
    y_span = log_lerp(2.40, 0.070, zoom)
    x_min = x_center - 0.5 * x_span
    x_max = x_center + 0.5 * x_span
    y_min = y_center - 0.5 * y_span
    y_max = y_center + 0.5 * y_span
    to_screen = make_mapper(x_min, x_max, y_min, y_max)

    draw_text(draw, (64, 42), "Every smooth curve looks straight up close", font_obj=TITLE)

    # A restrained camera-frame cue expands with the zoom and then disappears.
    # It is the final field of view expressed in the current camera coordinates.
    final_x_span = 0.105
    final_y_span = 0.070
    view_left, view_top = to_screen(x_center - final_x_span / 2, y_center + final_y_span / 2)
    view_right, view_bottom = to_screen(x_center + final_x_span / 2, y_center - final_y_span / 2)
    frame_alpha = 0.46 * (1.0 - ease((zoom - 0.66) / 0.30))
    corner = min(28.0, 0.22 * (view_right - view_left), 0.22 * (view_bottom - view_top))
    frame_color = rgba(MUTED, frame_alpha)
    if frame_alpha > 0.01:
        for x1, y1, x2, y2 in [
            (view_left, view_top, view_left + corner, view_top),
            (view_left, view_top, view_left, view_top + corner),
            (view_right - corner, view_top, view_right, view_top),
            (view_right, view_top, view_right, view_top + corner),
            (view_left, view_bottom, view_left + corner, view_bottom),
            (view_left, view_bottom - corner, view_left, view_bottom),
            (view_right - corner, view_bottom, view_right, view_bottom),
            (view_right, view_bottom - corner, view_right, view_bottom),
        ]:
            draw.line((s(x1), s(y1), s(x2), s(y2)), fill=frame_color, width=s(2))

    # The wiggly global function simplifies naturally as the camera closes in.
    curve = []
    samples = 520
    for i in range(samples):
        x = x_min + (x_max - x_min) * i / (samples - 1)
        curve.append(tuple(s(v) for v in to_screen(x, f(x))))
    draw.line(curve, fill=BLUE, width=s(5), joint="curve")

    # The actual tangent arrives only after the curve has nearly become it.
    tangent_alpha = ease((zoom - 0.68) / 0.27)
    if tangent_alpha > 0:
        tan_line = []
        for i in range(samples):
            x = x_min + (x_max - x_min) * i / (samples - 1)
            tan_line.append(tuple(s(v) for v in to_screen(x, tangent(x, x_ref))))
        draw.line(tan_line, fill=rgba(GOLD, 0.82 * tangent_alpha), width=s(3))

    # Two fixed, nearby points become visibly separated only because of zoom.
    p_shift = to_screen(x_shift, f(x_shift))
    p_ref = to_screen(x_ref, f(x_ref))
    dot_radius = 2
    for px, py in (p_shift, p_ref):
        draw.ellipse(
            (s(px - dot_radius), s(py - dot_radius), s(px + dot_radius), s(py + dot_radius)),
            fill=RED,
            outline=BG,
            width=s(1),
        )

    label_alpha = ease((zoom - 0.52) / 0.26)
    if label_alpha > 0:
        draw_text(
            draw,
            (p_shift[0], p_shift[1] + 34),
            "x-a",
            fill=rgba(INK, label_alpha),
            font_obj=SMALL,
            anchor="mm",
        )
        draw_text(
            draw,
            (p_ref[0], p_ref[1] + 34),
            "x",
            fill=rgba(INK, label_alpha),
            font_obj=SMALL,
            anchor="mm",
        )

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    samples = [0, 56, 120, 184, 256, 340]
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
        draw.text((x + 8, y + thumb_h + 6), f"{round(frame / (FRAMES - 1) * 100)}%", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(out)
    return out


def render() -> tuple[Path, Path]:
    name = "symmetry-translation-tangent-zoom"
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
        contact = make_contact_sheet(name)
        return video, contact
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact = render()
    print(video)
    print(contact)


if __name__ == "__main__":
    main()
