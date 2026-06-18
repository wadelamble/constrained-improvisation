from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"

PAPER = "#FFFDF8"
INK = "#2F2F2F"
BLUE = "#245E91"
ORANGE = "#B85C38"
GREEN = "#5B7F72"
MUTED = "#8B8278"


def line_segment_through(point: np.ndarray, direction: np.ndarray, half_length: float) -> tuple[np.ndarray, np.ndarray]:
    direction = direction / np.linalg.norm(direction)
    return point - half_length * direction, point + half_length * direction


def draw_angle_arc(ax, center, radius, start_deg, end_deg, color, label, label_angle_deg, label_radius):
    arc = Arc(
        center,
        2 * radius,
        2 * radius,
        angle=0,
        theta1=start_deg,
        theta2=end_deg,
        color=color,
        lw=1.8,
        zorder=8,
    )
    ax.add_patch(arc)
    angle = np.deg2rad(label_angle_deg)
    ax.text(
        center[0] + label_radius * np.cos(angle),
        center[1] + label_radius * np.sin(angle),
        label,
        fontsize=16,
        color=color,
        ha="center",
        va="center",
        zorder=9,
    )


def make_diagram(path: Path) -> None:
    theta1 = np.deg2rad(50.0)
    speed_ratio = 0.58
    theta2 = np.arcsin(speed_ratio * np.sin(theta1))

    A = np.array([0.0, 0.0])
    d_boundary = 4.25
    B = np.array([d_boundary, 0.0])

    incoming_ray = np.array([np.sin(theta1), -np.cos(theta1)])
    incoming_front_dir = np.array([np.cos(theta1), np.sin(theta1)])
    refracted_ray = np.array([np.sin(theta2), -np.cos(theta2)])
    refracted_front_dir = np.array([np.cos(theta2), np.sin(theta2)])

    upper_advance = d_boundary * np.sin(theta1)
    lower_radius = d_boundary * np.sin(theta2)
    tangent_point = lower_radius * refracted_ray

    fig, ax = plt.subplots(figsize=(12, 7), dpi=160)
    fig.patch.set_facecolor("#F7F3EC")
    ax.set_facecolor(PAPER)
    ax.set_xlim(-1.2, 6.3)
    ax.set_ylim(-3.35, 3.3)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    ax.axhspan(0, 3.4, color="#D8E8F7", alpha=0.34, zorder=0)
    ax.axhspan(-3.4, 0, color="#F7DFC9", alpha=0.36, zorder=0)
    ax.plot([-1.2, 6.3], [0, 0], color="#59524A", lw=2.0, zorder=4)
    ax.text(-1.05, 2.92, "medium 1, speed $v_1$", fontsize=13, color=BLUE)
    ax.text(-1.05, -3.08, "medium 2, speed $v_2$", fontsize=13, color=ORANGE)

    ax.text(
        0.5,
        1.03,
        "Huygens construction gives Snell's law",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=17,
        color=INK,
        weight="bold",
    )

    # Incoming wavefront at A and the later incoming wavefront at B.
    old_p0, old_p1 = line_segment_through(A, incoming_front_dir, 2.9)
    new_p0, new_p1 = line_segment_through(B, incoming_front_dir, 2.65)
    ax.plot([old_p0[0], old_p1[0]], [old_p0[1], old_p1[1]], color=BLUE, lw=2.4, alpha=0.48, zorder=3)
    ax.plot([new_p0[0], new_p1[0]], [new_p0[1], new_p1[1]], color=BLUE, lw=3.0, alpha=0.78, zorder=3)
    ax.text(-0.63, 1.28, "incoming front\nhits A first", fontsize=11.5, color=BLUE, ha="left")
    ax.text(4.23, 1.54, "same front\nat $T=t_A+\\Delta t$", fontsize=11.5, color=BLUE, ha="left")

    # Incoming ray and normal.
    ray_start = A - 2.4 * incoming_ray
    ax.annotate(
        "",
        xy=A,
        xytext=ray_start,
        arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 2.4},
        zorder=7,
    )
    ax.plot([A[0], A[0]], [-2.95, 2.95], ls="--", color="#6B625A", lw=1.2, alpha=0.75, zorder=2)
    ax.text(0.08, 2.72, "normal", fontsize=11.5, color="#6B625A")

    # Show the upper-medium advance between the two incoming fronts.
    measure_start = A + 3.85 * incoming_front_dir
    measure_end = measure_start + upper_advance * incoming_ray
    ax.annotate(
        "",
        xy=measure_end,
        xytext=measure_start,
        arrowprops={"arrowstyle": "<->", "color": BLUE, "lw": 1.8},
        zorder=7,
    )
    mid = 0.5 * (measure_start + measure_end)
    ax.text(mid[0] + 0.08, mid[1] + 0.18, "$v_1\\Delta t$", fontsize=14, color=BLUE)

    # Huygens wavelet in the second medium and refracted tangent front.
    wavelet = Arc(
        A,
        2 * lower_radius,
        2 * lower_radius,
        angle=0,
        theta1=180,
        theta2=360,
        edgecolor=ORANGE,
        lw=2.4,
        alpha=0.82,
        zorder=5,
    )
    ax.add_patch(wavelet)
    tangent_p0, tangent_p1 = line_segment_through(B, refracted_front_dir, 3.2)
    ax.plot(
        [tangent_p0[0], tangent_p1[0]],
        [tangent_p0[1], tangent_p1[1]],
        color=ORANGE,
        lw=3.0,
        alpha=0.88,
        zorder=6,
    )
    ax.scatter([tangent_point[0]], [tangent_point[1]], s=38, color=ORANGE, zorder=9)
    ax.plot([A[0], tangent_point[0]], [A[1], tangent_point[1]], color=ORANGE, lw=2.0, alpha=0.88, zorder=7)
    ax.text(tangent_point[0] + 0.18, tangent_point[1] - 0.34, "$v_2\\Delta t$", fontsize=14, color=ORANGE)
    ax.text(3.08, -1.72, "refracted front:\ntangent to the wavelet", fontsize=11.5, color=ORANGE, ha="left")

    ax.annotate(
        "",
        xy=tangent_point + 0.85 * refracted_ray,
        xytext=A,
        arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 2.4},
        zorder=8,
    )

    # Boundary points and shared distance.
    ax.scatter([A[0], B[0]], [A[1], B[1]], s=48, color=INK, zorder=10)
    ax.text(A[0] - 0.19, A[1] + 0.17, "A", fontsize=15, color=INK, weight="bold")
    ax.text(B[0] + 0.08, B[1] + 0.17, "B", fontsize=15, color=INK, weight="bold")
    ax.annotate(
        "",
        xy=(B[0], 0.20),
        xytext=(A[0], 0.20),
        arrowprops={"arrowstyle": "<->", "color": MUTED, "lw": 1.6},
        zorder=8,
    )
    ax.text(0.5 * d_boundary, 0.34, "$AB$", fontsize=14, color=MUTED, ha="center")

    # Angle arcs.
    draw_angle_arc(
        ax,
        A,
        0.70,
        90,
        90 + np.rad2deg(theta1),
        BLUE,
        "$\\theta_1$",
        90 + 0.52 * np.rad2deg(theta1),
        0.96,
    )
    draw_angle_arc(
        ax,
        A,
        0.86,
        270,
        270 + np.rad2deg(theta2),
        ORANGE,
        "$\\theta_2$",
        270 + 0.58 * np.rad2deg(theta2),
        1.14,
    )

    # Small formula callout.
    ax.text(
        5.04,
        0.78,
        "$\\sin\\theta_1=\\dfrac{v_1\\Delta t}{AB}$\n\n"
        "$\\sin\\theta_2=\\dfrac{v_2\\Delta t}{AB}$",
        fontsize=14,
        color=INK,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "fc": "#FFFDF8", "ec": "#D0C5B9", "lw": 1.0},
        zorder=12,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


if __name__ == "__main__":
    make_diagram(OUT / "lm-huygens-snell-two-point-construction-review.png")
