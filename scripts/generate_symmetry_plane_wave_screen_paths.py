"""Representative path view of the shared plane-wave screen calculation.

The drawn routes are a stable, finite selection of crossing sequences. They
are not the finite sample used to calculate the result: the result sums the
entire shared transverse grid by normalized angular-spectrum propagation.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import itertools
import json
import math
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
from plane_wave_screens_model import (WaveScreensModel, SCREEN_X, X_MAX,
    VIEW_HALF_HEIGHT, DURATION, LABELS, FPS, ENDPOINT_X, ENDPOINT_Y, K,
    TRANSITIONS, temporal_phase, state_at, label_at, ease)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-plane-wave-screen-paths"
WIDTH, HEIGHT, SCALE = 1280, 720, 2
BOX = (40, 80, 1240, 680)
BG = (3, 3, 8)
INK, MUTED = (245, 237, 232), (168, 160, 177)
BLUE, GOLD, GREEN = (74, 128, 181), (222, 171, 70), (89, 196, 149)
POSITIVE, NEGATIVE = (255, 42, 91), (37, 137, 255)
SAMPLES = (2.0, 8.5, 13.0, 18.0, 23.0, 29.0, 33.0, 37.0, 41.0, 44.0, 48.0)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, round(size * SCALE))
        except OSError:
            pass
    return ImageFont.load_default()


def px(x, y):
    return (SCALE * (BOX[0] + x / X_MAX * (BOX[2] - BOX[0])),
            SCALE * ((BOX[1] + BOX[3]) / 2 - y / (2 * VIEW_HALF_HEIGHT) * (BOX[3] - BOX[1])))


def text(draw, xy, value, size=17, color=INK, bold=False, anchor=None):
    draw.text(tuple(SCALE * v for v in xy), value, font=font(size, bold), fill=color, anchor=anchor)


def arrow(draw, start, end, color, width=2.5, head=6):
    start, end = np.asarray(start) * SCALE, np.asarray(end) * SCALE
    draw.line([tuple(start), tuple(end)], fill=color, width=round(width * SCALE))
    delta = end - start
    length = np.linalg.norm(delta)
    if length < 1:
        return
    unit = delta / length
    normal = np.array((-unit[1], unit[0]))
    h = min(head * SCALE, length * .55)
    draw.polygon([tuple(end), tuple(end - h * unit + .43 * h * normal),
                  tuple(end - h * unit - .43 * h * normal)], fill=color)


class Renderer:
    def __init__(self):
        self.model = WaveScreensModel()
        self.visible = np.flatnonzero(np.abs(self.model.y) <= VIEW_HALF_HEIGHT)
        self.b_index = int(np.argmin(np.abs(self.model.y - ENDPOINT_Y)))
        self.xnodes = np.r_[0.0, SCREEN_X, ENDPOINT_X]
        self.banks = {stage: self.route_bank(stage) for stage in range(len(LABELS))}
        self.cache = {}
        self.spatial_cache = {}
        self.screen_row_indices = np.rint(np.linspace(0, len(self.visible)-1,
            SCALE*(BOX[3]-BOX[1]))).astype(int)
        changes = np.r_[0, np.flatnonzero(np.diff(self.screen_row_indices))+1,
                        len(self.screen_row_indices)]
        self.screen_runs = tuple((int(begin), int(end), int(self.screen_row_indices[begin]))
                                 for begin, end in zip(changes[:-1], changes[1:]))
        impulse = np.zeros(self.model.n, complex)
        impulse[0] = 1
        self.last_kernel = self.model.propagate(impulse, ENDPOINT_X - SCREEN_X[-1])
        self.last_row = self.last_kernel[(self.b_index - np.arange(self.model.n)) % self.model.n]

    def route_bank(self, stage, count=72):
        """Fixed representative sequences; no frame-wise random resampling."""
        masks = self.model.targets[stage]
        active = np.flatnonzero(np.min(masks, axis=1) < 1 - 1e-12)
        if stage == 5:
            active = np.array([0])
        if stage == 9:
            active = np.arange(len(SCREEN_X))
        source = np.linspace(-3.35, 3.35, count)
        routes = []
        for r, sy in enumerate(source):
            xs, ys = [0.0], [sy]
            for p in active:
                candidates = np.flatnonzero((np.abs(self.model.y) <= 3.25) & (masks[p] > .1))
                # Small coherent bends keep dense chains readable. The same
                # deterministic parameter controls all nodes of one route.
                target = sy * (1 - SCREEN_X[p] / X_MAX)
                target += .74 * math.sin((r + .5) * 2.399963 + p * .72)
                j = candidates[np.argmin(np.abs(self.model.y[candidates] - target))]
                xs.append(float(SCREEN_X[p]))
                ys.append(float(self.model.y[j]))
            xs.append(ENDPOINT_X)
            ys.append(ENDPOINT_Y)
            crossings = np.interp(self.xnodes, xs, ys)
            indices = np.rint(crossings / self.model.dy + self.model.n // 2).astype(int)
            indices = np.clip(indices, 0, self.model.n - 1)
            routes.append(indices)
        # The central representative passes through the central opening on all
        # planes. Its color identifies a route, not an extra physical ray weight.
        routes.append(np.full(len(self.xnodes), self.model.n // 2, int))
        return np.asarray(routes)

    def quantities(self, seconds):
        a, b, amount = state_at(seconds)
        masks = self.model.masks_at(seconds)
        if a == b and a in self.cache:
            return masks, self.cache[a]
        fields = self.model.screen_fields(masks)
        output = self.model.propagate(fields[-1], ENDPOINT_X - SCREEN_X[-1])
        # Each term here groups every earlier source/screen choice by its last
        # crossing. There is no omitted complex prefactor or post-hoc rotation.
        groups = self.last_row * fields[-1]
        result = (output, complex(np.sum(groups)))
        if a == b:
            self.cache[a] = result
        return masks, result

    def draw_routes(self, draw, bank, masks, opacity):
        if opacity <= 0:
            return
        for r, indices in enumerate(bank):
            # Screen suppression is physical transmission, not interference.
            transmission = float(np.prod(masks[np.arange(len(SCREEN_X)), indices[1:-1]]))
            alpha = round((205 if r == len(bank) - 1 else 145) * opacity * transmission)
            if alpha <= 0:
                continue
            color = GOLD if r == len(bank) - 1 else BLUE
            points = [px(x, y) for x, y in zip(self.xnodes, self.model.y[indices])]
            draw.line(points, fill=(*color, alpha), width=round((1.8 if r == len(bank)-1 else 1.0) * SCALE), joint="curve")

    def draw_screens(self, draw, masks, seconds):
        a, b, amount = state_at(seconds)
        active_a = np.min(self.model.targets[a], axis=1) < 1 - 1e-12
        active_b = np.min(self.model.targets[b], axis=1) < 1 - 1e-12
        visibility = active_a.astype(float) * (1 - amount) + active_b.astype(float) * amount
        for p, (position, mask) in enumerate(zip(SCREEN_X, masks)):
            x = px(position, 0)[0]
            for tick_y in (73, 687):
                draw.line((x-4*SCALE, tick_y*SCALE, x+4*SCALE, tick_y*SCALE),
                          fill=(*INK, round(170*visibility[p])), width=2*SCALE)
            opacity = np.clip(1.0 - mask[self.visible], 0, 1)[::-1]
            for begin, end, index in self.screen_runs:
                alpha = round(245 * float(opacity[index]))
                if alpha:
                    draw.rectangle((x, SCALE*BOX[1]+begin, x+3*SCALE, SCALE*BOX[1]+end-1),
                                   fill=(*INK, alpha))
        imaginary = ease((seconds - 46) / 1.5)
        if imaginary:
            for position in SCREEN_X:
                x = px(position, 0)[0]
                for y in range(BOX[1], BOX[3], 20):
                    draw.line((x, y*SCALE, x, (y+7)*SCALE), fill=(205, 202, 214, round(50*imaginary)), width=SCALE)

    def frame(self, seconds, phase_seconds=None):
        masks, (output, resultant) = self.quantities(seconds)
        clock = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        a, b, amount = state_at(seconds)
        cache_key = a if a == b and not (46 <= seconds < 47.5) else None
        if cache_key is not None and cache_key in self.spatial_cache:
            image = self.spatial_cache[cache_key].copy()
        else:
            image = Image.new("RGB", (WIDTH*SCALE, HEIGHT*SCALE), BG)
            draw = ImageDraw.Draw(image, "RGBA")
            self.draw_routes(draw, self.banks[a], masks, 1 - amount)
            if a != b:
                self.draw_routes(draw, self.banks[b], masks, amount)
            self.draw_screens(draw, masks, seconds)
            if cache_key is not None:
                self.spatial_cache[cache_key] = image.copy()
        draw = ImageDraw.Draw(image, "RGBA")

        # The right-edge strip is the exact output field, with the wave film's
        # signed red/blue palette, clock and fixed amplitude transfer curve.
        amplitude = np.real(output[self.visible][::-1] * clock)
        for row in range(SCALE * (BOX[3]-BOX[1])):
            index = min(len(amplitude)-1, round(row / (SCALE*(BOX[3]-BOX[1])-1) * (len(amplitude)-1)))
            value = float(amplitude[index])
            strength = min(1.0, abs(value)) ** .72
            target = POSITIVE if value >= 0 else NEGATIVE
            color = tuple(round(BG[i] + (target[i]-BG[i]) * strength) for i in range(3))
            draw.line((SCALE*(BOX[2]-5), SCALE*BOX[1]+row, SCALE*BOX[2], SCALE*BOX[1]+row), fill=color, width=1)
        # Incident points share exactly the same initial phase and amplitude.
        source_value = clock.real
        target = POSITIVE if source_value >= 0 else NEGATIVE
        strength = abs(source_value) ** .72
        source_color = tuple(round(BG[i] + (target[i]-BG[i]) * strength) for i in range(3))
        draw.line((BOX[0]*SCALE, BOX[1]*SCALE, BOX[0]*SCALE, BOX[3]*SCALE), fill=source_color, width=4*SCALE)

        bx, by = px(ENDPOINT_X, ENDPOINT_Y)
        draw.ellipse((bx-4*SCALE, by-4*SCALE, bx+4*SCALE, by+4*SCALE), fill=GREEN)
        text(draw, (1254, 380), "B", size=20, color=GREEN, anchor="lm")
        text(draw, (40, 27), label_at(seconds), size=28, bold=True)
        text(draw, (1240, 33), "Paths to B", size=20, color=MUTED, anchor="ra")
        # A unit circle fixes the scale of the exact complex sum at every stage.
        center, radius = (922, 41), 25
        draw.ellipse(tuple(SCALE*v for v in (center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius)), outline=(64, 66, 72), width=SCALE)
        z = resultant * clock
        arrow(draw, center, (center[0]+radius*z.real, center[1]-radius*z.imag), GREEN)
        text(draw, (877, 40), "sum at B", size=17, color=GREEN, anchor="rm")
        text(draw, (40, 691), "Representative paths · equal-phase input plane", size=15, color=MUTED)
        text(draw, (1240, 691), "Full sum from the shared wave calculation", size=15, color=MUTED, anchor="ra")
        return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def checks(renderer):
    max_error = 0.0
    sample_times = sorted(set(SAMPLES + tuple((a+b)/2 for a,b,_ in TRANSITIONS)))
    for seconds in sample_times:
        masks, (_, grouped_sum) = renderer.quantities(seconds)
        direct = renderer.model.field_at(ENDPOINT_X, masks)[renderer.b_index]
        max_error = max(max_error, float(abs(direct - grouped_sum)))
    # Explicit expansion over every source and three intermediate coordinates
    # independently checks matrix-element normalization and multiplication.
    small = WaveScreensModel(n=7, period=4.0)
    positions = (1.2, 2.8, 4.1, 5.9)
    masks = np.array([[1,.2,.7,1,.7,.2,1], [.3,1,.2,1,.2,1,.3], [1,.4,1,.5,1,.4,1]])
    impulse = np.zeros(small.n, complex)
    impulse[0] = 1
    distances = np.diff(np.r_[0, positions])
    matrices = []
    for distance in distances:
        kernel = small.propagate(impulse, distance)
        matrices.append(kernel[(np.arange(small.n)[:,None] - np.arange(small.n)[None,:]) % small.n])
    total = 0j
    endpoint = 3
    for source, p, q, r in itertools.product(range(small.n), repeat=4):
        total += (matrices[3][endpoint,r] * masks[2,r] * matrices[2][r,q]
                  * masks[1,q] * matrices[1][q,p] * masks[0,p] * matrices[0][p,source])
    field = np.ones(small.n, complex)
    for i, distance in enumerate(distances):
        field = small.propagate(field, distance)
        if i < len(masks):
            field *= masks[i]
    expansion_error = float(abs(total - field[endpoint]))
    plane_error = max(float(abs(renderer.quantities(t)[1][1] - np.exp(1j*K*ENDPOINT_X))) for t in (0, 46, 50))
    assert max_error < 1e-12 and expansion_error < 1e-12 and plane_error < 1e-12
    result = {"grouped_sum_vs_wave_endpoint_max_error": max_error,
              "explicit_2401_path_expansion_error": expansion_error,
              "open_plane_absolute_complex_phase_error": plane_error,
              "fps": FPS, "duration": DURATION, "frames": round(FPS*DURATION),
              "box": BOX, "endpoint": [ENDPOINT_X, ENDPOINT_Y],
              "source": "unit amplitude and equal phase over the entire transverse domain"}
    print(json.dumps(result, indent=2), flush=True)
    return result


def previews(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1536, 4*316), (17, 17, 21))
    for index, seconds in enumerate(SAMPLES):
        frame = renderer.frame(seconds)
        frame.save(OUT / f"{NAME}-check-{seconds:g}.png")
        x, y = index%3*512, index//3*316
        sheet.paste(frame.resize((512,288)), (x,y))
        draw = ImageDraw.Draw(sheet)
        draw.text((x+12,y+291), f"{seconds:g} s", fill=INK)
    sheet.save(OUT / f"{NAME}-contact-sheet.png")
    renderer.frame(50).save(OUT / f"{NAME}-final.png")
    print(str(OUT / f"{NAME}-contact-sheet.png"), flush=True)


def render(renderer):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-nostats", "-f", "rawvideo", "-vcodec", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
               "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(DURATION*FPS)):
        process.stdin.write(renderer.frame(index/FPS).tobytes())
        if index % (FPS*4) == 0:
            print(f"{index/FPS:.0f}/{DURATION:g} seconds; elapsed {time.perf_counter()-start:.1f}s", flush=True)
    process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace")
    if process.wait():
        raise RuntimeError(stderr)
    print(json.dumps({"video": str(path), "bytes": path.stat().st_size}), flush=True)


def qa():
    """Decode the finished movie and save compact grids of encoded frames."""
    path = OUT / f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(path),
               "-vf", f"select=not(mod(n\\,{FPS//2})),scale=320:180", "-fps_mode", "vfr",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    assert not result.stderr, result.stderr.decode("utf-8", errors="replace")
    frame_size = 320*180*3
    assert len(result.stdout) == round(DURATION*2)*frame_size
    directory = ROOT / ".tools" / "plane-wave-paths-qa"
    directory.mkdir(parents=True, exist_ok=True)
    frames = np.frombuffer(result.stdout, np.uint8).reshape((-1,180,320,3))
    for page, start in enumerate(range(0, len(frames), 16), 1):
        sheet = Image.new("RGB", (1280, 816), (17,17,21))
        draw = ImageDraw.Draw(sheet)
        for slot, frame in enumerate(frames[start:start+16]):
            x, y = slot%4*320, slot//4*204
            sheet.paste(Image.fromarray(frame), (x,y))
            draw.text((x+9,y+184), f"{(start+slot)/2:g} s", fill=INK)
        sheet.save(directory / f"motion-{page:02d}.png")
    print(json.dumps({"decoded_samples": len(frames), "qa_directory": str(directory)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--qa", action="store_true")
    args = parser.parse_args()
    renderer = Renderer()
    if args.check:
        checks(renderer)
    if args.preview or not (args.check or args.render or args.qa):
        previews(renderer)
    if args.render:
        render(renderer)
    if args.qa:
        qa()


if __name__ == "__main__":
    main()
