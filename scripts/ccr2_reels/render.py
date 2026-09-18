"""Render, inspect, and package the complete CCR-2 portrait series."""
from __future__ import annotations
import argparse
import csv
import html
import hashlib
import importlib
import json
import re
import subprocess
import time
import zipfile
from core import *
import imageio_ffmpeg

OUT=ROOT/'content'/'reels'/'ccr2-series'
MODULES=('episodes_symmetry','episodes_wave','episodes_paths','episodes_quantum')

def episodes():
    result={}
    for name in MODULES:
        try: module=importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name==name:continue
            raise
        for number, original in module.EPISODES.items():
            entry=dict(original)
            entry['source_duration']=original['duration']
            entry['duration']=original['duration']/PLAYBACK_SPEED
            entry['render']=lambda t, render=original['render']: render(t*PLAYBACK_SPEED)
            for key in ('checkpoints',):
                if key in original:entry[key]=[t/PLAYBACK_SPEED for t in original[key]]
            if 'cover_time' in original:entry['cover_time']=original['cover_time']/PLAYBACK_SPEED
            result[number]=entry
    return dict(sorted(result.items()))

def slug(number):return f'ccr2-{number:02d}'

def review_frames(number,entry):
    folder=OUT/'review';folder.mkdir(parents=True,exist_ok=True)
    times=entry.get('checkpoints',[2,entry['duration']*.35,entry['duration']*.65,entry['duration']-1])
    thumbs=[]
    for t in times:
        pic=entry['render'](float(t))
        assert pic.size==(W,H), (number,pic.size)
        pic=pic.convert('RGB')
        name=folder/f'{slug(number)}-{t:05.1f}.jpg'
        pic.save(name,quality=90)
        thumb=pic.resize((270,480),Image.Resampling.LANCZOS)
        thumbs.append(thumb)
    sheet=Image.new('RGB',(270*len(thumbs),520),BG)
    d=ImageDraw.Draw(sheet)
    for i,(pic,t) in enumerate(zip(thumbs,times)):
        sheet.paste(pic,(270*i,0))
        d.text((270*i+10,488),f'{t:g}s',font=font(20),fill=INK)
    sheet.save(folder/f'{slug(number)}-contact-sheet.jpg',quality=93)
    cover_t=entry.get('cover_time',times[len(times)//2])
    source=entry['render'](cover_t).convert('RGB')
    # Keep the cover title and representative art within the central square too.
    cover=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(cover)
    d.text((90,430),'CONSTRAINED IMPROVISATION',font=font(27,True),fill=MUTED)
    d.text((90,490),f'{number:02d}  /  WAVES TO QUANTA',font=font(30,True),fill=GOLD)
    fitted_title(d, entry.get('video_title', entry['title']), x=90, y=550,
                 width=860, max_height=145, size=56)
    art=source.crop((70,480,950,1410)).resize((760,803),Image.Resampling.LANCZOS)
    cover.paste(art,(160,710))
    cover.save(OUT/f'{slug(number)}-cover.jpg',quality=95)
    return times

def encode(number,entry):
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/f'{slug(number)}.mp4'
    temporary=OUT/f'{slug(number)}.rendering.mp4'
    n=round(entry['duration']*FPS)
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
         '-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-threads','4',str(temporary)]
    start=time.time()
    with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
        try:
            for i in range(n):
                pic=entry['render'](i/FPS).convert('RGB')
                proc.stdin.write(pic.tobytes())
                if i%240==0:print(f'episode {number:02d}: {i}/{n} frames; {time.time()-start:.0f}s',flush=True)
            proc.stdin.close()
            error=proc.stderr.read().decode('utf8',errors='replace')
            status=proc.wait()
            if status:raise RuntimeError(error)
        except BaseException:
            proc.kill();raise
    temporary.replace(target)
    print(f'episode {number:02d}: DONE, {target.stat().st_size/1e6:.1f} MB, {time.time()-start:.1f}s',flush=True)

def preview(number):
    source=OUT/f'{slug(number)}.mp4'
    target=OUT/f'{slug(number)}-preview.webm'
    if target.exists() and target.stat().st_mtime>=source.stat().st_mtime:return
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(source),
        '-vf','scale=720:1280','-an','-c:v','libvpx-vp9','-b:v','0','-crf','30',
        '-deadline','realtime','-cpu-used','8','-threads','4',str(target)],check=True)
    print(f'Browser preview {number:02d} complete',flush=True)

def bundle():
    target=OUT.parent/'ccr2-series-package.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
        for path in sorted(OUT.iterdir()):
            if path.is_file() and not any(tag in path.name for tag in ('.rendering.','.retiming.')):
                archive.write(path,Path('ccr2-series')/path.name)
    print(f'Portable package: {target}',flush=True)

