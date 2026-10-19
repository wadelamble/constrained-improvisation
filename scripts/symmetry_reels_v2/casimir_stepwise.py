"""Independent, step-by-step Casimir preview. Does not modify series packaging.

J_i v = e_i cross v, with angles in radians. The first two applications are
shown as tangent vectors attached to their inputs, then translated to the
origin without changing their length or direction. The three J_i^2 v outputs
are added before the minus sign in C is applied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess

from core import *
import imageio_ffmpeg

OUT = ROOT / 'content/reels/symmetry-series-v2/casimir-stepwise'
DURATION = 66
TITLE = 'Building a Casimir operator'
V = np.array([.72, -.50, .62])
RADIUS = float(np.linalg.norm(V))
ZERO = np.zeros(3)
EX = np.array([1., 0., 0.])
J = np.array([[[0, 0, 0], [0, 0, -1], [0, 1, 0]],
              [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
              [[0, -1, 0], [1, 0, 0], [0, 0, 0]]], dtype=float)
U = J[0] @ V
OUTPUTS = np.array([g @ g @ V for g in J])
# A small adjustment from the original view separates the component arrows
# while keeping the tip-to-tail chain clear of its white resultant.
AZIMUTH, ELEVATION = np.deg2rad([-125., 5.])
RIGHT = np.array([-math.sin(AZIMUTH), math.cos(AZIMUTH), 0.])
UP = np.array([-math.sin(ELEVATION)*math.cos(AZIMUTH),
               -math.sin(ELEVATION)*math.sin(AZIMUTH), math.cos(ELEVATION)])
CAMERA = np.array([RIGHT, -UP])
COLORS = (BLUE, RED, GREEN)
MOMENTS = [0, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35,
           38, 41, 44, 47, 50, 54, 57, 61, 65]
CHAPTERS = [(0, 'The operator'), (5, 'Choose a vector'), (9, 'Apply Jx'),
            (19, 'Apply Jx again'), (28, 'Jy and Jz'), (36, 'Add the results'),
            (45, 'Apply the minus sign'), (52, 'Two copies of v'),
            (58, 'The eigenvalue')]


def tint(color, opacity=1):
    a = np.array([int(color[i:i+2], 16) for i in (1, 3, 5)])
    b = np.array([int(BG[i:i+2], 16) for i in (1, 3, 5)])
    return '#' + ''.join(f'{int(round(x)):02x}' for x in b+(a-b)*opacity)


def proj(q, origin, scale):
    return np.asarray(origin) + scale*(np.asarray(q) @ CAMERA.T)


def rotate(q, axis, angle):
    axis = np.asarray(axis)/np.linalg.norm(axis)
    return (q*math.cos(angle)+np.cross(axis, q)*math.sin(angle)
            +axis*np.dot(axis, q)*(1-math.cos(angle)))


def arrow(s, origin, scale, tail, vector, color, width=7, alpha=1):
    if alpha <= 0 or np.linalg.norm(vector) < 1e-8:
        return
    a, b = proj(tail, origin, scale), proj(tail+vector, origin, scale)
    s.arrow(a, b, BG, width+5, 23)
    s.arrow(a, b, tint(color, alpha), width, 21)


def label(s, p, tex, color, size=34):
    pic = equation(tex, size, color)
    left, top = round(p[0]-pic.width/2), round(p[1]-pic.height/2)
    s.d.rounded_rectangle((left-7, top-5, left+pic.width+7, top+pic.height+5),
                         radius=5, fill=BG)
    s.im.paste(pic, (left, top), pic)


def curve(s, origin, scale, points, color, width=2):
    s.line(proj(np.asarray(points), origin, scale), color, width)


def sphere(s, origin, scale, alpha=1):
    if alpha <= 0:
        return
    rad = RADIUS*scale
    ox, oy = origin
    s.d.ellipse((ox-rad, oy-rad, ox+rad, oy+rad),
                fill=tint('#101b2a', alpha), outline=tint('#344d65', alpha), width=2)
    theta = np.linspace(0, 2*math.pi, 100)
    for latitude in (-math.pi/3, -math.pi/6, 0, math.pi/6, math.pi/3):
        points = RADIUS*np.c_[np.cos(theta)*math.cos(latitude),
                              np.sin(theta)*math.cos(latitude),
                              np.full_like(theta, math.sin(latitude))]
        curve(s, origin, scale, points, tint('#27364a', alpha))
    for azimuth in (0, math.pi/4, math.pi/2, 3*math.pi/4):
        points = RADIUS*np.c_[np.cos(theta)*math.cos(azimuth),
                              np.cos(theta)*math.sin(azimuth), np.sin(theta)]
        curve(s, origin, scale, points, tint('#27364a', alpha))


def axes(s, origin, scale, alpha=1):
    if alpha <= 0:
        return
    for axis, name in zip(np.eye(3), ('x', 'y', 'z')):
        curve(s, origin, scale, [-axis*1.18, axis*1.25], tint('#64778e', alpha), 2)
        p = proj(axis*1.35, origin, scale)
        s.text(*p, name, 27, tint(MUTED, alpha), anchor='mm')
    s.dot(origin, 5, tint(MUTED, alpha))


def orbit(s, origin, scale, q, alpha=1):
    points = np.array([rotate(q, EX, angle) for angle in np.linspace(0, 2*math.pi, 160)])
    curve(s, origin, scale, points, tint('#737a96', alpha), 3)
    arc = np.array([rotate(q, EX, angle) for angle in np.linspace(-.45, .40, 35)])
    curve(s, origin, scale, arc, tint(INK, alpha), 3)
    s.arrow(proj(arc[-3], origin, scale), proj(arc[-1], origin, scale),
            tint(INK, alpha), 3, 12)
    s.dot(proj(q, origin, scale), 6, tint(INK, alpha))


def base(t, stage):
    s = Scene.__new__(Scene)
    s.im = Image.new('RGB', (W, H), BG)
    s.d = ImageDraw.Draw(s.im)
    s.text(70, 163, 'VARIATIONS ON SYMMETRY', 25, MUTED)
    s.text(70, 217, 'CASIMIR OPERATOR / STEP-BY-STEP', 26, GOLD, bold=True)
    fitted_title(s.d, TITLE)
    if stage == 'other_axes':
        s.text(70, 420, 'Similarly for', 32, INK)
        s.math(r'J_y\ \mathrm{and}\ J_z', x=355, y=440, size=35)
    else:
        s.text(70, 420, stage, 32, INK)
    s.math(r'C=-(J_x^2+J_y^2+J_z^2)', y=535, size=49)
    s.line([(70, 1676), (950, 1676)], GRID, 3)
    s.line([(70, 1676), (70+880*t/DURATION, 1676)], GOLD, 4)
    s.text(70, 1717, 'Ordinary 3D vector representation', 25, MUTED)
    s.text(950, 1717, f'{int(t):02d} / {DURATION:02d} s', 25, MUTED, anchor='ra')
    return s


def step_equation(s, tex, note='', color=INK):
    s.math(tex, y=1490, size=46, color=color)
    if note:
        s.text(510, 1580, note, 29, MUTED, anchor='mm')


def render(t):
    t = min(max(float(t), 0), DURATION-.001)
    if t < 5:
        stage = 'Build the operator one step at a time'
    elif t < 9:
        stage = 'Begin with a vector'
    elif t < 19:
        stage = 'Operate with Jₓ'
    elif t < 28:
        stage = 'Operate with Jₓ again'
    elif t < 36:
        stage = 'other_axes'
    elif t < 45:
        stage = 'Add the three results'
    elif t < 52:
        stage = 'Apply the minus sign'
    elif t < 58:
        stage = 'The result contains two copies of the input'
    else:
        stage = 'The Casimir eigenvalue is 2'
    s = base(t, stage)
    origin, scale = np.array([510., 1030.]), 290.

    if t < 36:
        sphere_alpha = float(ease(window(t, 1, 4)))
        if t >= 19:
            sphere_alpha *= .25
        sphere(s, origin, scale, sphere_alpha)
        axes(s, origin, scale, .8)
        input_alpha = 1 if t < 19 else .30
        arrow(s, origin, scale, ZERO, V*float(ease(window(t, 4.5, 7))), GOLD,
              width=7 if t < 19 else 3, alpha=input_alpha)
        if t > 6:
            label(s, proj(V, origin, scale)+[30, -33], r'v', tint(GOLD, input_alpha), 38)

        if t < 9:
            if t > 5:
                step_equation(s, r'v', 'The sphere marks the length of the input vector.', GOLD)
        elif t < 19:
            orbit(s, origin, scale, V, float(ease(window(t, 9, 10))))
            reveal = float(ease(window(t, 10.5, 12.5)))
            transfer = float(ease(window(t, 14, 17)))
            if 0 < transfer < 1:
                arrow(s, origin, scale, V, U, PURPLE, 3, .22)
            tail = V*(1-transfer)
            arrow(s, origin, scale, tail, U*reveal, PURPLE, 8)
            if reveal > .98:
                label(s, proj(tail+U*.60, origin, scale)+[-53, 37], r'J_xv', PURPLE)
            note = ('Draw the tangent to rotation about x.' if t < 14 else
                    'Move this tangent vector to the origin.')
            step_equation(s, r'v\quad\longrightarrow\quad J_xv', note, PURPLE)
        elif t < 28:
            orbit(s, origin, scale, U, float(ease(window(t, 19, 20))))
            arrow(s, origin, scale, ZERO, U, PURPLE, 6)
            label(s, proj(U, origin, scale)+[47, -30], r'J_xv', PURPLE)
            reveal = float(ease(window(t, 20.5, 22.5)))
            transfer = float(ease(window(t, 24, 26.5)))
            if 0 < transfer < 1:
                arrow(s, origin, scale, U, OUTPUTS[0], BLUE, 3, .22)
            tail = U*(1-transfer)
            arrow(s, origin, scale, tail, OUTPUTS[0]*reveal, BLUE, 8)
            if reveal > .98:
                label(s, proj(tail+OUTPUTS[0]*.65, origin, scale)+[-55, -38],
                      r'J_x^2v', BLUE)
            note = ('This tangent is computed from the new input.' if t < 24 else
                    'Move the new tangent vector to the origin.')
            step_equation(s, r'J_x(J_xv)=J_x^2v', note, BLUE)
        else:
            fractions = [1., float(ease(window(t, 29.5, 31.5))),
                         float(ease(window(t, 32.5, 34.5)))]
            offsets = ([55, 28], [-42, 37], [-10, -43])
            for i, (out, color, reveal, offset) in enumerate(zip(OUTPUTS, COLORS, fractions, offsets)):
                arrow(s, origin, scale, ZERO, out*reveal, color, 8)
                if reveal > .99:
                    label(s, proj(out, origin, scale)+offset,
                          rf'J_{"xyz"[i]}^2v', color)
            step_equation(s, r'J_x^2v,\qquad J_y^2v,\qquad J_z^2v',
                          'All three results now start at the origin.')

    elif t < 45:
        scale = lerp(290., 200., float(ease(window(t, 36, 38))))
        sphere(s, origin, scale, .25)
        axes(s, origin, scale, .65)
        arrow(s, origin, scale, ZERO, V, GOLD, 3, .5)
        label(s, proj(V, origin, scale)+[26, -27], 'v', GOLD)
        tail = ZERO.copy()
        for i, (out, color) in enumerate(zip(OUTPUTS, COLORS)):
            move = 0 if i == 0 else float(ease(window(t, 38+(i-1)*2.3, 40+(i-1)*2.3)))
            arrow(s, origin, scale, tail*move, out, color, 8)
            tail += out
        for i, color in enumerate(COLORS):
            s.math(rf'J_{"xyz"[i]}^2v', x=230+i*280, y=1420, size=35, color=color)
        if t >= 42.5:
            arrow(s, origin, scale, ZERO, -2*V*float(ease(window(t, 42.5, 43.5))), INK, 5)
            label(s, proj(-2*V, origin, scale)+[0, 39], r'-2v', INK, 37)
        step_equation(s, r'J_x^2v+J_y^2v+J_z^2v=-2v', 'Place the vectors tip to tail.')

    elif t < 52:
        scale = 200.
        sphere(s, origin, scale, .25*(1-float(ease(window(t, 48, 51)))))
        axes(s, origin, scale, .65*(1-float(ease(window(t, 48, 51)))))
        arrow(s, origin, scale, ZERO, V, GOLD, 3, .35)
        flip = float(ease(window(t, 46.5, 49.5)))
        if flip < .99:
            arrow(s, origin, scale, ZERO, -2*V, INK, 3, .22)
        normal = np.cross(V, np.array([0., 0., 1.]))
        result = rotate(-2*V, normal, math.pi*flip)
        arrow(s, origin, scale, ZERO, result, INK, 9)
        if flip == 0:
            label(s, proj(result, origin, scale)+[0, 39], r'-2v', INK, 38)
        elif flip == 1:
            label(s, proj(result, origin, scale)+[0, -39], r'2v', INK, 38)
        step_equation(s, r'Cv=-(-2v)=2v', 'The minus sign reverses the sum.')

    else:
        scale = 200.
        pv = scale*(CAMERA @ V)
        tail1 = origin
        tail2 = origin+pv
        for tail, color in ((tail1, GOLD), (tail2, PURPLE)):
            s.arrow(tail, tail+pv, color, 11, 24)
            label(s, tail+pv*.5+[0, 53], 'v', color, 39)
        s.dot(origin+pv, 8, INK)
        label(s, origin+2*pv+[2, -40], '2v', INK, 43)
        if t < 58:
            step_equation(s, r'Cv=2v', 'Twice the length, in the same direction.')
        else:
            s.math(r'Cv=2v', y=1440, size=68, color=GOLD)
            s.text(510, 1535, '2 is the Casimir eigenvalue', 34, INK, anchor='mm')
            s.text(510, 1580, 'in the three-dimensional irreducible', 29, MUTED, anchor='mm')
            s.text(510, 1620, 'representation of SO(3).', 29, MUTED, anchor='mm')
    return s.im


def validate():
    assert np.allclose(-sum(g@g for g in J), 2*np.eye(3))
    assert np.allclose(OUTPUTS.sum(axis=0), -2*V)
    assert np.allclose(CAMERA @ CAMERA.T, np.eye(2))
    # Check both arrangements used in the reel. Separation at the origin
    # alone does not prevent a component from hiding beneath the resultant.
    screen = OUTPUTS @ CAMERA.T
    lengths = np.linalg.norm(screen, axis=1)
    angles = [math.degrees(math.acos(np.clip(np.dot(screen[i], screen[j]) /
              (lengths[i]*lengths[j]), -1, 1))) for i, j in ((0, 1), (0, 2), (1, 2))]
    assert min(angles) > 14
    result = screen.sum(axis=0)
    corners = np.cumsum(screen, axis=0)[:2]
    clearance = 200*(result[0]*corners[:, 1]-result[1]*corners[:, 0])/np.linalg.norm(result)
    assert clearance[0]*clearance[1] > 0  # The chain stays on one side of the sum.
    assert min(abs(clearance)) > 40
    rng = np.random.default_rng(29)
    for vector in rng.normal(size=(100, 3)):
        for axis, g in zip(np.eye(3), J):
            derivative = (rotate(vector, axis, 1e-5)-rotate(vector, axis, -1e-5))/2e-5
            assert np.allclose(derivative, g@vector, atol=1e-8)
            assert np.allclose(g@g@vector, axis*np.dot(axis, vector)-vector)
        assert np.allclose(-sum(g@g@vector for g in J), 2*vector)
    return {'generator_derivatives': 'verified', 'squared_generators': 'negative projections',
            'casimir': '2I', 'sample_vectors': 100, 'duration_seconds': DURATION,
            'minimum_component_angle_degrees': round(min(angles), 1),
            'sum_to_internal_corners_clearance_pixels': np.round(abs(clearance), 1).tolist()}


def stills():
    review = OUT/'review'
    review.mkdir(parents=True, exist_ok=True)
    cols, tw, th = 4, 270, 510
    sheet = Image.new('RGB', (cols*tw, math.ceil(len(MOMENTS)/cols)*th), BG)
    for i, t in enumerate(MOMENTS):
        im = render(t)
        im.save(review/f'{t:05.1f}.png')
        x, y = (i % cols)*tw, (i//cols)*th
        sheet.paste(im.resize((270, 480), Image.Resampling.LANCZOS), (x, y))
        ImageDraw.Draw(sheet).text((x+10, y+484), f'{t}s', font=font(18), fill=INK)
    sheet.save(review/'contact.jpg', quality=95)
    render(61).save(OUT/'poster.jpg', quality=95)


def encode():
    OUT.mkdir(parents=True, exist_ok=True)
    temporary = OUT/'casimir-stepwise.rendering.mp4'
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-f', 'rawvideo',
               '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
               '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
               '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-threads', '3', str(temporary)]
    with subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        try:
            for index in range(DURATION*FPS):
                process.stdin.write(render(index/FPS).tobytes())
                if index % 300 == 0:
                    print(f'Rendered {index}/{DURATION*FPS} frames', flush=True)
            process.stdin.close()
            error = process.stderr.read().decode('utf8', errors='replace')
            if process.wait():
                raise RuntimeError(error)
        except BaseException:
            process.kill()
            raise
    temporary.replace(OUT/'casimir-stepwise.mp4')


def package():
    import html
    video = OUT/'casimir-stepwise.mp4'
    version = hashlib.sha256(video.read_bytes()).hexdigest()[:12] if video.exists() else 'preview'
    buttons = ''.join(f'<button data-time="{time}">{html.escape(name)}</button>'
                      for time, name in CHAPTERS)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Casimir operator · step-by-step preview</title>
<style>:root{color-scheme:dark;font-family:system-ui;background:#080b14;color:#fff2e4}
body{max-width:1060px;margin:auto;padding:24px}main{display:grid;grid-template-columns:minmax(250px,430px) 1fr;gap:28px}video{width:100%;max-height:86vh}h1{font-size:28px}p{line-height:1.6;color:#a5b2c8}nav{display:grid;gap:9px}button{font:inherit;color:inherit;text-align:left;border:1px solid #334258;border-radius:7px;background:#111a2a;padding:12px;cursor:pointer}button:hover{border-color:#ffb45e}a{color:#46beff}.rate{margin-top:18px}select{font:inherit;padding:6px}@media(max-width:700px){main{display:block}video{max-height:75vh}}</style>
<h1>Building a Casimir operator</h1><main><video id="reel" controls playsinline preload="metadata" poster="poster.jpg?v=VERSION" src="casimir-stepwise.mp4?v=VERSION"></video>
<section><p>DURATION seconds · Step-by-step revision · Separate review preview</p><nav>BUTTONS</nav>
<p class="rate">Playback speed <select id="speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></p>
<p>The two applications of Jx are shown separately. The three squared-generator results are then added, and the minus sign reverses their sum.</p>
<p><a href="casimir-stepwise.mp4">Open MP4</a> · <a href="../casimir.html">Original version</a></p></section></main>
<script>const v=document.getElementById('reel');document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{v.currentTime=Number(b.dataset.time);v.play()});document.getElementById('speed').onchange=e=>v.playbackRate=Number(e.target.value);</script></html>'''
    (OUT/'index.html').write_text(page.replace('VERSION', version).replace('BUTTONS', buttons)
                                .replace('DURATION', str(DURATION)), encoding='utf8')
    (OUT/'validation.json').write_text(json.dumps(validate(), indent=2)+'\n', encoding='utf8')


def check_video():
    video = OUT/'casimir-stepwise.mp4'
    decoder = imageio_ffmpeg.read_frames(str(video))
    try:
        meta = next(decoder)
    finally:
        decoder.close()
    assert meta['size'] == (W, H) and meta['fps'] == FPS
    assert abs(meta['duration']-DURATION) < .05
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(video),
                    '-f', 'null', '-'], check=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(video),
                    '-vf', f'fps=12/{DURATION},scale=270:480,tile=4x3', '-frames:v', '1', '-q:v', '2',
                    str(OUT/'review/decoded.jpg')], check=True)
    return meta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps(validate()), flush=True)
    stills()
    if args.render:
        encode()
    package()
    if args.check:
        print(json.dumps(check_video()), flush=True)
