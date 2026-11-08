"""Landscape adaptation of CCR reel 13: translation and uncertainty in physical units.

The first act holds the packet width fixed and performs one spatial translation
with K and P/hbar. The second compares minimum-uncertainty Gaussian preparations
on fixed axes. The changing widths are a family of states, not a free-evolution
claim. Run --render --check to encode and inspect the delivered video.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import generate_symmetry_casimir_desktop as art

np, Image, ImageDraw = art.np, art.Image, art.ImageDraw
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools/momentum-uncertainty-desktop-review'
NAME = 'symmetry-momentum-uncertainty'
W, H, FPS, DURATION = 1600, 900, 24, 38
HBAR = 1.054571817e-34
BG, INK, MUTED = art.BG, art.INK, art.MUTED
BLUE, RED, GOLD, GRID = art.BLUE, art.RED, art.GOLD, art.GRID
MOMENTS = [0, 3, 7, 11, 15, 18, 20, 22, 25, 28, 31, 34, 37.5]


def ramp(t, start, end):
    return art.ease((t-start)/(end-start))


def density(q, sigma):
    return np.exp(-np.asarray(q)**2/(2*sigma**2))/(math.sqrt(2*math.pi)*sigma)


def widths(t):
    sx_nm = 1.22 - .80*ramp(t, 23, 33)
    sp_units = HBAR/(2*sx_nm*1e-9)/1e-25
    return sx_nm, sp_units


def packet(q, shift, sigma=.72):
    return (2*np.pi*sigma**2)**(-.25)*np.exp(-(q-shift)**2/(4*sigma**2)+4j*(q-shift))


def header(s, t, stage):
    s.text(56, 36, 'Wave Number Becomes Momentum', 36, INK, bold=True)
    s.text(56, 93, stage, 25, MUTED)
    s.line([(56, 140), (1544, 140)], art.FAINT, 2)
    s.line([(56, 817), (1544, 817)], art.FAINT, 2)
    s.line([(56, 817), (56+1488*t/DURATION, 817)], GOLD, 3)


def wave(s, cy, shift):
    q = np.linspace(-4.5, 4.5, 900)
    z = packet(q, shift)
    px = 180+(q+4.5)/9*850
    gain = 127
    s.line([(180, cy), (1030, cy)], GRID, 2)
    s.line(np.c_[px, cy-gain*abs(z)], GOLD, 2)
    s.line(np.c_[px, cy+gain*abs(z)], GOLD, 2)
    tilted = z*np.exp(-.38j)
    s.line(np.c_[px+.28*gain*tilted.imag, cy-gain*tilted.real], BLUE, 4)
    center = 180+(shift+4.5)/9*850
    s.dot((center, cy), 4, GOLD)


def translation_act(s, t):
    a = -1.10+2.20*ramp(t, 3, 15)
    wave(s, 310, a)
    wave(s, 560, a)
    s.math(96, 310, r'\hat K', 39, BLUE, center=True)
    s.math(96, 560, r'\hat P/\hbar', 36, GOLD, center=True)
    s.line([(1080, 190), (1080, 655)], art.FAINT, 2)
    s.text(1130, 226, 'The same packet', 26, INK)
    s.text(1130, 267, 'The same displacement', 26, INK)
    s.math(1130, 385, r'\hat P=\hbar\hat K', 43)
    s.math(1130, 497, r'p=\hbar k', 39, GOLD)
    s.text(1130, 570, 'Only the units change.', 24, MUTED)
    s.math(800, 740, r'T_a=e^{-ia\hat K}=e^{-ia\hat P/\hbar}', 43, center=True)
    s.text(56, 846, 'One translation, written two ways', 23, MUTED)


def density_plot(s, left, right, sigma, color, title, variable, units, fill):
    base, gain = 550, 175
    q = np.linspace(-4, 4, 850)
    px = left+(q+4)/8*(right-left)
    py = base-gain*density(q, sigma)
    s.d.polygon([(left, base)]+list(map(tuple, np.c_[px, py]))+[(right, base)], fill=fill)
    s.line(np.c_[px, py], color, 4)
    s.line([(left, base), (right, base)], GRID, 2)
    for value in (-4, -2, 0, 2, 4):
        x = left+(value+4)/8*(right-left)
        s.line([(x, base-4), (x, base+6)], GRID, 2)
        s.text(x, base+12, str(value).replace('-', '−'), 20, MUTED, anchor='ma')
    center = (left+right)/2
    s.text(center, 270, title, 27, color, bold=True, anchor='ma')
    extent = sigma*(right-left)/8
    s.line([(center, 615), (center+extent, 615)], GOLD, 4)
    for x in (center, center+extent):
        s.line([(x, 606), (x, 624)], GOLD, 3)
    s.math(center+extent/2, 654, rf'\sigma_{variable}={sigma:.2f}', 31, GOLD, center=True)
    s.math(center, 700, variable+r'-\langle '+variable+r'\rangle', 28, color, center=True)
    s.text(center, 727, units, 23, MUTED, anchor='ma')


def uncertainty_act(s, t):
    sx, sp = widths(t)
    s.math(800, 199, r'[\hat X,\hat K]=iI\quad\longrightarrow\quad[\hat X,\hat P]=i\hbar I',
           37, center=True)
    density_plot(s, 90, 725, sx, BLUE, 'Position', 'x', 'nanometers', '#edf1f5')
    density_plot(s, 875, 1510, sp, RED, 'Momentum', 'p', '10⁻²⁵ kg m/s', '#f6ebe7')
    s.line([(800, 270), (800, 750)], art.FAINT, 2)
    s.math(800, 782, r'\sigma_x\sigma_p=\frac{\hbar}{2}', 32, GOLD, center=True)
    s.text(56, 846, 'Normalized probability densities. This Gaussian family reaches equality.', 23, MUTED)


def render(t):
    s = art.Canvas()
    if t < 20:
        header(s, t, 'Wave number and momentum generate the same translation.')
        translation_act(s, t)
    else:
        header(s, t, 'Compare wave packets with different position and momentum widths.')
        uncertainty_act(s, t)
    # Catch text collisions in every rendered frame, not only the preview times.
    for i, (a, name_a) in enumerate(s.boxes):
        for b, name_b in s.boxes[i+1:]:
            assert min(a[2], b[2]) <= max(a[0], b[0]) or min(a[3], b[3]) <= max(a[1], b[1]), (t, name_a, name_b)
    return s.im


def validate():
    q = np.linspace(-20, 20, 40001)
    checks = []
    for t in (20, 26, 29, 33, 37):
        sx, sp = widths(t)
        dx, dp = density(q, sx), density(q, sp)
        nx, np_ = np.trapezoid(dx, q), np.trapezoid(dp, q)
        varx = np.trapezoid((q*1e-9)**2*dx, q)
        varp = np.trapezoid((q*1e-25)**2*dp, q)
        error = abs(math.sqrt(varx*varp)/(HBAR/2)-1)
        assert abs(nx-1)<1e-12 and abs(np_-1)<1e-12 and error<1e-12
        checks.append(dict(time=t, sigma_x_nm=sx, sigma_p_1e25=sp, norm_x=float(nx), norm_p=float(np_), product_relative_error=error))
    k = np.linspace(-8e9, 8e9, 2001)
    p = HBAR*k
    error = max(float(np.max(abs(np.exp(-1j*a*k)-np.exp(-1j*a*p/HBAR)))) for a in (-1.1e-9, 0, 1.1e-9))
    assert error<1e-12
    return dict(size=[W,H], fps=FPS, duration_seconds=DURATION, hbar_Js=HBAR,
                translation_multiplier_max_error=error, independent_density_quadratures=checks,
                preparations='Gaussian family, not a simulation of free time evolution',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                renderer_sha256=hashlib.sha256(Path(art.__file__).read_bytes()).hexdigest())


def previews():
    REVIEW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1200, math.ceil(len(MOMENTS)/3)*250), BG)
    draw = ImageDraw.Draw(sheet)
    for i, t in enumerate(MOMENTS):
        im = render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        x,y = i%3*400, i//3*250
        sheet.paste(im.resize((400,225), Image.Resampling.LANCZOS), (x,y))
        draw.text((x+12,y+228), f'{t}s', fill=MUTED, font=art.font(17))
    sheet.save(REVIEW/'contact.png')
    render(29).save(OUT/f'{NAME}-poster.png')


def encode():
    destination = OUT/f'{NAME}.mp4'
    temporary = REVIEW/f'{NAME}.rendering.mp4'
    command = [art.imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-f', 'rawvideo',
               '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-an',
               '-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',
               '-movflags','+faststart','-threads','2',str(temporary)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for i in range(DURATION*FPS):
                process.stdin.write(render(i/FPS).tobytes())
                if i%(FPS*8)==0: print(f'{NAME}: {i/FPS:.0f}/{DURATION}s', flush=True)
            process.stdin.close()
            if process.wait(): raise RuntimeError('FFmpeg encoding failed')
        except BaseException:
            process.kill()
            raise
    temporary.replace(destination)


def check_video():
    video = OUT/f'{NAME}.mp4'
    ffmpeg = art.imageio_ffmpeg.get_ffmpeg_exe()
    reader = art.imageio_ffmpeg.read_frames(str(video))
    try: meta = next(reader)
    finally: reader.close()
    count, seconds = art.imageio_ffmpeg.count_frames_and_secs(str(video))
    assert meta['size']==(W,H) and meta['fps']==FPS and count==DURATION*FPS
    subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
    indices = [round(t*FPS) for t in (0,7,15,20,25,29,32,35,37.5)]
    select = '+'.join(f'eq(n\\,{i})' for i in indices)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                    f'select={select},scale=480:270,tile=3x3','-frames:v','1',
                    str(OUT/f'{NAME}-contact-sheet.png')],check=True)
    report = dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(), frame_count=count,
                  duration_seconds=seconds,size=meta['size'],fps=meta['fps'],decode='passed',
                  contact_sheet_frame_indices=indices)
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    report = validate()
    previews()
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)
    if args.render: encode()
    if args.check: print(json.dumps(check_video()),flush=True)


if __name__ == '__main__': main()
