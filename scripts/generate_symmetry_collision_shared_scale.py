"""Fixed-endpoint collision variation: phase and action require a shared scale.

Run with no arguments to produce review stills and numerical validation. Add
--render for the 30 s, 1600 x 900, 24 fps MP4. All output paths are repo-relative.

Model (illustrative units, c=1): two free timelike legs of each species join at
the candidate event (X,0), with fixed endpoints (x_i,-T) and (x_i,+T).
T=4, kappa=(32,64), x_1=-T/sqrt(2), x_2=T/sqrt(5). At X=0 the incoming spatial
wavevectors are (+32,-32), and the outgoing ones are (-32,+32). The proper duration
and phase of the two legs are

    tau_i(X)=2 sqrt(T^2-(X-x_i)^2),  Phi_i(X)=-kappa_i tau_i(X).

Thus Phi_i'=2 kappa_i (X-x_i)/sqrt(T^2-(X-x_i)^2), so Phi_1'(0)=+64 and
Phi_2'(0)=-64. With S_i=a_i Phi_i, S_total'(0)=64(a_1-a_2). The positive second
derivatives make both sums strictly convex over the plotted timelike domain.
For unequal a_i the stationary vertices differ; with a_1=a_2 they coincide.
The action model neglects the local interaction contribution at the vertex.

Playback first varies X among candidate histories with the endpoint events
fixed, then holds X=0 while testing a_2, then repeats the same X sweep with
equal conversion factors. Two overlapping Gaussian packet profiles replace
the collision dot. They show real parts of normalized incoming packets at a
fixed time, with mean k_i=kappa_i v_i/sqrt(1-v_i^2), v_i=(X-x_i)/T, and center
phase -kappa_i tau_i for the incoming leg. Their widths are fixed. These are
local packet snapshots attached to candidate histories, not a solution of
the scattering problem. Profile height encodes amplitude, not time.
Playback NEVER represents elapsed physical time or a particle moving along
its worldline. The plotted curves are exact
finite changes relative to X=0. Only the separate derivative panel expresses
first-order cancellation. No finite phase increments are claimed to cancel.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
import imageio_ffmpeg

OUT = ROOT / 'content' / 'drafts' / 'animations'
STEM = 'symmetry-collision-shared-scale'
W, H, FPS, DURATION = 1600, 900, 24, 30.0
BG, PANEL = '#fdfaf4', '#faf7f0'
INK, MUTED, BORDER = '#252628', '#6f6c66', '#dad3c8'
GRID, BLUE, GOLD, GREEN = '#cfcbc3', '#2b5d91', '#c08019', '#2b8059'
T = 4.0
# A common scale makes several actual phase cycles visible without changing
# the mass ratio, candidate geometry, or the stationary collision points.
KAPPAS = np.array([32.0, 64.0])
PACKET_SIGMA = .24
ENDPOINT_X = np.array([-T / math.sqrt(2), T / math.sqrt(5)])
X_LIMIT = .7
REVIEW_TIMES = [1.5, 5.5, 8.5, 16.0, 18.5, 22.0, 25.0, 28.0]


@lru_cache(64)
def font(size, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf'),
                  Path(matplotlib.get_data_path()) / 'fonts' / 'ttf' /
                  ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise RuntimeError('No suitable text font is available.')


@lru_cache(256)
def equation(tex, size=32, color=INK):
    buff = BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$' + tex + '$', buff, format='png', dpi=150, color=color,
                      prop=FontProperties(size=size * 72 / 150))
    buff.seek(0)
    return Image.open(buff).convert('RGBA')


def smooth(t, start, end):
    u = float(np.clip((t-start)/(end-start), 0, 1))
    return u*u*(3-2*u)


def sweep(seconds):
    if seconds < 3.5:
        x = 0.0
    elif seconds < 5.5:
        x = .55*smooth(seconds, 3.5, 5.5)
    elif seconds < 6:
        x = .55
    elif seconds < 8:
        x = .55-1.10*smooth(seconds, 6, 8)
    elif seconds < 8.5:
        x = -.55
    elif seconds < 10:
        x = -.55*(1-smooth(seconds, 8.5, 10))
    else:
        x = 0.0
    return x


def state(seconds):
    x = sweep(seconds if seconds < 18 else seconds-16.5)
    a2 = 1.6-.6*smooth(seconds, 14, 18)
    if seconds < 11:
        caption = 'Unequal factors · phase and action predict different collision points'
    elif seconds < 18:
        caption = 'Test two conversion factors · hold the collision point at X = 0'
    elif seconds < 26.5:
        caption = 'Equal factors · repeat the same collision-point sweep'
    else:
        caption = 'Equal factors · phase and action predict the same collision point'
    return dict(x=x, a2=a2, caption=caption)


def phases(x):
    q = np.asarray(x)[..., None]-ENDPOINT_X
    return -2*KAPPAS*np.sqrt(T*T-q*q)


def derivatives(x):
    q = np.asarray(x)[..., None]-ENDPOINT_X
    return 2*KAPPAS*q/np.sqrt(T*T-q*q)


def changes(x, a2):
    dp = phases(x)-phases(0.)
    return np.sum(dp, axis=-1), dp[..., 0]+a2*dp[..., 1]


def action_root(a2):
    lo, hi = -X_LIMIT, X_LIMIT
    for _ in range(64):
        mid = (lo+hi)/2
        slopes = derivatives(mid)
        if slopes[0]+a2*slopes[1] > 0:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la'):
        box = self.d.textbbox((x, y), str(value), font=font(size, bold), anchor=anchor)
        self.boxes.append((str(value), tuple(box)))
        self.d.text((x, y), str(value), font=font(size, bold), fill=color, anchor=anchor)

    def math(self, x, y, tex, size=32, color=INK, maxwidth=None):
        pic = equation(tex, size, color)
        if maxwidth and pic.width > maxwidth:
            pic = pic.resize((maxwidth, round(pic.height*maxwidth/pic.width)), Image.Resampling.LANCZOS)
        left, top = round(x-pic.width/2), round(y-pic.height/2)
        self.im.paste(pic, (left, top), pic)
        self.boxes.append((tex, (left, top, left+pic.width, top+pic.height)))

    def line(self, points, color=INK, width=2):
        self.d.line([tuple(p) for p in points], fill=color, width=width, joint='curve')

    def dash(self, a, b, color=GRID, width=2, dash=8, gap=7):
        a, b = np.asarray(a, float), np.asarray(b, float)
        length = float(np.linalg.norm(b-a))
        if length < 1:
            return
        direction = (b-a)/length
        for distance in np.arange(0, length, dash+gap):
            self.line([a+distance*direction, a+min(distance+dash, length)*direction], color, width)

    def arrow(self, a, b, color=GRID, width=2, head=10):
        a, b = np.asarray(a, float), np.asarray(b, float)
        self.line([a, b], color, width)
        u = (b-a)/np.linalg.norm(b-a)
        v = np.array([-u[1], u[0]])
        self.d.polygon([tuple(b), tuple(b-head*u+.45*head*v), tuple(b-head*u-.45*head*v)], fill=color)

    def dot(self, p, color=INK, radius=6, ring=False):
        x, y = p
        self.d.ellipse((x-radius, y-radius, x+radius, y+radius),
                       fill=PANEL if ring else color, outline=color, width=3)

    def panel(self, box):
        self.d.rounded_rectangle(box, radius=18, fill=PANEL, outline=BORDER, width=2)


def incoming_wave_numbers(x):
    velocity = (x-ENDPOINT_X)/T
    return KAPPAS*velocity/np.sqrt(1-velocity*velocity)


def packet_profiles(x, displacement):
    """Normalized Gaussian snapshots with each candidate's incoming mean k."""
    displacement = np.asarray(displacement)
    envelope = np.exp(-.5*(displacement/PACKET_SIGMA)**2)
    phase = displacement[..., None]*incoming_wave_numbers(x)+phases(x)/2
    normalization = 1/math.sqrt(PACKET_SIGMA*math.sqrt(math.pi))
    return normalization*envelope[..., None]*np.exp(1j*phase)


