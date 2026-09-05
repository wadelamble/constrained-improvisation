from __future__ import annotations

import math
import random
import shutil
import subprocess
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

import generate_symmetry_step2_packet_summary_point as base


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"
FFMPEG = base.FFMPEG
FFPROBE = base.FFPROBE

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24

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
RED = base.RED

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


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(v) for v in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def dashed_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill,
    width: int = 2,
    dash: float = 9,
    gap: float = 7,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    distance = 0.0
    while distance < length:
        stop = min(distance + dash, length)
        q0 = distance / length
        q1 = stop / length
        draw.line(
            (
                s(start[0] + q0 * dx),
                s(start[1] + q0 * dy),
                s(start[0] + q1 * dx),
                s(start[1] + q1 * dy),
            ),
            fill=fill,
            width=s(width),
        )
        distance += dash + gap


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill,
    width: int = 4,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=fill, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 10.0
    left = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    right = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=fill,
    )


def circle(draw: ImageDraw.ImageDraw, point: tuple[float, float], radius: float, fill, outline=None, width=2) -> None:
    x, y = point
    draw.ellipse(
        (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
        fill=fill,
        outline=outline,
        width=s(width),
    )


def forward_arc(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    fill,
    width: int = 2,
) -> None:
    x, y = center
    draw.arc(
        (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
        start=-82,
        end=82,
        fill=fill,
        width=s(width),
    )


def full_arc(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    fill,
    width: int = 2,
) -> None:
    x, y = center
    draw.ellipse(
        (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
        outline=fill,
        width=s(width),
    )


def composite_clipped(
    image: Image.Image,
    layer: Image.Image,
    bounds: tuple[float, float, float, float],
) -> None:
    box = tuple(s(v) for v in bounds)
    image.alpha_composite(layer.crop(box), dest=(box[0], box[1]))


def encode(name: str, duration: float, draw_frame: Callable[[int], Image.Image], samples: tuple[float, ...]) -> tuple[Path, Path, Path]:
    frames = round(duration * FPS)
    scratch = OUT / f"_{name}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    video = OUT / f"{name}.mp4"
    final_still = OUT / f"{name}-final.png"
    contact = OUT / f"{name}-contact-sheet.png"
    try:
        for index in range(frames):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        draw_frame(frames - 1).save(final_still)
        result = subprocess.run(
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
        if result.returncode != 0 or not video.exists() or video.stat().st_size == 0:
            raise RuntimeError(f"ffmpeg failed for {name}")

        thumb_w, thumb_h = 384, 216
        margin = 15
        sheet = Image.new("RGB", (3 * thumb_w + 4 * margin, 2 * thumb_h + 3 * margin), BG)
        for idx, seconds in enumerate(samples[:6]):
            frame = min(frames - 1, round(seconds * FPS))
            thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            col, row = idx % 3, idx // 3
            x = margin + col * (thumb_w + margin)
            y = margin + row * (thumb_h + margin)
            sheet.paste(thumb, (x, y))
        sheet.save(contact)
        return video, contact, final_still
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def verify(path: Path) -> str:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "stream=codec_name,pix_fmt,width,height,r_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# 2. Two apertures make two simultaneous contributions.

TWO_NAME = "symmetry-wave-paths-2-two-slits-two-contributions"
TWO_DURATION = 10.0


def draw_two_slits(frame: int) -> Image.Image:
    seconds = min(TWO_DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 30), "Two slits isolate two contributions to the field at B", font_obj=TITLE)
    draw_text(
        draw,
        (42, 71),
        "Both contributions exist at once. The broken lines label terms in the wave calculation—not parcel tracks.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 112, 895, 635))
    panel(draw, (920, 112, 1245, 635))

    A = (130.0, 365.0)
    C = (505.0, 275.0)
    D = (505.0, 455.0)
    B = (835.0, 365.0)
    barrier_x = 505.0

    # Wave marks live inside the physical panel; large circles must not wash over
    # the title or neighboring phasor panel.
    wave_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    wave_draw = ImageDraw.Draw(wave_layer, "RGBA")

    # Incoming wave reaches both apertures.
    incoming = interval(seconds, 0.5, 3.2)
    max_r = math.hypot(C[0] - A[0], C[1] - A[1])
    for offset in (0.0, 48.0, 96.0):
        radius = max(0.0, incoming * max_r - offset)
        if radius > 12:
            full_arc(wave_draw, A, radius, rgba(BLUE, 0.38), 2)

    # Secondary wavelets propagate from both openings.
    outgoing = interval(seconds, 3.2, 7.0)
    max_out = math.hypot(B[0] - C[0], B[1] - C[1])
    for source, color in ((C, BLUE), (D, GOLD)):
        for offset in (0.0, 42.0, 84.0):
            radius = max(0.0, outgoing * max_out - offset)
            if radius > 10:
                forward_arc(wave_draw, source, radius, rgba(color, 0.48), 3)
    composite_clipped(image, wave_layer, (38, 115, 892, 632))

    # Barrier, with two openings.
    for y0, y1 in ((155, 251), (299, 431), (479, 575)):
        draw.line((s(barrier_x), s(y0), s(barrier_x), s(y1)), fill=INK, width=s(8))
    circle(draw, A, 8, INK)
    circle(draw, C, 7, BLUE)
    circle(draw, D, 7, GOLD)
    circle(draw, B, 9, INK)
    draw_text(draw, (A[0] - 3, A[1] + 29), "A", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (C[0] + 15, C[1] - 9), "C", fill=BLUE, font_obj=LABEL_BOLD)
    draw_text(draw, (D[0] + 15, D[1] - 9), "D", fill=GOLD, font_obj=LABEL_BOLD)
    draw_text(draw, (B[0] + 2, B[1] + 29), "B", font_obj=LABEL_BOLD, anchor="ma")

    guides = interval(seconds, 6.0, 7.6)
    if guides > 0:
        dashed_line(draw, A, C, rgba(BLUE, 0.55 * guides), 2)
        dashed_line(draw, C, B, rgba(BLUE, 0.55 * guides), 2)
        dashed_line(draw, A, D, rgba(GOLD, 0.70 * guides), 2)
        dashed_line(draw, D, B, rgba(GOLD, 0.70 * guides), 2)
        draw_text(draw, (340, 169), "A → C → B", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (680, 557), "A → D → B", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")

    # Phasors show that the two endpoint fields add.
    draw_text(draw, (1082, 137), "At B", font_obj=PANE_TITLE, anchor="ma")
    draw_text(draw, (1082, 171), "add complex amplitudes", fill=MUTED, font_obj=SMALL, anchor="ma")
    phase = interval(seconds, 6.6, 8.4)
    origin = (1000.0, 420.0)
    # B lies on the symmetry axis, so the two equal-length routes arrive with
    # equal phase and magnitude. The second arrow therefore continues in the
    # same direction as the first.
    v1 = (78.0, -42.0)
    v2 = (78.0, -42.0)
    if phase > 0:
        end1 = (origin[0] + phase * v1[0], origin[1] + phase * v1[1])
        draw_arrow(draw, origin, end1, BLUE, 5)
        draw_text(draw, (1018, 339), "through C", fill=BLUE, font_obj=SMALL)
    if phase > 0.48:
        q = smoothstep((phase - 0.48) / 0.52)
        start2 = (origin[0] + v1[0], origin[1] + v1[1])
        end2 = (start2[0] + q * v2[0], start2[1] + q * v2[1])
        draw_arrow(draw, start2, end2, GOLD, 5)
        draw_text(draw, (1142, 327), "through D", fill=GOLD, font_obj=SMALL)
    if seconds >= 8.4:
        result = (origin[0] + v1[0] + v2[0], origin[1] + v1[1] + v2[1])
        draw_arrow(draw, origin, result, GREEN, 7)
        draw_text(draw, (1082, 514), "equal routes arrive in phase and add", fill=GREEN, font_obj=LABEL_BOLD, anchor="ma")
        draw_text(draw, (1082, 554), "ψ(B) = ψC(B) + ψD(B)", fill=INK, font_obj=LABEL_BOLD, anchor="ma")

    draw.rounded_rectangle(
        (s(168), s(580), s(762), s(626)),
        radius=s(10),
        fill=rgba(PANEL, 0.92),
    )
    draw_text(draw, (465, 603), "No opening is chosen; both outgoing waves contribute and interfere.", fill=GREEN, font_obj=FINAL, anchor="mm")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


# ---------------------------------------------------------------------------
# 3. Two slits become an imaginary Huygens slice.

HUYGENS_NAME = "symmetry-wave-paths-3-slits-to-huygens-slice"
HUYGENS_DURATION = 11.0


def opening_positions(count: int) -> list[float]:
    if count == 2:
        return [285.0, 455.0]
    return [205.0 + i * 330.0 / (count - 1) for i in range(count)]


def draw_slits_to_slice(frame: int) -> Image.Image:
    seconds = min(HUYGENS_DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 30), "From two slits to every point on an intermediate slice", font_obj=TITLE)
    draw_text(
        draw,
        (42, 71),
        "The slit screen teaches how to separate contributions. The final dashed slice is imaginary—there is no screen.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 112, 1245, 635))

    A = (120.0, 365.0)
    B = (1155.0, 365.0)
    sx = 610.0
    if seconds < 3.1:
        count = 2
        title = "two physical openings → two isolated contributions"
        barrier_alpha = 1.0
        imaginary = 0.0
    elif seconds < 6.0:
        count = 5 if seconds < 4.3 else (9 if seconds < 5.2 else 15)
        title = "more openings → more separately identifiable contributions"
        barrier_alpha = 1.0
        imaginary = 0.0
    else:
        count = 21
        title = "conceptual switch: every point ξ on an imaginary slice Σ contributes"
        imaginary = interval(seconds, 6.0, 7.2)
        barrier_alpha = 1.0 - imaginary

    draw_text(draw, (640, 139), title, fill=GREEN if imaginary > 0.6 else INK, font_obj=PANE_TITLE, anchor="ma")
    ys = opening_positions(count)

    # A train of fronts emitted by A. A point on the intermediate line begins
    # its outgoing front only after the corresponding incident front arrives,
    # so the outgoing phase includes the A-to-xi distance.
    wave_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    wave_draw = ImageDraw.Draw(wave_layer, "RGBA")
    wave_speed = 185.0
    wavelength = 62.0
    travel = wave_speed * seconds
    incident_radii: list[float] = []
    for ring in range(36):
        r = travel - ring * wavelength
        if 12.0 < r < 700.0:
            incident_radii.append(r)
            full_arc(wave_draw, A, r, rgba(BLUE, 0.18), 2)

    for index, y in enumerate(ys):
        point_color = GREEN if imaginary > 0.5 else (BLUE if index % 2 == 0 else GOLD)
        incident_distance = math.hypot(sx - A[0], y - A[1])
        for incident_radius in incident_radii:
            outgoing_radius = incident_radius - incident_distance
            if 8.0 < outgoing_radius < 610.0:
                forward_arc(
                    wave_draw,
                    (sx, y),
                    outgoing_radius,
                    rgba(point_color, 0.11 if count > 9 else 0.25),
                    2,
                )
    composite_clipped(image, wave_layer, (38, 115, 1242, 632))

    # Physical screen as solid segments, then fade it out.
    if barrier_alpha > 0.01:
        half_gap = 8.0 if count > 5 else 17.0
        edges = [160.0] + [v for y in ys for v in (y - half_gap, y + half_gap)] + [570.0]
        segments = list(zip(edges[0::2], edges[1::2]))
        for y0, y1 in segments:
            draw.line((s(sx), s(y0), s(sx), s(y1)), fill=rgba(INK, barrier_alpha), width=s(7))

    if imaginary > 0:
        dashed_line(draw, (sx, 166), (sx, 566), rgba(GREEN, imaginary), width=3, dash=10, gap=8)
        draw_text(draw, (sx + 14, 174), "Σ", fill=GREEN, font_obj=LABEL_BOLD)

    for index, y in enumerate(ys):
        active = 0.85 if imaginary > 0.5 else 1.0
        point_color = GREEN if imaginary > 0.5 else (BLUE if index % 2 == 0 else GOLD)
        circle(draw, (sx, y), 4.5, rgba(point_color, active))

    circle(draw, A, 8, INK)
    circle(draw, B, 9, INK)
    draw_text(draw, (A[0], A[1] + 29), "A", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (B[0], B[1] + 29), "B", font_obj=LABEL_BOLD, anchor="ma")

    # Highlight one arbitrary intermediate point as one contribution label.
    highlight_index = int((seconds * 0.7) % len(ys))
    hy = ys[highlight_index]
    if seconds >= 7.2:
        dashed_line(draw, A, (sx, hy), rgba(GOLD, 0.65), 3)
        dashed_line(draw, (sx, hy), B, rgba(GOLD, 0.65), 3)
        circle(draw, (sx, hy), 8, GOLD)
        draw_text(draw, (640, 585), "One selected ξ labels one A → ξ → B contribution; every other ξ contributes too.", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (640, 585), "Increasing the number of openings increases the number of wave contributions.", fill=MUTED, font_obj=SMALL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


# ---------------------------------------------------------------------------
# 4. Repeated imaginary slices create path labels.

PATHS_NAME = "symmetry-wave-paths-4-repeated-slices-create-paths"
PATHS_DURATION = 12.0


def deterministic_chains(slice_count: int, count: int) -> list[list[float]]:
    rng = random.Random(20260901 + slice_count)
    levels = [225.0, 270.0, 315.0, 365.0, 415.0, 460.0, 505.0]
    chains: list[list[float]] = []
    for _ in range(count):
        values = [rng.choice(levels) for _ in range(slice_count)]
        chains.append(values)
    return chains


def draw_repeated_slices(frame: int) -> Image.Image:
    seconds = min(PATHS_DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 30), "Repeating the imaginary slice turns intermediate points into path labels", font_obj=TITLE)
    draw_text(
        draw,
        (42, 71),
        "One ordered choice of points gives one product term. The completed terms are then added.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 112, 895, 635))
    panel(draw, (920, 112, 1245, 635))

    if seconds < 3.5:
        slice_count = 1
        stage = "one slice: every A → C₁ → B contribution"
    elif seconds < 7.0:
        slice_count = 3
        stage = "three slices: choose one point on each slice"
    else:
        slice_count = 5
        stage = "more slices: polygonal terms approach continuous path labels"

    left, right = 115.0, 840.0
    A = (left, 365.0)
    B = (right, 365.0)
    xs = [left + (j + 1) * (right - left) / (slice_count + 1) for j in range(slice_count)]
    levels = [225.0, 270.0, 315.0, 365.0, 415.0, 460.0, 505.0]
    draw_text(draw, (465, 139), stage, font_obj=PANE_TITLE, anchor="ma")

    for j, x in enumerate(xs, start=1):
        dashed_line(draw, (x, 180), (x, 550), rgba(GREEN, 0.50), 2, dash=8, gap=7)
        draw_text(draw, (x, 169), f"Σ{j}", fill=GREEN, font_obj=SMALL, anchor="ma")
        for y in levels:
            circle(draw, (x, y), 4, rgba(GREEN, 0.60))

    # A representative sample of the continuum, never claimed to be exhaustive.
    sample_count = 7 if slice_count == 1 else (24 if slice_count == 3 else 38)
    chains = deterministic_chains(slice_count, sample_count)
    for chain in chains:
        points = [A] + list(zip(xs, chain)) + [B]
        draw.line(tuple(s(v) for point in points for v in point), fill=rgba(BLUE, 0.12), width=s(2), joint="curve")

    # Cycle the highlighted tuple so the bookkeeping meaning is unmistakable.
    selected_index = int(max(0.0, seconds - 1.0) * 0.8) % len(chains)
    selected = chains[selected_index]
    selected_points = [A] + list(zip(xs, selected)) + [B]
    draw.line(tuple(s(v) for point in selected_points for v in point), fill=GOLD, width=s(6), joint="curve")
    for j, point in enumerate(selected_points[1:-1], start=1):
        circle(draw, point, 8, GOLD)
        draw_text(draw, (point[0] + 10, point[1] - 17), f"C{j}", fill=GOLD, font_obj=SMALL)
    circle(draw, A, 9, INK)
    circle(draw, B, 9, INK)
    draw_text(draw, (A[0], A[1] + 29), "A", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (B[0], B[1] + 29), "B", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (465, 594), "gold line = one selected chain of factors, not the track of a parcel", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")

    # Right-hand bookkeeping panel.
    draw_text(draw, (1082, 139), "One selected chain", font_obj=PANE_TITLE, anchor="ma")
    tuple_text = "(C₁)" if slice_count == 1 else ("(C₁, C₂, C₃)" if slice_count == 3 else "(C₁, C₂, C₃, C₄, C₅)")
    draw_text(draw, (1082, 184), tuple_text, fill=GOLD, font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (1082, 235), "multiply along the chain", fill=MUTED, font_obj=SMALL, anchor="ma")
    if slice_count == 1:
        factors = ["K(B,C₁)", "× K(C₁,A)"]
    elif slice_count == 3:
        factors = ["K(B,C₃) × K(C₃,C₂)", "× K(C₂,C₁) × K(C₁,A)"]
    else:
        factors = ["K(B,C₅) × ···", "··· × K(C₂,C₁) × K(C₁,A)"]
    for idx, text_value in enumerate(factors):
        draw_text(draw, (1082, 280 + idx * 40), text_value, fill=INK, font_obj=LABEL_BOLD, anchor="ma")
    draw.line((s(955), s(392), s(1210), s(392)), fill=FAINT, width=s(2))
    draw_text(draw, (1082, 424), "The full wave at B", font_obj=PANE_TITLE, anchor="ma")
    draw_text(draw, (1082, 468), "add every completed chain", fill=MUTED, font_obj=SMALL, anchor="ma")
    draw_text(draw, (1082, 517), "ψ(B) = Σ  Aγ", fill=GREEN, font_obj=FINAL, anchor="ma")
    draw_text(draw, (1082, 555), "continuum of path labels", fill=GREEN, font_obj=SMALL, anchor="ma")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


# ---------------------------------------------------------------------------
# 5. One selected chain produces one whole-path phasor.

ONE_PHASOR_NAME = "symmetry-wave-paths-5-one-path-one-phasor"
ONE_PHASOR_DURATION = 11.0


def draw_one_path_one_phasor(frame: int) -> Image.Image:
    seconds = min(ONE_PHASOR_DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 30), "One selected chain produces one whole-path complex contribution", font_obj=TITLE)
    draw_text(
        draw,
        (42, 71),
        "Segment transfer factors multiply; their phase changes accumulate into the angle of one final phasor.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 112, 825, 635))
    panel(draw, (850, 112, 1245, 635))

    points = [
        (95.0, 430.0),
        (225.0, 365.0),
        (355.0, 455.0),
        (490.0, 320.0),
        (625.0, 390.0),
        (785.0, 270.0),
    ]
    for index, x in enumerate((225.0, 355.0, 490.0, 625.0), start=1):
        dashed_line(draw, (x, 178), (x, 535), rgba(GREEN, 0.42), 2, dash=8, gap=7)
        draw_text(draw, (x, 166), f"Σ{index}", fill=GREEN, font_obj=SMALL, anchor="ma")

    draw.line(tuple(s(v) for point in points for v in point), fill=rgba(GOLD, 0.34), width=s(5), joint="curve")
    segment_phases = (0.32, 0.43, 0.27, 0.51, 0.39)
    segment_scales = (0.98, 0.96, 0.97, 0.95, 0.98)
    phase_start = 0.18
    segment_progress = max(0.0, min(len(segment_phases), (seconds - 1.0) / 1.45))
    completed = min(len(segment_phases), int(math.floor(segment_progress)))
    fraction = 0.0 if completed >= len(segment_phases) else segment_progress - completed

    for index, (p0, p1) in enumerate(zip(points[:-1], points[1:])):
        if index < completed:
            draw.line((s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])), fill=GOLD, width=s(8))
        elif index == completed and fraction > 0:
            q = (p0[0] + fraction * (p1[0] - p0[0]), p0[1] + fraction * (p1[1] - p0[1]))
            draw.line((s(p0[0]), s(p0[1]), s(q[0]), s(q[1])), fill=GOLD, width=s(8))
        midpoint = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 18)
        draw_text(draw, midpoint, f"δφ{index + 1}", fill=GOLD if index <= completed else MUTED, font_obj=SMALL, anchor="mm")

    for idx, point in enumerate(points):
        circle(draw, point, 8 if idx not in (0, len(points) - 1) else 9, GOLD if idx not in (0, len(points) - 1) else INK)
    draw_text(draw, (points[0][0], points[0][1] + 29), "A", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (points[-1][0], points[-1][1] + 29), "B", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (430, 587), "one ordered chain of intermediate points—not a parcel track", fill=GOLD, font_obj=LABEL_BOLD, anchor="mm")

    # Accumulate the phase and magnitude of the successive complex factors.
    angle = phase_start + sum(segment_phases[:completed])
    length = 112.0
    for scale_factor in segment_scales[:completed]:
        length *= scale_factor
    if completed < len(segment_phases):
        angle += fraction * segment_phases[completed]
        length *= segment_scales[completed] ** fraction

    origin = (1048.0, 359.0)
    circle(draw, origin, 112, None, rgba(MUTED, 0.35), 2)
    draw.line((s(origin[0] - 130), s(origin[1]), s(origin[0] + 130), s(origin[1])), fill=rgba(MUTED, 0.30), width=s(1))
    draw.line((s(origin[0]), s(origin[1] - 130), s(origin[0]), s(origin[1] + 130)), fill=rgba(MUTED, 0.30), width=s(1))
    circle(draw, origin, 3.5, INK)
    draw_text(draw, (1048, 139), "phase accumulator for this chain", font_obj=PANE_TITLE, anchor="ma")

    cumulative = phase_start
    cumulative_length = 112.0
    for idx in range(completed):
        cumulative += segment_phases[idx]
        cumulative_length *= segment_scales[idx]
        dashed_line(draw, origin, map_phasor(origin, cumulative, cumulative_length), rgba(MUTED, 0.28), 2, dash=6, gap=5)
    draw_arrow(draw, origin, map_phasor(origin, angle, length), GOLD, 7)
    draw_text(draw, (1048, 508), "angle = accumulated phase", fill=GOLD, font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (1048, 539), "length = amplitude magnitude", fill=MUTED, font_obj=SMALL, anchor="ma")

    if completed >= len(segment_phases):
        draw_text(draw, (1048, 579), "Aγ = aγ exp(i Φγ)", fill=GREEN, font_obj=FINAL, anchor="ma")
        draw_text(draw, (1048, 608), "Φγ = φA + Σj δφj", fill=GREEN, font_obj=LABEL_BOLD, anchor="ma")
    else:
        draw_text(draw, (1048, 589), f"multiply segment {completed + 1}", fill=MUTED, font_obj=SMALL, anchor="ma")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


# ---------------------------------------------------------------------------
# 6. Completed path contributions interfere into a ray.

RAY_NAME = "symmetry-wave-paths-6-path-phases-form-ray"
RAY_DURATION = 11.0


def curve_points(amplitude: float, skew: float = 0.0) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for idx in range(101):
        u = idx / 100
        x = 95.0 + 715.0 * u
        y = 365.0 + amplitude * math.sin(math.pi * u) + skew * math.sin(2 * math.pi * u)
        points.append((x, y))
    return points


def polyline_length(points: list[tuple[float, float]]) -> float:
    return sum(
        math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        for p0, p1 in zip(points[:-1], points[1:])
    )


def map_phasor(origin: tuple[float, float], angle: float, length: float) -> tuple[float, float]:
    return origin[0] + length * math.cos(angle), origin[1] - length * math.sin(angle)


def draw_paths_to_ray(frame: int) -> Image.Image:
    seconds = min(RAY_DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 30), "A ray emerges from the stationary family of path contributions", font_obj=TITLE)
    draw_text(
        draw,
        (42, 71),
        "Each arrow at right is one complete path contribution—not one segment, one mode, or one material parcel.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )
    panel(draw, (35, 112, 845, 635))
    panel(draw, (870, 112, 1245, 635))
    A, B = (95.0, 365.0), (810.0, 365.0)

    amplitudes = [-190, -145, -105, -70, -42, -22, -10, 0, 10, 22, 42, 70, 105, 145, 190]
    reveal = interval(seconds, 0.8, 4.0)
    shown = max(1, int(round(reveal * len(amplitudes))))
    center_order = sorted(range(len(amplitudes)), key=lambda i: abs(amplitudes[i]))
    visible = center_order[:shown]
    for index in visible:
        amp = amplitudes[index]
        near = abs(amp) <= 42
        color = rgba(GREEN if near else BLUE, 0.34 if near else 0.19)
        pts = curve_points(float(amp), skew=0.11 * amp)
        draw.line(tuple(s(v) for point in pts for v in point), fill=color, width=s(3), joint="curve")

    circle(draw, A, 9, INK)
    circle(draw, B, 9, INK)
    draw_text(draw, (A[0], A[1] + 29), "A", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (B[0], B[1] + 29), "B", font_obj=LABEL_BOLD, anchor="ma")
    draw_text(draw, (440, 139), "candidate path labels between the same endpoints", font_obj=PANE_TITLE, anchor="ma")

    # The phasor angles come from the actual lengths of the drawn curves:
    # Delta phi = k(L_gamma - L_star).  The chosen k makes the far sample wind
    # nearly closed while the stationary neighborhood stays aligned.
    far_origin = (1025.0, 300.0)
    near_origin = (930.0, 505.0)
    draw_text(draw, (1055, 139), "whole-path phasors added tip to tail", font_obj=PANE_TITLE, anchor="ma")
    draw_text(draw, (900, 202), "far candidates", fill=BLUE, font_obj=LABEL_BOLD)
    draw_text(draw, (900, 409), "stationary neighborhood", fill=GREEN, font_obj=LABEL_BOLD)
    draw_text(draw, (1058, 230), "angle = k(Lγ − L★)", fill=MUTED, font_obj=SMALL, anchor="ma")

    reference_length = polyline_length(curve_points(0.0))
    visual_k = 2.0 * math.pi / 66.0

    def path_phase(amplitude: float) -> float:
        length = polyline_length(curve_points(amplitude, skew=0.11 * amplitude))
        return visual_k * (length - reference_length)

    far_amplitudes = (-190, -145, -105, -70, 70, 105, 145, 190)
    near_amplitudes = (-42, -22, -10, 0, 10, 22, 42)
    far_angles = [path_phase(value) for value in far_amplitudes]
    near_angles = [path_phase(value) for value in near_amplitudes]
    phasor_reveal = interval(seconds, 3.6, 7.7)
    far_count = int(round(phasor_reveal * len(far_angles)))
    near_count = int(round(phasor_reveal * len(near_angles)))

    def draw_tip_to_tail(origin, angles, count, color, width, step_length):
        current = origin
        for angle in angles[:count]:
            finish = map_phasor(current, angle, step_length)
            draw_arrow(draw, current, finish, rgba(color, 0.76), width)
            current = finish
        return current

    far_end = draw_tip_to_tail(far_origin, far_angles, far_count, BLUE, 3, 55.0)
    near_end = draw_tip_to_tail(near_origin, near_angles, near_count, GREEN, 4, 38.0)
    circle(draw, far_origin, 3.5, INK)
    circle(draw, near_origin, 3.5, INK)

    if seconds >= 7.7:
        draw_arrow(draw, far_origin, far_end, rgba(BLUE, 0.90), 6)
        draw_text(draw, (1155, 318), "1.5% of aligned maximum", fill=BLUE, font_obj=SMALL, anchor="mm")
        draw_arrow(draw, near_origin, near_end, GREEN, 8)
        draw_text(draw, (1118, 554), "97% of aligned maximum", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
        straight = curve_points(0.0)
        draw.line(tuple(s(v) for point in straight for v in point), fill=GOLD, width=s(9), joint="curve")
        draw_arrow(draw, (620, 365), (760, 365), GOLD, 5)
        draw_text(draw, (440, 590), "the stationary curve is the geometrical-optics ray", fill=GOLD, font_obj=FINAL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = (
        (TWO_NAME, TWO_DURATION, draw_two_slits, (0.8, 2.8, 4.8, 6.9, 8.3, 9.7)),
        (HUYGENS_NAME, HUYGENS_DURATION, draw_slits_to_slice, (0.8, 2.5, 4.0, 5.6, 7.4, 10.2)),
        (PATHS_NAME, PATHS_DURATION, draw_repeated_slices, (0.8, 2.8, 4.2, 6.5, 8.1, 11.2)),
        (ONE_PHASOR_NAME, ONE_PHASOR_DURATION, draw_one_path_one_phasor, (0.7, 2.4, 4.0, 5.7, 7.4, 10.2)),
        (RAY_NAME, RAY_DURATION, draw_paths_to_ray, (0.7, 2.3, 4.2, 6.2, 8.1, 10.4)),
    )
    for name, duration, draw_frame, samples in jobs:
        video, contact, final_still = encode(name, duration, draw_frame, samples)
        print(video)
        print(contact)
        print(final_still)
        print(verify(video))


if __name__ == "__main__":
    main()
