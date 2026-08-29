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

N_SEGMENTS = 6
PATH_PLOT = (70.0, 210.0, 420.0, 514.0)
ROW_X = tuple(515.0 + 54.0 * index for index in range(N_SEGMENTS))
ROW_Y = tuple(250.0 + 48.0 * index for index in range(6))

# Each row is one complete assignment of a Fourier-mode label to every segment
# of the same fixed spatial candidate.
K_ASSIGNMENTS = (
    (1.25, 1.35, 1.15, 1.30, 1.40, 1.20),
    (1.75, 1.95, 1.70, 1.80, 2.00, 1.85),
    (2.40, 2.60, 2.30, 2.70, 2.50, 2.40),
    (3.00, 3.40, 3.20, 3.60, 3.30, 3.10),
    (3.80, 4.20, 4.00, 4.30, 4.10, 3.90),
    (4.80, 5.00, 4.70, 5.20, 4.90, 5.10),
)


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
    size = 8.5
    p1 = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    p2 = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=color)


def x_of_u(u: float) -> float:
    return 0.16 + 0.72 * u + 0.14 * math.sin(math.pi * u)


def omega(k: float) -> float:
    return 0.18 + 0.34 * k * k


def map_path_point(u: float) -> tuple[float, float]:
    left, top, right, bottom = PATH_PLOT
    px = left + x_of_u(u) / 1.12 * (right - left)
    py = bottom - u * (bottom - top)
    return px, py


def path_points(samples: int = 320) -> list[tuple[int, int]]:
    return [tuple(s(value) for value in map_path_point(index / (samples - 1))) for index in range(samples)]


def assignment_phase(assignment: tuple[float, ...]) -> float:
    total = 0.0
    for index, k_value in enumerate(assignment):
        u0 = index / N_SEGMENTS
        u1 = (index + 1) / N_SEGMENTS
        total += k_value * (x_of_u(u1) - x_of_u(u0)) - omega(k_value) * (u1 - u0)
    return total


PHASES = tuple(assignment_phase(assignment) for assignment in K_ASSIGNMENTS)
VECTORS = tuple((math.cos(phase), math.sin(phase)) for phase in PHASES)


def cumulative_vectors() -> tuple[tuple[float, float], ...]:
    points = [(0.0, 0.0)]
    for dx, dy in VECTORS:
        x_value, y_value = points[-1]
        points.append((x_value + dx, y_value + dy))
    return tuple(points)


CUMULATIVE = cumulative_vectors()


def make_phasor_mapper():
    left, top, right, bottom = 888.0, 270.0, 1220.0, 500.0
    xs = [point[0] for point in CUMULATIVE] + [0.0]
    ys = [point[1] for point in CUMULATIVE] + [0.0]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    scale = min((right - left - 50) / span_x, (bottom - top - 42) / span_y)
    offset_x = (left + right) / 2 - scale * (min_x + max_x) / 2
    offset_y = (top + bottom) / 2 + scale * (min_y + max_y) / 2

    def mapper(point: tuple[float, float]) -> tuple[float, float]:
        return offset_x + scale * point[0], offset_y - scale * point[1]

    return mapper, (left, top, right, bottom)


MAP_PHASOR, PHASOR_BOX = make_phasor_mapper()


def draw_fixed_path_panel(draw: ImageDraw.ImageDraw, active_assignment: int | None, final_hold: bool) -> None:
    panel(draw, (35, 108, 440, 625))
    draw_text(draw, (58, 129), "hold one spatial candidate fixed", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "same x(s), hence the same Δxⱼ and Δsⱼ, in every row", fill=MUTED, font_obj=SMALL)

    left, top, right, bottom = PATH_PLOT
    for index in range(1, 4):
        px = left + (right - left) * index / 4
        py = top + (bottom - top) * index / 4
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.60), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.60), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (right, bottom + 21), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 9, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")
    draw.line(path_points(), fill=BLUE, width=s(5), joint="curve")

    for index in range(N_SEGMENTS + 1):
        point = map_path_point(index / N_SEGMENTS)
        draw.ellipse(
            (s(point[0] - 5), s(point[1] - 5), s(point[0] + 5), s(point[1] + 5)),
            fill=INK if index in (0, N_SEGMENTS) else rgba(MUTED, 0.78),
        )

    start = map_path_point(0.0)
    finish = map_path_point(1.0)
    draw_text(draw, (start[0] - 11, start[1] + 15), "A", font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 11, finish[1] - 9), "B", font_obj=LABEL_BOLD)

    if active_assignment is not None:
        for segment in range(N_SEGMENTS):
            u0 = segment / N_SEGMENTS
            u1 = (segment + 1) / N_SEGMENTS
            midpoint = map_path_point((u0 + u1) / 2)
            draw.ellipse(
                (s(midpoint[0] - 5), s(midpoint[1] - 5), s(midpoint[0] + 5), s(midpoint[1] + 5)),
                fill=GOLD,
            )
        draw_text(
            draw,
            (238, 558),
            f"read assignment r={active_assignment} across this same path",
            fill=GOLD,
            font_obj=SMALL,
            anchor="mm",
        )
    elif final_hold:
        draw_text(draw, (238, 558), "x(s) never changed", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (238, 558), "only the mode labels will vary", fill=MUTED, font_obj=SMALL, anchor="mm")


