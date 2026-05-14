from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import FancyArrowPatch, Polygon

import scienceplots  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
LABEL_BOX = {
    "facecolor": "white",
    "edgecolor": "#D0D0D0",
    "linewidth": 0.6,
    "alpha": 0.92,
    "boxstyle": "round,pad=0.25",
}


def configure_style() -> None:
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.facecolor": "#fbfbfb",
            "figure.facecolor": "white",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
        }
    )


def save_animation(anim: FuncAnimation, path: Path, fps: int = 18) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2400,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def axes_label(ax: plt.Axes, text: str, x: float = 0.03, y: float = 0.97) -> None:
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.5,
        color="#333333",
        bbox=LABEL_BOX,
        zorder=10,
    )


def rk4_step(state: np.ndarray, dt: float) -> np.ndarray:
    def vf(s: np.ndarray) -> np.ndarray:
        q = s[..., 0]
        p = s[..., 1]
        return np.stack([p, -(q**3)], axis=-1)

    k1 = vf(state)
    k2 = vf(state + 0.5 * dt * k1)
    k3 = vf(state + 0.5 * dt * k2)
    k4 = vf(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def make_bulk_boundary_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 3.6))

    t = np.linspace(0.0, 1.0, 300)
    y = 0.35 * np.sin(np.pi * t) + 0.08 * np.sin(3 * np.pi * t)
    ax.plot(t, y, color="#355070", linewidth=2.2)

    interior_mask = (t > 0.36) & (t < 0.64)
    ax.plot(t[interior_mask], y[interior_mask] + 0.18 * np.sin(np.pi * (t[interior_mask] - 0.36) / 0.28), color="#6D597A", linewidth=2.0, linestyle="--")

    ax.annotate(
        "",
        xy=(0.98, y[-1] + 0.18),
        xytext=(0.98, y[-1]),
        arrowprops=dict(arrowstyle="->", color="#BC4749", linewidth=2),
    )
    ax.annotate(
        "",
        xy=(0.02, y[0] - 0.18),
        xytext=(0.02, y[0]),
        arrowprops=dict(arrowstyle="->", color="#BC4749", linewidth=2),
    )

    ax.text(0.49, 0.72, "bulk variation", ha="center", color="#6D597A")
    ax.text(0.78, 0.37, "boundary variation", ha="left", color="#BC4749", bbox=LABEL_BOX)
    ax.text(0.03, y[0] - 0.24, "boundary variation", ha="left", va="top", color="#BC4749", bbox=LABEL_BOX)
    ax.text(0.0, -0.42, "$t_1$", ha="center")
    ax.text(1.0, -0.42, "$t_2$", ha="center")

    ax.set_title("Bulk term and boundary term", pad=10)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.55, 0.95)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    save_figure(fig, path)


