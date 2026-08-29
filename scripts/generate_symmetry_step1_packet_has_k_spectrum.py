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
DURATION = 12.8
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
MODE_COLORS = (BLUE, GOLD, RED)

K0 = 7.0
DK = 0.80
KS = (K0 - DK, K0, K0 + DK)
AMPS = (0.50, 1.00, 0.50)
X_MIN = -4.15
X_MAX = 4.15
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


def interval_progress(seconds: float, start: float, end: float) -> float:
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


def partial_line(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    progress: float,
    fill,
    width: int,
) -> None:
    if progress <= 0 or len(points) < 2:
        return
    count = max(2, min(len(points), round(progress * len(points))))
    draw.line(points[:count], fill=fill, width=s(width), joint="curve")


def map_x(left: float, right: float, x: float) -> float:
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def component_points(
    left: float,
    right: float,
    baseline: float,
    k: float,
    amplitude: float,
    scale: float = 31.0,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        y = baseline - scale * amplitude * math.cos(k * x)
        points.append((s(map_x(left, right, x)), s(y)))
    return points


def packet_value(x: float) -> complex:
    return sum(amp * cmath.exp(1j * k * x) for amp, k in zip(AMPS, KS))


def packet_points(
    left: float,
    right: float,
    baseline: float,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    real: list[tuple[int, int]] = []
    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    scale = 35.0
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        value = packet_value(x)
        px = s(map_x(left, right, x))
        real.append((px, s(baseline - scale * value.real)))
        upper.append((px, s(baseline - scale * abs(value))))
        lower.append((px, s(baseline + scale * abs(value))))
    return real, upper, lower


def draw_header(draw: ImageDraw.ImageDraw) -> None:
    draw_text(draw, (42, 31), "Step 1 — One packet contains several wave numbers", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "Fixed slice s = s₀. The reveal sequence below is not evolution in s.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )


def draw_mode_panel(draw: ImageDraw.ImageDraw, mode_progress: tuple[float, float, float], sum_progress: float) -> None:
    bounds = (35, 108, 850, 643)
    panel(draw, bounds)
    left = 119.0
    right = 820.0
    draw_text(draw, (56, 129), "x-space: frozen profiles", font_obj=PANE_TITLE)
    draw_text(draw, (56, 158), "Each colored row shows Re[cⱼ exp(i kⱼx)] at the same fixed slice.", fill=MUTED, font_obj=SMALL)

    baselines = (222.0, 300.0, 378.0)
    for index, (baseline, color, k, amp, progress) in enumerate(
        zip(baselines, MODE_COLORS, KS, AMPS, mode_progress)
    ):
        draw.line((s(left), s(baseline), s(right), s(baseline)), fill=GRID, width=s(1))
        draw_text(draw, (left - 20, baseline), f"k{index + 1}", fill=color, font_obj=LABEL_BOLD, anchor="rm")
        if progress > 0:
            points = component_points(left, right, baseline, k, amp)
            partial_line(draw, points, progress, color, 3)
            if progress >= 0.995:
                draw_text(
                    draw,
                    (right - 2, baseline - 24),
                    f"c{index + 1} exp(i k{index + 1}x)",
                    fill=color,
                    font_obj=SMALL,
                    anchor="ra",
                )

    sum_y = 538.0
    draw.line((s(left), s(sum_y), s(right), s(sum_y)), fill=rgba(MUTED, 0.42), width=s(1))
    draw_text(draw, (left - 20, sum_y), "sum", fill=INK, font_obj=LABEL_BOLD, anchor="rm")
    if sum_progress > 0:
        draw_text(
            draw,
            (left, 445),
            "ψ(x, s₀) = c₁ exp(i k₁x) + c₂ exp(i k₂x) + c₃ exp(i k₃x)",
            fill=INK,
            font_obj=LABEL,
        )
        real, upper, lower = packet_points(left, right, sum_y)
        partial_line(draw, upper, sum_progress, LIGHT_BLUE, 3)
        partial_line(draw, lower, sum_progress, LIGHT_BLUE, 3)
        partial_line(draw, real, sum_progress, BLUE, 3)
        if sum_progress >= 0.995:
            draw_text(draw, (left + 2, 612), "dark: Re ψ", fill=BLUE, font_obj=SMALL)
            draw_text(draw, (left + 113, 612), "pale boundary: ±|ψ|", fill=LIGHT_BLUE, font_obj=SMALL)
            draw_text(draw, (right, 612), "three-mode schematic packet", fill=MUTED, font_obj=SMALL, anchor="ra")


def k_to_px(k: float) -> float:
    left = 925.0
    right = 1214.0
    lo = K0 - 1.45
    hi = K0 + 1.45
    return left + (k - lo) / (hi - lo) * (right - left)


def draw_spectrum_panel(draw: ImageDraw.ImageDraw, mode_progress: tuple[float, float, float], final_progress: float) -> None:
    bounds = (875, 108, 1245, 643)
    panel(draw, bounds)
    draw_text(draw, (896, 129), "k-space: Fourier coefficients", font_obj=PANE_TITLE)
    draw_text(draw, (896, 158), "All three coefficient phases are 0 here.", fill=MUTED, font_obj=SMALL)

    axis_y = 470.0
    draw.line((s(925), s(axis_y), s(1214), s(axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (1216, axis_y + 17), "k", fill=MUTED, font_obj=SMALL, anchor="ra")

    for index, (k, amp, color, progress) in enumerate(zip(KS, AMPS, MODE_COLORS, mode_progress)):
        px = k_to_px(k)
        draw.line((s(px), s(axis_y - 4), s(px), s(axis_y + 4)), fill=MUTED, width=s(1))
        draw_text(draw, (px, axis_y + 24), f"k{index + 1}", fill=color, font_obj=LABEL_BOLD, anchor="ma")
        if progress > 0:
            top = axis_y - 205.0 * amp * progress
            draw.line((s(px), s(axis_y), s(px), s(top)), fill=color, width=s(8))
            draw.ellipse((s(px - 5), s(top - 5), s(px + 5), s(top + 5)), fill=color)
            if progress >= 0.995:
                draw_text(draw, (px, top - 15), f"c{index + 1}", fill=color, font_obj=SMALL, anchor="ms")

    draw_text(draw, (896, 511), "Each nonzero coefficient selects", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (896, 533), "one wave number in the sum.", fill=MUTED, font_obj=SMALL)

    if final_progress > 0:
        y = 590.0
        left = k_to_px(KS[0]) - 25
        right = k_to_px(KS[-1]) + 25
        draw.line((s(left), s(y), s(right), s(y)), fill=GREEN, width=s(3))
        draw.line((s(left), s(y), s(left), s(y - 10 * final_progress)), fill=GREEN, width=s(3))
        draw.line((s(right), s(y), s(right), s(y - 10 * final_progress)), fill=GREEN, width=s(3))
        if final_progress >= 0.995:
            draw_text(draw, ((left + right) / 2, y + 17), "one spectrum", fill=GREEN, font_obj=SMALL, anchor="ma")


def draw_footer(draw: ImageDraw.ImageDraw, final_progress: float) -> None:
    if final_progress < 0.995:
        draw_text(draw, (640, 681), "We are only changing how the same fixed-slice function is displayed.", fill=MUTED, font_obj=SMALL, anchor="mm")
        return
    draw_text(
        draw,
        (640, 680),
        "This packet has several Fourier components — not one exact k.",
        fill=GREEN,
        font_obj=FINAL,
        anchor="mm",
    )


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_header(draw)

    p1 = interval_progress(seconds, 0.9, 2.3)
    p2 = interval_progress(seconds, 2.5, 3.9)
    p3 = interval_progress(seconds, 4.1, 5.5)
    sum_progress = interval_progress(seconds, 6.1, 8.9)
    final_progress = interval_progress(seconds, 9.1, 10.2)

    draw_mode_panel(draw, (p1, p2, p3), sum_progress)
    draw_spectrum_panel(draw, (p1, p2, p3), final_progress)
    draw_footer(draw, final_progress)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (2.2, 3.8, 5.4, 8.8, 11.7)
    labels = ("first mode", "second mode", "three modes", "their sum", "final statement")
    thumb_w = 384
    thumb_h = 216
    label_h = 26
    margin = 15
    sheet = Image.new("RGB", (3 * thumb_w + 4 * margin, 2 * (thumb_h + label_h) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(zip(sample_seconds, labels)):
        col = index % 3
        row = index // 3
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
    name = "symmetry-step1-packet-has-k-spectrum"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{name}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    final_still = OUTPUT_DIR / f"{name}-final.png"
    try:
        for index in range(FRAMES):
            frame = draw_frame(index)
            frame.save(scratch / f"frame_{index:04d}.png")
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
