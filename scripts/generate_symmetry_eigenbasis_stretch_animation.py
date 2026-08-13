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
FIRST_ACT_FRAMES = 144
FIRST_HOLD_FRAMES = 18
TRANSITION_FRAMES = 30
SECOND_SETUP_FRAMES = 36
SECOND_MOVE_FRAMES = 72
SECOND_HOLD_FRAMES = 48
STRETCH_PARAMETER = 2.0
FRAMES = (
    FIRST_ACT_FRAMES
    + FIRST_HOLD_FRAMES
    + TRANSITION_FRAMES
    + SECOND_SETUP_FRAMES
    + SECOND_MOVE_FRAMES
    + SECOND_HOLD_FRAMES
)

BG = (255, 252, 246)
INK = (35, 36, 38)
MUTED = (174, 168, 158)
FAINT = (226, 219, 209)
BLUE = (57, 103, 157)
RED = (184, 72, 48)
GOLD = (196, 132, 42)
GREEN = (71, 130, 101)


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


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    origin: tuple[float, float],
    vector: tuple[float, float],
    color: tuple[int, int, int] | tuple[int, int, int, int],
    scale: float,
    width: int = 5,
    head: float = 16,
) -> tuple[float, float]:
    x0, y0 = origin
    x1 = x0 + vector[0] * scale
    y1 = y0 - vector[1] * scale
    draw.line((s(x0), s(y0), s(x1), s(y1)), fill=color, width=s(width))
    angle = math.atan2(y1 - y0, x1 - x0)
    left = (x1 - head * math.cos(angle - math.pi / 7), y1 - head * math.sin(angle - math.pi / 7))
    right = (x1 - head * math.cos(angle + math.pi / 7), y1 - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(x1), s(y1)), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)
    return x1, y1


def draw_basis_grid(draw: ImageDraw.ImageDraw, origin: tuple[float, float], scale: float) -> None:
    ox, oy = origin
    for k in range(-2, 3):
        x = ox + k * scale
        y = oy + k * scale
        draw.line((s(x), s(oy - 2.2 * scale), s(x), s(oy + 2.2 * scale)), fill=rgba(FAINT, 0.75), width=s(1))
        draw.line((s(ox - 2.2 * scale), s(y), s(ox + 2.2 * scale), s(y)), fill=rgba(FAINT, 0.75), width=s(1))
    draw.line((s(ox - 2.35 * scale), s(oy), s(ox + 2.35 * scale), s(oy)), fill=rgba(MUTED, 0.85), width=s(2))
    draw.line((s(ox), s(oy + 2.35 * scale), s(ox), s(oy - 2.35 * scale)), fill=rgba(MUTED, 0.85), width=s(2))


def draw_diagonal_guides(draw: ImageDraw.ImageDraw, origin: tuple[float, float], scale: float) -> None:
    ox, oy = origin
    for sign in [-1, 1]:
        draw.line(
            (
                s(ox - 2.15 * scale),
                s(oy - sign * 2.15 * scale),
                s(ox + 2.15 * scale),
                s(oy + sign * 2.15 * scale),
            ),
            fill=rgba(MUTED, 0.55),
            width=s(2),
        )