def make_bulk_boundary_animation(path: Path) -> None:
    t = np.linspace(0.0, 1.0, 520)
    q = 0.06 + 0.42 * t + 0.18 * np.sin(np.pi * t) - 0.055 * np.sin(2 * np.pi * t)
    qdot = 0.42 + 0.18 * np.pi * np.cos(np.pi * t) - 0.11 * np.pi * np.cos(2 * np.pi * t)
    qddot = -0.18 * np.pi**2 * np.sin(np.pi * t) + 0.22 * np.pi**2 * np.sin(2 * np.pi * t)

    # Concrete toy Lagrangian, used only to make the action readouts honest.
    def action(path: np.ndarray, velocity: np.ndarray) -> float:
        lagrangian = 0.5 * velocity**2 - 0.5 * path**2
        return float(np.trapezoid(lagrangian, t))

    base_action = action(q, qdot)
    bulk_coefficient = -q - qddot

    frames = 106
    bump_width = 0.18
    bump_height = 0.05

    fig, (ax_path, ax_terms) = plt.subplots(
        1,
        2,
        figsize=(10.8, 4.8),
        gridspec_kw={"width_ratios": [1.78, 1.02]},
    )

    def smoothstep(value: float) -> float:
        value = min(1.0, max(0.0, value))
        return value * value * (3.0 - 2.0 * value)

    def eta_at(center: float) -> tuple[np.ndarray, np.ndarray]:
        shifted = (t - center) / bump_width
        active = np.abs(shifted) < 1.0
        eta = np.zeros_like(t)
        etadot = np.zeros_like(t)
        eta[active] = 0.5 * bump_height * (1.0 + np.cos(np.pi * shifted[active]))
        etadot[active] = -0.5 * bump_height * (np.pi / bump_width) * np.sin(np.pi * shifted[active])
        return eta, etadot

    def draw_row(y: float, label: str, value: float, color: str = "#333333") -> None:
        if abs(value) < 0.00005:
            value = 0.0
        ax_terms.text(0.10, y, label, ha="left", va="center", fontsize=8.8, color="#333333")
        ax_terms.text(0.92, y, f"{value:+.4f}", ha="right", va="center", fontsize=8.8, color=color)

    def draw_frame(frame: int) -> None:
        ax_path.clear()
        ax_terms.clear()

        phase = smoothstep(frame / (frames - 1))
        center = 0.18 + 0.82 * phase
        eta, etadot = eta_at(center)
        varied = q + eta
        varied_dot = qdot + etadot
        varied_action = action(varied, varied_dot)
        delta_action = varied_action - base_action
        bulk_value = float(np.trapezoid(bulk_coefficient * eta, t))
        boundary_value = float(qdot[-1] * eta[-1] - qdot[0] * eta[0])

        ax_path.plot(t, q, color="#355070", linewidth=2.4, zorder=3)
        ax_path.plot(t, varied, color="#BC4749", linewidth=2.0, linestyle="--", zorder=4)
        active = eta > 0.006
        ax_path.fill_between(t[active], q[active], varied[active], color="#BC4749", alpha=0.13, zorder=1)

        ax_path.scatter([t[0], t[-1]], [q[0], q[-1]], s=34, color="#355070", zorder=5)
        if eta[-1] > 0.018:
            ax_path.scatter([t[-1]], [varied[-1]], s=38, color="#BC4749", zorder=6)

        ax_path.text(0.04, 0.92, r"moving local variation $\eta(t)$", transform=ax_path.transAxes, ha="left", va="center", color="#6D597A", fontsize=9.2, bbox=LABEL_BOX)

        ax_path.text(0.0, -0.13, r"$t_1$", ha="center", va="top", fontsize=10)
        ax_path.text(1.0, -0.13, r"$t_2$", ha="center", va="top", fontsize=10)
        ax_path.set_title("A variation of the history", pad=10)
        ax_path.set_xlabel("time t")
        ax_path.set_ylabel("configuration q")
        ax_path.set_xlim(-0.05, 1.05)
        ax_path.set_ylim(-0.16, 0.98)
        ax_path.set_xticks([])
        ax_path.set_yticks([])
        ax_path.grid(color="#E8E8E8", linewidth=0.7)

        ax_terms.axis("off")
        ax_terms.set_xlim(0, 1)
        ax_terms.set_ylim(0, 1)
        panel = plt.Rectangle((0.04, 0.06), 0.92, 0.88, facecolor="#F9F7F1", edgecolor="#CFCAC0", linewidth=1.0)
        ax_terms.add_patch(panel)
        ax_terms.text(0.5, 0.88, "action meter", ha="center", va="center", fontsize=10.2, color="#333333")
        ax_terms.text(0.5, 0.80, r"toy $L=(\dot q^2-q^2)/2$", ha="center", va="center", fontsize=9.2, color="#555555")
        ax_terms.plot([0.10, 0.92], [0.735, 0.735], color="#CFCAC0", linewidth=0.8)
        draw_row(0.66, r"$S[q]$", base_action, "#555555")
        draw_row(0.56, r"$S[q+\eta]$", varied_action, "#555555")
        draw_row(0.46, r"$\Delta S$", delta_action, "#333333")
        ax_terms.plot([0.10, 0.92], [0.395, 0.395], color="#CFCAC0", linewidth=0.8)
        ax_terms.text(0.5, 0.34, "first-order split", ha="center", va="center", fontsize=9.0, color="#333333")
        draw_row(0.265, "interior term", bulk_value, "#6D597A")
        draw_row(0.18, "endpoint term", boundary_value, "#BC4749")

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_one_form_two_form_diagram(path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.5))

    ax = axes[0]
    origin = np.array([0.0, 0.0])
    p_dir = np.array([1.0, 0.46])
    p_unit = p_dir / np.linalg.norm(p_dir)
    normal = np.array([-p_unit[1], p_unit[0]])
    dq = np.array([1.22, -0.34])
    projection = np.dot(dq, p_unit) * p_unit

    for level in np.linspace(-0.7, 0.85, 6):
        center = level * p_unit
        start = center - 1.5 * normal
        end = center + 1.5 * normal
        ax.plot([start[0], end[0]], [start[1], end[1]], color="#D7E2E8", linewidth=1.0, zorder=1)

    ax.scatter([0], [0], s=46, color="#333333", zorder=5)
    ax.annotate("", xy=1.18 * p_unit, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#4C78A8"), zorder=6)
    ax.annotate("", xy=dq, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#BC4749"), zorder=7)
    ax.plot([dq[0], projection[0]], [dq[1], projection[1]], color="#8A8A8A", linestyle=":", linewidth=1.2, zorder=4)
    ax.plot([0, projection[0]], [0, projection[1]], color="#D49A3A", linewidth=4.0, alpha=0.8, solid_capstyle="round", zorder=5)
    ax.scatter([projection[0]], [projection[1]], s=24, color="#D49A3A", zorder=8)

    ax.text(*(1.18 * p_unit + np.array([0.08, 0.02])), r"$p_i$", color="#4C78A8", va="center")
    ax.text(*(dq + np.array([0.08, -0.02])), r"$\delta q^i$", color="#BC4749", va="center")
    ax.text(*(0.52 * projection + np.array([0.02, 0.10])), '"overlap"', color="#9A6A1F", ha="center", va="bottom", fontsize=9.2, bbox=LABEL_BOX)
    ax.text(0.0, -1.05, r"one displaced state", ha="center", fontsize=10)
    ax.text(0.0, -1.33, r"$p_i\,\delta q^i$", ha="center", fontsize=12)
    ax.set_title("One-form: pairing")
    ax.set_aspect("equal")
    ax.set_xlim(-1.45, 1.75)
    ax.set_ylim(-1.5, 1.42)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1]
    origin = np.array([0.0, 0.0])
    dq = np.array([1.18, -0.12])
    dp = np.array([0.35, 1.02])
    patch = np.array([origin, origin + dq, origin + dq + dp, origin + dp])
    poly = Polygon(patch, closed=True, facecolor="#54A24B", alpha=0.25, edgecolor="#2A9D8F", linewidth=2.0)
    ax.add_patch(poly)
    ax.annotate("", xy=origin + dq, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#BC4749"))
    ax.annotate("", xy=origin + dp, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#4C78A8"))
    ax.text(*(origin + dq + np.array([0.1, -0.1])), r"$dq$", color="#BC4749")
    ax.text(*(origin + dp + np.array([0.06, 0.06])), r"$dp$", color="#4C78A8")
    ax.text(*(origin + 0.58 * (dq + dp) + np.array([0.02, 0.02])), "area", color="#2A9D8F", ha="center", va="center", fontsize=10.2, bbox=LABEL_BOX)
    ax.text(0.75, -1.05, r"patch of nearby states", ha="center", fontsize=10)
    ax.text(0.75, -1.33, r"$dq^i \wedge dp_i$", ha="center", fontsize=12)
    ax.set_title("Two-form: oriented area")
    ax.set_aspect("equal")
    ax.set_xlim(-0.6, 2.0)
    ax.set_ylim(-1.5, 1.7)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle("From pairing to oriented area", y=0.98)
    save_figure(fig, path)


def make_one_form_two_form_animation(path: Path) -> None:
    frames = 126
    radius = 0.95
    p_vec = np.array([0.78, 0.52], dtype=float)
    p_unit = p_vec / np.linalg.norm(p_vec)
    contour_dir = np.array([-p_unit[1], p_unit[0]])
    levels = np.linspace(-0.92, 0.92, 8)
    square = np.array([[-0.46, -0.32], [0.46, -0.32], [0.46, 0.32], [-0.46, 0.32]])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9))

    def draw_reference_axes(ax: plt.Axes) -> None:
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-1.32, 1.36)
        ax.set_ylim(-1.26, 1.34)
        ax.axhline(0, color="#AAAAAA", linewidth=0.9, zorder=0)
        ax.axvline(0, color="#AAAAAA", linewidth=0.9, zorder=0)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    def shear(points: np.ndarray, amount: float) -> np.ndarray:
        matrix = np.array([[1.0, amount], [0.0, 1.0]])
        return points @ matrix.T

    def draw_frame(frame: int) -> None:
        theta = 2.0 * np.pi * frame / frames
        displacement = radius * np.array([np.cos(theta), 0.85 * np.sin(theta)])
        action_change = float(np.dot(p_unit, displacement))
        shear_amount = 0.78 * np.sin(theta)

        ax = axes[0]
        ax.clear()
        draw_reference_axes(ax)
        ax.set_title("One-form: action gradient")
        for level in levels:
            center = level * p_unit
            start = center - 1.9 * contour_dir
            end = center + 1.9 * contour_dir
            ax.plot([start[0], end[0]], [start[1], end[1]], color="#D7E2E8", linewidth=1.0, zorder=1)
        projection = action_change * p_unit
        ax.plot([displacement[0], projection[0]], [displacement[1], projection[1]], color="#8A8A8A", linestyle=":", linewidth=1.2, zorder=3)
        ax.plot([0, projection[0]], [0, projection[1]], color="#D49A3A", linewidth=4.0, alpha=0.85, solid_capstyle="round", zorder=4)
        ax.annotate("", xy=0.68 * p_unit, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.5, color="#4C78A8"), zorder=5)
        ax.annotate("", xy=displacement, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.3, color="#BC4749"), zorder=6)
        ax.scatter([0], [0], s=34, color="#333333", zorder=7)
        ax.text(-1.16, 1.13, "action level sets", color="#4F6F7B", ha="left", va="top", fontsize=9.2, bbox=LABEL_BOX)
        ax.text(0.48, 0.55, r"$p_i$", color="#4C78A8", ha="left", va="bottom", fontsize=11.5)
        ax.text(-1.16, -1.05, rf"$\delta S_\partial = {action_change:+.2f}$", color="#9A6A1F", ha="left", va="center", fontsize=10.4, bbox=LABEL_BOX)

        ax = axes[1]
        ax.clear()
        draw_reference_axes(ax)
        ax.set_title("Two-form: state-area measure")
        grid = np.linspace(-1.15, 1.15, 25)
        for value in grid:
            vertical = np.column_stack([np.full(60, value), np.linspace(-1.15, 1.15, 60)])
            horizontal = np.column_stack([np.linspace(-1.15, 1.15, 60), np.full(60, value)])
            vertical_sheared = shear(vertical, shear_amount)
            horizontal_sheared = shear(horizontal, shear_amount)
            ax.plot(vertical_sheared[:, 0], vertical_sheared[:, 1], color="#D7E2E8", linewidth=0.55, zorder=1)
            ax.plot(horizontal_sheared[:, 0], horizontal_sheared[:, 1], color="#D7E2E8", linewidth=0.55, zorder=1)
        gx, gy = np.meshgrid(grid, grid)
        dots = np.column_stack([gx.ravel(), gy.ravel()])
        dots_sheared = shear(dots, shear_amount)
        ax.scatter(dots_sheared[:, 0], dots_sheared[:, 1], s=5.0, color="#8CB8C8", alpha=0.5, linewidth=0, zorder=2)
        patch = shear(square, shear_amount)
        poly = Polygon(patch, closed=True, facecolor="#54A24B", alpha=0.25, edgecolor="#2A9D8F", linewidth=2.2, zorder=3)
        ax.add_patch(poly)
        center = patch.mean(axis=0)
        ax.scatter([center[0]], [center[1]], s=28, color="#2A9D8F", zorder=4)
        ax.text(-1.16, 1.13, r"$dq^i \wedge dp_i$", color="#333333", ha="left", va="top", fontsize=12.0, bbox=LABEL_BOX)
        ax.text(-1.16, -1.05, "measured area stays fixed", color="#2A9D8F", ha="left", va="center", fontsize=10.0, bbox=LABEL_BOX)

        fig.suptitle("Action sensitivity and state-area measure", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_function_to_flow_animation(path: Path) -> None:
    q = np.linspace(-1.75, 1.75, 260)
    p = np.linspace(-1.65, 1.65, 240)
    qq, pp = np.meshgrid(q, p)
    F = 0.5 * pp**2 + 0.25 * qq**4
    contour_levels = [0.10, 0.24, 0.42, 0.68, 1.02, 1.46, 2.05]

    qv = np.linspace(-1.52, 1.52, 15)
    pv = np.linspace(-1.35, 1.35, 13)
    qvq, pvq = np.meshgrid(qv, pv)
    uq = pvq
    vp = -(qvq**3)
    speed = np.hypot(uq, vp)
    scale = np.maximum(speed, 1e-8)

    angles = np.linspace(0.0, 2.0 * np.pi, 110, endpoint=False)
    patch0 = np.column_stack(
        [
            0.96 + 0.16 * np.cos(angles),
            0.18 + 0.09 * np.sin(angles),
        ]
    )
    state = np.array([0.96, 0.18], dtype=float)
    dt = 0.04
    n_frames = 166
    patch_frames = np.empty((n_frames, len(patch0), 2))
    state_frames = np.empty((n_frames, 2))
    patch = patch0.copy()
    current = state.copy()
    for i in range(n_frames):
        patch_frames[i] = patch
        state_frames[i] = current
        patch = rk4_step(patch, dt)
        current = rk4_step(current, dt)

    fig, ax = plt.subplots(figsize=(6.9, 6.0))

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def setup_axes() -> None:
        ax.set_title("Function to flow", pad=10)
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.set_xlim(-1.75, 1.75)
        ax.set_ylim(-1.65, 1.65)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(color="#E6E6E6", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def draw_patch(points: np.ndarray, alpha: float = 0.24) -> None:
        ax.fill(points[:, 0], points[:, 1], color="#54A24B", alpha=alpha, zorder=4)
        closed = np.vstack([points, points[0]])
        ax.plot(closed[:, 0], closed[:, 1], color="#2A9D8F", linewidth=2.0, zorder=5)

    def draw_stage_label(text: str) -> None:
        ax.text(
            0.03,
            0.96,
            text,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9.4,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=20,
        )

    def draw_frame(frame: int) -> None:
        ax.clear()
        setup_axes()
        contour_alpha = 0.78 * smooth(frame / 26.0)
        vector_alpha = 0.52 * smooth((frame - 32) / 28.0)
        flow_progress = smooth((frame - 62) / 44.0)
        idx = min(int(flow_progress * (n_frames - 1)), n_frames - 1)

        if frame < 62:
            draw_patch(patch0, 0.12 + 0.10 * smooth(frame / 20.0))
        if contour_alpha > 0.01:
            ax.contour(qq, pp, F, levels=contour_levels, colors="#777777", linewidths=1.0, alpha=contour_alpha)
        if vector_alpha > 0.01:
            ax.quiver(
                qvq,
                pvq,
                uq / scale,
                vp / scale,
                color="#355070",
                alpha=vector_alpha,
                pivot="mid",
                scale=25,
                width=0.0042,
            )
        if frame < 32:
            draw_stage_label(r"$F(q,p)$ gives height over this plane")
        elif frame < 62:
            draw_stage_label("level sets show the function from above")
        else:
            draw_stage_label(r"$\dot q=\partial_pF,\quad \dot p=-\partial_qF$")

        if frame >= 62:
            trail = state_frames[: idx + 1]
            if len(trail) > 1:
                ax.plot(trail[:, 0], trail[:, 1], color="#BC4749", linewidth=1.8, alpha=0.75, zorder=6)
            draw_patch(patch_frames[idx], 0.23)
            ax.scatter([state_frames[idx, 0]], [state_frames[idx, 1]], s=36, color="#BC4749", edgecolor="white", linewidth=0.7, zorder=7)

    anim = FuncAnimation(fig, draw_frame, frames=n_frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_level_set_density_vector_diagram(path: Path) -> None:
    q = np.linspace(-1.75, 1.75, 320)
    p = np.linspace(-1.65, 1.65, 300)
    qq, pp = np.meshgrid(q, p)
    F = 0.5 * pp**2 + 0.25 * qq**4

    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    ax.contour(
        qq,
        pp,
        F,
        levels=[0.10, 0.24, 0.42, 0.68, 1.02, 1.46, 2.05, 2.80],
        colors="#777777",
        linewidths=1.0,
        alpha=0.76,
    )

    points = [
        (np.array([0.25, 0.76]), "sparser level sets", "shorter vector", (-0.95, 1.25)),
        (np.array([1.23, 0.76]), "denser level sets", "longer vector", (0.86, -1.08)),
    ]
    arrow_scale = 0.28
    for point, density_label, vector_label, label_pos in points:
        flow = np.array([point[1], -(point[0] ** 3)])
        arrow = arrow_scale * flow
        ax.scatter([point[0]], [point[1]], s=42, color="#333333", zorder=4)
        ax.annotate(
            "",
            xy=point + arrow,
            xytext=point,
            arrowprops=dict(arrowstyle="->", color="#355070", linewidth=2.5),
            zorder=5,
        )
        ax.text(
            label_pos[0],
            label_pos[1],
            f"{density_label}\n{vector_label}",
            ha="left",
            va="center",
            fontsize=9.6,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=6,
        )

    ax.text(
        0.03,
        0.96,
        "level-set density becomes vector length",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10.0,
        color="#333333",
        bbox=LABEL_BOX,
        zorder=8,
    )
    ax.text(
        0.03,
        0.07,
        r"$X_F=(\partial_pF,\,-\partial_qF)$",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=11.5,
        color="#355070",
        bbox=LABEL_BOX,
        zorder=8,
    )
    ax.set_title("From level sets to vector field", pad=10)
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.65, 1.65)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color="#E6E6E6", linewidth=0.7)
    ax.axhline(0, color="#B8B8B8", linewidth=0.8)
    ax.axvline(0, color="#B8B8B8", linewidth=0.8)
    save_figure(fig, path)


def make_patch_shear_animation(path: Path) -> None:
    patch = np.array([[-0.8, -0.5], [0.2, -0.5], [0.2, 0.5], [-0.8, 0.5]])
    frames = 96
    qv = np.linspace(-1.4, 1.4, 11)
    pv = np.linspace(-1.2, 1.2, 9)
    qvq, pvq = np.meshgrid(qv, pv)
    uq = pvq
    vp = np.zeros_like(pvq)

    fig, ax = plt.subplots(figsize=(6.8, 5.7))

    def draw_frame(frame: int) -> None:
        ax.clear()
        t = 1.15 * frame / (frames - 1)
        current = patch.copy()
        current[:, 0] = current[:, 0] + t * current[:, 1]

        ax.quiver(qvq, pvq, np.sign(uq) * np.minimum(np.abs(uq), 1.0), vp, color="#355070", alpha=0.45, pivot="mid", scale=20, width=0.004)
        ax.fill(current[:, 0], current[:, 1], color="#54A24B", alpha=0.22, zorder=2)
        closed = np.vstack([current, current[0]])
        ax.plot(closed[:, 0], closed[:, 1], color="#2A9D8F", linewidth=2.2, zorder=3)

        axes_label(ax, r"$H=p^2/2:\quad \dot q=p,\quad \dot p=0$")
        ax.set_title("Area-preserving shear", pad=10)
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.set_xlim(-1.6, 1.8)
        ax.set_ylim(-1.25, 1.25)
        ax.set_aspect("equal")
        ax.grid(color="#E8E8E8", linewidth=0.7)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_spring_ensemble_animation(path: Path) -> None:
    rng = np.random.default_rng(7)
    mean = np.array([1.0, 0.0])
    cov = np.array([[0.05, 0.018], [0.018, 0.025]])
    points0 = rng.multivariate_normal(mean, cov, size=360)
    frames = 112

    fig, ax = plt.subplots(figsize=(6.8, 5.7))

    def draw_frame(frame: int) -> None:
        ax.clear()
        t = 2.3 * np.pi * frame / (frames - 1)
        c = np.cos(t)
        s = np.sin(t)
        # SHO flow in position-velocity space for m = k = 1.
        rot = np.array([[c, s], [-s, c]])
        pts = points0 @ rot.T
        ax.scatter(pts[:, 0], pts[:, 1], s=10, color="#355070", alpha=0.22, edgecolors="none")
        ax.scatter([pts[:, 0].mean()], [pts[:, 1].mean()], s=50, color="#BC4749", zorder=3)
        axes_label(ax, r"$\dot q=v,\quad \dot v=-q$")
        ax.set_title("Ensemble transport", pad=10)
        ax.set_xlabel("position q")
        ax.set_ylabel("velocity v")
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.grid(color="#E8E8E8", linewidth=0.7)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_pendulum_phase_space_ensemble_animation(path: Path) -> None:
    theta = np.linspace(-np.pi, np.pi, 360)
    p = np.linspace(-2.6, 2.6, 320)
    tt, pp = np.meshgrid(theta, p)
    H = 0.5 * pp**2 + 1.0 - np.cos(tt)

    tv = np.linspace(-np.pi, np.pi, 19)
    pv = np.linspace(-2.35, 2.35, 15)
    tvq, pvq = np.meshgrid(tv, pv)
    u = pvq
    v = -np.sin(tvq)
    speed = np.hypot(u, v)
    scale = np.maximum(speed, 1e-8)

    rng = np.random.default_rng(23)
    mean = np.array([1.92, 0.22])
    cov = np.array([[0.0065, -0.0032], [-0.0032, 0.0075]])
    points = rng.multivariate_normal(mean, cov, size=520)
    patch0 = np.array([[1.78, 0.05], [2.05, -0.02], [2.12, 0.22], [1.85, 0.30]])
    tracer = np.array([1.05, 0.0], dtype=float)

    frames = 130
    dt = 0.045

    def wrap_angle(value: np.ndarray) -> np.ndarray:
        return (value + np.pi) % (2.0 * np.pi) - np.pi

    def vf(state: np.ndarray) -> np.ndarray:
        angle = state[..., 0]
        mom = state[..., 1]
        return np.stack([mom, -np.sin(angle)], axis=-1)

    def step(state: np.ndarray, h: float) -> np.ndarray:
        k1 = vf(state)
        k2 = vf(state + 0.5 * h * k1)
        k3 = vf(state + 0.5 * h * k2)
        k4 = vf(state + h * k3)
        out = state + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        out[..., 0] = wrap_angle(out[..., 0])
        return out

    point_frames = np.empty((frames, len(points), 2))
    patch_frames = np.empty((frames, len(patch0), 2))
    tracer_frames = np.empty((frames, 2))
    current_points = points.copy()
    current_patch = patch0.copy()
    current_tracer = tracer.copy()
    for i in range(frames):
        point_frames[i] = current_points
        patch_frames[i] = current_patch
        tracer_frames[i] = current_tracer
        for _ in range(2):
            current_points = step(current_points, dt)
            current_patch = step(current_patch, dt)
            current_tracer = step(current_tracer, dt)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8), gridspec_kw={"width_ratios": [1.0, 2.15]})

    def draw_frame(frame: int) -> None:
        pend_ax, phase_ax = axes
        pend_ax.clear()
        phase_ax.clear()

        selected = tracer_frames[frame]
        angle = selected[0]
        bob = np.array([np.sin(angle), -np.cos(angle)])

        pend_ax.plot([0, bob[0]], [0, bob[1]], color="#355070", linewidth=2.4)
        pend_ax.scatter([bob[0]], [bob[1]], s=130, color="#BC4749", zorder=3)
        pend_ax.plot([-1.15, 1.15], [0, 0], color="#B8B8B8", linewidth=1.0)
        pend_ax.scatter([0], [0], s=24, color="#333333", zorder=4)
        pend_ax.set_title("one member", pad=9)
        pend_ax.set_xlim(-1.25, 1.25)
        pend_ax.set_ylim(-1.25, 0.35)
        pend_ax.set_aspect("equal")
        pend_ax.axis("off")

        phase_ax.contour(theta, p, H, levels=[0.25, 0.65, 1.05, 1.45, 1.85, 2.0, 2.35, 2.8, 3.4, 4.2], colors="#777777", linewidths=0.8, alpha=0.56)
        phase_ax.contour(theta, p, H, levels=[2.0], colors="#BC4749", linewidths=1.8, alpha=0.9)
        phase_ax.quiver(tvq, pvq, u / scale, v / scale, color="#355070", alpha=0.35, pivot="mid", scale=28, width=0.0038)

        pts = point_frames[frame]
        phase_ax.scatter(pts[:, 0], pts[:, 1], s=9, color="#355070", alpha=0.18, edgecolors="none", zorder=2)
        poly = patch_frames[frame]
        phase_ax.fill(poly[:, 0], poly[:, 1], color="#54A24B", alpha=0.20, zorder=3)
        closed = np.vstack([poly, poly[0]])
        phase_ax.plot(closed[:, 0], closed[:, 1], color="#2A9D8F", linewidth=1.8, zorder=4)
        phase_ax.scatter([selected[0]], [selected[1]], s=35, color="#BC4749", zorder=5)

        phase_ax.text(
            0.03,
            0.96,
            r"$H=p^2/2+1-\cos\theta$",
            transform=phase_ax.transAxes,
            ha="left",
            va="top",
            fontsize=9.5,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=10,
        )
        phase_ax.text(
            0.97,
            0.96,
            "separatrix",
            transform=phase_ax.transAxes,
            ha="right",
            va="top",
            fontsize=9.0,
            color="#BC4749",
            zorder=10,
        )
        phase_ax.set_title("Pendulum ensemble in phase space", pad=9)
        phase_ax.set_xlabel(r"angle $\theta$")
        phase_ax.set_ylabel("momentum p")
        phase_ax.set_xlim(-np.pi, np.pi)
        phase_ax.set_ylim(-2.6, 2.6)
        phase_ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
        phase_ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
        phase_ax.grid(color="#E8E8E8", linewidth=0.6)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 20, blit=False)
    save_animation(anim, path, fps=20)
    plt.close(fig)


