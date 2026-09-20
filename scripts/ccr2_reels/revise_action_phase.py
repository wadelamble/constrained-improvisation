"""Standalone Reel 12 review: choose a frame, then compare three shells.

Run with --render for MP4/WebM, or without it for review stills only.
Published masters, captions and publication records are never modified here.
"""
from __future__ import annotations

import argparse
import json

from core import *
import render as renderer
from retitle_live import live_title


OUT = ROOT / 'content/reels/ccr2-series/revisions/ccr2-12-action-phase'
TITLE = 'ℏ emerges as the conversion factor of phase to action'
DURATION = 24.0
SWEEP_END = 8.0
PASS_DURATION = (DURATION - SWEEP_END) / 3
START_HOLD, END_HOLD = .18, .42
TAU_MAX = 12.0  # femtoseconds, the same interval for each shell.
# With c=1, masses have energy units and positions have time units. Axes use
# light-fs / fs, generators fs^-1, and action eV fs. No unmarked phase slowdown.
HBAR = 1.054571817e-34 / 1.602176634e-19 / 1e-15  # eV fs
MASSES = np.array([1., 2., 3.])  # eV, illustrative values, not particle species.
KAPPAS = MASSES / HBAR
ACTION_MAX = MASSES[-1] * TAU_MAX


def state(seconds):
    """One clock supplies the event, unwrapped phase and signed action."""
    if seconds < SWEEP_END:
        # A frame sweep, not an accelerating worldline. Finish at eta=0.60.
        nodes = [(0., 0.), (2.2, -.78), (5.6, .78), (7.6, .60), (8., .60)]
        for (a, va), (b, vb) in zip(nodes, nodes[1:]):
            if seconds <= b:
                eta = lerp(va, vb, ease(window(seconds, a, b)))
                break
        tau = 0.
        shell_index = 0
    else:
        eta = .60
        shell_index = min(int((seconds-SWEEP_END) / PASS_DURATION), 2)
        local = seconds - SWEEP_END - shell_index * PASS_DURATION
        tau = TAU_MAX * window(local, START_HOLD, PASS_DURATION-END_HOLD)
    kappa, mass = KAPPAS[shell_index], MASSES[shell_index]
    k = kappa * np.sinh(eta)
    omega = kappa * np.cosh(eta)
    x = tau * np.sinh(eta)
    coordinate_time = tau * np.cosh(eta)
    phi = -kappa * tau
    action = -mass * tau
    return dict(eta=float(eta), tau=float(tau), k=float(k), omega=float(omega),
                shell_index=shell_index, kappa=float(kappa), mass=float(mass),
                x=float(x), coordinate_time=float(coordinate_time),
                phi=float(phi), action=float(action))


def shell(s, st):
    s.panel((70, 490, 495, 980), 'Wave-number shell')
    s.math(r'\kappa^2=\omega^2-k^2', x=282, y=585, size=36, maxwidth=367)
    px = lambda k: 282 + 36 * k
    py = lambda omega: 902 - 38 * omega
    s.arrow((103, 902), (467, 902), GRID, 3, 11)
    s.arrow((282, 909), (282, 642), GRID, 3, 11)
    q = np.linspace(-4.5, 4.5, 400)
    for ka in KAPPAS:
        s.line(np.c_[px(q), py(np.sqrt(q*q + ka*ka))], GRID, 2)
    s.line(np.c_[px(q), py(np.sqrt(q*q + st['kappa']**2))], BLUE, 4)
    end = (px(st['k']), py(st['omega']))
    s.arrow((282, 902), end, GOLD, 4, 13)
    s.dot(end, 8, GOLD)
    s.text(467, 912, 'k', 29, MUTED, anchor='ma')
    s.text(298, 632, 'ω', 29, MUTED)
    s.math(r'\kappa='+f'{st["kappa"]:.2f}'+r'\ \mathrm{fs}^{-1}',
           x=282, y=951, size=29, color=BLUE, maxwidth=365)


