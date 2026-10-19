"""Portrait mathematics for episodes 9–16 of Symmetry to Waves.

Each scene is drawn directly at 1080 x 1920. Playback time is normalized to a
24-second choreography, so changing an entry's duration retains all its holds.
The functions and conventions follow the pre-Fourier symmetry manuscript.
"""
from __future__ import annotations

import math
import re

import numpy as np
from PIL import Image

from core import (
    Scene, BLUE, RED, GOLD, GREEN, PURPLE, INK, MUTED, GRID, BG,
    ease, window, lerp, font,
)


DEFAULT_SCREEN_TEXT = {
    9: ["Lengths and angles stay fixed"],
    10: ["Hyperbolic rotation"],
    11: ["Same rotations, different order"],
    12: ["Translating points", "Translating functions"],
    13: ["A small shift follows the tangent"],
    14: ["Ordinary basis", "Eigenbasis"],
    15: ["The derivative returns a multiple", "A shift returns a multiple"],
    16: ["A complex wave"],
}

# Literal inventory for the review document. Numeric readings are generated
# by the displayed mathematics; no caption prose is baked into the artwork.
SCREEN_TEXT = {
    9: DEFAULT_SCREEN_TEXT[9] + [
        r"(R\mathbf{u})\cdot(R\mathbf{v})=\mathbf{u}\cdot\mathbf{v}",
        r"\mathbf{u}\cdot\mathbf{v}=|\mathbf{u}|\,|\mathbf{v}|\cos\theta",
        r"|\mathbf{u}|=1,\quad |\mathbf{v}|=\frac{3}{4},\quad \theta=60^\circ",
        r"\mathbf{u}\cdot\mathbf{v}=\frac{3}{8}", "x", "y", "u", "v", "θ"],
    10: DEFAULT_SCREEN_TEXT[10] + [
        r"(ct)^2-x^2=1\qquad(c=1)", "η = [value]", "ct", "x", "ct = −x", "ct = x",
        "(x, ct)", "ct = [value], x = [value]", r"ct=\cosh\eta,\qquad x=\sinh\eta",
        r"\cosh^2\eta-\sinh^2\eta=1"],
    11: DEFAULT_SCREEN_TEXT[11] + [
        r"R_yR_x\ne R_xR_y", r"R_x\;\longrightarrow\;R_y", r"R_y\;\longrightarrow\;R_x",
        "x", "y", "z", r"[J_x,J_y]=J_z"],
    12: DEFAULT_SCREEN_TEXT[12] + [
        r"T_a(x)=x+a", "a = [value]", r"T_a(2+3)=5+a", r"T_a(2)+T_a(3)=5+2a",
        r"T_a(u+v)\ne T_a(u)+T_a(v)\quad(a\ne0)", r"T_a(f+g)=T_af+T_ag",
        r"(f+g)(x-a)", r"f(x-a)+g(x-a)", r"(T_af)(x)=f(x-a),\qquad T_a0=0", "x"],
    13: DEFAULT_SCREEN_TEXT[13] + [
        r"f(x-a)=f(x)-a f'(x)+O(a^2)", "×[magnification]", "a = 0.035",
        "x − a", "x", "−a", r"\hat K=-i\frac{d}{dx}", r"T_a=e^{-ia\hat K}"],
    14: DEFAULT_SCREEN_TEXT[14] + [
        r"a=\frac{s+s^{-1}}{2},\qquad b=\frac{s-s^{-1}}{2}", "s = [value]", "x", "y", "u", "v",
        "x′", "y′", "s u", "s⁻¹ v", r"x'=ax+by,\qquad y'=bx+ay", r"u'=su,\qquad v'=s^{-1}v"],
    15: DEFAULT_SCREEN_TEXT[15] + [
        r"\frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}", "λ = [value]", r"f", r"f'=\lambda f",
        r"f(x-a)=e^{-\lambda a}f(x)", "a = [value], exp(−λa) = [value]", "x"],
    16: DEFAULT_SCREEN_TEXT[16] + [
        r"z(x,t)=e^{i(kx-\omega t)}", "Re z", "Im z", r"\cos(kx-\omega t)", r"\sin(kx-\omega t)",
        "Re", "Im", "x", r"x_0=4", r"|z|=1", r"z(x-a,t)=e^{-ika}z(x,t)"],
}


