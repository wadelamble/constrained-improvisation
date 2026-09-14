from __future__ import annotations

import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / ".tools" / "animation-python-packages"
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

from PIL import Image, ImageDraw
import imageio_ffmpeg

import generate_symmetry_xk_uncertainty_extremes_animation as amplitude


NAME = "symmetry-xk-squared-magnitudes"
FRAMES = round(amplitude.TOTAL_SECONDS * amplitude.FPS)


def density_points(
    graph: tuple[float, float, float, float],
    width: float,
    baseline: float,
    height: float,
) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(amplitude.SAMPLES):
        value = (
            amplitude.GRAPH_MIN
            + (amplitude.GRAPH_MAX - amplitude.GRAPH_MIN)
            * index
            / (amplitude.SAMPLES - 1)
        )
        # Squaring exp[-u²/(4 σ²)] gives a density with standard deviation σ.
        density = math.exp(-(value * value) / (2.0 * width * width))
        points.append(
            (
                amplitude.s(amplitude.graph_x(value, graph)),
                amplitude.s(baseline - height * density),
            )
        )
    return points


def draw_density_finite_state(
    draw: ImageDraw.ImageDraw,
    delta_x: float,
    delta_k: float,
    alpha: float,
) -> None:
    if alpha <= 0.0:
        return

    x_curve = density_points(amplitude.LEFT_GRAPH, delta_x, amplitude.AXIS_Y, 145.0)
    k_curve = density_points(amplitude.RIGHT_GRAPH, delta_k, amplitude.AXIS_Y, 145.0)

    amplitude.fill_to_axis(
        draw,
        x_curve,
        amplitude.LEFT_GRAPH,
        amplitude.AXIS_Y,
        amplitude.rgba(amplitude.BLUE, 0.16 * alpha),
    )
    amplitude.fill_to_axis(
        draw,
        k_curve,
        amplitude.RIGHT_GRAPH,
        amplitude.AXIS_Y,
        amplitude.rgba(amplitude.GREEN, 0.16 * alpha),
    )
    draw.line(
        x_curve,
        fill=amplitude.rgba(amplitude.BLUE, 0.98 * alpha),
        width=amplitude.s(4),
        joint="curve",
    )
    draw.line(
        k_curve,
        fill=amplitude.rgba(amplitude.GREEN, 0.98 * alpha),
        width=amplitude.s(4),
        joint="curve",
    )
    amplitude.draw_width_marker(
        draw,
        amplitude.LEFT_GRAPH,
        delta_x,
        "σₓ",
        amplitude.PURPLE,
        alpha,
    )
    amplitude.draw_width_marker(
        draw,
        amplitude.RIGHT_GRAPH,
        delta_k,
        "σₖ",
        amplitude.PURPLE,
        alpha,
    )


def draw_constant_density(
    draw: ImageDraw.ImageDraw,
    graph: tuple[float, float, float, float],
    color,
    alpha: float,
) -> None:
    top = 286.0
    draw.rectangle(
        (
            amplitude.s(graph[0]),
            amplitude.s(top),
            amplitude.s(graph[2]),
            amplitude.s(amplitude.AXIS_Y),
        ),
        fill=amplitude.rgba(color, 0.12 * alpha),
    )
    draw.line(
        (amplitude.s(graph[0]), amplitude.s(top), amplitude.s(graph[2]), amplitude.s(top)),
        fill=amplitude.rgba(color, alpha),
        width=amplitude.s(4),
    )


