from __future__ import annotations

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
LIGHT_BLUE = base.LIGHT_BLUE
GREEN = base.GREEN

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

X_MIN = -3.4
X_MAX = 4.3
K_MIN = 4.45
K_MAX = 8.75
K0 = 6.15
SIGMA_X = 0.95
SIGMA_K = 0.52
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


def dashed_polyline(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill, width: int = 2) -> None:
    if len(points) < 2:
        return
    for index in range(0, len(points) - 1, 16):
        stop = min(index + 9, len(points) - 1)
        if stop > index:
            draw.line(points[index : stop + 1], fill=fill, width=s(width), joint="curve")


def a_shift(u: float) -> float:
    return 0.90 * u


def b_shift(u: float) -> float:
    return 0.63 * math.sin(0.5 * math.pi * u)


def map_value(value: float, low: float, high: float, left: float, right: float) -> float:
    return left + (value - low) / (high - low) * (right - left)


def reference_packet(x: float) -> complex:
    envelope = math.exp(-(x * x) / (2 * SIGMA_X * SIGMA_X))
    return envelope * complex(math.cos(K0 * x), math.sin(K0 * x))


def displaced_packet(x: float, a: float, b: float) -> complex:
    # ψ_{a,b}(x)=exp(ibx)ψ₀(x-a)
    shifted = reference_packet(x - a)
    phase = complex(math.cos(b * x), math.sin(b * x))
    return phase * shifted


def spectrum_magnitude(k: float, b: float = 0.0) -> float:
    center = K0 + b
    return math.exp(-((k - center) ** 2) / (2 * SIGMA_K * SIGMA_K))


def draw_packet_panel(draw: ImageDraw.ImageDraw, u: float) -> None:
    panel(draw, (35, 108, 735, 381))
    draw_text(draw, (56, 129), "x-space: one reference shape, shifted by a", font_obj=PANE_TITLE)
    draw_text(draw, (56, 158), "Gray is ψ₀. Blue is the current displaced copy.", fill=MUTED, font_obj=SMALL)

    left = 83.0
    right = 704.0
    baseline = 270.0
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.42), width=s(1))
    a = a_shift(u)
    b = b_shift(u)
    ref_upper: list[tuple[int, int]] = []
    ref_lower: list[tuple[int, int]] = []
    current_upper: list[tuple[int, int]] = []
    current_lower: list[tuple[int, int]] = []
    current_real: list[tuple[int, int]] = []
    scale = 77.0
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        px = s(map_value(x, X_MIN, X_MAX, left, right))
        ref = reference_packet(x)
        current = displaced_packet(x, a, b)
        ref_upper.append((px, s(baseline - scale * abs(ref))))
        ref_lower.append((px, s(baseline + scale * abs(ref))))
        current_upper.append((px, s(baseline - scale * abs(current))))
        current_lower.append((px, s(baseline + scale * abs(current))))
        current_real.append((px, s(baseline - scale * current.real)))

    dashed_polyline(draw, ref_upper, rgba(MUTED, 0.72), 2)
    dashed_polyline(draw, ref_lower, rgba(MUTED, 0.72), 2)
    draw.line(current_upper, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(current_lower, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(current_real, fill=BLUE, width=s(3), joint="curve")
    center = map_value(a, X_MIN, X_MAX, left, right)
    draw.line((s(center), s(181), s(center), s(356)), fill=GREEN, width=s(3))
    draw_text(draw, (center + 9, 187), "x-center = a", fill=GREEN, font_obj=LABEL_BOLD)
    draw_text(draw, (right, 353), "x", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (left, 353), "dashed: reference envelope", fill=MUTED, font_obj=SMALL)


def draw_spectrum_panel(draw: ImageDraw.ImageDraw, u: float) -> None:
    panel(draw, (35, 398, 735, 643))
    draw_text(draw, (56, 418), "k-space: the same spectrum shape, shifted by b", font_obj=PANE_TITLE)
    draw_text(draw, (56, 447), "Gray is the reference magnitude. Gold is the shifted magnitude.", fill=MUTED, font_obj=SMALL)

    left = 83.0
    right = 704.0
    baseline = 574.0
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.65), width=s(2))
    ref_points: list[tuple[int, int]] = []
    current_points: list[tuple[int, int]] = []
    b = b_shift(u)
    scale = 91.0
    for index in range(SAMPLES):
        k = K_MIN + (K_MAX - K_MIN) * index / (SAMPLES - 1)
        px = s(map_value(k, K_MIN, K_MAX, left, right))
        ref_points.append((px, s(baseline - scale * spectrum_magnitude(k))))
        current_points.append((px, s(baseline - scale * spectrum_magnitude(k, b))))
    dashed_polyline(draw, ref_points, rgba(MUTED, 0.72), 2)
    draw.line(current_points, fill=GOLD, width=s(4), joint="curve")
    center = map_value(K0 + b, K_MIN, K_MAX, left, right)
    draw.line((s(center), s(461), s(center), s(baseline + 4)), fill=GREEN, width=s(3))
    draw_text(draw, (center + 9, 468), "k-center = k₀ + b", fill=GREEN, font_obj=LABEL_BOLD)
    draw_text(draw, (right, baseline + 21), "k", fill=MUTED, font_obj=SMALL, anchor="ra")


