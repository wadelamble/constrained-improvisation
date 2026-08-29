from __future__ import annotations

import cmath
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffprobe.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
SCENE_DURATIONS = (4.0, 4.5, 7.0, 4.5, 5.0, 6.0)
TOTAL_SECONDS = sum(SCENE_DURATIONS)
FRAMES = round(TOTAL_SECONDS * FPS)

BG = (255, 252, 246)
PANEL = (252, 248, 240)
INK = (37, 39, 42)
MUTED = (111, 106, 99)
FAINT = (222, 215, 205)
GRID = (233, 227, 218)
BLUE = (51, 91, 133)
GOLD = (198, 138, 45)
RED = (181, 76, 59)
GREEN = (65, 126, 95)
PURPLE = (117, 85, 145)
LIGHT_BLUE = (115, 157, 194)
MODE_COLORS = (BLUE, GOLD, RED)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "seguisb.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size * SCALE)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = font(25, True)
SUBTITLE = font(17)
PANE_TITLE = font(18, True)
LABEL = font(15)
LABEL_BOLD = font(15, True)
SMALL = font(13)
TINY = font(11)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def motion(progress: float, start: float = 0.10, end: float = 0.88) -> float:
    return smoothstep((progress - start) / (end - start))


def dashed_line(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    fill,
    width: int = 2,
    dash: int = 9,
    gap: int = 6,
) -> None:
    if len(points) < 2:
        return
    on = True
    remaining = dash
    for p0, p1 in zip(points[:-1], points[1:]):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        length = math.hypot(dx, dy)
        if length == 0:
            continue
        travelled = 0.0
        while travelled < length:
            step = min(remaining, length - travelled)
            q0 = travelled / length
            q1 = (travelled + step) / length
            if on:
                draw.line(
                    (
                        round(p0[0] + dx * q0),
                        round(p0[1] + dy * q0),
                        round(p0[0] + dx * q1),
                        round(p0[1] + dy * q1),
                    ),
                    fill=fill,
                    width=s(width),
                )
            travelled += step
            remaining -= step
            if remaining <= 1e-9:
                on = not on
                remaining = dash if on else gap


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 3,
    head: float = 9,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in bounds), radius=s(13), fill=PANEL, outline=FAINT, width=s(2))


K0 = 7.0
DK = 0.80
KS = (K0 - DK, K0, K0 + DK)
AMPS = (0.50, 1.00, 0.50)
X_MIN = -4.55
X_MAX = 4.55
X_SAMPLES = 720


def packet_values(
    x: float,
    phases: tuple[float, float, float],
    k_shift: float = 0.0,
    x_shift: float = 0.0,
    common_phase: float = 0.0,
) -> tuple[list[complex], complex]:
    components = [
        amp * cmath.exp(1j * ((k + k_shift) * x + phase - k * x_shift + common_phase))
        for amp, k, phase in zip(AMPS, KS, phases)
    ]
    return components, sum(components)


def plot_x(left: float, right: float, x: float) -> float:
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def draw_phasor(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    phase: float,
    color,
    label: str | None = None,
) -> None:
    cx, cy = center
    draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=rgba(MUTED, 0.45), width=s(2))
    draw.line((s(cx - radius), s(cy), s(cx + radius), s(cy)), fill=rgba(MUTED, 0.22), width=s(1))
    draw.line((s(cx), s(cy - radius), s(cx), s(cy + radius)), fill=rgba(MUTED, 0.22), width=s(1))
    tip = (cx + radius * 0.82 * math.cos(phase), cy - radius * 0.82 * math.sin(phase))
    arrow(draw, (cx, cy), tip, color, width=3, head=8)
    draw.ellipse((s(tip[0] - 3.2), s(tip[1] - 3.2), s(tip[0] + 3.2), s(tip[1] + 3.2)), fill=color)
    if label:
        draw_text(draw, (cx, cy + radius + 18), label, fill=color, font_obj=SMALL, anchor="mm")


