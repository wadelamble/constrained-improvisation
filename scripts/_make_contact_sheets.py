from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ANIMATION_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffmpeg.exe"
FFPROBE = ROOT / ".tools" / "micromamba-anim-root" / "envs" / "anim" / "Library" / "bin" / "ffprobe.exe"
SCRATCH_DIR = ANIMATION_DIR / "_contact_sheet_frames"

CONTACT_SHEET_FILES = [
    "liouville-permutation-3card.mp4",
    "liouville-contours-quartic.mp4",
    "differential-spring-ensemble-transport.mp4",
    "differential-incompressible-fluid-patch.mp4",
    "differential-function-to-flow.mp4",
    "differential-symplectic-patch-preservation.mp4",
]


def video_duration(path: Path) -> float:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def extract_frame(video: Path, timestamp: float, output: Path) -> None:
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-vf",
            "scale=720:-1",
            str(output),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


def fit_on_canvas(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = image.convert("RGB")
    image.thumbnail((size[0] - 20, size[1] - 36), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "white")
    canvas.paste(image, ((size[0] - image.width) // 2, 12))
    return canvas


def make_contact_sheet(video_name: str) -> Path:
    video = ANIMATION_DIR / video_name
    if not video.exists():
        raise FileNotFoundError(video)

    SCRATCH_DIR.mkdir(exist_ok=True)

    duration = video_duration(video)
    fractions = [0.0, 0.25, 0.5, 0.75, 0.95]
    frame_size = (420, 300)
    frames: list[Image.Image] = []

    for index, fraction in enumerate(fractions):
        timestamp = min(duration - 0.05, max(0.0, duration * fraction))
        frame_path = SCRATCH_DIR / f"{video.stem}-{index}.png"
        extract_frame(video, timestamp, frame_path)
        frame = fit_on_canvas(Image.open(frame_path), frame_size)
        draw = ImageDraw.Draw(frame)
        draw.text((14, frame_size[1] - 22), f"{fraction:.0%}", fill=(80, 80, 80))
        frames.append(frame)

    sheet = Image.new("RGB", (frame_size[0] * len(frames), frame_size[1]), "#F4F4F4")
    for index, frame in enumerate(frames):
        sheet.paste(frame, (frame_size[0] * index, 0))

    output = ANIMATION_DIR / f"{video.stem}-contact-sheet.png"
    sheet.save(output)
    return output


def main() -> None:
    try:
        for video_name in CONTACT_SHEET_FILES:
            print(make_contact_sheet(video_name))
    finally:
        if SCRATCH_DIR.exists():
            shutil.rmtree(SCRATCH_DIR)


if __name__ == "__main__":
    main()
