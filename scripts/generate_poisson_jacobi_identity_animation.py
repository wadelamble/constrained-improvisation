from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
SCRATCH = OUTPUT_DIR / "_jacobi_frames"

WIDTH = 1280
HEIGHT = 720
FPS = 18
FRAMES = 450


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(30, True)
FONT_PANEL = font(24, True)
FONT_TEXT = font(19)
FONT_SMALL = font(16)
FONT_MATH = font(18)

COLORS = {
    "ink": (32, 33, 36),
    "muted": (93, 93, 93),
    "line": (210, 210, 210),
    "red": (188, 71, 73),
    "green": (42, 157, 143),
    "blue": (76, 120, 168),
    "gold": (220, 170, 70),
}


def smooth(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def lerp(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 5,
) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=color, width=width)
    angle = math.atan2(ey - sy, ex - sx)
    length = 16
    spread = 0.52
    p1 = (ex - length * math.cos(angle - spread), ey - length * math.sin(angle - spread))
    p2 = (ex - length * math.cos(angle + spread), ey - length * math.sin(angle + spread))
    draw.polygon([(ex, ey), p1, p2], fill=color)


def draw_partial_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    vector: tuple[float, float],
    progress: float,
    color: tuple[int, int, int],
    width: int = 5,
) -> tuple[float, float]:
    visible = smooth(progress)
    end = (start[0] + vector[0], start[1] + vector[1])
    if visible <= 0.02:
        return start
    tip = (start[0] + vector[0] * visible, start[1] + vector[1] * visible)
    draw_arrow(draw, start, tip, color, width)
    return end if visible >= 0.995 else tip


def draw_label_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, text_font: ImageFont.ImageFont = FONT_SMALL) -> None:
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=text_font)
    pad_x, pad_y = 10, 7
    rect = (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y)
    draw.rounded_rectangle(rect, radius=7, fill=(255, 255, 255), outline=(208, 208, 208), width=1)
    draw.text((x, y), text, fill=COLORS["ink"], font=text_font)


def grouped_progress(progress: float, first: float, second: float) -> tuple[float, str]:
    pause = 0.08
    first_end = 0.42
    second_start = first_end + pause
    if progress < first_end:
        return first * smooth(progress / first_end), "first"
    if progress < second_start:
        return first, "pause"
    return first + second * smooth((progress - second_start) / (1.0 - second_start)), "second"


def draw_number_line(draw: ImageDraw.ImageDraw, zero_x: float, y: float, color: tuple[int, int, int], label_zero: bool = False) -> None:
    left = zero_x - 360
    right = zero_x + 360
    draw.line((left, y, right, y), fill=color, width=4)
    for index in range(-3, 4):
        x = zero_x + 90 * index
        draw.line((x, y - 15, x, y + 15), fill=color, width=3)
    draw.line((zero_x, y - 26, zero_x, y + 26), fill=color, width=4)
    if label_zero:
        draw.text((zero_x, y + 35), "0", fill=color, font=FONT_SMALL, anchor="ma")


def draw_line_scene(draw: ImageDraw.ImageDraw, progress: float, grouping: str) -> None:
    draw.text((WIDTH / 2, 104), "Number line: operations move the line", fill=COLORS["ink"], font=FONT_PANEL, anchor="ma")
    y = 360
    start_x = 330.0
    a, b, c = 150.0, 185.0, 135.0
    endpoint = start_x + a + b + c

    if grouping == "left":
        offset, stage = grouped_progress(progress, a + b, c)
        formula = "(a+b)+c"
        first_label = "move by a+b"
        second_label = "then move by c"
    else:
        offset, stage = grouped_progress(progress, a, b + c)
        formula = "a+(b+c)"
        first_label = "move by a"
        second_label = "then move by b+c"

    draw_number_line(draw, start_x, y - 105, (218, 218, 218), label_zero=True)
    draw_number_line(draw, endpoint, y + 105, (218, 218, 218), label_zero=True)
    draw.text((start_x, y - 148), "start", fill=COLORS["muted"], font=FONT_SMALL, anchor="ma")
    draw.text((endpoint, y + 148), "endpoint", fill=COLORS["muted"], font=FONT_SMALL, anchor="ma")

    draw_number_line(draw, start_x + offset, y, COLORS["ink"], label_zero=True)
    draw.text((WIDTH / 2, 520), formula, fill=COLORS["ink"], font=FONT_MATH, anchor="ma")

    if stage == "first":
        draw_label_box(draw, (145, 200), first_label, FONT_TEXT)
    elif stage == "pause":
        draw_label_box(draw, (145, 200), first_label + " complete", FONT_TEXT)
    else:
        draw_label_box(draw, (145, 200), second_label, FONT_TEXT)

    if progress > 0.90:
        draw_label_box(draw, (845, 430), "same final placement", FONT_TEXT)


