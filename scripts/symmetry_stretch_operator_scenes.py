"""Whole-grid introductions and conjugation for two stretch operators."""
from __future__ import annotations

from functools import lru_cache
import hashlib
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties
from symmetry_exponential_desktop_common import (
    Canvas, BLUE, GOLD, GREEN, INK, MUTED, FAINT, BG, ease,
)

ANGLE = math.pi / 4
IDENTITY = np.eye(2)
PLOT = (64, 220, 1030, 752)
ORIGIN = np.array([490., 570.])
SCALE = 75
CELL = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.], [0., 0.]]).T


def rotation(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]])


def points(m, p):
    transformed = m @ np.asarray(p, dtype=float)
    return np.column_stack((ORIGIN[0] + SCALE * transformed[0],
                            ORIGIN[1] - SCALE * transformed[1]))


def draw_grid(c, m):
    x0, y0, x1, y1 = PLOT
    im = Image.new('RGB', (x1-x0, y1-y0), BG)
    d = ImageDraw.Draw(im)
    offset = np.array([x0, y0])

    def path(p, mat=m):
        return points(mat, p)-offset

    def line(p, color, width=1, mat=m):
        d.line([tuple(a) for a in path(p, mat)], fill=color, width=width)

    for n in range(-14, 15):
        line([[n, n], [-16, 16]], '#eee9df', 1, IDENTITY)
        line([[-16, 16], [n, n]], '#eee9df', 1, IDENTITY)
    line([[-16, 16], [0, 0]], '#c1bcb3', 2, IDENTITY)
    line([[0, 0], [-16, 16]], '#c1bcb3', 2, IDENTITY)
    cell = path(CELL)
    d.polygon([tuple(a) for a in cell], fill='#dce8ee')
    for n in range(-14, 15):
        line([[n, n], [-16, 16]], '#9eafb8', 2)
        line([[-16, 16], [n, n]], '#9eafb8', 2)
    line([[-16, 16], [0, 0]], BLUE, 4)
    line([[0, 0], [-16, 16]], GOLD, 4)
    d.line([tuple(a) for a in cell], fill=BLUE, width=5)
    e1, e2 = m[:, 0], m[:, 1]
    e1, e2 = e1/np.linalg.norm(e1), e2/np.linalg.norm(e2)
    if abs(e1 @ e2) < .0001:
        corner = np.column_stack((.20*e1, .20*(e1+e2), .20*e2))
        line(corner, INK, 2, IDENTITY)
    else:
        start, end = math.atan2(e1[1], e1[0]), math.atan2(e2[1], e2[0])
        while end < start:
            end += 2*math.pi
        theta = np.linspace(start, end, 30)
        line(.25*np.array([np.cos(theta), np.sin(theta)]), INK, 2, IDENTITY)
    c.im.paste(im, (x0, y0))
    c.d.rectangle(PLOT, outline=FAINT, width=1)
    c.dot(ORIGIN, 4, INK)


@lru_cache(6)
def graphic_formula(active):
    parsed = MathTextParser('agg').parse(
        r'$A_s=U_s^\dagger A U_s$', dpi=180,
        prop=FontProperties(size=96*72/180))
    pixels = np.asarray(parsed.image, dtype=np.uint8)
    occupied = np.flatnonzero(pixels.any(axis=0))
    groups = np.split(occupied, np.flatnonzero(np.diff(occupied)>1)+1)
    assert len(groups) == 8, len(groups)
    glyphs = [(int(g[0]), int(g[-1])+1) for g in groups]
    bounds = [(glyphs[a][0], glyphs[b][1])
              for a, b in ((0, 1), (2, 2), (3, 4), (5, 5), (6, 7))]
    im = Image.new('RGBA', (pixels.shape[1], pixels.shape[0]), INK)
    if active is not None:
        a, b = bounds[active]
        ImageDraw.Draw(im).rectangle((a, 0, b, im.height), fill=GREEN)
    im.putalpha(Image.fromarray(pixels))
    return im, bounds


def sandwich_graphic(c, phase):
    active = {1: 4, 2: 3, 3: 2, 4: 0, 5: 0}.get(phase)
    im, bounds = graphic_formula(active)
    left, top = round((PLOT[0]+PLOT[2]-im.width)/2), 190
    bottom = top+im.height
    c.d.rounded_rectangle((left-22, top-15, left+im.width+22, bottom+18),
                          radius=13, fill=BG)
    c.track((left, top, left+im.width, bottom), 'large sandwich equation')
    c.im.paste(im, (left, top), im)
    if active is not None:
        a, b = bounds[active]
        c.line([(left+a, bottom+9), (left+b, bottom+9)], GREEN, 4)


