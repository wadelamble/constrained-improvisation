from __future__ import annotations

import cmath
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import generate_symmetry_step2_packet_summary_point as base


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = base.FFMPEG
FFPROBE = base.FFPROBE

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
DURATION = 12.5
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GRID = base.GRID
BLUE = base.BLUE
GOLD = base.GOLD
RED = base.RED
LIGHT_BLUE = base.LIGHT_BLUE
GREEN = base.GREEN

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

AMPS = (0.50, 1.00, 0.50)
DK = 0.80
X_MIN = -3.60
X_MAX = 3.60
K_MIN = 5.35
K_MAX = 8.65
PLANE_X_MIN = -0.80
PLANE_X_MAX = 0.80
PLANE_K_MIN = 6.25
PLANE_K_MAX = 7.75
SAMPLES = 720


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


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


def map_x(left: float, right: float, x: float) -> float:
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def map_k(left: float, right: float, k: float) -> float:
    return left + (k - K_MIN) / (K_MAX - K_MIN) * (right - left)


def x_bar(u: float) -> float:
    return -0.55 + 1.10 * u


def k_bar(u: float) -> float:
    # An arbitrary smooth example. This is not presented as a derived law.
    return 7.0 + 0.55 * math.sin(math.pi * (u - 0.5))


def mode_values(u: float) -> tuple[float, float, float]:
    center = k_bar(u)
    return center - DK, center, center + DK


def packet_value(x: float, u: float) -> complex:
    center_x = x_bar(u)
    return sum(
        amp * cmath.exp(1j * k * (x - center_x))
        for amp, k in zip(AMPS, mode_values(u))
    )


def draw_slice_progress(draw: ImageDraw.ImageDraw, u: float) -> None:
    left = 935.0
    right = 1215.0
    y = 73.0
    draw.line((s(left), s(y), s(right), s(y)), fill=rgba(MUTED, 0.38), width=s(2))
    px = left + (right - left) * u
    draw.line((s(left), s(y), s(px), s(y)), fill=GREEN, width=s(3))
    draw.ellipse((s(px - 5), s(y - 5), s(px + 5), s(y + 5)), fill=GREEN)
    draw_text(draw, (left - 8, y), "s₀", fill=MUTED, font_obj=SMALL, anchor="rm")
    draw_text(draw, (right + 8, y), "s₁", fill=MUTED, font_obj=SMALL, anchor="lm")
    draw_text(draw, ((left + right) / 2, y - 18), "current slice s", fill=GREEN, font_obj=SMALL, anchor="mm")