def plane_a(a: float) -> float:
    left = 805.0
    right = 1205.0
    return map_value(a, -0.12, 1.05, left, right)


def plane_b(b: float) -> float:
    top = 184.0
    bottom = 503.0
    return bottom - (b + 0.10) / 0.84 * (bottom - top)


def draw_displacement_panel(draw: ImageDraw.ImageDraw, u: float, final_hold: bool) -> None:
    panel(draw, (765, 108, 1245, 643))
    draw_text(draw, (786, 129), "displacement family", font_obj=PANE_TITLE)
    draw_text(draw, (786, 158), "Each point means: shift ψ₀ in x and k.", fill=MUTED, font_obj=SMALL)

    x_axis_y = 503.0
    y_axis_x = 805.0
    draw.line((s(y_axis_x), s(184), s(y_axis_x), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(y_axis_x), s(x_axis_y), s(1205), s(x_axis_y)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (1208, x_axis_y + 20), "x-shift a", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (y_axis_x - 8, 184), "k-shift b", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    path: list[tuple[int, int]] = []
    samples = max(2, round(220 * max(u, 0.005)))
    for index in range(samples):
        q = u * index / (samples - 1)
        path.append((s(plane_a(a_shift(q))), s(plane_b(b_shift(q)))))
    draw.line(path, fill=GREEN, width=s(4), joint="curve")
    start = (plane_a(0.0), plane_b(0.0))
    current = (plane_a(a_shift(u)), plane_b(b_shift(u)))
    draw.ellipse((s(start[0] - 6), s(start[1] - 6), s(start[0] + 6), s(start[1] + 6)), fill=rgba(GREEN, 0.55))
    draw_text(draw, (start[0] + 9, start[1] + 8), "ψ₀", fill=MUTED, font_obj=SMALL)
    draw.ellipse((s(current[0] - 9), s(current[1] - 9), s(current[0] + 9), s(current[1] + 9)), fill=GREEN)
    draw_text(draw, (current[0] - 13, current[1] - 8), "current shifted packet", fill=GREEN, font_obj=SMALL, anchor="ra")

    draw_text(draw, (1005, 551), "ψₐ,ᵦ(x) = exp(i b x) ψ₀(x − a)", fill=INK, font_obj=LABEL_BOLD, anchor="mm")
    if final_hold:
        draw_text(draw, (1005, 590), "No spreading. No deformation.", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (1005, 615), "A common phase is not visible in these plots.", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    if seconds <= 1.0:
        u = 0.0
    elif seconds >= 8.8:
        u = 1.0
    else:
        u = smoothstep((seconds - 1.0) / 7.8)
    final_hold = seconds >= 9.4

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 5 — Restrict candidates to x- and k-shifts of one packet", font_obj=TITLE)
    draw_text(draw, (42, 72), "Centers alone omit internal shape and phase; here the shape is held fixed.", fill=MUTED, font_obj=SUBTITLE)
    draw_packet_panel(draw, u)
    draw_spectrum_panel(draw, u)
    draw_displacement_panel(draw, u, final_hold)

    footer = (
        "From here on, an x-k curve means a sequence of shifts of this one reference packet."
        if final_hold
        else "Only the x-center and k-center move; both distribution shapes remain fixed."
    )
    draw_text(draw, (640, 681), footer, fill=GREEN if final_hold else MUTED, font_obj=FINAL if final_hold else SMALL, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (1.0, 3.2, 5.4, 8.7, 11.3)
    labels = ("reference packet", "x and k shift", "same shapes", "displaced packet", "restriction stated")
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
    name = "symmetry-step5-displacement-only-packet-family"
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