def _stage(number, entry, index=0):
    labels = entry.get("screen_text") or DEFAULT_SCREEN_TEXT[number]
    return labels[min(index, len(DEFAULT_SCREEN_TEXT[number])-1)]


def _scene(number, t, entry, stage_index=0):
    duration = float(entry.get("duration", 24))
    labels = SCREEN_TEXT[number] if entry.get("screen_text") is None else entry["screen_text"]
    if len(labels) != len(SCREEN_TEXT[number]):
        raise ValueError(f"Reel {number}: screen_text requires {len(SCREEN_TEXT[number])} "
                         f"stable slots; found {len(labels)}. Edit entries in place.")
    numeric_templates = []
    for position, template in enumerate(SCREEN_TEXT[number]):
        fields = re.findall(r"\[(value|magnification)\]", template)
        if fields:
            if re.findall(r"\[(value|magnification)\]", labels[position]) != fields:
                raise ValueError(f"Reel {number}, screen_text slot {position+1}: "
                                 "preserve the numerical placeholders in order.")
            pattern = re.escape(template).replace(r",\ ", r"[\s,]+")
            for field in ("value", "magnification"):
                pattern = pattern.replace(re.escape(f"[{field}]"), r"([-+]?\d+(?:\.\d+)?)")
            numeric_templates.append((re.compile(pattern), labels[position]))
    scene = Scene(number, entry["title"], _stage(number, entry, stage_index),
                  t=t, duration=duration, total=16)
    original_math = scene.math
    original_text = scene.text

    def edited(value):
        try:
            return labels[SCREEN_TEXT[number].index(value)]
        except ValueError:
            for pattern, replacement in numeric_templates:
                match = pattern.fullmatch(str(value))
                if match:
                    numbers = iter(match.groups())
                    return re.sub(r"\[(?:value|magnification)\]", lambda _: next(numbers), replacement)
        return value

    def reviewed_math(tex, *args, **kwargs):
        return original_math(edited(tex), *args, **kwargs)

    def reviewed_text(x, y, value, *args, **kwargs):
        return original_text(x, y, edited(value), *args, **kwargs)

    scene.math = reviewed_math
    scene.text = reviewed_text
    return scene


def _clock(t, entry):
    return float(np.clip(t / float(entry.get("duration", 24)), 0, 1)) * 24


