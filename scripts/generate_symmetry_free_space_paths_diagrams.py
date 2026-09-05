from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#fbf8f1"
INK = "#25282d"
MUTED = "#68645f"
BLUE = "#2d5f91"
BLUE_LIGHT = "#9eb5ca"
ORANGE = "#c67c13"
GREEN = "#347a5a"
RED = "#b45a4a"
GRID = "#ddd5c9"


def canvas(title, subtitle=None):
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 12.8)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.text(0.42, 6.83, title, fontsize=23, weight="medium", color=INK, va="top")
    if subtitle:
        ax.text(0.42, 6.43, subtitle, fontsize=13, color=MUTED, va="top")
    return fig, ax


def point(ax, xy, label, color=INK, label_offset=(0, -0.38), radius=0.095):
    ax.add_patch(Circle(xy, radius, facecolor=color, edgecolor=color, zorder=8))
    ax.text(
        xy[0] + label_offset[0],
        xy[1] + label_offset[1],
        label,
        fontsize=13,
        color=INK,
        ha="center",
        va="center",
        zorder=9,
    )


def arrow(ax, p0, p1, color=BLUE, lw=2.0, alpha=1.0, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            p0,
            p1,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=lw,
            linestyle=ls,
            color=color,
            alpha=alpha,
            shrinkA=7,
            shrinkB=7,
            zorder=5,
        )
    )


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=100, facecolor=BG, bbox_inches=None)
    plt.close(fig)
    print(path)


def diagram_1_spreading_vs_same_endpoint():
    fig, ax = canvas(
        "Spreading and alternate routes are different pictures",
        "Spreading alone does not show two routes from A to the same B.",
    )
    ax.plot([6.4, 6.4], [0.65, 6.05], color=GRID, lw=1.5)

    ax.text(3.2, 5.85, "one source → several endpoints", fontsize=17, color=BLUE, ha="center")
    A = (1.05, 3.25)
    endpoints = [(5.45, 4.95), (5.45, 3.25), (5.45, 1.55)]
    point(ax, A, "A")
    labels = ["B", "C", "D"]
    for p, lab in zip(endpoints, labels):
        point(ax, p, lab)
        ax.text(p[0] - 0.15, p[1] + 0.3, rf"$\psi({lab})$", color=BLUE, fontsize=12, ha="right")
    for r in (0.75, 1.55, 2.35, 3.15, 4.0, 4.75):
        ax.add_patch(Arc(A, 2 * r, 2 * r, theta1=-32, theta2=32, color=BLUE_LIGHT, lw=1.35))
    ax.text(
        3.2,
        0.85,
        "This is spreading.\nThe destinations differ.",
        fontsize=15,
        color=INK,
        ha="center",
        va="center",
    )

    ax.text(9.55, 5.85, "several contributions → one endpoint", fontsize=17, color=GREEN, ha="center")
    A2, C, D, B2 = (7.05, 3.25), (9.25, 4.65), (9.25, 1.85), (12.0, 3.25)
    point(ax, A2, "A")
    point(ax, C, "C", color=BLUE)
    point(ax, D, "D", color=ORANGE)
    point(ax, B2, "B")
    for p0, p1, col in ((A2, C, BLUE), (C, B2, BLUE), (A2, D, ORANGE), (D, B2, ORANGE)):
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=col, lw=2.2, ls="--")
    ax.text(
        9.55,
        0.85,
        "This is the question relevant to interference:\nwhat contributes to the same B?",
        fontsize=15,
        color=INK,
        ha="center",
        va="center",
    )
    save(fig, "symmetry-free-space-paths-1-spreading-versus-one-endpoint.png")


def diagram_2_extended_profile():
    fig, ax = canvas(
        "An extended initial wave contributes to one B from many points",
        "The dashed lines label terms in the propagation integral, not material tracks.",
    )
    x0 = 2.0
    ys = np.linspace(1.05, 5.8, 600)
    amp = np.exp(-0.5 * ((ys - 3.43) / 1.05) ** 2)
    ax.plot(x0 + 0.72 * amp, ys, color=BLUE, lw=3)
    ax.plot([x0, x0], [0.85, 6.0], color=INK, lw=1.2)
    ax.text(1.3, 5.8, r"prepared field $\psi_0(\xi)$", color=BLUE, fontsize=15, ha="center")
    ax.text(2.0, 0.63, r"initial plane", color=MUTED, fontsize=12, ha="center")

    B = (10.95, 3.42)
    point(ax, B, "B", label_offset=(0, -0.42))
    sample_y = np.linspace(1.25, 5.6, 9)
    weights = np.exp(-0.5 * ((sample_y - 3.43) / 1.05) ** 2)
    for yy, wt in zip(sample_y, weights):
        start = (x0 + 0.72 * wt, yy)
        ax.plot([start[0], B[0]], [start[1], B[1]], color=BLUE, lw=0.9 + 1.1 * wt, alpha=0.18 + 0.46 * wt, ls="--")
        ax.add_patch(Circle(start, 0.055, facecolor=GREEN, edgecolor=GREEN, zorder=6))

    ax.text(6.45, 5.55, "free propagation—no screen", color=GREEN, fontsize=17, ha="center")
    ax.text(
        6.45,
        1.03,
        r"$\psi(B)=\int K(B,\xi)\,\psi_0(\xi)\,d\xi$",
        fontsize=20,
        color=INK,
        ha="center",
    )
    ax.text(
        6.45,
        0.55,
        r"Every illuminated $\xi$ contributes to the same endpoint $B$.",
        fontsize=14,
        color=MUTED,
        ha="center",
    )
    save(fig, "symmetry-free-space-paths-2-extended-wave-to-one-endpoint.png")