def draw_exact_k_density(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0.0:
        return
    draw_constant_density(draw, amplitude.LEFT_GRAPH, amplitude.BLUE, alpha)
    amplitude.draw_delta(draw, amplitude.RIGHT_GRAPH, amplitude.GREEN, alpha)
    amplitude.draw_infinite_width_marker(
        draw,
        amplitude.LEFT_GRAPH,
        "σₓ → ∞",
        amplitude.PURPLE,
        alpha,
    )
    amplitude.draw_zero_width_label(
        draw,
        amplitude.RIGHT_GRAPH,
        "σₖ → 0",
        amplitude.PURPLE,
        alpha,
    )


def draw_exact_x_density(draw: ImageDraw.ImageDraw, alpha: float) -> None:
    if alpha <= 0.0:
        return
    amplitude.draw_delta(draw, amplitude.LEFT_GRAPH, amplitude.BLUE, alpha)
    draw_constant_density(draw, amplitude.RIGHT_GRAPH, amplitude.GREEN, alpha)
    amplitude.draw_zero_width_label(
        draw,
        amplitude.LEFT_GRAPH,
        "σₓ → 0",
        amplitude.PURPLE,
        alpha,
    )
    amplitude.draw_infinite_width_marker(
        draw,
        amplitude.RIGHT_GRAPH,
        "σₖ → ∞",
        amplitude.PURPLE,
        alpha,
    )


def density_scene_text(seconds: float) -> tuple[str, str]:
    if seconds < 1.4:
        return (
            "Exact wave-number limit",
            "position density spreads without bound; wave-number density localizes",
        )
    if seconds < 5.0:
        return (
            "Trade statistical width between representations",
            "as σₓ decreases, σₖ increases",
        )
    if seconds < 6.3:
        return (
            "Exact position limit",
            "position density localizes; wave-number density spreads without bound",
        )
    if seconds < 9.7:
        return (
            "Return from the exact-position limit",
            "the reciprocal standard deviations approach balance",
        )
    return (
        "Balanced Gaussian distributions",
        "equal standard deviations on reciprocal display scales",
    )


def density_scene_state(seconds: float) -> tuple[float, float, float]:
    # Preserve this movie's original return to balanced distributions. The
    # amplitude movie later acquired a different ending and is shared for art.
    if seconds < 6.3:
        return amplitude.scene_state(seconds)[:3]
    if seconds < 9.7:
        amount = amplitude.interval_progress(seconds, 6.3, 9.7)
        return (
            -amplitude.EXTREME_LOG_WIDTH * (1.0 - amount),
            0.0,
            1.0 - amplitude.interval_progress(seconds, 6.3, 6.78),
        )
    return 0.0, 0.0, 0.0


def draw_frame(frame: int) -> Image.Image:
    seconds = frame / amplitude.FPS
    log_width, exact_k, exact_x = density_scene_state(seconds)
    heading, caption = density_scene_text(seconds)
    delta_x = amplitude.BALANCED_WIDTH * math.exp(log_width)
    delta_k = amplitude.BALANCED_WIDTH * math.exp(-log_width)
    finite_alpha = 1.0 - max(exact_k, exact_x)

    image = Image.new(
        "RGB",
        (amplitude.WIDTH * amplitude.SCALE, amplitude.HEIGHT * amplitude.SCALE),
        amplitude.BG,
    )
    draw = ImageDraw.Draw(image, "RGBA")

    amplitude.draw_text(
        draw,
        (44, 28),
        "Uncertainty lives in the squared magnitudes",
        font_obj=amplitude.TITLE,
    )
    amplitude.draw_text(
        draw,
        (44, 65),
        heading,
        fill=amplitude.PURPLE,
        font_obj=amplitude.SUBTITLE,
    )
    amplitude.draw_text(
        draw,
        (44, 91),
        caption,
        fill=amplitude.MUTED,
        font_obj=amplitude.SMALL,
    )
    amplitude.draw_text(
        draw,
        (1236, 69),
        "shape vertically rescaled · not physical time",
        fill=amplitude.MUTED,
        font_obj=amplitude.SMALL,
        anchor="ra",
    )
    if exact_k > 0.55 or exact_x > 0.55:
        relation = "ideal limit of the Gaussian family"
    else:
        relation = "finite Gaussian family:  σₓ σₖ = 1/2"
    amplitude.draw_text(
        draw,
        (1236, 94),
        relation,
        fill=amplitude.GOLD,
        font_obj=amplitude.SMALL,
        anchor="ra",
    )

    amplitude.panel(draw, amplitude.LEFT_PANEL)
    amplitude.panel(draw, amplitude.RIGHT_PANEL)
    amplitude.draw_text(
        draw,
        (66, 139),
        "Position-space distribution",
        font_obj=amplitude.PANEL_TITLE,
    )
    amplitude.draw_text(
        draw,
        (604, 141),
        "|ψ(x)|²",
        fill=amplitude.BLUE,
        font_obj=amplitude.SMALL,
        anchor="ra",
    )
    amplitude.draw_text(
        draw,
        (676, 139),
        "Wave-number distribution",
        font_obj=amplitude.PANEL_TITLE,
    )
    amplitude.draw_text(
        draw,
        (1214, 141),
        "|ψ̃(k)|²",
        fill=amplitude.GREEN,
        font_obj=amplitude.SMALL,
        anchor="ra",
    )

    amplitude.draw_axis(draw, amplitude.LEFT_GRAPH, "x", "0")
    amplitude.draw_axis(draw, amplitude.RIGHT_GRAPH, "k", "k₀")

    draw_density_finite_state(draw, delta_x, delta_k, finite_alpha)
    draw_exact_k_density(draw, exact_k)
    draw_exact_x_density(draw, exact_x)

    if exact_k > 0.55:
        amplitude.draw_text(
            draw,
            (341, 570),
            "position density: unbounded spread",
            fill=amplitude.BLUE,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
        amplitude.draw_text(
            draw,
            (945, 570),
            "wave-number density → delta",
            fill=amplitude.GREEN,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
    elif exact_x > 0.55:
        amplitude.draw_text(
            draw,
            (341, 570),
            "position density → delta",
            fill=amplitude.BLUE,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
        amplitude.draw_text(
            draw,
            (945, 570),
            "wave-number density: unbounded spread",
            fill=amplitude.GREEN,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
    elif seconds >= 9.7:
        amplitude.draw_text(
            draw,
            (341, 570),
            "Gaussian position density",
            fill=amplitude.BLUE,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
        amplitude.draw_text(
            draw,
            (945, 570),
            "matching wave-number density",
            fill=amplitude.GREEN,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
    else:
        amplitude.draw_text(
            draw,
            (341, 570),
            "narrower position density",
            fill=amplitude.BLUE,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )
        amplitude.draw_text(
            draw,
            (945, 570),
            "broader wave-number density",
            fill=amplitude.GREEN,
            font_obj=amplitude.LABEL_BOLD,
            anchor="mm",
        )

    return image.resize(
        (amplitude.WIDTH, amplitude.HEIGHT),
        Image.Resampling.LANCZOS,
    )


def make_contact_sheet() -> Path:
    samples = [
        (0.7, "exact wave number"),
        (3.2, "reciprocal widths cross"),
        (5.6, "exact position"),
        (7.9, "returning from the extreme"),
        (10.7, "balanced distributions"),
    ]
    thumb_w = 400
    thumb_h = 225
    label_h = 28
    margin = 12
    sheet = Image.new(
        "RGB",
        (
            len(samples) * thumb_w + (len(samples) + 1) * margin,
            thumb_h + label_h + 2 * margin,
        ),
        amplitude.BG,
    )
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(samples):
        x_value = margin + index * (thumb_w + margin)
        y_value = margin
        frame = min(FRAMES - 1, round(seconds * amplitude.FPS))
        thumb = draw_frame(frame).resize(
            (thumb_w, thumb_h),
            Image.Resampling.LANCZOS,
        )
        sheet.paste(thumb, (x_value, y_value))
        sheet_draw.text(
            (x_value + 5, y_value + thumb_h + 5),
            label,
            fill=amplitude.MUTED,
            font=amplitude.SMALL,
        )
    output = amplitude.OUTPUT_DIR / f"{NAME}-contact-sheet.png"
    sheet.save(output)
    return output


def render() -> tuple[Path, Path, Path]:
    amplitude.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video = amplitude.OUTPUT_DIR / f"{NAME}.mp4"
    temporary_video = video.with_name(f"{NAME}-rendering.mp4")
    final_still = amplitude.OUTPUT_DIR / f"{NAME}-final.png"
    process = subprocess.Popen(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{amplitude.WIDTH}x{amplitude.HEIGHT}",
            "-r", str(amplitude.FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(temporary_video),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        for index in range(FRAMES):
            process.stdin.write(draw_frame(index).tobytes())
            if index % (3 * amplitude.FPS) == 0:
                print(f"Rendering {index // amplitude.FPS}/{amplitude.TOTAL_SECONDS:g}s", flush=True)
        process.stdin.close()
        error = process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
        temporary_video.replace(video)
        draw_frame(FRAMES - 1).save(final_still)
        contact = make_contact_sheet()
        return video, contact, final_still
    except BaseException:
        process.kill()
        process.wait()
        raise


def main() -> None:
    if amplitude.ESSENTIAL_CONTENT_BOTTOM >= amplitude.CONTROLS_SAFE_TOP:
        raise RuntimeError("essential content overlaps the native video-control region")
    video, contact, final_still = render()
    print(video)
    print(contact)
    print(final_still)
    reader = imageio_ffmpeg.read_frames(str(video), pix_fmt="rgb24")
    metadata = next(reader)
    decoded_frames = sum(1 for _ in reader)
    if (tuple(metadata["size"]) != (amplitude.WIDTH, amplitude.HEIGHT)
            or metadata["fps"] != amplitude.FPS or decoded_frames != FRAMES):
        raise RuntimeError(f"unexpected video output: {metadata}; frames={decoded_frames}")
    print(f"Verified {decoded_frames} frames; {metadata['fps']:g} fps; {metadata['size']}")
    print(
        f"essential_content_bottom={amplitude.ESSENTIAL_CONTENT_BOTTOM}; "
        f"controls_safe_top={amplitude.CONTROLS_SAFE_TOP}"
    )


if __name__ == "__main__":
    main()
