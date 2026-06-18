from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Arc
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"


def save_animation(anim: FuncAnimation, path: Path, fps: int = 24) -> None:
    writer = FFMpegWriter(
        fps=fps,
        bitrate=2600,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p"],
    )
    anim.save(path, writer=writer)


def smoothstep(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3.0 - 2.0 * x)


def line_points(point: np.ndarray, direction: np.ndarray, keep_above: bool | None) -> tuple[np.ndarray, np.ndarray]:
    s = np.linspace(-5.0, 5.0, 500)
    pts = point[:, None] + direction[:, None] * s
    if keep_above is None:
        return pts[0], pts[1]
    mask = pts[1] >= 0 if keep_above else pts[1] <= 0
    return np.ma.masked_where(~mask, pts[0]), np.ma.masked_where(~mask, pts[1])


def draw_line(
    ax: plt.Axes,
    point: np.ndarray,
    direction: np.ndarray,
    *,
    keep_above: bool | None,
    color: str,
    lw: float,
    alpha: float,
    zorder: int,
    linestyle: str = "-",
) -> None:
    x, y = line_points(point, direction, keep_above)
    ax.plot(x, y, color=color, linewidth=lw, alpha=alpha, zorder=zorder, linestyle=linestyle)


def forward_arc(
    center: np.ndarray,
    radius: float,
    normal: np.ndarray,
    tangent: np.ndarray,
    *,
    keep_above: bool | None,
) -> tuple[np.ndarray, np.ndarray]:
    phi = np.linspace(-np.pi / 2, np.pi / 2, 180)
    pts = center[:, None] + radius * (normal[:, None] * np.cos(phi)[None, :] + tangent[:, None] * np.sin(phi)[None, :])
    if keep_above is None:
        return pts[0], pts[1]
    mask = pts[1] >= 0 if keep_above else pts[1] <= 0
    return np.ma.masked_where(~mask, pts[0]), np.ma.masked_where(~mask, pts[1])


def draw_angle(ax: plt.Axes, center: np.ndarray, radius: float, theta1: float, theta2: float, label: str, xy: tuple[float, float]) -> None:
    ax.add_patch(Arc(center, 2 * radius, 2 * radius, theta1=theta1, theta2=theta2, color="#7E4B3A", linewidth=1.35, zorder=12))
    ax.text(xy[0], xy[1], label, fontsize=11, color="#7E4B3A", zorder=12)


def make_contact_sheet(frame_paths: list[Path], output: Path) -> None:
    thumbs = [Image.open(path).convert("RGB").resize((420, 276)) for path in frame_paths]
    margin = 28
    title_h = 40
    sheet = Image.new("RGB", (3 * 420 + 4 * margin, 2 * 276 + 3 * margin + title_h), "#F7F3EC")
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 14), "Huygens construction of Snell's law", fill="#2F2F2F")
    for idx, thumb in enumerate(thumbs):
        row, col = divmod(idx, 3)
        x = margin + col * (420 + margin)
        y = title_h + margin + row * (276 + margin)
        sheet.paste(thumb, (x, y))
        draw.rectangle([x, y, x + 420, y + 276], outline="#C9BCAA", width=2)
    sheet.save(output)
    for thumb in thumbs:
        thumb.close()