def row_point(row: int, column: int, k_value: float) -> tuple[float, float]:
    baseline = ROW_Y[row]
    normalized = (k_value - 3.1) / 2.25
    return ROW_X[column], baseline - 13.5 * normalized


def draw_assignment_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (455, 108, 850, 625))
    draw_text(draw, (478, 129), "vary the mode assignment k⁽ʳ⁾(s)", font_obj=PANE_TITLE)
    draw_text(draw, (478, 158), "row r chooses one kⱼ⁽ʳ⁾ on every segment j", fill=MUTED, font_obj=SMALL)
    draw_text(
        draw,
        (652, 194),
        "Φ⁽ʳ⁾[x] = Σⱼ [kⱼ⁽ʳ⁾ Δxⱼ − ω(kⱼ⁽ʳ⁾) Δsⱼ]",
        font_obj=SMALL,
        anchor="mm",
    )

    for column, x_value in enumerate(ROW_X):
        draw_text(draw, (x_value, 222), f"j={column}", fill=MUTED, font_obj=SMALL, anchor="mm")

    scaled = reveal * len(K_ASSIGNMENTS)
    completed = min(len(K_ASSIGNMENTS), int(math.floor(scaled)))
    active = completed if completed < len(K_ASSIGNMENTS) else None
    fraction = scaled - completed if active is not None else 0.0

    for row, assignment in enumerate(K_ASSIGNMENTS):
        baseline = ROW_Y[row]
        draw_text(draw, (486, baseline), f"r={row}", fill=MUTED, font_obj=SMALL, anchor="rm")
        draw.line((s(504), s(baseline), s(824), s(baseline)), fill=rgba(GRID, 0.62), width=s(1))
        if row < completed:
            row_fraction = 1.0
            color = rgba(BLUE, 0.76)
            width = 3
        elif row == active and fraction > 0:
            row_fraction = fraction
            color = GOLD
            width = 5
        else:
            continue

        points = [row_point(row, column, k_value) for column, k_value in enumerate(assignment)]
        scaled_columns = row_fraction * (N_SEGMENTS - 1)
        complete_segments = min(N_SEGMENTS - 1, int(math.floor(scaled_columns)))
        partial = scaled_columns - complete_segments if complete_segments < N_SEGMENTS - 1 else 0.0
        for column in range(complete_segments):
            p0 = points[column]
            p1 = points[column + 1]
            draw.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=color, width=s(width))
        if complete_segments < N_SEGMENTS - 1 and partial > 0:
            p0 = points[complete_segments]
            p1 = points[complete_segments + 1]
            current = (p0[0] + partial * (p1[0] - p0[0]), p0[1] + partial * (p1[1] - p0[1]))
            draw.line((s(p0[0]), s(p0[1]), s(current[0]), s(current[1])), fill=color, width=s(width))

        visible_points = max(1, min(N_SEGMENTS, complete_segments + 1 + (1 if partial > 0.12 else 0)))
        for point in points[:visible_points]:
            draw.ellipse((s(point[0] - 4), s(point[1] - 4), s(point[0] + 4), s(point[1] + 4)), fill=color)

    if final_hold:
        draw_text(draw, (652, 558), "six representatives stand in for all k(s) assignments", fill=GREEN, font_obj=SMALL, anchor="mm")
    elif active is not None and fraction > 0:
        draw_text(draw, (652, 558), f"one whole row supplies phase Φ⁽{active}⁾[x]", fill=GOLD, font_obj=SMALL, anchor="mm")
    else:
        draw_text(draw, (652, 558), "the path is fixed; the row is what changes", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_phasor_panel(draw: ImageDraw.ImageDraw, reveal: float, final_hold: bool) -> None:
    panel(draw, (865, 108, 1245, 625))
    draw_text(draw, (888, 129), "sum the mode assignments", font_obj=PANE_TITLE)
    draw_text(draw, (888, 158), "one complete row contributes one complex arrow", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (1055, 192), "A[x] ≈ Σᵣ wᵣ exp(iΦ⁽ʳ⁾[x])", font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (1055, 218), "→  ∫ Dk exp(iΦ[x,k])", font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (1055, 244), "representative equal-weight arrows; the actual sum is continuous", fill=MUTED, font_obj=SMALL, anchor="mm")

    left, top, right, bottom = PHASOR_BOX
    origin = MAP_PHASOR((0.0, 0.0))
    draw.line((s(left), s(origin[1]), s(right), s(origin[1])), fill=rgba(MUTED, 0.23), width=s(1))
    draw.line((s(origin[0]), s(top), s(origin[0]), s(bottom)), fill=rgba(MUTED, 0.23), width=s(1))
    draw.ellipse((s(origin[0] - 4), s(origin[1] - 4), s(origin[0] + 4), s(origin[1] + 4)), fill=INK)

    scaled = reveal * len(VECTORS)
    completed = min(len(VECTORS), int(math.floor(scaled)))
    active = completed if completed < len(VECTORS) else None
    fraction = scaled - completed if active is not None else 0.0

    for index in range(completed):
        start = MAP_PHASOR(CUMULATIVE[index])
        finish = MAP_PHASOR(CUMULATIVE[index + 1])
        draw_arrow(draw, start, finish, rgba(BLUE, 0.78), width=4)
        midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        draw_text(draw, (midpoint[0] + 5, midpoint[1] - 7), f"r={index}", fill=BLUE, font_obj=SMALL)

    if active is not None and fraction > 0:
        start_raw = CUMULATIVE[active]
        dx, dy = VECTORS[active]
        current_raw = (start_raw[0] + fraction * dx, start_raw[1] + fraction * dy)
        draw_arrow(draw, MAP_PHASOR(start_raw), MAP_PHASOR(current_raw), GOLD, width=6)
        draw_text(draw, (1055, 542), f"add the contribution from assignment r={active}", fill=GOLD, font_obj=SMALL, anchor="mm")
    elif final_hold:
        total = MAP_PHASOR(CUMULATIVE[-1])
        draw_arrow(draw, origin, total, GREEN, width=7)
        draw_text(draw, (1055, 542), "green arrow = A[x] for this one spatial path", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (1055, 542), "the mode-assignment sum has not begun", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    reveal = interval(seconds, 1.3, 9.5)
    final_hold = seconds >= 9.8
    scaled = reveal * len(K_ASSIGNMENTS)
    completed = min(len(K_ASSIGNMENTS), int(math.floor(scaled)))
    active = completed if completed < len(K_ASSIGNMENTS) and scaled - completed > 0 else None

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 9.5 — Sum mode assignments for one fixed spatial candidate", font_obj=TITLE)
    if final_hold:
        subtitle = "After summing every k(s) assignment, this spatial path contributes one amplitude A[x]."
        subtitle_color = GREEN
    else:
        subtitle = "Keep x(s) fixed; vary the complete sequence k₀, …, kₙ₋₁ attached to its segments."
        subtitle_color = MUTED
    draw_text(draw, (42, 72), subtitle, fill=subtitle_color, font_obj=SUBTITLE)

    draw_fixed_path_panel(draw, active, final_hold)
    draw_assignment_panel(draw, reveal, final_hold)
    draw_phasor_panel(draw, reveal, final_hold)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 2.7, 5.0, 7.4, 11.1)
    labels = ("fixed spatial path", "first mode assignments", "same path, new rows", "phasors accumulate", "one amplitude A[x]")
    thumb_w = 384
    thumb_h = 216
    label_h = 26
    margin = 15
    sheet = Image.new("RGB", (3 * thumb_w + 4 * margin, 2 * (thumb_h + label_h) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(zip(sample_seconds, labels)):
        col = index % 3
        row = index // 3
        x_value = margin + col * (thumb_w + margin)
        y_value = margin + row * (thumb_h + label_h + margin)
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x_value, y_value))
        sheet_draw.text((x_value + 4, y_value + thumb_h + 4), label, fill=MUTED)
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
    name = "symmetry-step9-5-sum-modes-for-fixed-candidate"
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
