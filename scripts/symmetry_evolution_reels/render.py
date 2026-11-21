"""Render, validate and package five local reels. Never publishes anything."""
from __future__ import annotations
import argparse
import hashlib
import html
import importlib
import json
import re
import subprocess
import time
from core import *
import imageio_ffmpeg

OUT=ROOT/'content/reels/symmetry-evolution'
TEXT=ROOT/'notes/reels/symmetry-evolution/reel-text.md'
DURATIONS={1:24,2:24,3:23,4:17,5:42}
MOMENTS={1:(0,3,6,9,13,16.5,18,21,23.9),
         2:(0,3,6,9,13,16.5,18,21,23.9),
         3:(0,2.5,4.5,8.5,12.5,16,19,20.5,22.9),
         4:(0,2.5,4.5,6.5,9.5,12,14,15,16.9),
         5:(0,3,7.5,12,18,23,28,35,41.9)}
POSTERS={1:18.3,2:18.3,3:20.5,4:14.5,5:28}
SOURCE_NAMES={1:'symmetry-reversible-histories',2:'symmetry-unitary-histories',
              3:'symmetry-operator-sandwich',4:'symmetry-uniform-operator-sandwich',
              5:'symmetry-mean-patch'}
MUSIC=ROOT/'.tools/reel-audio/music-bed.wav'
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def slug(n): return f'evolution-{n:02d}'
def module(n): return importlib.import_module('histories' if n<3 else 'operators' if n<5 else 'geometry')
def frame_at(n,t):
    im=module(n).render(n,float(t)).convert('RGB')
    assert im.size==(W,H)
    return im

def entries():
    parts=re.split(r'^## Reel\s+(\d+)\s*$',TEXT.read_text(encoding='utf-8-sig'),flags=re.M)
    result=[]
    for i in range(1,len(parts),2):
        n=int(parts[i]); sections=re.split(r'^###\s+(.+?)\s*$',parts[i+1],flags=re.M)
        fields={sections[j].lower().strip():sections[j+1].strip() for j in range(1,len(sections),2)}
        assert fields['title']==TITLES[n],f'Reel {n}: title changed; update renderer and rerender.'
        next_text=f'Next: {TITLES[n+1]}\n' if n<5 else ''
        caption=(f'State and evolution · {n}/5\n{fields["title"]}\n\n{fields["caption"]}\n\n'
                 +next_text+'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
                 '#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics')
        count=len(caption.encode('utf-16-le'))//2+caption.count('\n')
        assert count<=2196,(n,count)
        result.append(dict(number=n,title=fields['title'],caption=caption,caption_count=count,
            on_screen_text=fields.get('on-screen text',''),duration=DURATIONS[n],
            video=slug(n)+'.mp4',cover=slug(n)+'-cover.jpg',poster=slug(n)+'-poster.jpg',
            contact_sheet='review/'+slug(n)+'-decoded.jpg',
            source='content/drafts/animations/'+SOURCE_NAMES[n]+'.mp4'))
    assert [e['number'] for e in result]==[1,2,3,4,5]
    return result

