from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import generate_symmetry_wave_paths_explainer as wave


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-many-slit-paths-phasors-interference"

WIDTH = wave.WIDTH
HEIGHT = wave.HEIGHT
SCALE = wave.SCALE
FPS = wave.FPS
DURATION = 18.5

BG = wave.BG
PANEL = wave.PANEL
INK = wave.INK
MUTED = wave.MUTED
FAINT = wave.FAINT
BLUE = wave.BLUE
GOLD = wave.GOLD
GREEN = wave.GREEN

TITLE = wave.TITLE
SUBTITLE = wave.SUBTITLE
PANE_TITLE = wave.PANE_TITLE
LABEL = wave.LABEL
LABEL_BOLD = wave.LABEL_BOLD
SMALL = wave.SMALL

# Physical diagram coordinates. A and the detector are equally far from the
# aperture plane. The opening spacing is much smaller than the wavelength, so
# the 49 samples behave like a finely divided aperture rather than a grating.
SOURCE_DISTANCE = 4.5
DETECTOR_DISTANCE = 4.5
APERTURE_HALF_HEIGHT = 2.8
DETECTOR_HALF_HEIGHT = 3.2
OPENING_COUNT = 49
WAVELENGTH = 0.50
WAVE_NUMBER = 2.0 * math.pi / WAVELENGTH
OPENING_YS = np.linspace(APERTURE_HALF_HEIGHT, -APERTURE_HALF_HEIGHT, OPENING_COUNT)
SELECTED_B = 0.94

# Animation timing.
INTRO_END = 0.9
BUILD_END = 7.0
CENTER_HOLD_END = 7.9
MOVE_TO_TOP_END = 8.7
SCAN_END = 15.0
SETTLE_END = 16.0

# Panel geometry in output pixels.
ROUTE_PANEL = (35.0, 126.0, 585.0, 620.0)
PHASOR_PANEL = (602.0, 126.0, 1015.0, 620.0)
DETECTOR_PANEL = (1032.0, 126.0, 1245.0, 620.0)

ROUTE_A = (82.0, 379.0)
ROUTE_SCREEN_X = 306.0
ROUTE_DETECTOR_X = 553.0
ROUTE_TOP = 186.0
ROUTE_BOTTOM = 572.0
ROUTE_CENTER_Y = 379.0
ROUTE_Y_SCALE = (ROUTE_BOTTOM - ROUTE_TOP) / (2.0 * DETECTOR_HALF_HEIGHT)

PHASOR_BOUNDS = (625.0, 183.0, 991.0, 555.0)

DETECTOR_BASE_X = 1065.0
DETECTOR_MAX_X = 1218.0
DETECTOR_TOP = 190.0
DETECTOR_BOTTOM = 568.0


@dataclass(frozen=True)
class Contribution:
    opening_y: float
    length: float
    phase: float
    weight: float
    value: complex


def s(value: float) -> int:
    return wave.s(value)


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return wave.rgba(color, alpha)


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def lerp(start: float, end: float, amount: float) -> float:
    return start + (end - start) * amount


def route_y(value: float) -> float:
    return ROUTE_CENTER_Y - ROUTE_Y_SCALE * value


def detector_y(value: float) -> float:
    amount = (DETECTOR_HALF_HEIGHT - value) / (2.0 * DETECTOR_HALF_HEIGHT)
    return DETECTOR_TOP + amount * (DETECTOR_BOTTOM - DETECTOR_TOP)


def stationary_opening_y(b_value: float) -> float:
    return SOURCE_DISTANCE * b_value / (SOURCE_DISTANCE + DETECTOR_DISTANCE)


def reference_length(b_value: float) -> float:
    return math.hypot(SOURCE_DISTANCE + DETECTOR_DISTANCE, b_value)