def fresnel_field():
    y = np.linspace(-3.2, 3.2, 720)
    dy = y[1] - y[0]
    q = 2 * np.pi * np.fft.fftfreq(y.size, d=dy)
    sigma = 0.18
    sep = 0.72
    psi0 = np.exp(-((y - sep) ** 2) / (2 * sigma**2)) + np.exp(-((y + sep) ** 2) / (2 * sigma**2))
    psi0 /= np.sqrt(np.trapezoid(np.abs(psi0) ** 2, y))
    spectrum = np.fft.fft(psi0)
    z = np.linspace(0.04, 7.2, 620)
    carrier_k = 13.0
    intensity = np.empty((y.size, z.size))
    for idx, zz in enumerate(z):
        propagated = np.fft.ifft(spectrum * np.exp(-1j * q**2 * zz / (2 * carrier_k)))
        intensity[:, idx] = np.abs(propagated) ** 2
    intensity /= intensity.max()
    return y, z, psi0, intensity


def diagram_3_two_lobes():
    y, z, psi0, intensity = fresnel_field()
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=BG)
    ax = fig.add_axes([0.07, 0.17, 0.87, 0.65])
    ax.set_facecolor(BG)
    fig.text(0.035, 0.95, "Slit-like interference can develop during free propagation", fontsize=23, weight="medium", color=INK, va="top")
    fig.text(
        0.035,
        0.895,
        "Here the wave is prepared with two coherent lobes; there is no screen in the propagation region.",
        fontsize=13,
        color=MUTED,
        va="top",
    )
    extent = [z.min(), z.max(), y.min(), y.max()]
    ax.imshow(
        intensity,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="Blues",
        vmin=0,
        vmax=0.9,
        interpolation="bilinear",
    )
    ax.plot(0.06 + 0.54 * np.abs(psi0) / np.abs(psi0).max(), y, color=ORANGE, lw=2.4)
    ax.axvline(0.04, color=INK, lw=1.2)
    ax.text(0.55, 2.72, "two-lobed initial field", color=ORANGE, fontsize=14, ha="left")
    ax.text(4.2, 2.92, "free space", color=GREEN, fontsize=17, ha="center")
    ax.annotate(
        "the lobes overlap\nand interfere",
        xy=(4.7, 0.45),
        xytext=(5.8, 2.0),
        color=INK,
        fontsize=14,
        arrowprops=dict(arrowstyle="->", color=INK, lw=1.4),
        ha="center",
    )
    ax.set_xlabel("propagation distance", fontsize=13, color=INK)
    ax.set_ylabel("transverse position", fontsize=13, color=INK)
    ax.tick_params(colors=MUTED, labelsize=11)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    fig.text(
        0.5,
        0.035,
        "The preparation supplies the two coherent contributions; free propagation supplies their overlap and interference.",
        ha="center",
        color=INK,
        fontsize=14,
    )
    save(fig, "symmetry-free-space-paths-3-prepared-lobes-interfere.png")


