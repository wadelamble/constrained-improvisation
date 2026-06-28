from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "drafts" / "animations" / "lm-sphere-geodesic-sketch.png"

BG = "#F7F3EC"
PANEL = "#FFFDF8"
INK = "#2F2F2F"
GRID = "#BDB4A7"
FAINT = "#D8D0C5"
ORANGE = "#B85C38"
BLUE = "#3D6FB6"
TEXT = "#4B463F"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def normalize(points: np.ndarray) -> np.ndarray:
    return points / np.linalg.norm(points, axis=1)[:, None]


def slerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    omega = np.arccos(np.clip(np.dot(a, b), -1.0, 1.0))
    return (
        np.sin((1 - t) * omega)[:, None] * a
        + np.sin(t * omega)[:, None] * b
    ) / np.sin(omega)


def surface_path(a: np.ndarray, b: np.ndarray, t: np.ndarray, bump: np.ndarray, amount: float) -> np.ndarray:
    base = slerp(a, b, t)
    shaped = base + amount * np.sin(np.pi * t)[:, None] * bump
    return normalize(shaped)


def wavy_surface_path(
    a: np.ndarray,
    b: np.ndarray,
    t: np.ndarray,
    bump: np.ndarray,
    amount: float,
    wave: np.ndarray,
    wave_amount: float,
    cycles: float,
) -> np.ndarray:
    base = slerp(a, b, t)
    envelope = np.sin(np.pi * t)[:, None]
    ripple = np.sin(cycles * 2 * np.pi * t)[:, None]
    shaped = base + amount * envelope * bump + wave_amount * envelope * ripple * wave
    return normalize(shaped)


def main() -> None:
    scale = 3
    width, height = 1260, 820
    image = Image.new("RGB", (width * scale, height * scale), BG)
    draw = ImageDraw.Draw(image)

    def S(v: float) -> int:
        return int(round(v * scale))

    margin = 58
    draw.rounded_rectangle(
        [S(margin), S(margin), S(width - margin), S(height - margin)],
        radius=S(0),
        fill=PANEL,
        outline="#B9AA98",
        width=S(2),
    )

    cx, cy = width / 2, height / 2 + 20
    radius = 300

    def pt(x: float, z: float) -> tuple[int, int]:
        return S(cx + radius * x), S(cy - radius * z)

    def draw_arc_bbox(xr: float, zr: float, color: str, width_px: float = 2.0) -> None:
        bbox = [
            S(cx - radius * xr),
            S(cy - radius * zr),
            S(cx + radius * xr),
            S(cy + radius * zr),
        ]
        draw.ellipse(bbox, outline=color, width=S(width_px))

    title_font = font(S(28))
    label_font = font(S(21))
    small_font = font(S(19))

    title = "candidate paths on a sphere"
    title_w = draw.textlength(title, font=title_font)
    draw.text((S(cx) - title_w / 2, S(76)), title, fill=INK, font=title_font)

    outline_bbox = [S(cx - radius), S(cy - radius), S(cx + radius), S(cy + radius)]
    draw.ellipse(outline_bbox, outline=INK, width=S(4))
    draw_arc_bbox(1.0, 0.20, GRID, 2.2)
    draw_arc_bbox(0.28, 1.0, GRID, 2.0)
    draw_arc_bbox(0.62, 1.0, FAINT, 1.7)
    draw_arc_bbox(1.0, 0.40, FAINT, 1.7)

    start = np.array([-0.66, 0.70, 0.26])
    end = np.array([0.66, 0.70, 0.26])
    start = start / np.linalg.norm(start)
    end = end / np.linalg.norm(end)
    t = np.linspace(0, 1, 320)

    great = slerp(start, end, t)
    base_x = great[:, 0]
    base_z = great[:, 2]
    envelope = np.sin(np.pi * t)
    high_detour = np.column_stack(
        [
            base_x + 0.090 * envelope * np.sin(2 * np.pi * t),
            base_z + 0.52 * envelope + 0.045 * envelope * np.sin(4 * np.pi * t),
        ]
    )
    nearby_detour = np.column_stack(
        [
            base_x - 0.070 * envelope * np.sin(2 * np.pi * t),
            base_z + 0.28 * envelope - 0.040 * envelope * np.sin(4 * np.pi * t),
        ]
    )
    low_detour = np.column_stack(
        [
            base_x + 0.085 * envelope * np.sin(2 * np.pi * t),
            base_z - 0.42 * envelope + 0.055 * envelope * np.sin(4 * np.pi * t),
        ]
    )
    great = np.column_stack([base_x, base_z])

    def project(points: np.ndarray) -> list[tuple[int, int]]:
        return [pt(float(p[0]), float(p[1])) for p in points]

    for points, color, line_width in [
        (low_detour, GRID, 4.0),
        (nearby_detour, BLUE, 4.2),
        (high_detour, ORANGE, 6.0),
        (great, INK, 6.4),
    ]:
        draw.line(project(points), fill=color, width=S(line_width), joint="curve")

    sx, sy = pt(float(start[0]), float(start[2]))
    ex, ey = pt(float(end[0]), float(end[2]))
    dot_r = S(13)
    for x, y in [(sx, sy), (ex, ey)]:
        draw.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill="white")
        draw.ellipse([x - S(10), y - S(10), x + S(10), y + S(10)], fill=INK)

    draw.text((sx - S(114), sy + S(34)), "fixed start", fill=TEXT, font=small_font)
    draw.text((ex - S(5), ey + S(34)), "fixed end", fill=TEXT, font=small_font)
    draw.text((S(cx + 210), S(cy - 232)), "longer paths", fill=TEXT, font=label_font)
    draw.text((S(cx + 160), S(cy + 132)), "great circle", fill=INK, font=label_font)

    image = image.resize((width, height), Image.Resampling.LANCZOS)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT)


if __name__ == "__main__":
    main()
