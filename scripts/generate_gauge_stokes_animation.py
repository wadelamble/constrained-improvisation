from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"


def source_strength(phase: float) -> float:
    return 0.18 + 0.82 * (0.5 + 0.5 * np.sin(phase)) ** 1.4


def make_animation(video_path: Path, still_path: Path, contact_path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = 168
    fps = 24
    n_arrows = 28
    angles = np.linspace(0, 2 * np.pi, n_arrows, endpoint=False)

    fig = plt.figure(figsize=(12, 6.1), dpi=160)
    fig.patch.set_facecolor("#f8f5ef")
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1.0], height_ratios=[1.0, 0.42])
    ax_flux = fig.add_subplot(gs[:, 0])
    ax_cell = fig.add_subplot(gs[0, 1])
    ax_text = fig.add_subplot(gs[1, 1])

    for ax in [ax_flux, ax_cell, ax_text]:
        ax.set_facecolor("#f8f5ef")

    ax_flux.set_aspect("equal")
    ax_flux.set_xlim(-1.8, 1.8)
    ax_flux.set_ylim(-1.8, 1.8)
    ax_flux.axis("off")

    ax_cell.set_aspect("equal")
    ax_cell.set_xlim(-1.35, 1.35)
    ax_cell.set_ylim(-1.1, 1.25)
    ax_cell.axis("off")

    ax_text.axis("off")

    boundary = Circle((0, 0), 1.0, fill=False, ec="#333", lw=2.2)
    ax_flux.add_patch(boundary)
    ax_flux.text(0, 1.18, "boundary of the region", ha="center", va="center", fontsize=10)

    source = Circle((0, 0), 0.13, fc="#b5493a", ec="#7d2f25", lw=1.2, zorder=4)
    ax_flux.add_patch(source)
    source_text = ax_flux.text(0, -0.28, "", ha="center", va="center", fontsize=10, color="#7d2f25")

    flux_arrows = []
    for a in angles:
        p0 = np.array([np.cos(a), np.sin(a)]) * 0.82
        p1 = np.array([np.cos(a), np.sin(a)]) * 1.28
        arrow = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11,
                                lw=1.35, color="#1f6f78", alpha=0.75)
        ax_flux.add_patch(arrow)
        flux_arrows.append(arrow)

    scan_arc = Arc((0, 0), 2.08, 2.08, theta1=0, theta2=0, lw=5.0,
                   color="#d6a23a", alpha=0.95, capstyle="round")
    ax_flux.add_patch(scan_arc)
    scan_dot, = ax_flux.plot([], [], "o", color="#d6a23a", ms=8, zorder=5)

    ax_flux.text(0, -1.52, "add up the field crossing the boundary",
                 ha="center", va="center", fontsize=11)
    meter_back = Rectangle((-1.15, -1.36), 2.3, 0.12, fc="#eee4d6", ec="#c8b99f", lw=1)
    meter_fill = Rectangle((-1.15, -1.36), 0.0, 0.12, fc="#1f6f78", ec="none")
    ax_flux.add_patch(meter_back)
    ax_flux.add_patch(meter_fill)
    meter_text = ax_flux.text(0, -1.16, "", ha="center", va="center", fontsize=10)

    square = Rectangle((-0.55, -0.55), 1.1, 1.1, fill=False, ec="#333", lw=2.0)
    ax_cell.add_patch(square)
    cell_source = Circle((0, 0), 0.12, fc="#b5493a", ec="#7d2f25", lw=1.1, zorder=4)
    ax_cell.add_patch(cell_source)
    ax_cell.text(0, 0.82, "local version", ha="center", va="center", fontsize=12)
    ax_cell.text(0, -0.85, "net outward field from a tiny cell", ha="center", fontsize=10)

    cell_arrows = []
    base_pairs = [
        ((0, 0.55), (0, 0.93)),
        ((0.55, 0), (0.93, 0)),
        ((0, -0.55), (0, -0.93)),
        ((-0.55, 0), (-0.93, 0)),
    ]
    for p0, p1 in base_pairs:
        arrow = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14,
                                lw=1.8, color="#1f6f78", alpha=0.8)
        ax_cell.add_patch(arrow)
        cell_arrows.append((arrow, np.array(p0), np.array(p1)))

    ax_text.text(0.5, 0.82, r"$d{*F}=J$", ha="center", va="center", fontsize=22)
    ax_text.text(0.5, 0.52, r"$\int_{\partial V}{*F}=\int_V J$", ha="center", va="center", fontsize=19)
    ax_text.text(0.5, 0.19,
                 "Read it as: boundary field-flux equals enclosed source.",
                 ha="center", va="center", fontsize=11)

    def update(i: int):
        phase = 2 * np.pi * i / frames
        q = source_strength(phase)
        sweep = (360 * (i % frames) / frames)

        source.set_radius(0.11 + 0.07 * q)
        cell_source.set_radius(0.10 + 0.06 * q)
        source_text.set_text("source J")

        for arrow, a in zip(flux_arrows, angles):
            p0 = np.array([np.cos(a), np.sin(a)]) * (0.82 + 0.02 * q)
            p1 = np.array([np.cos(a), np.sin(a)]) * (1.02 + 0.38 * q)
            arrow.set_positions(p0, p1)
            arrow.set_alpha(0.25 + 0.65 * q)
            arrow.set_linewidth(0.8 + 1.1 * q)

        scan_arc.theta1 = 0
        scan_arc.theta2 = sweep
        dot_angle = np.deg2rad(sweep)
        scan_dot.set_data([1.04 * np.cos(dot_angle)], [1.04 * np.sin(dot_angle)])

        meter_fill.set_width(2.3 * q)
        meter_text.set_text("boundary flux grows with enclosed source")

        for arrow, p0_base, p1_base in cell_arrows:
            direction = p1_base - p0_base
            p1 = p0_base + direction * (0.45 + 0.9 * q)
            arrow.set_positions(p0_base, p1)
            arrow.set_alpha(0.25 + 0.65 * q)
            arrow.set_linewidth(0.9 + 1.4 * q)

        return [source, cell_source, source_text, scan_arc, scan_dot, meter_fill, meter_text] + flux_arrows + [a[0] for a in cell_arrows]

    update(35)
    fig.suptitle("The sourced Maxwell equation as a Stokes statement", fontsize=16, y=0.97)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(still_path, bbox_inches="tight")

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=True)
    anim.save(video_path, writer=FFMpegWriter(fps=fps, bitrate=2000))

    sheet_fig, sheet_axes = plt.subplots(1, 4, figsize=(12, 3.1), dpi=180)
    sheet_fig.patch.set_facecolor("#f8f5ef")
    for ax, idx, title in zip(sheet_axes, [0, 32, 64, 96], ["low source", "rising", "high source", "falling"]):
        ax.set_facecolor("#f8f5ef")
        ax.set_aspect("equal")
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        ax.axis("off")
        q = source_strength(2 * np.pi * idx / frames)
        ax.add_patch(Circle((0, 0), 1.0, fill=False, ec="#333", lw=1.5))
        ax.add_patch(Circle((0, 0), 0.11 + 0.07 * q, fc="#b5493a", ec="#7d2f25", lw=1))
        for a in angles[::2]:
            p0 = np.array([np.cos(a), np.sin(a)]) * 0.84
            p1 = np.array([np.cos(a), np.sin(a)]) * (1.02 + 0.38 * q)
            ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=9,
                                         lw=0.8 + 1.0 * q, color="#1f6f78",
                                         alpha=0.25 + 0.65 * q))
        ax.set_title(title, fontsize=10)
    sheet_fig.suptitle("Boundary flux tracks enclosed source", fontsize=13)
    sheet_fig.tight_layout()
    sheet_fig.savefig(contact_path, bbox_inches="tight")
    plt.close(sheet_fig)
    plt.close(fig)


def main() -> None:
    make_animation(
        OUTPUT_DIR / "gauge-source-stokes-flux.mp4",
        OUTPUT_DIR / "gauge-source-stokes-flux.png",
        OUTPUT_DIR / "gauge-source-stokes-flux-contact-sheet.png",
    )


if __name__ == "__main__":
    main()
