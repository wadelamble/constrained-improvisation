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
        bitrate=3200,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def crest_rgba(
    x: np.ndarray,
    y: np.ndarray,
    first_crest: float,
    spacing: float,
    source_x: float,
) -> np.ndarray:
    X, Y = np.meshgrid(x, y)
    stripe = np.zeros_like(X)
    for i in range(7):
        center = first_crest + i * spacing
        stripe += np.exp(-((X - center) / 0.085) ** 2)

    forward = 1.0 / (1.0 + np.exp(-(X - source_x - 0.12) / 0.10))
    vertical_window = np.exp(-((Y / 2.65) ** 8))
    near_source_haze = 0.28 * np.exp(-((X - source_x - 0.58 * spacing) / 0.30) ** 2)
    amp = np.clip(stripe * forward * vertical_window + near_source_haze * vertical_window, 0.0, 1.0)

    rgba = np.ones((*X.shape, 4), dtype=float)
    rgba[..., 0] = 0.10
    rgba[..., 1] = 0.36
    rgba[..., 2] = 0.62
    rgba[..., 3] = 0.52 * amp**1.2
    return rgba


def make_animation(path: Path) -> None:
    frames = 168
    cycles = 4.35
    x0 = 1.05
    spacing = 1.18
    y_points = np.linspace(-2.42, 2.42, 15)

    x = np.linspace(0.0, 8.2, 360)
    y = np.linspace(-3.0, 3.0, 230)

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
        "Each new wavefront becomes the next source",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=16,
        color=INK,
        weight="bold",
    )
    emitting_label = ax.text(0.0, 2.73, "emitting wavefront", fontsize=12, color="#7A7066")
    ax.text(0.66, 0.91, "coherent sum", transform=ax.transAxes, fontsize=12, color=BLUE)

    image = ax.imshow(
        np.zeros((len(y), len(x), 4)),
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        interpolation="bilinear",
        zorder=1,
    )

    previous_lines = [
        ax.plot([], [], color="#AFA79A", lw=1.4, alpha=0.0, zorder=2)[0]
        for _ in range(5)
    ]
    active_line, = ax.plot([], [], color="#AFA79A", lw=3.2, zorder=6)
    envelope_line, = ax.plot([], [], color=BLUE, lw=3.1, alpha=0.0, zorder=8)
    source_points = ax.scatter([], [], s=18, color=SOURCE, zorder=9)

    wavelets: list[Circle] = []
    for cy in y_points:
        for ring in range(2):
            circle = Circle((0, cy), 0.0, fill=False, edgecolor=WAVELET, lw=0.95, alpha=0.0, zorder=4)
            ax.add_patch(circle)
            wavelets.append(circle)

    cancellation_marks = LineCollection([], colors=WAVELET, linewidths=1.0, alpha=0.0, zorder=7)
    ax.add_collection(cancellation_marks)

    motion_arrow = ax.annotate(
        "",
        xy=(6.8, 0.0),
        xytext=(5.7, 0.0),
        arrowprops={"arrowstyle": "->", "color": "#5B7F72", "lw": 2.0},
        zorder=10,
    )
    motion_label = ax.text(5.72, 0.22, "motion", fontsize=12, color="#5B7F72")

    def update(frame: int):
        t = frame / frames * cycles
        step = int(np.floor(t))
        phase = t - step
        source_x = x0 + step * spacing
        radius = phase * spacing
        envelope_x = source_x + radius

        image.set_data(crest_rgba(x, y, envelope_x, spacing, source_x))

        y_min, y_max = -2.55, 2.55
        for idx, line in enumerate(previous_lines):
            px = x0 + idx * spacing
            if idx < step:
                line.set_data([px, px], [y_min, y_max])
                line.set_alpha(0.24)
            else:
                line.set_data([], [])
                line.set_alpha(0.0)

        active_line.set_data([source_x, source_x], [y_min, y_max])
        active_line.set_alpha(max(0.35, 1.0 - 0.25 * phase))
        emitting_label.set_position((max(0.28, source_x - 0.55), 2.73))

        source_points.set_offsets(np.column_stack([np.full_like(y_points, source_x), y_points]))
        source_points.set_alpha(max(0.45, 1.0 - 0.35 * phase))

        envelope_line.set_data([envelope_x, envelope_x], [y_min, y_max])
        envelope_line.set_alpha(0.10 + 0.72 * phase)

        radii = [radius, max(0.0, radius - 0.48 * spacing)]
        for idx, cy in enumerate(y_points):
            for ring, r in enumerate(radii):
                circle = wavelets[idx * 2 + ring]
                circle.center = (source_x, cy)
                circle.radius = r
                circle.set_alpha((0.26 if ring == 0 else 0.14) if r > 0.07 else 0.0)

        segments = []
        mark_x = source_x + 0.58 * spacing + 0.36 * radius
        for y0 in np.linspace(-2.25, 2.25, 9):
            if abs(y0) < 0.35:
                continue
            segments.append([(mark_x - 0.15, y0 - 0.09), (mark_x + 0.15, y0 + 0.09)])
            segments.append([(mark_x - 0.15, y0 + 0.09), (mark_x + 0.15, y0 - 0.09)])
        cancellation_marks.set_segments(segments)
        cancellation_marks.set_alpha(0.05 + 0.17 * phase * (1.0 - 0.35 * phase))

        return [
            image,
            *previous_lines,
            active_line,
            envelope_line,
            source_points,
            emitting_label,
            cancellation_marks,
            *wavelets,
            title,
            motion_arrow,
            motion_label,
        ]

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / 24, blit=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_animation(OUT / "lm-huygens-transverse-interference-cascade-review.mp4")
