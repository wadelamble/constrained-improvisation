from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from generate_symmetry_phase_advance_packet_animation import (
    FFMPEG,
    FPS,
    OUTPUT_DIR,
    scene_xk_loop,
)
from _make_contact_sheets import make_contact_sheet


NAME = "symmetry-ccr-loop-global-phase"
DURATION_SECONDS = 7.0


def render() -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{NAME}_frames"
    video = OUTPUT_DIR / f"{NAME}.mp4"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()

    frame_count = round(DURATION_SECONDS * FPS)
    try:
        for index in range(frame_count):
            progress = index / max(1, frame_count - 1)
            scene_xk_loop(progress, orientation=-1.0, phase_symbol="φ").save(
                scratch / f"frame_{index:04d}.png"
            )

        subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            check=True,
        )
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)

    contact_sheet = make_contact_sheet(video.name)
    return video, contact_sheet


if __name__ == "__main__":
    rendered_video, rendered_sheet = render()
    print(rendered_video)
    print(rendered_sheet)
