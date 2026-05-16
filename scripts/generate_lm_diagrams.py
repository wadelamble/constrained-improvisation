from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
SHELL_COLOR = "#2F2F2F"
LIGHT_CONE_COLOR = "#AFA79A"
SPACETIME_LIGHT_CONE = "#C9BCAA"
BEAD_COLOR = "#B85C38"
TRAIL_COLOR = "#3D6FB6"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def beta_wave(frames: int) -> np.ndarray:
    phase = np.linspace(0, 2 * np.pi, frames, endpoint=False)
    return 0.72 * np.sin(phase)


def momentum_wave(frames: int) -> np.ndarray:
    phase = np.linspace(0, 2 * np.pi, frames, endpoint=False)
    return 2.4 * np.sin(phase)


def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor("#FFFDF8")
    ax.grid(color="#DDD5C8", linewidth=0.8, alpha=0.75)
    for spine in ax.spines.values():
        spine.set_color("#B9AA98")


def make_mass_shell_spacetime_boost(path: Path) -> None:
    betas = np.array([-0.65, 0.0, 0.65])
    colors = ["#3D6FB6", "#4A4A4A", "#B85C38"]
    masses = [1.0, 2.0]

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8.0),
        gridspec_kw={"width_ratios": [1.05, 1.0], "hspace": 0.34, "wspace": 0.24},
    )
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle(
        r"Same boosts, different mass shells: $E^2-p^2=m^2$, $v=p/E$ ($c=1$)",
        fontsize=16,
        color="#2F2F2F",
        y=0.97,
    )

    p_grid = np.linspace(-3.2, 3.2, 500)
    t_grid = np.linspace(0, 3.1, 80)
    event_times = np.array([0.9, 1.8, 2.7])

    for row, mass in enumerate(masses):
        ax_shell = axes[row, 0]
        ax_space = axes[row, 1]

        for ax in (ax_shell, ax_space):
            style_axes(ax)

        energy = np.sqrt(mass**2 + p_grid**2)
        ax_shell.plot(p_grid, energy, color=SHELL_COLOR, linewidth=2.2)
        ax_shell.plot(p_grid, np.abs(p_grid), color=LIGHT_CONE_COLOR, linestyle="--", linewidth=1.0)
        ax_shell.axhline(0, color="#7E7468", linewidth=1.0)
        ax_shell.axvline(0, color="#7E7468", linewidth=1.0)
        ax_shell.set_xlim(-3.25, 3.25)
        ax_shell.set_ylim(0, 4.0)
        ax_shell.set_xlabel(r"momentum $p$")
        ax_shell.set_ylabel(r"energy $E$")
        ax_shell.set_title(rf"Mass shell $m={mass:g}$", fontsize=12.5, color="#2F2F2F")
        ax_shell.text(
            -3.05,
            3.55,
            r"invariant norm: $m$",
            fontsize=10.5,
            color="#5A5147",
            bbox={"boxstyle": "round,pad=0.25", "fc": "#F1E6D2", "ec": "#D7C6AA"},
        )
        ax_shell.annotate(
            "",
            xy=(-2.72, mass),
            xytext=(-2.72, 0),
            arrowprops={"arrowstyle": "<->", "color": "#8B6F47", "linewidth": 1.4},
        )
        ax_shell.text(-2.58, mass / 2, rf"$m={mass:g}$", va="center", fontsize=10, color="#8B6F47")

        ax_space.plot(t_grid, t_grid, color=SPACETIME_LIGHT_CONE, linestyle="--", linewidth=1.0)
        ax_space.plot(-t_grid, t_grid, color=SPACETIME_LIGHT_CONE, linestyle="--", linewidth=1.0)
        ax_space.axhline(0, color="#7E7468", linewidth=1.0)
        ax_space.axvline(0, color="#7E7468", linewidth=1.0)
        ax_space.set_xlim(-2.4, 2.4)
        ax_space.set_ylim(0, 3.2)
        ax_space.set_xlabel(r"space $x$")
        ax_space.set_ylabel(r"time $t$")
        ax_space.set_title("Worldline events for matching boosts", fontsize=12.5, color="#2F2F2F")
        ax_space.text(
            -2.24,
            2.9,
            "light cone",
            fontsize=9.5,
            color="#8C8176",
            bbox={"boxstyle": "round,pad=0.2", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )

        for beta, color in zip(betas, colors):
            gamma = 1.0 / np.sqrt(1.0 - beta**2)
            p = mass * gamma * beta
            e = mass * gamma
            ax_shell.scatter([p], [e], s=95, color=color, edgecolor="white", linewidth=1.4, zorder=5)
            ax_shell.text(
                p + 0.12,
                e + 0.08,
                rf"$\beta={beta:+.2f}$",
                fontsize=9.5,
                color=color,
            )

            x_grid = beta * t_grid
            ax_space.plot(x_grid, t_grid, color=color, linewidth=2.0, alpha=0.9)
            ax_space.scatter(
                beta * event_times,
                event_times,
                s=62 if mass == 1.0 else 92,
                color=color,
                edgecolor="white",
                linewidth=1.2,
                zorder=5,
            )

        if row == 1:
            ax_space.text(
                -2.24,
                0.28,
                "same beta values -> same spacetime tilt\nlarger m -> larger energy-momentum scale",
                fontsize=10.0,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.3", "fc": "#F1E6D2", "ec": "#D7C6AA"},
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_mass_shell_spacetime_boost_animation(path: Path) -> None:
    masses = [1.0, 2.0]
    frames = 144
    momenta = momentum_wave(frames)
    p_grid = np.linspace(-3.8, 3.8, 500)
    t_grid = np.linspace(0, 3.1, 90)
    event_times = np.array([0.85, 1.65, 2.45, 3.05])

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8.0),
        gridspec_kw={"width_ratios": [1.05, 1.0], "hspace": 0.34, "wspace": 0.24},
    )
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle(
        r"Same momentum coordinate, different mass shells: $v=p/E$",
        fontsize=16,
        color="#2F2F2F",
        y=0.97,
    )

    shell_beads = []
    shell_trails = []
    shell_labels = []
    worldlines = []
    event_beads = []
    event_trails = []

    for row, mass in enumerate(masses):
        ax_shell = axes[row, 0]
        ax_space = axes[row, 1]

        for ax in (ax_shell, ax_space):
            style_axes(ax)

        energy = np.sqrt(mass**2 + p_grid**2)
        ax_shell.plot(p_grid, energy, color=SHELL_COLOR, linewidth=2.2)
        ax_shell.plot(p_grid, np.abs(p_grid), color=LIGHT_CONE_COLOR, linestyle="--", linewidth=1.0)
        ax_shell.axhline(0, color="#7E7468", linewidth=1.0)
        ax_shell.axvline(0, color="#7E7468", linewidth=1.0)
        ax_shell.set_xlim(-3.85, 3.85)
        ax_shell.set_ylim(0, 4.6)
        ax_shell.set_xlabel(r"momentum $p$")
        ax_shell.set_ylabel(r"energy $E$")
        ax_shell.set_title(rf"Mass shell $m={mass:g}$", fontsize=12.5, color="#2F2F2F")
        ax_shell.text(
            -3.62,
            4.08,
            r"$E^2-p^2=m^2$",
            fontsize=10.5,
            color="#5A5147",
            bbox={"boxstyle": "round,pad=0.25", "fc": "#F1E6D2", "ec": "#D7C6AA"},
        )
        ax_shell.annotate(
            "",
            xy=(-3.32, mass),
            xytext=(-3.32, 0),
            arrowprops={"arrowstyle": "<->", "color": "#8B6F47", "linewidth": 1.4},
        )
        ax_shell.text(-3.18, mass / 2, rf"$m={mass:g}$", va="center", fontsize=10, color="#8B6F47")

        shell_trail, = ax_shell.plot([], [], color=TRAIL_COLOR, linewidth=1.6, alpha=0.55)
        shell_bead = ax_shell.scatter([], [], s=110, color=BEAD_COLOR, edgecolor="white", linewidth=1.4, zorder=5)
        shell_label = ax_shell.text(
            0.05,
            0.9,
            "",
            transform=ax_shell.transAxes,
            fontsize=10.5,
            color="#4B463F",
            bbox={"boxstyle": "round,pad=0.25", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )

        ax_space.plot(t_grid, t_grid, color=SPACETIME_LIGHT_CONE, linestyle="--", linewidth=1.0)
        ax_space.plot(-t_grid, t_grid, color=SPACETIME_LIGHT_CONE, linestyle="--", linewidth=1.0)
        ax_space.axhline(0, color="#7E7468", linewidth=1.0)
        ax_space.axvline(0, color="#7E7468", linewidth=1.0)
        ax_space.set_xlim(-3.15, 3.15)
        ax_space.set_ylim(0, 3.2)
        ax_space.set_xlabel(r"space $x$")
        ax_space.set_ylabel(r"time $t$")
        ax_space.set_title("Matching spacetime history", fontsize=12.5, color="#2F2F2F")
        ax_space.text(
            -2.28,
            2.9,
            "light cone",
            fontsize=9.5,
            color="#8C8176",
            bbox={"boxstyle": "round,pad=0.2", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )
        if row == 1:
            ax_space.text(
                -2.3,
                0.22,
                "same p -> different E\nlarger mass -> smaller v=p/E",
                fontsize=9.8,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.3", "fc": "#F1E6D2", "ec": "#D7C6AA"},
            )

        event_trail = ax_space.scatter([], [], s=18, color=TRAIL_COLOR, alpha=0.24, edgecolor="none", zorder=4)
        worldline, = ax_space.plot([], [], color=BEAD_COLOR, linewidth=2.4, alpha=0.9)
        beads = ax_space.scatter([], [], s=76, color=BEAD_COLOR, edgecolor="white", linewidth=1.2, zorder=5)

        shell_beads.append(shell_bead)
        shell_trails.append(shell_trail)
        shell_labels.append(shell_label)
        worldlines.append(worldline)
        event_beads.append(beads)
        event_trails.append(event_trail)

    def draw_frame(index: int):
        p = momenta[index]
        trail_start = max(0, index - 34)
        trail_momenta = momenta[trail_start : index + 1]
        artists = []

        for row, mass in enumerate(masses):
            e = np.sqrt(mass**2 + p**2)
            beta = p / e

            shell_beads[row].set_offsets([[p, e]])
            shell_labels[row].set_text(rf"$p={p:+.2f}$" + "\n" + rf"$E={e:.2f},\ \beta={beta:+.2f}$")

            trail_energy = np.sqrt(mass**2 + trail_momenta**2)
            trail_betas = trail_momenta / trail_energy
            shell_trails[row].set_data(trail_momenta, trail_energy)

            x_grid = beta * t_grid
            event_x = beta * event_times
            worldlines[row].set_data(x_grid, t_grid)
            event_beads[row].set_offsets(np.column_stack([event_x, event_times]))

            trail_t = np.repeat(event_times[:, None], trail_betas.size, axis=1)
            trail_x = event_times[:, None] * trail_betas[None, :]
            event_trails[row].set_offsets(np.column_stack([trail_x.ravel(), trail_t.ravel()]))

            artists.extend(
                [
                    shell_beads[row],
                    shell_trails[row],
                    shell_labels[row],
                    worldlines[row],
                    event_beads[row],
                    event_trails[row],
                ]
            )

        return artists

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


def main() -> None:
    make_mass_shell_spacetime_boost(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.png")
    make_mass_shell_spacetime_boost_animation(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.mp4")


if __name__ == "__main__":
    main()
