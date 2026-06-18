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
BAND = "#E8F2F7"
EDGE = "#7E7468"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def clipped_line(
    ax: plt.Axes,
    point: np.ndarray,
    tangent: np.ndarray,
    *,
    above: bool,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    u = np.linspace(-5.0, 5.0, 700)
    pts = point[:, None] + tangent[:, None] * u
    mask = pts[1] >= 0 if above else pts[1] <= 0
    x = np.ma.masked_where(~mask, pts[0])
    y = np.ma.masked_where(~mask, pts[1])
    ax.plot(x, y, color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)


def make_huygens_snell_crossing(path: Path) -> None:
    frames = 156
    theta1 = np.deg2rad(50.0)
    v1 = 1.0
    v2 = 1.0 / 1.55
    theta2 = np.arcsin((v2 / v1) * np.sin(theta1))

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    source_x = np.linspace(-0.18, 2.05, 6)
    source_phase = source_x * np.sin(theta1)

    fig, ax = plt.subplots(figsize=(8.8, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup_axes() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.0, color=PAPER, zorder=0)
        ax.axhspan(-2.15, 0, color=BAND, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.6, zorder=3)
        ax.set_xlim(-1.25, 2.75)
        ax.set_ylim(-2.05, 1.75)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("A refracted front is the envelope of slower wavelets", fontsize=14, color=INK)
        ax.text(-1.15, 0.12, "fast medium", fontsize=9.8, color="#4B463F")
        ax.text(-1.15, -0.25, "slow medium", fontsize=9.8, color="#4B463F")

    def draw_frame(frame: int):
        setup_axes()
        t = frame / (frames - 1)
        smooth = t * t * (3.0 - 2.0 * t)
        phase = -1.05 + 3.35 * smooth

        front_point = phase * d1
        clipped_line(
            ax,
            front_point,
            w1,
            above=True,
            color=BLUE,
            linewidth=2.35,
            alpha=0.9,
            zorder=7,
        )
        if phase < 1.35:
            ax.text(front_point[0] - 0.22, min(1.55, front_point[1] + 0.55), "incoming front", fontsize=9.3, color=BLUE)

        envelope_ready = np.count_nonzero(phase - source_phase > 0.2) >= 3
        tangent_points = []

        for x0, hit_phase in zip(source_x, source_phase):
            age = phase - hit_phase
            if age < 0:
                dot = np.array([x0, 0.0]) + age * d1
                if -1.5 < dot[0] < 2.9 and 0.0 <= dot[1] < 1.8:
                    ax.scatter([dot[0]], [dot[1]], s=42, color=BLUE, edgecolor="white", linewidth=0.8, zorder=9)
                    ax.plot([dot[0], x0], [dot[1], 0.0], color=BLUE, linewidth=0.8, alpha=0.16, zorder=4)
            else:
                radius = v2 * age
                alpha = max(0.22, 0.68 - 0.18 * radius)
                phi = np.linspace(np.pi, 2.0 * np.pi, 170)
                ax.plot(
                    x0 + radius * np.cos(phi),
                    radius * np.sin(phi),
                    color=ORANGE,
                    linewidth=1.45,
                    alpha=alpha,
                    zorder=5,
                )
                ax.scatter([x0], [0], s=34, color=ORANGE, edgecolor="white", linewidth=0.7, zorder=10)
                if age > 0.08:
                    tangent_points.append(np.array([x0, 0.0]) + radius * d2)

        if envelope_ready and len(tangent_points) >= 2:
            p0 = tangent_points[0] - 0.18 * w2
            p1 = tangent_points[-1] + 0.18 * w2
            ax.plot(
                [p0[0], p1[0]],
                [p0[1], p1[1]],
                color=ORANGE,
                linewidth=3.0,
                alpha=0.92,
                zorder=11,
            )
            midpoint = 0.5 * (p0 + p1)
            ax.text(midpoint[0] + 0.08, midpoint[1] - 0.15, "new front", fontsize=9.5, color=ORANGE)

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_crossing(OUT / "lm-huygens-snell-crossing-clean-review.mp4")