def _dashed(scene, a, b, color=GRID, width=2, dash=10, gap=8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    delta = b - a
    length = float(np.linalg.norm(delta))
    if length < .1:
        return
    direction = delta / length
    for start in np.arange(0, length, dash + gap):
        scene.line([a + start * direction,
                    a + min(start + dash, length) * direction], color, width)


def _mapper(box, xlim, ylim):
    left, top, right, bottom = box

    def xy(x, y):
        x, y = np.broadcast_arrays(np.asarray(x), np.asarray(y))
        return np.stack((left + (x - xlim[0]) / (xlim[1] - xlim[0]) * (right - left),
                         bottom - (y - ylim[0]) / (ylim[1] - ylim[0]) * (bottom - top)), axis=-1)
    return xy


def _clipped_curve(scene, points, box, color, width=4):
    """Clip the polyline into segments, rather than flattening out-of-view y."""
    left, top, right, bottom = box
    points = np.asarray(points, float)
    for a, b in zip(points[:-1], points[1:]):
        delta = b - a
        lo, hi = 0., 1.
        for p, q in ((-delta[0], a[0] - left), (delta[0], right - a[0]),
                     (-delta[1], a[1] - top), (delta[1], bottom - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    lo, hi = 1., 0.
                    break
            elif p < 0:
                lo = max(lo, q / p)
            else:
                hi = min(hi, q / p)
        if lo <= hi:
            scene.line([a + lo * delta, a + hi * delta], color, width)


def _plot_axes(scene, box, xy, xlim, ylim, color=GRID):
    left, top, right, bottom = box
    for f in (.25, .5, .75):
        scene.line([(left, top + f * (bottom-top)),
                    (right, top + f * (bottom-top))], color, 1)
    y0 = float(xy(0, 0)[1]) if ylim[0] <= 0 <= ylim[1] else bottom
    scene.arrow((left, y0), (right + 10, y0), MUTED, 2, 10)
    scene.text(right + 12, y0 + 13, "x", 30, MUTED, anchor="ma")


def _nine(t, entry):
    s = _scene(9, t, entry)
    q = _clock(t, entry)
    theta = .22 + 2 * math.pi * float(ease(window(q, 2, 21)))
    separation = math.pi / 3
    origin = np.array([510., 960.])
    scale = 270.
    u = np.array([math.cos(theta), math.sin(theta)])
    v = .75 * np.array([math.cos(theta + separation), math.sin(theta + separation)])
    projection = float(u @ v) * u

    def p(v):
        return origin + scale * np.asarray(v) * [1, -1]

    s.math(r"(R\mathbf{u})\cdot(R\mathbf{v})=\mathbf{u}\cdot\mathbf{v}", y=540, size=49)
    for value in (-1, -.5, .5, 1):
        s.line([p([value, -1.15]), p([value, 1.15])], GRID, 1)
        s.line([p([-1.15, value]), p([1.15, value])], GRID, 1)
    s.arrow(p([-1.28, 0]), p([1.28, 0]), MUTED, 2, 11)
    s.arrow(p([0, -1.28]), p([0, 1.28]), MUTED, 2, 11)
    s.text(878, 973, "x", 32, MUTED)
    s.text(530, 606, "y", 32, MUTED)
    ang = np.linspace(0, 2 * math.pi, 181)
    s.line([p([math.cos(a), math.sin(a)]) for a in ang], GRID, 2)
    _dashed(s, p(v), p(projection), GOLD, 3)
    s.line([origin, p(projection)], GOLD, 9)
    s.arrow(origin, p(u), BLUE, 7, 22)
    s.arrow(origin, p(v), RED, 7, 22)
    s.dot(p(projection), 7, GOLD)
    arc = np.linspace(theta, theta + separation, 65)
    s.line([p(.24 * np.array([math.cos(a), math.sin(a)])) for a in arc], INK, 3)
    mid = theta + separation / 2
    label = p(.38 * np.array([math.cos(mid), math.sin(mid)]))
    s.text(*label, "θ", 34, INK, anchor="mm")
    for vec, label, color in ((u, "u", BLUE), (v, "v", RED)):
        pos = p(vec + .13 * vec / np.linalg.norm(vec))
        # The label crosses coordinate axes during a full turn. A compact
        # background keeps its glyphs distinct from those reference lines.
        label = (entry.get("screen_text") or SCREEN_TEXT[9])[SCREEN_TEXT[9].index(label)]
        bounds = s.d.textbbox(tuple(pos), label, font=font(38), anchor="mm")
        s.d.rectangle((bounds[0]-5, bounds[1]-4, bounds[2]+5, bounds[3]+4), fill=BG)
        s.text(*pos, label, 38, color, anchor="mm")
    s.math(r"\mathbf{u}\cdot\mathbf{v}=|\mathbf{u}|\,|\mathbf{v}|\cos\theta", y=1385, size=49)
    s.math(r"|\mathbf{u}|=1,\quad |\mathbf{v}|=\frac{3}{4},\quad \theta=60^\circ", y=1454, size=46)
    s.math(r"\mathbf{u}\cdot\mathbf{v}=\frac{3}{8}", y=1535, size=47, color=GOLD)
    return s.im


def _ten(t, entry):
    s = _scene(10, t, entry)
    q = _clock(t, entry)
    # A boost orbit through (ct,x)=(1,0); rapidity stays bounded on screen.
    phase = float(ease(window(q, 2, 21))) * 2 * math.pi
    eta = 1.15 * math.sin(phase)
    origin = np.array([510., 1280.])
    scale = 210.

    def p(x, ct):
        return origin + np.array([x, -ct]) * scale

    s.math(r"(ct)^2-x^2=1\qquad(c=1)", y=540, size=55)
    s.text(510, 618, f"η = {eta:+.2f}", 35, GOLD, anchor="ma")
    s.arrow(p(-1.8, 0), p(1.8, 0), MUTED, 2, 12)
    s.arrow(p(0, -.2), p(0, 2.8), MUTED, 2, 12)
    s.text(912, 1285, "x", 32, MUTED)
    s.text(529, 682, "ct", 32, MUTED)
    for k in (1, 2):
        s.line([p(-.045, k), p(.045, k)], MUTED, 2)
        if k == 2:
            s.text(482, p(0, k)[1], str(k), 30, MUTED, anchor="rm")
    for sign in (-1, 1):
        _dashed(s, origin, p(sign*1.65, 1.65), GRID, 2)
    s.text(110, 1000, "ct = −x", 30, MUTED)
    s.text(785, 1000, "ct = x", 30, MUTED)
    r = np.linspace(-1.35, 1.35, 301)
    s.line([p(math.sinh(a), math.cosh(a)) for a in r], BLUE, 5)
    ct, x = math.cosh(eta), math.sinh(eta)
    point = p(x, ct)
    _dashed(s, point, p(x, 0), GOLD, 3)
    _dashed(s, point, p(0, ct), GOLD, 3)
    s.arrow(origin, point, RED, 6, 20)
    s.dot(point, 10, GOLD)
    s.dot((709, 755), 7, GOLD)
    s.text(730, 733, "(x, ct)", 32, GOLD)
    s.text(510, 1342, f"ct = {ct:.2f}     x = {x:+.2f}", 33, MUTED, anchor="ma")
    s.math(r"ct=\cosh\eta,\qquad x=\sinh\eta", y=1445, size=50)
    s.math(r"\cosh^2\eta-\sinh^2\eta=1", y=1530, size=51, color=GOLD)
    return s.im


def _rotation(axis, angle):
    c, sn = math.cos(angle), math.sin(angle)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -sn], [0, sn, c]])
    return np.array([[c, 0, sn], [0, 1, 0], [-sn, 0, c]])


