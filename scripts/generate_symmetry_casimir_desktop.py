"""Landscape adaptation of the revised, stepwise Casimir reel.

Real rotation generators obey [Jx,Jy]=Jz and J^2=-2I in the ordinary
three-dimensional vector representation. C=-J^2=2I is kept explicit.
The arrows are computed from these matrices, including when the final
input changes. Camera and coordinate axes stay fixed throughout.

Run with --render --check to encode and validate the movie. Without
--render, produce mathematical validation and review stills only.
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
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
import imageio_ffmpeg

NAME = 'symmetry-casimir-operator'
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools/casimir-desktop-review'
W, H, FPS, DURATION = 1600, 900, 24, 72
BG, INK, MUTED = '#fffcf6', '#232426', '#77746e'
GRID, FAINT = '#bdb8ae', '#e4ded3'
GOLD, PURPLE = '#a96d15', '#79559e'
BLUE, RED, GREEN = '#396fa8', '#bb4c40', '#32866c'
COLORS = (BLUE, RED, GREEN)
ZERO = np.zeros(3)
V = np.array([.72, -.50, .62])
J = np.array([[[0, 0, 0], [0, 0, -1], [0, 1, 0]],
              [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
              [[0, -1, 0], [1, 0, 0], [0, 0, 0]]], dtype=float)
C = -sum(j @ j for j in J)
U = J[0] @ V
OUTPUTS = np.array([j @ j @ V for j in J])
AZ, EL = np.deg2rad([-125., 5.])
CAMERA = np.array([[-math.sin(AZ), math.cos(AZ), 0.],
                   [math.sin(EL)*math.cos(AZ), math.sin(EL)*math.sin(AZ), -math.cos(EL)]])
ORIGIN = np.array([475., 465.])
MOMENTS = [0, 4, 8, 11, 14, 18, 21, 24, 28, 32, 36, 40, 43, 45, 47, 51, 57, 61, 65, 68, 71]


def ease(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


def progress(t, start, end):
    return ease((t-start)/(end-start))


def tint(color, opacity=1):
    a = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])
    b = np.array([int(BG[i:i+2], 16) for i in (1, 3, 5)])
    return tuple(np.round(b+(a-b)*opacity).astype(int))


@lru_cache(64)
def font(size=26, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('seguisb.ttf' if bold else 'segoeui.ttf'),
                  Path(matplotlib.get_data_path()) / 'fonts/ttf' /
                  ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError('No suitable text font')


@lru_cache(128)
def equation(tex, size=32, color=INK):
    stream = BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$'+tex+'$', stream, format='png', dpi=180, color=color,
                      prop=matplotlib.font_manager.FontProperties(size=size*72/180))
    stream.seek(0)
    return Image.open(stream).convert('RGBA')


def rotate(q, axis, angle):
    axis = np.asarray(axis, dtype=float)
    axis = axis/np.linalg.norm(axis)
    return q*math.cos(angle)+np.cross(axis, q)*math.sin(angle)+axis*np.dot(axis, q)*(1-math.cos(angle))


def project(q, scale=235):
    return ORIGIN+scale*(np.asarray(q) @ CAMERA.T)


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []

    def track(self, box, label):
        box = tuple(float(v) for v in box)
        assert box[0] >= 8 and box[1] >= 8 and box[2] <= W-8 and box[3] <= H-8, (label, box)
        self.boxes.append((box, label))

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la'):
        f = font(size, bold)
        self.track(self.d.textbbox((x, y), value, font=f, anchor=anchor), value)
        self.d.text((x, y), value, font=f, fill=color, anchor=anchor)

    def wrap(self, x, y, value, width=510, size=24, color=MUTED):
        line = ''
        for word in value.split():
            candidate = (line+' '+word).strip()
            if line and self.d.textlength(candidate, font=font(size)) > width:
                self.text(x, y, line, size, color)
                y += round(size*1.45)
                line = word
            else:
                line = candidate
        if line:
            self.text(x, y, line, size, color)

    def math(self, x, y, tex, size=35, color=INK, center=False, label=False):
        pic = equation(tex, size, color)
        px = round(x-pic.width/2) if center else round(x)
        py = round(y-pic.height/2)
        box = (px, py, px+pic.width, py+pic.height)
        self.track(box, tex)
        if label:
            self.d.rounded_rectangle((px-5, py-3, px+pic.width+5, py+pic.height+3), radius=3, fill=BG)
        self.im.paste(pic, (px, py), pic)

    def line(self, points, color=GRID, width=2):
        self.d.line([tuple(p) for p in points], fill=color, width=width, joint='curve')

    def arrow2(self, a, b, color, width=6, opacity=1):
        a, b = np.asarray(a), np.asarray(b)
        d = b-a
        length = np.linalg.norm(d)
        if length < 1 or opacity <= 0:
            return
        d /= length
        n = np.array([-d[1], d[0]])
        head = min(17, length*.45)
        self.line([a, b], BG, width+4)
        self.line([a, b], tint(color, opacity), width)
        self.d.polygon([tuple(b), tuple(b-head*d+.4*head*n), tuple(b-head*d-.4*head*n)],
                       fill=tint(color, opacity))

    def arrow(self, tail, vector, color, scale=235, width=6, opacity=1):
        self.arrow2(project(tail, scale), project(tail+vector, scale), color, width, opacity)

    def dot(self, point, radius=4, color=INK):
        x, y = point
        self.d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)


def draw_sphere(s, scale=235, opacity=1, radius=None):
    radius = np.linalg.norm(V) if radius is None else radius
    rad = radius*scale
    x, y = ORIGIN
    s.d.ellipse((x-rad, y-rad, x+rad, y+rad), fill=tint('#f2efe6', opacity),
                outline=tint('#cfc9bd', opacity), width=2)
    angles = np.linspace(0, 2*math.pi, 100)
    for latitude in (-math.pi/3, -math.pi/6, 0, math.pi/6, math.pi/3):
        pts = radius*np.c_[np.cos(angles)*math.cos(latitude),
                           np.sin(angles)*math.cos(latitude), np.full_like(angles, math.sin(latitude))]
        s.line(project(pts, scale), tint(FAINT, opacity))
    for azimuth in (0, math.pi/4, math.pi/2, 3*math.pi/4):
        pts = radius*np.c_[np.cos(angles)*math.cos(azimuth),
                           np.cos(angles)*math.sin(azimuth), np.sin(angles)]
        s.line(project(pts, scale), tint(FAINT, opacity))


def draw_axes(s, scale=235, opacity=.8):
    for axis, name in zip(np.eye(3), 'xyz'):
        s.line(project([-axis*1.18, axis*1.25], scale), tint('#8b8983', opacity), 2)
        s.math(*project(axis*1.35, scale), name, 25, MUTED, center=True, label=True)
    s.dot(ORIGIN, 4, MUTED)


def orbit(s, q, scale=235, opacity=1):
    pts = np.array([rotate(q, [1, 0, 0], angle) for angle in np.linspace(0, 2*math.pi, 150)])
    s.line(project(pts, scale), tint('#9b93a6', opacity), 2)
    arc = np.array([rotate(q, [1, 0, 0], a) for a in np.linspace(-.4, .3, 30)])
    s.line(project(arc, scale), tint(MUTED, opacity), 3)
    s.arrow2(project(arc[-3], scale), project(arc[-1], scale), MUTED, 3, opacity)
    s.dot(project(q, scale), 4, MUTED)


def label_vector(s, tail, vec, tex, color, scale=235, fraction=.65, offset=(0, 0)):
    p = project(tail+fraction*vec, scale)+np.asarray(offset)
    s.math(*p, tex, 30, color, center=True, label=True)


def header(s, t, stage):
    s.text(52, 42, 'Building a Casimir Operator', 34, INK, bold=True)
    s.text(52, 94, stage, 25, MUTED)
    s.math(1015, 75, r'C=-J^2=-(J_x^2+J_y^2+J_z^2)', 32)
    s.line([(940, 170), (940, 780)], FAINT, 2)
    s.line([(52, 827), (1548, 827)], FAINT, 2)
    s.line([(52, 827), (52+1496*t/DURATION, 827)], GOLD, 3)
    s.text(52, 850, 'Ordinary three-dimensional vector representation', 20, MUTED)


def sidebar(s, tex, note, color=INK, extra=None):
    s.math(990, 270, tex, 40, color)
    s.wrap(990, 338, note)
    if extra:
        s.math(990, 510, extra, 31, color)


def final_input(t):
    angle = progress(t, 54, 64)*.7
    magnitude = 1-.32*math.sin(math.pi*progress(t, 64, 69))
    return magnitude*rotate(V, [0., 0., 1.], angle)


def render(t):
    t = float(np.clip(t, 0, DURATION-1/FPS))
    s = Canvas()
    if t < 5:
        stage = 'Begin with a vector'
    elif t < 15:
        stage = 'Apply the rotation generator once'
    elif t < 25:
        stage = 'Apply the same generator again'
    elif t < 33:
        stage = 'Repeat for the other two axes'
    elif t < 42:
        stage = 'Add the three results'
    elif t < 48:
        stage = 'Reverse the sum'
    elif t < 54:
        stage = 'Two copies of the input vector'
    else:
        stage = 'Change the vector, keep the same operator'
    header(s, t, stage)

    if t < 33:
        draw_sphere(s, opacity=.7 if t < 15 else .22)
        draw_axes(s)
        s.arrow(ZERO, V*progress(t, .4, 2.2), GOLD, opacity=1 if t < 15 else .3,
                width=6 if t < 15 else 3)
        if t > 2.2:
            label_vector(s, ZERO, V, 'v', GOLD, fraction=1, offset=(22, -25))
        if t < 5:
            sidebar(s, r'v', 'We will apply each rotation generator twice, then add the results.', GOLD)
        elif t < 15:
            orbit(s, V, opacity=progress(t, 5, 6))
            reveal, transfer = progress(t, 6.2, 8.2), progress(t, 10, 13)
            tail = V*(1-transfer)
            if 0 < transfer < 1:
                s.arrow(V, U, PURPLE, width=3, opacity=.25)
            s.arrow(tail, reveal*U, PURPLE)
            if reveal > .98:
                label_vector(s, tail, U, r'J_xv', PURPLE, offset=(-46, 20))
            note = ('The generator gives the tangent to rotation about the x-axis.' if t < 10 else
                    'Bring that tangent vector to the origin. Its length and direction stay the same.')
            sidebar(s, r'v\ \longmapsto\ J_xv', note, PURPLE)
        elif t < 25:
            orbit(s, U, opacity=progress(t, 15, 16))
            s.arrow(ZERO, U, PURPLE)
            label_vector(s, ZERO, U, r'J_xv', PURPLE, fraction=1, offset=(40, -25))
            reveal, transfer = progress(t, 16.2, 18.2), progress(t, 20, 23)
            tail = U*(1-transfer)
            if 0 < transfer < 1:
                s.arrow(U, OUTPUTS[0], BLUE, width=3, opacity=.25)
            s.arrow(tail, OUTPUTS[0]*reveal, BLUE)
            if reveal > .98:
                label_vector(s, tail, OUTPUTS[0], r'J_x^2v', BLUE, offset=(-45, -25))
            sidebar(s, r'J_x(J_xv)=J_x^2v', 'Squaring the generator means applying it twice. The second tangent is computed from the new input.', BLUE)
        else:
            fractions = [1, progress(t, 25.8, 28), progress(t, 28.7, 31)]
            offsets = [(50, 30), (-43, 20), (-8, -32)]
            for i, (out, col, fraction, off) in enumerate(zip(OUTPUTS, COLORS, fractions, offsets)):
                s.arrow(ZERO, out*fraction, col)
                if fraction > .99:
                    label_vector(s, ZERO, out, rf'J_{"xyz"[i]}^2v', col, fraction=1, offset=off)
            for i, col in enumerate(COLORS):
                s.math(990, 250+i*86, rf'J_{"xyz"[i]}^2v', 39, col)
            s.wrap(990, 535, 'These are three different output vectors, all computed from the same input v.')

    elif t < 42:
        scale = 235-65*progress(t, 33, 35)
        draw_sphere(s, scale, .2)
        draw_axes(s, scale, .6)
        s.arrow(ZERO, V, GOLD, scale, 3, .6)
        label_vector(s, ZERO, V, 'v', GOLD, scale, 1, (26, -24))
        tail = ZERO.copy()
        for i, (out, col) in enumerate(zip(OUTPUTS, COLORS)):
            amount = 0 if i == 0 else progress(t, 35+(i-1)*2.2, 37+(i-1)*2.2)
            s.arrow(tail*amount, out, col, scale)
            tail += out
            s.math(990, 225+70*i, rf'J_{"xyz"[i]}^2v', 33, col)
        if t >= 39.5:
            s.arrow(ZERO, -2*V*progress(t, 39.5, 40.5), INK, scale, 5)
            label_vector(s, ZERO, -2*V, '-2v', INK, scale, 1, (0, 28))
        s.math(990, 480, r'J_x^2v+J_y^2v+J_z^2v=-2v', 31)
        s.wrap(990, 550, 'Moving the output vectors tip to tail adds them without changing any of them.')

    elif t < 48:
        scale = 170
        draw_sphere(s, scale, .15)
        draw_axes(s, scale, .55)
        s.arrow(ZERO, V, GOLD, scale, 3, .35)
        q = progress(t, 43, 46)
        s.arrow(ZERO, -2*V, INK, scale, 3, .15)
        s.arrow(ZERO, 2*V, INK, scale, 3, .15)
        # Scalar sign reversal stays on one line. This is a visual transition
        # between endpoints, not a finite spatial rotation or an intermediate C.
        result = (1-2*q)*(-2*V)
        s.arrow(ZERO, result, INK, scale, 8)
        if q == 0:
            label_vector(s, ZERO, result, '-2v', INK, scale, 1, (0, 28))
        elif q == 1:
            label_vector(s, ZERO, result, '2v', INK, scale, 1, (10, -26))
        sidebar(s, r'C=-J^2', 'The minus sign reverses the sum.', extra=r'J^2v=-2v')
        if q == 1:
            s.math(990, 640, r'Cv=2v', 44, GOLD)

    elif t < 54:
        scale = 170
        s.arrow(ZERO, V, GOLD, scale, 9)
        s.arrow(V, V, PURPLE, scale, 9)
        s.dot(project(V, scale), 6, INK)
        for tail, col in [(ZERO, GOLD), (V, PURPLE)]:
            label_vector(s, tail, V, 'v', col, scale, .5, (0, 40))
        label_vector(s, ZERO, 2*V, '2v', INK, scale, 1, (10, -27))
        sidebar(s, r'Cv=2v', 'The result points along v and has twice its length.', GOLD)

    else:
        scale = 155
        vector = final_input(t)
        contributions = np.array([-j @ j @ vector for j in J])
        draw_sphere(s, scale, .18, np.linalg.norm(vector))
        draw_axes(s, scale, .55)
        tail = ZERO.copy()
        for out, col in zip(contributions, COLORS):
            s.arrow(tail, out, col, scale, 4, .85)
            tail += out
        s.arrow(ZERO, C @ vector, INK, scale, 8)
        s.arrow(ZERO, vector, GOLD, scale, 6)
        s.dot(project(vector, scale), 5, GOLD)
        p = project(vector, scale)
        d = p-ORIGIN
        perpendicular = np.array([-d[1], d[0]])/np.linalg.norm(d)
        s.math(*(p+35*perpendicular), 'v', 32, GOLD, center=True, label=True)
        s.math(*(project(2*vector, scale)+35*d/np.linalg.norm(d)), '2v', 32, INK, center=True, label=True)
        s.math(990, 250, r'Cv=2v', 48, GOLD)
        for i, col in enumerate(COLORS):
            s.math(990+i*164, 350, rf'-J_{"xyz"[i]}^2v', 29, col)
        s.wrap(990, 420, 'The contributions change with v. Their sum always gives the same scale factor.')
        s.math(990, 570, r'C=2I', 49)
        s.wrap(990, 635, '2 labels this irreducible representation.', size=25, color=INK)

    # Text must remain separated even when moving labels are introduced.
    for i, (a, name_a) in enumerate(s.boxes):
        for b, name_b in s.boxes[i+1:]:
            overlap_w = min(a[2], b[2])-max(a[0], b[0])
            overlap_h = min(a[3], b[3])-max(a[1], b[1])
            assert overlap_w <= 0 or overlap_h <= 0, (t, name_a, name_b)
    return s.im


def validate():
    assert np.array_equal(C, 2*np.eye(3))
    assert np.allclose(CAMERA @ CAMERA.T, np.eye(2))
    for i in range(3):
        assert np.array_equal(J[i] @ J[(i+1)%3]-J[(i+1)%3] @ J[i], J[(i+2)%3])
        assert np.array_equal(C @ J[i], J[i] @ C)
    rng = np.random.default_rng(29)
    derivative_error = 0.
    for v in rng.normal(size=(100, 3)):
        for axis, j in zip(np.eye(3), J):
            derivative = (rotate(v, axis, 1e-5)-rotate(v, axis, -1e-5))/2e-5
            derivative_error = max(derivative_error, float(np.max(abs(derivative-j@v))))
            assert np.allclose(derivative, j@v, atol=1e-8)
            assert np.allclose(j@j@v, axis*np.dot(axis, v)-v)
        assert np.allclose(C@v, 2*v)
    for t in np.linspace(54, DURATION, 200):
        v = final_input(t)
        assert np.allclose(-sum(j@j@v for j in J), 2*v)
    return {'generator_convention': '[Jx,Jy]=Jz, cyclically', 'J_squared': '-2I',
            'C': '-J_squared = 2I', 'derivative_max_error': derivative_error,
            'random_vectors_checked': 100, 'varying_input_samples_checked': 200,
            'size': [W, H], 'fps': FPS, 'duration_seconds': DURATION,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1200, math.ceil(len(MOMENTS)/3)*250), BG)
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(MOMENTS):
        im = render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        x, y = i%3*400, i//3*250
        sheet.paste(im.resize((400, 225), Image.Resampling.LANCZOS), (x, y))
        draw.text((x+12, y+228), f'{t}s', fill=MUTED, font=font(17))
    sheet.save(REVIEW/'contact.png')
    render(57).save(OUT/f'{NAME}-poster.png')


def encode():
    destination = OUT/f'{NAME}.mp4'
    temporary = REVIEW/f'{NAME}.rendering.mp4'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264',
               '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
               '-threads', '3', str(temporary)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for i in range(DURATION*FPS):
                process.stdin.write(render(i/FPS).tobytes())
                if i % (FPS*12) == 0:
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
    indices = [round(t*FPS) for t in (8, 18, 28, 40, 47, 51, 57, 65, 71)]
    selection = '+'.join(f'eq(n\\,{n})' for n in indices)
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-i', str(video), '-vf',
                    f'select={selection},scale=480:270,tile=3x3', '-frames:v', '1',
                    str(OUT/f'{NAME}-contact-sheet.png')], check=True)
    report = {'video_sha256': hashlib.sha256(video.read_bytes()).hexdigest(),
              'frame_count': count, 'duration_seconds': seconds, 'size': meta['size'],
              'fps': meta['fps'], 'decode': 'passed', 'contact_sheet_frame_indices': indices}
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
