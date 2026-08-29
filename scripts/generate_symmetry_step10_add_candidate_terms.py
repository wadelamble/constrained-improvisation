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
DURATION = 13.5
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GRID = base.GRID
GREEN = base.GREEN
GOLD = base.GOLD
BLUE = base.BLUE
LIGHT_BLUE = base.LIGHT_BLUE

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

LEFT_PLOT = (88.0, 186.0, 755.0, 562.0)
S_LEVELS = (0.0, 1 / 3, 2 / 3, 1.0)
CANDIDATES = (
    (0.15, 0.25, 0.50, 0.82),
    (0.15, 0.40, 0.60, 0.82),
    (0.15, 0.57, 0.45, 0.82),
    (0.15, 0.68, 0.72, 0.82),
    (0.15, 0.34, 0.78, 0.82),
    (0.15, 0.52, 0.30, 0.82),
)
PHASE_ANGLES = (0.35, 1.25, 2.45, -1.00, 0.70, -2.40)
WEIGHTS = (1.00, 0.85, 0.72, 0.90, 0.78, 0.68)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def interval(seconds: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0 if seconds >= end else 0.0
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
    left, _, right, _ = LEFT_PLOT
    return left + x * (right - left)


def map_s(u: float) -> float:
    _, top, _, bottom = LEFT_PLOT
    return bottom - u * (bottom - top)


def candidate_points(candidate: tuple[float, ...]) -> list[tuple[float, float]]:
    return [(map_x(x), map_s(u)) for x, u in zip(candidate, S_LEVELS)]


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 4,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 9.0
    p1 = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    p2 = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=color)


def draw_wave_slice(draw: ImageDraw.ImageDraw, u: float, phase: float) -> None:
    left, _, right, _ = LEFT_PLOT
    baseline = map_s(u)
    points: list[tuple[int, int]] = []
    for index in range(320):
        p = index / 319
        x = left + p * (right - left)
        envelope = math.sin(math.pi * p) ** 0.65
        y = baseline - 8.0 * envelope * math.sin(8 * math.pi * p + phase)
        points.append((s(x), s(y)))
    draw.line(points, fill=rgba(LIGHT_BLUE, 0.50), width=s(2), joint="curve")
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(GRID, 0.62), width=s(1))


def draw_partial_candidate(
    draw: ImageDraw.ImageDraw,
    candidate_index: int,
    partial: float,
    color,
    width: int,
) -> None:
    points = candidate_points(CANDIDATES[candidate_index])
    scaled = partial * (len(points) - 1)
    complete = min(len(points) - 1, int(math.floor(scaled)))
    fraction = min(1.0, max(0.0, scaled - complete))
    for index in range(complete):
        draw.line(
            (s(points[index][0]), s(points[index][1]), s(points[index + 1][0]), s(points[index + 1][1])),
            fill=color,
            width=s(width),
        )
    if complete < len(points) - 1 and fraction > 0:
        start = points[complete]
        finish = points[complete + 1]
        current = (start[0] + fraction * (finish[0] - start[0]), start[1] + fraction * (finish[1] - start[1]))
        draw.line((s(start[0]), s(start[1]), s(current[0]), s(current[1])), fill=color, width=s(width))


def draw_left_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (35, 108, 785, 643))
    draw_text(draw, (58, 129), "representative candidate terms connect the same endpoints", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "one term = intermediate x-values + one Fourier-mode label kⱼ per segment", fill=MUTED, font_obj=SMALL)

    left, top, right, bottom = LEFT_PLOT
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (right + 1, bottom + 22), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 10, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    draw_wave_slice(draw, 1 / 3, 0.7)
    draw_wave_slice(draw, 2 / 3, 1.9)
    draw_text(draw, (right - 8, map_s(1 / 3) + 18), "wave on intermediate slice", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (right - 8, map_s(2 / 3) + 18), "wave on intermediate slice", fill=MUTED, font_obj=SMALL, anchor="ra")

    scaled = reveal * len(CANDIDATES)
    completed = min(len(CANDIDATES), int(math.floor(scaled)))
    active = completed if completed < len(CANDIDATES) else None
    active_fraction = scaled - completed if active is not None else 0.0

    for index in range(completed):
        draw_partial_candidate(draw, index, 1.0, rgba(BLUE, 0.53 if not final_hold else 0.38), 3)
    if active is not None and active_fraction > 0:
        draw_partial_candidate(draw, active, active_fraction, GOLD, 6)

    if active is not None and active_fraction > 0.12:
        points = candidate_points(CANDIDATES[active])
        for point_index, point in enumerate(points[1:-1], start=1):
            draw.ellipse((s(point[0] - 7), s(point[1] - 7), s(point[0] + 7), s(point[1] + 7)), fill=GOLD)
        for segment_index in range(3):
            p0 = points[segment_index]
            p1 = points[segment_index + 1]
            mid = ((p0[0] + p1[0]) / 2 + 8, (p0[1] + p1[1]) / 2 - 9)
            draw_text(draw, mid, f"k{segment_index}", fill=GOLD, font_obj=SMALL)
        draw_text(draw, (418, 594), f"highlighted term γ{active}: one selected mode contribution on every segment", fill=GOLD, font_obj=SMALL, anchor="mm")
    elif final_hold:
        draw_text(draw, (418, 594), "representative terms shown; the continuum of terms is not drawn", fill=BLUE, font_obj=SMALL, anchor="mm")
    else:
        draw_text(draw, (418, 594), "composing the linear wave map produces these alternative sequences", fill=MUTED, font_obj=SMALL, anchor="mm")

    start = candidate_points(CANDIDATES[0])[0]
    finish = candidate_points(CANDIDATES[0])[-1]
    for p in (start, finish):
        draw.ellipse((s(p[0] - 9), s(p[1] - 9), s(p[0] + 9), s(p[1] + 9)), fill=INK)
    draw_text(draw, (start[0] - 12, start[1] + 15), "A", fill=INK, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 12, finish[1] - 10), "B", fill=INK, font_obj=LABEL_BOLD)


