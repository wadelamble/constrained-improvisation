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
DURATION = 13.0
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GRID = base.GRID
GREEN = base.GREEN
GOLD = base.GOLD
PURPLE = (117, 85, 145)
LIGHT_GOLD = (238, 216, 170)
LIGHT_PURPLE = (218, 205, 228)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL


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
        tuple(s(v) for v in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def arrow_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 4,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 10.0
    p1 = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    p2 = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=color)


def partial_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    progress: float,
    color,
    width: int = 5,
) -> tuple[float, float]:
    current = (
        start[0] + (end[0] - start[0]) * progress,
        start[1] + (end[1] - start[1]) * progress,
    )
    if progress > 0.01:
        arrow_segment(draw, start, current, color, width=width)
    return current


def draw_phase_dial(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    horizontal_progress: float,
    vertical_progress: float,
) -> None:
    cx, cy = center
    draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=rgba(MUTED, 0.62), width=s(2))
    draw.line((s(cx - radius - 8), s(cy), s(cx + radius + 8), s(cy)), fill=rgba(MUTED, 0.26), width=s(1))
    draw.line((s(cx), s(cy - radius - 8), s(cx), s(cy + radius + 8)), fill=rgba(MUTED, 0.26), width=s(1))

    hand = radius * 0.78
    initial = (cx + hand, cy)
    draw.line((s(cx), s(cy), s(initial[0]), s(initial[1])), fill=rgba(MUTED, 0.45), width=s(3))

    phi_x = 1.35 * horizontal_progress
    after_x = (cx + hand * math.cos(phi_x), cy - hand * math.sin(phi_x))
    if horizontal_progress > 0:
        draw.line((s(cx), s(cy), s(after_x[0]), s(after_x[1])), fill=rgba(GOLD, 0.52), width=s(3))

    phi_total = phi_x - 0.82 * vertical_progress
    current = (cx + hand * math.cos(phi_total), cy - hand * math.sin(phi_total))
    arrow_segment(draw, (cx, cy), current, GREEN if vertical_progress > 0 else GOLD, width=5)
    draw.ellipse((s(cx - 4), s(cy - 4), s(cx + 4), s(cy + 4)), fill=INK)

    if horizontal_progress >= 0.98:
        draw_math(draw, (after_x[0] - 5, after_x[1] - 10), r"\mathrm{after}\ k_n\Delta x_j", fill=GOLD, size=13, anchor="rm")
    if vertical_progress >= 0.98:
        draw_text(draw, (current[0] + 8, current[1] - 6), "after both", fill=GREEN, font_obj=SMALL)