def collision_packets(c, vertex, x, pixels_per_x):
    """Two separate real-part profiles under a shared amplitude envelope."""
    d = np.linspace(-3.5*PACKET_SIGMA, 3.5*PACKET_SIGMA, 600)
    envelope = np.exp(-.5*(d/PACKET_SIGMA)**2)
    profiles = packet_profiles(x, d)*math.sqrt(PACKET_SIGMA*math.sqrt(math.pi))
    xp = vertex[0]+pixels_per_x*d
    height = 38
    top = np.c_[xp, vertex[1]-height*envelope]
    bottom = np.c_[xp, vertex[1]+height*envelope]
    c.d.polygon([tuple(p) for p in np.concatenate((top, bottom[::-1]))], fill=PANEL)
    # This shared envelope is a guide, not the sum of the two particle states.
    for curve in (top, bottom):
        for j in range(0, len(d)-1, 18):
            c.line(curve[j:min(j+10, len(d))], MUTED, 1)
    c.line([(xp[0], vertex[1]), (xp[-1], vertex[1])], GRID, 1)
    for i, color in enumerate((BLUE, GOLD)):
        c.line(np.c_[xp, vertex[1]-height*profiles[:, i].real], color, 2)


def worldlines(c, st):
    c.panel((48, 162, 663, 623))
    c.text(72, 182, 'Candidate collision', 26, bold=True)
    c.text(72, 220, 'Incoming amplitude profiles at t = 0', 22, MUTED)
    x0, y0, xs, ts = 379, 405, 82, 30
    px = lambda x: x0+xs*x
    py = lambda t: y0-ts*t
    c.arrow((95, y0), (613, y0))
    c.arrow((x0, 558), (x0, 261))
    c.text(616, y0-15, 'x', 23, MUTED)
    c.text(x0+13, 254, 't', 23, MUTED)
    c.math(600, py(T), '+T', 22, MUTED)
    c.math(600, py(-T), '-T', 22, MUTED)
    vertex = (px(st['x']), y0)
    for i, color in enumerate((BLUE, GOLD)):
        ends = [(px(ENDPOINT_X[i]), py(t)) for t in (-T, T)]
        base, panel = np.array(ImageColor.getrgb(color)), np.array(ImageColor.getrgb(PANEL))
        light = tuple(np.rint(.55*base+.45*panel).astype(int))
        c.line([ends[0], vertex, ends[1]], light, 3)
        for ex, ey in ends:
            c.d.rectangle((ex-6, ey-6, ex+6, ey+6), fill=PANEL, outline=color, width=3)
        c.math(px(ENDPOINT_X[i]), 265, rf'\kappa_{i+1}={KAPPAS[i]:g}', 25, color)
    collision_packets(c, vertex, st['x'], xs)
    wave_numbers = incoming_wave_numbers(st['x'])
    c.text(108, 540, f'k₁ = {wave_numbers[0]:+.2f}', 25, BLUE)
    c.text(430, 540, f'k₂ = {wave_numbers[1]:+.2f}', 25, GOLD)
    c.text(75, 580, 'Fixed endpoints', 21, MUTED)
    c.d.rectangle((242, 589, 252, 599), fill=PANEL, outline=MUTED, width=2)
    c.math(412, 594, rf'X={st["x"]:+.2f}' if abs(st['x'])>.00001 else 'X=0', 28)
    c.text(558, 580, 'T = 4', 21, MUTED)


