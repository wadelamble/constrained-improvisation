"""Shared portrait artwork for the CCR-2 silent reel series.

Coordinates are in the final 1080 x 1920 pixels. Keep essential artwork inside
x=70..950, y=160..1620, away from common social-player controls.
"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
import math
from functools import lru_cache
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image

W, H = 1080, 1920
# Episode choreography remains in its original clock. Playback preserves every
# authored frame while running that clock 1.75 times faster.
SOURCE_FPS = 24
PLAYBACK_SPEED = 1.75
FPS = round(SOURCE_FPS * PLAYBACK_SPEED)
BG = '#080b14'
PANEL = '#111a2a'
INK = '#fff2e4'
MUTED = '#a5b2c8'
GRID = '#334258'
BLUE = '#46beff'
RED = '#ff4269'
GOLD = '#ffb45e'
GREEN = '#36e099'
PURPLE = '#b999ff'

@lru_cache(128)
def font(size=32, bold=False):
    filename = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    paths = [Path('C:/Windows/Fonts') / filename,
             Path(matplotlib.get_data_path()) / 'fonts' / 'ttf' / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in paths:
        if p.exists():
            return ImageFont.truetype(str(p), int(size))
    return ImageFont.load_default()

def ease(u):
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2*u)

def lerp(a,b,u):
    return a + (b-a)*u

def window(t,a,b):
    return float(np.clip((t-a)/(b-a),0,1))

@lru_cache(384)
def equation(tex, size=44, color=INK):
    buf=BytesIO()
    with matplotlib.rc_context({'savefig.transparent': True}):
        math_to_image('$'+tex+'$',buf,format='png',dpi=150,color=color,
                      prop=matplotlib.font_manager.FontProperties(size=size*72/150))
    buf.seek(0)
    return Image.open(buf).convert('RGBA')

def fitted_title(draw, title, x=70, y=269, width=880, max_height=138, size=54):
    """Keep complete caption titles above the stage label, without truncation."""
    for chosen in range(size, 29, -1):
        lines = []
        for paragraph in title.split('\n'):
            line = ''
            for word in paragraph.split():
                candidate = (line + ' ' + word).strip()
                if line and draw.textlength(candidate, font=font(chosen, True)) > width:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        leading = round(chosen * 1.13)
        boxes = [draw.textbbox((x, y + i * leading), line,
                              font=font(chosen, True), anchor='la')
                 for i, line in enumerate(lines)]
        if max(box[3] for box in boxes) <= y + max_height:
            break
    else:
        raise ValueError(f'Title does not fit: {title}')
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=font(chosen, True),
                  fill=INK, anchor='la')
    return dict(size=chosen, lines=lines, boxes=boxes)


class Scene:
    def __init__(self, number, title, stage='', t=0, duration=42):
        self.im=Image.new('RGB',(W,H),BG)
        self.d=ImageDraw.Draw(self.im)
        self.text(70,163,'CONSTRAINED IMPROVISATION',25,MUTED,bold=True)
        self.text(70,217,f'{number:02d}  /  WAVES TO QUANTA',27,GOLD,bold=True)
        fitted_title(self.d, title)
        if stage: self.text(70,420,stage,31,MUTED)
        self.d.line((70,1676,950,1676),fill=GRID,width=3)
        self.d.line((70,1676,70+880*float(np.clip(t/duration,0,1)),1676),fill=GOLD,width=4)
        self.text(70,1717,'A series in 13 parts',25,MUTED)
        self.text(950,1717,f'{number:02d} / 13',25,MUTED,anchor='ra')

    def text(self,x,y,value,size=32,color=INK,bold=False,anchor='la'):
        self.d.text((x,y),str(value),font=font(size,bold),fill=color,anchor=anchor)

    def wrap(self,value,x,y,width,size=32,color=INK,bold=False,leading=None):
        leading=leading or int(size*1.32)
        yy=y
        for paragraph in str(value).split('\n'):
            words=paragraph.split(); line=''
            for word in words:
                proposed=(line+' '+word).strip()
                if self.d.textlength(proposed,font=font(size,bold))>width and line:
                    self.text(x,yy,line,size,color,bold); yy+=leading; line=word
                else: line=proposed
            self.text(x,yy,line,size,color,bold); yy+=leading
        return yy

    def math(self,tex,x=510,y=1510,size=44,color=INK,maxwidth=880):
        pic=equation(tex,size,color)
        if pic.width>maxwidth:
            pic=pic.resize((maxwidth,round(pic.height*maxwidth/pic.width)),Image.Resampling.LANCZOS)
        self.im.paste(pic,(round(x-pic.width/2),round(y-pic.height/2)),pic)

    def panel(self,box,label=None,color=MUTED):
        self.d.rounded_rectangle(tuple(box),radius=22,fill=PANEL,outline=GRID,width=2)
        if label:self.text(box[0]+24,box[1]+22,label,30,color)

    def line(self,points,color=BLUE,width=3):
        p=np.asarray(points,dtype=float)
        if len(p)>=2:self.d.line([tuple(a) for a in p],fill=color,width=int(width),joint='curve')

    def arrow(self,start,end,color=GOLD,width=5,head=16):
        a=np.array(start,dtype=float); b=np.array(end,dtype=float)
        self.line([a,b],color,width)
        u=b-a; n=np.linalg.norm(u)
        if n<1:return
        u/=n; v=np.array([-u[1],u[0]])
        p=[tuple(b),tuple(b-head*u+.48*head*v),tuple(b-head*u-.48*head*v)]
        self.d.polygon(p,fill=color)

    def dot(self,p,r=6,color=GOLD):
        self.d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=color)

    def note(self,value,y=1580,color=MUTED,size=30):
        self.wrap(value,70,y,880,size=size,color=color,leading=39)

def helix(scene, x, z, box, color=BLUE, envelope=True, gain=None, depth=.28):
    """Fixed oblique projection of (coordinate, Re psi, Im psi)."""
    x=np.asarray(x); z=np.asarray(z)
    l,top,r,b=box; cy=(top+b)/2
    if gain is None:gain=.38*(b-top)
    xx=l+(x-x.min())/(x.max()-x.min())*(r-l)
    scene.line([(l,cy),(r,cy)],GRID,2)
    if envelope:
        scene.line(np.c_[xx,cy-gain*abs(z)],GOLD,2)
        scene.line(np.c_[xx,cy+gain*abs(z)],GOLD,2)
    w=z*np.exp(-.38j)
    pts=np.c_[xx+depth*gain*w.imag,cy-gain*w.real]
    scene.line(pts,color,4)
    return pts

def phasor(scene,origin,z,scale=100,color=GOLD,width=5):
    end=(origin[0]+scale*z.real,origin[1]-scale*z.imag)
    scene.arrow(origin,end,color,width)
    return end

def spectrum_color(u):
    colors=np.array([[70,150,255],[36,211,216],[65,216,142],[248,204,77],[255,128,75],[255,66,105]])
    p=np.clip(u,0,1)*(len(colors)-1)
    lo=int(p); hi=min(lo+1,len(colors)-1)
    return tuple(np.rint(colors[lo]*(1-(p-lo))+colors[hi]*(p-lo)).astype(int))
