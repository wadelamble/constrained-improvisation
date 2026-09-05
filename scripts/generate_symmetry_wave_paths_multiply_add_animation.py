from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

import generate_symmetry_wave_paths_explainer as wave


ROOT = Path(__file__).resolve().parents[1]
NAME = "symmetry-wave-paths-2b-propagate-along-add-across"
DURATION = 11.0
FPS = wave.FPS


def fade(seconds: float, start: float, end: float) -> float:
    return wave.interval(seconds, start, end)


def mix_point(a: tuple[float, float], b: tuple[float, float], q: float) -> tuple[float, float]:
    return a[0] + q * (b[0] - a[0]), a[1] + q * (b[1] - a[1])


def phase_arrow(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    radius: float,
    angle: float,
    length: float,
    color,
    alpha: float,
) -> tuple[float, float]:
    cx, cy = center
    ink = wave.rgba(wave.MUTED, 0.42 * alpha)
    draw.ellipse(
        (
            wave.s(cx - radius),
            wave.s(cy - radius),
            wave.s(cx + radius),
            wave.s(cy + radius),
        ),
        outline=ink,
        width=wave.s(1),
    )
    draw.line(
        (wave.s(cx - radius - 5), wave.s(cy), wave.s(cx + radius + 5), wave.s(cy)),
        fill=ink,
        width=wave.s(1),
    )
    draw.line(
        (wave.s(cx), wave.s(cy - radius - 5), wave.s(cx), wave.s(cy + radius + 5)),
        fill=ink,
        width=wave.s(1),
    )
    end = (cx + length * math.cos(angle), cy - length * math.sin(angle))
    wave.draw_arrow(draw, center, end, wave.rgba(color, alpha), 4)
    wave.circle(draw, center, 3.2, wave.rgba(wave.INK, alpha))
    return end