def _sphere(s, center, matrix):
    center = np.asarray(center, float)
    # Orthonormal fixed camera vectors. Geometry remains genuinely 3D.
    horizontal = np.array([.8, -.6, 0.])
    vertical = np.array([.3, .4, math.sqrt(.75)])
    radius = 163.

    def p(v):
        v = np.asarray(v)
        return center + radius * np.stack((v @ horizontal, -(v @ vertical)), axis=-1)

    a = np.linspace(0, 2*math.pi, 121)
    for plane in range(3):
        points = np.zeros((len(a), 3))
        points[:, (plane+1) % 3] = np.cos(a)
        points[:, (plane+2) % 3] = np.sin(a)
        s.line(p(points), GRID, 2)
    s.d.ellipse((center[0]-radius, center[1]-radius,
                 center[0]+radius, center[1]+radius), outline=GRID, width=2)
    for k, label in enumerate(("x", "y", "z")):
        axis = np.eye(3)[k]
        s.arrow(p(-.23*axis), p(1.24*axis), MUTED, 2, 10)
        pos = p(1.38*axis)
        s.text(*pos, label, 30, MUTED, anchor="mm")
    # Two perpendicular material arrows mark the sphere's orientation.
    for axis, color in ((np.array([0., 0., 1.]), GOLD),
                        (np.array([1., 0., 0.]), BLUE)):
        s.arrow(center, p(matrix @ axis), color, 7, 20)
        s.dot(p(matrix @ axis), 8, color)
    meridian = np.stack((np.sin(a), np.zeros_like(a), np.cos(a)), axis=-1)
    s.line(p(meridian @ matrix.T), BLUE, 3)


