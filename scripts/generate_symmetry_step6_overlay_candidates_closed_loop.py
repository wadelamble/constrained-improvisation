from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

import generate_symmetry_step2_packet_summary_point as base
import generate_symmetry_step4_alternate_summary_histories as candidates


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = base.FFMPEG
FFPROBE = base.FFPROBE

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
DURATION = 13.0
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GREEN = base.GREEN
PURPLE = (117, 85, 145)
GOLD = (198, 138, 45)
LIGHT_GOLD = (238, 216, 170)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

X_MIN = candidates.X_MIN
X_MAX = candidates.X_MAX
K_MIN = candidates.K_MIN
K_MAX = candidates.K_MAX
PLOT = (185.0, 180.0, 1095.0, 570.0)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def interval(seconds: float, start: float, end: float) -> float:
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


def map_x(x: float) -> float:
    left, _, right, _ = PLOT
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def map_k(k: float) -> float:
    _, top, _, bottom = PLOT
    return bottom - (k - K_MIN) / (K_MAX - K_MIN) * (bottom - top)


def point(candidate, u: float) -> tuple[float, float]:
    x, k = candidate(u)
    return map_x(x), map_k(k)


def path(candidate, start: float, end: float, samples: int = 260) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(samples):
        u = start + (end - start) * index / (samples - 1)
        px, py = point(candidate, u)
        points.append((s(px), s(py)))
    return points


def partial_path(candidate, upto: float) -> list[tuple[int, int]]:
    count = max(2, round(260 * max(upto, 0.005)))
    return path(candidate, 0.0, max(upto, 0.005), count)


def draw_arrowhead(draw: ImageDraw.ImageDraw, candidate, u: float, forward: bool, color) -> None:
    delta = 0.008
    u0 = max(0.0, min(1.0, u - delta if forward else u + delta))
    p0 = point(candidate, u0)
    p1 = point(candidate, u)
    angle = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    size = 11.0
    left = (p1[0] - size * math.cos(angle - math.pi / 6), p1[1] - size * math.sin(angle - math.pi / 6))
    right = (p1[0] - size * math.cos(angle + math.pi / 6), p1[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([(s(p1[0]), s(p1[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    left, top, right, bottom = PLOT
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw_text(draw, (right + 2, bottom + 22), "x-shift a", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 8, top), "k-shift b", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")


def draw_endpoints(draw: ImageDraw.ImageDraw) -> None:
    start = point(candidates.candidate_a, 0.0)
    end = point(candidates.candidate_a, 1.0)
    for p in (start, end):
        draw.ellipse((s(p[0] - 8), s(p[1] - 8), s(p[0] + 8), s(p[1] + 8)), fill=INK)
    draw_text(draw, (start[0] - 13, start[1] + 16), "A: shared start", fill=INK, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (end[0] + 13, end[1] - 11), "B: shared finish", fill=INK, font_obj=LABEL_BOLD)


def draw_region(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0:
        return
    polygon = path(candidates.candidate_a, 0.0, 1.0, 280) + path(candidates.candidate_b, 1.0, 0.0, 280)
    draw.polygon(polygon, fill=rgba(LIGHT_GOLD, 0.32 * alpha))


def draw_traversal(draw: ImageDraw.ImageDraw, loop_progress: float) -> None:
    if loop_progress <= 0:
        return
    if loop_progress <= 0.5:
        u = loop_progress * 2.0
        trail = path(candidates.candidate_a, 0.0, max(u, 0.005), max(2, round(230 * max(u, 0.005))))
        draw.line(trail, fill=GOLD, width=s(7), joint="curve")
        current = point(candidates.candidate_a, u)
        draw.ellipse((s(current[0] - 9), s(current[1] - 9), s(current[0] + 9), s(current[1] + 9)), fill=GOLD)
        if u > 0.03:
            draw_arrowhead(draw, candidates.candidate_a, u, True, GOLD)
        draw_text(draw, (640, 606), "follow Candidate A forward: A → B", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")
    else:
        u = 2.0 - loop_progress * 2.0
        draw.line(path(candidates.candidate_a, 0.0, 1.0), fill=GOLD, width=s(7), joint="curve")
        trail = path(candidates.candidate_b, 1.0, min(0.995, u), max(2, round(230 * max(1.0 - u, 0.005))))
        draw.line(trail, fill=GOLD, width=s(7), joint="curve")
        current = point(candidates.candidate_b, u)
        draw.ellipse((s(current[0] - 9), s(current[1] - 9), s(current[0] + 9), s(current[1] + 9)), fill=GOLD)
        if u < 0.97:
            draw_arrowhead(draw, candidates.candidate_b, u, False, GOLD)
        draw_text(draw, (640, 606), "then follow Candidate B backward: B → A", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    p_a = interval(seconds, 0.8, 3.4)
    p_b = interval(seconds, 3.5, 6.1)
    loop_progress = interval(seconds, 6.4, 10.0)
    region_alpha = interval(seconds, 10.0, 10.8)
    final_hold = seconds >= 10.8

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 6 — Overlay two candidates to make one closed x-k loop", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "The parameter s runs along each boundary curve; it is not a third axis in this picture.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 108, 1245, 643))
    draw_text(draw, (58, 128), "both displacement histories on the same plane", font_obj=PANE_TITLE)
    draw_text(draw, (1209, 130), "green: A   purple: B", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_axes(draw)

    draw_region(draw, region_alpha)
    if p_a > 0:
        draw.line(partial_path(candidates.candidate_a, p_a), fill=GREEN, width=s(4), joint="curve")
    if p_b > 0:
        draw.line(partial_path(candidates.candidate_b, p_b), fill=PURPLE, width=s(4), joint="curve")
    draw_endpoints(draw)
    if not final_hold:
        draw_traversal(draw, loop_progress)

    if seconds < 3.5:
        footer = "First draw Candidate A from the shared start to the shared finish."
    elif seconds < 6.4:
        footer = "Then draw Candidate B between exactly the same two points."
    elif not final_hold:
        footer = "The reverse traversal of B is only how we close the comparison boundary."
    else:
        footer = "A forward plus B backward is a closed boundary in the two-dimensional x-k plane."
    draw_text(draw, (640, 681), footer, fill=GREEN if final_hold else MUTED, font_obj=FINAL if final_hold else SMALL, anchor="mm")

    if final_hold:
        draw_text(draw, (640, 606), "the shaded region lies in the x-k plane", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (3.3, 6.0, 7.9, 9.8, 12.0)
    labels = ("candidate A", "both candidates", "A forward", "B backward", "closed x-k loop")
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
    name = "symmetry-step6-two-candidates-form-closed-xk-loop"
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
