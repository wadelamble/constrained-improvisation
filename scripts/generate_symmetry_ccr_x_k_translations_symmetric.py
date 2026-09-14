"""Matched own-representation translations of an exact Gaussian Fourier pair.

The two panels are separate experiments from the same initial state. They are
not simultaneous Fourier views of one state after both operations.

Fourier convention: psi_tilde(k) = integral psi(x) exp(-ikx) dx / sqrt(2 pi).
With c = x0 = k0 and unit Gaussian width, the initial real parts are identical:
  psi(x)       = pi**(-1/4) exp(-(x-c)**2/2) exp(+i*c*(x-c/2))
  psi_tilde(k) = pi**(-1/4) exp(-(k-c)**2/2) exp(-i*c*(k-c/2)).

Only real parts and +/- magnitudes are plotted, with identical conventions.
Translation of each full complex profile is rigid in its own representation.
The animation parameter is displacement, not physical time.
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-ccr-x-k-translations-symmetric"
WIDTH, HEIGHT = 1440, 810
SCALE = 2
FPS = 30
SECONDS = 17.0
FRAMES = round(FPS * SECONDS)
C = 2.2
DOMAIN = (-4.0, 8.4)
SAMPLES = np.linspace(*DOMAIN, 1000)
BG = (255, 252, 246)
PANEL = (252, 248, 240)
INK = (37, 39, 42)
MUTED = (111, 106, 99)
FAINT = (222, 215, 205)
BLUE = (51, 91, 133)
GOLD = (198, 138, 45)
ENVELOPE = (205, 167, 109)
AXIS = (164, 157, 147)
PANELS = ((44, 142, 704, 634), (736, 142, 1396, 634))
BASELINE = 385
COORDINATE_AXIS = 514
AMPLITUDE = 145
ESSENTIAL_CONTENT_BOTTOM = 706
CONTROLS_SAFE_TOP = 710


def font(size: int, bold: bool = False):
    for candidate in (
        "seguisb.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(candidate, size * SCALE)
        except OSError:
            pass
    return ImageFont.load_default(size=size * SCALE)


FONTS = {size: font(size) for size in (17, 18, 21, 26)}
TITLE = font(31, True)
PANEL_TITLE = font(23, True)


def s(value):
    return round(value * SCALE)


def txt(draw, xy, value, fill=INK, size=21, anchor=None, face=None):
    draw.text(tuple(s(v) for v in xy), value, fill=fill,
              font=face or FONTS[size], anchor=anchor)


def line(draw, points, color, width=1):
    draw.line([(s(x), s(y)) for x, y in points], fill=color,
              width=s(width), joint="curve")


def profile(q, sign=1):
    """The normalized initial state in either Fourier representation."""
    q = np.asarray(q)
    return np.pi ** (-0.25) * np.exp(-0.5 * (q - C) ** 2 + sign * 1j * C * (q - C / 2))


def ramp(seconds, start, end):
    u = max(0.0, min(1.0, (seconds - start) / (end - start)))
    # Brief eased ends, nearly constant speed through most of each motion.
    e = 0.12
    if u < e:
        return u * u / (2 * e * (1 - e))
    if u > 1 - e:
        return 1 - (1 - u) ** 2 / (2 * e * (1 - e))
    return (u - e / 2) / (1 - e)


def displacement(seconds):
    if seconds < 6.5:
        return 2.0 * ramp(seconds, 1.5, 5.5)
    if seconds < 13.5:
        return 2.0 - 4.0 * ramp(seconds, 6.5, 12.5)
    return -2.0 + 2.0 * ramp(seconds, 13.5, 16.5)


def xpos(value, panel):
    lo, _, hi, _ = PANELS[panel]
    return lo + 30 + (np.asarray(value) - DOMAIN[0]) / (DOMAIN[1] - DOMAIN[0]) * (hi - lo - 60)


def arrow(draw, start, end):
    line(draw, (start, end), GOLD, 2.5)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    wings = [(end[0] - 10 * math.cos(angle + d), end[1] - 10 * math.sin(angle + d))
             for d in (-math.pi / 6, math.pi / 6)]
    draw.polygon([(s(x), s(y)) for x, y in (end, *wings)], fill=GOLD)


def make_base():
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), BG)
    draw = ImageDraw.Draw(image)
    txt(draw, (44, 27), "Translation in position and in wave number", face=TITLE)
    txt(draw, (44, 80), "Two separate translations of the same starting wave function.", fill=MUTED)
    for index, bounds in enumerate(PANELS):
        lo, top, hi, bottom = bounds
        draw.rounded_rectangle(tuple(s(v) for v in bounds), radius=s(13),
                               fill=PANEL, outline=FAINT, width=s(1))
        q, amount = (("x", "a"), ("k", "b"))[index]
        label = "Position representation" if index == 0 else "Wave-number representation"
        txt(draw, (lo + 27, top + 22), label, face=PANEL_TITLE)
        wave = "ψ" if index == 0 else "ψ̃"
        txt(draw, ((lo + hi) / 2, 224), f"{wave}({q})  →  {wave}({q} − {amount})", size=26, anchor="mm")
        line(draw, ((lo + 29, BASELINE), (hi - 28, BASELINE)), AXIS, 1)
        line(draw, ((lo + 29, COORDINATE_AXIS), (hi - 28, COORDINATE_AXIS)), FAINT, 1)
        for tick in range(-4, 9, 2):
            px = xpos(tick, index)
            line(draw, ((px, COORDINATE_AXIS - 4), (px, COORDINATE_AXIS + 4)), AXIS, 1)
            txt(draw, (px, COORDINATE_AXIS + 8), str(tick).replace("-", "−"),
                fill=MUTED, size=17, anchor="mt")
        txt(draw, (hi - 16, COORDINATE_AXIS), q, fill=MUTED, size=21, anchor="lm")
    line(draw, ((407, 667), (452, 667)), BLUE, 3)
    txt(draw, (463, 667), "real part", fill=BLUE, size=18, anchor="lm")
    line(draw, ((665, 667), (710, 667)), ENVELOPE, 1.8)
    txt(draw, (721, 667), "envelope: ±magnitude", fill=MUTED, size=18, anchor="lm")
    txt(draw, (720, 696), "The translation parameter changes; this is not time evolution.",
        fill=MUTED, size=17, anchor="mm")
    return image


BASE = None


def draw_frame(frame):
    global BASE
    if BASE is None:
        BASE = make_base()
    image = BASE.copy()
    draw = ImageDraw.Draw(image)
    shift = displacement(frame / FPS)
    for index in (0, 1):
        values = profile(SAMPLES - shift, sign=1 if index == 0 else -1)
        x_values = xpos(SAMPLES, index)
        for sign in (-1, 1):
            ys = BASELINE - sign * AMPLITUDE * np.abs(values)
            line(draw, zip(x_values, ys), ENVELOPE, 1.7)
        line(draw, zip(x_values, BASELINE - AMPLITUDE * values.real), BLUE, 3)
        start, end = float(xpos(C, index)), float(xpos(C + shift, index))
        line(draw, ((start, 564), (start, 580)), ENVELOPE, 1.5)
        if abs(end - start) > 2:
            arrow(draw, (start, 572), (end, 572))
        parameter = "a" if index == 0 else "b"
        amount = 0.0 if abs(shift) < 0.005 else shift
        value = f"{parameter} = {amount:+.2f}".replace("-", "−")
        txt(draw, ((start + end) / 2, 602), value, fill=GOLD, size=21, anchor="mm")
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def find_ffmpeg():
    configured = os.environ.get("FFMPEG_BINARY")
    if configured and Path(configured).is_file():
        return str(Path(configured))
    system = shutil.which("ffmpeg")
    if system:
        return system
    candidates = sorted((ROOT / ".tools" / "animation-python-packages" /
                         "imageio_ffmpeg" / "binaries").glob("ffmpeg*"))
    for candidate in candidates:
        if candidate.is_file() and candidate.suffix in ("", ".exe"):
            return str(candidate)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise RuntimeError("Install ffmpeg or set FFMPEG_BINARY to its executable.") from exc


def validate():
    # Independent quadrature of the Fourier transform, including its phase.
    xs = np.linspace(-12, 16, 28001)
    ks = np.linspace(-3, 8, 73)
    quadrature = np.array([np.trapezoid(profile(xs) * np.exp(-1j * k * xs), xs)
                           / np.sqrt(2 * np.pi) for k in ks])
    ft_error = float(np.max(np.abs(quadrature - profile(ks, -1))))
    norm_errors = []
    moment_errors = []
    for amount in (-2.0, 0.0, 2.0):
        for sign in (-1, 1):
            vals = profile(xs - amount, sign)
            density = abs(vals) ** 2
            norm_errors.append(abs(float(np.trapezoid(density, xs)) - 1))
            moment_errors.append(abs(float(np.trapezoid(xs * density, xs)) - C - amount))
    matched_real_error = float(np.max(abs(profile(ks).real - profile(ks, -1).real)))
    assert ft_error < 1e-10, ft_error
    assert max(norm_errors) < 1e-10, norm_errors
    assert max(moment_errors) < 1e-10, moment_errors
    assert matched_real_error < 1e-13
    assert ESSENTIAL_CONTENT_BOTTOM < CONTROLS_SAFE_TOP <= HEIGHT - 100
    print(f"Fourier quadrature max error: {ft_error:.3g}", flush=True)
    print(f"Norm max error: {max(norm_errors):.3g}; translated mean max error: {max(moment_errors):.3g}", flush=True)
    print(f"Matched real-profile max error: {matched_real_error:.3g}", flush=True)


def make_stills():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    poster = OUTPUT / f"{NAME}-poster.png"
    draw_frame(round(4.1 * FPS)).save(poster)
    draw_frame(FRAMES - 1).save(OUTPUT / f"{NAME}-final.png")
    samples = (0.5, 3.5, 5.8, 9.5, 12.8, 15.5)
    tw, th, margin, lh = 480, 270, 18, 29
    sheet = Image.new("RGB", (3 * tw + 4 * margin, 2 * (th + lh) + 3 * margin), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = FONTS[17].font_variant(size=17) if isinstance(FONTS[17], ImageFont.FreeTypeFont) else FONTS[17]
    for index, sec in enumerate(samples):
        x, y = margin + (index % 3) * (tw + margin), margin + (index // 3) * (th + lh + margin)
        sheet.paste(draw_frame(round(sec * FPS)).resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.text((x + 4, y + th + 5), f"{sec:.1f}s   a = b = {displacement(sec):+.2f}",
                  font=label_font, fill=MUTED)
    contact = OUTPUT / f"{NAME}-contact-sheet.png"
    sheet.save(contact)
    print(poster, flush=True)
    print(contact, flush=True)


def render():
    ffmpeg = find_ffmpeg()
    video = OUTPUT / f"{NAME}.mp4"
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
               "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast",
               "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in range(FRAMES):
            process.stdin.write(draw_frame(frame).tobytes())
            if frame % (FPS * 3) == 0:
                print(f"Rendered {frame}/{FRAMES} frames", flush=True)
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError("ffmpeg encoding failed")
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    # Decode one real encoded video frame for visual inspection; no frame cache.
    sample = OUTPUT / f"{NAME}-encoded-sample.png"
    subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", "9.5",
                    "-i", str(video), "-frames:v", "1", "-update", "1", str(sample)], check=True)
    report = subprocess.run([ffmpeg, "-hide_banner", "-i", str(video), "-f", "null", "-"],
                            capture_output=True, text=True, check=True)
    print(report.stderr[-1800:], flush=True)
    print(video, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stills-only", action="store_true")
    args = parser.parse_args()
    validate()
    make_stills()
    if not args.stills_only:
        render()


if __name__ == "__main__":
    main()