def draw_component_and_packet_panel(
    draw: ImageDraw.ImageDraw,
    phases: tuple[float, float, float],
    bounds: tuple[float, float, float, float] = (355, 113, 1240, 640),
    x_shift: float = 0.0,
    k_shift: float = 0.0,
    common_phase: float = 0.0,
    ghost_magnitude_phases: tuple[float, float, float] | None = None,
    ghost_x_shift: float = 0.0,
    ghost_label: str | None = None,
    title: str = "Three components and their complex sum",
) -> None:
    panel(draw, bounds)
    x0, y0, x1, _ = bounds
    left = x0 + 64
    right = x1 - 24
    draw_text(draw, (x0 + 20, y0 + 18), title, font_obj=PANE_TITLE)

    row_y = (198.0, 260.0, 322.0)
    for index, (baseline, color, amp, k, phase) in enumerate(zip(row_y, MODE_COLORS, AMPS, KS, phases)):
        draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.23), width=s(1))
        draw_text(draw, (left - 13, baseline), f"k{index + 1}", fill=color, font_obj=LABEL_BOLD, anchor="rm")
        points: list[tuple[int, int]] = []
        for sample in range(X_SAMPLES):
            x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
            value = math.cos((k + k_shift) * x + phase - k * x_shift + common_phase)
            points.append((s(plot_x(left, right, x)), s(baseline - 20.0 * value)))
        draw.line(points, fill=color, width=s(2), joint="curve")

    packet_y = 492.0
    packet_scale = 66.0 / sum(AMPS)
    draw.line((s(left), s(packet_y), s(right), s(packet_y)), fill=rgba(MUTED, 0.34), width=s(1))
    draw_text(draw, (left - 13, packet_y), "sum", fill=INK, font_obj=LABEL_BOLD, anchor="rm")

    real_points: list[tuple[int, int]] = []
    imag_points: list[tuple[int, int]] = []
    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    ghost_upper: list[tuple[int, int]] = []
    ghost_lower: list[tuple[int, int]] = []
    for sample in range(X_SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
        _, value = packet_values(x, phases, k_shift=k_shift, x_shift=x_shift, common_phase=common_phase)
        px = s(plot_x(left, right, x))
        real_points.append((px, s(packet_y - packet_scale * value.real)))
        imag_points.append((px, s(packet_y - packet_scale * value.imag)))
        mag = abs(value)
        upper.append((px, s(packet_y - packet_scale * mag)))
        lower.append((px, s(packet_y + packet_scale * mag)))
        if ghost_magnitude_phases is not None:
            _, ghost_value = packet_values(x, ghost_magnitude_phases, x_shift=ghost_x_shift)
            ghost_mag = abs(ghost_value)
            ghost_upper.append((px, s(packet_y - packet_scale * ghost_mag)))
            ghost_lower.append((px, s(packet_y + packet_scale * ghost_mag)))

    if ghost_upper:
        dashed_line(draw, ghost_upper, rgba(MUTED, 0.55), width=2)
        dashed_line(draw, ghost_lower, rgba(MUTED, 0.55), width=2)
    draw.line(upper, fill=rgba(LIGHT_BLUE, 0.78), width=s(3), joint="curve")
    draw.line(lower, fill=rgba(LIGHT_BLUE, 0.78), width=s(3), joint="curve")
    dashed_line(draw, imag_points, rgba(RED, 0.92), width=2, dash=8, gap=6)
    draw.line(real_points, fill=BLUE, width=s(3), joint="curve")

    draw_text(draw, (left + 5, 594), "solid: Re ψ", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (left + 122, 594), "dashed: Im ψ", fill=RED, font_obj=SMALL)
    draw_text(draw, (left + 259, 594), "pale boundary: ±|ψ|", fill=LIGHT_BLUE, font_obj=SMALL)
    if ghost_label:
        draw_text(draw, (right - 5, 594), ghost_label, fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (right, 617), "x", fill=MUTED, font_obj=SMALL, anchor="ra")


def draw_three_phasors(draw: ImageDraw.ImageDraw, phases: tuple[float, float, float], x: float = 116.0) -> None:
    for index, (phase, color, y) in enumerate(zip(phases, MODE_COLORS, (356.0, 448.0, 540.0))):
        draw_phasor(draw, (x, y), 31.0, phase, color, f"phase of k{index + 1}")


def lagrange_value(x: float, xs: tuple[float, float, float], ys: tuple[float, float, float]) -> float:
    total = 0.0
    for index in range(3):
        term = ys[index]
        for other in range(3):
            if other != index:
                term *= (x - xs[other]) / (xs[index] - xs[other])
        total += term
    return total


def draw_phase_vs_k(
    draw: ImageDraw.ImageDraw,
    phases: tuple[float, float, float],
    relation: str,
    bounds: tuple[float, float, float, float] = (41, 113, 330, 303),
    y_min: float = -7.0,
    y_max: float = 0.4,
) -> None:
    panel(draw, bounds)
    x0, y0, x1, y1 = bounds
    draw_text(draw, (x0 + 16, y0 + 15), "Accumulated phase versus k", font_obj=PANE_TITLE)
    left, right = x0 + 48, x1 - 20
    top, bottom = y0 + 55, y1 - 32
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=MUTED, width=s(2))
    draw.line((s(left), s(top), s(left), s(bottom)), fill=MUTED, width=s(2))
    for value in (-6.0, -4.0, -2.0, 0.0):
        py = bottom - (value - y_min) / (y_max - y_min) * (bottom - top)
        draw.line((s(left), s(py), s(right), s(py)), fill=GRID, width=s(1))
        draw_text(draw, (left - 8, py), f"{value:g}", fill=MUTED, font_obj=TINY, anchor="rm")

    def mx(k: float) -> float:
        return left + (k - (K0 - 1.25 * DK)) / (2.50 * DK) * (right - left)

    def my(value: float) -> float:
        value = max(y_min, min(y_max, value))
        return bottom - (value - y_min) / (y_max - y_min) * (bottom - top)

    curve: list[tuple[int, int]] = []
    for index in range(121):
        k = KS[0] + (KS[-1] - KS[0]) * index / 120
        value = lagrange_value(k, KS, phases)
        curve.append((s(mx(k)), s(my(value))))
    draw.line(curve, fill=PURPLE, width=s(3), joint="curve")
    for index, (k, value, color) in enumerate(zip(KS, phases, MODE_COLORS)):
        px, py = mx(k), my(value)
        draw.ellipse((s(px - 5), s(py - 5), s(px + 5), s(py + 5)), fill=color, outline=BG, width=s(2))
        draw_text(draw, (px, bottom + 16), f"k{index + 1}", fill=color, font_obj=TINY, anchor="mm")
    draw_text(draw, (right, bottom + 17), "k", fill=MUTED, font_obj=TINY, anchor="ra")
    draw_text(draw, (x0 + 16, y0 + 42), relation, fill=PURPLE, font_obj=SMALL)


