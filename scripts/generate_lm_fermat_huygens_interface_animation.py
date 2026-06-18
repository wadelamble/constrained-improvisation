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


def smoothstep(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def clipped_line(point: np.ndarray, direction: np.ndarray, keep_above: bool | None) -> tuple[np.ndarray, np.ndarray]:
    s = np.linspace(-5.0, 5.0, 500)
    pts = point[:, None] + direction[:, None] * s
    if keep_above is None:
        return pts[0], pts[1]
    mask = pts[1] >= 0 if keep_above else pts[1] <= 0
    return np.ma.masked_where(~mask, pts[0]), np.ma.masked_where(~mask, pts[1])


def draw_line(ax: plt.Axes, point: np.ndarray, direction: np.ndarray, *, keep_above: bool | None, color: str, lw: float, alpha: float, zorder: int) -> None:
    x, y = clipped_line(point, direction, keep_above)
    ax.plot(x, y, color=color, linewidth=lw, alpha=alpha, zorder=zorder)


def draw_angle(ax: plt.Axes, center: np.ndarray, radius: float, theta_a: float, theta_b: float, label: str, label_xy: tuple[float, float]) -> None:
    arc = Arc(center, 2 * radius, 2 * radius, theta1=theta_a, theta2=theta_b, color="#7E4B3A", linewidth=1.4, zorder=10)
    ax.add_patch(arc)
    ax.text(label_xy[0], label_xy[1], label, fontsize=11, color="#7E4B3A", zorder=10)


def make_animation(video_path: Path, contact_path: Path) -> None:
    theta1 = np.deg2rad(50.0)
    v1 = 1.0
    v2 = 0.58
    theta2 = np.arcsin((v2 / v1) * np.sin(theta1))

    A = np.array([-1.25, 0.0])
    B = np.array([1.28, 0.0])
    dx = B[0] - A[0]
    v1dt = dx * np.sin(theta1)
    v2dt = dx * np.sin(theta2)

    incident_ray = np.array([np.sin(theta1), -np.cos(theta1)])
    incident_front = np.array([np.cos(theta1), np.sin(theta1)])
    refracted_ray = np.array([np.sin(theta2), -np.cos(theta2)])
    refracted_front = np.array([np.cos(theta2), np.sin(theta2)])

    final_incoming_front_point = B
    foot_from_a = final_incoming_front_point + np.dot(A - final_incoming_front_point, incident_front) * incident_front
    tangent_point = B + np.dot(A - B, refracted_front) * refracted_front

    frames = 132
    sample_indices = [0, 20, 42, 66, 92, 126]
    scratch = OUTPUT_DIR / "_huygens_snell_frames"
    scratch.mkdir(exist_ok=True)
    sample_paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(10.8, 6.2), dpi=150)
    fig.patch.set_facecolor("#F7F3EC")

    def setup_axis() -> None:
        ax.set_facecolor("#FFFDF8")
        ax.set_xlim(-3.05, 3.20)
        ax.set_ylim(-2.25, 2.28)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#C9BCAA")
            spine.set_linewidth(1.2)
        ax.axhspan(0, 2.55, color="#FFFDF8", zorder=0)
        ax.axhspan(-2.55, 0, color="#E8F2F7", zorder=0)
        ax.axhline(0, color="#7E7468", linewidth=1.5, zorder=3)
        ax.text(-2.90, 2.02, "Huygens construction of Snell's law", fontsize=13, color="#2F2F2F", weight="bold")
        ax.text(-2.90, 0.12, "fast medium", fontsize=10, color="#4B463F")
        ax.text(-2.90, -0.33, "slow medium", fontsize=10, color="#4B463F")

    def draw_frame(frame: int) -> None:
        ax.clear()
        setup_axis()

        t = frame / (frames - 1)
        front_p = smoothstep(t / 0.62)
        tangent_alpha = smoothstep((t - 0.50) / 0.22)
        rays_alpha = smoothstep((t - 0.67) / 0.18)
        formula_alpha = smoothstep((t - 0.78) / 0.16)

        hit = A + front_p * (B - A)
        radius = front_p * v2dt

        # Initial and moving incoming wavefronts.
        draw_line(ax, A, incident_front, keep_above=True, color="#355070", lw=1.5, alpha=0.22, zorder=2)
        draw_line(ax, hit, incident_front, keep_above=True, color="#355070", lw=2.8, alpha=0.92, zorder=6)
        ax.text(-2.55, 1.35, "incoming wavefront", fontsize=10, color="#355070")

        # Construction points.
        ax.scatter([A[0], B[0]], [A[1], B[1]], s=58, color="#2F2F2F", edgecolor="white", linewidth=0.8, zorder=9)
        ax.text(A[0] - 0.12, 0.15, "A", fontsize=13, color="#2F2F2F", weight="bold")
        ax.text(B[0] + 0.05, 0.15, "B", fontsize=13, color="#2F2F2F", weight="bold")
        ax.plot([A[0], B[0]], [0, 0], color="#2F2F2F", linewidth=1.0, alpha=0.32, zorder=4)
        ax.text((A[0] + B[0]) / 2 - 0.18, 0.10, r"$\Delta x$", fontsize=11, color="#4B463F")

        if front_p < 0.98:
            ax.scatter([hit[0]], [hit[1]], s=38, color="#355070", edgecolor="white", linewidth=0.7, zorder=10)

        # A emits a wavelet into the lower medium while the incoming front advances to B.
        if radius > 0.04:
            phi = np.linspace(np.pi, 2 * np.pi, 240)
            ax.plot(A[0] + radius * np.cos(phi), A[1] + radius * np.sin(phi), color="#B85C38", linewidth=2.5, alpha=0.92, zorder=6)
            current_tangent_point = B + np.dot(A - B, refracted_front) * refracted_front
            partial = A + front_p * (current_tangent_point - A)
            ax.plot([A[0], partial[0]], [A[1], partial[1]], color="#B85C38", linewidth=1.2, alpha=0.45, zorder=5)
            ax.text(A[0] - 0.34, -1.18, r"$v_2\Delta t$", fontsize=11, color="#B85C38")

        # The final tangent is the refracted wavefront.
        if tangent_alpha > 0:
            draw_line(ax, B, refracted_front, keep_above=False, color="#B85C38", lw=3.0, alpha=0.92 * tangent_alpha, zorder=7)
            ax.scatter([tangent_point[0]], [tangent_point[1]], s=36, color="#B85C38", edgecolor="white", linewidth=0.6, alpha=tangent_alpha, zorder=10)
            ax.text(1.35, -0.86, "tangent wavefront", fontsize=10, color="#B85C38", alpha=tangent_alpha)

        # Distances that make the Snell relation readable.
        if formula_alpha > 0:
            ax.plot([A[0], foot_from_a[0]], [A[1], foot_from_a[1]], color="#355070", linewidth=1.8, alpha=formula_alpha, zorder=8)
            ax.text(foot_from_a[0] - 0.36, foot_from_a[1] + 0.12, r"$v_1\Delta t$", fontsize=11, color="#355070", alpha=formula_alpha)
            ax.plot([A[0], tangent_point[0]], [A[1], tangent_point[1]], color="#B85C38", linewidth=1.8, alpha=formula_alpha, zorder=8)

        # Rays are perpendicular to wavefronts.
        if rays_alpha > 0:
            ax.annotate("", xy=B, xytext=B - 1.55 * incident_ray, arrowprops={"arrowstyle": "->", "color": "#355070", "linewidth": 2.1, "alpha": rays_alpha}, zorder=10)
            ax.annotate("", xy=B + 1.55 * refracted_ray, xytext=B, arrowprops={"arrowstyle": "->", "color": "#B85C38", "linewidth": 2.1, "alpha": rays_alpha}, zorder=10)
            ax.plot([B[0], B[0]], [-1.05, 1.05], color="#BDB4A7", linewidth=1.0, linestyle="--", alpha=rays_alpha, zorder=4)
            draw_angle(ax, B, 0.42, 90, 90 + np.rad2deg(theta1), r"$\theta_1$", (B[0] - 0.62, 0.42))
            draw_angle(ax, B, 0.52, 270 - np.rad2deg(theta2), 270, r"$\theta_2$", (B[0] + 0.14, -0.72))

        if formula_alpha < 1:
            ax.text(-2.64, -1.88, "A emits a wavelet while the incoming wavefront advances to B.", fontsize=10.2, color="#4B463F")
        else:
            ax.text(
                -2.70,
                -1.92,
                r"$v_1\Delta t=\Delta x\sin\theta_1$" + "\n" + r"$v_2\Delta t=\Delta x\sin\theta_2$" + "\n" + r"$\sin\theta_1/v_1=\sin\theta_2/v_2$",
                fontsize=11.5,
                color="#2F2F2F",
                bbox={"boxstyle": "round,pad=0.30", "fc": "#FFFDF8", "ec": "#D7C6AA"},
            )

    def update(frame: int):
        draw_frame(frame)
        return []

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / 24, blit=False)
    video_path.parent.mkdir(parents=True, exist_ok=True)
    save_animation(anim, video_path, fps=24)

    for index in sample_indices:
        draw_frame(index)
        frame_path = scratch / f"huygens-snell-{index:03d}.png"
        fig.savefig(frame_path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.10)
        sample_paths.append(frame_path)
    make_contact_sheet(sample_paths, contact_path)
    plt.close(fig)


if __name__ == "__main__":
    make_animation(
        OUTPUT_DIR / "lm-fermat-snell-huygens-interface.mp4",
        OUTPUT_DIR / "lm-fermat-snell-huygens-interface-contact-sheet.png",
    )
