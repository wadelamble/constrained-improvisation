from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _make_contact_sheets import make_contact_sheet


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SCRATCH = OUTPUT_DIR / "_symmetry_triangle_actions_frames"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"

WIDTH = 900
HEIGHT = 620
FPS = 18
MOVE = 42
HOLD = 18

BG = (255, 255, 255)
INK = (10, 10, 10)
REFERENCE = (224, 224, 224)

CENTER = (450.0, 245.0)
RADIUS = 165.0


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_SET = font(30, True)

BASE = {
    "A": (CENTER[0], CENTER[1] - RADIUS),
    "B": (CENTER[0] - RADIUS * math.cos(math.radians(30)), CENTER[1] + RADIUS * 0.5),
    "C": (CENTER[0] + RADIUS * math.cos(math.radians(30)), CENTER[1] + RADIUS * 0.5),
}

ORDER = ["A", "B", "C"]

ACTIONS = [
    ("e", "identity", None),
    ("r", "rotate", 120.0),
    ("r^2", "rotate", 240.0),
    ("s", "flip", "A"),
    ("sr", "flip_rotate", ("A", 120.0)),
    ("sr^2", "flip_rotate", ("A", 240.0)),
]


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def rotate_point(point: tuple[float, float], degrees: float) -> tuple[float, float]:
    theta = math.radians(degrees)
    x = point[0] - CENTER[0]
    y = point[1] - CENTER[1]
    return (
        CENTER[0] + math.cos(theta) * x - math.sin(theta) * y,
        CENTER[1] + math.sin(theta) * x + math.cos(theta) * y,
    )


def fold_point(point: tuple[float, float], axis_label: str, progress: float) -> tuple[float, float]:
    axis_point = BASE[axis_label]
    vx = axis_point[0] - CENTER[0]
    vy = axis_point[1] - CENTER[1]
    length = math.hypot(vx, vy)
    ux = vx / length
    uy = vy / length

    px = point[0] - CENTER[0]
    py = point[1] - CENTER[1]

    along = px * ux + py * uy
    perp_x = px - along * ux
    perp_y = py - along * uy

    # Projection of a 180 degree flip through the page: perpendicular distance
    # collapses to zero halfway through, then reappears on the other side.
    scale = math.cos(math.pi * ease(progress))
    return (
        CENTER[0] + along * ux + scale * perp_x,
        CENTER[1] + along * uy + scale * perp_y,
    )


def positions_for(
    action_kind: str,
    parameter: float | str | tuple[str, float] | None,
    progress: float,
) -> dict[str, tuple[float, float]]:
    if action_kind == "rotate":
        degrees = float(parameter) * ease(progress)
        return {key: rotate_point(point, degrees) for key, point in BASE.items()}
    if action_kind == "flip":
        return {key: fold_point(point, str(parameter), progress) for key, point in BASE.items()}
    if action_kind == "flip_rotate":
        axis_label, degrees = parameter if isinstance(parameter, tuple) else ("A", 0.0)
        if progress < 0.5:
            phase = progress / 0.5
            return {key: fold_point(point, axis_label, phase) for key, point in BASE.items()}

        phase = (progress - 0.5) / 0.5
        flipped = {key: fold_point(point, axis_label, 1.0) for key, point in BASE.items()}
        return {key: rotate_point(point, degrees * ease(phase)) for key, point in flipped.items()}
    return dict(BASE)


def draw_triangle(
    draw: ImageDraw.ImageDraw,
    positions: dict[str, tuple[float, float]],
    color: tuple[int, int, int],
    width: int,
) -> None:
    points = [positions[key] for key in ORDER]
    draw.line(points + [points[0]], fill=color, width=width, joint="curve")


def set_text(count: int) -> str:
    if count <= 0:
        return ""
    symbols = [symbol for symbol, _, _ in ACTIONS[:count]]
    body = " + ".join(symbols)
    if count == len(ACTIONS):
        return "{" + body + "} = D3"
    return "{" + body


def text_width(draw: ImageDraw.ImageDraw, text: str) -> int:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=FONT_SET)
    return box[2] - box[0]


def draw_set(draw: ImageDraw.ImageDraw, count: int) -> None:
    text = set_text(count)
    if not text:
        return
    x = (WIDTH - text_width(draw, text)) / 2
    draw.text((x, 500), text, fill=INK, font=FONT_SET)


def draw_frame(action_index: int, progress: float, completed_count: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    symbol, kind, parameter = ACTIONS[action_index]
    draw_triangle(draw, BASE, REFERENCE, 3)

    if kind == "identity":
        width = int(4 + 8 * math.sin(math.pi * ease(progress)))
        positions = dict(BASE)
    else:
        width = 4
        positions = positions_for(kind, parameter, progress)

    draw_triangle(draw, positions, INK, width)
    draw_set(draw, completed_count)
    return image


def build_frames() -> list[Image.Image]:
    frames: list[Image.Image] = []
    completed = 0
    for index, _action in enumerate(ACTIONS):
        for step in range(MOVE):
            progress = step / (MOVE - 1)
            frames.append(draw_frame(index, progress, completed))
        completed = index + 1
        for _ in range(HOLD):
            frames.append(draw_frame(index, 1.0, completed))
    return frames


def main() -> None:
    frames = build_frames()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir()
    try:
        for index, frame in enumerate(frames):
            frame.save(SCRATCH / f"frame_{index:04d}.png")

        video = OUTPUT_DIR / "symmetry-triangle-actions.mp4"
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
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        sheet = make_contact_sheet(video.name)
        print(video)
        print(sheet)
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)
        contact_scratch = OUTPUT_DIR / "_contact_sheet_frames"
        for path in contact_scratch.glob("symmetry-triangle-actions-*.png"):
            path.unlink()


if __name__ == "__main__":
    main()