def build_contributions(b_value: float) -> tuple[Contribution, ...]:
    stationary_y = stationary_opening_y(b_value)
    reference = reference_length(b_value)
    result: list[Contribution] = []
    for opening_y in OPENING_YS:
        first = math.hypot(SOURCE_DISTANCE, float(opening_y))
        second = math.hypot(DETECTOR_DISTANCE, b_value - float(opening_y))
        length = first + second
        phase = WAVE_NUMBER * (length - reference)
        # This geometric-spreading weight makes longer routes visibly, but only
        # moderately, shorter than routes near the stationary opening.
        weight = math.sqrt((SOURCE_DISTANCE * DETECTOR_DISTANCE) / (first * second))
        value = weight * complex(math.cos(phase), math.sin(phase))
        result.append(
            Contribution(
                opening_y=float(opening_y),
                length=length,
                phase=phase,
                weight=weight,
                value=value,
            )
        )
    return tuple(result)


def cumulative_values(contributions: tuple[Contribution, ...]) -> tuple[complex, ...]:
    values = [0j]
    for contribution in contributions:
        values.append(values[-1] + contribution.value)
    return tuple(values)


DETECTOR_B_VALUES = np.linspace(DETECTOR_HALF_HEIGHT, -DETECTOR_HALF_HEIGHT, 193)
DETECTOR_TOTALS = tuple(sum(item.value for item in build_contributions(float(b))) for b in DETECTOR_B_VALUES)
DETECTOR_INTENSITIES = np.asarray([abs(total) ** 2 for total in DETECTOR_TOTALS])
MAX_INTENSITY = float(DETECTOR_INTENSITIES.max())


def make_phasor_mapper():
    values: list[complex] = [0j]
    for b_value in np.linspace(DETECTOR_HALF_HEIGHT, -DETECTOR_HALF_HEIGHT, 101):
        values.extend(cumulative_values(build_contributions(float(b_value))))
    min_x = min(value.real for value in values)
    max_x = max(value.real for value in values)
    min_y = min(value.imag for value in values)
    max_y = max(value.imag for value in values)
    left, top, right, bottom = PHASOR_BOUNDS
    span_x = max(1.0, max_x - min_x)
    span_y = max(1.0, max_y - min_y)
    scale = min((right - left - 24.0) / span_x, (bottom - top - 24.0) / span_y)
    offset_x = (left + right) / 2.0 - scale * (min_x + max_x) / 2.0
    offset_y = (top + bottom) / 2.0 + scale * (min_y + max_y) / 2.0

    def mapper(value: complex) -> tuple[float, float]:
        return offset_x + scale * value.real, offset_y - scale * value.imag

    return mapper


MAP_PHASOR = make_phasor_mapper()


