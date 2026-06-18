from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"

BLUE = "#355070"
ORANGE = "#B85C38"
INK = "#2F2F2F"
PAPER = "#FFFDF8"
SLOW = "#E8F2F7"
EDGE = "#6F685F"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2800,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def draw_front(
    ax: plt.Axes,
    normal: np.ndarray,
    tangent: np.ndarray,
    value: float,
    *,
    above: bool,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
    linestyle: str | tuple = "-",
) -> None:
    u = np.linspace(-8.0, 8.0, 1000)
    pts = value * normal[:, None] + tangent[:, None] * u
    mask = pts[1] >= 0 if above else pts[1] <= 0
    ax.plot(
        np.ma.masked_where(~mask, pts[0]),
        np.ma.masked_where(~mask, pts[1]),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
        linestyle=linestyle,
    )


def draw_lower_wavelet(
    ax: plt.Axes,
    x0: float,
    radius: float,
    *,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
    linestyle: str | tuple = "-",
) -> None:
    if radius <= 0:
        return
    phi = np.linspace(np.pi, 2.0 * np.pi, 260)
    x = x0 + radius * np.cos(phi)
    y = radius * np.sin(phi)
    ax.plot(
        x,
        y,
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
        linestyle=linestyle,
    )


def make_huygens_snell_ghost_reference(path: Path) -> None:
    frames = 168
    theta1 = np.deg2rad(46.0)
    speed_ratio = 1.0 / 1.55
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    spacing = 0.72
    source_xs = np.arange(-1.8, 3.1, 0.43)

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.2, color=PAPER, zorder=0)
        ax.axhspan(-2.2, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.6, zorder=8)
        ax.set_xlim(-2.0, 3.05)
        ax.set_ylim(-2.0, 1.9)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Huygens to Snell: slower wavelets bend the envelope", fontsize=14.4, color=INK)
        ax.text(-1.88, 0.13, "fast medium", fontsize=9.6, color="#4B463F", zorder=30)
        ax.text(-1.88, -0.25, "slow medium", fontsize=9.6, color="#4B463F", zorder=30)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        phase = -0.45 + 3.25 * progress

        # Moving incident wavefront train above the boundary.
        for n in range(-4, 8):
            value = phase - n * spacing
            if -2.8 < value < 3.4:
                active = n == 0
                draw_front(
                    ax,
                    d1,
                    w1,
                    value,
                    above=True,
                    color=BLUE,
                    linewidth=2.65 if active else 1.25,
                    alpha=0.92 if active else 0.30,
                    zorder=18 if active else 3,
                )

        # The lower-medium wavefront train. The highlighted front is the envelope
        # of the smaller orange Huygens wavelets.
        for n in range(-4, 8):
            value = phase - n * spacing
            if value <= -0.1:
                continue
            active = n == 0
            draw_front(
                ax,
                d2,
                w2,
                speed_ratio * value,
                above=False,
                color=ORANGE,
                linewidth=3.05 if active else 1.25,
                alpha=0.94 if active else 0.30,
                zorder=22 if active else 4,
            )

        # Dashed blue "same speed" reference: what the envelope would do if the
        # wavelets below kept the fast-medium speed. It continues the old direction.
        if phase > 0.02:
            draw_front(
                ax,
                d1,
                w1,
                phase,
                above=False,
                color=BLUE,
                linewidth=2.0,
                alpha=0.50,
                zorder=12,
                linestyle=(0, (7, 5)),
            )

        active_sources: list[tuple[float, float]] = []
        for x0 in source_xs:
            age = phase - d1[0] * x0
            if 0.04 < age < 1.45:
                active_sources.append((x0, age))

        for x0, age in active_sources:
            fast_radius = age
            slow_radius = speed_ratio * age

            draw_lower_wavelet(
                ax,
                x0,
                fast_radius,
                color=BLUE,
                linewidth=1.25,
                alpha=0.34,
                zorder=10,
                linestyle=(0, (6, 5)),
            )
            draw_lower_wavelet(
                ax,
                x0,
                slow_radius,
                color=ORANGE,
                linewidth=1.55,
                alpha=0.68,
                zorder=16,
            )
            ax.scatter([x0], [0], s=24, color=ORANGE, edgecolor="white", linewidth=0.6, zorder=28)

        x_cross = phase / d1[0]
        if -1.8 < x_cross < 3.0:
            start = np.array([x_cross, 0.0]) - 1.18 * d1
            end = np.array([x_cross, 0.0]) - 0.06 * d1
            ax.annotate(
                "",
                xy=end,
                xytext=start,
                arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.0, "alpha": 0.84},
                zorder=25,
            )
            refr_start = np.array([x_cross, 0.0]) + 0.05 * d2
            refr_end = np.array([x_cross, 0.0]) + 1.18 * d2
            ax.annotate(
                "",
                xy=refr_end,
                xytext=refr_start,
                arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2, "alpha": 0.86},
                zorder=25,
            )

        if progress > 0.22:
            ax.plot([1.83, 2.18], [1.45, 1.45], color=BLUE, linewidth=1.7, linestyle=(0, (7, 5)), alpha=0.62)
            ax.text(2.24, 1.41, "fast reference", fontsize=9.1, color=BLUE, alpha=0.8)
            ax.plot([1.83, 2.18], [1.22, 1.22], color=ORANGE, linewidth=2.0, alpha=0.80)
            ax.text(2.24, 1.18, "slow wavelets", fontsize=9.1, color=ORANGE, alpha=0.84)

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_ghost_reference(OUT / "lm-huygens-snell-ghost-reference-review.mp4")