def make_pendulum_regimes_animation(path: Path) -> None:
    theta = np.linspace(-np.pi, np.pi, 360)
    p = np.linspace(-2.7, 2.7, 320)
    tt, pp = np.meshgrid(theta, p)
    H = 0.5 * pp**2 + 1.0 - np.cos(tt)

    frames = 140
    dt = 0.04
    states0 = {
        "oscillation": np.array([1.05, 0.0], dtype=float),
        "near boundary": np.array([2.45, 0.08], dtype=float),
        "rotation": np.array([0.0, 2.18], dtype=float),
    }
    colors = {
        "oscillation": "#355070",
        "near boundary": "#BC4749",
        "rotation": "#2A9D8F",
    }

    def wrap_angle(value: np.ndarray) -> np.ndarray:
        return (value + np.pi) % (2.0 * np.pi) - np.pi

    def vf(state: np.ndarray) -> np.ndarray:
        angle = state[..., 0]
        mom = state[..., 1]
        return np.stack([mom, -np.sin(angle)], axis=-1)

    def step(state: np.ndarray, h: float) -> np.ndarray:
        k1 = vf(state)
        k2 = vf(state + 0.5 * h * k1)
        k3 = vf(state + 0.5 * h * k2)
        k4 = vf(state + h * k3)
        out = state + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        out[..., 0] = wrap_angle(out[..., 0])
        return out

    histories: dict[str, np.ndarray] = {}
    for name, state0 in states0.items():
        current = state0.copy()
        hist = np.empty((frames, 2))
        for i in range(frames):
            hist[i] = current
            for _ in range(2):
                current = step(current, dt)
        histories[name] = hist

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8), gridspec_kw={"width_ratios": [1.15, 1.85]})

    def draw_pendulum(ax: plt.Axes, angle: float, x_offset: float, color: str, label: str) -> None:
        pivot = np.array([x_offset, 0.0])
        bob = pivot + np.array([0.68 * np.sin(angle), -0.68 * np.cos(angle)])
        ax.plot([pivot[0], bob[0]], [pivot[1], bob[1]], color="#355070", linewidth=2.0)
        ax.scatter([bob[0]], [bob[1]], s=82, color=color, zorder=3)
        ax.scatter([pivot[0]], [pivot[1]], s=18, color="#333333", zorder=4)
        ax.text(x_offset, -0.93, label, ha="center", va="top", fontsize=9.0, color=color)

    def draw_frame(frame: int) -> None:
        pend_ax, phase_ax = axes
        pend_ax.clear()
        phase_ax.clear()

        pend_ax.plot([-1.55, 1.55], [0, 0], color="#B8B8B8", linewidth=1.0)
        draw_pendulum(pend_ax, histories["oscillation"][frame, 0], -0.95, colors["oscillation"], "oscillates")
        draw_pendulum(pend_ax, histories["near boundary"][frame, 0], 0.0, colors["near boundary"], "near boundary")
        draw_pendulum(pend_ax, histories["rotation"][frame, 0], 0.95, colors["rotation"], "rotates")
        pend_ax.set_title("same system, different regimes", pad=9)
        pend_ax.set_xlim(-1.75, 1.75)
        pend_ax.set_ylim(-1.15, 0.35)
        pend_ax.set_aspect("equal")
        pend_ax.axis("off")

        phase_ax.contour(theta, p, H, levels=[0.25, 0.65, 1.05, 1.45, 1.85, 2.0, 2.35, 2.8, 3.4, 4.2], colors="#777777", linewidths=0.85, alpha=0.6)
        phase_ax.contour(theta, p, H, levels=[2.0], colors="#BC4749", linewidths=1.8, alpha=0.9)
        for name, hist in histories.items():
            n = min(frame + 1, len(hist))
            # Break wrapped paths so the trace does not draw across the periodic boundary.
            trace = hist[:n].copy()
            jumps = np.where(np.abs(np.diff(trace[:, 0])) > np.pi)[0]
            start = 0
            for jump in jumps:
                segment = trace[start : jump + 1]
                phase_ax.plot(segment[:, 0], segment[:, 1], color=colors[name], linewidth=1.7, alpha=0.85)
                start = jump + 1
            segment = trace[start:]
            if len(segment) > 1:
                phase_ax.plot(segment[:, 0], segment[:, 1], color=colors[name], linewidth=1.7, alpha=0.85)
            phase_ax.scatter([hist[frame, 0]], [hist[frame, 1]], s=34, color=colors[name], zorder=5)

        phase_ax.text(
            0.03,
            0.96,
            r"$\dot\theta=p,\quad \dot p=-\sin\theta$",
            transform=phase_ax.transAxes,
            ha="left",
            va="top",
            fontsize=9.5,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=10,
        )
        phase_ax.text(
            0.97,
            0.96,
            "separatrix",
            transform=phase_ax.transAxes,
            ha="right",
            va="top",
            fontsize=9.0,
            color="#BC4749",
            zorder=10,
        )
        phase_ax.set_title("Pendulum phase portrait", pad=9)
        phase_ax.set_xlabel(r"angle $\theta$")
        phase_ax.set_ylabel("momentum p")
        phase_ax.set_xlim(-np.pi, np.pi)
        phase_ax.set_ylim(-2.7, 2.7)
        phase_ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
        phase_ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
        phase_ax.grid(color="#E8E8E8", linewidth=0.6)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 20, blit=False)
    save_animation(anim, path, fps=20)
    plt.close(fig)


