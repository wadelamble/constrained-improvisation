from __future__ import annotations

import math
import shutil
import subprocess
from dataclasses import dataclass
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
DURATION = 18.0
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GRID = base.GRID
BLUE = base.BLUE
LIGHT_BLUE = base.LIGHT_BLUE
GOLD = base.GOLD
GREEN = base.GREEN

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

NAME = "symmetry-wave-paths-7-all-paths-sum-at-b"

# Two seven-opening screens. The ratios are a scaled version of a simple
# paraxial construction chosen so that the 42 paths away from the straight
# neighborhood wind through almost three phase turns and nearly cancel, while
# the seven closest paths remain strongly coherent.
CENTER_Y = 230.0
SLIT_STEP = 28.0
SEGMENT_X = 252.0
A = (262.0, CENTER_Y)
SCREEN_1_X = A[0] + SEGMENT_X
SCREEN_2_X = SCREEN_1_X + SEGMENT_X
B = (SCREEN_2_X + SEGMENT_X, CENTER_Y)
SLIT_INDICES = tuple(range(-3, 4))
SLIT_YS = tuple(CENTER_Y + SLIT_STEP * index for index in SLIT_INDICES)

# The phase-only demonstration uses equal path weights. The common phase is
# removed, and a final common phase reference is chosen so that the resultant
# lies on the positive real axis.
WAVELENGTH = 26.6448
WAVE_NUMBER = 2.0 * math.pi / WAVELENGTH

INTRO_END = 1.8
FAR_PATH_DURATION = 0.205
FAR_START = INTRO_END
FAR_END = FAR_START + 42 * FAR_PATH_DURATION
FAR_PAUSE_END = FAR_END + 1.15
NEAR_PATH_DURATION = 0.43
NEAR_START = FAR_PAUSE_END
NEAR_END = NEAR_START + 7 * NEAR_PATH_DURATION
RESULT_START = NEAR_END + 0.20
RESULT_END = RESULT_START + 0.85


