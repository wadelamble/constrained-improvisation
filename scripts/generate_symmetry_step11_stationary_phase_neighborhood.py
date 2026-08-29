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
DURATION = 14.0
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
LIGHT_GREEN = (181, 210, 193)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

LEFT_PLOT = (92.0, 190.0, 680.0, 508.0)
N_TERMS = 55
EPSILONS = tuple(-1.4 + 2.8 * index / (N_TERMS - 1) for index in range(N_TERMS))
PHI_0 = 0.62
PHASES = tuple(PHI_0 + 9.0 * epsilon * epsilon for epsilon in EPSILONS)
STATIONARY_WIDTH = 0.31


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


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 4,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 8.0
    p1 = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    p2 = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=color)


def x_of_u(u: float, epsilon: float) -> float:
    base_x = 0.16 + 0.70 * u + 0.10 * math.sin(math.pi * u)
    variation = 0.105 * epsilon * math.sin(math.pi * u)
    return base_x + variation


def map_path_point(u: float, epsilon: float) -> tuple[float, float]:
    left, top, right, bottom = LEFT_PLOT
    x = x_of_u(u, epsilon)
    px = left + x / 1.10 * (right - left)
    py = bottom - u * (bottom - top)
    return px, py


def path_points(epsilon: float, samples: int = 260) -> list[tuple[int, int]]:
    return [tuple(s(v) for v in map_path_point(index / (samples - 1), epsilon)) for index in range(samples)]


def draw_left_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (35, 108, 710, 643))
    draw_text(draw, (58, 129), "one variation through candidate space", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "only the x-s projection is drawn; every candidate also has segment labels {kⱼ(ε)}", fill=MUTED, font_obj=SMALL)

    left, top, right, bottom = LEFT_PLOT
    for index in range(1, 5):
        px = left + (right - left) * index / 5
        py = top + (bottom - top) * index / 5
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.64), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.64), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (right + 1, bottom + 22), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 10, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    representatives = (-1.30, -1.05, -0.80, -0.55, -0.30, 0.0, 0.30, 0.55, 0.80, 1.05, 1.30)
    for epsilon in representatives:
        if abs(epsilon) <= STATIONARY_WIDTH:
            color = rgba(LIGHT_GREEN, 0.62 if final_hold else 0.38)
            width = 3
        else:
            color = rgba(BLUE, 0.25)
            width = 2
        draw.line(path_points(epsilon), fill=color, width=s(width), joint="curve")

    current_index = min(N_TERMS - 1, int(math.floor(reveal * N_TERMS)))
    current_epsilon = EPSILONS[current_index]
    if reveal < 0.999:
        current_color = GREEN if abs(current_epsilon) <= STATIONARY_WIDTH else GOLD
        draw.line(path_points(current_epsilon), fill=current_color, width=s(6), joint="curve")
        draw_text(
            draw,
            (374, 556),
            "near ε=0: phase turns slowly" if abs(current_epsilon) <= STATIONARY_WIDTH else "away from ε=0: phase turns rapidly",
            fill=current_color,
            font_obj=LABEL_BOLD,
            anchor="mm",
        )
    else:
        draw.line(path_points(0.0), fill=GREEN, width=s(6), joint="curve")
        draw_text(draw, (374, 556), "green family = stationary neighborhood; center curve has ε=0", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")

    start = map_path_point(0.0, 0.0)
    finish = map_path_point(1.0, 0.0)
    for point in (start, finish):
        draw.ellipse((s(point[0] - 9), s(point[1] - 9), s(point[0] + 9), s(point[1] + 9)), fill=INK)
    draw_text(draw, (start[0] - 12, start[1] + 15), "A", fill=INK, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 12, finish[1] - 10), "B", fill=INK, font_obj=LABEL_BOLD)


def cumulative_phasors() -> list[tuple[float, float]]:
    points = [(0.0, 0.0)]
    for phase in PHASES:
        x, y = points[-1]
        points.append((x + math.cos(phase), y + math.sin(phase)))
    return points


CUMULATIVE = cumulative_phasors()


def phasor_mapper():
    left, top, right, bottom = 745.0, 270.0, 1215.0, 508.0
    xs = [point[0] for point in CUMULATIVE] + [0.0]
    ys = [point[1] for point in CUMULATIVE] + [0.0]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1.0)
    span_y = max(max_y - min_y, 1.0)
    scale = min((right - left - 54) / span_x, (bottom - top - 44) / span_y)
    offset_x = (left + right) / 2 - scale * (min_x + max_x) / 2
    offset_y = (top + bottom) / 2 + scale * (min_y + max_y) / 2

    def mapper(point: tuple[float, float]) -> tuple[float, float]:
        return offset_x + scale * point[0], offset_y - scale * point[1]

    return mapper, (left, top, right, bottom)


