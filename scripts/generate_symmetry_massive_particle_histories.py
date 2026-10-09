"""A localized relativistic particle, with playback carrying physical time.

Free spin-zero, positive-energy one-particle model in one fixed inertial frame.
The plotted L2 position wave function uses the canonical/Newton-Wigner position
representation, not a Klein-Gordon field amplitude or its indefinite density.
In scaled units c=hbar=1, H=sqrt(m*m+px*px+py*py). No low-speed expansion is used.

Each run has exactly the same Gaussian position density, with carrier momentum
p0=gamma*m*v0. Thus the central mode has the same group velocity in every run.
The mean velocity of a finite-width packet is also checked and reported rather
than silently identified with that central group velocity.

All intermediate positions C at time t/2 are included in
  psi(B,t) = integral K(B-C,t/2) psi(C,t/2) dC.
The displayed phasor trace groups the inner x integral, then accumulates over
y. Faint spatial segments are representative C-to-B legs, not blocking screens
or a claim that the particle follows one of the drawn lines. The incoming
amplitude at C already contains the full initial-state propagation.

Carrier factoring avoids a wasteful grid resolving the heavy mass's carrier.
The unitary numerical kernel and wave use the identical spectral dispersion.
Main-picture phase colors remove a spatially uniform rotating phase only.
The phasor pictures remove the common carrier factor at each endpoint, which
preserves all route phase differences and the squared magnitude of the sum.

The movie compares three independent evolutions. Mass changes only between
runs, not while a particle evolves. Time is playback, never a spatial axis.
Run --check --preview, inspect PNGs, then --render --encoded-check.
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
NAME = 'symmetry-massive-particle-histories'
W, H, SS, FPS = 1600, 1000, 2, 24
RUN_SECONDS, DURATION = 8., 24.
T_FINAL = 8.
MASSES = (16., 48., 128.)
V0 = .8
GAMMA = 1/math.sqrt(1-V0**2)
SIGMA_X, SIGMA_Y = .38, .20
OFF_Y = 1.10
BG = (253, 250, 244)
INK, MUTED = (37, 38, 40), (111, 108, 101)
GRID, AXIS = (235, 229, 219), (176, 171, 161)
BLUE, CORAL, GOLD = (43, 93, 145), (194, 91, 72), (181, 118, 22)
PLOT = (75., 169., 1525., 689.)
XMIN, XMAX = -2., 10.
YMIN, YMAX = -2.15, 2.15
SAMPLE_TIMES = (.65, 3.4, 7.8, 11.4, 15.8, 19.4, 22.0, 23.8)


@lru_cache(None)
def font(size, bold=False):
    for filename in ('seguisb.ttf' if bold else 'segoeui.ttf',
                     'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(filename, round(size*SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(float(v)*SS) for v in values)


def text(draw, pos, value, size=22, color=INK, bold=False, anchor=None):
    draw.text(px(pos), value, font=font(size, bold), fill=color, anchor=anchor)


def line(draw, start, end, color, width=1):
    draw.line(px((*start, *end)), fill=color, width=max(1, round(width*SS)))


def curve(draw, points, color, width=1):
    if len(points)<2:
        return
    draw.line([px(p) for p in points], fill=color,
              width=max(1, round(width*SS)), joint='curve')


def dot(draw, point, radius, color, outline=None):
    x, y = point
    draw.ellipse(px((x-radius, y-radius, x+radius, y+radius)),
                 fill=color, outline=outline, width=SS)


def dashed(draw, start, end, color, width=1, step=13, dash=5):
    start, end = np.asarray(start), np.asarray(end)
    delta = end-start
    length = float(np.linalg.norm(delta))
    if length<1e-10:
        return
    unit = delta/length
    for value in np.arange(0, length, step):
        line(draw, start+value*unit, start+min(value+dash, length)*unit, color, width)


def arrow(draw, start, end, color, width=2.5, head=10):
    start, end = np.asarray(start), np.asarray(end)
    delta = end-start
    length = float(np.linalg.norm(delta))
    if length<.5:
        return
    unit = delta/length
    side = np.array([-unit[1], unit[0]])
    line(draw, start, end, color, width)
    head = min(head, length/3)
    draw.polygon([px(end), px(end-head*unit+.4*head*side),
                  px(end-head*unit-.4*head*side)], fill=color)


@lru_cache(None)
def formula(value, size=24, color=INK):
    stream = BytesIO()
    math_to_image('$'+value+'$', stream, dpi=144,
                  prop=FontProperties(size=size), format='png',
                  color=tuple(v/255 for v in color))
    array = np.asarray(Image.open(stream).convert('RGBA')).copy()
    alpha = 255-np.min(array[:, :, :3], axis=2).astype(float)
    array[:, :, 3] = np.clip(np.round(alpha*255/(255-min(color))), 0, 255).astype(np.uint8)
    array[:, :, :3] = color
    image = Image.fromarray(array)
    return image.crop(image.getbbox())


def put_math(image, pos, value, size=24, color=INK):
    art = formula(value, size, color)
    image.paste(art, px(pos), art)


def xy(x, y):
    left, top, right, bottom = PLOT
    return np.stack((left+(np.asarray(x)-XMIN)/(XMAX-XMIN)*(right-left),
                     bottom-(np.asarray(y)-YMIN)/(YMAX-YMIN)*(bottom-top)), axis=-1)


def smooth(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


def clock(playback):
    run = min(int(playback/RUN_SECONDS), len(MASSES)-1)
    local = playback-run*RUN_SECONDS
    physical = T_FINAL*float(np.clip((local-.65)/6.65, 0, 1))
    return run, physical


class Particle:
    def __init__(self, mass, n=1024, period=32.):
        self.mass, self.n, self.period = mass, n, period
        self.dx = self.dy = period/n
        self.x = (np.arange(n)-n//2)*self.dx
        self.y = self.x.copy()
        q = 2*np.pi*np.fft.fftfreq(n, d=self.dx)
        self.p0 = GAMMA*mass*V0
        self.e0 = GAMMA*mass
        self.wavelength = 2*np.pi/self.p0
        self.px = q[None, :]+self.p0
        self.py = q[:, None]
        self.energy = np.sqrt(mass*mass+self.px*self.px+self.py*self.py)
        self.relative_energy = self.energy-self.e0
        initial = np.exp(-self.x[None, :]**2/(4*SIGMA_X**2)-self.y[:, None]**2/(4*SIGMA_Y**2))
        initial /= np.sqrt(np.sum(initial**2)*self.dx*self.dy)
        self.initial = initial
        self.spectrum = np.fft.fft2(np.fft.ifftshift(initial))
        weights = np.abs(self.spectrum)**2
        weights /= weights.sum()
        self.mean_vx = float(np.sum(weights*self.px/self.energy))
        self.mean_vy = float(np.sum(weights*self.py/self.energy))
        self.initial_peak = float(np.max(initial**2))
        # Sampling arrays for the full spatial picture, with carrier restored
        # analytically at display resolution instead of interpolating its stripes.
        self.draw_x = np.linspace(XMIN, XMAX, 1451)
        self.draw_y = np.linspace(YMAX, YMIN, 521)
        fx = (self.draw_x-self.x[0])/self.dx
        fy = (self.draw_y-self.y[0])/self.dy
        self.ix, self.iy = np.floor(fx).astype(int), np.floor(fy).astype(int)
        self.wx, self.wy = fx-self.ix, fy-self.iy

    def propagate(self, t):
        transfer = np.exp(-1j*self.relative_energy*t)
        return np.fft.fftshift(np.fft.ifft2(self.spectrum*transfer))

    def frame_state(self, t):
        transfer_half = np.exp(-1j*self.relative_energy*(t/2))
        midway = np.fft.fftshift(np.fft.ifft2(self.spectrum*transfer_half))
        final = np.fft.fftshift(np.fft.ifft2(self.spectrum*transfer_half**2))
        kernel = np.fft.fftshift(np.fft.ifft2(transfer_half))
        bx = int(round(V0*t/self.dx))+self.n//2
        targets = [(bx, self.n//2), (bx, self.n//2+round(OFF_Y/self.dy))]
        traces, values, errors = [], [], []
        columns = (bx-np.arange(self.n)+self.n//2)%self.n
        for _, by in targets:
            rows = (by-np.arange(self.n)+self.n//2)%self.n
            # Discrete K already includes the position-cell area. This is an
            # exact convolution identity on the numerical unitary Hilbert space.
            terms = midway*kernel[np.ix_(rows, columns)]
            grouped = terms.sum(axis=1)
            trace = np.r_[0j, np.cumsum(grouped)]
            traces.append(trace)
            value = final[by, bx]
            values.append(value)
            errors.append(float(abs(trace[-1]-value)))
        return final, midway, targets, traces, values, errors

    def display_sample(self, field):
        rows = self.iy[:, None]
        columns = self.ix[None, :]
        wx, wy = self.wx[None, :], self.wy[:, None]
        return ((1-wy)*((1-wx)*field[rows, columns]+wx*field[rows, columns+1])
                +wy*((1-wx)*field[rows+1, columns]+wx*field[rows+1, columns+1]))


class Scene:
    def __init__(self):
        self.particles = [Particle(mass) for mass in MASSES]
        samples = []
        for particle in self.particles:
            for t in (.5, 2., 4., 6., 8.):
                _, _, _, traces, _, _ = particle.frame_state(t)
                samples.extend(traces)
        values = np.concatenate(samples)
        # One square complex-plane scale across both endpoints and all masses.
        self.rmin, self.rmax = min(-.1, float(values.real.min())), max(.1, float(values.real.max()))
        self.imin, self.imax = min(-.1, float(values.imag.min())), max(.1, float(values.imag.max()))
        self.scale = min(420/(self.rmax-self.rmin), 154/(self.imax-self.imin))
        print(f'Common phasor scale {self.scale:.2f} px/unit', flush=True)


@lru_cache(None)
def backdrop():
    image = Image.new('RGB', (W*SS, H*SS), BG)
    d = ImageDraw.Draw(image, 'RGBA')
    text(d, (48, 24), 'A massive particle, built from wave contributions', 34, bold=True)
    text(d, (49, 78), 'Same initial position profile and central motion', 23, MUTED)
    put_math(image, (51, 116), r'\omega^2=c^2k^2+(mc^2/\hbar)^2', 24)
    left, top, right, bottom = PLOT
    for x in (0, 2, 4, 6, 8, 10):
        pos = xy(x, YMIN)
        line(d, pos, pos+(0, 5), AXIS, 1)
        text(d, (pos[0], bottom+8), str(x), 16, MUTED, anchor='ma')
    for y in (-2, -1, 0, 1, 2):
        pos = xy(XMIN, y)
        line(d, pos+(-5, 0), pos, AXIS, 1)
        text(d, (left-12, pos[1]), str(y), 16, MUTED, anchor='rm')
    text(d, (right+28, bottom+3), 'x', 21, MUTED, anchor='ma')
    text(d, (left-25, top-22), 'y', 21, MUTED)
    text(d, (53, 749), 'At the classical position', 23, BLUE, bold=True)
    text(d, (836, 749), 'Away from the trajectory', 23, CORAL, bold=True)
    text(d, (53, 968), 'Phasors sum over all intermediate positions. Faint routes show a sample at t/2.', 19, MUTED)
    return image


def density_image(particle, final):
    sampled = particle.display_sample(final)
    density = np.abs(sampled)**2
    # This removes only the common temporal carrier exp(-i E0 t). The spatial
    # wavelength is genuine, with phase differences at a given time preserved.
    phased = sampled*np.exp(1j*particle.p0*particle.draw_x[None, :])
    phase_weight = .5+.5*np.cos(np.angle(phased))
    pigment = (np.asarray(CORAL)[None, None, :]*(1-phase_weight[:, :, None])
               +np.asarray(BLUE)[None, None, :]*phase_weight[:, :, None])
    opacity = .92*np.clip(density/particle.initial_peak, 0, 1)**.52
    pixels = np.asarray(BG)[None, None, :]*(1-opacity[:, :, None])+pigment*opacity[:, :, None]
    return Image.fromarray(np.round(pixels).astype(np.uint8))


def draw_phasor(image, draw, trace, value, color, scene, offset):
    left, top, right, bottom = offset+60, 802, offset+615, 952
    scale = scene.scale
    center_r = (scene.rmin+scene.rmax)/2
    center_i = (scene.imin+scene.imax)/2
    origin = np.array([(left+right)/2-scale*center_r, (top+bottom)/2+scale*center_i])
    line(draw, (left, origin[1]), (right, origin[1]), (*GRID, 220), 1)
    if left<origin[0]<right:
        line(draw, (origin[0], top), (origin[0], bottom), (*GRID, 220), 1)
    points = origin+scale*np.c_[trace.real, -trace.imag]
    curve(draw, points, (*color, 220), 1.65)
    arrow(draw, origin, points[-1], color, 2.9, 9)
    dot(draw, origin, 2.7, INK)
    dot(draw, points[-1], 3.5, color)
    put_math(image, (offset+600, 816), r'|\sum a_C|^2', 22, color)
    number = abs(value)**2
    label = f'{number:.3f}' if number>=.001 else f'{number:.1e}'
    text(draw, (offset+672, 861), label, 25, color, bold=True, anchor='ma')


def render_frame(playback, scene):
    run, t = clock(playback)
    particle = scene.particles[run]
    final, midway, targets, traces, values, _ = particle.frame_state(t)
    image = backdrop().copy()
    draw = ImageDraw.Draw(image, 'RGBA')
    mass_ratio = particle.mass/MASSES[0]
    ratio_text = ('1', '1/3', '1/8')[run]
    put_math(image, (960, 74), rf'm={mass_ratio:g}m_0\qquad\lambda={ratio_text}\,\lambda_0', 26)
    text(draw, (1528, 122), f'Time    {t/T_FINAL:.2f} T', 24, MUTED, anchor='ra')
    for i in range(3):
        dot(draw, (1428+i*32, 45), 6, BLUE if i==run else GRID)
    tile = density_image(particle, final).resize(px((PLOT[2]-PLOT[0], PLOT[3]-PLOT[1])), Image.Resampling.LANCZOS)
    image.paste(tile, px(PLOT[:2]))
    draw = ImageDraw.Draw(image, 'RGBA')
    line(draw, (PLOT[0], PLOT[3]), (PLOT[2], PLOT[3]), AXIS, 1)
    line(draw, (PLOT[0], PLOT[1]), (PLOT[0], PLOT[3]), AXIS, 1)
    dashed(draw, xy(0, 0), xy(9.25, 0), (*GOLD, 175), 1.15)
    text(draw, xy(8.2, -.18), 'Classical trajectory', 18, GOLD, anchor='ma')
    # Initial preparation is a location marker, not a physical source or slit.
    dot(draw, xy(0, 0), 3, (*GOLD, 210))
    text(draw, xy(0, -.46), 'Start', 17, MUTED, anchor='ma')
    annotation_opacity = smooth((t-.65)/1.2)
    if annotation_opacity>0:
        # Representative points in the earlier spatial distribution. The actual
        # sum uses every grid point over the entire two-dimensional plane.
        for cy in np.linspace(-1.35, 1.35, 9):
            for cx in (V0*t/2-.5, V0*t/2, V0*t/2+.5):
                i = int(round(cx/particle.dx))+particle.n//2
                j = int(round(cy/particle.dy))+particle.n//2
                density = abs(midway[j, i])**2/particle.initial_peak
                alpha = round(annotation_opacity*(16+75*min(1., math.sqrt(density))))
                point = xy(cx, cy)
                for target, color in zip(targets, (BLUE, CORAL)):
                    bx, by = target
                    end = xy(particle.x[bx], particle.y[by])
                    line(draw, point, end, (*color, round(alpha*.60)), .85)
                dot(draw, point, 2., (*MUTED, alpha+20))
        text(draw, xy(V0*t/2, -1.66), 'Intermediate positions · t/2', 17,
             (*MUTED, round(annotation_opacity*255)), anchor='ma')
    for target, color, label in zip(targets, (BLUE, CORAL), ('B', 'B′')):
        bx, by = target
        point = xy(particle.x[bx], particle.y[by])
        dot(draw, point, 6, BG)
        dot(draw, point, 4.2, color)
        text(draw, point+(14, -10), label, 23, color, bold=True)
    text(draw, (788, 720), 'Position probability. Color shows phase in a common rotating reference.', 17, MUTED, anchor='ma')
    for i, (trace, value, color) in enumerate(zip(traces, values, (BLUE, CORAL))):
        draw_phasor(image, draw, trace, value, color, scene, i*780)
    return image.resize((W, H), Image.Resampling.LANCZOS)


def check():
    rows = []
    for mass in MASSES:
        particle = Particle(mass)
        final, midway, targets, traces, values, errors = particle.frame_state(T_FINAL)
        rho = np.abs(final)**2
        area = particle.dx*particle.dy
        norm = float(np.sum(rho)*area)
        mean_x = float(np.sum(rho*particle.x[None, :])*area)
        std_x = float(np.sqrt(np.sum(rho*(particle.x[None, :]-mean_x)**2)*area))
        std_y = float(np.sqrt(np.sum(rho*particle.y[:, None]**2)*area))
        view = ((particle.x>=XMIN)&(particle.x<=XMAX))[None, :] & ((particle.y>=YMIN)&(particle.y<=YMAX))[:, None]
        captured = float(np.sum(rho[view])*area)
        # A finer spatial grid independently tests propagation, not just its
        # composition identity. Compare the coincident samples at t=T_FINAL.
        finer = Particle(mass, n=1536)
        fine = finer.propagate(T_FINAL)
        target_values = []
        for bx, by in targets:
            x, y = particle.x[bx], particle.y[by]
            ix = (x-finer.x[0])/finer.dx
            iy = (y-finer.y[0])/finer.dy
            i, j = int(np.floor(ix)), int(np.floor(iy))
            wx, wy = ix-i, iy-j
            interpolated = ((1-wy)*((1-wx)*fine[j,i]+wx*fine[j,i+1])
                            +wy*((1-wx)*fine[j+1,i]+wx*fine[j+1,i+1]))
            target_values.append(float(abs(interpolated-final[by,bx])))
        row = {'mass': mass, 'central_wave_number': particle.p0,
               'central_frequency': particle.e0, 'wavelength': particle.wavelength,
               'central_group_velocity': V0, 'mean_velocity_x': particle.mean_vx,
               'mean_position_x': mean_x, 'norm': norm,
               'initial_sigma_x': SIGMA_X, 'initial_sigma_y': SIGMA_Y,
               'final_sigma_x': std_x, 'final_sigma_y': std_y,
               'probability_inside_picture': captured,
               'on_trajectory_density': float(abs(values[0])**2),
               'off_trajectory_density': float(abs(values[1])**2),
               'composition_errors': errors, 'finer_grid_amplitude_errors': target_values}
        rows.append(row)
        assert abs(norm-1)<1e-10, row
        assert max(errors)<1e-10, row
        assert abs(mean_x-particle.mean_vx*T_FINAL)<1e-7, row
        assert captured>.99, row
        assert max(target_values)<.003, row
        print(json.dumps(row, indent=2), flush=True)
    assert rows[-1]['off_trajectory_density']<rows[0]['off_trajectory_density']/100
    assert rows[-1]['final_sigma_y']<rows[0]['final_sigma_y']/2
    report = {'model': 'free positive-energy massive scalar particle in a fixed inertial frame',
              'position_representation': 'L2 canonical/Newton-Wigner',
              'scaled_units': 'c=hbar=1',
              'physical_time_is_playback': True,
              'physical_barriers': False,
              'same_initial_position_density': True,
              'same_central_group_velocity': True,
              'phase_gauge': 'common temporal carrier removed in picture; endpoint carrier removed in sums',
              'all_intermediate_positions_summed': True,
              'phasors_grouped_by_intermediate_y': True,
              'checks': rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


def contact(images, labels, destination):
    tw, th, label_height = 800, 500, 36
    sheet = Image.new('RGB', (tw*2, (th+label_height)*math.ceil(len(images)/2)), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype('segoeui.ttf', 20)
    for index, (image, label) in enumerate(zip(images, labels)):
        x, y = (index%2)*tw, (index//2)*(th+label_height)
        sheet.paste(image.resize((tw, th), Image.Resampling.LANCZOS), (x,y))
        draw.text((x+20,y+th+5), label, font=label_font, fill=MUTED)
    sheet.save(destination)


def preview(scene):
    images = [render_frame(t, scene) for t in SAMPLE_TIMES]
    contact(images, [f'{t:.2f}s' for t in SAMPLE_TIMES], OUT/f'{NAME}-contact-sheet.png')
    images[-1].save(OUT/f'{NAME}-poster.png')
    images[2].save(OUT/f'{NAME}-long-wavelength.png')
    print('Preview saved.', flush=True)


def render(scene):
    # Warm the shared read-only typography before concurrent frame production.
    for t in (0., 8., 16.):
        render_frame(t, scene)
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
               '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
               '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', str(OUT/f'{NAME}.mp4')]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    started = time.monotonic()
    try:
        total = round(FPS*DURATION)
        with ThreadPoolExecutor(max_workers=3) as pool:
            pending = deque(pool.submit(render_frame, i/FPS, scene) for i in range(6))
            for index in range(total):
                process.stdin.write(pending.popleft().result().tobytes())
                if index+6<total:
                    pending.append(pool.submit(render_frame, (index+6)/FPS, scene))
                if index%(FPS*2)==0:
                    print(f'Render {index/FPS:.0f}/{DURATION:g}s  elapsed {time.monotonic()-started:.1f}s', flush=True)
        process.stdin.close()
        if process.wait()!=0:
            raise RuntimeError('Video encoder failed')
    except BaseException:
        process.kill()
        raise
    print('MP4 saved.', flush=True)


def encoded_check(scene):
    reader = imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'), pix_fmt='rgb24')
    metadata = next(reader)
    indices = [round(t*FPS) for t in SAMPLE_TIMES]
    images, errors, count = [], [], 0
    for index, raw in enumerate(reader):
        count += 1
        if index in indices:
            image = Image.frombytes('RGB', (W,H), raw)
            reference = np.asarray(render_frame(index/FPS, scene)).astype(float)
            errors.append(float(np.mean(np.abs(np.asarray(image).astype(float)-reference))))
            images.append(image)
    assert count==round(FPS*DURATION)
    assert tuple(metadata['size'])==(W,H)
    assert max(errors)<3
    contact(images, [f'{i/FPS:.2f}s decoded' for i in indices], OUT/f'{NAME}-encoded-contact-sheet.png')
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
        scene = Scene()
        if args.preview:
            preview(scene)
        if args.render:
            render(scene)
        if args.encoded_check:
            encoded_check(scene)
