"""Rendering and encoded-review helpers for the two D3 desktop adaptations."""
from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
import imageio_ffmpeg

W, H, FPS = 1600, 900, 24
BG, INK, MUTED = '#fffcf6', '#232426', '#77746e'
GRID, FAINT = '#bdb8ae', '#e4ded3'
BLUE, GOLD, RED, GREEN = '#396fa8', '#a96d15', '#bb4c40', '#32866c'
OUT = ROOT / 'content/drafts/animations'


def ease(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


@lru_cache(64)
def font(size=26, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('seguisb.ttf' if bold else 'segoeui.ttf'),
                  Path(matplotlib.get_data_path()) / 'fonts/ttf' /
                  ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError('No suitable font')


@lru_cache(160)
def equation(tex, size=32, color=INK):
    stream = BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$'+tex+'$', stream, format='png', dpi=180, color=color,
                      prop=matplotlib.font_manager.FontProperties(size=size*72/180))
    stream.seek(0)
    return Image.open(stream).convert('RGBA')


class Canvas:
    def __init__(self):
        self.im = Image.new('RGB', (W, H), BG)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []

    def track(self, box, label):
        box = tuple(float(v) for v in box)
        assert box[0] >= 8 and box[1] >= 8 and box[2] <= W-8 and box[3] <= H-8, (label, box)
        self.boxes.append((box, label))

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la'):
        f = font(size, bold)
        self.track(self.d.textbbox((x, y), value, font=f, anchor=anchor), value)
        self.d.text((x, y), value, font=f, fill=color, anchor=anchor)

    def math(self, x, y, tex, size=35, color=INK, center=False):
        pic = equation(tex, size, color)
        px = round(x-pic.width/2) if center else round(x)
        py = round(y-pic.height/2)
        self.track((px, py, px+pic.width, py+pic.height), tex)
        self.im.paste(pic, (px, py), pic)

    def line(self, points, color=GRID, width=2):
        self.d.line([tuple(p) for p in points], fill=color, width=width, joint='curve')

    def arrow(self, a, b, color, width=5):
        a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        d = b-a
        length = np.linalg.norm(d)
        if length < 1:
            return
        d /= length
        n = np.array([-d[1], d[0]])
        head = min(19, length*.4)
        self.line([a,b], color, width)
        self.d.polygon([tuple(b), tuple(b-head*d+.4*head*n), tuple(b-head*d-.4*head*n)], fill=color)

    def dot(self, p, r, color, outline=None, width=2):
        x,y=p
        self.d.ellipse((x-r,y-r,x+r,y+r), fill=color, outline=outline, width=width)

    def check(self):
        for i,(a,na) in enumerate(self.boxes):
            for b,nb in self.boxes[i+1:]:
                ow=min(a[2],b[2])-max(a[0],b[0])
                oh=min(a[3],b[3])-max(a[1],b[1])
                assert ow<=0 or oh<=0,(na,nb,a,b)


def run(name, duration, moments, poster_time, render, validate, source):
    parser=argparse.ArgumentParser()
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--check', action='store_true')
    args=parser.parse_args()
    out=OUT
    review=ROOT/'.tools'/f'{name}-review'
    out.mkdir(parents=True,exist_ok=True)
    review.mkdir(parents=True,exist_ok=True)
    report=validate()
    report.update({'size':[W,H], 'fps':FPS, 'duration_seconds':duration,
                   'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
                   'helper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    # Every rendered frame checks text bounds and label-label collisions.
    sheet=Image.new('RGB',(1200,math.ceil(len(moments)/3)*250),BG)
    draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(moments):
        im=render(t)
        im.save(review/f'{t:05.1f}.png')
        x,y=(i%3)*400,(i//3)*250
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+228),f'{t:g}s',font=font(17),fill=MUTED)
    sheet.save(review/'contact.png')
    render(poster_time).save(out/f'{name}-poster.png')
    (out/f'{name}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    video=out/f'{name}.mp4'
    if args.render:
        temp=review/f'{name}.rendering.mp4'
        command=[ffmpeg,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
                 '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
                 '-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',
                 '-threads','2',str(temp)]
        with subprocess.Popen(command,stdin=subprocess.PIPE) as proc:
            try:
                for i in range(round(duration*FPS)):
                    proc.stdin.write(render(i/FPS).tobytes())
                    if i%(FPS*6)==0:
                        print(f'{name}: {i/FPS:g}/{duration}s',flush=True)
                proc.stdin.close()
                if proc.wait():
                    raise RuntimeError('FFmpeg failed')
            except BaseException:
                proc.kill()
                raise
        temp.replace(video)
    if args.check:
        reader=imageio_ffmpeg.read_frames(str(video))
        try:
            meta=next(reader)
        finally:
            reader.close()
        count,seconds=imageio_ffmpeg.count_frames_and_secs(str(video))
        assert meta['size']==(W,H) and meta['fps']==FPS
        assert count==round(duration*FPS) and abs(seconds-duration)<.05
        subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
        indices=[min(count-1,round(t*FPS)) for t in moments]
        selection='+'.join(f'eq(n\\,{n})' for n in indices)
        subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                        f'select={selection},scale=480:270,tile=3x{math.ceil(len(indices)/3)}',
                        '-frames:v','1',str(out/f'{name}-contact-sheet.png')],check=True)
        report={'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
                'frame_count':count,'duration_seconds':seconds,'size':meta['size'],
                'fps':meta['fps'],'decode':'passed','contact_sheet_frame_indices':indices}
        (out/f'{name}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
        print(json.dumps(report),flush=True)