def _eleven(t, entry):
    s = _scene(11, t, entry)
    q = _clock(t, entry)
    first = math.pi/2 * float(ease(window(q, 2, 8)))
    second = math.pi/2 * float(ease(window(q, 10, 17)))
    s.math(r"R_yR_x\ne R_xR_y", y=540, size=59)
    s.math(r"R_x\;\longrightarrow\;R_y", x=260, y=653, size=46, maxwidth=360)
    s.math(r"R_y\;\longrightarrow\;R_x", x=260, y=1113, size=46, maxwidth=360)
    _sphere(s, (580, 842), _rotation("y", second) @ _rotation("x", first))
    _sphere(s, (580, 1302), _rotation("x", second) @ _rotation("y", first))
    s.math(r"[J_x,J_y]=J_z", y=1535, size=55, color=GOLD)
    return s.im


def _number_line(s, y):
    left, right = 140., 905.
    s.arrow((left, y), (right, y), MUTED, 3, 12)
    for k in range(0, 29, 5):
        x = left + (right-left) * k/28
        s.line([(x, y-8), (x, y+8)], MUTED, 2)
        s.text(x, y+22, str(k), 30, MUTED, anchor="ma")
    return lambda value: left + (right-left)*value/28


def _twelve(t, entry):
    q = _clock(t, entry)
    point_act = q < 10
    s = _scene(12, t, entry, 0 if point_act else 1)
    if point_act:
        a = 10 * float(ease(window(q, 1.5, 6.5)))
        s.math(r"T_a(x)=x+a", y=545, size=57)
        s.text(510, 647, f"a = {a:.1f}", 36, GOLD, anchor="ma")
        for y, tex, result, color in (
            (885, r"T_a(2+3)=5+a", 5+a, BLUE),
            (1200, r"T_a(2)+T_a(3)=5+2a", 5+2*a, RED),
        ):
            s.math(tex, y=y-147, size=48)
            pos = _number_line(s, y)
            s.dot((pos(5), y), 7, GRID)
            s.arrow((pos(5), y-35), (pos(result), y-35), color, 5, 16)
            s.dot((pos(result), y), 11, color)
            s.text(pos(result), y-83, f"{result:.1f}", 36, color, anchor="ma")
        s.math(r"T_a(u+v)\ne T_a(u)+T_a(v)\quad(a\ne0)", y=1470, size=45, color=GOLD)
    else:
        a = 1.5 * float(ease(window(q, 12, 20)))
        s.math(r"T_a(f+g)=T_af+T_ag", y=540, size=51)
        s.text(510, 627, f"a = {a:.2f}", 35, GOLD, anchor="ma")
        x = np.linspace(-4, 5, 500)
        f = lambda z: .80*np.exp(-((z+1.0)/.90)**2)
        g = lambda z: .55*np.exp(-((z-.8)/1.10)**2)
        for lower, box in ((False, (140, 770, 900, 975)),
                           (True, (140, 1120, 900, 1325))):
            xy = _mapper(box, (-4, 5), (0, 1.1))
            _plot_axes(s, box, xy, (-4, 5), (0, 1.1))
            s.math(r"(f+g)(x-a)" if not lower else r"f(x-a)+g(x-a)",
                   y=box[1]-62, size=44, color=GREEN if not lower else GOLD)
            if lower:
                s.line(xy(x, f(x-a)), BLUE, 4)
                s.line(xy(x, g(x-a)), RED, 4)
            else:
                s.line(xy(x, f(x)+g(x)), GRID, 3)
            s.line(xy(x, f(x-a)+g(x-a)), GOLD if lower else GREEN, 6)
        s.math(r"(T_af)(x)=f(x-a),\qquad T_a0=0", y=1470, size=47)
    return s.im


