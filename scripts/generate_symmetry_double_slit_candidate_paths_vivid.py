"""Two candidate contributions, refreshed in the vivid signed-wave idiom.

An ideal monochromatic source A replaces the old plane-wave/first-screen
apparatus. A, C, D, B retain the original geometry. Lambda now matches the
preceding animation's initial wavelength; its matching phasor still is updated
separately. This keeps the original phase-only two-point-aperture
model and its illustrative common amplitude falloff. It is not a finite-slit
boundary-value solution or a calibrated irradiance picture. Only route guides
are revealed over time; the physical two-contribution field is always summed.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import time

import generate_symmetry_widening_apertures as style

np,Image,ImageDraw=style.np,style.Image,style.ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content'/'drafts'/'animations'
NAME='symmetry-double-slit-candidate-paths-shortwave-arcs'
WIDTH,HEIGHT=1440,810
BOX=(60,100,1380,712)
PW,PH=BOX[2]-BOX[0],BOX[3]-BOX[1]
XMIN,XMAX,YMIN,YMAX=-5.,6.,-2.55,2.55
A=(-3.2,0.)
C=(0.,1.)
D=(0.,-1.)
B=(5.2,.55)
WAVELENGTH=.5
K=2*np.pi/WAVELENGTH
AC,AD,CB,DB=(math.dist(*pair) for pair in ((A,C),(A,D),(C,B),(D,B)))
BG,INK,MUTED=style.BG,style.INK,style.MUTED
VIA_C=(125,220,255)
VIA_D=(255,214,144)
FPS,DURATION,PERIOD=30,10.,1.6
FRAMES=round(FPS*DURATION)
SAMPLES=(.6,2.5,3.7,4.5,6.3,8.8)
DISPLAY_LIMIT=1.35
font=style.font


def xy(point):
    x,y=point
    return (BOX[0]+(x-XMIN)/(XMAX-XMIN)*PW,
            BOX[1]+(YMAX-y)/(YMAX-YMIN)*PH)


class Scene:
    def __init__(self):
        self.x,self.y=np.meshgrid(np.linspace(XMIN,XMAX,PW),np.linspace(YMAX,YMIN,PH))
        ra=np.hypot(self.x-A[0],self.y-A[1])
        rc=np.hypot(self.x-C[0],self.y-C[1])
        rd=np.hypot(self.x-D[0],self.y-D[1])
        incident=.72*np.exp(1j*K*ra)/np.sqrt(.70+.45*ra)
        common=.82/np.sqrt(.34+.5*(rc+rd))
        self.c=common*np.exp(1j*K*(AC+rc))
        self.d=common*np.exp(1j*K*(AD+rd))
        self.field=np.where(self.x<=0,incident,self.c+self.d).astype(np.complex64)


def label(draw,position,text,color=INK,anchor='mm',size=26):
    draw.text(position,text,font=font(size,True),fill=color,anchor=anchor,
              stroke_width=4,stroke_fill=BG)


def dashed_segment(draw,start,end,color,opacity):
    p,q=np.array(start),np.array(end)
    length=float(np.linalg.norm(q-p))
    direction=(q-p)/length
    for begin in np.arange(0,length,20.):
        a=p+direction*begin
        b=p+direction*min(begin+12,length)
        draw.line((*a,*b),fill=(*BG,round(230*opacity)),width=8)
        draw.line((*a,*b),fill=(*color,round(255*opacity)),width=3)


def point(draw,position,color,radius=5):
    x,y=position
    draw.ellipse((x-radius-3,y-radius-3,x+radius+3,y+radius+3),fill=BG)
    draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=color)


def front_radii(seconds,source,incoming_length):
    # k*(incoming_length+r)-omega*t = 2*pi*n: positive-phase fronts of
    # each individual spherical component, not fronts of their summed field.
    phase=2*np.pi*seconds/PERIOD
    offset=((phase-K*incoming_length)%(2*np.pi))/K
    xlo,xhi=(XMIN,0.) if source==A else (0.,XMAX)
    farthest=max(math.dist(source,(x,y)) for x in (xlo,xhi) for y in (YMIN,YMAX))
    return [float(r) for r in np.arange(offset,farthest+WAVELENGTH,WAVELENGTH)
            if .025<r<=farthest]


def draw_component_fronts(picture,seconds):
    # Supersampling keeps thin arcs smooth without adding a glow or changing
    # the field's amplitude/color mapping. C and D use their route colors.
    scale=2
    layer=Image.new('RGBA',(WIDTH*scale,HEIGHT*scale),(0,0,0,0))
    draw=ImageDraw.Draw(layer,'RGBA')
    for source,incoming,color,alpha in ((A,0.,INK,110),(C,AC,VIA_C,175),(D,AD,VIA_D,175)):
        angles=np.linspace(0,2*np.pi,1001) if source==A else np.linspace(-np.pi/2,np.pi/2,801)
        for radius in front_radii(seconds,source,incoming):
            xx=source[0]+radius*np.cos(angles)
            yy=source[1]+radius*np.sin(angles)
            visible=(xx>=XMIN)&(xx<=XMAX)&(yy>=YMIN)&(yy<=YMAX)
            visible&=(xx<=0.) if source==A else (xx>=0.)
            points=[]
            for x,y,show in zip(xx,yy,visible):
                if show:
                    px,py=xy((x,y))
                    points.append((px*scale,py*scale))
                else:
                    if len(points)>1: draw.line(points,fill=(*color,alpha),width=3)
                    points=[]
            if len(points)>1: draw.line(points,fill=(*color,alpha),width=3)
    layer=layer.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
    return Image.alpha_composite(picture.convert('RGBA'),layer).convert('RGB')


def frame(seconds,scene):
    phase=2*np.pi*seconds/PERIOD
    real=scene.field.real*np.cos(phase)+scene.field.imag*np.sin(phase)
    indices=np.rint((np.clip(real/DISPLAY_LIMIT,-1,1)+1)*4096).astype(np.int32)
    picture=Image.new('RGB',(WIDTH,HEIGHT),BG)
    picture.paste(Image.fromarray(style.color_table()[indices]),BOX[:2])
    picture=draw_component_fronts(picture,seconds)
    draw=ImageDraw.Draw(picture,'RGBA')

    # Narrow openings are clear gaps rather than being plugged by point marks.
    half_gap=.15
    sx=xy(C)[0]
    for low,high in ((YMIN,D[1]-half_gap),(D[1]+half_gap,C[1]-half_gap),(C[1]+half_gap,YMAX)):
        draw.line((sx,xy((0,low))[1],sx,xy((0,high))[1]),fill=INK,width=6)

    # These fades reveal guides only. Both aperture fields remain present.
    c_alpha=style.ease((seconds-1.6)/.8)
    d_alpha=style.ease((seconds-3.8)/.8)
    for mid,color,alpha in ((C,VIA_C,c_alpha),(D,VIA_D,d_alpha)):
        if alpha:
            dashed_segment(draw,xy(A),xy(mid),color,alpha)
            dashed_segment(draw,xy(mid),xy(B),color,alpha)
    for p,color in ((A,INK),(C,VIA_C),(D,VIA_D),(B,INK)):
        point(draw,xy(p),color)
    offsets=((A,'A',(-23,-24),INK),(C,'C',(25,-30),VIA_C),
             (D,'D',(25,30),VIA_D),(B,'B',(27,-2),INK))
    for p,name,(dx,dy),color in offsets:
        x,y=xy(p)
        label(draw,(x+dx,y+dy),name,color)

    draw.text((60,27),'Two contributions at B',font=font(32,True),fill=INK)
    draw.text((1380,31),'Point source · two narrow openings',font=font(22),fill=MUTED,anchor='ra')
    draw.text((60,752),'Real part of the wave',font=font(20),fill=MUTED)
    for x,sign,color in ((279,'−',style.NEGATIVE),(315,'0',MUTED),(352,'+',style.POSITIVE)):
        draw.text((x,752),sign,font=font(21),fill=color)
    for x,name,color,alpha in ((1060,'ACB',VIA_C,c_alpha),(1260,'ADB',VIA_D,d_alpha)):
        draw.line((x-62,766,x-22,766),fill=(*color,round(255*alpha)),width=3)
        draw.text((x,752),name,font=font(22,True),fill=(*color,round(255*alpha)))
    return picture


def previews(scene):
    sheet=Image.new('RGB',(1440,3*435),BG)
    for j,seconds in enumerate(SAMPLES):
        pic=frame(seconds,scene)
        pic.save(OUT/f'{NAME}-check-{seconds:g}.png')
        x,y=j%2*720,j//2*435
        sheet.paste(pic.resize((720,405),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+30,y+410),f'{seconds:g} s',font=font(17),fill=MUTED)
    sheet.save(OUT/f'{NAME}-contact-sheet.png')
    frame(8.8,scene).save(OUT/f'{NAME}-poster.png')


def validate(scene):
    # Preserve the original path geometry; the user-requested shorter
    # wavelength changes the relative phase, which the matching still shares.
    delta=K*((AD+DB)-(AC+CB))
    assert abs(((AD+DB)-(AC+CB))-.20665952436062707)<1e-12
    assert abs(PW/(XMAX-XMIN)-PH/(YMAX-YMIN))<1e-10
    errors=[]
    for phase in (0.,.63,2.9):
        rc=np.hypot(scene.x-C[0],scene.y-C[1])
        rd=np.hypot(scene.x-D[0],scene.y-D[1])
        expected=.82*(np.cos(K*(AC+rc)-phase)+np.cos(K*(AD+rd)-phase))/np.sqrt(.34+.5*(rc+rd))
        actual=((scene.c+scene.d)*np.exp(-1j*phase)).real
        errors.append(float(np.max(abs(expected-actual))))
    assert max(errors)<1e-12,errors
    front_errors=[]
    for seconds in SAMPLES:
        for source,incoming in ((A,0.),(C,AC),(D,AD)):
            for radius in front_radii(seconds,source,incoming):
                phase=K*(incoming+radius)-2*np.pi*seconds/PERIOD
                front_errors.append(abs(np.exp(1j*phase)-1))
    assert max(front_errors)<1e-12,front_errors
    report={'A':A,'C':C,'D':D,'B':B,'wavelength':WAVELENGTH,
            'path_lengths':[AC+CB,AD+DB],'relative_phase_at_B':delta,
            'signed_sum_max_error':max(errors),'phase_step_per_frame':2*np.pi/(PERIOD*FPS),
            'display_limit':DISPLAY_LIMIT,'component_front_max_phase_error':float(max(front_errors)),
            'model':'original phase-only two-point-aperture illustration',
            'size':[WIDTH,HEIGHT],'fps':FPS,'duration':DURATION}
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


def render(scene):
    temporary=OUT/f'{NAME}-rendering.mp4'
    cmd=[style.imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
         '-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(temporary)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start=time.perf_counter()
    try:
        for i in range(FRAMES):
            p.stdin.write(frame(i/FPS,scene).tobytes())
            if i%(FPS*2)==0: print(f'{i/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-start:.1f}s',flush=True)
        p.stdin.close()
        error=p.stderr.read().decode(errors='replace')
        if p.wait(): raise RuntimeError(error)
    except BaseException:
        p.kill()
        p.wait()
        raise
    temporary.replace(OUT/f'{NAME}.mp4')


def encoded_check(scene):
    reader=style.imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'),pix_fmt='rgb24')
    meta=next(reader)
    selected={round(t*FPS) for t in SAMPLES}
    sheet=Image.new('RGB',(1440,1215),BG)
    errors=[]
    for i,data in enumerate(reader):
        if i not in selected: continue
        decoded=np.frombuffer(data,np.uint8).reshape(HEIGHT,WIDTH,3)
        errors.append(float(np.mean(abs(decoded.astype(float)-np.asarray(frame(i/FPS,scene)).astype(float)))))
        j=len(errors)-1
        pic=Image.fromarray(decoded.copy())
        sheet.paste(pic.resize((720,405),Image.Resampling.LANCZOS),(j%2*720,j//2*405))
        if j==len(SAMPLES)-1: pic.save(OUT/f'{NAME}-encoded-final.png')
    assert i+1==FRAMES and len(errors)==len(SAMPLES)
    assert tuple(meta['size'])==(WIDTH,HEIGHT) and meta['fps']==FPS
    sheet.save(OUT/f'{NAME}-encoded-contact-sheet.png')
    report={'decoded_frames':i+1,'size':meta['size'],'fps':FPS,'duration':(i+1)/FPS,'mean_rgb_errors':errors}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    assert max(errors)<3.,report
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for flag in ('check','preview','render','encoded-check'):
        parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    scene=Scene()
    if args.check: validate(scene)
    if args.preview: previews(scene)
    if args.render: render(scene)
    if args.encoded_check: encoded_check(scene)