def phasor_vectors() -> list[tuple[float, float]]:
    return [(weight * math.cos(angle), weight * math.sin(angle)) for weight, angle in zip(WEIGHTS, PHASE_ANGLES)]


VECTORS = phasor_vectors()


def cumulative_points() -> list[tuple[float, float]]:
    points = [(0.0, 0.0)]
    for dx, dy in VECTORS:
        x, y = points[-1]
        points.append((x + dx, y + dy))
    return points


CUMULATIVE = cumulative_points()


def map_phasor(point: tuple[float, float]) -> tuple[float, float]:
    cx, cy, scale = 1014.0, 436.0, 78.0
    return cx + scale * point[0], cy - scale * point[1]


def draw_right_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (810, 108, 1245, 643))
    draw_text(draw, (832, 129), "add the candidate terms tip to tail", font_obj=PANE_TITLE)
    draw_text(draw, (832, 158), "direction = accumulated per-mode phase; length = nonnegative weight", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (1027, 198), "schematically: K(B,A) = Σγ wγ e^{iΦγ}", fill=INK, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (1027, 229), "one slice: K(B,A) = ∫ K(B,x₁)K(x₁,A) dx₁", fill=MUTED, font_obj=SMALL, anchor="mm")

    cx, cy = map_phasor((0.0, 0.0))
    draw.line((s(842), s(cy), s(1215), s(cy)), fill=rgba(MUTED, 0.23), width=s(1))
    draw.line((s(cx), s(263), s(cx), s(570)), fill=rgba(MUTED, 0.23), width=s(1))
    draw.ellipse((s(cx - 4), s(cy - 4), s(cx + 4), s(cy + 4)), fill=INK)

    scaled = reveal * len(VECTORS)
    completed = min(len(VECTORS), int(math.floor(scaled)))
    active = completed if completed < len(VECTORS) else None
    fraction = scaled - completed if active is not None else 0.0

    for index in range(completed):
        start = map_phasor(CUMULATIVE[index])
        finish = map_phasor(CUMULATIVE[index + 1])
        draw_arrow(draw, start, finish, rgba(BLUE, 0.78), width=4)
        mid = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        draw_text(draw, (mid[0] + 5, mid[1] - 8), f"γ{index}", fill=BLUE, font_obj=SMALL)
    if active is not None and fraction > 0:
        start_vec = CUMULATIVE[active]
        dx, dy = VECTORS[active]
        current_vec = (start_vec[0] + fraction * dx, start_vec[1] + fraction * dy)
        draw_arrow(draw, map_phasor(start_vec), map_phasor(current_vec), GOLD, width=6)
        draw_text(draw, (1027, 585), f"add the complex contribution from highlighted term γ{active}", fill=GOLD, font_obj=SMALL, anchor="mm")
    elif final_hold:
        origin = map_phasor((0.0, 0.0))
        total = map_phasor(CUMULATIVE[-1])
        draw_arrow(draw, origin, total, GREEN, width=7)
        draw_text(draw, (1027, 585), "green arrow = total complex amplitude at B", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (1027, 585), "the sum has not begun", fill=MUTED, font_obj=SMALL, anchor="mm")

    draw_text(draw, (1027, 615), "These are terms in one linear wave calculation—not observed trajectories.", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    reveal = interval(seconds, 1.4, 9.4)
    final_hold = seconds >= 9.7

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 10 — Linear wave propagation adds candidate terms", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "Each candidate sequence supplies one weighted complex contribution to the same endpoint.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    draw_left_panel(draw, reveal, final_hold)
    draw_right_panel(draw, reveal, final_hold)

    if final_hold:
        footer = "Linearity makes every intermediate position—and every segment mode kⱼ—contribute to the amplitude at B."
        draw_text(draw, (640, 681), footer, fill=GREEN, font_obj=FINAL, anchor="mm")
    else:
        footer = "Within each term, per-mode segment factors multiply. Across different terms, complex contributions add."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.9, 3.0, 5.1, 7.4, 11.2)
    labels = ("wave slices", "first candidate terms", "mode labels per segment", "tip-to-tail sum", "total amplitude")
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
    name = "symmetry-step10-add-candidate-terms"
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