def package(entries):
    OUT.mkdir(parents=True,exist_ok=True)
    receipt_path=ROOT/'notes'/'reels'/'ccr2-series'/'buffer-staging-status.json'
    receipt=json.loads(receipt_path.read_text(encoding='utf8')) if receipt_path.exists() else None
    receipts={row['order']:row for row in receipt.get('episodes',[])} if receipt is not None else {}
    matching_receipts=0
    items=[]
    for number,e in entries.items():
        stem=slug(number)
        prose=e['caption'].strip()
        prose=re.sub(r'^\d+\s*/\s*13\s*[—·–-]\s*','',prose)
        if prose.split('\n',1)[0].strip()==e['title']:
            prose=prose.split('\n',1)[1].strip()
        prose=re.sub(r'\s*Next:.*$','',prose,flags=re.S).strip()
        caption=f'Waves to Quanta · {number}/13\n{e["title"]}\n\n{prose}\n\n'
        if number<13:
            following=entries[number+1]['title']
            caption+=f'Next: {following}'+('' if following.endswith(('.', '?', '!')) else '.')+'\n'
        caption+='Website: https://wadelamble.github.io/constrained-improvisation/\n'
        caption+='Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n#Physics #ScienceExplained #FourierTransform #NaturalPhilosophy #QuantumMechanics'
        (OUT/f'{stem}-caption.txt').write_text(caption,encoding='utf8')
        times=e.get('checkpoints',[2,e['duration']*.35,e['duration']*.65,e['duration']-1])
        item=dict(order=number,title=e['title'],video_title=e.get('video_title',e['title']),duration_seconds=e['duration'],
                  video=f'{stem}.mp4',cover=f'{stem}-cover.jpg',caption_file=f'{stem}-caption.txt',
                  preview=f'{stem}-preview.webm',
                  caption=caption,cover_video_timestamp=e.get('cover_time',times[len(times)//2]),
                  source_section=('Wave Symmetry' if number<=4 else 'Position / Wave Number Uncertainty' if number==5 else 'Wave Propagation and Interference' if number<=11 else 'From Wave Mechanics to Quantum Mechanics'),
                  status='staged',audio='silent',width=W,height=H,fps=FPS,
                  playback_speed=PLAYBACK_SPEED,source_duration_seconds=e['source_duration'])
        video_path=OUT/f'{stem}.mp4'
        if video_path.exists():
            item['video_bytes']=video_path.stat().st_size
            with video_path.open('rb') as handle:
                item['video_sha256']=hashlib.file_digest(handle,'sha256').hexdigest()
        recorded=receipts.get(number)
        # Receipts hash caption text with LF line endings, as in the manifest.
        if (recorded and item.get('video_sha256')
                and recorded.get('video_sha256')==item['video_sha256']
                and recorded.get('caption_sha256')==hashlib.sha256(caption.encode('utf8')).hexdigest()):
            matching_receipts+=1
            item['status']=recorded.get('status','staged')
            for key in ('media_url','buffer_post_id','sent_at','external_link'):
                if recorded.get(key):item[key]=recorded[key]
            instagram_url=recorded.get('instagram_url') or recorded.get('external_link')
            if instagram_url:item['instagram_url']=instagram_url
        items.append(item)
    publishing_status='Local staging only; no account connected or posts submitted.'
    publishing_label='No account connected'
    publishing_notes='''These files are staged locally. Nothing has been uploaded or published, and no
Instagram credentials have been requested or stored. When the account is ready,
the manifest can drive an authorized upload queue: create a Reel container,
upload/fetch its video, await processing, then publish in order. Actual publishing
needs an eligible professional account and appropriate permissions; see the
research and preparation notes in `notes/reels/ccr2-series/` in the repository.'''
    if receipt is not None:
        hosted=sum(bool(item.get('media_url')) for item in items)
        drafts=sum(item['status']=='draft' and bool(item.get('buffer_post_id')) for item in items)
        published=sum(item['status']=='sent' and bool(item.get('buffer_post_id')) for item in items)
        account='@'+receipt['instagram'] if receipt.get('instagram') else 'Instagram'
        publishing_status=f'Recorded for {account}: {hosted}/{len(items)} current videos hosted; {published}/{len(items)} current Instagram reels published; {drafts}/{len(items)} Buffer drafts.'
        if receipt.get('published') is False and not any(row.get('status')=='sent' for row in receipts.values()):
            publishing_status+=' No Instagram posts published in this staging run.'
        if matching_receipts<len(items):
            publishing_status+=f' {len(items)-matching_receipts} current episodes have no matching receipt; local staging status retained.'
        if receipt.get('updated_at'):
            publishing_status+=f' Receipt updated: {receipt["updated_at"]}.'
        publishing_label=publishing_status
        publishing_notes=publishing_status+'\n\n'+'''The manifest includes public media URLs, Buffer post IDs, Instagram links, and
publication timestamps only when the recorded video and caption hashes match
this package. Any remaining Buffer drafts require a separate scheduling or
publishing action. Publishing receipts remain in
`notes/reels/ccr2-series/buffer-staging-status.json`; the website build copies
only the MP4 media, not these receipts or this review package.'''
    manifest=dict(series='Waves to Quanta',source='notes/worked/symmetry-ccr-2.md',
                  publishing_status=publishing_status,
                  sequence='Cumulative: publish in order.',episodes=items)
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    with (OUT/'manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['order','title','video','cover','caption_file','duration_seconds','status','caption'])
        writer.writeheader()
        for item in items:writer.writerow({k:item[k] for k in writer.fieldnames})
    data=json.dumps(items,ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Waves to Quanta — the reel series</title>
<style>:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#080b14;color:#fff2e4}*{box-sizing:border-box}body{margin:0}header{max-width:1380px;margin:auto;padding:42px 32px 26px}.eyebrow{color:#ffb45e;letter-spacing:.14em;font-size:12px;text-transform:uppercase}h1{font-size:clamp(30px,4vw,54px);margin:14px 0}header p{color:#a5b2c8;max-width:760px;line-height:1.65}a{color:#46beff}main{max-width:1380px;margin:auto;padding:0 32px 64px;display:grid;grid-template-columns:220px minmax(250px,430px) minmax(250px,1fr);gap:26px;align-items:start}nav{display:grid;gap:7px}button{font:inherit;cursor:pointer;background:#111a2a;border:1px solid #334258;color:#fff2e4;border-radius:9px;padding:12px;text-align:left}nav button{font-size:14px;line-height:1.4}button.active{border-color:#ffb45e;background:#252031}video{width:100%;max-height:76vh;aspect-ratio:9/16;background:#080b14;border-radius:15px}article{background:#111a2a;border:1px solid #334258;border-radius:15px;padding:24px}h2{margin-top:0;font-size:24px}pre{font:16px/1.65 system-ui;white-space:pre-wrap;overflow-wrap:anywhere}.links{display:flex;gap:15px;flex-wrap:wrap;font-size:14px}.muted{color:#a5b2c8;font-size:13px}.copy{margin:12px 0}@media(max-width:1000px){main{grid-template-columns:1fr 1fr}nav{grid-column:1/-1;grid-template-columns:repeat(auto-fill,minmax(170px,1fr))}}@media(max-width:650px){header{padding:25px 20px}main{display:flex;flex-direction:column;padding:0 20px 40px}nav{display:flex;width:100%;overflow:auto}nav button{min-width:180px}video{max-height:75vh}article{width:100%}}</style>
<header><div class="eyebrow">Constrained Improvisation · CCR-2</div><h1>Waves to Quanta</h1><p>Thirteen silent reels, one connected argument. Start with translations, follow the interference, and arrive at quantum mechanics. The explanation beside each video is its accompanying post caption.</p><p class="muted">Local review package · 1080 × 1920 · 24 fps · No account connected · <a href="manifest.csv">Publishing manifest</a> · <a href="README.md">Production notes</a></p></header>
<main><nav id="episodes" aria-label="Episodes"></nav><video id="player" controls playsinline preload="metadata"></video><article><h2 id="title"></h2><p class="muted" id="duration"></p><div class="links"><a id="download">Video</a><a id="cover">Cover</a><a id="captionfile">Caption TXT</a></div><button class="copy" id="copy">Copy caption</button><pre id="caption"></pre></article></main>
<script>const items=__DATA__;let current=0;const q=id=>document.getElementById(id);function select(i){current=i;const e=items[i];q('player').pause();q('player').src=e.preview||e.video;q('player').poster=e.cover;q('title').textContent=String(e.order).padStart(2,'0')+' · '+(e.video_title||e.title);q('duration').textContent=e.duration_seconds+' seconds · Silent';q('caption').textContent=e.caption;for(const [id,key] of [['download','video'],['cover','cover'],['captionfile','caption_file']])q(id).href=e[key];document.querySelectorAll('nav button').forEach((b,j)=>b.classList.toggle('active',i===j));history.replaceState(null,'','#'+e.order)}items.forEach((e,i)=>{const b=document.createElement('button');b.textContent=String(e.order).padStart(2,'0')+'  '+(e.video_title||e.title);b.onclick=()=>select(i);q('episodes').append(b)});q('copy').onclick=async()=>{try{await navigator.clipboard.writeText(items[current].caption);q('copy').textContent='Copied';setTimeout(()=>q('copy').textContent='Copy caption',1800)}catch{const r=document.createRange();r.selectNodeContents(q('caption'));const s=window.getSelection();s.removeAllRanges();s.addRange(r);q('copy').textContent='Caption selected — press Ctrl+C'}};select(Math.max(0,Math.min(items.length-1,Number(location.hash.slice(1)||1)-1)));</script></html>'''.replace('__DATA__',data)
    page=page.replace('<a id="captionfile">Caption TXT</a>',
        '<a id="captionfile">Caption TXT</a><a id="instagram" target="_blank" rel="noopener noreferrer" hidden>View on Instagram</a>')
    page=page.replace("q('caption').textContent=e.caption;",
        "q('caption').textContent=e.caption;q('instagram').hidden=!e.instagram_url;"
        "if(e.instagram_url)q('instagram').href=e.instagram_url;else q('instagram').removeAttribute('href');")
    page=page.replace('24 fps · No account connected ·',f'{FPS} fps · {PLAYBACK_SPEED:g}× playback · {html.escape(publishing_label)} ·',1)
    page=page.replace("e.duration_seconds+' seconds · Silent'","e.duration_seconds.toFixed(2)+' seconds · Silent'")
    page=page.replace('<video id="player" controls playsinline preload="metadata"></video>',
        '<section class="watch"><video id="player" controls playsinline preload="metadata"></video>'
        '<div class="links"><button id="toggle">Play</button><button id="previous">Previous</button>'
        '<button id="next">Next</button><span class="muted" id="elapsed"></span></div></section>')
    page=page.replace('items.forEach((e,i)=>{',
        "q('toggle').onclick=()=>{const v=q('player');if(v.paused)v.play().catch(()=>q('elapsed').textContent='Open the Video link to play');else v.pause()};"
        "q('player').onplay=()=>q('toggle').textContent='Pause';q('player').onpause=()=>q('toggle').textContent='Play';"
        "q('player').ontimeupdate=()=>q('elapsed').textContent=Math.floor(q('player').currentTime)+' / '+items[current].duration_seconds.toFixed(2)+' s';"
        "q('previous').onclick=()=>select(Math.max(0,current-1));q('next').onclick=()=>select(Math.min(items.length-1,current+1));"
        'items.forEach((e,i)=>{')
    (OUT/'index.html').write_text(page,encoding='utf8')
    (OUT/'README.md').write_text('''# Waves to Quanta — review and publishing package

Open `index.html` to review thirteen reels in order. Each video has a matching
cover JPEG and UTF-8 post-caption TXT. `manifest.json` and `manifest.csv` retain
the ordering and exact pairings. Captions are post text, not narration.

__PUBLISHING_NOTES__
The CSV is our portable manifest, not a claim that Instagram directly imports CSV.

All MP4s are 1080×1920, __FPS__ fps, H.264/yuv420p, fast-start, and silent.
Playback is __SPEED__× the original pace, with all original frames retained.
The gallery
uses lighter 720×1280 WebM previews; the Video link provides the full MP4. Preview
framing leaves margins for player controls. Platforms can change overlays, so
check the first draft in the destination app before posting the series.

Source: `notes/worked/symmetry-ccr-2.md`. Production source:
`scripts/ccr2_reels/`. Original chapter and existing animations are preserved.
Run `render.py --review`, `render.py --render --episodes 1 2`, or
`render.py --previews --package --bundle` with the project Python runtime to
regenerate the review and portable publishing package.

Equations and simulations are original renderings. The final spacetime/action
episodes are a compact preview, with physical assumptions identified in captions.
The series does not claim to derive dynamics or the Born rule from the CCR alone.
'''.replace('__PUBLISHING_NOTES__',publishing_notes).replace('__FPS__',str(FPS)).replace('__SPEED__',f'{PLAYBACK_SPEED:g}'),encoding='utf8')
    print(f'Packaged {len(items)} episodes at {OUT}',flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--episodes',nargs='+',type=int)
    parser.add_argument('--review',action='store_true');parser.add_argument('--render',action='store_true')
    parser.add_argument('--package',action='store_true');parser.add_argument('--previews',action='store_true')
    parser.add_argument('--bundle',action='store_true');args=parser.parse_args()
    entries=episodes();selected=args.episodes or list(entries)
    if args.package:package(entries)
    for number in selected:
        entry=entries[number]
        if args.review:review_frames(number,entry);print(f'Reviewed {number:02d}',flush=True)
        if args.render:encode(number,entry)
        if args.previews:preview(number)
    if args.bundle:bundle()

if __name__=='__main__':main()
