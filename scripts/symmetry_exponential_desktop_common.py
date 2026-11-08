"""Drawing and delivery helpers for the two exponential desktop adaptations."""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
from io import BytesIO
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
OUT = ROOT / 'content/drafts/animations'
BG, INK, MUTED = '#fffcf6', '#232426', '#77746e'
GRID, FAINT = '#c6c0b6', '#e7e1d7'
BLUE, RED, GREEN, GOLD = '#396fa8', '#bb4c40', '#32866c', '#a96d15'


def ease(u):
    u = float(np.clip(u, 0, 1))
    return u*u*(3-2*u)


def progress(t, start, end):
    return ease((t-start)/(end-start))


@lru_cache(64)
def font(size=26, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('seguisb.ttf' if bold else 'segoeui.ttf'),
                  Path(matplotlib.get_data_path()) / 'fonts/ttf' /
                  ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise FileNotFoundError('No suitable text font')


@lru_cache(512)
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
        assert min(box[:2]) >= 8 and box[2] <= W-8 and box[3] <= H-8, (label, box)
        self.boxes.append((box, label))

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la'):
        f = font(size, bold)
        self.track(self.d.textbbox((x,y), value, font=f, anchor=anchor), value)
        self.d.text((x,y), value, font=f, fill=color, anchor=anchor)

    def math(self, x, y, tex, size=35, color=INK, center=False, label=False):
        pic = equation(tex, size, color)
        px, py = round(x-pic.width/2) if center else round(x), round(y-pic.height/2)
        self.track((px,py,px+pic.width,py+pic.height),tex)
        if label:
            self.d.rectangle((px-5,py-4,px+pic.width+5,py+pic.height+4),fill=BG)
        self.im.paste(pic,(px,py),pic)

    def line(self, points, color=GRID, width=2):
        self.d.line([tuple(p) for p in points],fill=color,width=width,joint='curve')

    def arrow(self, a, b, color=INK, width=3, head=12):
        a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
        delta=b-a
        length=np.linalg.norm(delta)
        if length < 1:
            return
        unit=delta/length
        normal=np.array([-unit[1],unit[0]])
        head=min(head,.4*length)
        self.line([a,b],color,width)
        self.d.polygon([tuple(b),tuple(b-head*unit+.4*head*normal),
                        tuple(b-head*unit-.4*head*normal)],fill=color)

    def dot(self,p,r=5,color=INK):
        x,y=p
        self.d.ellipse((x-r,y-r,x+r,y+r),fill=color)


def footer(s,t,duration,caption):
    s.line([(52,833),(1548,833)],FAINT,2)
    s.line([(52,833),(52+1496*t/duration,833)],GOLD,3)
    s.text(52,853,caption,21,MUTED)


def run(name, duration, render, validate, moments, poster_time, source):
    parser=argparse.ArgumentParser()
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    review=ROOT/'.tools'/f'{name}-review'
    review.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    report=validate()
    report.update(size=[W,H],fps=FPS,duration_seconds=duration,
                  source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
                  helper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUT/f'{name}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    sheet=Image.new('RGB',(1200,math.ceil(len(moments)/3)*250),BG)
    draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(moments):
        im=render(t)
        im.save(review/f'{t:05.1f}.png')
        x,y=i%3*400,i//3*250
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+228),f'{t:g}s',font=font(17),fill=MUTED)
    sheet.save(review/'contact.png')
    render(poster_time).save(OUT/f'{name}-poster.png')
    print(json.dumps(report),flush=True)
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    destination=OUT/f'{name}.mp4'
    if args.render:
        temporary=review/f'{name}.rendering.mp4'
        command=[ffmpeg,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
                 '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
                 '-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',
                 '-threads','2',str(temporary)]
        with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
            try:
                for i in range(duration*FPS):
                    process.stdin.write(render(i/FPS).tobytes())
                    if i%(FPS*8)==0:
                        print(f'{name}: {i/FPS:.0f}/{duration} seconds',flush=True)
                process.stdin.close()
                if process.wait():
                    raise RuntimeError('FFmpeg encoding failed')
            except BaseException:
                process.kill()
                raise
        temporary.replace(destination)
    if args.check:
        stream=imageio_ffmpeg.read_frames(str(destination))
        meta=next(stream)
        stream.close()
        count,seconds=imageio_ffmpeg.count_frames_and_secs(str(destination))
        assert meta['size']==(W,H) and meta['fps']==FPS
        assert count==duration*FPS and abs(seconds-duration)<.05
        subprocess.run([ffmpeg,'-v','error','-i',str(destination),'-f','null','-'],check=True)
        indices=[min(round(t*FPS),count-1) for t in moments[:9]]
        selection='+'.join(f'eq(n\\,{n})' for n in indices)
        subprocess.run([ffmpeg,'-y','-v','error','-i',str(destination),'-vf',
                        f'select={selection},scale=480:270,tile=3x3','-frames:v','1',
                        str(OUT/f'{name}-contact-sheet.png')],check=True)
        result=dict(video_sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),
                    frame_count=count,duration_seconds=seconds,size=meta['size'],fps=meta['fps'],
                    decode='passed',contact_sheet_frame_indices=indices)
        (OUT/f'{name}-encoded-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
        print(json.dumps(result),flush=True)
