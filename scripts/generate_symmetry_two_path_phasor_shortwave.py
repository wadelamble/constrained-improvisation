"""Short-wave companion still for the two-path movie.

Retains the original still's source geometry, layout, and palette while using
lambda = 0.5 and the movie's equal contribution magnitudes. A common complex
factor is removed, so both displayed contributions have unit magnitude.
The old shared generator and its assets remain unchanged.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

import generate_symmetry_ccr2_visuals as shared

wave = shared.wave
A, C, D, B = shared.A, shared.C, shared.D, shared.B
L_ACB = math.dist(A, C) + math.dist(C, B)
L_ADB = math.dist(A, D) + math.dist(D, B)
DELTA_LENGTH = L_ADB - L_ACB
WAVELENGTH = 0.5
DELTA_PHASE = 2.0 * math.pi * DELTA_LENGTH / WAVELENGTH
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-double-slit-two-path-phasor-sum-shortwave.png"
world_to_canvas = shared.world_to_canvas
draw_source_screen = shared.draw_source_screen
phasor_endpoint = shared.phasor_endpoint
finish_frame = shared.finish_frame


def draw_phasor_sum_diagram() -> Image.Image:
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.draw_text(draw, (42, 28), "The two path contributions add tip to tail", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 69),
        "Equal magnitudes; the path difference determines their relative phase.",
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
    draw_source_screen(draw, mini_bounds)
    screen_x, _ = world_to_canvas((0.0, 0.0), mini_bounds)
    for y0, y1 in ((mini_bounds[1], c[1] - 8), (c[1] + 8, d[1] - 8), (d[1] + 8, mini_bounds[3])):
        draw.line((wave.s(screen_x), wave.s(y0), wave.s(screen_x), wave.s(y1)), fill=wave.INK, width=wave.s(5))
    for p0, p1, color in ((a, c, wave.BLUE), (c, b, wave.BLUE), (a, d, wave.GOLD), (d, b, wave.GOLD)):
        draw.line((wave.s(p0[0]), wave.s(p0[1]), wave.s(p1[0]), wave.s(p1[1])), fill=color, width=wave.s(4))
    for point, color in ((a, wave.INK), (c, wave.BLUE), (d, wave.GOLD), (b, wave.INK)):
        wave.circle(draw, point, 5.5, color)
    wave.draw_text(draw, (a[0] - 8, a[1] - 15), "A", fill=wave.INK, font_obj=wave.SMALL, anchor="rm")
    wave.draw_text(draw, (c[0] + 9, c[1] - 14), "C", fill=wave.INK, font_obj=wave.SMALL)
    wave.draw_text(draw, (d[0] + 9, d[1] + 3), "D", fill=wave.INK, font_obj=wave.SMALL)
    wave.draw_text(draw, (b[0], b[1] + 22), "B", fill=wave.INK, font_obj=wave.SMALL, anchor="ma")

    wave.draw_text(draw, (272, 473), f"L(ACB) = {L_ACB:.2f}", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 510), f"L(ADB) = {L_ADB:.2f}", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 549), f"Delta L = {DELTA_LENGTH:.2f}", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 587), f"wavelength = {WAVELENGTH:.2f}", fill=wave.MUTED, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (272, 625), f"Delta phi = k Delta L = {DELTA_PHASE:.2f} rad", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")

    wave.draw_text(draw, (890, 142), "complex contributions at B", font_obj=wave.PANE_TITLE, anchor="ma")
    origin = (830.0, 285.0)
    step_acb = 235.0
    step_adb = step_acb
    # A common phase reference places the two contributions at +/- Delta
    # phi / 2. Divide out the common magnitude used by the movie at B.
    phi_acb = -DELTA_PHASE / 2.0
    phi_adb = DELTA_PHASE / 2.0
    first_tip = phasor_endpoint(origin, step_acb, phi_acb)
    final_tip = phasor_endpoint(first_tip, step_adb, phi_adb)
    draw.line((wave.s(610), wave.s(origin[1]), wave.s(1200), wave.s(origin[1])), fill=wave.rgba(wave.MUTED, 0.35), width=wave.s(2))
    wave.circle(draw, origin, 4.0, wave.INK)
    wave.draw_arrow(draw, origin, first_tip, wave.BLUE, 7)
    wave.draw_arrow(draw, first_tip, final_tip, wave.GOLD, 7)
    wave.draw_arrow(draw, origin, final_tip, wave.GREEN, 10)
    wave.circle(draw, first_tip, 4.0, wave.BLUE)
    wave.circle(draw, final_tip, 5.0, wave.GREEN)
    wave.draw_text(draw, (785, 399), "path ACB", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="rm")
    wave.draw_text(draw, (1000, 399), "path ADB", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="lm")
    wave.draw_text(draw, ((origin[0] + final_tip[0]) / 2.0, origin[1] - 31.0), "resultant at B", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="mm")
    wave.draw_text(draw, (890, 550), f"relative phase = {DELTA_PHASE:.2f} rad", fill=wave.INK, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (890, 591), "A common phase rotates every arrow together.", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ma")
    wave.draw_text(draw, (890, 620), "It leaves the relative angle and resultant length unchanged.", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ma")
    return finish_frame(image)


def main() -> None:
    acb = complex(math.cos(-DELTA_PHASE / 2), math.sin(-DELTA_PHASE / 2))
    adb = complex(math.cos(DELTA_PHASE / 2), math.sin(DELTA_PHASE / 2))
    resultant = acb + adb
    actual_phase = math.atan2((adb / acb).imag, (adb / acb).real)
    assert math.isclose(abs(acb), 1.0, abs_tol=1e-12)
    assert math.isclose(abs(adb), 1.0, abs_tol=1e-12)
    assert math.isclose(actual_phase, DELTA_PHASE, abs_tol=1e-12)
    assert math.isclose(resultant.imag, 0.0, abs_tol=1e-12)
    assert math.isclose(abs(resultant), 2 * math.cos(DELTA_PHASE / 2), abs_tol=1e-12)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    draw_phasor_sum_diagram().save(OUTPUT)
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "wavelength": WAVELENGTH,
        "length_acb": L_ACB,
        "length_adb": L_ADB,
        "relative_phase_rad": actual_phase,
        "relative_phase_deg": math.degrees(actual_phase),
        "contribution_magnitudes": [abs(acb), abs(adb)],
        "resultant": [resultant.real, resultant.imag],
        "resultant_magnitude": abs(resultant),
    }, indent=2))


if __name__ == "__main__":
    main()
