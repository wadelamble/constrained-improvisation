from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from animation_math import paste_math
import generate_symmetry_step2_packet_summary_point as base


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = base.FFMPEG
FFPROBE = base.FFPROBE

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
DURATION = 15.0
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GRID = base.GRID
BLUE = base.BLUE
LIGHT_BLUE = base.LIGHT_BLUE
GREEN = base.GREEN
GOLD = base.GOLD
RED = base.RED
PURPLE = (117, 85, 145)
LIGHT_GOLD = (238, 216, 170)
LIGHT_GREEN = (181, 210, 193)
LIGHT_RED = (236, 204, 197)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

MODE_ANGLES = (0.25, 1.15, 2.45, -0.55, -1.45, 0.60)
MODE_WEIGHTS = (1.00, 0.82, 0.66, 0.88, 0.62, 0.72)
MODE_COUNT = len(MODE_ANGLES)
ARROW_STAGE_START = 2.0
ARROW_STAGE_SECONDS = 1.20
ARROW_STAGE_END = ARROW_STAGE_START + MODE_COUNT * ARROW_STAGE_SECONDS

# Native video controls can cover the bottom of the frame. All essential copy
# ends inside the panels by y=608; y>=624 is deliberately left blank.
ESSENTIAL_CONTENT_BOTTOM = 608
CONTROLS_SAFE_TOP = 624


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


