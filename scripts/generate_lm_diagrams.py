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


def main() -> None:
    make_plane_path_length_variation(OUTPUT_DIR / "lm-plane-path-length-variation.png")
    make_sphere_geodesic_sketch(OUTPUT_DIR / "lm-sphere-geodesic-sketch.png")
    make_mass_shell_spacetime_boost(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.png")
    make_mass_shell_spacetime_boost_animation(OUTPUT_DIR / "lm-mass-shell-spacetime-boost.mp4")
    make_fixed_endpoint_action_sweep(
        OUTPUT_DIR / "lm-fixed-endpoint-action-sweep.mp4",
        OUTPUT_DIR / "lm-fixed-endpoint-action-sweep.png",
    )


if __name__ == "__main__":
    main()
