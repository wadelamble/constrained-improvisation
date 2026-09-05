from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import generate_symmetry_wave_paths_explainer as wave


ROOT = Path(__file__).resolve().parents[1]
ANIMATIONS = ROOT / "content" / "drafts" / "animations"
DIAGRAMS = ROOT / "content" / "drafts" / "diagrams"

PLANE_SPHERICAL_NAME = "symmetry-plane-and-spherical-wave-rays"
DOUBLE_SLIT_NAME = "symmetry-double-slit-candidate-paths"
PHASOR_NAME = "symmetry-complex-phasor-rotation"

# A single geometry is shared by the moving two-slit scene, the clean path
# diagram, and the corresponding tip-to-tail phasor diagram. Coordinates are
# diagram units, not pixels.
WORLD_X = (-5.0, 6.0)
WORLD_Y = (-2.55, 2.55)
A = (-4.2, 0.0)
C = (0.0, 1.0)
D = (0.0, -1.0)
B = (5.2, 0.55)
WAVELENGTH = 1.25
WAVE_NUMBER = 2.0 * math.pi / WAVELENGTH

L_AC = math.dist(A, C)
L_AD = math.dist(A, D)
L_CB = math.dist(C, B)
L_DB = math.dist(D, B)
L_ACB = L_AC + L_CB
L_ADB = L_AD + L_DB
DELTA_LENGTH = L_ADB - L_ACB
DELTA_PHASE = WAVE_NUMBER * DELTA_LENGTH


def world_to_canvas(
    point: tuple[float, float],
    bounds: tuple[float, float, float, float],
) -> tuple[float, float]:
    left, top, right, bottom = bounds
    x, y = point
    px = left + (x - WORLD_X[0]) / (WORLD_X[1] - WORLD_X[0]) * (right - left)
    py = top + (WORLD_Y[1] - y) / (WORLD_Y[1] - WORLD_Y[0]) * (bottom - top)
    return px, py


def mix_rgb(a: np.ndarray, b: np.ndarray, q: np.ndarray) -> np.ndarray:
    return a + (b - a) * q[..., None]


def field_to_image(values: np.ndarray, limit: float = 1.0) -> Image.Image:
    """Map a signed field to the manuscript's muted blue/ivory/red palette."""
    normalized = np.clip(values / limit, -1.0, 1.0)
    panel = np.asarray(wave.PANEL, dtype=float)
    blue = np.asarray((52, 91, 126), dtype=float)
    red = np.asarray((174, 78, 58), dtype=float)
    negative = mix_rgb(panel, blue, np.clip(-normalized, 0.0, 1.0) ** 0.82)
    positive = mix_rgb(panel, red, np.clip(normalized, 0.0, 1.0) ** 0.82)
    rgb = np.where((normalized >= 0.0)[..., None], positive, negative)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def paste_rounded_field(
    image: Image.Image,
    field: Image.Image,
    bounds: tuple[float, float, float, float],
    radius: float = 13.0,
) -> None:
    box = tuple(wave.s(v) for v in bounds)
    resized = field.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.BICUBIC).convert("RGBA")
    mask = Image.new("L", resized.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, resized.width - 1, resized.height - 1), radius=wave.s(radius), fill=255)
    image.alpha_composite(Image.composite(resized, Image.new("RGBA", resized.size, (0, 0, 0, 0)), mask), dest=(box[0], box[1]))


def finish_frame(image: Image.Image) -> Image.Image:
    return image.convert("RGB").resize((wave.WIDTH, wave.HEIGHT), Image.Resampling.LANCZOS)


def draw_panel_border(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(wave.s(v) for v in bounds),
        radius=wave.s(13),
        outline=wave.FAINT,
        width=wave.s(2),
    )


def draw_small_arrowhead(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 3,
) -> None:
    wave.draw_arrow(draw, start, end, color, width)


# ---------------------------------------------------------------------------
# 1. Plane and spherical wavefronts, with their normal rays.


PLANE_SPHERICAL_DURATION = 6.0


