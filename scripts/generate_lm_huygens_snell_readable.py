from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def draw_line_segment(ax: plt.Axes, p0: np.ndarray, p1: np.ndarray, **kwargs) -> None:
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], **kwargs)


def draw_wavefront_through(
    ax: plt.Axes,
    point: np.ndarray,
    tangent: np.ndarray,
    length: float,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int = 4,
) -> None:
    p0 = point - 0.5 * length * tangent
    p1 = point + 0.5 * length * tangent
    draw_line_segment(ax, p0, p1, color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)


def make_huygens_snell_readable(path: Path) -> None:
    frames = 150
    theta1 = np.deg2rad(52.0)
    v1 = 1.0
    v2 = 1.0 / 1.55
    theta2 = np.arcsin((v2 / v1) * np.sin(theta1))

    A = np.array([0.0, 0.0])
    C = np.array([2.45, 0.0])
    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    v1_dt = C[0] * np.sin(theta1)
    v2_dt = (v2 / v1) * v1_dt
    B = C - v1_dt * d1
    D = C - (C @ w2) * w2

    fig, ax = plt.subplots(figsize=(8.8, 6.6))
    fig.patch.set_facecolor("#F7F3EC")

    def setup_axes() -> None:
        ax.clear()
        ax.set_facecolor("#FFFDF8")
        ax.axhspan(-2.1, 0, color="#E8F2F7", zorder=0)
        ax.axhspan(0, 2.05, color="#FFFDF8", zorder=0)
        ax.axhline(0, color="#6F685F", linewidth=1.7, zorder=2)
        ax.set_xlim(-0.65, 3.05)
        ax.set_ylim(-1.85, 1.75)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.text(-0.55, 0.12, "fast medium", fontsize=10, color="#4B463F")
        ax.text(-0.55, -0.23, "slow medium", fontsize=10, color="#4B463F")
        ax.set_title("Huygens construction gives the refracted wavefront", fontsize=14, color="#2F2F2F")

    def draw_frame(frame: int):
        setup_axes()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.72)
        ease = q * q * (3.0 - 2.0 * q)
        reveal = max(0.0, (progress - 0.58) / 0.28)
        reveal = min(1.0, reveal * reveal * (3.0 - 2.0 * reveal))

        Bq = B + ease * v1_dt * d1
        radius = ease * v2_dt

        draw_line_segment(ax, A, B, color="#355070", linewidth=2.3, alpha=0.85, zorder=5)
        ax.text(B[0] - 0.03, B[1] + 0.12, "incoming front", fontsize=9.4, color="#355070")

        ax.annotate(
            "",
            xy=Bq,
            xytext=B,
            arrowprops={"arrowstyle": "->", "color": "#355070", "linewidth": 2.0},
            zorder=6,
        )
        ax.text((B[0] + C[0]) / 2 + 0.04, (B[1] + C[1]) / 2 + 0.09, r"$v_1\Delta t$", fontsize=10.2, color="#355070")

        if radius > 0.01:
            phi = np.linspace(-np.pi, 0, 180)
            ax.plot(
                A[0] + radius * np.cos(phi),
                A[1] + radius * np.sin(phi),
                color="#B85C38",
                linewidth=2.0,
                alpha=0.78,
                zorder=4,
            )
            ax.annotate(
                "",
                xy=A + radius * d2,
                xytext=A,
                arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 1.8, "alpha": 0.75},
                zorder=5,
            )
            ax.text(A[0] + 0.25, A[1] - 0.45, r"$v_2\Delta t$", fontsize=10.2, color="#B85C38")

        ax.scatter([A[0], B[0], Bq[0]], [A[1], B[1], Bq[1]], s=[58, 42, 42], color=["#2F2F2F", "#355070", "#355070"], edgecolor="white", linewidth=0.9, zorder=8)
        ax.text(A[0] - 0.12, A[1] + 0.11, "A", fontsize=11, color="#2F2F2F")
        ax.text(B[0] - 0.11, B[1] + 0.02, "B", fontsize=11, color="#355070")

        if ease > 0.98:
            ax.scatter([C[0], D[0]], [C[1], D[1]], s=[48, 46], color=["#355070", "#B85C38"], edgecolor="white", linewidth=0.9, zorder=8)
            ax.text(C[0] + 0.05, C[1] + 0.09, "C", fontsize=11, color="#355070")
            ax.text(D[0] - 0.16, D[1] - 0.13, "D", fontsize=11, color="#B85C38")

        if reveal > 0.02:
            draw_line_segment(
                ax,
                D - 0.16 * w2,
                C + 0.28 * w2,
                color="#B85C38",
                linewidth=2.6,
                alpha=0.9 * reveal,
                zorder=7,
            )
            ax.annotate(
                "",
                xy=A + 1.65 * d2 * reveal,
                xytext=A,
                arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 2.1, "alpha": 0.9 * reveal},
                zorder=7,
            )
            ax.text(0.52, -1.42, "refracted front is tangent to the wavelet", fontsize=9.6, color="#B85C38", alpha=reveal)

        if progress > 0.80:
            ax.text(
                -0.48,
                -1.62,
                r"same $\Delta t$: the fast-medium point reaches C, while A's wavelet is smaller",
                fontsize=9.6,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.25", "fc": "#FFFDF8", "ec": "#D7C6AA"},
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_readable(OUT / "lm-huygens-snell-readable-review.mp4")
