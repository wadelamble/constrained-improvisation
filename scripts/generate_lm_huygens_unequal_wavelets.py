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


def unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def segment(ax: plt.Axes, a: np.ndarray, b: np.ndarray, **kwargs) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], **kwargs)


def front_line(ax: plt.Axes, center: np.ndarray, tangent: np.ndarray, length: float, **kwargs) -> None:
    a = center - 0.5 * length * tangent
    b = center + 0.5 * length * tangent
    segment(ax, a, b, **kwargs)


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
    phi = np.linspace(0.0, 2.0 * np.pi, 520)
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


def make_huygens_unequal_wavelets(path: Path) -> None:
    frames = 156
    theta = np.deg2rad(46.0)
    old_normal = np.array([np.sin(theta), -np.cos(theta)])
    old_tangent = np.array([np.cos(theta), np.sin(theta)])

    slow_source = np.array([-0.22, -0.06])
    separation = 1.58
    fast_source = slow_source + separation * old_tangent
    slow_radius = 0.36
    fast_radius = 0.78

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.05, color=PAPER, zorder=0)
        ax.axhspan(-1.75, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.55, zorder=4)
        ax.set_xlim(-0.95, 2.55)
        ax.set_ylim(-1.45, 1.85)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Huygens wavelets rotate the phase front", fontsize=15, color=INK)
        ax.text(-0.85, 0.12, "fast medium", fontsize=10, color="#4B463F", zorder=30)
        ax.text(-0.85, -0.25, "slow medium", fontsize=10, color="#4B463F", zorder=30)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.78)
        q = q * q * (3.0 - 2.0 * q)

        k = q * (slow_radius - fast_radius) / separation
        new_normal = unit(k * old_tangent + np.sqrt(max(0.0, 1.0 - k * k)) * old_normal)
        new_tangent = np.array([new_normal[1], -new_normal[0]])
        if np.dot(new_tangent, old_tangent) < 0:
            new_tangent = -new_tangent

        slow_touch = slow_source + q * slow_radius * new_normal
        fast_touch = fast_source + q * fast_radius * new_normal
        new_center = 0.5 * (slow_touch + fast_touch)

        for offset in [-0.64, 0.64]:
            front_line(
                ax,
                0.5 * (slow_source + fast_source) + offset * old_normal,
                old_tangent,
                3.2,
                color=BLUE,
                linewidth=1.25,
                alpha=0.20,
                zorder=1,
            )
        segment(ax, slow_source, fast_source, color=BLUE, linewidth=2.6, alpha=0.84, zorder=7)
        ax.text(0.32, 0.82, "old phase front", fontsize=9.7, color=BLUE, alpha=0.84)

        clipped_circle(
            ax,
            fast_source,
            q * fast_radius,
            above=True,
            color=BLUE,
            linewidth=1.85,
            alpha=0.54,
            zorder=8,
        )
        clipped_circle(
            ax,
            slow_source,
            q * slow_radius,
            above=False,
            color=ORANGE,
            linewidth=2.15,
            alpha=0.78,
            zorder=9,
        )

        ax.scatter(
            [slow_source[0], fast_source[0]],
            [slow_source[1], fast_source[1]],
            s=52,
            color=[ORANGE, BLUE],
            edgecolor="white",
            linewidth=0.8,
            zorder=12,
        )
        ax.scatter(
            [slow_touch[0], fast_touch[0]],
            [slow_touch[1], fast_touch[1]],
            s=38,
            color=[ORANGE, BLUE],
            edgecolor="white",
            linewidth=0.65,
            alpha=0.85,
            zorder=13,
        )

        front_line(
            ax,
            new_center,
            new_tangent,
            2.45,
            color=ORANGE,
            linewidth=3.0,
            alpha=0.92,
            zorder=14,
        )

        ax.text(fast_source[0] + 0.20, fast_source[1] + 0.26, "larger fast wavelet", fontsize=9.5, color=BLUE, alpha=0.76)
        ax.text(slow_source[0] + 0.16, slow_source[1] - 0.48, "smaller slow wavelet", fontsize=9.5, color=ORANGE, alpha=0.86)
        ax.text(new_center[0] + 0.13, new_center[1] - 0.16, "new phase front", fontsize=9.7, color=ORANGE, alpha=0.86)

        if q > 0.70:
            old_mid = 0.5 * (slow_source + fast_source)
            ax.annotate(
                "",
                xy=old_mid + 0.70 * old_normal,
                xytext=old_mid - 0.08 * old_normal,
                arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.0, "alpha": 0.72},
                zorder=16,
            )
            ax.annotate(
                "",
                xy=new_center + 0.80 * new_normal,
                xytext=new_center - 0.06 * new_normal,
                arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2, "alpha": 0.86},
                zorder=16,
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_unequal_wavelets(OUT / "lm-huygens-unequal-wavelets-review.mp4")
