from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffprobe.exe"

NAME = "symmetry-ccr-x-k-translations"
WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
TOTAL_SECONDS = 15.0
FRAMES = round(TOTAL_SECONDS * FPS)
CONTROLS_SAFE_TOP = 624
ESSENTIAL_CONTENT_BOTTOM = 600

BG = (255, 252, 246)
PANEL = (252, 248, 240)
INK = (37, 39, 42)
MUTED = (111, 106, 99)
FAINT = (222, 215, 205)
GRID = (233, 227, 218)
BLUE = (51, 91, 133)
GOLD = (198, 138, 45)
GREEN = (65, 126, 95)
PURPLE = (117, 85, 145)


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
SUBTITLE = font(17)
PANEL_TITLE = font(17, True)
LABEL = font(14)
LABEL_BOLD = font(14, True)
SMALL = font(12)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(255 * alpha)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def interval_progress(seconds: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0
    return smoothstep((seconds - start) / (end - start))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(tuple(s(v) for v in bounds), radius=s(13), fill=PANEL, outline=FAINT, width=s(2))


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 3,
    head: float = 9,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - math.pi / 7), end[1] - head * math.sin(angle - math.pi / 7))
    right = (end[0] - head * math.cos(angle + math.pi / 7), end[1] - head * math.sin(angle + math.pi / 7))
    draw.polygon(
        [(s(end[0]), s(end[1])), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


X_MIN = -6.2
X_MAX = 6.2
K_MIN = 0.0
K_MAX = 10.0
SIGMA_X = 1.65
K0 = 4.5
MAX_X_SHIFT = 2.15
MAX_K_SHIFT = 2.15
SAMPLES = 760

X_PANEL = (44, 112, 1236, 365)
K_PANEL = (44, 386, 1236, 600)
X_GRAPH = (92, 168, 1202, 337)
K_GRAPH = (92, 442, 1202, 568)


def graph_x(x: float) -> float:
    left, _, right, _ = X_GRAPH
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def graph_k(k: float) -> float:
    left, _, right, _ = K_GRAPH
    return left + (k - K_MIN) / (K_MAX - K_MIN) * (right - left)


def packet_envelope(x: float, center: float) -> float:
    return math.exp(-0.5 * ((x - center) / SIGMA_X) ** 2)


def packet_real(x: float, center: float, wave_number: float) -> float:
    return packet_envelope(x, center) * math.cos(wave_number * (x - center) + (wave_number - K0) * center)


def spectrum_magnitude(k: float, center: float) -> float:
    sigma_k = 0.58
    return math.exp(-0.5 * ((k - center) / sigma_k) ** 2)


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    x_axis_y = 253.0
    k_axis_y = 548.0
    draw.line((s(X_GRAPH[0]), s(x_axis_y), s(X_GRAPH[2]), s(x_axis_y)), fill=rgba(MUTED, 0.65), width=s(2))
    draw.line((s(K_GRAPH[0]), s(k_axis_y), s(K_GRAPH[2]), s(k_axis_y)), fill=rgba(MUTED, 0.65), width=s(2))
    x_zero = graph_x(0.0)
    k_zero = graph_k(K0)
    draw.line((s(x_zero), s(X_GRAPH[1]), s(x_zero), s(X_GRAPH[3])), fill=rgba(MUTED, 0.25), width=s(1))
    draw.line((s(k_zero), s(K_GRAPH[1]), s(k_zero), s(k_axis_y)), fill=rgba(MUTED, 0.25), width=s(1))
    draw_text(draw, (X_GRAPH[2], x_axis_y + 18), "x", fill=MUTED, font_obj=SMALL, anchor="rm")
    draw_text(draw, (K_GRAPH[2], k_axis_y + 18), "k", fill=MUTED, font_obj=SMALL, anchor="rm")


def packet_points(center: float, wave_number: float) -> list[tuple[int, int]]:
    baseline = 253.0
    scale_y = 66.0
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        points.append((s(graph_x(x)), s(baseline - scale_y * packet_real(x, center, wave_number))))
    return points


def envelope_points(center: float, sign: float) -> list[tuple[int, int]]:
    baseline = 253.0
    scale_y = 66.0
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        x = X_MIN + (X_MAX - X_MIN) * index / (SAMPLES - 1)
        points.append((s(graph_x(x)), s(baseline - sign * scale_y * packet_envelope(x, center))))
    return points


def spectrum_points(center: float) -> list[tuple[int, int]]:
    baseline = 548.0
    scale_y = 82.0
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        k = K_MIN + (K_MAX - K_MIN) * index / (SAMPLES - 1)
        points.append((s(graph_k(k)), s(baseline - scale_y * spectrum_magnitude(k, center))))
    return points


def draw_dashed_polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    color,
    width: int = 2,
    dash: int = 10,
    gap: int = 7,
) -> None:
    for first in range(0, len(points) - 1, dash + gap):
        last = min(len(points), first + dash + 1)
        if last - first >= 2:
            draw.line(points[first:last], fill=color, width=s(width), joint="curve")


def scene_state(seconds: float) -> tuple[float, float, str, str, str]:
    if seconds < 1.6:
        return 0.0, 0.0, "The starting packet", "localized in x", "localized around k₀"
    if seconds < 7.2:
        amount = interval_progress(seconds, 2.0, 6.1)
        return (
            MAX_X_SHIFT * amount,
            0.0,
            "1. Translate in x",
            "the entire packet moves rigidly",
            "the spectral magnitude stays fixed",
        )
    amount = interval_progress(seconds, 8.0, 12.8)
    return (
        MAX_X_SHIFT,
        MAX_K_SHIFT * amount,
        "2. Translate in k",
        "the envelope stays fixed while the carrier changes",
        "the spectral magnitude shifts rigidly",
    )


def draw_frame(frame: int) -> Image.Image:
    seconds = frame / FPS
    x_shift, k_shift, heading, x_caption, k_caption = scene_state(seconds)
    wave_number = K0 + k_shift

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (44, 28), "A wave packet can be translated in x or in k", font_obj=TITLE)
    draw_text(draw, (44, 68), heading, fill=PURPLE, font_obj=SUBTITLE)
    draw_text(draw, (1236, 70), "transformation parameters—not physical time", fill=MUTED, font_obj=SMALL, anchor="rm")

    panel(draw, X_PANEL)
    panel(draw, K_PANEL)
    draw_text(draw, (66, 130), "Position representation", font_obj=PANEL_TITLE)
    draw_text(draw, (1212, 131), x_caption, fill=BLUE, font_obj=LABEL, anchor="ra")
    draw_text(draw, (66, 404), "Wave-number representation", font_obj=PANEL_TITLE)
    draw_text(draw, (1212, 405), k_caption, fill=GREEN, font_obj=LABEL, anchor="ra")
    draw_axes(draw)

    # Each act retains its own starting state as a faint reference.
    if 1.6 <= seconds < 7.2:
        reference_center = 0.0
        draw_dashed_polyline(draw, packet_points(reference_center, K0), rgba(MUTED, 0.38), width=2)
        draw_dashed_polyline(draw, envelope_points(reference_center, 1.0), rgba(MUTED, 0.30), width=1)
        draw_dashed_polyline(draw, envelope_points(reference_center, -1.0), rgba(MUTED, 0.30), width=1)
        draw_dashed_polyline(draw, spectrum_points(K0), rgba(MUTED, 0.38), width=2)
    elif seconds >= 7.2:
        reference_center = MAX_X_SHIFT
        draw_dashed_polyline(draw, packet_points(reference_center, K0), rgba(MUTED, 0.42), width=2)
        draw_dashed_polyline(draw, envelope_points(reference_center, 1.0), rgba(MUTED, 0.28), width=1)
        draw_dashed_polyline(draw, envelope_points(reference_center, -1.0), rgba(MUTED, 0.28), width=1)
        draw_dashed_polyline(draw, spectrum_points(K0), rgba(MUTED, 0.38), width=2)

    draw.line(packet_points(x_shift, wave_number), fill=BLUE, width=s(3), joint="curve")
    draw.line(envelope_points(x_shift, 1.0), fill=rgba(GOLD, 0.82), width=s(2), joint="curve")
    draw.line(envelope_points(x_shift, -1.0), fill=rgba(GOLD, 0.82), width=s(2), joint="curve")
    draw.line(spectrum_points(K0 + k_shift), fill=GREEN, width=s(4), joint="curve")

    draw_text(draw, (108, 326), "blue: Re ψ(x)", fill=BLUE, font_obj=SMALL)
    draw_text(draw, (228, 326), "gold: ±|ψ(x)|", fill=GOLD, font_obj=SMALL)
    draw_text(draw, (108, 590), "green: |ψ̃(k)|", fill=GREEN, font_obj=SMALL)

    if 1.6 <= seconds < 7.2:
        start = graph_x(0.0)
        end = graph_x(x_shift)
        if end - start > 5:
            arrow(draw, (start, 155), (end, 155), PURPLE, width=3, head=9)
        draw_text(draw, ((start + max(end, start + 1)) / 2, 146), "a", fill=PURPLE, font_obj=LABEL_BOLD, anchor="ms")
        draw_text(draw, (1120, 590), "k₀ unchanged", fill=GREEN, font_obj=LABEL_BOLD, anchor="rm")
    elif seconds >= 7.2:
        start = graph_k(K0)
        end = graph_k(K0 + k_shift)
        if end - start > 5:
            arrow(draw, (start, 432), (end, 432), PURPLE, width=3, head=9)
        draw_text(draw, ((start + max(end, start + 1)) / 2, 423), "b", fill=PURPLE, font_obj=LABEL_BOLD, anchor="ms")
        draw_text(draw, (1120, 326), "same center and envelope", fill=GOLD, font_obj=LABEL_BOLD, anchor="rm")

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    samples = [
        (0.8, "starting packet"),
        (3.6, "x shift begins"),
        (6.4, "translated in x"),
        (7.5, "same shifted packet"),
        (10.4, "k shift begins"),
        (14.0, "translated in k"),
    ]
    thumb_w = 400
    thumb_h = 225
    label_h = 26
    margin = 18
    cols = 3
    rows = 2
    sheet = Image.new(
        "RGB",
        (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin),
        BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(samples):
        col = index % cols
        row = index // cols
        x_value = margin + col * (thumb_w + margin)
        y_value = margin + row * (thumb_h + label_h + margin)
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x_value, y_value))
        sheet_draw.text((x_value + 4, y_value + thumb_h + 4), label, fill=MUTED, font=SMALL)
    output = OUTPUT_DIR / f"{NAME}-contact-sheet.png"
    sheet.save(output)
    return output


def verify_video(video: Path) -> str:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "stream=codec_name,pix_fmt,width,height,r_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    report = result.stdout.strip()
    if "codec_name=h264" not in report or "pix_fmt=yuv420p" not in report:
        raise RuntimeError(f"unexpected video encoding:\n{report}")
    return report


def render() -> tuple[Path, Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{NAME}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{NAME}.mp4"
    final_still = OUTPUT_DIR / f"{NAME}-final.png"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        draw_frame(FRAMES - 1).save(final_still)
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
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        contact = make_contact_sheet()
        return video, contact, final_still
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    if ESSENTIAL_CONTENT_BOTTOM >= CONTROLS_SAFE_TOP:
        raise RuntimeError("essential content overlaps the native video-control region")
    video, contact, final_still = render()
    print(video)
    print(contact)
    print(final_still)
    print(verify_video(video))
    print(f"essential_content_bottom={ESSENTIAL_CONTENT_BOTTOM}; controls_safe_top={CONTROLS_SAFE_TOP}")


if __name__ == "__main__":
    main()