def worldline(s, st, evolving):
    s.panel((525, 490, 950, 980), 'Worldline')
    x0, y0 = 730, 902
    scale = 200 / TAU_MAX
    s.arrow((557, y0), (921, y0), GRID, 3, 11)
    s.arrow((x0, y0 + 7), (x0, 622), GRID, 3, 11)
    end = (x0 + scale * TAU_MAX * np.sinh(st['eta']),
           y0 - scale * TAU_MAX * np.cosh(st['eta']))
    s.line([(x0, y0), end], BLUE, 4)
    now = (x0 + scale * st['x'], y0 - scale * st['coordinate_time'])
    if evolving:
        s.line([(x0, y0), now], GOLD, 5)
    s.dot(now, 9, GOLD)
    s.text(923, 912, 'x', 29, MUTED, anchor='ma')
    s.text(x0 + 17, 612, 't', 29, MUTED)
    if evolving:
        s.text(737, 935, f'τ = {st["tau"]:.1f} fs', 29, GOLD, anchor='ma')
    else:
        s.text(737, 935, 'Event at the origin', 28, MUTED, anchor='ma')


def phase(s, st, evolving):
    s.panel((70, 1010, 495, 1525), 'Phase')
    if evolving:
        s.math(r'e^{i\phi}=e^{-i\kappa\tau}', x=282, y=1115, size=40, maxwidth=367)
    else:
        s.math(r'e^{i\phi}', x=282, y=1115, size=40, color=MUTED)
    cx, cy, radius = 282, 1310, 119
    s.d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=GRID, width=3)
    for index in range(12):
        a = index * 2 * np.pi / 12
        s.line([(cx+(radius-7)*np.cos(a), cy-(radius-7)*np.sin(a)),
                (cx+radius*np.cos(a), cy-radius*np.sin(a))], MUTED, 2)
    s.line([(cx-radius-10, cy), (cx+radius+10, cy)], GRID, 2)
    s.line([(cx, cy-radius-10), (cx, cy+radius+10)], GRID, 2)
    s.text(cx+radius+15, cy-12, 'Re', 23, MUTED)
    s.text(cx+10, cy-radius-29, 'Im', 23, MUTED)
    phasor(s, (cx, cy), np.exp(1j*st['phi']), radius*.90, GOLD, width=6)


def action_bar(s, st, evolving):
    s.panel((525, 1010, 950, 1525), 'Action magnitude', color=GREEN)
    if evolving:
        s.math(r'|S|=m\tau', x=737, y=1098, size=39, color=GREEN, maxwidth=365)
    if evolving:
        s.math(r'm=\hbar\kappa='+f'{st["mass"]:.0f}'+r'\ \mathrm{eV}',
               x=737, y=1150, size=33, color=INK, maxwidth=365)
    left, right, top, bottom = 635, 713, 1208, 1397
    s.d.rectangle((left, top, right, bottom), fill=BG, outline=GRID, width=2)
    level = bottom - (bottom-top) * abs(st['action']) / ACTION_MAX
    if bottom - level >= 3:
        s.d.rectangle((left+2, level, right-2, bottom-2), fill=GREEN)
        s.line([(left-6, level), (right+7, level)], INK, 3)
    for fraction, label in [(0, '0'), (1/3, '12'), (2/3, '24'), (1, '36')]:
        y = bottom - fraction*(bottom-top)
        s.line([(right+6, y), (right+16, y)], GRID, 2)
        s.text(751, y, label, 27, MUTED, anchor='lm')
    s.text(825, 1297, 'eV fs', 24, MUTED, anchor='mm')
    if evolving:
        s.text(737, 1442, f'|S| = {abs(st["action"]):05.2f} eV fs', 32, GREEN, anchor='mm')
        s.math(r'S=-m\tau', x=737, y=1490, size=27, color=MUTED, maxwidth=365)


def episode(seconds):
    st = state(seconds)
    evolving = seconds >= SWEEP_END
    stage = (f'Shell {st["shell_index"]+1} of 3 · The same proper-time interval.'
             if evolving else 'Change the frame. Keep the event fixed.')
    s = Scene(12, '', stage, seconds, DURATION)
    live_title(s.d, TITLE)
    shell(s, st)
    worldline(s, st, evolving)
    phase(s, st, evolving)
    action_bar(s, st, evolving)
    s.note('Free motion · illustrative masses · c = 1', y=1587, size=28)
    return s.im


