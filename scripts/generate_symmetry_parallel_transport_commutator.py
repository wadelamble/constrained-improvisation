"""An explicit parallel-transport commutator on a spherical coordinate patch.

Review-only asset. A gnomonic chart makes each coordinate segment a great
circle arc. Both orders have exactly the same destination. Forward transport
on vector fields has generators D_i=-nabla_i; Tx Ty means y then x.
The inset uses a true orthonormal tangent frame at the common destination,
and its green vector is exactly (copper arrow) minus (blue arrow).
The infinitesimal relation is labeled as a small-step approximation; the
finite paths shown are never claimed to satisfy it exactly.
"""
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
from parallel_transport_geometry import unit, slerp, transport_leg, arc_angle, signed_tangent_angle

NAME = 'symmetry-parallel-transport-commutator'
OUT = ROOT/'content/drafts/animations'
REVIEW = ROOT/'.tools/parallel-transport-commutator-review'
W,H,S,FPS,DURATION = 1600,900,2,24,34.
BG,INK,MUTED = '#fffcf6','#263139','#76817e'
GRID,FAINT,SURFACE = '#bec6c0','#e6e9e2','#f4f2e9'
BLUE,COPPER,GREEN = '#326fa7','#b46239','#328573'
ORIGIN,RADIUS = np.array([400.,535.]),255.
N,E1,E2 = np.array([0.,0.,1.]),np.array([1.,0.,0.]),np.array([0.,1.,0.])
DEPTH = unit([.45,.45,1.])
RIGHT = unit(np.cross(E2,DEPTH))
UP = np.cross(DEPTH,RIGHT)
CAMERA = np.array([RIGHT,-UP])
A,B = 1.1,1.1
V0 = E1.copy()
MOMENTS = [0.,2.5,4.5,7.,9.,11.5,13.5,16.,19.,22.,24.,27.,30.,33.5]


def ease(u):
    u=float(np.clip(u,0.,1.))
    return u*u*u*(10.+u*(-15.+6.*u))


def fade(t,a,b):
    return ease((t-a)/(b-a))


def rgb(value):
    return tuple(int(value[i:i+2],16) for i in (1,3,5))


def color(value,alpha=1.):
    return tuple(round(x+(y-x)*alpha) for x,y in zip(rgb(BG),rgb(value)))