def make_animation(video_path: Path, contact_path: Path) -> None:
    theta_inc = np.deg2rad(50.0)
    v1 = 1.0
    v2 = 0.58
    theta_ref = np.arcsin((v2 / v1) * np.sin(theta_inc))

    A = np.array([-1.25, 0.0])
    B = np.array([1.28, 0.0])
    dx = B[0] - A[0]

    d1 = np.array([np.sin(theta_inc), -np.cos(theta_inc)])
    w1 = np.array([np.cos(theta_inc), np.sin(theta_inc)])
    d2 = np.array([np.sin(theta_ref), -np.cos(theta_ref)])
    w2 = np.array([np.cos(theta_ref), np.sin(theta_ref)])

    v1dt = dx * np.sin(theta_inc)
    v2dt = dx * np.sin(theta_ref)
    T = B + np.dot(A - B, w2) * w2
    C = A + 2.05 * w1
    C2 = C + v1dt * d1

    frames = 144
    sample_indices = [0, 24, 48, 72, 100, 134]
    scratch = OUTPUT_DIR / "_huygens_snell_readable_frames"
    scratch.mkdir(exist_ok=True)
    sample_paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(10.8, 6.2), dpi=150)
    fig.patch.set_facecolor("#F7F3EC")

    def setup() -> None:
        ax.set_facecolor("#FFFDF8")
        ax.set_xlim(-3.10, 3.20)
        ax.set_ylim(-2.25, 2.28)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#C9BCAA")
            spine.set_linewidth(1.2)
        ax.axhspan(0, 2.4, color="#FFFDF8", zorder=0)
        ax.axhspan(-2.4, 0, color="#E8F2F7", zorder=0)
        ax.axhline(0, color="#7E7468", linewidth=1.5, zorder=3)
        ax.text(-2.92, 2.02, "Huygens construction of Snell's law", fontsize=13, color="#2F2F2F", weight="bold")
        ax.text(-2.92, 0.12, "fast medium", fontsize=10, color="#4B463F")
        ax.text(-2.92, -0.33, "slow medium", fontsize=10, color="#4B463F")

    def draw_frame(frame: int) -> None:
        ax.clear()
        setup()

        t = frame / (frames - 1)
        p = smoothstep(t / 0.62)
        reveal = smoothstep((t - 0.56) / 0.22)
        formula = smoothstep((t - 0.76) / 0.16)

        hit = A + p * (B - A)
        r_blue = p * v1dt
        r_orange = p * v2dt

        # Old and moving incoming blue wavefronts.
        draw_line(ax, A, w1, keep_above=True, color="#355070", lw=1.7, alpha=0.26, zorder=2)
        draw_line(ax, hit, w1, keep_above=True, color="#355070", lw=2.8, alpha=0.90, zorder=7)
        ax.text(-2.55, 1.34, "old and advancing blue wavefronts", fontsize=9.7, color="#355070")

        # Blue Huygens wavelets: old front generates the advancing blue front.
        for u in [0.85, 1.45, 2.05]:
            center = A + u * w1
            x, y = forward_arc(center, r_blue, d1, w1, keep_above=True)
            ax.plot(x, y, color="#355070", linewidth=1.0, alpha=0.24, zorder=4)
            ax.scatter([center[0]], [center[1]], s=16, color="#355070", alpha=0.46, zorder=5)

        # Orange wavelet from the first boundary point.
        if r_orange > 0.02:
            phi = np.linspace(np.pi, 2 * np.pi, 240)
            ax.plot(A[0] + r_orange * np.cos(phi), A[1] + r_orange * np.sin(phi), color="#B85C38", linewidth=2.4, alpha=0.92, zorder=6)

        # Final refracted wavefront: tangent from B to the orange wavelet.
        if reveal > 0:
            draw_line(ax, B, w2, keep_above=False, color="#B85C38", lw=3.0, alpha=0.92 * reveal, zorder=8)
            ax.scatter([T[0]], [T[1]], s=34, color="#B85C38", edgecolor="white", linewidth=0.6, alpha=reveal, zorder=10)
            ax.text(1.18, -0.86, "tangent orange wavefront", fontsize=9.8, color="#B85C38", alpha=reveal)

        # Construction distances.
        if formula > 0:
            ax.annotate("", xy=C2, xytext=C, arrowprops={"arrowstyle": "<->", "color": "#355070", "linewidth": 1.8, "alpha": formula}, zorder=12)
            ax.text(C2[0] - 0.40, C2[1] + 0.13, r"$v_1\Delta t$", fontsize=11, color="#355070", alpha=formula)
            ax.plot([A[0], T[0]], [A[1], T[1]], color="#B85C38", linewidth=1.8, alpha=formula, zorder=10)
            ax.text(T[0] - 0.20, T[1] - 0.20, r"$v_2\Delta t$", fontsize=11, color="#B85C38", alpha=formula)

        # Rays perpendicular to wavefronts.
        if reveal > 0.55:
            ax.annotate("", xy=B, xytext=B - 1.58 * d1, arrowprops={"arrowstyle": "->", "color": "#355070", "linewidth": 2.1}, zorder=11)
            ax.annotate("", xy=B + 1.55 * d2, xytext=B, arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 2.1}, zorder=11)
            ax.plot([B[0], B[0]], [-1.05, 1.05], color="#BDB4A7", linewidth=1.0, linestyle="--", zorder=4)
            draw_angle(ax, B, 0.42, 90, 90 + np.rad2deg(theta_inc), r"$\theta_1$", (B[0] - 0.62, 0.42))
            draw_angle(ax, B, 0.54, 270 - np.rad2deg(theta_ref), 270, r"$\theta_2$", (B[0] + 0.13, -0.73))

        ax.scatter([A[0], B[0]], [0, 0], s=58, color="#2F2F2F", edgecolor="white", linewidth=0.8, zorder=13)
        ax.text(A[0] - 0.12, 0.15, "A", fontsize=13, color="#2F2F2F", weight="bold")
        ax.text(B[0] + 0.05, 0.15, "B", fontsize=13, color="#2F2F2F", weight="bold")
        ax.plot([A[0], B[0]], [0, 0], color="#2F2F2F", linewidth=1.0, alpha=0.32, zorder=4)
        ax.text((A[0] + B[0]) / 2 - 0.18, 0.10, r"$\Delta x$", fontsize=11, color="#4B463F")

        if formula < 1:
            ax.text(-2.62, -1.90, "In the same time, blue wavelets advance farther than orange wavelets.", fontsize=10.2, color="#4B463F")
        else:
            ax.text(
                -2.72,
                -1.96,
                r"$v_1\Delta t=\Delta x\sin\theta_1$" + "\n" + r"$v_2\Delta t=\Delta x\sin\theta_2$" + "\n" + r"$\sin\theta_1/v_1=\sin\theta_2/v_2$",
                fontsize=11.4,
                color="#2F2F2F",
                bbox={"boxstyle": "round,pad=0.30", "fc": "#FFFDF8", "ec": "#D7C6AA"},
            )

    def update(frame: int):
        draw_frame(frame)
        return []

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / 24, blit=False)
    video_path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, video_path, fps=24)

    for idx in sample_indices:
        draw_frame(idx)
        frame_path = scratch / f"huygens-snell-readable-{idx:03d}.png"
        fig.savefig(frame_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.10)
        sample_paths.append(frame_path)
    make_contact_sheet(sample_paths, contact_path)
    plt.close(fig)


if __name__ == "__main__":
    make_animation(
        OUTPUT_DIR / "lm-fermat-snell-huygens.mp4",
        OUTPUT_DIR / "lm-fermat-snell-huygens-contact-sheet.png",
    )
