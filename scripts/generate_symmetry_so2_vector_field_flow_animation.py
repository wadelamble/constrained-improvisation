from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_so2_vector_field_flow_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 210

BG = (255, 252, 246)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (224, 217, 206)
CIRCLE = (64, 91, 104)
ACCENT = (184, 72, 48)
BLUE = (55, 103, 157)
GOLD = (198, 139, 54)
GREEN = (72, 132, 103)
PURPLE = (116, 91, 155)


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
LABEL = font(18)
SMALL = font(14)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float = 1.0) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, int(round(255 * alpha))))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * max(0.0, min(1.0, t))


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


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 4,
    head: float = 15.0,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def circle_point(cx: float, cy: float, r: float, theta: float) -> tuple[float, float]:
    return cx + r * math.cos(theta), cy - r * math.sin(theta)


def draw_axes(draw: ImageDraw.ImageDraw, cx: float, cy: float, extent: float, alpha: float = 1.0) -> None:
    axis = rgba(MUTED, 0.72 * alpha)
    draw.line((s(cx - extent), s(cy), s(cx + extent), s(cy)), fill=axis, width=s(2))
    draw.line((s(cx), s(cy + extent), s(cx), s(cy - extent)), fill=axis, width=s(2))
    draw_text(draw, (cx + extent + 18, cy - 6), "x", fill=rgba(MUTED, alpha), font_obj=SMALL)
    draw_text(draw, (cx + 10, cy - extent - 20), "y", fill=rgba(MUTED, alpha), font_obj=SMALL)


def theta_label(step: int) -> str:
    return ["0", "\u03c0/2", "\u03c0", "3\u03c0/2", "2\u03c0"][step]


