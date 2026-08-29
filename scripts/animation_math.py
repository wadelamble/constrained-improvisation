from __future__ import annotations

from functools import lru_cache
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

from matplotlib import mathtext, rcParams
from matplotlib.font_manager import FontProperties
from PIL import Image, ImageOps


rcParams["mathtext.fontset"] = "cm"


@lru_cache(maxsize=256)
def _render_math(
    expression: str,
    size: int,
    scale: int,
    color: tuple[int, int, int],
) -> Image.Image:
    buffer = BytesIO()
    mathtext.math_to_image(
        f"${expression}$",
        buffer,
        prop=FontProperties(size=size * scale),
        dpi=72,
        format="png",
        color="#000000",
    )
    buffer.seek(0)
    with Image.open(buffer) as rendered:
        rgba = rendered.convert("RGBA")
        ink_mask = ImageOps.invert(ImageOps.grayscale(rgba))
        colored = Image.new("RGBA", rgba.size, color + (0,))
        colored.putalpha(ink_mask)
        return colored


def paste_math(
    canvas: Image.Image,
    xy: tuple[float, float],
    expression: str,
    *,
    size: int,
    scale: int,
    color: tuple[int, int, int],
    anchor: str = "mm",
    opacity: float = 1.0,
) -> None:
    rendered = _render_math(expression, size, scale, color).copy()
    if opacity < 1.0:
        alpha = rendered.getchannel("A").point(
            lambda value: round(value * max(0.0, min(1.0, opacity)))
        )
        rendered.putalpha(alpha)

    x = round(xy[0] * scale)
    y = round(xy[1] * scale)
    width, height = rendered.size

    horizontal = anchor[0] if anchor else "l"
    vertical = anchor[1] if len(anchor) > 1 else "t"
    if horizontal == "m":
        x -= width // 2
    elif horizontal == "r":
        x -= width
    if vertical == "m":
        y -= height // 2
    elif vertical == "b":
        y -= height

    canvas.alpha_composite(rendered, (x, y))
