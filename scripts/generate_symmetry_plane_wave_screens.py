"""Standalone wave-field animation in the confirmed red/blue reel style."""
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
from plane_wave_screens_model import (WaveScreensModel, FieldSampler, SCREEN_X, X_MAX,
                                     DURATION, label_at, FPS, temporal_phase, state_at, ease)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-plane-wave-screens"
WIDTH, HEIGHT = 1280, 720
BOX = (40, 80, 1240, 680)
POSITIVE = np.array((255.0, 42.0, 91.0))
NEGATIVE = np.array((37.0, 137.0, 255.0))
NEUTRAL = np.array((3.0, 3.0, 8.0))
INK, MUTED = (245, 237, 232), (168, 160, 177)
SAMPLES = (2.0, 8.5, 13.0, 18.0, 23.0, 29.0, 33.0, 37.0, 41.0, 44.0, 48.0)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


class Renderer:
    def __init__(self):
        self.model = WaveScreensModel()
        self.sampler = FieldSampler(self.model)
        self.cache = {}
        self.transition_cache = {}

    def complex_field(self, seconds):
        a, b, amount = state_at(seconds)
        masks = self.model.masks_at(seconds)
        if a == b:
            if a not in self.cache:
                self.cache[a] = self.sampler.sample(masks)
            return masks, self.cache[a]
        key = (a, b)
        if key not in self.transition_cache:
            changed = np.max(np.abs(self.model.targets[a] - self.model.targets[b]), axis=1) > 1e-12
            degree = int(np.count_nonzero(changed))
            # Every changing transmission mask is linear in amount. The field
            # is therefore a polynomial of at most this degree, even after
            # propagation through multiple screens. This evaluates that exact
            # polynomial, rather than blending a pair of unrelated fields.
            nodes = (1.0 - np.cos(np.pi * np.arange(degree + 1) / degree)) / 2.0
            weights = (-1.0) ** np.arange(degree + 1)
            weights[[0, -1]] *= 0.5
            values = []
            for node in nodes:
                state = self.model.targets[a] + node * (self.model.targets[b] - self.model.targets[a])
                values.append(self.sampler.sample(state))
            self.transition_cache[key] = (nodes, weights, values)
        nodes, weights, values = self.transition_cache[key]
        exact = np.flatnonzero(np.abs(nodes - amount) < 1e-14)
        if len(exact):
            return masks, values[int(exact[0])]
        factors = weights / (amount - nodes)
        factors /= factors.sum()
        result = np.zeros_like(values[0])
        for factor, value in zip(factors, values):
            result += factor * value
        return masks, result

    def frame(self, seconds, phase_seconds=None):
        masks, field = self.complex_field(seconds)
        phase_factor = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        real = np.clip(np.real(field * phase_factor), -1.0, 1.0)
        strength = np.abs(real) ** 0.72
        target = np.where((real >= 0)[..., None], POSITIVE, NEGATIVE)
        rgb = NEUTRAL + (target - NEUTRAL) * strength[..., None]
        wave = Image.fromarray(np.clip(rgb[::-1], 0, 255).astype(np.uint8))
        wave = wave.resize((BOX[2] - BOX[0], BOX[3] - BOX[1]), Image.Resampling.BICUBIC)
        image = Image.new("RGB", (WIDTH, HEIGHT), tuple(NEUTRAL.astype(int)))
        image.paste(wave, BOX[:2])
        draw = ImageDraw.Draw(image, "RGBA")
        a, b, amount = state_at(seconds)
        active_a = np.max(1.0 - self.model.targets[a], axis=1) > 1e-8
        active_b = np.max(1.0 - self.model.targets[b], axis=1) > 1e-8
        active_visibility = active_a.astype(float) + amount * (active_b.astype(float) - active_a)
        for position, mask in zip(SCREEN_X, masks):
            x = BOX[0] + position / X_MAX * (BOX[2] - BOX[0])
            opacity = np.clip(1.0 - mask[self.sampler.indices], 0, 1)[::-1]
            for row in range(BOX[3] - BOX[1]):
                index = min(len(opacity) - 1, round(row / (BOX[3] - BOX[1] - 1) * (len(opacity) - 1)))
                alpha = round(245 * float(opacity[index]))
                if alpha > 0:
                    draw.line((x, BOX[1] + row, x + 3, BOX[1] + row), fill=(*INK, alpha), width=1)
        for position, visibility in zip(SCREEN_X, active_visibility):
            x = BOX[0] + position / X_MAX * (BOX[2] - BOX[0])
            if visibility > 0:
                for y in (BOX[1] - 7, BOX[3] + 7):
                    draw.line((x - 4, y, x + 4, y), fill=(*INK, round(170 * visibility)), width=2)
        # Physical masks have reached identity before these optional slice marks appear.
        imaginary = ease((seconds - 46.0) / 1.5)
        if imaginary > 0:
            for position in SCREEN_X:
                x = BOX[0] + position / X_MAX * (BOX[2] - BOX[0])
                for y in range(BOX[1], BOX[3], 20):
                    draw.line((x, y, x, y + 7), fill=(205, 202, 214, round(50 * imaginary)), width=1)
        draw.text((40, 27), label_at(seconds), font=font(28, True), fill=INK)
        draw.text((1240, 33), "Plane-wave illumination", font=font(20), fill=MUTED, anchor="ra")
        draw.text((40, 691), "positive", font=font(15), fill=tuple(POSITIVE.astype(int)))
        draw.text((125, 691), "negative", font=font(15), fill=tuple(NEGATIVE.astype(int)))
        draw.text((1240, 691), "real wave amplitude", font=font(15), fill=MUTED, anchor="ra")
        return image


def previews(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    frames = []
    for seconds in SAMPLES:
        frame = renderer.frame(seconds)
        frame.save(OUT / f"{NAME}-check-{seconds:g}.png")
        thumb = frame.resize((512, 288))
        frames.append((seconds, thumb))
    contact = Image.new("RGB", (1536, 4 * 316), (17, 17, 21))
    draw = ImageDraw.Draw(contact)
    for index, (seconds, thumb) in enumerate(frames):
        x, y = (index % 3) * 512, (index // 3) * 316
        contact.paste(thumb, (x, y))
        draw.text((x + 12, y + 291), f"{seconds:g} s", fill=INK, font=font(17))
    contact.save(OUT / f"{NAME}-contact-sheet.png")
    renderer.frame(50.0).save(OUT / f"{NAME}-final.png")
    # Equal clock phase makes recovery directly comparable, independent of playback time.
    renderer.frame(0.0, phase_seconds=0.0).save(OUT / f"{NAME}-baseline-phase.png")
    renderer.frame(46.0, phase_seconds=0.0).save(OUT / f"{NAME}-recovered-phase.png")
    print(json.dumps({"contact_sheet": str(OUT / f"{NAME}-contact-sheet.png")}), flush=True)


def render(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-nostats", "-f", "rawvideo", "-vcodec", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
               "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(DURATION * FPS)):
        process.stdin.write(renderer.frame(index / FPS).tobytes())
        if index % (FPS * 4) == 0:
            print(f"{index / FPS:.0f}/{DURATION:g} seconds; elapsed {time.perf_counter()-start:.1f}s", flush=True)
    process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace")
    return_code = process.wait()
    if return_code:
        raise RuntimeError(stderr)
    print(json.dumps({"video": str(path), "bytes": path.stat().st_size}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    renderer = Renderer()
    if args.preview or not args.render:
        previews(renderer)
    if args.render:
        render(renderer)


if __name__ == "__main__":
    main()
