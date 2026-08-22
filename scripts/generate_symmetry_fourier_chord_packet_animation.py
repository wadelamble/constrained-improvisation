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
AUDIO_SAMPLE_RATE = 48_000

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


CARRIER_FREQUENCIES = (261.6, 329.6, 392.0)
K_PER_HZ = 11.0 * math.pi / CARRIER_FREQUENCIES[0]
CARRIER_WAVENUMBERS = tuple(frequency * K_PER_HZ for frequency in CARRIER_FREQUENCIES)
CARRIER_PHASES = (0.10, 0.75, -0.45)
CARRIER_AMPLITUDES = (1.00, 0.72, 0.52)
MODE_OFFSETS = tuple(range(-11, 12))
MODE_STEP = 0.45
MODE_SIGMA = 3.25
MODE_WEIGHTS = tuple(math.exp(-0.5 * (offset / MODE_SIGMA) ** 2) for offset in MODE_OFFSETS)
MODE_WEIGHT_SUM = sum(MODE_WEIGHTS)


def mode_weight(offset: int) -> float:
    return MODE_WEIGHTS[offset - MODE_OFFSETS[0]]


def audio_expression() -> str:
    """FFmpeg expression for the same three frequency clusters shown on screen."""
    terms: list[str] = []
    mode_hz_step = MODE_STEP / K_PER_HZ
    mode_count = len(MODE_OFFSETS)
    for cluster_index, carrier_frequency in enumerate(CARRIER_FREQUENCIES):
        for mode_index, offset in enumerate(MODE_OFFSETS):
            amplitude = CARRIER_AMPLITUDES[cluster_index] * mode_weight(offset) / MODE_WEIGHT_SUM
            frequency = carrier_frequency + offset * mode_hz_step
            # Schroeder phases keep an equally spaced multisine from turning
            # into an artificial train of synchronized pulses.
            phase = (
                CARRIER_PHASES[cluster_index]
                - math.pi * mode_index * (mode_index - 1) / mode_count
                + 0.37 * cluster_index * mode_index
            )
            terms.append(f"{amplitude:.10f}*sin(2*PI*{frequency:.10f}*t+({phase:.10f}))")
    return "0.75*(" + "+".join(terms) + ")"


def mode_value(q: float, cluster_index: int, offset: int) -> float:
    """One pure traveling mode from one of the three frequency clusters."""
    amplitude = CARRIER_AMPLITUDES[cluster_index] * mode_weight(offset) / MODE_WEIGHT_SUM
    wavenumber = CARRIER_WAVENUMBERS[cluster_index] + offset * MODE_STEP
    return amplitude * math.cos(wavenumber * q + CARRIER_PHASES[cluster_index])


def cluster_value(q: float, cluster_index: int) -> float:
    return sum(mode_value(q, cluster_index, offset) for offset in MODE_OFFSETS)


def chord_value(q: float) -> float:
    # The packet is the direct sum of every pure mode in all three clusters.
    return sum(cluster_value(q, index) for index in range(3)) / sum(CARRIER_AMPLITUDES)


def emergent_envelope(q: float) -> float:
    # The shared frequency spread makes the cluster modes interfere into this
    # envelope. This curve is a guide, not a separately imposed multiplier.
    return abs(
        sum(mode_weight(offset) * math.cos(offset * MODE_STEP * q) for offset in MODE_OFFSETS)
        / MODE_WEIGHT_SUM
    )


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


def draw_wave_trace(
    draw: ImageDraw.ImageDraw,
    center: float,
    baseline: float,
    amplitude: float,
    value_fn,
    color,
    width: int,
    left_clip: float = 128.0,
    right_clip: float = 807.0,
) -> None:
    half_width = 174.0
    points: list[tuple[int, int]] = []
    for index in range(850):
        x = left_clip + (right_clip - left_clip) * index / 849
        q = (x - center) / half_width
        points.append((s(x), s(baseline - amplitude * value_fn(q))))
    draw.line(points, fill=color, width=s(width), joint="curve")


