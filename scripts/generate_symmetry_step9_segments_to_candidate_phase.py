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
LIGHT_GREEN = (181, 210, 193)
LIGHT_GOLD = (238, 216, 170)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

PLOT = (100.0, 190.0, 742.0, 548.0)
N_SEGMENTS = 6


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


def x_of_u(u: float) -> float:
    return 0.16 + 0.72 * u + 0.14 * math.sin(math.pi * u)


def k_of_u(u: float) -> float:
    return 3.4 + 0.65 * math.sin(2 * math.pi * u + 0.30)


def omega(k: float) -> float:
    return 0.75 + 0.05 * k * k


def map_point(u: float) -> tuple[float, float]:
    left, top, right, bottom = PLOT
    x = x_of_u(u)
    px = left + x / 1.12 * (right - left)
    py = bottom - u * (bottom - top)
    return px, py


def segment_data() -> list[dict[str, float]]:
    data: list[dict[str, float]] = []
    for index in range(N_SEGMENTS):
        u0 = index / N_SEGMENTS
        u1 = (index + 1) / N_SEGMENTS
        um = (u0 + u1) / 2
        k = k_of_u(um)
        dx = x_of_u(u1) - x_of_u(u0)
        ds = u1 - u0
        dphi = k * dx - omega(k) * ds
        data.append({"u0": u0, "u1": u1, "k": k, "dx": dx, "ds": ds, "dphi": dphi})
    return data


SEGMENTS = segment_data()
TOTAL_PHASE = sum(item["dphi"] for item in SEGMENTS)


def phase_at(progress: float) -> float:
    scaled = progress * N_SEGMENTS
    complete = min(N_SEGMENTS, int(math.floor(scaled)))
    fraction = min(1.0, max(0.0, scaled - complete))
    total = sum(SEGMENTS[index]["dphi"] for index in range(complete))
    if complete < N_SEGMENTS:
        total += SEGMENTS[complete]["dphi"] * fraction
    return total


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    left, top, right, bottom = PLOT
    for index in range(1, 5):
        px = left + (right - left) * index / 5
        py = top + (bottom - top) * index / 5
        draw.line((s(px), s(top), s(px), s(bottom)), fill=rgba(GRID, 0.72), width=s(1))
        draw.line((s(left), s(py), s(right), s(py)), fill=rgba(GRID, 0.72), width=s(1))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.72), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.72), width=s(2))
    draw_text(draw, (right + 1, bottom + 22), "x", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 10, top), "s", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")


def smooth_path_points(samples: int = 360) -> list[tuple[int, int]]:
    return [tuple(s(v) for v in map_point(index / (samples - 1))) for index in range(samples)]