def draw_segment_panel(draw: ImageDraw.ImageDraw, x_progress: float, s_progress: float) -> None:
    panel(draw, (35, 108, 760, 643))
    draw_text(draw, (58, 129), "one candidate segment in the x-s plane", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "j labels the segment; n labels one Fourier mode", fill=MUTED, font_obj=SMALL)

    left, top, right, bottom = 105.0, 196.0, 710.0, 548.0
    for index in range(1, 5):
        px = left + (right - left) * index / 5
        py = top + (bottom - top) * index / 5
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.72), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.72), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.72), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.72), width=s(2))
    draw_text(draw, (right + 2, bottom + 22), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 10, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")

    start = (205.0, 474.0)
    corner = (590.0, 474.0)
    finish = (590.0, 250.0)
    draw.line((s(start[0]), s(start[1]), s(finish[0]), s(finish[1])), fill=rgba(MUTED, 0.42), width=s(3))
    draw_text(draw, (390, 338), "the candidate segment", fill=MUTED, font_obj=SMALL, anchor="mm")

    x_current = partial_arrow(draw, start, corner, x_progress, GOLD)
    if x_progress >= 0.98:
        s_current = partial_arrow(draw, corner, finish, s_progress, PURPLE)
    else:
        s_current = corner

    current = s_current if s_progress > 0 else x_current
    draw.ellipse((s(current[0] - 8), s(current[1] - 8), s(current[0] + 8), s(current[1] + 8)), fill=GREEN)

    draw.ellipse((s(start[0] - 8), s(start[1] - 8), s(start[0] + 8), s(start[1] + 8)), fill=INK)
    draw.ellipse((s(finish[0] - 8), s(finish[1] - 8), s(finish[0] + 8), s(finish[1] + 8)), fill=INK)
    draw_math(draw, (start[0] - 12, start[1] + 15), r"(x_j,s_j)", fill=INK, anchor="rm")
    draw_math(draw, (finish[0] + 12, finish[1] - 9), r"(x_{j+1},s_{j+1})", fill=INK, anchor="lm")
    draw_math(draw, ((start[0] + corner[0]) / 2, corner[1] + 26), r"\Delta x_j", fill=GOLD)
    draw_math(draw, (corner[0] + 19, (corner[1] + finish[1]) / 2), r"\Delta s_j", fill=PURPLE, anchor="lm")

    draw.rounded_rectangle((s(248), s(205), s(525), s(250)), radius=s(8), fill=rgba(LIGHT_GOLD, 0.42))
    draw_math(draw, (386, 227), r"\mathrm{selected\ contribution:\ mode}\ k_n", fill=INK, size=15)
    draw_text(draw, (405, 594), "gold and purple are phase bookkeeping, not two physical legs", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_phase_panel(draw: ImageDraw.ImageDraw, x_progress: float, s_progress: float, formula_alpha: float) -> None:
    panel(draw, (785, 108, 1245, 643))
    draw_text(draw, (807, 129), "one mode's phase across this segment", font_obj=PANE_TITLE)
    draw_math(draw, (807, 158), r"\mathrm{supplied\ relation:}\ q_n=-\omega(k_n)", fill=MUTED, size=13, anchor="lm")

    draw_math(draw, (1015, 204), r"u_{k_n}(x,s)=\exp\!\left(i[k_nx-\omega(k_n)s]\right)", fill=INK, size=16)

    draw.rounded_rectangle((s(827), s(241), s(1203), s(289)), radius=s(8), fill=rgba(LIGHT_GOLD, 0.32))
    draw_text(draw, (850, 265), "x change", fill=GOLD, font_obj=LABEL_BOLD, anchor="lm")
    draw_math(draw, (1180, 265), r"+\,k_n\Delta x_j", fill=INK, anchor="rm")

    draw.rounded_rectangle((s(827), s(301), s(1203), s(349)), radius=s(8), fill=rgba(LIGHT_PURPLE, 0.42))
    draw_text(draw, (850, 325), "s change", fill=PURPLE, font_obj=LABEL_BOLD, anchor="lm")
    draw_math(draw, (1180, 325), r"-\,\omega(k_n)\Delta s_j", fill=INK, anchor="rm")

    draw_phase_dial(draw, (1015.0, 470.0), 73.0, x_progress, s_progress)

    if formula_alpha > 0:
        draw_math(
            draw,
            (1015, 572),
            r"e^{ik_n\Delta x_j}e^{-i\omega(k_n)\Delta s_j}=e^{i\Delta\phi_{j,n}}",
            fill=INK,
            size=16,
            opacity=formula_alpha,
        )
        draw_math(
            draw,
            (1015, 607),
            r"\Delta\phi_{j,n}=k_n\Delta x_j-\omega(k_n)\Delta s_j",
            fill=GREEN,
            size=18,
            opacity=formula_alpha,
        )


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    x_progress = interval(seconds, 1.4, 4.4)
    s_progress = interval(seconds, 4.8, 7.8)
    formula_alpha = interval(seconds, 7.7, 8.7)
    final_hold = seconds >= 9.0

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 8 — Find one mode's phase across one candidate segment", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "Each Fourier mode has its own phase contribution across the same segment.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    draw_segment_panel(draw, x_progress, s_progress)
    draw_phase_panel(draw, x_progress, s_progress, formula_alpha)

    if final_hold:
        footer = "This dial shows one mode. The segment kernel adds the contributions from every mode."
        draw_text(draw, (640, 681), footer, fill=GREEN, font_obj=FINAL, anchor="mm")
    elif seconds < 4.6:
        footer = "For the selected mode, the x displacement contributes the spatial phase term."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")
    else:
        footer = "The supplied Fourier relation contributes that same mode's second-coordinate phase term."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 3.7, 5.8, 8.1, 10.7)
    labels = ("one segment", "x phase term", "s phase term", "terms combine", "one phase factor")
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
    name = "symmetry-step8-one-segment-two-phase-terms"
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
