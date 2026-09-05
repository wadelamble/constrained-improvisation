from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG_BUNDLED = (
    ROOT
    / ".tools"
    / "micromamba-anim-root"
    / "envs"
    / "anim"
    / "Library"
    / "bin"
    / "ffmpeg.exe"
)

NAME = "symmetry-wave-paths-1-disturbance-not-parcel"
VIDEO_PATH = OUTPUT_DIR / f"{NAME}.mp4"
CONTACT_PATH = OUTPUT_DIR / f"{NAME}-contact-sheet.png"
FINAL_PATH = OUTPUT_DIR / f"{NAME}-final.png"

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
FRAMES = 240

BG = (248, 244, 237)
PAPER = (255, 253, 249)
INK = (46, 46, 45)
MUTED = (105, 98, 89)
FAINT = (205, 196, 183)
VERY_FAINT = (230, 223, 212)
BLUE = (52, 96, 142)
BLUE_LIGHT = (117, 151, 183)
ORANGE = (177, 92, 49)
GOLD = (188, 137, 43)
GREEN = (70, 126, 100)


def find_ffmpeg() -> str:
    if FFMPEG_BUNDLED.exists():
        return str(FFMPEG_BUNDLED)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise FileNotFoundError("ffmpeg was not found")


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


TITLE = font(28, True)
SUBTITLE = font(18)
LABEL = font(16, True)
SMALL = font(14)
TINY = font(12)


