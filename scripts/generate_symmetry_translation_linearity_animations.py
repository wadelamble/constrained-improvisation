from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 156

BG = (255, 252, 246)
PANEL = (250, 246, 238)
PANEL_EDGE = (224, 216, 204)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (226, 219, 209)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (196, 132, 42)
GREEN = (71, 130, 101)
PURPLE = (116, 91, 155)


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


def s(value: float) -> int:
    return int(round(value * SCALE))


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_panel(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in box), radius=s(14), fill=PANEL, outline=PANEL_EDGE, width=s(2))


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 4,
    head: float = 15,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_number_line(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float], y: float) -> tuple[float, float]:
    x0, x1 = box[0] + 54, box[2] - 54
    draw.line((s(x0), s(y), s(x1), s(y)), fill=MUTED, width=s(3))
    for value in range(0, 29, 5):
        x = number_to_x(value, x0, x1)
        draw.line((s(x), s(y - 9), s(x), s(y + 9)), fill=MUTED, width=s(2))
        draw_text(draw, (x, y + 28), str(value), fill=(110, 105, 98), font_obj=SMALL, anchor="mm")
    return x0, x1


def number_to_x(value: float, x0: float, x1: float) -> float:
    return x0 + (x1 - x0) * value / 28.0


def draw_point(draw: ImageDraw.ImageDraw, x: float, y: float, label: str, color: tuple[int, int, int]) -> None:
    draw.ellipse((s(x - 10), s(y - 10), s(x + 10), s(y + 10)), fill=color)
    draw_text(draw, (x, y - 30), label, fill=color, font_obj=LABEL, anchor="mm")


def phase_parts(frame: int) -> tuple[float, float]:
    t = frame / (FRAMES - 1)
    first = ease((t - 0.18) / 0.26)
    second = ease((t - 0.54) / 0.26)
    return first, second