def segment(
    draw: ImageDraw.ImageDraw,
    p0: tuple[float, float],
    p1: tuple[float, float],
    color,
    alpha: float,
    width: int = 4,
) -> None:
    wave.dashed_line(draw, p0, p1, wave.rgba(color, alpha), width=width, dash=12, gap=8)


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    wave.draw_text(draw, (42, 28), "Follow the waves: propagate along each route, then add at B", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 70),
        "Simplest case: one frequency, identical slits, and no attenuation. Propagation changes phase only.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )

    wave.panel(draw, (35, 112, 420, 675))
    wave.panel(draw, (440, 112, 895, 675))
    wave.panel(draw, (915, 112, 1245, 675))

    wave.draw_text(draw, (228, 136), "the two spatial routes", font_obj=wave.PANE_TITLE, anchor="ma")
    wave.draw_text(draw, (667, 136), "along a route: propagate, then propagate again", font_obj=wave.PANE_TITLE, anchor="ma")
    wave.draw_text(draw, (1080, 136), "across routes: add the finished arrows", font_obj=wave.PANE_TITLE, anchor="ma")

    A = (85.0, 377.5)
    C = (260.0, 235.0)
    D = (260.0, 520.0)
    B = (385.0, 315.0)

    # Both physical slit waves are present throughout. Sequential highlighting
    # below is only a teaching device.
    field_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    field_draw = ImageDraw.Draw(field_layer, "RGBA")
    for source, color in ((C, wave.BLUE), (D, wave.GOLD)):
        for radius in (58.0, 96.0, 134.0):
            wave.forward_arc(field_draw, source, radius, wave.rgba(color, 0.18), 2)
    wave.composite_clipped(image, field_layer, (38, 115, 417, 672))
    draw = ImageDraw.Draw(image, "RGBA")

    # Slit screen and marked points.
    for y0, y1 in ((170, 211), (259, 496), (544, 605)):
        draw.line((wave.s(260), wave.s(y0), wave.s(260), wave.s(y1)), fill=wave.INK, width=wave.s(7))
    for p, color in ((A, wave.INK), (C, wave.BLUE), (D, wave.GOLD), (B, wave.INK)):
        wave.circle(draw, p, 7.5, color)
    wave.draw_text(draw, (A[0], A[1] + 27), "A", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (C[0] + 15, C[1] - 8), "C", fill=wave.BLUE, font_obj=wave.LABEL_BOLD)
    wave.draw_text(draw, (D[0] + 15, D[1] - 8), "D", fill=wave.GOLD, font_obj=wave.LABEL_BOLD)
    wave.draw_text(draw, (B[0], B[1] + 27), "B", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (385, 270), "generic off-axis point", fill=wave.MUTED, font_obj=wave.SMALL, anchor="ra")

    segment(draw, A, C, wave.BLUE, 0.18, width=2)
    segment(draw, C, B, wave.BLUE, 0.18, width=2)
    segment(draw, A, D, wave.GOLD, 0.18, width=2)
    segment(draw, D, B, wave.GOLD, 0.18, width=2)

    upper_1 = fade(seconds, 0.8, 2.0)
    upper_2 = fade(seconds, 2.0, 3.2)
    lower_1 = fade(seconds, 3.2, 4.4)
    lower_2 = fade(seconds, 4.4, 5.6)
    if upper_1 > 0:
        segment(draw, A, mix_point(A, C, upper_1), wave.BLUE, 0.95)
    if upper_2 > 0:
        segment(draw, C, mix_point(C, B, upper_2), wave.BLUE, 0.95)
    if lower_1 > 0:
        segment(draw, A, mix_point(A, D, lower_1), wave.GOLD, 0.95)
    if lower_2 > 0:
        segment(draw, D, mix_point(D, B, lower_2), wave.GOLD, 0.95)
    if seconds >= 5.6:
        wave.draw_text(draw, (225, 625), "both complete waves arrive at B", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="ma")

    # Phases derive from the actual segment lengths in the spatial panel. A
    # common source phase rotates everything together and is chosen only to
    # keep the final arrows visually legible.
    wavelength = 240.0
    k = 2 * math.pi / wavelength
    len_ac = math.dist(A, C)
    len_cb = math.dist(C, B)
    len_ad = math.dist(A, D)
    len_db = math.dist(D, B)
    source_phase = -0.35 - k * (len_ac + len_cb)
    phases_upper = (source_phase, source_phase + k * len_ac, source_phase + k * (len_ac + len_cb))
    phases_lower = (source_phase, source_phase + k * len_ad, source_phase + k * (len_ad + len_db))

    xs = (505.0, 667.0, 829.0)
    upper_y = 255.0
    lower_y = 505.0
    radius = 43.0

    upper_reveals = (fade(seconds, 0.3, 0.9), fade(seconds, 1.4, 2.2), fade(seconds, 2.6, 3.4))
    lower_reveals = (fade(seconds, 2.9, 3.5), fade(seconds, 3.8, 4.6), fade(seconds, 5.0, 5.8))
    upper_lengths = (34.0, 34.0, 34.0)
    lower_lengths = (34.0, 34.0, 34.0)
    upper_labels = ("starting wave at A", "after A → C", "after C → B")
    lower_labels = ("same starting wave", "after A → D", "after D → B")

    for idx, x in enumerate(xs):
        if upper_reveals[idx] > 0:
            phase_arrow(draw, (x, upper_y), radius, phases_upper[idx], upper_lengths[idx], wave.BLUE, upper_reveals[idx])
            wave.draw_text(draw, (x, upper_y + 66), upper_labels[idx], fill=wave.BLUE, font_obj=wave.SMALL, anchor="ma")
        if lower_reveals[idx] > 0:
            phase_arrow(draw, (x, lower_y), radius, phases_lower[idx], lower_lengths[idx], wave.GOLD, lower_reveals[idx])
            wave.draw_text(draw, (x, lower_y + 66), lower_labels[idx], fill=wave.GOLD, font_obj=wave.SMALL, anchor="ma")

    for x0, x1, y, start, end, color in (
        (550, 618, upper_y, 1.4, 2.2, wave.BLUE),
        (712, 780, upper_y, 2.6, 3.4, wave.BLUE),
        (550, 618, lower_y, 3.8, 4.6, wave.GOLD),
        (712, 780, lower_y, 5.0, 5.8, wave.GOLD),
    ):
        q = fade(seconds, start, end)
        if q > 0:
            wave.draw_arrow(draw, (x0, y), mix_point((x0, y), (x1, y), q), wave.rgba(color, q), 2)

    if seconds >= 5.8:
        wave.draw_text(draw, (667, 627), "each row now contains one finished contribution at B", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="ma")

    # Add the two completed endpoint arrows tip to tail.
    add_c = fade(seconds, 6.0, 7.0)
    add_d = fade(seconds, 7.0, 8.1)
    add_sum = fade(seconds, 8.1, 9.1)
    origin = (1000.0, 440.0)
    scale_c = 76.0
    scale_d = 76.0
    vc = (scale_c * math.cos(phases_upper[-1]), -scale_c * math.sin(phases_upper[-1]))
    vd = (scale_d * math.cos(phases_lower[-1]), -scale_d * math.sin(phases_lower[-1]))
    c_tip = (origin[0] + vc[0], origin[1] + vc[1])
    d_tip = (c_tip[0] + vd[0], c_tip[1] + vd[1])

    draw.line((wave.s(958), wave.s(origin[1]), wave.s(1213), wave.s(origin[1])), fill=wave.rgba(wave.MUTED, 0.35), width=wave.s(1))
    draw.line((wave.s(origin[0]), wave.s(320), wave.s(origin[0]), wave.s(565)), fill=wave.rgba(wave.MUTED, 0.35), width=wave.s(1))
    if add_c > 0:
        wave.draw_arrow(draw, origin, mix_point(origin, c_tip, add_c), wave.BLUE, 6)
        wave.draw_text(draw, (1054, 481), "wave through C", fill=wave.BLUE, font_obj=wave.SMALL)
    if add_d > 0:
        wave.draw_arrow(draw, c_tip, mix_point(c_tip, d_tip, add_d), wave.GOLD, 6)
        wave.draw_text(draw, (1115, 370), "wave through D", fill=wave.GOLD, font_obj=wave.SMALL)
    if add_sum > 0:
        wave.draw_arrow(draw, origin, mix_point(origin, d_tip, add_sum), wave.GREEN, 8)
        wave.draw_text(draw, (1080, 592), "the resulting wave at B", fill=wave.GREEN, font_obj=wave.LABEL_BOLD, anchor="ma")

    if seconds >= 9.1:
        wave.draw_text(
            draw,
            (640, 696),
            "Finish each route first. Then superpose the waves that arrived.",
            fill=wave.INK,
            font_obj=wave.FINAL,
            anchor="ms",
        )

    return image.convert("RGB")


if __name__ == "__main__":
    video, contact, final = wave.encode(NAME, DURATION, draw_frame, (0.4, 2.2, 3.6, 5.7, 7.6, 10.2))
    print(video)
    print(contact)
    print(final)
    print(wave.verify(video))
