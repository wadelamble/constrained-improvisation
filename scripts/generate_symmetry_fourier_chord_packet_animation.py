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
FRAMES = 192

BG = (255, 252, 246)
PANEL = (252, 248, 240)
INK = (37, 39, 42)
MUTED = (112, 107, 99)
FAINT = (224, 217, 207)
GRID = (232, 226, 217)
BLUE = (51, 91, 133)
LIGHT_BLUE = (112, 153, 190)
RED = (182, 76, 59)
GOLD = (199, 139, 45)
GREEN = (67, 126, 96)


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
PANE_TITLE = font(19, True)
LABEL = font(16)
LABEL_BOLD = font(16, True)
SMALL = font(13)
TINY = font(11)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def packet_envelope(q: float) -> float:
    """Smooth finite envelope; q runs from -1 at the tail to +1 at the front."""
    aq = abs(q)
    if aq >= 1.0:
        return 0.0
    # A shallow superellipse keeps a broad sustain region while rounding the
    # previously near-linear shoulders just enough to avoid a hexagonal look.
    return (1.0 - aq**4) ** 0.32


def chord_value(q: float) -> float:
    # Three pure spatial tones under one common envelope. Frequencies are chosen
    # for visual clarity rather than literal screen-space acoustic wavelengths.
    phase = math.pi * (q + 1.0)
    components = (
        0.48 * math.cos(11.0 * phase + 0.10),
        0.32 * math.cos(14.0 * phase + 0.75),
        0.22 * math.cos(17.0 * phase - 0.45),
    )
    return packet_envelope(q) * sum(components) / 1.02


def draw_listener(draw: ImageDraw.ImageDraw, x: float, baseline: float) -> None:
    # Listener marker and simple profile.
    draw.line((s(x), s(166), s(x), s(552)), fill=rgba(GREEN, 0.32), width=s(2))
    draw.ellipse((s(x - 13), s(baseline + 72), s(x + 17), s(baseline + 110)), outline=GREEN, width=s(3))
    draw.arc((s(x - 4), s(baseline + 83), s(x + 7), s(baseline + 99)), 65, 290, fill=GREEN, width=s(2))
    draw.line((s(x + 1), s(baseline + 109), s(x - 10), s(baseline + 139)), fill=GREEN, width=s(3))
    draw_text(draw, (x, baseline + 158), "listener", fill=GREEN, font_obj=SMALL, anchor="mm")


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float], color, width: int = 3) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = 11
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon([(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))], fill=color)


def draw_packet(draw: ImageDraw.ImageDraw, center: float) -> None:
    baseline = 350.0
    half_width = 174.0
    amplitude = 116.0
    left_clip = 66.0
    right_clip = 807.0

    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    wave: list[tuple[int, int]] = []
    for index in range(850):
        x = left_clip + (right_clip - left_clip) * index / 849
        q = (x - center) / half_width
        env = packet_envelope(q)
        value = chord_value(q)
        upper.append((s(x), s(baseline - amplitude * env)))
        lower.append((s(x), s(baseline + amplitude * env)))
        wave.append((s(x), s(baseline - amplitude * value)))

    draw.line(upper, fill=rgba(LIGHT_BLUE, 0.65), width=s(2))
    draw.line(lower, fill=rgba(LIGHT_BLUE, 0.65), width=s(2))
    draw.line(wave, fill=BLUE, width=s(3), joint="curve")

    # A small motion arrow follows the packet without obscuring it.
    arrow_y = 193
    draw_arrow(draw, (center - 42, arrow_y), (center + 42, arrow_y), rgba(BLUE, 0.82), width=3)
    draw_text(draw, (center, arrow_y - 22), "translation", fill=BLUE, font_obj=SMALL, anchor="mm")


def gaussian(x: float, center: float, sigma: float, height: float) -> float:
    return height * math.exp(-0.5 * ((x - center) / sigma) ** 2)


