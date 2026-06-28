from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "drafts" / "animations" / "lm-functional-paths-to-numbers.png"

BG = "#F7F3EC"
PANEL = "#FFFDF8"
INK = "#2F2F2F"
MUTED = "#7E7468"
GRID = "#D8D0C5"
ORANGE = "#B85C38"
BLUE = "#3D6FB6"
TAUPE = "#BDB4A7"
TEXT = "#4B463F"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def main() -> None:
    scale = 3
    width, height = 1280, 520
    image = Image.new("RGB", (width * scale, height * scale), BG)
    draw = ImageDraw.Draw(image)

    def S(value: float) -> int:
        return int(round(value * scale))

    title_font = font(S(28))
    label_font = font(S(22))
    math_font = font(S(26))
    number_font = font(S(25))

    left = (80, 88, 500, 420)
    right = (780, 88, 1200, 420)

    for box in [left, right]:
        draw.rounded_rectangle(
            [S(box[0]), S(box[1]), S(box[2]), S(box[3])],
            radius=S(28),
            fill=PANEL,
            outline="#B9AA98",
            width=S(2),
        )

    title = "a functional maps paths to numbers"
    tw = draw.textlength(title, font=title_font)
    draw.text((S(width / 2) - tw / 2, S(28)), title, fill=INK, font=title_font)

    draw.text((S(242), S(104)), "paths", fill=TEXT, font=label_font)
    draw.text((S(940), S(104)), "numbers", fill=TEXT, font=label_font)

    x0, y0 = 150, 350
    x1, y1 = 435, 155
    t = np.linspace(0, 1, 260)
    base_x = x0 + (x1 - x0) * t
    base_y = y0 + (y1 - y0) * t
    curves = [
        (base_x + 22 * np.sin(np.pi * t), base_y - 72 * np.sin(np.pi * t), ORANGE, 7),
        (base_x - 34 * np.sin(np.pi * t), base_y + 58 * np.sin(np.pi * t), BLUE, 5),
        (base_x + 18 * np.sin(4 * np.pi * t) * np.sin(np.pi * t), base_y, TAUPE, 5),
        (base_x - 10 * np.sin(np.pi * t), base_y + 25 * np.sin(2 * np.pi * t) * np.sin(np.pi * t), INK, 6),
    ]

    for xs, ys, color, line_width in curves:
        points = [(S(float(x)), S(float(y))) for x, y in zip(xs, ys)]
        draw.line(points, fill=color, width=S(line_width), joint="curve")

    for x, y in [(x0, y0), (x1, y1)]:
        draw.ellipse([S(x - 12), S(y - 12), S(x + 12), S(y + 12)], fill="white")
        draw.ellipse([S(x - 9), S(y - 9), S(x + 9), S(y + 9)], fill=INK)

    arrow_y = 254
    draw.line([S(545), S(arrow_y), S(725), S(arrow_y)], fill=MUTED, width=S(5))
    draw.polygon(
        [
            (S(725), S(arrow_y)),
            (S(700), S(arrow_y - 16)),
            (S(700), S(arrow_y + 16)),
        ],
        fill=MUTED,
    )
    arrow_label = "S[γ]"
    lw = draw.textlength(arrow_label, font=math_font)
    draw.text((S(635) - lw / 2, S(205)), arrow_label, fill=INK, font=math_font)

    numbers = [
        ("3.7", 865, 170, ORANGE),
        ("-1.2", 1022, 205, BLUE),
        ("0.0", 900, 305, INK),
        ("5.4", 1080, 328, TAUPE),
        ("2.1", 990, 260, MUTED),
    ]
    for text, x, y, color in numbers:
        draw.text((S(x), S(y)), text, fill=color, font=number_font)

    image = image.resize((width, height), Image.Resampling.LANCZOS)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT)


if __name__ == "__main__":
    main()
