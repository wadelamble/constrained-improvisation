from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

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
        }
    )


def save_animation(anim: FuncAnimation, path: Path, fps: int = 18) -> None:
    writer = FFMpegWriter(fps=fps, bitrate=2400, codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
    anim.save(path, writer=writer)


def polygon_area(points: np.ndarray) -> float:
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def segment_length(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(b - a))


def rotation(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]])


def euclidean_transform(points: np.ndarray, s: float) -> np.ndarray:
    theta = 1.15 * s
    shift = np.array([1.6 * s, 0.55 * math.sin(math.pi * s)])
    return (points @ rotation(theta).T) + shift


def symplectic_transform(points: np.ndarray, s: float) -> np.ndarray:
    k = 1.8 * s
    a = 1.15 * s
    b = 0.45 * math.sin(math.pi * s)
    q = points[:, 0]
    p = points[:, 1]
    return np.column_stack([q + k * p + a, p + b])


def make_euclidean_animation(path: Path) -> None:
    patch = np.array([[-1.0, -0.6], [1.0, -0.6], [1.0, 0.6], [-1.0, 0.6]])
    a0 = np.array([-0.75, -0.25])
    b0 = np.array([0.55, 0.35])
    base_length = segment_length(a0, b0)
    base_area = polygon_area(patch)

    fig, ax = plt.subplots(figsize=(7.4, 6.0))
    frames = 96

    def draw_frame(frame: int) -> None:
        ax.clear()
        s = frame / (frames - 1)
        cur_patch = euclidean_transform(patch, s)
        cur_a = euclidean_transform(a0[None, :], s)[0]
        cur_b = euclidean_transform(b0[None, :], s)[0]
        cur_length = segment_length(cur_a, cur_b)
        cur_area = polygon_area(cur_patch)

        # Initial reference.
        closed = np.vstack([patch, patch[0]])
        ax.plot(closed[:, 0], closed[:, 1], linestyle="--", color="#B3B3B3", linewidth=1.4, zorder=1)

        # Current transformed patch.
        closed_cur = np.vstack([cur_patch, cur_patch[0]])
        ax.fill(cur_patch[:, 0], cur_patch[:, 1], color="#4C78A8", alpha=0.18, zorder=2)
        ax.plot(closed_cur[:, 0], closed_cur[:, 1], color="#4C78A8", linewidth=2.0, zorder=3)

        # Highlight a distance-preserved segment.
        ax.plot([cur_a[0], cur_b[0]], [cur_a[1], cur_b[1]], color="#F58518", linewidth=2.7, zorder=4)
        ax.scatter([cur_a[0], cur_b[0]], [cur_a[1], cur_b[1]], color="#F58518", s=30, zorder=5)
        mid = 0.5 * (cur_a + cur_b)
        ax.text(mid[0], mid[1] + 0.16, f"distance = {cur_length:.2f}", color="#F58518", ha="center")

        ax.text(0.02, 1.03, "Euclidean rigid motion", transform=ax.transAxes, ha="left", va="bottom", fontsize=12)
        ax.text(
            0.02,
            0.98,
            r"$(Q,P)=R_\theta(q,p)+(a,b)$",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#555555",
        )
        ax.text(
            0.02,
            0.92,
            f"segment length preserved: {cur_length:.2f} = {base_length:.2f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#333333",
        )
        ax.text(
            0.02,
            0.87,
            f"patch area preserved: {cur_area:.2f} = {base_area:.2f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#333333",
        )

        ax.set_title("Metric geometry preserves distance under the allowed transforms", pad=18)
        ax.set_xlabel("q-like coordinate")
        ax.set_ylabel("p-like coordinate")
        ax.set_xlim(-1.7, 3.0)
        ax.set_ylim(-1.8, 2.0)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(color="#E8E8E8", linewidth=0.8)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path)
    plt.close(fig)


def make_symplectic_animation(path: Path) -> None:
    patch = np.array([[-1.0, -0.55], [1.0, -0.55], [1.0, 0.55], [-1.0, 0.55]])
    a0 = np.array([0.0, -0.55])
    b0 = np.array([0.0, 0.55])
    base_length = segment_length(a0, b0)
    base_area = polygon_area(patch)

    fig, ax = plt.subplots(figsize=(7.4, 6.0))
    frames = 96

    def draw_frame(frame: int) -> None:
        ax.clear()
        s = frame / (frames - 1)
        cur_patch = symplectic_transform(patch, s)
        cur_a = symplectic_transform(a0[None, :], s)[0]
        cur_b = symplectic_transform(b0[None, :], s)[0]
        cur_length = segment_length(cur_a, cur_b)
        cur_area = polygon_area(cur_patch)

        closed = np.vstack([patch, patch[0]])
        ax.plot(closed[:, 0], closed[:, 1], linestyle="--", color="#B3B3B3", linewidth=1.4, zorder=1)

        closed_cur = np.vstack([cur_patch, cur_patch[0]])
        ax.fill(cur_patch[:, 0], cur_patch[:, 1], color="#54A24B", alpha=0.18, zorder=2)
        ax.plot(closed_cur[:, 0], closed_cur[:, 1], color="#54A24B", linewidth=2.0, zorder=3)

        ax.plot([cur_a[0], cur_b[0]], [cur_a[1], cur_b[1]], color="#E45756", linewidth=2.7, zorder=4)
        ax.scatter([cur_a[0], cur_b[0]], [cur_a[1], cur_b[1]], color="#E45756", s=30, zorder=5)
        mid = 0.5 * (cur_a + cur_b)
        ax.text(mid[0] + 0.2, mid[1] + 0.18, f"distance = {cur_length:.2f}", color="#E45756", ha="left")

        ax.text(0.02, 1.03, "Symplectic transformation", transform=ax.transAxes, ha="left", va="bottom", fontsize=12)
        ax.text(
            0.02,
            0.98,
            r"$(Q,P)=(q+k p + a,\; p+b)$",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#555555",
        )
        ax.text(
            0.02,
            0.92,
            f"area preserved: {cur_area:.2f} = {base_area:.2f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#333333",
        )
        ax.text(
            0.02,
            0.87,
            f"distance changes: {cur_length:.2f} \u2260 {base_length:.2f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            color="#333333",
        )

        ax.set_title("Symplectic geometry preserves area, not distance", pad=18)
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.set_xlim(-1.8, 3.1)
        ax.set_ylim(-1.5, 1.7)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(color="#E8E8E8", linewidth=0.8)

    anim = FuncAnimation(fig, draw_frame, frames=frames, interval=1000 / 18, blit=False)
    save_animation(anim, path)
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_style()
    make_euclidean_animation(OUTPUT_DIR / "euclidean-rigid-motion-distance.mp4")
    make_symplectic_animation(OUTPUT_DIR / "symplectic-canonical-area.mp4")


if __name__ == "__main__":
    main()