def draw_single_tangent(draw: ImageDraw.ImageDraw, frame: int) -> None:
    cx, cy = 520.0, 380.0
    r = 180.0
    draw_text(draw, (68, 60), "A tangent direction at one state", font_obj=TITLE)

    step = min(4, frame // 16)
    theta = step * math.pi / 2
    p = circle_point(cx, cy, r, theta)
    tangent = (-math.sin(theta), -math.cos(theta))
    end = (p[0] + 132 * tangent[0], p[1] + 132 * tangent[1])

    draw_axes(draw, cx, cy, 260)
    draw.ellipse((s(cx - r), s(cy - r), s(cx + r), s(cy + r)), outline=CIRCLE, width=s(5))
    draw.ellipse((s(p[0] - 8), s(p[1] - 8), s(p[0] + 8), s(p[1] + 8)), fill=INK)
    draw_arrow(draw, p, end, ACCENT, width=5, head=18)

    draw_text(draw, (930, 160), "\u03b8 = " + theta_label(step), fill=INK, font_obj=TITLE)
    draw_text(draw, (930, 207), "tangent nudge", fill=ACCENT, font_obj=LABEL)

    arc_r = 58
    draw.arc((s(cx - arc_r), s(cy - arc_r), s(cx + arc_r), s(cy + arc_r)), start=-110, end=-10, fill=rgba(ACCENT, 0.9), width=s(4))
    ax = cx + arc_r * math.cos(math.radians(-110))
    ay = cy + arc_r * math.sin(math.radians(-110))
    for offset in (-2.55, 2.55):
        bx = ax + 12 * math.cos(math.radians(-110) - math.pi / 2 + offset)
        by = ay + 12 * math.sin(math.radians(-110) - math.pi / 2 + offset)
        draw.line((s(ax), s(ay), s(bx), s(by)), fill=ACCENT, width=s(3))


def draw_vector_field(
    draw: ImageDraw.ImageDraw,
    alpha: float,
    dots_phase: float | None = None,
    trails: bool = False,
) -> None:
    cx, cy = 640.0, 380.0
    unit = 98.0
    extent_units = 2.65

    draw_text(draw, (68, 60), "The tangent rule at every state", fill=rgba(INK, alpha), font_obj=TITLE)
    draw_text(draw, (68, 100), "K(x,y)=(-y,x)", fill=rgba(ACCENT, alpha), font_obj=LABEL)

    draw_axes(draw, cx, cy, unit * extent_units, alpha)
    for rr in (0.8, 1.45, 2.12):
        draw.ellipse(
            (s(cx - rr * unit), s(cy - rr * unit), s(cx + rr * unit), s(cy + rr * unit)),
            outline=rgba(FAINT, 0.78 * alpha),
            width=s(2),
        )

    xs = [-2.25, -1.5, -0.75, 0.0, 0.75, 1.5, 2.25]
    ys = [-2.25, -1.5, -0.75, 0.0, 0.75, 1.5, 2.25]
    for x in xs:
        for y in ys:
            radius = math.hypot(x, y)
            if radius < 0.18 or radius > 2.55:
                continue
            px = cx + x * unit
            py = cy - y * unit
            vx, vy = -y, x
            vmag = math.hypot(vx, vy)
            vx /= vmag
            vy /= vmag
            length = 24 + 9 * min(radius, 2.4)
            start = (px - 0.45 * length * vx, py + 0.45 * length * vy)
            end = (px + 0.55 * length * vx, py - 0.55 * length * vy)
            draw_arrow(draw, start, end, rgba(CIRCLE, 0.72 * alpha), width=2, head=8)

    dot_specs = [
        (0.78, 0.08 * math.pi, BLUE),
        (1.18, 0.82 * math.pi, ACCENT),
        (1.62, 1.42 * math.pi, GOLD),
        (2.06, 0.36 * math.pi, GREEN),
        (2.34, 1.1 * math.pi, PURPLE),
    ]
    if dots_phase is None:
        dot_alpha = alpha
        angle_shift = 0.0
        trail_phase = 0.0
    else:
        dot_alpha = alpha
        angle_shift = 1.85 * math.pi * ease(dots_phase)
        trail_phase = ease(dots_phase)

    for rr, base, color in dot_specs:
        if trails and trail_phase > 0.02:
            current = base + angle_shift
            start = current - 1.85 * math.pi * trail_phase
            steps = 48
            prev = None
            for i in range(steps + 1):
                t = i / steps
                angle = start + (current - start) * t
                x = cx + rr * unit * math.cos(angle)
                y = cy - rr * unit * math.sin(angle)
                if prev is not None:
                    draw.line((s(prev[0]), s(prev[1]), s(x), s(y)), fill=rgba(color, 0.18 + 0.34 * t), width=s(3))
                prev = (x, y)
        angle = base + angle_shift
        x = cx + rr * unit * math.cos(angle)
        y = cy - rr * unit * math.sin(angle)
        draw.ellipse((s(x - 8), s(y - 8), s(x + 8), s(y + 8)), fill=rgba(color, dot_alpha))


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    if frame < 80:
        draw_single_tangent(draw, frame)
    elif frame < 102:
        t = ease((frame - 80) / 21)
        # Fade from the single tangent view into the field view.
        layer_a = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer_b = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw_a = ImageDraw.Draw(layer_a, "RGBA")
        draw_b = ImageDraw.Draw(layer_b, "RGBA")
        draw_single_tangent(draw_a, 79)
        draw_vector_field(draw_b, 1.0)
        layer_a.putalpha(int(255 * (1 - t)))
        layer_b.putalpha(int(255 * t))
        image.alpha_composite(layer_a)
        image.alpha_composite(layer_b)
    elif frame < 132:
        draw_vector_field(draw, 1.0)
    else:
        phase = min(1.0, (frame - 132) / (FRAMES - 133))
        draw_vector_field(draw, 1.0, dots_phase=phase, trails=True)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet() -> Path:
    samples = [
        (0, "theta = 0"),
        (16, "theta = pi/2"),
        (32, "theta = pi"),
        (48, "theta = 3pi/2"),
        (64, "theta = 2pi"),
        (103, "vector field"),
        (133, "dots released"),
        (171, "flow"),
        (209, "trails"),
    ]
    thumb_w = 410
    thumb_h = 230
    label_h = 32
    margin = 18
    cols = 3
    rows = 3
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    draw = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text((x + 8, y + thumb_h + 7), label, fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / "symmetry-so2-vector-field-flow-contact-sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    video = OUTPUT_DIR / "symmetry-so2-vector-field-flow.mp4"

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
