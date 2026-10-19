"""Opposite rotation orders and their normalized infinitesimal mismatch.

Active rotations act on column vectors. Blue applies j first, then i, and
therefore has matrix R_i(a) R_j(b). Red reverses those actions. Their
blue-minus-red difference divided by a*b tends to [J_i,J_j]v = J_k v.
No four-step group loop or Hermitian-generator convention is used here.
"""
from __future__ import annotations

from core import *

DURATION = 40
TITLE = "What the commutator measures"
SCREEN_TEXT = [
    "Run the same two rotations", "Overlay the two results",
    "Shrink both angles", "Cycle the axis pairs", "The generators close",
    "y then x", "x then y", "z then y", "y then z", "x then z", "z then x",
    "First rotation", "Second rotation", "Same starting frame",
    "Rightmost rotation acts first", "Blue minus red", "Magnified mismatch",
    "Magnification = 1/(ab)", "rad", "Lie algebra", "Generators + commutators",
    "x", "y", "z",
    r"R_x(a)R_y(b)\mathbf{v}", r"R_y(b)R_x(a)\mathbf{v}",
    r"R_y(a)R_z(b)\mathbf{v}", r"R_z(b)R_y(a)\mathbf{v}",
    r"R_z(a)R_x(b)\mathbf{v}", r"R_x(b)R_z(a)\mathbf{v}",
    r"R_x(a)R_y(b)\ne R_y(b)R_x(a)",
    r"R_i(\theta)=e^{\theta J_i}", r"a=b", r"\Delta\mathbf{v}",
    r"\frac{\Delta\mathbf{v}}{ab}",
    r"\Delta\mathbf{v}=(R_x(a)R_y(b)-R_y(b)R_x(a))\mathbf{v}",
    r"\Delta\mathbf{v}=(R_y(a)R_z(b)-R_z(b)R_y(a))\mathbf{v}",
    r"\Delta\mathbf{v}=(R_z(a)R_x(b)-R_x(b)R_z(a))\mathbf{v}",
    r"\frac{\Delta\mathbf{v}}{ab}\longrightarrow J_z\mathbf{v}",
    r"\frac{\Delta\mathbf{v}}{ab}\longrightarrow J_x\mathbf{v}",
    r"\frac{\Delta\mathbf{v}}{ab}\longrightarrow J_y\mathbf{v}",
    r"J_z\mathbf{v}", r"J_x\mathbf{v}", r"J_y\mathbf{v}",
    r"[J_x,J_y]=J_z", r"[J_y,J_z]=J_x", r"[J_z,J_x]=J_y",
    r"\mathfrak{so}(3)=\mathrm{span}\{J_x,J_y,J_z\}",
    r"[A,B]=AB-BA", r"\mathbf{v}", "Target angles",
]

GENERATORS = np.array([
    [[0, 0, 0], [0, 0, -1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 0], [-1, 0, 0]],
    [[0, -1, 0], [1, 0, 0], [0, 0, 0]],
], dtype=float)
RIGHT = np.array([.8, -.6, 0.])
UP = np.array([-.3, -.4, math.sqrt(.75)])
CAMERA = np.array([RIGHT, -UP])
V = np.array([.62, .48, .62])
FRAME = np.diag([.96, .86, 1.02])
PAIRS = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
NAMES = ('x', 'y', 'z')
INITIAL_ANGLE, SMALL_ANGLE = .85, .025
ORDER_LABELS = (("y then x", "x then y"), ("z then y", "y then z"),
                ("x then z", "z then x"))
ORDER_TEX = tuple((
    rf"R_{NAMES[i]}(a)R_{NAMES[j]}(b)\mathbf{{v}}",
    rf"R_{NAMES[j]}(b)R_{NAMES[i]}(a)\mathbf{{v}}") for i, j, k in PAIRS)
DELTA_TEX = tuple(
    rf"\Delta\mathbf{{v}}=(R_{NAMES[i]}(a)R_{NAMES[j]}(b)-R_{NAMES[j]}(b)R_{NAMES[i]}(a))\mathbf{{v}}"
    for i, j, k in PAIRS)
LIMIT_TEX = tuple(rf"\frac{{\Delta\mathbf{{v}}}}{{ab}}\longrightarrow J_{NAMES[k]}\mathbf{{v}}"
                  for i, j, k in PAIRS)
