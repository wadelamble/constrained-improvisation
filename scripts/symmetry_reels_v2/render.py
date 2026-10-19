"""Offline-only rendering and packaging of Symmetry to Waves first cuts.

The editable Markdown file is the only title/caption input. This program never
edits it, touches the CCR series, calls an account, or publishes anything.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import importlib
import json
import os
import re
import subprocess
import time
from core import *
import imageio_ffmpeg

OUT = ROOT / 'content/reels/symmetry-series-v2'
TEXT = ROOT / 'notes/reels/symmetry-series-v2/reel-text.md'
SPECS = json.loads((Path(__file__).parent/'series.json').read_text(encoding='utf8'))
SPEC_BY_NUMBER = {e['number']:e for e in SPECS}
DURATIONS = {e['number']:e['duration'] for e in SPECS}


def slug(number):
    return f'symmetry-{number:02d}'


def buffer_count(text):
    return len(text.encode('utf-16-le'))//2 + text.count('\n')


def caption_math_text(text):
    """Remove paired dollar math delimiters for plain-text caption export.

    Keep equation contents, ordinary currency, and unmatched delimiters intact.
    The editable Markdown and on-screen TeX are not modified.
    """
    pattern = re.compile(
        r'(?<![\\$])\$\$(?!\$)(?P<display>.*?)\$\$(?!\$)'
        r'|(?<![\\$])\$(?![\s$])(?P<inline>[^\n$]*?)(?<![\s\\])\$(?![\w$])',
        flags=re.S,
    )
    return pattern.sub(lambda match: match.group('display')
                       if match.group('display') is not None
                       else match.group('inline'), text)


def visual_signature(entry):
    # Numbering is baked into every frame. A renumbered series must never
    # accept an old video or preview just because its title stayed the same.
    payload = dict(order=entry['order'],total=TOTAL,title=entry['title'],
                   screen_text=entry['on_screen_text'],duration=entry['duration'])
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode('utf8')).hexdigest()


def record_render(number, entry, kind):
    folder=OUT/'render-records'
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/f'{slug(number)}-{kind}.json'
    data=dict(order=number,total=TOTAL,title=entry['title'],screen_text=entry['on_screen_text'],
              visual_sha256=visual_signature(entry),width=W,height=H,fps=FPS,
              duration=entry['duration'])
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')


def entries(path=TEXT):
    if not Path(path).exists():
        raise ValueError(f'The editable title/caption document is required: {path}')
    document = Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    headings = re.findall(r'^## Reel\s+(.+?)\s*$', document, flags=re.M)
    if any(not h.isdigit() for h in headings) or [int(h) for h in headings] != list(range(1, TOTAL+1)):
        raise ValueError(f'Expected ordered Reel headings 1–{TOTAL}; found {headings}')
    parts = re.split(r'^## Reel\s+(\d+)\s*$', document, flags=re.M)
    result = {}
    for i in range(1, len(parts), 2):
        number, section = int(parts[i]), parts[i+1]
        sections = re.split(r'^###\s+(.+?)\s*$', section, flags=re.M)
        fields = {sections[j].strip().lower(): sections[j+1].strip()
                  for j in range(1, len(sections), 2)}
        if number in result:
            raise ValueError(f'Duplicate reel {number}')
        title = fields.get('title', '')
        body = fields.get('caption', '')
        if not title or '\n' in title or not body:
            raise ValueError(f'Reel {number}: one-line Title and nonempty Caption required')
        result[number] = dict(order=number, title=title, body=body,
                              duration=DURATIONS[number],
                              on_screen_text=[s[2:].strip() for s in fields.get('on-screen text', '').splitlines() if s.startswith('- ')],
                              source=fields.get('source', ''))
        result[number]['screen_text'] = result[number]['on_screen_text']
    if sorted(result) != list(range(1, TOTAL+1)):
        raise ValueError(f'Expected reels 1–{TOTAL}; found {sorted(result)}')
    for number, entry in result.items():
        continuation = (f'Next: {result[number+1]["title"]}' if number < TOTAL
                        else 'Continue with Waves to Quanta')
        caption = (f'Symmetry to Waves · {number}/{TOTAL}\n{entry["title"]}\n\n'
                   f'{entry["body"]}\n\n{continuation}\n'
                   'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
                   '#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics')
        caption = caption_math_text(caption)
        count = buffer_count(caption)
        if count > 2196:
            raise ValueError(f'Reel {number} caption needs author revision: Buffer count {count} > 2196; no truncation performed')
        entry['caption'], entry['buffer_count'] = caption, count
    return dict(sorted(result.items()))


@lru_cache(2)
def episode_module(number):
    return importlib.import_module('scenes')


def frame(number, t, entry):
    pic = episode_module(number).render(number, float(t), entry)
    if pic.size != (W, H):
        raise ValueError((number, pic.size))
    return pic.convert('RGB')


def review(number, entry):
    folder = OUT/'review'
    folder.mkdir(parents=True, exist_ok=True)
    times = np.linspace(0, entry['duration']-1/FPS, 9)
    sheet = Image.new('RGB', (3*270, 3*510), BG)
    d = ImageDraw.Draw(sheet)
    for index, t in enumerate(times):
        pic = frame(number, t, entry)
        pic.save(folder/f'{slug(number)}-{t:05.1f}.jpg', quality=93)
        x, y = (index%3)*270, (index//3)*510
        sheet.paste(pic.resize((270,480), Image.Resampling.LANCZOS), (x,y))
        d.text((x+12,y+484),f'{t:.2f} s',font=font(18),fill=INK)
    sheet.save(folder/f'{slug(number)}-contact-sheet.jpg',quality=94)
    cover_t = entry['duration']*.83
    source = frame(number, cover_t, entry)
    cover = Image.new('RGB',(W,H),BG)
    d = ImageDraw.Draw(cover)
    d.text((90,405),'VARIATIONS ON SYMMETRY',font=font(27,True),fill=MUTED)
    d.text((90,464),f'{number:02d}  /  SYMMETRY TO WAVES',font=font(30,True),fill=GOLD)
    fitted_title(d,entry['title'],x=90,y=525,width=860,max_height=158,size=56)
    art = source.crop((70,470,950,1640)).resize((660,878),Image.Resampling.LANCZOS)
    cover.paste(art,(210,709))
    cover.save(OUT/f'{slug(number)}-cover.jpg',quality=95)
    record_render(number,entry,'cover')
    return dict(order=number,title=entry['title'],checkpoints=times.tolist(),cover_time=cover_t)


def encode(number, entry):
    OUT.mkdir(parents=True,exist_ok=True)
    target, temporary = OUT/f'{slug(number)}.mp4', OUT/f'{slug(number)}.rendering.mp4'
    count = round(entry['duration']*FPS)
    command = [imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
               '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
               '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',
               '-movflags','+faststart','-threads','3',str(temporary)]
    start = time.time()
    with subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as process:
        try:
            for index in range(count):
                process.stdin.write(frame(number,index/FPS,entry).tobytes())
                if index%300 == 0:
                    print(f'Reel {number:02d}: {index}/{count} frames',flush=True)
            process.stdin.close()
            error = process.stderr.read().decode('utf8',errors='replace')
            if process.wait():
                raise RuntimeError(error)
        except BaseException:
            process.kill()
            raise
    temporary.replace(target)
    record_render(number,entry,'video')
    print(f'Reel {number:02d} encoded in {time.time()-start:.1f}s',flush=True)


def preview(number):
    source, target = OUT/f'{slug(number)}.mp4', OUT/f'{slug(number)}-preview.webm'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(source),
                    '-vf','scale=720:1280','-an','-c:v','libvpx-vp9','-b:v','0','-crf','32',
                    '-deadline','realtime','-cpu-used','8','-threads','3',str(target)],check=True)
    record_path=OUT/'render-records'/f'{slug(number)}-video.json'
    if record_path.exists():
        record=json.loads(record_path.read_text(encoding='utf8'))
        record['source_video_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
        (record_path.parent/f'{slug(number)}-preview.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')


def validate_media(number, entry):
    """Check the canonical MP4 and decode a contact sheet for motion review."""
    source = OUT/f'{slug(number)}.mp4'
    frames = imageio_ffmpeg.read_frames(str(source))
    try:
        metadata = next(frames)
    finally:
        frames.close()
    assert metadata['size'] == (W,H) and metadata['fps'] == FPS, number
    assert abs(metadata['duration']-entry['duration']) < .1, number
    folder = OUT/'review'
    folder.mkdir(parents=True,exist_ok=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(source),
                    '-vf',f'fps={12/entry["duration"]},scale=270:480,tile=4x3',
                    '-frames:v','1','-q:v','2',str(folder/f'{slug(number)}-decoded.jpg')],check=True)
    return metadata


def package(all_entries, text_path=TEXT):
    text_path = Path(text_path)
    if not text_path.exists():
        raise ValueError('The editable title/caption document must exist before packaging.')
    OUT.mkdir(parents=True,exist_ok=True)
    items = []
    for number, entry in all_entries.items():
        stem = slug(number)
        (OUT/f'{stem}-caption.txt').write_text(entry['caption'],encoding='utf8')
        item = dict(order=number,title=entry['title'],duration_seconds=entry['duration'],
                    video=f'{stem}.mp4',preview=f'{stem}-preview.webm',cover=f'{stem}-cover.jpg',
                    caption_file=f'{stem}-caption.txt',caption=entry['caption'],
                    caption_buffer_count=entry['buffer_count'],source=entry['source'],
                    on_screen_text=entry['on_screen_text'],status='offline review',
                    width=W,height=H,fps=FPS,audio='silent')
        item['desktop_sources']=SPEC_BY_NUMBER[number]['sources']
        item['required_visual_argument']=SPEC_BY_NUMBER[number]['required']
        item['visual_sha256']=visual_signature(entry)
        for kind in ('video','cover','preview'):
            record_path=OUT/'render-records'/f'{stem}-{kind}.json'
            record=json.loads(record_path.read_text(encoding='utf8')) if record_path.exists() else None
            item[f'{kind}_visual_sha256']=record.get('visual_sha256') if record else None
            item[f'{kind}_stale']=record is None or record.get('visual_sha256')!=item['visual_sha256']
        for key in ('video','preview','cover'):
            asset = OUT/item[key]
            item[f'{key}_available'] = asset.exists()
            if asset.exists():
                item[f'{key}_sha256'] = hashlib.sha256(asset.read_bytes()).hexdigest()
        preview_record = OUT/'render-records'/f'{stem}-preview.json'
        if preview_record.exists():
            record = json.loads(preview_record.read_text(encoding='utf8'))
            item['preview_stale'] |= record.get('source_video_sha256') != item.get('video_sha256')
        items.append(item)
    manifest = dict(series='Symmetry to Waves',source='content/drafts/symmetry-draft.md',
                    text_source=Path(os.path.relpath(text_path, ROOT)).as_posix(),
                    scope='Before The Fourier Structure of Waves',
                    status='Offline rebuilt series; nothing uploaded or published',episodes=items)
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    columns = ['order','title','video','cover','caption_file','duration_seconds','caption_buffer_count','status','caption']
    with (OUT/'manifest.csv').open('w',newline='',encoding='utf-8-sig') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns)
        writer.writeheader()
        writer.writerows({k:e[k] for k in columns} for e in items)
    data=json.dumps(items,ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Symmetry to Waves — offline review</title>
<style>:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#080b14;color:#fff2e4}*{box-sizing:border-box}body{margin:0}header{max-width:1420px;margin:auto;padding:32px}h1{font-size:42px;margin:12px 0}.muted{color:#a5b2c8;font-size:14px}a{color:#46beff}main{max-width:1420px;margin:auto;padding:0 32px 60px;display:grid;grid-template-columns:230px minmax(250px,430px) minmax(280px,1fr);gap:24px;align-items:start}nav{display:grid;gap:6px}button{font:inherit;color:#fff2e4;background:#111a2a;border:1px solid #334258;padding:10px;border-radius:7px;cursor:pointer;text-align:left}nav button{font-size:14px}.active{border-color:#ffb45e;background:#252031}video{width:100%;max-height:76vh;aspect-ratio:9/16;background:#080b14}article{padding:20px;background:#111a2a;border:1px solid #334258;border-radius:12px}h2{font-size:25px;margin:0 0 14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.62 system-ui}.links{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0}@media(max-width:1000px){main{grid-template-columns:1fr 1fr}nav{grid-column:1/-1;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}}@media(max-width:650px){main{display:flex;flex-direction:column;padding:0 20px}nav{display:flex;overflow:auto;width:100%}nav button{min-width:170px}article,.watch{width:100%}header{padding:24px 20px}}</style>
<header><div class="muted">VARIATIONS ON SYMMETRY</div><h1>Symmetry to Waves</h1><p>__TOTAL__ reels from the pool table to complex waves, including Casimir operators and Lie algebra.</p><p class="muted">Offline review · 1080 × 1920 · 30 fps · Nothing uploaded or published</p><div class="links"><a href="../../../notes/reels/symmetry-series-v2/reel-text.md">Review document (Markdown)</a><a href="manifest.csv">Manifest</a></div></header>
<main><nav id="nav"></nav><section class="watch"><video id="video" controls playsinline preload="metadata"></video><div class="links"><button id="previous">Previous</button><button id="next">Next</button><span id="elapsed" class="muted"></span></div><p id="availability" class="muted"></p></section><article><h2 id="title"></h2><p id="count" class="muted"></p><div class="links"><a id="mp4">MP4</a><a id="cover">Cover</a><a id="txt">Caption TXT</a></div><button id="copy">Copy caption</button><pre id="caption"></pre><details><summary>Desktop comparison</summary><p id="visual-argument"></p><div id="desktop-links" class="links"></div></details></article></main>
<script>const items=__DATA__;const q=id=>document.getElementById(id);let selected=0;function choose(i){selected=i;const e=items[i],v=q('video');v.pause();v.poster=e.cover;v.removeAttribute('src');if(e.preview_available||e.video_available)v.src=e.preview_available?e.preview:e.video;q('title').textContent=String(e.order).padStart(2,'0')+' · '+e.title;q('caption').textContent=e.caption;q('visual-argument').textContent=e.required_visual_argument;q('desktop-links').replaceChildren();e.desktop_sources.forEach((source,j)=>{const a=document.createElement('a');a.href='../../drafts/'+source;a.target='_blank';a.textContent='Desktop original'+(e.desktop_sources.length>1?' '+(j+1):'');q('desktop-links').append(a)});q('count').textContent=e.duration_seconds+' seconds · Caption count '+e.caption_buffer_count+' / 2196';q('availability').textContent=e.video_available?'':'Video is being prepared.';for(const[id,key]of[['mp4','video'],['cover','cover'],['txt','caption_file']])q(id).href=e[key];document.querySelectorAll('nav button').forEach((b,j)=>b.classList.toggle('active',i===j));history.replaceState(null,'','#'+e.order)}items.forEach((e,i)=>{const b=document.createElement('button');b.textContent=String(e.order).padStart(2,'0')+' '+e.title;b.onclick=()=>choose(i);q('nav').append(b)});q('previous').onclick=()=>choose(Math.max(0,selected-1));q('next').onclick=()=>choose(Math.min(items.length-1,selected+1));q('video').ontimeupdate=()=>q('elapsed').textContent=q('video').currentTime.toFixed(1)+' / '+items[selected].duration_seconds+' s';q('copy').onclick=async()=>{try{await navigator.clipboard.writeText(items[selected].caption);q('copy').textContent='Copied';setTimeout(()=>q('copy').textContent='Copy caption',1800)}catch{const r=document.createRange();r.selectNodeContents(q('caption'));const s=window.getSelection();s.removeAllRanges();s.addRange(r);q('copy').textContent='Selected — press Ctrl+C'}};choose(Math.max(0,Math.min(items.length-1,Number(location.hash.slice(1)||1)-1)));</script></html>'''.replace('__DATA__',data)
    page=page.replace("q('availability').textContent=e.video_available?'':'Video is being prepared.';",
        "q('availability').textContent=!e.video_available?'Video is being prepared.':e.video_stale?'Title or on-screen text changed — this video needs a new render.':'';"
        "q('availability').style.color=e.video_stale?'#ffb45e':'#a5b2c8';")
    page=page.replace("v.src=e.preview_available?e.preview:e.video;",
                      "v.src=e.preview_available&&!e.preview_stale?e.preview:e.video;")
    # A newly rendered reel keeps its filename. Version its preview URL so a
    # refreshed review page cannot silently replay the browser's old video.
    page=page.replace("let selected=0;",
        "const assetUrl=(e,key)=>e[key]+'?v='+(e[key+'_sha256']||'').slice(0,12);let selected=0;")
    page=page.replace("v.poster=e.cover;","v.poster=assetUrl(e,'cover');")
    page=page.replace("v.src=e.preview_available&&!e.preview_stale?e.preview:e.video;",
        "v.src=assetUrl(e,e.preview_available&&!e.preview_stale?'preview':'video');")
    page=page.replace('</style>', '''
@media(min-width:1001px){nav{position:sticky;top:20px;max-height:calc(100vh - 40px);overflow-y:auto;scrollbar-width:thin}.watch{position:sticky;top:20px}}
</style>''')
    page=page.replace('<a href="manifest.csv">Manifest</a>',
        '<a href="../../../notes/reels/symmetry-series-v2/desktop-coverage.md">Desktop coverage</a><a href="manifest.csv">Manifest</a>')
    page=page.replace('__TOTAL__',str(TOTAL))
    page=page.replace('Title or on-screen text changed — this video needs a new render.',
                      'Series numbering, title or on-screen text changed — this video needs a new render.')
    page=page.replace("q('desktop-links').replaceChildren();",
                      "q('desktop-links').replaceChildren();if(!e.desktop_sources.length)q('desktop-links').textContent='Supplementary equation demonstration.';")
    (OUT/'index.html').write_text(page,encoding='utf8')
    # Retain old bookmarks while all playback and navigation use one gallery.
    for alias, number in (('casimir.html',17),('lie.html',16)):
        target=f'index.html#{number}'
        title=html.escape(all_entries[number]['title'])
        redirect=(f'<!doctype html><html lang="en"><meta charset="utf-8">'
                  f'<meta http-equiv="refresh" content="0;url={target}">'
                  f'<title>{title} — Reel {number}</title>'
                  f'<p><a href="{target}">Reel {number}: {title}</a></p>'
                  f'<script>location.replace({json.dumps(target)});</script></html>')
        (OUT/alias).write_text(redirect,encoding='utf8')
    (OUT/'README.md').write_text('''# Symmetry to Waves — complete desktop adaptation

Open `index.html` to review all 27 reels in order. Titles, captions and on-screen text come from
`notes/reels/symmetry-series-v2/reel-text.md`; edit that document, then rerun
`scripts/symmetry_reels_v2/render.py --package`. Numbering, title or on-screen text
changes also require new video and cover renders. No account, upload, or
publishing code is present. Casimir and Lie algebra are Reels 17 and 16;
`casimir.html` and `lie.html` redirect to their normal gallery entries.

The source is `content/drafts/symmetry-draft.md`, stopping before “The Fourier
Structure of Waves.” The manuscript and Waves to Quanta series are preserved.
Masters: 1080×1920, 30 fps, silent H.264/yuv420p, fast-start. The gallery plays
the MP4 masters directly; optional 720×1280 WebM previews are used if generated.
Captions use the Buffer-adjusted UTF-16 count, limited to 2196.
The gallery and manifest explicitly identify missing media during production.
Render records include reel number and series length; previews from older
numbering remain stale until regenerated from the current MP4 masters.

Production commands use the available scientific Python runtime:
`render.py --review --render --package` (add `--episodes 1 2` for a subset).
Use `render.py --previews --package` only to make optional WebM previews.
The review contact sheets initially come from
the renderer. Final motion QA must also inspect dense frames decoded from MP4s.
''',encoding='utf8')
    print(f'Packaged {len(items)} offline captions; maximum count {max(e["caption_buffer_count"] for e in items)}',flush=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes',nargs='+',type=int)
    parser.add_argument('--review',action='store_true')
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--previews',action='store_true')
    parser.add_argument('--validate-media',action='store_true')
    parser.add_argument('--package',action='store_true')
    parser.add_argument('--text',type=Path,default=TEXT)
    args=parser.parse_args(argv)
    all_entries=entries(args.text)
    selected=args.episodes or list(all_entries)
    if any(number not in all_entries for number in selected):
        parser.error(f'--episodes must be in the range 1–{TOTAL}')
    review_rows=[]
    for number in selected:
        entry=all_entries[number]
        if args.review:
            review_rows.append(review(number,entry))
            print(f'Reviewed {number:02d}',flush=True)
        if args.render:
            encode(number,entry)
        if args.previews:
            preview(number)
        if args.validate_media:
            print(json.dumps(dict(order=number,metadata=validate_media(number,entry))),flush=True)
    if review_rows:
        (OUT/'review'/'last-review.json').write_text(json.dumps(review_rows,ensure_ascii=False,indent=2),encoding='utf8')
    if args.package:
        package(all_entries,args.text)


if __name__=='__main__':
    main()