def draw_modes_and_packet(draw: ImageDraw.ImageDraw, center: float) -> None:
    left_clip = 128.0
    right_clip = 807.0
    half_width = 174.0
    mode_baselines = (200.0, 258.0, 316.0)
    mode_colors = (BLUE, GOLD, RED)
    mode_labels = ("near C4", "+ near E4", "+ near G4")
    representative_offsets = (-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10)

    draw_text(draw, (66, 158), "representative modes (11 of 23 per pitch; magnified)", fill=MUTED, font_obj=SMALL)
    for cluster_index, (baseline, color, label) in enumerate(zip(mode_baselines, mode_colors, mode_labels)):
        draw.line((s(left_clip), s(baseline), s(right_clip), s(baseline)), fill=rgba(MUTED, 0.22), width=s(1))
        draw_text(draw, (102, baseline), label, fill=color, font_obj=SMALL, anchor="rm")
        for offset in representative_offsets:
            relative_weight = mode_weight(offset) / mode_weight(0)
            alpha = 0.18 + 0.48 * relative_weight
            draw_wave_trace(
                draw,
                center,
                baseline,
                20.0 * CARRIER_AMPLITUDES[cluster_index] * relative_weight,
                lambda q, index=cluster_index, m=offset: math.cos(
                    (CARRIER_WAVENUMBERS[index] + m * MODE_STEP) * q + CARRIER_PHASES[index]
                ),
                rgba(color, alpha),
                2 if offset == 0 else 1,
                left_clip,
                right_clip,
            )
        draw_wave_trace(
            draw,
            center,
            baseline,
            20.0,
            lambda q, index=cluster_index: cluster_value(q, index),
            color,
            2,
            left_clip,
            right_clip,
        )

    draw.line((s(left_clip), s(347), s(right_clip), s(347)), fill=rgba(MUTED, 0.36), width=s(1))
    draw_text(draw, ((left_clip + right_clip) / 2, 371), "sum of all the modes", fill=MUTED, font_obj=SMALL, anchor="mm")

    packet_baseline = 459.0
    packet_amplitude = 76.0
    draw.line((s(left_clip), s(packet_baseline), s(right_clip), s(packet_baseline)), fill=rgba(MUTED, 0.36), width=s(1))
    draw_text(draw, (102, packet_baseline), "packet", fill=BLUE, font_obj=SMALL, anchor="rm")

    upper: list[tuple[int, int]] = []
    lower: list[tuple[int, int]] = []
    for index in range(850):
        x = left_clip + (right_clip - left_clip) * index / 849
        q = (x - center) / half_width
        env = emergent_envelope(q)
        upper.append((s(x), s(packet_baseline - packet_amplitude * env)))
        lower.append((s(x), s(packet_baseline + packet_amplitude * env)))

    draw.line(upper, fill=rgba(LIGHT_BLUE, 0.65), width=s(2))
    draw.line(lower, fill=rgba(LIGHT_BLUE, 0.65), width=s(2))
    draw_wave_trace(
        draw,
        center,
        packet_baseline,
        packet_amplitude,
        chord_value,
        BLUE,
        3,
        left_clip,
        right_clip,
    )
    draw_arrow(draw, (center - 34, 394), (center + 34, 394), rgba(BLUE, 0.82), width=3)


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
        mode_hz_step = MODE_STEP / K_PER_HZ
        sigma_hz = mode_hz_step * MODE_SIGMA
        spectrum_span = mode_hz_step * 12.0
        points: list[tuple[int, int]] = []
        fill_points: list[tuple[int, int]] = [(s(map_x(freq - spectrum_span)), s(y_base))]
        for index in range(121):
            f = freq - spectrum_span + 2.0 * spectrum_span * index / 120
            mag = gaussian(f, freq, sigma_hz, height)
            x = map_x(f)
            y = y_base - mag * (y_base - y_top) * 0.90
            points.append((s(x), s(y)))
            fill_points.append((s(x), s(y)))
        fill_points.append((s(map_x(freq + spectrum_span)), s(y_base)))
        draw.polygon(fill_points, fill=rgba(color, 0.16))
        for offset in MODE_OFFSETS:
            mode_freq = freq + offset * mode_hz_step
            mode_height = height * mode_weight(offset) / mode_weight(0)
            mode_x = map_x(mode_freq)
            mode_y = y_base - mode_height * (y_base - y_top) * 0.90
            draw.line((s(mode_x), s(y_base), s(mode_x), s(mode_y)), fill=rgba(color, 0.42), width=s(1))
        draw.line(points, fill=color, width=s(3), joint="curve")
        draw_text(draw, (center_x, y_base + 23), note, fill=color, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (center_x, y_base + 44), hz, fill=MUTED, font_obj=TINY, anchor="mm")

    draw_text(draw, (x0 - 18, y_top - 4), "magnitude", fill=MUTED, font_obj=SMALL, anchor="ls")
    draw_text(draw, ((x0 + x1) / 2, y_base + 76), "frequency", fill=MUTED, font_obj=SMALL, anchor="mm")
    draw_text(draw, ((x0 + x1) / 2, 595), "same three clusters", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    draw_text(draw, ((x0 + x1) / 2, 617), "unchanged by translation", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_frame(frame: int) -> Image.Image:
    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    progress = frame / (FRAMES - 1)
    packet_center = 260.0 + 531.0 * progress

    draw_text(draw, (54, 42), "A chord travels; its Fourier composition stays fixed", font_obj=TITLE)

    left_panel = (40, 100, 824, 637)
    right_panel = (842, 100, 1238, 637)
    draw.rounded_rectangle(tuple(s(v) for v in left_panel), radius=s(14), fill=PANEL, outline=FAINT, width=s(2))
    draw.rounded_rectangle(tuple(s(v) for v in right_panel), radius=s(14), fill=PANEL, outline=FAINT, width=s(2))

    draw_text(draw, (66, 128), "Nearby modes sum directly into a packet", font_obj=PANE_TITLE)
    draw_text(draw, (866, 128), "Fourier magnitude: three clusters", font_obj=PANE_TITLE)

    draw_text(draw, (790, 615), "x", fill=MUTED, font_obj=SMALL)
    draw_listener(draw, 749.0, 448.0)
    draw_modes_and_packet(draw, packet_center)
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
        encoded = subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-f",
                "lavfi",
                "-i",
                f"aevalsrc={audio_expression()}:s={AUDIO_SAMPLE_RATE}:d={FRAMES / FPS:.6f}",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ac",
                "2",
                "-af",
                "afade=t=in:st=0:d=0.35,afade=t=out:st=6.4:d=1.6,alimiter=limit=0.92",
                "-shortest",
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if encoded.returncode != 0 and (not video.exists() or video.stat().st_size == 0):
            raise subprocess.CalledProcessError(encoded.returncode, encoded.args)
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