BRACKET_TEX = tuple(rf"[J_{NAMES[i]},J_{NAMES[j]}]=J_{NAMES[k]}" for i, j, k in PAIRS)


def rotation3(axis, angle):
    """Rodrigues formula for the real skew generator of active rotations."""
    j = GENERATORS[axis]
    return np.eye(3)+math.sin(angle)*j+(1-math.cos(angle))*(j@j)


def project(origin, scale, v):
    return np.asarray(origin)+scale*(CAMERA@np.asarray(v))


def dashed(s, start, end, color=GRID, width=2, dash=8):
    a, b = np.asarray(start), np.asarray(end)
    length = float(np.linalg.norm(b-a))
    if length < 1e-8:
        return
    for step in np.arange(0, length, 1.8*dash):
        s.line([a+(b-a)*step/length, a+(b-a)*min(step+dash, length)/length], color, width)


def axes3(s, origin, scale, labels=True):
    for axis, name in zip(np.eye(3), NAMES):
        s.line([project(origin, scale, -.25*axis), project(origin, scale, 1.22*axis)], GRID, 2)
        if labels:
            q = project(origin, scale, 1.37*axis)
            s.text(*q, name, 25, MUTED, anchor='mm')


def marker(s, p, index, color, radius=7):
    x, y = p
    if index == 0:
        s.d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=BG, outline=color, width=3)
    elif index == 1:
        s.d.rectangle((x-radius, y-radius, x+radius, y+radius), fill=BG, outline=color, width=3)
    else:
        s.d.polygon(((x, y-radius-2), (x+radius+2, y+radius), (x-radius-2, y+radius)),
                    fill=BG, outline=color, width=3)


def frame(s, matrix, origin, scale, color, width=4):
    """Three marked basis arms and a tracked vector with x,y,z all nonzero."""
    points = [project(origin, scale, matrix@p) for p in FRAME]
    # The connecting triangle makes a rigid, recognizably identical 3D object.
    s.line(points+points[:1], color, 2)
    for index, point in enumerate(points):
        s.line([origin, point], color, width)
        marker(s, point, index, color)
    endpoint = project(origin, scale, matrix@V)
    s.arrow(origin, endpoint, color, width+1, 14)
    s.dot(endpoint, 8, color)
    s.dot(origin, 4, INK)
    return endpoint


def pair_state(t):
    """One-sided a=b -> 0 limit, using radians in every computation."""
    pair = 0 if t < 25 else 1 if t < 29 else 2
    if pair == 0:
        u = float(ease(window(t, 14, 23)))
        angle = math.exp(lerp(math.log(INITIAL_ANGLE), math.log(SMALL_ANGLE), u))
    else:
        start = 25 if pair == 1 else 29
        u = float(ease(window(t, start+.3, start+2.6)))
        angle = math.exp(lerp(math.log(.45), math.log(SMALL_ANGLE), u))
    i, j, k = PAIRS[pair]
    blue = rotation3(i, angle)@rotation3(j, angle)
    red = rotation3(j, angle)@rotation3(i, angle)
    return pair, angle, blue, red


def parameter_row(s, angle, y):
    s.math(r'a=b', x=385, y=y+17, size=34, maxwidth=150)
    s.text(450, y, f'= {angle:.3f}', 33, INK)
    s.text(594, y+2, 'rad', 29, MUTED)


