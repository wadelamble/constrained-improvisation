from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_noether_symmetry_tangent_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
FPS = 24
FRAMES = 144

BG = (251, 250, 247)
INK = (47, 47, 47)
MUTED = (111, 103, 94)
BORDER = (214, 206, 193)
GRID = (232, 226, 216)
BLUE = (36, 94, 145)
ORANGE = (184, 92, 56)
GOLD = (181, 138, 53)
GREEN = (79, 125, 90)
FAINT_BLUE = (232, 243, 250)
FAINT_ORANGE = (248, 234, 220)
GRAY = (160, 154, 145)

CENTER = (605.0, 365.0)
SCALE = 145.0
Q_RADIUS = 2.0
BASE_ANGLE = math.radians(-38)
MAX_EPSILON = 0.42


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(32, True)
FONT_SUBTITLE = font(20)
FONT_TEXT = font(19)
FONT_SMALL = font(16)
FONT_LABEL = font(25, True)
FONT_EQ = font(28)


def ease(value: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, value)))


def world_to_px(point: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    return CENTER[0] + SCALE * x, CENTER[1] - SCALE * y


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 4,
    head: float = 16,
) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=color, width=width)
    angle = math.atan2(ey - sy, ex - sx)
    p1 = (ex - head * math.cos(angle - 0.55), ey - head * math.sin(angle - 0.55))
    p2 = (ex - head * math.cos(angle + 0.55), ey - head * math.sin(angle + 0.55))
    draw.polygon([(ex, ey), p1, p2], fill=color)


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 3,
    dash: float = 14,
    gap: float = 10,
) -> None:
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    t = 0.0
    while t < length:
        end = min(length, t + dash)
        draw.line((x1 + ux * t, y1 + uy * t, x1 + ux * end, y1 + uy * end), fill=color, width=width)
        t += dash + gap


def draw_arc(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    start: float,
    end: float,
    color: tuple[int, int, int],
    width: int = 5,
) -> None:
    points = []
    steps = max(2, int(abs(end - start) * 90))
    for i in range(steps + 1):
        a = start + (end - start) * i / steps
        points.append((center[0] + radius * math.cos(a), center[1] - radius * math.sin(a)))
    draw.line(points, fill=color, width=width, joint="curve")


def q_at(angle: float) -> tuple[float, float]:
    return Q_RADIUS * math.cos(angle), Q_RADIUS * math.sin(angle)


def tangent_at(angle: float) -> tuple[float, float]:
    return -Q_RADIUS * math.sin(angle), Q_RADIUS * math.cos(angle)


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    left, right = 110, 1110
    top, bottom = 122, 612
    draw.rounded_rectangle((70, 104, 1150, 640), radius=10, fill=(255, 255, 255), outline=BORDER, width=2)
    for x in range(left, right + 1, 72):
        draw.line((x, top, x, bottom), fill=GRID, width=1)
    for y in range(top, bottom + 1, 72):
        draw.line((left, y, right, y), fill=GRID, width=1)
    arrow(draw, (left, CENTER[1]), (right, CENTER[1]), INK, width=3, head=14)
    arrow(draw, (CENTER[0], bottom), (CENTER[0], top), INK, width=3, head=14)
    draw.text((right + 14, CENTER[1] + 4), "q¹", fill=INK, font=FONT_TEXT, anchor="lm")
    draw.text((CENTER[0] + 10, top - 12), "q²", fill=INK, font=FONT_TEXT, anchor="lm")


