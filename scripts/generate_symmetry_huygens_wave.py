"""Huygens' construction as a coherent red/blue wave field.

This is a new standalone asset; earlier screen/slit animations are preserved.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

from huygens_construction_model import (HuygensModel, FieldSampler, WIDTH, HEIGHT, FPS,
    BOX, DURATION, X_MAX, VIEW_HALF_HEIGHT, CONSTRUCTION_X, ELEMENT_CENTERS,
    coefficients_at, label_at, selection_caption_at, temporal_phase, construction_visibility,
    tracked_front_x, tracking_visibility)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-huygens-wave"
POSITIVE = np.asarray((255.0, 42.0, 91.0))
NEGATIVE = np.asarray((37.0, 137.0, 255.0))
NEUTRAL = np.asarray((3.0, 3.0, 8.0))
INK = (249, 239, 229)
MUTED = (159, 150, 169)
ELEMENT = (255, 211, 148)
SAMPLES = (1.5, 5.0, 9.5, 14.5, 18.7, 21.8, 25.5, 29.5, 35.0, 39.5)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def world_to_pixel(x, y):
    return (BOX[0] + x / X_MAX * (BOX[2] - BOX[0]),
            (BOX[1] + BOX[3]) / 2 - y / (2 * VIEW_HALF_HEIGHT) * (BOX[3] - BOX[1]))


class Renderer:
    def __init__(self):
        self.model = HuygensModel()
        self.sampler = FieldSampler(self.model)

    def frame(self, seconds, phase_seconds=None):
        selection = coefficients_at(seconds)
        field = self.sampler.sample(selection)
        clock = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        real = np.clip(np.real(field * clock), -1.0, 1.0)
        strength = np.abs(real) ** 0.72
        target = np.where((real >= 0)[..., None], POSITIVE, NEGATIVE)
        rgb = NEUTRAL + (target - NEUTRAL) * strength[..., None]
        wave = Image.fromarray(np.clip(rgb[::-1], 0, 255).astype(np.uint8))
        wave = wave.resize((BOX[2]-BOX[0], BOX[3]-BOX[1]), Image.Resampling.BICUBIC)
        image = Image.new("RGB", (WIDTH, HEIGHT), tuple(NEUTRAL.astype(int)))
        image.paste(wave, BOX[:2])
        draw = ImageDraw.Draw(image, "RGBA")

        visibility = construction_visibility(seconds)
        if visibility > 0:
            for center, coefficient in zip(ELEMENT_CENTERS, selection):
                x, y = world_to_pixel(CONSTRUCTION_X, float(center))
                alpha = visibility * (75 + 180 * float(coefficient))
                if coefficient > 0:
                    r = 7.0
                    draw.ellipse((x-r, y-r, x+r, y+r),
                                 fill=(*ELEMENT, round(22 * visibility * coefficient)))
                r = 2.5 + 0.7 * coefficient
                draw.ellipse((x-r, y-r, x+r, y+r), fill=(*ELEMENT, round(alpha)))

        tracking = tracking_visibility(seconds)
        if tracking > 0:
            x, _ = world_to_pixel(tracked_front_x(seconds), 0)
            fill = (*INK, round(230 * tracking))
            draw.polygon(((x-5, BOX[1]-9), (x+5, BOX[1]-9), (x, BOX[1]-2)), fill=fill)
            draw.polygon(((x-5, BOX[3]+9), (x+5, BOX[3]+9), (x, BOX[3]+2)), fill=fill)

        draw.text((40, 27), label_at(seconds), fill=INK, font=font(28, True))
        draw.text((1240, 33), "Huygens’ construction", fill=MUTED, font=font(20), anchor="ra")
        draw.text((40, 691), "positive", fill=tuple(POSITIVE.astype(int)), font=font(15))
        draw.text((125, 691), "negative", fill=tuple(NEGATIVE.astype(int)), font=font(15))
        draw.text((1240, 691), selection_caption_at(seconds), fill=MUTED, font=font(15), anchor="ra")
        return image


def previews(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    contact = Image.new("RGB", (1536, 1264), (18, 18, 22))
    draw = ImageDraw.Draw(contact)
    for index, seconds in enumerate(SAMPLES):
        frame = renderer.frame(seconds)
        frame.save(OUT / f"{NAME}-check-{seconds:g}.png")
        x, y = (index % 3)*512, (index // 3)*316
        contact.paste(frame.resize((512, 288)), (x, y))
        draw.text((x+12, y+291), f"{seconds:g} s", fill=INK, font=font(17))
    contact.save(OUT / f"{NAME}-contact-sheet.png")
    renderer.frame(38.0).save(OUT / f"{NAME}-final.png")
    renderer.frame(0.0, phase_seconds=0.0).save(OUT / f"{NAME}-baseline-phase.png")
    renderer.frame(32.0, phase_seconds=0.0).save(OUT / f"{NAME}-reconstructed-phase.png")
    print(json.dumps({"contact_sheet":str(OUT / f"{NAME}-contact-sheet.png")}), flush=True)


def render(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(DURATION * FPS)):
        process.stdin.write(renderer.frame(index / FPS).tobytes())
        if index % (FPS * 4) == 0:
            print(f"{index/FPS:.0f}/{DURATION:g}s; elapsed {time.perf_counter()-start:.1f}s", flush=True)
    process.stdin.close()
    error = process.stderr.read().decode(errors="replace")
    if process.wait():
        raise RuntimeError(error)
    print(json.dumps({"video":str(output), "bytes":output.stat().st_size}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    renderer = Renderer()
    if args.preview or not args.render:
        previews(renderer)
    if args.render:
        render(renderer)


if __name__ == "__main__":
    main()
