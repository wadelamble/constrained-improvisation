from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
SCRATCH = OUTPUT_DIR / "_source_sink_frames"

WIDTH = 1280
HEIGHT = 620
FPS = 18
FRAMES = 120
WORLD_MIN = -1.75
WORLD_MAX = 1.75


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(26, True)
FONT_PANEL = font(21, True)
FONT_TEXT = font(17)
FONT_SMALL = font(15)
FONT_AXIS = font(18, True)


def pane_rect(index: int) -> tuple[int, int, int, int]:
    if index == 0:
        return (60, 90, 550, 460)
    return (670, 90, 550, 460)


def plot_rect(pane: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, w, h = pane
    return (x + 42, y + 42, w - 76, h - 82)


def to_px(point: tuple[float, float], pane: tuple[int, int, int, int]) -> tuple[float, float]:
    x0, y0, w, h = plot_rect(pane)
    q, p = point
    px = x0 + (q - WORLD_MIN) / (WORLD_MAX - WORLD_MIN) * w
    py = y0 + (WORLD_MAX - p) / (WORLD_MAX - WORLD_MIN) * h
    return px, py


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], color: tuple[int, int, int]) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=color, width=2)
    angle = math.atan2(ey - sy, ex - sx)
    length = 8
    spread = 0.55
    p1 = (ex - length * math.cos(angle - spread), ey - length * math.sin(angle - spread))
    p2 = (ex - length * math.cos(angle + spread), ey - length * math.sin(angle + spread))
    draw.polygon([(ex, ey), p1, p2], fill=color)


def draw_dashed_polyline(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], color: tuple[int, int, int]) -> None:
    for a, b in zip(points, points[1:] + points[:1]):
        ax, ay = a
        bx, by = b
        length = math.hypot(bx - ax, by - ay)
        if length == 0:
            continue
        pieces = max(1, int(length / 10))
        for i in range(pieces):
            if i % 2 == 0:
                t0 = i / pieces
                t1 = min(1.0, (i + 1) / pieces)
                draw.line((ax + (bx - ax) * t0, ay + (by - ay) * t0, ax + (bx - ax) * t1, ay + (by - ay) * t1), fill=color, width=2)


def base_patch() -> list[tuple[float, float]]:
    center = (0.34, 0.22)
    return [
        (center[0] - 0.42, center[1] - 0.28),
        (center[0] + 0.42, center[1] - 0.28),
        (center[0] + 0.42, center[1] + 0.28),
        (center[0] - 0.42, center[1] + 0.28),
    ]


def transformed_patch(kind: str, amount: float) -> list[tuple[float, float]]:
    a = 0.72
    sx = math.exp(a * amount)
    sy = math.exp(a * amount) if kind == "source" else math.exp(-a * amount)
    return [(x * sx, y * sy) for x, y in base_patch()]


def draw_grid(draw: ImageDraw.ImageDraw, pane: tuple[int, int, int, int]) -> None:
    x0, y0, w, h = plot_rect(pane)
    draw.rectangle((x0, y0, x0 + w, y0 + h), fill=(251, 251, 251), outline=(207, 202, 192), width=1)
    for i in range(1, 8):
        x = x0 + w * i / 8
        y = y0 + h * i / 8
        draw.line((x, y0, x, y0 + h), fill=(236, 236, 236), width=1)
        draw.line((x0, y, x0 + w, y), fill=(236, 236, 236), width=1)
    zero_x, zero_y = to_px((0, 0), pane)
    draw.line((x0, zero_y, x0 + w, zero_y), fill=(169, 169, 169), width=2)
    draw.line((zero_x, y0, zero_x, y0 + h), fill=(169, 169, 169), width=2)
    draw.text((x0 + w - 12, zero_y + 8), "q", fill=(45, 45, 45), font=FONT_AXIS, anchor="ra")
    draw.text((zero_x + 8, y0 + 4), "p", fill=(45, 45, 45), font=FONT_AXIS)


