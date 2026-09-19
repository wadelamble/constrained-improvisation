"""Landscape manuscript adaptation of CCR-2 Reel 11.

The complex amplitude is the exact normalized paraxial Gaussian already used
in episodes_quantum.detector_state. Its initial intensity width and propagation
distance stay fixed. Two separate, seeded preparations are compared. Dots are
independent position measurements; their vertical offsets only separate marks.

Usage (with the repository's scientific Python environment):
    python scripts/generate_symmetry_amplitude_probability.py --preview
    python scripts/generate_symmetry_amplitude_probability.py --frame 24
    python scripts/generate_symmetry_amplitude_probability.py --render

--preview writes a poster and contact sheet without encoding the full movie.
--frame writes a full-size frame at the requested time. All outputs default to
content/drafts/animations and begin with symmetry-amplitude-probability.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".tools" / "animation-python-packages"))
sys.path.insert(0, str(ROOT / "scripts" / "ccr2_reels"))

import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
from core import BG, PANEL, INK, MUTED, GRID, BLUE, GOLD, GREEN, font, equation
from episodes_quantum import detector_state

WIDTH, HEIGHT, FPS, DURATION = 1920, 1080, 30, 28.0
STEM = "symmetry-amplitude-probability"
DEFAULT_OUT = ROOT / "content" / "drafts" / "animations"
SOURCE_SIGMA, DISTANCE = 0.20, 4.0
WAVE_NUMBERS = (8.0, 160.0)
SEEDS = (73921, 73922)
SAMPLE_COUNT = 540
X_MIN, X_MAX = -5.0, 5.0
LEFT, RIGHT = 255, 1775
AMPLITUDE_BASE, AMPLITUDE_GAIN, COMPLEX_DEPTH = 354, 82, 0.30
DENSITY_BASE, DENSITY_GAIN = 770, 99
DOT_TOP, DOT_BOTTOM = 851, 926
CHECKPOINTS = (0.0, 2.0, 6.0, 12.5, 13.5, 18.0, 24.0, 27.0)


def screen_x(x):
    return LEFT + (np.asarray(x) - X_MIN) * (RIGHT - LEFT) / (X_MAX - X_MIN)


def sigma_at_detector(k):
    return math.sqrt(SOURCE_SIGMA**2 + (DISTANCE / (2*k*SOURCE_SIGMA))**2)


@lru_cache(2)
def samples(preparation):
    rng = np.random.default_rng(SEEDS[preparation])
    x = rng.normal(0, sigma_at_detector(WAVE_NUMBERS[preparation]), SAMPLE_COUNT)
    # This jitter has no physical interpretation; only horizontal position does.
    y = rng.uniform(DOT_TOP + 6, DOT_BOTTOM - 6, SAMPLE_COUNT)
    assert np.all((x > X_MIN) & (x < X_MAX)), "Expand the fixed window; do not clip samples."
    return np.column_stack((screen_x(x), y)), x


def text(draw, x, y, value, size=28, color=INK, bold=False, anchor="la"):
    draw.text((x, y), value, font=font(size, bold), fill=color, anchor=anchor)


def math_label(im, tex, x, y, size=36, color=INK, anchor="center"):
    scale = im.width / WIDTH
    pic = equation(tex, size*scale, color)
    px = x*scale if anchor == "left" else x*scale-pic.width/2
    im.paste(pic, (round(px), round(y*scale-pic.height/2)), pic)


class SmoothDraw:
    """Draw the two cached mathematical preparations at twice final resolution."""
    def __init__(self, im):
        self.draw = ImageDraw.Draw(im)

    @staticmethod
    def coords(values):
        if isinstance(values[0], (tuple, list, np.ndarray)):
            return [tuple(2*float(v) for v in point) for point in values]
        return tuple(2*float(v) for v in values)

    def text(self, position, value, font, **kwargs):
        self.draw.text(self.coords(position), value,
                       font=font.font_variant(size=font.size*2), **kwargs)

    def line(self, xy, width=1, **kwargs):
        self.draw.line(self.coords(xy), width=width*2, **kwargs)

    def polygon(self, xy, **kwargs):
        self.draw.polygon(self.coords(xy), **kwargs)

    def rounded_rectangle(self, xy, radius=0, width=1, **kwargs):
        self.draw.rounded_rectangle(self.coords(xy), radius=radius*2,
                                    width=width*2, **kwargs)


def line(draw, points, color, width=3):
    draw.line([tuple(p) for p in points], fill=color, width=width, joint="curve")


def dashed(draw, x, y0, y1, color=GRID):
    for y in range(round(y0), round(y1), 14):
        draw.line((x, y, x, min(y+6, y1)), fill=color, width=2)


def arrow(draw, start, end, color=MUTED, width=2, head=8):
    a, b = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
    line(draw, (a, b), color, width)
    unit = (b-a) / np.linalg.norm(b-a)
    normal = np.array((-unit[1], unit[0]))
    draw.polygon([tuple(b), tuple(b-head*unit+head*.45*normal),
                  tuple(b-head*unit-head*.45*normal)], fill=color)


@lru_cache(2)
def base_frame(preparation):
    """Every preparation uses identical geometric and numerical plot scales."""
    im = Image.new("RGB", (WIDTH*2, HEIGHT*2), BG)
    d = SmoothDraw(im)
    text(d, 76, 43, "Amplitude and probability", 47, INK, True)
    text(d, 78, 112, "Same Gaussian opening · same propagation distance", 27, MUTED)
    math_label(im, r"\lambda=\lambda_0" if preparation == 0 else r"\lambda=\lambda_0/20",
               1690, 94, 42, GOLD)
    d.rounded_rectangle((66, 174, 1854, 500), radius=20, fill=PANEL, outline=GRID, width=2)
    d.rounded_rectangle((66, 522, 1854, 964), radius=20, fill=PANEL, outline=GRID, width=2)
    text(d, 94, 191, "Complex amplitude at the detector", 30, INK)
    math_label(im, r"\psi(x)", 1328, 219, 33, BLUE)
    text(d, 1383, 198, "complex amplitude", 26, BLUE)
    math_label(im, r"|\psi(x)|", 1654, 219, 33, GOLD)
    text(d, 1715, 198, "magnitude", 26, GOLD)
    # A small orientation key states what the oblique complex plot represents.
    origin = (142, 365)
    arrow(d, origin, (142, 301))
    arrow(d, origin, (181, 388))
    text(d, 132, 263, "Re", 25, MUTED)
    text(d, 181, 389, "Im", 25, MUTED)
    text(d, 124, 442, "ψ(x)", 25, MUTED)

    q = np.linspace(X_MIN, X_MAX, 2600)
    z = detector_state(q, WAVE_NUMBERS[preparation], DISTANCE, SOURCE_SIGMA)
    xx = screen_x(q)
    d.line((LEFT, AMPLITUDE_BASE, RIGHT, AMPLITUDE_BASE), fill=GRID, width=2)
    dashed(d, screen_x(0), 248, 469)
    for sign in (-1, 1):
        line(d, np.column_stack((xx, AMPLITUDE_BASE + sign*AMPLITUDE_GAIN*abs(z))), GOLD, 3)
    # Fixed oblique projection of (x, Re psi, Im psi), with a fixed phase origin.
    w = z * np.exp(-.38j)
    points = np.column_stack((xx + COMPLEX_DEPTH*AMPLITUDE_GAIN*w.imag,
                              AMPLITUDE_BASE-AMPLITUDE_GAIN*w.real))
    line(d, points, BLUE, 4)
    text(d, RIGHT, 453, "position x", 25, MUTED, anchor="ra")

    text(d, 94, 542, "Probability density", 30, INK)
    math_label(im, r"\rho(x)=|\psi(x)|^2,\qquad\int\rho(x)\,dx=1",
               1410, 565, 38, GREEN)
    # Numeric density ticks make the unchanged vertical gain explicit.
    for value in (0, .5, 1, 1.5):
        py = DENSITY_BASE - DENSITY_GAIN*value
        d.line((LEFT-8, py, LEFT, py), fill=GRID, width=2)
        text(d, LEFT-20, py-17, f"{value:g}", 23, MUTED, anchor="ra")
    density = abs(z)**2
    density_points = np.column_stack((xx, DENSITY_BASE-DENSITY_GAIN*density))
    d.polygon([(LEFT, DENSITY_BASE), *[tuple(p) for p in density_points],
               (RIGHT, DENSITY_BASE)], fill="#12362f")
    dashed(d, screen_x(0), 596, DOT_BOTTOM, color="#3e5662")
    line(d, density_points, GREEN, 4)
    d.line((LEFT, DENSITY_BASE, RIGHT, DENSITY_BASE), fill=GRID, width=2)
    for value in (-4, -2, 0, 2, 4):
        px = float(screen_x(value))
        d.line((px, DENSITY_BASE, px, DENSITY_BASE+6), fill=GRID, width=2)
        text(d, px, DENSITY_BASE+8, str(value).replace("-", "−"), 23, MUTED, anchor="ma")
    text(d, RIGHT, DENSITY_BASE+8, "position x", 25, MUTED, anchor="ra")
    text(d, LEFT, 811, "Repeated position measurements", 26, MUTED)
    d.rounded_rectangle((LEFT, DOT_TOP, RIGHT, DOT_BOTTOM), radius=8,
                        fill="#07181a", outline="#284239", width=1)
    dashed(d, screen_x(0), DOT_TOP+2, DOT_BOTTOM-2, color="#284239")
    text(d, 78, 1002, "Fixed spatial, amplitude, and density scales", 26, MUTED)
    text(d, 1844, 1002, "Independent simulated detections", 26, MUTED, anchor="ra")
    return im.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def detection_count(t):
    """The first few events remain legible before the repetition rate increases."""
    preparation = int(t >= 13)
    begin = 2.0 if preparation == 0 else 15.0
    elapsed = float(np.clip(t-begin, 0, 10))
    # A slow first two seconds (one at a time), then steady accumulation.
    if elapsed <= 2:
        count = int(12*elapsed)
    else:
        count = int(24 + (SAMPLE_COUNT-24)*(elapsed-2)/8)
    return preparation, min(SAMPLE_COUNT, count)


def frame(t):
    preparation, count = detection_count(t)
    im = base_frame(preparation).copy()
    d = ImageDraw.Draw(im)
    points, _ = samples(preparation)
    for x, y in points[:count]:
        d.ellipse((x-3, y-3, x+3, y+3), fill=GREEN)
    text(d, RIGHT, 811, f"{count:3d} detections", 26, GREEN, anchor="ra")
    if 13 <= t < 15:
        status = "New preparation · shorter wavelength"
    else:
        status = f"Preparation {preparation+1} · one state, many repetitions"
    text(d, 970, 112, status, 27, MUTED, anchor="la")
    # Only the mathematical consequence is revealed; the prepared amplitude is
    # static while measurements build. No artificial global-phase animation.
    if t < 1.6:
        alpha = float(np.clip((t-.4)/1.2, 0, 1))
        region = im.crop((68, 524, 1852, 962))
        under = Image.new("RGB", region.size, PANEL)
        im.paste(Image.blend(under, region, alpha), (68, 524))
    return im


def validate_model():
    grid = np.linspace(-20, 20, 80001)
    reports = []
    for prep, k in enumerate(WAVE_NUMBERS):
        density = abs(detector_state(grid, k, DISTANCE, SOURCE_SIGMA))**2
        sigma = sigma_at_detector(k)
        reference = np.exp(-grid**2/(2*sigma*sigma))/(math.sqrt(2*math.pi)*sigma)
        norm = float(np.trapezoid(density, grid))
        variance = float(np.trapezoid(grid**2*density, grid))
        assert abs(norm-1) < 1e-12
        assert abs(variance-sigma*sigma) < 1e-12
        assert np.max(abs(density-reference)) < 1e-12
        _, positions = samples(prep)
        reports.append(dict(wave_number=k, wavelength_ratio=8/k,
                            integrated_norm=norm, integrated_variance=variance,
                            detector_sigma=sigma, seed=SEEDS[prep],
                            density_vs_sampling_pdf_max_error=float(np.max(abs(density-reference))),
                            sample_count=len(positions), sample_mean=float(positions.mean()),
                            sample_std=float(positions.std()),
                            samples_outside_display=0))
    assert not np.array_equal(samples(0)[1]/sigma_at_detector(8),
                              samples(1)[1]/sigma_at_detector(160))
    return dict(model="Exact normalized paraxial free Gaussian from accepted Reel 11",
                source_intensity_sigma=SOURCE_SIGMA, propagation_distance=DISTANCE,
                preparations=reports, samples="Independent normal draws from the exact displayed density",
                horizontal_domain=[X_MIN, X_MAX], fixed_amplitude_gain=AMPLITUDE_GAIN,
                fixed_density_gain=DENSITY_GAIN,
                complex_projection="x + 0.30 * gain * Im(psi exp(-0.38i)); y - gain * Re(psi exp(-0.38i))",
                reset_seconds=13, accumulation_intervals_seconds=[[2, 12], [15, 25]],
                dots="Each displayed point remains fixed until preparation reset; vertical jitter separates marks only",
                short_wavelength_limit="Width approaches the finite initial opening width, not a point")


def previews(out):
    frame(12.5).save(out / f"{STEM}-poster.png")
    contact_sheet([frame(t) for t in CHECKPOINTS], out)


def contact_sheet(frames, out):
    tile_w, tile_h, label_h = 640, 360, 37
    sheet = Image.new("RGB", (tile_w*2, (tile_h+label_h)*4), BG)
    d = ImageDraw.Draw(sheet)
    for i, (t, pic) in enumerate(zip(CHECKPOINTS, frames)):
        x, y = (i%2)*tile_w, (i//2)*(tile_h+label_h)
        sheet.paste(pic.resize((tile_w, tile_h), Image.Resampling.LANCZOS), (x, y))
        text(d, x+16, y+tile_h+3, f"{t:04.1f} s", 23, MUTED)
    sheet.save(out / f"{STEM}-contact-sheet.png")


def encode(out):
    output = out / f"{STEM}.mp4"
    temporary = out / f"{STEM}.rendering.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
               "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt",
               "yuv420p", "-movflags", "+faststart", "-threads", "4", str(temporary)]
    start = time.time()
    with subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        try:
            for index in range(round(DURATION*FPS)):
                proc.stdin.write(frame(index/FPS).tobytes())
                if index % 120 == 0:
                    print(f"Rendered {index}/{round(DURATION*FPS)} frames ({time.time()-start:.1f}s)", flush=True)
            proc.stdin.close()
            error = proc.stderr.read().decode("utf8", errors="replace")
            if proc.wait():
                raise RuntimeError(error)
        except BaseException:
            proc.kill()
            raise
    temporary.replace(output)
    return output


def validate_video(path):
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt="rgb24")
    metadata = next(reader)
    count = 0
    sample_frames = {}
    contact_frames = []
    checkpoint_indices = {round(t*FPS) for t in CHECKPOINTS}
    for count, data in enumerate(reader, 1):
        frame_index = count-1
        if frame_index in checkpoint_indices:
            sample_frames[str(frame_index/FPS)] = hashlib.sha256(data).hexdigest()
            pic = Image.frombytes("RGB", (WIDTH, HEIGHT), data)
            contact_frames.append(pic)
            if frame_index == 720:
                pic.save(path.parent / f"{STEM}-encoded-frame-24.00.png")
    assert metadata["size"] == (WIDTH, HEIGHT), metadata
    assert abs(metadata["fps"]-FPS) < 1e-8, metadata
    assert count == round(DURATION*FPS), count
    assert abs(metadata["duration"]-DURATION) < .01, metadata
    contact_sheet(contact_frames, path.parent)
    return dict(codec=metadata["codec"], pixel_format=metadata["pix_fmt"],
                width=WIDTH, height=HEIGHT, fps=FPS, decoded_frames=count,
                duration_seconds=metadata["duration"], bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                contact_sheet_source="Representative frames decoded from the final MP4",
                representative_decoded_frame_sha256=sample_frames)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--frame", type=float)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--verify-video", action="store_true",
                        help="Decode an existing MP4 and refresh its validation and contact sheet.")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = validate_model()
    if args.frame is not None:
        if not 0 <= args.frame <= DURATION:
            parser.error(f"--frame must be between 0 and {DURATION}")
        target = args.out_dir / f"{STEM}-frame-{args.frame:05.2f}.png"
        frame(args.frame).save(target)
        print(target)
    if args.preview or args.render:
        previews(args.out_dir)
    if args.render:
        report["video"] = validate_video(encode(args.out_dir))
    elif args.verify_video:
        report["video"] = validate_video(args.out_dir / f"{STEM}.mp4")
    report["visual_review"] = "Inspect the generated poster/contact sheet and encoded representative frames before acceptance."
    report_path = args.out_dir / f"{STEM}-validation.json"
    # A quick frame export must not discard completed encoding/review evidence.
    if "video" in report or not report_path.exists():
        report_path.write_text(json.dumps(report, indent=2)+"\n", encoding="utf8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
