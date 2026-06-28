from __future__ import annotations

import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_noether_flux_continuity_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1500
HEIGHT = 820
FPS = 24
FRAMES = 192

BG = (251, 250, 247)
INK = (47, 47, 47)
MUTED = (111, 103, 94)
LIGHT_LINE = (224, 218, 207)
PANEL = (255, 255, 255)
BORDER = (214, 206, 193)
BLUE = (36, 94, 145)
LIGHT_BLUE = (232, 243, 250)
ORANGE = (184, 92, 56)
LIGHT_ORANGE = (248, 234, 220)
GOLD = (181, 138, 53)
GOLD_DARK = (142, 103, 32)
GREEN = (79, 125, 90)
RED = (169, 74, 69)
GRAY = (165, 160, 151)

CENTER = (650.0, 425.0)
RADIUS = 230.0
HUD = (1040, 126, 1370, 606)


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
FONT_HUD = font(22, True)
FONT_TEXT = font(18)
FONT_SMALL = font(15)
FONT_COUNTER = font(28, True)
FONT_EQ = font(24)


def ease(value: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, value)))


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


def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def cloud_offsets() -> list[tuple[float, float]]:
    random.seed(17)
    offsets: list[tuple[float, float]] = []
    while len(offsets) < 125:
        x = random.gauss(0, 102)
        y = random.gauss(0, 76)
        if (x / 210) ** 2 + (y / 150) ** 2 < 1.05:
            offsets.append((x, y))
    return offsets


OFFSETS = cloud_offsets()


def center_x(phase: float) -> float:
    # Starts mostly inside the boundary, sweeps outward, then returns.
    return CENTER[0] - 92 + 320 * math.sin(math.pi * phase)


def velocity(phase: float) -> float:
    return 320 * math.pi * math.cos(math.pi * phase)


def dot_position(offset: tuple[float, float], phase: float) -> tuple[float, float]:
    ox, oy = offset
    wobble = 10 * math.sin(math.pi * phase + oy * 0.017)
    shear = 0.08 * oy * math.sin(math.pi * phase)
    return center_x(phase) + ox + shear, CENTER[1] + oy + wobble


def inside_weight(point: tuple[float, float]) -> float:
    x, y = point
    dist = math.hypot(x - CENTER[0], y - CENTER[1])
    # Smooth edge keeps the counter readable while dots visibly cross.
    return 1.0 / (1.0 + math.exp((dist - RADIUS) / 9.0))


def stats_for_frame(frame: int) -> tuple[float, float, float, float, list[tuple[float, float, float]]]:
    phase = frame / FRAMES
    positions = [dot_position(offset, phase) for offset in OFFSETS]
    q = sum(inside_weight(p) for p in positions)
    dt = 1.0 / FPS
    prev_phase = ((frame - 1) % FRAMES) / FRAMES
    next_phase = ((frame + 1) % FRAMES) / FRAMES
    prev_q = sum(inside_weight(dot_position(offset, prev_phase)) for offset in OFFSETS)
    next_q = sum(inside_weight(dot_position(offset, next_phase)) for offset in OFFSETS)
    dqdt = (next_q - prev_q) / (2 * dt)
    outward_flux = -dqdt
    speed = abs(velocity(phase)) / max(abs(velocity(0.0)), 1.0)
    weighted_positions = [(p[0], p[1], inside_weight(p)) for p in positions]
    return q, dqdt, outward_flux, speed, weighted_positions


def draw_background(draw: ImageDraw.ImageDraw) -> None:
    draw.text((WIDTH / 2, 48), "Continuity Equation and Divergence", fill=INK, font=FONT_TITLE, anchor="mm")
    for x in range(80, 1000, 80):
        draw.line((x, 130, x, 700), fill=(238, 234, 226), width=1)
    for y in range(150, 700, 80):
        draw.line((70, y, 990, y), fill=(238, 234, 226), width=1)


def draw_boundary(draw: ImageDraw.ImageDraw) -> None:
    cx, cy = CENTER
    draw.ellipse(
        (cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS),
        fill=LIGHT_BLUE,
        outline=BLUE,
        width=5,
    )
    draw.text((cx, cy - RADIUS - 28), "fixed boundary", fill=BLUE, font=FONT_TEXT, anchor="mm")
    draw.text((cx, cy), "region", fill=BLUE, font=FONT_TEXT, anchor="mm")