def draw_candidate_panel(draw: ImageDraw.ImageDraw, progress: float, refine: float) -> None:
    panel(draw, (35, 108, 770, 643))
    draw_text(draw, (58, 129), "one complete candidate in the x-s plane", font_obj=PANE_TITLE)
    draw_text(draw, (58, 158), "candidate = x-s curve + one selected Fourier mode on each segment", fill=MUTED, font_obj=SMALL)
    draw_axes(draw)

    smooth_alpha = 0.24 + 0.62 * refine
    draw.line(smooth_path_points(), fill=rgba(BLUE, smooth_alpha), width=s(3 if refine < 0.7 else 5), joint="curve")

    scaled = progress * N_SEGMENTS
    for index, item in enumerate(SEGMENTS):
        start = map_point(item["u0"])
        finish = map_point(item["u1"])
        if index + 1 <= scaled:
            color = GREEN
            width = 6
        elif index < scaled < index + 1:
            fraction = scaled - index
            current = (
                start[0] + (finish[0] - start[0]) * fraction,
                start[1] + (finish[1] - start[1]) * fraction,
            )
            draw.line((s(start[0]), s(start[1]), s(current[0]), s(current[1])), fill=GOLD, width=s(7))
            draw.line((s(current[0]), s(current[1]), s(finish[0]), s(finish[1])), fill=rgba(MUTED, 0.34), width=s(3))
            color = None
            width = 0
        else:
            color = rgba(MUTED, 0.34)
            width = 3
        if color is not None:
            draw.line((s(start[0]), s(start[1]), s(finish[0]), s(finish[1])), fill=color, width=s(width))

        midpoint = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
        if refine < 0.55:
            draw_math(draw, (midpoint[0] + 8, midpoint[1] - 10), rf"k_{{n_{index}}}", fill=MUTED, size=12)

    for index in range(N_SEGMENTS + 1):
        p = map_point(index / N_SEGMENTS)
        draw.ellipse((s(p[0] - 5), s(p[1] - 5), s(p[0] + 5), s(p[1] + 5)), fill=INK if index in (0, N_SEGMENTS) else rgba(MUTED, 0.75))

    if progress < 1.0:
        segment_index = min(N_SEGMENTS - 1, int(math.floor(scaled)))
        fraction = scaled - segment_index
        start = map_point(SEGMENTS[segment_index]["u0"])
        finish = map_point(SEGMENTS[segment_index]["u1"])
        current = (
            start[0] + (finish[0] - start[0]) * fraction,
            start[1] + (finish[1] - start[1]) * fraction,
        )
        draw.ellipse((s(current[0] - 9), s(current[1] - 9), s(current[0] + 9), s(current[1] + 9)), fill=GOLD)

    start = map_point(0.0)
    finish = map_point(1.0)
    draw_text(draw, (start[0] - 12, start[1] + 15), "A", fill=INK, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 12, finish[1] - 10), "B", fill=INK, font_obj=LABEL_BOLD)

    if refine > 0:
        count = max(N_SEGMENTS + 1, round(N_SEGMENTS + 22 * refine))
        for index in range(1, count - 1):
            p = map_point(index / (count - 1))
            draw.ellipse((s(p[0] - 2.2), s(p[1] - 2.2), s(p[0] + 2.2), s(p[1] + 2.2)), fill=BLUE)
        draw_text(draw, (405, 593), "refine the bookkeeping; the candidate curve stays the same", fill=BLUE, font_obj=SMALL, anchor="mm")
    else:
        draw_text(draw, (405, 593), "along one candidate: multiply successive phase factors", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_phase_dial(draw: ImageDraw.ImageDraw, center: tuple[float, float], radius: float, angle: float) -> None:
    cx, cy = center
    draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=rgba(MUTED, 0.62), width=s(2))
    draw.line((s(cx - radius - 7), s(cy), s(cx + radius + 7), s(cy)), fill=rgba(MUTED, 0.25), width=s(1))
    draw.line((s(cx), s(cy - radius - 7), s(cx), s(cy + radius + 7)), fill=rgba(MUTED, 0.25), width=s(1))
    hand = radius * 0.78
    draw.line((s(cx), s(cy), s(cx + hand), s(cy)), fill=rgba(MUTED, 0.40), width=s(3))
    end = (cx + hand * math.cos(angle), cy - hand * math.sin(angle))
    draw.line((s(cx), s(cy), s(end[0]), s(end[1])), fill=GREEN, width=s(5))
    direction = math.atan2(end[1] - cy, end[0] - cx)
    size = 10.0
    p1 = (end[0] - size * math.cos(direction - math.pi / 6), end[1] - size * math.sin(direction - math.pi / 6))
    p2 = (end[0] - size * math.cos(direction + math.pi / 6), end[1] - size * math.sin(direction + math.pi / 6))
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=GREEN)
    draw.ellipse((s(cx - 4), s(cy - 4), s(cx + 4), s(cy + 4)), fill=INK)