def review():
    OUT.mkdir(parents=True, exist_ok=True)
    times = [2.2, 8, 13.05, 18.4, 20.65, 23.7]
    sheet = Image.new('RGB', (1620, 1000), BG)
    draw = ImageDraw.Draw(sheet)
    for i, seconds in enumerate(times):
        im = episode(seconds)
        im.save(OUT / f'frame-{i+1:02d}.jpg', quality=94)
        sheet.paste(im.resize((270, 480), Image.Resampling.LANCZOS), (i*270, 0))
        # A second row enlarges the mathematical artwork.
        art = im.crop((70, 490, 950, 1525)).resize((270, 318), Image.Resampling.LANCZOS)
        sheet.paste(art, (i*270, 530))
        draw.text((i*270+16, 487), f'{seconds:g} s', font=font(23), fill=INK)
    sheet.crop((0, 0, 1620, 855)).save(OUT / 'contact-sheet.jpg', quality=95)
    episode(22.8).save(OUT / 'ccr2-12-cover.jpg', quality=95)


def validate():
    """Verify that all four views describe the same free-worldline model."""
    values = [state(t) for t in np.linspace(0, DURATION, 1001)]
    errors = dict(
        shell=max(abs(v['omega']**2-v['k']**2-v['kappa']**2) for v in values),
        proper_time=max(abs(v['coordinate_time']**2-v['x']**2-v['tau']**2) for v in values),
        spacetime_phase=max(abs(v['k']*v['x']-v['omega']*v['coordinate_time']-v['phi']) for v in values),
        action_to_phase=max(abs(v['action']/HBAR-v['phi']) for v in values))
    assert max(errors.values()) < 1e-10, errors
    assert all(v['tau'] == v['phi'] == v['action'] == 0 for t, v in
               zip(np.linspace(0, DURATION, 1001), values) if t < SWEEP_END)
    assert all(v['eta'] == .60 for t, v in
               zip(np.linspace(0, DURATION, 1001), values) if t >= SWEEP_END)
    endpoints = [state(SWEEP_END+(i+1)*PASS_DURATION-END_HOLD/2) for i in range(3)]
    for i, st in enumerate(endpoints):
        assert st['shell_index'] == i
        assert st['tau'] == TAU_MAX
        assert abs(abs(st['action']) / ACTION_MAX - (i+1)/3) < 1e-12
    # At equal within-pass times, worldline events match and phase/action scale
    # with the shell value. This also catches accidental bar renormalization.
    for local in np.linspace(START_HOLD, PASS_DURATION-END_HOLD, 31):
        passes = [state(SWEEP_END+i*PASS_DURATION+local) for i in range(3)]
        assert np.ptp([v['tau'] for v in passes]) < 1e-12
        for i, v in enumerate(passes):
            assert abs(v['phi']-(i+1)*passes[0]['phi']) < 1e-11
            assert abs(v['action']-(i+1)*passes[0]['action']) < 1e-11
    report = dict(duration_seconds=DURATION, sweep_seconds=SWEEP_END,
                  passes=3, pass_seconds=PASS_DURATION, tau_interval_fs=[0, TAU_MAX],
                  masses_eV=MASSES.tolist(), kappa_per_fs=KAPPAS.tolist(),
                  endpoint_turns=[-v['phi']/(2*np.pi) for v in endpoints],
                  endpoint_action_eV_fs=[abs(v['action']) for v in endpoints],
                  action_bar_fractions=[abs(v['action'])/ACTION_MAX for v in endpoints],
                  frames=round(DURATION*FPS), fps=FPS,
                  max_phase_step_radians=KAPPAS[-1]*TAU_MAX/(PASS_DURATION-START_HOLD-END_HOLD)/FPS,
                  invariant_errors=errors, published_master_changed=False)
    (OUT / 'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    review()
    validate()
    if args.render:
        renderer.OUT = OUT
        renderer.encode(12, dict(duration=DURATION, render=episode))
        renderer.preview(12)
    html = '''<!doctype html><html><meta charset="utf-8"><title>Reel 12 · Action and phase</title>
<style>body{margin:0;background:#080b14;color:#fff2e4;font:16px system-ui;display:grid;place-items:center;min-height:100vh}main{text-align:center}video{display:block;max-height:87vh;max-width:96vw;margin:auto}a{color:#46beff}p{margin:12px}</style>
<main><video controls playsinline loop preload="metadata" poster="ccr2-12-cover.jpg"><source src="ccr2-12-preview.webm" type="video/webm"><source src="ccr2-12.mp4" type="video/mp4"></video>
<p>Reel 12 · Action and phase · 24 seconds · <a href="ccr2-12.mp4">MP4</a></p></main></html>'''
    (OUT/'index.html').write_text(html, encoding='utf8')


if __name__ == '__main__':
    main()