def draw_point_linearity_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (58, 48), "Point translation is not linear", font_obj=TITLE)
    draw_text(draw, (58, 88), "Use x1=2, x2=3, and a=10", fill=(91, 87, 81), font_obj=LABEL)

    top = (54, 132, 1226, 344)
    bottom = (54, 392, 1226, 604)
    draw_panel(draw, top)
    draw_panel(draw, bottom)
    draw_text(draw, (top[0] + 28, top[1] + 24), "add first, then translate", font_obj=LABEL)
    draw_text(draw, (bottom[0] + 28, bottom[1] + 24), "translate first, then add", font_obj=LABEL)

    first, second = phase_parts(frame)

    y_top = 254
    y_bottom = 514
    x0_top, x1_top = draw_number_line(draw, top, y_top)
    x0_bot, x1_bot = draw_number_line(draw, bottom, y_bottom)

    # Top track: 2 and 3 combine to 5, then 5 moves to 15.
    x2_top = number_to_x(2, x0_top, x1_top)
    x3_top = number_to_x(3, x0_top, x1_top)
    x5_top = number_to_x(5, x0_top, x1_top)
    x15_top = number_to_x(15, x0_top, x1_top)
    if first < 0.98:
        draw_point(draw, lerp(x2_top, x5_top - 12, first), y_top, "2", BLUE)
        draw_point(draw, lerp(x3_top, x5_top + 12, first), y_top, "3", RED)
        draw_text(draw, (x5_top, y_top - 70), "2 + 3 = 5", fill=INK, font_obj=LABEL, anchor="mm")
    else:
        x = lerp(x5_top, x15_top, second)
        draw_point(draw, x, y_top, "5" if second < 0.5 else "15", PURPLE)
        if second > 0.08:
            draw_arrow(draw, (x5_top + 28, y_top - 48), (x15_top - 28, y_top - 48), GOLD, width=4)
            draw_text(draw, ((x5_top + x15_top) / 2, y_top - 80), "+10", fill=GOLD, font_obj=LABEL, anchor="mm")
        if second > 0.92:
            draw_text(draw, (x15_top, y_top + 66), "T10(2+3)=15", fill=PURPLE, font_obj=LABEL, anchor="mm")

    # Bottom track: 2 and 3 move to 12 and 13, then combine as 25.
    x2_bot = number_to_x(2, x0_bot, x1_bot)
    x3_bot = number_to_x(3, x0_bot, x1_bot)
    x12_bot = number_to_x(12, x0_bot, x1_bot)
    x13_bot = number_to_x(13, x0_bot, x1_bot)
    x25_bot = number_to_x(25, x0_bot, x1_bot)
    if second < 0.98:
        draw_point(draw, lerp(x2_bot, x12_bot, first), y_bottom, "2" if first < 0.5 else "12", BLUE)
        draw_point(draw, lerp(x3_bot, x13_bot, first), y_bottom, "3" if first < 0.5 else "13", RED)
        if first > 0.08:
            draw_arrow(draw, (x2_bot + 28, y_bottom - 48), (x12_bot - 28, y_bottom - 48), GOLD, width=4)
            draw_arrow(draw, (x3_bot + 28, y_bottom - 76), (x13_bot - 28, y_bottom - 76), GOLD, width=4)
            draw_text(draw, ((x2_bot + x12_bot) / 2, y_bottom - 83), "+10", fill=GOLD, font_obj=SMALL, anchor="mm")
            draw_text(draw, ((x3_bot + x13_bot) / 2, y_bottom - 111), "+10", fill=GOLD, font_obj=SMALL, anchor="mm")
    else:
        draw_point(draw, x25_bot, y_bottom, "25", PURPLE)
        draw_text(draw, (x25_bot, y_bottom + 66), "T10(2)+T10(3)=25", fill=PURPLE, font_obj=LABEL, anchor="mm")

    if frame > FRAMES * 0.86:
        draw_text(draw, (WIDTH / 2, 666), "15 != 25", fill=RED, font_obj=TITLE, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def f_value(x: float) -> float:
    return 0.92 * math.exp(-((x + 1.15) ** 2) / 0.34)


def g_value(x: float) -> float:
    return 0.62 * math.exp(-((x - 0.62) ** 2) / 0.22)


def graph_point(box: tuple[float, float, float, float], x: float, y: float) -> tuple[float, float]:
    x_min, x_max = -3.2, 4.2
    y_min, y_max = -0.12, 1.35
    px = box[0] + (x - x_min) / (x_max - x_min) * (box[2] - box[0])
    py = box[3] - (y - y_min) / (y_max - y_min) * (box[3] - box[1])
    return px, py


def draw_graph_axes(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    y0 = graph_point(box, 0, 0)[1]
    x0 = graph_point(box, 0, 0)[0]
    draw.line((s(box[0]), s(y0), s(box[2]), s(y0)), fill=MUTED, width=s(2))
    draw.line((s(x0), s(box[1]), s(x0), s(box[3])), fill=rgba(MUTED, 0.55), width=s(2))


def draw_curve(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fn,
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: int = 4,
    x_shift: float = 0.0,
) -> None:
    points = []
    for i in range(260):
        x = -3.2 + 7.4 * i / 259
        y = fn(x - x_shift)
        points.append(tuple(s(v) for v in graph_point(box, x, y)))
    draw.line(points, fill=color, width=s(width))


def sum_fn(x: float) -> float:
    return f_value(x) + g_value(x)


def draw_function_linearity_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (58, 48), "Function translation is linear", font_obj=TITLE)
    draw_text(draw, (58, 88), "Add then slide, or slide then add, the final function is the same", fill=(91, 87, 81), font_obj=LABEL)

    top = (58, 138, 1222, 344)
    bottom = (58, 424, 1222, 630)
    draw_panel(draw, (42, 112, 1238, 372))
    draw_panel(draw, (42, 398, 1238, 658))
    draw_text(draw, (70, 126), "add first, then slide", font_obj=LABEL)
    draw_text(draw, (70, 412), "slide first, then add", font_obj=LABEL)

    first, second = phase_parts(frame)
    shift = 1.35

    draw_graph_axes(draw, top)
    draw_graph_axes(draw, bottom)

    # Top: reveal sum, then slide the sum.
    if first < 0.98:
        draw_curve(draw, top, f_value, rgba(BLUE, 0.72), width=4)
        draw_curve(draw, top, g_value, rgba(RED, 0.72), width=4)
        draw_curve(draw, top, sum_fn, rgba(PURPLE, 0.25 + 0.65 * first), width=5)
        draw_text(draw, (1038, 160), "f + g", fill=PURPLE, font_obj=LABEL)
    else:
        current_shift = shift * second
        draw_curve(draw, top, sum_fn, rgba(PURPLE, 1.0), width=5, x_shift=current_shift)
        draw_arrow(draw, (565, 164), (690, 164), GOLD, width=4)
        draw_text(draw, (626, 136), "slide", fill=GOLD, font_obj=SMALL, anchor="mm")
        if second > 0.88:
            draw_text(draw, (1020, 160), "T_a(f+g)", fill=PURPLE, font_obj=LABEL)

    # Bottom: slide f and g separately, then add.
    current_shift = shift * first
    if second < 0.98:
        draw_curve(draw, bottom, f_value, BLUE, width=4, x_shift=current_shift)
        draw_curve(draw, bottom, g_value, RED, width=4, x_shift=current_shift)
        if first > 0.1:
            draw_arrow(draw, (565, 450), (690, 450), GOLD, width=4)
            draw_text(draw, (626, 422), "slide", fill=GOLD, font_obj=SMALL, anchor="mm")
    else:
        draw_curve(draw, bottom, f_value, rgba(BLUE, 0.35), width=3, x_shift=shift)
        draw_curve(draw, bottom, g_value, rgba(RED, 0.35), width=3, x_shift=shift)
        draw_curve(draw, bottom, sum_fn, PURPLE, width=5, x_shift=shift)
        draw_text(draw, (1010, 446), "T_a f + T_a g", fill=PURPLE, font_obj=LABEL)

    if frame > FRAMES * 0.86:
        draw_text(draw, (WIDTH / 2, 690), "T_a(f+g) = T_a f + T_a g", fill=GREEN, font_obj=TITLE, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str, draw_frame) -> Path:
    samples = [0, 28, 56, 84, 112, 155]
    thumb_w = 400
    thumb_h = 225
    label_h = 28
    margin = 18
    cols = 3
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
        draw.text((x + 8, y + thumb_h + 6), f"{round(frame / (FRAMES - 1) * 100)}%", fill=(96, 92, 86), font=SMALL)
    out = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(out)
    return out


def render(name: str, draw_frame) -> tuple[Path, Path]:
    scratch = OUTPUT_DIR / f"_{name}_frames"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        subprocess.run(
            [
                str(FFMPEG),
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
        contact = make_contact_sheet(name, draw_frame)
        return video, contact
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    for name, drawer in [
        ("symmetry-translation-point-linearity-failure", draw_point_linearity_frame),
        ("symmetry-translation-function-linearity", draw_function_linearity_frame),
    ]:
        video, contact = render(name, drawer)
        print(video)
        print(contact)


if __name__ == "__main__":
    main()
