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
FRAMES = 168

BG = (255, 252, 246)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (226, 219, 209)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (196, 132, 42)
GREEN = (71, 130, 101)


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


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 4,
    head: float = 14,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_double_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 3,
    head: float = 11,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    for tip, tail in ((start, end), (end, start)):
        angle = math.atan2(tip[1] - tail[1], tip[0] - tail[0])
        left = (tip[0] - head * math.cos(angle - math.pi / 7), tip[1] - head * math.sin(angle - math.pi / 7))
        right = (tip[0] - head * math.cos(angle + math.pi / 7), tip[1] - head * math.sin(angle + math.pi / 7))
        draw.polygon([(s(tip[0]), s(tip[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def helix_point(u: float) -> tuple[float, float, float, float]:
    left = 126
    right = 844
    cy = 318
    radius = 122
    turns = 3.15
    theta = 2 * math.pi * turns * u
    x = left + (right - left) * u
    y = cy - radius * math.sin(theta)
    return x, y, math.cos(theta), math.sin(theta)


def draw_polyline(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], color, width: int) -> None:
    if len(points) < 2:
        return
    draw.line([tuple(s(v) for v in p) for p in points], fill=color, width=s(width), joint="curve")


def draw_component_trace(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fn,
    current_u: float,
    color,
    label: str,
) -> None:
    x0, y0, x1, y1 = box
    mid = (y0 + y1) / 2
    amp = (y1 - y0) * 0.36
    draw.line((s(x0), s(mid), s(x1), s(mid)), fill=rgba(MUTED, 0.6), width=s(2))
    points = []
    for i in range(220):
        u = i / 219
        x = x0 + (x1 - x0) * u
        y = mid - amp * fn(2 * math.pi * 3.15 * u)
        points.append((x, y))
    draw_polyline(draw, points, rgba(color, 0.88), 3)
    cx = x0 + (x1 - x0) * current_u
    cy = mid - amp * fn(2 * math.pi * 3.15 * current_u)
    draw.ellipse((s(cx - 7), s(cy - 7), s(cx + 7), s(cy + 7)), fill=color)
    draw_text(draw, (x0, y0 - 12), label, fill=color, font_obj=SMALL)


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    u = frame / (FRAMES - 1)

    draw_text(draw, (58, 42), "A complex exponential is a rotating value along a line", font_obj=TITLE)

    left = 126
    right = 844
    cy = 318
    radius = 122
    depth = 42

    # Cylinder scaffold.
    draw.ellipse((s(left - depth), s(cy - radius), s(left + depth), s(cy + radius)), outline=rgba(MUTED, 0.55), width=s(2))
    draw.ellipse((s(right - depth), s(cy - radius), s(right + depth), s(cy + radius)), outline=rgba(MUTED, 0.55), width=s(2))
    draw.line((s(left), s(cy - radius), s(right), s(cy - radius)), fill=rgba(MUTED, 0.38), width=s(2))
    draw.line((s(left), s(cy + radius), s(right), s(cy + radius)), fill=rgba(MUTED, 0.38), width=s(2))
    draw_arrow(draw, (left - 60, cy), (right + 86, cy), rgba(MUTED, 0.95), width=3)
    draw_text(draw, (right + 100, cy + 18), "time", fill=MUTED, font_obj=SMALL)

    # One wavelength, measured crest to crest.
    turns = 3.15
    crest_u = 1 / (4 * turns)
    crest_x = left + (right - left) * crest_u
    next_crest_x = left + (right - left) * (crest_u + 1 / turns)
    marker_y = cy - radius - 42
    draw.line((s(crest_x), s(marker_y + 8), s(crest_x), s(cy - radius + 9)), fill=rgba(GOLD, 0.55), width=s(2))
    draw.line((s(next_crest_x), s(marker_y + 8), s(next_crest_x), s(cy - radius + 9)), fill=rgba(GOLD, 0.55), width=s(2))
    draw_double_arrow(draw, (crest_x, marker_y), (next_crest_x, marker_y), rgba(GOLD, 0.92), width=3)
    draw_text(draw, ((crest_x + next_crest_x) / 2, marker_y - 28), "crest to crest: λ = 1/k", fill=GOLD, font_obj=SMALL, anchor="mm")

    # Transverse axes at the left end.
    draw.line((s(left - 65), s(cy), s(left + 65), s(cy)), fill=rgba(BLUE, 0.62), width=s(2))
    draw.line((s(left), s(cy + 78), s(left), s(cy - 78)), fill=rgba(RED, 0.62), width=s(2))
    draw_text(draw, (left + 72, cy + 15), "real", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (left + 10, cy - 90), "imag", fill=RED, font_obj=SMALL)

    # Helix path.
    for i in range(360):
        u0 = i / 360
        u1 = (i + 1) / 360
        p0 = helix_point(u0)
        p1 = helix_point(u1)
        front = max(0.0, (p0[2] + p1[2]) / 2)
        alpha = 0.18 + 0.45 * front
        draw.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=rgba(GREEN, alpha), width=s(4))
    for i in range(int(360 * u)):
        u0 = i / 360
        u1 = (i + 1) / 360
        p0 = helix_point(u0)
        p1 = helix_point(u1)
        front = max(0.0, (p0[2] + p1[2]) / 2)
        alpha = 0.42 + 0.50 * front
        draw.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=rgba(GREEN, alpha), width=s(5))

    bx, by, c, sn = helix_point(u)
    axis_x = left + (right - left) * u
    draw.line((s(axis_x), s(cy), s(bx), s(by)), fill=rgba(GOLD, 0.68), width=s(3))
    draw.ellipse((s(bx - 11), s(by - 11), s(bx + 11), s(by + 11)), fill=GOLD, outline=INK, width=s(2))
    draw_text(draw, (bx + 18, by - 24), "e^{iθ}", fill=GREEN, font_obj=SMALL)

    # Equation panel.
    panel = (905, 104, 1196, 286)
    draw.rounded_rectangle(tuple(s(v) for v in panel), radius=s(12), fill=(250, 246, 238, 255), outline=(224, 216, 204, 255), width=s(2))
    draw_text(draw, (930, 136), "1D complex scaling", font_obj=LABEL)
    draw_text(draw, (930, 178), "e^{iθ} = cos θ + i sin θ", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (930, 230), "2D real rotation", font_obj=LABEL)
    draw_text(draw, (930, 260), "(cos θ, sin θ)", fill=INK, font_obj=LABEL)

    # Component traces.
    draw_component_trace(draw, (910, 374, 1190, 466), math.cos, u, BLUE, "real part = cos θ")
    draw_component_trace(draw, (910, 552, 1190, 644), math.sin, u, RED, "imaginary part = sin θ")
    draw_text(draw, (910, 520), "each component moves back and forth", fill=(91, 87, 81), font_obj=SMALL)

    # Projection hints from bead to component traces.
    draw_text(draw, (58, 642), "The spiral is the one-dimensional complex value. Its two real components are sine and cosine waves.", fill=(91, 87, 81), font_obj=LABEL)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    samples = [0, 28, 56, 84, 112, 167]
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
    name = "symmetry-complex-exponential-plane-wave"
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
