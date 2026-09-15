"""Shorten the accepted schematic construction without changing its fields.

Retimes the existing MP4 as a whole: gold sums and blue components retain
their common clock. All construction stages remain; no frame interpolation,
cross-fading, field recomputation, or individual layer retiming is used.
The original 52-second movie is preserved.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / ".tools" / "animation-python-packages"
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

import imageio_ffmpeg
from PIL import Image, ImageDraw

OUT = ROOT / "content" / "drafts" / "animations"
SOURCE = OUT / "symmetry-schematic-screens-v3.mp4"
NAME = "symmetry-schematic-screens-v3-concise"
VIDEO = OUT / f"{NAME}.mp4"
FPS, DURATION = 24, 24
# Source seconds, then presentation seconds. Continuous and monotone.
KNOTS = ((0, 0), (2, 1), (22, 7), (42, 17), (48, 21), (52, 24))
SAMPLES = (0.5, 1.8, 3.0, 4.2, 5.4, 6.6, 7.9, 11.9, 15.9, 18.6, 21.5, 23.5)


def output_time(source_time):
    for (s0, t0), (s1, t1) in zip(KNOTS, KNOTS[1:]):
        if source_time <= s1:
            return t0 + (source_time - s0) * (t1 - t0) / (s1 - s0)
    raise ValueError(source_time)


def source_time(output_seconds):
    for (s0, t0), (s1, t1) in zip(KNOTS, KNOTS[1:]):
        if output_seconds <= t1:
            return s0 + (output_seconds - t0) * (s1 - s0) / (t1 - t0)
    raise ValueError(output_seconds)


def pts_expression():
    expression = ""
    for (s0, t0), (s1, t1) in reversed(list(zip(KNOTS, KNOTS[1:]))):
        part = f"({t0}+(T-{s0})*({t1}-{t0})/({s1}-{s0}))"
        expression = part if not expression else f"if(lt(T,{s1}),{part},{expression})"
    return expression + "/TB"


def main():
    source_frames, source_seconds = imageio_ffmpeg.count_frames_and_secs(str(SOURCE))
    assert source_frames == 1248 and abs(source_seconds - 52) < 0.001
    for s, t in KNOTS:
        assert abs(output_time(s) - t) < 1e-12
        assert abs(source_time(t) - s) < 1e-12

    temporary = OUT / f"{NAME}-rendering.mp4"
    expression = pts_expression()
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
        "-i", str(SOURCE), "-an", "-vf", f"setpts='{expression}',fps={FPS}",
        "-frames:v", str(FPS * DURATION), "-c:v", "libx264", "-preset", "medium",
        "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(temporary)
    ], check=True)
    temporary.replace(VIDEO)

    reader = imageio_ffmpeg.read_frames(str(VIDEO), pix_fmt="rgb24")
    metadata = next(reader)
    size = tuple(metadata["size"])
    assert size == (1280, 720) and metadata["fps"] == FPS
    wanted = {round(t * FPS): t for t in SAMPLES}
    images = {}
    count = 0
    for index, frame in enumerate(reader):
        if index in wanted:
            image = Image.frombytes("RGB", size, frame)
            images[wanted[index]] = image
        count = index + 1
    assert count == FPS * DURATION and len(images) == len(SAMPLES)

    # These are previews of the encoded deliverable, not regenerated fields.
    sheet = Image.new("RGB", (1536, 316 * math.ceil(len(SAMPLES) / 3)), (255, 252, 246))
    draw = ImageDraw.Draw(sheet)
    for index, t in enumerate(SAMPLES):
        image = images[t]
        x, y = (index % 3) * 512, (index // 3) * 316
        sheet.paste(image.resize((512, 288), Image.Resampling.LANCZOS), (x, y))
        draw.text((x + 12, y + 295), f"{t:g} s", fill=(40, 40, 40))
    sheet.save(OUT / f"{NAME}-contact-sheet.png")
    images[15.9].save(OUT / f"{NAME}-poster.png")
    images[23.5].save(OUT / f"{NAME}-final.png")

    # At the fastest portion, output frames advance at most four original
    # frames: < 0.35 rad of the common three-second wave cycle, well below pi.
    frame_indices = [round(source_time(i / FPS) * FPS) for i in range(count)]
    maximum_step = max(b - a for a, b in zip(frame_indices, frame_indices[1:]))
    phase_step = maximum_step * 2 * math.pi / (3 * FPS)
    assert min(b - a for a, b in zip(frame_indices, frame_indices[1:])) >= 1
    assert phase_step < math.pi
    report = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "video": str(VIDEO.relative_to(ROOT)),
        "video_sha256": hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
        "source_seconds": source_seconds, "seconds": count / FPS,
        "decoded_frames": count, "fps": FPS, "size": size,
        "source_output_time_knots": KNOTS,
        "first_screen_seconds": output_time(2),
        "second_screen_seconds": output_time(22),
        "fifteen_screens_seconds": output_time(38),
        "open_slices_seconds": output_time(48),
        "maximum_source_frame_step": maximum_step,
        "maximum_common_phase_step_radians": phase_step,
        "method": "whole-frame monotone retiming; no interpolated pictures; original preserved",
        "encoded_samples": SAMPLES,
    }
    (OUT / f"{NAME}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
