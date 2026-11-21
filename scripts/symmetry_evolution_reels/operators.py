"""Portrait whole-grid operator scenes, using the existing mathematical states.

The desktop source remains the authority for timing and transformation order.
Only the layout is new: a large portrait grid, then equation and matrix readout.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib
import math as pymath
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS.parent / '.tools/animation-python-packages'))

import numpy as np
from PIL import Image, ImageColor, ImageDraw
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties

from symmetry_stretch_operator_scenes import StretchScenes, rotation, ANGLE, CELL
try:
    from .core import BG, PANEL, INK, MUTED, GRID, BLUE, GOLD, GREEN, font, frame, text, math
except ImportError:
    from core import BG, PANEL, INK, MUTED, GRID, BLUE, GOLD, GREEN, font, frame, text, math

DURATIONS = {3: 23, 4: 17}
durations = DURATIONS
TITLES = {3: 'Transforming an operator', 4: 'Commuting operators'}
MOMENTS = {
    3: (0, 2.5, 5, 8.5, 11.5, 12.5, 14.5, 17, 19, 20.5, 22.9),
    4: (0, 2.5, 5, 6.5, 8.5, 11, 13, 14.5, 16.9),
}
POSTERS = {3: 20.5, 4: 14.5}
SCENES = {3: StretchScenes(False), 4: StretchScenes(True)}

PLOT = (80, 540, 940, 1150)
ORIGIN = np.array([480., 970.])
SCALE = 118.
IDENTITY = np.eye(2)


def _blend(a, b, fraction):
    aa, bb = np.array(ImageColor.getrgb(a)), np.array(ImageColor.getrgb(b))
    return tuple(np.rint((1-fraction)*aa+fraction*bb).astype(int))


def _points(matrix, coordinates):
    transformed = matrix @ np.asarray(coordinates, dtype=float)
    return np.column_stack((ORIGIN[0]+SCALE*transformed[0],
                            ORIGIN[1]-SCALE*transformed[1]))


def _grid(image, matrix):
    """Apply the current linear map to the complete grid and a marked cell."""
    x0, y0, x1, y1 = PLOT
    layer = Image.new('RGB', (x1-x0, y1-y0), PANEL)
    draw = ImageDraw.Draw(layer)
    offset = np.array([x0, y0])

    def path(coordinates, transform=matrix):
        return _points(transform, coordinates)-offset

    def line(coordinates, fill, width=1, transform=matrix):
        draw.line([tuple(p) for p in path(coordinates, transform)],
                  fill=fill, width=width)

    # A fixed, faint reference grid makes the complete-grid motion legible.
    for n in range(-12, 13):
        line([[n, n], [-14, 14]], _blend(PANEL, GRID, .36), transform=IDENTITY)
        line([[-14, 14], [n, n]], _blend(PANEL, GRID, .36), transform=IDENTITY)
    line([[-14, 14], [0, 0]], _blend(PANEL, MUTED, .34), 2, IDENTITY)
    line([[0, 0], [-14, 14]], _blend(PANEL, MUTED, .34), 2, IDENTITY)
    cell = path(CELL)
    draw.polygon([tuple(p) for p in cell], fill=_blend(PANEL, BLUE, .2))
    for n in range(-12, 13):
        line([[n, n], [-14, 14]], _blend(PANEL, MUTED, .65), 2)
        line([[-14, 14], [n, n]], _blend(PANEL, MUTED, .65), 2)
    line([[-14, 14], [0, 0]], BLUE, 5)
    line([[0, 0], [-14, 14]], GOLD, 5)
    draw.line([tuple(p) for p in cell], fill=BLUE, width=6, joint='curve')

    # The angle mark follows the actual basis vectors; it is not decorative.
    e1, e2 = matrix[:, 0], matrix[:, 1]
    e1, e2 = e1/np.linalg.norm(e1), e2/np.linalg.norm(e2)
    if abs(e1@e2) < .0001:
        corner = np.column_stack((.19*e1, .19*(e1+e2), .19*e2))
        line(corner, INK, 3, IDENTITY)
    else:
        a, b = pymath.atan2(e1[1], e1[0]), pymath.atan2(e2[1], e2[0])
        while b < a:
            b += 2*pymath.pi
        angles = np.linspace(a, b, 40)
        line(.25*np.array([np.cos(angles), np.sin(angles)]), INK, 3, IDENTITY)
    image.paste(layer, (x0, y0))
    draw = ImageDraw.Draw(image)
    draw.rectangle(PLOT, outline=GRID, width=2)
    ox, oy = ORIGIN
    draw.ellipse((ox-5, oy-5, ox+5, oy+5), fill=INK)


@lru_cache(6)
def _sandwich_image(active):
    """Color the acting factor in one large, typographically intact equation."""
    parsed = MathTextParser('agg').parse(
        r'$A_s=U_s^\dagger A U_s$', dpi=180,
        prop=FontProperties(size=82*72/180))
    pixels = np.asarray(parsed.image, dtype=np.uint8)
    occupied = np.flatnonzero(pixels.any(axis=0))
    groups = np.split(occupied, np.flatnonzero(np.diff(occupied)>1)+1)
    assert len(groups) == 8, len(groups)
    glyphs = [(int(g[0]), int(g[-1])+1) for g in groups]
    bounds = [(glyphs[a][0], glyphs[b][1])
              for a, b in ((0, 1), (2, 2), (3, 4), (5, 5), (6, 7))]
    pic = Image.new('RGBA', (pixels.shape[1], pixels.shape[0]), INK)
    if active is not None:
        a, b = bounds[active]
        ImageDraw.Draw(pic).rectangle((a, 0, b, pic.height), fill=GREEN)
    pic.putalpha(Image.fromarray(pixels))
    return pic, bounds


def _sandwich(image, phase, boxes):
    active = {1: 4, 2: 3, 3: 2, 4: 0, 5: 0}[phase]
    pic, ranges = _sandwich_image(active)
    left, top = round(510-pic.width/2), round(1238-pic.height/2)
    image.paste(pic, (left, top), pic)
    boxes.append(((left, top, left+pic.width, top+pic.height), 'sandwich equation'))
    a, b = ranges[active]
    ImageDraw.Draw(image).line([(left+a, top+pic.height+9),
                               (left+b, top+pic.height+9)], fill=GREEN, width=4)


def _label(draw, xy, value, size, boxes, fill=INK, bold=False, anchor='mm'):
    box = draw.textbbox(xy, value, font=font(size, bold), anchor=anchor)
    boxes.append((box, value))
    text(draw, xy, value, size=size, fill=fill, anchor=anchor, bold=bold)


def _formula(image, tex, xy, size, boxes, fill=INK):
    box = math(image, tex, xy, size=size, fill=fill, anchor='mm', max_width=840)
    boxes.append((box, tex))


def _matrix(image, draw, matrix, heading, boxes, angle=None):
    _label(draw, (510, 1342), heading, 28, boxes, MUTED)
    # The readout is below the formula, never over moving geometry.
    left, right, top, bottom = 346, 674, 1389, 1511
    draw.line([(left+14, top), (left, top), (left, bottom), (left+14, bottom)],
              fill=INK, width=3)
    draw.line([(right-14, top), (right, top), (right, bottom), (right-14, bottom)],
              fill=INK, width=3)
    for row in range(2):
        for col in range(2):
            value = float(matrix[row, col])
            value = 0. if abs(value) < .005 else value
            _label(draw, (428+164*col, 1416+68*row), f'{value:.2f}',
                   45, boxes, BLUE if col == 0 else GOLD)
    if angle is not None:
        _label(draw, (814, 1450), f's = {pymath.degrees(angle):.0f}°',
               31, boxes, GREEN)


def _stage(scene, st):
    if st['scene'] == 'A':
        return ('Apply '+scene.kind+' stretch' if st['phase'] == 1
                else 'Undo the stretch with A⁻¹')
    if st['scene'] == 'U':
        return 'Rotate the grid, then rotate back'
    return {
        1: 'Rotate 45° counterclockwise',
        2: 'Apply the '+scene.kind+' stretch',
        3: 'Rotate back',
        4: 'The complete operator',
        5: 'Vary the rotation angle s',
    }[st['phase']]


def render(index, t, *, _boxes=False):
    """Return one RGB portrait frame, with original source timing intact."""
    scene = SCENES[index]
    t = max(0., min(float(t), DURATIONS[index]))
    st = scene.state(t)
    image, draw = frame(TITLES[index], index, t, DURATIONS[index])
    boxes = []
    _label(draw, (510, 488), _stage(scene, st), 33, boxes, INK, True)
    _grid(image, st['matrix'])
    if st['scene'] == 'main':
        _sandwich(image, st['phase'], boxes)
        heading = 'Transformed operator' if st['phase'] >= 4 else 'Current grid map'
        _matrix(image, draw, st['matrix'], heading, boxes,
                st['angle'] if st['phase'] >= 4 else None)
        if scene.uniform and st['phase'] >= 4:
            _formula(image, r'[A,U_s]=0\quad\Longrightarrow\quad A_s=A',
                     (510, 1570), 43, boxes, GREEN)
        elif st['phase'] >= 4:
            _label(draw, (510, 1570), 'The stretching direction changes with s.',
                   29, boxes, MUTED)
        else:
            _label(draw, (510, 1570), 'Rightmost factor acts first.',
                   29, boxes, MUTED)
    elif st['scene'] == 'A':
        _formula(image, r'A:\ (x,y)\longmapsto(2x,'+('2y' if scene.uniform else 'y')+')',
                 (510, 1238), 63, boxes)
        _matrix(image, draw, scene.A, 'Uniform stretch A' if scene.uniform else 'Horizontal stretch A', boxes)
        _formula(image, r'A^\dagger A\ne I', (510, 1570), 43, boxes, MUTED)
    else:
        _formula(image, r'U_s=R(s)', (510, 1238), 74, boxes)
        _matrix(image, draw, st['matrix'], 'Rotation Uₛ', boxes, st['angle'])
        _formula(image, r'U_s^\dagger U_s=I', (510, 1570), 43, boxes, GREEN)
    return (image, boxes) if _boxes else image.convert('RGB')


def validate():
    """Retain source tests and verify portrait-specific bounds and geometry."""
    report = {}
    for index, scene in SCENES.items():
        source = scene.validate()
        assert scene.duration == DURATIONS[index]
        assert scene.main_start == (12 if index == 3 else 6)
        assert np.allclose(rotation(ANGLE).T@rotation(ANGLE), IDENTITY)
        assert not np.allclose(scene.A.T@scene.A, IDENTITY)
        collisions = []
        min_cell_clearance = float('inf')
        for t in np.linspace(0, scene.duration, 600):
            st = scene.state(float(t))
            p = _points(st['matrix'], CELL)
            clearance = min(p[:, 0].min()-PLOT[0], PLOT[2]-p[:, 0].max(),
                            p[:, 1].min()-PLOT[1], PLOT[3]-p[:, 1].max())
            min_cell_clearance = min(min_cell_clearance, float(clearance))
        assert min_cell_clearance >= 20, min_cell_clearance
        for t in MOMENTS[index]:
            im, boxes = render(index, t, _boxes=True)
            assert im.size == (1080, 1920)
            for a, label in boxes:
                assert a[0] >= 70 and a[2] <= 950, (index, t, label, a)
                assert a[1] >= 470 and a[3] <= 1600, (index, t, label, a)
            for n, (a, al) in enumerate(boxes):
                for b, bl in boxes[n+1:]:
                    if (min(a[2], b[2])-max(a[0], b[0]) > 1 and
                            min(a[3], b[3])-max(a[1], b[1]) > 1):
                        collisions.append({'time': t, 'a': al, 'b': bl})
        assert not collisions, collisions
        if scene.uniform:
            first_grid = render(index, 14.5).crop(PLOT).tobytes()
            for t in (15., 15.5, 16., 16.5, 17.):
                assert render(index, t).crop(PLOT).tobytes() == first_grid
        report[str(index)] = dict(source=source,
            portrait_cell_min_edge_clearance_pixels=min_cell_clearance,
            portrait_label_collisions=collisions, sequence_repetitions=1,
            rotation_unitary=True, stretch_unitary=False,
            duration_seconds=DURATIONS[index], size=[1080, 1920])
    report['portrait_renderer_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return report