def draw_spectrum(draw: ImageDraw.ImageDraw) -> None:
    x0, x1 = 878.0, 1198.0
    y_base, y_top = 501.0, 180.0
    f_min, f_max = 220.0, 435.0
    peaks = [
        (261.6, 1.00, BLUE, "C4", "261.6 Hz"),
        (329.6, 0.72, GOLD, "E4", "329.6 Hz"),
        (392.0, 0.52, RED, "G4", "392.0 Hz"),
    ]

    for fraction in (0.25, 0.50, 0.75, 1.00):
        y = y_base - (y_base - y_top) * fraction
        draw.line((s(x0), s(y), s(x1), s(y)), fill=GRID, width=s(1))
    draw.line((s(x0), s(y_base), s(x1), s(y_base)), fill=MUTED, width=s(2))
    draw.line((s(x0), s(y_top), s(x0), s(y_base)), fill=MUTED, width=s(2))

    def map_x(freq: float) -> float:
        return x0 + (freq - f_min) / (f_max - f_min) * (x1 - x0)

    for freq, height, color, note, hz in peaks:
        center_x = map_x(freq)
        sigma_hz = 3.0
        points: list[tuple[int, int]] = []
        fill_points: list[tuple[int, int]] = [(s(map_x(freq - 13)), s(y_base))]
        for index in range(121):
            f = freq - 13.0 + 26.0 * index / 120
            mag = gaussian(f, freq, sigma_hz, height)
            x = map_x(f)
            y = y_base - mag * (y_base - y_top) * 0.90
            points.append((s(x), s(y)))
            fill_points.append((s(x), s(y)))
        fill_points.append((s(map_x(freq + 13)), s(y_base)))
        draw.polygon(fill_points, fill=rgba(color, 0.16))
        draw.line(points, fill=color, width=s(3), joint="curve")
        draw.line((s(center_x), s(y_base), s(center_x), s(y_top + 12)), fill=rgba(color, 0.22), width=s(1))
        draw_text(draw, (center_x, y_base + 23), note, fill=color, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (center_x, y_base + 44), hz, fill=MUTED, font_obj=TINY, anchor="mm")

    draw_text(draw, (x0 - 18, y_top - 4), "magnitude", fill=MUTED, font_obj=SMALL, anchor="ls")
    draw_text(draw, ((x0 + x1) / 2, y_base + 76), "frequency", fill=MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, ((x0 + x1) / 2, 575), "same three peaks", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, ((x0 + x1) / 2, 600), "no frequency mixing", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    progress = smoothstep((frame / (FRAMES - 1) - 0.035) / 0.93)
    packet_center = 260.0 + 531.0 * progress

    draw_text(draw, (54, 42), "A chord travels; its Fourier composition stays fixed", font_obj=TITLE)

    left_panel = (40, 100, 824, 637)
    right_panel = (842, 100, 1238, 637)
    draw.rounded_rectangle(tuple(s(v) for v in left_panel), radius=s(14), fill=PANEL, outline=FAINT, width=s(2))
    draw.rounded_rectangle(tuple(s(v) for v in right_panel), radius=s(14), fill=PANEL, outline=FAINT, width=s(2))

    draw_text(draw, (66, 128), "Sound in space", font_obj=PANE_TITLE)
    draw_text(draw, (866, 128), "One-sided Fourier magnitude", font_obj=PANE_TITLE)

    baseline = 350.0
    draw.line((s(66), s(baseline), s(807), s(baseline)), fill=rgba(MUTED, 0.42), width=s(2))
    draw_text(draw, (790, baseline + 23), "x", fill=MUTED, font_obj=SMALL)
    draw_listener(draw, 749.0, baseline)
    draw_packet(draw, packet_center)
    draw_spectrum(draw)

    draw_text(
        draw,
        (640, 679),
        "Translation changes the phases of the Fourier components, not their magnitudes.",
        fill=INK,
        font_obj=LABEL,
        anchor="mm",
    )

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_sheet(name: str, dense: bool) -> Path:
    samples = list(range(0, FRAMES, 16)) if dense else [0, 38, 76, 114, 152, 191]
    cols = 4 if dense else 3
    thumb_w = 320 if dense else 400
    thumb_h = 180 if dense else 225
    label_h = 23
    margin = 14
    rows = math.ceil(len(samples) / cols)
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(samples):
        col = index % cols
        row = index // cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 5, y + thumb_h + 4), f"frame {frame:03d}", fill=MUTED)
    suffix = "dense-motion-qa" if dense else "contact-sheet"
    out = OUTPUT_DIR / f"{name}-{suffix}.png"
    sheet.save(out)
    return out


def render() -> tuple[Path, Path, Path]:
    name = "symmetry-fourier-three-tone-packet"
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
                "-crf",
                "18",
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
        contact = make_sheet(name, dense=False)
        dense = make_sheet(name, dense=True)
        return video, contact, dense
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    for path in render():
        print(path)


if __name__ == "__main__":
    main()
