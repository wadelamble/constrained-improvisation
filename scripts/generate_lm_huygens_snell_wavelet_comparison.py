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
EDGE = "#7E7468"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def clipped_front(
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
) -> None:
    u = np.linspace(-6.0, 6.0, 900)
    pts = value * normal[:, None] + tangent[:, None] * u
    mask = pts[1] >= 0 if above else pts[1] <= 0
    x = np.ma.masked_where(~mask, pts[0])
    y = np.ma.masked_where(~mask, pts[1])
    ax.plot(x, y, color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)


def clipped_circle(
    ax: plt.Axes,
    center: np.ndarray,
    radius: float,
    *,
    above: bool,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    if radius <= 0.01:
        return
    phi = np.linspace(0, 2.0 * np.pi, 420)
    x = center[0] + radius * np.cos(phi)
    y = center[1] + radius * np.sin(phi)
    mask = y >= 0 if above else y <= 0
    ax.plot(
        np.ma.masked_where(~mask, x),
        np.ma.masked_where(~mask, y),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )


def make_wavelet_comparison(path: Path) -> None:
    frames = 168
    theta1 = np.deg2rad(46.0)
    speed_ratio = 1.0 / 1.55
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    step = 0.62
    spacing = 0.78
    x0 = -0.28
    p1 = d1[0] * x0
    p2 = d2[0] * x0

    upper_sources = np.array([x0, 0.0]) + np.array([0.38, 0.82, 1.26, 1.70])[:, None] * w1
    lower_sources = np.array([x0, 0.0]) + np.array([-0.36, -0.78, -1.20, -1.62])[:, None] * w2

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.25, color=PAPER, zorder=0)
        ax.axhspan(-2.25, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.55, zorder=5)
        ax.set_xlim(-1.85, 2.85)
        ax.set_ylim(-2.05, 1.95)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Fast wavelets outrun slow wavelets, so the envelope bends", fontsize=14.2, color=INK)
        ax.text(-1.72, 0.13, "fast medium", fontsize=9.5, color="#4B463F", zorder=20)
        ax.text(-1.72, -0.25, "slow medium", fontsize=9.5, color="#4B463F", zorder=20)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.78)
        q = q * q * (3.0 - 2.0 * q)

        for offset in range(-2, 5):
            value1 = p1 + offset * spacing
            x_cross = value1 / d1[0]
            value2 = d2[0] * x_cross
            clipped_front(
                ax,
                d1,
                w1,
                value1,
                above=True,
                color=BLUE,
                linewidth=1.35,
                alpha=0.28,
                zorder=2,
            )
            clipped_front(
                ax,
                d2,
                w2,
                value2,
                above=False,
                color=ORANGE,
                linewidth=1.35,
                alpha=0.28,
                zorder=2,
            )

        clipped_front(ax, d1, w1, p1, above=True, color=BLUE, linewidth=2.7, alpha=0.9, zorder=8)
        clipped_front(ax, d2, w2, p2, above=False, color=ORANGE, linewidth=2.7, alpha=0.9, zorder=8)

        r_fast = q * step
        r_slow = q * step * speed_ratio

        for center in upper_sources:
            clipped_circle(ax, center, r_fast, above=True, color=BLUE, linewidth=1.55, alpha=0.55, zorder=10)
            ax.scatter([center[0]], [center[1]], s=24, color=BLUE, edgecolor="white", linewidth=0.6, zorder=12)

        for center in lower_sources:
            clipped_circle(ax, center, r_slow, above=False, color=ORANGE, linewidth=1.55, alpha=0.6, zorder=10)
            ax.scatter([center[0]], [center[1]], s=24, color=ORANGE, edgecolor="white", linewidth=0.6, zorder=12)

        p1_next = p1 + q * step
        p2_next = p2 + q * step * speed_ratio
        clipped_front(ax, d1, w1, p1_next, above=True, color=BLUE, linewidth=3.0, alpha=0.64 + 0.26 * q, zorder=15)
        clipped_front(ax, d2, w2, p2_next, above=False, color=ORANGE, linewidth=3.0, alpha=0.64 + 0.26 * q, zorder=15)

        if q > 0.12:
            ax.text(
                0.94,
                1.42,
                "larger",
                fontsize=9.4,
                color=BLUE,
                alpha=0.74,
            )
            ax.text(
                0.48,
                -1.38,
                "smaller",
                fontsize=9.4,
                color=ORANGE,
                alpha=0.76,
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_wavelet_comparison(OUT / "lm-huygens-snell-wavelet-comparison-review.mp4")
