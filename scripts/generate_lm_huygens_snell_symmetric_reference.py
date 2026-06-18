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
        bitrate=2800,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(PAPER)
    ax.grid(color="#DDD5C8", linewidth=0.8, alpha=0.65)
    for spine in ax.spines.values():
        spine.set_color("#B9AA98")


def draw_clipped_wavefront(
    ax: plt.Axes,
    d: np.ndarray,
    w: np.ndarray,
    phase_distance: float,
    keep_above: bool,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
    linestyle: str | tuple = "-",
) -> None:
    u = np.linspace(-4.8, 4.8, 650)
    pts = phase_distance * d[:, None] + w[:, None] * u
    mask = pts[1] >= 0 if keep_above else pts[1] <= 0
    ax.plot(
        np.ma.masked_where(~mask, pts[0]),
        np.ma.masked_where(~mask, pts[1]),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
        linestyle=linestyle,
    )


def draw_clipped_circle(
    ax: plt.Axes,
    center: np.ndarray,
    radius: float,
    keep_above: bool,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    if radius <= 0.01:
        return
    phi = np.linspace(0, 2.0 * np.pi, 440)
    x = center[0] + radius * np.cos(phi)
    y = center[1] + radius * np.sin(phi)
    mask = y >= 0 if keep_above else y <= 0
    ax.plot(
        np.ma.masked_where(~mask, x),
        np.ma.masked_where(~mask, y),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )


def draw_band_clipped_circle(
    ax: plt.Axes,
    center: np.ndarray,
    radius: float,
    y_min: float,
    y_max: float,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    if radius <= 0.01:
        return
    phi = np.linspace(0, 2.0 * np.pi, 440)
    x = center[0] + radius * np.cos(phi)
    y = center[1] + radius * np.sin(phi)
    mask = (y >= y_min) & (y <= y_max)
    ax.plot(
        np.ma.masked_where(~mask, x),
        np.ma.masked_where(~mask, y),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )


def make_huygens_snell_synthesis(path: Path) -> None:
    frames = 168
    n1 = 1.0
    n2 = 1.55
    theta1 = np.deg2rad(46.0)
    theta2 = np.arcsin((n1 / n2) * np.sin(theta1))
    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])
    spacing1 = 0.56
    spacing2 = spacing1 / n2
    reference_y = 1.18

    fig, ax = plt.subplots(figsize=(8.8, 7.0))
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle("Huygens wavelets make the refracted front pivot", fontsize=15, color=INK, y=0.965)

    def draw_frame(frame: int):
        ax.clear()
        progress = frame / (frames - 1)
        smooth = progress * progress * (3.0 - 2.0 * progress)
        phase = -1.05 + 3.30 * smooth

        style_axes(ax)
        ax.axhspan(0, 2.55, color=PAPER, zorder=0)
        ax.axhspan(-2.55, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.6, zorder=4)
        ax.set_xlim(-2.75, 2.75)
        ax.set_ylim(-2.35, 2.35)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("same elapsed time: fast wavelets reach farther than slow wavelets", fontsize=12.2, color=INK)
        ax.text(-2.62, 0.12, "fast medium", fontsize=9.8, color="#4B463F", zorder=30)
        ax.text(-2.62, -0.32, "slow medium", fontsize=9.8, color="#4B463F", zorder=30)

        start = -2.55 * d1
        end = 2.55 * d2
        ax.annotate("", xy=(0, 0), xytext=start, arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.2}, zorder=24)
        ax.annotate("", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2}, zorder=24)
        ax.text(start[0] - 0.1, start[1] + 0.1, "incoming ray", fontsize=9.2, color=BLUE)
        ax.text(end[0] + 0.05, end[1] - 0.12, "bent ray", fontsize=9.2, color=ORANGE)

        # Moving transverse incident fronts.
        for index in range(-3, 7):
            p = phase - index * spacing1
            if -2.6 < p < 2.8:
                active = index == 0
                draw_clipped_wavefront(
                    ax,
                    d1,
                    w1,
                    p,
                    True,
                    BLUE,
                    2.2 if active else 1.15,
                    0.84 if active else 0.32,
                    18 if active else 2,
                )

        # Fast-medium Huygens reference, mirroring the orange boundary construction.
        ax.axhline(reference_y, color=BLUE, linewidth=1.1, alpha=0.32, linestyle=(0, (5, 4)), zorder=5)
        ax.text(-2.62, reference_y + 0.08, "reference", fontsize=9.2, color=BLUE, alpha=0.72, zorder=30)
        reference_points = np.linspace(-1.7, 2.7, 12)
        for xb in reference_points:
            source_phase = d1[0] * xb + d1[1] * reference_y
            age = phase - source_phase
            if 0.0 < age < 1.55:
                center = np.array([xb, reference_y])
                draw_band_clipped_circle(ax, center, age, 0.0, reference_y, BLUE, 1.05, 0.34, 12)
                ax.scatter([xb], [reference_y], s=20, color=BLUE, alpha=0.74, edgecolor="white", linewidth=0.4, zorder=21)
                tangent_point = center + age * d1
                if -2.4 < tangent_point[0] < 2.75 and 0.02 < tangent_point[1] < reference_y:
                    ax.scatter(
                        [tangent_point[0]],
                        [tangent_point[1]],
                        s=13,
                        color=BLUE,
                        alpha=0.82,
                        zorder=23,
                    )

        # Moving transmitted fronts below; the active one is the Huygens envelope.
        active_p2 = phase / n2
        if phase > -0.05:
            for index in range(0, 8):
                p2 = active_p2 - index * spacing2
                if -0.2 < p2 < 2.2:
                    active = index == 0
                    draw_clipped_wavefront(
                        ax,
                        d2,
                        w2,
                        p2,
                        False,
                        ORANGE,
                        3.0 if active else 1.15,
                        0.94 if active else 0.34,
                        22 if active else 3,
                    )
                    if active:
                        draw_clipped_wavefront(
                            ax,
                            d2,
                            w2,
                            p2,
                            True,
                            ORANGE,
                            1.35,
                            0.34,
                            11,
                            linestyle=(0, (4, 4)),
                        )

        # Slow-medium Huygens wavelets born where the incident front reaches the boundary.
        boundary_points = np.linspace(-1.7, 1.7, 9)
        for xb in boundary_points:
            age = phase - d1[0] * xb
            if 0.0 < age < 1.85:
                radius = age / n2
                draw_clipped_circle(ax, np.array([xb, 0.0]), radius, False, ORANGE, 1.15, 0.42, 14)
                ax.scatter([xb], [0], s=20, color=ORANGE, alpha=0.74, edgecolor="white", linewidth=0.4, zorder=21)
                tangent_point = np.array([xb, 0.0]) + radius * d2
                if -2.4 < tangent_point[0] < 2.75 and -2.2 < tangent_point[1] < -0.02:
                    ax.scatter(
                        [tangent_point[0]],
                        [tangent_point[1]],
                        s=13,
                        color=ORANGE,
                        alpha=0.82,
                        zorder=23,
                    )

        current_hit_x = phase / d1[0]
        if -1.65 <= current_hit_x <= 1.65:
            ax.scatter([current_hit_x], [0], s=48, color=INK, edgecolor="white", linewidth=0.8, zorder=26)
            ax.text(
                0.04,
                0.06,
                "the lower envelope pivots because\nits wavelets grow less in the same time",
                transform=ax.transAxes,
                ha="left",
                va="bottom",
                fontsize=9.3,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.25", "fc": PAPER, "ec": "#D7C6AA"},
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_synthesis(OUT / "lm-huygens-snell-symmetric-reference-review.mp4")
