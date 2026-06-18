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
    )


def draw_clipped_circle(
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
    phi = np.linspace(0.0, 2.0 * np.pi, 460)
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


def make_two_speed_reference(path: Path) -> None:
    frames = 168
    theta1 = np.deg2rad(46.0)
    speed_ratio = 1.0 / 1.55
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    spacing = 0.70
    blue_dt = 0.50
    boundary_sources = np.arange(-1.85, 3.05, 0.42)

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.2, color=PAPER, zorder=0)
        ax.axhspan(-2.2, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.55, zorder=8)
        ax.set_xlim(-2.0, 3.05)
        ax.set_ylim(-2.0, 1.9)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Fast wavelets make a farther envelope; slow wavelets bend it", fontsize=14.0, color=INK)
        ax.text(-1.88, 0.13, "fast medium", fontsize=9.6, color="#4B463F", zorder=30)
        ax.text(-1.88, -0.25, "slow medium", fontsize=9.6, color="#4B463F", zorder=30)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        phase = -0.42 + 2.45 * progress

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
                    linewidth=2.55 if active else 1.20,
                    alpha=0.90 if active else 0.30,
                    zorder=18 if active else 3,
                )
            if value > -0.05:
                draw_front(
                    ax,
                    d2,
                    w2,
                    speed_ratio * value,
                    above=False,
                    color=ORANGE,
                    linewidth=3.0 if n == 0 else 1.20,
                    alpha=0.92 if n == 0 else 0.28,
                    zorder=22 if n == 0 else 4,
                )

        # Fast reference wavelets entirely in the upper medium.
        old_blue_phase = phase - blue_dt
        blue_source_ys = np.array([0.42, 0.76, 1.10, 1.44])
        for y_target in blue_source_ys:
            u = (y_target - old_blue_phase * d1[1]) / w1[1]
            center = old_blue_phase * d1 + u * w1
            if center[1] <= 0.08 or not (-1.9 < center[0] < 2.9):
                continue
            draw_clipped_circle(
                ax,
                center,
                blue_dt,
                above=True,
                color=BLUE,
                linewidth=1.55,
                alpha=0.48,
                zorder=12,
            )
            ax.scatter([center[0]], [center[1]], s=22, color=BLUE, edgecolor="white", linewidth=0.6, zorder=20)
        draw_front(
            ax,
            d1,
            w1,
            phase,
            above=True,
            color=BLUE,
            linewidth=2.85,
            alpha=0.80,
            zorder=24,
        )

        # Slow transmitted wavelets entirely in the lower medium.
        for x0 in boundary_sources:
            age = phase - d1[0] * x0
            if not (0.04 < age < 1.45):
                continue
            radius = speed_ratio * age
            draw_clipped_circle(
                ax,
                np.array([x0, 0.0]),
                radius,
                above=False,
                color=ORANGE,
                linewidth=1.55,
                alpha=0.66,
                zorder=16,
            )
            ax.scatter([x0], [0], s=22, color=ORANGE, edgecolor="white", linewidth=0.55, zorder=25)

        x_cross = phase / d1[0]
        if -1.75 < x_cross < 2.9:
            hit = np.array([x_cross, 0.0])
            ax.annotate(
                "",
                xy=hit,
                xytext=hit - 1.12 * d1,
                arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.1, "alpha": 0.86},
                zorder=26,
            )
            ax.annotate(
                "",
                xy=hit + 1.16 * d2,
                xytext=hit + 0.04 * d2,
                arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2, "alpha": 0.86},
                zorder=26,
            )

        if progress > 0.18:
            ax.text(1.82, 1.55, "fast wavelets", fontsize=9.1, color=BLUE, alpha=0.82)
            ax.text(1.82, -1.55, "slower wavelets", fontsize=9.1, color=ORANGE, alpha=0.86)

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_two_speed_reference(OUT / "lm-huygens-snell-two-speed-reference-review.mp4")
