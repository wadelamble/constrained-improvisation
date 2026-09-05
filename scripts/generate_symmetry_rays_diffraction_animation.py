from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"

VIDEO_PATH = OUTPUT_DIR / "symmetry-rays-and-double-slit.mp4"
CONTACT_PATH = OUTPUT_DIR / "symmetry-rays-and-double-slit-contact-sheet.png"
FINAL_PATH = OUTPUT_DIR / "symmetry-rays-and-double-slit-final.png"

BG = "#F7F3EC"
PANEL = "#FFFDF8"
INK = "#2F2F2F"
MUTED = "#675F56"
BORDER = "#C9BCAA"
RAY = "#A66B2B"
SOURCE = "#7E4B3A"

WAVE_CMAP = LinearSegmentedColormap.from_list(
    "wave_diverging",
    ["#315B7D", "#8DAAC0", "#FFFDF8", "#D9A184", "#A74F35"],
    N=256,
)


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=3600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    )
    anim.save(path, writer=writer)


def add_panel_title(ax: plt.Axes, title: str, subtitle: str) -> None:
    ax.text(
        0.02,
        0.965,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=13,
        fontweight="bold",
        color=INK,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": BG, "edgecolor": "none", "alpha": 0.92},
        zorder=30,
    )
    ax.text(
        0.02,
        0.895,
        subtitle,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.5,
        color=MUTED,
        bbox={"boxstyle": "round,pad=0.22", "facecolor": BG, "edgecolor": "none", "alpha": 0.88},
        zorder=30,
    )


def style_axis(ax: plt.Axes) -> None:
    ax.set_facecolor(PANEL)
    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(BORDER)
        spine.set_linewidth(1.15)


def radial_field(xx: np.ndarray, yy: np.ndarray, phase: float) -> tuple[np.ndarray, np.ndarray]:
    source_x, source_y = -0.75, 0.0
    radius = np.hypot(xx - source_x, yy - source_y)
    wavelength = 0.62
    envelope = 1.0 / np.sqrt(0.45 + radius)
    source_ramp = 1.0 - np.exp(-(radius / 0.22) ** 2)
    field = envelope * source_ramp * np.cos(2.0 * np.pi * radius / wavelength - phase)
    return field, radius


def slit_field(xx: np.ndarray, yy: np.ndarray, phase: float) -> np.ndarray:
    barrier_x = -0.82
    slit_y = (-0.72, 0.72)
    wavelength = 0.58
    wave_number = 2.0 * np.pi / wavelength

    incident = 0.82 * np.cos(wave_number * (xx - barrier_x) - phase)

    transmitted = np.zeros_like(xx)
    for y0 in slit_y:
        radius = np.hypot(xx - barrier_x, yy - y0)
        attenuation = 0.78 / np.sqrt(radius + 0.34)
        transmitted += attenuation * np.cos(wave_number * radius - phase)
    transmitted *= 0.72

    field = np.where(xx <= barrier_x, incident, transmitted)
    return field


def draw_radial_rays(ax: plt.Axes) -> None:
    source = np.array([-0.75, 0.0])
    for angle in np.linspace(-0.90 * np.pi, 0.90 * np.pi, 11):
        direction = np.array([np.cos(angle), np.sin(angle)])
        start = source + 0.52 * direction
        end = source + 3.45 * direction
        if not (-3.9 < end[0] < 3.9 and -2.9 < end[1] < 2.9):
            scale_x = 3.55 / max(abs(end[0] - source[0]), 1e-9)
            scale_y = 2.55 / max(abs(end[1] - source[1]), 1e-9)
            end = source + min(scale_x, scale_y) * (end - source)
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            arrowprops={
                "arrowstyle": "->",
                "color": RAY,
                "linewidth": 1.35,
                "alpha": 0.78,
                "shrinkA": 0,
                "shrinkB": 0,
            },
            zorder=15,
        )
    ax.scatter([-0.75], [0.0], s=54, color=SOURCE, edgecolor=BG, linewidth=1.0, zorder=20)