@lru_cache(60)
def font(size,bold=False):
    choices=[Path('C:/Windows/Fonts')/('seguisb.ttf' if bold else 'segoeui.ttf'),
             Path(matplotlib.get_data_path())/'fonts/ttf'/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in choices:
        if p.exists():
            return ImageFont.truetype(str(p),round(size*S))
    raise FileNotFoundError('No suitable font')


@lru_cache(80)
def equation(tex,size=37,tint=INK):
    tex=tex.replace(r'\mathbf v',r'\mathbf{v}').replace(r'\hat D',r'\hat{D}')
    stream=BytesIO()
    with matplotlib.rc_context({'savefig.transparent':True,'mathtext.fontset':'stix'}):
        math_to_image('$'+tex+'$',stream,format='png',dpi=180,color=tint,
            prop=matplotlib.font_manager.FontProperties(size=size*S*72/180))
    stream.seek(0)
    return Image.open(stream).convert('RGBA')


class Canvas:
    def __init__(self,base=None):
        self.im=base.copy() if base is not None else Image.new('RGB',(W*S,H*S),BG)
        self.d=ImageDraw.Draw(self.im)
        self.boxes=[]

    def track(self,box,label):
        assert box[0]>=24 and box[1]>=24 and box[2]<=W-24 and box[3]<=H-24,(label,box)
        for other,name in self.boxes:
            dx=min(box[2],other[2])-max(box[0],other[0])
            dy=min(box[3],other[3])-max(box[1],other[1])
            assert dx<=0 or dy<=0,(label,name)
        self.boxes.append((box,label))

    def text(self,xy,label,size=25,tint=INK,bold=False,alpha=1.,center=False,backing=False):
        if alpha<.002:return
        x,y=np.array(xy)*S
        f=font(size,bold)
        if center:x-=self.d.textlength(label,font=f)/2
        box=self.d.textbbox((x,y),label,font=f,anchor='lt')
        self.track(tuple(v/S for v in box),label)
        if backing:self.d.rectangle((box[0]-4*S,box[1]-3*S,box[2]+4*S,box[3]+3*S),fill=BG)
        self.d.text((x,y),label,font=f,anchor='lt',fill=color(tint,alpha))

    def math(self,xy,tex,size=37,tint=INK,alpha=1.,center=False):
        if alpha<.002:return (0,0)
        im=equation(tex,size,tint)
        if alpha<.999:
            im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:round(v*alpha)))
        x,y=np.array(xy)*S
        if center:x-=im.width/2
        y-=im.height/2
        box=(x/S,y/S,(x+im.width)/S,(y+im.height)/S)
        self.track(box,tex)
        self.im.paste(im,(round(x),round(y)),im)
        return im.width/S,im.height/S

    def line(self,pts,tint=GRID,width=1.,alpha=1.):
        if alpha<.002 or len(pts)<2:return
        self.d.line([tuple(np.array(p)*S) for p in pts],fill=color(tint,alpha),width=max(1,round(width*S)),joint='curve')

    def dot(self,p,r=4.,tint=INK,alpha=1.):
        x,y=np.array(p)*S
        self.d.ellipse((x-r*S,y-r*S,x+r*S,y+r*S),fill=color(tint,alpha))

    def arrow(self,p,q,tint=BLUE,width=4.,alpha=1.,head=13.):
        p,q=np.array(p),np.array(q)
        delta=q-p;length=np.linalg.norm(delta)
        if length<.1 or alpha<.002:return
        u=delta/length;n=np.array([-u[1],u[0]])
        head=min(head,length*.32)
        self.line([p,q-.65*head*u],tint,width,alpha)
        self.d.polygon([tuple(v*S) for v in (q,q-head*u+.35*head*n,q-head*u-.35*head*n)],fill=color(tint,alpha))

    def finish(self):
        return self.im.resize((W,H),Image.Resampling.LANCZOS)


def point(x,y):
    return unit(N+x*E1+y*E2)


def routes(a=A,b=B):
    start,end=point(0,0),point(a,b)
    return np.array([start,point(a,0),end]),np.array([start,point(0,b),end])


BLUE_ROUTE,COPPER_ROUTE=routes()


def transport(route,leg_parameter):
    p=float(np.clip(leg_parameter,0.,2.))
    if p<=1.:
        return transport_leg(route[0],route[1],V0,p)
    _,v=transport_leg(route[0],route[1],V0,1.)
    return transport_leg(route[1],route[2],v,p-1.)


END,V_BLUE=transport(BLUE_ROUTE,2.)
_,V_COPPER=transport(COPPER_ROUTE,2.)
INSET_E1=V_BLUE
INSET_E2=np.cross(END,INSET_E1)
DELTA=V_COPPER-V_BLUE


def project(p):
    return ORIGIN+RADIUS*(np.asarray(p)@CAMERA.T)


def route_curve(route,leg_parameter=2.):
    pts=[route[0]]
    for i in range(2):
        u=float(np.clip(leg_parameter-i,0.,1.))
        if u>0:
            pts.extend(slerp(route[i],route[i+1],np.linspace(0,u,max(2,round(100*u)))))
    return np.array(pts)


def stage(t):
    if t<3.:return 'intro',0.,0.
    if t<7.:return 'blue-x',fade(t,3.,6.7),0.
    if t<12.5:return 'blue-y',1.+fade(t,7.,10.7),0.
    if t<14.:return 'reset',2.,0.
    if t<18.:return 'copper-y',2.,fade(t,14.,17.7)
    if t<22.5:return 'copper-x',2.,1.+fade(t,18.,21.7)
    return 'compare',2.,2.


