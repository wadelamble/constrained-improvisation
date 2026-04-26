from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.ndimage import gaussian_filter

import scienceplots  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"


def configure_style() -> None:
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.labelsize": 11,
            "axes.titlesize": 13,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.facecolor": "#fbfbfb",
            "figure.facecolor": "white",
        }
    )


def save_animation(anim: FuncAnimation, path: Path, fps: int) -> None:
    writer = FFMpegWriter(fps=fps, bitrate=2400, codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
    anim.save(path, writer=writer)


def make_permutation_animation(path: Path) -> None:
    states = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
    x_slots = np.arange(len(states), dtype=float)
    slot_index = {state: i for i, state in enumerate(states)}
    perm = {
        "ABC": "BCA",
        "BCA": "CAB",
        "CAB": "ABC",
        "ACB": "CBA",
        "CBA": "BAC",
        "BAC": "ACB",
    }

    masses = [
        {"label": r"$1/2$", "height": 0.5, "state": "ABC", "color": "#4C78A8"},
        {"label": r"$1/3$", "height": 1.0 / 3.0, "state": "BAC", "color": "#F58518"},
        {"label": r"$1/6$", "height": 1.0 / 6.0, "state": "CBA", "color": "#54A24B"},
    ]

    steps = 6
    frames_per_step = 18
    total_frames = steps * frames_per_step

    fig, ax = plt.subplots(figsize=(10, 4.8))

    def draw_frame(frame: int) -> None:
        ax.clear()
        step = frame // frames_per_step
        alpha = (frame % frames_per_step) / frames_per_step

        current_states = [m["state"] for m in masses]
        next_states = [perm[state] for state in current_states]

        if step > 0:
            for _ in range(step):
                current_states = [perm[state] for state in current_states]
            next_states = [perm[state] for state in current_states]

        ax.bar(
            x_slots,
            [0] * len(states),
            width=0.72,
            color="none",
            edgecolor="#D8D8D8",
            linewidth=1.2,
        )

        for state, mass in zip(current_states, masses):
            start_x = slot_index[state]
            end_x = slot_index[perm[state]]
            x = (1.0 - alpha) * start_x + alpha * end_x
            ax.bar(
                [x],
                [mass["height"]],
                width=0.58,
                color=mass["color"],
                edgecolor="white",
                linewidth=1.3,
                zorder=3,
            )
            ax.text(
                x,
                mass["height"] + 0.022,
                mass["label"],
                ha="center",
                va="bottom",
                fontsize=10,
                color=mass["color"],
            )

        shown_mapping = ", ".join(f"{s}\N{RIGHTWARDS ARROW}{perm[s]}" for s in ["ABC", "BAC", "CBA"])
        ax.text(
            0.0,
            1.03,
            f"Permutation step {step + 1} of {steps}:  move top card to bottom",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=11,
            color="#333333",
        )
        ax.text(
            0.0,
            0.97,
            shown_mapping,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color="#666666",
        )

        ax.set_title("Three-card permutation: probability weights are preserved up to rearrangement", pad=18)
        ax.set_ylabel("Probability")
        ax.set_xticks(x_slots)
        ax.set_xticklabels(states)
        ax.set_ylim(0, 0.62)
        ax.set_xlim(-0.6, len(states) - 0.4)
        ax.grid(axis="y", color="#E8E8E8", linewidth=0.8)

    anim = FuncAnimation(fig, draw_frame, frames=total_frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def simulate_quartic_ensemble(n_samples: int, n_frames: int, dt: float, steps_per_frame: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(12)
    q = rng.normal(loc=0.95, scale=0.15, size=n_samples)
    p = rng.normal(loc=0.0, scale=0.22, size=n_samples)

    q_hist = np.empty((n_frames, n_samples), dtype=np.float32)
    p_hist = np.empty((n_frames, n_samples), dtype=np.float32)

    def force(qv: np.ndarray) -> np.ndarray:
        return -(qv ** 3)

    for frame in range(n_frames):
        q_hist[frame] = q
        p_hist[frame] = p
        for _ in range(steps_per_frame):
            p_half = p + 0.5 * dt * force(q)
            q = q + dt * p_half
            p = p_half + 0.5 * dt * force(q)

    return q_hist, p_hist


def make_liouville_animation(path: Path) -> None:
    n_frames = 160
    q_hist, p_hist = simulate_quartic_ensemble(n_samples=2600, n_frames=n_frames, dt=0.03, steps_per_frame=4)

    q_range = (-1.55, 1.55)
    p_range = (-1.85, 1.85)
    bins = 140
    q_edges = np.linspace(*q_range, bins + 1)
    p_edges = np.linspace(*p_range, bins + 1)
    q_centers = 0.5 * (q_edges[:-1] + q_edges[1:])
    p_centers = 0.5 * (p_edges[:-1] + p_edges[1:])
    qq, pp = np.meshgrid(q_centers, p_centers)

    densities: list[np.ndarray] = []
    mass_levels = None
    level_values = None
    max_density = 0.0

    for frame in range(n_frames):
        hist, _, _ = np.histogram2d(q_hist[frame], p_hist[frame], bins=[q_edges, p_edges], density=True)
        smoothed = gaussian_filter(hist.T, sigma=1.15)
        densities.append(smoothed)
        max_density = max(max_density, float(smoothed.max()))

    initial = densities[0]
    flat = np.sort(initial.ravel())[::-1]
    cdf = np.cumsum(flat) / np.sum(flat)
    mass_levels = [0.50, 0.80, 0.95]
    level_values = []
    for mass in mass_levels:
        idx = np.searchsorted(cdf, mass)
        idx = min(idx, len(flat) - 1)
        level_values.append(float(flat[idx]))
    level_values = np.array(sorted(set(level_values)))

    fig, ax = plt.subplots(figsize=(6.8, 6.2))

    def draw_frame(frame: int) -> None:
        ax.clear()
        density = densities[frame]
        ax.contourf(
            qq,
            pp,
            density,
            levels=np.linspace(0, max_density, 12),
            cmap="cividis",
            alpha=0.95,
        )
        ax.contour(
            qq,
            pp,
            density,
            levels=level_values,
            colors=["#F94144", "#F8961E", "#277DA1"],
            linewidths=2.0,
        )

        t = frame * 0.12
        ax.set_title("Liouville transport in a nonlinear oscillator", pad=14)
        ax.text(
            0.01,
            1.02,
            "A probability hill may deform, but it does not flatten by diffusion.",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=10,
            color="#333333",
        )
        ax.text(
            0.01,
            0.97,
            f"quartic Hamiltonian  H = p²/2 + q⁴/4      t = {t:0.1f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9.5,
            color="#555555",
        )

        ax.set_xlabel("Position  q")
        ax.set_ylabel("Momentum  p")
        ax.set_xlim(*q_range)
        ax.set_ylim(*p_range)
        ax.set_aspect("equal")
        ax.grid(color="#E6E6E6", linewidth=0.6)

    anim = FuncAnimation(fig, draw_frame, frames=n_frames, interval=1000 / 24, blit=False)
    save_animation(anim, path, fps=24)
    plt.close(fig)


def main() -> None:
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    make_permutation_animation(OUTPUT_DIR / "liouville-permutation-3card.mp4")
    make_liouville_animation(OUTPUT_DIR / "liouville-contours-quartic.mp4")


if __name__ == "__main__":
    main()
