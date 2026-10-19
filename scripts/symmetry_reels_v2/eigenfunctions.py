"""A restrained, more active version of the translation-eigenfunction reel.

The exponential stays fixed. One forward pass constructs its derivative by vertical
scaling and compares a horizontal translation with an equal vertical scaling.
Intermediate scaling curves are constructions, not derivatives of changing f.
"""
from __future__ import annotations

from core import *


LAMBDA = .5
SHIFT = 1.8

NARRATION = [
    'Blue is the exponential. Gold is its derivative.',
    'Halve every height of a copy. Watch it meet the gold derivative.',
    'The scaled copy matches the derivative at every x.',
    'Now slide a copy to the right. Its shape stays the same.',
    'Keep the translated curve in place.',
    'Scale a fresh copy of the original vertically.',
    'It matches the translated curve at every x. A shift is also a rescaling.',
]
SCREEN_TEXT = NARRATION + [
    r'\frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}',
    'λ = 0.50', 'f', r"f'=\lambda f",
    r'f(x-a)=e^{-\lambda a}f(x)', 'x',
]


def motion(t, duration):
    """Three monotone operations separated by holds, ending on the match."""
    q = float(np.clip(t/duration, 0, 1))*26
    scaling = float(ease(window(q, 2, 7.5)))
    translation = float(ease(window(q, 9.5, 15)))
    comparison = float(ease(window(q, 17.5, 22.5)))
    return q, scaling, translation, comparison


def _map(box, x, y):
    x, y = np.broadcast_arrays(np.asarray(x), np.asarray(y))
    left, top, right, bottom = box
    return np.stack((left+(x+2)/5*(right-left),
                     bottom-y/5.2*(bottom-top)), axis=-1)


def _axes(s, box):
    for y in (1, 2, 3, 4):
        s.line(_map(box, [-2, 3], [y, y]), GRID, 1)
    s.arrow(_map(box, -2, 0), _map(box, 3, 0), MUTED, 2, 10)
    s.text(box[2]+13, box[3]+3, 'x', 30, MUTED)


def render(t, entry):
    q, scaling, translation, comparison = motion(t, entry['duration'])
    stage_index = int(np.searchsorted([2, 7.5, 9.5, 15, 17.5, 22.5], q, side='right'))
    s = Scene(24, entry['title'], '', t, entry['duration'])
    # The existing subtitle strip has room for two short narration lines.
    s.wrap(NARRATION[stage_index], 70, 420, 880, size=32, color=INK, leading=39)
    x = np.linspace(-2, 3, 501)
    f = np.exp(LAMBDA*x)
    a = SHIFT*translation
    factor = math.exp(-LAMBDA*a)
    top = (140, 720, 900, 1055)
    bottom = (140, 1215, 900, 1550)

    s.math(r'\frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}',
           y=530, size=50)
    s.text(510, 610, 'λ = 0.50', 35, GOLD, anchor='ma')
    s.math('f', x=275, y=674, size=44, color=BLUE)
    s.math(r"f'=\lambda f", x=665, y=674, size=44, color=GOLD)
    _axes(s, top)
    # Gold always denotes the actual derivative, including during the tween.
    # White denotes a working copy, as it does in the lower scaling comparison.
    s.line(_map(top, x, f), BLUE, 6)
    s.line(_map(top, x, LAMBDA*f), GOLD, 5)
    multiplier = 1+(LAMBDA-1)*scaling
    if q >= 2:
        s.line(_map(top, x, multiplier*f), INK, 2)
        for anchor in (-.4, 1.1, 2.5):
            value = math.exp(LAMBDA*anchor)
            start, end = _map(top, anchor, value), _map(top, anchor, multiplier*value)
            s.arrow(start, end, INK, 2, 9)
            s.dot(start, 5, BLUE)
            s.dot(end, 5, INK)

    s.math(r'f(x-a)=e^{-\lambda a}f(x)', y=1135, size=49, color=GREEN)
    _axes(s, bottom)
    s.line(_map(bottom, x, f), BLUE, 6)
    shifted = np.exp(LAMBDA*(x-a))
    if q >= 9.5:
        s.line(_map(bottom, x, shifted), GREEN, 5)
    # Two marked features visibly move horizontally with the entire curve.
    for anchor in (-.7, .65):
        value = math.exp(LAMBDA*anchor)
        start = _map(bottom, anchor, value)
        end = _map(bottom, anchor+a, value)
        if q >= 9.5:
            s.arrow(start, end, GREEN, 2, 9)
        s.dot(start, 5, BLUE)
        if q >= 9.5:
            s.dot(end, 6, GREEN)

    # A white working copy scales vertically to the already translated curve.
    # Once it coincides, its thin white trace leaves the green result visible.
    if q >= 17.5:
        scale = 1+(factor-1)*comparison
        s.line(_map(bottom, x, scale*f), INK, 2)
        for anchor in (-.4, 1.1, 2.5):
            value = math.exp(LAMBDA*anchor)
            s.arrow(_map(bottom, anchor, value),
                    _map(bottom, anchor, scale*value), INK, 2, 8)
    return s.im