def _f(x):
    x = np.asarray(x)
    return (.46*np.sin(.72*x+.35) + .24*np.sin(1.65*x-.60)
            + .13*np.sin(3.35*x+1.10) + .04*x)


def _fp(x):
    return (.46*.72*np.cos(.72*x+.35) + .24*1.65*np.cos(1.65*x-.60)
            + .13*3.35*np.cos(3.35*x+1.10) + .04)


def _thirteen(t, entry):
    q = _clock(t, entry)
    s = _scene(13, t, entry, 0 if q < 16 else 1)
    zoom = float(ease(window(q, 3, 16)))
    x0, a = 1.92, .035
    xc = x0-a/2
    yc = float((_f(x0)+_f(x0-a))/2)
    xspan = 10.5 * (.14/10.5)**zoom
    yspan = 2.4 * (.085/2.4)**zoom
    xlim = (xc-xspan/2, xc+xspan/2)
    ylim = (yc-yspan/2, yc+yspan/2)
    box = (110, 715, 910, 1260)
    xy = _mapper(box, xlim, ylim)
    s.math(r"f(x-a)=f(x)-a f'(x)+O(a^2)", y=540, size=48)
    s.text(110, 639, f"×{10.5/xspan:.1f}", 35, MUTED)
    s.text(710, 639, "a = 0.035", 33, GOLD)
    for k in np.linspace(0, 1, 5):
        s.line([(110+800*k, 715), (110+800*k, 1260)], GRID, 1)
        s.line([(110, 715+545*k), (910, 715+545*k)], GRID, 1)
    x = np.linspace(*xlim, 500)
    _clipped_curve(s, xy(x, _f(x)), box, BLUE, 5)
    _clipped_curve(s, xy(x, _f(x0)+_fp(x0)*(x-x0)), box, GOLD, 3)
    for xx, color in ((x0, BLUE), (x0-a, GOLD)):
        pp = xy(xx, _f(xx))
        s.dot(pp, 9, color)
        if zoom > .72:
            _dashed(s, pp, (pp[0], 1260), color, 2)
    if zoom > .72:
        px1, px2 = xy(x0-a, 0)[0], xy(x0, 0)[0]
        s.text(px1, 1290, "x − a", 32, GOLD, anchor="ma")
        s.text(px2, 1290, "x", 32, BLUE, anchor="ma")
        s.arrow((px2, 1350), (px1, 1350), MUTED, 3, 12)
        s.text((px1+px2)/2, 1370, "−a", 31, MUTED, anchor="ma")
    s.math(r"\hat K=-i\frac{d}{dx}", x=295, y=1490, size=54, maxwidth=390)
    s.math(r"T_a=e^{-ia\hat K}", x=735, y=1490, size=54, maxwidth=400)
    return s.im


