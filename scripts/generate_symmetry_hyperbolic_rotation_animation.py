from __future__ import annotations

import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".tools" / "animation-python-packages"))
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 168

BG = (255, 252, 246)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (226, 219, 209)
HYPERBOLA = (64, 91, 104)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (151, 93, 24)
GREEN = (71, 130, 101)
PANEL = (250, 246, 238)
PANEL_EDGE = (224, 216, 204)


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
LABEL = font(18)
SMALL = font(14)
MATH = font(17)


def s(value: float) -> int:
    return int(round(value * SCALE))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
    halo: bool = False,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor,
              stroke_width=s(2) if halo else 0, stroke_fill=BG)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 6,
    head: float = 19,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in box), radius=s(12), fill=PANEL, outline=PANEL_EDGE, width=s(2))


def world_to_screen(cx: float, cy: float, scale: float, x: float, t: float) -> tuple[float, float]:
    return cx + scale * x, cy - scale * t


def hyperbola_point(rapidity: float) -> tuple[float, float]:
    # Top branch of t² − x² = 1.
    return math.sinh(rapidity), math.cosh(rapidity)


def draw_hyperbola(draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float) -> None:
    top: list[tuple[int, int]] = []
    bottom: list[tuple[int, int]] = []
    for i in range(-174, 175):
        x = i / 65
        t = math.sqrt(1 + x * x)
        top.append(tuple(s(v) for v in world_to_screen(cx, cy, scale, x, t)))
        bottom.append(tuple(s(v) for v in world_to_screen(cx, cy, scale, x, -t)))
    draw.line(top, fill=HYPERBOLA, width=s(4))
    draw.line(bottom, fill=FAINT, width=s(3))


def draw_readouts(draw: ImageDraw.ImageDraw, eta: float, interval_a: float, interval_b: float,
                  screen_distance: float, interval_ab: float) -> None:
    draw_panel(draw, (790, 142, 1218, 610))
    draw_text(draw, (820, 165), "Hyperbolic rotation", font_obj=TITLE)
    draw_text(draw, (1186, 184), f"η = {eta:.2f}", font_obj=LABEL, anchor="rm")
    draw_text(draw, (820, 257), "B(η) =", font_obj=MATH, anchor="lm")
    for x, inward in ((909, 8), (1113, -8)):
        bracket = [(x + inward, 219), (x, 219), (x, 295), (x + inward, 295)]
        draw.line([(s(px), s(py)) for px, py in bracket], fill=INK, width=s(2))
    for y, row in ((240, ("cosh η", "sinh η")), (274, ("sinh η", "cosh η"))):
        for x, entry in zip((965, 1056), row):
            draw_text(draw, (x, y), entry, font_obj=MATH, anchor="mm")
    draw_text(draw, (820, 319), f"cosh η = {math.cosh(eta):.2f}", font_obj=LABEL)
    draw_text(draw, (1009, 319), f"sinh η = {math.sinh(eta):.2f}", font_obj=LABEL)
    draw.line((s(820), s(366), s(1187), s(366)), fill=PANEL_EDGE, width=s(1))
    draw_text(draw, (820, 385), "From the origin", font_obj=LABEL)
    draw_text(draw, (820, 418), f"A    t² − x² = {interval_a:.2f}", fill=BLUE, font_obj=MATH)
    draw_text(draw, (1009, 418), f"B    t² − x² = {interval_b:.2f}", fill=RED, font_obj=MATH)
    draw_text(draw, (820, 477), "Between A and B", font_obj=LABEL)
    draw_text(draw, (820, 512), "Ordinary distance", fill=GOLD, font_obj=LABEL)
    draw_text(draw, (1186, 512), f"{screen_distance:.2f}", fill=GOLD, font_obj=LABEL, anchor="ra")
    draw_text(draw, (820, 549), "Interval   (Δt)² − (Δx)²", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (1186, 549), f"{interval_ab:.2f}".replace("-", "−"), fill=GREEN, font_obj=LABEL, anchor="ra")


