from __future__ import annotations

import math
import shutil
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = (
    ROOT
    / ".tools"
    / "micromamba-anim-root"
    / "envs"
    / "anim"
    / "Library"
    / "bin"
    / "ffmpeg.exe"
)
FFPROBE = (
    ROOT
    / ".tools"
    / "micromamba-anim-root"
    / "envs"
    / "anim"
    / "Library"
    / "bin"
    / "ffprobe.exe"
)

NAME = "symmetry-xk-fourier-amplitudes"
WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
TOTAL_SECONDS = 12.0
FRAMES = round(TOTAL_SECONDS * FPS)
CONTROLS_SAFE_TOP = 624
ESSENTIAL_CONTENT_BOTTOM = 606

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
LIGHT_BLUE = (115, 157, 194)


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


TITLE = font(26, True)
SUBTITLE = font(17)
PANEL_TITLE = font(18, True)
LABEL = font(15)
LABEL_BOLD = font(15, True)
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


def interval_progress(seconds: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0
    return smoothstep((seconds - start) / (end - start))


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(v) for v in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def remove_scratch_tree(path: Path) -> None:
    """Remove generated frames, tolerating brief Windows file-indexer locks."""
    for attempt in range(8):
        try:
            shutil.rmtree(path)
            return
        except FileNotFoundError:
            return
        except PermissionError:
            if attempt == 7:
                raise
            time.sleep(0.20 * (attempt + 1))


def arrow_head(
    draw: ImageDraw.ImageDraw,
    point: tuple[float, float],
    angle: float,
    color,
    size: float = 7.0,
) -> None:
    px, py = point
    left = (
        px - size * math.cos(angle - math.pi / 6),
        py - size * math.sin(angle - math.pi / 6),
    )
    right = (
        px - size * math.cos(angle + math.pi / 6),
        py - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon(
        [(s(px), s(py)), (s(left[0]), s(left[1])), (s(right[0]), s(right[1]))],
        fill=color,
    )


LEFT_PANEL = (44.0, 118.0, 626.0, 606.0)
RIGHT_PANEL = (654.0, 118.0, 1236.0, 606.0)
LEFT_GRAPH = (82.0, 196.0, 598.0, 480.0)
RIGHT_GRAPH = (692.0, 196.0, 1208.0, 480.0)
AXIS_Y = 431.0
GRAPH_MIN = -4.8
GRAPH_MAX = 4.8
SAMPLES = 760
BALANCED_WIDTH = 1.0 / math.sqrt(2.0)
EXTREME_LOG_WIDTH = 2.42
POSITION_X0 = 1.8
CARRIER_K = 4.2


def graph_x(value: float, graph: tuple[float, float, float, float]) -> float:
    left, _, right, _ = graph
    return left + (value - GRAPH_MIN) / (GRAPH_MAX - GRAPH_MIN) * (right - left)


def gaussian_amplitude(value: float, width: float) -> float:
    # width is the standard deviation of the corresponding squared magnitude.
    return math.exp(-(value * value) / (4.0 * width * width))


def gaussian_points(
    graph: tuple[float, float, float, float],
    width: float,
    baseline: float,
    height: float,
    sign: float = 1.0,
    center: float = 0.0,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        value = GRAPH_MIN + (GRAPH_MAX - GRAPH_MIN) * index / (SAMPLES - 1)
        amplitude = gaussian_amplitude(value - center, width)
        points.append((s(graph_x(value, graph)), s(baseline - sign * height * amplitude)))
    return points


def complex_wave_points(
    graph: tuple[float, float, float, float],
    width: float,
    center: float,
    phase_rate: float,
    phase_origin: float,
    baseline: float,
    height: float,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        value = GRAPH_MIN + (GRAPH_MAX - GRAPH_MIN) * index / (SAMPLES - 1)
        amplitude = gaussian_amplitude(value - center, width)
        real_value = amplitude * math.cos(phase_rate * (value - phase_origin))
        points.append((s(graph_x(value, graph)), s(baseline - height * real_value)))
    return points


def plane_wave_points(
    graph: tuple[float, float, float, float],
    phase_rate: float,
    phase_origin: float,
    baseline: float,
    height: float,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(SAMPLES):
        value = GRAPH_MIN + (GRAPH_MAX - GRAPH_MIN) * index / (SAMPLES - 1)
        points.append(
            (
                s(graph_x(value, graph)),
                s(baseline - height * math.cos(phase_rate * (value - phase_origin))),
            )
        )
    return points


def fill_between(
    draw: ImageDraw.ImageDraw,
    upper: list[tuple[int, int]],
    lower: list[tuple[int, int]],
    color,
) -> None:
    draw.polygon(upper + list(reversed(lower)), fill=color)


def fill_to_axis(
    draw: ImageDraw.ImageDraw,
    curve: list[tuple[int, int]],
    graph: tuple[float, float, float, float],
    baseline: float,
    color,
) -> None:
    polygon = curve + [(s(graph[2]), s(baseline)), (s(graph[0]), s(baseline))]
    draw.polygon(polygon, fill=color)


def draw_axis(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    variable: str,
    center_label: str,
) -> None:
    center = graph_x(0.0, graph)
    draw.line(
        (s(graph[0]), s(AXIS_Y), s(graph[2]), s(AXIS_Y)),
        fill=rgba(MUTED, 0.72),
        width=s(2),
    )
    draw.line(
        (s(center), s(graph[1] + 9), s(center), s(AXIS_Y + 14)),
        fill=rgba(MUTED, 0.24),
        width=s(1),
    )
    draw_text(draw, (graph[2], AXIS_Y + 24), variable, fill=MUTED, font_obj=SMALL, anchor="ra")
    draw_text(draw, (center, AXIS_Y + 24), center_label, fill=MUTED, font_obj=SMALL, anchor="ma")


def draw_delta(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    color,
    alpha: float,
    value: float = 0.0,
) -> None:
    center = graph_x(value, graph)
    top = 221.0
    spike_color = rgba(color, alpha)
    draw.line((s(center), s(AXIS_Y), s(center), s(top)), fill=spike_color, width=s(5))
    arrow_head(draw, (center, top), -math.pi / 2, spike_color, size=9.0)


def draw_uniform_wave(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    phase_rate: float,
    phase_origin: float,
    carrier_color,
    alpha: float,
) -> None:
    upper_y = AXIS_Y - 112.0
    lower_y = AXIS_Y + 112.0
    draw.rectangle(
        (s(graph[0]), s(upper_y), s(graph[2]), s(lower_y)),
        fill=rgba(LIGHT_BLUE, 0.08 * alpha),
    )
    draw.line(
        (s(graph[0]), s(upper_y), s(graph[2]), s(upper_y)),
        fill=rgba(GOLD, 0.84 * alpha),
        width=s(3),
    )
    draw.line(
        (s(graph[0]), s(lower_y), s(graph[2]), s(lower_y)),
        fill=rgba(GOLD, 0.84 * alpha),
        width=s(3),
    )
    draw.line(
        plane_wave_points(graph, phase_rate, phase_origin, AXIS_Y, 112.0),
        fill=rgba(carrier_color, 0.96 * alpha),
        width=s(3),
        joint="curve",
    )


def draw_reference_tick(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    value: float,
    label: str,
    color,
) -> None:
    position = graph_x(value, graph)
    draw.line(
        (s(position), s(AXIS_Y - 8), s(position), s(AXIS_Y + 10)),
        fill=rgba(color, 0.76),
        width=s(2),
    )
    draw_text(draw, (position, AXIS_Y + 24), label, fill=color, font_obj=SMALL, anchor="ma")


def draw_width_marker(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    width_value: float,
    label: str,
    color,
    alpha: float,
) -> None:
    center = graph_x(0.0, graph)
    endpoint_value = min(width_value, GRAPH_MAX)
    endpoint = graph_x(endpoint_value, graph)
    y = 520.0
    marker_color = rgba(color, alpha)
    draw.line((s(center), s(y), s(endpoint), s(y)), fill=marker_color, width=s(3))
    arrow_head(draw, (center, y), math.pi, marker_color, size=6.5)
    arrow_head(draw, (endpoint, y), 0.0, marker_color, size=6.5)
    draw.line((s(center), s(y - 8), s(center), s(y + 8)), fill=marker_color, width=s(2))
    draw.line((s(endpoint), s(y - 8), s(endpoint), s(y + 8)), fill=marker_color, width=s(2))
    draw_text(draw, ((center + endpoint) / 2, y - 14), label, fill=marker_color, font_obj=LABEL_BOLD, anchor="ms")


def draw_infinite_width_marker(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    label: str,
    color,
    alpha: float,
) -> None:
    left = graph[0] + 12
    right = graph[2] - 12
    y = 520.0
    marker_color = rgba(color, alpha)
    draw.line((s(left), s(y), s(right), s(y)), fill=marker_color, width=s(3))
    arrow_head(draw, (left, y), math.pi, marker_color, size=7.0)
    arrow_head(draw, (right, y), 0.0, marker_color, size=7.0)
    draw_text(draw, ((left + right) / 2, y - 14), label, fill=marker_color, font_obj=LABEL_BOLD, anchor="ms")


def draw_zero_width_label(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    label: str,
    color,
    alpha: float,
) -> None:
    center = graph_x(0.0, graph)
    draw_text(draw, (center, 506), label, fill=rgba(color, alpha), font_obj=LABEL_BOLD, anchor="ma")


def scene_state(seconds: float) -> tuple[float, float, float, str, str]:
    if seconds < 1.4:
        return (
            EXTREME_LOG_WIDTH,
            1.0,
            0.0,
            "Exact wave number",
            "one k; no preferred position",
        )
    if seconds < 5.0:
        amount = interval_progress(seconds, 1.4, 5.0)
        log_width = EXTREME_LOG_WIDTH * (1.0 - 2.0 * amount)
        exact_k = 1.0 - interval_progress(seconds, 1.4, 1.88)
        exact_x = interval_progress(seconds, 4.52, 5.0)
        return (
            log_width,
            exact_k,
            exact_x,
            "Trade localization across Fourier partners",
            "as the position envelope narrows, the spectrum broadens",
        )
    if seconds < 6.3:
        return (
            -EXTREME_LOG_WIDTH,
            0.0,
            1.0,
            "Exact position",
            "one x; every wave number contributes equally",
        )
    if seconds < 10.1:
        amount = interval_progress(seconds, 6.3, 10.1)
        log_width = -EXTREME_LOG_WIDTH * (1.0 - 2.0 * amount)
        exact_x = 1.0 - interval_progress(seconds, 6.3, 6.78)
        exact_k = interval_progress(seconds, 9.62, 10.1)
        return (
            log_width,
            exact_k,
            exact_x,
            "Reverse the Fourier transform",
            "the same localization trade runs backward",
        )
    return (
        EXTREME_LOG_WIDTH,
        1.0,
        0.0,
        "Exact wave number recovered",
        "reversibility restores the original Fourier partner",
    )


def draw_finite_state(
    draw: ImageDraw.ImageDraw,
    delta_x: float,
    delta_k: float,
    alpha: float,
) -> None:
    if alpha <= 0.0:
        return

    x_upper = gaussian_points(LEFT_GRAPH, delta_x, AXIS_Y, 112.0, 1.0, POSITION_X0)
    x_lower = gaussian_points(LEFT_GRAPH, delta_x, AXIS_Y, 112.0, -1.0, POSITION_X0)
    x_carrier = complex_wave_points(
        LEFT_GRAPH,
        delta_x,
        POSITION_X0,
        CARRIER_K,
        POSITION_X0,
        AXIS_Y,
        112.0,
    )
    k_upper = gaussian_points(RIGHT_GRAPH, delta_k, AXIS_Y, 112.0, 1.0)
    k_lower = gaussian_points(RIGHT_GRAPH, delta_k, AXIS_Y, 112.0, -1.0)
    k_carrier = complex_wave_points(
        RIGHT_GRAPH,
        delta_k,
        0.0,
        -POSITION_X0,
        0.0,
        AXIS_Y,
        112.0,
    )

    fill_between(draw, x_upper, x_lower, rgba(LIGHT_BLUE, 0.10 * alpha))
    fill_between(draw, k_upper, k_lower, rgba(GREEN, 0.08 * alpha))
    draw.line(x_upper, fill=rgba(GOLD, 0.88 * alpha), width=s(3), joint="curve")
    draw.line(x_lower, fill=rgba(GOLD, 0.88 * alpha), width=s(3), joint="curve")
    draw.line(x_carrier, fill=rgba(BLUE, 0.96 * alpha), width=s(3), joint="curve")
    draw.line(k_upper, fill=rgba(GOLD, 0.88 * alpha), width=s(3), joint="curve")
    draw.line(k_lower, fill=rgba(GOLD, 0.88 * alpha), width=s(3), joint="curve")
    draw.line(k_carrier, fill=rgba(GREEN, 0.96 * alpha), width=s(3), joint="curve")

def draw_exact_k_state(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0.0:
        return
    draw_uniform_wave(draw, LEFT_GRAPH, CARRIER_K, POSITION_X0, BLUE, alpha)
    draw_delta(draw, RIGHT_GRAPH, GREEN, alpha)


def draw_exact_x_state(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0.0:
        return
    draw_delta(draw, LEFT_GRAPH, BLUE, alpha, POSITION_X0)
    draw_uniform_wave(draw, RIGHT_GRAPH, -POSITION_X0, 0.0, GREEN, alpha)


def draw_frame(frame: int) -> Image.Image:
    seconds = frame / FPS
    log_width, exact_k, exact_x, heading, caption = scene_state(seconds)
    delta_x = BALANCED_WIDTH * math.exp(log_width)
    delta_k = BALANCED_WIDTH * math.exp(-log_width)
    finite_alpha = 1.0 - max(exact_k, exact_x)

    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image, "RGBA")

    draw_text(draw, (44, 28), "Fourier duality works in both directions", font_obj=TITLE)
    draw_text(draw, (44, 65), heading, fill=PURPLE, font_obj=SUBTITLE)
    draw_text(draw, (44, 91), caption, fill=MUTED, font_obj=SMALL)
    draw_text(
        draw,
        (1236, 69),
        "real part shown inside each magnitude envelope",
        fill=MUTED,
        font_obj=SMALL,
        anchor="ra",
    )
    if exact_k > 0.55 or exact_x > 0.55:
        relation = "ideal Fourier limit"
    else:
        relation = "one state · two Fourier-conjugate representations"
    draw_text(draw, (1236, 94), relation, fill=GOLD, font_obj=SMALL, anchor="ra")

    panel(draw, LEFT_PANEL)
    panel(draw, RIGHT_PANEL)
    draw_text(draw, (66, 139), "Position representation", font_obj=PANEL_TITLE)
    draw_text(draw, (604, 141), "Re ψ(x) with ±|ψ(x)|", fill=BLUE, font_obj=SMALL, anchor="ra")
    draw_text(draw, (676, 139), "Wave-number representation", font_obj=PANEL_TITLE)
    draw_text(draw, (1214, 141), "Re ψ̃(k) with ±|ψ̃(k)|", fill=GREEN, font_obj=SMALL, anchor="ra")

    draw_axis(draw, LEFT_GRAPH, "x", "0")
    draw_axis(draw, RIGHT_GRAPH, "k", "k₀")
    draw_reference_tick(draw, LEFT_GRAPH, POSITION_X0, "x₀", BLUE)

    draw_finite_state(draw, delta_x, delta_k, finite_alpha)
    draw_exact_k_state(draw, exact_k)
    draw_exact_x_state(draw, exact_x)

    if exact_k > 0.55:
        draw_text(draw, (341, 570), "ψ(x) = C eⁱᵏ⁰⁽ˣ⁻ˣ⁰⁾", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (945, 570), "ψ̃(k) = C δ(k − k₀)", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    elif exact_x > 0.55:
        draw_text(draw, (341, 570), "ψ(x) = C δ(x − x₀)", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (945, 570), "ψ̃(k) = C e⁻ⁱ⁽ᵏ⁻ᵏ⁰⁾ˣ⁰", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    elif 6.3 <= seconds < 10.1:
        draw_text(draw, (341, 570), "position distribution broadens", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (945, 570), "wave-number distribution narrows", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")
    else:
        draw_text(draw, (341, 570), "position distribution narrows", fill=BLUE, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (945, 570), "wave-number distribution broadens", fill=GREEN, font_obj=LABEL_BOLD, anchor="mm")

    image = image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return image


def make_contact_sheet() -> Path:
    samples = [
        (0.7, "exact wave number"),
        (3.2, "localization moving into x"),
        (5.6, "exact position"),
        (8.2, "reverse transform"),
        (10.7, "exact wave number recovered"),
    ]
    thumb_w = 400
    thumb_h = 225
    label_h = 28
    margin = 12
    sheet = Image.new(
        "RGB",
        (len(samples) * thumb_w + (len(samples) + 1) * margin, thumb_h + label_h + 2 * margin),
        BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(samples):
        x_value = margin + index * (thumb_w + margin)
        y_value = margin
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x_value, y_value))
        sheet_draw.text(
            (x_value + 5, y_value + thumb_h + 5),
            label,
            fill=MUTED,
            font=SMALL,
        )
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
        remove_scratch_tree(scratch)
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
            remove_scratch_tree(scratch)


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
