"""A sparse picture of a vector-valued function under active planar rotation.

Both plotted coordinates are inputs. Arrows, not vertical coordinates, are
outputs. Nine samples are transported with the function on fixed axes:
q = R p, F_theta(q) = R F(p), hence F_theta(x) = R F(R^-1 x).
The smooth function is defined over the entire plane; its sampled lattice
is only a display choice. Its directional bias makes rotation visible.
Playback advances a transformation parameter, not physical time evolution.
No manuscript is edited. Run with --check --preview --render --encoded-check.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / '.tools' / 'animation-python-packages'
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties

OUT = ROOT / 'content' / 'drafts' / 'animations'
NAME = 'symmetry-function-arrows'
W, H, SS, FPS, DURATION = 1440, 900, 2, 30, 12
N = FPS * DURATION
BG = (253, 250, 244)
INK, MUTED = (37, 38, 40), (111, 108, 101)
GRID, AXIS = (235, 229, 219), (176, 171, 161)
BLUE, GOLD = (43, 93, 145), (181, 118, 22)
CENTER, SCALE = np.array([485., 484.]), 155.
POINTS = np.array([(x,y) for y in (-1.,0.,1.) for x in (-1.,0.,1.)])
P = np.array([1., 1.])
SAMPLE_TIMES = (.0, 3.8, 5.8, 7.3, 9.2, 11.9)


@lru_cache(None)
def font(size, bold=False):
    for name in ('seguisb.ttf' if bold else 'segoeui.ttf',
                 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, round(size*SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(float(v)*SS) for v in values)


def text(d, pos, value, size=22, color=INK, bold=False, anchor=None):
    d.text(px(pos), value, font=font(size,bold), fill=color, anchor=anchor)


def line(d, a, b, color, width=1):
    d.line(px((*a,*b)), fill=color, width=max(1,round(width*SS)))


def arrow(d, a, b, color, width=4, head=14):
    a, b = np.asarray(a), np.asarray(b)
    v = b-a
    length = float(np.linalg.norm(v))
    if length < 1:
        return
    u = v/length
    side = np.array([-u[1],u[0]])
    head = min(head, .35*length)
    line(d, a, b-head*.3*u, color, width)
    d.polygon([px(b),px(b-head*u+.43*head*side),px(b-head*u-.43*head*side)],fill=color)


def dot(d, q, radius, color):
    q=np.asarray(q)
    d.ellipse(px((* (q-radius), * (q+radius))),fill=color)


@lru_cache(None)
def formula(value, size=24, color=INK):
    stream=BytesIO()
    math_to_image('$'+value+'$',stream,dpi=144,
                  prop=FontProperties(size=size),format='png',
                  color=tuple(c/255 for c in color))
    rgba=np.asarray(Image.open(stream).convert('RGBA')).copy()
    # Recover the text's antialiasing from matplotlib's white canvas.
    alpha=(255-np.min(rgba[:,:,:3],axis=2)).astype(float)
    rgba[:,:,3]=np.minimum(255,np.round(alpha*255/(255-min(color)))).astype(np.uint8)
    rgba[:,:,:3]=color
    art=Image.fromarray(rgba)
    return art.crop(art.getbbox())


def put_math(im,pos,value,size=24,color=INK):
    art=formula(value,size,color)
    im.paste(art,px(pos),art)
    return art.width/SS,art.height/SS


def rotation(theta):
    c,s=math.cos(theta),math.sin(theta)
    return np.array([[c,-s],[s,c]])


def field(q):
    q=np.asarray(q)
    return np.stack((.55-.15*q[...,1], .2+.18*q[...,0]),axis=-1)


def transformed(q,theta):
    r=rotation(theta)
    return field(np.asarray(q)@r)@r.T


def angle(t):
    # One smooth full turn, with short initial/final holds.
    u=float(np.clip((t-.8)/10.,0,1))
    return 2*math.pi*u*u*(3-2*u)


def screen(q):
    return CENTER+np.asarray(q)*np.array([SCALE,-SCALE])


def pair(v):
    v=np.where(np.abs(v)<.005,0,v)
    return ('('+', '.join(f'{x:.2f}' for x in v)+')').replace('-','−')


@lru_cache(None)
def backdrop():
    im=Image.new('RGB',(W*SS,H*SS),BG)
    d=ImageDraw.Draw(im,'RGBA')
    text(d,(48,29),'Turning a function',34,bold=True)
    text(d,(49,83),'Each position is an input. Each arrow is an output.',23,MUTED)
    # Coordinates stay fixed while sample locations and values turn.
    for tick in (-2,-1,0,1,2):
        for dim in (0,1):
            a,b=np.zeros(2),np.zeros(2)
            a[dim]=b[dim]=tick
            a[1-dim],b[1-dim]=-2.12,2.12
            line(d,screen(a),screen(b),GRID,1)
    for dim in (0,1):
        a,b=np.zeros(2),np.zeros(2)
        a[dim],b[dim]=-2.10,2.22
        arrow(d,screen(a),screen(b),AXIS,1.35,8)
    # Keep tick numerals outside the rotating geometry, including their
    # minus signs. The interior axes alone indicate the zero lines.
    for tick in (-2,-1,0,1,2):
        text(d,screen((tick,-2.12))+[0,7],str(tick).replace('-','−'),16,MUTED,anchor='mt')
        text(d,screen((-2.12,tick))+[-15,0],str(tick).replace('-','−'),16,MUTED,anchor='rm')
    put_math(im,screen((2.28,0))+[0,-13],'x',24,MUTED)
    put_math(im,screen((0,2.22))+[13,-10],'y',24,MUTED)
    line(d,(924,196),(924,748),GRID,1)
    text(d,(982,214),'Highlighted input',24,bold=True)
    put_math(im,(984,260),r'\mathbf{p}_\theta=R_\theta\mathbf{p}',25)
    text(d,(982,390),'Its output arrow',24,bold=True)
    put_math(im,(984,436),r'\mathbf{f}_\theta(\mathbf{p}_\theta)',26)
    text(d,(982,596),'The position moves.',23)
    text(d,(982,634),'The arrow turns.',23)
    put_math(im,(983,710),r'\mathbf{f}_\theta(R_\theta\mathbf{p})=R_\theta\mathbf{f}(\mathbf{p})',22)
    text(d,(48,852),'A function assigning a vector to each point in a plane',18,MUTED)
    return im


def frame(t):
    theta=angle(t)
    r=rotation(theta)
    q=POINTS@r.T
    v=field(POINTS)@r.T
    im=backdrop().copy()
    d=ImageDraw.Draw(im,'RGBA')
    text(d,(1388,35),f'θ = {math.degrees(theta):.0f}°',30,GOLD,anchor='ra')
    marked=r@P
    # Coordinate projections emphasize that BOTH axes specify the input.
    guide=(*GOLD,70)
    for a,b in (([marked[0],0],marked),([0,marked[1]],marked)):
        a,b=screen(a),screen(b)
        length=np.linalg.norm(b-a)
        for start in np.arange(0,length,11):
            if length:
                line(d,a+(b-a)*start/length,a+(b-a)*min(start+5,length)/length,guide,1.25)
    for point,value in zip(q,v):
        if np.linalg.norm(point-marked)<1e-8:
            continue
        tail,tip=screen(point),screen(point+value)
        arrow(d,tail,tip,BG,8,18)
        arrow(d,tail,tip,BLUE,4,14)
        dot(d,tail,4.5,BLUE)
    value=r@field(P)
    tail,tip=screen(marked),screen(marked+value)
    arrow(d,tail,tip,BG,11,22)
    arrow(d,tail,tip,GOLD,5.4,18)
    dot(d,tail,7,BG)
    dot(d,tail,5.3,GOLD)
    text(d,(984,313),pair(marked),33,GOLD,bold=True)
    text(d,(984,490),pair(value),33,GOLD,bold=True)
    return im.resize((W,H),Image.Resampling.LANCZOS)


def check():
    rng=np.random.default_rng(6121)
    pts=rng.uniform(-2,2,(200,2))
    error=norm_error=composition_error=0.
    margin=math.inf
    for theta in np.linspace(0,2*math.pi,181):
        r=rotation(theta)
        vals=transformed(pts@r.T,theta)
        error=max(error,float(np.max(abs(vals-field(pts)@r.T))))
        norm_error=max(norm_error,float(np.max(abs(np.linalg.norm(vals,axis=1)-np.linalg.norm(field(pts),axis=1)))))
        phi=.73
        twice=transformed(pts@rotation(phi),theta)@rotation(phi).T
        composition_error=max(composition_error,float(np.max(abs(twice-transformed(pts,theta+phi)))))
        bases,tips=screen(POINTS@r.T),screen((POINTS+field(POINTS))@r.T)
        geometry=np.vstack((bases,tips))
        bounds=np.column_stack((geometry[:,0]-75,880-geometry[:,0],geometry[:,1]-145,815-geometry[:,1]))
        margin=min(margin,float(bounds.min()))
    assert max(error,norm_error,composition_error)<1e-13
    assert margin>25
    assert np.max(abs(transformed(pts,2*math.pi)-field(pts)))<1e-14
    # The sample at the origin stays put, but its output rotates.
    assert np.max(abs(transformed(np.zeros(2),math.pi/2)-rotation(math.pi/2)@field(np.zeros(2))))<1e-14
    assert max(put_width for put_width in [formula(r'\mathbf{f}_\theta(R_\theta\mathbf{p})=R_\theta\mathbf{f}(\mathbf{p})',22).width/SS])<405
    report={'rule':'f_theta(x)=R_theta f(R_theta^-1 x)',
            'base_field':'f(x,y)=(0.55-0.15*y, 0.20+0.18*x)',
            'sample_count':len(POINTS),'sample_correspondence_error':error,
            'norm_error':norm_error,'composition_error':composition_error,
            'minimum_geometry_margin_px':margin,'size':[W,H],'fps':FPS,'duration':DURATION,
            'note':'Both plot axes are inputs. Moving samples display a function defined on all of R^2. Rotation parameter is not physical time.'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1440,1380),BG)
    for i,t in enumerate(SAMPLE_TIMES):
        pic=frame(t)
        x,y=(i%2)*720,(i//2)*460
        sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),(x,y))
    frame(3.8).save(OUT/f'{NAME}-poster.png')
    sheet.save(OUT/f'{NAME}-contact-sheet.png')
    print(str(OUT/f'{NAME}-contact-sheet.png'),flush=True)


def render():
    path=OUT/f'{NAME}.mp4'
    proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error',
        '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
        '-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        last_angle,raw=None,None
        for i in range(N):
            theta=angle(i/FPS)
            if theta!=last_angle:
                raw=frame(i/FPS).tobytes()
                last_angle=theta
            proc.stdin.write(raw)
            if i%(FPS*3)==0:
                print(f'Rendered {i/FPS:g}/{DURATION} seconds',flush=True)
        proc.stdin.close()
        err=proc.stderr.read().decode(errors='replace')
        if proc.wait():
            raise RuntimeError(err)
    except BaseException:
        proc.kill();proc.wait();raise
    print(str(path),flush=True)


def encoded_check():
    reader=imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'),pix_fmt='rgb24')
    meta=next(reader)
    assert tuple(meta['size'])==(W,H) and meta['fps']==FPS
    indices={min(N-1,round(t*FPS)) for t in SAMPLE_TIMES}
    sheet=Image.new('RGB',(1440,1350),BG)
    errors=[]
    count=0
    for i,raw in enumerate(reader):
        count+=1
        if i in indices:
            decoded=np.frombuffer(raw,dtype=np.uint8).reshape(H,W,3)
            error=float(np.mean(abs(decoded.astype(float)-np.asarray(frame(i/FPS)).astype(float))))
            assert error<2
            n=len(errors)
            sheet.paste(Image.fromarray(decoded).resize((720,450),Image.Resampling.LANCZOS),((n%2)*720,(n//2)*450))
            errors.append(error)
    assert count==N and len(errors)==len(indices)
    sheet.save(OUT/f'{NAME}-encoded-contact-sheet.png')
    report={'decoded_frames':count,'duration':count/FPS,'size':meta['size'],
            'fps':meta['fps'],'max_decoded_rgb_error':max(errors)}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for flag in ('check','preview','render','encoded-check'):
        parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    if args.check:check()
    if args.preview:preview()
    if args.render:render()
    if args.encoded_check:encoded_check()