MAP_PHASOR, PHASOR_BOX = phasor_mapper()


def draw_right_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (735, 108, 1245, 643))
    draw_text(draw, (757, 129), "tip-to-tail contributions from this family", font_obj=PANE_TITLE)
    draw_text(draw, (757, 158), "equal lengths isolate phase; candidates are sampled in increasing ε", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (990, 198), "stationary at ε=0:   dΦ/dε = 0", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (990, 229), "Φ(ε) = Φ(0) + ½Φ″(0)ε² + O(ε³)", fill=INK, font_obj=LABEL_BOLD, anchor="mm")

    left, top, right, bottom = PHASOR_BOX
    origin = MAP_PHASOR((0.0, 0.0))
    draw.line((s(left), s(origin[1]), s(right), s(origin[1])), fill=rgba(MUTED, 0.20), width=s(1))
    draw.line((s(origin[0]), s(top), s(origin[0]), s(bottom)), fill=rgba(MUTED, 0.20), width=s(1))
    draw.ellipse((s(origin[0] - 4), s(origin[1] - 4), s(origin[0] + 4), s(origin[1] + 4)), fill=INK)

    scaled = reveal * N_TERMS
    complete = min(N_TERMS, int(math.floor(scaled)))
    fraction = scaled - complete if complete < N_TERMS else 0.0
    central_midpoint: tuple[float, float] | None = None

    for index in range(complete):
        start = MAP_PHASOR(CUMULATIVE[index])
        finish = MAP_PHASOR(CUMULATIVE[index + 1])
        epsilon = EPSILONS[index]
        color = GREEN if abs(epsilon) <= STATIONARY_WIDTH else rgba(BLUE, 0.72)
        draw_arrow(draw, start, finish, color, width=5 if abs(epsilon) <= STATIONARY_WIDTH else 3)
        if abs(epsilon) <= 0.03:
            central_midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)

    if complete < N_TERMS and fraction > 0:
        start_raw = CUMULATIVE[complete]
        phase = PHASES[complete]
        current_raw = (start_raw[0] + fraction * math.cos(phase), start_raw[1] + fraction * math.sin(phase))
        current_color = GREEN if abs(EPSILONS[complete]) <= STATIONARY_WIDTH else GOLD
        draw_arrow(draw, MAP_PHASOR(start_raw), MAP_PHASOR(current_raw), current_color, width=6)

    if complete > 0:
        current = min(complete - 1, N_TERMS - 1)
        epsilon = EPSILONS[current]
        if abs(epsilon) <= STATIONARY_WIDTH:
            note = "near stationarity: neighboring arrows remain nearly aligned"
            color = GREEN
        else:
            note = "rapid phase sweep: arrows wind and largely cancel"
            color = BLUE
        draw_text(draw, (990, 536), note, fill=color, font_obj=LABEL_BOLD, anchor="mm")

    if final_hold:
        total = MAP_PHASOR(CUMULATIVE[-1])
        draw_arrow(draw, origin, total, GOLD, width=7)
        draw_text(draw, (990, 562), "gold = resultant from the entire sampled family", fill=GOLD, font_obj=SMALL, anchor="mm")
        if central_midpoint is not None:
            draw_text(draw, (central_midpoint[0] + 12, central_midpoint[1] - 11), "coherent neighborhood", fill=GREEN, font_obj=SMALL)
    else:
        draw_text(draw, (990, 562), "every arrow still comes from accumulated per-segment mode phases", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    reveal = interval(seconds, 1.2, 10.3)
    final_hold = seconds >= 10.6

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 11 — Stationary phase makes a neighborhood reinforce", font_obj=TITLE)
    if final_hold:
        subtitle = "Full stationarity: first-order phase change vanishes for every allowed fixed-endpoint variation."
        subtitle_color = GREEN
    else:
        current_index = min(N_TERMS - 1, int(math.floor(reveal * N_TERMS)))
        if abs(EPSILONS[current_index]) <= STATIONARY_WIDTH:
            subtitle = "Nearby stationary terms change angle only at second order, so their contributions reinforce."
        elif reveal > 0:
            subtitle = "Where phase sweeps at first order, neighboring contributions largely cancel."
        else:
            subtitle = "One drawn variation tests one direction through the full space of candidate terms."
        subtitle_color = MUTED
    draw_text(draw, (42, 72), subtitle, fill=subtitle_color, font_obj=SUBTITLE)

    draw_left_panel(draw, reveal, final_hold)
    draw_right_panel(draw, reveal, final_hold)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 3.3, 5.7, 8.0, 11.7)
    labels = ("one variation", "rapid phase winding", "stationary neighborhood", "winding resumes", "resultant")
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
    name = "symmetry-step11-stationary-phase-neighborhood"
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