def mismatch_diagram(s, pair, angle, blue, red):
    """Translate the mismatch to v; enlarge it by the explicitly shown 1/(ab)."""
    i, j, k = PAIRS[pair]
    q = (blue@V-red@V)/(angle*angle)
    target = GENERATORS[k]@V
    origin, scale = np.array([716., 1305.]), 145.
    # An orbit of v under R_k makes the gold vector's tangent meaning visible.
    orbit = [project(origin, scale, rotation3(k, theta)@V)
             for theta in np.linspace(0, 2*math.pi, 121)]
    s.line(orbit, GRID, 2)
    p = project(origin, scale, V)
    limit = project(origin, scale, V+target)
    endpoint = project(origin, scale, V+q)
    dashed(s, p, limit, GOLD, 4, 9)
    delta = limit-p
    if np.linalg.norm(delta)>0:
        unit = delta/np.linalg.norm(delta)
        s.arrow(limit-16*unit, limit, GOLD, 4, 14)
    s.d.ellipse((limit[0]-13, limit[1]-13, limit[0]+13, limit[1]+13), outline=GOLD, width=3)
    s.arrow(p, endpoint, INK, 4, 13)
    s.dot(endpoint, 6, INK)
    s.dot(p, 5, MUTED)
    s.math(r'\mathbf{v}', x=p[0]-20, y=p[1]+21, size=25, color=MUTED, maxwidth=50)
    s.text(105, 1200, 'Magnified mismatch', 30, INK)
    s.math(r'\frac{\Delta\mathbf{v}}{ab}', x=285, y=1305, size=52, maxwidth=270)
    s.text(105, 1380, 'Magnification = 1/(ab)', 27, MUTED)
    s.text(105, 1417, f'× {1/(angle*angle):,.1f}', 32, GOLD)
    # Fixed legend positions never chase moving endpoints.
    s.line([(574, 1505), (604, 1505)], GOLD, 4)
    s.math(rf'J_{NAMES[k]}\mathbf{{v}}', x=665, y=1505, size=30, color=GOLD, maxwidth=110)
    s.line([(755, 1505), (785, 1505)], INK, 4)
    s.math(r'\frac{\Delta\mathbf{v}}{ab}', x=850, y=1505, size=32, maxwidth=110)


def closure(s, t):
    s.text(510, 532, 'Lie algebra', 48, GOLD, bold=True, anchor='ma')
    s.math(r'\mathfrak{so}(3)=\mathrm{span}\{J_x,J_y,J_z\}', y=664, size=47)
    s.text(510, 773, 'Generators + commutators', 31, MUTED, anchor='ma')
    for index, tex in enumerate(BRACKET_TEX):
        y = 926+169*index
        s.panel((185, y-66, 835, y+66))
        s.math(tex, y=y, size=57, color=GOLD, maxwidth=580)
    s.math(r'[A,B]=AB-BA', y=1492, size=49)
    s.math(r'R_i(\theta)=e^{\theta J_i}', y=1591, size=39, color=MUTED)


def render(t, entry):
    t = float(np.clip(t, 0, DURATION))
    stage = SCREEN_TEXT[0 if t<10 else 1 if t<14 else 2 if t<25 else 3 if t<33 else 4]
    s = Scene(entry.get('order',17), entry.get('title', TITLE), stage, t, DURATION)
    if t >= 33:
        closure(s, t)
        return s.im

    pair, angle, blue, red = pair_state(t)
    if t < 10:
        first = float(ease(window(t, 2, 5)))
        second = float(ease(window(t, 5.6, 8.6)))
        # Matrices compose right to left: y first then x is Rx @ Ry.
        blue = rotation3(0, INITIAL_ANGLE*second)@rotation3(1, INITIAL_ANGLE*first)
        red = rotation3(1, INITIAL_ANGLE*second)@rotation3(0, INITIAL_ANGLE*first)
        for index, (cx, color, matrix) in enumerate(((285, BLUE, blue), (735, RED, red))):
            s.panel((cx-210, 550, cx+210, 1155))
            s.text(cx, 582, ORDER_LABELS[0][index], 31, color, bold=True, anchor='ma')
            s.math(ORDER_TEX[0][index], x=cx, y=678, size=37, color=color, maxwidth=380)
            origin, scale = np.array([cx, 925.]), 180.
            axes3(s, origin, scale)
            frame(s, matrix, origin, scale, color)
            if t < 2:
                label = 'Same starting frame'
            elif t < 5.6:
                label = 'First rotation'
            else:
                label = 'Second rotation'
            s.text(cx, 1090, label, 27, MUTED, anchor='ma')
        s.text(510, 1172, 'Target angles', 26, MUTED, anchor='ma')
        parameter_row(s, INITIAL_ANGLE, 1212)
        if t >= 8.6:
            s.math(r'R_x(a)R_y(b)\ne R_y(b)R_x(a)', y=1340, size=47)
        else:
            s.math(r'R_i(\theta)=e^{\theta J_i}', y=1340, size=47)
        s.text(510, 1465, 'Rightmost rotation acts first', 31, MUTED, anchor='ma')
        return s.im

    merge = float(ease(window(t, 10, 12)))
    origins = (lerp(np.array([285., 925.]), np.array([510., 867.]), merge),
               lerp(np.array([735., 925.]), np.array([510., 867.]), merge))
    scale = lerp(180., 213., merge)
    for index, color in enumerate((BLUE, RED)):
        x = (285, 735)[index]
        s.text(x, 540, ORDER_LABELS[pair][index], 29, color, bold=True, anchor='ma')
        s.math(ORDER_TEX[pair][index], x=x, y=611, size=36, color=color, maxwidth=390)
    axes3(s, np.array([510., 867.]), scale, labels=True)
    # The red result is underneath blue only when the two converge.
    red_tip = frame(s, red, origins[1], scale, RED, 4)
    blue_tip = frame(s, blue, origins[0], scale, BLUE, 4)
    if t >= 12:
        s.arrow(red_tip, blue_tip, GOLD, 3, 10)
    parameter_row(s, angle, 1050)
    s.math(DELTA_TEX[pair], y=1140, size=35, maxwidth=880)
    if t >= 14:
        mismatch_diagram(s, pair, angle, blue, red)
        if t < 25:
            s.math(LIMIT_TEX[pair], y=1583, size=46, color=GOLD)
        else:
            for index, tex in enumerate(BRACKET_TEX):
                s.math(tex, x=(215, 510, 805)[index], y=1580, size=34,
                       color=GOLD if pair==index else MUTED, maxwidth=278)
    else:
        s.text(510, 1320, 'Blue minus red', 34, GOLD, anchor='ma')
        s.math(r'\Delta\mathbf{v}', y=1430, size=57, color=GOLD)
    return s.im