def sphere_curve(c,pts):
    pts=np.array(pts)
    front=pts@DEPTH>=0
    pp=project(pts)
    start=0
    for i in range(1,len(pts)):
        if front[i]!=front[i-1]:
            c.line(pp[start:i+1],GRID if front[i-1] else FAINT,.85)
            start=i
    c.line(pp[start:],GRID if front[-1] else FAINT,.85)


@lru_cache(1)
def base():
    c=Canvas()
    c.text((65,42),'Parallel transport, in two orders',42,bold=True)
    c.text((65,108),'Transport along x by a, or along y by b.',24,MUTED)
    parts=[(r'[T_x(a),T_y(b)]\mathbf v',INK),(r'=',INK),
           (r'T_x(a)T_y(b)\mathbf v',COPPER),(r'-',INK),(r'T_y(b)T_x(a)\mathbf v',BLUE)]
    widths=[equation(tex,40,tint).width/S for tex,tint in parts]
    total=sum(widths)+4*25
    x=(W-total)/2
    for i,((tex,tint),width) in enumerate(zip(parts,widths)):
        c.math((x,180),tex,40,tint)
        if i in (2,4):
            c.text((x+width/2,211),'y, then x' if i==2 else 'x, then y',21,tint,center=True)
        x+=width+25
    c.line([(65,252),(1535,252)],FAINT,1.)
    x,y=ORIGIN*S;r=RADIUS*S
    c.d.ellipse((x-r,y-r,x+r,y+r),fill=SURFACE,outline=GRID,width=2)
    angles=np.linspace(0,2*math.pi,601)
    for lat in (-math.pi/3,-math.pi/6,0,math.pi/6,math.pi/3):
        rr,z=math.cos(lat),math.sin(lat)
        sphere_curve(c,np.column_stack([rr*np.cos(angles),rr*np.sin(angles),np.full(len(angles),z)]))
    for lon in np.linspace(0,math.pi,7,endpoint=False):
        sphere_curve(c,np.column_stack([np.cos(angles)*math.cos(lon),np.cos(angles)*math.sin(lon),np.sin(angles)]))
    c.line(project(route_curve(BLUE_ROUTE)),GRID,1.8)
    c.line(project(route_curve(COPPER_ROUTE)),GRID,1.8)
    c.dot(project(N),5.,INK)
    c.dot(project(END),5.,INK)
    c.text(project(N)+[-30,22],'A',24,INK,bold=True,backing=True)
    c.text(project(END)+[17,-33],'B',24,INK,bold=True,backing=True)
    c.text(project(point(.53*A,0))+[0,23],'x: a',21,MUTED,center=True,backing=True)
    c.text(project(point(0,.53*B))+[-44,0],'y: b',21,MUTED,backing=True)
    return c.im


def final_comparison(c,t):
    a=fade(t,22.5,23.5)
    if a<.002:return
    c.text((955,307),'At the same endpoint B',29,INK,bold=True,alpha=a)
    c.text((955,355),'A view within the tangent plane',23,MUTED,alpha=a)
    origin=np.array([990.,475.]);length=215.
    def tangent(v):
        return origin+length*np.array([np.dot(v,INSET_E1),-np.dot(v,INSET_E2)])
    blue,copper=tangent(V_BLUE),tangent(V_COPPER)
    c.arrow(origin,blue,BLUE,5.,a,17)
    c.arrow(origin,copper,COPPER,5.,a,17)
    c.dot(origin,5.,INK,a)
    c.text(origin+[-25,-37],'B',23,INK,bold=True,alpha=a)
    c.text(blue+[18,-26],'x, then y',22,BLUE,alpha=a)
    c.text(copper+[15,14],'y, then x',22,COPPER,alpha=a)
    d=fade(t,24.,25.2)
    # Exact tip-to-tip subtraction, not an angular arc substituted for a vector.
    c.arrow(blue,blue+d*(copper-blue),GREEN,4.5,d,14)
    c.math((1260,560),r'\Delta\mathbf v',37,GREEN,alpha=d)
    c.text((955,685),'The commutator gives their difference.',25,INK,alpha=fade(t,25.4,26.3))
    c.math((955,742),r'\Delta\mathbf v=[T_x(a),T_y(b)]\mathbf v',34,INK,alpha=fade(t,25.4,26.3))
    # The fine leader connects the sphere's common endpoint to the tangent view.
    start=project(END)+[15,15];end=origin+[-30,-20]
    u=np.linspace(0,1,35)
    for i in range(0,len(u)-1,2):
        c.line([start+(end-start)*u[i],start+(end-start)*u[i+1]],MUTED,1.,a*.55)