def draw_text(
    draw: ImageDraw.ImageDraw,
    point: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    wave.draw_text(draw, point, text, fill=fill, font_obj=font_obj, anchor=anchor)


def draw_small_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 3,
    head: float = 4.2,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (
        end[0] - head * math.cos(angle - math.pi / 6.0),
        end[1] - head * math.sin(angle - math.pi / 6.0),
    )
    right = (
        end[0] - head * math.cos(angle + math.pi / 6.0),
        end[1] - head * math.sin(angle + math.pi / 6.0),
    )
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


def draw_route(
    draw: ImageDraw.ImageDraw,
    opening_y: float,
    b_value: float,
    color,
    width: int,
) -> None:
    opening = (ROUTE_SCREEN_X, route_y(opening_y))
    target = (ROUTE_DETECTOR_X, route_y(b_value))
    draw.line(
        (s(ROUTE_A[0]), s(ROUTE_A[1]), s(opening[0]), s(opening[1])),
        fill=color,
        width=s(width),
    )
    draw.line(
        (s(opening[0]), s(opening[1]), s(target[0]), s(target[1])),
        fill=color,
        width=s(width),
    )


def draw_aperture_screen(draw: ImageDraw.ImageDraw) -> None:
    draw.line(
        (s(ROUTE_SCREEN_X), s(ROUTE_TOP), s(ROUTE_SCREEN_X), s(ROUTE_BOTTOM)),
        fill=rgba(INK, 0.86),
        width=s(5),
    )
    for opening_y in OPENING_YS:
        point = (ROUTE_SCREEN_X, route_y(float(opening_y)))
        wave.circle(draw, point, 2.45, PANEL)


def draw_detector_line(draw: ImageDraw.ImageDraw, b_value: float) -> None:
    draw.line(
        (s(ROUTE_DETECTOR_X), s(ROUTE_TOP), s(ROUTE_DETECTOR_X), s(ROUTE_BOTTOM)),
        fill=rgba(MUTED, 0.56),
        width=s(2),
    )
    for sample in np.linspace(DETECTOR_HALF_HEIGHT, -DETECTOR_HALF_HEIGHT, 25):
        y = route_y(float(sample))
        wave.circle(draw, (ROUTE_DETECTOR_X, y), 1.7, rgba(MUTED, 0.50))
    target = (ROUTE_DETECTOR_X, route_y(b_value))
    wave.circle(draw, target, 7.5, INK)
    draw_text(draw, (target[0] + 13, target[1]), "B", fill=INK, font_obj=LABEL_BOLD, anchor="lm")


def draw_route_panel(
    draw: ImageDraw.ImageDraw,
    b_value: float,
    visible_count: int,
    active_index: int | None,
    active_fraction: float,
    complete_fan: bool,
) -> None:
    wave.panel(draw, ROUTE_PANEL)
    draw_text(draw, (58, 145), "routes through 49 openings", font_obj=PANE_TITLE)
    draw_text(draw, (58, 172), "one opening C_j selects one route A to C_j to B", fill=MUTED, font_obj=SMALL)

    contributions = build_contributions(b_value)
    count = OPENING_COUNT if complete_fan else visible_count
    for index in range(count):
        alpha = 0.12 if complete_fan else 0.10
        draw_route(draw, contributions[index].opening_y, b_value, rgba(BLUE, alpha), 2)

    draw_aperture_screen(draw)
    draw_detector_line(draw, b_value)

    stationary_index = min(
        range(OPENING_COUNT),
        key=lambda index: abs(contributions[index].opening_y - stationary_opening_y(b_value)),
    )
    if complete_fan:
        draw_route(draw, contributions[stationary_index].opening_y, b_value, rgba(GOLD, 0.92), 4)
        opening = (ROUTE_SCREEN_X, route_y(contributions[stationary_index].opening_y))
        wave.circle(draw, opening, 5.2, GOLD)

    if active_index is not None:
        active = contributions[active_index]
        color = rgba(GOLD, 0.35 + 0.65 * active_fraction)
        draw_route(draw, active.opening_y, b_value, color, 5)
        opening = (ROUTE_SCREEN_X, route_y(active.opening_y))
        wave.circle(draw, opening, 5.7, GOLD)
        draw_text(
            draw,
            (ROUTE_SCREEN_X + 12, opening[1]),
            f"C{active_index + 1}",
            fill=INK,
            font_obj=SMALL,
            anchor="lm",
        )

    wave.circle(draw, ROUTE_A, 7.5, INK)
    draw_text(draw, (ROUTE_A[0] - 12, ROUTE_A[1]), "A", fill=INK, font_obj=LABEL_BOLD, anchor="rm")
    draw_text(draw, (ROUTE_SCREEN_X, 591), "49 openings C_j", fill=INK, font_obj=SMALL, anchor="ma")
    draw_text(draw, (ROUTE_DETECTOR_X, 591), "detector", fill=INK, font_obj=SMALL, anchor="ma")

    if active_index is not None:
        draw_text(
            draw,
            (560, 145),
            f"route {active_index + 1} of 49",
            fill=GOLD,
            font_obj=LABEL_BOLD,
            anchor="ra",
        )
    elif complete_fan:
        draw_text(draw, (560, 145), "all 49 routes", fill=GREEN, font_obj=LABEL_BOLD, anchor="ra")


def draw_phasor_panel(
    draw: ImageDraw.ImageDraw,
    b_value: float,
    visible_count: int,
    active_index: int | None,
    active_fraction: float,
    complete_chain: bool,
) -> complex:
    wave.panel(draw, PHASOR_PANEL)
    draw_text(draw, (625, 145), "complex contributions at B", font_obj=PANE_TITLE)
    draw_text(draw, (625, 172), "top opening to bottom opening", fill=MUTED, font_obj=SMALL)

    contributions = build_contributions(b_value)
    cumulative = cumulative_values(contributions)
    count = OPENING_COUNT if complete_chain else visible_count
    origin = MAP_PHASOR(0j)
    draw.line(
        (s(PHASOR_BOUNDS[0]), s(origin[1]), s(PHASOR_BOUNDS[2]), s(origin[1])),
        fill=rgba(MUTED, 0.20),
        width=s(1),
    )
    draw.line(
        (s(origin[0]), s(PHASOR_BOUNDS[1]), s(origin[0]), s(PHASOR_BOUNDS[3])),
        fill=rgba(MUTED, 0.20),
        width=s(1),
    )
    draw_text(draw, (PHASOR_BOUNDS[2], origin[1] - 6), "Re", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (origin[0] + 7, PHASOR_BOUNDS[1]), "Im", fill=MUTED, font_obj=SMALL)

    for index in range(count):
        start = MAP_PHASOR(cumulative[index])
        finish = MAP_PHASOR(cumulative[index + 1])
        draw_small_arrow(draw, start, finish, rgba(BLUE, 0.76), width=2, head=4.0)

    current = cumulative[count]
    if active_index is not None:
        start_value = cumulative[active_index]
        current = start_value + active_fraction * contributions[active_index].value
        draw_small_arrow(
            draw,
            MAP_PHASOR(start_value),
            MAP_PHASOR(current),
            GOLD,
            width=5,
            head=7.0,
        )

    if count > 0 or active_index is not None:
        wave.dashed_line(draw, origin, MAP_PHASOR(current), rgba(GREEN, 0.34), width=2, dash=6, gap=5)
        wave.circle(draw, MAP_PHASOR(current), 3.5, GOLD if not complete_chain else GREEN)

    if complete_chain:
        total = cumulative[-1]
        wave.draw_arrow(draw, origin, MAP_PHASOR(total), rgba(GREEN, 0.94), 7)
        draw_text(draw, (810, 582), "green arrow = total amplitude", fill=GREEN, font_obj=LABEL_BOLD, anchor="ma")
        return total

    draw_text(draw, (810, 582), "arrow angle = phase, arrow length = route weight", fill=MUTED, font_obj=SMALL, anchor="ma")
    return current


def detector_intensity_x(intensity: float) -> float:
    return DETECTOR_BASE_X + (DETECTOR_MAX_X - DETECTOR_BASE_X) * min(1.0, max(0.0, intensity / MAX_INTENSITY))


def draw_detector_panel(
    draw: ImageDraw.ImageDraw,
    b_value: float,
    current_total: complex,
    reveal_fraction: float,
    scanning: bool,
    final_hold: bool,
    complete: bool,
) -> None:
    wave.panel(draw, DETECTOR_PANEL)
    draw_text(draw, (1052, 145), "intensity at detector", font_obj=PANE_TITLE)
    detector_caption = (
        "intensity = |total amplitude|²"
        if complete
        else "running |partial sum|²"
    )
    draw_text(draw, (1052, 172), detector_caption, fill=MUTED, font_obj=SMALL)
    draw.line(
        (s(DETECTOR_BASE_X), s(DETECTOR_TOP), s(DETECTOR_BASE_X), s(DETECTOR_BOTTOM)),
        fill=rgba(MUTED, 0.50),
        width=s(2),
    )

    if scanning or final_hold:
        visited = len(DETECTOR_B_VALUES) if final_hold else max(1, round(reveal_fraction * len(DETECTOR_B_VALUES)))
        points = []
        for index, (sample_b, intensity) in enumerate(zip(DETECTOR_B_VALUES, DETECTOR_INTENSITIES)):
            y = detector_y(float(sample_b))
            if index < visited:
                amount = float(intensity / MAX_INTENSITY)
                x = detector_intensity_x(float(intensity))
                points.append((s(x), s(y)))
                wave.circle(draw, (DETECTOR_BASE_X, y), 2.2, rgba(GOLD, 0.24 + 0.68 * amount))
            else:
                wave.circle(draw, (DETECTOR_BASE_X, y), 1.15, rgba(MUTED, 0.18))
        if len(points) > 1:
            draw.line(points, fill=rgba(BLUE, 0.82), width=s(3))

        full_total = sum(item.value for item in build_contributions(b_value))
        intensity = abs(full_total) ** 2
    else:
        intensity = abs(current_total) ** 2

    marker = (detector_intensity_x(intensity), detector_y(b_value))
    draw.line(
        (s(DETECTOR_BASE_X), s(marker[1]), s(marker[0]), s(marker[1])),
        fill=rgba(GOLD, 0.68),
        width=s(3),
    )
    wave.circle(draw, marker, 5.5, GREEN if final_hold else GOLD)
    draw_text(draw, (DETECTOR_BASE_X - 7, DETECTOR_TOP), "+", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (DETECTOR_BASE_X - 7, (DETECTOR_TOP + DETECTOR_BOTTOM) / 2.0), "0", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (DETECTOR_BASE_X - 7, DETECTOR_BOTTOM), "-", fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, ((DETECTOR_BASE_X + DETECTOR_MAX_X) / 2.0, 590), "brighter to the right", fill=MUTED, font_obj=SMALL, anchor="ma")


def animation_state(seconds: float):
    if seconds < INTRO_END:
        return 0.0, 0, None, 0.0, False, 0.0, False, "Start at the center point B."
    if seconds < BUILD_END:
        raw = (seconds - INTRO_END) / (BUILD_END - INTRO_END) * OPENING_COUNT
        active = min(OPENING_COUNT - 1, int(math.floor(raw)))
        fraction = raw - math.floor(raw)
        return 0.0, active, active, fraction, False, 0.0, False, "Each route adds one complex arrow in slit order."
    if seconds < CENTER_HOLD_END:
        return 0.0, OPENING_COUNT, None, 0.0, True, 0.0, False, "All 49 arrows give the amplitude at center B."
    if seconds < MOVE_TO_TOP_END:
        amount = smoothstep((seconds - CENTER_HOLD_END) / (MOVE_TO_TOP_END - CENTER_HOLD_END))
        b_value = lerp(0.0, DETECTOR_HALF_HEIGHT, amount)
        return b_value, OPENING_COUNT, None, 0.0, True, 0.0, False, "Now scan B down the detector."
    if seconds < SCAN_END:
        amount = (seconds - MOVE_TO_TOP_END) / (SCAN_END - MOVE_TO_TOP_END)
        b_value = lerp(DETECTOR_HALF_HEIGHT, -DETECTOR_HALF_HEIGHT, amount)
        return b_value, OPENING_COUNT, None, 0.0, True, amount, True, "Every B changes the routes, phases, and intensity."
    if seconds < SETTLE_END:
        amount = smoothstep((seconds - SCAN_END) / (SETTLE_END - SCAN_END))
        b_value = lerp(-DETECTOR_HALF_HEIGHT, SELECTED_B, amount)
        return b_value, OPENING_COUNT, None, 0.0, True, 1.0, True, "The scan leaves the complete interference pattern."
    return SELECTED_B, OPENING_COUNT, None, 0.0, True, 1.0, True, "A bright detector point has a long resultant arrow."


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1.0 / FPS, frame / FPS)
    (
        b_value,
        visible_count,
        active_index,
        active_fraction,
        complete,
        reveal_fraction,
        scanning,
        subtitle,
    ) = animation_state(seconds)
    final_hold = seconds >= SETTLE_END

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 27), "Many openings, one amplitude at each detector point", font_obj=TITLE)
    draw_text(draw, (42, 67), subtitle, fill=GREEN if final_hold else MUTED, font_obj=SUBTITLE)

    draw_route_panel(draw, b_value, visible_count, active_index, active_fraction, complete)
    current_total = draw_phasor_panel(draw, b_value, visible_count, active_index, active_fraction, complete)
    draw_detector_panel(draw, b_value, current_total, reveal_fraction, scanning, final_hold, complete)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video, contact, final = wave.encode(
        NAME,
        DURATION,
        draw_frame,
        (0.4, 3.0, 7.4, 10.2, 14.3, 17.2),
    )
    print(video)
    print(contact)
    print(final)
    print(wave.verify(video))
    print(f"center intensity: {abs(sum(item.value for item in build_contributions(0.0))) ** 2:.6f}")
    print(f"selected intensity: {abs(sum(item.value for item in build_contributions(SELECTED_B))) ** 2:.6f}")
    print(f"maximum sampled intensity: {MAX_INTENSITY:.6f}")


if __name__ == "__main__":
    main()