def make_incompressible_fluid_animation(path: Path) -> None:
    x = np.linspace(-1.7, 1.7, 280)
    y = np.linspace(-1.6, 1.6, 260)
    xx, yy = np.meshgrid(x, y)
    psi = 0.5 * yy**2 + 0.25 * xx**4

    xv = np.linspace(-1.5, 1.5, 13)
    yv = np.linspace(-1.35, 1.35, 11)
    xvq, yvq = np.meshgrid(xv, yv)
    u = yvq
    v = -(xvq**3)
    speed = np.hypot(u, v)
    scale = np.maximum(speed, 1e-8)

    angles = np.linspace(0.0, 2.0 * np.pi, 180, endpoint=False)
    patch0 = np.column_stack(
        [
            -0.74 + 0.28 * np.cos(angles),
            -0.05 + 0.20 * np.sin(angles),
        ]
    )
    dt = 0.035
    frames = 112

    def vf_xy(s: np.ndarray) -> np.ndarray:
        xpos = s[..., 0]
        ypos = s[..., 1]
        return np.stack([ypos, -(xpos**3)], axis=-1)

    def rk4_xy(state: np.ndarray, h: float) -> np.ndarray:
        k1 = vf_xy(state)
        k2 = vf_xy(state + 0.5 * h * k1)
        k3 = vf_xy(state + 0.5 * h * k2)
        k4 = vf_xy(state + h * k3)
        return state + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    patch_frames = np.empty((frames, len(patch0), 2))
    current = patch0.copy()
    for i in range(frames):
        patch_frames[i] = current
        current = rk4_xy(current, dt)

    fig, ax = plt.subplots(figsize=(6.8, 5.8))

    def draw_frame(frame: int) -> None:
        ax.clear()
        phase = min(frame / 22.0, 1.0)
        ax.contour(xx, yy, psi, levels=[0.12, 0.28, 0.52, 0.85, 1.28, 1.82], colors="#7A7A7A", linewidths=1.0, alpha=0.6)
        ax.quiver(xvq, yvq, u / scale, v / scale, color="#355070", alpha=0.08 + 0.7 * phase, pivot="mid", scale=24, width=0.0045)

        poly = patch_frames[frame]
        closed = np.vstack([poly, poly[0]])
        ax.fill(poly[:, 0], poly[:, 1], color="#54A24B", alpha=0.22, zorder=2)
        ax.plot(closed[:, 0], closed[:, 1], color="#2A9D8F", linewidth=2.1, zorder=3)

        axes_label(ax, r"$u=\partial_y\psi,\quad v=-\partial_x\psi$")
        ax.set_title("Incompressible patch transport", pad=10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.grid(color="#E8E8E8", linewidth=0.7)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_legendre_trade_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    left_box = plt.Rectangle((0.8, 1.35), 2.1, 1.2, facecolor="#E9EEF6", edgecolor="#355070", linewidth=1.8)
    right_box = plt.Rectangle((7.0, 1.35), 2.1, 1.2, facecolor="#EAF5EE", edgecolor="#2A9D8F", linewidth=1.8)
    ax.add_patch(left_box)
    ax.add_patch(right_box)
    ax.text(1.85, 1.95, r"$(q,\dot q)$", ha="center", va="center", fontsize=14)
    ax.text(8.05, 1.95, r"$(q,p)$", ha="center", va="center", fontsize=14)

    arrow = FancyArrowPatch((3.05, 1.95), (6.85, 1.95), arrowstyle="simple", mutation_scale=18, color="#BC4749", alpha=0.85)
    ax.add_patch(arrow)
    ax.text(4.95, 2.28, r"$p_i=\partial L/\partial \dot q^i$", ha="center", va="bottom", color="#BC4749")
    ax.text(4.95, 1.45, r"$H(q,p)=p_i\dot q^i-L$", ha="center", va="top", color="#333333")

    ax.set_title("Legendre transform: velocities to momenta", pad=12)
    save_figure(fig, path)


def make_legendre_tangent_animation(path: Path) -> None:
    velocity = np.linspace(0.0, 2.45, 360)
    lagrangian = 0.5 * velocity**2
    momentum = np.linspace(0.0, 2.45, 360)
    hamiltonian = 0.5 * momentum**2

    frames = 132
    fig, (ax_l, ax_h) = plt.subplots(1, 2, figsize=(10.8, 5.2), gridspec_kw={"width_ratios": [1.15, 1.0]})
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.84, wspace=0.24)

    def draw_frame(frame: int) -> None:
        ax_l.clear()
        ax_h.clear()

        phase = 2.0 * np.pi * frame / frames
        v0 = 1.38 + 0.62 * np.sin(phase)
        p0 = v0
        l0 = 0.5 * v0**2
        h0 = p0 * v0 - l0
        tangent = l0 + p0 * (velocity - v0)

        ax_l.plot(velocity, lagrangian, color="#355070", linewidth=2.2)
        ax_l.plot(velocity, tangent, color="#BC4749", linewidth=1.8, alpha=0.88)
        ax_l.scatter([v0], [l0], s=44, color="#BC4749", zorder=5)
        ax_l.plot([v0, v0], [0, l0], color="#999999", linestyle="--", linewidth=1.0)
        ax_l.plot([0, v0], [l0, l0], color="#999999", linestyle="--", linewidth=1.0)
        ax_l.scatter([0], [-h0], s=30, color="#2A9D8F", zorder=5)
        ax_l.annotate(
            "",
            xy=(0, 0),
            xytext=(0, -h0),
            arrowprops=dict(arrowstyle="<->", color="#2A9D8F", linewidth=2.0),
            zorder=6,
        )
        ax_l.text(0.08, -0.52 * h0, r"$H=p\dot q-L$", color="#2A9D8F", ha="left", va="center", fontsize=10.5, bbox=LABEL_BOX)
        ax_l.text(v0 + 0.06, l0 + 0.14, r"$p=\partial L/\partial \dot q$", color="#BC4749", ha="left", va="bottom", fontsize=10.0, bbox=LABEL_BOX)
        ax_l.text(v0, -0.28, r"$\dot q$", color="#333333", ha="center", va="top", fontsize=10.0)
        ax_l.text(0.04, 0.95, "tangent data", transform=ax_l.transAxes, ha="left", va="top", fontsize=10.0, color="#333333", bbox=LABEL_BOX)
        ax_l.set_title(r"Start with $L(\dot q)$")
        ax_l.set_xlabel(r"velocity $\dot q$")
        ax_l.set_ylabel("L")
        ax_l.set_xlim(-0.08, 2.45)
        ax_l.set_ylim(-2.35, 3.05)
        ax_l.grid(color="#E8E8E8", linewidth=0.7)
        ax_l.spines["bottom"].set_linewidth(1.1)

        ax_h.plot(momentum, hamiltonian, color="#355070", linewidth=2.2)
        ax_h.scatter([p0], [h0], s=44, color="#2A9D8F", zorder=5)
        ax_h.plot([p0, p0], [0, h0], color="#999999", linestyle="--", linewidth=1.0)
        ax_h.plot([0, p0], [h0, h0], color="#999999", linestyle="--", linewidth=1.0)
        ax_h.text(p0, -0.18, r"$p$", color="#333333", ha="center", va="top", fontsize=10.0)
        ax_h.text(0.08, h0 + 0.08, r"$H(p)$", color="#2A9D8F", ha="left", va="bottom", fontsize=10.5, bbox=LABEL_BOX)
        ax_h.text(0.04, 0.95, "slope becomes coordinate", transform=ax_h.transAxes, ha="left", va="top", fontsize=10.0, color="#333333", bbox=LABEL_BOX)
        ax_h.set_title("Rewrite by momentum")
        ax_h.set_xlabel("momentum p")
        ax_h.set_ylabel("H")
        ax_h.set_xlim(-0.08, 2.45)
        ax_h.set_ylim(-0.28, 3.05)
        ax_h.grid(color="#E8E8E8", linewidth=0.7)
        ax_h.spines["bottom"].set_linewidth(1.1)

        fig.suptitle("Legendre transform: velocity traded for tangent slope", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_relativistic_boundary_pairing_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)

    ax.annotate("", xy=(0.9, 5.3), xytext=(0.9, 0.7), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.annotate("", xy=(5.4, 0.9), xytext=(0.7, 0.9), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.text(0.55, 5.35, "t", color="#555555")
    ax.text(5.45, 0.63, "x", color="#555555")

    path_x = np.linspace(1.2, 4.5, 200)
    path_t = 1.15 + 0.8 * path_x + 0.25 * np.sin(1.1 * path_x)
    ax.plot(path_x, path_t, color="#355070", linewidth=2.2)
    end = np.array([path_x[-1], path_t[-1]])
    disp = np.array([1.35, 0.85])
    ax.scatter([end[0]], [end[1]], s=35, color="#355070", zorder=3)
    ax.annotate("", xy=end + disp, xytext=end, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#BC4749"))
    ax.text(*(end + disp + np.array([0.1, 0.05])), r"$\delta x^\mu$", color="#BC4749")

    ax.text(8.3, 4.3, r"$p_\mu\,\delta x^\mu$", fontsize=16, ha="center")
    ax.text(8.3, 2.8, r"$p_i\,\delta q^i - E\,\delta t$", fontsize=16, ha="center", color="#333333")
    ax.annotate("", xy=(8.3, 3.95), xytext=(8.3, 3.15), arrowprops=dict(arrowstyle="->", linewidth=1.8, color="#6D597A"))

    ax.set_title("Boundary pairing under time slicing", pad=12)
    save_figure(fig, path)


def make_endpoint_covector_animation(path: Path) -> None:
    frames = 126
    radius = 0.82
    p_vec = np.array([0.74, -1.0], dtype=float)
    p_unit = p_vec / np.linalg.norm(p_vec)
    contour_dir = np.array([-p_unit[1], p_unit[0]])
    levels = np.linspace(-0.9, 0.9, 7)
    max_value = radius

    fig, (ax_plane, ax_meter) = plt.subplots(
        1,
        2,
        figsize=(10.8, 5.0),
        gridspec_kw={"width_ratios": [1.45, 1.0]},
    )

    def draw_meter(value: float) -> None:
        ax_meter.axis("off")
        ax_meter.set_xlim(0, 1)
        ax_meter.set_ylim(0, 1)
        panel = plt.Rectangle((0.06, 0.08), 0.88, 0.84, facecolor="#F9F7F1", edgecolor="#CFCAC0", linewidth=1.0)
        ax_meter.add_patch(panel)

        ax_meter.text(0.5, 0.82, "boundary scalar", ha="center", va="center", fontsize=10.4, color="#333333")
        ax_meter.text(0.5, 0.69, r"$\delta S_{\partial}\approx p_\mu\,\delta x^\mu$", ha="center", va="center", fontsize=14.0, color="#333333")
        ax_meter.text(0.5, 0.55, f"{value:+.3f}", ha="center", va="center", fontsize=15.5, color="#BC4749")

        x0, x1, y = 0.18, 0.82, 0.39
        ax_meter.plot([x0, x1], [y, y], color="#C9C4BA", linewidth=2.0, solid_capstyle="round")
        ax_meter.plot([0.5, 0.5], [y - 0.045, y + 0.045], color="#777777", linewidth=1.1)
        marker_x = 0.5 + 0.31 * float(np.clip(value / max_value, -1.0, 1.0))
        ax_meter.plot([0.5, marker_x], [y, y], color="#BC4749", linewidth=4.0, solid_capstyle="round")
        ax_meter.scatter([marker_x], [y], s=70, color="#BC4749", edgecolor="white", linewidth=0.8, zorder=4)
        ax_meter.text(x0, y - 0.09, "-", ha="center", va="center", fontsize=11, color="#666666")
        ax_meter.text(x1, y - 0.09, "+", ha="center", va="center", fontsize=11, color="#666666")

        ax_meter.text(0.5, 0.22, "parallel to a contour, the first-order change vanishes", ha="center", va="center", fontsize=8.8, color="#555555")

    def draw_frame(frame: int) -> None:
        ax_plane.clear()
        ax_meter.clear()

        theta = 2.0 * np.pi * frame / frames
        displacement = radius * np.array([np.cos(theta), 0.82 * np.sin(theta)])
        value = float(np.dot(p_unit, displacement))

        ax_plane.set_aspect("equal", adjustable="box")
        ax_plane.set_xlim(-1.18, 1.18)
        ax_plane.set_ylim(-1.18, 1.18)
        ax_plane.set_facecolor("#FBFBFB")
        ax_plane.grid(color="#ECECEC", linewidth=0.7)
        ax_plane.axhline(0, color="#AAAAAA", linewidth=1.0)
        ax_plane.axvline(0, color="#AAAAAA", linewidth=1.0)

        for level in levels:
            center = level * p_unit
            start = center - 1.9 * contour_dir
            end = center + 1.9 * contour_dir
            ax_plane.plot([start[0], end[0]], [start[1], end[1]], color="#C7D5DD", linewidth=1.1, alpha=0.85, zorder=1)

        ax_plane.scatter([0], [0], s=42, color="#333333", zorder=5)
        ax_plane.annotate("", xy=0.55 * p_unit, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.5, color="#BC4749"), zorder=6)
        ax_plane.annotate("", xy=displacement, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.3, color="#355070"), zorder=7)
        ax_plane.scatter([displacement[0]], [displacement[1]], s=32, color="#355070", edgecolor="white", linewidth=0.7, zorder=8)

        ax_plane.text(0.08, 0.94, "equal boundary-action contours", transform=ax_plane.transAxes, ha="left", va="center", fontsize=9.0, color="#4F6F7B", bbox=LABEL_BOX)
        ax_plane.text(0.63, 0.65, r"$p_\mu$", transform=ax_plane.transAxes, ha="left", va="center", fontsize=12.0, color="#BC4749")
        ax_plane.text(0.74, 0.18, r"$\delta x^\mu$", transform=ax_plane.transAxes, ha="left", va="center", fontsize=12.0, color="#355070")
        ax_plane.set_title("A covector measures endpoint displacement", pad=10)
        ax_plane.set_xlabel(r"spatial displacement $\delta x$")
        ax_plane.set_ylabel(r"time displacement $\delta t$")
        ax_plane.set_xticks([])
        ax_plane.set_yticks([])
        for spine in ax_plane.spines.values():
            spine.set_visible(False)

        draw_meter(value)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_worldline_phase_space_bridge_diagram(path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.2))

    ax = axes[0]
    ax.annotate("", xy=(0.12, 0.92), xytext=(0.12, 0.12), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.annotate("", xy=(0.92, 0.12), xytext=(0.12, 0.12), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    x = np.linspace(0.18, 0.84, 200)
    t = 0.18 + 0.7 * x + 0.06 * np.sin(8 * x)
    ax.plot(x, t, color="#355070", linewidth=2.2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Worldline")

    ax = axes[1]
    ax.annotate("", xy=(0.12, 0.92), xytext=(0.12, 0.12), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.annotate("", xy=(0.92, 0.12), xytext=(0.12, 0.12), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.scatter([0.58], [0.48], s=55, color="#BC4749")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("Phase space")

    fig.suptitle("From a full history to an instantaneous state", y=0.98)
    save_figure(fig, path)


def make_worldline_phase_space_bridge_animation(path: Path) -> None:
    frames = 126
    t = np.linspace(0.0, 1.0, 260)
    x = 0.62 * np.cos(1.7 * np.pi * t) + 0.18 * t
    y = 0.42 * np.sin(1.35 * np.pi * t) - 0.08 * t

    qv = np.linspace(-1.35, 1.35, 13)
    pv = np.linspace(-1.35, 1.35, 13)
    qq, pp = np.meshgrid(qv, pv)
    uq = pp
    vp = -qq
    speed = np.hypot(uq, vp)
    scale = np.maximum(speed, 1e-8)

    contour_axis = np.linspace(-1.55, 1.55, 240)
    cq, cp = np.meshgrid(contour_axis, contour_axis)
    H = 0.5 * (cq**2 + cp**2)

    def orbit_points(progress: np.ndarray) -> np.ndarray:
        angle = 0.16 + 2.25 * np.pi * progress
        radius = 1.08
        return np.column_stack([radius * np.cos(angle), -radius * np.sin(angle)])

    path_points = orbit_points(np.linspace(0.0, 1.0, frames))
    guide_points = orbit_points(np.linspace(0.0, 1.0, 420))
    ellipse_theta = np.linspace(0, 2 * np.pi, 80)

    fig = plt.figure(figsize=(11.2, 5.0))
    ax_world = fig.add_subplot(1, 2, 1, projection="3d")
    ax_phase = fig.add_subplot(1, 2, 2)
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.13, top=0.84, wspace=0.22)
    fig.suptitle("Static worldline, moving phase-space state", y=0.96)

    def draw_worldline() -> None:
        ax_world.clear()
        ax_world.plot(x, y, t, color="#355070", linewidth=2.4)
        ax_world.scatter([x[0]], [y[0]], [t[0]], s=28, color="#355070")
        ax_world.scatter([x[-1]], [y[-1]], [t[-1]], s=32, color="#BC4749")
        ax_world.text(x[0] - 0.1, y[0] - 0.04, t[0] - 0.05, r"$t_1$", color="#355070", fontsize=9)
        ax_world.text(x[-1] + 0.04, y[-1] + 0.03, t[-1] + 0.04, r"$t_2$", color="#BC4749", fontsize=9)
        ax_world.set_title("Spacetime diagram: history as shape", pad=10)
        ax_world.set_xlabel("x")
        ax_world.set_ylabel("y")
        ax_world.set_zlabel("t")
        ax_world.set_xlim(-0.78, 0.88)
        ax_world.set_ylim(-0.64, 0.58)
        ax_world.set_zlim(0, 1)
        ax_world.set_xticks([])
        ax_world.set_yticks([])
        ax_world.set_zticks([])
        ax_world.view_init(elev=24, azim=-58)
        ax_world.grid(color="#E8E8E8")
        ax_world.xaxis.pane.set_facecolor((0.98, 0.98, 0.98, 1.0))
        ax_world.yaxis.pane.set_facecolor((0.98, 0.98, 0.98, 1.0))
        ax_world.zaxis.pane.set_facecolor((0.98, 0.98, 0.98, 1.0))

    def state_patch(center: np.ndarray) -> np.ndarray:
        flow = np.array([center[1], -center[0]])
        tangent = flow / np.maximum(np.linalg.norm(flow), 1e-8)
        normal = np.array([-tangent[1], tangent[0]])
        return (
            center
            + 0.18 * np.cos(ellipse_theta)[:, None] * tangent
            + 0.075 * np.sin(ellipse_theta)[:, None] * normal
        )

    def draw_recent_tail(points: np.ndarray) -> None:
        if len(points) < 2:
            return

        weights = np.linspace(0.0, 1.0, len(points) - 1)
        for index, weight in enumerate(weights):
            segment = points[index : index + 2]
            ax_phase.plot(
                segment[:, 0],
                segment[:, 1],
                color="#BC4749",
                linewidth=0.8 + 1.3 * weight,
                alpha=0.14 + 0.56 * weight,
                solid_capstyle="round",
                zorder=4,
            )

    def draw_frame(frame: int) -> None:
        draw_worldline()
        ax_phase.clear()

        state = path_points[frame]
        patch = state_patch(state)
        tail = path_points[max(0, frame - 28) : frame + 1]

        ax_phase.contour(cq, cp, H, levels=[0.18, 0.38, 0.68, 1.05], colors="#B8B8B8", linewidths=0.9, alpha=0.68)
        ax_phase.quiver(
            qq,
            pp,
            uq / scale,
            vp / scale,
            color="#355070",
            alpha=0.34,
            pivot="mid",
            scale=24,
            width=0.0042,
            zorder=2,
        )
        ax_phase.plot(guide_points[:, 0], guide_points[:, 1], color="#BC4749", linewidth=1.1, alpha=0.16, zorder=3)
        draw_recent_tail(tail)
        ax_phase.fill(patch[:, 0], patch[:, 1], color="#2A9D8F", alpha=0.18, zorder=5)
        ax_phase.plot(patch[:, 0], patch[:, 1], color="#2A9D8F", linewidth=2.0, zorder=6)
        ax_phase.scatter([state[0]], [state[1]], s=44, color="#BC4749", edgecolor="white", linewidth=0.7, zorder=6)
        ax_phase.set_title("Phase space: state carried by flow", pad=10)
        ax_phase.set_xlabel("q")
        ax_phase.set_ylabel("p")
        ax_phase.set_xlim(-1.55, 1.55)
        ax_phase.set_ylim(-1.55, 1.55)
        ax_phase.set_aspect("equal", adjustable="box")
        ax_phase.set_xticks([])
        ax_phase.set_yticks([])
        ax_phase.grid(color="#ECECEC", linewidth=0.7)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_action_decomposition_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)

    origin = np.array([1.0, 0.95])
    dx = np.array([3.65, 0.0])
    dt = np.array([0.0, 3.15])
    disp = dx + dt
    end = origin + disp

    ax.annotate("", xy=(5.25, origin[1]), xytext=(0.65, origin[1]), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.annotate("", xy=(origin[0], 4.65), xytext=(origin[0], 0.55), arrowprops=dict(arrowstyle="-", linewidth=1.2, color="#999999"))
    ax.text(5.35, origin[1] - 0.18, "space", ha="left", va="top", fontsize=9.5, color="#555555")
    ax.text(origin[0] - 0.18, 4.72, "time", ha="right", va="bottom", fontsize=9.5, color="#555555")

    ax.plot([origin[0], end[0]], [origin[1], end[1]], color="#355070", linewidth=2.4, zorder=3)
    ax.scatter([origin[0], end[0]], [origin[1], end[1]], s=[28, 34], color=["#355070", "#BC4749"], zorder=4)
    ax.plot([end[0], end[0]], [origin[1], end[1]], color="#4C78A8", linewidth=2.0, linestyle="--")
    ax.plot([origin[0], end[0]], [origin[1], origin[1]], color="#BC4749", linewidth=2.0, linestyle="--")

    ax.annotate("", xy=origin + dx, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#BC4749"))
    ax.annotate("", xy=end, xytext=origin + dx, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#4C78A8"))
    ax.annotate("", xy=end, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.3, color="#355070"))

    ax.text(*(origin + dx / 2 + np.array([0.0, -0.33])), r"$dx$", color="#BC4749", ha="center", va="top", fontsize=12)
    ax.text(*(origin + dx + dt / 2 + np.array([0.2, 0.0])), r"$dt$", color="#4C78A8", ha="left", va="center", fontsize=12)
    ax.text(*(origin + 0.55 * disp + np.array([-0.12, 0.22])), r"$dx^\mu$", color="#355070", ha="right", va="bottom", fontsize=12)

    left_panel = plt.Rectangle((6.4, 0.9), 4.7, 3.8, facecolor="#F9F7F1", edgecolor="#D8D0C4", linewidth=1.0)
    ax.add_patch(left_panel)
    ax.text(8.75, 4.25, "covector pairing", ha="center", va="center", fontsize=10.5, color="#333333")
    ax.text(8.75, 3.45, r"$p_\mu\,dx^\mu$", ha="center", va="center", fontsize=17, color="#333333")
    ax.text(8.75, 2.65, r"$=$", ha="center", va="center", fontsize=16, color="#777777")
    ax.text(8.75, 2.0, r"$p_x\,dx\;-\;E\,dt$", ha="center", va="center", fontsize=17, color="#333333")

    ax.text(6.95, 1.35, r"space piece", ha="left", va="center", fontsize=9.5, color="#BC4749")
    ax.plot([7.95, 8.55], [1.35, 1.35], color="#BC4749", linewidth=2.0)
    ax.text(9.0, 1.35, r"time piece", ha="left", va="center", fontsize=9.5, color="#4C78A8")
    ax.plot([9.88, 10.48], [1.35, 1.35], color="#4C78A8", linewidth=2.0)

    ax.set_title("Decomposing a spacetime displacement", pad=12)
    save_figure(fig, path)


def make_poisson_compression_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    lines = [
        (5.0, 5.1, r"$\dot q=\partial H/\partial p,\qquad \dot p=-\partial H/\partial q$"),
        (5.0, 3.4, r"$\dot f=\{f,H\}$"),
        (5.0, 1.7, r"$\{f,H\}=0 \Longleftrightarrow \{H,f\}=0$"),
    ]
    labels = [
        "coordinate-by-coordinate equations",
        "master dynamical statement",
        "conservation and symmetry in one relation",
    ]

    for (x, y, text), label in zip(lines, labels):
        ax.text(x, y, text, ha="center", va="center", fontsize=14)
        ax.text(x, y - 0.55, label, ha="center", va="top", color="#555555")

    ax.set_title("Poisson bracket compression", pad=12)
    save_figure(fig, path)


def make_poisson_antisymmetry_area_animation(path: Path) -> None:
    frames = 90
    origin = np.array([-0.18, -0.28])
    u = np.array([0.92, 0.26])
    v = np.array([-0.28, 0.82])
    positive = np.vstack([origin, origin + u, origin + u + v, origin + v])
    negative = np.vstack([origin, origin + v, origin + u + v, origin + u])

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.8, 5.0))

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=10)
        ax.set_xlim(-1.05, 1.45)
        ax.set_ylim(-1.0, 1.25)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def draw_constructed_area(ax: plt.Axes, order: str, progress: float) -> None:
        first, second = (u, v) if order == "fg" else (v, u)
        polygon = positive if order == "fg" else negative
        fill = "#4C78A8" if order == "fg" else "#D08C2D"
        sign = "+" if order == "fg" else "-"
        first_color = "#BC4749" if order == "fg" else "#2A9D8F"
        second_color = "#2A9D8F" if order == "fg" else "#BC4749"
        first_label = "$f$ first" if order == "fg" else "$g$ first"
        second_label = "$g$ second" if order == "fg" else "$f$ second"

        p1 = min(progress / 0.34, 1.0)
        p2 = min(max((progress - 0.24) / 0.34, 0.0), 1.0)
        pfill = min(max((progress - 0.56) / 0.24, 0.0), 1.0)

        if pfill > 0:
            ax.fill(polygon[:, 0], polygon[:, 1], color=fill, alpha=0.16 + 0.12 * pfill, zorder=1)
            closed = np.vstack([polygon, polygon[0]])
            ax.plot(closed[:, 0], closed[:, 1], color=fill, linewidth=1.8, alpha=0.55 + 0.35 * pfill, zorder=2)

        end_first = origin + p1 * first
        ax.annotate(
            "",
            xy=(end_first[0], end_first[1]),
            xytext=(origin[0], origin[1]),
            arrowprops=dict(arrowstyle="->", color=first_color, linewidth=2.5),
            zorder=4,
        )
        if p1 > 0.55:
            ax.text(end_first[0] + 0.04, end_first[1], first_label, color=first_color, ha="left", va="center", fontsize=10, bbox=LABEL_BOX)

        start_second = origin + first
        end_second = start_second + p2 * second
        if p2 > 0:
            ax.annotate(
                "",
                xy=(end_second[0], end_second[1]),
                xytext=(start_second[0], start_second[1]),
                arrowprops=dict(arrowstyle="->", color=second_color, linewidth=2.5),
                zorder=5,
            )
        if p2 > 0.55:
            ax.text(end_second[0] + 0.04, end_second[1], second_label, color=second_color, ha="left", va="center", fontsize=10, bbox=LABEL_BOX)

        if pfill > 0.65:
            ax.text(
                0.03,
                0.08,
                rf"${sign}$ same area, opposite orientation",
                transform=ax.transAxes,
                ha="left",
                va="bottom",
                fontsize=10.0,
                color="#333333",
                bbox=LABEL_BOX,
                zorder=10,
            )

    def draw_frame(frame: int) -> None:
        progress = frame / (frames - 1)
        ax_left.clear()
        ax_right.clear()
        setup_axis(ax_left, r"$\{f,g\}$")
        setup_axis(ax_right, r"$\{g,f\}$")
        draw_constructed_area(ax_left, "fg", progress)
        draw_constructed_area(ax_right, "gf", progress)
        fig.suptitle("Swapping the inputs reverses the oriented area", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_poisson_antisymmetry_area_diagram(path: Path) -> None:
    origin = np.array([-0.18, -0.28])
    u = np.array([0.92, 0.26])
    v = np.array([-0.28, 0.82])
    positive = np.vstack([origin, origin + u, origin + u + v, origin + v])
    negative = np.vstack([origin, origin + v, origin + u + v, origin + u])

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.8, 5.0))

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=10)
        ax.set_xlim(-1.05, 1.45)
        ax.set_ylim(-1.0, 1.25)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def draw_area(ax: plt.Axes, order: str) -> None:
        first, second = (u, v) if order == "fg" else (v, u)
        polygon = positive if order == "fg" else negative
        fill = "#4C78A8" if order == "fg" else "#D08C2D"
        sign = "+" if order == "fg" else "-"
        first_color = "#BC4749" if order == "fg" else "#2A9D8F"
        second_color = "#2A9D8F" if order == "fg" else "#BC4749"
        first_label = r"$f$ input" if order == "fg" else r"$g$ input"
        second_label = r"$g$ input" if order == "fg" else r"$f$ input"

        ax.fill(polygon[:, 0], polygon[:, 1], color=fill, alpha=0.24, zorder=1)
        closed = np.vstack([polygon, polygon[0]])
        ax.plot(closed[:, 0], closed[:, 1], color=fill, linewidth=2.0, alpha=0.80, zorder=2)

        first_end = origin + first
        ax.annotate(
            "",
            xy=(first_end[0], first_end[1]),
            xytext=(origin[0], origin[1]),
            arrowprops=dict(arrowstyle="->", color=first_color, linewidth=2.8),
            zorder=4,
        )
        ax.text(first_end[0] + 0.04, first_end[1], first_label, color=first_color, ha="left", va="center", fontsize=10, bbox=LABEL_BOX)

        second_start = first_end
        second_end = second_start + second
        ax.annotate(
            "",
            xy=(second_end[0], second_end[1]),
            xytext=(second_start[0], second_start[1]),
            arrowprops=dict(arrowstyle="->", color=second_color, linewidth=2.8),
            zorder=5,
        )
        ax.text(second_end[0] + 0.04, second_end[1], second_label, color=second_color, ha="left", va="center", fontsize=10, bbox=LABEL_BOX)
        ax.text(
            0.03,
            0.08,
            rf"${sign}$ same area, opposite orientation",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=10.0,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=10,
        )

    setup_axis(ax_left, r"$\{f,g\}$")
    setup_axis(ax_right, r"$\{g,f\}$")
    draw_area(ax_left, "fg")
    draw_area(ax_right, "gf")
    fig.suptitle("Swapping the inputs reverses the oriented area", y=0.98)
    save_figure(fig, path)


