"""Monochromatic Gaussian diffraction approaching the ray-optics limit.

This is a 2D scalar paraxial beam with ONE transverse coordinate y. Each
frame is a separate steady monochromatic configuration, not a pulse or a
particle movie. Playback changes wavelength, not physical propagation time.
The entrance amplitude, flat entrance phase, propagation distance, plotting
scales, and color transfer remain fixed throughout.

With k=2*pi/lambda, z_R=k*w0**2/2, and q=1+i*z/z_R,
  psi(y,z,t)=q**(-1/2)*exp(-y**2/(w0**2*q))*exp(i*(k*z-omega*t)).
The sampled physical time is t=0. The right panel plots |psi(y,L,0)|**2.
This 1-transverse model uses HALF the usual cylindrical-beam Gouy phase
and sqrt(w0/w) amplitude. Its transverse integrated intensity is constant.

The dashed parallel lines denote the ray-optics reference y=+/-w0. The
solid lines are the actual 1/e^2 intensity contours, not hard beam edges.
Color shows the real field, using a fixed signed contrast mapping. The
Gaussian intensity and width curves use the unmodified physical values.

The monochromatic construction excludes temporal-frequency bandwidth.
Stationary phase explains its short-wavelength ray limit, not an extra
independent broadening effect. No existing media or prose is changed.

Run --check --preview, inspect, then --render --encoded-check.
"""
from __future__ import annotations

import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / '.tools' / 'animation-python-packages'
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties

OUT = ROOT / 'content' / 'drafts' / 'animations'
NAME = 'symmetry-monochromatic-gaussian'
W, H, SS, FPS, DURATION = 1600, 1000, 2, 24, 15
BG = (253, 250, 244)
INK, MUTED = (37, 38, 40), (111, 108, 101)
AXIS, GRID = (176, 171, 161), (231, 226, 218)
BLUE, CORAL = (43, 93, 145), (194, 91, 72)
W0, LENGTH, YMAX = .7, 14., 3.7
LAM_LONG, LAM_SHORT = .28, .04
PLOT = (110., 231., 1250., 775.)
PROFILE = (1320., 231., 1530., 775.)
CY = (PLOT[1] + PLOT[3]) / 2
Y_SCALE = (PLOT[3] - PLOT[1]) / (2 * YMAX)
SAMPLE_TIMES = (0., 2.5, 4.5, 6.5, 8.5, 10., 12., 14.9)
MATH_LOCK = threading.RLock()