def draw_hud(draw: ImageDraw.ImageDraw, epsilon: float) -> None:
    x1, x2 = 290, 920
    y = 666
    draw.text((x1 - 20, y + 8), "ε", fill=ORANGE, font=FONT_EQ, anchor="rm")
    draw.text((x2 + 20, y + 8), f"{epsilon:0.2f}", fill=ORANGE, font=FONT_EQ, anchor="lm")
    bar_x1, bar_x2 = x1, x2
    bar_y = y
    draw.rounded_rectangle((bar_x1, bar_y, bar_x2, bar_y + 16), radius=7, fill=(242, 239, 232), outline=GRID)
    fill = (bar_x2 - bar_x1) * epsilon / MAX_EPSILON
    draw.rounded_rectangle((bar_x1, bar_y, bar_x1 + fill, bar_y + 16), radius=7, fill=ORANGE)
    draw.text(((x1 + x2) / 2, y + 44), "δq = ε R(q)", fill=INK, font=FONT_EQ, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    raw = (frame % FRAMES) / FRAMES
    cycle = raw * 2.0
    if cycle <= 1.0:
        epsilon = MAX_EPSILON * ease(cycle)
    else:
        epsilon = MAX_EPSILON * (1.0 - ease(cycle - 1.0))

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.text((WIDTH / 2, 46), "A continuous symmetry has a tangent direction", fill=INK, font=FONT_TITLE, anchor="mm")
    draw.text((WIDTH / 2, 80), "R(q) tells how the point starts to move as the symmetry parameter changes", fill=MUTED, font=FONT_SUBTITLE, anchor="mm")
    draw_axes(draw)
    draw_hud(draw, epsilon)

    orbit_radius = Q_RADIUS * SCALE
    draw.ellipse(
        (CENTER[0] - orbit_radius, CENTER[1] - orbit_radius, CENTER[0] + orbit_radius, CENTER[1] + orbit_radius),
        outline=(205, 198, 187),
        width=4,
    )
    draw.text((CENTER[0] - orbit_radius + 54, CENTER[1] - orbit_radius + 28), "symmetry orbit", fill=MUTED, font=FONT_SMALL)

    q0 = q_at(BASE_ANGLE)
    q0_px = world_to_px(q0)
    tangent = tangent_at(BASE_ANGLE)
    tangent_len = 0.72
    tangent_end = world_to_px((q0[0] + tangent_len * tangent[0] / Q_RADIUS, q0[1] + tangent_len * tangent[1] / Q_RADIUS))
    arrow(draw, q0_px, tangent_end, BLUE, width=5, head=18)
    draw.text((tangent_end[0] - 12, tangent_end[1] - 18), "R(q)", fill=BLUE, font=FONT_TEXT, anchor="rm")

    q_eps = q_at(BASE_ANGLE + epsilon)
    q_eps_px = world_to_px(q_eps)
    linear_eps_px = world_to_px((q0[0] + epsilon * tangent[0], q0[1] + epsilon * tangent[1]))

    draw_arc(draw, CENTER, orbit_radius, BASE_ANGLE, BASE_ANGLE + epsilon, ORANGE, width=6)
    if epsilon > 0.02:
        arrow(draw, q0_px, linear_eps_px, ORANGE, width=4, head=14)
        draw.text((linear_eps_px[0] + 18, linear_eps_px[1] + 18), "εR(q)", fill=ORANGE, font=FONT_SMALL, anchor="lm")
        draw_dashed_line(draw, linear_eps_px, q_eps_px, GRAY, width=2)

    draw.ellipse((q0_px[0] - 12, q0_px[1] - 12, q0_px[0] + 12, q0_px[1] + 12), fill=GOLD, outline=(255, 255, 255), width=3)
    draw.text((q0_px[0] - 28, q0_px[1] + 26), "q", fill=GOLD, font=FONT_TEXT, anchor="rm")
    draw.ellipse((q_eps_px[0] - 12, q_eps_px[1] - 12, q_eps_px[0] + 12, q_eps_px[1] + 12), fill=ORANGE, outline=(255, 255, 255), width=3)
    draw.text((q_eps_px[0] + 18, q_eps_px[1] - 18), "Φε(q)", fill=ORANGE, font=FONT_TEXT, anchor="lm")

    draw.text((WIDTH / 2, 630), "for very small ε, the curved symmetry motion begins as the straight tangent step", fill=MUTED, font=FONT_TEXT, anchor="mm")
    return img


def encode_video(video_path: Path) -> None:
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
            str(video_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    try:
        for frame in range(FRAMES):
            draw_frame(frame).save(SCRATCH / f"frame_{frame:04d}.png")
        video = OUTPUT_DIR / "lm-noether-symmetry-tangent.mp4"
        encode_video(video)
        sheet = make_contact_sheet(video.name)
        print(video)
        print(sheet)
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


if __name__ == "__main__":
    main()