def make_poisson_jacobi_identity_animation(path: Path) -> None:
    frames = 132
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.2, 5.6))

    colors = ["#BC4749", "#2A9D8F", "#4C78A8"]
    node_angles = np.deg2rad([90, 210, 330])
    nodes = np.column_stack([np.cos(node_angles), np.sin(node_angles)])
    node_labels = ["$f$", "$g$", "$h$"]
    cyclic_labels = [
        r"$\{f,\{g,h\}\}$",
        r"$\{g,\{h,f\}\}$",
        r"$\{h,\{f,g\}\}$",
    ]
    cyclic_vectors = [
        np.array([0.92, 0.00]),
        np.array([-0.42, 0.72]),
        np.array([-0.50, -0.72]),
    ]

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=10)
        ax.set_xlim(-1.42, 1.42)
        ax.set_ylim(-1.22, 1.30)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

    def draw_permutation_panel(progress: float) -> None:
        setup_axis(ax_left, "Cyclic permutations")
        triangle = np.vstack([nodes, nodes[0]])
        ax_left.plot(triangle[:, 0], triangle[:, 1], color="#D0D0D0", linewidth=1.8, zorder=1)

        for node, label, color in zip(nodes, node_labels, colors):
            ax_left.scatter([node[0]], [node[1]], s=250, facecolor="white", edgecolor=color, linewidth=2.0, zorder=4)
            ax_left.text(node[0], node[1], label, ha="center", va="center", fontsize=15, color=color, zorder=5)

        for index in range(3):
            visible = smooth((progress - 0.16 * index) / 0.26)
            if visible <= 0:
                continue
            start = nodes[index]
            end = nodes[(index + 1) % 3]
            mid = start + visible * (end - start)
            ax_left.annotate(
                "",
                xy=(mid[0], mid[1]),
                xytext=(start[0], start[1]),
                arrowprops=dict(arrowstyle="->", color=colors[index], linewidth=2.7, alpha=0.92),
                zorder=3,
            )
            label_pos = 0.58 * start + 0.42 * end
            ax_left.text(
                label_pos[0],
                label_pos[1],
                cyclic_labels[index],
                ha="center",
                va="center",
                fontsize=9.4,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=visible,
                zorder=6,
            )

        alpha = smooth((progress - 0.66) / 0.18)
        if alpha > 0:
            ax_left.text(
                0.02,
                0.08,
                "only the cyclic order enters",
                transform=ax_left.transAxes,
                ha="left",
                va="bottom",
                fontsize=9.4,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=alpha,
            )

    def draw_vector_path(origin: np.ndarray, progress: float) -> np.ndarray:
        current = origin.copy()
        for index, vector in enumerate(cyclic_vectors):
            visible = smooth((progress - 0.18 * index) / 0.26)
            if visible <= 0:
                break
            end = current + visible * vector
            ax_right.annotate(
                "",
                xy=(end[0], end[1]),
                xytext=(current[0], current[1]),
                arrowprops=dict(
                    arrowstyle="->",
                    color=colors[index],
                    linewidth=3.0,
                    alpha=0.95,
                ),
                zorder=5,
            )
            if visible > 0.65:
                label_offset = np.array([0.03, 0.08 if vector[1] >= 0 else -0.10])
                ax_right.text(
                    end[0] + label_offset[0],
                    end[1] + label_offset[1],
                    cyclic_labels[index],
                    ha="left",
                    va="center",
                    fontsize=9.0,
                    color="#333333",
                    bbox=LABEL_BOX,
                    alpha=0.92,
                    zorder=6,
                )
            if visible < 0.999:
                return end
            current = current + vector
        return current

    def draw_closure_panel(progress: float) -> None:
        setup_axis(ax_right, "Cyclic sum closes")
        origin = np.array([-0.42, -0.34])
        cyclic_points = [origin]
        for vector in cyclic_vectors:
            cyclic_points.append(cyclic_points[-1] + vector)
        cyclic_outline = np.vstack(cyclic_points)
        ax_right.plot(cyclic_outline[:, 0], cyclic_outline[:, 1], color="#D0D0D0", linewidth=1.5, zorder=1)
        ax_right.scatter([origin[0]], [origin[1]], s=48, color="#333333", edgecolor="white", linewidth=0.6, zorder=7)

        draw_vector_path(origin, progress)

        close_alpha = smooth((progress - 0.72) / 0.14)
        if close_alpha > 0:
            ax_right.scatter([origin[0]], [origin[1]], s=78, color="#333333", edgecolor="white", linewidth=0.7, alpha=close_alpha, zorder=8)
            ax_right.text(
                0.03,
                0.08,
                "cyclic permutations return to the start",
                transform=ax_right.transAxes,
                ha="left",
                va="bottom",
                fontsize=9.4,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=close_alpha,
                zorder=8,
            )

        formula_alpha = smooth((progress - 0.80) / 0.16)
        if formula_alpha > 0:
            ax_right.text(
                0.50,
                -0.06,
                r"$\{f,\{g,h\}\}+\{g,\{h,f\}\}+\{h,\{f,g\}\}=0$",
                transform=ax_right.transAxes,
                ha="center",
                va="top",
                fontsize=9.6,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=formula_alpha,
                zorder=8,
            )

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()
        progress = frame / (frames - 1)
        draw_permutation_panel(progress)
        draw_closure_panel(progress)
        fig.suptitle("Jacobi identity as cyclic closure", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_skier_position_generates_momentum_animation(path: Path) -> None:
    frames = 132
    dt = 0.055

    def potential(q: np.ndarray) -> np.ndarray:
        return 0.50 * np.sin(1.15 * q) + 0.11 * q

    def dpotential(q: np.ndarray) -> np.ndarray:
        return 0.575 * np.cos(1.15 * q) + 0.11

    def vf(state: np.ndarray) -> np.ndarray:
        q, p = state
        return np.array([p, -dpotential(q)])

    states = np.zeros((frames, 2))
    state = np.array([-2.70, 0.42])
    for index in range(frames):
        states[index] = state
        k1 = vf(state)
        k2 = vf(state + 0.5 * dt * k1)
        k3 = vf(state + 0.5 * dt * k2)
        k4 = vf(state + dt * k3)
        state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    q_hill = np.linspace(-3.25, 0.20, 500)
    y_hill = potential(q_hill)
    q_grid = np.linspace(-3.15, 0.10, 15)
    p_grid = np.linspace(-1.10, 1.10, 11)
    qq, pp = np.meshgrid(q_grid, p_grid)
    uq = pp
    vp = -dpotential(qq)

    fig, (ax_hill, ax_phase) = plt.subplots(1, 2, figsize=(11.2, 5.4))

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def meter(ax: plt.Axes, label: str, value: float, max_abs: float, color: str, y: float) -> None:
        x0 = 0.69
        width = 0.24
        center = x0 + width / 2
        ax.text(
            x0,
            y + 0.055,
            label,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=9.0,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=10,
        )
        ax.plot([x0, x0 + width], [y, y], transform=ax.transAxes, color="#C8C8C8", linewidth=4.0, solid_capstyle="round", zorder=9)
        ax.plot([center, center], [y - 0.035, y + 0.035], transform=ax.transAxes, color="#777777", linewidth=0.9, zorder=10)
        end = center + (width / 2) * np.clip(value / max_abs, -1.0, 1.0)
        ax.plot([center, end], [y, y], transform=ax.transAxes, color=color, linewidth=4.8, solid_capstyle="round", zorder=11)

    def draw_frame(frame: int) -> None:
        ax_hill.clear()
        ax_phase.clear()

        q, p = states[frame]
        y = potential(q)
        slope = dpotential(q)
        pdot = -slope

        ax_hill.plot(q_hill, y_hill, color="#6B7F5A", linewidth=2.3)
        ax_hill.fill_between(q_hill, y_hill, y_hill.min() - 0.35, color="#E7E8D8", alpha=0.80)
        ax_hill.scatter([q], [y + 0.055], s=95, color="#BC4749", edgecolor="white", linewidth=0.9, zorder=6)
        ax_hill.plot(states[: frame + 1, 0], potential(states[: frame + 1, 0]) + 0.055, color="#BC4749", linewidth=1.7, alpha=0.55)

        tangent = np.array([1.0, slope])
        tangent = tangent / np.linalg.norm(tangent)
        tangent_len = 0.45
        ax_hill.plot(
            [q - tangent_len * tangent[0], q + tangent_len * tangent[0]],
            [y - tangent_len * tangent[1], y + tangent_len * tangent[1]],
            color="#355070",
            linewidth=2.0,
            alpha=0.75,
            zorder=5,
        )
        force_dir = np.sign(pdot) if abs(pdot) > 0.04 else 0.0
        downhill = force_dir * tangent
        if np.linalg.norm(downhill) > 0:
            ax_hill.annotate(
                "",
                xy=(q + 0.52 * downhill[0], y + 0.055 + 0.52 * downhill[1]),
                xytext=(q, y + 0.055),
                arrowprops=dict(arrowstyle="->", color="#BC4749", linewidth=2.4),
                zorder=7,
            )
        momentum_dir = np.sign(p) if abs(p) > 0.04 else 0.0
        if momentum_dir:
            ax_hill.annotate(
                "",
                xy=(q + 0.45 * momentum_dir, y + 0.26),
                xytext=(q, y + 0.26),
                arrowprops=dict(arrowstyle="->", color="#2A9D8F", linewidth=2.2),
                zorder=7,
            )
            ax_hill.text(q + 0.48 * momentum_dir, y + 0.26, r"$p$", ha="left" if momentum_dir > 0 else "right", va="center", fontsize=10, color="#2A9D8F", bbox=LABEL_BOX)

        ax_hill.text(
            0.03,
            0.94,
            r"position selects slope",
            transform=ax_hill.transAxes,
            ha="left",
            va="top",
            fontsize=10.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_hill.text(
            0.03,
            0.08,
            r"slope changes momentum: $\dot p=-V'(q)$",
            transform=ax_hill.transAxes,
            ha="left",
            va="bottom",
            fontsize=10.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_hill.set_title("A potential gradient as an actual hill", pad=10)
        ax_hill.set_xlim(q_hill.min(), q_hill.max())
        ax_hill.set_ylim(y_hill.min() - 0.35, y_hill.max() + 0.42)
        ax_hill.set_xlabel("position $q$")
        ax_hill.set_ylabel("height / potential")
        ax_hill.grid(color="#E8E8E8", linewidth=0.7)

        ax_phase.quiver(qq, pp, uq, vp, color="#6D7F95", alpha=0.32, pivot="mid", scale=27, width=0.0035)
        ax_phase.plot(states[: frame + 1, 0], states[: frame + 1, 1], color="#BC4749", linewidth=2.0, alpha=0.72)
        ax_phase.scatter([q], [p], s=62, color="#BC4749", edgecolor="white", linewidth=0.8, zorder=7)
        ax_phase.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax_phase.axvline(0, color="#B8B8B8", linewidth=0.8)
        ax_phase.set_title("The same relation in phase space", pad=10)
        ax_phase.set_xlabel("$q$")
        ax_phase.set_ylabel("$p$")
        ax_phase.set_xlim(q_hill.min(), q_hill.max())
        ax_phase.set_ylim(-1.18, 1.18)
        ax_phase.grid(color="#E8E8E8", linewidth=0.7)
        axes_label(ax_phase, r"$\dot q=p,\quad \dot p=-V'(q)$")
        meter(ax_phase, r"$\dot q$ from $p$", p, 1.05, "#2A9D8F", 0.18)
        meter(ax_phase, r"$\dot p$ from slope", pdot, 0.72, "#BC4749", 0.08)

        fig.suptitle(r"Position generates momentum through the slope of $H$", y=0.985)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_poisson_product_rule_animation(path: Path) -> None:
    frames = 96
    g0, h0 = 1.02, 0.72
    dg, dh = 0.42, 0.30

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.8, 5.4))

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def setup_axes() -> None:
        for ax in (ax_left, ax_right):
            ax.set_xlim(-0.18, 1.72)
            ax.set_ylim(-0.18, 1.30)
            ax.set_aspect("equal", adjustable="box")
            ax.axis("off")

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()
        setup_axes()
        progress = frame / (frames - 1)
        grow_g = smooth(progress / 0.42)
        grow_h = smooth((progress - 0.28) / 0.42)
        show_equation = smooth((progress - 0.64) / 0.26)

        width = g0 + dg * grow_g
        height = h0 + dh * grow_h

        ax_left.set_title("A product changes one factor at a time", pad=10)
        base = plt.Rectangle((0, 0), g0, h0, facecolor="#E9EEF6", edgecolor="#355070", linewidth=2.0, alpha=0.88)
        ax_left.add_patch(base)
        if grow_g > 0:
            strip_g = plt.Rectangle((g0, 0), dg * grow_g, h0, facecolor="#BC4749", edgecolor="#BC4749", linewidth=1.6, alpha=0.34)
            ax_left.add_patch(strip_g)
            ax_left.text(g0 + 0.5 * dg * grow_g, h0 * 0.5, r"$\{f,g\}h$", ha="center", va="center", fontsize=10.5, color="#7C2D2F")
        if grow_h > 0:
            strip_h = plt.Rectangle((0, h0), g0, dh * grow_h, facecolor="#2A9D8F", edgecolor="#2A9D8F", linewidth=1.6, alpha=0.32)
            ax_left.add_patch(strip_h)
            ax_left.text(g0 * 0.5, h0 + 0.5 * dh * grow_h, r"$g\{f,h\}$", ha="center", va="center", fontsize=10.5, color="#1F6F66")
        if grow_g > 0 and grow_h > 0:
            corner = plt.Rectangle((g0, h0), dg * grow_g, dh * grow_h, facecolor="#E0E0E0", edgecolor="#BBBBBB", linewidth=1.0, alpha=0.32)
            ax_left.add_patch(corner)
        ax_left.plot([0, width], [0, 0], color="#333333", linewidth=1.0)
        ax_left.plot([0, 0], [0, height], color="#333333", linewidth=1.0)
        ax_left.text(g0 * 0.5, -0.08, r"$g$", ha="center", va="top", fontsize=11)
        ax_left.text(width - 0.5 * dg * grow_g, -0.08, r"$+\;dg$", ha="center", va="top", fontsize=10, color="#BC4749", alpha=max(grow_g, 0.2))
        ax_left.text(-0.06, h0 * 0.5, r"$h$", ha="right", va="center", fontsize=11)
        ax_left.text(-0.06, height - 0.5 * dh * grow_h, r"$+\;dh$", ha="right", va="center", fontsize=10, color="#2A9D8F", alpha=max(grow_h, 0.2))
        ax_left.text(
            0.02,
            0.96,
            r"the tiny corner is second order",
            transform=ax_left.transAxes,
            ha="left",
            va="top",
            fontsize=9.2,
            color="#555555",
            bbox=LABEL_BOX,
        )

        ax_right.set_title("Leibniz rule for the bracket", pad=10)
        ax_right.text(
            0.50,
            0.82,
            r"$\{f,gh\}$",
            transform=ax_right.transAxes,
            ha="center",
            va="center",
            fontsize=18,
            color="#333333",
        )
        ax_right.text(
            0.50,
            0.62,
            r"$=$",
            transform=ax_right.transAxes,
            ha="center",
            va="center",
            fontsize=18,
            color="#333333",
            alpha=show_equation,
        )
        ax_right.text(
            0.50,
            0.44,
            r"$\{f,g\}h+g\{f,h\}$",
            transform=ax_right.transAxes,
            ha="center",
            va="center",
            fontsize=16,
            color="#333333",
            alpha=show_equation,
        )
        ax_right.text(
            0.50,
            0.22,
            r"with $f$ held fixed, the bracket acts like a derivative",
            transform=ax_right.transAxes,
            ha="center",
            va="center",
            fontsize=10.2,
            color="#333333",
            bbox=LABEL_BOX,
            alpha=0.35 + 0.65 * show_equation,
        )
        fig.suptitle("Product rule: the bracket changes one factor and then the other", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_fourier_momentum_shift_phase_animation(path: Path) -> None:
    frames = 96
    k = np.linspace(-3.2, 3.2, 500)
    x = np.linspace(-8.0, 8.0, 700)
    k0 = -0.35
    b_final = 1.35
    sigma_k = 0.38
    envelope = np.exp(-(x / 5.4) ** 2)

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 6.8))
    ax_k = axes[0, 0]
    ax_phase = axes[0, 1]
    ax_original = axes[1, 0]
    ax_product = axes[1, 1]

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def draw_frame(frame: int) -> None:
        for ax in axes.ravel():
            ax.clear()
        progress = smooth(frame / (frames - 1))
        b = b_final * progress
        profile_initial = np.exp(-0.5 * ((k - k0) / sigma_k) ** 2)
        profile_shifted = np.exp(-0.5 * ((k - (k0 + b)) / sigma_k) ** 2)

        ax_k.plot(k, profile_initial, color="#A8B5C6", linewidth=1.8, alpha=0.55, linestyle="--")
        ax_k.plot(k, profile_shifted, color="#BC4749", linewidth=2.5)
        ax_k.fill_between(k, 0, profile_shifted, color="#BC4749", alpha=0.14)
        ax_k.annotate(
            "",
            xy=(k0 + b, 0.86),
            xytext=(k0, 0.86),
            arrowprops=dict(arrowstyle="->", color="#BC4749", linewidth=2.0),
        )
        ax_k.text(k0 + 0.5 * b, 0.93, r"$+b$", ha="center", va="bottom", color="#BC4749", fontsize=11)
        ax_k.text(
            0.03,
            0.95,
            r"$\hat\psi(k)\mapsto\hat\psi(k-b)$",
            transform=ax_k.transAxes,
            ha="left",
            va="top",
            fontsize=11.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_k.set_title("Momentum shift in wave-number space", pad=10)
        ax_k.set_xlabel("k")
        ax_k.set_ylabel(r"$|\hat\psi(k)|$")
        ax_k.set_xlim(-3.2, 3.2)
        ax_k.set_ylim(-0.04, 1.12)
        ax_k.grid(color="#E8E8E8", linewidth=0.7)

        wave_initial = envelope * np.cos(k0 * x)
        phase_factor = np.cos(b * x)
        wave_shifted = envelope * np.cos((k0 + b) * x)

        ax_phase.plot(x, phase_factor, color="#BC4749", linewidth=1.8)
        ax_phase.text(
            0.03,
            0.90,
            r"phase factor $e^{ibx}$",
            transform=ax_phase.transAxes,
            ha="left",
            va="top",
            fontsize=10.5,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_phase.set_title("Position-dependent phase", pad=10)
        ax_phase.set_xlim(-8.0, 8.0)
        ax_phase.set_ylim(-1.12, 1.12)
        ax_phase.grid(color="#E8E8E8", linewidth=0.7)
        ax_phase.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax_phase.set_xlabel("x")
        ax_phase.set_ylabel("real part")

        ax_original.plot(x, wave_initial, color="#A8B5C6", linewidth=1.8)
        ax_original.plot(x, envelope, color="#D0D0D0", linewidth=0.8, alpha=0.65)
        ax_original.plot(x, -envelope, color="#D0D0D0", linewidth=0.8, alpha=0.65)
        ax_original.text(
            0.03,
            0.90,
            r"original $\psi(x)$",
            transform=ax_original.transAxes,
            ha="left",
            va="top",
            fontsize=10.5,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_original.set_title("Original wave", pad=10)
        ax_original.set_xlim(-8.0, 8.0)
        ax_original.set_ylim(-1.12, 1.12)
        ax_original.grid(color="#E8E8E8", linewidth=0.7)
        ax_original.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax_original.set_xlabel("x")
        ax_original.set_ylabel("real part")

        ax_product.plot(x, wave_initial, color="#A8B5C6", linewidth=1.1, alpha=0.42, linestyle="--")
        ax_product.plot(x, wave_shifted, color="#355070", linewidth=2.0)
        ax_product.plot(x, envelope, color="#D0D0D0", linewidth=0.8, alpha=0.65)
        ax_product.plot(x, -envelope, color="#D0D0D0", linewidth=0.8, alpha=0.65)
        ax_product.text(
            0.03,
            0.95,
            r"$(M_b\psi)(x)=e^{ibx}\psi(x)$",
            transform=ax_product.transAxes,
            ha="left",
            va="top",
            fontsize=11.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_product.text(
            0.03,
            0.08,
            r"$e^{ikx}\mapsto e^{i(k+b)x}$",
            transform=ax_product.transAxes,
            ha="left",
            va="bottom",
            fontsize=11.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_product.set_title("Product: phase times wave", pad=10)
        ax_product.set_xlabel("x")
        ax_product.set_ylabel("real part")
        ax_product.set_xlim(-8.0, 8.0)
        ax_product.set_ylim(-1.12, 1.12)
        ax_product.grid(color="#E8E8E8", linewidth=0.7)
        ax_product.axhline(0, color="#B8B8B8", linewidth=0.8)

        fig.suptitle("A shift in wave number appears as phase modulation", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_fourier_phase_shift_mechanism_animation(path: Path) -> None:
    frames = 108
    x = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 650)
    k = np.linspace(-0.3, 4.6, 500)
    k0 = 1.0
    b_final = 1.45
    sigma = 0.075

    fig, (ax_wave, ax_k) = plt.subplots(1, 2, figsize=(11.2, 5.0))

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def draw_frame(frame: int) -> None:
        ax_wave.clear()
        ax_k.clear()
        progress = smooth(frame / (frames - 1))
        b = b_final * progress
        wave_before = np.cos(k0 * x)
        phase = np.cos(b * x)
        wave_after = np.cos((k0 + b) * x)

        ax_wave.plot(x, wave_before, color="#A8B5C6", linewidth=1.2, linestyle="--", alpha=0.62, label=r"$e^{ikx}$")
        ax_wave.plot(x, phase, color="#BC4749", linewidth=1.3, alpha=0.56, label=r"$e^{ibx}$")
        ax_wave.plot(x, wave_after, color="#355070", linewidth=2.2, label=r"$e^{i(k+b)x}$")
        ax_wave.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax_wave.set_xlim(x.min(), x.max())
        ax_wave.set_ylim(-1.18, 1.18)
        ax_wave.set_xlabel("x")
        ax_wave.set_ylabel("real part")
        ax_wave.grid(color="#E8E8E8", linewidth=0.7)
        ax_wave.set_title("Phase multiplication adds wave number", pad=10)
        ax_wave.text(
            0.03,
            0.94,
            r"$e^{ibx}\,e^{ikx}=e^{i(k+b)x}$",
            transform=ax_wave.transAxes,
            ha="left",
            va="top",
            fontsize=12.0,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_wave.text(
            0.03,
            0.08,
            rf"$k=1.00,\quad b={b:0.2f},\quad k+b={k0 + b:0.2f}$",
            transform=ax_wave.transAxes,
            ha="left",
            va="bottom",
            fontsize=10.2,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_wave.legend(loc="upper right", frameon=True, fontsize=8.8)

        before = np.exp(-0.5 * ((k - k0) / sigma) ** 2)
        after = np.exp(-0.5 * ((k - (k0 + b)) / sigma) ** 2)
        ax_k.plot(k, before, color="#A8B5C6", linewidth=1.4, linestyle="--", alpha=0.65)
        ax_k.plot(k, after, color="#355070", linewidth=2.2)
        ax_k.axvline(k0, color="#A8B5C6", linewidth=1.0, linestyle="--", alpha=0.75)
        ax_k.axvline(k0 + b, color="#355070", linewidth=1.2, alpha=0.85)
        ax_k.annotate(
            "",
            xy=(k0 + b, 0.82),
            xytext=(k0, 0.82),
            arrowprops=dict(arrowstyle="->", color="#BC4749", linewidth=2.0),
            zorder=6,
        )
        ax_k.text(
            (2 * k0 + b) / 2,
            0.91,
            r"shift by $b$",
            ha="center",
            va="bottom",
            fontsize=10.0,
            color="#BC4749",
            bbox=LABEL_BOX,
        )
        ax_k.set_xlim(k.min(), k.max())
        ax_k.set_ylim(-0.05, 1.12)
        ax_k.set_xlabel("wave number k")
        ax_k.set_ylabel("amplitude")
        ax_k.grid(color="#E8E8E8", linewidth=0.7)
        ax_k.set_title("The same operation in wave-number space", pad=10)

        fig.suptitle("Multiplying by a phase shifts Fourier components", y=0.985)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_weyl_order_phase_animation(path: Path) -> None:
    frames = 108
    x = np.linspace(-7.0, 7.0, 650)
    a = 1.55
    b = 0.95
    k0 = 1.15

    def smooth(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    def envelope(center: float) -> np.ndarray:
        return np.exp(-0.5 * ((x - center) / 2.2) ** 2)

    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(9.8, 6.4), sharex=True)

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=8)
        ax.set_xlim(-7.0, 7.0)
        ax.set_ylim(-1.15, 1.15)
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.set_ylabel("real part")

    def draw_wave(ax: plt.Axes, center: float, carrier_shift: float, phase_offset: float, color: str, alpha: float = 1.0) -> None:
        env = envelope(center)
        wave = env * np.cos((k0 + carrier_shift) * (x - center) + phase_offset)
        ax.plot(x, wave, color=color, linewidth=2.2, alpha=alpha)
        ax.plot(x, env, color="#D0D0D0", linewidth=0.8, alpha=0.65)
        ax.plot(x, -env, color="#D0D0D0", linewidth=0.8, alpha=0.65)

    def draw_frame(frame: int) -> None:
        ax_top.clear()
        ax_bottom.clear()
        progress = frame / (frames - 1)
        shift_progress = smooth(progress / 0.48)
        mod_progress = smooth((progress - 0.38) / 0.48)
        mod_first = smooth(progress / 0.48)
        shift_second = smooth((progress - 0.38) / 0.48)

        setup_axis(ax_top, r"$M_bT_a$: shift in $x$, then shift in $k$")
        center_top = a * shift_progress
        carrier_top = b * mod_progress
        phase_top = 0.0
        draw_wave(ax_top, center_top, carrier_top, phase_top, "#BC4749")
        ax_top.text(
            0.02,
            0.90,
            r"$M_bT_a\psi(x)=e^{ibx}\psi(x-a)$",
            transform=ax_top.transAxes,
            ha="left",
            va="top",
            fontsize=10.4,
            color="#333333",
            bbox=LABEL_BOX,
        )

        setup_axis(ax_bottom, r"$T_aM_b$: shift in $k$, then shift in $x$")
        center_bottom = a * shift_second
        carrier_bottom = b * mod_first
        phase_bottom = -b * a * shift_second * mod_first
        draw_wave(ax_bottom, center_bottom, carrier_bottom, phase_bottom, "#2A9D8F")
        ax_bottom.text(
            0.02,
            0.90,
            r"$T_aM_b\psi(x)=e^{ib(x-a)}\psi(x-a)$",
            transform=ax_bottom.transAxes,
            ha="left",
            va="top",
            fontsize=10.4,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_bottom.set_xlabel("x")

        if progress > 0.78:
            fade = smooth((progress - 0.78) / 0.16)
            phase = b * a
            for ax in (ax_top, ax_bottom):
                ax.text(
                    0.98,
                    0.10,
                    rf"same translated envelope; phase differs by $e^{{iab}}$",
                    transform=ax.transAxes,
                    ha="right",
                    va="bottom",
                    fontsize=10.0,
                    color="#333333",
                    bbox=LABEL_BOX,
                    alpha=fade,
                )
            ax_bottom.text(
                0.50,
                -0.34,
                rf"$ab={phase:.2f}$ controls the phase picked up by changing the order",
                transform=ax_bottom.transAxes,
                ha="center",
                va="top",
                fontsize=10.2,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=fade,
            )

        fig.suptitle("Position and momentum shifts do not commute on waves", y=0.985)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_poisson_bidirectional_flow_animation(path: Path) -> None:
    frames = 108
    dt = 0.045

    q = np.linspace(-1.8, 1.8, 210)
    p = np.linspace(-1.55, 1.55, 190)
    qq, pp = np.meshgrid(q, p)

    def f_value(state: np.ndarray) -> np.ndarray:
        q0 = state[..., 0]
        p0 = state[..., 1]
        return 0.5 * (q0**2 + p0**2)

    def g_value(state: np.ndarray) -> np.ndarray:
        q0 = state[..., 0]
        p0 = state[..., 1]
        return 0.5 * p0**2 + 0.25 * q0**4 + 0.16 * q0

    f_grid = f_value(np.stack([qq, pp], axis=-1))
    g_grid = g_value(np.stack([qq, pp], axis=-1))
    f_levels = [0.10, 0.20, 0.34, 0.52, 0.74, 1.00, 1.30, 1.64, 2.02]
    g_levels = [-0.06, 0.04, 0.16, 0.31, 0.50, 0.75, 1.06, 1.44, 1.88, 2.40]

    qv = np.linspace(-1.55, 1.55, 13)
    pv = np.linspace(-1.30, 1.30, 11)
    qvq, pvq = np.meshgrid(qv, pv)
    xg_u = pvq
    xg_v = -(qvq**3 + 0.16)
    xf_u = pvq
    xf_v = -qvq

    def step(state: np.ndarray, which: str) -> np.ndarray:
        def vf(s: np.ndarray) -> np.ndarray:
            q0 = s[..., 0]
            p0 = s[..., 1]
            if which == "f":
                return np.stack([p0, -q0], axis=-1)
            return np.stack([p0, -(q0**3 + 0.16)], axis=-1)

        k1 = vf(state)
        k2 = vf(state + 0.5 * dt * k1)
        k3 = vf(state + 0.5 * dt * k2)
        k4 = vf(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    left_states = np.empty((frames, 2))
    right_states = np.empty((frames, 2))
    left = np.array([0.92, 0.28], dtype=float)
    right = np.array([0.92, 0.28], dtype=float)
    for index in range(frames):
        left_states[index] = left
        right_states[index] = right
        left = step(left, "g")
        right = step(right, "f")

    left_values = f_value(left_states)
    right_values = g_value(right_states)
    left_min, left_max = float(left_values.min()), float(left_values.max())
    right_min, right_max = float(right_values.min()), float(right_values.max())

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.2, 5.3))

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=10)
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.55, 1.55)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def meter(ax: plt.Axes, label: str, value: float, low: float, high: float, color: str) -> None:
        x0, x1, y = 0.14, 0.52, 0.08
        frac = 0.5 if high == low else float(np.clip((value - low) / (high - low), 0.0, 1.0))
        ax.plot([x0, x1], [y, y], transform=ax.transAxes, color="#D0D0D0", linewidth=4.2, solid_capstyle="round", zorder=20)
        ax.plot([x0, x0 + frac * (x1 - x0)], [y, y], transform=ax.transAxes, color=color, linewidth=4.2, solid_capstyle="round", zorder=21)
        ax.scatter([x0 + frac * (x1 - x0)], [y], transform=ax.transAxes, s=28, color=color, edgecolor="white", linewidth=0.7, zorder=22)
        ax.text(
            x0,
            y + 0.055,
            label,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=9.0,
            color="#333333",
            bbox=LABEL_BOX,
            zorder=23,
        )

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()
        setup_axis(ax_left, r"$\{f,g\}$: read $f$ along the flow of $g$")
        setup_axis(ax_right, r"$\{g,f\}$: read $g$ along the flow of $f$")

        ax_left.contour(qq, pp, g_grid, levels=g_levels, colors="#777777", linewidths=0.95, alpha=0.62)
        ax_left.streamplot(q, p, pp, -(qq**3 + 0.16), color=(0.19, 0.31, 0.44, 0.36), density=1.0, linewidth=0.75, arrowsize=0.8)
        ax_left.quiver(qvq, pvq, xg_u, xg_v, color="#355070", alpha=0.34, pivot="mid", scale=23, width=0.0035)
        ax_right.contour(qq, pp, f_grid, levels=f_levels, colors="#777777", linewidths=0.95, alpha=0.62)
        ax_right.streamplot(q, p, pp, -qq, color=(0.19, 0.31, 0.44, 0.36), density=1.0, linewidth=0.75, arrowsize=0.8)
        ax_right.quiver(qvq, pvq, xf_u, xf_v, color="#355070", alpha=0.34, pivot="mid", scale=23, width=0.0035)

        for ax, states, color in [(ax_left, left_states, "#BC4749"), (ax_right, right_states, "#2A9D8F")]:
            trail = states[: frame + 1]
            ax.plot(trail[:, 0], trail[:, 1], color=color, linewidth=2.0, alpha=0.74, zorder=6)
            ax.scatter([states[frame, 0]], [states[frame, 1]], s=44, color=color, edgecolor="white", linewidth=0.8, zorder=7)

        axes_label(ax_left, r"$g$ generates the motion; measure $f$")
        axes_label(ax_right, r"$f$ generates the motion; measure $g$")
        meter(ax_left, r"value of $f$", float(left_values[frame]), left_min, left_max, "#BC4749")
        meter(ax_right, r"value of $g$", float(right_values[frame]), right_min, right_max, "#2A9D8F")
        fig.suptitle("Either function can be measured along the flow generated by the other", y=0.985)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_poisson_bracket_vectorfield_identity_animation(path: Path) -> None:
    frames = 96
    eps = 0.62
    start = np.array([0.62, 0.56])

    def flow_f(point: np.ndarray, amount: float) -> np.ndarray:
        q0, p0 = point
        return np.array([q0 + amount * p0, p0])

    def flow_g(point: np.ndarray, amount: float) -> np.ndarray:
        q0, p0 = point
        return np.array([q0, p0 - amount * q0])

    after_f = flow_f(start, eps)
    fg_end = flow_g(after_f, eps)
    after_g = flow_g(start, eps)
    gf_end = flow_f(after_g, eps)

    q = np.linspace(-1.45, 1.45, 180)
    p = np.linspace(-1.20, 1.20, 160)
    qq, pp = np.meshgrid(q, p)
    bracket = -qq * pp

    qv = np.linspace(-1.25, 1.25, 11)
    pv = np.linspace(-1.00, 1.00, 9)
    qvq, pvq = np.meshgrid(qv, pv)
    xf_u, xf_v = pvq, np.zeros_like(pvq)
    xg_u, xg_v = np.zeros_like(qvq), -qvq
    xbr_u, xbr_v = -qvq, pvq

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.2, 5.4))

    def setup_axis(ax: plt.Axes, title: str) -> None:
        ax.set_title(title, pad=10)
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.20, 1.20)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def interpolate_path(points: list[np.ndarray], progress: float) -> np.ndarray:
        if progress <= 0:
            return points[0][None, :]
        segments = len(points) - 1
        scaled = np.clip(progress, 0, 1) * segments
        whole = int(np.floor(scaled))
        frac = scaled - whole
        path_points = points[: whole + 1]
        if whole < segments:
            current = points[whole] + frac * (points[whole + 1] - points[whole])
            path_points = path_points + [current]
        return np.vstack(path_points)

    def draw_segmented_route(
        ax: plt.Axes,
        points: list[np.ndarray],
        progress: float,
        colors: tuple[str, str],
    ) -> np.ndarray:
        progress = float(np.clip(progress, 0.0, 1.0))
        first_progress = min(progress * 2.0, 1.0)
        second_progress = min(max(progress * 2.0 - 1.0, 0.0), 1.0)
        first_end = points[0] + first_progress * (points[1] - points[0])
        ax.plot(
            [points[0][0], first_end[0]],
            [points[0][1], first_end[1]],
            color=colors[0],
            linewidth=3.8,
            alpha=0.88,
            solid_capstyle="round",
            zorder=5,
        )
        current = first_end
        if progress > 0.5:
            second_end = points[1] + second_progress * (points[2] - points[1])
            ax.plot(
                [points[1][0], second_end[0]],
                [points[1][1], second_end[1]],
                color=colors[1],
                linewidth=3.8,
                alpha=0.88,
                solid_capstyle="round",
                zorder=5,
            )
            current = second_end
        ax.scatter([current[0]], [current[1]], s=46, color=colors[1 if progress > 0.5 else 0], edgecolor="white", linewidth=0.7, zorder=7)
        return current

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()
        progress = frame / (frames - 1)

        setup_axis(ax_left, "Commutator of generated flows")
        ax_left.quiver(qvq, pvq, xf_u, xf_v, color="#BC4749", alpha=0.26, pivot="mid", scale=20, width=0.0034)
        ax_left.quiver(qvq, pvq, xg_u, xg_v, color="#2A9D8F", alpha=0.26, pivot="mid", scale=20, width=0.0034)
        ax_left.scatter([start[0]], [start[1]], s=46, color="#333333", edgecolor="white", linewidth=0.7, zorder=7)

        phase_a = min(progress / 0.72, 1.0)
        phase_b = min(max((progress - 0.10) / 0.72, 0.0), 1.0)
        current_a = draw_segmented_route(ax_left, [start, after_f, fg_end], phase_a, ("#BC4749", "#2A9D8F"))
        current_b = draw_segmented_route(ax_left, [start, after_g, gf_end], phase_b, ("#2A9D8F", "#BC4749"))

        if progress > 0.78:
            fade = min((progress - 0.78) / 0.18, 1.0)
            ax_left.annotate(
                "",
                xy=(gf_end[0], gf_end[1]),
                xytext=(fg_end[0], fg_end[1]),
                arrowprops=dict(arrowstyle="->", color="#355070", linewidth=2.3, alpha=fade),
                zorder=8,
            )
            ax_left.text(
                0.03,
                0.08,
                r"endpoint difference: $[X_f,X_g]$",
                transform=ax_left.transAxes,
                ha="left",
                va="bottom",
                fontsize=9.2,
                color="#333333",
                bbox=LABEL_BOX,
                alpha=fade,
            )

        axes_label(ax_left, r"$X_f$ then $X_g$ vs. $X_g$ then $X_f$")
        ax_left.text(0.66, 0.92, r"$X_f$", transform=ax_left.transAxes, color="#BC4749", fontsize=11, bbox=LABEL_BOX)
        ax_left.text(0.82, 0.92, r"$X_g$", transform=ax_left.transAxes, color="#2A9D8F", fontsize=11, bbox=LABEL_BOX)

        setup_axis(ax_right, r"The bracket encodes the same infinitesimal direction")
        ax_right.contour(qq, pp, bracket, levels=np.linspace(-1.2, 1.2, 13), colors="#777777", linewidths=0.9, alpha=0.58)
        ax_right.quiver(qvq, pvq, xbr_u, xbr_v, color="#355070", alpha=0.42, pivot="mid", scale=22, width=0.0038)
        ax_right.scatter([start[0]], [start[1]], s=46, color="#333333", edgecolor="white", linewidth=0.7, zorder=7)
        direction = gf_end - fg_end
        if np.linalg.norm(direction) > 0:
            unit = direction / np.linalg.norm(direction)
        else:
            unit = direction
        arrow_scale = 0.48 * min(max((progress - 0.42) / 0.36, 0.0), 1.0)
        ax_right.annotate(
            "",
            xy=(start[0] + arrow_scale * unit[0], start[1] + arrow_scale * unit[1]),
            xytext=(start[0], start[1]),
            arrowprops=dict(arrowstyle="->", color="#355070", linewidth=2.5),
            zorder=8,
        )
        axes_label(ax_right, r"$\{f,g\}\mapsto X_{\{f,g\}}$")
        ax_right.text(
            0.03,
            0.08,
            r"$[X_f,X_g]=X_{\{f,g\}}$",
            transform=ax_right.transAxes,
            ha="left",
            va="bottom",
            fontsize=11.0,
            color="#333333",
            bbox=LABEL_BOX,
        )

        fig.suptitle("The vector-field commutator is encoded by the Poisson bracket", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_lie_generator_tangent_flow_animation(path: Path) -> None:
    frames = 96
    theta_final = 1.45 * np.pi
    circle_theta = np.linspace(0.0, 2.0 * np.pi, 400)
    circle = np.column_stack([np.cos(circle_theta), np.sin(circle_theta)])

    fig, ax = plt.subplots(figsize=(8.8, 5.0))

    def draw_frame(frame: int) -> None:
        ax.clear()
        progress = frame / (frames - 1)
        theta = theta_final * progress
        point = np.array([np.cos(theta), np.sin(theta)])
        tangent = np.array([-np.sin(theta), np.cos(theta)])
        arrow_end = point + 0.42 * tangent

        ax.plot(circle[:, 0], circle[:, 1], color="#D0D0D0", linewidth=2.0)
        if frame > 0:
            arc_theta = np.linspace(0.0, theta, max(4, frame + 2))
            ax.plot(np.cos(arc_theta), np.sin(arc_theta), color="#BC4749", linewidth=3.0, alpha=0.78)

        ax.plot([1.0, 1.0], [-0.42, 0.50], color="#9AA3AF", linewidth=1.5, alpha=0.75)
        ax.scatter([1.0], [0.0], s=46, color="#355070", zorder=4)
        ax.text(1.08, -0.08, r"$e$", ha="left", va="top", fontsize=12, color="#355070")
        ax.annotate(
            "",
            xy=(1.0, 0.42),
            xytext=(1.0, 0.02),
            arrowprops=dict(arrowstyle="->", color="#355070", linewidth=2.2),
            zorder=6,
        )
        ax.text(1.08, 0.45, r"$X$", ha="left", va="bottom", fontsize=13, color="#355070")

        ax.scatter([point[0]], [point[1]], s=58, color="#BC4749", edgecolor="white", linewidth=0.8, zorder=5)
        ax.text(point[0] + 0.07, point[1] + 0.07, r"$G(t)$", ha="left", va="bottom", fontsize=12, color="#BC4749")
        ax.annotate(
            "",
            xy=(arrow_end[0], arrow_end[1]),
            xytext=(point[0], point[1]),
            arrowprops=dict(arrowstyle="->", color="#2A9D8F", linewidth=2.4),
            zorder=6,
        )
        ax.text(
            arrow_end[0] + 0.05,
            arrow_end[1],
            r"$XG(t)$",
            ha="left",
            va="center",
            fontsize=12.5,
            color="#2A9D8F",
            bbox=LABEL_BOX,
        )

        step_thetas = np.linspace(0.0, theta, 6)[1:-1] if theta > 0.35 else []
        for t0 in step_thetas:
            p0 = np.array([np.cos(t0), np.sin(t0)])
            v0 = np.array([-np.sin(t0), np.cos(t0)])
            ax.annotate(
                "",
                xy=(p0[0] + 0.18 * v0[0], p0[1] + 0.18 * v0[1]),
                xytext=(p0[0], p0[1]),
                arrowprops=dict(arrowstyle="->", color="#2A9D8F", linewidth=1.2, alpha=0.48),
            )

        ax.text(
            0.03,
            0.95,
            "fixed generator at the identity",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax.text(
            0.03,
            0.84,
            r"the current tangent is $XG(t)$",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax.text(
            0.03,
            0.08,
            r"$\frac{d}{dt}G(t)=XG(t)$",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=14,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax.set_title("A fixed generator induces the moving tangent", pad=10)
        ax.set_xlim(-1.55, 1.75)
        ax.set_ylim(-1.35, 1.35)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_exponential_map_accumulation_animation(path: Path) -> None:
    frames = 108
    total_angle = 1.45 * np.pi
    n_steps = 18
    circle_theta = np.linspace(0.0, total_angle, 260)
    unit_circle = np.column_stack([np.cos(circle_theta), np.sin(circle_theta)])

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.2, 5.4))

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()
        progress = frame / (frames - 1)
        theta = total_angle * progress
        visible_steps = max(1, int(np.floor(progress * n_steps)))
        step_angles = np.linspace(0.0, total_angle, n_steps + 1)[: visible_steps + 1]

        ax_left.plot(unit_circle[:, 0], unit_circle[:, 1], color="#D0D0D0", linewidth=2.0)
        if len(step_angles) > 1:
            ax_left.plot(np.cos(step_angles), np.sin(step_angles), color="#BC4749", linewidth=2.4, alpha=0.82)
            ax_left.scatter(np.cos(step_angles), np.sin(step_angles), s=26, color="#BC4749", edgecolor="white", linewidth=0.6, zorder=4)

        current = np.array([np.cos(theta), np.sin(theta)])
        tangent = np.array([-np.sin(theta), np.cos(theta)])
        ax_left.scatter([1.0], [0.0], s=42, color="#355070", zorder=5)
        ax_left.text(1.08, -0.08, r"$I$", ha="left", va="top", fontsize=12, color="#355070")
        ax_left.scatter([current[0]], [current[1]], s=58, color="#BC4749", edgecolor="white", linewidth=0.8, zorder=6)
        ax_left.annotate(
            "",
            xy=(current[0] + 0.34 * tangent[0], current[1] + 0.34 * tangent[1]),
            xytext=(current[0], current[1]),
            arrowprops=dict(arrowstyle="->", color="#2A9D8F", linewidth=2.1),
            zorder=7,
        )

        ax_left.text(
            0.03,
            0.95,
            "repeat the infinitesimal step",
            transform=ax_left.transAxes,
            ha="left",
            va="top",
            fontsize=9.6,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_left.text(
            0.03,
            0.08,
            r"$G_{k+1}\approx(I+\Delta t\,X)G_k$",
            transform=ax_left.transAxes,
            ha="left",
            va="bottom",
            fontsize=11.5,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_left.set_title("Accumulating infinitesimal transformations", pad=10)
        ax_left.set_xlim(-1.35, 1.45)
        ax_left.set_ylim(-1.25, 1.25)
        ax_left.set_aspect("equal", adjustable="box")
        ax_left.axis("off")

        ax_right.set_title("The limit is the exponential map", pad=10)
        ax_right.set_xlim(-1.35, 1.35)
        ax_right.set_ylim(-1.35, 1.35)
        ax_right.set_aspect("equal", adjustable="box")
        ax_right.axis("off")
        full = np.linspace(0.0, 2.0 * np.pi, 260)
        ax_right.plot(np.cos(full), np.sin(full), color="#E0E0E0", linewidth=1.4)
        ax_right.arrow(0, 0, 1.0, 0.0, color="#A8B5C6", width=0.012, head_width=0.07, length_includes_head=True)
        ax_right.arrow(0, 0, current[0], current[1], color="#BC4749", width=0.016, head_width=0.08, length_includes_head=True)
        ax_right.text(1.05, -0.05, r"$v$", color="#6C757D", ha="left", va="top", fontsize=12)
        ax_right.text(current[0] + 0.06, current[1], r"$G(t)v$", color="#BC4749", ha="left", va="center", fontsize=12)
        ax_right.text(
            0.03,
            0.95,
            r"$G(t)=e^{tX}$",
            transform=ax_right.transAxes,
            ha="left",
            va="top",
            fontsize=12.5,
            color="#333333",
            bbox=LABEL_BOX,
        )
        ax_right.text(
            0.03,
            0.08,
            "finite transformation from repeated tangent motion",
            transform=ax_right.transAxes,
            ha="left",
            va="bottom",
            fontsize=9.6,
            color="#333333",
            bbox=LABEL_BOX,
        )
        fig.suptitle("The exponential map accumulates the generator", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_generator_vector_field_contrast_animation(path: Path) -> None:
    frames = 120

    grid = np.linspace(-1.35, 1.35, 13)
    xx, yy = np.meshgrid(grid, grid)
    rot_u = -yy
    rot_v = xx

    seed_x, seed_y = np.meshgrid(np.linspace(-0.9, 0.9, 5), np.linspace(-0.9, 0.9, 5))
    seed_points = np.column_stack([seed_x.ravel(), seed_y.ravel()])

    q = np.linspace(-1.75, 1.75, 220)
    p = np.linspace(-1.55, 1.55, 200)
    qq, pp = np.meshgrid(q, p)
    rr = qq**2 + pp**2
    F = 0.5 * rr + 0.08 * rr**2 + 0.08 * (qq**3 - 3.0 * qq * pp**2)
    levels = [0.08, 0.16, 0.27, 0.40, 0.56, 0.74, 0.96, 1.22, 1.52, 1.86, 2.25, 2.70]

    qv = np.linspace(-1.55, 1.55, 15)
    pv = np.linspace(-1.32, 1.32, 13)
    qvq, pvq = np.meshgrid(qv, pv)
    rv = qvq**2 + pvq**2
    ham_u = pvq + 0.32 * pvq * rv - 0.48 * qvq * pvq
    ham_v = -(qvq + 0.32 * qvq * rv + 0.24 * (qvq**2 - pvq**2))

    patch0 = np.array(
        [
            [0.62, 0.18],
            [0.92, 0.14],
            [0.98, 0.38],
            [0.68, 0.46],
        ],
        dtype=float,
    )
    patch_frames = np.empty((frames, len(patch0), 2))
    patch = patch0.copy()

    def swirl_step(state: np.ndarray, dt: float) -> np.ndarray:
        def vf(s: np.ndarray) -> np.ndarray:
            q0 = s[..., 0]
            p0 = s[..., 1]
            r0 = q0**2 + p0**2
            dq = p0 + 0.32 * p0 * r0 - 0.48 * q0 * p0
            dp = -(q0 + 0.32 * q0 * r0 + 0.24 * (q0**2 - p0**2))
            return np.stack([dq, dp], axis=-1)

        k1 = vf(state)
        k2 = vf(state + 0.5 * dt * k1)
        k3 = vf(state + 0.5 * dt * k2)
        k4 = vf(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    for index in range(frames):
        patch_frames[index] = patch
        patch = swirl_step(patch, 0.04)

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11.2, 5.4))

    def setup_axis(ax: plt.Axes, xlim: tuple[float, float], ylim: tuple[float, float], xlabel: str, ylabel: str) -> None:
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(color="#E8E8E8", linewidth=0.7)
        ax.axhline(0, color="#B8B8B8", linewidth=0.8)
        ax.axvline(0, color="#B8B8B8", linewidth=0.8)

    def draw_frame(frame: int) -> None:
        ax_left.clear()
        ax_right.clear()

        t = 2.0 * np.pi * frame / (frames - 1)
        rotation = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
        rotated_points = seed_points @ rotation.T

        setup_axis(ax_left, (-1.6, 1.6), (-1.6, 1.6), "x", "y")
        ax_left.set_title("Matrix symmetry generator", pad=10)
        ax_left.quiver(
            xx,
            yy,
            rot_u,
            rot_v,
            color="#355070",
            alpha=0.48,
            pivot="mid",
            scale=18,
            width=0.004,
        )
        ax_left.scatter(seed_points[:, 0], seed_points[:, 1], s=16, color="#A8B5C6", alpha=0.45, edgecolors="none")
        ax_left.scatter(rotated_points[:, 0], rotated_points[:, 1], s=22, color="#BC4749", alpha=0.85, edgecolors="white", linewidth=0.35)
        axes_label(ax_left, r"one global rule: $X(z)=Az$")

        idx = frame
        current = patch_frames[idx]
        setup_axis(ax_right, (-1.75, 1.75), (-1.55, 1.55), "q", "p")
        ax_right.set_title("Hamiltonian generator", pad=10)
        ax_right.contour(
            qq,
            pp,
            F,
            levels=levels,
            colors=["#42658A", "#D89B34", "#6C8FB5"],
            linewidths=1.05,
            alpha=0.68,
        )
        ax_right.quiver(
            qvq,
            pvq,
            ham_u,
            ham_v,
            color="#2F4F73",
            alpha=0.42,
            pivot="mid",
            scale=30,
            width=0.0034,
        )
        ax_right.fill(current[:, 0], current[:, 1], color="#54A24B", alpha=0.24, zorder=4)
        closed = np.vstack([current, current[0]])
        ax_right.plot(closed[:, 0], closed[:, 1], color="#2A9D8F", linewidth=2.0, zorder=5)
        axes_label(ax_right, r"one function: $f\mapsto X_f$")

        fig.suptitle("Infinitesimal generators as vector fields", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_function_flow_stack_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.8, 6.0))
    ax.axis("off")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 10)

    ys = [8.4, 6.3, 4.2, 2.1]
    labels = [
        r"function $f(q,p)$",
        r"vector field $X_f$",
        r"flow $t \mapsto \phi_t^f$",
        r"canonical transformation $\phi_t^f$ at fixed $t$",
    ]
    face = ["#E9EEF6", "#EEF4FB", "#F8EFE8", "#EAF5EE"]
    edge = ["#355070", "#4C78A8", "#BC4749", "#2A9D8F"]
    for y, label, fc, ec in zip(ys, labels, face, edge):
        rect = plt.Rectangle((1.0, y - 0.7), 6.0, 1.2, facecolor=fc, edgecolor=ec, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(4.0, y - 0.1, label, ha="center", va="center", fontsize=12)
    for upper, lower in zip(ys[:-1], ys[1:]):
        ax.annotate("", xy=(4.0, lower + 0.6), xytext=(4.0, upper - 0.8), arrowprops=dict(arrowstyle="->", linewidth=1.8, color="#666666"))

    ax.set_title("Function to canonical transformation", pad=12)
    save_figure(fig, path)


def make_quantum_bridge_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)

    x_left = 2.8
    x_right = 9.2
    ys = [4.8, 3.3, 1.8]
    left = ["functions on phase space", "Poisson brackets", "classical state geometry"]
    right = ["operators", "commutators", "quantum state geometry"]

    for y, ltxt, rtxt in zip(ys, left, right):
        ax.text(x_left, y, ltxt, ha="center", va="center", fontsize=12, color="#355070")
        ax.text(x_right, y, rtxt, ha="center", va="center", fontsize=12, color="#6D597A")
        ax.annotate("", xy=(x_right - 1.3, y), xytext=(x_left + 1.3, y), arrowprops=dict(arrowstyle="->", linewidth=1.9, color="#BC4749"))

    ax.text(6.0, 5.55, "what transports", ha="center", va="center", fontsize=11, color="#333333")
    ax.text(6.0, 0.85, "what changes", ha="center", va="center", fontsize=11, color="#333333")
    ax.set_title("Classical algebra to quantum algebra", pad=12)
    save_figure(fig, path)


def make_canonical_commutation_chain_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10.2, 3.2))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)

    xs = [2.0, 6.0, 10.0]
    equations = [
        r"$\{q,p\}=1$",
        r"$[\hat x,\hat k]=i$",
        r"$[\hat x,\hat p]=i\hbar$",
    ]
    captions = [
        "classical canonical pairing",
        "Fourier generator pairing",
        "quantum commutation relation",
    ]
    colors = ["#355070", "#6D597A", "#BC4749"]

    for x, equation, caption, color in zip(xs, equations, captions, colors):
        rect = plt.Rectangle((x - 1.35, 1.55), 2.7, 1.05, facecolor="#F8F8F8", edgecolor=color, linewidth=1.7)
        ax.add_patch(rect)
        ax.text(x, 2.12, equation, ha="center", va="center", fontsize=18, color="#333333")
        ax.text(x, 1.03, caption, ha="center", va="center", fontsize=9.8, color="#555555")

    for left, right in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(right - 1.55, 2.08), xytext=(left + 1.55, 2.08), arrowprops=dict(arrowstyle="->", linewidth=1.9, color="#777777"))

    ax.set_title("Canonical pairing becomes canonical commutation", pad=10)
    save_figure(fig, path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_style()
    make_spring_ensemble_animation(OUTPUT_DIR / "differential-spring-ensemble-transport.mp4")
    make_pendulum_phase_space_ensemble_animation(OUTPUT_DIR / "differential-pendulum-ensemble-phase-space.mp4")
    make_incompressible_fluid_animation(OUTPUT_DIR / "differential-incompressible-fluid-patch.mp4")
    make_bulk_boundary_diagram(OUTPUT_DIR / "differential-bulk-boundary-variation.png")
    make_bulk_boundary_animation(OUTPUT_DIR / "differential-bulk-boundary-variation.mp4")
    make_one_form_two_form_diagram(OUTPUT_DIR / "differential-one-form-to-two-form.png")
    make_one_form_two_form_animation(OUTPUT_DIR / "differential-one-form-to-two-form.mp4")
    make_level_set_density_vector_diagram(OUTPUT_DIR / "differential-level-set-density-vector.png")
    make_function_to_flow_animation(OUTPUT_DIR / "differential-function-to-flow.mp4")
    make_patch_shear_animation(OUTPUT_DIR / "differential-symplectic-patch-preservation.mp4")
    make_legendre_trade_diagram(OUTPUT_DIR / "differential-legendre-transform-trade.png")
    make_legendre_tangent_animation(OUTPUT_DIR / "differential-legendre-transform-tangent.mp4")
    make_relativistic_boundary_pairing_diagram(OUTPUT_DIR / "differential-relativistic-boundary-pairing.png")
    make_endpoint_covector_animation(OUTPUT_DIR / "differential-endpoint-covector-measurement.mp4")
    make_worldline_phase_space_bridge_diagram(OUTPUT_DIR / "differential-worldline-phase-space-bridge.png")
    make_worldline_phase_space_bridge_animation(OUTPUT_DIR / "differential-worldline-phase-space-bridge.mp4")
    make_action_decomposition_diagram(OUTPUT_DIR / "differential-action-decomposition.png")
    make_poisson_compression_diagram(OUTPUT_DIR / "differential-poisson-compression.png")
    make_poisson_antisymmetry_area_animation(OUTPUT_DIR / "differential-poisson-antisymmetry-area.mp4")
    make_poisson_antisymmetry_area_diagram(OUTPUT_DIR / "differential-poisson-antisymmetry-area.png")
    make_poisson_jacobi_identity_animation(OUTPUT_DIR / "differential-poisson-jacobi-identity.mp4")
    make_skier_position_generates_momentum_animation(OUTPUT_DIR / "differential-skier-position-generates-momentum.mp4")
    make_poisson_product_rule_animation(OUTPUT_DIR / "differential-poisson-product-rule.mp4")
    make_poisson_bidirectional_flow_animation(OUTPUT_DIR / "differential-poisson-bidirectional-flow.mp4")
    make_poisson_bracket_vectorfield_identity_animation(OUTPUT_DIR / "differential-poisson-bracket-vectorfield-identity.mp4")
    make_fourier_momentum_shift_phase_animation(OUTPUT_DIR / "differential-fourier-momentum-shift-phase.mp4")
    make_fourier_phase_shift_mechanism_animation(OUTPUT_DIR / "differential-fourier-phase-shift-mechanism.mp4")
    make_weyl_order_phase_animation(OUTPUT_DIR / "differential-weyl-order-phase.mp4")
    make_lie_generator_tangent_flow_animation(OUTPUT_DIR / "differential-lie-generator-tangent-flow.mp4")
    make_exponential_map_accumulation_animation(OUTPUT_DIR / "differential-exponential-map-accumulation.mp4")
    make_generator_vector_field_contrast_animation(OUTPUT_DIR / "differential-generator-vector-field-contrast.mp4")
    make_function_flow_stack_diagram(OUTPUT_DIR / "differential-function-flow-stack.png")
    make_quantum_bridge_diagram(OUTPUT_DIR / "differential-quantum-bridge.png")
    make_canonical_commutation_chain_diagram(OUTPUT_DIR / "differential-canonical-commutation-chain.png")


if __name__ == "__main__":
    main()