def render(t):
    c=Canvas(base())
    which,blue_p,copper_p=stage(t)
    if blue_p>0:c.line(project(route_curve(BLUE_ROUTE,blue_p)),BLUE,3.2)
    if copper_p>0:c.line(project(route_curve(COPPER_ROUTE,copper_p)),COPPER,3.2)
    # Initial gray reference is fixed at A throughout the two trials.
    c.arrow(project(N),project(N+.28*V0),MUTED,2.3,.65,12)
    if which=='intro':
        c.arrow(project(N),project(N+.28*V0),INK,4.,1.,14)
        c.text((930,330),'One arrow. Two routes.',31,INK,bold=True)
        c.text((930,390),'Both routes lead from A to B.',25,MUTED)
    elif which.startswith('blue'):
        p,v=transport(BLUE_ROUTE,blue_p)
        c.arrow(project(p),project(p+.28*v),BLUE,5.,1.,15)
        c.dot(project(p),5.,BLUE)
        c.text((930,330),'First x, then y',31,BLUE,bold=True)
        c.math((930,405),r'T_y(b)T_x(a)\mathbf v',42,BLUE)
        c.text((930,470),'Keep the resulting blue arrow.',24,MUTED,alpha=fade(t,10.8,11.6))
    else:
        c.arrow(project(END),project(END+.28*V_BLUE),BLUE,5.,1.,15)
        if which=='reset':
            alpha=fade(t,12.7,13.5)
            c.arrow(project(N),project(N+.28*V0),COPPER,5.,alpha,15)
            c.text((930,330),'Start again from A.',31,INK,bold=True)
        elif which.startswith('copper'):
            p,v=transport(COPPER_ROUTE,copper_p)
            c.arrow(project(p),project(p+.28*v),COPPER,5.,1.,15)
            c.dot(project(p),5.,COPPER)
            c.text((930,330),'First y, then x',31,COPPER,bold=True)
            c.math((930,405),r'T_x(a)T_y(b)\mathbf v',42,COPPER)
        else:
            c.arrow(project(END),project(END+.28*V_COPPER),COPPER,5.,1.,15)
            c.dot(project(END),5.,INK)
            final_comparison(c,t)
    footer=fade(t,28.,29.)
    c.text((800,800),'For small a, b, with Dₓ and Dᵧ the generators of these transports:',22,MUTED,center=True,alpha=footer)
    c.math((800,850),r'\Delta\mathbf v\approx ab[\hat D_x,\hat D_y]\mathbf v',36,INK,center=True,alpha=footer)
    return c.finish()


