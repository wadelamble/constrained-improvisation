"""Portrait drawing tools for the independent Symmetry to Waves review series.

All coordinates are final 1080 x 1920 pixels. The manuscript and prior reels
are inputs only. Essential artwork belongs inside x=70..950, y=160..1620.
"""
from __future__ import annotations

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
import math
from functools import lru_cache
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image

W, H, FPS = 1080, 1920, 30
TOTAL = 27
TEXT_REPLACEMENTS = {}
BG, PANEL, INK = '#080b14', '#111a2a', '#fff2e4'
MUTED, GRID = '#a5b2c8', '#334258'
BLUE, RED, GOLD, GREEN, PURPLE = '#46beff', '#ff4269', '#ffb45e', '#36e099', '#b999ff'


@lru_cache(128)
def font(size=32, bold=False):
    filename = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    paths = [Path('C:/Windows/Fonts') / filename,
             Path(matplotlib.get_data_path()) / 'fonts' / 'ttf' /
             ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in paths:
        if path.exists():
            return ImageFont.truetype(str(path), round(size))
    return ImageFont.load_default()


def ease(u):
    u = np.clip(u, 0, 1)
    return u*u*(3-2*u)


def lerp(a, b, u):
    return a + (b-a)*u


def window(t, a, b):
    return float(np.clip((t-a)/(b-a), 0, 1))


@lru_cache(512)
def equation(tex, size=44, color=INK):
    buf = BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$'+tex+'$', buf, format='png', dpi=150, color=color,
                      prop=matplotlib.font_manager.FontProperties(size=size*72/150))
    buf.seek(0)
    return Image.open(buf).convert('RGBA')


def fitted_title(draw, title, x=70, y=269, width=880, max_height=138, size=54):
    for chosen in range(size, 29, -1):
        lines = []
        for paragraph in title.split('\n'):
            line = ''
            for word in paragraph.split():
                candidate = (line+' '+word).strip()
                if line and draw.textlength(candidate, font=font(chosen, True)) > width:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        leading = round(chosen*1.13)
        boxes = [draw.textbbox((x, y+i*leading), line,
                              font=font(chosen, True), anchor='la')
                 for i, line in enumerate(lines)]
        if boxes and max(b[3] for b in boxes) <= y+max_height and max(b[2] for b in boxes) <= x+width:
            break
    else:
        raise ValueError(f'Title does not fit: {title}')
    for i, line in enumerate(lines):
        draw.text((x, y+i*leading), line, font=font(chosen, True), fill=INK, anchor='la')
    return dict(size=chosen, lines=lines, boxes=boxes)


def apply_series_numbering(image, number, total=TOTAL):
    """Replace only the series-number strips, preserving the scientific scene."""
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 205, 960, 262), fill=BG)
    draw.text((70, 217), f'{number:02d}  /  SYMMETRY TO WAVES',
              font=font(27, True), fill=GOLD, anchor='la')
    draw.rectangle((60, 1692, 975, 1790), fill=BG)
    draw.text((70, 1717), f'A series in {total} parts',
              font=font(25), fill=MUTED, anchor='la')
    draw.text((950, 1717), f'{number:02d} / {total:02d}',
              font=font(25), fill=MUTED, anchor='ra')
    return image


def numbering_overlay(number, total=TOTAL):
    """Opaque number strips on a transparent 1080 x 1920 RGBA canvas.

    Inclusive strip bounds are (60,205,960,262) and (60,1692,975,1790).
    The time-progress rule at y=1676 is outside both strips.
    """
    return apply_series_numbering(Image.new('RGBA', (W, H), (0, 0, 0, 0)), number, total)


