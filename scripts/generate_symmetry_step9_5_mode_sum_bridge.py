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
DURATION = 16.5
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

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL

N_SEGMENTS = 6
PLOT = (100.0, 190.0, 742.0, 520.0)
INTRO_END = 1.6
STAGE_DURATION = 2.65
FINAL_START = INTRO_END + 4 * STAGE_DURATION

K_ASSIGNMENTS = (
    (1.25, 1.35, 1.15, 1.30, 1.40, 1.20),
    (2.40, 2.60, 2.30, 2.70, 2.50, 2.40),
    (3.00, 3.40, 3.20, 3.60, 3.30, 3.10),
    (3.80, 4.20, 4.00, 4.30, 4.10, 3.90),
)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


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


def x_of_u(u: float) -> float:
    return 0.16 + 0.72 * u + 0.14 * math.sin(math.pi * u)


def omega(k_value: float) -> float:
    return 0.18 + 0.34 * k_value * k_value


def map_path_point(u: float) -> tuple[float, float]:
    left, top, right, bottom = PLOT
    px = left + x_of_u(u) / 1.12 * (right - left)
    py = bottom - u * (bottom - top)
    return px, py


def path_points(samples: int = 360) -> list[tuple[int, int]]:
    return [tuple(s(value) for value in map_path_point(index / (samples - 1))) for index in range(samples)]


def assignment_phase(assignment: tuple[float, ...]) -> float:
    total = 0.0
    for segment, k_value in enumerate(assignment):
        u0 = segment / N_SEGMENTS
        u1 = (segment + 1) / N_SEGMENTS
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
    left, top, right, bottom = 827.0, 270.0, 1214.0, 500.0
    possible = list(CUMULATIVE) + [(0.0, 0.0)] + list(VECTORS)
    xs = [point[0] for point in possible]
    ys = [point[1] for point in possible]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    scale = min((right - left - 54) / span_x, (bottom - top - 46) / span_y)
    offset_x = (left + right) / 2 - scale * (min_x + max_x) / 2
    offset_y = (top + bottom) / 2 + scale * (min_y + max_y) / 2

    def mapper(point: tuple[float, float]) -> tuple[float, float]:
        return offset_x + scale * point[0], offset_y - scale * point[1]

    return mapper, (left, top, right, bottom)


MAP_PHASOR, PHASOR_BOX = make_phasor_mapper()


def stage_state(seconds: float) -> tuple[int | None, float, int, bool]:
    if seconds < INTRO_END:
        return None, 0.0, 0, False
    if seconds >= FINAL_START:
        return None, 1.0, len(K_ASSIGNMENTS), True
    position = (seconds - INTRO_END) / STAGE_DURATION
    index = min(len(K_ASSIGNMENTS) - 1, int(math.floor(position)))
    local = position - index
    return index, local, index, False