def validate_math():
    max_norm=max_tangent=max_endpoint=0.
    for route in (BLUE_ROUTE,COPPER_ROUTE):
        for u in np.linspace(0,2,201):
            p,v=transport(route,u)
            max_norm=max(max_norm,abs(np.linalg.norm(v)-1),abs(np.linalg.norm(p)-1))
            max_tangent=max(max_tangent,abs(np.dot(p,v)))
        p,_=transport(route,2.)
        max_endpoint=max(max_endpoint,np.linalg.norm(p-END))
    gap_inset=np.array([np.dot(DELTA,INSET_E1),np.dot(DELTA,INSET_E2)])
    assert abs(np.linalg.norm(gap_inset)-np.linalg.norm(DELTA))<1e-12
    convergence=[]
    for a in (.3,.1,.03,.01,.003):
        blue,copper=routes(a,a)
        end,vb=transport(blue,2.)
        _,vc=transport(copper,2.)
        _,back=transport_leg(end,N,vc-vb,1.)
        normalized=back/(a*a)
        convergence.append({'a_equals_b':a,'normalized_gap_in_initial_frame':normalized.tolist(),
                            'error_from_minus_Jv':float(np.linalg.norm(normalized+E2))})
    assert convergence[-1]['error_from_minus_Jv']<1e-5
    assert max(max_norm,max_tangent,max_endpoint)<1e-12
    return {'max_norm_error':float(max_norm),'max_tangency_error':float(max_tangent),
        'max_common_endpoint_error':float(max_endpoint),'finite_arrow_difference':DELTA.tolist(),
        'signed_blue_to_copper_angle_degrees':math.degrees(signed_tangent_angle(END,V_BLUE,V_COPPER)),
        'small_loop_convergence':convergence,'coordinate_model':'gnomonic, both coordinate curves great circles',
        'finite_bracket_order':'copper y-then-x minus blue x-then-y',
        'duration_seconds':DURATION,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def make_sheet(times,target,frames=None):
    ww,hh,cols=480,270,3
    result=Image.new('RGB',(ww*cols,math.ceil(len(times)/cols)*(hh+32)),BG)
    draw=ImageDraw.Draw(result)
    for i,t in enumerate(times):
        im=render(t) if frames is None else frames[i]
        x,y=(i%cols)*ww,(i//cols)*(hh+32)
        result.paste(im.resize((ww,hh),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+10,y+hh+5),f'{t:.1f} s',font=font(9),fill=INK)
    result.save(target)


def preview():
    for t in MOMENTS:render(t).save(REVIEW/f'preview-{t:04.1f}.png')
    make_sheet(MOMENTS,REVIEW/'preview-contact-sheet.png')
    render(27.).save(OUT/f'{NAME}-poster.png')
    print('Preview complete',flush=True)


def encode():
    tmp=REVIEW/f'{NAME}.rendering.mp4'
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
             '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an',
             '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p',
             '-movflags','+faststart','-threads','2',str(tmp)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as proc:
        try:
            for i in range(round(DURATION*FPS)):
                proc.stdin.write(render(i/FPS).tobytes())
                if i%(FPS*2)==0:print(f'{i/FPS:g}/{DURATION:g} seconds rendered',flush=True)
            proc.stdin.close()
            if proc.wait():raise RuntimeError('FFmpeg failed')
        except BaseException:
            proc.kill();raise
    tmp.replace(OUT/f'{NAME}.mp4')


def encoded_check():
    video=OUT/f'{NAME}.mp4'
    reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24')
    meta=next(reader)
    times=sorted(set(MOMENTS+[12.4,12.6,13.,13.8,14.1,22.4,22.6,23.,23.5,25.,26.,28.5]))
    wanted={round(t*FPS) for t in times}
    frames={}
    for i,data in enumerate(reader):
        if i in wanted:frames[i]=Image.frombytes('RGB',(W,H),data)
    reader.close()
    assert i+1==round(DURATION*FPS)
    assert meta['size']==(W,H) and meta['fps']==FPS
    for i,im in frames.items():im.save(REVIEW/f'decoded-{i:04d}.png')
    make_sheet(MOMENTS,OUT/f'{NAME}-contact-sheet.png',[frames[round(t*FPS)] for t in MOMENTS])
    make_sheet(times,REVIEW/'decoded-review-contact-sheet.png',[frames[round(t*FPS)] for t in times])
    frames[round(27.*FPS)].save(OUT/f'{NAME}-poster.png')
    report={'size':meta['size'],'fps':meta['fps'],'duration_seconds':meta['duration'],
            'frame_count':round(DURATION*FPS),'complete_decode':'passed',
            'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'decoded_review_times':times,
            'text_bounds_and_text_text_collisions':'checked on every rendered frame'}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)


def main():
    parser=argparse.ArgumentParser()
    for flag in ('preview','render','check'):parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(validate_math(),indent=2)+'\n',encoding='utf8')
    if args.preview or not(args.render or args.check):preview()
    if args.render:encode()
    if args.check:encoded_check()


if __name__=='__main__':main()
