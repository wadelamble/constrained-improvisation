from pathlib import Path
import math

from PIL import Image, ImageDraw

import generate_symmetry_wave_paths_explainer as wave


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams" / "symmetry-ray-versus-candidate-path.png"


def polyline(draw, points, fill, width=3):
    draw.line([(wave.s(x), wave.s(y)) for x, y in points], fill=fill, width=wave.s(width), joint="curve")


def main():
    image = Image.new("RGB", (wave.WIDTH * wave.SCALE, wave.HEIGHT * wave.SCALE), wave.BG)
    draw = ImageDraw.Draw(image, "RGBA")

    wave.draw_text(draw, (42, 30), "Two different meanings of “path”", font_obj=wave.TITLE)
    wave.draw_text(
        draw,
        (42, 72),
        "The ray belongs to the wave picture. Candidate paths belong to the sum used to recover that wave.",
        fill=wave.MUTED,
        font_obj=wave.SUBTITLE,
    )
    wave.panel(draw, (35, 112, 615, 650))
    wave.panel(draw, (640, 112, 1245, 650))

    # Left: circular equal-phase fronts and their normal ray.
    wave.draw_text(draw, (325, 140), "a ray in a wave", font_obj=wave.PANE_TITLE, anchor="ma")
    source = (125.0, 380.0)
    wave.circle(draw, source, 8, wave.INK)
    wave.draw_text(draw, (source[0], source[1] + 28), "source", font_obj=wave.SMALL, anchor="ma")
    for radius in (85.0, 155.0, 225.0, 295.0, 365.0):
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer, "RGBA")
        ld.ellipse(
            (
                wave.s(source[0] - radius),
                wave.s(source[1] - radius),
                wave.s(source[0] + radius),
                wave.s(source[1] + radius),
            ),
            outline=wave.rgba(wave.BLUE, 0.42),
            width=wave.s(3),
        )
        wave.composite_clipped(image, layer, (38, 115, 612, 647))
    draw = ImageDraw.Draw(image, "RGBA")
    ray_start = (source[0] + 12, source[1])
    ray_end = (575.0, source[1])
    wave.draw_arrow(draw, ray_start, ray_end, wave.GOLD, 7)
    wave.draw_text(draw, (510, 352), "ray", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (330, 585), "equal-phase fronts", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="ma")
    # Right-angle marks emphasize normality.
    for x in (source[0] + 155.0, source[0] + 295.0):
        draw.line((wave.s(x), wave.s(source[1]), wave.s(x), wave.s(source[1] - 15)), fill=wave.INK, width=wave.s(2))
        draw.line((wave.s(x), wave.s(source[1] - 15), wave.s(x + 15), wave.s(source[1] - 15)), fill=wave.INK, width=wave.s(2))
    wave.draw_text(
        draw,
        (325, 620),
        "Follow the perpendicular direction from front to front.",
        fill=wave.INK,
        font_obj=wave.SMALL,
        anchor="ma",
    )

    # Right: arbitrary candidate curves versus the stationary/ray curve.
    wave.draw_text(draw, (943, 140), "candidate paths in a sum", font_obj=wave.PANE_TITLE, anchor="ma")
    A = (700.0, 380.0)
    B = (1180.0, 380.0)
    wave.circle(draw, A, 8, wave.INK)
    wave.circle(draw, B, 8, wave.INK)
    wave.draw_text(draw, (A[0], A[1] + 28), "A", font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (B[0], B[1] + 28), "B", font_obj=wave.LABEL_BOLD, anchor="ma")
    for x in (800.0, 900.0, 1000.0, 1100.0):
        draw.line((wave.s(x), wave.s(190), wave.s(x), wave.s(565)), fill=wave.rgba(wave.BLUE, 0.28), width=wave.s(3))
    wave.draw_text(draw, (1135, 198), "phase fronts", fill=wave.BLUE, font_obj=wave.SMALL, anchor="ra")

    amplitudes = (-155.0, -92.0, 92.0, 155.0)
    for amplitude in amplitudes:
        pts = []
        for j in range(161):
            u = j / 160
            x = A[0] + u * (B[0] - A[0])
            y = A[1] + amplitude * math.sin(math.pi * u)
            pts.append((x, y))
        polyline(draw, pts, wave.rgba(wave.BLUE, 0.72), 3)
    wave.draw_arrow(draw, (A[0] + 10, A[1]), (B[0] - 10, B[1]), wave.GOLD, 7)
    wave.draw_text(draw, (943, 355), "stationary path → ray", fill=wave.GOLD, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(draw, (943, 555), "the other curves are candidate paths", fill=wave.BLUE, font_obj=wave.LABEL_BOLD, anchor="ma")
    wave.draw_text(
        draw,
        (943, 620),
        "They need not be perpendicular to the phase fronts.",
        fill=wave.INK,
        font_obj=wave.SMALL,
        anchor="ma",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.resize((wave.WIDTH, wave.HEIGHT), Image.Resampling.LANCZOS).save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
