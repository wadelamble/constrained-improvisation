"""Landscape adaptation of the revised commutator-sphere reel.

Run with --render --check. Blue is Rx(theta) Ry(theta) v, coral is
Ry(theta) Rx(theta) v. Their difference approaches theta^2 Jz v.
The connected magnifier applies the same orthographic camera and an exact
1/theta^2 scale. That numeric scale is intentionally absent from the image.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
import imageio_ffmpeg

NAME = 'symmetry-commutator-sphere'
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools/commutator-desktop-review'
W, H, FPS, DURATION = 1600, 900, 24, 54
BG, PANEL, INK, MUTED = '#fffcf6', '#f5f1e8', '#232426', '#77746e'
GRID, FAINT = '#bdb8ae', '#e4ded3'
BLUE, RED, GOLD, GREEN = '#396fa8', '#bb4c40', '#a96d15', '#32866c'
INITIAL, MID, FINAL = .8, .4, .02
V = np.array([1., 6., 8.]) / math.sqrt(101)
DEPTH = np.array([2., -3., 5.]) / math.sqrt(38)
RIGHT = np.array([3., 2., 0.]) / math.sqrt(13)
UP = np.array([-10., 15., 13.]) / math.sqrt(494)
CAMERA = np.array([RIGHT, -UP])
J = np.array([[[0, 0, 0], [0, 0, -1], [0, 1, 0]],
              [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
              [[0, -1, 0], [1, 0, 0], [0, 0, 0]]], dtype=float)
ORIGIN, SCALE = np.array([465., 495.]), 278.
INSET = (950, 360, 1520, 640)
INSET_CENTER = np.array([1235., 500.])
MOMENTS = [0, 4, 8, 11, 14.5, 19, 22, 26, 29.5, 33, 37, 41, 44.5, 47, 50, 53]
STAGES = [(0, 'A fixed-length vector on a sphere.'),
          (2, 'First, turn about y.'),
          (6.3, 'Then turn about x.'),
          (9.8, 'Keep the blue result.'),
          (11.5, 'Start again from the same vector.'),
          (12.8, 'Now turn about x.'),
          (17, 'Then turn about y.'),
          (20.5, 'The same turns end at different points.'),
          (24, 'Reduce both rotation angles.'),
          (28, 'Enlarge the gap between the endpoints.'),
          (31, 'Keep enlarging the shrinking gap.'),
          (42, 'Compare with a turn about z.'),
          (46, 'Move this tangent to compare the changes.'),
          (48, 'The enlarged gap approaches the z tangent.')]


def ease(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


def progress(t, start, end):
    return ease((t-start)/(end-start))


def lerp(a, b, u):
    return a+(b-a)*u


def mix(color, strength=1., background=BG):
    a = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])
    b = np.array([int(background[i:i+2], 16) for i in (1, 3, 5)])
    return tuple(np.rint(b+(a-b)*np.clip(strength, 0, 1)).astype(int))


@lru_cache(64)
def font(size=26, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('seguisb.ttf' if bold else 'segoeui.ttf'),
                  Path(matplotlib.get_data_path()) / 'fonts/ttf' /
                  ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError('No text font')


@lru_cache(128)
def equation(tex, size=32, color=INK):
    stream = BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$'+tex+'$', stream, format='png', dpi=180, color=color,
                      prop=matplotlib.font_manager.FontProperties(size=size*72/180))
    stream.seek(0)
    return Image.open(stream).convert('RGBA')


class Canvas:
    def __init__(self, image=None):
        self.im = image.copy() if image is not None else Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []

    def track(self, box, name):
        assert box[0] >= 8 and box[1] >= 8 and box[2] <= W-8 and box[3] <= H-8, (name, box)
        self.boxes.append((box, name))

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la'):
        f = font(size, bold)
        self.track(self.d.textbbox((x, y), value, font=f, anchor=anchor), value)
        self.d.text((x, y), value, font=f, fill=color, anchor=anchor)

    def math(self, x, y, tex, size=32, color=INK, center=False, backing=False):
        pic = equation(tex, size, color)
        px, py = round(x-pic.width/2) if center else round(x), round(y-pic.height/2)
        self.track((px, py, px+pic.width, py+pic.height), tex)
        if backing:
            self.d.rounded_rectangle((px-5, py-3, px+pic.width+5, py+pic.height+3), radius=3, fill=BG)
        self.im.paste(pic, (px, py), pic)

    def line(self, points, color=GRID, width=2):
        self.d.line([tuple(p) for p in points], fill=color, width=width, joint='curve')

    def arrow(self, start, end, color, width=5, head=16):
        a, b = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
        u = b-a
        length = np.linalg.norm(u)
        if length < .5:
            return
        u /= length
        n = np.array([-u[1], u[0]])
        head = min(head, length*.5)
        self.line([a, b], color, width)
        self.d.polygon([tuple(b), tuple(b-head*u+.42*head*n), tuple(b-head*u-.42*head*n)], fill=color)

    def dot(self, point, radius=6, color=INK):
        x, y = point
        self.d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)


def rotation3(axis, theta):
    g = J[axis]
    return np.eye(3)+math.sin(theta)*g+(1-math.cos(theta))*(g@g)


def project(q):
    return ORIGIN+SCALE*(np.asarray(q)@CAMERA.T)


def angle_at(t):
    if t < 24:
        return INITIAL
    if t < 28:
        return lerp(INITIAL, MID, progress(t, 24, 28))
    if t < 31:
        return MID
    if t < 40:
        return math.exp(lerp(math.log(MID), math.log(FINAL), progress(t, 31, 40)))
    return FINAL


def route(theta, first_axis, second_axis, first=1., second=1., samples=85):
    leg1 = np.array([rotation3(first_axis, a)@V for a in np.linspace(0, theta*first, samples)])
    leg2 = np.array([rotation3(second_axis, a)@leg1[-1] for a in np.linspace(0, theta*second, samples)])
    return leg1, leg2


def full_results(theta):
    return rotation3(0, theta)@rotation3(1, theta)@V, rotation3(1, theta)@rotation3(0, theta)@V


def dash(s, start, end, color=MUTED, width=2, dash_length=8):
    start, end = np.asarray(start), np.asarray(end)
    d = end-start
    length = np.linalg.norm(d)
    if length < .1:
        return
    for z in np.arange(0, length, dash_length*1.8):
        s.line([start+d*z/length, start+d*min(z+dash_length, length)/length], color, width)


def hollow(s, p, color, radius=7, width=3):
    x, y = p
    s.d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=BG, outline=color, width=width)


def sphere_curves():
    curves = []
    a = np.linspace(0, 2*math.pi, 181)
    for latitude in np.linspace(-math.pi/3, math.pi/3, 5):
        curves.append(np.c_[np.cos(a)*math.cos(latitude), np.sin(a)*math.cos(latitude),
                            np.full_like(a, math.sin(latitude))])
    for longitude in np.linspace(0, math.pi, 6, endpoint=False):
        curves.append(np.c_[np.cos(a)*math.cos(longitude), np.cos(a)*math.sin(longitude), np.sin(a)])
    return curves


GRID_CURVES = sphere_curves()


@lru_cache(1)
def base():
    s = Canvas()
    s.text(52, 38, 'What the Commutator Measures', 36, INK, bold=True)
    x, y = ORIGIN
    s.d.ellipse((x-SCALE, y-SCALE, x+SCALE, y+SCALE), fill=PANEL, outline=GRID, width=2)
    for curve in GRID_CURVES:
        pp = project(curve)
        for i in range(len(curve)-1):
            front = DEPTH@((curve[i]+curve[i+1])*.5) >= 0
            if front or i%4 < 2:
                s.line(pp[i:i+2], '#c4bfb4' if front else '#ded8cb', 2 if front else 1)
    for axis, name in zip(np.eye(3), 'xyz'):
        dash(s, project(-1.15*axis), ORIGIN, '#c7c1b5', 2, 7)
        s.arrow(ORIGIN, project(1.18*axis), '#969187', 2, 10)
        s.math(*project(1.29*axis), name, 28, MUTED, center=True, backing=True)
    s.dot(ORIGIN, 4, MUTED)
    s.line([(52, 827), (1548, 827)], FAINT, 2)
    s.text(52, 850, 'Rotations in three dimensions', 20, MUTED)
    return s.im


def active_axis(s, axis, color):
    direction = np.eye(3)[axis]
    s.arrow(ORIGIN, project(1.18*direction), mix(color, .8), 4, 13)
    s.math(*project(1.29*direction), 'xyz'[axis], 28, color, center=True, backing=True)


def draw_route(s, legs, color, strength=1.):
    color = mix(color, strength)
    for leg in legs:
        if np.linalg.norm(leg[-1]-leg[0]) > .002:
            points = project(leg)
            s.line(points, color, 4)
            if np.linalg.norm(points[-1]-points[0]) > 12:
                s.arrow(points[-4], points[-1], color, 4, 12)
    if np.linalg.norm(legs[0][-1]-V) > .03:
        hollow(s, project(legs[0][-1]), color, 5, 2)


def vector(s, endpoint, color, strength=1., width=5):
    color = mix(color, strength)
    s.arrow(ORIGIN, project(endpoint), color, width, 17)
    s.dot(project(endpoint), 7, color)


def magnifier_geometry(theta):
    blue, red = full_results(theta)
    middle, zoom = (blue+red)*.5, theta**-2
    def pp(p):
        return INSET_CENTER+SCALE*zoom*((np.asarray(p)-middle)@CAMERA.T)
    half = np.array([(INSET[2]-INSET[0])/2, (INSET[3]-INSET[1])/2])/zoom
    return pp, zoom, project(middle), half


def tangent(s, start, end, color=GREEN, strength=1., width=5):
    color = mix(color, strength)
    dash(s, start, end, color, width, 10)
    d = np.asarray(end)-start
    length = np.linalg.norm(d)
    if length > 15:
        s.arrow(np.asarray(end)-d/length*19, end, color, width, 17)
    x, y = end
    s.d.ellipse((x-10, y-10, x+10, y+10), outline=color, width=3)


def inset(s, theta, t):
    alpha = progress(t, 28, 28.8)
    pp, zoom, center, half = magnifier_geometry(theta)
    left, top = center-half
    right, bottom = center+half
    color = mix(MUTED, .45*alpha)
    s.d.rectangle((left, top, right, bottom), outline=color, width=2)
    s.d.ellipse((center[0]-10, center[1]-10, center[0]+10, center[1]+10), outline=color, width=2)
    dash(s, (right, top), (INSET[0], INSET[1]), color, 2, 8)
    dash(s, (right, bottom), (INSET[0], INSET[3]), color, 2, 8)
    layer = Canvas()
    layer.d.rectangle(INSET, fill=PANEL)
    for curve in GRID_CURVES:
        for i in range(0, len(curve)-1, 2):
            if DEPTH@curve[i] > 0:
                layer.line(pp(curve[i:i+3]), '#dcd6c9', 2)
    for first, second, col in ((1, 0, BLUE), (0, 1, RED)):
        for leg in route(theta, first, second, samples=130):
            layer.line(pp(leg), mix(col, .45, PANEL), 3)
    blue, red = full_results(theta)
    bp, rp = pp(blue), pp(red)
    layer.arrow(rp, bp, GOLD, 6, 18)
    if t >= 48:
        tangent(layer, rp, rp+SCALE*(CAMERA@(J[2]@V)), GREEN)
    layer.dot(rp, 8, RED)
    layer.dot(bp, 8, BLUE)
    s.im.paste(Image.blend(s.im.crop(INSET), layer.im.crop(INSET), alpha), INSET[:2])
    s.d.rounded_rectangle(INSET, radius=10, outline=mix(MUTED, alpha), width=2)
    s.text(INSET_CENTER[0], 331, 'Same gap, enlarged', 27, mix(INK, alpha), anchor='mm')
    if t >= 46:
        dash(s, (1150, 675), (1205, 675), GREEN, 4, 9)
        s.math(1230, 675, r'J_zv', 31, GREEN)
    return bp, rp


def z_reference(s, t, red_inset):
    reveal = progress(t, 42, 43)
    orbit = np.array([rotation3(2, a)@V for a in np.linspace(-.35, .42, 90)])
    s.line(project(orbit), mix(GREEN, .65*reveal), 4)
    turn = .25*progress(t, 42.5, 44.5)
    s.dot(project(rotation3(2, turn)@V), 7, mix(GREEN, reveal))
    if t >= 44:
        amount = progress(t, 44, 45.3)
        start, delta = project(V), SCALE*(CAMERA@(J[2]@V))
        tangent(s, start, start+delta*amount, GREEN, .7)
        if t < 46:
            s.math(start[0]+delta[0]/2-20, start[1]+delta[1]/2-30,
                   r'J_zv', 29, GREEN, center=True, backing=True)
    if 46 <= t < 48:
        start = lerp(project(V), red_inset, progress(t, 46, 48))
        tangent(s, start, start+SCALE*(CAMERA@(J[2]@V)), GREEN)
    active_axis(s, 2, GREEN)


def render(t):
    t = float(np.clip(t, 0, DURATION))
    s = Canvas(base())
    stage = next(label for start, label in reversed(STAGES) if t >= start)
    s.text(52, 96, stage, 27, MUTED)
    theta = angle_at(t)
    blue_legs = route(theta, 1, 0, progress(t, 2, 5.5), progress(t, 6.3, 9.8))
    red_legs = route(theta, 0, 1, progress(t, 12.8, 16.3), progress(t, 17, 20.5))
    blue, red = blue_legs[-1][-1], red_legs[-1][-1]
    red_visible = progress(t, 11.5, 12.3)
    for y, color, title, tex, visibility in (
        (190, BLUE, '1. y then x', r'R_x(\theta)R_y(\theta)v', 1.),
        (266, RED, '2. x then y', r'R_y(\theta)R_x(\theta)v', .28+.72*red_visible)):
        s.text(930, y, title, 26, mix(color, visibility), bold=True, anchor='lm')
        s.math(1150, y, tex, 30, color)
    dash(s, ORIGIN, project(V), mix(INK, .45), 3, 8)
    hollow(s, project(V), INK, 8, 2)
    s.math(project(V)[0]+26, project(V)[1]-26, 'v', 30, center=True, backing=True)
    reduced = .35 if t >= 42 else 1.
    draw_route(s, blue_legs, BLUE, (.65 if t >= 11.5 else 1.)*reduced)
    vector(s, blue, BLUE, .85*reduced if t >= 11.5 else 1.)
    if red_visible:
        draw_route(s, red_legs, RED, red_visible*reduced)
        vector(s, red, RED, red_visible*reduced)
    if 2 <= t < 5.5:
        active_axis(s, 1, BLUE)
    elif 6.3 <= t < 9.8:
        active_axis(s, 0, BLUE)
    elif 12.8 <= t < 16.3:
        active_axis(s, 0, RED)
    elif 17 <= t < 20.5:
        active_axis(s, 1, RED)
    if t >= 20.5:
        a, b = project(red), project(blue)
        if np.linalg.norm(b-a) > 2:
            s.arrow(a, b, GOLD, 4, min(16, max(5, .35*np.linalg.norm(b-a))))
    if 20.5 <= t < 28:
        s.text(1235, 430, 'The gap points from coral to blue.', 27, GOLD, anchor='mm')
        s.math(1235, 510, r'\Delta v=(R_xR_y-R_yR_x)v', 33, center=True)
    elif t >= 28:
        _, rp = inset(s, theta, t)
        if t >= 42:
            z_reference(s, t, rp)
        if t >= 48:
            s.math(1235, 750, r'[J_x,J_y]v=J_zv', 42, center=True)
        elif t >= 42:
            s.text(1235, 744, 'Green is the tangent generated by Jz.', 25, GREEN, anchor='mm')
    s.line([(52, 827), (52+1496*t/DURATION, 827)], GOLD, 3)
    # Every dynamic text box is checked on every encoded frame.
    for i, (a, name_a) in enumerate(s.boxes):
        for b, name_b in s.boxes[i+1:]:
            overlap_w = min(a[2], b[2])-max(a[0], b[0])
            overlap_h = min(a[3], b[3])-max(a[1], b[1])
            assert overlap_w <= 0 or overlap_h <= 0, (t, name_a, name_b)
    return s.im


def validate():
    assert np.isclose(np.linalg.norm(V), 1)
    assert np.allclose(CAMERA@CAMERA.T, np.eye(2)) and np.allclose(CAMERA@DEPTH, 0)
    assert np.array_equal(J[0]@J[1]-J[1]@J[0], J[2])
    errors = []
    for theta in (.8, .4, .2, .1, .02, .001, .0001):
        blue, red = full_results(theta)
        assert np.isclose(np.linalg.norm(blue), 1) and np.isclose(np.linalg.norm(red), 1)
        difference = (blue-red)/theta**2
        errors.append(float(np.linalg.norm(difference-J[2]@V)))
        pp, _, _, _ = magnifier_geometry(theta)
        assert np.allclose(pp(blue)-pp(red), SCALE*CAMERA@difference)
        for a, b in ((1, 0), (0, 1)):
            legs = route(theta, a, b)
            assert all(np.allclose(np.linalg.norm(leg, axis=1), 1) for leg in legs)
            assert np.allclose(legs[-1][-1], rotation3(b, theta)@rotation3(a, theta)@V)
    assert all(b < a for a, b in zip(errors, errors[1:])) and errors[-1] < .0002
    routes = np.concatenate([leg for a, b in ((1, 0), (0, 1)) for leg in route(INITIAL, a, b)])
    assert np.min(routes@DEPTH) > .2
    for theta in np.geomspace(MID, FINAL, 130):
        pp, _, _, _ = magnifier_geometry(theta)
        blue, red = full_results(theta)
        pts = np.array([pp(blue), pp(red), pp(red)+SCALE*CAMERA@(J[2]@V)])
        assert pts[:, 0].min() > INSET[0]+20 and pts[:, 0].max() < INSET[2]-20
        assert pts[:, 1].min() > INSET[1]+15 and pts[:, 1].max() < INSET[3]-15
    return dict(unit_sphere='preserved', rotation_order='verified', blue_minus_coral='positive Jz',
                inset_geometry='same camera, exact 1/theta^2 magnification',
                reference_vector='Jz v, translated only', limit_errors=errors,
                size=[W, H], fps=FPS, duration_seconds=DURATION,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1600, math.ceil(len(MOMENTS)/4)*250), BG)
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(MOMENTS):
        im = render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        x, y = i%4*400, i//4*250
        sheet.paste(im.resize((400, 225), Image.Resampling.LANCZOS), (x, y))
        draw.text((x+12, y+228), f'{t}s', fill=MUTED, font=font(17))
    sheet.save(REVIEW/'contact.png')
    render(50).save(OUT/f'{NAME}-poster.png')


def encode():
    destination = OUT/f'{NAME}.mp4'
    temporary = REVIEW/f'{NAME}.rendering.mp4'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
               '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
               '-threads', '2', str(temporary)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for i in range(DURATION*FPS):
                process.stdin.write(render(i/FPS).tobytes())
                if i % (FPS*9) == 0:
                    print(f'Rendered {i/FPS:.0f}/{DURATION} seconds', flush=True)
            process.stdin.close()
            if process.wait():
                raise RuntimeError('FFmpeg encoding failed')
        except BaseException:
            process.kill()
            raise
    temporary.replace(destination)


def check_video():
    video = OUT/f'{NAME}.mp4'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    reader = imageio_ffmpeg.read_frames(str(video))
    try:
        meta = next(reader)
    finally:
        reader.close()
    assert meta['size'] == (W, H) and meta['fps'] == FPS
    count, seconds = imageio_ffmpeg.count_frames_and_secs(str(video))
    assert count == DURATION*FPS and abs(seconds-DURATION) < .05
    subprocess.run([ffmpeg, '-v', 'error', '-i', str(video), '-f', 'null', '-'], check=True)
    indices = [round(t*FPS) for t in (4, 8, 14.5, 19, 22, 29.5, 37, 44.5, 47, 50, 52, 53)]
    selection = '+'.join(f'eq(n\\,{n})' for n in indices)
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-i', str(video), '-vf',
                    f'select={selection},scale=480:270,tile=3x4', '-frames:v', '1',
                    str(OUT/f'{NAME}-contact-sheet.png')], check=True)
    report = dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(), frame_count=count,
                  duration_seconds=seconds, size=meta['size'], fps=meta['fps'], decode='passed',
                  contact_sheet_frame_indices=indices)
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = validate()
    previews()
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report), flush=True)
    if args.render:
        encode()
    if args.check:
        print(json.dumps(check_video()), flush=True)


if __name__ == '__main__':
    main()