def draw_packet_panel(draw: ImageDraw.ImageDraw, u: float) -> None:
    panel(draw, (35, 108, 675, 367))
    draw_text(draw, (56, 129), "x-space: packet on the current slice", font_obj=PANE_TITLE)
    draw_text(draw, (56, 158), "Its center changes from x̄(s₀) to x̄(s₁).", fill=MUTED, font_obj=SMALL)

    left = 78.0
    right = 645.0
    baseline = 261.0
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.42), width=s(1))
    real: list[tuple[int, int]] = []
    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    scale = 41.0
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        value = packet_value(x, u)
        px = s(map_x(left, right, x))
        real.append((px, s(baseline - scale * value.real)))
        upper.append((px, s(baseline - scale * abs(value))))
        lower.append((px, s(baseline + scale * abs(value))))
    draw.line(upper, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(lower, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(real, fill=BLUE, width=s(3), joint="curve")

    center_px = map_x(left, right, x_bar(u))
    draw.line((s(center_px), s(170), s(center_px), s(351)), fill=GREEN, width=s(3))
    draw.ellipse((s(center_px - 5), s(baseline - 5), s(center_px + 5), s(baseline + 5)), fill=GREEN)
    draw_text(draw, (center_px + 9, 182), "x̄(s)", fill=GREEN, font_obj=LABEL_BOLD)
    draw_text(draw, (right, 337), "x", fill=MUTED, font_obj=SMALL, anchor="ra")


def draw_spectrum_panel(draw: ImageDraw.ImageDraw, u: float) -> None:
    panel(draw, (35, 385, 675, 643))
    draw_text(draw, (56, 405), "k-space: spectrum on the same slice", font_obj=PANE_TITLE)
    draw_text(draw, (56, 434), "Its center changes from k̄(s₀) to k̄(s₁).", fill=MUTED, font_obj=SMALL)

    left = 84.0
    right = 639.0
    axis_y = 565.0
    draw.line((s(left), s(axis_y), s(right), s(axis_y)), fill=rgba(MUTED, 0.65), width=s(2))
    colors = (BLUE, GOLD, RED)
    for index, (k, amp, color) in enumerate(zip(mode_values(u), AMPS, colors)):
        px = map_k(left, right, k)
        top = axis_y - amp * 88.0
        draw.line((s(px), s(axis_y), s(px), s(top)), fill=color, width=s(8))
        draw.ellipse((s(px - 5), s(top - 5), s(px + 5), s(top + 5)), fill=color)
        draw_text(draw, (px, axis_y + 20), f"k{index + 1}", fill=color, font_obj=SMALL, anchor="ma")
    center_px = map_k(left, right, k_bar(u))
    draw.line((s(center_px), s(axis_y + 4), s(center_px), s(445)), fill=GREEN, width=s(3))
    draw_text(draw, (center_px + 10, 452), "k̄(s)", fill=GREEN, font_obj=LABEL_BOLD)
    draw_text(draw, (right, axis_y + 20), "k", fill=MUTED, font_obj=SMALL, anchor="ra")


def plane_x(x: float) -> float:
    left = 755.0
    right = 1210.0
    return left + (x - PLANE_X_MIN) / (PLANE_X_MAX - PLANE_X_MIN) * (right - left)


def plane_k(k: float) -> float:
    top = 180.0
    bottom = 570.0
    return bottom - (k - PLANE_K_MIN) / (PLANE_K_MAX - PLANE_K_MIN) * (bottom - top)


def draw_summary_curve(draw: ImageDraw.ImageDraw, u: float, final_hold: bool) -> None:
    panel(draw, (700, 108, 1245, 643))
    draw_text(draw, (721, 129), "x-k plane: one summary point per slice", font_obj=PANE_TITLE)
    draw_text(draw, (721, 158), "The green trail records earlier values of s.", fill=MUTED, font_obj=SMALL)

    x_axis_y = 570.0
    k_axis_x = 755.0
    draw.line((s(k_axis_x), s(180), s(k_axis_x), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(k_axis_x), s(x_axis_y), s(1210), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (1212, x_axis_y + 19), "x̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (k_axis_x - 7, 180), "k̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    trail: list[tuple[int, int]] = []
    samples = max(2, round(180 * u))
    for index in range(samples):
        q = u * index / (samples - 1)
        trail.append((s(plane_x(x_bar(q))), s(plane_k(k_bar(q)))))
    draw.line(trail, fill=rgba(GREEN, 0.70), width=s(4), joint="curve")

    start = (plane_x(x_bar(0.0)), plane_k(k_bar(0.0)))
    current = (plane_x(x_bar(u)), plane_k(k_bar(u)))
    draw.ellipse((s(start[0] - 5), s(start[1] - 5), s(start[0] + 5), s(start[1] + 5)), fill=rgba(GREEN, 0.55))
    draw_text(draw, (start[0] - 8, start[1] + 11), "s₀", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw.ellipse((s(current[0] - 8), s(current[1] - 8), s(current[0] + 8), s(current[1] + 8)), fill=GREEN)
    draw_text(draw, (current[0] + 13, current[1] - 7), "(x̄(s), k̄(s))", fill=GREEN, font_obj=LABEL_BOLD)
    if final_hold:
        draw_text(draw, (983, 615), "curve parameterized by s", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    if seconds <= 1.0:
        u = 0.0
    elif seconds >= 9.0:
        u = 1.0
    else:
        u = smoothstep((seconds - 1.0) / 8.0)
    final_hold = seconds >= 9.7

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 3 — Packet slices trace a curve in the x-k plane", font_obj=TITLE)
    draw_text(draw, (42, 72), "Illustrative family of slices only: no CCR and no evolution law yet.", fill=MUTED, font_obj=SUBTITLE)
    draw_slice_progress(draw, u)
    draw_packet_panel(draw, u)
    draw_spectrum_panel(draw, u)
    draw_summary_curve(draw, u, final_hold)

    footer = (
        "A one-parameter family of packets maps to a curve of summary points."
        if final_hold
        else "At each s, record only the two centers (x̄(s), k̄(s))."
    )
    draw_text(draw, (640, 681), footer, fill=GREEN if final_hold else MUTED, font_obj=FINAL if final_hold else SMALL, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (1.0, 3.7, 6.3, 8.9, 11.2)
    labels = ("slice s0", "later slice", "later again", "slice s1", "completed curve")
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
    name = "symmetry-step3-packet-slices-trace-xk-curve"
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