def curves(c, st):
    c.panel((687, 162, 1552, 623))
    c.text(711, 182, 'Changes relative to X = 0', 26, bold=True)
    c.dash((718, 241), (756, 241), INK, 3, 8, 5)
    c.text(770, 225, 'Total phase', 23)
    c.line([(989, 241), (1027, 241)], GREEN, 4)
    c.text(1041, 225, 'Total action', 23, GREEN)
    left, right, top, bottom = 802, 1485, 278, 553
    phase_scale = KAPPAS[0]
    ymin, ymax = -.32*phase_scale, 1.90*phase_scale
    px = lambda x: left+(x+X_LIMIT)/(2*X_LIMIT)*(right-left)
    py = lambda y: bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
    for value in (0., phase_scale):
        c.line([(left, py(value)), (right, py(value))], GRID, 1)
        c.text(left-18, py(value), f'{value:g}', 21, MUTED, anchor='rm')
    c.arrow((left-8, py(0)), (right+18, py(0)), GRID, 2)
    c.arrow((px(0), bottom), (px(0), top-5), GRID, 2)
    c.text(right+29, py(0)-18, 'X', 23, MUTED)
    for value in (-.7, .7):
        c.line([(px(value), py(0)-5), (px(value), py(0)+5)], MUTED, 1)
        c.text(px(value), py(0)+13, f'{value:+.1f}', 20, MUTED, anchor='ma')
    xx = np.linspace(-X_LIMIT, X_LIMIT, 500)
    p, s = changes(xx, st['a2'])
    c.line(np.c_[px(xx), py(s)], GREEN, 5)
    # A neutral dashed curve remains identifiable when both totals coincide.
    phase_points = np.c_[px(xx), py(p)]
    for idx in range(0, len(xx)-1, 11):
        c.line(phase_points[idx:min(idx+7, len(xx))], INK, 3)
    root = action_root(st['a2'])
    root_y = changes(root, st['a2'])[1]
    rail_y = 570
    c.dash((px(0), py(0)+10), (px(0), rail_y), INK, 1, 4, 5)
    c.dash((px(root), py(root_y)+10), (px(root), rail_y), GREEN, 1, 4, 5)
    c.line([(px(0), rail_y), (px(root), rail_y)], GREEN, 3)
    c.line([(px(0), rail_y-4), (px(0), rail_y+4)], INK, 2)
    c.line([(px(root), rail_y-4), (px(root), rail_y+4)], GREEN, 2)
    c.dot((px(root), py(root_y)), GREEN, 8)
    c.dot((px(0), py(0)), INK, 5, ring=True)
    if abs(st['x']) > .003:
        pnow, snow = changes(st['x'], st['a2'])
        c.dash((px(st['x']), py(max(pnow, snow)) - 14), (px(st['x']), bottom), MUTED, 1)
        c.dot((px(st['x']), py(snow)), GREEN, 7)
        c.dot((px(st['x']), py(pnow)), INK, 4, ring=abs(pnow-snow)<1.e-10)
    c.text(1120, 587, f'Stationary points:  phase 0.000    action {root:+.3f}', 22, MUTED, anchor='ma')


