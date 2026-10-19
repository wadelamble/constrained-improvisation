"""Render the proposed Casimir addition without renumbering the review series."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from core import *
import imageio_ffmpeg
import casimir
import render as series

OUT = series.OUT
STEM = 'casimir-15a'
REVIEW = OUT/'review'/'casimir'


def initialize_text():
    text = series.TEXT.read_text(encoding='utf8')
    if '## Reel 15a' in text:
        return
    caption = (series.TEXT.parent/'casimir-caption-draft.txt').read_text(encoding='utf8').strip()
    addition = '\n'.join([
        '## Reel 15a', '', '### Title', '', casimir.TITLE, '', '### Caption', '',
        caption, '', '### On-screen text', '',
        *['- '+value for value in casimir.SCREEN_TEXT], '', '### Source', '',
        'Invariants and Casimir operators. New visual construction in the ordinary three-dimensional vector representation, with C = L²/ℏ². Proposed addition after Reel 15. Review numbering is unchanged pending approval.', '',
        '### Visual check', '',
        'Apply the three squared-generator terms on fixed axes, bring their output arrows tip to tail, then turn the input while recomputing every contribution. Their sum remains 2v.', '',
        '---', '', '',
    ])
    assert '## Reel 16\n' in text
    series.TEXT.write_text(text.replace('## Reel 16\n',addition+'## Reel 16\n',1),encoding='utf8')


def entry():
    text = series.TEXT.read_text(encoding='utf8')
    match = re.search(r'^## Reel 15a\s*\n(.*?)(?=^## |\Z)',text,re.M|re.S)
    if not match:
        raise ValueError('Missing editable Reel 15a in reel-text.md')
    sections = re.split(r'^###\s+(.+?)\s*$',match.group(1),flags=re.M)
    fields = {sections[i].lower():sections[i+1].strip() for i in range(1,len(sections),2)}
    title, body = fields['title'], fields['caption']
    onscreen = [line[2:].strip() for line in fields['on-screen text'].splitlines() if line.startswith('- ')]
    if len(onscreen)!=len(casimir.SCREEN_TEXT):
        raise ValueError('Preserve the on-screen label slots.')
    TEXT_REPLACEMENTS.clear()
    TEXT_REPLACEMENTS.update(zip(casimir.SCREEN_TEXT,onscreen))
    continuation = re.search(r'^## Reel 15b\s*\n.*?^### Title\s*\n+([^\n]+)', text, re.M|re.S)
    next_title = continuation.group(1).strip() if continuation else series.entries()[16]['title']
    caption = ('Symmetry to Waves · Casimir operators\n'+title+'\n\n'+body+
               '\n\nNext: '+next_title+'\n'
               'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
               '#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics')
    assert series.buffer_count(caption)<=2196, series.buffer_count(caption)
    return dict(title=title,caption=caption,on_screen_text=onscreen,duration=casimir.DURATION,
                caption_count=series.buffer_count(caption))


def review(e):
    REVIEW.mkdir(parents=True,exist_ok=True)
    times = [0,3,5.5,7.5,9.5,11.5,14,18,22,26,30,33]
    sheet = Image.new('RGB',(4*270,3*510),BG)
    for i,t in enumerate(times):
        pic = casimir.render(t,e)
        pic.save(REVIEW/f'{STEM}-{t:04.1f}.png')
        x,y = (i%4)*270,(i//4)*510
        sheet.paste(pic.resize((270,480),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+8,y+484),f'{t:.1f}s',fill=INK,font=font(18))
    sheet.save(REVIEW/f'{STEM}-contact.jpg',quality=95)
    casimir.render(14.8,e).save(OUT/f'{STEM}-cover.jpg',quality=95)


def encode(e):
    target,temporary = OUT/f'{STEM}.mp4',OUT/f'{STEM}.rendering.mp4'
    command = [imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
               '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
               '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',
               '-movflags','+faststart','-threads','3',str(temporary)]
    with subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as process:
        try:
            for index in range(casimir.DURATION*FPS):
                process.stdin.write(casimir.render(index/FPS,e).tobytes())
                if index%300==0:
                    print(f'Casimir: {index}/{casimir.DURATION*FPS} frames',flush=True)
            process.stdin.close()
            err = process.stderr.read().decode('utf8',errors='replace')
            if process.wait():
                raise RuntimeError(err)
        except BaseException:
            process.kill()
            raise
    temporary.replace(target)


def package(e):
    video = OUT/f'{STEM}.mp4'
    digest = hashlib.sha256(video.read_bytes()).hexdigest()[:12] if video.exists() else 'pending'
    (OUT/f'{STEM}-caption.txt').write_text(e['caption'],encoding='utf8')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Casimir operator — reel review</title>
<style>:root{color-scheme:dark;font-family:system-ui;background:#080b14;color:#fff2e4}body{max-width:1100px;margin:auto;padding:28px}a{color:#46beff}h1{font-size:32px}main{display:grid;grid-template-columns:minmax(250px,430px) 1fr;gap:30px;align-items:start}video{width:100%;max-height:80vh;position:sticky;top:16px}pre{white-space:pre-wrap;font:16px/1.6 system-ui}article{background:#111a2a;border:1px solid #334258;border-radius:12px;padding:22px}button{font:inherit;background:#1d3543;color:#fff2e4;padding:9px;border:1px solid #547c8e;border-radius:6px;cursor:pointer}.links{display:flex;gap:18px;flex-wrap:wrap}.muted{color:#a5b2c8}@media(max-width:720px){main{display:block}video{position:static;max-height:72vh}}</style>
<div class="links"><a href="index.html#15">← Reel 15</a><a href="index.html#16">Reel 16 →</a><a href="../../../notes/reels/symmetry-series-v2/reel-text.md">Edit titles and captions</a></div>
<h1>15a · __TITLE__</h1><p class="muted">Proposed addition after Reel 15 · 34 seconds · Offline review</p>
<main><video controls playsinline preload="metadata" poster="casimir-15a-cover.jpg?v=__VERSION__" src="casimir-15a.mp4?v=__VERSION__"></video><article><p class="muted">Caption count __COUNT__ / 2196</p><button id="copy">Copy caption</button><pre id="caption">__CAPTION__</pre><a href="casimir-15a.mp4?v=__VERSION__">Open MP4</a></article></main>
<script>document.getElementById('copy').onclick=async()=>{await navigator.clipboard.writeText(document.getElementById('caption').textContent);document.getElementById('copy').textContent='Copied';};</script></html>'''
    for key,value in {'__TITLE__':html.escape(e['title']),'__VERSION__':digest,
                      '__COUNT__':str(e['caption_count']),'__CAPTION__':html.escape(e['caption'])}.items():
        page = page.replace(key,value)
    if re.search(r'^## Reel 15b\s*$',series.TEXT.read_text(encoding='utf8'),re.M):
        page = page.replace('<a href="index.html#16">Reel 16 →</a>',
                            '<a href="lie.html">Reel 15b →</a>')
    (OUT/'casimir.html').write_text(page,encoding='utf8')
    series.package(series.entries())


def validate_media():
    video = OUT/f'{STEM}.mp4'
    frames = imageio_ffmpeg.read_frames(str(video))
    try:
        meta = next(frames)
    finally:
        frames.close()
    assert meta['size']==(W,H) and meta['fps']==FPS
    assert abs(meta['duration']-casimir.DURATION)<.1
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(video),
                    '-vf',f'fps={12/casimir.DURATION},scale=270:480,tile=4x3',
                    '-frames:v','1','-q:v','2',str(REVIEW/f'{STEM}-decoded.jpg')],check=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--init-text',action='store_true')
    parser.add_argument('--review',action='store_true')
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--package',action='store_true')
    parser.add_argument('--validate-media',action='store_true')
    args = parser.parse_args()
    if args.init_text:
        initialize_text()
    e = entry()
    print(json.dumps(casimir.validate()),flush=True)
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