def draw_comparison_scene(progress: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    t = ease(progress)

    draw_text(draw, (58, 44), "A stretch looks different in different bases", font_obj=TITLE)

    left_origin = (330, 405)
    right_origin = (930, 405)
    scale = 110
    root2 = math.sqrt(2)

    draw_text(draw, (160, 116), "horizontal / vertical basis", font_obj=LABEL)
    draw_text(draw, (760, 116), "45-degree basis", font_obj=LABEL)

    draw_basis_grid(draw, left_origin, scale)
    draw_basis_grid(draw, right_origin, scale)
    draw_diagonal_guides(draw, right_origin, scale)

    diagonal_entry = 0.5 * (STRETCH_PARAMETER + 1.0 / STRETCH_PARAMETER)
    off_diagonal_entry = 0.5 * (STRETCH_PARAMETER - 1.0 / STRETCH_PARAMETER)
    ex_final = (diagonal_entry, off_diagonal_entry)
    ey_final = (off_diagonal_entry, diagonal_entry)
    ex_now = (lerp(1.0, ex_final[0], t), lerp(0.0, ex_final[1], t))
    ey_now = (lerp(0.0, ey_final[0], t), lerp(1.0, ey_final[1], t))

    draw_arrow(draw, left_origin, ex_now, BLUE, scale)
    draw_arrow(draw, left_origin, ey_now, RED, scale)
    draw_text(draw, (left_origin[0] + ex_now[0] * scale + 24, left_origin[1] - ex_now[1] * scale), "x", fill=BLUE, font_obj=LABEL)
    draw_text(draw, (left_origin[0] + ey_now[0] * scale + 20, left_origin[1] - ey_now[1] * scale - 8), "y", fill=RED, font_obj=LABEL)

    u = (1 / root2, 1 / root2)
    v = (1 / root2, -1 / root2)
    u_now = (
        lerp(u[0], STRETCH_PARAMETER * u[0], t),
        lerp(u[1], STRETCH_PARAMETER * u[1], t),
    )
    v_now = (
        lerp(v[0], v[0] / STRETCH_PARAMETER, t),
        lerp(v[1], v[1] / STRETCH_PARAMETER, t),
    )

    draw_arrow(draw, right_origin, u_now, GREEN, scale)
    draw_arrow(draw, right_origin, v_now, GOLD, scale)
    draw_text(draw, (right_origin[0] + u_now[0] * scale + 18, right_origin[1] - u_now[1] * scale - 8), "u", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (right_origin[0] + v_now[0] * scale + 18, right_origin[1] - v_now[1] * scale + 2), "v", fill=GOLD, font_obj=LABEL)

    # Faint starting vectors.
    draw_arrow(draw, left_origin, (1, 0), rgba(BLUE, 0.22), scale, width=3, head=12)
    draw_arrow(draw, left_origin, (0, 1), rgba(RED, 0.22), scale, width=3, head=12)
    draw_arrow(draw, right_origin, u, rgba(GREEN, 0.22), scale, width=3, head=12)
    draw_arrow(draw, right_origin, v, rgba(GOLD, 0.22), scale, width=3, head=12)

    draw_text(draw, (180, 624), "basis vectors turn into mixtures", fill=(91, 87, 81), font_obj=LABEL)
    draw_text(draw, (800, 624), "basis vectors only scale", fill=(91, 87, 81), font_obj=LABEL)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def draw_matrix(
    draw: ImageDraw.ImageDraw,
    origin: tuple[float, float],
    alpha: float,
) -> None:
    x, y = origin
    color = rgba(INK, alpha)
    muted = rgba((91, 87, 81), alpha)

    draw_text(draw, (x, y + 57), "r =", fill=color, font_obj=LABEL, anchor="lm")
    left = x + 78
    right = x + 260
    top = y
    bottom = y + 132
    tick = 16
    width = 3

    draw.line((s(left), s(top), s(left), s(bottom)), fill=color, width=s(width))
    draw.line((s(left), s(top), s(left + tick), s(top)), fill=color, width=s(width))
    draw.line((s(left), s(bottom), s(left + tick), s(bottom)), fill=color, width=s(width))
    draw.line((s(right), s(top), s(right), s(bottom)), fill=color, width=s(width))
    draw.line((s(right - tick), s(top), s(right), s(top)), fill=color, width=s(width))
    draw.line((s(right - tick), s(bottom), s(right), s(bottom)), fill=color, width=s(width))

    draw_text(draw, (left + 58, top + 35), "s", fill=color, font_obj=LABEL, anchor="mm")
    draw_text(draw, (left + 138, top + 35), "0", fill=color, font_obj=LABEL, anchor="mm")
    draw_text(draw, (left + 58, top + 98), "0", fill=color, font_obj=LABEL, anchor="mm")
    draw_text(draw, (left + 138, top + 98), "1/s", fill=color, font_obj=LABEL, anchor="mm")
    draw_text(draw, (right + 24, y + 57), "r_in", fill=color, font_obj=LABEL, anchor="lm")
    draw_text(draw, (x, bottom + 48), "diagonal matrix: no mixing", fill=muted, font_obj=SMALL)


def draw_combination_scene(progress: float, matrix_alpha: float) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (58, 44), "An arbitrary vector is a sum of eigen-components", font_obj=TITLE)

    origin = (405, 390)
    scale = 155
    root2 = math.sqrt(2)
    u_hat = (1 / root2, 1 / root2)
    v_hat = (1 / root2, -1 / root2)

    draw_diagonal_guides(draw, origin, scale)
    draw.ellipse(
        (s(origin[0] - 4), s(origin[1] - 4), s(origin[0] + 4), s(origin[1] + 4)),
        fill=INK,
    )

    draw_text(draw, (origin[0] + 232, origin[1] - 232), "u", fill=GREEN, font_obj=LABEL)
    draw_text(draw, (origin[0] + 232, origin[1] + 214), "v", fill=GOLD, font_obj=LABEL)

    u_coefficient = lerp(1.0, STRETCH_PARAMETER, progress)
    v_coefficient = lerp(0.75, 0.75 / STRETCH_PARAMETER, progress)

    initial_u = (u_hat[0], u_hat[1])
    initial_v = (0.75 * v_hat[0], 0.75 * v_hat[1])
    initial_u_end = (
        origin[0] + initial_u[0] * scale,
        origin[1] - initial_u[1] * scale,
    )
    initial_end = (
        initial_u_end[0] + initial_v[0] * scale,
        initial_u_end[1] - initial_v[1] * scale,
    )

    current_u = (u_coefficient * u_hat[0], u_coefficient * u_hat[1])
    current_v = (v_coefficient * v_hat[0], v_coefficient * v_hat[1])
    current_u_end = (
        origin[0] + current_u[0] * scale,
        origin[1] - current_u[1] * scale,
    )
    current_end = (
        current_u_end[0] + current_v[0] * scale,
        current_u_end[1] - current_v[1] * scale,
    )

    # Keep only the original vector as a quiet reference; the colored
    # components appear once, head-to-tail, rather than as a parallelogram.
    if progress > 0.001:
        draw_arrow(
            draw,
            origin,
            ((initial_end[0] - origin[0]) / scale, (origin[1] - initial_end[1]) / scale),
            rgba(INK, 0.17),
            scale,
            width=3,
            head=11,
        )
        draw_text(
            draw,
            (initial_end[0] + 18, initial_end[1] + 14),
            "r_in",
            fill=rgba((91, 87, 81), 0.72),
            font_obj=SMALL,
        )

    # The result vector and its two independently changing components.
    draw_arrow(
        draw,
        origin,
        ((current_end[0] - origin[0]) / scale, (origin[1] - current_end[1]) / scale),
        BLUE,
        scale,
        width=5,
        head=16,
    )
    draw_arrow(draw, origin, current_u, GREEN, scale, width=6, head=16)
    draw_arrow(draw, current_u_end, current_v, GOLD, scale, width=6, head=16)

    result_label = "r_in" if progress <= 0.001 else "r"
    draw_text(draw, (current_end[0] + 18, current_end[1] - 12), result_label, fill=BLUE, font_obj=LABEL)
    draw_text(
        draw,
        ((origin[0] + current_u_end[0]) / 2 - 38, (origin[1] + current_u_end[1]) / 2 - 12),
        "u component",
        fill=GREEN,
        font_obj=SMALL,
    )
    draw_text(
        draw,
        ((current_u_end[0] + current_end[0]) / 2 + 14, (current_u_end[1] + current_end[1]) / 2),
        "v component",
        fill=GOLD,
        font_obj=SMALL,
    )

    draw_text(draw, (795, 132), "s > 1: stretch parameter", fill=(91, 87, 81), font_obj=SMALL)
    draw_text(draw, (795, 176), "r_in = u û + v v̂", font_obj=LABEL)
    final_equation_alpha = ease((progress - 0.08) / 0.45)
    if final_equation_alpha > 0.01:
        draw_text(
            draw,
            (795, 228),
            "r = s u û + (1/s) v v̂",
            fill=rgba(INK, final_equation_alpha),
            font_obj=LABEL,
        )
    draw_text(
        draw,
        (795, 276),
        "each coefficient changes independently",
        fill=(91, 87, 81),
        font_obj=SMALL,
    )

    if matrix_alpha > 0:
        draw_matrix(draw, (810, 348), matrix_alpha)

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def draw_frame(frame: int) -> Image.Image:
    first_motion_end = FIRST_ACT_FRAMES
    first_hold_end = first_motion_end + FIRST_HOLD_FRAMES
    transition_end = first_hold_end + TRANSITION_FRAMES
    second_setup_end = transition_end + SECOND_SETUP_FRAMES
    second_move_end = second_setup_end + SECOND_MOVE_FRAMES

    if frame < first_motion_end:
        return draw_comparison_scene(frame / (FIRST_ACT_FRAMES - 1))

    if frame < first_hold_end:
        return draw_comparison_scene(1.0)

    if frame < transition_end:
        blend = ease((frame - first_hold_end) / (TRANSITION_FRAMES - 1))
        return Image.blend(draw_comparison_scene(1.0), draw_combination_scene(0.0, 0.0), blend)

    if frame < second_setup_end:
        return draw_combination_scene(0.0, 0.0)

    if frame < second_move_end:
        progress = ease((frame - second_setup_end) / (SECOND_MOVE_FRAMES - 1))
        return draw_combination_scene(progress, 0.0)

    matrix_alpha = ease((frame - second_move_end) / max(1, SECOND_HOLD_FRAMES // 2))
    return draw_combination_scene(1.0, matrix_alpha)


def make_contact_sheet(name: str) -> Path:
    samples = [0, 72, 143, 210, 272, FRAMES - 1]
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


def render() -> tuple[Path, Path]:
    name = "symmetry-eigenbasis-stretch"
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
        contact = make_contact_sheet(name)
        return video, contact
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact = render()
    print(video)
    print(contact)


if __name__ == "__main__":
    main()
