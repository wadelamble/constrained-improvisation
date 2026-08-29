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
GREEN = base.GREEN
PURPLE = (117, 85, 145)
LIGHT_GREEN = (154, 190, 169)
LIGHT_PURPLE = (181, 160, 199)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

X_MIN = -0.80
X_MAX = 0.80
K_MIN = 6.25
K_MAX = 7.75


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


def candidate_a(u: float) -> tuple[float, float]:
    x = -0.55 + 1.10 * u
    k = 7.0 + 0.55 * math.sin(math.pi * (u - 0.5))
    return x, k


def candidate_b(u: float) -> tuple[float, float]:
    x_a, k_a = candidate_a(u)
    # The sine factors vanish at u=0 and u=1, so both candidates share endpoints.
    x = x_a + 0.20 * math.sin(math.pi * u)
    k = k_a - 0.55 * math.sin(math.pi * u)
    return x, k


def plane_x(bounds: tuple[float, float, float, float], x: float) -> float:
    left, _, right, _ = bounds
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def plane_k(bounds: tuple[float, float, float, float], k: float) -> float:
    _, top, _, bottom = bounds
    return bottom - (k - K_MIN) / (K_MAX - K_MIN) * (bottom - top)


def curve_points(
    bounds: tuple[float, float, float, float],
    candidate,
    upto: float,
    samples: int = 240,
) -> list[tuple[int, int]]:
    count = max(2, round(samples * upto))
    points: list[tuple[int, int]] = []
    for index in range(count):
        u = upto * index / (count - 1)
        x, k = candidate(u)
        points.append((s(plane_x(bounds, x)), s(plane_k(bounds, k))))
    return points


def draw_candidate_panel(
    draw: ImageDraw.ImageDraw,
    outer: tuple[float, float, float, float],
    label: str,
    color,
    light_color,
    candidate,
    u: float,
) -> None:
    panel(draw, outer)
    x0, y0, x1, y1 = outer
    draw_text(draw, (x0 + 21, y0 + 20), label, fill=color, font_obj=PANE_TITLE)
    draw_text(draw, (x0 + 21, y0 + 49), "one hypothetical history of packet summaries", fill=MUTED, font_obj=SMALL)

    plot = (x0 + 63, y0 + 91, x1 - 27, y1 - 54)
    left, top, right, bottom = plot
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.67), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.67), width=s(2))
    draw_text(draw, (right + 2, bottom + 20), "x̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 7, top), "k̄", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    start_x, start_k = candidate(0.0)
    end_x, end_k = candidate(1.0)
    start = (plane_x(plot, start_x), plane_k(plot, start_k))
    end = (plane_x(plot, end_x), plane_k(plot, end_k))
    draw.ellipse((s(start[0] - 7), s(start[1] - 7), s(start[0] + 7), s(start[1] + 7)), fill=light_color)
    draw.ellipse((s(end[0] - 7), s(end[1] - 7), s(end[0] + 7), s(end[1] + 7)), fill=light_color)
    draw_text(draw, (start[0] - 10, start[1] + 13), "A at s₀", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (end[0] + 10, end[1] - 10), "B at s₁", fill=MUTED, font_obj=SMALL)

    points = curve_points(plot, candidate, max(u, 0.005))
    draw.line(points, fill=color, width=s(4), joint="curve")
    current_x, current_k = candidate(u)
    current = (plane_x(plot, current_x), plane_k(plot, current_k))
    draw.ellipse((s(current[0] - 9), s(current[1] - 9), s(current[0] + 9), s(current[1] + 9)), fill=color)
    if 0.04 < u < 0.96:
        draw_text(draw, (current[0] + 13, current[1] - 8), "same current s", fill=color, font_obj=SMALL)


def draw_s_progress(draw: ImageDraw.ImageDraw, u: float) -> None:
    left = 285.0
    right = 995.0
    y = 625.0
    draw.line((s(left), s(y), s(right), s(y)), fill=rgba(MUTED, 0.38), width=s(3))
    px = left + (right - left) * u
    draw.line((s(left), s(y), s(px), s(y)), fill=INK, width=s(3))
    draw.ellipse((s(px - 7), s(y - 7), s(px + 7), s(y + 7)), fill=INK)
    draw_text(draw, (left - 12, y), "s₀", fill=MUTED, font_obj=LABEL, anchor="rm")
    draw_text(draw, (right + 12, y), "s₁", fill=MUTED, font_obj=LABEL, anchor="lm")
    draw_text(draw, ((left + right) / 2, y - 19), "one shared value of s for both alternatives", fill=MUTED, font_obj=SMALL, anchor="mm")


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
    draw_text(draw, (42, 31), "Step 4 — Same boundary summaries, different candidate histories", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "Compare two hypothetical alternatives—not two packets existing at once. No phase or law yet.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    draw_candidate_panel(draw, (35, 108, 625, 583), "Candidate A", GREEN, LIGHT_GREEN, candidate_a, u)
    draw_candidate_panel(draw, (655, 108, 1245, 583), "Candidate B", PURPLE, LIGHT_PURPLE, candidate_b, u)
    draw_s_progress(draw, u)

    if final_hold:
        footer = "Same A and B. Different intermediate (x̄, k̄). Each curve is one candidate summary history."
        draw_text(draw, (640, 681), footer, fill=GREEN, font_obj=FINAL, anchor="mm")
    else:
        footer = "At the same intermediate s, the two candidates generally give different summaries."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (1.0, 3.3, 5.7, 8.7, 11.2)
    labels = ("same start", "different intermediates", "same s", "same finish", "two complete candidates")
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
    name = "symmetry-step4-alternate-packet-summary-histories"
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