def draw_current_field(draw: ImageDraw.ImageDraw, phase: float, speed: float) -> None:
    v = velocity(phase)
    sign = 1 if v >= 0 else -1
    color = ORANGE if sign > 0 else BLUE
    length = 28 + 58 * speed
    alpha_mix = 0.25 + 0.55 * speed
    arrow_color = blend(GRAY, color, alpha_mix)
    for y in [255, 330, 405, 480, 555]:
        for x in [180, 330, 480, 630, 780, 930]:
            start = (x - sign * length * 0.45, y)
            end = (x + sign * length * 0.45, y)
            arrow(draw, start, end, arrow_color, width=3, head=12)


def draw_boundary_crossing_marks(draw: ImageDraw.ImageDraw, positions: list[tuple[float, float, float]], phase: float) -> None:
    v = velocity(phase)
    outward_right = v > 0
    color = ORANGE if outward_right else BLUE
    cx, cy = CENTER
    # Highlight dots currently near the boundary in the flow direction.
    candidates = []
    for x, y, weight in positions:
        dist = math.hypot(x - cx, y - cy)
        side = x > cx if outward_right else x < cx
        if abs(dist - RADIUS) < 16 and side:
            candidates.append((x, y))
    for x, y in candidates[:12]:
        draw.ellipse((x - 15, y - 15, x + 15, y + 15), outline=color, width=3)


def draw_charge_dots(draw: ImageDraw.ImageDraw, positions: list[tuple[float, float, float]]) -> None:
    for x, y, weight in sorted(positions, key=lambda p: p[2]):
        if weight > 0.52:
            fill = GOLD
            outline = (255, 255, 255)
            r = 6.5
        elif weight > 0.12:
            fill = blend(GRAY, GOLD, 0.45)
            outline = (255, 255, 255)
            r = 5.2
        else:
            fill = (200, 196, 188)
            outline = (255, 255, 255)
            r = 4.2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=1)


def draw_meter(draw: ImageDraw.ImageDraw, label: str, value: float, units: str, y: int, color: tuple[int, int, int], scale: float) -> None:
    x1, _, x2, _ = HUD
    draw.text((x1 + 28, y), label, fill=INK, font=FONT_TEXT, anchor="lm")
    draw.text((x2 - 28, y), f"{value:+.1f}{units}", fill=color, font=FONT_COUNTER, anchor="rm")
    bar_y = y + 28
    draw.rounded_rectangle((x1 + 28, bar_y, x2 - 28, bar_y + 16), radius=7, fill=(242, 239, 232), outline=LIGHT_LINE)
    center = (x1 + x2) / 2
    half = (x2 - x1 - 56) / 2
    if value >= 0:
        draw.rounded_rectangle((center, bar_y, center + min(half, half * value / scale), bar_y + 16), radius=7, fill=color)
    else:
        draw.rounded_rectangle((center + max(-half, half * value / scale), bar_y, center, bar_y + 16), radius=7, fill=color)
    draw.line((center, bar_y - 2, center, bar_y + 18), fill=(170, 164, 154), width=1)


def draw_hud(draw: ImageDraw.ImageDraw, q: float, dqdt: float, flux: float, speed: float) -> None:
    x1, y1, x2, y2 = HUD
    draw.rounded_rectangle((x1, y1, x2, y2), radius=12, fill=PANEL, outline=BORDER, width=2)
    draw.text(((x1 + x2) / 2, y1 + 76), "∂ₜ j⁰ = -∇·j", fill=INK, font=FONT_COUNTER, anchor="mm")

    draw_meter(draw, "dQ/dt", dqdt, "", y1 + 210, BLUE if dqdt > 0 else ORANGE, 45)
    draw_meter(draw, "outward flux", flux, "", y1 + 330, ORANGE if flux > 0 else BLUE, 45)

    draw.text(((x1 + x2) / 2, y2 - 46), "dQ/dt = - outward flux", fill=INK, font=FONT_TEXT, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    q, dqdt, flux, speed, positions = stats_for_frame(frame)
    phase = frame / FRAMES
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_background(draw)
    draw_current_field(draw, phase, speed)
    draw_boundary(draw)
    draw_boundary_crossing_marks(draw, positions, phase)
    draw_charge_dots(draw, positions)
    draw_hud(draw, q, dqdt, flux, speed)
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
        video = OUTPUT_DIR / "lm-noether-flux-continuity.mp4"
        encode_video(video)
        sheet = make_contact_sheet(video.name)
        static = OUTPUT_DIR / "lm-noether-flux-continuity.png"
        if static.exists():
            static.unlink()
        print(video)
        print(sheet)
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


if __name__ == "__main__":
    main()
