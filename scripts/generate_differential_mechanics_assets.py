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
    ax.text(0.98, y[-1] + 0.22, "boundary variation", ha="right", color="#BC4749")
    ax.text(0.02, y[0] - 0.24, "boundary variation", ha="left", va="top", color="#BC4749")
    ax.text(0.0, -0.42, "$t_1$", ha="center")
    ax.text(1.0, -0.42, "$t_2$", ha="center")

    ax.set_title("Action variation separates into bulk and boundary pieces")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.55, 0.95)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    save_figure(fig, path)


def make_one_form_two_form_diagram(path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))

    ax = axes[0]
    ax.scatter([0], [0], s=55, color="#355070", zorder=3)
    ax.annotate("", xy=(1.25, 0.35), xytext=(0, 0), arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#BC4749"))
    ax.text(1.32, 0.38, r"$\delta q$", color="#BC4749", va="center")
    ax.text(0.0, -1.05, r"one state", ha="center", fontsize=10)
    ax.text(0.0, -1.33, r"$p_i\,\delta q^i$", ha="center", fontsize=12)
    ax.set_title("One-form")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.8)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1]
    origin = np.array([0.0, 0.0])
    dq = np.array([1.15, 0.18])
    dp = np.array([0.28, 1.0])
    patch = np.array([origin, origin + dq, origin + dq + dp, origin + dp])
    poly = Polygon(patch, closed=True, facecolor="#54A24B", alpha=0.25, edgecolor="#2A9D8F", linewidth=2.0)
    ax.add_patch(poly)
    ax.annotate("", xy=origin + dq, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#BC4749"))
    ax.annotate("", xy=origin + dp, xytext=origin, arrowprops=dict(arrowstyle="->", linewidth=2.2, color="#4C78A8"))
    ax.text(*(origin + dq + np.array([0.1, -0.1])), r"$dq$", color="#BC4749")
    ax.text(*(origin + dp + np.array([0.06, 0.06])), r"$dp$", color="#4C78A8")
    ax.text(0.75, -1.05, r"patch of nearby states", ha="center", fontsize=10)
    ax.text(0.75, -1.33, r"$dq^i \wedge dp_i$", ha="center", fontsize=12)
    ax.set_title("Two-form")
    ax.set_aspect("equal")
    ax.set_xlim(-0.6, 2.0)
    ax.set_ylim(-1.5, 1.7)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle("From one displaced state to a phase-space area element", y=0.98)
    save_figure(fig, path)


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

        ax.set_title("A phase-space function induces a crossed flow field", pad=14)
        ax.text(0.02, 1.02, r"$F(q,p)=p^2/2+q^4/4$", transform=ax.transAxes, ha="left", va="bottom", color="#555555")
        ax.text(0.02, 0.97, r"$\dot q=\partial F/\partial p,\ \dot p=-\partial F/\partial q$", transform=ax.transAxes, ha="left", va="top", color="#333333")
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

        ax.text(0.02, 1.02, r"$H=p^2/2 \Rightarrow \dot q = p,\ \dot p = 0$", transform=ax.transAxes, ha="left", va="bottom", color="#555555")
        ax.text(0.02, 0.97, "Patch shears while area stays fixed", transform=ax.transAxes, ha="left", va="top", color="#333333")
        ax.set_title("A Hamiltonian flow can distort shape without compressing phase-space area", pad=14)
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.set_xlim(-1.6, 1.8)
        ax.set_ylim(-1.25, 1.25)
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

    ax.set_title("The Legendre transform trades velocity variables for conjugate momenta", pad=12)
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

    ax.set_title("Poisson algebra compresses the same mechanics into a smaller set of relations", pad=12)
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
    ax.set_title("The algebraic skeleton carries across the classical-to-quantum transition", pad=12)
    save_figure(fig, path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_style()
    make_bulk_boundary_diagram(OUTPUT_DIR / "differential-bulk-boundary-variation.png")
    make_one_form_two_form_diagram(OUTPUT_DIR / "differential-one-form-to-two-form.png")
    make_function_to_flow_animation(OUTPUT_DIR / "differential-function-to-flow.mp4")
    make_patch_shear_animation(OUTPUT_DIR / "differential-symplectic-patch-preservation.mp4")
    make_legendre_trade_diagram(OUTPUT_DIR / "differential-legendre-transform-trade.png")
    make_poisson_compression_diagram(OUTPUT_DIR / "differential-poisson-compression.png")
    make_quantum_bridge_diagram(OUTPUT_DIR / "differential-quantum-bridge.png")


if __name__ == "__main__":
    main()