def plane_point(center: tuple[float, float], angle: float, point: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    ca = math.cos(angle)
    sa = math.sin(angle)
    return (center[0] + ca * x - sa * y, center[1] + sa * x + ca * y)


def draw_plane(draw: ImageDraw.ImageDraw, center: tuple[float, float], angle: float, color: tuple[int, int, int], ghost: bool = False) -> None:
    width, height = 430, 260
    fill = (248, 250, 252) if not ghost else (255, 255, 255)
    outline = color if not ghost else (205, 205, 205)
    corners = [
        plane_point(center, angle, (-width / 2, -height / 2)),
        plane_point(center, angle, (width / 2, -height / 2)),
        plane_point(center, angle, (width / 2, height / 2)),
        plane_point(center, angle, (-width / 2, height / 2)),
    ]
    draw.polygon(corners, fill=fill, outline=outline)
    line_color = (226, 226, 226) if not ghost else (232, 232, 232)
    axis_color = color if not ghost else (205, 205, 205)
    for x in [-150, -75, 0, 75, 150]:
        a = plane_point(center, angle, (x, -height / 2))
        b = plane_point(center, angle, (x, height / 2))
        draw.line((*a, *b), fill=line_color, width=1)
    for y in [-90, -45, 0, 45, 90]:
        a = plane_point(center, angle, (-width / 2, y))
        b = plane_point(center, angle, (width / 2, y))
        draw.line((*a, *b), fill=line_color, width=1)
    draw.line((*plane_point(center, angle, (-width / 2, 0)), *plane_point(center, angle, (width / 2, 0))), fill=axis_color, width=3 if not ghost else 2)
    draw.line((*plane_point(center, angle, (0, -height / 2)), *plane_point(center, angle, (0, height / 2))), fill=axis_color, width=3 if not ghost else 2)
    if not ghost:
        draw.ellipse((center[0] - 6, center[1] - 6, center[0] + 6, center[1] + 6), fill=color)


def accumulated_plane_motion(progress: float, steps: list[tuple[tuple[float, float], float]]) -> tuple[tuple[float, float], float, int]:
    x, y, angle = 0.0, 0.0, 0.0
    current_step = 0
    for index, (delta, rotation) in enumerate(steps):
        local = (progress - 0.12 - 0.24 * index) / 0.22
        amount = smooth(local)
        x += delta[0] * amount
        y += delta[1] * amount
        angle += rotation * amount
        if local < 1.0:
            current_step = index
            break
        current_step = index + 1
    return (x, y), angle, min(current_step, len(steps) - 1)


def draw_plane_scene(draw: ImageDraw.ImageDraw, progress: float, cyclic: bool) -> None:
    draw.text((WIDTH / 2, 92), "Bracket operations move the plane", fill=COLORS["ink"], font=FONT_PANEL, anchor="ma")
    base_center = (640.0, 355.0)
    draw_plane(draw, base_center, 0.0, (190, 190, 190), ghost=True)

    if cyclic:
        scene_title = "cyclic Jacobi sum returns the plane"
        formula = "{f,{g,h}} + {g,{h,f}} + {h,{f,g}} = 0"
        steps = [
            ((165.0, -15.0), 0.12),
            ((-82.0, -112.0), -0.21),
            ((-83.0, 127.0), 0.09),
        ]
        labels = ["{f,{g,h}}", "{g,{h,f}}", "{h,{f,g}}"]
    else:
        scene_title = "non-cyclic sum leaves the plane displaced"
        formula = "{f,{g,h}} + {g,{f,h}} + {h,{f,g}} != 0"
        steps = [
            ((165.0, -15.0), 0.12),
            ((82.0, 112.0), 0.21),
            ((-83.0, 127.0), 0.09),
        ]
        labels = ["{f,{g,h}}", "{g,{f,h}}", "{h,{f,g}}"]

    offset, angle, active = accumulated_plane_motion(progress, steps)
    center = (base_center[0] + offset[0], base_center[1] + offset[1])
    draw_plane(draw, center, angle, COLORS["blue"])
    draw_label_box(draw, (72, 135), scene_title, FONT_TEXT)
    draw.text((WIDTH / 2, 628), formula, fill=COLORS["ink"], font=FONT_MATH, anchor="ma")
    draw_label_box(draw, (870, 150), "apply " + labels[active], FONT_SMALL)

    if progress > 0.86:
        if cyclic:
            draw_label_box(draw, (845, 455), "same final placement", FONT_TEXT)
        else:
            draw_label_box(draw, (845, 455), "does not close", FONT_TEXT)


def draw_frame(frame: int) -> Image.Image:
    progress = frame / (FRAMES - 1)
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    draw.text((WIDTH / 2, 34), "Associativity on a line; Jacobi closure in a plane", fill=COLORS["ink"], font=FONT_TITLE, anchor="ma")

    if progress < 0.24:
        draw_line_scene(draw, progress / 0.24, "left")
    elif progress < 0.48:
        draw_line_scene(draw, (progress - 0.24) / 0.24, "right")
    elif progress < 0.72:
        draw_plane_scene(draw, (progress - 0.48) / 0.24, cyclic=False)
    else:
        draw_plane_scene(draw, (progress - 0.72) / 0.28, cyclic=True)

    return image


def make_contact_sheet(frames: list[Path], output: Path) -> None:
    fractions = [0.20, 0.44, 0.70, 0.85, 0.98]
    frame_size = (420, 300)
    sheet = Image.new("RGB", (frame_size[0] * len(fractions), frame_size[1]), "#F4F4F4")
    for index, fraction in enumerate(fractions):
        frame_index = min(len(frames) - 1, max(0, round((len(frames) - 1) * fraction)))
        image = Image.open(frames[frame_index]).convert("RGB")
        image.thumbnail((frame_size[0] - 20, frame_size[1] - 36), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", frame_size, "white")
        canvas.paste(image, ((frame_size[0] - image.width) // 2, 12))
        draw = ImageDraw.Draw(canvas)
        draw.text((14, frame_size[1] - 23), f"{fraction:.0%}", fill=(80, 80, 80), font=FONT_SMALL)
        sheet.paste(canvas, (frame_size[0] * index, 0))
    sheet.save(output)


def encode_video(video: Path) -> None:
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(SCRATCH / "frame_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def make_animation(video: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    try:
        frame_paths: list[Path] = []
        for frame in range(FRAMES):
            path = SCRATCH / f"frame_{frame:04d}.png"
            draw_frame(frame).save(path)
            frame_paths.append(path)
        encode_video(video)
        make_contact_sheet(frame_paths, video.with_name(f"{video.stem}-contact-sheet.png"))
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)


def main() -> None:
    video = OUTPUT_DIR / "differential-poisson-jacobi-identity.mp4"
    make_animation(video)
    print(video)
    print(video.with_name(f"{video.stem}-contact-sheet.png"))


if __name__ == "__main__":
    main()