def slope_panel(c, st):
    c.panel((48, 648, 1552, 830))
    c.text(72, 665, 'First-order response at X = 0', 25, bold=True)
    c.line([(862, 672), (862, 807)], BORDER, 2)
    derivative = float(derivatives(0.)[0])
    c.math(267, 733, r'\phi_1^{\prime}(0)=+'+f'{derivative:g}', 33, BLUE)
    c.math(632, 733, r'\phi_2^{\prime}(0)=-'+f'{derivative:g}', 33, GOLD)
    c.math(450, 790, r'\phi_{\mathrm{total}}^{\prime}(0)=0', 34)
    c.text(1207, 665, 'Trial conversion factors' if st['a2']>1.000001 else 'Shared conversion factor',
           25, bold=True, anchor='ma')
    c.math(1207, 724, r'a_1=1.00,\quad a_2='+f'{st["a2"]:.2f}', 31)
    slope = derivative*(1-st['a2'])
    value = '0' if abs(slope)<1.e-9 else f'{slope:.2f}'
    c.math(1207, 787, r'S_{\mathrm{total}}^{\prime}(0)='+f'{derivative:g}'+r'(a_1-a_2)='+value, 32, GREEN, maxwidth=622)


def frame(seconds, inspect=False):
    st = state(seconds)
    c = Canvas()
    c.text(48, 35, 'A shared scale for phase and action', 41, bold=True)
    c.text(48, 99, st['caption'], 26, MUTED)
    c.math(1280, 68, r'S_i=a_i\phi_i,\quad a_i=\frac{m_i}{\kappa_i}', 39)
    worldlines(c, st)
    curves(c, st)
    slope_panel(c, st)
    c.line([(48, 846), (1552, 846)], GRID, 2)
    c.line([(48, 846), (48+1504*np.clip(seconds/DURATION, 0, 1), 846)], GOLD, 3)
    c.text(48, 859, 'Vary X, not time · fixed packet envelopes · negligible interaction contribution · illustrative units', 21, MUTED)
    return (c.im, c.boxes) if inspect else c.im


