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


def make_wavefront_train(path: Path) -> None:
    frames = 168
    theta1 = np.deg2rad(46.0)
    speed_ratio = 1.0 / 1.55
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    spacing1 = 0.72
    source_xs = np.arange(-1.9, 3.05, 0.42)

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.25, color=PAPER, zorder=0)
        ax.axhspan(-2.25, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.55, zorder=5)
        ax.set_xlim(-2.05, 3.05)
        ax.set_ylim(-2.05, 1.95)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Huygens wavelets bend a wavefront at a slower medium", fontsize=14.5, color=INK)
        ax.text(-1.94, 0.13, "fast medium", fontsize=9.5, color="#4B463F", zorder=20)
        ax.text(-1.94, -0.25, "slow medium", fontsize=9.5, color="#4B463F", zorder=20)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        phase = -0.55 + 3.75 * progress

        visible_values = [phase - index * spacing1 for index in range(-4, 9)]

        for value in visible_values:
            if -2.8 < value < 3.2:
                active = abs(value - phase) < 1e-9
                clipped_front(
                    ax,
                    d1,
                    w1,
                    value,
                    above=True,
                    color=BLUE,
                    linewidth=2.3 if active else 1.35,
                    alpha=0.92 if active else 0.34,
                    zorder=12 if active else 3,
                )

        for value in visible_values:
            if value <= 0:
                continue
            active = abs(value - phase) < 1e-9
            clipped_front(
                ax,
                d2,
                w2,
                speed_ratio * value,
                above=False,
                color=ORANGE,
                linewidth=2.75 if active else 1.35,
                alpha=0.92 if active else 0.34,
                zorder=14 if active else 4,
            )

        for x0 in source_xs:
            age = phase - x0 * np.sin(theta1)
            if not (0.03 < age < 1.55):
                continue
            radius = speed_ratio * age
            phi = np.linspace(np.pi, 2.0 * np.pi, 190)
            alpha = 0.34 + 0.38 * (1.0 - min(1.0, age / 1.55))
            ax.plot(
                x0 + radius * np.cos(phi),
                radius * np.sin(phi),
                color=ORANGE,
                linewidth=1.45,
                alpha=alpha,
                zorder=9,
            )
            ax.scatter([x0], [0], s=22, color=ORANGE, edgecolor="white", linewidth=0.55, alpha=0.8, zorder=16)

            tangent_point = np.array([x0, 0.0]) + radius * d2
            if -2.05 < tangent_point[0] < 3.05 and -2.05 < tangent_point[1] < 0:
                ax.scatter(
                    [tangent_point[0]],
                    [tangent_point[1]],
                    s=11,
                    color=ORANGE,
                    alpha=0.55,
                    zorder=15,
                )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_wavefront_train(OUT / "lm-huygens-snell-wavefront-train-review.mp4")