def _fourteen(t, entry):
    q = _clock(t, entry)
    s = _scene(14, t, entry, 0 if q < 12 else 1)
    stretch = 1 + .8*float(ease(window(q, 2, 17)))
    aa, bb = (stretch+1/stretch)/2, (stretch-1/stretch)/2
    s.math(r"a=\frac{s+s^{-1}}{2},\qquad b=\frac{s-s^{-1}}{2}", y=540, size=46)
    s.text(510, 608, f"s = {stretch:.2f}", 33, GOLD, anchor="ma")
    for origin, eigen in ((np.array([510., 825.]), False),
                          (np.array([510., 1300.]), True)):
        scale = 140.

        def p(v):
            return origin + scale*np.asarray(v)*[1, -1]

        if not eigen:
            basis = [np.array([1., 0.]), np.array([0., 1.])]
            transformed = [np.array([aa, bb]), np.array([bb, aa])]
            labels = ("x′", "y′")
        else:
            basis = [np.array([1., 1.])/math.sqrt(2), np.array([-1., 1.])/math.sqrt(2)]
            transformed = [stretch*basis[0], basis[1]/stretch]
            labels = ("s u", "s⁻¹ v")
        for index, v in enumerate(basis):
            extent = 1.95 if eigen else (1.6 if index == 0 else 1.2)
            s.line([p(-1.5*v), p(extent*v)], GRID, 2)
            s.arrow(origin, p(v), MUTED, 3, 14)
        if not eigen:
            s.text(735, 824, "x", 30, MUTED)
            s.text(460, 665, "y", 30, MUTED, anchor="ra")
        else:
            s.text(752, 1070, "u", 30, MUTED)
            s.text(285, 1100, "v", 30, MUTED)
        for vec, label, color in zip(transformed, labels, (BLUE, RED)):
            end = p(vec)
            s.arrow(origin, end, color, 7, 21)
            # Leader-free labels have deliberately fixed, separated homes.
            if not eigen:
                delta = (34, 22) if color == BLUE else (-28, 22)
                s.text(end[0]+delta[0], end[1]+delta[1], label, 34, color,
                       anchor="ma" if color == BLUE else "ra")
            else:
                s.text(end[0]+(28 if color == BLUE else -28), end[1]-15,
                       label, 32, color, anchor="la" if color == BLUE else "ra")
    s.math(r"x'=ax+by,\qquad y'=bx+ay", y=1005, size=47)
    s.math(r"u'=su,\qquad v'=s^{-1}v", y=1530, size=51, color=GOLD)
    return s.im


def _fifteen(t, entry):
    q = _clock(t, entry)
    s = _scene(15, t, entry, 0 if q < 11 else 1)
    lam = .35 + .35*float(ease(window(q, 2, 9)))
    a = 1.4*float(ease(window(q, 12, 21)))
    factor = math.exp(-lam*a)
    s.math(r"\frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}", y=540, size=50)
    s.text(510, 630, f"λ = {lam:.2f}", 35, GOLD, anchor="ma")
    x = np.linspace(-2, 2, 400)
    for translated, box in ((False, (140, 730, 900, 995)),
                            (True, (140, 1155, 900, 1420))):
        xy = _mapper(box, (-2, 2), (0, 4.6))
        _plot_axes(s, box, xy, (-2, 2), (0, 4.6))
        s.line(xy(x, np.exp(lam*x)), GRID if translated else BLUE, 4)
        if translated:
            s.line(xy(x, np.exp(lam*(x-a))), GREEN, 6)
            s.math(r"f(x-a)=e^{-\lambda a}f(x)", y=1085, size=49, color=GREEN)
        else:
            s.line(xy(x, lam*np.exp(lam*x)), GOLD, 5)
            s.math(r"f", x=275, y=690, size=44, color=BLUE)
            s.math(r"f'=\lambda f", x=665, y=690, size=44, color=GOLD)
    s.text(510, 1500, f"a = {a:.2f}       exp(−λa) = {factor:.2f}", 34, GREEN, anchor="ma")
    return s.im


