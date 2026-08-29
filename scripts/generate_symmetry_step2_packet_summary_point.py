from __future__ import annotations

import cmath
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffprobe.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
DURATION = 12.5
FRAMES = round(DURATION * FPS)

BG = (255, 252, 246)
PANEL = (252, 248, 240)
INK = (37, 39, 42)
MUTED = (103, 100, 95)
FAINT = (221, 214, 204)
GRID = (232, 226, 217)
BLUE = (51, 91, 133)
GOLD = (198, 138, 45)
RED = (181, 76, 59)
LIGHT_BLUE = (115, 157, 194)
GREEN = (65, 126, 95)

K0 = 7.0
DK = 0.80
KS = (K0 - DK, K0, K0 + DK)
AMPS = (0.50, 1.00, 0.50)
X_BAR = 1.05
K_BAR = K0
X_MIN = X_BAR - 4.15
X_MAX = X_BAR + 4.15
SAMPLES = 720


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
SUBTITLE = font(17)
PANE_TITLE = font(18, True)
LABEL = font(15)
LABEL_BOLD = font(15, True)
SMALL = font(13)
FINAL = font(18, True)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def progress(seconds: float, start: float, end: float) -> float:
    return smoothstep((seconds - start) / (end - start))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(v) for v in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def dashed_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill,
    width: int = 2,
    dash: float = 8,
    gap: float = 6,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    distance = 0.0
    while distance < length:
        stop = min(distance + dash, length)
        q0 = distance / length
        q1 = stop / length
        draw.line(
            (
                s(start[0] + q0 * dx),
                s(start[1] + q0 * dy),
                s(start[0] + q1 * dx),
                s(start[1] + q1 * dy),
            ),
            fill=fill,
            width=s(width),
        )
        distance += dash + gap


def map_x(left: float, right: float, x: float) -> float:
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def packet_value(x: float) -> complex:
    return sum(amp * cmath.exp(1j * k * (x - X_BAR)) for amp, k in zip(AMPS, KS))