def review():
    OUT.mkdir(parents=True, exist_ok=True)
    for index, seconds in enumerate(REVIEW_TIMES):
        image = frame(seconds)
        image.save(OUT / f'{STEM}-review-{index+1:02d}.png')
    # Full-width paired stages remain large enough to inspect mathematical labels.
    sheet = Image.new('RGB', (1600, math.ceil(len(REVIEW_TIMES)/2)*478), BG)
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(REVIEW_TIMES):
        left, top = index % 2 * 800, index // 2 * 478
        draw.text((left+18, top+4), f'{seconds:g} s', font=font(20), fill=MUTED)
        sheet.paste(frame(seconds).resize((800, 450), Image.Resampling.LANCZOS), (left, top+28))
    sheet.save(OUT / f'{STEM}-contact-sheet.jpg', quality=96)
    frame(28).save(OUT / f'{STEM}-poster.png')


def validate():
    xx = np.linspace(-X_LIMIT, X_LIMIT, 2001)
    proper_square = T*T-(xx[:, None]-ENDPOINT_X)**2
    slopes = derivatives(0.)
    trial_root = action_root(1.6)
    shared_root = action_root(1.)
    assert np.min(proper_square) > 0
    expected = 2*KAPPAS[0]
    assert abs(slopes[0]-expected) < 1e-12 and abs(slopes[1]+expected) < 1e-12
    assert abs(sum(slopes)) < 1e-12
    assert abs(slopes[0]+1.6*slopes[1]+.6*expected) < 1e-12
    assert abs(shared_root) < 1e-12 and .31 < trial_root < .32
    h = 1e-5
    finite_differences = (phases(h)-phases(-h))/(2*h)
    derivative_error = float(np.max(abs(finite_differences-slopes)))
    assert derivative_error < 1e-8
    for a2 in np.linspace(1, 1.6, 61):
        root = action_root(a2)
        d = derivatives(root)
        assert abs(d[0]+a2*d[1]) < 1e-12
    timeline = [state(float(t)) for t in np.linspace(0, DURATION, 577)]
    assert all(abs(v['x']) <= .55+1e-12 for v in timeline)
    assert all(state(float(t))['x'] == 0 for t in np.linspace(10, 20, 101))
    assert all(state(float(t))['a2'] == 1 for t in np.linspace(18, DURATION, 121))
    for t in np.linspace(3.5, 10, 157):
        assert abs(state(float(t))['x']-state(float(t+16.5))['x']) < 1.e-12
        p, s = changes(state(float(t+16.5))['x'], 1.)
        assert abs(p-s) < 1.e-12
    for x in np.linspace(-.55, .55, 51):
        wave_numbers = incoming_wave_numbers(x)
        omega = np.sqrt(wave_numbers**2+KAPPAS**2)
        assert np.allclose(wave_numbers/omega, (x-ENDPOINT_X)/T, atol=1.e-12)
        assert np.allclose(omega**2-wave_numbers**2, KAPPAS**2, atol=1.e-10)
        assert np.allclose(2*wave_numbers, derivatives(x), atol=1.e-12)
        d = np.linspace(-8*PACKET_SIGMA, 8*PACKET_SIGMA, 4097)
        profiles = packet_profiles(x, d)
        norms = np.sum(abs(profiles)**2, axis=0)*(d[1]-d[0])
        assert np.allclose(norms, 1., atol=1.e-10)
        assert np.allclose(np.angle(profiles[2049]/profiles[2048])/(d[1]-d[0]), wave_numbers, atol=1.e-9)
    text_errors = []
    overlap_errors = []
    for seconds in REVIEW_TIMES:
        _, boxes = frame(seconds, inspect=True)
        for text, (x0, y0, x1, y1) in boxes:
            if min(x0, y0) < 0 or x1 > W or y1 > H:
                text_errors.append(dict(time=seconds, text=text, box=[x0, y0, x1, y1]))
        for i, (text_a, a) in enumerate(boxes):
            for text_b, b in boxes[i+1:]:
                if min(a[2], b[2])-max(a[0], b[0]) > 0 and min(a[3], b[3])-max(a[1], b[1]) > 0:
                    overlap_errors.append(dict(time=seconds, first=text_a, second=text_b))
    assert not text_errors, text_errors
    assert not overlap_errors, overlap_errors
    report = dict(model='Fixed-endpoint free timelike collision legs; local interaction contribution neglected',
                  dimensions=[W, H], fps=FPS, duration_seconds=DURATION, frames=round(FPS*DURATION),
                  parameters=dict(c=1, T=T, kappas=KAPPAS.tolist(), endpoint_x=ENDPOINT_X.tolist(), x_domain=[-X_LIMIT, X_LIMIT]),
                  minimum_timelike_interval_squared=float(np.min(proper_square)),
                  phase_derivatives_at_zero=slopes.tolist(), total_phase_derivative_at_zero=float(sum(slopes)),
                  trial_a2=1.6, trial_action_derivative_at_zero=float(slopes[0]+1.6*slopes[1]),
                  trial_stationary_action_vertex=trial_root, shared_stationary_action_vertex=shared_root,
                  derivative_finite_difference_error=derivative_error,
                  fixed_vertex_during_factor_test=True, no_physical_time_animation=True,
                  graph_shows_exact_changes=True, derivative_panel_is_first_order=True,
                  repeated_equal_factor_sweep=True, equal_factor_sweep_seconds=[20, 26.5],
                  incoming_gaussian_packets=True, packet_sigma=PACKET_SIGMA,
                  packet_centers_at_candidate_vertex=True,
                  packet_wave_numbers_from_candidate_velocity=True,
                  packet_norms_and_local_phase_gradient='passed',
                  packet_snapshot_family_not_scattering_simulation=True,
                  equal_factor_final_hold_seconds=3.5, review_times=REVIEW_TIMES,
                  text_bounds_errors=text_errors, text_overlap_errors=overlap_errors,
                  numerical_validation='passed')
    (OUT / f'{STEM}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    return report


def encoded_reviews(target):
    for seconds, suffix in [(5.5, 'encoded-variation'), (16, 'encoded-transition'),
                            (22, 'encoded-equal-sweep'), (28, 'encoded-frame')]:
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
                        '-ss', str(seconds), '-i', str(target), '-frames:v', '1', '-y',
                        str(OUT / f'{STEM}-{suffix}.png')], check=True)


def render():
    target = OUT / f'{STEM}.mp4'
    writer = imageio_ffmpeg.write_frames(str(target), (W, H), fps=FPS, codec='libx264',
                                        pix_fmt_in='rgb24', pix_fmt_out='yuv420p',
                                        output_params=['-crf', '18', '-preset', 'medium', '-movflags', '+faststart'],
                                        macro_block_size=2)
    writer.send(None)
    for index in range(round(FPS*DURATION)):
        writer.send(np.asarray(frame(index/FPS)))
    writer.close()
    encoded_reviews(target)
    count, duration = imageio_ffmpeg.count_frames_and_secs(str(target))
    assert count == round(FPS*DURATION) and abs(duration-DURATION) < 1/FPS
    reader = imageio_ffmpeg.read_frames(str(target))
    metadata = next(reader)
    reader.close()
    assert metadata['size'] == (W, H) and metadata['fps'] == FPS
    report_path = OUT / f'{STEM}-validation.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    report['encoded_video'] = dict(decoded_frames=count, duration_seconds=duration,
                                   dimensions=list(metadata['size']), fps=metadata['fps'],
                                   codec=metadata['codec'], file_bytes=target.stat().st_size)
    report_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'Rendered {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    review()
    validate()
    if args.render:
        render()
