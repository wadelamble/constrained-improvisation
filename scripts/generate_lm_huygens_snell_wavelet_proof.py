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


def draw_segment(ax: plt.Axes, a: np.ndarray, b: np.ndarray, **kwargs) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], **kwargs)


def draw_front(
    ax: plt.Axes,
    point: np.ndarray,
    tangent: np.ndarray,
    *,
    above: bool | None,
    color: str,
    linewidth: float,
    alpha: float,
    zorder: int,
) -> None:
    u = np.linspace(-5.0, 5.0, 800)
    pts = point[:, None] + tangent[:, None] * u
    if above is None:
        mask = np.ones_like(pts[1], dtype=bool)
    elif above:
        mask = pts[1] >= 0
    else:
        mask = pts[1] <= 0
    ax.plot(
        np.ma.masked_where(~mask, pts[0]),
        np.ma.masked_where(~mask, pts[1]),
        color=color,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )


def draw_circle_clip(
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
    phi = np.linspace(0.0, 2.0 * np.pi, 500)
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


def make_huygens_snell_wavelet_proof(path: Path) -> None:
    frames = 168
    theta1 = np.deg2rad(48.0)
    speed_ratio = 1.0 / 1.55
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    ray1 = np.array([np.sin(theta1), -np.cos(theta1)])
    front1 = np.array([np.cos(theta1), np.sin(theta1)])
    ray2 = np.array([np.sin(theta2), -np.cos(theta2)])
    front2 = np.array([np.cos(theta2), np.sin(theta2)])

    A = np.array([0.0, 0.0])
    AC = 2.55
    C = np.array([AC, 0.0])
    fast_radius = AC * np.sin(theta1)
    slow_radius = speed_ratio * fast_radius
    B = C - fast_radius * ray1
    D = A + slow_radius * ray2

    source_us = np.array([0.62, 1.28])
    sources = [A + u * front1 for u in source_us]

    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.clear()
        ax.set_facecolor(PAPER)
        ax.axhspan(0, 2.1, color=PAPER, zorder=0)
        ax.axhspan(-1.95, 0, color=SLOW, zorder=0)
        ax.axhline(0, color=EDGE, linewidth=1.55, zorder=4)
        ax.set_xlim(-0.62, 3.12)
        ax.set_ylim(-1.75, 1.85)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#B9AA98")
        ax.set_title("Huygens wavelets: faster above, slower below", fontsize=15, color=INK)
        ax.text(-0.53, 0.12, "fast medium", fontsize=10, color="#4B463F", zorder=30)
        ax.text(-0.53, -0.25, "slow medium", fontsize=10, color="#4B463F", zorder=30)

    def draw_frame(frame: int):
        setup()
        progress = frame / (frames - 1)
        q = min(1.0, progress / 0.76)
        q = q * q * (3.0 - 2.0 * q)
        reveal = min(1.0, max(0.0, (progress - 0.55) / 0.30))
        reveal = reveal * reveal * (3.0 - 2.0 * reveal)

        r_fast = q * fast_radius
        r_slow = q * slow_radius
        Cq = B + q * fast_radius * ray1
        Dq = A + q * slow_radius * ray2

        # Incoming transverse wavefronts.
        for offset in [-0.72, 0.72]:
            draw_front(
                ax,
                A + offset * ray1,
                front1,
                above=True,
                color=BLUE,
                linewidth=1.25,
                alpha=0.24,
                zorder=1,
            )
        draw_segment(ax, A, B, color=BLUE, linewidth=2.7, alpha=0.88, zorder=8)
        ax.text(0.24, 0.72, "old wavefront", fontsize=9.7, color=BLUE, alpha=0.86)

        # Fast-medium Huygens wavelets and their next envelope.
        for source in sources:
            draw_circle_clip(
                ax,
                source,
                r_fast,
                above=True,
                color=BLUE,
                linewidth=1.35,
                alpha=0.38,
                zorder=9,
            )
            ax.scatter([source[0]], [source[1]], s=24, color=BLUE, edgecolor="white", linewidth=0.6, zorder=12)
        draw_front(
            ax,
            A + r_fast * ray1,
            front1,
            above=True,
            color=BLUE,
            linewidth=2.05,
            alpha=0.30,
            zorder=10,
        )

        # Slow-medium wavelet from the first point to enter the lower medium.
        draw_circle_clip(
            ax,
            A,
            r_slow,
            above=False,
            color=ORANGE,
            linewidth=2.0,
            alpha=0.76,
            zorder=11,
        )
        ax.scatter([A[0]], [A[1]], s=52, color=ORANGE, edgecolor="white", linewidth=0.8, zorder=13)

        # The endpoint still in the fast medium reaches C after the same dt.
        ax.scatter([Cq[0]], [Cq[1]], s=48, color=BLUE, edgecolor="white", linewidth=0.8, zorder=14)
        ax.annotate(
            "",
            xy=Cq,
            xytext=B,
            arrowprops={"arrowstyle": "->", "color": BLUE, "linewidth": 2.0, "alpha": 0.74},
            zorder=15,
        )

        if q > 0.10:
            ax.text(1.36, 1.36, "larger fast wavelets", fontsize=9.5, color=BLUE, alpha=0.72)
            ax.text(0.18, -0.58, "smaller slow wavelet", fontsize=9.5, color=ORANGE, alpha=0.86)

        if reveal > 0.02:
            draw_segment(ax, D, C, color=ORANGE, linewidth=3.0, alpha=0.95 * reveal, zorder=18)
            ax.scatter([Dq[0]], [Dq[1]], s=38, color=ORANGE, edgecolor="white", linewidth=0.7, alpha=reveal, zorder=19)
            mid = 0.5 * (D + C)
            ax.text(mid[0] - 0.28, mid[1] - 0.16, "new wavefront", fontsize=9.8, color=ORANGE, alpha=reveal)
            ax.annotate(
                "",
                xy=mid + 0.92 * ray2,
                xytext=mid + 0.10 * ray2,
                arrowprops={"arrowstyle": "->", "color": ORANGE, "linewidth": 2.2, "alpha": 0.86 * reveal},
                zorder=20,
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


if __name__ == "__main__":
    make_huygens_snell_wavelet_proof(OUT / "lm-huygens-snell-wavelet-proof-review.mp4")
