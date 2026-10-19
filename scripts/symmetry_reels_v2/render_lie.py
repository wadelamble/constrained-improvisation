"""Render and stage the Lie algebra continuation for offline review."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from core import *
import imageio_ffmpeg
import lie_commutator as animation
import render as series

OUT = series.OUT
STEM = 'lie-15b'
REVIEW = OUT/'review'/'lie'


def entry():
    document = series.TEXT.read_text(encoding='utf-8-sig')
    match = re.search(r'^## Reel 15b\s*\n(.*?)(?=^## |\Z)', document, re.M|re.S)
    if not match:
        raise ValueError('Missing editable Reel 15b in reel-text.md')
    sections = re.split(r'^###\s+(.+?)\s*$', match.group(1), flags=re.M)
    fields = {sections[i].lower():sections[i+1].strip() for i in range(1,len(sections),2)}
    onscreen = [line[2:].strip() for line in fields['on-screen text'].splitlines() if line.startswith('- ')]
    if len(onscreen)!=len(animation.SCREEN_TEXT):
        raise ValueError('Preserve the on-screen label slots.')
    TEXT_REPLACEMENTS.clear()
    TEXT_REPLACEMENTS.update(zip(animation.SCREEN_TEXT,onscreen))
    title = fields['title']
    if not title or '\n' in title:
        raise ValueError('A nonempty, one-line title is required.')
    next_title = series.entries()[16]['title']
    caption = ('Symmetry to Waves · Lie algebra\n'+title+'\n\n'+fields['caption']+
               '\n\nNext: '+next_title+'\n'
               'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
               '#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics')
    count = series.buffer_count(caption)
    if count>2196:
        raise ValueError(f'Caption needs author revision: {count} > 2196. No truncation performed.')
    signature = hashlib.sha256(json.dumps([title,onscreen],ensure_ascii=False).encode('utf8')).hexdigest()
    return dict(title=title,caption=caption,on_screen_text=onscreen,duration=animation.DURATION,
                caption_count=count,visual_sha256=signature)


def review(e):
    REVIEW.mkdir(parents=True,exist_ok=True)
    times = [0,3,6,9,12,16,20,24,28,32,36,animation.DURATION-1]
    sheet = Image.new('RGB',(4*270,3*510),BG)
    for i,t in enumerate(times):
        pic = animation.render(t,e)
        pic.save(REVIEW/f'{STEM}-{t:04.1f}.png')
        x,y = (i%4)*270,(i//4)*510
        sheet.paste(pic.resize((270,480),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+8,y+484),f'{t:.1f}s',fill=INK,font=font(18))
    sheet.save(REVIEW/f'{STEM}-contact.jpg',quality=95)
    animation.render(24,e).save(OUT/f'{STEM}-cover.jpg',quality=95)


def encode(e):
    OUT.mkdir(parents=True,exist_ok=True)
    target,temporary = OUT/f'{STEM}.mp4',OUT/f'{STEM}.rendering.mp4'
    count = round(animation.DURATION*FPS)
    command = [imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
               '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
               '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',
               '-movflags','+faststart','-threads','3',str(temporary)]
    with subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as process:
        try:
            for index in range(count):
                process.stdin.write(animation.render(index/FPS,e).tobytes())
                if index%300==0:
                    print(f'Lie algebra: {index}/{count} frames',flush=True)
            process.stdin.close()
            err = process.stderr.read().decode('utf8',errors='replace')
            if process.wait():
                raise RuntimeError(err)
        except BaseException:
            process.kill()
            raise
    temporary.replace(target)
    (OUT/f'{STEM}-render.json').write_text(json.dumps({'visual_sha256':e['visual_sha256']},indent=2),encoding='utf8')


def package(e):
    video = OUT/f'{STEM}.mp4'
    digest = hashlib.sha256(video.read_bytes()).hexdigest()[:12] if video.exists() else 'pending'
    record = OUT/f'{STEM}-render.json'
    stale = not record.exists() or json.loads(record.read_text(encoding='utf8'))['visual_sha256']!=e['visual_sha256']
    (OUT/f'{STEM}-caption.txt').write_text(e['caption'],encoding='utf8')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lie algebra — reel review</title>
<style>:root{color-scheme:dark;font-family:system-ui;background:#080b14;color:#fff2e4}body{max-width:1100px;margin:auto;padding:28px}a{color:#46beff}h1{font-size:32px}main{display:grid;grid-template-columns:minmax(250px,430px) 1fr;gap:30px;align-items:start}video{width:100%;max-height:80vh;position:sticky;top:16px}pre{white-space:pre-wrap;font:16px/1.6 system-ui}article{background:#111a2a;border:1px solid #334258;border-radius:12px;padding:22px}button{font:inherit;background:#1d3543;color:#fff2e4;padding:9px;border:1px solid #547c8e;border-radius:6px;cursor:pointer}.links{display:flex;gap:18px;flex-wrap:wrap}.muted{color:#a5b2c8}@media(max-width:720px){main{display:block}video{position:static;max-height:72vh}}</style>
<div class="links"><a href="casimir.html">← Reel 15a</a><a href="index.html#16">Reel 16 →</a><a href="../../../notes/reels/symmetry-series-v2/reel-text.md">Edit titles and captions</a></div>
<h1>15b · __TITLE__</h1><p class="muted">New continuation of Reel 15 · __DURATION__ seconds · Offline review</p>__STALE__
<main><video controls playsinline preload="metadata" poster="lie-15b-cover.jpg?v=__VERSION__" src="lie-15b.mp4?v=__VERSION__"></video><article><p class="muted">Caption count __COUNT__ / 2196</p><button id="copy">Copy caption</button><pre id="caption">__CAPTION__</pre><a href="lie-15b.mp4?v=__VERSION__">Open MP4</a></article></main>
<script>document.getElementById('copy').onclick=async()=>{try{await navigator.clipboard.writeText(document.getElementById('caption').textContent);document.getElementById('copy').textContent='Copied';}catch{const r=document.createRange();r.selectNodeContents(document.getElementById('caption'));const s=window.getSelection();s.removeAllRanges();s.addRange(r);document.getElementById('copy').textContent='Selected — press Ctrl+C';}};</script></html>'''
    for key,value in {'__TITLE__':html.escape(e['title']),'__VERSION__':digest,
                      '__DURATION__':str(animation.DURATION),
                      '__COUNT__':str(e['caption_count']),'__CAPTION__':html.escape(e['caption']),
                      '__STALE__':'<p style="color:#ffb45e">The video needs rendering after text edits.</p>' if stale else ''}.items():
        page = page.replace(key,value)
    (OUT/'lie.html').write_text(page,encoding='utf8')
    series.package(series.entries())


def validate_media():
    video = OUT/f'{STEM}.mp4'
    frames = imageio_ffmpeg.read_frames(str(video))
    try:
        meta = next(frames)
    finally:
        frames.close()
    assert meta['size']==(W,H) and meta['fps']==FPS
    assert abs(meta['duration']-animation.DURATION)<.1
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(video),
                    '-vf',f'fps={12/animation.DURATION},scale=270:480,tile=4x3',
                    '-frames:v','1','-q:v','2',str(REVIEW/f'{STEM}-decoded.jpg')],check=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('review','render','package','validate-media'):
        parser.add_argument('--'+flag,action='store_true')
    args = parser.parse_args()
    e = entry()
    print(json.dumps(animation.validate()),flush=True)
    if args.review:
        review(e)
    if args.render:
        encode(e)
    if args.package:
        package(e)
    if args.validate_media:
        print(json.dumps(validate_media()),flush=True)


if __name__=='__main__':
    main()
