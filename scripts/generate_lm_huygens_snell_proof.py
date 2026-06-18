from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Arc


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


def segment(ax: plt.Axes, p0: np.ndarray, p1: np.ndarray, **kwargs) -> None:
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], **kwargs)


def label_point(ax: plt.Axes, p: np.ndarray, label: str, dx: float, dy: float, color: str = INK) -> None:
    ax.text(p[0] + dx, p[1] + dy, label, fontsize=12, color=color, weight="bold")


def make_huygens_snell_proof(path: Path) -> None:
    frames = 150
    theta1 = np.deg2rad(48.0)
    v_ratio = 1.0 / 1.55
    theta2 = np.arcsin(v_ratio * np.sin(theta1))

    A = np.array([0.0, 0.0])
    AC = 2.6
    C = np.array([AC, 0.0])

    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])

    BC = AC * np.sin(theta1)
    AD = v_ratio * BC
    B = C - BC * d1
    D = A + AD * d2

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 1.95, color=PAPER, zorder=0)
        ax.axhspan(-1.95, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.6, zorder=2)
        ax.set_xlim(-0.65, 3.05)
        ax.set_ylim(-1.65, 1.7)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Huygens construction of Snell's law", fontsize=15, color=INK)
        ax.text(-0.56, 0.12, "medium 1", fontsize=10, color="#4B463F")
        ax.text(-0.56, -0.25, "medium 2", fontsize=10, color="#4B463F")

    def draw_static_geometry(q: float) -> tuple[np.ndarray, float]:
        B_now = B + q * BC * d1
        radius = q * AD

        segment(ax, A, B, color=BLUE, linewidth=2.4, alpha=0.88, zorder=5)
        segment(ax, B, C, color=BLUE, linewidth=1.5, alpha=0.26, linestyle="--", zorder=4)
        segment(ax, A, C, color="#7E7468", linewidth=1.2, alpha=0.45, zorder=3)

        ax.scatter([A[0]], [A[1]], s=62, color=INK, edgecolor="white", linewidth=0.9, zorder=9)
        ax.scatter([B_now[0]], [B_now[1]], s=58, color=BLUE, edgecolor="white", linewidth=0.9, zorder=9)
        label_point(ax, A, "A", 0.04, 0.09)
        if q < 0.98:
            ax.text(B_now[0] + 0.05, B_now[1] + 0.06, "B", fontsize=11, color=BLUE, weight="bold")

        if q > 0.02:
            phi = np.linspace(-np.pi, 0, 220)
            ax.plot(
                A[0] + radius * np.cos(phi),
                A[1] + radius * np.sin(phi),
                color=ORANGE,
                linewidth=2.1,
                alpha=0.82,
                zorder=6,
            )

        if q > 0.08:
            segment(ax, A, A + radius * d2, color=ORANGE, linewidth=1.9, alpha=0.72, zorder=7)

        if q > 0.98:
            ax.scatter([C[0], D[0]], [C[1], D[1]], s=58, color=[BLUE, ORANGE], edgecolor="white", linewidth=0.9, zorder=10)
            label_point(ax, C, "C", 0.06, 0.08, BLUE)
            label_point(ax, D, "D", 0.05, -0.03, ORANGE)

        return B_now, radius

    def draw_final_proof(reveal: float) -> None:
        alpha = reveal
        segment(ax, D, C, color=ORANGE, linewidth=2.9, alpha=0.92 * alpha, zorder=11)
        segment(ax, A, D, color=ORANGE, linewidth=2.0, alpha=0.82 * alpha, zorder=10)

        arc1 = Arc(A, 0.55, 0.55, angle=0, theta1=0, theta2=np.rad2deg(theta1), color=BLUE, linewidth=1.4, alpha=alpha)
        arc2 = Arc(C, 0.55, 0.55, angle=0, theta1=180, theta2=180 + np.rad2deg(theta2), color=ORANGE, linewidth=1.4, alpha=alpha)
        ax.add_patch(arc1)
        ax.add_patch(arc2)

        t1_mid = 0.5 * theta1
        t2_mid = np.pi + 0.5 * theta2
        ax.text(A[0] + 0.38 * np.cos(t1_mid), A[1] + 0.38 * np.sin(t1_mid), r"$\theta_1$", fontsize=12, color=BLUE, alpha=alpha)
        ax.text(C[0] + 0.38 * np.cos(t2_mid), C[1] + 0.38 * np.sin(t2_mid), r"$\theta_2$", fontsize=12, color=ORANGE, alpha=alpha)

        ax.text(1.35, 0.08, r"$AC$", fontsize=11, color="#5A5147", alpha=alpha)
        ax.text(1.95, 0.74, r"$BC=v_1\Delta t$", fontsize=11, color=BLUE, alpha=alpha)
        ax.text(0.26, -0.57, r"$AD=v_2\Delta t$", fontsize=11, color=ORANGE, alpha=alpha)
        ax.text(
            0.14,
            -1.45,
            r"$\sin\theta_1=\frac{BC}{AC},\quad \sin\theta_2=\frac{AD}{AC}\quad\Rightarrow\quad"
            r"\frac{\sin\theta_1}{v_1}=\frac{\sin\theta_2}{v_2}$",
            fontsize=12,
            color=INK,
            alpha=alpha,
            bbox={"boxstyle": "round,pad=0.35", "fc": PAPER, "ec": "#D7C6AA", "alpha": 0.95 * alpha},
        )

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.64)
        q = q * q * (3.0 - 2.0 * q)
        reveal = min(1.0, max(0.0, (progress - 0.62) / 0.24))
        reveal = reveal * reveal * (3.0 - 2.0 * reveal)

        B_now, radius = draw_static_geometry(q)

        if q < 0.98:
            ax.annotate(
                "",
                xy=B_now,
                xytext=B,
                arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.0, "alpha": 0.8},
                zorder=8,
            )
            ax.text(0.14, -1.45, r"after the same $\Delta t$, B reaches C while A's wavelet grows in medium 2", fontsize=11, color="#4B463F")
        else:
            draw_final_proof(reveal)

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_proof(OUT / "lm-huygens-snell-proof-review.mp4")
