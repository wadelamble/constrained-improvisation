"""Portrait comparisons of the existing classical and quantum histories.

The numerical models and physical clock are imported without alteration.
Two views merge while that clock is stopped; overlay never couples the two
classical systems and never adds the two quantum states.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
sys.path.insert(0, str(ROOT / 'scripts'))
import numpy as np
from PIL import Image, ImageDraw

try:
    from . import core as c
except ImportError:
    import core as c
from generate_symmetry_reversible_histories import (
    BEATS, PLAYBACK_SPEED, STORY_DURATION, timeline,
)
from symmetry_reversible_balls import (
    build_histories as build_balls, validation_report as validate_balls,
)
from symmetry_unitary_waves import (
    build_histories as build_waves, validate as validate_waves,
)

DURATION = 24
TITLES = {
    1: 'Reversible evolution preserves information',
    2: 'Unitary evolution preserves overlap',
}
MOMENTS = (0., 2.333333, 4., 6., 8., 13.333333, 16.666667, 18.933333, 23.666667)
GRID = np.linspace(0., 1., 97)
GX, GY = np.meshgrid(GRID, GRID)
VERTICAL_SCALE = .040
COLORS = (c.BLUE, c.GOLD)


def _rgba(color, alpha):
    return tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) + (round(alpha),)


def _line(draw, points, fill, width=2):
    draw.line([tuple(np.round(p).astype(int)) for p in points],
              fill=fill, width=round(width), joint='curve')


def _merged(t):
    return float(c.ease((t*PLAYBACK_SPEED-24.)/2.))


def _ball_geometry(t, which):
    m = _merged(t)
    width = 600.+220.*m
    y = (580., 1045.)[which]*(1.-m)+790.*m
    return 510.-width/2., y, width, m


def _ball_projection(points, x, y, width, box):
    points = np.asarray(points)
    return np.stack((x+width*points[..., 0]/box[0],
                     y+width*(box[1]-points[..., 1])/box[0]), axis=-1)


def _draw_table(im, x, y, width, box):
    draw = ImageDraw.Draw(im)
    height = width*box[1]/box[0]
    draw.rounded_rectangle((x-8, y-8, x+width+8, y+height+8),
                           radius=16, fill=c.PANEL, outline=c.GRID, width=2)
    draw.rectangle((x, y, x+width, y+height), outline=c.GRID, width=2)


def _draw_balls(im, history, physical_t, trail_direction, geometry, color):
    x, y, width, merged = geometry
    draw = ImageDraw.Draw(im, 'RGBA')
    positions, _ = history.sample(physical_t)
    radius = history.radius*width/history.box[0]
    tails = np.linspace(.32, 0., 13)
    sample_times = np.clip(physical_t-trail_direction*tails, 0., history.duration)
    traces = _ball_projection(history.sample(sample_times)[0], x, y, width, history.box)
    for ball in range(len(positions)):
        for j in range(len(tails)-1):
            _line(draw, traces[j:j+2, ball], _rgba(color, 24+115*j/(len(tails)-2)), 3)
    centers = _ball_projection(positions, x, y, width, history.box)
    for px, py in centers:
        draw.ellipse((px-radius, py-radius, px+radius, py+radius),
                     fill=_rgba(color, 255-95*merged), outline=_rgba(color, 255), width=2)
        rr = radius*.16
        cx, cy = px-radius*.27, py-radius*.27
        draw.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), fill=_rgba(c.INK, 100-25*merged))


def _wave_geometry(t, which):
    m = _merged(t)
    return 510., (790., 1240.)[which]*(1.-m)+1075.*m, 800.+80.*m, m


def _wave_projection(x, y, z, cx, cy, width):
    x, y = np.asarray(x)-.5, np.asarray(y)-.5
    return np.stack((cx+width*(.68*x-.28*y),
                     cy+width*(.18*x+.28*y-VERTICAL_SCALE*np.asarray(z))), axis=-1)


def _draw_floor(im, cx, cy, width):
    draw = ImageDraw.Draw(im, 'RGBA')
    corners = _wave_projection(np.array([0., 1., 1., 0.]),
                               np.array([0., 0., 1., 1.]), 0., cx, cy, width)
    draw.polygon([tuple(p) for p in corners], fill=_rgba(c.PANEL, 220))
    for f in np.linspace(0., 1., 5):
        for x, y in ((np.array([0., 1.]), np.array([f, f])),
                     (np.array([f, f]), np.array([0., 1.]))):
            _line(draw, _wave_projection(x, y, 0., cx, cy, width), _rgba(c.GRID, 135), 1)
    _line(draw, np.vstack((corners, corners[:1])), _rgba(c.GRID, 255), 2)


def _draw_surface_fill(im, height, geometry, color):
    cx, cy, width, merged = geometry
    draw = ImageDraw.Draw(im, 'RGBA')
    points = _wave_projection(GX, GY, height, cx, cy, width)[::3, ::3]
    z = height[::3, ::3]
    count = len(points)-1
    alpha = 38*(1.-merged)+8*merged
    for row, col in sorted(((r, q) for r in range(count) for q in range(count)), key=sum):
        polygon = points[[row, row, row+1, row+1], [col, col+1, col+1, col]]
        strength = min(1., abs(float(np.mean(z[row:row+2, col:col+2])))/3.)
        draw.polygon([tuple(p) for p in polygon], fill=_rgba(color, alpha*(.3+.7*strength)))


def _draw_surface_mesh(im, height, geometry, color):
    cx, cy, width, merged = geometry
    draw = ImageDraw.Draw(im, 'RGBA')
    points = _wave_projection(GX, GY, height, cx, cy, width)
    for row in range(0, len(GRID), 6):
        _line(draw, points[row], _rgba(color, 240), 2)
    for col in range(0, len(GRID), 8):
        _line(draw, points[:, col], _rgba(color, 125), 1)


def _labels(im, t, kind):
    draw = ImageDraw.Draw(im, 'RGBA')
    m = _merged(t)
    # Moving the lower label with its pane would carry it through the upper
    # state's picture. Fade to a common comparison row before merging panes.
    comparison = t >= 16.
    alpha = 255.*(float(c.ease((t-16.)/.25)) if comparison
                  else 1.-float(c.ease((t-15.5)/.5)))
    for i, color in enumerate(COLORS):
        x = (370., 650.)[i] if comparison else 510.
        geometry_index = 0 if comparison else i
        if kind == 'balls':
            y = _ball_geometry(t, geometry_index)[1]-35.
        else:
            y = _wave_geometry(t, geometry_index)[1]-240.
        c.text(draw, (x, y), ('State A', 'State B')[i], size=31,
               fill=_rgba(color, alpha), anchor='mm', bold=True)
    if comparison:
        c.text(draw, (510, y), '≠', size=38, fill=_rgba(c.INK, alpha), anchor='mm')


def _clock(im, physical_t, direction):
    draw = ImageDraw.Draw(im)
    label = {1: 'FORWARD', -1: 'BACKWARD', 0: 'PAUSED'}[direction]
    c.text(draw, (510, 1536), f't = {physical_t:.1f}     {label}', size=30,
           fill=c.INK, anchor='mm')
    a, b, y = 280., 740., 1584.
    draw.line((a, y, b, y), fill=c.GRID, width=3)
    for value in range(9):
        x = a+(b-a)*value/8.
        draw.line((x, y-5, x, y+5), fill=c.MUTED, width=1)
    marker = a+(b-a)*physical_t/8.
    draw.ellipse((marker-6, y-6, marker+6, y+6), fill=c.INK)
    c.text(draw, (a-27, y), '0', size=23, fill=c.MUTED, anchor='mm')
    c.text(draw, (b+27, y), '8', size=23, fill=c.MUTED, anchor='mm')
    if direction:
        ax, ay = 205., 1536.
        draw.line((ax-19*direction, ay, ax+19*direction, ay), fill=c.GOLD, width=3)
        draw.polygon(((ax+19*direction, ay), (ax+8*direction, ay-7),
                      (ax+8*direction, ay+7)), fill=c.GOLD)


def render(index, t):
    """Render a full RGB portrait frame, with source time accelerated 1.5x."""
    if index not in TITLES:
        raise ValueError('histories renderer supplies reel 1 or reel 2')
    t = float(np.clip(t, 0., DURATION))
    physical_t, direction, trail_direction = timeline(t*PLAYBACK_SPEED)
    merged = _merged(t)
    stage = ('Two initial states · one reversible law' if index == 1
             else 'Two initial states · one unitary evolution')
    if t >= 16.:
        stage = 'Overlay of independent histories' if index == 1 else 'Overlay compares the two states'
    im, draw = c.frame(TITLES[index], index, t, DURATION, stage=stage)
    if index == 1:
        c.math(im, r'\Phi_{-t}\Phi_t=I', (510, 500), size=43, max_width=840)
        histories = build_balls(duration=8.)
        geometries = [_ball_geometry(t, i) for i in range(2)]
        for i, (x, y, width, m) in enumerate(geometries):
            if i == 1 and m == 1.:
                continue
            _draw_table(im, x, y, width, histories[i].box)
        for i, geometry in enumerate(geometries):
            _draw_balls(im, histories[i], physical_t, trail_direction, geometry, COLORS[i])
        _labels(im, t, 'balls')
        c.text(ImageDraw.Draw(im), (510, 1480), 'Distinct states remain distinct', size=28,
               fill=c.MUTED, anchor='mm')
    else:
        c.math(im, r'\langle U\psi_A\mid U\psi_B\rangle=\langle\psi_A\mid\psi_B\rangle',
               (510, 500), size=40, max_width=850)
        waves = build_waves()
        states = waves.evaluate(physical_t, GRID, GRID)
        geometries = [_wave_geometry(t, i) for i in range(2)]
        for i, (cx, cy, width, m) in enumerate(geometries):
            if i == 1 and m == 1.:
                continue
            _draw_floor(im, cx, cy, width)
        # Both independent fills precede both meshes, so each outline remains visible.
        for i, geometry in enumerate(geometries):
            _draw_surface_fill(im, states[i].real, geometry, COLORS[i])
        for i, geometry in enumerate(geometries):
            _draw_surface_mesh(im, states[i].real, geometry, COLORS[i])
        _labels(im, t, 'waves')
        overlap = waves.overlap(physical_t)
        # Round negligible residuals instead of printing a distracting negative zero.
        real, imag = float(overlap.real), 0. if abs(overlap.imag) < 5e-10 else float(overlap.imag)
        c.text(ImageDraw.Draw(im), (510, 1458), f'Complex overlap  {real:.2f} + {imag:.2f}i',
               size=30, fill=c.INK, anchor='mm', bold=True)
        c.text(ImageDraw.Draw(im), (510, 1497), 'Surface height: Re ψ · fixed scale',
               size=25, fill=c.MUTED, anchor='mm')
    _clock(im, physical_t, direction)
    return im.convert('RGB')


def validate():
    """Run the original physical checks plus the portrait clock/bounds checks."""
    classical = validate_balls(duration=8.)
    quantum = validate_waves()
    assert STORY_DURATION/PLAYBACK_SPEED == DURATION
    assert BEATS[0][0] == 0. and BEATS[-1][1] == STORY_DURATION
    for first, second in zip(BEATS, BEATS[1:]):
        assert first[1] == second[0] and first[3] == second[2]
    for t in np.linspace(16., 26./1.5, 129):
        assert timeline(t*PLAYBACK_SPEED)[0] == 0.
    lower, upper = np.array([np.inf, np.inf]), np.array([-np.inf, -np.inf])
    waves = build_waves()
    for t in np.linspace(0., DURATION, 257):
        physical_t, _, _ = timeline(t*PLAYBACK_SPEED)
        assert 0. <= physical_t <= 8.
        states = waves.evaluate(physical_t, GRID, GRID)
        for i in range(2):
            x, y, width, _ = _ball_geometry(t, i)
            assert x-8 >= 70 and x+width+8 <= 950
            assert y-8 >= 535 and y+width*.66+8 <= 1450
            cx, cy, width, _ = _wave_geometry(t, i)
            points = _wave_projection(GX, GY, states[i].real, cx, cy, width)
            lower = np.minimum(lower, points.min(axis=(0, 1)))
            upper = np.maximum(upper, points.max(axis=(0, 1)))
    assert lower[0] >= 70 and upper[0] <= 950
    assert lower[1] >= 580 and upper[1] <= 1445
    return {
        'passed': True, 'duration_seconds': DURATION, 'size': [1080, 1920],
        'playback_speed': PLAYBACK_SPEED, 'separate_cycles': 2, 'overlay_cycles': 1,
        'merge_seconds': [16., 26./1.5], 'merge_clock_paused': True,
        'classical': classical, 'quantum': quantum,
        'overlay_is_comparison': True, 'inter_history_collisions': False,
        'quantum_states_added': False, 'surface_component': 'real',
        'surface_height_scale': VERTICAL_SCALE, 'surface_autoscaling': False,
        'sampled_surface_bounds': [lower.tolist(), upper.tolist()],
        'representative_moments': list(MOMENTS),
    }
