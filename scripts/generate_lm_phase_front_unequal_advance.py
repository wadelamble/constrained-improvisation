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
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def draw_segment(ax: plt.Axes, a: np.ndarray, b: np.ndarray, **kwargs) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], **kwargs)


def draw_extended_front(
    ax: plt.Axes,
    a: np.ndarray,
    b: np.ndarray,
    *,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    t = unit(b - a)
    c = 0.5 * (a + b)
    p0 = c - 2.0 * t
    p1 = c + 2.0 * t
    draw_segment(ax, p0, p1, color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)


def make_phase_front_unequal_advance(path: Path) -> None:
    frames = 156
    theta = np.deg2rad(46.0)
    old_normal = np.array([np.sin(theta), -np.cos(theta)])
    old_tangent = np.array([np.cos(theta), np.sin(theta)])

    # Two points on the same incoming phase front. A has just entered the slow
    # medium; B is still in the fast medium.
    A0 = np.array([-0.10, 0.00])
    B0 = A0 + 1.70 * old_tangent
    fast_step = 0.78
    slow_step = 0.34
    A1 = A0 + slow_step * old_normal
    B1 = B0 + fast_step * old_normal

    new_tangent = unit(B1 - A1)
    new_normal = unit(np.array([new_tangent[1], -new_tangent[0]]))
    if new_normal[1] > 0:
        new_normal = -new_normal

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.1, color=PAPER, zorder=0)
        ax.axhspan(-1.75, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.6, zorder=3)
        ax.set_xlim(-0.95, 2.55)
        ax.set_ylim(-1.45, 1.95)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Unequal advance rotates the phase front", fontsize=15, color=INK)
        ax.text(-0.86, 0.12, "fast medium", fontsize=10, color="#4B463F", zorder=20)
        ax.text(-0.86, -0.25, "slow medium", fontsize=10, color="#4B463F", zorder=20)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.76)
        q = q * q * (3.0 - 2.0 * q)
        reveal = min(1.0, max(0.0, (progress - 0.58) / 0.24))
        reveal = reveal * reveal * (3.0 - 2.0 * reveal)

        A = A0 + q * slow_step * old_normal
        B = B0 + q * fast_step * old_normal

        # A quiet incoming wavefront train, so the marked line reads as a transverse front.
        for offset in [-0.70, 0.70]:
            draw_extended_front(
                ax,
                A0 + offset * old_normal,
                B0 + offset * old_normal,
                color=BLUE,
                linewidth=1.25,
                alpha=0.22,
                zorder=2,
            )

        draw_extended_front(ax, A0, B0, color=BLUE, linewidth=2.4, alpha=0.36, zorder=4)
        draw_segment(ax, A, B, color=ORANGE, linewidth=3.0, alpha=0.94, zorder=8)

        ax.scatter([A0[0], B0[0]], [A0[1], B0[1]], s=34, color=BLUE, edgecolor="white", linewidth=0.7, alpha=0.75, zorder=10)
        ax.scatter([A[0], B[0]], [A[1], B[1]], s=58, color=[ORANGE, BLUE], edgecolor="white", linewidth=0.9, zorder=11)

        ax.annotate(
            "",
            xy=A,
            xytext=A0,
            arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.0, "alpha": 0.88},
            zorder=12,
        )
        ax.annotate(
            "",
            xy=B,
            xytext=B0,
            arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.2, "alpha": 0.88},
            zorder=12,
        )

        ax.text(A0[0] + 0.16, A0[1] - 0.42, "short advance", fontsize=10, color=ORANGE)
        ax.text(B0[0] + 0.10, B0[1] - 0.06, "long advance", fontsize=10, color=BLUE)
        ax.text(0.35, 1.25, "same phase front", fontsize=10, color=BLUE, alpha=0.82)
        ax.text(0.15, -0.98, "same time step", fontsize=10.5, color="#4B463F")

        if reveal > 0.02:
            mid_old = 0.5 * (A0 + B0)
            mid_new = 0.5 * (A1 + B1)
            ax.annotate(
                "",
                xy=mid_old + 0.72 * old_normal,
                xytext=mid_old - 0.10 * old_normal,
                arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.0, "alpha": 0.72 * reveal},
                zorder=14,
            )
            ax.annotate(
                "",
                xy=mid_new + 0.78 * new_normal,
                xytext=mid_new - 0.10 * new_normal,
                arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2, "alpha": 0.86 * reveal},
                zorder=14,
            )
            ax.text(mid_new[0] + 0.16, mid_new[1] - 0.18, "new ray", fontsize=10, color=ORANGE, alpha=reveal)

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_phase_front_unequal_advance(OUT / "lm-phase-front-unequal-advance-review.mp4")
