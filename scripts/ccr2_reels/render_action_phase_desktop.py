"""Landscape companion to the approved action/phase reel.

Run without arguments for stills and validation, or add --render for MP4/WebM.
The shared reel state supplies every event, phase and action value unchanged.
No manuscript, reel master, caption or publication record is modified.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time

from core import ROOT, Scene, Image, ImageDraw, font, np, phasor
from revise_action_phase import (state, TITLE, DURATION, SWEEP_END,
                                 PASS_DURATION, START_HOLD, END_HOLD,
                                 TAU_MAX, HBAR, MASSES, KAPPAS, ACTION_MAX, FPS)
import imageio_ffmpeg


OUT = ROOT / 'content/drafts/animations'
STEM = 'symmetry-action-phase-desktop'
WIDTH, HEIGHT = 1920, 1080
TIMES = [2.2, 8.0, 13.1, 18.4, 20.65, 23.7]
# Match the manuscript's unitarity and complex-phase desktop palette.
# Keep these local so the approved portrait reel remains unchanged.
BG, PANEL = '#fdfaf4', '#faf7f0'
INK, MUTED, BORDER = '#252628', '#6f6c66', '#dad3c8'
GRID, BLUE, GOLD, GREEN = '#cfcbc3', '#2b5d91', '#c08019', '#2b8059'


class DesktopScene(Scene):
    def panel(self, box, label=None, color=MUTED):
        self.d.rounded_rectangle(tuple(box), radius=22, fill=PANEL, outline=BORDER, width=2)
        if label:
            self.text(box[0]+24, box[1]+22, label, 30, color)

    def math(self, tex, x=510, y=1510, size=44, color=INK, maxwidth=880):
        return super().math(tex, x=x, y=y, size=size, color=color, maxwidth=maxwidth)

    def __init__(self, seconds, st):
        self.im = Image.new('RGB', (WIDTH, HEIGHT), BG)
        self.d = ImageDraw.Draw(self.im)
        # Mathtext supplies the actual h-bar symbol rather than a font fallback.
        self.math(r'\hbar', x=81, y=59, size=49, maxwidth=48)
        self.text(116, 31, TITLE.split(' ', 1)[1], 43, INK, bold=True)
        stage = (f'Shell {st["shell_index"] + 1} of 3 · The same proper-time interval.'
                 if seconds >= SWEEP_END else 'Change the frame. Keep the event fixed.')
        self.text(64, 93, stage, 26, MUTED)
        self.text(64, 1024, 'Free motion · illustrative masses · c = 1', 23, MUTED)
        self.line([(64, 1008), (1856, 1008)], GRID, 2)
        self.line([(64, 1008), (64 + 1792 * seconds / DURATION, 1008)], GOLD, 3)


def shell(s, st):
    s.panel((64, 150, 944, 550), 'Wave-number shell')
    x0, y0, scale = 352, 485, 41
    px = lambda k: x0 + scale * k
    py = lambda omega: y0 - scale * omega
    s.arrow((98, y0), (624, y0), GRID, 3, 12)
    s.arrow((x0, y0 + 7), (x0, 225), GRID, 3, 12)
    q = np.linspace(-4.5, 4.5, 450)
    for kappa in KAPPAS:
        s.line(np.c_[px(q), py(np.sqrt(q*q + kappa*kappa))], GRID, 2)
    s.line(np.c_[px(q), py(np.sqrt(q*q + st['kappa']**2))], BLUE, 4)
    end = (px(st['k']), py(st['omega']))
    s.arrow((x0, y0), end, GOLD, 4, 15)
    s.dot(end, 8, GOLD)
    s.text(613, 502, 'k', 27, MUTED, anchor='ma')
    s.text(x0 + 16, 218, 'ω', 27, MUTED)
    s.math(r'\kappa^2=\omega^2-k^2', x=748, y=304, size=37, maxwidth=305)
    s.math(r'\kappa=' + f'{st["kappa"]:.2f}' + r'\ \mathrm{fs}^{-1}',
           x=748, y=391, size=32, color=BLUE, maxwidth=305)


def worldline(s, st, evolving):
    s.panel((976, 150, 1856, 550), 'Worldline')
    x0, y0, scale = 1264, 485, 16.0
    s.arrow((1010, y0), (1536, y0), GRID, 3, 12)
    s.arrow((x0, y0 + 7), (x0, 210), GRID, 3, 12)
    end = (x0 + scale * TAU_MAX * np.sinh(st['eta']),
           y0 - scale * TAU_MAX * np.cosh(st['eta']))
    s.line([(x0, y0), end], BLUE, 4)
    now = (x0 + scale * st['x'], y0 - scale * st['coordinate_time'])
    if evolving:
        s.line([(x0, y0), now], GOLD, 5)
    s.dot(now, 9, GOLD)
    s.text(1525, 502, 'x', 27, MUTED, anchor='ma')
    s.text(x0 + 16, 202, 't', 27, MUTED)
    if evolving:
        s.text(1676, 357, f'τ = {st["tau"]:.1f} fs', 35, GOLD, anchor='mm')
    else:
        s.text(1676, 346, 'Event at', 27, MUTED, anchor='mm')
        s.text(1676, 384, 'the origin', 27, MUTED, anchor='mm')


def phase(s, st, evolving):
    s.panel((64, 574, 944, 984), 'Phase')
    cx, cy, radius = 344, 804, 127
    s.d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=GRID, width=3)
    for index in range(12):
        angle = index * 2*np.pi / 12
        s.line([(cx+(radius-7)*np.cos(angle), cy-(radius-7)*np.sin(angle)),
                (cx+radius*np.cos(angle), cy-radius*np.sin(angle))], MUTED, 2)
    s.line([(cx-radius-10, cy), (cx+radius+10, cy)], GRID, 2)
    s.line([(cx, cy-radius-10), (cx, cy+radius+10)], GRID, 2)
    s.text(cx+radius+19, cy, 'Re', 23, MUTED, anchor='lm')
    s.text(cx+12, cy-radius-29, 'Im', 23, MUTED)
    phasor(s, (cx, cy), np.exp(1j*st['phi']), radius*.9, GOLD, width=6)
    s.math(r'e^{i\phi}=e^{-i\kappa\tau}' if evolving else r'e^{i\phi}',
           x=738, y=804, size=46, color=INK if evolving else MUTED, maxwidth=342)


def action_bar(s, st, evolving):
    s.panel((976, 574, 1856, 984), 'Action magnitude', color=GREEN)
    left, right, top, bottom = 1178, 1262, 676, 918
    s.d.rectangle((left, top, right, bottom), fill=BG, outline=GRID, width=2)
    level = bottom - (bottom-top) * abs(st['action']) / ACTION_MAX
    if bottom-level >= 3:
        s.d.rectangle((left+2, level, right-2, bottom-2), fill=GREEN)
        s.line([(left-7, level), (right+8, level)], INK, 3)
    for fraction, label in [(0, '0'), (1/3, '12'), (2/3, '24'), (1, '36')]:
        y = bottom-fraction*(bottom-top)
        s.line([(right+7, y), (right+18, y)], GRID, 2)
        s.text(right+37, y, label, 27, MUTED, anchor='lm')
    s.text((left+right)/2, 950, 'eV fs', 25, MUTED, anchor='mm')
    if evolving:
        s.math(r'|S|=m\tau', x=1615, y=694, size=43, color=GREEN, maxwidth=380)
        s.math(r'm=\hbar\kappa='+f'{st["mass"]:.0f}'+r'\ \mathrm{eV}',
               x=1615, y=769, size=37, maxwidth=380)
        s.text(1615, 857, f'|S| = {abs(st["action"]):05.2f} eV fs',
               35, GREEN, anchor='mm')
        s.math(r'S=-m\tau', x=1615, y=923, size=29, color=MUTED, maxwidth=380)


def frame(seconds):
    st = state(seconds)
    s = DesktopScene(seconds, st)
    evolving = seconds >= SWEEP_END
    shell(s, st)
    worldline(s, st, evolving)
    phase(s, st, evolving)
    action_bar(s, st, evolving)
    return s.im


def review():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1920, 800), BG)
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(TIMES):
        x, y = index % 3 * 640, index // 3 * 400
        image = frame(seconds).resize((640, 360), Image.Resampling.LANCZOS)
        sheet.paste(image, (x, y+28))
        draw.text((x+21, y+4), f'{seconds:g} s', font=font(19), fill=MUTED)
    sheet.save(OUT / f'{STEM}-contact-sheet.jpg', quality=95)
    frame(20.65).save(OUT / f'{STEM}-poster.png')
    frame(2.2).save(OUT / f'{STEM}-sweep.png')


def validate():
    values = [state(t) for t in np.linspace(0, DURATION, 1001)]
    errors = dict(
        shell=max(abs(v['omega']**2-v['k']**2-v['kappa']**2) for v in values),
        proper_time=max(abs(v['coordinate_time']**2-v['x']**2-v['tau']**2) for v in values),
        spacetime_phase=max(abs(v['k']*v['x']-v['omega']*v['coordinate_time']-v['phi']) for v in values),
        action_to_phase=max(abs(v['action']/HBAR-v['phi']) for v in values))
    assert max(errors.values()) < 1e-10, errors
    assert all(v['tau'] == v['phi'] == v['action'] == 0 for t, v in
               zip(np.linspace(0, DURATION, 1001), values) if t < SWEEP_END)
    endpoints = [state(SWEEP_END+(i+1)*PASS_DURATION-END_HOLD/2) for i in range(3)]
    for i, st in enumerate(endpoints):
        assert st['tau'] == TAU_MAX
        assert abs(abs(st['action'])/ACTION_MAX-(i+1)/3) < 1e-12
    for local in np.linspace(START_HOLD, PASS_DURATION-END_HOLD, 31):
        passes = [state(SWEEP_END+i*PASS_DURATION+local) for i in range(3)]
        assert np.ptp([v['tau'] for v in passes]) < 1e-12
        for i, v in enumerate(passes):
            assert abs(v['phi']-(i+1)*passes[0]['phi']) < 1e-11
            assert abs(v['action']-(i+1)*passes[0]['action']) < 1e-11
    report = dict(width=WIDTH, height=HEIGHT, fps=FPS, duration_seconds=DURATION,
                  frames=round(DURATION*FPS), shared_state='revise_action_phase.state',
                  sweep_seconds=SWEEP_END, pass_seconds=PASS_DURATION,
                  masses_eV=MASSES.tolist(), tau_interval_fs=[0, TAU_MAX],
                  endpoint_action_eV_fs=[abs(v['action']) for v in endpoints],
                  endpoint_turns=[-v['phi']/(2*np.pi) for v in endpoints],
                  invariant_errors=errors)
    (OUT / f'{STEM}-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, indent=2), flush=True)


def render():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    target = OUT / f'{STEM}.mp4'
    temporary = OUT / f'{STEM}.rendering.mp4'
    count = round(DURATION*FPS)
    command = [ffmpeg, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS), '-i', '-', '-an',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p',
               '-movflags', '+faststart', '-threads', '4', str(temporary)]
    started = time.time()
    with subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        try:
            for index in range(count):
                proc.stdin.write(frame(index/FPS).tobytes())
                if index % 252 == 0:
                    print(f'{index}/{count} frames, {time.time()-started:.1f}s', flush=True)
            proc.stdin.close()
            error = proc.stderr.read().decode('utf8', errors='replace')
            if proc.wait():
                raise RuntimeError(error)
        except BaseException:
            proc.kill()
            raise
    temporary.replace(target)
    subprocess.run([ffmpeg, '-v', 'error', '-i', str(target), '-f', 'null', '-'], check=True)
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-i', str(target), '-vf', 'scale=1280:720',
                    '-an', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '28',
                    '-deadline', 'realtime', '-cpu-used', '8', '-threads', '4',
                    str(OUT / f'{STEM}-preview.webm')], check=True)
    # Inspect encoded pixels, not only the still renderer.
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-ss', '20.65', '-i', str(target),
                    '-frames:v', '1', str(OUT / f'{STEM}-encoded-frame.png')], check=True)
    print(f'Done: {target.name}, {target.stat().st_size/1e6:.2f} MB', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    review()
    validate()
    if args.render:
        render()
    (OUT / f'{STEM}.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase and action</title>
<style>body{margin:0;background:#fdfaf4;color:#252628;font:16px system-ui;display:grid;place-items:center;min-height:100vh}main{width:min(96vw,1600px)}video{width:100%;max-height:88vh;display:block}p{color:#6f6c66}a{color:#2b5d91}</style>
<main><video controls playsinline loop preload="metadata" poster="''' + STEM + '''-poster.png">
<source src="''' + STEM + '''-preview.webm" type="video/webm"><source src="''' + STEM + '''.mp4" type="video/mp4"></video>
<p>Phase and action · 24 seconds · <a href="''' + STEM + '''.mp4">1920 × 1080 MP4</a></p></main></html>''', encoding='utf8')


if __name__ == '__main__':
    main()
