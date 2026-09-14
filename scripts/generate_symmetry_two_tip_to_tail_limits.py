"""Two evolving Fresnel sums: increasing distance and decreasing wavelength.

Uniform plane-wave illumination of one finite opening [-a,a], on-axis B.
Each arrow is an integrated aperture element of the normalized 1D Fresnel
propagator. The unobstructed plane wave exp(ikz) is the phase reference at B;
its magnitude is one. No resultant-dependent rotation or amplitude rescaling.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
for package_folder in ("animation-python-packages", "tip-to-tail-corrected-python-packages"):
    location = ROOT / ".tools" / package_folder
    if location.is_dir():
        sys.path.insert(0, str(location))

import numpy as np
from scipy.special import fresnel
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-two-tip-to-tail-limits"
WIDTH, HEIGHT, SUPERSAMPLE = 1440, 840, 2
FPS, DURATION = 30, 26.0
BEGIN, FINISH = 1.5, 23.5
F_START, F_LEFT_END, F_RIGHT_END = 2.0, 0.05, 24.0
ELEMENTS = 256
EDGES = np.linspace(-1.0, 1.0, ELEMENTS + 1)
FINE_EDGES = np.linspace(-1.0, 1.0, 4097)
BG, PANEL = (253, 250, 244), (250, 247, 240)
INK, MUTED, BORDER = (37, 38, 40), (111, 108, 102), (218, 211, 200)
BLUE, GOLD = (43, 93, 145), (192, 128, 25)
AXIS = (217, 214, 207)
PANELS = ((28, 108, 704, 754), (736, 108, 1412, 754))
PIXELS_PER_UNIT = 355.0
SAMPLES = (0, 1.5, 5, 9, 13, 17, 21, 23.5, 25.5)


def cumulative(f_number, edges=EDGES):
    """Integral from the lower aperture edge to each supplied edge, / exp(ikz)."""
    s, c = fresnel(np.sqrt(2.0 * f_number) * np.asarray(edges))
    s0, c0 = fresnel(-np.sqrt(2.0 * f_number))
    return np.exp(-0.25j * np.pi) / np.sqrt(2.0) * ((c - c0) + 1j * (s - s0))


def progress(seconds):
    raw = float(np.clip((seconds - BEGIN) / (FINISH - BEGIN), 0, 1))
    # A short velocity ramp only at either end; the long middle is linear.
    ramp = 0.035
    if raw < ramp:
        return raw * raw / (2 * ramp * (1 - ramp))
    if raw > 1 - ramp:
        return 1 - (1 - raw) ** 2 / (2 * ramp * (1 - ramp))
    return (raw - ramp / 2) / (1 - ramp)


def state(seconds):
    p = progress(seconds)
    return (F_START * (F_LEFT_END / F_START) ** p,
            F_START + (F_RIGHT_END - F_START) * p)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, round(size * SUPERSAMPLE))
        except OSError:
            pass
    return ImageFont.load_default()


def pixels(values):
    return tuple(round(value * SUPERSAMPLE) for value in values)


def text(draw, xy, value, size=20, fill=INK, bold=False, anchor=None):
    draw.text(pixels(xy), value, font=font(size, bold), fill=fill, anchor=anchor)


def line(draw, first, last, fill, width=1):
    draw.line(pixels((*first, *last)), fill=fill, width=max(1, round(width * SUPERSAMPLE)))


def arrow(draw, first, last, fill, width=1.5, head=5):
    length = math.dist(first, last)
    if length < 0.05:
        return
    line(draw, first, last, fill, width)
    head = min(head, length * 0.62)
    angle = math.atan2(last[1] - first[1], last[0] - first[0])
    points = [last] + [(last[0] - head * math.cos(angle + turn),
                       last[1] - head * math.sin(angle + turn)) for turn in (-0.5, 0.5)]
    draw.polygon([pixels(point) for point in points], fill=fill)


def mapper(panel):
    # Identical fixed scale and placement relative to the two panel boundaries.
    origin = (panel[0] + 144, 407)
    return lambda z: (origin[0] + PIXELS_PER_UNIT * z.real,
                      origin[1] - PIXELS_PER_UNIT * z.imag)


def draw_chain(draw, panel, f_number):
    point = mapper(panel)
    origin = point(0j)
    xmin, xmax = panel[0] + 33, panel[2] - 32
    ymin, ymax = 249, 660
    line(draw, (xmin, origin[1]), (xmax, origin[1]), AXIS)
    line(draw, (origin[0], ymin), (origin[0], ymax), AXIS)
    text(draw, (xmax, origin[1] - 13), "Re", 14, MUTED, anchor="ra")
    text(draw, (origin[0] + 8, ymin), "Im", 14, MUTED)
    for value in (0.5, 1.0):
        x, y = point(complex(value))
        line(draw, (x, y - 4), (x, y + 4), AXIS)
        text(draw, (x, y + 12), f"{value:g}", 13, MUTED, anchor="ma")

    values = cumulative(f_number)
    # Draw exact integrated-cell arrows. At very short pixel lengths, heads
    # are shown on exact 8-cell group resultants, not enlarged tiny vectors.
    group = 8 if 2 * math.sqrt(f_number) * PIXELS_PER_UNIT / ELEMENTS < 3 else 1
    vertices = values[::group]
    if len(vertices) == 0 or vertices[-1] != values[-1]:
        vertices = np.r_[vertices, values[-1]]
    # Fine cumulative trace retains curvature even when arrows are grouped.
    fine = [pixels(point(z)) for z in cumulative(f_number, FINE_EDGES)]
    draw.line(fine, fill=(*BLUE, 150), width=round(1.35 * SUPERSAMPLE))
    for first, last in zip(vertices[:-1], vertices[1:]):
        arrow(draw, point(first), point(last), (*BLUE, 235), width=1.45, head=3.8)
    # The gold arrow is always the actual sum of the same aperture terms.
    arrow(draw, origin, point(values[-1]), (*GOLD, 255), width=3.3, head=11)
    for z, color, radius in ((0j, MUTED, 3), (values[-1], GOLD, 3.4)):
        x, y = point(z)
        draw.ellipse(pixels((x-radius, y-radius, x+radius, y+radius)), fill=color)
    return values


def frame(seconds):
    image = Image.new("RGB", (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), BG)
    draw = ImageDraw.Draw(image, "RGBA")
    text(draw, (35, 25), "Two limits · tip-to-tail", 31, bold=True)
    text(draw, (37, 70), "One finite opening · plane-wave illumination · observation straight ahead", 19, MUTED)
    arrow(draw, (1080, 48), (1113, 48), BLUE, 2, 6)
    text(draw, (1123, 36), "contributions", 17, BLUE)
    arrow(draw, (1280, 48), (1313, 48), GOLD, 3, 7)
    text(draw, (1323, 36), "sum", 17, GOLD)
    numbers = state(seconds)
    titles = ("Distance increases", "Wavelength decreases")
    settings = ("Wavelength fixed", "Distance fixed")
    captions = ("The contributions align", "The outer contributions curl and cancel")
    for index, (panel, f_number) in enumerate(zip(PANELS, numbers)):
        draw.rounded_rectangle(pixels(panel), radius=round(15*SUPERSAMPLE),
                               fill=PANEL, outline=BORDER, width=round(1.4*SUPERSAMPLE))
        text(draw, (panel[0]+26, 128), titles[index], 26, bold=True)
        text(draw, (panel[0]+27, 168), settings[index], 18, MUTED)
        readout = f"z / z₀ = {F_START / f_number:.2f}" if index == 0 else f"λ / λ₀ = {F_START / f_number:.3f}"
        text(draw, (panel[2]-27, 168), readout, 21, INK, anchor="ra")
        line(draw, (panel[0]+27, 215), (panel[2]-27, 215), BORDER)
        draw_chain(draw, panel, f_number)
        text(draw, ((panel[0]+panel[2])/2, 697), captions[index], 20, MUTED, anchor="ma")
        start, stop = panel[0]+28, panel[2]-28
        line(draw, (start, 731), (stop, 731), BORDER, 2)
        line(draw, (start, 731), (start+(stop-start)*progress(seconds), 731), BLUE, 2)
    text(draw, (36, 779), "Phase reference: unobstructed wave at the observation point", 17, MUTED)
    text(draw, (1404, 779), "Same fixed amplitude scale in both panes", 17, MUTED, anchor="ra")
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def checks():
    from numpy.polynomial.legendre import leggauss
    nodes, weights = leggauss(24)
    middle = (EDGES[1:] + EDGES[:-1])/2
    half = (EDGES[1:] - EDGES[:-1])/2
    y = middle[:, None] + half[:, None] * nodes
    largest_error = 0.0
    minimum_margin = math.inf
    for f_number in np.r_[np.linspace(F_LEFT_END, F_START, 100), np.linspace(F_START, F_RIGHT_END, 150)]:
        values = cumulative(float(f_number))
        quadrature = (np.exp(-0.25j*np.pi)*math.sqrt(f_number)*half*
                      np.sum(weights*np.exp(1j*np.pi*f_number*y*y), axis=1))
        largest_error = max(largest_error, float(np.max(np.abs(np.diff(values)-quadrature))))
        for panel in PANELS:
            points = np.array([mapper(panel)(z) for z in cumulative(f_number, FINE_EDGES)])
            margin = min(np.min(points[:, 0]-(panel[0]+29)),
                         np.min(panel[2]-29-points[:, 0]),
                         np.min(points[:, 1]-241), np.min(675-points[:, 1]))
            minimum_margin = min(minimum_margin, float(margin))
    assert largest_error < 1e-11, largest_error
    assert minimum_margin > 5, minimum_margin
    assert np.allclose(cumulative(state(0)[0]), cumulative(state(0)[1]))
    result = {"finite_element_quadrature_max_error":largest_error,
              "minimum_curve_margin_px":minimum_margin,
              "same_initial_chain":True,
              "phase_reference":"U / exp(ikz); normalized Fresnel prefactor retained",
              "fixed_pixels_per_unit":PIXELS_PER_UNIT,
              "start_F":F_START,"final_left_F":F_LEFT_END,"final_right_F":F_RIGHT_END,
              "duration_seconds":DURATION,"fps":FPS,"resolution":[WIDTH,HEIGHT],
              "endpoint_left":[float(cumulative(F_LEFT_END)[-1].real),float(cumulative(F_LEFT_END)[-1].imag)],
              "endpoint_right":[float(cumulative(F_RIGHT_END)[-1].real),float(cumulative(F_RIGHT_END)[-1].imag)]}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result),flush=True)


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1440, 924), BG)
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(SAMPLES):
        rendered = frame(seconds)
        rendered.save(OUT/f"{NAME}-check-{seconds:g}.png")
        x, y = (index % 3)*480, (index//3)*308
        sheet.paste(rendered.resize((480,280),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+284),f"{seconds:g} s",fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(25).save(OUT/f"{NAME}-final.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
               "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
               "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","medium",
               "-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(FPS*DURATION)):
        process.stdin.write(frame(index/FPS).tobytes())
        if index % (FPS*4) == 0:
            print(f"{index/FPS:g}/{DURATION:g} s; elapsed {time.perf_counter()-start:.1f} s",flush=True)
    process.stdin.close()
    error = process.stderr.read().decode(errors="replace")
    if process.wait():
        raise RuntimeError(error)
    print(json.dumps({"video":str(output),"bytes":output.stat().st_size}),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--preview",action="store_true")
    parser.add_argument("--render",action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        checks()
    if arguments.preview:
        previews()
    if arguments.render:
        render()