@dataclass(frozen=True)
class Candidate:
    first: int
    second: int
    points: tuple[tuple[float, float], ...]
    length: float
    raw_phase: float
    near_stationary: bool


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
        tuple(s(value) for value in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def circle(
    draw: ImageDraw.ImageDraw,
    point: tuple[float, float],
    radius: float,
    fill,
    outline=None,
    width: int = 2,
) -> None:
    x, y = point
    draw.ellipse(
        (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
        fill=fill,
        outline=outline,
        width=s(width),
    )


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill,
    width: int = 4,
    head: float = 7.0,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=fill, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (
        end[0] - head * math.cos(angle - math.pi / 6),
        end[1] - head * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - head * math.cos(angle + math.pi / 6),
        end[1] - head * math.sin(angle + math.pi / 6),
    )
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=fill,
    )


def dashed_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill,
    width: int = 2,
    dash: float = 7.0,
    gap: float = 6.0,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    cursor = 0.0
    while cursor < length:
        stop = min(cursor + dash, length)
        u0 = cursor / length
        u1 = stop / length
        draw.line(
            (
                s(start[0] + u0 * dx),
                s(start[1] + u0 * dy),
                s(start[0] + u1 * dx),
                s(start[1] + u1 * dy),
            ),
            fill=fill,
            width=s(width),
        )
        cursor += dash + gap


def candidate_length(points: tuple[tuple[float, float], ...]) -> float:
    return sum(
        math.hypot(points[index + 1][0] - points[index][0], points[index + 1][1] - points[index][1])
        for index in range(len(points) - 1)
    )


def build_candidates() -> tuple[Candidate, ...]:
    straight_length = 3.0 * SEGMENT_X
    candidates: list[Candidate] = []
    for first in SLIT_INDICES:
        for second in SLIT_INDICES:
            points = (
                A,
                (SCREEN_1_X, CENTER_Y + SLIT_STEP * first),
                (SCREEN_2_X, CENTER_Y + SLIT_STEP * second),
                B,
            )
            length = candidate_length(points)
            near = abs(first) <= 1 and abs(second) <= 1 and abs(first - second) <= 1
            candidates.append(
                Candidate(
                    first=first,
                    second=second,
                    points=points,
                    length=length,
                    raw_phase=WAVE_NUMBER * (length - straight_length),
                    near_stationary=near,
                )
            )

    far = sorted(
        (candidate for candidate in candidates if not candidate.near_stationary),
        key=lambda candidate: (candidate.raw_phase, candidate.first, candidate.second),
    )
    near = sorted(
        (candidate for candidate in candidates if candidate.near_stationary),
        key=lambda candidate: (-candidate.raw_phase, candidate.first, candidate.second),
    )
    return tuple(far + near)


CANDIDATES = build_candidates()


def raw_total() -> complex:
    return sum(complex(math.cos(candidate.raw_phase), math.sin(candidate.raw_phase)) for candidate in CANDIDATES)


PHASE_REFERENCE = math.atan2(raw_total().imag, raw_total().real)
PHASES = tuple(candidate.raw_phase - PHASE_REFERENCE for candidate in CANDIDATES)
VECTORS = tuple((math.cos(phase), math.sin(phase)) for phase in PHASES)


def cumulative_points() -> tuple[tuple[float, float], ...]:
    points = [(0.0, 0.0)]
    for dx, dy in VECTORS:
        x, y = points[-1]
        points.append((x + dx, y + dy))
    return tuple(points)


CUMULATIVE = cumulative_points()
FAR_SUBTOTAL = CUMULATIVE[42]
TOTAL = CUMULATIVE[-1]


def make_phasor_mapper():
    bounds = (365.0, 423.0, 915.0, 602.0)
    left, top, right, bottom = bounds
    xs = [point[0] for point in CUMULATIVE] + [0.0, TOTAL[0]]
    ys = [point[1] for point in CUMULATIVE] + [0.0, TOTAL[1]]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    scale = min((right - left - 36.0) / span_x, (bottom - top - 22.0) / span_y)
    offset_x = (left + right) / 2.0 - scale * (min_x + max_x) / 2.0
    offset_y = (top + bottom) / 2.0 + scale * (min_y + max_y) / 2.0

    def mapper(point: tuple[float, float]) -> tuple[float, float]:
        return offset_x + scale * point[0], offset_y - scale * point[1]

    return mapper, bounds


MAP_PHASOR, PHASOR_BOUNDS = make_phasor_mapper()


def draw_screen(draw: ImageDraw.ImageDraw, x: float, label: str) -> None:
    top = 143.0
    bottom = 319.0
    half_gap = 5.5
    cursor = top
    for slit_y in SLIT_YS:
        segment_end = max(cursor, slit_y - half_gap)
        if segment_end > cursor:
            draw.line((s(x), s(cursor), s(x), s(segment_end)), fill=rgba(INK, 0.75), width=s(5))
        cursor = slit_y + half_gap
    if cursor < bottom:
        draw.line((s(x), s(cursor), s(x), s(bottom)), fill=rgba(INK, 0.75), width=s(5))
    for slit_y in SLIT_YS:
        circle(draw, (x, slit_y), 3.2, PANEL, outline=rgba(MUTED, 0.65), width=1)
    draw_text(draw, (x, 326), label, fill=MUTED, font_obj=SMALL, anchor="ma")


def partial_polyline(
    draw: ImageDraw.ImageDraw,
    points: tuple[tuple[float, float], ...],
    progress: float,
    fill,
    width: int,
) -> None:
    progress = max(0.0, min(1.0, progress))
    scaled = progress * (len(points) - 1)
    complete = min(len(points) - 1, int(math.floor(scaled)))
    fraction = min(1.0, max(0.0, scaled - complete))
    for index in range(complete):
        draw.line(
            (
                s(points[index][0]),
                s(points[index][1]),
                s(points[index + 1][0]),
                s(points[index + 1][1]),
            ),
            fill=fill,
            width=s(width),
        )
    if complete < len(points) - 1 and fraction > 0:
        start = points[complete]
        finish = points[complete + 1]
        current = (
            start[0] + fraction * (finish[0] - start[0]),
            start[1] + fraction * (finish[1] - start[1]),
        )
        draw.line(
            (s(start[0]), s(start[1]), s(current[0]), s(current[1])),
            fill=fill,
            width=s(width),
        )


def animation_state(seconds: float) -> tuple[int, int | None, float]:
    if seconds < FAR_START:
        return 0, None, 0.0
    if seconds < FAR_END:
        value = (seconds - FAR_START) / FAR_PATH_DURATION
        completed = min(41, int(math.floor(value)))
        return completed, completed, value - completed
    if seconds < FAR_PAUSE_END:
        return 42, None, 0.0
    if seconds < NEAR_END:
        value = (seconds - NEAR_START) / NEAR_PATH_DURATION
        local = min(6, int(math.floor(value)))
        return 42 + local, 42 + local, value - local
    return 49, None, 0.0


def subtitle_for(seconds: float) -> tuple[str, tuple[int, int, int]]:
    if seconds < FAR_START:
        return "Two seven-opening screens produce 49 complete routes from A to B.", MUTED
    if seconds < FAR_END:
        return "Paths away from the straight neighborhood sweep through phase and largely cancel.", BLUE
    if seconds < FAR_PAUSE_END:
        return "After 42 paths, the running sum has returned almost to its starting point.", BLUE
    if seconds < NEAR_END:
        return "The seven near-straight paths arrive at nearly the same phase and reinforce.", GREEN
    return "The resultant of all 49 complex contributions is the amplitude at B.", GREEN


def draw_upper_panel(
    draw: ImageDraw.ImageDraw,
    completed: int,
    active: int | None,
    active_fraction: float,
    final_hold: bool,
) -> None:
    panel(draw, (35, 93, 1245, 338))
    draw_text(draw, (58, 109), "one opening on each screen makes one complete path", font_obj=PANE_TITLE)
    upper_note = (
        "gold = stationary path; green = its nearest sampled neighbors"
        if final_hold
        else "the highlighted path and highlighted complex arrow are the same contribution"
    )
    draw_text(
        draw,
        (58, 135),
        upper_note,
        fill=GREEN if final_hold else MUTED,
        font_obj=SMALL,
    )

    # The unobstructed line is a quiet reference, not an extra contribution.
    dashed_line(draw, A, B, rgba(GREEN, 0.24 if not final_hold else 0.42), width=2, dash=9, gap=7)
    draw_screen(draw, SCREEN_1_X, "screen 1")
    draw_screen(draw, SCREEN_2_X, "screen 2")

    # Completed paths remain as very faint memory, so the active one never gets
    # lost in the combinatorial mesh.
    for index in range(completed):
        candidate = CANDIDATES[index]
        if final_hold and candidate.near_stationary:
            color = rgba(GREEN, 0.34)
            width = 3
        else:
            color = rgba(BLUE, 0.065 if not final_hold else 0.020)
            width = 2
        partial_polyline(draw, candidate.points, 1.0, color, width)

    if active is not None:
        candidate = CANDIDATES[active]
        path_progress = interval(active_fraction, 0.0, 0.58)
        partial_polyline(draw, candidate.points, path_progress, GOLD, 6)
        if path_progress > 0.34:
            for point in candidate.points[1:-1]:
                circle(draw, point, 7.0, GOLD)
        draw_text(
            draw,
            (1214, 113),
            f"path {active + 1} of 49",
            fill=GOLD,
            font_obj=LABEL_BOLD,
            anchor="ra",
        )
    elif completed:
        draw_text(
            draw,
            (1214, 113),
            f"{completed} of 49 added",
            fill=GREEN if completed == 49 else BLUE,
            font_obj=LABEL_BOLD,
            anchor="ra",
        )

    if final_hold:
        straight = next(candidate for candidate in CANDIDATES if candidate.first == 0 and candidate.second == 0)
        partial_polyline(draw, straight.points, 1.0, GOLD, 6)

    for point, label in ((A, "A"), (B, "B")):
        circle(draw, point, 8.5, INK)
        draw_text(draw, (point[0], point[1] + 26), label, fill=INK, font_obj=LABEL_BOLD, anchor="ma")


def draw_lower_panel(
    draw: ImageDraw.ImageDraw,
    seconds: float,
    completed: int,
    active: int | None,
    active_fraction: float,
    final_hold: bool,
) -> None:
    panel(draw, (35, 354, 1245, 625))
    draw_text(draw, (58, 371), "add one whole-path contribution at a time", font_obj=PANE_TITLE)
    lower_note = (
        "near-straight paths reinforce; the remaining paths largely cancel"
        if final_hold
        else "arrow direction = accumulated phase; equal arrow lengths isolate interference"
    )
    draw_text(
        draw,
        (58, 398),
        lower_note,
        fill=GREEN if final_hold else MUTED,
        font_obj=SMALL,
    )
    draw_text(
        draw,
        (1215, 371),
        "shown in phase order; the final sum is order-independent",
        fill=MUTED,
        font_obj=SMALL,
        anchor="ra",
    )

    left, top, right, bottom = PHASOR_BOUNDS
    origin = MAP_PHASOR((0.0, 0.0))
    draw.line((s(left), s(origin[1]), s(right), s(origin[1])), fill=rgba(MUTED, 0.18), width=s(1))
    draw.line((s(origin[0]), s(top), s(origin[0]), s(bottom)), fill=rgba(MUTED, 0.18), width=s(1))
    draw_text(draw, (right, origin[1] - 8), "Re", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (origin[0] + 9, top), "Im", fill=MUTED, font_obj=SMALL)
    circle(draw, origin, 3.6, INK)

    result_progress = interval(seconds, RESULT_START, RESULT_END)
    chain_fade = 1.0 - 0.58 * result_progress
    for index in range(completed):
        start = MAP_PHASOR(CUMULATIVE[index])
        finish = MAP_PHASOR(CUMULATIVE[index + 1])
        candidate = CANDIDATES[index]
        color = rgba(GREEN, 0.90 * chain_fade) if candidate.near_stationary else rgba(BLUE, 0.74 * chain_fade)
        draw_arrow(draw, start, finish, color, width=3, head=5.5)

    if active is not None:
        arrow_progress = interval(active_fraction, 0.43, 1.0)
        if arrow_progress > 0:
            start_raw = CUMULATIVE[active]
            dx, dy = VECTORS[active]
            current_raw = (start_raw[0] + arrow_progress * dx, start_raw[1] + arrow_progress * dy)
            draw_arrow(draw, MAP_PHASOR(start_raw), MAP_PHASOR(current_raw), GOLD, width=5, head=7.0)

    current_point = CUMULATIVE[completed]
    if active is not None and active_fraction > 0.43:
        arrow_progress = interval(active_fraction, 0.43, 1.0)
        dx, dy = VECTORS[active]
        current_point = (
            CUMULATIVE[active][0] + arrow_progress * dx,
            CUMULATIVE[active][1] + arrow_progress * dy,
        )
    if completed or active is not None:
        current_tip = MAP_PHASOR(current_point)
        dashed_line(draw, origin, current_tip, rgba(GOLD, 0.26), width=2, dash=6, gap=6)
        circle(draw, current_tip, 3.8, GOLD)

    if FAR_END <= seconds < NEAR_START:
        far_tip = MAP_PHASOR(FAR_SUBTOTAL)
        draw_arrow(draw, origin, far_tip, BLUE, width=6, head=8.0)
        draw_text(draw, (980, 493), "42 contributions", fill=BLUE, font_obj=LABEL_BOLD)
        draw_text(draw, (980, 519), "almost cancel", fill=BLUE, font_obj=LABEL_BOLD)

    if result_progress > 0:
        result_raw = (TOTAL[0] * result_progress, TOTAL[1] * result_progress)
        draw_arrow(draw, origin, MAP_PHASOR(result_raw), GOLD, width=8, head=11.0)
        draw_text(draw, (973, 493), "total amplitude at B", fill=GOLD, font_obj=LABEL_BOLD)
        draw_text(draw, (973, 520), "49 paths added", fill=GOLD, font_obj=LABEL_BOLD)
        draw_text(draw, (973, 548), "phase reference chosen so the resultant points right", fill=MUTED, font_obj=SMALL)


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    completed, active, active_fraction = animation_state(seconds)
    final_hold = seconds >= RESULT_END
    subtitle, subtitle_color = subtitle_for(seconds)

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 27), "Every path contributes to the amplitude at B", font_obj=TITLE)
    draw_text(draw, (42, 65), subtitle, fill=subtitle_color, font_obj=SUBTITLE)

    draw_upper_panel(draw, completed, active, active_fraction, final_hold)
    draw_lower_panel(draw, seconds, completed, active, active_fraction, final_hold)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet() -> Path:
    samples = (
        (0.9, "49 possible paths"),
        (3.8, "one path, one arrow"),
        (FAR_END - 0.6, "phase winding"),
        (FAR_END + 0.5, "42 nearly cancel"),
        (NEAR_END - 0.5, "near paths reinforce"),
        (17.2, "total amplitude"),
    )
    thumb_w, thumb_h = 384, 216
    label_h = 25
    margin = 15
    sheet = Image.new("RGB", (3 * thumb_w + 4 * margin, 2 * (thumb_h + label_h) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(samples):
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col, row = index % 3, index // 3
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 4, y + thumb_h + 3), label, fill=MUTED)
    output = OUTPUT_DIR / f"{NAME}-contact-sheet.png"
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{NAME}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{NAME}.mp4"
    final_still = OUTPUT_DIR / f"{NAME}-final.png"
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
        contact = make_contact_sheet()
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
    far_magnitude = abs(sum(complex(math.cos(phase), math.sin(phase)) for phase in PHASES[:42]))
    near_magnitude = abs(sum(complex(math.cos(phase), math.sin(phase)) for phase in PHASES[42:]))
    print(f"far subtotal: {far_magnitude:.6f} / 42")
    print(f"near subtotal: {near_magnitude:.6f} / 7")
    print(f"total: {abs(raw_total()):.6f} / 49")


if __name__ == "__main__":
    main()
