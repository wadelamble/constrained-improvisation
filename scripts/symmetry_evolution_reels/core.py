"""Portrait layout shared by the five state-and-evolution reels."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
sys.path.insert(0, str(ROOT / 'scripts'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties

W, H, FPS = 1080, 1920, 30
BG, PANEL, INK = '#080b14', '#111a2a', '#fff2e4'
MUTED, GRID = '#a5b2c8', '#334258'
BLUE, RED, GOLD = '#46beff', '#ff4269', '#ffb45e'
GREEN, PURPLE = '#36e099', '#b999ff'
TITLES = {
    1: 'Reversible evolution preserves information',
    2: 'Unitary evolution preserves overlap',
    3: 'Transforming an operator',
    4: 'Commuting operators',
    5: 'Information preservation and state-space geometry',
}

def ease(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)

@lru_cache(80)
def font(size, bold=False):
    name = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    path = Path('C:/Windows/Fonts') / name
    if not path.exists():
        from matplotlib import get_data_path
        path = Path(get_data_path()) / 'fonts/ttf' / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(path), round(size))

def text(draw, xy, string, size=30, fill=INK, anchor='lt', bold=False):
    draw.text(xy, str(string), font=font(size,bold), fill=fill, anchor=anchor)

@lru_cache(300)
def _equation(tex, size, fill):
    parsed = MathTextParser('agg').parse('$'+tex+'$', dpi=150,
        prop=FontProperties(size=size*72/150))
    alpha = Image.fromarray(np.asarray(parsed.image, dtype=np.uint8))
    im = Image.new('RGBA', alpha.size, fill)
    im.putalpha(alpha)
    return im

def math(image, tex, xy, size=40, fill=INK, anchor='mm', max_width=880):
    im = _equation(tex, size, fill)
    if im.width > max_width:
        im = im.resize((round(max_width),round(im.height*max_width/im.width)),Image.Resampling.LANCZOS)
    x,y=xy
    if anchor[0]=='m': x-=im.width/2
    elif anchor[0]=='r': x-=im.width
    if anchor[1]=='m': y-=im.height/2
    elif anchor[1] in ('b','s'): y-=im.height
    image.paste(im,(round(x),round(y)),im)
    return (x,y,x+im.width,y+im.height)

def wrap(draw,string,size,width,bold=False):
    lines=[]
    for paragraph in string.split('\n'):
        line=''
        for word in paragraph.split():
            candidate=(line+' '+word).strip()
            if line and draw.textlength(candidate,font=font(size,bold))>width:
                lines.append(line); line=word
            else: line=candidate
        lines.append(line)
    return lines

def frame(title,index,t,duration,stage=''):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    text(d,(70,164),'NATURE’S IMPROVISATION ON SYMMETRY',25,MUTED,bold=True)
    text(d,(70,214),f'STATE AND EVOLUTION  ·  {index}/5',27,GOLD,bold=True)
    size=55
    while True:
        lines=wrap(d,title,size,880,True)
        if len(lines)*(size+9)<=148 or size<=36: break
        size-=1
    for j,line in enumerate(lines): text(d,(70,269+j*(size+9)),line,size,INK,bold=True)
    if stage:
        lines=wrap(d,stage,29,880)
        for j,line in enumerate(lines): text(d,(70,430+j*35),line,29,MUTED)
    d.line((70,1676,950,1676),fill=GRID,width=2)
    d.line((70,1676,70+880*min(max(t/duration,0),1),1676),fill=GOLD,width=4)
    text(d,(70,1710),'SYMMETRY',23,MUTED)
    text(d,(950,1710),f'{t:04.1f} / {duration:g} s',23,MUTED,anchor='rt')
    return im,d
