"""A proposed complex plane wave: one field, three synchronized views.

The curve is the true graph (x, Re z, Im z), under a fixed parallel camera.
Playback advances physical time in z(x,t)=A exp(i(kx-omega*t)); the highlighted
spatial coordinate never moves. Two initial/final seconds hold the same state.
No manuscript, previous generator, or previous media is changed.

Run with --check --preview, inspect the PNGs, then --render --encoded-check.
All output and optional dependency paths are relative to this repository.
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
import time

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
NAME = 'symmetry-complex-plane-wave-v2'
W, H, SS, FPS, DURATION = 1440, 900, 2, 30, 12
FRAMES = FPS * DURATION
BG = (253, 250, 244)
INK, MUTED = (37, 38, 40), (111, 108, 101)
GRID, AXIS = (235, 229, 219), (176, 171, 161)
BLUE, CORAL, GOLD = (43, 93, 145), (194, 91, 72), (181, 118, 22)
HELIX = (46, 72, 94)
BACK_HELIX = tuple(round(.62*c+.38*b) for c,b in zip(HELIX,BG))
A, WAVELENGTH, PERIOD = 1., 4., 4.
K, OMEGA = 2*np.pi/WAVELENGTH, 2*np.pi/PERIOD
XMIN, XMAX, X0 = 0., 10., 5.
X = np.linspace(XMIN, XMAX, 1801)
START_HOLD, ACTIVE_DURATION = 2., 8.
LEFT, RIGHT = 135., 845.
BASELINE, GAIN, DEPTH = 347., 110., .70
VIEW_ANGLE = np.deg2rad(25.)
VIEW_ROTATION = np.exp(-1j*VIEW_ANGLE)
PLOT_Y, PLOT_GAIN = 676., 83.
DIAL_CENTER, DIAL_RADIUS = np.array([1175., 349.]), 143.
SAMPLE_TIMES = (0., 2.5, 3.5, 4.5, 5.5, 11.9)


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


def curve(d, points, color, width=1):
    d.line([px(q) for q in points], fill=color,
           width=max(1,round(width*SS)), joint='curve')


def arrow(d, a, b, color, width=3, head=11):
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    v=b-a
    length=float(np.linalg.norm(v))
    if length<1:
        return
    u=v/length
    side=np.array([-u[1],u[0]])
    head=min(head,.35*length)
    line(d,a,b-.3*head*u,color,width)
    d.polygon([px(b),px(b-head*u+.43*head*side),
               px(b-head*u-.43*head*side)],fill=color)


def dot(d, q, radius, color, halo=False):
    q=np.asarray(q,dtype=float)
    if halo:
        dot(d,q,radius+2.2,BG)
    d.ellipse(px((*(q-radius),*(q+radius))),fill=color)


def dashed(d, a, b, color, width=1, step=10, dash=4):
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    length=float(np.linalg.norm(b-a))
    if length<.1:
        return
    u=(b-a)/length
    for start in np.arange(0,length,step):
        line(d,a+start*u,a+min(start+dash,length)*u,color,width)


@lru_cache(None)
def formula(value, size=24, color=INK):
    stream=BytesIO()
    math_to_image('$'+value+'$',stream,dpi=144,
                  prop=FontProperties(size=size),format='png',
                  color=tuple(c/255 for c in color))
    rgba=np.asarray(Image.open(stream).convert('RGBA')).copy()
    alpha=(255-np.min(rgba[:,:,:3],axis=2)).astype(float)
    rgba[:,:,3]=np.minimum(255,np.round(alpha*255/(255-min(color)))).astype(np.uint8)
    rgba[:,:,:3]=color
    art=Image.fromarray(rgba)
    return art.crop(art.getbbox())


def put_math(im, pos, value, size=24, color=INK, center=False):
    art=formula(value,size,color)
    pos=np.asarray(pos,dtype=float)
    if center:
        pos=pos-[art.width/(2*SS),0]
    im.paste(art,px(pos),art)
    return art.width/SS,art.height/SS


def physical_time(playback_seconds):
    return float(np.clip(playback_seconds-START_HOLD,0.,ACTIVE_DURATION))


def wave(x, t):
    return A*np.exp(1j*(K*np.asarray(x)-OMEGA*t))


def spatial_x(x):
    return LEFT+(np.asarray(x)-XMIN)/(XMAX-XMIN)*(RIGHT-LEFT)


def project(x, value):
    """Fixed linear projection of the actual three coordinates x, Re z, Im z.

    The camera rotates the transverse coordinate plane by a fixed 25 degrees.
    Its 0.70 foreshortening gives visibly open helix loops; opacity alone is
    never used to fabricate depth from a scalar sinusoid.
    """
    value=np.asarray(value)*VIEW_ROTATION
    return np.stack((spatial_x(x)+GAIN*DEPTH*value.imag,
                     BASELINE-GAIN*value.real),axis=-1)


def component_point(x, value):
    return np.stack((spatial_x(x),PLOT_Y-PLOT_GAIN*np.asarray(value)),axis=-1)


def dial(value):
    value=np.asarray(value)
    return DIAL_CENTER+np.stack((DIAL_RADIUS*value.real,
                                -DIAL_RADIUS*value.imag),axis=-1)


def draw_helix(d, values):
    points=project(X,values)
    front=(values*VIEW_ROTATION).imag>=0
    breaks=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(X)-1]
    # Back/front tint is only a depth cue: the geometry is the projected helix.
    for side,color in ((False,BACK_HELIX),(True,HELIX)):
        for a,b in zip(breaks[:-1],breaks[1:]):
            if bool(front[a])==side:
                curve(d,points[a:b+1],color,3.0)


@lru_cache(None)
def backdrop():
    im=Image.new('RGB',(W*SS,H*SS),BG)
    d=ImageDraw.Draw(im,'RGBA')
    text(d,(48,28),'A complex plane wave',34,bold=True)
    put_math(im,(50,92),r'z(x,t)=A e^{i(kx-\omega t)}',33)
    text(d,(135,178),'Complex wave',21,MUTED)
    # A stationary cylinder shows constant pointwise modulus, not unitarity.
    theta=np.linspace(0,2*np.pi,361)
    for x in (XMIN,XMAX):
        curve(d,project(np.full(theta.shape,x),A*np.exp(1j*theta)),(*GOLD,66),1)
    for y in (BASELINE-GAIN*A,BASELINE+GAIN*A):
        line(d,(LEFT,y),(RIGHT,y),(*GOLD,70),1)
    arrow(d,(LEFT-13,BASELINE),(RIGHT+24,BASELINE),AXIS,1.2,8)
    text(d,(RIGHT+36,BASELINE),'x',21,MUTED,anchor='lm')
    # One gold cross-section is anchored to x0 throughout playback.
    curve(d,project(np.full(theta.shape,X0),A*np.exp(1j*theta)),(*GOLD,150),1.35)
    dot(d,project(X0,0j),3,GOLD)
    dashed(d,(spatial_x(X0),BASELINE+GAIN+9),(spatial_x(X0),496),(*GOLD,130),1.2)
    put_math(im,(spatial_x(X0),480),r'x_0',22,GOLD,center=True)
    # A small fixed triad identifies the helix's three coordinates.
    origin=np.array([143.,534.])
    directions=((r'x',np.array([60.,0.]),(8,-9),MUTED),
                (r'\mathrm{Re}\,z',np.array([-DEPTH*math.sin(VIEW_ANGLE),-math.cos(VIEW_ANGLE)])*45,(-13,-24),BLUE),
                (r'\mathrm{Im}\,z',np.array([DEPTH*math.cos(VIEW_ANGLE),-math.sin(VIEW_ANGLE)])*45,(7,-12),CORAL))
    for label,delta,offset,color in directions:
        arrow(d,origin,origin+delta,color,1.2,7)
        put_math(im,origin+delta+offset,label,17,color)
    # The shared spatial plot uses the same x mapping as the helix axis.
    line(d,(LEFT,PLOT_Y-PLOT_GAIN),(RIGHT,PLOT_Y-PLOT_GAIN),GRID,1)
    line(d,(LEFT,PLOT_Y+PLOT_GAIN),(RIGHT,PLOT_Y+PLOT_GAIN),GRID,1)
    arrow(d,(LEFT-8,PLOT_Y),(RIGHT+24,PLOT_Y),AXIS,1.2,8)
    for x in np.arange(XMIN,XMAX+1,2.):
        line(d,(spatial_x(x),PLOT_Y-4),(spatial_x(x),PLOT_Y+4),AXIS,1)
    for value,label in ((A,'A'),(-A,'−A')):
        text(d,(LEFT-21,PLOT_Y-PLOT_GAIN*value),label,17,MUTED,anchor='rm')
    dashed(d,(spatial_x(X0),PLOT_Y-PLOT_GAIN-14),
           (spatial_x(X0),PLOT_Y+PLOT_GAIN+12),(*GOLD,120),1.2)
    put_math(im,(spatial_x(X0),780),r'x_0',21,GOLD,center=True)
    line(d,(350,545),(382,545),BLUE,3)
    put_math(im,(393,533),r'\mathrm{Re}\,z',22,BLUE)
    line(d,(543,545),(575,545),CORAL,3)
    put_math(im,(586,533),r'\mathrm{Im}\,z',22,CORAL)
    text(d,(RIGHT+36,PLOT_Y),'x',21,MUTED,anchor='lm')
    # The bracket spans exactly lambda along the actual spatial axis.
    y=813.
    line(d,(spatial_x(0),y),(spatial_x(WAVELENGTH),y),AXIS,1.1)
    for x in (0.,WAVELENGTH):
        line(d,(spatial_x(x),y-5),(spatial_x(x),y+5),AXIS,1.1)
    put_math(im,((spatial_x(0)+spatial_x(WAVELENGTH))/2,y+10),
             r'\lambda=\frac{2\pi}{k}',23,MUTED,center=True)
    text(d,(RIGHT,823),'position x',19,MUTED,anchor='ra')
    # The round dial has exactly the same pixel scale in both components.
    line(d,(963,173),(963,804),GRID,1)
    put_math(im,(1175,150),r'z(x_0,t)',25,INK,center=True)
    curve(d,dial(A*np.exp(1j*theta)),(*GOLD,160),1.8)
    for a,b in ((-1.13+0j,1.13+0j),(-1.13j,1.13j)):
        arrow(d,dial(a),dial(b),AXIS,1.2,8)
    put_math(im,(1345,337),r'\mathrm{Re}\,z',20,BLUE)
    put_math(im,(1188,178),r'\mathrm{Im}\,z',20,CORAL)
    put_math(im,(1175,548),r'|z|=A',29,GOLD,center=True)
    put_math(im,(1175,646),r'\mathrm{Re}\,z=A\cos(kx-\omega t)',24,BLUE,center=True)
    put_math(im,(1175,702),r'\mathrm{Im}\,z=A\sin(kx-\omega t)',24,CORAL,center=True)
    return im


def frame(seconds):
    t=physical_time(seconds)
    values=wave(X,t)
    marked=wave(X0,t)
    im=backdrop().copy()
    d=ImageDraw.Draw(im,'RGBA')
    text(d,(1389,34),f't = {t:.2f} s',28,GOLD,anchor='ra')
    draw_helix(d,values)
    arrow(d,project(X0,0j),project(X0,marked),GOLD,2.8,11)
    dot(d,project(X0,marked),6.2,GOLD,halo=True)
    for component,color in ((values.real,BLUE),(values.imag,CORAL)):
        curve(d,component_point(X,component),color,2.7)
    for value,color in ((marked.real,BLUE),(marked.imag,CORAL)):
        dot(d,component_point(X0,value),5.8,color,halo=True)
    end=dial(marked)
    re,imag=dial(marked.real+0j),dial(1j*marked.imag)
    dashed(d,re,end,(*BLUE,150),1.4)
    dashed(d,imag,end,(*CORAL,150),1.4)
    line(d,DIAL_CENTER,re,BLUE,3.3)
    line(d,DIAL_CENTER,imag,CORAL,3.3)
    dot(d,re,4.4,BLUE)
    dot(d,imag,4.4,CORAL)
    arrow(d,DIAL_CENTER,end,GOLD,3.5,14)
    dot(d,DIAL_CENTER,3.8,GOLD)
    dot(d,end,6.2,GOLD,halo=True)
    return im.resize((W,H),Image.Resampling.LANCZOS)


def check():
    modulus_error=component_error=projection_error=dial_radius_error=0.
    margin=math.inf
    matrix=np.array([[1.,-GAIN*DEPTH*np.sin(VIEW_ANGLE),GAIN*DEPTH*np.cos(VIEW_ANGLE)],
                     [0.,-GAIN*np.cos(VIEW_ANGLE),-GAIN*np.sin(VIEW_ANGLE)]])
    for t in np.linspace(0,ACTIVE_DURATION,161):
        values=wave(X,t)
        modulus_error=max(modulus_error,float(np.max(abs(abs(values)-A))))
        expected_real=A*np.cos(K*X-OMEGA*t)
        expected_imag=A*np.sin(K*X-OMEGA*t)
        component_error=max(component_error,float(np.max(abs(values.real-expected_real))),
                            float(np.max(abs(values.imag-expected_imag))))
        xyz=np.column_stack((spatial_x(X),values.real,values.imag))
        independent=xyz@matrix.T+np.array([0.,BASELINE])
        projection_error=max(projection_error,float(np.max(abs(project(X,values)-independent))))
        marked=wave(X0,t)
        dial_radius_error=max(dial_radius_error,abs(float(np.linalg.norm(dial(marked)-DIAL_CENTER))-DIAL_RADIUS*A))
        # All displayed components of the fixed marked input recover its z.
        reconstructed=(dial(marked)-DIAL_CENTER)/[DIAL_RADIUS,-DIAL_RADIUS]
        assert np.max(abs(reconstructed-[marked.real,marked.imag]))<1e-14
        assert abs(component_point(X0,marked.real)[0]-spatial_x(X0))<1e-14
        assert abs(component_point(X0,marked.imag)[0]-spatial_x(X0))<1e-14
        assert abs((PLOT_Y-component_point(X0,marked.real)[1])/PLOT_GAIN-marked.real)<1e-14
        assert abs((PLOT_Y-component_point(X0,marked.imag)[1])/PLOT_GAIN-marked.imag)<1e-14
        points=project(X,values)
        margin=min(margin,float(np.min(np.column_stack((points[:,0]-48,940-points[:,0],points[:,1]-219,472-points[:,1])))))
    dt=.2
    shift=OMEGA/K*dt
    travel_error=float(np.max(abs(wave(X+shift,dt)-wave(X,0.))))
    wavelength_error=float(np.max(abs(wave(X+WAVELENGTH,0.)-wave(X,0.))))
    angles=np.unwrap(np.angle(wave(X0,np.linspace(0,ACTIVE_DURATION,161))))
    phase_step=float(np.max(np.diff(angles)))
    assert phase_step<0 and shift>0 and travel_error<1e-13
    assert max(modulus_error,component_error,wavelength_error)<1e-13
    assert projection_error<1e-11 and dial_radius_error<1e-11 and margin>9
    assert physical_time(0)==physical_time(START_HOLD)==0.
    assert physical_time(DURATION)==ACTIVE_DURATION
    # Header, side equations and display elements leave useful edge clearance.
    assert formula(r'\mathrm{Re}\,z=A\cos(kx-\omega t)',24,BLUE).width/SS<396
    report={'equation':'z(x,t)=A exp(i(k x - omega t))',
            'A':A,'k':K,'omega':OMEGA,'wavelength':WAVELENGTH,'phase_period_seconds':PERIOD,
            'spatial_range':[XMIN,XMAX],'visible_spatial_cycles':(XMAX-XMIN)/WAVELENGTH,
            'fixed_highlight_x':X0,'max_modulus_error':modulus_error,
            'max_component_error':component_error,'max_independent_3d_projection_error_px':projection_error,
            'max_dial_radius_error_px':dial_radius_error,'dial_scale_xy':[DIAL_RADIUS,DIAL_RADIUS],
            'wavelength_repeat_error':wavelength_error,'rightward_phase_speed':OMEGA/K,
            'rightward_travel_test_shift':shift,'rightward_travel_test_error':travel_error,
            'largest_phase_step_radians':phase_step,'dial_time_direction':'clockwise',
            'camera_fixed':True,'camera_transverse_rotation_degrees':25.,'camera_depth_foreshortening':DEPTH,
            'minimum_helix_clearance_px':margin,'size':[W,H],'fps':FPS,'frames':FRAMES,
            'duration_seconds':DURATION,'start_hold_seconds':START_HOLD,
            'active_physical_time_seconds':ACTIVE_DURATION,'time_phase_cycles':ACTIVE_DURATION/PERIOD,
            'end_hold_seconds':DURATION-START_HOLD-ACTIVE_DURATION,
            'meaning':'Spatial complex field at successive physical times. Constant pointwise modulus is displayed without defining unitarity.'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1440,1350),BG)
    for i,t in enumerate(SAMPLE_TIMES):
        pic=frame(t)
        sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),((i%2)*720,(i//2)*450))
    frame(3.5).save(OUT/f'{NAME}-poster.png')
    sheet.save(OUT/f'{NAME}-contact-sheet.png')
    print(str(OUT/f'{NAME}-poster.png'),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/f'{NAME}.mp4'
    proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error',
        '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
        '-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    start=time.perf_counter()
    try:
        last_t,raw=None,None
        for i in range(FRAMES):
            t=physical_time(i/FPS)
            if t!=last_t:
                raw=frame(i/FPS).tobytes()
                last_t=t
            proc.stdin.write(raw)
            if i%(FPS*2)==0:
                print(f'Rendered {i/FPS:g}/{DURATION}s; elapsed {time.perf_counter()-start:.1f}s',flush=True)
        proc.stdin.close()
        err=proc.stderr.read().decode(errors='replace')
        if proc.wait():
            raise RuntimeError(err)
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    print(str(path),flush=True)


def encoded_check():
    reader=imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'),pix_fmt='rgb24')
    meta=next(reader)
    assert tuple(meta['size'])==(W,H) and meta['fps']==FPS
    indices={min(FRAMES-1,round(t*FPS)) for t in SAMPLE_TIMES}
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
            pic=Image.fromarray(decoded)
            sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),((n%2)*720,(n//2)*450))
            if n in (0,2,4):
                pic.save(OUT/f'{NAME}-decoded-{i:03d}.png')
            errors.append(error)
    assert count==FRAMES and len(errors)==len(indices)
    sheet.save(OUT/f'{NAME}-encoded-contact-sheet.png')
    report={'decoded_frames':count,'duration_seconds':count/FPS,'size':meta['size'],
            'fps':meta['fps'],'codec':meta.get('codec'),'pixel_format':meta.get('pix_fmt'),
            'max_decoded_rgb_error':max(errors),'sample_frame_indices':sorted(indices),
            'sample_decoded_rgb_errors':errors,'file_bytes':(OUT/f'{NAME}.mp4').stat().st_size}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for flag in ('check','preview','render','encoded-check'):
        parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    if args.check: check()
    if args.preview: preview()
    if args.render: render()
    if args.encoded_check: encoded_check()
