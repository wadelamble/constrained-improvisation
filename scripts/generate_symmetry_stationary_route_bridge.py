"""Prototype connecting a route sum at B to a distribution over B.

Scalar monochromatic Fresnel propagation in two spatial dimensions. This is
the small-angle wave model, not a time-dependent particle-spreading movie.
The entrance aperture prepares a fixed, localized amplitude with a flat phase.
The intermediate plane is completely open: its 'openings' are integration
cells, not an additional opaque grating. Every crossing contributes coherently.

For the carrier-removed envelope,
  K_z(b,c) = exp(i*pi*(b-c)**2/(wavelength*z))/sqrt(i*wavelength*z).
  psi_z = K_z psi_0,  psi_B = integral K_6(B,C) psi_6(C) dC.
The common axial phase does not affect the intensity or cancellation picture.
Playback first scans the endpoint B, then changes wavelength with geometry,
entrance intensity, entrance phase direction, and color/plot scales fixed.

The intensity map and phasor sum use the same numerical wave. Intermediate
integration cells are combined only for drawing. No contributions are dropped
to manufacture cancellation. Probability language is an interpretation of
the normalized transverse intensity, not a simulated arrival-time detector.

Run --check --preview, inspect, then --render --encoded-check.
Only new prototype assets are written. No manuscript or older asset is changed.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
import json
import hashlib
import math
from pathlib import Path
import subprocess
import sys
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
NAME = 'symmetry-stationary-route-bridge'
W, H, SS, FPS, DURATION = 1440, 940, 2, 24, 24
BG = (253, 250, 244)
INK, MUTED = (37, 38, 40), (111, 108, 101)
GRID, AXIS = (235, 229, 219), (176, 171, 161)
BLUE, CORAL, GOLD = (43, 93, 145), (194, 91, 72), (181, 118, 22)

N, PERIOD = 16384, 64.0
DY = PERIOD / N
Y = (np.arange(N) - N // 2) * DY
Q = 2 * np.pi * np.fft.fftfreq(N, d=DY)
APERTURE = 1.0
EDGE = .15
SIGMA = .30
ZC, ZB = 6.0, 12.0
LAM_LONG, LAM_SHORT = .18, .006
DISPLAY_Y = 4.7
XL, XR, YT, YB = 124., 1010., 194., 558.
DETECTOR_RIGHT = 1357.
CY = (YT + YB) / 2
YS = (YB - YT) / (2 * DISPLAY_Y)
CX = XL + (XR - XL) / 2
SAMPLE_TIMES = (1.8, 4.0, 6.0, 9.0, 14.0, 18.0, 21.2, 23.9)

mask = np.ones_like(Y)
distance = np.abs(Y)
mask[distance >= APERTURE / 2] = 0
edge = (distance > APERTURE / 2 - EDGE) & (distance < APERTURE / 2)
mask[edge] = .5 * (1 + np.cos(np.pi * (distance[edge] - APERTURE / 2 + EDGE) / EDGE))
PSI0 = np.exp(-Y * Y / (4 * SIGMA * SIGMA)) * mask
PSI0 /= np.sqrt(np.sum(np.abs(PSI0)**2) * DY)
SPEC0 = np.fft.fft(np.fft.ifftshift(PSI0))
I_SCALE = float(np.max(PSI0**2))
C_SEL = np.abs(Y) <= 20.0
CS = Y[C_SEL]


@lru_cache(None)
def font(size, bold=False):
    for filename in ('seguisb.ttf' if bold else 'segoeui.ttf',
                     'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(filename, round(size * SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(float(v) * SS) for v in values)


def text(d, pos, value, size=22, color=INK, bold=False, anchor=None):
    d.text(px(pos), value, font=font(size, bold), fill=color, anchor=anchor)


def line(d, a, b, color, width=1):
    d.line(px((*a, *b)), fill=color, width=max(1, round(width * SS)))


def curve(d, points, color, width=1):
    d.line([px(point) for point in points], fill=color,
           width=max(1, round(width * SS)), joint='curve')


def dot(d, point, radius, color):
    x, y = point
    d.ellipse(px((x-radius, y-radius, x+radius, y+radius)), fill=color)


def arrow(d, start, end, color, width=2, head=10):
    start, end = np.asarray(start), np.asarray(end)
    delta = end - start
    length = np.linalg.norm(delta)
    if length < .5:
        return
    u = delta / length
    v = np.array([-u[1], u[0]])
    line(d, start, end, color, width)
    size = min(head, length / 3)
    d.polygon([px(end), px(end-size*u+.4*size*v),
               px(end-size*u-.4*size*v)], fill=color)


def dashed(d, start, end, color, width=1):
    start, end = np.asarray(start), np.asarray(end)
    delta = end-start
    length = np.linalg.norm(delta)
    u = delta/length
    for value in np.arange(0, length, 12):
        line(d, start+value*u, start+min(value+5, length)*u, color, width)


@lru_cache(None)
def formula(value, size=23, color=INK):
    stream = BytesIO()
    math_to_image('$'+value+'$', stream, dpi=144,
                  prop=FontProperties(size=size), format='png',
                  color=tuple(c/255 for c in color))
    array = np.asarray(Image.open(stream).convert('RGBA')).copy()
    alpha = 255 - np.min(array[:, :, :3], axis=2).astype(float)
    array[:, :, 3] = np.clip(np.round(alpha*255/(255-min(color))), 0, 255).astype(np.uint8)
    array[:, :, :3] = color
    image = Image.fromarray(array)
    return image.crop(image.getbbox())


def put_math(image, pos, value, size=23, color=INK):
    art = formula(value, size, color)
    image.paste(art, px(pos), art)


def field(wavelength, z):
    transfer = np.exp(-1j*wavelength*z*Q*Q/(4*np.pi))
    return np.fft.fftshift(np.fft.ifft(SPEC0*transfer))


def contributions(wavelength, b, at_c=None):
    if at_c is None:
        at_c = field(wavelength, ZC)
    kernel = np.exp(1j*np.pi*(b-CS)**2/(wavelength*(ZB-ZC))) / np.sqrt(1j*wavelength*(ZB-ZC))
    return at_c[C_SEL]*kernel*DY


def smooth(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


def state(t):
    if t < 2.5:
        return LAM_LONG, 0., 'A sum at one endpoint', smooth(t/2.1)
    if t < 7.5:
        u = (t-2.5)/5
        return LAM_LONG, .98*DISPLAY_Y*(1-2*u), 'Repeat the sum across the screen', 1.
    if t < 9.:
        start = -.98*DISPLAY_Y
        return LAM_LONG, start+(0.9-start)*smooth((t-7.5)/1.5), 'Keep the incoming wave fixed', 1.
    if t < 20.:
        u = smooth((t-9)/11)
        wavelength = LAM_LONG*(LAM_SHORT/LAM_LONG)**u
        return wavelength, .9, 'Shorten the wavelength', 1.
    if t < 22.:
        return LAM_SHORT, .9*(1-smooth((t-20)/2)), 'Compare the off-ray and on-ray sums', 1.
    return LAM_SHORT, 0., 'A narrow distribution along the ray', 1.


def py(y):
    return CY - np.asarray(y)*YS


def phase_color(phase):
    # Cyclic blue / gold / coral. This codes the actual relative complex phase.
    p = np.mod(np.asarray(phase), 2*np.pi)*3/(2*np.pi)
    palette = np.array([BLUE, GOLD, CORAL, BLUE], float)
    first = np.floor(p).astype(int)
    mix = (p-first)[..., None]
    return np.round(palette[first]*(1-mix)+palette[first+1]*mix).astype(np.uint8)


class Model:
    def __init__(self):
        self.lambdas = np.geomspace(LAM_LONG, LAM_SHORT, 65)
        self.plot_y = np.linspace(DISPLAY_Y, -DISPLAY_Y, 330)
        self.plot_z = np.linspace(0, ZB, 440)
        self.maps = []
        self.long_profile = np.abs(field(LAM_LONG, ZB))**2
        self.max_vector = 0.
        signature = hashlib.sha256(PSI0.tobytes()+np.array(
            [N, PERIOD, ZC, ZB, LAM_LONG, LAM_SHORT, DISPLAY_Y,
             len(self.lambdas), len(self.plot_y), len(self.plot_z)], dtype=float).tobytes()).hexdigest()[:16]
        cache = ROOT / '.tools' / 'animation-cache' / f'{NAME}-{signature}.npz'
        if cache.exists():
            with np.load(cache) as saved:
                self.maps = saved['maps']
                self.max_vector = float(saved['max_vector'])
            self.vector_scale = 163.0 / self.max_vector
            print('Using cached wave maps.', flush=True)
            return
        started = time.monotonic()
        for index, wavelength in enumerate(self.lambdas):
            transfer = np.exp(-1j*wavelength*self.plot_z[:, None]*Q[None, :]**2/(4*np.pi))
            waves = np.fft.fftshift(np.fft.ifft(transfer*SPEC0[None, :], axis=1), axes=1)
            intensities = np.abs(waves)**2
            cropped = np.stack([np.interp(self.plot_y, Y, row) for row in intensities], axis=1)
            self.maps.append(cropped.astype(np.float32))
            at_c = field(wavelength, ZC)
            for b in (0, .9):
                cumulative = np.r_[0j, np.cumsum(contributions(wavelength, b, at_c))]
                self.max_vector = max(self.max_vector, float(np.max(np.abs(cumulative))))
            if index % 16 == 0:
                print(f'Wave sums {index+1}/{len(self.lambdas)}  {time.monotonic()-started:.1f}s', flush=True)
        self.maps = np.asarray(self.maps)
        self.vector_scale = 163.0 / self.max_vector
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cache, maps=self.maps, max_vector=self.max_vector)

    def intensity_map(self, wavelength):
        u = math.log(LAM_LONG/wavelength)/math.log(LAM_LONG/LAM_SHORT)*(len(self.lambdas)-1)
        lower = min(int(u), len(self.lambdas)-2)
        mix = u-lower
        return self.maps[lower]*(1-mix) + self.maps[lower+1]*mix


@lru_cache(None)
def backdrop():
    image = Image.new('RGB', (W*SS, H*SS), BG)
    d = ImageDraw.Draw(image, 'RGBA')
    text(d, (48, 25), 'From a route sum to an outgoing distribution', 34, bold=True)
    text(d, (XL, 158), 'Fixed entrance slit', 20, MUTED)
    text(d, (CX, 158), 'All intermediate crossings C', 20, MUTED, anchor='ma')
    text(d, (XR+30, 158), 'At every B', 20, MUTED)
    text(d, (48, 599), 'The same contributions, added tip to tail', 23, bold=True)
    text(d, (768, 599), 'One preparation. One geometry.', 23, bold=True)
    put_math(image, (772, 650), r'\psi(B)=\int K(B,C)\,\psi(C)\,dC', 26)
    put_math(image, (773, 722), r'I(B)=|\psi(B)|^2', 26, BLUE)
    text(d, (773, 789), 'In QM, normalized intensity gives', 22, MUTED)
    text(d, (773, 823), 'the position probability distribution.', 22, MUTED)
    text(d, (48, 900), 'The intermediate plane is fully open. Each marked crossing contributes to the sum.', 19, MUTED)
    for y in (-3, -2, -1, 0, 1, 2, 3):
        line(d, (XL, py(y)), (DETECTOR_RIGHT, py(y)), (*GRID, 160), 1)
    line(d, (XR, YT), (XR, YB), AXIS, 2)
    line(d, (XL, YB), (XR, YB), AXIS, 1)
    text(d, ((XL+XR)/2, 571), 'Distance from the entrance slit', 18, MUTED, anchor='ma')
    text(d, (XR+30, 571), 'Intensity across the screen', 18, MUTED)
    # The complex-plane axes have one scale for the entire animation.
    line(d, (93, 755), (684, 755), (*GRID, 220), 1)
    line(d, (355, 652), (355, 869), (*GRID, 220), 1)
    text(d, (672, 762), 'Re', 17, MUTED)
    text(d, (361, 650), 'Im', 17, MUTED)
    return image


def render_frame(t, model):
    wavelength, b, heading, fraction = state(t)
    b = round(b/DY)*DY  # Both the screen sampling and integral use this point.
    image = backdrop().copy()
    d = ImageDraw.Draw(image, 'RGBA')
    text(d, (49, 90), heading, 27, BLUE, bold=True)
    text(d, (1390, 91), f'Wavelength / slit width    {wavelength/APERTURE:.3f}', 23, MUTED, anchor='ra')
    intensity = model.intensity_map(wavelength)
    strength = np.clip(np.sqrt(intensity/I_SCALE), 0, 1)
    color = np.asarray(BG)[None, None, :]*(1-.72*strength[:, :, None]) + np.asarray(BLUE)[None, None, :]*(.72*strength[:, :, None])
    tile = Image.fromarray(np.round(color).astype(np.uint8)).resize(px((XR-XL, YB-YT)), Image.Resampling.BICUBIC)
    image.paste(tile, px((XL, YT)))
    d = ImageDraw.Draw(image, 'RGBA')
    dashed(d, (XL+3, CY), (XR, CY), (*GOLD, 170), 1.5)
    text(d, (XL+35, CY-23), 'Ray', 18, GOLD)
    # The opaque material appears only at the actual entrance aperture.
    slit_top, slit_bottom = py(APERTURE/2), py(-APERTURE/2)
    d.rectangle(px((XL-8, YT, XL+8, slit_top)), fill=(*INK, 225))
    d.rectangle(px((XL-8, slit_bottom, XL+8, YB)), fill=(*INK, 225))
    arrow(d, (51, CY), (XL-17, CY), BLUE, 2.5, 10)
    source_y = np.linspace(-APERTURE/2, APERTURE/2, 181)
    source_i = np.interp(source_y, Y, PSI0**2)
    curve(d, np.c_[XL-16-32*source_i/I_SCALE, py(source_y)], BLUE, 1.8)
    # Fully open integration plane. Rings denote sample crossings, not blockers.
    line(d, (CX, YT), (CX, YB), (*AXIS, 80), 1)
    for crossing in np.linspace(-.95*DISPLAY_Y, .95*DISPLAY_Y, 63):
        dot(d, (CX, py(crossing)), 1.8, (*AXIS, 130))

    at_c = field(wavelength, ZC)
    terms = contributions(wavelength, b, at_c)
    # Colors correspond to the integrated contribution of each *displayed* cell.
    edges = np.linspace(np.searchsorted(CS, -DISPLAY_Y), np.searchsorted(CS, DISPLAY_Y), 66).astype(int)
    cells = np.array([np.sum(terms[first:last]) for first, last in zip(edges[:-1], edges[1:])])
    centers = np.array([np.mean(CS[first:last]) for first, last in zip(edges[:-1], edges[1:])])
    colors = phase_color(np.angle(cells))
    weights = np.abs(cells)
    wmax = max(float(np.max(weights)), 1e-15)
    for crossing, color, weight in zip(centers, colors, weights):
        # Visibility follows true magnitude. It does not affect the actual sum.
        opacity = round(20+105*np.sqrt(weight/wmax))
        line(d, (CX, py(crossing)), (XR, py(b)), (*tuple(color), opacity), .8)
        dot(d, (CX, py(crossing)), 2., (*tuple(color), opacity+65))
    dot(d, (XR, py(b)), 6, BG)
    dot(d, (XR, py(b)), 4.2, CORAL)
    text(d, (XR-13, py(b)-17), 'B', 22, CORAL, bold=True, anchor='ra')

    final_wave = field(wavelength, ZB)
    rho = np.abs(final_wave)**2
    plot_ys = np.linspace(-DISPLAY_Y, DISPLAY_Y, 1201)
    density = np.interp(plot_ys, Y, rho)
    profile_x = XR+28+295*density/I_SCALE
    if t >= 9:
        reference = np.interp(plot_ys, Y, model.long_profile)
        curve(d, np.c_[XR+28+295*reference/I_SCALE, py(plot_ys)], (*AXIS, 105), 1.7)
    points = np.c_[profile_x, py(plot_ys)]
    if 2.5 <= t < 7.5:
        points = points[plot_ys >= b]
    if t >= 2.5 and len(points)>1:
        d.polygon([px((XR+28, points[0,1])), *[px(p) for p in points],
                   px((XR+28, points[-1,1]))], fill=(*BLUE, 19))
        curve(d, points, BLUE, 2.7)
    value = float(rho[int(round(b/DY))+N//2])
    dot(d, (XR+28+295*value/I_SCALE, py(b)), 4, CORAL)
    line(d, (XR+7, py(b)), (XR+28+295*value/I_SCALE, py(b)), (*CORAL, 140), 1)

    cumulative = np.r_[0j, np.cumsum(terms)]
    count = max(2, int(fraction*len(cumulative)))
    # Individual increments are never replaced with equal arrows or random phase.
    z = cumulative[:count]
    coords = np.c_[355+model.vector_scale*z.real, 755-model.vector_scale*z.imag]
    # Use precisely the same cell colors in the route fan and its cumulative trace.
    boundaries = np.r_[0, edges, len(terms)]
    cell_colors = [AXIS, *[tuple(color) for color in colors], AXIS]
    for first, last, color in zip(boundaries[:-1], boundaries[1:], cell_colors):
        if first >= count-1:
            break
        last = min(last+1, count)
        curve(d, coords[first:last], (*color, 215), 1.3)
    endpoint = coords[-1]
    arrow(d, (355, 755), endpoint, BLUE, 3., 9)
    dot(d, (355, 755), 3.1, INK)
    dot(d, endpoint, 4., BLUE)
    put_math(image, (83, 854), r'\left|\sum_C \psi(C)K(B,C)\,\Delta C\right|^2', 20, BLUE)
    text(d, (678, 856), f'= {abs(cumulative[count-1])**2:.3f}', 21, BLUE, anchor='ra')
    return image.resize((W, H), Image.Resampling.LANCZOS)


def check():
    rows = []
    norm0 = float(np.sum(np.abs(PSI0)**2)*DY)
    for wavelength in (LAM_LONG, .08, LAM_SHORT):
        at_c = field(wavelength, ZC)
        final = field(wavelength, ZB)
        rho = np.abs(final)**2
        norm = float(np.sum(rho)*DY)
        errors = []
        for target in (0., .9, 2.1):
            b = round(target/DY)*DY
            summation = np.sum(contributions(wavelength, b, at_c))
            reference = final[int(round(b/DY))+N//2]
            errors.append(float(abs(summation-reference)))
        in_frame = float(np.sum(rho[np.abs(Y)<=DISPLAY_Y])*DY)
        row = {'wavelength': wavelength, 'norm': norm,
               'route_sum_max_absolute_error': max(errors),
               'displayed_probability': in_frame,
               'rms_width': float(np.sqrt(np.sum(rho*Y*Y)*DY)),
               'central_intensity': float(rho[N//2]),
               'off_ray_intensity': float(rho[N//2+round(.9/DY)])}
        rows.append(row)
        assert abs(norm-norm0)<1e-10
        assert max(errors)<.003, row
        assert in_frame>.985, row
    assert rows[-1]['rms_width'] < rows[0]['rms_width']/2
    assert rows[-1]['off_ray_intensity'] < rows[0]['off_ray_intensity']/100
    report = {'model': 'unitary scalar Fresnel propagation; fixed preparation; open intermediate plane',
              'playback_is_not_physical_time': True,
              'entrance_intensity_identical_at_every_wavelength': True,
              'axial_global_phase_removed': True,
              'color_and_plot_scales_fixed': True,
              'aperture_width': APERTURE, 'intermediate_plane': ZC,
              'receiving_screen': ZB, 'norm0': norm0, 'checks': rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


def contact(images, labels, destination):
    thumb_w, thumb_h = 720, 470
    sheet = Image.new('RGB', (thumb_w*2, (thumb_h+38)*math.ceil(len(images)/2)), BG)
    d = ImageDraw.Draw(sheet)
    small_font = ImageFont.truetype('segoeui.ttf', 20)
    for index, (image, label) in enumerate(zip(images, labels)):
        x, y = (index%2)*thumb_w, (index//2)*(thumb_h+38)
        sheet.paste(image.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), (x, y))
        d.text((x+18, y+thumb_h+7), label, font=small_font, fill=MUTED)
    sheet.save(destination)


def preview(model):
    images = [render_frame(t, model) for t in SAMPLE_TIMES]
    contact(images, [f'{t:.1f}s' for t in SAMPLE_TIMES], OUT/f'{NAME}-contact-sheet.png')
    images[-1].save(OUT/f'{NAME}-poster.png')
    print('Preview saved.', flush=True)


def render(model):
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
               '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
               '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', str(OUT/f'{NAME}.mp4')]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    started = time.monotonic()
    try:
        for index in range(FPS*DURATION):
            process.stdin.write(render_frame(index/FPS, model).tobytes())
            if index%(FPS*2)==0:
                print(f'Render {index/FPS:.0f}/{DURATION}s  elapsed {time.monotonic()-started:.1f}s', flush=True)
        process.stdin.close()
        if process.wait()!=0:
            raise RuntimeError('Video encoder failed')
    except BaseException:
        process.kill()
        raise
    print('MP4 saved.', flush=True)


def encoded_check(model):
    reader = imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'), pix_fmt='rgb24')
    metadata = next(reader)
    indices = [round(t*FPS) for t in SAMPLE_TIMES]
    frames, errors, count = [], [], 0
    for index, raw in enumerate(reader):
        count += 1
        if index in indices:
            image = Image.frombytes('RGB', (W, H), raw)
            reference = np.asarray(render_frame(index/FPS, model)).astype(float)
            errors.append(float(np.mean(np.abs(np.asarray(image).astype(float)-reference))))
            frames.append(image)
    assert count==FPS*DURATION
    assert tuple(metadata['size'])==(W,H)
    assert max(errors)<3
    contact(frames, [f'{i/FPS:.1f}s decoded' for i in indices], OUT/f'{NAME}-encoded-contact-sheet.png')
    report = {'frames': count, 'fps': metadata['fps'], 'size': metadata['size'],
              'mean_pixel_errors': errors}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    for option in ('check', 'preview', 'render', 'encoded-check'):
        parser.add_argument('--'+option, action='store_true')
    args = parser.parse_args()
    if args.check:
        check()
    if args.preview or args.render or args.encoded_check:
        OUT.mkdir(parents=True, exist_ok=True)
        model = Model()
        if args.preview:
            preview(model)
        if args.render:
            render(model)
        if args.encoded_check:
            encoded_check(model)