def draw_plane_and_spherical(frame: int) -> Image.Image:
    seconds = min(PLANE_SPHERICAL_DURATION - 1 / wave.FPS, frame / wave.FPS)
    phase = 2.0 * math.pi * 1.5 * seconds / PLANE_SPHERICAL_DURATION

    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "Wavefronts and their rays", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "A ray points normal to a moving phase front.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )

    left_bounds = (35.0, 112.0, 625.0, 675.0)
    right_bounds = (655.0, 112.0, 1245.0, 675.0)

    nx, ny = 520, 480
    xx, yy = np.meshgrid(np.linspace(0.0, 1.0, nx), np.linspace(-0.5, 0.5, ny))
    plane = np.cos(2.0 * math.pi * 5.4 * xx - phase)
    plane *= 0.72
    paste_rounded_field(image, field_to_image(plane, 1.0), left_bounds)

    sx, sy = 0.23, 0.0
    radius = np.hypot(xx - sx, yy - sy)
    spherical = np.cos(2.0 * math.pi * radius / 0.18 - phase)
    spherical *= 0.82 / np.sqrt(0.55 + 2.1 * radius)
    spherical *= 1.0 - np.exp(-((radius / 0.035) ** 2))
    paste_rounded_field(image, field_to_image(spherical, 1.05), right_bounds)

    draw = ImageDraw.Draw(image, "RGBA")
    draw_panel_border(draw, left_bounds)
    draw_panel_border(draw, right_bounds)
    wave.draw_text(draw, (330, 136), "plane wave", font_obj=wave.PANE_TITLE, anchor="ma")
    wave.draw_text(draw, (950, 136), "spherical wave", font_obj=wave.PANE_TITLE, anchor="ma")

    # Parallel rays are normal to the vertical plane-wave fronts.
    for y in (235.0, 315.0, 395.0, 475.0, 555.0):
        draw_small_arrowhead(draw, (105.0, y), (565.0, y), wave.rgba(wave.GOLD, 0.88), 3)
    wave.draw_text(draw, (330, 635), "parallel fronts  ->  parallel rays", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")

    # Radial rays are normal to concentric spherical fronts.
    source = (655.0 + 0.23 * (1245.0 - 655.0), (112.0 + 675.0) / 2.0)
    for angle in np.linspace(-1.15, 1.15, 9):
        direction = (math.cos(angle), -math.sin(angle))
        start = (source[0] + 42.0 * direction[0], source[1] + 42.0 * direction[1])
        length = min(
            500.0,
            (1230.0 - source[0]) / max(direction[0], 0.12),
            245.0 / max(abs(direction[1]), 0.12),
        )
        end = (source[0] + length * direction[0], source[1] + length * direction[1])
        draw_small_arrowhead(draw, start, end, wave.rgba(wave.GOLD, 0.88), 3)
    wave.circle(draw, source, 7.0, wave.RED)
    wave.draw_text(draw, (950, 635), "concentric fronts  ->  radial rays", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")

    return finish_frame(image)


# ---------------------------------------------------------------------------
# 2. Plane wave through two slits, with two candidate contributions to B.


DOUBLE_SLIT_DURATION = 7.0
DOUBLE_SLIT_BOUNDS = (35.0, 112.0, 1245.0, 675.0)


def double_slit_field(phase: float, width: int = 800, height: int = 370) -> Image.Image:
    xs = np.linspace(WORLD_X[0], WORLD_X[1], width)
    ys = np.linspace(WORLD_Y[1], WORLD_Y[0], height)
    xx, yy = np.meshgrid(xs, ys)

    incident = 0.72 * np.cos(WAVE_NUMBER * xx - phase)
    r_c = np.hypot(xx - C[0], yy - C[1])
    r_d = np.hypot(xx - D[0], yy - D[1])
    outgoing = (
        np.cos(WAVE_NUMBER * r_c - phase) / np.sqrt(0.34 + r_c)
        + np.cos(WAVE_NUMBER * r_d - phase) / np.sqrt(0.34 + r_d)
    )
    outgoing *= 0.82
    field = np.where(xx <= 0.0, incident, outgoing)
    return field_to_image(field, 1.32)


def draw_slit_screen(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    screen_x, _ = world_to_canvas((0.0, 0.0), bounds)
    c = world_to_canvas(C, bounds)
    d = world_to_canvas(D, bounds)
    half_gap = 18.0
    top, bottom = bounds[1] + 2.0, bounds[3] - 2.0
    for y0, y1 in ((top, c[1] - half_gap), (c[1] + half_gap, d[1] - half_gap), (d[1] + half_gap, bottom)):
        draw.line((wave.s(screen_x), wave.s(y0), wave.s(screen_x), wave.s(y1)), fill=wave.INK, width=wave.s(8))
    wave.circle(draw, c, 6.0, wave.BLUE)
    wave.circle(draw, d, 6.0, wave.GOLD)


def draw_shared_routes(
    draw: ImageDraw.ImageDraw,
    bounds: tuple[float, float, float, float],
    alpha: float = 0.92,
    labels: bool = True,
) -> None:
    a = world_to_canvas(A, bounds)
    c = world_to_canvas(C, bounds)
    d = world_to_canvas(D, bounds)
    b = world_to_canvas(B, bounds)
    for p0, p1, color in ((a, c, wave.BLUE), (c, b, wave.BLUE), (a, d, wave.GOLD), (d, b, wave.GOLD)):
        wave.dashed_line(draw, p0, p1, wave.rgba(color, alpha), width=3, dash=12, gap=8)
    for point, color in ((a, wave.INK), (c, wave.BLUE), (d, wave.GOLD), (b, wave.INK)):
        wave.circle(draw, point, 7.0, color)
    if labels:
        wave.draw_text(draw, (a[0] - 2, a[1] + 29), "A", font_obj=wave.LABEL_BOLD, anchor="ma")
        wave.draw_text(draw, (c[0] + 15, c[1] - 11), "C", fill=wave.BLUE, font_obj=wave.LABEL_BOLD)
        wave.draw_text(draw, (d[0] + 15, d[1] + 7), "D", fill=wave.GOLD, font_obj=wave.LABEL_BOLD)
        wave.draw_text(draw, (b[0], b[1] + 29), "B", font_obj=wave.LABEL_BOLD, anchor="ma")
        wave.draw_text(draw, (262, 188), "plane wave", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
        wave.draw_text(draw, (905, 188), "outgoing waves interfere", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
        wave.draw_text(draw, (790, 630), "dashed lines: two contributions to the field at B", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ma")


def draw_double_slit(frame: int) -> Image.Image:
    seconds = min(DOUBLE_SLIT_DURATION - 1 / wave.FPS, frame / wave.FPS)
    phase = 2.0 * math.pi * 2.0 * seconds / DOUBLE_SLIT_DURATION
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "Two slits create two simultaneous contributions at B", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "The field propagates through both openings; the dashed routes label the two terms being added.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    paste_rounded_field(image, double_slit_field(phase), DOUBLE_SLIT_BOUNDS)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_panel_border(draw, DOUBLE_SLIT_BOUNDS)
    draw_slit_screen(draw, DOUBLE_SLIT_BOUNDS)
    draw_shared_routes(draw, DOUBLE_SLIT_BOUNDS)
    return finish_frame(image)


# ---------------------------------------------------------------------------
# 3. Static A-C/D-B path geometry.


DIAMOND_PATH = DIAGRAMS / "symmetry-double-slit-two-path-diamond.png"


def route_label_position(
    p0: tuple[float, float],
    p1: tuple[float, float],
    normal_offset: float,
) -> tuple[float, float]:
    mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = max(math.hypot(dx, dy), 1e-9)
    return mx - normal_offset * dy / length, my + normal_offset * dx / length


def draw_diamond_diagram() -> Image.Image:
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "Two paths through the apertures reach the same point B", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "B is deliberately off the centerline, so the two path lengths differ.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    bounds = (35.0, 112.0, 1245.0, 675.0)
    wave.panel(draw, bounds)
    a = world_to_canvas(A, bounds)
    c = world_to_canvas(C, bounds)
    d = world_to_canvas(D, bounds)
    b = world_to_canvas(B, bounds)
    center_left = world_to_canvas((WORLD_X[0], 0.0), bounds)
    center_right = world_to_canvas((WORLD_X[1], 0.0), bounds)
    wave.dashed_line(draw, center_left, center_right, wave.rgba(wave.MUTED, 0.32), width=2, dash=10, gap=8)
    draw_slit_screen(draw, bounds)
    for p0, p1, color in ((a, c, wave.BLUE), (c, b, wave.BLUE), (a, d, wave.GOLD), (d, b, wave.GOLD)):
        draw.line((wave.s(p0[0]), wave.s(p0[1]), wave.s(p1[0]), wave.s(p1[1])), fill=color, width=wave.s(5))
    for point, color in ((a, wave.INK), (c, wave.BLUE), (d, wave.GOLD), (b, wave.INK)):
        wave.circle(draw, point, 8.0, color)
    wave.draw_text(draw, (a[0], a[1] + 31), "A", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (c[0] + 16, c[1] - 13), "C", fill=wave.BLUE, font_obj=wave.LABEL_BOLD)
    wave.draw_text(draw, (d[0] + 16, d[1] + 8), "D", fill=wave.GOLD, font_obj=wave.LABEL_BOLD)
    wave.draw_text(draw, (b[0], b[1] + 31), "B", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (b[0] + 15, b[1] - 24), "off center", fill=wave.MUTED, font_obj=wave.SMALL)

    labels = (
        (a, c, "AC", wave.BLUE, -22.0),
        (c, b, "CB", wave.BLUE, -22.0),
        (a, d, "AD", wave.GOLD, 22.0),
        (d, b, "DB", wave.GOLD, 22.0),
    )
    for p0, p1, text, color, offset in labels:
        wave.draw_text(draw, route_label_position(p0, p1, offset), text, fill=color, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, (640, 641), "path ACB", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (790, 641), "path ADB", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    return finish_frame(image)


# ---------------------------------------------------------------------------
# 4. Minimal rotating complex phasor.


PHASOR_DURATION = 6.0


def phasor_endpoint(origin: tuple[float, float], length: float, angle: float) -> tuple[float, float]:
    return origin[0] + length * math.cos(angle), origin[1] - length * math.sin(angle)


def draw_rotating_phasor(frame: int) -> Image.Image:
    seconds = min(PHASOR_DURATION - 1 / wave.FPS, frame / wave.FPS)
    angle = 2.0 * math.pi * seconds / PHASOR_DURATION
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "A complex wave value has magnitude and phase", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "Here the magnitude stays fixed while the phase angle changes.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    wave.panel(draw, (150, 112, 1130, 675))
    origin = (500.0, 397.0)
    radius = 205.0
    axis = wave.rgba(wave.MUTED, 0.46)
    draw.line((wave.s(origin[0] - 250), wave.s(origin[1]), wave.s(origin[0] + 250), wave.s(origin[1])), fill=axis, width=wave.s(2))
    draw.line((wave.s(origin[0]), wave.s(origin[1] - 250), wave.s(origin[0]), wave.s(origin[1] + 250)), fill=axis, width=wave.s(2))
    wave.circle(draw, origin, radius, None, wave.rgba(wave.MUTED, 0.55), 2)
    reference = phasor_endpoint(origin, radius, 0.0)
    wave.dashed_line(draw, origin, reference, wave.rgba(wave.MUTED, 0.42), width=2, dash=8, gap=7)
    endpoint = phasor_endpoint(origin, radius, angle)
    wave.draw_arrow(draw, origin, endpoint, wave.PURPLE if hasattr(wave, "PURPLE") else (117, 85, 145), 7)
    wave.circle(draw, endpoint, 7.0, wave.GOLD)
    wave.circle(draw, origin, 4.0, wave.INK)
    arc_box = (
        wave.s(origin[0] - 82),
        wave.s(origin[1] - 82),
        wave.s(origin[0] + 82),
        wave.s(origin[1] + 82),
    )
    draw.arc(arc_box, start=-math.degrees(angle), end=0, fill=wave.GOLD, width=wave.s(4))
    label_point = phasor_endpoint(origin, 105.0, angle / 2.0)
    wave.draw_text(draw, label_point, "phi", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, (origin[0] + radius + 20, origin[1] + 10), "Re", fill=wave.MUTED, font_obj=wave.LABEL_BOLD)
    wave.draw_text(draw, (origin[0] + 12, origin[1] - radius - 22), "Im", fill=wave.MUTED, font_obj=wave.LABEL_BOLD)

    wave.draw_text(draw, (870, 265), "z(phi) = exp(i phi)", font_obj=wave.FINAL, anchor="ma")
    wave.draw_text(draw, (870, 342), "magnitude:  |z| = 1", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (870, 399), "phase:  phi", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (870, 479), "the arrow turns", fill=wave.MUTED, font_obj=wave.LABEL, anchor="ma")
    wave.draw_text(draw, (870, 510), "without changing length", fill=wave.MUTED, font_obj=wave.LABEL, anchor="ma")
    return finish_frame(image)


# ---------------------------------------------------------------------------
# 5. Static tip-to-tail sum for the same A-C/D-B geometry.


PHASOR_SUM_PATH = DIAGRAMS / "symmetry-double-slit-two-path-phasor-sum.png"


def draw_phasor_sum_diagram() -> Image.Image:
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "The two path contributions add tip to tail", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "Their angle difference comes from the path-length difference in the preceding diagram.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    wave.panel(draw, (35, 112, 510, 675))
    wave.panel(draw, (535, 112, 1245, 675))

    wave.draw_text(draw, (272, 142), "same two paths", font_obj=wave.PANE_TITLE, anchor="ma")
    mini_bounds = (65.0, 190.0, 480.0, 430.0)
    a = world_to_canvas(A, mini_bounds)
    c = world_to_canvas(C, mini_bounds)
    d = world_to_canvas(D, mini_bounds)
    b = world_to_canvas(B, mini_bounds)
    screen_x, _ = world_to_canvas((0.0, 0.0), mini_bounds)
    for y0, y1 in ((mini_bounds[1], c[1] - 8), (c[1] + 8, d[1] - 8), (d[1] + 8, mini_bounds[3])):
        draw.line((wave.s(screen_x), wave.s(y0), wave.s(screen_x), wave.s(y1)), fill=wave.INK, width=wave.s(5))
    for p0, p1, color in ((a, c, wave.BLUE), (c, b, wave.BLUE), (a, d, wave.GOLD), (d, b, wave.GOLD)):
        draw.line((wave.s(p0[0]), wave.s(p0[1]), wave.s(p1[0]), wave.s(p1[1])), fill=color, width=wave.s(4))
    for point, color in ((a, wave.INK), (c, wave.BLUE), (d, wave.GOLD), (b, wave.INK)):
        wave.circle(draw, point, 5.5, color)
    wave.draw_text(draw, (a[0], a[1] + 22), "A", font_obj=wave.SMALL, anchor="ma")
    wave.draw_text(draw, (c[0] + 9, c[1] - 14), "C", fill=wave.BLUE, font_obj=wave.SMALL)
    wave.draw_text(draw, (d[0] + 9, d[1] + 3), "D", fill=wave.GOLD, font_obj=wave.SMALL)
    wave.draw_text(draw, (b[0], b[1] + 22), "B", font_obj=wave.SMALL, anchor="ma")

    wave.draw_text(draw, (272, 480), f"L(ACB) = {L_ACB:.2f}", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 517), f"L(ADB) = {L_ADB:.2f}", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 565), f"Delta L = {DELTA_LENGTH:.2f}", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 604), f"Delta phi = k Delta L = {DELTA_PHASE:.2f} rad", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")

    wave.draw_text(draw, (890, 142), "complex contributions at B", font_obj=wave.PANE_TITLE, anchor="ma")
    origin = (650.0, 402.0)
    step = 235.0
    # A common phase reference is chosen so equal contributions at +/- Delta
    # phi / 2 have a horizontal resultant. Only their difference is physical.
    phi_acb = -DELTA_PHASE / 2.0
    phi_adb = DELTA_PHASE / 2.0
    first_tip = phasor_endpoint(origin, step, phi_acb)
    final_tip = phasor_endpoint(first_tip, step, phi_adb)
    draw.line((wave.s(610), wave.s(origin[1]), wave.s(1200), wave.s(origin[1])), fill=wave.rgba(wave.MUTED, 0.35), width=wave.s(2))
    wave.circle(draw, origin, 4.0, wave.INK)
    wave.draw_arrow(draw, origin, first_tip, wave.BLUE, 7)
    wave.draw_arrow(draw, first_tip, final_tip, wave.GOLD, 7)
    wave.draw_arrow(draw, origin, final_tip, wave.GREEN, 10)
    wave.circle(draw, first_tip, 4.0, wave.BLUE)
    wave.circle(draw, final_tip, 5.0, wave.GREEN)
    wave.draw_text(draw, route_label_position(origin, first_tip, 28.0), "path ACB", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, route_label_position(first_tip, final_tip, -30.0), "path ADB", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, ((origin[0] + final_tip[0]) / 2.0, origin[1] - 31.0), "resultant at B", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, (890, 550), f"relative phase = {DELTA_PHASE:.2f} rad", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (890, 591), "A common phase rotates every arrow together.", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ma")
    wave.draw_text(draw, (890, 620), "It leaves the relative angle and resultant length unchanged.", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ma")
    return finish_frame(image)


def main() -> None:
    ANIMATIONS.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)

    jobs = (
        (
            PLANE_SPHERICAL_NAME,
            PLANE_SPHERICAL_DURATION,
            draw_plane_and_spherical,
            (0.2, 1.1, 2.1, 3.1, 4.1, 5.1),
        ),
        (
            DOUBLE_SLIT_NAME,
            DOUBLE_SLIT_DURATION,
            draw_double_slit,
            (0.2, 1.3, 2.5, 3.7, 4.9, 6.1),
        ),
        (
            PHASOR_NAME,
            PHASOR_DURATION,
            draw_rotating_phasor,
            (0.0, 1.0, 2.0, 3.0, 4.0, 5.0),
        ),
    )
    for name, duration, draw_frame, samples in jobs:
        video, contact, final = wave.encode(name, duration, draw_frame, samples)
        print(video)
        print(contact)
        print(final)
        print(wave.verify(video))

    draw_diamond_diagram().save(DIAMOND_PATH)
    draw_phasor_sum_diagram().save(PHASOR_SUM_PATH)
    print(DIAMOND_PATH)
    print(PHASOR_SUM_PATH)


if __name__ == "__main__":
    main()
