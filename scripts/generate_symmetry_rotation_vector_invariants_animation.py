from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_rotation_vector_invariants_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 144

BG = (255, 252, 246)
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


TITLE = font(25, True)
LABEL = font(18)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


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
    head: float = 20,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def point_at(cx: float, cy: float, length: float, angle: float) -> tuple[float, float]:
    return cx + length * math.cos(angle), cy - length * math.sin(angle)


def draw_arc_arrow(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    start: float,
    end: float,
    color: tuple[int, int, int],
    width: int = 4,
) -> None:
    # PIL angles are clockwise from x-axis in screen coordinates.
    draw.arc(
        (s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)),
        start=-math.degrees(end),
        end=-math.degrees(start),
        fill=color,
        width=s(width),
    )
    ax, ay = point_at(cx, cy, radius, end)
    tangent = end + math.pi / 2
    for offset in (-2.55, 2.55):
        bx = ax - 13 * math.cos(tangent + offset)
        by = ay + 13 * math.sin(tangent + offset)
        draw.line((s(ax), s(ay), s(bx), s(by)), fill=color, width=s(3))


def draw_frame(frame: int) -> Image.Image:
    phase = frame / FRAMES
    rotation = 2 * math.pi * phase
    wedge = math.radians(30)

    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)

    cx, cy = 610.0, 390.0
    short = 165.0
    long = 247.5
    a0 = math.radians(18) + rotation
    a1 = a0 + wedge

    # Faint coordinate frame and circular guides.
    draw.line((s(cx - 330), s(cy), s(cx + 330), s(cy)), fill=MUTED, width=s(2))
    draw.line((s(cx), s(cy + 255), s(cx), s(cy - 255)), fill=MUTED, width=s(2))
    for radius in (short, long):
        draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=FAINT, width=s(2))

    v_end = point_at(cx, cy, short, a0)
    w_end = point_at(cx, cy, long, a1)

    draw_arrow(draw, (cx, cy), v_end, BLUE, width=6, head=20)
    draw_arrow(draw, (cx, cy), w_end, RED, width=6, head=20)

    # Wedge showing the invariant angle.
    draw_arc_arrow(draw, cx, cy, 78, a0, a1, GOLD, width=5)
    mid = (a0 + a1) / 2
    label_x, label_y = point_at(cx, cy, 108, mid)
    draw_text(draw, (label_x, label_y), "30°", fill=GOLD, font_obj=LABEL, anchor="mm")

    draw.ellipse((s(cx - 7), s(cy - 7), s(cx + 7), s(cy + 7)), fill=INK)

    # Labels move with the vectors but stay slightly offset from arrowheads.
    vx, vy = point_at(cx, cy, short + 28, a0)
    wx, wy = point_at(cx, cy, long + 30, a1)
    draw_text(draw, (vx, vy), "|v|", fill=BLUE, font_obj=LABEL, anchor="mm")
    draw_text(draw, (wx, wy), "|w| = 1.5|v|", fill=RED, font_obj=LABEL, anchor="mm")

    draw_text(draw, (70, 62), "Rotation changes coordinates, not lengths or angle", font_obj=TITLE)
    draw_text(draw, (70, 106), "|v| constant     |w| constant     θ constant", fill=(92, 88, 82), font_obj=LABEL)

    image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    frames = [0, 24, 48, 72, 96, 120]
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
    for index, frame in enumerate(frames):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text((x + 8, y + thumb_h + 6), f"{int(round(frame / FRAMES * 360))}° rotation", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / "symmetry-rotation-vector-invariants-contact-sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video = OUTPUT_DIR / "symmetry-rotation-vector-invariants.mp4"

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