class StretchScenes:
    def __init__(self, uniform=False):
        self.uniform = uniform
        self.kind = 'uniform' if uniform else 'horizontal'
        self.name = 'symmetry-' + ('uniform-' if uniform else '') + 'operator-sandwich'
        self.A = np.diag([2., 2. if uniform else 1.])
        self.main_start = 6 if uniform else 12
        self.duration = self.main_start + 11
        self.starts = (0, 6) if uniform else (0, 6, 12)
        self.moments = ((0, 2.5, 4.5, 6.5, 8, 11, 13, 14.5, 16.5) if uniform
                        else (2.5, 4.5, 8.5, 12.5, 14, 17, 19, 20.5, 22.5))
        self.poster = self.duration - 2.5

    def conjugate(self, s):
        u = rotation(s)
        # Remove floating-point residue before rasterization, so an invariant
        # grid does not jump across integer pixel boundaries as s varies.
        return np.round(u.T @ self.A @ u, 14)

    def state(self, t):
        if t < 6:
            amount = ease((t-.6)/1.7) if t < 3 else 1-ease((t-3)/1.7)
            return dict(scene='A', matrix=IDENTITY+amount*(self.A-IDENTITY),
                        symbol='A', phase=1 if t < 3 else 2, angle=0,
                        note='Apply A' if t < 3 else 'Undo the stretch with A⁻¹')
        if t < self.main_start:
            q = t-6
            angle = ANGLE*(ease((q-.5)/1.9) if q < 3 else 1-ease((q-3)/2.4))
            return dict(scene='U', matrix=rotation(angle), symbol='U_s', phase=0,
                        angle=angle, note='Rotate space, then rotate back')
        q = min(t-self.main_start, 11)
        if q < 3.5:
            m = rotation(ANGLE*ease((q-1)/2))
            phase, symbol, note = 1, 'U_s', 'Rotate space 45° counterclockwise'
        elif q < 6:
            m = (IDENTITY+ease((q-3.5)/2)*(self.A-IDENTITY)) @ rotation(ANGLE)
            phase, symbol, note = 2, 'A U_s', 'Apply the ' + self.kind + ' stretch'
        elif q < 8:
            m = rotation(-ANGLE*ease((q-6)/2)) @ self.A @ rotation(ANGLE)
            phase, symbol, note = 3, r'U_s^\dagger A U_s', 'Rotate space back'
        else:
            angle = ANGLE*(1-ease((q-9)/2))
            m = self.conjugate(angle)
            return dict(scene='main', matrix=m, phase=4 if q < 9 else 5,
                        symbol='A_s', angle=angle,
                        note='The complete operator' if q < 9 else 'Vary the rotation angle s')
        return dict(scene='main', matrix=m, phase=phase, symbol=symbol,
                    angle=ANGLE, note=note)

    def matrix_panel(self, c, st):
        scene, phase, cx = st['scene'], st['phase'], 1300
        if scene == 'A':
            heading, subhead, matrix = self.kind.capitalize()+' stretch', 'operator A', self.A
        elif scene == 'U':
            heading, subhead, matrix = 'Rotation', 'transformation Uₛ', st['matrix']
        elif phase < 4:
            heading, subhead, matrix = 'Current grid map', 'during the construction', st['matrix']
        else:
            heading, subhead, matrix = 'Transformed operator', 'Aₛ', st['matrix']
        c.text(cx, 244, heading, 25, MUTED, anchor='mm')
        c.text(cx, 277, subhead, 25, MUTED, anchor='mm')
        c.math(cx, 329, st['symbol'], 35, center=True)
        c.line([(1143, 350), (1125, 350), (1125, 505), (1143, 505)], INK, 3)
        c.line([(1457, 350), (1475, 350), (1475, 505), (1457, 505)], INK, 3)
        for i in range(2):
            for j in range(2):
                v = float(matrix[i, j])
                c.text(1203+194*j, 385+84*i, f'{0. if abs(v)<.005 else v:.2f}',
                       43, BLUE if j == 0 else GOLD, anchor='mm')
        c.text(cx, 553, st['note'], 21, INK, anchor='mm')
        if scene == 'main':
            labels = ('Uₛ  rotate counterclockwise', 'A  stretch', 'Uₛ†  rotate back')
            for i, label in enumerate(labels):
                c.text(cx, 606+36*i, label, 23,
                       GREEN if phase == i+1 else MUTED, bold=phase == i+1, anchor='mm')
            if phase >= 4:
                c.text(cx, 721, f's = {math.degrees(st["angle"]):.0f}°', 25, GREEN, anchor='mm')
                if self.uniform:
                    c.math(cx, 765, 'A_s=A', 32, GREEN, center=True)
        elif scene == 'U':
            c.text(cx, 620, f's = {math.degrees(st["angle"]):.0f}°', 30, GREEN, anchor='mm')

    def render(self, t, boxes=False):
        st = self.state(t)
        c = Canvas()
        c.text(64, 35, 'EVOLVING A MATRIX TRANSFORMATION', 19, MUTED)
        if st['scene'] == 'A':
            c.text(64, 76, f'A is the {self.kind} stretch operator to be transformed', 36, INK, bold=True)
            c.math(66, 165, r'A:\ (x,y)\longmapsto(2x,'+('2y' if self.uniform else 'y')+')', 33)
            line1 = 'The square expands equally in both directions.' if self.uniform else 'The square stretches horizontally.'
            line2 = 'The return motion undoes the stretch.'
        elif st['scene'] == 'U':
            c.text(64, 76, 'Uₛ is a rotation transformation', 40, INK, bold=True)
            c.math(66, 165, 'U_s=R(s)', 33)
            line1, line2 = 'Rotate the whole grid 45° counterclockwise.', 'Then rotate it back.'
        else:
            c.text(64, 76, 'Evolve A under the transformation Uₛ', 40, INK, bold=True)
            line1 = 'Read the product from right to left: rotate, stretch, rotate back.'
            line2 = 'The right-hand rotation acts before the stretch.'
            if st['phase'] >= 4:
                line2 = 'The uniform stretch is unchanged.' if self.uniform else 'The stretching direction is now rotated 45° clockwise.'
            if st['phase'] == 5:
                line1 = 'Now vary s in the complete operator Aₛ.'
                line2 = 'The uniform stretch stays unchanged.' if self.uniform else 'The horizontal stretch changes orientation as s changes.'
        draw_grid(c, st['matrix'])
        if st['scene'] == 'main':
            sandwich_graphic(c, st['phase'])
        self.matrix_panel(c, st)
        c.text(64, 785, line1, 28, INK)
        c.text(64, 828, line2, 24, GREEN if st['scene']=='main' and st['phase']>=4 else MUTED)
        c.text(1535, 850, f'{t:04.1f} / {self.duration}s', 18, MUTED, anchor='ra')
        c.line([(64, 879), (1536, 879)], FAINT, 2)
        c.line([(64, 879), (64+1472*min(t/self.duration, 1), 879)], GOLD, 3)
        return c if boxes else c.im

    def validate(self):
        assert np.allclose(self.state(2.5)['matrix'], self.A)
        assert np.allclose(self.state(5)['matrix'], IDENTITY)
        expected = 2*IDENTITY if self.uniform else np.array([[1.5, -.5], [-.5, 1.5]])
        assert np.allclose(self.conjugate(ANGLE), expected)
        G = 1j*np.array([[0., -1.], [1., 0.]])
        derivative_error, change = 0., 0.
        for s in np.linspace(0, ANGLE, 20):
            mat, h = self.conjugate(s), 1e-5
            derivative = (self.conjugate(s+h)-self.conjugate(s-h))/(2*h)
            derivative_error = max(derivative_error, float(np.max(np.abs(derivative-1j*(G@mat-mat@G)))))
            change = max(change, float(np.max(np.abs(mat-self.A))))
        assert derivative_error < 1e-8
        assert change < 1e-12 if self.uniform else change > .49
        phases = [self.state(t)['phase']
                  for t in np.linspace(self.main_start, self.duration, 100)]
        assert phases == sorted(phases)
        assert phases[0] == 1 and phases[-1] == 5
        assert np.allclose(self.state(self.duration)['matrix'], self.A)
        min_clearance = float('inf')
        formula_bottom = 190+graphic_formula(None)[0].height+18
        for t in np.linspace(0, self.duration-.01, 700):
            st = self.state(t)
            assert np.linalg.det(st['matrix']) >= 1-1e-10
            if st['scene'] == 'main':
                min_clearance = min(min_clearance, float(points(st['matrix'], CELL)[:, 1].min()-formula_bottom))
                if st['phase'] >= 4:
                    assert np.allclose(st['matrix'], self.conjugate(st['angle']))
        assert min_clearance > 8, min_clearance
        collisions = []
        for t in sorted(set(self.moments+tuple(self.starts))):
            c = self.render(t, True)
            for i, (a, al) in enumerate(c.boxes):
                for b, bl in c.boxes[i+1:]:
                    if min(a[2], b[2])-max(a[0], b[0]) > 1 and min(a[3], b[3])-max(a[1], b[1]) > 1:
                        collisions.append(dict(t=t, a=al, b=bl))
        assert not collisions, collisions
        return dict(model=f'Whole-grid conjugation of {self.kind} stretch',
                    A=self.A.tolist(), stages=self.starts, repetitions=1,
                    construction_cycle_seconds=11, target=expected.tolist(),
                    derivative_max_error=derivative_error, operator_change=change,
                    equation_cell_clearance_pixels=min_clearance, label_collisions=collisions,
                    scene_renderer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
