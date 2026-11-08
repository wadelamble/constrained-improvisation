"""An eight-scene animated argument for completeness of displacement operators.

The finite scenes are the EXACT N=8 periodic Weyl model, not a truncation
claiming an exact finite-dimensional CCR. The last scene shows the continuum
kernel construction schematically by refining samples and widening the window.
All synthesis coefficients are computed from the operator, never from an input.

Run without flags for source previews and validation; --render --check makes
the 184-second master MP4 and decodes it for independent delivery checks.
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
from symmetry_exponential_desktop_common import (
    Canvas, W, H, FPS, BG, INK, MUTED, GRID, FAINT, BLUE, GOLD,
    RED, GREEN, font, equation, ease,
)
import symmetry_operator_basis as model

NAME = 'symmetry-operator-completeness'
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools' / (NAME + '-review')
DURATION = 184
STARTS = (0, 20, 42, 64, 88, 120, 146, 168)
TITLES = (
    'An operator combines input values',
    'Position shifts select displacement diagonals',
    'Each displacement needs its own weights',
    'Wave-number shifts supply phase patterns',
    'Fourier patterns build the weights',
    'All displacements build the operator',
    'The same operator works on different states',
    'From samples to functions',
)
TEX = (
    r'g_j=\sum_i A_{ji} f_i',
    r'(T_x(a)f)_j=f_{j-a}',
    r'g_j=w_a(j)\,f_{j-a}',
    r'(T_k(b)f)_j=e^{2\pi i b j/8}f_j',
    r'w_a(j)=\sum_b c_{ab}\,e^{2\pi i b j/8}',
    r'A=\sum_a\operatorname{diag}(w_a)T_x(a)=\sum_{a,b}c_{ab}T_k(b)T_x(a)',
    r'A f=\left(\sum_{a,b}c_{ab}T_k(b)T_x(a)\right)f',
    r'\hat A=\iint c(a,b)\,T_k(b)T_x(a)\,da\,db',
)
MOMENTS = (2, 9, 18, 24, 34, 40, 46, 55, 61, 67, 75, 85,
           91, 100, 109, 118, 123, 133, 145, 150, 156, 167, 170, 176, 182)
POSTER_TIME = 145
A = model.TARGET_MATRIX
COEFF = model.coefficients(A)
WEIGHTS = model.band_weights(A)
REBUILT = model.reconstruct(COEFF)
N = model.N
FREQ_ORDER = (0, 1, 7, 2, 6, 3, 5, 4)
SIGNED_FREQ = (0, 1, -1, 2, -2, 3, -3, -4)
PLOT_COLORS = (BLUE, GOLD)
MAX_WEIGHT = float(np.max(np.abs(A)))
CAPTIONS = (
    ('Every output receives a weighted contribution from the inputs.',
     'Rows are output positions. Columns are input positions.'),
    ('A shift sends every sample the same number of positions forward.',
     'The periodic grid makes each shift an exact, reversible permutation.'),
    ('The shift chooses the displacement. The weights choose the contribution.',
     'One diagonal connects every input to its displaced output.'),
    ('A wave-number shift multiplies each sample by a unit complex number.',
     'Across position, those multipliers form a Fourier pattern.'),
    ('Weight the phase patterns, then add them.',
     'Their real and imaginary parts combine to reproduce the chosen weights.'),
    ('Each displacement supplies one diagonal. Together they cover every entry.',
     'Adding the weighted translations reconstructs the whole operator.'),
    ('Change the input. Keep all 64 operator coefficients fixed.',
     'Direct multiplication and the translation expansion give the same output.'),
    ('Refine the samples and widen the interval. Sums become integrals.',
     'Position shifts select displacements. Fourier patterns supply the weights.'),
)


def blend(color, amount=1., base=BG):
    def rgb(c):
        return np.array([int(c[i:i+2],16) for i in (1,3,5)])
    return tuple(np.rint(rgb(base)+(rgb(color)-rgb(base))*np.clip(amount,0,1)).astype(int))


def dashed(s, points, color=GRID, width=2, dash=8):
    for start,end in zip(points[:-1], points[1:]):
        start,end=np.asarray(start,float),np.asarray(end,float)
        length=np.linalg.norm(end-start)
        if length < 1: continue
        for d in np.arange(0,length,dash*2):
            s.line([start+(end-start)*d/length,
                    start+(end-start)*min(d+dash,length)/length],color,width)


def header(s, scene, t):
    s.text(52,35,f'{scene+1:02d} / 08',20,GOLD,True)
    s.text(1548,35,'TRANSLATIONS AS AN OPERATOR FAMILY',17,MUTED,anchor='ra')
    s.text(800,82,TITLES[scene],38,INK,True,anchor='mm')
    formula=TEX[scene]
    if scene==7 and t-STARTS[7]<6.8:
        formula=r'g(x_j)\approx\sum_i A(x_j,y_i)\,f(y_i)\,\Delta y'
    s.math(800,147,formula,size=31 if scene==5 else 34,center=True)
    s.line([(52,193),(1548,193)],FAINT,2)
    s.line([(52,872),(1548,872)],FAINT,2)
    s.line([(52,872),(52+1496*t/DURATION,872)],GOLD,3)
    for start in STARTS:
        x=52+1496*start/DURATION
        s.line([(x,868),(x,877)],GRID,1)
    note='8 equally spaced positions · periodic grid' if scene<7 else 'Continuous kernel · wider window and finer samples'
    s.text(52,840,note,18,MUTED)
    s.text(1548,840,f'{int(t)//60}:{int(t)%60:02d} / 3:04',18,MUTED,anchor='ra')


def caption(s, scene, first=None, second=None):
    first = CAPTIONS[scene][0] if first is None else first
    second = CAPTIONS[scene][1] if second is None else second
    s.text(800,766,first,26,INK,anchor='mm')
    if second:
        s.text(800,807,second,22,MUTED,anchor='mm')


def matrix(s, values, x, y, cell=48, numbers=True, highlight=None, ghost=None,
           selected_row=None, title=None, axes=True):
    values=np.asarray(values)
    n=len(values)
    for j in range(n):
        for i in range(n):
            z=values[j,i]
            value=float(z.real)
            color=BLUE if value>=0 else RED
            fill=blend(color,.66*min(abs(value)/MAX_WEIGHT,1))
            if abs(z)<1e-10:
                fill=blend(GRID,.10)
            x0,y0=x+i*cell,y+j*cell
            s.d.rectangle((x0+1,y0+1,x0+cell-1,y0+cell-1),fill=fill)
            if ghost is not None and abs(z)<1e-10:
                marker=ghost[j,i]
                s.d.ellipse((x0+cell/2-2,y0+cell/2-2,x0+cell/2+2,y0+cell/2+2),fill=blend(MUTED,.25))
            if numbers and abs(z)>1e-9:
                label=f'{value:.2f}' if abs(value-1)>1e-10 else '1'
                s.text(x0+cell/2,y0+cell/2,label,16 if cell>=44 else 12,INK,anchor='mm')
    if selected_row is not None:
        y0=y+selected_row*cell
        s.d.rectangle((x-2,y0-2,x+n*cell+2,y0+cell+2),outline=GOLD,width=3)
    if highlight is not None:
        for j,i in highlight:
            x0,y0=x+i*cell,y+j*cell
            s.d.rectangle((x0+2,y0+2,x0+cell-2,y0+cell-2),outline=GOLD,width=3)
    if axes:
        for i in range(n):
            s.text(x+(i+.5)*cell,y-17,str(i),19,MUTED,anchor='mm')
            s.text(x-19,y+(i+.5)*cell,str(i),19,MUTED,anchor='mm')
        s.text(x+n*cell/2,y-52,'input position i',22,MUTED,anchor='mm')
        s.text(x-21,y+n*cell+7,'output j',18,MUTED,anchor='la')
    if title:
        s.text(x+n*cell/2,y-80,title,27,INK,True,anchor='mm')


def column(s, v, x, y, cell=48, scale=90, active=None, label=None, pale=False):
    if label:
        s.text(x,y-58,label,27,INK,True,anchor='mm')
    for j,z in enumerate(v):
        yy=y+(j+.5)*cell
        if np.isnan(z): continue
        color=BLUE if z>=0 else RED
        if pale: color=blend(color,.30)
        s.line([(x-75,yy),(x+75,yy)],FAINT,1)
        s.line([(x,yy-9),(x,yy+9)],GRID,1)
        end=x+scale*z
        s.line([(x,yy),(end,yy)],color,5)
        s.dot((end,yy),5,color)
        s.text(x+106,yy,f'{z:.2f}',21,INK if not pale else MUTED,anchor='mm')
        if active==j:
            s.d.rounded_rectangle((x-86,yy-20,x+141,yy+20),radius=6,outline=GOLD,width=2)


def samples(s, values, x, base, width, height=78, limit=1., color=BLUE,
            title=None, target=None, indices=False, imaginary=False,
            active=None, numbers=False):
    values=np.asarray(values)
    xx=np.linspace(x,x+width,len(values))
    s.line([(x-10,base),(x+width+10,base)],GRID,1)
    if title:
        s.text(x,base-height-34,title,24,INK,True)
    if target is not None:
        tar=base-height*np.asarray(target).real/limit
        dashed(s,list(zip(xx,tar)),MUTED,2,5)
        for px,py in zip(xx,tar):
            s.d.ellipse((px-7,py-7,px+7,py+7),outline=MUTED,width=2)
    rr=base-height*values.real/limit
    s.line(list(zip(xx,rr)),color,3)
    for j,(px,py) in enumerate(zip(xx,rr)):
        s.line([(px,base),(px,py)],blend(color,.45),2)
        s.dot((px,py),5,color)
        if indices: s.text(px,base+height+21,str(j),18,MUTED,anchor='mm')
        if numbers: s.text(px,base+height+22,f'{values[j].real:.2f}',17,MUTED,anchor='mm')
        if active==j:
            s.d.ellipse((px-11,py-11,px+11,py+11),outline=GOLD,width=3)
    if imaginary:
        ii=base-height*values.imag/limit
        s.line(list(zip(xx,ii)),GOLD,2)
        for px,py in zip(xx,ii):
            s.d.rectangle((px-3,py-3,px+3,py+3),fill=GOLD)
    s.text(x-22,base,'0',17,MUTED,anchor='rm')
    return np.column_stack((xx,rr))


def scene_inputs(s,t):
    f=model.INPUT_VECTORS[0]
    target=A@f
    row=3
    nterms=np.clip((t-3)/1.35,0,8)
    full=int(nterms)
    frac=ease(nterms-full)
    factors=np.zeros(N)
    factors[:full]=1
    if full<N: factors[full]=frac
    selected=None if t>16 else row
    matrix(s,A,620,274,selected_row=selected)
    column(s,f,200,274,label='Input f')
    output=np.full(N,np.nan)
    output[row]=np.sum(A[row]*f*factors)
    if t>=15:
        output=target*ease((t-15)/1.6)
        output[row]=target[row]
    column(s,output,1320,274,label='Output Af',active=selected)
    if 3<t<14:
        i=min(full,7)
        start=np.array([345,274+(i+.5)*48])
        # Keep the moving contribution outside the matrix so it never runs
        # through the row's numeric weights. The selected weight is outlined.
        end=np.array([570,274+(row+.5)*48])
        s.arrow(start,end,GOLD,2,10)
        s.dot(start+(end-start)*frac,7,GOLD)
        s.d.rectangle((620+i*48+2,274+row*48+2,620+(i+1)*48-2,274+(row+1)*48-2),outline=GOLD,width=4)
    s.arrow((1026,442),(1200,442),INK,2,12)
    s.text(800,710,f'Output {row}: {min(full,8)} of 8 contributions added' if t<15 else 'One fixed matrix determines all eight outputs',25,INK,anchor='mm')
    caption(s,0)


def scene_shift(s,t):
    a=0 if t<5 else 1 if t<12 else 2
    f=model.INPUT_VECTORS[0]
    tx=model.shift_matrix(a)
    matrix(s,tx,200,292,title=f'Position shift: a = {a}')
    samples(s,f,860,330,580,height=72,limit=.85,title='Input samples',indices=False)
    samples(s,tx@f,860,590,580,height=72,limit=.85,title=f'Shifted samples · a = {a}',target=f,indices=True)
    s.arrow((1140,428),(1140,467),INK,3,12)
    active=int(max(0,t-1)*1.1)%N
    cell=((active+a)%N,active)
    x,y=200+(cell[1]+.5)*48,292+(cell[0]+.5)*48
    s.d.rectangle((x-22,y-22,x+22,y+22),outline=GOLD,width=3)
    if a:
        s.text(1148,718,f'Input {active} goes to output {(active+a)%N}',23,INK,anchor='mm')
    else:
        s.text(1148,718,'Zero displacement leaves each sample in place',23,INK,anchor='mm')
    caption(s,1)


def scene_weights(s,t):
    a=2
    f=model.INPUT_VECTORS[0]
    shifted=model.shift_matrix(a)@f
    u=ease((t-3)/8)
    w=(1-u)*np.ones(N)+u*WEIGHTS[a]
    band=np.diag(w)@model.shift_matrix(a)
    active=int(max(0,t-11)/.85)%N if t>11 else None
    highlight=None if active is None else [(active,(active-a)%N)]
    matrix(s,band,200,292,title='One displacement: a = 2',highlight=highlight,ghost=A)
    samples(s,shifted,860,310,580,height=47,limit=.85,title='Shifted input',active=active)
    samples(s,w,860,484,580,height=50,limit=1.05,title='Weights on this diagonal',active=active)
    samples(s,w*shifted,860,655,580,height=45,limit=.55,title='Weighted output',active=active)
    s.text(802,480,'×',35,INK,anchor='mm')
    s.text(802,650,'=',35,INK,anchor='mm')
    caption(s,2)


def phasor(s,x,y,z,r=43,color=BLUE):
    s.d.ellipse((x-r,y-r,x+r,y+r),outline=GRID,width=1)
    s.line([(x-r-5,y),(x+r+5,y)],FAINT,1)
    s.line([(x,y-r-5),(x,y+r+5)],FAINT,1)
    s.arrow((x,y),(x+r*z.real,y-r*z.imag),color,3,10)


def scene_phases(s,t):
    # Integer Fourier indices keep every displayed pattern an exact finite
    # cyclic wave-number shift. The moving highlight scans position, not time.
    b=0 if t<4 else 1 if t<10 else 2 if t<16 else 3
    z=np.exp(2j*np.pi*b*np.arange(N)/N)
    s.text(800,238,f'Wave-number step b = {b}',27,INK,True,anchor='mm')
    xs=np.linspace(225,1375,N)
    for j,x in enumerate(xs):
        phasor(s,x,355,z[j],47)
        s.text(x,431,f'j = {j}',20,MUTED,anchor='mm')
    active=int(t*1.4)%N
    s.d.ellipse((xs[active]-53,302,xs[active]+53,408),outline=GOLD,width=2)
    samples(s,z,225,610,1150,height=85,limit=1.,imaginary=True,indices=True)
    s.text(350,484,'Real part',22,BLUE,True)
    s.text(1125,484,'Imaginary part',22,GOLD,True)
    caption(s,3)


def scene_fourier(s,t):
    a=2
    completed=np.clip((t-3)/3.1,0,8)
    full=int(completed)
    frac=ease(completed-full)
    partial=np.zeros(N,complex)
    for b in FREQ_ORDER[:full]:
        partial+=COEFF[a,b]*np.exp(2j*np.pi*b*np.arange(N)/N)
    active=FREQ_ORDER[min(full,7)]
    term=COEFF[a,active]*np.exp(2j*np.pi*active*np.arange(N)/N)
    if full<8:
        partial+=frac*term
    samples(s,term,170,358,980,height=90,limit=.40,imaginary=True,
            title=f'One weighted phase pattern · b = {SIGNED_FREQ[min(full,7)]}')
    samples(s,partial,170,619,980,height=92,limit=.72,imaginary=True,
            target=WEIGHTS[a],title='Sum so far',indices=False)
    s.arrow((660,462),(660,491),INK,2,10)
    s.text(1282,263,'Coefficient',23,INK,True,anchor='mm')
    coeff=COEFF[a,active]
    phasor(s,1282,354,coeff/.23,r=65,color=GREEN)
    s.text(1282,448,f'{coeff.real:+.3f} {coeff.imag:+.3f}i',21,INK,anchor='mm')
    s.text(1282,494,'Same displacement a = 2',20,MUTED,anchor='mm')
    for ii,b in enumerate(SIGNED_FREQ):
        x=1208+(ii%4)*49
        y=552+(ii//4)*50
        c=GREEN if ii<full else GOLD if ii==full else GRID
        s.d.ellipse((x-18,y-18,x+18,y+18),outline=c,width=2)
        s.text(x,y,str(b),18,c,anchor='mm')
    s.text(1282,657,'Weights match' if full==8 else f'{full} / 8 patterns added',23,GREEN if full==8 else INK,True,anchor='mm')
    s.text(225,717,'Real',20,BLUE,True)
    s.text(330,717,'Imaginary',20,GOLD,True)
    s.text(520,717,'○ target weights',20,MUTED)
    caption(s,4)


def scene_assemble(s,t):
    count=np.clip((t-2)/2.65,0,8)
    full=int(count)
    frac=ease(count-full)
    built=np.zeros((N,N),complex)
    for a in range(full):
        built+=np.diag(WEIGHTS[a])@model.shift_matrix(a)
    active=min(full,7)
    band=np.diag(WEIGHTS[active])@model.shift_matrix(active)
    if full<N: built+=frac*band
    matrix(s,A,150,300,title='Target operator')
    matrix(s,built,1040,300,title='Assembled operator',ghost=A)
    matrix(s,band,690,415,cell=25,numbers=False,axes=False)
    s.text(790,375,f'Displacement a = {active}',22,INK,anchor='mm')
    s.text(961,514,'+',40,GOLD,anchor='mm')
    s.arrow((918,555),(1011,555),GOLD,2,10)
    if full==8:
        s.text(790,673,'All 64 entries match',24,GREEN,True,anchor='mm')
    else:
        s.text(790,673,f'{full*8} / 64 entries assembled',22,INK,anchor='mm')
    caption(s,5)


def scene_verify(s,t):
    idx=0 if t<11 else 1
    local=t-11*idx
    f=model.INPUT_VECTORS[idx]
    direct=A@f
    count=np.clip((local-1)/.92,0,8)
    full=int(count)
    frac=ease(count-full)
    built=np.zeros(N,complex)
    for a in range(full):
        built+=sum(COEFF[a,b]*(model.displacement(a,b)@f) for b in range(N))
    if full<N:
        built+=frac*sum(COEFF[full,b]*(model.displacement(full,b)@f) for b in range(N))
    assert np.max(np.abs(built.imag))<1e-12
    s.text(800,238,f'Input {idx+1} · coefficients unchanged',29,INK,True,anchor='mm')
    samples(s,f,110,483,330,height=130,limit=.85,title='Input state',indices=True)
    samples(s,direct,635,483,330,height=130,limit=.85,title='Direct matrix action',indices=True)
    samples(s,built.real,1160,483,330,height=130,limit=.85,title='Translation expansion',indices=True,target=direct)
    s.arrow((483,481),(573,481),INK,2,12)
    s.text(1055,481,'=',40,GREEN if full==8 else GRID,anchor='mm')
    s.text(800,681,'The two outputs agree' if full==8 else f'Adding displacement {min(full,7)}',27,GREEN if full==8 else INK,True,anchor='mm')
    caption(s,6)


@lru_cache(4)
def continuous_model(level):
    n=(8,16,32,64)[level]
    extent=(2,3,4,5)[level]
    x=np.linspace(-extent,extent,n,endpoint=False)+extent/n
    xx,yy=np.meshgrid(x,x,indexing='ij')
    kernel=np.exp(-.8*(xx-.6*yy)**2)*np.exp(-(xx*xx+yy*yy)/28)*(.7*np.cos(.7*xx*yy)+.3*np.sin(xx-yy))
    f=np.exp(-(x+.5)**2)-.45*np.exp(-(x-1.0)**2/.3)
    output=kernel@f*(2*extent/n)
    return x,kernel,f,output


def scene_continuum(s,t):
    level=min(int(t/3.4),3)
    x,kernel,f,out=continuous_model(level)
    n=len(x)
    picture=Image.new('RGB',(n,n),BG)
    for j in range(n):
        for i in range(n):
            z=kernel[j,i]
            picture.putpixel((i,j),blend(BLUE if z>=0 else RED,.76*min(abs(z)/.85,1)))
    s.im.paste(picture.resize((440,440),Image.Resampling.NEAREST),(130,248))
    s.text(350,219,'A continuous-kernel example',25,INK,True,anchor='mm')
    s.text(350,709,'Input position →',21,INK,anchor='mm')
    s.text(93,247,'x',23,INK,anchor='mm')
    s.text(130,748,f'{n} × {n} samples · window −{(2,3,4,5)[level]} to {(2,3,4,5)[level]}',19,MUTED)
    samples(s,f,850,353,600,height=84,limit=1.4,title='Input function')
    samples(s,out,850,613,600,height=84,limit=1.4,title='Output function')
    s.arrow((1150,462),(1150,491),INK,2,10)
    # This scene uses one shorter caption to keep the matrix-axis labels clear.
    s.text(1095,728,'Finer samples turn sums into integrals.',23,MUTED,anchor='mm')
    caption(s,7,first='',second=CAPTIONS[7][1])


SCENES=(scene_inputs,scene_shift,scene_weights,scene_phases,scene_fourier,scene_assemble,scene_verify,scene_continuum)


def render(t, return_boxes=False):
    t=min(max(0.,float(t)),DURATION-1/FPS)
    scene=max(i for i,start in enumerate(STARTS) if t>=start)
    s=Canvas()
    header(s,scene,t)
    SCENES[scene](s,t-STARTS[scene])
    return (s.im,s.boxes) if return_boxes else s.im


def validate_visuals():
    collisions=[]
    # Reject actual label collisions, excluding small touching glyph bounds.
    for t in sorted(set(MOMENTS+tuple(start+.05 for start in STARTS))):
        _,boxes=render(t,True)
        for i,(a,an) in enumerate(boxes):
            for b,bn in boxes[i+1:]:
                w=min(a[2],b[2])-max(a[0],b[0])
                h=min(a[3],b[3])-max(a[1],b[1])
                if w>3 and h>3:
                    collisions.append({'time':t,'labels':[an,bn],'overlap':[w,h]})
    return collisions


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    REVIEW.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1600,math.ceil(len(MOMENTS)/4)*248),BG)
    d=ImageDraw.Draw(sheet)
    for i,t in enumerate(MOMENTS):
        im=render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        x,y=i%4*400,i//4*248
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),(x,y))
        d.text((x+12,y+226),f'{t:g}s',font=font(17),fill=MUTED)
    sheet.save(REVIEW/'contact.png')
    render(POSTER_TIME).save(OUT/f'{NAME}-poster.png')
    collisions=validate_visuals()
    report={'label_collisions':collisions,'checked_times':list(MOMENTS),'duration_seconds':DURATION,
            'scenes':[{'start':start,'title':title,'equation':tex,'caption':cap}
                      for start,title,tex,cap in zip(STARTS,TITLES,TEX,CAPTIONS)],
            'finite_model':'Exact N=8 periodic Weyl basis, not a finite-dimensional CCR',
            'continuum_scene':'Illustrative refinement of a smooth fixed kernel on wider windows',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/f'{NAME}-visual-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'source_previews':len(MOMENTS),'label_collisions':collisions}),flush=True)
    if collisions: raise AssertionError('Resolve label collisions before video render')


def encode():
    temporary=REVIEW/f'{NAME}.rendering.mp4'
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
             '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
             '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','3',str(temporary)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
        try:
            for i in range(DURATION*FPS):
                process.stdin.write(render(i/FPS).tobytes())
                if i%(FPS*8)==0: print(f'{i/FPS:.0f} / {DURATION} seconds rendered',flush=True)
            process.stdin.close()
            if process.wait(): raise RuntimeError('Encoding failed')
        except BaseException:
            process.kill()
            raise
    temporary.replace(OUT/f'{NAME}.mp4')


def check():
    video=OUT/f'{NAME}.mp4'
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    reader=imageio_ffmpeg.read_frames(str(video))
    try: meta=next(reader)
    finally: reader.close()
    count,seconds=imageio_ffmpeg.count_frames_and_secs(str(video))
    assert meta['size']==(W,H) and meta['fps']==FPS
    assert count==DURATION*FPS and abs(seconds-DURATION)<.05
    subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
    times=(9,34,55,75,100,118,133,145,156,167,176,182)
    indices=[round(t*FPS) for t in times]
    selection='+'.join(f'eq(n\\,{n})' for n in indices)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                    f'select={selection},scale=480:270,tile=3x4','-frames:v','1',
                    str(OUT/f'{NAME}-contact-sheet.png')],check=True)
    # Extract decoded frames, not only images produced directly by the renderer.
    for t in (55,100,145,167,182):
        subprocess.run([ffmpeg,'-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',
                        str(REVIEW/f'decoded-{t}.png')],check=True)
    report={'frame_count':count,'duration_seconds':seconds,'size':meta['size'],'fps':meta['fps'],
            'decode':'passed','video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
            'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'math_sha256':hashlib.sha256(Path(model.__file__).read_bytes()).hexdigest(),
            'decoded_contact_sheet_times':times}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    preview()
    if args.render: encode()
    if args.check: check()
