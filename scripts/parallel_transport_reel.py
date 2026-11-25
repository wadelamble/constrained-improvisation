"""Portrait adaptation of the chapter's parallel-transport commutator.

Renders new reel assets only; never changes the desktop figure or publishes.
Exact geometry and canvas primitives are reused from the desktop renderer.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
import generate_symmetry_parallel_transport_commutator as model

OUT = ROOT / 'content/reels/parallel-transport'
REVIEW = OUT / 'review'
TEXT = ROOT / 'notes/reels/parallel-transport/reel-text.md'
NAME = 'parallel-transport'
TITLE = 'The commutator encodes curvature'
W, H, FPS, DURATION = 1080, 1920, 30, 34.
BG, INK, MUTED = '#080b14', '#fff2e4', '#a5b2c8'
GRID, FAINT, SURFACE = '#34465b', '#182234', '#0d1421'
BLUE, GOLD, GREEN = '#46beff', '#ffb45e', '#36e099'
TIMES = [0., 4.5, 8., 11.5, 14., 18., 22., 25.5, 31.5]
POSTER_TIME = 31.5
MUSIC_START = 130.
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Canvas drawing is parameterized by the desktop module's display constants.
# Only this Python process is affected; desktop source/assets stay unchanged.
for key, value in dict(W=W, H=H, S=2, BG=BG, INK=INK, MUTED=MUTED,
                       GRID=GRID, FAINT=FAINT, SURFACE=SURFACE,
                       BLUE=BLUE, COPPER=GOLD, GREEN=GREEN,
                       ORIGIN=np.array([540., 930.]), RADIUS=345.).items():
    setattr(model, key, value)

Canvas, project, fade = model.Canvas, model.project, model.fade


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sphere_base():
    c = Canvas()
    c.text((70, 164), 'NATURE’S IMPROVISATION ON SYMMETRY', 25, MUTED, bold=True)
    c.text((70, 214), 'PARALLEL TRANSPORT', 27, GOLD, bold=True)
    c.text((70, 270), 'The commutator', 57, INK, bold=True)
    c.text((70, 338), 'encodes curvature', 57, INK, bold=True)
    c.math((540, 450), r'\Delta\mathbf v=[T_x(a),T_y(b)]\mathbf v', 45, INK, center=True)
    c.math((120, 520), '=', 42, INK, center=True)
    c.math((310, 520), r'T_x(a)T_y(b)\mathbf v', 42, GOLD, center=True)
    c.math((540, 520), '-', 42, INK, center=True)
    c.math((770, 520), r'T_y(b)T_x(a)\mathbf v', 42, BLUE, center=True)
    c.text((310, 556), 'y, then x', 27, GOLD, center=True)
    c.text((770, 556), 'x, then y', 27, BLUE, center=True)
    x, y = model.ORIGIN * model.S
    r = model.RADIUS * model.S
    c.d.ellipse((x-r, y-r, x+r, y+r), fill=SURFACE, outline=GRID, width=3)
    angles = np.linspace(0, 2*math.pi, 601)
    for lat in (-math.pi/3, -math.pi/6, 0, math.pi/6, math.pi/3):
        rr, z = math.cos(lat), math.sin(lat)
        model.sphere_curve(c, np.column_stack([rr*np.cos(angles), rr*np.sin(angles), np.full(len(angles), z)]))
    for lon in np.linspace(0, math.pi, 7, endpoint=False):
        model.sphere_curve(c, np.column_stack([np.cos(angles)*math.cos(lon), np.cos(angles)*math.sin(lon), np.sin(angles)]))
    c.line(project(model.route_curve(model.BLUE_ROUTE)), GRID, 2.)
    c.line(project(model.route_curve(model.COPPER_ROUTE)), GRID, 2.)
    c.dot(project(model.N), 6., INK)
    c.dot(project(model.END), 6., INK)
    c.text(project(model.N)+[-36, 28], 'A', 30, INK, bold=True, backing=True)
    c.text(project(model.END)+[24, -34], 'B', 30, INK, bold=True, backing=True)
    c.text(project(model.point(.5*model.A, 0))+[3, 28], 'x', 28, MUTED, backing=True)
    c.text(project(model.point(0, .5*model.B))+[-37, 0], 'y', 28, MUTED, backing=True)
    c.line([(70, 1690), (950, 1690)], GRID, 2.)
    c.text((70, 1724), 'SYMMETRY', 23, MUTED)
    return c.im, c.boxes


BASE = None


def vector_on_sphere(c, p, v, color, alpha=1.):
    c.arrow(project(p), project(p+.32*v), color, 6., alpha, 20.)
    c.dot(project(p), 5., color, alpha)


def compare(c, t):
    visible = fade(t, 22.5, 23.5)
    if visible < .002:
        return
    c.text((540, 1318), 'Same endpoint. Different directions.', 32, INK,
           bold=True, center=True, alpha=visible)
    c.text((540, 1371), 'In the tangent plane at B', 26, MUTED, center=True, alpha=visible)
    origin, length = np.array([395., 1425.]), 220.
    def tangent(v):
        return origin + length*np.array([np.dot(v, model.INSET_E1), -np.dot(v, model.INSET_E2)])
    blue, gold = tangent(model.V_BLUE), tangent(model.V_COPPER)
    c.arrow(origin, blue, BLUE, 6., visible, 20.)
    c.arrow(origin, gold, GOLD, 6., visible, 20.)
    c.dot(origin, 5., INK, visible)
    c.text(origin+[-34, -13], 'B', 27, INK, bold=True, alpha=visible)
    c.text(blue+[22, -13], 'x, then y', 26, BLUE, alpha=visible)
    c.text(gold+[-14, 23], 'y, then x', 26, GOLD, alpha=visible)
    grow = fade(t, 24., 25.2)
    c.arrow(blue, blue+grow*(gold-blue), GREEN, 5., grow, 17.)
    c.math((700, 1507), r'\Delta\mathbf v', 40, GREEN, alpha=grow)
    foot = fade(t, 28., 29.)
    c.text((540, 1605), 'For small coordinate steps a and b:', 25, MUTED, center=True, alpha=foot)
    c.math((540, 1657), r'\Delta\mathbf v\approx ab[\hat D_x,\hat D_y]\mathbf v', 40, INK,
           center=True, alpha=foot)


def render(t):
    global BASE
    if BASE is None:
        BASE = sphere_base()
    c = Canvas(BASE[0])
    c.boxes = BASE[1].copy()
    which, blue_p, gold_p = model.stage(t)
    if blue_p > 0:
        c.line(project(model.route_curve(model.BLUE_ROUTE, blue_p)), BLUE, 4.3)
    if gold_p > 0:
        c.line(project(model.route_curve(model.COPPER_ROUTE, gold_p)), GOLD, 4.3)
    vector_on_sphere(c, model.N, model.V0, MUTED, .4)
    if which == 'intro':
        vector_on_sphere(c, model.N, model.V0, INK)
        c.text((540, 1335), 'One arrow. Two routes.', 35, INK, bold=True, center=True)
        c.text((540, 1400), 'Carry the arrow from A to B.', 29, MUTED, center=True)
        c.text((540, 1450), 'The surface determines how it turns.', 29, MUTED, center=True)
    elif which.startswith('blue'):
        p, v = model.transport(model.BLUE_ROUTE, blue_p)
        vector_on_sphere(c, p, v, BLUE)
        c.text((540, 1335), 'First x, then y', 35, BLUE, bold=True, center=True)
        c.math((540, 1420), r'T_y(b)T_x(a)\mathbf v', 51, BLUE, center=True)
        c.text((540, 1500), 'Keep the resulting blue arrow.', 29, MUTED, center=True,
               alpha=fade(t, 10.8, 11.6))
    else:
        vector_on_sphere(c, model.END, model.V_BLUE, BLUE)
        if which == 'reset':
            vector_on_sphere(c, model.N, model.V0, GOLD, fade(t, 12.7, 13.5))
            c.text((540, 1335), 'Start again from A.', 35, INK, bold=True, center=True)
            c.text((540, 1400), 'Same initial arrow. Reverse the order.', 29, MUTED, center=True)
        elif which.startswith('copper'):
            p, v = model.transport(model.COPPER_ROUTE, gold_p)
            vector_on_sphere(c, p, v, GOLD)
            c.text((540, 1335), 'First y, then x', 35, GOLD, bold=True, center=True)
            c.math((540, 1420), r'T_x(a)T_y(b)\mathbf v', 51, GOLD, center=True)
        else:
            vector_on_sphere(c, model.END, model.V_COPPER, GOLD)
            compare(c, t)
    c.line([(70, 1690), (70+880*np.clip(t/DURATION, 0, 1), 1690)], GOLD, 4.)
    c.text((830, 1724), f'{t:04.1f} / {DURATION:g} s', 23, MUTED)
    return c.finish()


def sheet(frames, times, path):
    result = Image.new('RGB', (900, 1710), BG)
    draw = ImageDraw.Draw(result)
    for i, (frame, t) in enumerate(zip(frames, times)):
        x, y = (i % 3)*300, (i // 3)*570
        result.paste(frame.resize((300, 533), Image.Resampling.LANCZOS), (x, y))
        draw.text((x+12, y+539), f'{t:g} s', font=model.font(10), fill=INK)
    result.save(path, quality=95)


def preview():
    for t in TIMES:
        render(t).save(REVIEW / f'preview-{t:04.1f}.jpg', quality=95)
    sheet([render(t) for t in TIMES], TIMES, REVIEW / 'source-contact-sheet.jpg')
    render(POSTER_TIME).save(OUT / f'{NAME}-poster.jpg', quality=95)
    render(POSTER_TIME).save(OUT / f'{NAME}-cover.jpg', quality=95)
    print('Preview and poster ready', flush=True)


def encode(music):
    assert music.is_file(), f'Missing supplied music: {music}'
    target = OUT / f'{NAME}.mp4'
    temporary = OUT / f'{NAME}.rendering.mp4'
    cmd = [FFMPEG, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-ss', str(MUSIC_START),
           '-i', str(music), '-map', '0:v:0', '-map', '1:a:0',
           '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-threads', '3',
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
           '-af', f'volume=-4dB,afade=t=in:st=0:d=1.5,afade=t=out:st={DURATION-2}:d=2',
           '-t', str(DURATION), '-map_metadata', '-1', '-movflags', '+faststart', str(temporary)]
    start = time.time()
    log = ROOT / '.tools/parallel-transport-reel-encode.log'
    with log.open('wb') as err, subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=err) as proc:
        try:
            for i in range(round(DURATION*FPS)):
                proc.stdin.write(render(i/FPS).tobytes())
                if i % 150 == 0:
                    print(f'Rendered {i/FPS:g}/{DURATION:g}s', flush=True)
            proc.stdin.close()
            if proc.wait():
                raise RuntimeError(log.read_text(errors='replace'))
        except BaseException:
            proc.kill()
            raise
    temporary.replace(target)
    print(f'Encoded in {time.time()-start:.1f}s', flush=True)


def validate(music=None):
    path = OUT / f'{NAME}.mp4'
    reader = imageio_ffmpeg.read_frames(str(path), pix_fmt='rgb24')
    meta = next(reader)
    wanted = {round(t*FPS) for t in TIMES}
    frames = {}
    count = 0
    for i, data in enumerate(reader):
        count += 1
        if i in wanted:
            frames[i] = Image.frombytes('RGB', (W,H), data)
    reader.close()
    assert count == round(DURATION*FPS)
    assert meta['size'] == (W,H) and meta['fps'] == FPS
    assert abs(meta['duration']-DURATION) < .1 and meta.get('audio_codec') == 'aac'
    decoded = subprocess.run([FFMPEG, '-v', 'error', '-i', str(path), '-map', '0:a:0',
                              '-f', 'f32le', '-acodec', 'pcm_f32le', '-'], capture_output=True, check=True)
    audio = np.frombuffer(decoded.stdout, dtype='<f4')
    peak, rms = float(np.max(np.abs(audio))), float(np.sqrt(np.mean(audio.astype(float)**2)))
    assert np.isfinite(audio).all() and peak < .95 and rms > 1e-5
    assert abs(len(audio)/(48000*2)-DURATION) < .1
    sheet([frames[round(t*FPS)] for t in TIMES], TIMES, REVIEW / 'decoded-contact-sheet.jpg')
    frames[round(POSTER_TIME*FPS)].save(OUT / f'{NAME}-poster.jpg', quality=95)
    frames[round(POSTER_TIME*FPS)].save(OUT / f'{NAME}-cover.jpg', quality=95)
    report = dict(passed=True, metadata=meta, complete_decode_frames=count, audio_rms=rms, audio_peak=peak,
                  video_sha256=sha(path), renderer_sha256=sha(__file__),
                  source_sha256=sha(ROOT/'scripts/generate_symmetry_parallel_transport_commutator.py'),
                  geometry=model.validate_math(),
                  layout='Text bounds and pairwise text collisions checked on every rendered frame',
                  music=dict(artist='Herbie Hancock',title='Maiden Voyage (Remastered 2012)',
                             excerpt_start_seconds=MUSIC_START, gain_db=-4, fade_in_seconds=1.5, fade_out_seconds=2))
    if music:
        report['music']['source_sha256'] = sha(music)
    (REVIEW/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(f'Validated {count} frames; audio RMS {rms:.4f}, peak {peak:.4f}', flush=True)


def package():
    content = TEXT.read_text(encoding='utf8')
    body = content.split('### Caption\n', 1)[1].split('\n### ', 1)[0].strip()
    caption = (TITLE+'\n\n'+body+'\n\n'
               'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
               '#Physics #ScienceExplained #Symmetry #Geometry #Mathematics')
    assert len(caption) < 2100
    (OUT/f'{NAME}-caption.txt').write_text(caption+'\n', encoding='utf8')
    episode = dict(number=1,title=TITLE,caption=caption,caption_file=f'{NAME}-caption.txt',
                   duration=DURATION,video=f'{NAME}.mp4',cover=f'{NAME}-cover.jpg',poster=f'{NAME}-poster.jpg',
                   contact_sheet='review/decoded-contact-sheet.jpg',thumbnail_offset_ms=round(POSTER_TIME*1000),
                   source='content/drafts/animations/symmetry-parallel-transport-commutator.mp4')
    if (OUT/f'{NAME}.mp4').exists():
        episode['video_sha256'] = sha(OUT/f'{NAME}.mp4')
    manifest = dict(series='Parallel transport',status='validated local reel',published=False,
                    editable_text=TEXT.relative_to(ROOT).as_posix(),episodes=[episode],
                    music=dict(artist='Herbie Hancock',title='Maiden Voyage (Remastered 2012)',
                               excerpt_start_seconds=MUSIC_START,duration_seconds=DURATION))
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parallel transport — reel review</title><style>body{background:#080b14;color:#fff2e4;font:17px/1.6 system-ui;max-width:1100px;margin:auto;padding:28px}a{color:#46beff}.row{display:grid;grid-template-columns:minmax(240px,390px) 1fr;gap:30px}video{width:100%;max-height:80vh}pre{white-space:pre-wrap;font:inherit}@media(max-width:700px){.row{grid-template-columns:1fr}}</style>
<h1>'''+html.escape(TITLE)+'''</h1><div class="row"><video controls playsinline preload="metadata" poster="parallel-transport-poster.jpg" src="parallel-transport.mp4"></video><div><p>34 seconds · 1080 × 1920 · 30 fps</p><p>Herbie Hancock — <i>Maiden Voyage (Remastered 2012)</i></p><p><a href="parallel-transport.mp4">MP4</a> · <a href="review/decoded-contact-sheet.jpg">Contact sheet</a> · <a href="parallel-transport-caption.txt">Caption</a></p><pre>'''+html.escape(caption)+'''</pre></div></div></html>'''
    (OUT/'index.html').write_text(page,encoding='utf8')


def main():
    parser = argparse.ArgumentParser()
    for flag in ('preview','render','validate','package'):
        parser.add_argument('--'+flag,action='store_true')
    parser.add_argument('--music-source',type=Path)
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True,parents=True)
    REVIEW.mkdir(exist_ok=True)
    if args.preview:
        preview()
    if args.render:
        if args.music_source is None:
            parser.error('--render requires --music-source pointing to the supplied recording')
        encode(args.music_source)
    if args.validate:
        validate(args.music_source)
    if args.package:
        package()


if __name__ == '__main__':
    main()