class Scene:
    def __init__(self, number, title, stage='', t=0, duration=24, total=TOTAL):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.number, self.duration = number, duration
        self.text(70, 163, 'VARIATIONS ON SYMMETRY', 25, MUTED, bold=True)
        self.text(70, 217, f'{number:02d}  /  SYMMETRY TO WAVES', 27, GOLD, bold=True)
        self.title_layout = fitted_title(self.d, title)
        if stage:
            self.text(70, 420, stage, 31, MUTED)
        self.d.line((70, 1676, 950, 1676), fill=GRID, width=3)
        self.d.line((70, 1676, 70+880*float(np.clip(t/duration, 0, 1)), 1676), fill=GOLD, width=4)
        self.text(70, 1717, f'A series in {total} parts', 25, MUTED)
        self.text(950, 1717, f'{number:02d} / {total:02d}', 25, MUTED, anchor='ra')

    def text(self, x, y, value, size=32, color=INK, bold=False, anchor='la'):
        value = TEXT_REPLACEMENTS.get(str(value), value)
        self.d.text((x, y), str(value), font=font(size, bold), fill=color, anchor=anchor)

    def wrap(self, value, x, y, width, size=32, color=INK, bold=False, leading=None):
        leading = leading or round(size*1.32)
        yy = y
        for paragraph in str(value).split('\n'):
            line = ''
            for word in paragraph.split():
                proposed = (line+' '+word).strip()
                if self.d.textlength(proposed, font=font(size, bold)) > width and line:
                    self.text(x, yy, line, size, color, bold)
                    yy += leading
                    line = word
                else:
                    line = proposed
            self.text(x, yy, line, size, color, bold)
            yy += leading
        return yy

    def math(self, tex, x=510, y=1510, size=44, color=INK, maxwidth=880):
        tex = TEXT_REPLACEMENTS.get(tex, tex)
        pic = equation(tex, size, color)
        if pic.width > maxwidth:
            pic = pic.resize((maxwidth, round(pic.height*maxwidth/pic.width)), Image.Resampling.LANCZOS)
        self.im.paste(pic, (round(x-pic.width/2), round(y-pic.height/2)), pic)

    def panel(self, box, label=None, color=MUTED):
        self.d.rounded_rectangle(tuple(box), radius=22, fill=PANEL, outline=GRID, width=2)
        if label:
            self.text(box[0]+24, box[1]+22, label, 30, color)

    def line(self, points, color=BLUE, width=3):
        points = np.asarray(points, dtype=float)
        if len(points) >= 2:
            self.d.line([tuple(p) for p in points], fill=color, width=round(width), joint='curve')

    def arrow(self, start, end, color=GOLD, width=5, head=16):
        a, b = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
        self.line([a, b], color, width)
        u = b-a
        n = np.linalg.norm(u)
        if n < 1:
            return
        u /= n
        v = np.array([-u[1], u[0]])
        self.d.polygon([tuple(b), tuple(b-head*u+.48*head*v), tuple(b-head*u-.48*head*v)], fill=color)

    def dot(self, p, r=6, color=GOLD):
        self.d.ellipse((p[0]-r, p[1]-r, p[0]+r, p[1]+r), fill=color)

    def note(self, value, y=1580, color=MUTED, size=30):
        return self.wrap(value, 70, y, 880, size=size, color=color, leading=39)

    def matrix(self, rows, x, y, cell=67, size=38, color=INK, highlights=()):
        """Draw a small numeric or symbolic matrix, centered at (x,y)."""
        nr, nc = len(rows), len(rows[0])
        left, top = x-nc*cell/2, y-nr*cell/2
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.text(left+(j+.5)*cell, top+(i+.5)*cell, value, size,
                          GOLD if (i, j) in highlights else color, anchor='mm')
        for edge, sign in ((left-14, 1), (left+nc*cell+14, -1)):
            self.line([(edge+sign*10, top), (edge, top),
                       (edge, top+nr*cell), (edge+sign*10, top+nr*cell)], color, 3)


def axes(scene, origin, xrange, yrange, color=GRID, labels=('x', 'y')):
    x, y = origin
    scene.line([(x+xrange[0], y), (x+xrange[1], y)], color, 2)
    scene.line([(x, y+yrange[0]), (x, y+yrange[1])], color, 2)
    if labels:
        scene.text(x+xrange[1]+10, y+8, labels[0], 30, MUTED)
        scene.text(x+12, y+yrange[0]-8, labels[1], 30, MUTED, anchor='ls')


def rotation(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def helix(scene, x, z, box, color=BLUE, envelope=True, gain=None, depth=.28):
    x, z = np.asarray(x), np.asarray(z)
    left, top, right, bottom = box
    cy = (top+bottom)/2
    gain = gain if gain is not None else .38*(bottom-top)
    xx = left+(x-x.min())/(x.max()-x.min())*(right-left)
    scene.line([(left, cy), (right, cy)], GRID, 2)
    if envelope:
        scene.line(np.c_[xx, cy-gain*abs(z)], GOLD, 2)
        scene.line(np.c_[xx, cy+gain*abs(z)], GOLD, 2)
    zz = z*np.exp(-.38j)
    points = np.c_[xx+depth*gain*zz.imag, cy-gain*zz.real]
    scene.line(points, color, 4)
    return points


def phasor(scene, origin, z, scale=100, color=GOLD, width=5):
    end = (origin[0]+scale*z.real, origin[1]-scale*z.imag)
    scene.arrow(origin, end, color, width)
    return end
