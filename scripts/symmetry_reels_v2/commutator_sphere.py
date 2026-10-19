"""Sequential rotation orders on S², with a connected magnified endpoint gap.

Independent review version. Existing reels, numbering and captions are untouched.
Blue is Rx(theta) Ry(theta) v. Coral is Ry(theta) Rx(theta) v.
The inset uses the same orthographic camera and magnifies geometry by 1/theta².
Its green comparison vector is Jz v, translated without rotation or rescaling.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from core import *
import imageio_ffmpeg

OUT = ROOT / 'content/reels/symmetry-series-v2/commutator-sphere'
DURATION = 54
INITIAL, MID, FINAL = .8, .4, .02
V = np.array([1., 6., 8.]) / math.sqrt(101)
DEPTH = np.array([2., -3., 5.]) / math.sqrt(38)
RIGHT = np.array([3., 2., 0.]) / math.sqrt(13)
UP = np.array([-10., 15., 13.]) / math.sqrt(494)
CAMERA = np.array([RIGHT, -UP])
J = np.array([
    [[0, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
    [[0, -1, 0], [1, 0, 0], [0, 0, 0]],
], dtype=float)
ORIGIN = np.array([520., 820.])
SCALE = 300.
INSET = (110, 1260, 970, 1500)
INSET_CENTER = np.array([540., 1380.])
MOMENTS = [0, 4, 8, 11, 14.5, 19, 22, 26, 29.5, 33, 37, 41, 44.5, 47, 50, 53]
STAGES = [
    (0, 'A fixed-length vector on a sphere.'),
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
    (48, 'The scaled gap approaches the z tangent.'),
]


def mix(color, strength=1., background=BG):
    def rgb(h):
        return np.array([int(h[k:k+2], 16) for k in (1, 3, 5)])
    out = np.rint(lerp(rgb(background), rgb(color), np.clip(strength, 0, 1))).astype(int)
    return '#' + ''.join(f'{x:02x}' for x in out)


def rotation3(axis, theta):
    g = J[axis]
    return np.eye(3) + math.sin(theta)*g + (1-math.cos(theta))*(g@g)


def project(p):
    return ORIGIN + SCALE*(np.asarray(p) @ CAMERA.T)


def angle_at(t):
    if t < 24:
        return INITIAL
    if t < 28:
        return lerp(INITIAL, MID, float(ease(window(t, 24, 28))))
    if t < 31:
        return MID
    if t < 40:
        return math.exp(lerp(math.log(MID), math.log(FINAL), float(ease(window(t, 31, 40)))))
    return FINAL


def progress(t):
    return (float(ease(window(t, 2, 5.5))), float(ease(window(t, 6.3, 9.8))),
            float(ease(window(t, 12.8, 16.3))), float(ease(window(t, 17, 20.5))))


def route(theta, first_axis, second_axis, first=1., second=1., samples=85):
    leg1 = np.array([rotation3(first_axis, a)@V for a in np.linspace(0, theta*first, samples)])
    joint = leg1[-1]
    leg2 = np.array([rotation3(second_axis, a)@joint for a in np.linspace(0, theta*second, samples)])
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


def curved_arrow(s, points, color, width=4, head=13):
    points = np.asarray(points)
    s.line(points, color, width)
    if len(points)>3 and np.linalg.norm(points[-1]-points[0])>12:
        s.arrow(points[-4], points[-1], color, width, head)


class Canvas(Scene):
    def __init__(self):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)


def sphere_curves():
    curves = []
    for latitude in np.linspace(-math.pi/3, math.pi/3, 5):
        a = np.linspace(0, 2*math.pi, 181)
        curves.append(np.c_[np.cos(a)*math.cos(latitude), np.sin(a)*math.cos(latitude),
                               np.full_like(a, math.sin(latitude))])
    for longitude in np.linspace(0, math.pi, 6, endpoint=False):
        a = np.linspace(0, 2*math.pi, 181)
        curves.append(np.c_[np.cos(a)*math.cos(longitude), np.cos(a)*math.sin(longitude), np.sin(a)])
    return curves


GRID_CURVES = sphere_curves()


@lru_cache(1)
def base():
    s = Canvas()
    s.text(70, 165, 'VARIATIONS ON SYMMETRY', 25, MUTED, bold=True)
    s.text(70, 218, 'COMMUTATORS · SPHERE PREVIEW', 26, GOLD, bold=True)
    fitted_title(s.d, 'What the commutator measures', y=267, max_height=120, size=55)
    # A softly lit spherical surface keeps the projected trails visibly on S².
    rr = round(SCALE)
    yy, xx = np.mgrid[-rr:rr+1, -rr:rr+1] / SCALE
    mask = xx*xx+yy*yy <= 1
    depth = np.sqrt(np.maximum(0, 1-xx*xx-yy*yy))
    light = np.clip(.35 + .38*depth - .12*xx - .12*yy, 0, 1)
    tile = np.zeros((2*rr+1, 2*rr+1, 3), dtype=np.uint8)
    for channel, (dark, bright) in enumerate(((8, 19), (11, 31), (20, 48))):
        tile[:, :, channel] = np.where(mask, dark+(bright-dark)*light, dark).astype(np.uint8)
    s.im.paste(Image.fromarray(tile), (round(ORIGIN[0]-SCALE), round(ORIGIN[1]-SCALE)))
    for curve in GRID_CURVES:
        pp = project(curve)
        for i in range(len(curve)-1):
            front = DEPTH @ ((curve[i]+curve[i+1])*.5) >= 0
            if front or i%4 < 2:
                s.line(pp[i:i+2], '#354861' if front else '#1e2b3e', 2 if front else 1)
    s.d.ellipse((ORIGIN[0]-SCALE, ORIGIN[1]-SCALE, ORIGIN[0]+SCALE, ORIGIN[1]+SCALE),
                outline='#617089', width=2)
    for axis, name in zip(np.eye(3), 'xyz'):
        dash(s, project(-1.15*axis), ORIGIN, '#3d4b60', 2, 7)
        s.arrow(ORIGIN, project(1.18*axis), '#7a89a0', 2, 10)
        s.text(*project(1.29*axis), name, 30, MUTED, anchor='mm')
    s.dot(ORIGIN, 5, INK)
    return s.im


def active_axis(s, axis, color):
    direction = np.eye(3)[axis]
    s.arrow(ORIGIN, project(1.18*direction), mix(color, .8), 4, 13)
    s.text(*project(1.29*direction), 'xyz'[axis], 32, color, bold=True, anchor='mm')


def draw_route(s, legs, color, strength=1.):
    color = mix(color, strength)
    for leg in legs:
        if np.linalg.norm(leg[-1]-leg[0]) > .002:
            curved_arrow(s, project(leg), color, 4, 12)
    if np.linalg.norm(legs[0][-1]-V)>.03:
        hollow(s, project(legs[0][-1]), color, 5, 2)


def vector(s, endpoint, color, strength=1., width=6):
    color = mix(color, strength)
    p = project(endpoint)
    s.arrow(ORIGIN, p, color, width, 18)
    s.dot(p, 8, color)


def magnifier_geometry(theta):
    blue, red = full_results(theta)
    middle = (blue+red)*.5
    zoom = theta**-2
    def pp(p):
        return INSET_CENTER + SCALE*zoom*((np.asarray(p)-middle) @ CAMERA.T)
    half = np.array([(INSET[2]-INSET[0])/2, (INSET[3]-INSET[1])/2])/zoom
    center = project(middle)
    return pp, zoom, center, half


def tangent(s, start, end, color=GREEN, strength=1., width=5):
    color = mix(color, strength, PANEL)
    dash(s, start, end, color, width, 10)
    d = np.asarray(end)-start
    length = np.linalg.norm(d)
    if length > 15:
        s.arrow(np.asarray(end)-d/length*19, end, color, width, 17)
    x, y = end
    s.d.ellipse((x-11, y-11, x+11, y+11), outline=color, width=3)


def inset(s, theta, t, alpha):
    pp, zoom, center, half = magnifier_geometry(theta)
    # This rectangle is the actual region mapped into the inset. A separate
    # locator ring remains visible once the rectangle becomes sub-pixel.
    left, top = center-half
    right, bottom = center+half
    linecolor = mix(MUTED, .5*alpha)
    s.d.rectangle((left, top, right, bottom), outline=linecolor, width=2)
    s.d.ellipse((center[0]-10, center[1]-10, center[0]+10, center[1]+10), outline=linecolor, width=2)
    dash(s, (left, bottom), (INSET[0], INSET[1]), linecolor, 2, 8)
    dash(s, (right, bottom), (INSET[2], INSET[1]), linecolor, 2, 8)
    layer = Canvas()
    layer.d.rectangle(INSET, fill=PANEL)
    for curve in GRID_CURVES:
        for i in range(0, len(curve)-1, 2):
            if DEPTH @ curve[i] > 0:
                layer.line(pp(curve[i:i+3]), '#2e3e54', 2)
    for first, second, color in ((1, 0, BLUE), (0, 1, RED)):
        for leg in route(theta, first, second, samples=130):
            layer.line(pp(leg), mix(color, .4, PANEL), 3)
    blue, red = full_results(theta)
    bp, rp = pp(blue), pp(red)
    if t >= 48:
        tangent(layer, rp, rp+SCALE*(CAMERA@(J[2]@V)), GREEN)
    layer.arrow(rp, bp, GOLD, 5, 18)
    layer.dot(rp, 8, RED)
    layer.dot(bp, 8, BLUE)
    # Keep marker sizes readable while the underlying coordinates magnify.
    crop = layer.im.crop(INSET)
    s.im.paste(Image.blend(s.im.crop(INSET), crop, alpha), INSET[:2])
    s.d.rounded_rectangle(INSET, radius=12, outline=mix('#617089', alpha), width=2)
    s.text(540, 1220, 'Same gap, enlarged', 28, mix(INK, alpha), anchor='mm')
    if t >= 46:
        dash(s, (635, 1540), (680, 1540), GREEN, 4, 9)
        s.math(r'J_zv', x=755, y=1540, size=33, color=GREEN, maxwidth=150)
    return bp, rp


def z_reference(s, t, red_inset):
    reveal = float(ease(window(t, 42, 43)))
    # This is a genuine small Rz orbit through the original vector, not
    # a tangent attached to one of the finite two-order endpoints.
    orbit = np.array([rotation3(2, a)@V for a in np.linspace(-.35, .42, 90)])
    s.line(project(orbit), mix(GREEN, .55*reveal), 4)
    turn = .25*float(ease(window(t, 42.5, 44.5)))
    s.dot(project(rotation3(2, turn)@V), 7, mix(GREEN, reveal))
    if t >= 44:
        amount = float(ease(window(t, 44, 45.3)))
        start = project(V)
        delta = SCALE*(CAMERA@(J[2]@V))
        tangent(s, start, start+delta*amount, GREEN, .7)
        if t < 46:
            s.math(r'J_zv', x=start[0]+delta[0]/2-35, y=start[1]+delta[1]/2-28,
                   size=31, color=GREEN, maxwidth=120)
    if 46 <= t < 48:
        u = float(ease(window(t, 46, 48)))
        start = lerp(project(V), red_inset, u)
        delta = SCALE*(CAMERA@(J[2]@V))
        tangent(s, start, start+delta, GREEN)
    active_axis(s, 2, GREEN)


def render(t):
    t = float(np.clip(t, 0, DURATION))
    s = Canvas()
    s.im = base().copy()
    s.d = ImageDraw.Draw(s.im)
    stage = next(label for start, label in reversed(STAGES) if t >= start)
    s.text(70, 400, stage, 30, INK)
    theta = angle_at(t)
    b1, b2, r1, r2 = progress(t)
    blue_legs, red_legs = route(theta, 1, 0, b1, b2), route(theta, 0, 1, r1, r2)
    blue, red = blue_legs[-1][-1], red_legs[-1][-1]
    red_visible = float(ease(window(t, 11.5, 12.3)))
    for x, color, title, tex, visible in (
        (300, BLUE, '1. y then x', r'R_x(\theta)R_y(\theta)v', 1.),
        (780, RED, '2. x then y', r'R_y(\theta)R_x(\theta)v', .35+.65*red_visible)):
        s.text(x, 465, title, 29, mix(color, visible), bold=True, anchor='mm')
        s.math(tex, x=x, y=506, size=28, color=mix(color, visible), maxwidth=360)
    # The original vector and starting point persist throughout the comparison.
    dash(s, ORIGIN, project(V), mix(INK, .45), 3, 8)
    hollow(s, project(V), INK, 8, 2)
    s.math('v', x=project(V)[0]+25, y=project(V)[1]-23, size=33, color=INK, maxwidth=60)
    reduced = .35 if t >= 42 else 1.
    draw_route(s, blue_legs, BLUE, (.65 if t >= 11.5 else 1.)*reduced)
    vector(s, blue, BLUE, .85*reduced if t >= 11.5 else 1., 5)
    if red_visible:
        draw_route(s, red_legs, RED, red_visible*reduced)
        vector(s, red, RED, red_visible*reduced, 5)
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
        if np.linalg.norm(b-a)>2:
            s.arrow(a, b, GOLD, 4, min(16, max(5, .35*np.linalg.norm(b-a))))
        if t < 28:
            middle = (a+b)/2
            s.line([middle+np.array([12.,0.]), (870,middle[1])], mix(GOLD,.45), 2)
            s.math(r'\Delta v', x=915, y=middle[1], size=35, color=GOLD, maxwidth=120)
    if 20.5 <= t < 28:
        s.text(540, 1305, 'The gap points from coral to blue.', 31, GOLD, anchor='mm')
        s.math(r'\Delta v=(R_xR_y-R_yR_x)v', y=1400, size=43, color=INK, maxwidth=880)
        if t >= 24:
            s.text(540, 1510, 'Both routes contract toward the starting point.', 29, MUTED, anchor='mm')
    elif t >= 28:
        alpha = float(ease(window(t, 28, 28.8)))
        bp, rp = inset(s, theta, t, alpha)
        if t >= 42:
            z_reference(s, t, rp)
        if t >= 48:
            s.math(r'[J_x,J_y]v=J_zv',
                   y=1620, size=40, maxwidth=860)
        elif t >= 42:
            s.text(540, 1610, 'Green shows the change per radian about z.', 29, GREEN, anchor='mm')
        else:
            s.text(540, 1610, 'The two endpoints are still on the same sphere.', 28, MUTED, anchor='mm')
    s.line([(70, 1708), (1010, 1708)], GRID, 3)
    s.line([(70, 1708), (70+940*t/DURATION, 1708)], GOLD, 4)
    s.text(70, 1750, 'SYMMETRY TO WAVES', 24, MUTED)
    s.text(1010, 1750, f'{t:04.1f} / {DURATION} s', 24, MUTED, anchor='ra')
    return s.im


def validate():
    assert np.isclose(np.linalg.norm(V), 1)
    assert np.allclose(CAMERA@CAMERA.T, np.eye(2))
    assert np.allclose(CAMERA@DEPTH, 0)
    assert np.allclose(J[0]@J[1]-J[1]@J[0], J[2])
    errors = []
    for theta in (.8, .4, .2, .1, .02, .001, .0001):
        blue, red = full_results(theta)
        assert np.isclose(np.linalg.norm(blue), 1) and np.isclose(np.linalg.norm(red), 1)
        difference = (blue-red)/theta**2
        errors.append(float(np.linalg.norm(difference-J[2]@V)))
        pp, zoom, center, half = magnifier_geometry(theta)
        assert np.allclose(pp(blue)-pp(red), SCALE*CAMERA@difference)
        for a, b in ((1, 0), (0, 1)):
            legs = route(theta, a, b)
            assert all(np.allclose(np.linalg.norm(leg, axis=1), 1) for leg in legs)
            assert np.allclose(legs[-1][-1], rotation3(b, theta)@rotation3(a, theta)@V)
    assert all(b<a for a, b in zip(errors, errors[1:]))
    assert errors[-1] < .0002
    full_routes = np.concatenate([leg for a,b in ((1,0),(0,1)) for leg in route(INITIAL,a,b)])
    assert np.min(full_routes@DEPTH)>.2, 'All routes must remain on the visible hemisphere.'
    for theta in np.geomspace(MID, FINAL, 130):
        pp, _, _, _ = magnifier_geometry(theta)
        blue, red = full_results(theta)
        points = np.array([pp(blue),pp(red),pp(red)+SCALE*CAMERA@(J[2]@V)])
        assert points[:,0].min()>INSET[0]+20 and points[:,0].max()<INSET[2]-20
        assert points[:,1].min()>INSET[1]+15 and points[:,1].max()<INSET[3]-15
    return dict(unit_sphere='preserved', rotation_order='verified', blue_minus_coral='positive Jz',
                inset_geometry='same camera, exact 1/theta² magnification',
                reference_vector='Jz v, translated only', limit_errors=errors,
                duration=DURATION, fps=FPS)


def stills():
    folder = OUT/'review'
    folder.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1080, 510*math.ceil(len(MOMENTS)/4)), BG)
    for i, t in enumerate(MOMENTS):
        pic = render(t)
        pic.save(folder/f'{t:05.1f}.png')
        x, y = (i%4)*270, (i//4)*510
        sheet.paste(pic.resize((270,480), Image.Resampling.LANCZOS), (x,y))
        ImageDraw.Draw(sheet).text((x+10,y+484), f'{t}s', font=font(18), fill=INK)
    sheet.save(folder/'contact.jpg', quality=95)
    render(22).save(OUT/'poster.jpg', quality=95)


def encode():
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT/'commutator-sphere.mp4'
    temporary = OUT/'commutator-sphere.rendering.mp4'
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-f', 'rawvideo',
           '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-movflags', '+faststart', '-threads', '3', str(temporary)]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as process:
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
    temporary.replace(target)


def package():
    video = OUT/'commutator-sphere.mp4'
    if video.exists():
        version = hashlib.sha256(video.read_bytes()).hexdigest()[:12]
        page = OUT/'index.html'
        if page.exists():
            import re
            content = page.read_text(encoding='utf8').replace('__VERSION__', version)
            content = re.sub(r'((?:commutator-sphere\.mp4|poster\.jpg)\?v=)[a-f0-9]+',
                             lambda m:m.group(1)+version, content)
            page.write_text(content, encoding='utf8')
        print('Video version '+version, flush=True)
    (OUT/'validation.json').write_text(json.dumps(validate(), indent=2)+'\n', encoding='utf8')


def check_video():
    video = OUT/'commutator-sphere.mp4'
    decoder = imageio_ffmpeg.read_frames(str(video))
    try:
        meta = next(decoder)
    finally:
        decoder.close()
    assert meta['size']==(W,H) and meta['fps']==FPS and abs(meta['duration']-DURATION)<.05
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(video),
                    '-f', 'null', '-'], check=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(video),
                    '-vf', f'fps=12/{DURATION},scale=270:480,tile=4x3', '-frames:v', '1',
                    '-q:v', '2', str(OUT/'review/decoded.jpg')], check=True)
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
