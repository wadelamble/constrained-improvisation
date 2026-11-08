"""Conjugation and its derivative as a six-scene, exact 2D animated argument.

U(s)=R(s)=exp(-isG), G=iJ, A=diag(1.6,.6).  The plotted real plane
is invariant under U and A, although G itself has imaginary entries.
Only -iG=J is drawn as a real tangent.  s is an angle, not elapsed time.

Run without flags for previews, --render --check for the 112-second MP4.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
from symmetry_exponential_desktop_common import (
    Canvas,W,H,FPS,BG,INK,MUTED,GRID,FAINT,BLUE,RED,GREEN,GOLD,font,ease,equation,
)

NAME='symmetry-heisenberg-operator'
OUT=ROOT/'content/drafts/animations'
REVIEW=ROOT/'.tools'/f'{NAME}-review'
DURATION=112
STARTS=(0,16,40,60,84,102)
TITLES=('A unitary transformation','The three steps of conjugation',
        'An operator changes with the parameter','Two factors contribute to the change',
        'The commutator is the rate of change','When the operators commute')
FORMULAS=(
    r'U(s)=e^{-isG}',
    r'A_s=U(s)^\dagger A\,U(s)',
    r'A_s=U(s)^\dagger A\,U(s)',
    r'\frac{dA_s}{ds}=\frac{dU^\dagger}{ds}A\,U+U^\dagger A\frac{dU}{ds}',
    r'\frac{dA_s}{ds}=\lim_{\epsilon\to0}\frac{A_{s+\epsilon}-A_s}{\epsilon}=i[G,A_s]',
    r'[G,A]=0\quad\Longrightarrow\quad A_s=A,\qquad\frac{dA_s}{ds}=0',
)
MOMENTS=(3,10,15,19,23,28,33,39,44,51,59,63,70,77,83,87,93,100,105,110)
POSTER_TIME=77
J=np.array([[0.,-1.],[1.,0.]])
G=1j*J
A=np.diag([1.6,.6])
V=np.array([1.,0.])
S0=math.pi/4
ANGLES=np.linspace(0,2*math.pi,241)
CIRCLE=np.array([np.cos(ANGLES),np.sin(ANGLES)])


def rotation(s):
    c,z=math.cos(s),math.sin(s)
    return np.array([[c,-z],[z,c]])


def operator(s):
    u=rotation(s)
    return u.T@A@u


def rate(s):
    a=operator(s)
    return a@J-J@a


def point(v,center,scale):
    return np.asarray(center)+scale*np.array([v[0],-v[1]])


def curve(s,points,center,scale,color=BLUE,width=3,dashed=False):
    p=np.asarray(center)[None,:]+scale*np.asarray(points).T*np.array([1,-1])
    if dashed:
        for i in range(0,len(p)-1,8):
            s.line(p[i:min(i+4,len(p))],color,width)
    else:
        s.line(p,color,width)


def axes(s,center,scale,extent=1.8):
    for axis in (0,1):
        a=np.zeros(2);a[axis]=-extent
        b=np.zeros(2);b[axis]=extent
        s.line([point(a,center,scale),point(b,center,scale)],FAINT,1)
    s.dot(center,3,GRID)


def vector(s,v,center,scale,color=BLUE,width=4,start=None):
    start=np.zeros(2) if start is None else np.asarray(start)
    s.arrow(point(start,center,scale),point(start+v,center,scale),color,width,13)


def plane_image(s,matrix,center,scale,active=True):
    axes(s,center,scale)
    curve(s,CIRCLE,center,scale,GRID,1,True)
    curve(s,matrix@CIRCLE,center,scale,BLUE if active else GRID,3 if active else 1)
    vector(s,matrix@V,center,scale,BLUE if active else GRID)


def caption(s,first,second=''):
    s.text(800,774,first,26,INK,anchor='mm')
    if second:s.text(800,813,second,22,MUTED,anchor='mm')


def header(s,index,t):
    s.text(52,35,f'{index+1:02d} / 06',20,GOLD,True)
    s.text(1548,35,'HOW ONE OPERATOR CHANGES UNDER ANOTHER',17,MUTED,anchor='ra')
    s.text(800,82,TITLES[index],38,INK,True,anchor='mm')
    tex=FORMULAS[index]
    if index==3 and t-STARTS[index]>=14:
        tex=r'\frac{dA_s}{ds}=iGA_s-iA_sG=i[G,A_s]'
    s.math(800,147,tex,31 if index in (3,4,5) else 36,center=True)
    s.line([(52,194),(1548,194)],FAINT,2)
    s.line([(52,875),(1548,875)],FAINT,2)
    s.line([(52,875),(52+1496*t/DURATION,875)],GOLD,3)
    for start in STARTS:
        x=52+1496*start/DURATION
        s.line([(x,870),(x,879)],GRID,1)
    s.text(52,848,'Two-component vectors · s is a rotation angle',18,MUTED)
    s.text(1548,848,f'{int(t)//60}:{int(t)%60:02d} / 1:52',18,MUTED,anchor='ra')


def matrix2(s,values,center,label,colors=None):
    cx,cy=center
    s.math(cx-136,cy,label,38,center=True)
    for j in range(2):
        for i in range(2):
            s.math(cx+(i-.5)*87,cy+(j-.5)*66,values[j][i],34,
                   color=INK if colors is None else colors[j][i],center=True)
    for sign in (-1,1):
        x=cx+sign*93
        s.line([(x-sign*12,cy-71),(x,cy-71),(x,cy+71),(x-sign*12,cy+71)],INK,2)


def scene_unitary(s,t):
    angle=(math.pi/2)*ease((t-2)/10)
    u=rotation(angle)
    center=(435,470);scale=156
    axes(s,center,scale,1.65)
    curve(s,CIRCLE,center,scale,GRID,2)
    vector(s,V,center,scale,GRID,2)
    vector(s,u@V,center,scale,BLUE)
    vector(s,J@u@V,center,scale,GOLD,3,start=u@V)
    s.text(435,230,f's = {math.degrees(angle):.0f}°',27,INK,True,anchor='mm')
    s.math(330,731,r'U(s)\mathbf{v}',29,color=BLUE,center=True)
    s.math(575,731,r'-iG\,U(s)\mathbf{v}',29,color=GOLD,center=True)
    matrix2(s,(('0','-i'),('i','0')),(1130,345),r'G=')
    s.math(1090,470,r'G^\dagger=G',34,center=True)
    s.math(1090,562,r'-iG=J,\qquad J(x,y)=(-y,x)',30,center=True)
    s.math(1090,659,r'U^\dagger U=I',34,center=True)
    caption(s,'The generator gives the tangent. Its exponential gives the rotation.',
            'G is self-adjoint. U preserves the length of the vector.')


def scene_sandwich(s,t):
    p1=ease((t-2)/5);p2=ease((t-7)/5);p3=ease((t-12)/5)
    u=rotation(S0)
    stretch=np.diag(1+p2*(np.diag(A)-1))
    matrices=(np.eye(2),rotation(S0*p1),stretch@u,rotation(-S0*p3)@A@u)
    labels=(r'\mathbf{v}',r'U\mathbf{v}',r'AU\mathbf{v}',r'U^\dagger AU\mathbf{v}')
    names=('Start','Rotate','Stretch','Rotate back')
    visible=(True,t>=2,t>=7,t>=12)
    for i,cx in enumerate((200,600,1000,1400)):
        s.text(cx,248,names[i],27,INK if visible[i] else MUTED,True,anchor='mm')
        if visible[i]:
            plane_image(s,matrices[i],(cx,460),83)
        else:
            axes(s,(cx,460),83)
            curve(s,CIRCLE,(cx,460),83,FAINT,1,True)
        s.math(cx,660,labels[i],29,center=True)
    for i,cx in enumerate((400,800,1200)):
        on=t>=(2,7,12)[i]
        s.arrow((cx-38,460),(cx+38,460),INK if on else GRID,2,10)
        s.math(cx,402,(r'U',r'A',r'U^\dagger')[i],30,center=True)
    s.math(800,721,r'A(x,y)=(1.6x,\,0.6y),\qquad s=45^\circ',29,center=True)
    caption(s,'The entire three-step operation is a new operator, Aₛ.',
            'Read U† A U from right to left. Only the U steps are rotations.')


def scene_family(s,t):
    angle=S0*ease((t-2)/14)
    m=operator(angle)
    left=(425,485);right=(1115,485)
    s.text(425,243,'Action on the whole unit circle',27,INK,True,anchor='mm')
    s.text(1115,243,'Action on one fixed input',27,INK,True,anchor='mm')
    plane_image(s,m,left,135)
    for i in range(2):
        e=rotation(-angle)[:,i]
        curve(s,np.stack((-m@e,m@e),axis=1),left,135,GRID,1)
    axes(s,right,158,1.85)
    curve(s,1.1*V[:,None]+.5*CIRCLE,right,158,GRID,1,True)
    vector(s,V,right,158,GRID,2)
    vector(s,m@V,right,158,BLUE)
    path=np.stack([operator(q)@V for q in np.linspace(0,angle,100)],axis=1)
    curve(s,path,right,158,BLUE,3)
    s.math(425,721,r'A_s=R(-s)\,A\,R(s)',30,center=True)
    s.math(1115,721,r'\mathbf{v}\ \mathrm{fixed},\qquad A_s\mathbf{v}\ \mathrm{changes}',29,center=True)
    s.text(800,232,f's = {math.degrees(angle):.0f}°',23,MUTED,anchor='mm')
    caption(s,'Changing s changes the operator, even when the input stays fixed.',
            'Its eigenvalues stay 1.6 and 0.6. Its eigenvector directions rotate.')


def scene_product(s,t):
    m=operator(S0)
    left=-J@m@V
    right=m@J@V
    total=left+right
    reveal_left=ease((t-1)/5)
    reveal_right=ease((t-7)/5)
    reveal_sum=ease((t-14)/3)
    centers=((300,520),(800,520),(1300,520))
    names=('Change in the left factor','Change in the right factor','Add the two contributions')
    for c,name in zip(centers,names):
        s.text(c[0],258,name,25,INK,True,anchor='mm')
        axes(s,c,130,1.3)
    s.math(300,319,r'\frac{dU^\dagger}{ds}=iG\,U^\dagger',27,color=GOLD,center=True)
    s.math(800,319,r'\frac{dU}{ds}=-iG\,U',27,color=BLUE,center=True)
    vector(s,left*reveal_left,centers[0],130,GOLD)
    vector(s,right*reveal_right,centers[1],130,BLUE)
    if t>=14:
        vector(s,left,centers[2],130,GOLD,3)
        vector(s,right*reveal_sum,centers[2],130,BLUE,3,start=left)
        vector(s,total*reveal_sum,centers[2],130,GREEN,5)
    s.math(300,710,r'(iGA_s)\mathbf{v}',30,color=GOLD,center=True)
    s.math(800,710,r'(-iA_sG)\mathbf{v}',30,color=BLUE,center=True)
    s.math(1300,710,r'i[G,A_s]\mathbf{v}',30,color=GREEN,center=True)
    s.text(800,224,'s = 45° · the same fixed input in all three panels',21,MUTED,anchor='mm')
    caption(s,'The product rule gives two contributions with opposite signs.',
            'Together they give i[G, Aₛ]. The arrows show rates of change.')


def scene_limit(s,t):
    epsilon=.4*math.exp(-math.log(16)*ease((t-2)/11))
    m=operator(S0)
    initial=m@V
    exact=operator(S0+epsilon)@V
    derivative=rate(S0)@V
    predicted=initial+epsilon*derivative
    finite=(exact-initial)/epsilon
    c=(300,475);scale=285
    axes(s,c,scale,extent=.3)
    curve(s,1.1*V[:,None]+.5*CIRCLE,c,scale,GRID,1,True)
    vector(s,initial,c,scale,GRID,2)
    s.dot(point(initial,c,scale),6,INK)
    vector(s,exact-initial,c,scale,GOLD,4,start=initial)
    vector(s,epsilon*derivative,c,scale,GREEN,4,start=initial)
    s.dot(point(exact,c,scale),6,GOLD)
    s.dot(point(predicted,c,scale),5,GREEN)
    s.line([point(exact,c,scale),point(predicted,c,scale)],RED,2)
    s.text(505,254,'Finite change in the output',27,INK,True,anchor='mm')
    s.text(505,710,f'ε = {epsilon:.3f} radians',26,INK,True,anchor='mm')
    rc=(1330,475);rs=215
    axes(s,rc,rs,1.05)
    vector(s,derivative,rc,rs,GREEN,5)
    vector(s,finite,rc,rs,GOLD,3)
    s.text(1240,254,'Change divided by ε',27,INK,True,anchor='mm')
    s.math(1240,660,r'\frac{(A_{s+\epsilon}-A_s)\mathbf{v}}{\epsilon}',30,color=GOLD,center=True)
    s.math(1240,716,r'i[G,A_s]\mathbf{v}',30,color=GREEN,center=True)
    caption(s,'As the step shrinks, the finite rate approaches the commutator.',
            'Gold: exact finite change. Green: the derivative prediction.')


def scene_commute(s,t):
    angle=(math.pi/2)*ease((t-1)/6)
    left=(435,480);scale=157
    axes(s,left,scale,1.7)
    curve(s,CIRCLE,left,scale,GRID,2)
    vector(s,rotation(angle)@V,left,scale,GRID,2)
    vector(s,V,left,scale,BLUE,5)
    s.text(435,246,'Set A = I',28,INK,True,anchor='mm')
    s.math(435,714,r'U^\dagger I\,U\mathbf{v}=\mathbf{v}',32,center=True)
    right=(1170,430);rs=165
    axes(s,right,rs,1.4)
    # A small horizontal offset separates coincident opposite arrows visibly.
    p0=point(np.zeros(2),right,rs);p1=point(-J@V,right,rs)
    s.arrow(p0+[-5,0],p1+[-5,0],GOLD,4,12)
    s.arrow(p1+[5,0],p0+[5,0],BLUE,4,12)
    s.dot(p0,7,GREEN)
    s.text(1170,246,'The contributions cancel',27,INK,True,anchor='mm')
    s.math(1000,525,r'iG\mathbf{v}',28,color=GOLD,center=True)
    s.math(1360,525,r'-iG\mathbf{v}',28,color=BLUE,center=True)
    s.math(1170,714,r'i[G,I]=0',32,color=GREEN,center=True)
    caption(s,'Commuting operators leave no net change.',
            'Choosing time as the parameter gives the general Heisenberg equation.')


SCENES=(scene_unitary,scene_sandwich,scene_family,scene_product,scene_limit,scene_commute)


def render(t,boxes=False):
    t=float(np.clip(t,0,DURATION-1/FPS))
    index=max(i for i,start in enumerate(STARTS) if t>=start)
    s=Canvas();header(s,index,t);SCENES[index](s,t-STARTS[index])
    return (s.im,s.boxes) if boxes else s.im


def validate():
    errors={key:0. for key in ('unitarity','self_adjoint_G','self_adjoint_A_s',
                              'analytic_derivative','finite_difference','fixed_eigenvalues',
                              'sandwich','circle_path','commuting_control')}
    errors['self_adjoint_G']=float(np.max(abs(G-G.conj().T)))
    for angle in np.linspace(-math.pi,math.pi,51):
        u=rotation(angle);a=operator(angle);d=rate(angle)
        tests={'unitarity':u.T@u-np.eye(2),'self_adjoint_A_s':a-a.T,
               'analytic_derivative':d-1j*(G@a-a@G),
               'finite_difference':(operator(angle+1e-6)-operator(angle-1e-6))/2e-6-d,
               'fixed_eigenvalues':np.linalg.eigvalsh(a)-[.6,1.6],
               'sandwich':a@V-u.T@(A@(u@V)),
               'circle_path':np.array([np.linalg.norm(a@V-1.1*V)-.5]),
               'commuting_control':u.T@np.eye(2)@u-np.eye(2)}
        for key,value in tests.items():errors[key]=max(errors[key],float(np.max(abs(value))))
    assert max(errors.values())<1e-8,errors
    residuals=[]
    for eps in (.4,.2,.1,.05):
        error=float(np.linalg.norm(operator(S0+eps)@V-operator(S0)@V-eps*rate(S0)@V))
        assert error<=eps**2+1e-12
        residuals.append({'epsilon':eps,'linear_prediction_error':error})
    collisions=[]
    times=sorted(set(MOMENTS+tuple(start+.05 for start in STARTS)))
    for t in times:
        _,boxes=render(t,True)
        for i,(a,an) in enumerate(boxes):
            for b,bn in boxes[i+1:]:
                w=min(a[2],b[2])-max(a[0],b[0]);h=min(a[3],b[3])-max(a[1],b[1])
                if w>3 and h>3:collisions.append({'time':t,'labels':[an,bn],'overlap':[w,h]})
    return {'numerical_errors':errors,'first_order_residuals':residuals,
            'label_collisions':collisions,'duration_seconds':DURATION,'size':[W,H],'fps':FPS,
            'model':'G=iJ, U=R(s), A=diag(1.6,0.6), v=(1,0)',
            'scope':'Generic transformation parameter. No position-wave-number CCR used.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def preview():
    OUT.mkdir(exist_ok=True,parents=True);REVIEW.mkdir(exist_ok=True,parents=True)
    sheet=Image.new('RGB',(1600,math.ceil(len(MOMENTS)/4)*250),BG)
    d=ImageDraw.Draw(sheet)
    for i,t in enumerate(MOMENTS):
        im=render(t);im.save(REVIEW/f'{t:05.1f}.png')
        x,y=i%4*400,i//4*250
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),(x,y))
        d.text((x+12,y+229),f'{t:g}s',font=font(17),fill=MUTED)
    sheet.save(REVIEW/'contact.png')
    render(POSTER_TIME).save(OUT/f'{NAME}-poster.png')
    report=validate()
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)
    assert not report['label_collisions'],'Resolve label collisions before rendering'


def encode():
    tmp=REVIEW/f'{NAME}.rendering.mp4'
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
         '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','3',str(tmp)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        try:
            for i in range(DURATION*FPS):
                process.stdin.write(render(i/FPS).tobytes())
                if i%(FPS*8)==0:print(f'{i/FPS:.0f} / {DURATION} seconds rendered',flush=True)
            process.stdin.close()
            if process.wait():raise RuntimeError('FFmpeg encoding failed')
        except BaseException:
            process.kill();raise
    tmp.replace(OUT/f'{NAME}.mp4')


def check():
    video=OUT/f'{NAME}.mp4';ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    reader=imageio_ffmpeg.read_frames(str(video))
    try:meta=next(reader)
    finally:reader.close()
    count,seconds=imageio_ffmpeg.count_frames_and_secs(str(video))
    assert meta['size']==(W,H) and meta['fps']==FPS
    assert count==DURATION*FPS and abs(seconds-DURATION)<.05
    subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
    times=(10,23,33,39,51,59,70,83,87,93,100,110)
    selection='+'.join(f'eq(n\\,{round(t*FPS)})' for t in times)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                    f'select={selection},scale=480:270,tile=3x4','-frames:v','1',
                    str(OUT/f'{NAME}-contact-sheet.png')],check=True)
    for t in (10,39,59,83,93,110):
        subprocess.run([ffmpeg,'-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',
                        str(REVIEW/f'decoded-{t}.png')],check=True)
    report={'frame_count':count,'duration_seconds':seconds,'size':meta['size'],'fps':meta['fps'],
            'decode':'passed','video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
            'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'decoded_contact_sheet_times':times}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    preview()
    if args.render:encode()
    if args.check:check()
