from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"


def draw_wavefront(
    ax: plt.Axes,
    d: np.ndarray,
    w: np.ndarray,
    phase_distance: float,
    keep_above: bool,
    color: str,
    linewidth: float,
    alpha: float,
) -> None:
    u = np.linspace(-5.5, 5.5, 500)
    pts = phase_distance * d[:, None] + w[:, None] * u
    mask = pts[1] >= 0 if keep_above else pts[1] <= 0
    x = np.ma.masked_where(~mask, pts[0])
    y = np.ma.masked_where(~mask, pts[1])
    ax.plot(x, y, color=color, linewidth=linewidth, alpha=alpha, zorder=3)


def make_diagram(path: Path) -> None:
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

    fig, ax = plt.subplots(figsize=(10.8, 6.2), dpi=180)
    fig.patch.set_facecolor("#F7F3EC")
    ax.set_facecolor("#FFFDF8")
    ax.set_xlim(-3.15, 3.15)
    ax.set_ylim(-2.25, 2.35)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#C9BCAA")
        spine.set_linewidth(1.2)

    ax.axhspan(0, 2.55, color="#FFFDF8", zorder=0)
    ax.axhspan(-2.55, 0, color="#E8F2F7", zorder=0)
    ax.axhline(0, color="#7E7468", linewidth=1.6, zorder=4)
    ax.axvline(0, color="#BDB4A7", linewidth=1.0, linestyle="--", zorder=2)
    ax.text(-3.0, 0.15, "fast medium", fontsize=10.5, color="#4B463F")
    ax.text(-3.0, -0.35, "slow medium", fontsize=10.5, color="#4B463F")
    ax.text(0.08, 2.02, "normal", fontsize=10.5, color="#7E7468")

    # Keep only the wavefronts needed to orient the eye.
    phase = 0.88
    draw_wavefront(ax, d1, w1, phase - spacing1, True, "#355070", 1.25, 0.22)
    draw_wavefront(ax, d1, w1, phase, True, "#355070", 2.6, 0.86)
    draw_wavefront(ax, d2, w2, phase / n2, False, "#B85C38", 2.8, 0.90)

    # Rays perpendicular to the wavefronts.
    start = -2.35 * d1
    end = 1.95 * d2
    ax.annotate("", xy=(0, 0), xytext=start, arrowprops={"arrowstyle": "->", "color": "#355070", "linewidth": 2.4}, zorder=7)
    ax.annotate("", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 2.4}, zorder=7)
    ax.text(start[0] - 0.25, start[1] + 0.20, "incoming ray", fontsize=10.2, color="#355070")
    ax.text(end[0] + 0.06, end[1] + 0.08, "refracted ray", fontsize=10.2, color="#B85C38")

    # Secondary wavelets from points on the interface. Top wavelets are larger for the same elapsed time.
    boundary_points = np.linspace(-1.55, 1.55, 6)
    elapsed = 0.62
    r_fast = elapsed / n1
    r_slow = elapsed / n2
    phi_top = np.linspace(0, np.pi, 140)
    phi_bottom = np.linspace(np.pi, 2 * np.pi, 140)
    for xb in boundary_points:
        ax.plot(xb + r_fast * np.cos(phi_top), r_fast * np.sin(phi_top), color="#355070", linewidth=1.15, alpha=0.30, zorder=2)
        ax.plot(xb + r_slow * np.cos(phi_bottom), r_slow * np.sin(phi_bottom), color="#B85C38", linewidth=1.35, alpha=0.62, zorder=5)
        ax.scatter([xb], [0], s=18, color="#2F2F2F", edgecolor="white", linewidth=0.45, zorder=8)

    ax.text(1.25, -0.78, "lower envelope", fontsize=10.5, color="#B85C38")

    ax.text(
        -2.95,
        2.08,
        "Huygens construction at a medium boundary",
        fontsize=12.2,
        color="#2F2F2F",
        weight="bold",
    )
    ax.text(-2.72, 0.86, "larger wavelets", fontsize=10.2, color="#355070")
    ax.text(-2.72, -0.84, "smaller wavelets", fontsize=10.2, color="#B85C38")
    ax.text(1.10, 0.22, "interface", fontsize=10.0, color="#7E7468")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_diagram(OUTPUT_DIR / "lm-fermat-snell-huygens-interface.png")