def previews(n):
    (OUT/'review').mkdir(exist_ok=True,parents=True)
    sheet=Image.new('RGB',(900,1710),BG)
    d=ImageDraw.Draw(sheet)
    for i,t in enumerate(MOMENTS[n]):
        im=frame_at(n,t); x=(i%3)*300; y=(i//3)*570
        sheet.paste(im.resize((300,533),Image.Resampling.LANCZOS),(x,y))
        text(d,(x+12,y+538),f'{t:.1f} s',21,MUTED)
    sheet.save(OUT/'review'/f'{slug(n)}-source.jpg',quality=95)
    pic=frame_at(n,POSTERS[n]); pic.save(OUT/f'{slug(n)}-poster.jpg',quality=95)
    cover=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(cover)
    text(d,(90,354),'NATURE’S IMPROVISATION ON SYMMETRY',25,MUTED,bold=True)
    text(d,(90,405),f'STATE AND EVOLUTION · {n}/5',27,GOLD,bold=True)
    size=54
    while True:
        lines=wrap(d,TITLES[n],size,900,True)
        if len(lines)*(size+9)<=145:break
        size-=1
    for j,s in enumerate(lines):text(d,(90,465+j*(size+9)),s,size,INK,bold=True)
    art=pic.crop((70,470,950,1620));art.thumbnail((880,1000),Image.Resampling.LANCZOS)
    cover.paste(art,((W-art.width)//2,650))
    cover.save(OUT/f'{slug(n)}-cover.jpg',quality=95)
    print(f'Reel {n}: preview sheet + poster + cover',flush=True)

def encode(n):
    OUT.mkdir(exist_ok=True,parents=True)
    target=OUT/f'{slug(n)}.mp4'; temp=OUT/f'{slug(n)}.rendering.mp4'
    count=round(DURATIONS[n]*FPS); start=time.time()
    offset=sum(DURATIONS[j] for j in range(1,n))
    assert MUSIC.exists(),'Previously supplied music bed missing.'
    cmd=[FFMPEG,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
         '-r',str(FPS),'-i','-','-ss',str(offset),'-i',str(MUSIC),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','3',
         '-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
         '-af',f'afade=t=in:st=0:d=1.5,afade=t=out:st={DURATIONS[n]-2}:d=2',
         '-t',str(DURATIONS[n]),'-movflags','+faststart',str(temp)]
    log=OUT/'review'/f'{slug(n)}-encode.log'; log.parent.mkdir(exist_ok=True,parents=True)
    with log.open('wb') as err,subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err) as p:
        try:
            for i in range(count):
                p.stdin.write(frame_at(n,i/FPS).tobytes())
                if i%300==0:print(f'Reel {n}: {i}/{count}',flush=True)
            p.stdin.close()
            if p.wait():raise RuntimeError(log.read_text(errors='replace'))
        except BaseException:
            p.kill();raise
    temp.replace(target)
    print(f'Reel {n}: encoded {count} frames in {time.time()-start:.1f}s',flush=True)

def validate_media(n):
    path=OUT/f'{slug(n)}.mp4'
    reader=imageio_ffmpeg.read_frames(str(path));meta=next(reader);reader.close()
    assert meta['size']==(W,H) and meta['fps']==FPS,meta
    assert abs(meta['duration']-DURATIONS[n])<.1,meta
    assert meta.get('audio_codec')=='aac',meta
    decoded=subprocess.run([FFMPEG,'-v','error','-i',str(path),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','-'],capture_output=True,check=True)
    audio=np.frombuffer(decoded.stdout,dtype='<f4')
    assert np.isfinite(audio).all() and np.max(np.abs(audio))<.95
    rms=float(np.sqrt(np.mean(audio.astype(float)**2)))
    assert rms>1e-5
    assert abs(len(audio)/(48000*2)-DURATIONS[n])<.1
    subprocess.run([FFMPEG,'-y','-v','error','-i',str(path),'-vf',
         f'fps={9/DURATIONS[n]},scale=300:533,tile=3x3','-frames:v','1','-q:v','2',
         str(OUT/'review'/f'{slug(n)}-decoded.jpg')],check=True)
    record=dict(metadata=meta,audio_rms=rms,audio_peak=float(np.max(np.abs(audio))),
        video_sha256=sha(path),frames=count_frames(path),title=TITLES[n],
        source_sha256=sha(ROOT/'content/drafts/animations'/f'{SOURCE_NAMES[n]}.mp4'),
        render_source_sha256={p.relative_to(ROOT).as_posix():sha(p)
                             for p in sorted(Path(__file__).parent.glob('*.py'))})
    assert record['frames']==round(DURATIONS[n]*FPS)
    (OUT/'review'/f'{slug(n)}-validation.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    print(f'Reel {n}: video/audio validated',flush=True)
    return record

def count_frames(path):
    frames,seconds=imageio_ffmpeg.count_frames_and_secs(str(path))
    return frames

def package():
    all_entries=entries(); cards=[]
    for e in all_entries:
        n=e['number']; file=slug(n)+'-caption.txt'
        (OUT/file).write_text(e['caption'],encoding='utf8')
        e['caption_file']=file
        e['video_available']=(OUT/e['video']).exists()
        if e['video_available']:e['video_sha256']=sha(OUT/e['video'])
        cards.append(f'''<article id="reel-{n}"><h2>{n}. {html.escape(e['title'])}</h2>
<div class="row"><video controls preload="metadata" playsinline poster="{e['poster']}" src="{e['video']}"></video>
<div><p>{e['duration']} seconds · 1080 × 1920 · 30 fps</p>
<p><a href="{e['video']}" download>MP4</a> · <a href="{e['cover']}">Cover</a> · <a href="{e['contact_sheet']}">Contact sheet</a> · <a href="{file}">Caption text</a></p>
<button onclick="copyCaption(this)">Copy caption</button><small>{e['caption_count']} / 2200 characters</small>
<pre>{html.escape(e['caption'])}</pre></div></div></article>''')
    music_config=json.loads((ROOT/'.tools/reel-audio/music-bed.json').read_text())
    manifest=dict(status='local review',series='State and evolution',episodes=all_entries,
                  editable_text=TEXT.relative_to(ROOT).as_posix(),
                  music=dict(title='String Quartet No. 5, movement I',artist='Philip Glass · Kronos Quartet',
                             bed=music_config,fade_in_seconds=1.5,fade_out_seconds=2),
                  published=False)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>State and evolution — reel review</title><style>
*{box-sizing:border-box}body{background:#080b14;color:#fff2e4;font:17px/1.55 system-ui;margin:auto;padding:28px;max-width:1400px}a{color:#46beff}h1{margin-bottom:8px}h2{font-size:25px}article{border-top:1px solid #334258;margin-top:48px;padding-top:20px}.row{display:grid;grid-template-columns:minmax(240px,390px) 1fr;gap:32px}video{width:100%;max-height:780px;background:#111a2a}pre{white-space:pre-wrap;font:16px/1.6 system-ui;background:#111a2a;padding:24px;border-radius:10px}button{background:#ffb45e;border:0;border-radius:5px;padding:10px 18px;font:inherit;cursor:pointer}small{margin-left:16px;color:#a5b2c8}nav a{margin-right:18px} @media(max-width:760px){.row{grid-template-columns:1fr}body{padding:18px}video{max-height:72vh}pre{padding:16px}}
</style><h1>State and evolution</h1><p>Five new reels from <i>Nature’s Improvisation on Symmetry</i>. Local review.</p>
<p><a href="../../../notes/reels/symmetry-evolution/reel-text.md">Edit captions in Markdown</a> · Captions can be refreshed without rerendering the videos.</p>
<nav>'''+''.join(f'<a href="#reel-{n}">Reel {n}</a>' for n in range(1,6))+'''</nav>'''+''.join(cards)+'''
<script>async function copyCaption(b){const s=b.parentElement.querySelector('pre').textContent;try{await navigator.clipboard.writeText(s);b.textContent='Copied'}catch(e){b.textContent='Select caption below'}setTimeout(()=>b.textContent='Copy caption',2000)}document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})))</script></html>'''
    (OUT/'index.html').write_text(page,encoding='utf8')
    print('Packaged editable captions and local gallery',flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--reels',nargs='+',type=int,default=list(range(1,6)))
    p.add_argument('--preview',action='store_true');p.add_argument('--render',action='store_true')
    p.add_argument('--validate',action='store_true');p.add_argument('--package',action='store_true')
    p.add_argument('--models',action='store_true');a=p.parse_args()
    OUT.mkdir(exist_ok=True,parents=True)
    if a.models:
        checks={name:importlib.import_module(name).validate() for name in ('histories','operators','geometry')}
        (OUT/'model-validation.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
        print('All numerical models validated',flush=True)
    for n in a.reels:
        if a.preview:previews(n)
        if a.render:encode(n)
        if a.validate:validate_media(n)
    if a.package:package()

if __name__=='__main__':main()