def diagram_4_point_source_factorization():
    fig, ax = canvas(
        "A point-source wave can be factored through an imaginary slice",
        "The imaginary slice factors one propagation calculation; it does not reveal hidden tracks.",
    )
    A, B = (1.0, 3.45), (11.8, 3.45)
    point(ax, A, "A")
    point(ax, B, "B")
    for r in np.linspace(1.0, 10.0, 10):
        ax.add_patch(Arc(A, 2 * r, 2 * r, theta1=-24, theta2=24, color=BLUE_LIGHT, lw=1.15, alpha=0.58, zorder=1))
    ax.text(3.2, 5.55, "one uninterrupted free wave", color=BLUE, fontsize=15, ha="center")

    slice_x = 6.4
    ax.plot([slice_x, slice_x], [0.95, 5.95], color=INK, lw=1.2, ls="--")
    ax.text(slice_x, 6.02, r"imaginary slice $\Sigma$", color=INK, fontsize=15, ha="center")
    xis = np.linspace(1.2, 5.7, 10)
    for i, yy in enumerate(xis):
        col = ORANGE if i == 6 else BLUE
        alpha = 0.95 if i == 6 else 0.24
        lw = 2.7 if i == 6 else 1.25
        ax.plot([A[0], slice_x, B[0]], [A[1], yy, B[1]], color=col, lw=lw, alpha=alpha, ls="--", zorder=4)
        ax.add_patch(Circle((slice_x, yy), 0.055, facecolor=col, edgecolor=col, alpha=alpha, zorder=6))
    ax.text(6.4, 0.62, r"$K(B,A)=\int_\Sigma K(B,\xi)K(\xi,A)\,d\xi$", fontsize=20, color=INK, ha="center")
    ax.text(
        6.4,
        0.22,
        r"Each $A\to\xi\to B$ line labels one term.  Only their sum is the propagated field.",
        fontsize=14,
        color=MUTED,
        ha="center",
    )
    save(fig, "symmetry-free-space-paths-4-point-source-factorization.png")


def phasor_chain(ax, angles, start, step, color, label, resultant_label, label_dy=0.75):
    x, y = start
    x0, y0 = x, y
    ax.text(x0, y0 + label_dy, label, fontsize=14, color=color, ha="left")
    for th in angles:
        nx = x + step * np.cos(th)
        ny = y + step * np.sin(th)
        arrow(ax, (x, y), (nx, ny), color=color, lw=1.6, alpha=0.9)
        x, y = nx, ny
    arrow(ax, (x0, y0), (x, y), color=INK, lw=3.0)
    ax.text(x + 0.15, y, resultant_label, fontsize=12, color=INK, va="center")


def candidate_curve(x0, x1, y0, amplitude, samples=500):
    x = np.linspace(x0, x1, samples)
    u = (x - x0) / (x1 - x0)
    y = y0 + amplitude * np.sin(np.pi * u)
    return x, y


def curve_length(x, y):
    return np.sum(np.hypot(np.diff(x), np.diff(y)))


def diagram_5_ray_limit():
    fig, ax = canvas(
        "Free space and the ray limit are not the same condition",
        "The relevant comparison is wavelength versus the spatial scale over which the field and geometry vary.",
    )
    ax.plot([6.4, 6.4], [0.65, 6.05], color=GRID, lw=1.5)
    ax.text(3.2, 5.85, "wavelength not small", fontsize=18, color=BLUE, ha="center")
    ax.text(9.55, 5.85, "short-wavelength limit", fontsize=18, color=GREEN, ha="center")

    amplitudes = np.linspace(-1.35, 1.35, 13)
    left_curves = [candidate_curve(0.85, 5.55, 1.35, amp * 0.42) for amp in amplitudes]
    left_lengths = np.array([curve_length(x, y) for x, y in left_curves])
    left_angles = 0.7 * (left_lengths - left_lengths[len(left_lengths) // 2])
    phasor_chain(ax, left_angles, (0.9, 3.7), 0.31, BLUE, "phase varies slowly across many contributions", "broad coherent sum")
    for x, y in left_curves:
        ax.plot(x, y, color=BLUE, alpha=0.30, lw=1.15)
    ax.text(3.2, 0.34, "wave behavior need not collapse to one ray", fontsize=14, color=INK, ha="center")

    right_curves = [candidate_curve(7.0, 12.0, 0.98, amp * 0.42) for amp in amplitudes]
    right_lengths = np.array([curve_length(x, y) for x, y in right_curves])
    right_angles = 39.4 * (right_lengths - right_lengths[len(right_lengths) // 2])
    far_mask = np.abs(amplitudes) >= 0.65
    near_mask = np.abs(amplitudes) < 0.65
    phasor_chain(ax, right_angles[far_mask], (7.05, 4.15), 0.25, BLUE, "far from stationarity: rapid phase winding", "small resultant", label_dy=0.72)
    phasor_chain(ax, right_angles[near_mask], (7.05, 2.55), 0.33, GREEN, "near the stationary route: phases align", "leading resultant", label_dy=0.68)
    for amp, (x, y) in zip(amplitudes, right_curves):
        if amp == 0:
            ax.plot(x, y, color=ORANGE, lw=3.8, zorder=5)
        else:
            ax.plot(x, y, color=GREEN if abs(amp) < 0.65 else BLUE, alpha=0.22, lw=1.05)
    ax.text(9.5, 0.28, "stationary path ≈ geometrical ray", fontsize=14, color=INK, ha="center")
    save(fig, "symmetry-free-space-paths-5-ray-limit.png")


if __name__ == "__main__":
    diagram_1_spreading_vs_same_endpoint()
    diagram_2_extended_profile()
    diagram_3_two_lobes()
    diagram_4_point_source_factorization()
    diagram_5_ray_limit()
