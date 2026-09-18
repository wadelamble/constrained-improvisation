"""Draw the selected Symmetry and Material Information profile mark.

Run from any directory. Outputs live in content/branding/symmetryphysics.
The plain sine wave runs across the full horizontal diameter of the circle.
"""
from pathlib import Path
import math
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
from PIL import Image, ImageDraw

OUT = ROOT / 'content' / 'branding' / 'symmetryphysics'
SIZE = 1024
BG = '#080b14'
WAVE = '#46beff'
LEFT, RIGHT = 0, SIZE
AMPLITUDE = 126
STROKE = 26
CYCLES = 2


def point(t):
    angle = 2 * math.pi * CYCLES * t
    return LEFT + (RIGHT - LEFT) * t, SIZE / 2 - AMPLITUDE * math.sin(angle)


def derivative(t):
    angle = 2 * math.pi * CYCLES * t
    return RIGHT - LEFT, -AMPLITUDE * 2 * math.pi * CYCLES * math.cos(angle)


def svg_path():
    # Hermite cubic segments preserve the analytic slope at every join.
    n = 128
    x, y = point(0)
    parts = [f'M {x:.6f} {y:.6f}']
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        p0, p1 = point(t0), point(t1)
        d0, d1 = derivative(t0), derivative(t1)
        c0 = tuple(p0[j] + d0[j] / (3 * n) for j in (0, 1))
        c1 = tuple(p1[j] - d1[j] / (3 * n) for j in (0, 1))
        parts.append('C ' + ' '.join(f'{v:.6f}' for v in (*c0, *c1, *p1)))
    return ' '.join(parts)


def render(color=WAVE):
    scale = 4
    image = Image.new('RGB', (SIZE * scale, SIZE * scale), BG)
    draw = ImageDraw.Draw(image)
    points = [tuple(v * scale for v in point(i / 3200)) for i in range(3201)]
    radius = STROKE * scale / 2
    sides = [[], []]
    for i, (x, y) in enumerate(points):
        dx, dy = derivative(i / 3200)
        length = math.hypot(dx, dy)
        nx, ny = -dy / length, dx / length
        sides[0].append((x + radius * nx, y + radius * ny))
        sides[1].append((x - radius * nx, y - radius * ny))
    draw.polygon(sides[0] + sides[1][::-1], fill=color)
    for x, y in (points[0], points[-1]):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def circular(image):
    s = image.width
    mask = Image.new('L', (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    mask = mask.resize((s, s), Image.Resampling.LANCZOS)
    result = image.convert('RGBA')
    result.putalpha(mask)
    return result


def save_logo(name, color, stem):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" role="img" aria-labelledby="title desc">
  <title id="title">Symmetry and Material Information</title>
  <desc id="desc">A {name.lower()} sine wave with two cycles across the full horizontal diameter of a dark navy circle.</desc>
  <defs><clipPath id="disc"><circle cx="512" cy="512" r="512"/></clipPath></defs>
  <circle cx="512" cy="512" r="512" fill="{BG}"/>
  <path d="{svg_path()}" fill="none" stroke="{color}" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#disc)"/>
</svg>
'''
    (OUT / f'{stem}.svg').write_text(svg, encoding='utf-8')
    upload = render(color)
    upload.save(OUT / f'{stem}.png')
    circle = circular(upload)
    circle.save(OUT / f'{stem}-circle.png')
    circle.resize((384, 384), Image.Resampling.LANCZOS).save(OUT / f'{stem}-preview.png')
    return circle


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    circle = save_logo('Blue', WAVE, 'profile-logo')
    save_logo('Blue', WAVE, 'profile-logo-blue-edge')

    # Actual small-avatar sizes, plus a larger view, for visual review.
    sheet = Image.new('RGB', (740, 380), '#f4f1eb')
    for x, y, size in ((22, 30, 320), (390, 32, 110), (390, 174, 64), (510, 174, 40), (610, 174, 32)):
        icon = circle.resize((size, size), Image.Resampling.LANCZOS)
        sheet.paste(icon, (x, y), icon)
    sheet.save(OUT / 'profile-logo-size-check.png')

    print(OUT)


if __name__ == '__main__':
    main()