def validate():
    assert np.all(V != 0), 'Every coordinate must be nonzero.'
    assert np.allclose(CAMERA@CAMERA.T, np.eye(2))
    assert np.allclose(GENERATORS+GENERATORS.transpose(0, 2, 1), 0)
    limits = []
    for i, j, k in PAIRS:
        assert np.allclose(GENERATORS[i]@GENERATORS[j]-GENERATORS[j]@GENERATORS[i], GENERATORS[k])
        target = GENERATORS[k]@V
        assert np.linalg.norm(CAMERA@target)>.3, 'Target tangent must be visible.'
        errors = []
        for a in (.85, .45, .2, .1, .025, .001):
            ri, rj = rotation3(i, a), rotation3(j, a)
            for r in (ri, rj):
                assert np.allclose(r.T@r, np.eye(3))
                assert np.isclose(np.linalg.det(r), 1.)
            q = (ri@rj-rj@ri)@V/(a*a)
            errors.append(float(np.linalg.norm(q-target)))
        assert errors[-1]<.001
        assert all(b<a for a, b in zip(errors, errors[1:])), errors
        limits.append(dict(pair=f'{NAMES[i]}{NAMES[j]}', result=NAMES[k],
                           final_error=errors[-2], small_angle_error=errors[-1]))
    # The finite two-step playback must agree exactly with its labeled product.
    assert np.allclose(rotation3(0, .85)@(rotation3(1, .85)@V),
                       (rotation3(0, .85)@rotation3(1, .85))@V)
    for t in np.linspace(14, 32.99, 381):
        pair, angle, blue, red = pair_state(t)
        q = (blue@V-red@V)/(angle*angle)
        i, j, k = PAIRS[pair]
        tangent = GENERATORS[k]@V
        points = np.array([project((716, 1305), 145, p) for p in (V, V+q, V+tangent)])
        assert points[:, 0].min()>540 and points[:, 0].max()<935, (t, points)
        assert points[:, 1].min()>1160 and points[:, 1].max()<1455, (t, points)
    for i, j, k in PAIRS:
        orbit = np.array([project((716, 1305), 145, rotation3(k, theta)@V)
                          for theta in np.linspace(0, 2*math.pi, 361)])
        assert orbit[:, 0].min()>540 and orbit[:, 0].max()<935
        assert orbit[:, 1].min()>1160 and orbit[:, 1].max()<1455, (k, orbit.min(axis=0), orbit.max(axis=0))
    return dict(convention='active real skew generators; blue minus red',
                order='blue = Ri(a) Rj(b), j acts first', cyclic_limits=limits,
                final_angle_radians=SMALL_ANGLE, final_magnification=1/SMALL_ANGLE**2,
                frame_rate=FPS, duration=DURATION, dimensions=[W, H],
                normalized_arrow_samples=381)
