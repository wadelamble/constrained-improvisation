from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"

BLUE = "#355070"
RED = "#BC4749"
PURPLE = "#6D597A"
INK = "#333333"
PAPER = "#FFFDF8"
GRID = "#E8E8E8"
PANEL = "#F9F7F1"
EDGE = "#CFCAC0"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 18) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def make_animation(path: Path) -> None:
    lam = np.linspace(0.0, 1.0, 600)
    y = 0.08 + 0.48 * lam + 0.18 * np.sin(np.pi * lam) - 0.055 * np.sin(2 * np.pi * lam)
    ydot = 0.48 + 0.18 * np.pi * np.cos(np.pi * lam) - 0.11 * np.pi * np.cos(2 * np.pi * lam)
    yddot = -0.18 * np.pi**2 * np.sin(np.pi * lam) + 0.22 * np.pi**2 * np.sin(2 * np.pi * lam)
    r = np.sqrt(1.0 + ydot**2)

    # First variation of ∫sqrt(1+y'^2)dλ after integration by parts.
    bulk_coefficient = -yddot / (r**3)

    frames = 108
    bump_width = 0.16
    bump_height = 0.055

    fig, (ax_path, ax_meter) = plt.subplots(
        1,
        2,
        figsize=(10.8, 4.8),
        gridspec_kw={"width_ratios": [1.78, 1.02]},
    )
    fig.patch.set_facecolor("#F7F3EC")

    def smoothstep(value: float) -> float:
        value = min(1.0, max(0.0, value))
        return value * value * (3.0 - 2.0 * value)

    def eta_at(center: float) -> np.ndarray:
        shifted = (lam - center) / bump_width
        active = np.abs(shifted) < 1.0
        eta = np.zeros_like(lam)
        eta[active] = 0.5 * bump_height * (1.0 + np.cos(np.pi * shifted[active]))
        return eta

    def draw_frame(frame: int) -> None:
        ax_path.clear()
        ax_meter.clear()

        phase = smoothstep(frame / (frames - 1))
        center = bump_width + (1.0 - 2.0 * bump_width) * phase
        eta = eta_at(center)
        varied = y + eta
        active = eta > 0.006
        bulk_value = float(np.trapezoid(bulk_coefficient * eta, lam))

        ax_path.set_facecolor(PAPER)
        ax_path.plot(lam, y, color=BLUE, linewidth=2.4, zorder=3)
        ax_path.plot(lam, varied, color=RED, linewidth=2.0, linestyle="--", zorder=4)
        ax_path.fill_between(lam[active], y[active], varied[active], color=RED, alpha=0.14, zorder=1)
        ax_path.scatter([lam[0], lam[-1]], [y[0], y[-1]], s=36, color=BLUE, zorder=5)
        ax_path.scatter([lam[0], lam[-1]], [varied[0], varied[-1]], s=22, facecolors=PAPER, edgecolors=RED, linewidths=1.6, zorder=6)

        ax_path.text(
            0.04,
            0.92,
            r"fixed endpoint variation $\eta(\lambda)$",
            transform=ax_path.transAxes,
            ha="left",
            va="center",
            color=PURPLE,
            fontsize=9.2,
            bbox={"facecolor": "#FFFDF8", "edgecolor": "#D8D0C2", "boxstyle": "round,pad=0.25"},
        )
        ax_path.text(0.0, -0.13, r"$\lambda_1$", ha="center", va="top", fontsize=10)
        ax_path.text(1.0, -0.13, r"$\lambda_2$", ha="center", va="top", fontsize=10)
        ax_path.text(0.015, y[0] + 0.035, "fixed", color="#555555", fontsize=8.6, ha="left")
        ax_path.text(0.985, y[-1] + 0.035, "fixed", color="#555555", fontsize=8.6, ha="right")
        ax_path.set_title(r"A local variation of the curve", pad=10)
        ax_path.set_xlabel(r"parameter $\lambda$")
        ax_path.set_ylabel(r"coordinate $y$")
        ax_path.set_xlim(-0.05, 1.05)
        ax_path.set_ylim(-0.08, 0.90)
        ax_path.set_xticks([])
        ax_path.set_yticks([])
        ax_path.grid(color=GRID, linewidth=0.7)

        ax_meter.axis("off")
        ax_meter.set_xlim(0, 1)
        ax_meter.set_ylim(0, 1)
        panel = plt.Rectangle((0.04, 0.06), 0.92, 0.88, facecolor=PANEL, edgecolor=EDGE, linewidth=1.0)
        ax_meter.add_patch(panel)
        ax_meter.text(0.5, 0.84, r"length variation", ha="center", va="center", fontsize=10.2, color=INK)
        ax_meter.text(0.5, 0.73, r"$\delta\ell_{\mathrm{bulk}}$", ha="center", va="center", fontsize=14.0, color=INK)
        ax_meter.plot([0.12, 0.88], [0.62, 0.62], color=EDGE, linewidth=0.9)
        ax_meter.text(0.13, 0.50, "variation", ha="left", va="center", fontsize=9.2, color=INK)
        if abs(bulk_value) < 0.00005:
            bulk_value = 0.0
        ax_meter.text(0.87, 0.50, f"{bulk_value:+.4f}", ha="right", va="center", fontsize=10.0, color=PURPLE)
        ax_meter.text(0.5, 0.26, r"endpoints fixed", ha="center", va="center", fontsize=9.0, color="#666666")
        ax_meter.text(0.5, 0.18, r"$\eta(\lambda_1)=\eta(\lambda_2)=0$", ha="center", va="center", fontsize=10.2, color=RED)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=18)
    plt.close(fig)


if __name__ == "__main__":
    make_animation(OUTPUT_DIR / "lm-fixed-endpoint-length-variation-review.mp4")
