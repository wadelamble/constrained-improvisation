from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Arc, Circle, Rectangle


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


def make_plane_path_length_variation(path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.2), gridspec_kw={"wspace": 0.22})
    fig.patch.set_facecolor("#F7F3EC")

    x0, y0 = 0.12, 0.18
    x1, y1 = 0.88, 0.82
    s = np.linspace(0, 1, 260)
    straight_x = x0 + (x1 - x0) * s
    straight_y = y0 + (y1 - y0) * s
    candidate_x = straight_x + 0.17 * np.sin(np.pi * s) - 0.06 * np.sin(2 * np.pi * s)
    candidate_y = straight_y - 0.12 * np.sin(np.pi * s) + 0.08 * np.sin(2 * np.pi * s)
    variation_x = candidate_x - 0.08 * np.sin(np.pi * s)
    variation_y = candidate_y + 0.11 * np.sin(np.pi * s)

    panel_data = [
        ("candidate curve", [(candidate_x, candidate_y, BEAD_COLOR, 2.8, "-")]),
        (
            "nearby variations",
            [
                (candidate_x, candidate_y, BEAD_COLOR, 2.6, "-"),
                (variation_x, variation_y, TRAIL_COLOR, 2.0, "--"),
            ],
        ),
        (
            "straight minimizer",
            [
                (candidate_x, candidate_y, "#BDB4A7", 1.6, "-"),
                (straight_x, straight_y, "#2F2F2F", 2.8, "-"),
            ],
        ),
    ]

    for ax, (title, curves) in zip(axes, panel_data):
        style_axes(ax)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=11.5, color="#2F2F2F")
        ax.annotate("", xy=(0.96, 0.08), xytext=(0.06, 0.08), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
        ax.annotate("", xy=(0.08, 0.96), xytext=(0.08, 0.06), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
        ax.text(0.94, 0.015, "$x$", fontsize=10, color="#4B463F")
        ax.text(0.025, 0.94, "$y$", fontsize=10, color="#4B463F")
        for x_values, y_values, color, linewidth, linestyle in curves:
            ax.plot(x_values, y_values, color=color, linewidth=linewidth, linestyle=linestyle)
        ax.scatter([x0, x1], [y0, y1], s=64, color="#2F2F2F", edgecolor="white", linewidth=1.0, zorder=5)
        ax.text(x0 - 0.03, y0 - 0.08, r"$(x_1,y_1)$", fontsize=9.5, color="#4B463F")
        ax.text(x1 - 0.02, y1 + 0.04, r"$(x_2,y_2)$", fontsize=9.5, color="#4B463F")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_sphere_geodesic_sketch(path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.4), gridspec_kw={"wspace": 0.16})
    fig.patch.set_facecolor("#F7F3EC")

    def draw_sphere(ax: plt.Axes) -> None:
        style_axes(ax)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-1.22, 1.22)
        ax.set_ylim(-1.12, 1.12)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.add_patch(Circle((0, 0), 1.0, fill=False, edgecolor="#2F2F2F", linewidth=1.8))
        ax.add_patch(Arc((0, 0), 2.0, 0.42, angle=0, theta1=0, theta2=360, color="#BDB4A7", linewidth=1.1))
        ax.add_patch(Arc((0, 0), 0.55, 2.0, angle=0, theta1=0, theta2=360, color="#BDB4A7", linewidth=1.1))
        ax.add_patch(Arc((0, 0), 1.35, 2.0, angle=0, theta1=82, theta2=278, color="#D6CEC2", linewidth=0.9))

    theta = np.linspace(-0.86, 0.82, 200)
    great_x = 0.58 * np.sin(theta)
    great_y = np.cos(theta) * 0.92 - 0.05
    detour_x = great_x + 0.25 * np.sin(np.linspace(0, np.pi, theta.size))
    detour_y = great_y - 0.16 * np.sin(np.linspace(0, np.pi, theta.size))
    points_x = [great_x[0], great_x[-1]]
    points_y = [great_y[0], great_y[-1]]

    panel_data = [
        ("curved surface", []),
        ("candidate path", [(detour_x, detour_y, BEAD_COLOR, 2.7, "-")]),
        (
            "great-circle geodesic",
            [
                (detour_x, detour_y, "#BDB4A7", 1.5, "-"),
                (great_x, great_y, "#2F2F2F", 2.8, "-"),
            ],
        ),
    ]

    for ax, (title, curves) in zip(axes, panel_data):
        draw_sphere(ax)
        ax.set_title(title, fontsize=11.5, color="#2F2F2F")
        for x_values, y_values, color, linewidth, linestyle in curves:
            ax.plot(x_values, y_values, color=color, linewidth=linewidth, linestyle=linestyle)
        if curves:
            ax.scatter(points_x, points_y, s=58, color="#2F2F2F", edgecolor="white", linewidth=1.0, zorder=5)
        if title == "curved surface":
            ax.plot(great_x, great_y, color="#2F2F2F", linewidth=1.6, alpha=0.65)
            ax.text(-0.88, -0.9, "length is measured\ninside the surface", fontsize=9.2, color="#4B463F")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_possible_spacetime_paths(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 7.8))
    fig.patch.set_facecolor("#F7F3EC")
    style_axes(ax)

    s = np.linspace(0, 1, 420)
    t0, t1 = 0.35, 4.45
    x0, x1 = -1.75, 1.65
    t = t0 + (t1 - t0) * s
    baseline = x0 + (x1 - x0) * s

    nice = baseline + 0.95 * s * (1 - s)
    high_detour = baseline + 1.95 * np.sin(np.pi * s) ** 1.1 + 0.58 * np.sin(2 * np.pi * s)
    low_detour = baseline - 1.35 * np.sin(np.pi * s) - 0.28 * np.sin(2 * np.pi * s) + 0.18 * np.sin(3 * np.pi * s)
    wild = baseline + 0.95 * np.sin(np.pi * s) * np.sin(5.4 * np.pi * s) + 0.44 * np.sin(np.pi * s) * np.sin(2 * np.pi * s)

    candidates = [
        (low_detour, "#BDB4A7", 1.8),
        (high_detour, "#BDB4A7", 1.8),
        (wild, "#A8B5C6", 1.8),
        (nice, "#B85C38", 3.2),
    ]

    for x, color, linewidth in candidates:
        ax.plot(x, t, color=color, linewidth=linewidth, alpha=0.95)

    ax.scatter([x0, x1], [t0, t1], s=92, color="#2F2F2F", edgecolor="white", linewidth=1.2, zorder=6)
    ax.text(x0 - 0.18, t0 - 0.30, "fixed start", fontsize=10, color="#4B463F", ha="left")
    ax.text(x1 - 0.34, t1 + 0.18, "fixed end", fontsize=10, color="#4B463F", ha="left")

    ax.annotate("", xy=(4.35, 0.0), xytext=(-3.25, 0.0), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
    ax.annotate("", xy=(-3.05, 4.95), xytext=(-3.05, 0.0), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
    ax.text(4.27, -0.25, "$x$", fontsize=12, color="#4B463F")
    ax.text(-3.32, 4.86, "$t$", fontsize=12, color="#4B463F")

    ax.set_title("Possible paths between fixed spacetime events", fontsize=14, color="#2F2F2F", pad=14)
    ax.set_xlim(-3.35, 4.45)
    ax.set_ylim(-0.05, 5.05)
    ax.set_aspect("auto")
    ax.set_xlabel("space")
    ax.set_ylabel("time")
    ax.set_xticks([])
    ax.set_yticks([])

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_free_vs_uniform_force_spacetime(path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.6), gridspec_kw={"wspace": 0.22})
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle("Simple paths in spacetime", fontsize=15, color="#2F2F2F", y=0.96)

    t = np.linspace(0.0, 4.2, 360)
    x_free = -1.35 + 0.55 * t
    x_force = -1.42 + 0.12 * t + 0.18 * t**2

    panels = [
        (axes[0], x_free, "Free particle", "constant velocity", "#355070"),
        (axes[1], x_force, "Uniform force field", "constant acceleration", "#B85C38"),
    ]

    for ax, x, title, note, color in panels:
        style_axes(ax)
        ax.plot(x, t, color=color, linewidth=3.0)
        ax.scatter([x[0], x[-1]], [t[0], t[-1]], s=76, color="#2F2F2F", edgecolor="white", linewidth=1.1, zorder=5)
        ax.annotate("", xy=(2.45, 0.0), xytext=(-2.15, 0.0), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
        ax.annotate("", xy=(-2.0, 4.7), xytext=(-2.0, 0.0), arrowprops={"arrowstyle": "->", "color": "#7E7468"})
        ax.text(2.34, -0.28, "$x$", fontsize=12, color="#4B463F")
        ax.text(-2.22, 4.6, "$t$", fontsize=12, color="#4B463F")
        ax.set_xlim(-2.25, 2.55)
        ax.set_ylim(-0.05, 4.75)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("space")
        ax.set_ylabel("time")
        ax.set_title(title, fontsize=13, color="#2F2F2F", pad=12)
        ax.text(
            0.05,
            0.9,
            note,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=10.5,
            color="#4B463F",
            bbox={"boxstyle": "round,pad=0.28", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )

    axes[0].text(
        0.95,
        0.08,
        "straight worldline",
        transform=axes[0].transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color="#355070",
        bbox={"boxstyle": "round,pad=0.25", "fc": "#F1E6D2", "ec": "#D7C6AA"},
    )
    axes[1].text(
        0.95,
        0.08,
        "parabolic worldline",
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
        color="#B85C38",
        bbox={"boxstyle": "round,pad=0.25", "fc": "#F1E6D2", "ec": "#D7C6AA"},
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_fermat_snell_huygens_animation(path: Path) -> None:
    frames = 150
    n1 = 1.0
    n2 = 1.55
    theta1 = np.deg2rad(46.0)
    theta2 = np.arcsin((n1 / n2) * np.sin(theta1))
    d1 = np.array([np.sin(theta1), -np.cos(theta1)])
    w1 = np.array([np.cos(theta1), np.sin(theta1)])
    d2 = np.array([np.sin(theta2), -np.cos(theta2)])
    w2 = np.array([np.cos(theta2), np.sin(theta2)])
    spacing1 = 0.55
    spacing2 = spacing1 / n2

    fig, ax_wave = plt.subplots(figsize=(8.6, 7.2))
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle("Fermat's principle emerges from local wave propagation", fontsize=15, color="#2F2F2F", y=0.965)

    def draw_clipped_wavefront(
        ax: plt.Axes,
        d: np.ndarray,
        w: np.ndarray,
        phase_distance: float,
        keep_above: bool,
        color: str,
        linewidth: float,
        alpha: float,
    ) -> None:
        u = np.linspace(-4.4, 4.4, 420)
        pts = phase_distance * d[:, None] + w[:, None] * u
        mask = pts[1] >= 0 if keep_above else pts[1] <= 0
        x = np.ma.masked_where(~mask, pts[0])
        y = np.ma.masked_where(~mask, pts[1])
        ax.plot(x, y, color=color, linewidth=linewidth, alpha=alpha)

    def draw_frame(frame: int):
        ax_wave.clear()
        progress = frame / (frames - 1)
        smooth = progress * progress * (3.0 - 2.0 * progress)
        phase = -1.15 + 3.65 * smooth

        style_axes(ax_wave)
        ax_wave.axhspan(0, 2.55, color="#FFFDF8", zorder=0)
        ax_wave.axhspan(-2.55, 0, color="#E8F2F7", zorder=0)
        ax_wave.axhline(0, color="#7E7468", linewidth=1.6, zorder=2)
        ax_wave.text(-2.62, 0.12, "fast medium", fontsize=9.8, color="#4B463F")
        ax_wave.text(-2.62, -0.32, "slow medium", fontsize=9.8, color="#4B463F")
        ax_wave.set_xticks([])
        ax_wave.set_yticks([])

        ax_wave.set_title("Huygens: the wavefront pivots locally", fontsize=12.4, color="#2F2F2F")
        ax_wave.set_xlim(-2.75, 2.75)
        ax_wave.set_ylim(-2.35, 2.35)
        ax_wave.set_aspect("equal", adjustable="box")
        ax_wave.axvline(0, color="#BDB4A7", linewidth=1.0, linestyle="--")
        ax_wave.text(0.08, 1.95, "normal", fontsize=9.5, color="#7E7468")

        start = -2.55 * d1
        end = 2.55 * d2
        ax_wave.annotate("", xy=(0, 0), xytext=start, arrowprops={"arrowstyle": "->", "color": "#355070", "linewidth": 2.2})
        ax_wave.annotate("", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 2.2})
        ax_wave.text(start[0] - 0.1, start[1] + 0.1, "incoming ray", fontsize=9.2, color="#355070")
        ax_wave.text(end[0] + 0.05, end[1] - 0.12, "bent ray", fontsize=9.2, color="#B85C38")

        for index in range(-3, 6):
            p = phase - index * spacing1
            if -2.4 < p < 2.6:
                if index == 0:
                    draw_clipped_wavefront(ax_wave, d1, w1, p, True, "#355070", 2.0, 0.82)
                else:
                    draw_clipped_wavefront(ax_wave, d1, w1, p, True, "#355070", 1.15, 0.36)

        if phase > -0.05:
            for index in range(0, 8):
                p2 = phase / n2 - index * spacing2
                if -0.2 < p2 < 2.2:
                    draw_clipped_wavefront(ax_wave, d2, w2, p2, False, "#B85C38", 1.2, 0.5)

        current_hit_x = phase / d1[0]
        boundary_points = np.linspace(-1.5, 1.5, 7)
        phi = np.linspace(0, np.pi, 90)
        for xb in boundary_points:
            age = phase - d1[0] * xb
            if 0.0 < age < 1.95:
                xs_fast = xb + age * np.cos(phi)
                ys_fast = age * np.sin(phi)
                ax_wave.plot(xs_fast, ys_fast, color="#355070", linewidth=1.1, alpha=0.28)
                radius = age / n2
                xs = xb + radius * np.cos(phi)
                ys = -radius * np.sin(phi)
                ax_wave.plot(xs, ys, color="#B85C38", linewidth=1.0, alpha=0.34)
                ax_wave.scatter([xb], [0], s=18, color="#B85C38", alpha=0.62, zorder=5)

        if -1.55 <= current_hit_x <= 1.55:
            ax_wave.scatter([current_hit_x], [0], s=50, color="#2F2F2F", edgecolor="white", linewidth=0.8, zorder=6)
            ax_wave.text(
                0.04,
                0.06,
                "the lower medium advances less\nin the same time",
                transform=ax_wave.transAxes,
                ha="left",
                va="bottom",
                fontsize=9.5,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.25", "fc": "#FFFDF8", "ec": "#D7C6AA"},
            )

        return []

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    plt.close(fig)


def make_fixed_endpoint_action_sweep(path: Path, poster_path: Path) -> None:
    frames = 168
    t_end = 4.0
    x_start = -1.55
    x_end = 1.55
    amplitude_max = 1.1
    t = np.linspace(0, t_end, 420)
    candidate_amplitudes = np.linspace(-amplitude_max, amplitude_max, 13)

    def path_x(amplitude: float) -> np.ndarray:
        baseline = x_start + (x_end - x_start) * t / t_end
        return baseline + amplitude * np.sin(np.pi * t / t_end)

    def velocity(amplitude: float) -> np.ndarray:
        baseline_velocity = (x_end - x_start) / t_end
        return baseline_velocity + amplitude * (np.pi / t_end) * np.cos(np.pi * t / t_end)

    def action(amplitude: float) -> float:
        return float(np.trapezoid(0.5 * velocity(amplitude) ** 2, t))

    actions = np.array([action(a) for a in candidate_amplitudes])
    action_min = action(0.0)
    action_max = actions.max()

    phase = np.linspace(0, 6.0 * np.pi, frames)
    envelope = np.ones(frames)
    settle_start = int(frames * 0.54)
    settle = np.linspace(0, 1, frames - settle_start)
    envelope[settle_start:] = np.exp(-4.0 * settle)
    amplitudes = amplitude_max * envelope * np.sin(phase)
    amplitudes[-1] = 0.0

    fig, (ax_path, ax_meter) = plt.subplots(
        1,
        2,
        figsize=(11.0, 6.2),
        gridspec_kw={"width_ratios": [1.45, 0.62], "wspace": 0.28},
    )
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle(
        "Fixed endpoints, many possible paths, one minimum action",
        fontsize=15,
        color="#2F2F2F",
        y=0.96,
    )

    for ax in (ax_path, ax_meter):
        style_axes(ax)

    for amplitude in candidate_amplitudes:
        ax_path.plot(path_x(amplitude), t, color="#BDB4A7", linewidth=1.0, alpha=0.48)

    minimum_path = path_x(0.0)
    ax_path.plot(minimum_path, t, color="#2F2F2F", linewidth=1.8, linestyle="--", alpha=0.86)
    active_path, = ax_path.plot([], [], color=BEAD_COLOR, linewidth=3.0, alpha=0.96)
    endpoint_points = ax_path.scatter(
        [x_start, x_end],
        [0.0, t_end],
        s=92,
        color="#2F2F2F",
        edgecolor="white",
        linewidth=1.2,
        zorder=6,
    )
    current_dot = ax_path.scatter([], [], s=70, color=BEAD_COLOR, edgecolor="white", linewidth=1.1, zorder=7)
    ax_path.text(
        x_start + 0.1,
        0.12,
        "fixed start",
        fontsize=9.2,
        color="#4B463F",
        bbox={"boxstyle": "round,pad=0.22", "fc": "#FFFDF8", "ec": "#D7C6AA"},
    )
    ax_path.text(
        x_end - 1.0,
        t_end - 0.32,
        "fixed end",
        fontsize=9.2,
        color="#4B463F",
        bbox={"boxstyle": "round,pad=0.22", "fc": "#FFFDF8", "ec": "#D7C6AA"},
    )
    ax_path.set_xlim(-2.9, 2.9)
    ax_path.set_ylim(-0.08, t_end + 0.08)
    ax_path.set_xlabel("space x")
    ax_path.set_ylabel("time t")
    ax_path.set_title("Candidate histories", fontsize=12, color="#2F2F2F")

    ax_meter.set_xlim(0, 1)
    ax_meter.set_ylim(0, 1)
    ax_meter.set_xticks([])
    ax_meter.set_yticks([])
    ax_meter.set_title("Action meter", fontsize=12, color="#2F2F2F")
    ax_meter.text(0.5, 0.08, "minimum", ha="center", va="center", fontsize=9.5, color="#4B463F")
    ax_meter.text(0.5, 0.94, "larger", ha="center", va="center", fontsize=9.5, color="#4B463F")
    ax_meter.plot([0.23, 0.77], [0.17, 0.17], color="#2F2F2F", linewidth=1.4, linestyle="--")
    meter_outline = Rectangle((0.34, 0.17), 0.32, 0.68, facecolor="#FFFDF8", edgecolor="#7E7468", linewidth=1.4)
    meter_bar = Rectangle((0.34, 0.17), 0.32, 0.01, facecolor=BEAD_COLOR, edgecolor="none", alpha=0.9)
    ax_meter.add_patch(meter_outline)
    ax_meter.add_patch(meter_bar)
    meter_text = ax_meter.text(
        0.5,
        0.88,
        "",
        ha="center",
        va="center",
        fontsize=10.0,
        color="#4B463F",
        bbox={"boxstyle": "round,pad=0.25", "fc": "#F1E6D2", "ec": "#D7C6AA"},
    )
    phase_text = ax_meter.text(
        0.5,
        0.02,
        "",
        ha="center",
        va="bottom",
        fontsize=9.3,
        color="#4B463F",
    )

    def draw_frame(index: int):
        amplitude = amplitudes[index]
        x_values = path_x(amplitude)
        current_action = action(amplitude)
        normalized = (current_action - action_min) / max(action_max - action_min, 1e-9)
        bar_height = 0.04 + 0.64 * normalized

        active_path.set_data(x_values, t)
        probe_index = min(len(t) - 1, int((index / (frames - 1)) * (len(t) - 1)))
        current_dot.set_offsets([[x_values[probe_index], t[probe_index]]])
        meter_bar.set_height(bar_height)
        meter_bar.set_y(0.17)
        meter_text.set_text(f"S = {current_action:.2f}")

        if index < settle_start:
            phase_text.set_text("sweeping candidate paths")
        elif index < frames - 8:
            phase_text.set_text("settling toward minimum")
        else:
            phase_text.set_text("minimum-action path")

        return [active_path, endpoint_points, current_dot, meter_bar, meter_text, phase_text]

    draw_frame(0)
    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    draw_frame(frames - 1)
    fig.savefig(poster_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_one_parameter_variation_slice(path: Path, poster_path: Path) -> None:
    frames = 144
    t_end = 4.0
    x_start = -1.35
    x_end = 1.35
    t = np.linspace(0.0, t_end, 480)
    eps_values = np.linspace(-0.8, 0.8, 240)
    bump_width = 0.38
    display_epsilon = 0.55

    def straight_path() -> np.ndarray:
        return x_start + (x_end - x_start) * t / t_end

    def curved_path() -> np.ndarray:
        return straight_path() + 0.58 * np.sin(np.pi * t / t_end)

    def wiggle_shape(center: float) -> np.ndarray:
        endpoint_gate = np.sin(np.pi * t / t_end)
        bump = np.exp(-0.5 * ((t - center) / bump_width) ** 2)
        return endpoint_gate * bump

    def path_x(base: np.ndarray, epsilon: float, center: float) -> np.ndarray:
        return base + epsilon * wiggle_shape(center)

    def action_coefficients(base: np.ndarray, center: float) -> tuple[float, float, float]:
        base_velocity = np.gradient(base, t)
        shape_velocity = np.gradient(wiggle_shape(center), t)
        base_action = float(np.trapezoid(0.5 * base_velocity**2, t))
        linear = float(np.trapezoid(base_velocity * shape_velocity, t))
        quadratic = float(np.trapezoid(0.5 * shape_velocity**2, t))
        return base_action, linear, quadratic

    def action(base: np.ndarray, epsilon: float, center: float) -> float:
        base_action, linear, quadratic = action_coefficients(base, center)
        return base_action + epsilon * linear + epsilon**2 * quadratic

    center_frames = np.linspace(0.48, t_end - 0.48, frames)
    epsilon_frames = display_epsilon * np.sin(np.linspace(0.0, 5.0 * np.pi, frames))
    bases = [straight_path(), curved_path()]
    row_labels = ["stationary candidate", "not stationary"]
    row_notes = [
        r"$dS/d\epsilon=0$ at $\epsilon=0$",
        r"$dS/d\epsilon\ne0$ at $\epsilon=0$",
    ]

    row_ranges = []
    for base in bases:
        sampled = []
        for center in center_frames[::6]:
            base_action, linear, quadratic = action_coefficients(base, center)
            sampled.extend((base_action + eps_values * linear + eps_values**2 * quadratic).tolist())
        row_ranges.append((min(sampled), max(sampled)))

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12.0, 8.4),
        gridspec_kw={"width_ratios": [1.05, 1.0], "hspace": 0.34, "wspace": 0.26},
    )
    fig.patch.set_facecolor("#F7F3EC")
    fig.suptitle(
        "Stationarity means every local wiggle has zero first-order effect",
        fontsize=15,
        color="#2F2F2F",
        y=0.975,
    )

    active_paths = []
    bump_fills = []
    labels = []
    action_lines = []
    tangent_lines = []
    zero_dots = []
    moving_dots = []
    zero_lines = []

    for row, base in enumerate(bases):
        ax_path = axes[row, 0]
        ax_graph = axes[row, 1]
        for ax in (ax_path, ax_graph):
            style_axes(ax)

        ax_path.set_title(row_labels[row], fontsize=12, color="#2F2F2F")
        ax_path.set_xlabel("space x")
        ax_path.set_ylabel("time t")
        ax_path.set_xlim(-2.2, 2.35)
        ax_path.set_ylim(-0.08, t_end + 0.08)
        ax_path.plot(base, t, color="#2F2F2F", linewidth=1.9, linestyle="--", alpha=0.86)
        active_path, = ax_path.plot([], [], color=BEAD_COLOR, linewidth=3.0, alpha=0.96)
        active_paths.append(active_path)
        bump_fills.append(ax_path.fill_betweenx(t, base, base, color=BEAD_COLOR, alpha=0.15, linewidth=0))
        ax_path.scatter(
            [x_start, x_end],
            [0.0, t_end],
            s=70,
            color="#2F2F2F",
            edgecolor="white",
            linewidth=1.0,
            zorder=6,
        )
        labels.append(
            ax_path.text(
                0.05,
                0.91,
                "",
                transform=ax_path.transAxes,
                ha="left",
                va="top",
                fontsize=9.5,
                color="#4B463F",
                bbox={"boxstyle": "round,pad=0.23", "fc": "#F1E6D2", "ec": "#D7C6AA"},
            )
        )
        ax_path.text(
            0.05,
            0.08,
            "same local test, moved along the path",
            transform=ax_path.transAxes,
            ha="left",
            va="bottom",
            fontsize=8.9,
            color="#4B463F",
            bbox={"boxstyle": "round,pad=0.2", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )

        ax_graph.set_title(r"Diagnostic graph $S(\epsilon)$", fontsize=12, color="#2F2F2F")
        ax_graph.set_xlabel(r"local wiggle amount $\epsilon$")
        ax_graph.set_ylabel(r"action $S$")
        action_line, = ax_graph.plot([], [], color="#2F2F2F", linewidth=2.0)
        action_lines.append(action_line)
        ax_graph.axvline(0.0, color="#7E7468", linewidth=1.1, linestyle="--", alpha=0.85)
        zero_line = ax_graph.axhline(row_ranges[row][0], color="#7E7468", linewidth=1.0, linestyle="--", alpha=0.44)
        zero_lines.append(zero_line)
        zero_dots.append(
            ax_graph.scatter([], [], s=48, color="#2F2F2F", edgecolor="white", linewidth=0.8, zorder=6)
        )
        moving_dots.append(
            ax_graph.scatter([], [], s=105, color=BEAD_COLOR, edgecolor="white", linewidth=1.1, zorder=5)
        )
        tangent_line, = ax_graph.plot([], [], color=TRAIL_COLOR, linewidth=2.2, alpha=0.9)
        tangent_lines.append(tangent_line)
        ax_graph.text(
            0.5,
            0.09,
            row_notes[row],
            transform=ax_graph.transAxes,
            ha="center",
            va="center",
            fontsize=9.5,
            color="#4B463F",
            bbox={"boxstyle": "round,pad=0.23", "fc": "#FFFDF8", "ec": "#D7C6AA"},
        )
        y_min, y_max = row_ranges[row]
        margin = max(0.08 * (y_max - y_min), 0.035)
        ax_graph.set_xlim(-0.86, 0.86)
        ax_graph.set_ylim(y_min - margin, y_max + margin)

    def draw_frame(index: int):
        nonlocal bump_fills
        center = center_frames[index]
        current_epsilon = epsilon_frames[index]
        current_shape = wiggle_shape(center)

        for row, base in enumerate(bases):
            ax_path = axes[row, 0]
            base_action, linear, quadratic = action_coefficients(base, center)
            varied_path = path_x(base, current_epsilon, center)
            action_values = base_action + eps_values * linear + eps_values**2 * quadratic
            current_action = base_action + current_epsilon * linear + current_epsilon**2 * quadratic

            active_paths[row].set_data(varied_path, t)
            bump_fills[row].remove()
            bump_fills[row] = ax_path.fill_betweenx(
                t,
                base,
                base + current_epsilon * current_shape,
                color=BEAD_COLOR,
                alpha=0.15,
                linewidth=0,
            )
            labels[row].set_text(rf"local test at $t={center:.2f}$" + "\n" + rf"$\epsilon={current_epsilon:+.2f}$")
            action_lines[row].set_data(eps_values, action_values)
            zero_lines[row].set_ydata([base_action, base_action])
            zero_dots[row].set_offsets([[0.0, base_action]])
            moving_dots[row].set_offsets([[current_epsilon, current_action]])

            line_x = np.array([-0.28, 0.28])
            line_y = base_action + linear * line_x
            tangent_lines[row].set_data(line_x, line_y)

        return active_paths + zero_dots + moving_dots + tangent_lines + labels + action_lines

    draw_frame(0)
    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 24, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=24)
    draw_frame(frames - 1)
    fig.savefig(poster_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def make_geodesic_convergence_animation(path: Path) -> None:
    frames = 96
    phi_values = [-0.34, 0.34]
    theta_start = np.deg2rad(104)
    theta_end = np.deg2rad(16)
    theta_path = np.linspace(theta_start, theta_end, 360)

    def sphere_point(theta: np.ndarray | float, phi: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        radius = np.sin(theta)
        return radius * np.cos(phi), radius * np.sin(phi), np.cos(theta)

    fig = plt.figure(figsize=(7.2, 7.2))
    fig.patch.set_facecolor("#F7F3EC")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#FFFDF8")
    ax.set_title("Geodesics can converge on curved geometry", fontsize=15, color="#2F2F2F", pad=18)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-55)

    u = np.linspace(0, 2 * np.pi, 72)
    v = np.linspace(0, np.pi, 36)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, color="#E8F2F7", alpha=0.32, linewidth=0, shade=False)

    for phi in np.linspace(-0.9, 0.9, 5):
        gx, gy, gz = sphere_point(theta_path, phi)
        ax.plot(gx, gy, gz, color="#CFC2B0", linewidth=1.0, alpha=0.48)

    colors = ["#3D6FB6", BEAD_COLOR]
    trails = []
    for phi, color in zip(phi_values, colors):
        gx, gy, gz = sphere_point(theta_path, phi)
        ax.plot(gx, gy, gz, color="#7E7468", linewidth=1.15, alpha=0.34)
        trail, = ax.plot([], [], [], color=color, linewidth=3.1, alpha=0.94)
        trails.append(trail)

    x0_a, y0_a, z0_a = sphere_point(theta_start, phi_values[0])
    x0_b, y0_b, z0_b = sphere_point(theta_start, phi_values[1])
    beads = ax.scatter(
        [x0_a, x0_b],
        [y0_a, y0_b],
        [z0_a, z0_b],
        s=118,
        color=colors,
        edgecolor="white",
        linewidth=1.2,
        depthshade=False,
        zorder=6,
    )
    separation_line, = ax.plot([], [], [], color="#2F2F2F", linewidth=1.35, alpha=0.8)
    ax.text2D(
        0.5,
        0.92,
        "longitude lines are locally straight paths on the sphere",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9.5,
        color="#4B463F",
        bbox={"boxstyle": "round,pad=0.24", "fc": "#F1E6D2", "ec": "#D7C6AA"},
    )
    ax.text2D(
        0.5,
        0.07,
        "the beads move straight-on-the-surface, yet approach each other",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9.3,
        color="#4B463F",
        bbox={"boxstyle": "round,pad=0.22", "fc": "#FFFDF8", "ec": "#D7C6AA"},
    )
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.08, 1.08)
    ax.set_zlim(-1.02, 1.05)

    def draw_frame(index: int):
        progress = index / (frames - 1)
        upto = max(2, int(progress * (len(theta_path) - 1)))
        current_points = []
        for phi, trail in zip(phi_values, trails):
            gx, gy, gz = sphere_point(theta_path[:upto], phi)
            trail.set_data(gx, gy)
            trail.set_3d_properties(gz)
            current_points.append(sphere_point(theta_path[upto - 1], phi))

        bead_offsets = np.array(current_points, dtype=float)
        beads._offsets3d = (bead_offsets[:, 0], bead_offsets[:, 1], bead_offsets[:, 2])
        separation_line.set_data(bead_offsets[:, 0], bead_offsets[:, 1])
        separation_line.set_3d_properties(bead_offsets[:, 2])
        return trails + [beads, separation_line]

    draw_frame(0)
    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def main() -> None:
    make_possible_spacetime_paths(OUTPUT_DIR / "lm-possible-spacetime-paths.png")
    make_free_vs_uniform_force_spacetime(OUTPUT_DIR / "lm-free-vs-uniform-force-spacetime.png")
    make_fermat_snell_huygens_animation(OUTPUT_DIR / "lm-fermat-snell-huygens.mp4")
    make_plane_path_length_variation(OUTPUT_DIR / "lm-plane-path-length-variation.png")
    make_sphere_geodesic_sketch(OUTPUT_DIR / "lm-sphere-geodesic-sketch.png")
    make_mass_shell_spacetime_boost(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.png")
    make_mass_shell_spacetime_boost_animation(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.mp4")
    make_fixed_endpoint_action_sweep(
        OUTPUT_DIR / "lm-fixed-endpoint-action-sweep.mp4",
        OUTPUT_DIR / "lm-fixed-endpoint-action-sweep.png",
    )
    make_one_parameter_variation_slice(
        OUTPUT_DIR / "lm-one-parameter-variation-slice.mp4",
        OUTPUT_DIR / "lm-one-parameter-variation-slice.png",
    )
    make_geodesic_convergence_animation(OUTPUT_DIR / "lm-geodesic-convergence.mp4")


if __name__ == "__main__":
    main()
