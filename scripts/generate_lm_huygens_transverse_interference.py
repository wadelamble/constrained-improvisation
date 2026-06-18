from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"

BLUE = "#245E91"
SOURCE = "#2F2F2F"
WAVELET = "#B85C38"
INK = "#2F2F2F"
PAPER = "#FFFDF8"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=3000,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def field_rgba(field: np.ndarray, scale: float) -> np.ndarray:
    f = np.clip(field / scale, -1.0, 1.0)
    crest = np.clip(f, 0.0, 1.0)
    rgba = np.ones((*field.shape, 4), dtype=float)

    rgba[..., 0] = 0.10
    rgba[..., 1] = 0.36
    rgba[..., 2] = 0.62
    rgba[..., 3] = 0.52 * crest**1.25
    return rgba


def make_transverse_interference(path: Path) -> None:
    frames = 144
    x0 = 1.18
    wavelength = 0.82
    k = 2.0 * np.pi / wavelength
    omega = 2.0 * np.pi * 0.95

    visible_sources = np.linspace(-2.42, 2.42, 15)
    field_sources = np.linspace(-5.0, 5.0, 83)

    x = np.linspace(0.0, 8.2, 380)
    y = np.linspace(-3.0, 3.0, 250)
    X, Y = np.meshgrid(x, y)
    dx = X[None, :, :] - x0
    dy = Y[None, :, :] - field_sources[:, None, None]
    D = np.sqrt(dx * dx + dy * dy)
    forward = 1.0 / (1.0 + np.exp(-(X - x0) / 0.10))
    vertical_window = np.exp(-((Y / 2.95) ** 8))
    weight = forward * vertical_window / np.sqrt(D + 0.45)

    # Ignore the singular near-field right on the source line; this keeps the
    # visual about interference, not point-source brightness.
    near_source = (X < x0 + 0.10)
    weight = np.where(near_source, 0.0, weight)

    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    fig.patch.set_facecolor("#F7F3EC")
    ax.set_facecolor(PAPER)
    ax.set_xlim(0.0, 8.2)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    title = ax.text(
        0.5,
        1.03,
        "Interference leaves a plane wavefront",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=16,
        color=INK,
        weight="bold",
    )
    ax.text(0.06, 0.91, "source wavefront", transform=ax.transAxes, fontsize=12, color="#7A7066")
    ax.text(0.67, 0.91, "coherent sum", transform=ax.transAxes, fontsize=12, color=BLUE)
    ax.text(
        0.06,
        0.08,
        "off the straight crest, the circular contributions wash out",
        transform=ax.transAxes,
        fontsize=12.5,
        color=WAVELET,
    )

    image = ax.imshow(
        np.zeros((len(y), len(x), 4)),
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        interpolation="bilinear",
        zorder=1,
    )

    ax.plot([x0, x0], [-2.55, 2.55], color="#AFA79A", lw=3.0, zorder=5)
    source_points = ax.scatter(
        np.full_like(visible_sources, x0),
        visible_sources,
        s=18,
        color=SOURCE,
        zorder=8,
    )

    wavelets: list[Circle] = []
    for cy in visible_sources:
        for ring in range(2):
            circle = Circle((x0, cy), 0.0, fill=False, edgecolor=WAVELET, lw=0.95, alpha=0.0, zorder=4)
            ax.add_patch(circle)
            wavelets.append(circle)

    crest_lines = [
        ax.plot([], [], color=BLUE, lw=2.8, alpha=0.0, zorder=8)[0]
        for _ in range(3)
    ]
    cancellation_marks = LineCollection([], colors="#B85C38", linewidths=1.0, alpha=0.0, zorder=6)
    ax.add_collection(cancellation_marks)
    motion_arrow = ax.annotate(
        "",
        xy=(6.8, 0.0),
        xytext=(5.7, 0.0),
        arrowprops={"arrowstyle": "->", "color": "#5B7F72", "lw": 2.0},
        zorder=10,
    )
    ax.text(5.72, 0.22, "motion", fontsize=12, color="#5B7F72")

    # Static normalization chosen from a few phases so the movie does not pulse
    # merely because the color scale changes.
    probe_scales = []
    for phase_t in np.linspace(0.0, 1.0, 8, endpoint=False):
        raw = np.sum(np.cos(k * D - omega * phase_t) * weight, axis=0)
        probe_scales.append(np.percentile(np.abs(raw[X > x0 + 0.35]), 98.5))
    scale = float(np.max(probe_scales))

    def update(frame: int):
        t = frame / frames * 2.8
        raw = np.sum(np.cos(k * D - omega * t) * weight, axis=0)

        # Fade the ragged top/bottom edge of the finite-source construction.
        rgba = field_rgba(raw, scale)
        image.set_data(rgba)

        # Faint individual circular phase fronts from the visible source points.
        radii = ((t * omega / k) + np.arange(2) * wavelength) % (2.4 * wavelength)
        radii = radii + 0.16
        for idx, cy in enumerate(visible_sources):
            for ring in range(2):
                circle = wavelets[idx * 2 + ring]
                circle.center = (x0, cy)
                circle.radius = radii[ring]
                circle.set_alpha(0.24 if radii[ring] > 0.24 else 0.0)

        # Mark a few coherent plane crests of the summed field.
        phase_offset = (omega * t / k) % wavelength
        for i, line in enumerate(crest_lines):
            cx = x0 + phase_offset + (i + 1) * wavelength
            if x0 + 0.2 < cx < 8.05:
                line.set_data([cx, cx], [-2.58, 2.58])
                line.set_alpha(0.48)
            else:
                line.set_data([], [])
                line.set_alpha(0.0)

        # Short fading strokes suggest the off-crest pieces cancelling rather
        # than becoming a new wavefront.
        segments = []
        fade_x = x0 + phase_offset + 1.35 * wavelength
        for y0 in np.linspace(-2.25, 2.25, 9):
            if abs(y0) < 0.35:
                continue
            segments.append([(fade_x - 0.18, y0 - 0.10), (fade_x + 0.18, y0 + 0.10)])
            segments.append([(fade_x - 0.18, y0 + 0.10), (fade_x + 0.18, y0 - 0.10)])
        cancellation_marks.set_segments(segments)
        cancellation_marks.set_alpha(0.16 + 0.10 * np.sin(2 * np.pi * t) ** 2)

        return [image, source_points, cancellation_marks, *wavelets, *crest_lines, title]

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / 24, blit=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_transverse_interference(OUT / "lm-huygens-transverse-interference-review.mp4")