def draw_packet_panel(draw: ImageDraw.ImageDraw, center_progress: float) -> None:
    bounds = (35, 108, 675, 367)
    panel(draw, bounds)
    draw_text(draw, (56, 129), "x-space: one fixed-slice packet", font_obj=PANE_TITLE)
    draw_text(draw, (56, 158), "The packet still contains all three k-components from Step 1.", fill=MUTED, font_obj=SMALL)

    left = 78.0
    right = 645.0
    baseline = 260.0
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.42), width=s(1))
    real: list[tuple[int, int]] = []
    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    scale = 42.0
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        value = packet_value(x)
        px = s(map_x(left, right, x))
        real.append((px, s(baseline - scale * value.real)))
        upper.append((px, s(baseline - scale * abs(value))))
        lower.append((px, s(baseline + scale * abs(value))))
    draw.line(upper, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(lower, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(real, fill=BLUE, width=s(3), joint="curve")
    draw_text(draw, (right, 337), "x", fill=MUTED, font_obj=SMALL, anchor="ra")

    if center_progress > 0:
        px = map_x(left, right, X_BAR)
        line_top = baseline - 91.0 * center_progress
        line_bottom = baseline + 91.0 * center_progress
        draw.line((s(px), s(line_top), s(px), s(line_bottom)), fill=GREEN, width=s(3))
        draw.ellipse((s(px - 5), s(baseline - 5), s(px + 5), s(baseline + 5)), fill=GREEN)
        if center_progress >= 0.995:
            draw_text(draw, (px + 9, 184), "x̄ = center of |ψ(x)|²", fill=GREEN, font_obj=LABEL_BOLD)


def k_to_px(k: float) -> float:
    left = 84.0
    right = 639.0
    low = K0 - 1.45
    high = K0 + 1.45
    return left + (k - low) / (high - low) * (right - left)


def draw_spectrum_panel(draw: ImageDraw.ImageDraw, center_progress: float) -> None:
    bounds = (35, 385, 675, 643)
    panel(draw, bounds)
    draw_text(draw, (56, 405), "k-space: the same packet’s spectrum", font_obj=PANE_TITLE)
    draw_text(draw, (56, 434), "It has several k-values, but their distribution has a center.", fill=MUTED, font_obj=SMALL)

    axis_y = 565.0
    draw.line((s(84), s(axis_y), s(639), s(axis_y)), fill=rgba(MUTED, 0.65), width=s(2))
    colors = (BLUE, GOLD, RED)
    for index, (k, amp, color) in enumerate(zip(KS, AMPS, colors)):
        px = k_to_px(k)
        top = axis_y - amp * 88.0
        draw.line((s(px), s(axis_y), s(px), s(top)), fill=color, width=s(8))
        draw.ellipse((s(px - 5), s(top - 5), s(px + 5), s(top + 5)), fill=color)
        draw_text(draw, (px, axis_y + 20), f"k{index + 1}", fill=color, font_obj=SMALL, anchor="ma")
    draw_text(draw, (640, axis_y + 20), "k", fill=MUTED, font_obj=SMALL, anchor="ra")

    if center_progress > 0:
        px = k_to_px(K_BAR)
        top = axis_y - 123.0 * center_progress
        draw.line((s(px), s(axis_y + 4), s(px), s(top)), fill=GREEN, width=s(3))
        if center_progress >= 0.995:
            draw_text(draw, (px + 10, top - 2), "k̄ = center of the spectrum", fill=GREEN, font_obj=LABEL_BOLD)


def plane_x_to_px(x: float) -> float:
    left = 755.0
    right = 1210.0
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def plane_k_to_py(k: float) -> float:
    top = 180.0
    bottom = 570.0
    low = K0 - 1.45
    high = K0 + 1.45
    return bottom - (k - low) / (high - low) * (bottom - top)


def draw_summary_plane(draw: ImageDraw.ImageDraw, point_progress: float) -> None:
    bounds = (700, 108, 1245, 643)
    panel(draw, bounds)
    draw_text(draw, (721, 129), "x-k plane: a two-number summary", font_obj=PANE_TITLE)
    draw_text(draw, (721, 158), "The axes record the two centers—not every component.", fill=MUTED, font_obj=SMALL)

    x_axis_y = 570.0
    k_axis_x = 755.0
    draw.line((s(k_axis_x), s(180), s(k_axis_x), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(k_axis_x), s(x_axis_y), s(1210), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (1212, x_axis_y + 19), "x̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (k_axis_x - 7, 180), "k̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    if point_progress <= 0:
        return
    px = plane_x_to_px(X_BAR)
    py = plane_k_to_py(K_BAR)
    horizontal_end = k_axis_x + (px - k_axis_x) * point_progress
    vertical_end = x_axis_y + (py - x_axis_y) * point_progress
    dashed_line(draw, (k_axis_x, py), (horizontal_end, py), rgba(GREEN, 0.72), width=2)
    dashed_line(draw, (px, x_axis_y), (px, vertical_end), rgba(GREEN, 0.72), width=2)
    draw.ellipse((s(k_axis_x - 4), s(py - 4), s(k_axis_x + 4), s(py + 4)), fill=GREEN)
    draw.ellipse((s(px - 4), s(x_axis_y - 4), s(px + 4), s(x_axis_y + 4)), fill=GREEN)
    if point_progress >= 0.995:
        draw.ellipse((s(px - 8), s(py - 8), s(px + 8), s(py + 8)), fill=GREEN)
        draw_text(draw, (px + 14, py - 9), "(x̄, k̄)", fill=GREEN, font_obj=FINAL)
        draw_text(draw, (973, 616), "summary point", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")


def draw_footer(draw: ImageDraw.ImageDraw, final_progress: float) -> None:
    if final_progress < 0.995:
        draw_text(draw, (640, 681), "Still one fixed slice: no path and no time evolution yet.", fill=MUTED, font_obj=SMALL, anchor="mm")
        return
    draw_text(
        draw,
        (640, 681),
        "The point (x̄, k̄) summarizes the packet; it is not the packet itself.",
        fill=GREEN,
        font_obj=FINAL,
        anchor="mm",
    )


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 2 — Summarize one fixed packet by (x̄, k̄)", font_obj=TITLE)
    draw_text(draw, (42, 72), "Fixed slice s = s₀. Nothing in this animation evolves in s.", fill=MUTED, font_obj=SUBTITLE)

    x_progress = progress(seconds, 1.0, 3.0)
    k_progress = progress(seconds, 3.3, 5.3)
    point_progress = progress(seconds, 5.8, 8.7)
    final_progress = progress(seconds, 9.0, 10.0)
    draw_packet_panel(draw, x_progress)
    draw_spectrum_panel(draw, k_progress)
    draw_summary_plane(draw, point_progress)
    draw_footer(draw, final_progress)
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (2.8, 5.1, 8.5, 11.4)
    labels = ("find x center", "find k center", "combine the two numbers", "final statement")
    thumb_w = 480
    thumb_h = 270
    label_h = 27
    margin = 15
    sheet = Image.new("RGB", (2 * thumb_w + 3 * margin, 2 * (thumb_h + label_h) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(zip(sample_seconds, labels)):
        col = index % 2
        row = index // 2
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 4, y + thumb_h + 4), label, fill=MUTED)
    output = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(output)
    return output


def verify_video(video: Path) -> str:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "stream=codec_name,pix_fmt,width,height,r_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def render() -> tuple[Path, Path, Path]:
    name = "symmetry-step2-packet-summary-point"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{name}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    final_still = OUTPUT_DIR / f"{name}-final.png"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        draw_frame(FRAMES - 1).save(final_still)
        encoded = subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if encoded.returncode != 0 or not video.exists() or video.stat().st_size == 0:
            raise RuntimeError("ffmpeg failed to encode the animation")
        contact = make_contact_sheet(name)
        return video, contact, final_still
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact, final_still = render()
    print(video)
    print(contact)
    print(final_still)
    print(verify_video(video))


if __name__ == "__main__":
    main()
