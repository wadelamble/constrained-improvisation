from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle


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
    from PIL import Image, ImageDraw

    thumbs = [Image.open(path).convert("RGB").resize((420, 252)) for path in frame_paths]
    margin = 28
    title_h = 42
    sheet = Image.new("RGB", (3 * 420 + 4 * margin, 2 * 252 + 3 * margin + title_h), "#F7F3EC")
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 16), "Huygens principle: secondary wavelets build the next plane wavefront", fill="#2F2F2F")
    for idx, thumb in enumerate(thumbs):
        row, col = divmod(idx, 3)
        x = margin + col * (420 + margin)
        y = title_h + margin + row * (252 + margin)
        sheet.paste(thumb, (x, y))
        draw.rectangle([x, y, x + 420, y + 252], outline="#C9BCAA", width=2)
    sheet.save(output)
    for thumb in thumbs:
        thumb.close()


def make_animation(video_path: Path, contact_path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / "_huygens_transverse_wave_frames"
    scratch.mkdir(exist_ok=True)

    frames = 120
    cycles = 3
    advance = 1.8
    x0 = 1.2
    y_points = np.linspace(-2.1, 2.1, 9)

    fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
    fig.patch.set_facecolor("#F7F3EC")
    ax.set_facecolor("#FFFDF8")
    ax.set_xlim(0.0, 8.2)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    ax.text(
        0.5,
        1.03,
        "Huygens principle for a plane wavefront",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=16,
        color="#2F2F2F",
        weight="bold",
    )
    ax.text(0.06, 0.91, "wavefront at t", transform=ax.transAxes, fontsize=12, color="#7A7066")
    ax.text(0.68, 0.91, "envelope = wavefront at t + dt", transform=ax.transAxes, fontsize=12, color="#245E91")

    old_line, = ax.plot([], [], color="#AFA79A", lw=3.0, zorder=2)
    envelope_line, = ax.plot([], [], color="#245E91", lw=3.2, zorder=6)
    prior_lines = [
        ax.plot([], [], color="#AFA79A", lw=1.5, alpha=0.35, zorder=1)[0]
        for _ in range(cycles)
    ]
    future_lines = [
        ax.plot([], [], color="#245E91", lw=1.6, alpha=0.0, zorder=5)[0]
        for _ in range(cycles)
    ]
    message = ax.text(0.06, 0.08, "", transform=ax.transAxes, fontsize=13, color="#B85C38")
    ax.annotate(
        "",
        xy=(6.7, 0.0),
        xytext=(5.5, 0.0),
        arrowprops=dict(arrowstyle="->", color="#5B7F72", lw=2.0),
        zorder=8,
    )
    ax.text(5.55, 0.22, "motion", fontsize=12, color="#5B7F72")

    center_points = ax.scatter([], [], s=18, color="#2F2F2F", zorder=6)
    wavelets = [
        Circle((0, 0), 0.0, fill=False, edgecolor="#B85C38", lw=1.4, alpha=0.0, zorder=3)
        for _ in y_points
    ]
    for circle in wavelets:
        ax.add_patch(circle)

    sample_frame_indices = [0, 16, 36, 56, 76, 104]
    sample_paths: list[Path] = []

    def update(frame: int):
        progress = (frame % frames) / frames * cycles
        step = min(cycles - 1, int(progress))
        phase = progress - step
        front_x = x0 + step * advance
        radius = advance * phase
        envelope_x = front_x + radius

        y_min, y_max = -2.45, 2.45
        old_line.set_data([front_x, front_x], [y_min, y_max])
        old_line.set_alpha(1.0 - 0.35 * phase)
        envelope_line.set_data([envelope_x, envelope_x], [y_min, y_max])
        envelope_line.set_alpha(0.15 + 0.85 * phase)

        for idx, line in enumerate(prior_lines):
            px = x0 + idx * advance
            if idx < step:
                line.set_data([px, px], [y_min, y_max])
                line.set_alpha(0.25)
            else:
                line.set_data([], [])
                line.set_alpha(0.0)

        for idx, line in enumerate(future_lines):
            px = x0 + (idx + 1) * advance
            if idx == step:
                line.set_data([px, px], [y_min, y_max])
                line.set_alpha(0.15 + 0.45 * phase)
            else:
                line.set_data([], [])
                line.set_alpha(0.0)

        if phase < 0.28:
            message.set_text("points on the wavefront emit circular wavelets")
        elif phase < 0.82:
            message.set_text("the wavelets expand outward")
        else:
            message.set_text("their common envelope is the next parallel wavefront")

        centers_x = np.full_like(y_points, front_x)
        center_points.set_offsets(np.column_stack([centers_x, y_points]))
        center_points.set_alpha(1.0 - 0.25 * phase)
        for cy, circle in zip(y_points, wavelets):
            circle.center = (front_x, cy)
            circle.radius = radius
            circle.set_alpha(0.85 if phase > 0.03 else 0.0)

        return [
            old_line,
            envelope_line,
            *prior_lines,
            *future_lines,
            message,
            center_points,
            *wavelets,
        ]

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / 24, blit=True)
    save_animation(anim, video_path, fps=24)

    for frame in sample_frame_indices:
        update(frame)
        path = scratch / f"huygens_transverse_{frame:03d}.png"
        fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.12)
        sample_paths.append(path)
    make_contact_sheet(sample_paths, contact_path)
    plt.close(fig)


if __name__ == "__main__":
    make_animation(
        OUTPUT_DIR / "lm-huygens-transverse-wave.mp4",
        OUTPUT_DIR / "lm-huygens-transverse-wave-contact-sheet.png",
    )