def draw_factor_boxes(draw: ImageDraw.ImageDraw, progress: float) -> None:
    left = 819.0
    top = 216.0
    width = 61.0
    gap = 7.0
    scaled = progress * N_SEGMENTS
    for index in range(N_SEGMENTS):
        x0 = left + index * (width + gap)
        complete = scaled >= index + 1
        active = index < scaled < index + 1
        fill = rgba(LIGHT_GREEN, 0.62) if complete else rgba(LIGHT_GOLD, 0.62) if active else rgba(FAINT, 0.34)
        outline = GREEN if complete else GOLD if active else rgba(MUTED, 0.34)
        draw.rounded_rectangle((s(x0), s(top), s(x0 + width), s(top + 52)), radius=s(7), fill=fill, outline=outline, width=s(2))
        draw_math(
            draw,
            (x0 + width / 2, top + 26),
            rf"e^{{i\Delta\phi_{index}}}",
            fill=INK if complete or active else MUTED,
            size=11,
        )


def draw_ledger_panel(draw: ImageDraw.ImageDraw, progress: float, refine: float) -> None:
    panel(draw, (795, 108, 1245, 643))
    draw_text(draw, (817, 129), "phase ledger for one mode-labeled candidate", font_obj=PANE_TITLE)
    draw_math(draw, (817, 158), r"\mathrm{segment}\ j\ \mathrm{uses\ selected\ mode}\ k_{n_j}", fill=MUTED, size=13, anchor="lm")

    draw_factor_boxes(draw, progress)
    draw_math(draw, (1020, 293), r"\prod_j e^{i\Delta\phi_{j,n_j}}=e^{i\sum_j\Delta\phi_{j,n_j}}", fill=INK, size=16)

    draw_phase_dial(draw, (1020.0, 418.0), 76.0, phase_at(progress))
    if progress >= 0.98:
        draw_text(draw, (1020, 502), "one mode-labeled candidate gives", fill=GREEN, font_obj=SMALL, anchor="mm")
        draw_math(draw, (1020, 527), r"e^{i\Phi[x,k]}", fill=GREEN, size=18)
    else:
        current_index = min(N_SEGMENTS - 1, int(math.floor(progress * N_SEGMENTS)))
        draw_text(draw, (1020, 514), f"current accumulated angle after segment {current_index}", fill=MUTED, font_obj=SMALL, anchor="mm")

    if refine > 0:
        draw_math(
            draw,
            (1020, 561),
            r"\Phi_N[x,k]=\sum_j\!\left[k_{n_j}\Delta x_j-\omega(k_{n_j})\Delta s_j\right]",
            fill=INK,
            size=13,
        )
        draw_math(draw, (1020, 601), r"\longrightarrow\ \int_\gamma\!\left(k\,dx-\omega(k)\,ds\right)", fill=GREEN, size=18)
    else:
        draw_math(
            draw,
            (1020, 574),
            r"\Delta\phi_{j,n_j}=k_{n_j}\Delta x_j-\omega(k_{n_j})\Delta s_j",
            fill=MUTED,
            size=15,
        )


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    progress = interval(seconds, 1.2, 7.7)
    refine = interval(seconds, 8.2, 10.4)
    final_hold = seconds >= 10.5

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 9 — Multiply one selected mode factor from each segment", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "A mode is selected on each segment; successive factors multiply, so their angles add.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    draw_candidate_panel(draw, progress, refine)
    draw_ledger_panel(draw, progress, refine)

    if final_hold:
        footer = "Different mode selections and different candidate curves are summed only afterward."
        draw_text(draw, (640, 681), footer, fill=GREEN, font_obj=FINAL, anchor="mm")
    elif refine > 0:
        footer = "As the segments become finer, the phase sum becomes a line integral."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")
    else:
        footer = "The phase dial retains every earlier turn and adds the current segment's turn."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.8, 3.2, 5.8, 8.0, 11.4)
    labels = ("one segmented candidate", "factors accumulate", "carry the phase dial", "all segments", "sum becomes integral")
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
    name = "symmetry-step9-segments-to-candidate-phase"
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
