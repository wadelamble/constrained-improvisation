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
    fixed = np.array([1.0, 0.0])
    radius = 1.0

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8))

    def draw_reference_axes(ax: plt.Axes) -> None:
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-1.25, 1.35)
        ax.set_ylim(-1.25, 1.35)
        ax.axhline(0, color="#AAAAAA", linewidth=0.9, zorder=0)
        ax.axvline(0, color="#AAAAAA", linewidth=0.9, zorder=0)
        ax.grid(color="#ECECEC", linewidth=0.7)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    def draw_frame(frame: int) -> None:
        theta = 2.0 * np.pi * frame / frames
        moving = radius * np.array([np.cos(theta), np.sin(theta)])
        overlap = float(np.dot(fixed, moving))
        area = float(fixed[0] * moving[1] - fixed[1] * moving[0])

        ax = axes[0]
        ax.clear()
        draw_reference_axes(ax)
        ax.set_title("One-form: overlap")
        ax.annotate("", xy=fixed, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#4C78A8"), zorder=4)
        ax.annotate("", xy=moving, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#BC4749"), zorder=5)
        ax.plot([moving[0], overlap], [moving[1], 0], color="#8A8A8A", linestyle=":", linewidth=1.2, zorder=3)
        ax.plot([0, overlap], [0, 0], color="#D49A3A", linewidth=4.0, alpha=0.85, solid_capstyle="round", zorder=6)
        ax.scatter([0], [0], s=32, color="#333333", zorder=7)
        ax.text(0.95, 0.12, r"$p_i$", color="#4C78A8", ha="center", va="bottom", fontsize=11.5)
        ax.text(-1.10, 1.12, r"$p_i\,\delta q^i$", color="#333333", ha="left", va="top", fontsize=12.5, bbox=LABEL_BOX)
        ax.text(-1.10, -1.08, f'"overlap" = {overlap:+.2f}', color="#9A6A1F", ha="left", va="center", fontsize=10.0, bbox=LABEL_BOX)

        ax = axes[1]
        ax.clear()
        draw_reference_axes(ax)
        ax.set_title("Two-form: oriented area")
        patch = np.array([[0, 0], fixed, fixed + moving, moving])
        poly = Polygon(patch, closed=True, facecolor="#54A24B", alpha=0.24, edgecolor="#2A9D8F", linewidth=2.0, zorder=2)
        ax.add_patch(poly)
        ax.annotate("", xy=fixed, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#4C78A8"), zorder=4)
        ax.annotate("", xy=moving, xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#BC4749"), zorder=5)
        ax.scatter([0], [0], s=32, color="#333333", zorder=7)
        ax.text(0.95, 0.12, r"$dq$", color="#4C78A8", ha="center", va="bottom", fontsize=11.5)
        ax.text(-1.10, 1.12, r"$dq^i \wedge dp_i$", color="#333333", ha="left", va="top", fontsize=12.5, bbox=LABEL_BOX)
        ax.text(-1.10, -1.08, f"area = {area:+.2f}", color="#2A9D8F", ha="left", va="center", fontsize=10.0, bbox=LABEL_BOX)

        fig.suptitle("Same directions, different measurements", y=0.98)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


def make_function_to_flow_animation(path: Path) -> None:
    q = np.linspace(-1.7, 1.7, 280)
    p = np.linspace(-1.6, 1.6, 260)
    qq, pp = np.meshgrid(q, p)
    F = 0.5 * pp**2 + 0.25 * qq**4

    qv = np.linspace(-1.5, 1.5, 14)
    pv = np.linspace(-1.35, 1.35, 12)
    qvq, pvq = np.meshgrid(qv, pv)
    uq = pvq
    vp = -(qvq**3)
    speed = np.hypot(uq, vp)
    scale = np.maximum(speed, 1e-8)

    state = np.array([1.05, 0.0], dtype=float)
    dt = 0.045
    n_frames = 110
    trail = np.empty((n_frames, 2))
    for i in range(n_frames):
        trail[i] = state
        state = rk4_step(state, dt)

    fig, ax = plt.subplots(figsize=(6.8, 6.0))

    def draw_frame(frame: int) -> None:
        ax.clear()
        phase_a = min(frame / 24.0, 1.0)
        phase_b = min(max(frame - 18, 0) / 26.0, 1.0)
        tracer_n = min(frame + 1, n_frames)

        ax.contour(
            qq,
            pp,
            F,
            levels=[0.12, 0.28, 0.52, 0.85, 1.28, 1.82],
            colors="#7A7A7A",
            linewidths=1.0,
            alpha=0.65 + 0.35 * phase_a,
        )

        ax.quiver(
            qvq,
            pvq,
            uq / scale,
            vp / scale,
            color="#355070",
            alpha=0.08 + 0.72 * phase_b,
            pivot="mid",
            scale=24,
            width=0.0045,
        )

        ax.plot(trail[:tracer_n, 0], trail[:tracer_n, 1], color="#BC4749", linewidth=2.2, alpha=0.85)
        ax.scatter([trail[tracer_n - 1, 0]], [trail[tracer_n - 1, 1]], color="#BC4749", s=34, zorder=4)

        ax.set_title("Function to flow", pad=10)
        axes_label(ax, r"$F=p^2/2+q^4/4,\quad \dot q=\partial_p F,\quad \dot p=-\partial_q F$")
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.grid(color="#E8E8E8", linewidth=0.7)

    anim = FuncAnimation(fig, draw_frame, frames=n_frames, interval=1000 / 18, blit=False)
    save_animation(anim, path, fps=18)
    plt.close(fig)


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


def make_action_decomposition_diagram(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    origin = np.array([1.4, 1.2])
    dx = np.array([4.0, 0.0])
    dt = np.array([0.0, 3.2])
    disp = dx + 0.72 * dt
    ax.annotate("", xy=origin + dx, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.0, color="#BC4749"))
    ax.annotate("", xy=origin + 0.72 * dt, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.0, color="#4C78A8"))
    ax.annotate("", xy=origin + disp, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.4, color="#355070"))
    ax.text(*(origin + dx / 2 + np.array([0.0, -0.35])), r"$\delta q$", color="#BC4749", ha="center")
    ax.text(*(origin + 0.72 * dt / 2 + np.array([-0.3, 0.0])), r"$\delta t$", color="#4C78A8", va="center")
    ax.text(*(origin + disp + np.array([0.15, 0.08])), r"$\delta x^\mu$", color="#355070")

    ax.text(7.45, 4.15, r"$\delta S = p_i\,\delta q^i - E\,\delta t$", fontsize=16, ha="center")
    ax.text(7.45, 2.75, r"$-\int E\,dt \quad + \quad \int p_x\,dx \quad + \cdots$", fontsize=15, ha="center", color="#333333")
    ax.set_title("Temporal and spatial action pieces", pad=12)
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
    make_function_to_flow_animation(OUTPUT_DIR / "differential-function-to-flow.mp4")
    make_patch_shear_animation(OUTPUT_DIR / "differential-symplectic-patch-preservation.mp4")
    make_legendre_trade_diagram(OUTPUT_DIR / "differential-legendre-transform-trade.png")
    make_relativistic_boundary_pairing_diagram(OUTPUT_DIR / "differential-relativistic-boundary-pairing.png")
    make_endpoint_covector_animation(OUTPUT_DIR / "differential-endpoint-covector-measurement.mp4")
    make_worldline_phase_space_bridge_diagram(OUTPUT_DIR / "differential-worldline-phase-space-bridge.png")
    make_action_decomposition_diagram(OUTPUT_DIR / "differential-action-decomposition.png")
    make_poisson_compression_diagram(OUTPUT_DIR / "differential-poisson-compression.png")
    make_function_flow_stack_diagram(OUTPUT_DIR / "differential-function-flow-stack.png")
    make_quantum_bridge_diagram(OUTPUT_DIR / "differential-quantum-bridge.png")


if __name__ == "__main__":
    main()