def s(value: float) -> int:
    return int(round(value * SCALE))


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def ease(value: float) -> float:
    value = clamp(value)
    return value * value * (3.0 - 2.0 * value)


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], int(round(255 * clamp(alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    *,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = INK,
    font_obj: ImageFont.FreeTypeFont | ImageFont.ImageFont = SMALL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    color: tuple[int, int, int],
    width: float = 3.0,
    head: float = 10.0,
) -> None:
    x0, y0 = start
    x1, y1 = end
    draw.line((s(x0), s(y0), s(x1), s(y1)), fill=color, width=s(width))
    angle = math.atan2(y1 - y0, x1 - x0)
    left = (
        x1 - head * math.cos(angle) + 0.55 * head * math.sin(angle),
        y1 - head * math.sin(angle) - 0.55 * head * math.cos(angle),
    )
    right = (
        x1 - head * math.cos(angle) - 0.55 * head * math.sin(angle),
        y1 - head * math.sin(angle) + 0.55 * head * math.cos(angle),
    )
    draw.polygon(
        [(s(x1), s(y1)), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


def dashed_vertical(
    draw: ImageDraw.ImageDraw,
    x: float,
    y0: float,
    y1: float,
    *,
    color: tuple[int, int, int] | tuple[int, int, int, int],
    width: float = 1.5,
    dash: float = 8.0,
    gap: float = 7.0,
) -> None:
    y = y0
    while y < y1:
        draw.line((s(x), s(y), s(x), s(min(y + dash, y1))), fill=color, width=s(width))
        y += dash + gap


PLOT_LEFT = 78.0
PLOT_RIGHT = 1202.0
REST_Y = 430.0
AMPLITUDE = 112.0
SIGMA = 145.0
WAVELENGTH = 108.0
PACKET_START = -105.0
PACKET_END = 1385.0


def motion_progress(frame: int) -> float:
    normalized = frame / (FRAMES - 1)
    return clamp((normalized - 0.055) / 0.84)


def packet_center(frame: int) -> float:
    progress = motion_progress(frame)
    return PACKET_START + (PACKET_END - PACKET_START) * progress


def displacement(x: float, center: float) -> float:
    offset = x - center
    envelope = math.exp(-0.5 * (offset / SIGMA) ** 2)
    carrier = math.cos(2.0 * math.pi * offset / WAVELENGTH)
    return AMPLITUDE * envelope * carrier


TRACERS = [
    ("A", 350.0, ORANGE),
    ("B", 640.0, GOLD),
    ("C", 930.0, GREEN),
]


def draw_frame(frame: int) -> Image.Image:
    canvas = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(canvas, "RGBA")

    center = packet_center(frame)
    progress = motion_progress(frame)

    # Header: every critical explanatory label stays well above video controls.
    draw_text(
        draw,
        (64, 42),
        "A wave carries a disturbance—not a parcel of matter",
        font_obj=TITLE,
    )
    draw_text(
        draw,
        (64, 83),
        "The wave pattern travels right; each marked material element moves only up and down at its fixed x-position.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    # Compact, directly labelled motion keys.
    draw_arrow(draw, (93, 135), (185, 135), color=BLUE, width=3.0, head=10.0)
    draw_text(draw, (198, 135), "traveling wave pattern", fill=BLUE, font_obj=LABEL, anchor="lm")

    draw.line((s(650), s(119), s(650), s(151)), fill=ORANGE, width=s(2.5))
    draw.polygon([(s(650), s(114)), (s(644), s(124)), (s(656), s(124))], fill=ORANGE)
    draw.polygon([(s(650), s(156)), (s(644), s(146)), (s(656), s(146))], fill=ORANGE)
    draw_text(draw, (670, 135), "local motion of the medium", fill=ORANGE, font_obj=LABEL, anchor="lm")

    # The panel is intentionally quiet: a string, rest positions, and fixed-x tracks.
    draw.rounded_rectangle(
        (s(48), s(178), s(1232), s(590)),
        radius=s(12),
        fill=PAPER,
        outline=FAINT,
        width=s(1),
    )
    draw_text(draw, (72, 204), "same material elements throughout", fill=MUTED, font_obj=SMALL)

    draw.line(
        (s(PLOT_LEFT), s(REST_Y), s(PLOT_RIGHT), s(REST_Y)),
        fill=VERY_FAINT,
        width=s(2),
    )
    draw_text(draw, (1194, REST_Y + 19), "rest position", fill=MUTED, font_obj=TINY, anchor="ra")

    # Persistent vertical tracks make the no-horizontal-transport claim visible.
    for name, x, color in TRACERS:
        dashed_vertical(draw, x, 250, 545, color=rgba(color, 0.55), width=1.4)
        draw.ellipse(
            (s(x - 6), s(REST_Y - 6), s(x + 6), s(REST_Y + 6)),
            fill=PAPER,
            outline=rgba(color, 0.72),
            width=s(2),
        )
        draw_text(draw, (x, 562), f"element {name}: fixed x", fill=color, font_obj=SMALL, anchor="mm")

    # Smooth string profile.
    line_points: list[tuple[int, int]] = []
    profile_samples = 700
    for index in range(profile_samples):
        x = PLOT_LEFT + (PLOT_RIGHT - PLOT_LEFT) * index / (profile_samples - 1)
        y = REST_Y - displacement(x, center)
        line_points.append((s(x), s(y)))
    draw.line(line_points, fill=BLUE, width=s(4), joint="curve")

    # A row of actual medium elements. Every element keeps its own horizontal coordinate.
    bead_count = 73
    tracer_by_x = {round(x, 6): (name, color) for name, x, color in TRACERS}
    bead_xs = [PLOT_LEFT + (PLOT_RIGHT - PLOT_LEFT) * i / (bead_count - 1) for i in range(bead_count)]
    # Force the three tracers into the sampled material row.
    bead_xs.extend(x for _, x, _ in TRACERS)
    bead_xs = sorted(set(round(x, 6) for x in bead_xs))

    for x in bead_xs:
        y = REST_Y - displacement(x, center)
        draw.line((s(x), s(REST_Y), s(x), s(y)), fill=rgba(FAINT, 0.58), width=s(1))
        tracer = tracer_by_x.get(round(x, 6))
        if tracer:
            name, color = tracer
            radius = 10.0
            draw.ellipse(
                (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
                fill=color,
                outline=PAPER,
                width=s(2),
            )
            draw_text(draw, (x, y), name, fill=PAPER, font_obj=TINY, anchor="mm")
        else:
            radius = 3.4
            draw.ellipse(
                (s(x - radius), s(y - radius), s(x + radius), s(y + radius)),
                fill=INK,
                outline=PAPER,
                width=s(1),
            )

    # Track the central crest only while it is comfortably within the panel.
    if PLOT_LEFT + 28 < center < PLOT_RIGHT - 28:
        crest_y = REST_Y - AMPLITUDE
        dashed_vertical(draw, center, 231, crest_y - 15, color=rgba(BLUE, 0.65), width=1.6)
        draw.polygon(
            [
                (s(center), s(crest_y - 5)),
                (s(center - 7), s(crest_y - 17)),
                (s(center + 7), s(crest_y - 17)),
            ],
            fill=BLUE,
        )
        label_x = clamp(center, 155, 1125)
        draw_text(draw, (label_x, 218), "moving crest", fill=BLUE, font_obj=LABEL, anchor="mm")

    # A late hold states what the viewer has just watched without relying on playback controls.
    conclusion_alpha = ease((progress - 0.86) / 0.11)
    if conclusion_alpha > 0.01:
        draw.rounded_rectangle(
            (s(345), s(188), s(935), s(242)),
            radius=s(9),
            fill=rgba(PAPER, 0.94 * conclusion_alpha),
            outline=rgba(FAINT, conclusion_alpha),
            width=s(1),
        )
        draw_text(
            draw,
            (640, 215),
            "The pattern crossed the string; A, B, and C never traveled with it.",
            fill=rgba(INK, conclusion_alpha),
            font_obj=LABEL,
            anchor="mm",
        )

    return canvas.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def encode_video() -> None:
    ffmpeg = find_ffmpeg()
    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(VIDEO_PATH),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None
    for frame in range(FRAMES):
        process.stdin.write(draw_frame(frame).tobytes())
    process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(stderr)


def make_contact_sheet() -> None:
    samples = [8, 56, 92, 128, 164, 222]
    thumb_width = 400
    thumb_height = 225
    label_height = 27
    margin = 18
    columns = 3
    rows = 2
    sheet = Image.new(
        "RGB",
        (
            columns * thumb_width + (columns + 1) * margin,
            rows * (thumb_height + label_height) + (rows + 1) * margin,
        ),
        BG,
    )
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        column = index % columns
        row = index // columns
        x = margin + column * (thumb_width + margin)
        y = margin + row * (thumb_height + label_height + margin)
        thumbnail = draw_frame(frame).resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        sheet.paste(thumbnail, (x, y))
        draw.rectangle((x, y, x + thumb_width, y + thumb_height), outline=FAINT, width=1)
        seconds = frame / FPS
        draw.text((x + 7, y + thumb_height + 5), f"t = {seconds:.1f} s", fill=MUTED, font=TINY)
    sheet.save(CONTACT_PATH)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    encode_video()
    make_contact_sheet()

    # Use the instant at which the packet reaches the third tracer as the reference still.
    representative_frame = 154
    draw_frame(representative_frame).save(FINAL_PATH)

    print(VIDEO_PATH)
    print(CONTACT_PATH)
    print(FINAL_PATH)


if __name__ == "__main__":
    main()