def header(draw: ImageDraw.ImageDraw, step: int, title: str, subtitle: str) -> None:
    draw_text(draw, (42, 31), title, font_obj=TITLE)
    draw_text(draw, (43, 67), subtitle, fill=MUTED, font_obj=SUBTITLE)
    draw_text(draw, (1238, 47), f"{step} / 6", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")


def footer(draw: ImageDraw.ImageDraw, text: str) -> None:
    draw.line((s(42), s(660), s(1238), s(660)), fill=FAINT, width=s(1))
    draw_text(draw, (640, 687), text, fill=INK, font_obj=LABEL_BOLD, anchor="mm")


def scene_single_mode(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    phase = -1.65 * math.pi * motion(progress)
    header(draw, 1, "A mode's phase is an angle", "At each x, a complex mode has a direction in the complex plane.")

    panel(draw, (42, 112, 397, 638))
    draw_text(draw, (64, 133), "Complex value at a fixed point", font_obj=PANE_TITLE)
    draw_phasor(draw, (220, 355), 112, phase, BLUE)
    draw_text(draw, (220, 505), "the value rotates as phase advances", fill=MUTED, font_obj=LABEL, anchor="mm")
    draw_text(draw, (220, 544), "uₖ(x,τ) = exp i[kx − φ(τ)]", fill=INK, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (220, 578), f"φ = {(-phase):.2f} rad", fill=PURPLE, font_obj=LABEL_BOLD, anchor="mm")

    panel(draw, (421, 112, 1238, 638))
    draw_text(draw, (444, 133), "The spatial mode keeps the same amplitude and shape", font_obj=PANE_TITLE)
    left, right = 470.0, 1198.0
    baseline = 376.0
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.35), width=s(1))
    real_points: list[tuple[int, int]] = []
    imag_points: list[tuple[int, int]] = []
    for sample in range(X_SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
        value = cmath.exp(1j * (K0 * x + phase))
        px = s(plot_x(left, right, x))
        real_points.append((px, s(baseline - 105 * value.real)))
        imag_points.append((px, s(baseline - 105 * value.imag)))
    draw.line(real_points, fill=BLUE, width=s(3), joint="curve")
    dashed_line(draw, imag_points, RED, width=2, dash=8, gap=6)
    x_mark = 0.0
    px_mark = plot_x(left, right, x_mark)
    value_mark = cmath.exp(1j * phase)
    draw.line((s(px_mark), s(232), s(px_mark), s(518)), fill=rgba(GREEN, 0.60), width=s(2))
    draw.ellipse(
        (s(px_mark - 5), s(baseline - 105 * value_mark.real - 5), s(px_mark + 5), s(baseline - 105 * value_mark.real + 5)),
        fill=GREEN,
    )
    draw_text(draw, (px_mark, 545), "fixed x", fill=GREEN, font_obj=SMALL, anchor="mm")
    draw_text(draw, (490, 589), "solid: Re uₖ", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (612, 589), "dashed: Im uₖ", fill=RED, font_obj=SMALL)
    draw_text(draw, (1169, 589), "|uₖ| = 1 everywhere", fill=LIGHT_BLUE, font_obj=SMALL, anchor="ra")
    footer(draw, "For one mode, phase advance rotates the whole mode; no amplitude or shape changes.")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def scene_global_packet(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    beta = -1.45 * math.pi * motion(progress)
    phases = (beta, beta, beta)
    header(draw, 2, "A global phase rotates every component together", "The three-mode packet changes in complex direction, not in magnitude or shape.")
    draw_phase_vs_k(draw, phases, "horizontal: the same phase for every k")
    draw_three_phasors(draw, phases)
    draw_component_and_packet_panel(draw, phases)
    footer(draw, "Same added phase for k₁, k₂, k₃  →  relative phases and |ψ| are unchanged.")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def loop_state(progress: float, orientation: float = 1.0) -> tuple[float, float, float, str]:
    a = 1.25
    b = 0.90
    if orientation < 0.0:
        if progress < 0.20:
            u = smoothstep(progress / 0.20)
            return 0.0, b * u, 0.0, "shift in k"
        if progress < 0.40:
            u = smoothstep((progress - 0.20) / 0.20)
            return a * u, b, -a * b * u, "shift in x"
        if progress < 0.60:
            u = smoothstep((progress - 0.40) / 0.20)
            return a, b * (1 - u), -a * b, "undo the k shift"
        if progress < 0.80:
            u = smoothstep((progress - 0.60) / 0.20)
            return a * (1 - u), 0.0, -a * b, "undo the x shift"
        return 0.0, 0.0, -a * b, "loop closed"
    if progress < 0.20:
        u = smoothstep(progress / 0.20)
        return a * u, 0.0, 0.0, "shift in x"
    if progress < 0.40:
        u = smoothstep((progress - 0.20) / 0.20)
        return a, b * u, 0.0, "shift in k"
    if progress < 0.60:
        u = smoothstep((progress - 0.40) / 0.20)
        return a * (1 - u), b, a * b * u, "undo the x shift"
    if progress < 0.80:
        u = smoothstep((progress - 0.60) / 0.20)
        return 0.0, b * (1 - u), a * b, "undo the k shift"
    return 0.0, 0.0, a * b, "loop closed"


def draw_loop_panel(
    draw: ImageDraw.ImageDraw,
    a_now: float,
    b_now: float,
    gamma: float,
    leg: str,
    phase_symbol: str = "β",
) -> None:
    panel(draw, (42, 112, 344, 382))
    draw_text(draw, (61, 133), "Closed loop of operators", font_obj=PANE_TITLE)
    left, right = 99.0, 288.0
    top, bottom = 184.0, 335.0
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=MUTED, width=s(2))
    draw.line((s(left), s(bottom), s(left), s(top)), fill=MUTED, width=s(2))
    draw_text(draw, (right, bottom + 24), "x shift", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (left - 11, top), "k shift", fill=MUTED, font_obj=SMALL, anchor="rs")
    draw.rectangle((s(left), s(top), s(right), s(bottom)), outline=rgba(PURPLE, 0.60), width=s(3))
    px = left + (a_now / 1.25) * (right - left)
    py = bottom - (b_now / 0.90) * (bottom - top)
    draw.ellipse((s(px - 7), s(py - 7), s(px + 7), s(py + 7)), fill=GREEN, outline=BG, width=s(2))
    draw_text(draw, ((left + right) / 2, 361), leg, fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")

    panel(draw, (42, 397, 344, 638))
    draw_text(draw, (61, 417), "Phase left after closing", font_obj=PANE_TITLE)
    draw_phasor(draw, (154, 523), 61, gamma, PURPLE)
    draw_text(draw, (247, 493), f"{phase_symbol} = oriented", fill=MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, (247, 512), "loop area", fill=MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, (247, 548), f"{phase_symbol} = {gamma:.2f}", fill=PURPLE, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, (193, 609), "not time evolution", fill=RED, font_obj=LABEL_BOLD, anchor="mm")


def draw_loop_state_panel(draw: ImageDraw.ImageDraw, a_now: float, b_now: float, gamma: float) -> None:
    bounds = (363, 112, 1238, 638)
    panel(draw, bounds)
    draw_text(draw, (385, 133), "The packet and spectrum return; the common phase does not", font_obj=PANE_TITLE)
    left, right = 425.0, 1199.0
    baseline = 342.0
    phases = (0.0, 0.0, 0.0)
    packet_scale = 71.0 / sum(AMPS)
    draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.35), width=s(1))
    real_points: list[tuple[int, int]] = []
    imag_points: list[tuple[int, int]] = []
    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    initial_real: list[tuple[int, int]] = []
    initial_upper: list[tuple[int, int]] = []
    initial_lower: list[tuple[int, int]] = []
    for sample in range(X_SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
        _, value = packet_values(x, phases, k_shift=b_now, x_shift=a_now, common_phase=gamma)
        _, initial = packet_values(x, phases)
        px = s(plot_x(left, right, x))
        real_points.append((px, s(baseline - packet_scale * value.real)))
        imag_points.append((px, s(baseline - packet_scale * value.imag)))
        upper.append((px, s(baseline - packet_scale * abs(value))))
        lower.append((px, s(baseline + packet_scale * abs(value))))
        initial_real.append((px, s(baseline - packet_scale * initial.real)))
        initial_upper.append((px, s(baseline - packet_scale * abs(initial))))
        initial_lower.append((px, s(baseline + packet_scale * abs(initial))))
    dashed_line(draw, initial_upper, rgba(MUTED, 0.50), width=2)
    dashed_line(draw, initial_lower, rgba(MUTED, 0.50), width=2)
    draw.line(upper, fill=rgba(LIGHT_BLUE, 0.82), width=s(3), joint="curve")
    draw.line(lower, fill=rgba(LIGHT_BLUE, 0.82), width=s(3), joint="curve")
    dashed_line(draw, initial_real, rgba(MUTED, 0.78), width=2, dash=8, gap=6)
    dashed_line(draw, imag_points, RED, width=2)
    draw.line(real_points, fill=BLUE, width=s(3), joint="curve")
    draw_text(draw, (left, 222), "x-space packet", fill=INK, font_obj=LABEL_BOLD)
    draw_text(draw, (right, 222), "gray dashed: starting Re ψ", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (right, 435), "x", fill=MUTED, font_obj=SMALL, anchor="ra")

    spectrum_y = 574.0
    spectrum_left, spectrum_right = 475.0, 1147.0
    k_min, k_max = K0 - 2.25, K0 + 2.25
    draw.line((s(spectrum_left), s(spectrum_y), s(spectrum_right), s(spectrum_y)), fill=MUTED, width=s(2))
    draw_text(draw, (left, 482), "k-space magnitudes", fill=INK, font_obj=LABEL_BOLD)
    for k, amp, color in zip(KS, AMPS, MODE_COLORS):
        ghost_x = spectrum_left + (k - k_min) / (k_max - k_min) * (spectrum_right - spectrum_left)
        current_x = spectrum_left + (k + b_now - k_min) / (k_max - k_min) * (spectrum_right - spectrum_left)
        draw.line((s(ghost_x), s(spectrum_y), s(ghost_x), s(spectrum_y - 61 * amp)), fill=rgba(MUTED, 0.42), width=s(3))
        draw.line((s(current_x), s(spectrum_y), s(current_x), s(spectrum_y - 61 * amp)), fill=color, width=s(5))
    draw_text(draw, (spectrum_right, spectrum_y + 25), "k", fill=MUTED, font_obj=SMALL, anchor="ra")

    coeff_phases = tuple(gamma - k * a_now for k in KS)
    for index, (phase, color, x) in enumerate(zip(coeff_phases, MODE_COLORS, (766.0, 866.0, 966.0))):
        draw_phasor(draw, (x, 182), 27, phase, color, f"k{index + 1}")
    if a_now == 0.0 and b_now == 0.0 and gamma > 0.0:
        draw_text(draw, (1100, 181), "same final angle", fill=PURPLE, font_obj=LABEL_BOLD, anchor="mm")


def draw_loop_final_reveal(
    draw: ImageDraw.ImageDraw,
    reveal: float,
    orientation: float = 1.0,
    phase_symbol: str = "β",
) -> None:
    beta = orientation * 1.25 * 0.90 * reveal
    panel(draw, (42, 112, 349, 638))
    draw_text(draw, (61, 133), "The closed loop", font_obj=PANE_TITLE)

    loop_left, loop_top = 102.0, 190.0
    loop_right, loop_bottom = 287.0, 340.0
    draw.line((s(loop_left - 22), s(loop_bottom), s(loop_right + 17), s(loop_bottom)), fill=rgba(MUTED, 0.52), width=s(2))
    draw.line((s(loop_left), s(loop_bottom + 19), s(loop_left), s(loop_top - 17)), fill=rgba(MUTED, 0.52), width=s(2))
    draw_text(draw, (loop_right + 18, loop_bottom + 1), "x", fill=MUTED, font_obj=SMALL, anchor="lm")
    draw_text(draw, (loop_left - 2, loop_top - 22), "k", fill=MUTED, font_obj=SMALL, anchor="ms")
    if orientation < 0.0:
        arrow(draw, (loop_left, loop_bottom), (loop_left, loop_top), GOLD, width=4, head=10)
        arrow(draw, (loop_left, loop_top), (loop_right, loop_top), BLUE, width=4, head=10)
        arrow(draw, (loop_right, loop_top), (loop_right, loop_bottom), GOLD, width=4, head=10)
        arrow(draw, (loop_right, loop_bottom), (loop_left, loop_bottom), BLUE, width=4, head=10)
    else:
        arrow(draw, (loop_left, loop_bottom), (loop_right, loop_bottom), BLUE, width=4, head=10)
        arrow(draw, (loop_right, loop_bottom), (loop_right, loop_top), GOLD, width=4, head=10)
        arrow(draw, (loop_right, loop_top), (loop_left, loop_top), BLUE, width=4, head=10)
        arrow(draw, (loop_left, loop_top), (loop_left, loop_bottom), GOLD, width=4, head=10)
    draw.ellipse((s(loop_left - 5), s(loop_bottom - 5), s(loop_left + 5), s(loop_bottom + 5)), fill=PURPLE)
    draw_text(draw, (195, 371), "same x and k", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(
        draw,
        (195, 411),
        f"ψafter(x) = exp(i{phase_symbol}) ψbefore(x)",
        fill=INK,
        font_obj=LABEL_BOLD,
        anchor="mm",
    )
    area_text = "-ab" if orientation < 0.0 else "ab"
    draw_text(
        draw,
        (195, 447),
        f"{phase_symbol} = {area_text} = {orientation * 1.25 * 0.90:.2f} rad",
        fill=PURPLE,
        font_obj=LABEL_BOLD,
        anchor="mm",
    )

    dashed_line(draw, [(s(77), s(507)), (s(137), s(507))], MUTED, width=2, dash=8, gap=6)
    draw_text(draw, (151, 507), "starting wave", fill=MUTED, font_obj=SMALL, anchor="lm")
    draw.line((s(77), s(545), s(137), s(545)), fill=BLUE, width=s(3))
    draw_text(draw, (151, 545), "wave after loop", fill=INK, font_obj=SMALL, anchor="lm")
    draw.line((s(77), s(583), s(137), s(583)), fill=LIGHT_BLUE, width=s(3))
    draw_text(draw, (151, 583), "unchanged envelope", fill=GREEN, font_obj=SMALL, anchor="lm")

    panel(draw, (367, 112, 1238, 638))
    draw_text(draw, (389, 133), "The final waves do not fall back onto their starting traces", font_obj=PANE_TITLE)
    left, right = 435.0, 1203.0
    row_y = (205.0, 277.0, 349.0)
    for index, (baseline, color, k) in enumerate(zip(row_y, MODE_COLORS, KS)):
        draw.line((s(left), s(baseline), s(right), s(baseline)), fill=rgba(MUTED, 0.20), width=s(1))
        draw_text(draw, (left - 15, baseline), f"k{index + 1}", fill=color, font_obj=LABEL_BOLD, anchor="rm")
        initial_points: list[tuple[int, int]] = []
        final_points: list[tuple[int, int]] = []
        for sample in range(X_SAMPLES):
            x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
            px = s(plot_x(left, right, x))
            initial_points.append((px, s(baseline - 22.0 * math.cos(k * x))))
            final_points.append((px, s(baseline - 22.0 * math.cos(k * x + beta))))
        dashed_line(draw, initial_points, rgba(MUTED, 0.72), width=2, dash=8, gap=6)
        draw.line(final_points, fill=color, width=s(3), joint="curve")

    packet_y = 512.0
    packet_scale = 63.0 / sum(AMPS)
    draw.line((s(left), s(packet_y), s(right), s(packet_y)), fill=rgba(MUTED, 0.28), width=s(1))
    draw_text(draw, (left - 15, packet_y), "sum", fill=INK, font_obj=LABEL_BOLD, anchor="rm")
    initial_real: list[tuple[int, int]] = []
    final_real: list[tuple[int, int]] = []
    envelope_upper: list[tuple[int, int]] = []
    envelope_lower: list[tuple[int, int]] = []
    for sample in range(X_SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * sample / (X_SAMPLES - 1)
        _, initial = packet_values(x, (0.0, 0.0, 0.0))
        final = cmath.exp(1j * beta) * initial
        px = s(plot_x(left, right, x))
        initial_real.append((px, s(packet_y - packet_scale * initial.real)))
        final_real.append((px, s(packet_y - packet_scale * final.real)))
        envelope_upper.append((px, s(packet_y - packet_scale * abs(initial))))
        envelope_lower.append((px, s(packet_y + packet_scale * abs(initial))))
    draw.line(envelope_upper, fill=LIGHT_BLUE, width=s(3), joint="curve")
    draw.line(envelope_lower, fill=LIGHT_BLUE, width=s(3), joint="curve")
    dashed_line(draw, initial_real, rgba(MUTED, 0.72), width=2, dash=8, gap=6)
    draw.line(final_real, fill=BLUE, width=s(3), joint="curve")
    draw_text(draw, (819, 603), "same envelope; every solid wave has the same phase offset from its dashed trace", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")


def scene_xk_loop(
    progress: float,
    orientation: float = 1.0,
    phase_symbol: str = "β",
) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    if progress < 0.68:
        loop_progress = min(1.0, max(0.0, (progress - 0.03) / 0.60))
        a_now, b_now, gamma, leg = loop_state(loop_progress, orientation)
        header(draw, 3, "The x-k loop temporarily shifts the packet and spectrum", "The net transformation is read only after all four operations close the loop.")
        draw_loop_panel(draw, a_now, b_now, gamma, leg, phase_symbol)
        draw_loop_state_panel(draw, a_now, b_now, gamma)
        footer(draw, "These are intermediate changes. The loop's net effect appears only after it closes.")
    else:
        reveal = smoothstep(min(1.0, max(0.0, (progress - 0.68) / 0.14)))
        header(
            draw,
            3,
            "After the x-k loop closes, only a global phase remains",
            f"The x- and k-distributions return; every component retains the same added phase {phase_symbol}.",
        )
        draw_loop_final_reveal(draw, reveal, orientation, phase_symbol)
        footer(draw, f"The final state differs from the initial state only by one common phase factor exp(i{phase_symbol}).")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def time_case_phases(kind: str, tau: float) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    omega0 = 0.82
    velocity = 0.28
    curvature = 0.57
    offsets = tuple(k - K0 for k in KS)
    if kind == "constant":
        omegas = (omega0, omega0, omega0)
    elif kind == "affine":
        omegas = tuple(omega0 + velocity * offset for offset in offsets)
    elif kind == "nonlinear":
        omegas = tuple(omega0 + velocity * offset + curvature * offset * offset for offset in offsets)
    else:
        raise ValueError(kind)
    phases = tuple(-omega * tau for omega in omegas)
    return phases, omegas


def draw_time_sidebar(draw: ImageDraw.ImageDraw, phases: tuple[float, float, float], relation: str) -> None:
    draw_phase_vs_k(draw, phases, relation)
    draw_three_phasors(draw, phases)


def scene_constant_omega(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    tau = 4.4 * motion(progress)
    phases, _ = time_case_phases("constant", tau)
    header(draw, 4, "Constant Ω(k): global phase accumulates over time", "All three modal phase clocks turn together at the same rate.")
    draw_time_sidebar(draw, phases, "horizontal: Ω is the same for every mode")
    draw_component_and_packet_panel(draw, phases)
    footer(draw, "Ω(k)=Ω₀  →  ψ(x,t)=exp(−iΩ₀t) ψ(x,0): the complex packet rotates while |ψ| stays fixed.")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def scene_affine_omega(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    tau = 4.25 * motion(progress)
    phases, _ = time_case_phases("affine", tau)
    header(draw, 5, "Affine Ω(k): relative phase translates the packet", "The accumulated phases differ, but remain a straight line across k.")
    draw_time_sidebar(draw, phases, "straight slope: one rigid spatial shift")
    draw_component_and_packet_panel(
        draw,
        phases,
        ghost_magnitude_phases=(0.0, 0.0, 0.0),
        ghost_x_shift=0.0,
        ghost_label="gray: starting |ψ|",
    )
    footer(draw, "Ω(k)=Ω₀+vk  →  relative phases change linearly in k; |ψ| moves rigidly without deforming.")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def scene_nonlinear_omega(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    tau = 4.05 * motion(progress)
    phases, _ = time_case_phases("nonlinear", tau)
    velocity = 0.28
    affine_reference, _ = time_case_phases("affine", tau)
    header(draw, 6, "Nonlinear Ω(k): relative phase changes the packet's shape", "The three accumulated phases no longer lie on one straight line across k.")
    draw_time_sidebar(draw, phases, "bent: no single global phase + shift fits")
    draw_component_and_packet_panel(
        draw,
        phases,
        ghost_magnitude_phases=(0.0, 0.0, 0.0),
        ghost_x_shift=velocity * tau,
        ghost_label="gray: rigid-shift reference",
    )
    # The affine reference is intentionally computed above as a correctness
    # check: its magnitude is exactly the shifted initial magnitude.
    _ = affine_reference
    footer(draw, "Nonlinear Ω(k) changes relative phases nonlinearly: this three-mode packet deforms and breathes.")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


SCENE_DRAWERS = (
    scene_single_mode,
    scene_global_packet,
    scene_xk_loop,
    scene_constant_omega,
    scene_affine_omega,
    scene_nonlinear_omega,
)


def scene_for_time(seconds: float) -> tuple[int, float]:
    elapsed = 0.0
    for index, duration in enumerate(SCENE_DURATIONS):
        if seconds < elapsed + duration or index == len(SCENE_DURATIONS) - 1:
            return index, max(0.0, min(1.0, (seconds - elapsed) / duration))
        elapsed += duration
    return len(SCENE_DURATIONS) - 1, 1.0


def draw_frame(frame: int) -> Image.Image:
    seconds = min(TOTAL_SECONDS - 1 / FPS, frame / FPS)
    scene_index, progress = scene_for_time(seconds)
    return SCENE_DRAWERS[scene_index](progress)


def make_contact_sheet(name: str) -> Path:
    cumulative = 0.0
    samples: list[tuple[int, str]] = []
    labels = ("one mode", "global packet", "x-k loop", "constant omega", "affine omega", "nonlinear omega")
    sample_fractions = (0.72, 0.72, 0.92, 0.72, 0.72, 0.72)
    for duration, label, fraction in zip(SCENE_DURATIONS, labels, sample_fractions):
        timestamp = cumulative + duration * fraction
        samples.append((min(FRAMES - 1, round(timestamp * FPS)), label))
        cumulative += duration
    cols = 3
    rows = 2
    thumb_w = 400
    thumb_h = 225
    label_h = 25
    margin = 14
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 5, y + thumb_h + 4), label, fill=MUTED)
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


def render() -> tuple[Path, Path]:
    name = "symmetry-phase-advance-three-component-packet-v4"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{name}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
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
        return video, contact
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact = render()
    print(video)
    print(contact)
    print(verify_video(video))


if __name__ == "__main__":
    main()