def draw_frame(frame: int) -> Image.Image:
    phase = frame / (FRAMES - 1)
    eta = 1.28 * ease(phase)
    gap = 0.42

    x1, t1 = hyperbola_point(eta)
    x2, t2 = hyperbola_point(eta + gap)
    inv1 = t1 * t1 - x1 * x1
    inv2 = t2 * t2 - x2 * x2
    interval_ab = (t2 - t1) ** 2 - (x2 - x1) ** 2
    screen_distance = math.hypot(x2 - x1, t2 - t1)

    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)

    draw_text(draw, (64, 58), "A boost preserves the hyperbolic interval", font_obj=TITLE)
    draw_text(draw, (64, 101), "The ordinary distance between A and B changes during a boost.", fill=(91, 87, 81), font_obj=LABEL)

    cx, cy = 420.0, 604.0
    scale = 120.0

    # Axes.
    draw.line((s(cx - 340), s(cy), s(cx + 330), s(cy)), fill=MUTED, width=s(2))
    draw.line((s(cx), s(cy + 84), s(cx), s(cy - 451)), fill=MUTED, width=s(2))
    draw_text(draw, (cx + 348, cy - 8), "x", fill=MUTED, font_obj=SMALL)
    draw_text(draw, (cx + 12, cy - 464), "t", fill=MUTED, font_obj=SMALL)

    # Hyperbola and light-cone guides.
    draw.line((s(cx - 292), s(cy + 292), s(cx + 292), s(cy - 292)), fill=FAINT, width=s(2))
    draw.line((s(cx - 292), s(cy - 292), s(cx + 292), s(cy + 292)), fill=FAINT, width=s(2))
    draw_hyperbola(draw, cx, cy, scale)
    draw_text(draw, (cx - 300, cy - 359), "t² − x² = 1", fill=HYPERBOLA, font_obj=LABEL)

    p0 = (cx, cy)
    p1 = world_to_screen(cx, cy, scale, x1, t1)
    p2 = world_to_screen(cx, cy, scale, x2, t2)

    draw.line((s(p1[0]), s(p1[1]), s(p2[0]), s(p2[1])), fill=GOLD, width=s(3))

    draw_arrow(draw, p0, p1, BLUE, width=6)
    draw_arrow(draw, p0, p2, RED, width=6)
    draw.ellipse((s(p0[0] - 6), s(p0[1] - 6), s(p0[0] + 6), s(p0[1] + 6)), fill=INK)
    draw.ellipse((s(p1[0] - 6), s(p1[1] - 6), s(p1[0] + 6), s(p1[1] + 6)), fill=BLUE)
    draw.ellipse((s(p2[0] - 6), s(p2[1] - 6), s(p2[0] + 6), s(p2[1] + 6)), fill=RED)

    draw_text(draw, (p1[0] - 14, p1[1] - 21), "A", fill=BLUE, anchor="rm", halo=True)
    draw_text(draw, (p2[0] - 14, p2[1] - 21), "B", fill=RED, anchor="rm", halo=True)

    draw_readouts(draw, eta, inv1, inv2, screen_distance, interval_ab)

    image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    samples = [0, 28, 56, 84, 112, 140, 167]
    thumb_w = 365
    thumb_h = 205
    label_h = 28
    margin = 16
    cols = 4
    rows = 2
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        eta = 1.28 * ease(frame / (FRAMES - 1))
        draw.text((x + 8, y + thumb_h + 6), f"eta = {eta:0.2f}", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / "symmetry-hyperbolic-rotation-contact-sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video = OUTPUT_DIR / "symmetry-hyperbolic-rotation.mp4"

    with tempfile.TemporaryDirectory(prefix="boost-frames-") as temporary:
        scratch = Path(temporary)
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")

        subprocess.run(
            [
                imageio_ffmpeg.get_ffmpeg_exe(),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(video)
        print(make_contact_sheet())


if __name__ == "__main__":
    main()