def _sixteen(t, entry):
    s = _scene(16, t, entry)
    q = _clock(t, entry)
    physical_t = float(np.clip(q-2, 0, 20))
    k, omega, x0 = math.pi/2, math.pi/3, 4.
    x = np.linspace(0, 8, 850)
    z = np.exp(1j*(k*x-omega*physical_t))
    z0 = complex(np.exp(1j*(k*x0-omega*physical_t)))
    left, right, center_y, gain, depth = 160., 860., 815., 115., .65
    rotation = np.exp(-.38j)

    def project(xx, zz):
        xx, zz = np.broadcast_arrays(np.asarray(xx), np.asarray(zz))
        transverse = zz*rotation
        return np.stack((left+xx/8*(right-left)+depth*gain*transverse.imag,
                         center_y-gain*transverse.real), axis=-1)

    s.math(r"z(x,t)=e^{i(kx-\omega t)}", y=540, size=60)
    s.line([project(0, 0), project(8, 0)], MUTED, 2)
    s.text(882, 813, "x", 32, MUTED)
    for value in (0, 4, 8):
        pos = project(value, 0)
        s.line([(pos[0], center_y-7), (pos[0], center_y+7)], MUTED, 2)
        s.text(pos[0], center_y+119, str(value), 30, MUTED, anchor="ma")
    # A real fixed spatial slice: only its complex vector rotates.
    phase = np.linspace(0, 2*math.pi, 181)
    s.line(project(x0, np.exp(1j*phase)), GRID, 3)
    s.line(project(x, z), BLUE, 5)
    p0 = project(x0, z0)
    s.arrow(project(x0, 0), p0, GOLD, 5, 17)
    s.dot(p0, 9, GOLD)
    for zz, label, color, label_x in ((1, "Re z", BLUE, 85),
                                     (1j, "Im z", RED, 235)):
        end = project(0, zz)
        s.arrow(project(0, 0), end, color, 3, 12)
        s.text(label_x, 646, label, 30, color)
    # Both scalar component plots use the same spatial coordinates as the helix.
    mid, amp = 1120., 70.
    xx = left+x/8*(right-left)
    s.line([(left, mid), (right, mid)], GRID, 2)
    s.line(np.c_[xx, mid-amp*z.real], BLUE, 4)
    s.line(np.c_[xx, mid-amp*z.imag], RED, 4)
    _dashed(s, (510, 1004), (510, 1204), GOLD, 2)
    s.dot((510, mid-amp*z0.real), 7, BLUE)
    s.dot((510, mid-amp*z0.imag), 7, RED)
    s.math(r"\cos(kx-\omega t)", x=285, y=1010, size=42, color=BLUE, maxwidth=390)
    s.math(r"\sin(kx-\omega t)", x=745, y=1010, size=42, color=RED, maxwidth=390)
    # Unit-circle dial of exactly the same selected complex value.
    center, radius = np.array([510., 1370.]), 112.
    s.d.ellipse((398, 1258, 622, 1482), outline=GRID, width=3)
    s.arrow((365, 1370), (665, 1370), MUTED, 2, 10)
    s.arrow((510, 1492), (510, 1228), MUTED, 2, 10)
    s.text(681, 1368, "Re", 31, MUTED)
    s.text(529, 1210, "Im", 31, MUTED)
    end = center + radius*np.array([z0.real, -z0.imag])
    _dashed(s, end, (end[0], center[1]), BLUE, 2)
    _dashed(s, end, (center[0], end[1]), RED, 2)
    s.arrow(center, end, GOLD, 6, 18)
    s.dot(end, 8, GOLD)
    s.math(r"x_0=4", x=210, y=1320, size=45, color=GOLD, maxwidth=250)
    s.math(r"|z|=1", x=805, y=1455, size=47, color=GOLD, maxwidth=260)
    s.math(r"z(x-a,t)=e^{-ika}z(x,t)", y=1538, size=47)
    return s.im


_RENDERERS = {
    9: _nine, 10: _ten, 11: _eleven, 12: _twelve,
    13: _thirteen, 14: _fourteen, 15: _fifteen, 16: _sixteen,
}


def render(number: int, t: float, entry: dict) -> Image.Image:
    """Draw an episode at playback time ``t`` in seconds."""
    try:
        renderer = _RENDERERS[int(number)]
    except KeyError as exc:
        raise ValueError(f"episodes_second handles 9–16, not {number}") from exc
    return renderer(t, entry)