@lru_cache(None)
def font(size, bold=False):
    for name in ('seguisb.ttf' if bold else 'segoeui.ttf',
                 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, round(size * SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(float(v) * SS) for v in values)


def text(draw, pos, value, size=22, color=INK, bold=False, anchor=None):
    draw.text(px(pos), value, font=font(size, bold), fill=color, anchor=anchor)


def line(draw, a, b, color, width=1):
    draw.line(px((*a, *b)), fill=color, width=max(1, round(width * SS)))


def curve(draw, points, color, width=1):
    draw.line([px(p) for p in points], fill=color,
              width=max(1, round(width * SS)), joint='curve')


def dashed(draw, a, b, color, width=1, step=13, dash=5):
    a, b = np.asarray(a), np.asarray(b)
    delta = b - a
    length = float(np.linalg.norm(delta))
    unit = delta / length
    for start in np.arange(0, length, step):
        line(draw, a + start * unit, a + min(start + dash, length) * unit, color, width)


def arrow(draw, a, b, color, width=2, head=10):
    a, b = np.asarray(a), np.asarray(b)
    delta = b - a
    unit = delta / np.linalg.norm(delta)
    normal = np.array([-unit[1], unit[0]])
    line(draw, a, b, color, width)
    draw.polygon([px(b), px(b-head*unit+.4*head*normal),
                  px(b-head*unit-.4*head*normal)], fill=color)


@lru_cache(None)
def formula(value, size=24, color=INK):
    stream = BytesIO()
    # Matplotlib's shared math parser is not thread-safe.
    with MATH_LOCK:
        math_to_image('$' + value + '$', stream, dpi=144,
                      prop=FontProperties(size=size), format='png',
                      color=tuple(c / 255 for c in color))
    array = np.asarray(Image.open(stream).convert('RGBA')).copy()
    alpha = 255 - np.min(array[:, :, :3], axis=2).astype(float)
    array[:, :, 3] = np.clip(np.round(alpha*255/(255-min(color))), 0, 255).astype(np.uint8)
    array[:, :, :3] = color
    art = Image.fromarray(array)
    return art.crop(art.getbbox())


def put_math(image, pos, value, size=24, color=INK):
    art = formula(value, size, color)
    image.paste(art, px(pos), art)


def smooth(value):
    value = float(np.clip(value, 0, 1))
    return value * value * (3 - 2 * value)


def wavelength_at(playback):
    # The fixed initial and final holds make the comparison readable.
    u = smooth((playback - 1.6) / 8.5)
    return LAM_LONG * (LAM_SHORT / LAM_LONG) ** u


def beam(y, z, wavelength):
    k = 2 * np.pi / wavelength
    zr = np.pi * W0 * W0 / wavelength
    q = 1 + 1j * np.asarray(z) / zr
    return np.exp(-np.asarray(y)**2 / (W0*W0*q)) / np.sqrt(q) * np.exp(1j*k*np.asarray(z))


def radius(z, wavelength):
    return W0 * np.sqrt(1 + (wavelength*np.asarray(z)/(np.pi*W0*W0))**2)


def xy(z, y):
    left, top, right, bottom = PLOT
    return np.stack((left + np.asarray(z)/LENGTH*(right-left),
                     CY - np.asarray(y)*Y_SCALE), axis=-1)


class Scene:
    def __init__(self):
        # Render the actual carrier at twice the delivered resolution.
        # The smallest wavelength still spans >3 delivered pixels/cycle.
        self.z = np.linspace(0, LENGTH, round((PLOT[2]-PLOT[0])*SS))
        self.y = np.linspace(YMAX, -YMAX, round((PLOT[3]-PLOT[1])*SS))
        self.output_y = np.linspace(YMAX, -YMAX, 1200)
        self.contour_z = np.linspace(0, LENGTH, 700)

    @lru_cache(maxsize=4)
    def field_image(self, wavelength):
        real = beam(self.y[:, None], self.z[None, :], wavelength).real
        colors = np.where(real[:, :, None] >= 0, np.asarray(BLUE), np.asarray(CORAL))
        opacity = .80 * np.abs(real[:, :, None])**.75
        rgb = np.asarray(BG) + opacity*(colors-np.asarray(BG))
        return Image.fromarray(np.clip(np.round(rgb), 0, 255).astype(np.uint8))


def render_frame(playback, scene):
    wavelength = wavelength_at(playback)
    u = math.log(LAM_LONG/wavelength)/math.log(LAM_LONG/LAM_SHORT)
    width = float(radius(LENGTH, wavelength))
    image = Image.new('RGB', (W*SS, H*SS), BG)
    image.paste(scene.field_image(wavelength), px(PLOT[:2]))
    draw = ImageDraw.Draw(image)

    text(draw, (73, 39), 'A monochromatic Gaussian beam', 34, bold=True)
    text(draw, (75, 93), 'Same starting width and flat wavefront', 23, MUTED)
    put_math(image, (1260, 48), rf'\lambda = {wavelength:.3f}', 27, BLUE)
    # A wavelength comparison control. It is not a physical-time clock.
    text(draw, (1265, 105), 'longer', 17, MUTED)
    text(draw, (1532, 105), 'shorter', 17, MUTED, anchor='ra')
    line(draw, (1266, 143), (1532, 143), GRID, 3)
    line(draw, (1266, 143), (1266+266*u, 143), BLUE, 3)
    x_marker = 1266+266*u
    draw.ellipse(px((x_marker-5, 138, x_marker+5, 148)), fill=BLUE)

    put_math(image, (110, 184), r'\mathrm{Re}\,\psi(y,z)', 23)
    put_math(image, (1305, 184), r'I(y,L)=|\psi(y,L)|^2', 22)
    text(draw, (1320, 214), 'dashed = entrance profile', 15, MUTED)
    # Real-field color key, separate from the geometrical contour key.
    line(draw, (442, 202), (465, 202), BLUE, 5)
    text(draw, (475, 186), '+', 23, MUTED)
    line(draw, (524, 202), (547, 202), CORAL, 5)
    text(draw, (557, 186), '−', 23, MUTED)

    # These are reference rays, not walls or sharp beam edges.
    for sign in (-1, 1):
        y_ref = CY-sign*W0*Y_SCALE
        dashed(draw, (PLOT[0], y_ref), (PLOT[2], y_ref), AXIS, 1.4)
        widths = sign*radius(scene.contour_z, wavelength)
        curve(draw, xy(scene.contour_z, widths), INK, 1.6)

    arrow(draw, (PLOT[0], PLOT[3]+19), (PLOT[2]+8, PLOT[3]+19), AXIS, 1.2, 8)
    arrow(draw, (PLOT[0]-18, PLOT[3]), (PLOT[0]-18, PLOT[1]-7), AXIS, 1.2, 8)
    text(draw, (PLOT[0]-24, PLOT[1]-31), 'y', 22, MUTED)
    text(draw, (PLOT[2]+18, PLOT[3]+3), 'z', 22, MUTED)
    text(draw, (PLOT[0], PLOT[3]+34), '0', 18, MUTED, anchor='ma')
    text(draw, (PLOT[2], PLOT[3]+34), 'L', 18, MUTED, anchor='ma')
    line(draw, (PLOT[0]-23, CY), (PLOT[0]-14, CY), AXIS)
    text(draw, (PLOT[0]-33, CY-12), '0', 17, MUTED, anchor='ra')

    # Output intensity uses a single fixed linear scale in every frame.
    pleft, ptop, pright, pbottom = PROFILE
    y_screen = CY-scene.output_y*Y_SCALE
    intensity = np.abs(beam(scene.output_y, LENGTH, wavelength))**2
    entrance = np.exp(-2*scene.output_y**2/(W0*W0))
    x_screen = pleft+(pright-pleft)*intensity
    fill = [px((pleft, ptop))]+[px(p) for p in np.column_stack((x_screen, y_screen))]+[px((pleft, pbottom))]
    draw.polygon(fill, fill=(222, 231, 233))
    # Dashed starting profile shows that the width is held fixed at z=0.
    initial_points = np.column_stack((pleft+(pright-pleft)*entrance, y_screen))
    for first in range(0, len(initial_points)-5, 10):
        curve(draw, initial_points[first:first+5], AXIS, 1.3)
    curve(draw, np.column_stack((x_screen, y_screen)), BLUE, 3.0)
    line(draw, (pleft, ptop), (pleft, pbottom), AXIS, 1)
    line(draw, (pleft, pbottom+19), (pright+5, pbottom+19), AXIS, 1)
    text(draw, (pleft, pbottom+34), '0', 18, MUTED, anchor='ma')
    text(draw, (pright, pbottom+34), '1', 18, MUTED, anchor='ma')

    # The beam stays an extended Gaussian in the ray limit, not a delta spike.
    line(draw, (110, 865), (150, 865), INK, 1.6)
    put_math(image, (163, 847), r'y=\pm w(z)', 22)
    dashed(draw, (414, 865), (454, 865), AXIS, 1.4)
    text(draw, (466, 847), 'straight-ray reference', 20, MUTED)
    put_math(image, (931, 842), rf'w(L)/w_0 = {width/W0:.2f}', 24, BLUE)
    put_math(image, (110, 905), r'w(z)=w_0\sqrt{1+\left(\frac{\lambda z}{\pi w_0^2}\right)^2}', 25)
    text(draw, (1530, 905), 'One temporal frequency in each setup.', 20, MUTED, anchor='ra')
    text(draw, (1530, 942), 'Playback compares wavelengths, not elapsed time.', 18, MUTED, anchor='ra')
    return image.resize((W, H), Image.Resampling.LANCZOS)


def check():
    rows = []
    y = np.linspace(-14, 14, 32768, endpoint=False)
    dy = y[1]-y[0]
    transverse_k = 2*np.pi*np.fft.fftfreq(len(y), dy)
    source = np.exp(-y*y/(W0*W0))
    source_spectrum = np.fft.fft(source)
    power0 = float(np.sum(abs(source)**2)*dy)
    spectrum_power = abs(source_spectrum)**2
    for wavelength in (LAM_LONG, .14, .07, LAM_SHORT):
        k = 2*np.pi/wavelength
        analytic = beam(y, LENGTH, wavelength)*np.exp(-1j*k*LENGTH)
        numerical = np.fft.ifft(source_spectrum*np.exp(-1j*transverse_k**2*LENGTH/(2*k)))
        # Independent angular-spectrum Helmholtz propagation tests the
        # paraxial approximation used in the drawing, without that expansion.
        kz = np.sqrt((k*k-transverse_k**2).astype(complex))
        exact = np.fft.ifft(source_spectrum*np.exp(1j*(kz-k)*LENGTH))
        power = float(np.sum(abs(analytic)**2)*dy)
        sigma = float(np.sqrt(np.sum(y*y*abs(analytic)**2)*dy/power))
        row = {'wavelength': wavelength,
               'output_radius': float(radius(LENGTH, wavelength)),
               'radius_ratio': float(radius(LENGTH, wavelength)/W0),
               'power': power,
               'power_relative_error': abs(power/power0-1),
               'fresnel_complex_max_error': float(max(abs(analytic-numerical))),
               'helmholtz_intensity_max_error': float(max(abs(abs(analytic)**2-abs(exact)**2))),
               'output_rms_width': sigma,
               'propagating_spectral_power_fraction': float(np.sum(spectrum_power[abs(transverse_k)<k])/np.sum(spectrum_power)),
               'initial_field_max_error': float(max(abs(beam(y,0,wavelength)-source)))}
        assert row['power_relative_error'] < 1e-9, row
        assert row['fresnel_complex_max_error'] < 1e-9, row
        assert row['helmholtz_intensity_max_error'] < .001, row
        assert abs(2*sigma-row['output_radius']) < 1e-8, row
        assert row['initial_field_max_error'] < 1e-14, row
        rows.append(row)
    assert rows[0]['radius_ratio'] > 2.7
    assert rows[-1]['radius_ratio'] < 1.07
    assert (PLOT[2]-PLOT[0])*LAM_SHORT/LENGTH > 3
    report = {'model': '2D scalar monochromatic paraxial Gaussian beam with one transverse coordinate',
              'source_radius': W0, 'observation_distance': LENGTH,
              'temporal_frequency_count_per_configuration': 1,
              'playback_is_physical_time': False,
              'source_amplitude_and_flat_phase_fixed': True,
              'field_phase': 'true spatial carrier, sampled at physical t=0',
              'width_contours': '1/e^2 intensity, not edges',
              'real_field_contrast_mapping': '0.8*abs(Re psi)^0.75, sign sets blue/coral',
              'intensity_profile_scale': 'fixed linear, initial on-axis intensity = 1',
              'checks': rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


def contact(images, labels, path):
    tw, th, lh = 800, 500, 34
    sheet = Image.new('RGB', (tw*2, (th+lh)*math.ceil(len(images)/2)), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype('segoeui.ttf', 19)
    for index, (frame, label) in enumerate(zip(images, labels)):
        x, y = index%2*tw, index//2*(th+lh)
        sheet.paste(frame.resize((tw, th), Image.Resampling.LANCZOS), (x, y))
        draw.text((x+15, y+th+4), label, fill=MUTED, font=label_font)
    sheet.save(path)


def preview(scene):
    images = [render_frame(t, scene) for t in SAMPLE_TIMES]
    contact(images, [f'{t:.1f}s  lambda={wavelength_at(t):.3f}' for t in SAMPLE_TIMES],
            OUT/f'{NAME}-contact-sheet.png')
    images[0].save(OUT/f'{NAME}-long-wavelength.png')
    images[-1].save(OUT/f'{NAME}-poster.png')
    print('Preview saved.', flush=True)


def render(scene):
    # Warm typography before concurrent rendering.
    for t in (0., 7., 14.):
        render_frame(t, scene)
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
               '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
               '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', str(OUT/f'{NAME}.mp4')]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    started = time.monotonic()
    total = FPS*DURATION
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            pending = deque(pool.submit(render_frame, i/FPS, scene) for i in range(6))
            for index in range(total):
                process.stdin.write(pending.popleft().result().tobytes())
                if index+6 < total:
                    pending.append(pool.submit(render_frame, (index+6)/FPS, scene))
                if index%(FPS*2) == 0:
                    print(f'Render {index/FPS:.0f}/{DURATION}s  elapsed {time.monotonic()-started:.1f}s', flush=True)
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError('Video encoder failed')
    except BaseException:
        process.kill()
        raise
    print('MP4 saved.', flush=True)


def encoded_check(scene):
    reader = imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'), pix_fmt='rgb24')
    metadata = next(reader)
    selected = [round(t*FPS) for t in SAMPLE_TIMES]
    frames, errors, count = [], [], 0
    for index, raw in enumerate(reader):
        count += 1
        if index in selected:
            image = Image.frombytes('RGB', (W,H), raw)
            reference = np.asarray(render_frame(index/FPS, scene)).astype(float)
            errors.append(float(np.mean(abs(np.asarray(image).astype(float)-reference))))
            frames.append(image)
    assert count == FPS*DURATION
    assert tuple(metadata['size']) == (W,H)
    assert max(errors) < 3
    contact(frames, [f'{i/FPS:.1f}s decoded' for i in selected], OUT/f'{NAME}-encoded-contact-sheet.png')
    report = {'frames': count, 'fps': metadata['fps'], 'size': metadata['size'],
              'mean_pixel_errors': errors}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for option in ('check', 'preview', 'render', 'encoded-check'):
        parser.add_argument('--'+option, action='store_true')
    args = parser.parse_args()
    if args.check:
        check()
    if args.preview or args.render or args.encoded_check:
        OUT.mkdir(parents=True, exist_ok=True)
        scene = Scene()
        if args.preview:
            preview(scene)
        if args.render:
            render(scene)
        if args.encoded_check:
            encoded_check(scene)
