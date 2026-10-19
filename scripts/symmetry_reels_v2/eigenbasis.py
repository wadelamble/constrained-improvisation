"""Episode 20: two bases on the same visibly deforming rubber sheet."""
from __future__ import annotations

from core import *


# Keep the established editable slots in their original order.
SCREEN_TEXT = [
    "Ordinary basis", "Eigenbasis",
    r"a=\frac{s+s^{-1}}{2},\qquad b=\frac{s-s^{-1}}{2}",
    "s = [value]", "x", "y", "u", "v", "x′", "y′", "s u", "s⁻¹ v",
    r"x'=ax+by,\qquad y'=bx+ay",
    r"u'=su,\qquad v'=s^{-1}v",
]


def rubber_sheet(scene, project, transform):
    """Carry a finite material square and its grid through the arrow's map.

    The grid is painted on the sheet, rather than fixed coordinate axes.
    Reciprocal principal stretches preserve every cell's area.
    """
    mesh = np.linspace(-1., 1., 9)

    def point(x, y):
        return project(transform @ np.array([x, y]))

    for i, (left, right) in enumerate(zip(mesh[:-1], mesh[1:])):
        for j, (bottom, top) in enumerate(zip(mesh[:-1], mesh[1:])):
            corners = [point(left, bottom), point(right, bottom),
                       point(right, top), point(left, top)]
            scene.d.polygon([tuple(v) for v in corners],
                            fill='#1d3543' if (i+j) % 2 else '#182f3c')
    for value in mesh[1:-1]:
        scene.line([point(value, -1), point(value, 1)], '#557c8d', 2)
        scene.line([point(-1, value), point(1, value)], '#557c8d', 2)
    corners = [point(-1, -1), point(1, -1), point(1, 1), point(-1, 1)]
    scene.line(corners + corners[:1], '#94bfcb', 4)
    for corner in corners:
        scene.dot(corner, 6, '#b5dae2')


def render(t, entry):
    duration = float(entry.get("duration", 25))
    q = float(np.clip(t / duration, 0, 1)) * 24
    s = Scene(20, entry["title"], "Ordinary basis" if q < 12 else "Eigenbasis",
              t=t, duration=duration)
    stretch = 1 + .8*float(ease(window(q, 2, 17)))
    aa, bb = (stretch+1/stretch)/2, (stretch-1/stretch)/2
    transform = np.array([[aa, bb], [bb, aa]])
    s.math(r"a=\frac{s+s^{-1}}{2},\qquad b=\frac{s-s^{-1}}{2}", y=510, size=46)
    reading = TEXT_REPLACEMENTS.get("s = [value]", "s = [value]")
    s.text(510, 560, reading.replace("[value]", f"{stretch:.2f}"), 33, GOLD, anchor="ma")
    for origin, eigen in ((np.array([510., 815.]), False),
                          (np.array([510., 1340.]), True)):
        scale = 120.

        def p(v):
            return origin + scale*np.asarray(v)*[1, -1]

        rubber_sheet(s, p, transform)

        if not eigen:
            basis = [np.array([1., 0.]), np.array([0., 1.])]
            transformed = [np.array([aa, bb]), np.array([bb, aa])]
            labels = ("x′", "y′")
        else:
            # These are the same oriented axes used by the desktop source
            # and the following component-decomposition episode.
            basis = [np.array([1., 1.])/math.sqrt(2), np.array([1., -1.])/math.sqrt(2)]
            transformed = [stretch*basis[0], basis[1]/stretch]
            labels = ("s u", "s⁻¹ v")
        for index, v in enumerate(basis):
            extent = (1.95 if index == 0 else 1.8) if eigen else (1.6 if index == 0 else 1.2)
            s.line([p(-1.5*v), p(extent*v)], '#64778c', 2)
            s.arrow(origin, p(v), MUTED, 3, 14)
        if not eigen:
            s.text(735, 814, "x", 30, MUTED)
            s.text(460, 635, "y", 30, MUTED, anchor="ra")
        else:
            s.text(755, 1140, "u", 30, MUTED)
            # The southeast axis ends above the equation; its label sits
            # to its right, with a clear gap above the footer formula.
            s.text(697, 1510, "v", 30, MUTED, anchor="mm")
        for vec, label, color in zip(transformed, labels, (BLUE, RED)):
            end = p(vec)
            s.arrow(origin, end, BG, 12, 25)
            s.arrow(origin, end, color, 7, 21)
            if not eigen:
                # Keep x-prime above the fixed horizontal axis throughout
                # the stretch, rather than sweeping its text through it.
                delta = (40, -60) if color == BLUE else (-28, 22)
                if color == RED:
                    position = (end[0]+delta[0], end[1]+delta[1])
                    visible = TEXT_REPLACEMENTS.get(label, label)
                    box = s.d.textbbox(position, visible, font=font(34), anchor="ra")
                    s.d.rounded_rectangle((box[0]-5, box[1]-3, box[2]+5, box[3]+3),
                                          radius=4, fill=BG)
                s.text(end[0]+delta[0], end[1]+delta[1], label, 34, color,
                       anchor="ma" if color == BLUE else "ra")
            elif color == BLUE:
                s.text(end[0]+70, end[1]-15, label, 32, color)
            else:
                s.text(end[0]+65, end[1]-15, label, 32, color)
    s.math(r"x'=ax+by,\qquad y'=bx+ay", y=1080, size=47)
    s.math(r"u'=su,\qquad v'=s^{-1}v", y=1610, size=51, color=GOLD)
    return s.im
