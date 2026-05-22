from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"


def make_derivative_diagram(path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    x = np.linspace(-2.5 * np.pi, 2.5 * np.pi, 500)
    c = 1.0
    t0 = 0.65
    dt = 0.42
    x0 = 0.65

    def h(t):
        return np.sin(x - c * t)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), dpi=180)
    fig.patch.set_facecolor("#f8f5ef")

    ax = axes[0]
    for t, label, color, alpha in [
        (t0 - dt, "earlier", "#9b6a2f", 0.45),
        (t0, "now", "#1f6f78", 1.0),
        (t0 + dt, "later", "#b5493a", 0.45),
    ]:
        ax.plot(x, h(t), lw=2.2, color=color, alpha=alpha, label=label)

    idx = np.argmin(np.abs(x - x0))
    ax.scatter([x0] * 3, [h(t0 - dt)[idx], h(t0)[idx], h(t0 + dt)[idx]],
               s=42, color=["#9b6a2f", "#1f6f78", "#b5493a"], zorder=3)
    ax.axvline(x0, color="#444", lw=1.1, ls="--", alpha=0.55)
    ax.annotate("same place,\ndifferent times", xy=(x0, h(t0)[idx]),
                xytext=(x0 + 1.1, 1.25), fontsize=10,
                arrowprops=dict(arrowstyle="->", lw=1.1, color="#333"))
    ax.set_title("Time derivatives: how h changes at one place", fontsize=12, pad=10)
    ax.set_xlabel("space x")
    ax.set_ylabel("metric ripple h")
    ax.set_ylim(-1.55, 1.55)
    ax.legend(frameon=False, loc="lower left")
    ax.grid(True, alpha=0.18)

    ax = axes[1]
    y = h(t0)
    ax.plot(x, y, lw=2.4, color="#1f6f78")
    x_a, x_b, x_c = x0 - 0.52, x0, x0 + 0.52
    for xp in [x_a, x_b, x_c]:
        idp = np.argmin(np.abs(x - xp))
        ax.scatter(xp, y[idp], s=45, color="#1f6f78", zorder=3)
    ax.plot([x_a, x_b, x_c],
            [y[np.argmin(np.abs(x - x_a))], y[np.argmin(np.abs(x - x_b))], y[np.argmin(np.abs(x - x_c))]],
            color="#b5493a", lw=1.8, alpha=0.8)
    ax.annotate("neighboring places,\none time", xy=(x_b, y[np.argmin(np.abs(x - x_b))]),
                xytext=(x_b + 1.05, 1.18), fontsize=10,
                arrowprops=dict(arrowstyle="->", lw=1.1, color="#333"))
    ax.text(0.5, -0.30, "wave equation: second time-change balances second space-bend",
            transform=ax.transAxes, ha="center", va="center", fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="#fffaf2", ec="#d2c7b3"))
    ax.text(0.5, -0.43, "in simple 1D form:  d_t^2 h = d_x^2 h  (c=1)",
            transform=ax.transAxes, ha="center", va="center", fontsize=10.5)
    ax.set_title("Space derivatives: how h bends across places", fontsize=12, pad=10)
    ax.set_xlabel("space x")
    ax.set_ylabel("metric ripple h")
    ax.set_ylim(-1.55, 1.55)
    ax.grid(True, alpha=0.18)

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("What the derivatives in the gravitational-wave equation mean", fontsize=15, y=1.02)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def make_ring_animation(video_path: Path, still_path: Path, contact_path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    n = 28
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    base = np.c_[np.cos(theta), np.sin(theta)]
    amp = 0.22
    frames = 144

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), dpi=160)
    fig.patch.set_facecolor("#f8f5ef")
    ax_ring, ax_wave = axes

    for ax in axes:
        ax.set_facecolor("#f8f5ef")

    ax_ring.set_aspect("equal")
    ax_ring.set_xlim(-1.55, 1.55)
    ax_ring.set_ylim(-1.55, 1.55)
    ax_ring.axis("off")
    ax_ring.set_title("Free test masses in a passing metric ripple", fontsize=12)

    circle_line, = ax_ring.plot([], [], color="#777", lw=1.3, alpha=0.35)
    points = ax_ring.scatter([], [], s=42, color="#1f6f78", zorder=3)
    cross_x, = ax_ring.plot([], [], color="#b5493a", lw=2.1)
    cross_y, = ax_ring.plot([], [], color="#b5493a", lw=2.1)
    label = ax_ring.text(0, -1.42, "", ha="center", va="center", fontsize=10)

    wave_t = np.linspace(0, 2 * np.pi, 400)
    ax_wave.plot(wave_t, amp * np.sin(wave_t), color="#888", lw=1.5)
    wave_dot = ax_wave.scatter([], [], s=52, color="#b5493a", zorder=3)
    ax_wave.axhline(0, color="#444", lw=0.8, alpha=0.35)
    ax_wave.set_xlim(0, 2 * np.pi)
    ax_wave.set_ylim(-0.32, 0.32)
    ax_wave.set_title("One polarization: h(t)", fontsize=12)
    ax_wave.set_xlabel("time")
    ax_wave.set_ylabel("metric ripple")
    ax_wave.set_xticks([0, np.pi, 2 * np.pi])
    ax_wave.set_xticklabels(["0", "half cycle", "full cycle"])
    ax_wave.grid(True, alpha=0.18)
    ax_wave.spines["top"].set_visible(False)
    ax_wave.spines["right"].set_visible(False)

    def deformed(phase):
        h = amp * np.sin(phase)
        scale_x = 1 + h
        scale_y = 1 - h
        return np.c_[scale_x * base[:, 0], scale_y * base[:, 1]], h

    def draw_frame(i):
        phase = 2 * np.pi * i / frames
        pts, h = deformed(phase)
        loop = np.vstack([pts, pts[0]])
        circle_line.set_data(loop[:, 0], loop[:, 1])
        points.set_offsets(pts)
        cross_x.set_data([-(1 + h), 1 + h], [0, 0])
        cross_y.set_data([0, 0], [-(1 - h), 1 - h])
        wave_dot.set_offsets([[phase, h]])
        if h >= 0:
            label.set_text("x distances stretch while y distances shrink")
        else:
            label.set_text("x distances shrink while y distances stretch")
        return circle_line, points, cross_x, cross_y, wave_dot, label

    draw_frame(18)
    fig.tight_layout()
    fig.savefig(still_path, bbox_inches="tight")

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=True)
    writer = FFMpegWriter(fps=24, bitrate=1800)
    anim.save(video_path, writer=writer)

    sheet_fig, sheet_axes = plt.subplots(1, 4, figsize=(12, 3.1), dpi=180)
    sheet_fig.patch.set_facecolor("#f8f5ef")
    phases = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
    titles = ["neutral", "x stretch", "neutral", "y stretch"]
    for ax, phase, title in zip(sheet_axes, phases, titles):
        pts, h = deformed(phase)
        loop = np.vstack([pts, pts[0]])
        ax.plot(loop[:, 0], loop[:, 1], color="#777", lw=1.2, alpha=0.45)
        ax.scatter(pts[:, 0], pts[:, 1], s=22, color="#1f6f78")
        ax.plot([-(1 + h), 1 + h], [0, 0], color="#b5493a", lw=1.5)
        ax.plot([0, 0], [-(1 - h), 1 - h], color="#b5493a", lw=1.5)
        ax.set_aspect("equal")
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")
        ax.set_title(title, fontsize=10)
    sheet_fig.suptitle("A passing gravitational wave changes distances between free masses", fontsize=13)
    sheet_fig.tight_layout()
    sheet_fig.savefig(contact_path, bbox_inches="tight")
    plt.close(sheet_fig)
    plt.close(fig)


def main() -> None:
    make_derivative_diagram(OUTPUT_DIR / "gr-wave-derivative-diagram.png")
    make_ring_animation(
        OUTPUT_DIR / "gr-wave-test-mass-ring.mp4",
        OUTPUT_DIR / "gr-wave-test-mass-ring.png",
        OUTPUT_DIR / "gr-wave-test-mass-ring-contact-sheet.png",
    )


if __name__ == "__main__":
    main()