def draw_barrier_and_wavelets(ax: plt.Axes, phase: float) -> None:
    barrier_x = -0.82
    slit_centers = (-0.72, 0.72)
    half_gap = 0.18
    segments = [
        (-3.0, slit_centers[0] - half_gap),
        (slit_centers[0] + half_gap, slit_centers[1] - half_gap),
        (slit_centers[1] + half_gap, 3.0),
    ]
    for y0, y1 in segments:
        ax.plot([barrier_x, barrier_x], [y0, y1], color=INK, linewidth=6.5, solid_capstyle="butt", zorder=25)

    ax.scatter(
        [barrier_x, barrier_x],
        list(slit_centers),
        s=25,
        color=SOURCE,
        edgecolor=BG,
        linewidth=0.7,
        zorder=26,
    )

    wavelength = 0.58
    phase_distance = (phase / (2.0 * np.pi)) * wavelength
    theta = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 220)
    for slit_y in slit_centers:
        for index in range(1, 8):
            radius = phase_distance + index * wavelength
            while radius > 4.3:
                radius -= wavelength
            arc_x = barrier_x + radius * np.cos(theta)
            arc_y = slit_y + radius * np.sin(theta)
            mask = (arc_x <= 4.0) & (arc_y >= -3.0) & (arc_y <= 3.0)
            ax.plot(
                arc_x[mask],
                arc_y[mask],
                color=BG,
                linewidth=0.75,
                alpha=0.35,
                zorder=12,
            )


def make_animation() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    frame_dir = OUTPUT_DIR / "_symmetry_rays_diffraction_frames"
    frame_dir.mkdir(exist_ok=True)

    x = np.linspace(-4.0, 4.0, 520)
    y = np.linspace(-3.0, 3.0, 390)
    xx, yy = np.meshgrid(x, y)

    frames = 144
    fps = 24
    sample_indices = [0, 24, 48, 72, 96, 120]
    sample_paths: list[Path] = []

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.45), dpi=120)
    fig.patch.set_facecolor(BG)
    fig.subplots_adjust(left=0.025, right=0.985, top=0.965, bottom=0.045, wspace=0.055)

    def draw_frame(frame: int) -> None:
        phase = 2.0 * np.pi * frame / frames
        for ax in axes:
            ax.clear()
            style_axis(ax)

        left_field, _ = radial_field(xx, yy, phase)
        axes[0].imshow(
            left_field,
            extent=(-4.0, 4.0, -3.0, 3.0),
            origin="lower",
            cmap=WAVE_CMAP,
            vmin=-1.15,
            vmax=1.15,
            interpolation="bilinear",
            zorder=1,
        )
        draw_radial_rays(axes[0])
        add_panel_title(
            axes[0],
            "Ray-like propagation",
            "Rays point normal to the moving wavefronts",
        )

        right_field = slit_field(xx, yy, phase)
        axes[1].imshow(
            right_field,
            extent=(-4.0, 4.0, -3.0, 3.0),
            origin="lower",
            cmap=WAVE_CMAP,
            vmin=-1.45,
            vmax=1.45,
            interpolation="bilinear",
            zorder=1,
        )
        draw_barrier_and_wavelets(axes[1], phase)
        add_panel_title(
            axes[1],
            "Diffraction and interference",
            "Each opening emits spreading wavelets that superpose",
        )

    def update(frame: int):
        draw_frame(frame)
        return []

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)
    save_animation(anim, VIDEO_PATH, fps=fps)

    for index in sample_indices:
        draw_frame(index)
        frame_path = frame_dir / f"rays-diffraction-{index:03d}.png"
        fig.savefig(frame_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.08)
        sample_paths.append(frame_path)

    draw_frame(frames - 1)
    fig.savefig(FINAL_PATH, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)

    thumbs: list[Image.Image] = []
    for path in sample_paths:
        with Image.open(path) as image:
            thumbs.append(image.convert("RGB").resize((640, 270), Image.Resampling.LANCZOS))

    margin = 24
    title_height = 42
    sheet = Image.new("RGB", (2 * 640 + 3 * margin, 3 * 270 + 4 * margin + title_height), BG)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    draw.text((margin, 13), "Rays, diffraction, and interference over one wave cycle", fill=INK, font=font)
    for idx, thumb in enumerate(thumbs):
        row, col = divmod(idx, 2)
        px = margin + col * (640 + margin)
        py = title_height + margin + row * (270 + margin)
        sheet.paste(thumb, (px, py))
        draw.rectangle([px, py, px + 640, py + 270], outline=BORDER, width=2)
    sheet.save(CONTACT_PATH)


if __name__ == "__main__":
    make_animation()