def badge(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    text: str,
    *,
    fill,
    outline,
    text_color,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=SMALL)
    width = (bbox[2] - bbox[0]) / SCALE + 12
    height = (bbox[3] - bbox[1]) / SCALE + 8
    cx, cy = center
    draw.rounded_rectangle(
        (s(cx - width / 2), s(cy - height / 2), s(cx + width / 2), s(cy + height / 2)),
        radius=s(5),
        fill=fill,
        outline=outline,
        width=s(1),
    )
    draw_text(draw, center, text, fill=text_color, font_obj=SMALL, anchor="mm")


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    left, top, right, bottom = PLOT
    for index in range(1, 5):
        px = left + (right - left) * index / 5
        py = top + (bottom - top) * index / 5
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.70), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.70), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw_text(draw, (right + 1, bottom + 22), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 10, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")


def draw_fixed_candidate(
    draw: ImageDraw.ImageDraw,
    assignment_index: int | None,
    local: float,
    final_hold: bool,
) -> None:
    panel(draw, (35, 108, 770, 625))
    draw_text(draw, (58, 129), "one complete candidate in the x-s plane", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "same Step 9 curve; only its selected segment modes are replaced", fill=MUTED, font_obj=SMALL)
    draw_axes(draw)
    draw.line(path_points(), fill=BLUE, width=s(5), joint="curve")

    for segment in range(N_SEGMENTS + 1):
        point = map_path_point(segment / N_SEGMENTS)
        draw.ellipse(
            (s(point[0] - 5), s(point[1] - 5), s(point[0] + 5), s(point[1] + 5)),
            fill=INK if segment in (0, N_SEGMENTS) else rgba(MUTED, 0.78),
        )

    start = map_path_point(0.0)
    finish = map_path_point(1.0)
    draw_text(draw, (start[0] - 12, start[1] + 15), "A", font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 12, finish[1] - 10), "B", font_obj=LABEL_BOLD)

    if assignment_index is None and not final_hold:
        draw_text(draw, (421, 564), "first fix the spatial curve", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        return

    shown_index = len(K_ASSIGNMENTS) - 1 if final_hold else assignment_index
    assert shown_index is not None
    assignment = K_ASSIGNMENTS[shown_index]
    reveal_count = N_SEGMENTS if final_hold else max(0, min(N_SEGMENTS, int(math.ceil(clamp01(local / 0.24) * N_SEGMENTS))))

    label_offsets = ((13, 17), (13, 17), (14, 14), (13, -17), (-45, -18), (-47, -18))
    for segment, k_value in enumerate(assignment):
        u0 = segment / N_SEGMENTS
        u1 = (segment + 1) / N_SEGMENTS
        midpoint = map_path_point((u0 + u1) / 2)
        draw_text(draw, (midpoint[0] - 4, midpoint[1] + 2), f"j={segment}", fill=MUTED, font_obj=SMALL, anchor="mm")
        if segment >= reveal_count:
            continue
        dx, dy = label_offsets[segment]
        badge(
            draw,
            (midpoint[0] + dx, midpoint[1] + dy),
            f"k{segment}={k_value:.2f}",
            fill=rgba(BG, 0.96),
            outline=GREEN if final_hold else GOLD,
            text_color=GREEN if final_hold else GOLD,
        )

    if final_hold:
        draw_text(draw, (421, 564), "the spatial curve never moved", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(
            draw,
            (421, 564),
            f"assignment r={shown_index}: one kⱼ value on every segment j",
            fill=GOLD,
            font_obj=LABEL_BOLD,
            anchor="mm",
        )


def lerp_point(start: tuple[float, float], finish: tuple[float, float], amount: float) -> tuple[float, float]:
    return start[0] + amount * (finish[0] - start[0]), start[1] + amount * (finish[1] - start[1])


def draw_phasor_panel(
    draw: ImageDraw.ImageDraw,
    assignment_index: int | None,
    local: float,
    completed: int,
    final_hold: bool,
) -> None:
    panel(draw, (795, 108, 1245, 625))
    draw_text(draw, (817, 129), "add mode assignments tip to tail", font_obj=PANE_TITLE)
    draw_text(draw, (817, 158), "same Step 10 sum, but the spatial curve is still fixed", fill=MUTED, font_obj=SMALL)

    if final_hold:
        draw_text(draw, (1020, 198), "all mode assignments summed for this one curve", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    elif assignment_index is None:
        draw_text(draw, (1020, 198), "no mode assignment has contributed yet", fill=MUTED, font_obj=LABEL_BOLD, anchor="mm")
    elif local < 0.42:
        draw_text(draw, (1020, 198), f"finish choosing all six kⱼ values for r={assignment_index}", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")
    elif local < 0.70:
        draw_text(draw, (1020, 198), f"the complete assignment r={assignment_index} produces one arrow", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (1020, 198), "move that same arrow into the running sum", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")

    left, top, right, bottom = PHASOR_BOX
    origin = MAP_PHASOR((0.0, 0.0))
    draw.line((s(left), s(origin[1]), s(right), s(origin[1])), fill=rgba(MUTED, 0.23), width=s(1))
    draw.line((s(origin[0]), s(top), s(origin[0]), s(bottom)), fill=rgba(MUTED, 0.23), width=s(1))
    draw.ellipse((s(origin[0] - 4), s(origin[1] - 4), s(origin[0] + 4), s(origin[1] + 4)), fill=INK)

    for index in range(completed):
        start = MAP_PHASOR(CUMULATIVE[index])
        finish = MAP_PHASOR(CUMULATIVE[index + 1])
        draw_arrow(draw, start, finish, rgba(BLUE, 0.82), width=4)
        midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        draw_text(draw, (midpoint[0] + 5, midpoint[1] - 8), f"r={index}", fill=BLUE, font_obj=SMALL)

    if assignment_index is not None and local >= 0.42:
        vector = VECTORS[assignment_index]
        growth = smoothstep(clamp01((local - 0.42) / 0.23))
        slide = smoothstep(clamp01((local - 0.70) / 0.23))
        cumulative_start = CUMULATIVE[assignment_index]
        display_start_raw = lerp_point((0.0, 0.0), cumulative_start, slide)
        display_finish_raw = (
            display_start_raw[0] + growth * vector[0],
            display_start_raw[1] + growth * vector[1],
        )
        if slide > 0.02 and assignment_index > 0:
            ghost_finish = MAP_PHASOR((vector[0], vector[1]))
            draw_arrow(draw, origin, ghost_finish, rgba(GOLD, 0.20), width=3)
        draw_arrow(draw, MAP_PHASOR(display_start_raw), MAP_PHASOR(display_finish_raw), GOLD, width=6)

    if final_hold:
        total = MAP_PHASOR(CUMULATIVE[-1])
        draw_arrow(draw, origin, total, GREEN, width=7)
        draw_text(draw, (1020, 545), "green arrow = A[x] for this fixed spatial candidate", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    elif assignment_index is not None and local >= 0.42:
        draw_text(draw, (1020, 545), "one whole relabeling—not one segment—gives one arrow", fill=GOLD, font_obj=SMALL, anchor="mm")
    else:
        draw_text(draw, (1020, 545), "completed assignments remain as blue arrows", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    assignment_index, local, completed, final_hold = stage_state(seconds)

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 9.5 — Keep the path fixed; sum its mode assignments", font_obj=TITLE)

    if final_hold:
        subtitle = "After every k(s) assignment is added, this one spatial path has one amplitude A[x]."
        subtitle_color = GREEN
    elif assignment_index is None:
        subtitle = "Begin with the same single spatial candidate constructed in Step 9."
        subtitle_color = MUTED
    elif local < 0.42:
        subtitle = "Change only the selected mode on each segment; the spatial curve does not move."
        subtitle_color = MUTED
    elif local < 0.70:
        subtitle = "Read the six segment choices together: one complete assignment gives one complex arrow."
        subtitle_color = MUTED
    else:
        subtitle = "Add that arrow to the previous assignments, just as candidate terms are added in Step 10."
        subtitle_color = MUTED
    draw_text(draw, (42, 72), subtitle, fill=subtitle_color, font_obj=SUBTITLE)

    draw_fixed_candidate(draw, assignment_index, local, final_hold)
    draw_phasor_panel(draw, assignment_index, local, completed, final_hold)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 2.4, 3.0, 5.6, 13.5)
    labels = ("fixed Step 9 curve", "one complete assignment", "one origin arrow", "same arrow joins sum", "one amplitude A[x]")
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
    name = "symmetry-step9-5-mode-sum-bridge"
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