def draw_vector_field(draw: ImageDraw.ImageDraw, pane: tuple[int, int, int, int], kind: str) -> None:
    values = [-1.25, -0.85, -0.45, 0.0, 0.45, 0.85, 1.25]
    for q in values:
        for p in values:
            if abs(q) < 0.001 and abs(p) < 0.001:
                continue
            if kind == "source":
                u, v = 0.72 * q, 0.72 * p
            else:
                u, v = 0.72 * q, -0.72 * p
            start = to_px((q, p), pane)
            end = to_px((q + 0.26 * u, p + 0.26 * v), pane)
            draw_arrow(draw, start, end, (130, 130, 130))


def draw_area_meter(draw: ImageDraw.ImageDraw, pane: tuple[int, int, int, int], area_ratio: float) -> None:
    x, y, _, _ = pane
    label = f"area x {area_ratio:.2f}"
    draw.text((x + 58, y + 404), label, fill=(45, 45, 45), font=FONT_SMALL)
    bar_x, bar_y = x + 58, y + 430
    bar_w, bar_h = 190, 20
    draw.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), outline=(207, 202, 192), fill=(255, 255, 255))
    fill_w = min(bar_w, max(0, bar_w * area_ratio / 4.3))
    draw.rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h), fill=(188, 71, 73))


def draw_panel(image: Image.Image, pane: tuple[int, int, int, int], kind: str, amount: float) -> None:
    draw = ImageDraw.Draw(image)
    x, y, w, _ = pane
    title = "source: local expansion" if kind == "source" else "no source/sink: Hamiltonian balance"
    subtitle = "divergence > 0" if kind == "source" else "divergence = 0"
    note = "states spread out" if kind == "source" else "stretch balanced by squeeze"
    color = (188, 71, 73) if kind == "source" else (53, 80, 112)
    area_ratio = math.exp(2 * 0.72 * amount) if kind == "source" else 1.0

    draw.text((x + w / 2, y), title, fill=(32, 33, 36), font=FONT_PANEL, anchor="ma")
    draw_grid(draw, pane)
    draw_vector_field(draw, pane, kind)

    initial = [to_px(point, pane) for point in base_patch()]
    draw_dashed_polyline(draw, initial, (150, 150, 150))

    patch = [to_px(point, pane) for point in transformed_patch(kind, amount)]
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.polygon(patch, fill=(*color, 85), outline=(*color, 255))
    image.alpha_composite(overlay)
    draw = ImageDraw.Draw(image)
    draw.line(patch + [patch[0]], fill=color, width=3)

    box_x, box_y = x + 58, y + 50
    draw.rounded_rectangle((box_x, box_y, box_x + 150, box_y + 34), radius=8, fill=(255, 255, 255), outline=(208, 208, 208))
    draw.text((box_x + 12, box_y + 8), subtitle, fill=(45, 45, 45), font=FONT_SMALL)
    draw.text((x + w - 54, y + 434), note, fill=(80, 80, 80), font=FONT_SMALL, anchor="ra")
    draw_area_meter(draw, pane, area_ratio)


def draw_frame(frame: int) -> Image.Image:
    phase = 0.5 - 0.5 * math.cos(2 * math.pi * frame / FRAMES)
    image = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((WIDTH / 2, 30), "Sources change area; Hamiltonian flows do not", fill=(32, 33, 36), font=FONT_TITLE, anchor="ma")
    draw_panel(image, pane_rect(0), "source", phase)
    draw_panel(image, pane_rect(1), "hamiltonian", phase)
    return image.convert("RGB")


def encode_video(video: Path) -> None:
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
            str(video),
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
        video = OUTPUT_DIR / "differential-source-sink-vs-symplectic.mp4"
        encode_video(video)
        sheet = make_contact_sheet(video.name)
        print(video)
        print(sheet)
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


if __name__ == "__main__":
    main()
