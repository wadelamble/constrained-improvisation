from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

import generate_symmetry_wave_paths_explainer as wave


ROOT = Path(__file__).resolve().parents[1]
NAME = "symmetry-wave-paths-4a-wave-crosses-repeated-slices"
DURATION = 12.0
FPS = wave.FPS


def reveal(seconds: float, start: float, end: float) -> float:
    return wave.interval(seconds, start, end)


def clipped_ring(
    image: Image.Image,
    center: tuple[float, float],
    radius: float,
    alpha: float,
    bounds: tuple[float, float, float, float],
) -> None:
    if radius <= 2 or alpha <= 0:
        return
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    cx, cy = center
    draw.ellipse(
        (
            wave.s(cx - radius),
            wave.s(cy - radius),
            wave.s(cx + radius),
            wave.s(cy + radius),
        ),
        outline=wave.rgba(wave.BLUE, alpha),
        width=wave.s(3),
    )
    wave.composite_clipped(image, layer, bounds)


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    image = Image.new("RGBA", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    wave.draw_text(draw, (42, 28), "One continuous wave crosses every imaginary slice", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 70),
        "The slices do nothing to the wave. They mark places where we may describe how it continues.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    wave.panel(draw, (35, 112, 1245, 650))

    bounds = (38, 115, 1242, 647)
    A = (105.0, 375.0)
    B = (1172.0, 375.0)
    slice_xs = (300.0, 480.0, 660.0, 840.0, 1020.0)
    chosen_ys = (350.0, 300.0, 410.0, 335.0, 390.0)

    # A finite train of circular wavefronts expands from A. Once the leading
    # front reaches B, the field remains visible while the bookkeeping overlay
    # is introduced.
    front = min(1.0, reveal(seconds, 0.3, 5.1)) * 1120.0
    spacing = 58.0
    for n in range(21):
        radius = front - n * spacing
        if radius > 4:
            envelope = min(1.0, radius / 90.0)
            clipped_ring(image, A, radius, 0.34 * envelope, bounds)

    draw = ImageDraw.Draw(image, "RGBA")
    wave.circle(draw, A, 9, wave.INK)
    wave.circle(draw, B, 9, wave.INK)
    wave.draw_text(draw, (A[0], A[1] + 31), "A", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (B[0], B[1] + 31), "B", font_obj=wave.LABEL_BOLD, anchor="ma")

    slices = reveal(seconds, 4.9, 6.4)
    if slices > 0:
        for idx, sx in enumerate(slice_xs, start=1):
            wave.dashed_line(draw, (sx, 155), (sx, 590), wave.rgba(wave.GREEN, 0.78 * slices), width=2, dash=8, gap=7)
            wave.draw_text(draw, (sx, 139), f"Σ{idx}", fill=wave.rgba(wave.GREEN, slices), font_obj=wave.LABEL_BOLD, anchor="ma")
            for yy in range(175, 581, 29):
                wave.circle(draw, (sx, float(yy)), 3.2, wave.rgba(wave.GREEN, 0.62 * slices))
        wave.draw_text(
            draw,
            (640, 615),
            "every point on every slice carries part of the wave",
            fill=wave.rgba(wave.GREEN, slices),
            font_obj=wave.LABEL_BOLD,
            anchor="ma",
        )

    select = reveal(seconds, 6.7, 8.0)
    if select > 0:
        selected = [A] + list(zip(slice_xs, chosen_ys)) + [B]
        for p in selected[1:-1]:
            wave.circle(draw, p, 7.0, wave.rgba(wave.GOLD, select))
        for p0, p1 in zip(selected[:-1], selected[1:]):
            wave.dashed_line(draw, p0, p1, wave.rgba(wave.GOLD, 0.94 * select), width=4, dash=13, gap=9)
        wave.draw_text(
            draw,
            (640, 170),
            "choose one point on each slice",
            fill=wave.rgba(wave.GOLD, select),
            font_obj=wave.PANE_TITLE,
            anchor="ma",
        )

    explanation = reveal(seconds, 8.0, 9.2)
    if explanation > 0:
        draw.rounded_rectangle(
            (wave.s(323), wave.s(512), wave.s(957), wave.s(584)),
            radius=wave.s(12),
            fill=wave.rgba(wave.PANEL, 0.94 * explanation),
            outline=wave.rgba(wave.FAINT, 0.8 * explanation),
            width=wave.s(1),
        )
        wave.draw_text(
            draw,
            (640, 535),
            "one connected choice traces one contribution from A to B",
            fill=wave.rgba(wave.INK, explanation),
            font_obj=wave.LABEL_BOLD,
            anchor="ma",
        )
        wave.draw_text(
            draw,
            (640, 562),
            "all other choices remain present in the surrounding wave",
            fill=wave.rgba(wave.MUTED, explanation),
            font_obj=wave.SMALL,
            anchor="ma",
        )

    if seconds >= 9.2:
        wave.draw_text(
            draw,
            (640, 692),
            "Repeat the choice more finely and the connected points approach a continuous path.",
            fill=wave.INK,
            font_obj=wave.FINAL,
            anchor="ms",
        )

    return image.convert("RGB")


if __name__ == "__main__":
    video, contact, final = wave.encode(NAME, DURATION, draw_frame, (0.6, 3.0, 5.4, 6.7, 8.5, 10.7))
    print(video)
    print(contact)
    print(final)
    print(wave.verify(video))