def draw_math(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    expression: str,
    *,
    fill=INK,
    size: int = 16,
    anchor: str = "mm",
    opacity: float = 1.0,
) -> None:
    paste_math(
        draw._image,
        xy,
        expression,
        size=size,
        scale=SCALE,
        color=fill[:3],
        anchor=anchor,
        opacity=opacity,
    )


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(value) for value in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def arrow_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    finish: tuple[float, float],
    color,
    width: int = 4,
    head: float = 9.0,
) -> None:
    draw.line(
        (s(start[0]), s(start[1]), s(finish[0]), s(finish[1])),
        fill=color,
        width=s(width),
    )
    angle = math.atan2(finish[1] - start[1], finish[0] - start[0])
    p1 = (
        finish[0] - head * math.cos(angle - math.pi / 6),
        finish[1] - head * math.sin(angle - math.pi / 6),
    )
    p2 = (
        finish[0] - head * math.cos(angle + math.pi / 6),
        finish[1] - head * math.sin(angle + math.pi / 6),
    )
    draw.polygon(
        [(s(finish[0]), s(finish[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))],
        fill=color,
    )


def mode_vectors() -> list[tuple[float, float]]:
    return [
        (weight * math.cos(angle), weight * math.sin(angle))
        for weight, angle in zip(MODE_WEIGHTS, MODE_ANGLES)
    ]


MODE_VECTORS = mode_vectors()


def cumulative_vectors() -> list[tuple[float, float]]:
    points = [(0.0, 0.0)]
    for dx, dy in MODE_VECTORS:
        x_value, y_value = points[-1]
        points.append((x_value + dx, y_value + dy))
    return points


CUMULATIVE = cumulative_vectors()


def map_phasor(point: tuple[float, float]) -> tuple[float, float]:
    origin_x, origin_y, phasor_scale = 755.0, 474.0, 135.0
    return origin_x + phasor_scale * point[0], origin_y - phasor_scale * point[1]


def stage_state(seconds: float) -> tuple[int | None, float, int]:
    if seconds < ARROW_STAGE_START:
        return None, 0.0, 0
    scaled = (seconds - ARROW_STAGE_START) / ARROW_STAGE_SECONDS
    completed = min(MODE_COUNT, max(0, int(math.floor(scaled))))
    if completed >= MODE_COUNT:
        return None, 0.0, MODE_COUNT
    return completed, smoothstep(scaled - completed), completed


def draw_fixed_segment(draw: ImageDraw.ImageDraw) -> None:
    left, top, right, bottom = 76.0, 184.0, 620.0, 349.0
    for index in range(1, 5):
        px = left + (right - left) * index / 5
        py = top + (bottom - top) * index / 5
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.70), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.70), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.68), width=s(2))
    draw_text(draw, (right, bottom + 19), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 8, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    start = (160.0, 319.0)
    corner = (522.0, 319.0)
    finish = (522.0, 218.0)
    draw.line(
        (s(start[0]), s(start[1]), s(finish[0]), s(finish[1])),
        fill=BLUE,
        width=s(5),
    )
    arrow_segment(draw, start, corner, GOLD, width=4, head=8)
    arrow_segment(draw, corner, finish, PURPLE, width=4, head=8)
    for point in (start, finish):
        draw.ellipse(
            (s(point[0] - 6), s(point[1] - 6), s(point[0] + 6), s(point[1] + 6)),
            fill=INK,
        )
    draw_math(draw, (start[0] - 10, start[1] + 14), r"(x_j,s_j)", fill=INK, size=13, anchor="rm")
    draw_math(draw, (finish[0] + 10, finish[1] - 8), r"(x_{j+1},s_{j+1})", fill=INK, size=13, anchor="lm")
    draw_math(draw, ((start[0] + corner[0]) / 2, corner[1] + 22), r"\Delta x_j", fill=GOLD, size=14)
    draw_math(draw, (corner[0] + 14, (corner[1] + finish[1]) / 2), r"\Delta s_j", fill=PURPLE, size=14, anchor="lm")

    draw.rounded_rectangle(
        (s(257), s(188), s(450), s(220)),
        radius=s(7),
        fill=rgba(LIGHT_GREEN, 0.48),
        outline=rgba(GREEN, 0.62),
        width=s(1),
    )
    draw_text(draw, (353, 204), "FIXED SEGMENT j", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")


def mode_card_bounds(index: int) -> tuple[float, float, float, float]:
    col = index % 2
    row = index // 2
    x0 = 57.0 + col * 294.0
    y0 = 399.0 + row * 58.0
    return x0, y0, x0 + 276.0, y0 + 46.0


def draw_mode_cards(
    draw: ImageDraw.ImageDraw,
    active_index: int | None,
    active_progress: float,
    completed: int,
    final_hold: bool,
) -> None:
    draw_text(draw, (58, 374), "same geometry; six alternative Fourier modes", fill=MUTED, font_obj=SMALL)
    for index in range(MODE_COUNT):
        x0, y0, x1, y1 = mode_card_bounds(index)
        is_active = active_index == index
        is_completed = index < completed or final_hold
        if is_active:
            fill = rgba(LIGHT_GOLD, 0.58)
            outline = GOLD
            label_color = GOLD
            width = 2
        elif is_completed:
            fill = rgba(LIGHT_BLUE, 0.16)
            outline = rgba(BLUE, 0.62)
            label_color = BLUE
            width = 1
        else:
            fill = rgba(BG, 0.30)
            outline = rgba(FAINT, 0.90)
            label_color = MUTED
            width = 1
        draw.rounded_rectangle(
            (s(x0), s(y0), s(x1), s(y1)),
            radius=s(7),
            fill=fill,
            outline=outline,
            width=s(width),
        )
        dot_radius = 4.5 + (1.5 * active_progress if is_active else 0.0)
        draw.ellipse(
            (
                s(x0 + 18 - dot_radius),
                s((y0 + y1) / 2 - dot_radius),
                s(x0 + 18 + dot_radius),
                s((y0 + y1) / 2 + dot_radius),
            ),
            fill=label_color,
        )
        draw_math(draw, (x0 + 41, (y0 + y1) / 2), rf"k_{index}", fill=label_color, size=14, anchor="lm")
        draw_math(
            draw,
            (x1 - 10, (y0 + y1) / 2),
            rf"z_{{j,{index}}}=w_{index}e^{{i\Delta\phi_j(k_{index})}}",
            fill=label_color,
            size=13,
            anchor="rm",
        )


def draw_left_panel(
    draw: ImageDraw.ImageDraw,
    active_index: int | None,
    active_progress: float,
    completed: int,
    final_hold: bool,
) -> None:
    panel(draw, (35, 108, 655, 612))
    draw_text(draw, (58, 129), "hold one x-s segment fixed", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "Changing k changes the complex contribution—not the segment.", fill=MUTED, font_obj=SMALL)
    draw_fixed_segment(draw)
    draw_mode_cards(draw, active_index, active_progress, completed, final_hold)

    draw.rounded_rectangle(
        (s(57), s(574), s(633), s(607)),
        radius=s(7),
        fill=rgba(LIGHT_GREEN, 0.30),
    )
    draw_math(
        draw,
        (345, 590),
        r"\Delta\phi_j(k_n)=k_n\Delta x_j-\omega(k_n)\Delta s_j",
        fill=GREEN,
        size=15,
    )


def draw_complex_axes(draw: ImageDraw.ImageDraw) -> None:
    origin = map_phasor((0.0, 0.0))
    draw.line((s(716), s(origin[1]), s(1210), s(origin[1])), fill=rgba(MUTED, 0.28), width=s(1))
    draw.line((s(origin[0]), s(244), s(origin[0]), s(559)), fill=rgba(MUTED, 0.28), width=s(1))
    draw.ellipse(
        (s(origin[0] - 4), s(origin[1] - 4), s(origin[0] + 4), s(origin[1] + 4)),
        fill=INK,
    )
    draw_text(draw, (1207, origin[1] + 16), "Re", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (origin[0] - 9, 247), "Im", fill=MUTED, font_obj=SMALL, anchor="rs")


def draw_phasor_sum(
    draw: ImageDraw.ImageDraw,
    active_index: int | None,
    active_progress: float,
    completed: int,
    resultant_progress: float,
    final_hold: bool,
) -> None:
    draw_complex_axes(draw)

    for index in range(completed):
        start = map_phasor(CUMULATIVE[index])
        finish = map_phasor(CUMULATIVE[index + 1])
        arrow_segment(draw, start, finish, rgba(BLUE, 0.78), width=4)
        midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        draw_math(draw, (midpoint[0] + 5, midpoint[1] - 10), rf"z_{{j,{index}}}", fill=BLUE, size=12)

    if active_index is not None and active_progress > 0.0:
        start_vec = CUMULATIVE[active_index]
        dx, dy = MODE_VECTORS[active_index]
        current_vec = (start_vec[0] + active_progress * dx, start_vec[1] + active_progress * dy)
        start = map_phasor(start_vec)
        finish = map_phasor(current_vec)
        arrow_segment(draw, start, finish, GOLD, width=6, head=10)
        midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        draw_math(draw, (midpoint[0] + 6, midpoint[1] - 11), rf"z_{{j,{active_index}}}", fill=GOLD, size=13)

    if completed >= MODE_COUNT and resultant_progress > 0.0:
        origin = map_phasor((0.0, 0.0))
        total = map_phasor(
            (CUMULATIVE[-1][0] * resultant_progress, CUMULATIVE[-1][1] * resultant_progress)
        )
        arrow_segment(draw, origin, total, GREEN, width=7, head=12)
        if resultant_progress > 0.82:
            draw_math(draw, (total[0] + 14, total[1] - 5), r"K_j^{(N)}", fill=GREEN, size=17, anchor="lm")
            draw_text(draw, (963, 557), "green resultant: origin to final tip", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    elif active_index is not None:
        draw_text(
            draw,
            (963, 557),
            f"add zⱼ,{active_index} at the previous arrow's tip",
            fill=GOLD,
            font_obj=LABEL_BOLD,
            anchor="mm",
        )
    elif not final_hold:
        draw_text(draw, (963, 557), "the phasor sum has not begun", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_equation_strip(
    draw: ImageDraw.ImageDraw,
    discrete_alpha: float,
    continuum_alpha: float,
    final_hold: bool,
) -> None:
    draw_math(
        draw,
        (963, 198),
        r"z_{j,n}=w_ne^{i\Delta\phi_j(k_n)}",
        fill=INK,
        size=16,
    )

    if discrete_alpha > 0.0:
        draw.rounded_rectangle(
            (s(708), s(573), s(1227), s(608)),
            radius=s(7),
            fill=rgba(LIGHT_GREEN, 0.28 * discrete_alpha),
        )
        draw_math(
            draw,
            (967, 590),
            r"K_j^{(N)}=\sum_n z_{j,n}=\sum_n w_ne^{i\Delta\phi_j(k_n)}",
            fill=GREEN,
            size=15,
            opacity=discrete_alpha,
        )

    if continuum_alpha > 0.0:
        draw.rounded_rectangle(
            (s(708), s(216), s(1227), s(252)),
            radius=s(7),
            fill=rgba(LIGHT_BLUE, 0.15 * continuum_alpha),
        )
        draw_math(
            draw,
            (967, 234),
            r"K_j=\int\!\frac{dk}{2\pi}\,e^{i[k\Delta x_j-\omega(k)\Delta s_j]}",
            fill=BLUE,
            size=15,
            opacity=continuum_alpha,
        )

    if final_hold:
        draw.rounded_rectangle(
            (s(706), s(516), s(1229), s(548)),
            radius=s(7),
            fill=rgba(LIGHT_RED, 0.42),
        )
        draw_text(draw, (732, 532), "NOT", fill=RED, font_obj=LABEL_BOLD, anchor="lm")
        draw_math(
            draw,
            (800, 532),
            r"\Delta\phi_j(k_0)+\Delta\phi_j(k_1)+\cdots",
            fill=RED,
            size=14,
            anchor="lm",
        )
        draw_text(draw, (1207, 532), "phases are not summed across modes", fill=RED, font_obj=SMALL, anchor="ra")


def draw_right_panel(
    draw: ImageDraw.ImageDraw,
    active_index: int | None,
    active_progress: float,
    completed: int,
    resultant_progress: float,
    discrete_alpha: float,
    continuum_alpha: float,
    final_hold: bool,
) -> None:
    panel(draw, (680, 108, 1245, 612))
    draw_text(draw, (703, 129), "add the mode contributions tip to tail", font_obj=PANE_TITLE)
    draw_text(draw, (703, 158), "Each arrow is a complex number; its direction is that mode's phase.", fill=MUTED, font_obj=SMALL)
    draw_equation_strip(draw, discrete_alpha, continuum_alpha, final_hold)
    draw_phasor_sum(draw, active_index, active_progress, completed, resultant_progress, final_hold)


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    active_index, active_progress, completed = stage_state(seconds)
    resultant_progress = interval(seconds, 9.45, 10.55)
    discrete_alpha = interval(seconds, 9.95, 10.85)
    continuum_alpha = interval(seconds, 11.15, 12.15)
    final_hold = seconds >= 12.55

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 8.5 — Sum the modes to form one segment kernel", font_obj=TITLE)
    if final_hold:
        subtitle = "Across modes, add complex phasors: their resultant—not summed phase angles—is the segment kernel Kⱼ."
        subtitle_color = GREEN
    else:
        subtitle = "For fixed segment j, linearity adds weighted complex contributions from the alternative Fourier modes."
        subtitle_color = MUTED
    draw_text(draw, (42, 72), subtitle, fill=subtitle_color, font_obj=SUBTITLE)

    draw_left_panel(draw, active_index, active_progress, completed, final_hold)
    draw_right_panel(
        draw,
        active_index,
        active_progress,
        completed,
        resultant_progress,
        discrete_alpha,
        continuum_alpha,
        final_hold,
    )

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 3.0, 6.2, 10.4, 13.7)
    labels = (
        "one fixed segment",
        "add the first modes",
        "phasors join tip to tail",
        "resultant is K_j",
        "discrete sum to continuum",
    )
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
    report = result.stdout.strip()
    if "codec_name=h264" not in report or "pix_fmt=yuv420p" not in report:
        raise RuntimeError(f"unexpected video encoding:\n{report}")
    return report


def verify_footer_clearance() -> None:
    if ESSENTIAL_CONTENT_BOTTOM >= CONTROLS_SAFE_TOP:
        raise RuntimeError(
            f"essential content extends to y={ESSENTIAL_CONTENT_BOTTOM}, "
            f"inside control-safe area beginning at y={CONTROLS_SAFE_TOP}"
        )


def render() -> tuple[Path, Path, Path]:
    name = "symmetry-step8-5-modes-form-segment-kernel"
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
        verify_footer_clearance()
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
    print(
        f"essential_content_bottom={ESSENTIAL_CONTENT_BOTTOM}; "
        f"controls_safe_top={CONTROLS_SAFE_TOP}"
    )


if __name__ == "__main__":
    main()
