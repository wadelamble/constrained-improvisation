"""A common phase change of a packet and exactly nine constituent modes.

Both panes plot real parts in position space, with identical horizontal and
amplitude scales. All nine complex mode contributions are included in the sum.
The actual |sum| envelope stays fixed under a common multiplication by exp(iφ).
Modes have integer k=3,...,11; one spatial period [-π,π] is shown. This finite
Fourier packet repeats outside the view; it is not a compactly supported wave.

The phase counter is a transformation parameter, not physical time evolution.
Gold dots track one crest of each pure mode; they are not particle markers.
They wrap across the displayed spatial period as five phase turns accumulate.
The single amplitude normalization is fixed before animation starts.
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
PACKAGES = ROOT / ".tools" / "animation-python-packages"
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import matplotlib
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-packet-phase-modes"
WIDTH, HEIGHT, SS = 1440, 1080, 2
FPS = 30
PHASE_TURNS = 5
INTRO, MOVE, HOLD, END_HOLD = 1., 3.5, .5, 1.
DURATION = INTRO + 4*(MOVE+HOLD) + END_HOLD
FRAMES = round(FPS*DURATION)
BG, PANEL = (253,250,244), (250,247,240)
INK, MUTED, BORDER = (37,38,40), (111,108,102), (218,211,200)
BLUE, GOLD, AXIS = (43,93,145), (192,128,25), (207,203,195)
PANELS = ((28,136,704,942),(736,136,1412,942))
XMIN, XMAX = -math.pi, math.pi
X = np.linspace(XMIN,XMAX,1201)
K = np.arange(3,12)
M = K-7
WEIGHTS = np.exp(-M*M/(2*2.2**2))
INITIAL_PHASES = .10*M*M + .012*M*M*M
FINE_X = np.linspace(XMIN,XMAX,32769)
RAW_FINE = np.sum(WEIGHTS[:,None]*np.exp(1j*(K[:,None]*FINE_X+INITIAL_PHASES[:,None])),axis=0)
FIXED_NORMALIZER = float(np.max(abs(RAW_FINE)))
A = WEIGHTS/FIXED_NORMALIZER
BASE_MODES = A[:,None]*np.exp(1j*(K[:,None]*X+INITIAL_PHASES[:,None]))
BASE_PACKET = BASE_MODES.sum(axis=0)
ENVELOPE = abs(BASE_PACKET)
GAIN = 150.0
PACKET_BASELINE = 537.
ROW_Y = np.arange(9)*76.+233.
PLOT_LEFT = (76.,784.)
PLOT_WIDTH = 590.
PIXEL_X = [(X-XMIN)/(XMAX-XMIN)*PLOT_WIDTH+left for left in PLOT_LEFT]
AXIS_Y = 908.
CONTENT_BOTTOM, CONTROLS_SAFE_TOP = 977, 980


@lru_cache(None)
def font(size,bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf",
                 "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name,round(size*SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(v*SS) for v in values)


def text(d,xy,value,size=20,color=INK,bold=False,anchor=None):
    d.text(px(xy),value,fill=color,font=font(size,bold),anchor=anchor)


def line(d,a,b,color,width=1):
    d.line(px((*a,*b)),fill=color,width=max(1,round(width*SS)))


def curve(d,points,color,width=1.5):
    flat=np.rint(np.asarray(points)*SS).astype(int).ravel().tolist()
    d.line(flat,fill=color,width=max(1,round(width*SS)),joint="curve")


def dot(d,xy,color,radius=3.5,outline=None):
    x,y=xy
    d.ellipse(px((x-radius,y-radius,x+radius,y+radius)),
              fill=color,outline=outline,width=SS)


def arrow(d,a,b,color,width=2.5,head=9):
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    delta=b-a
    norm=float(np.linalg.norm(delta))
    if norm<1e-9:
        return
    u=delta/norm
    v=np.array([-u[1],u[0]])
    line(d,a,b,color,width)
    d.polygon([px(b),px(b-head*u+.43*head*v),px(b-head*u-.43*head*v)],fill=color)


@lru_cache(None)
def formula(expression,size=21,color=INK):
    buffer=BytesIO()
    with matplotlib.rc_context({"savefig.transparent":True}):
        math_to_image(expression,buffer,prop=FontProperties(size=size),dpi=72*SS,
                      format="png",color="#%02x%02x%02x"%color)
    buffer.seek(0)
    return Image.open(buffer).convert("RGBA")


def paste_formula(image,xy,expression,size=21,color=INK,centered=False):
    pic=formula(expression,size,color)
    x,y=px(xy)
    if centered:
        x-=pic.width//2
    image.paste(pic,(x,y),pic)


def eased(u):
    u=float(np.clip(u,0,1))
    ramp=.08
    if u<ramp:
        return u*u/(2*ramp*(1-ramp))
    if u>1-ramp:
        return 1-(1-u)**2/(2*ramp*(1-ramp))
    return (u-ramp/2)/(1-ramp)


def phase_at(seconds):
    if seconds<=INTRO:
        return 0.
    elapsed=seconds-INTRO
    quarter=int(elapsed//(MOVE+HOLD))
    if quarter>=4:
        return PHASE_TURNS*2*math.pi
    progress=eased((elapsed-quarter*(MOVE+HOLD))/MOVE)
    return PHASE_TURNS*(quarter+progress)*math.pi/2


def crest_positions(phase):
    unwrapped=-(INITIAL_PHASES+phase)/K
    return (unwrapped-XMIN)%(XMAX-XMIN)+XMIN


def map_x(x,col):
    return PLOT_LEFT[col]+(x-XMIN)/(XMAX-XMIN)*PLOT_WIDTH


@lru_cache(None)
def background():
    image=Image.new("RGB",(WIDTH*SS,HEIGHT*SS),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,25),"One phase change, nine modes",32,bold=True)
    text(d,(40,77),"The packet stays put while every mode advances by the same phase.",19,MUTED)
    for box in PANELS:
        d.rounded_rectangle(px(box),radius=14*SS,fill=PANEL,outline=BORDER,width=SS)
    text(d,(52,153),"Packet · exact sum",25,bold=True)
    text(d,(54,192),"The envelope stays fixed",19,GOLD)
    text(d,(760,153),"Nine pure modes",25,bold=True)
    text(d,(762,191),"Each gold dot follows one crest",17,MUTED)
    # An exact, stationary reference drawn from the same complex sum.
    for sign in (-1,1):
        curve(d,np.column_stack((PIXEL_X[0],PACKET_BASELINE-sign*GAIN*ENVELOPE)),(*GOLD,220),1.8)
    line(d,(PLOT_LEFT[0],PACKET_BASELINE),(PLOT_LEFT[0]+PLOT_WIDTH,PACKET_BASELINE),(*AXIS,200))
    xzero=map_x(0,0)
    line(d,(xzero,PACKET_BASELINE-GAIN-25),(xzero,PACKET_BASELINE+GAIN+25),(*AXIS,135))
    for value in (-1,-.5,0,.5,1):
        y=PACKET_BASELINE-GAIN*value
        line(d,(PLOT_LEFT[0]-3,y),(PLOT_LEFT[0]+2,y),AXIS)
        text(d,(PLOT_LEFT[0]-9,y),f"{value:g}",13,MUTED,anchor="rm")
    text(d,(PLOT_LEFT[0],PACKET_BASELINE-GAIN-57),"Re Ψ",17,BLUE)
    # Baselines and starting-crest references remain fixed in each mode row.
    for j,(k,y) in enumerate(zip(K,ROW_Y)):
        line(d,(PLOT_LEFT[1],y),(PLOT_LEFT[1]+PLOT_WIDTH,y),(*AXIS,160),.8)
        text(d,(749,y),f"k={k}",14,MUTED,anchor="lm")
        xstart=map_x(-INITIAL_PHASES[j]/k,1)
        crest_y=y-GAIN*A[j]
        dot(d,(xstart,crest_y),(*PANEL,255),2.8,(*MUTED,120))
    # Both panes use the same coordinate ruler and the same amplitude scale.
    labels=((XMIN,"−π"),(-math.pi/2,"−π/2"),(0,"0"),(math.pi/2,"π/2"),(XMAX,"π"))
    for col in range(2):
        line(d,(PLOT_LEFT[col],AXIS_Y),(PLOT_LEFT[col]+PLOT_WIDTH,AXIS_Y),AXIS,1)
        for x,label in labels:
            xp=map_x(x,col)
            line(d,(xp,AXIS_Y-4),(xp,AXIS_Y+4),AXIS,1)
            text(d,(xp,AXIS_Y+9),label,14,MUTED,anchor="ma")
        text(d,(PLOT_LEFT[col]+PLOT_WIDTH+11,AXIS_Y),"x",17,MUTED,anchor="lm")
    line(d,(84,785),(114,785),BLUE,2.8)
    text(d,(125,773),"real part",18,BLUE)
    line(d,(368,785),(398,785),GOLD,1.8)
    text(d,(409,773),"envelope: ±|Ψ|",18,GOLD)
    paste_formula(image,(366,829),r"$\Psi_{\phi}(x)=e^{i\phi}\,\Psi_0(x)$",24,centered=True)
    text(d,(39,955),"One spatial period shown · the same x and amplitude scales in both panes.",16,MUTED)
    text(d,(1400,955),"φ changes; this is not time evolution.",16,MUTED,anchor="ra")
    return image


def draw_counter(d,phase):
    center=np.array([1055.,62.])
    radius=33.
    d.ellipse(px((* (center-radius), * (center+radius))),outline=BORDER,width=SS)
    for angle in np.arange(4)*math.pi/2:
        v=np.array([math.cos(angle),-math.sin(angle)])
        line(d,center+(radius-3)*v,center+(radius+3)*v,(*MUTED,170))
    if phase>0:
        arc_phase=min(phase,2*math.pi)
        angles=np.linspace(0,arc_phase,max(2,int(arc_phase*28)))
        curve(d,[center+radius*np.array([math.cos(a),-math.sin(a)]) for a in angles],GOLD,2.1)
    tip=center+(radius-5)*np.array([math.cos(phase),-math.sin(phase)])
    arrow(d,center,tip,GOLD,2.5,7)
    degrees=math.degrees(phase)
    text(d,(1113,30),f"φ = {degrees:.1f}°",31,GOLD,bold=True)
    text(d,(1116,77),f"{phase/(2*math.pi):.2f} turns",18,MUTED)


def frame(seconds):
    phase=phase_at(seconds)
    values=BASE_MODES*np.exp(1j*phase)
    packet=values.sum(axis=0)
    image=background().copy()
    d=ImageDraw.Draw(image,"RGBA")
    curve(d,np.column_stack((PIXEL_X[0],PACKET_BASELINE-GAIN*packet.real)),BLUE,2.8)
    crests=crest_positions(phase)
    for j,y in enumerate(ROW_Y):
        curve(d,np.column_stack((PIXEL_X[1],y-GAIN*values[j].real)),BLUE,1.8)
        dot(d,(map_x(crests[j],1),y-GAIN*A[j]),GOLD,3.7)
    draw_counter(d,phase)
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def check():
    phases=np.linspace(0,PHASE_TURNS*2*math.pi,PHASE_TURNS*18+1)
    max_sum_error=max_envelope_error=max_crest_error=0.
    for phase in phases:
        direct=A[:,None]*np.exp(1j*(K[:,None]*X+INITIAL_PHASES[:,None]+phase))
        total=direct.sum(axis=0)
        max_sum_error=max(max_sum_error,float(np.max(abs(total-np.exp(1j*phase)*BASE_PACKET))))
        max_envelope_error=max(max_envelope_error,float(np.max(abs(abs(total)-ENVELOPE))))
        assert np.all(abs(total.real)<=ENVELOPE+1e-13)
        crests=crest_positions(phase)
        assert np.all((crests>=XMIN)&(crests<=XMAX))
        max_crest_error=max(max_crest_error,float(np.max(abs(np.exp(1j*(K*crests+INITIAL_PHASES+phase))-1))))
    periodic_x=np.linspace(0,2*math.pi,4096,endpoint=False)
    periodic_sum=np.sum(A[:,None]*np.exp(1j*(K[:,None]*periodic_x+INITIAL_PHASES[:,None])),axis=0)
    spectrum=np.fft.fft(periodic_sum)/len(periodic_x)
    wanted=np.zeros(len(spectrum),dtype=complex)
    wanted[K]=A*np.exp(1j*INITIAL_PHASES)
    fft_error=float(np.max(abs(spectrum-wanted)))
    parseval_error=abs(float(np.mean(abs(periodic_sum)**2))-float(np.sum(A*A)))
    closure_error=float(np.max(abs(np.exp(PHASE_TURNS*2j*math.pi)*BASE_PACKET-BASE_PACKET)))
    assert max_sum_error<1e-12 and max_envelope_error<1e-12
    assert fft_error<1e-12 and parseval_error<1e-12 and closure_error<1e-12
    assert max_crest_error<1e-12
    assert CONTENT_BOTTOM<CONTROLS_SAFE_TOP<=HEIGHT-100
    assert max(A)*GAIN < .5*np.min(np.diff(ROW_Y))-4
    density=abs(RAW_FINE)**2
    near=abs(FINE_X)<1.4
    fraction=float(np.trapezoid(density[near],FINE_X[near])/np.trapezoid(density,FINE_X))
    report={"wave_numbers":K.tolist(),"amplitudes":A.tolist(),"initial_phases":INITIAL_PHASES.tolist(),
        "fixed_normalizer":FIXED_NORMALIZER,"exactly_nine_modes":True,
        "one_period":[XMIN,XMAX],"energy_fraction_within_abs_x_1p4":fraction,
        "boundary_envelope_relative_to_peak":float(abs(RAW_FINE[0])/FIXED_NORMALIZER),
        "max_direct_sum_error":max_sum_error,"max_envelope_error":max_envelope_error,
        "max_fft_error":fft_error,"parseval_error":parseval_error,"closure_error":closure_error,
        "max_crest_phase_error":max_crest_error,
        "crest_displacements_per_full_turn":(-2*np.pi/K).tolist(),
        "common_amplitude_pixels_per_unit":GAIN,"common_x_plot_width":PLOT_WIDTH,
        "duration":DURATION,"fps":FPS,"frames":FRAMES,"size":[WIDTH,HEIGHT],
        "phase_turns":PHASE_TURNS,"phase_speed_multiplier":PHASE_TURNS,
        "content_bottom":CONTENT_BOTTOM,"controls_safe_top":CONTROLS_SAFE_TOP,
        "interpretation":"Common phase parameter, not free physical time evolution; periodic finite Fourier packet."}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    times=(0.,INTRO+MOVE,INTRO+2*(MOVE+HOLD)-HOLD,INTRO+3*(MOVE+HOLD)-HOLD,
           INTRO+4*(MOVE+HOLD)-HOLD,DURATION-1/FPS)
    sheet=Image.new("RGB",(1440,1668),BG)
    for slot,seconds in enumerate(times):
        pic=frame(seconds)
        x,y=(slot%2)*720,(slot//2)*556
        sheet.paste(pic.resize((720,540),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+12,y+540),f"{math.degrees(phase_at(seconds)):.0f} deg",fill=MUTED)
    frame(INTRO+MOVE).save(OUT/f"{NAME}-poster.png")
    frame(0.).save(OUT/f"{NAME}-initial.png")
    frame(DURATION-1/FPS).save(OUT/f"{NAME}-final.png")
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output=OUT/f"{NAME}.mp4"
    command=[imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
        "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),
        "-i","-","-an","-c:v","libx264","-preset","fast","-crf","18",
        "-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    started=time.perf_counter()
    key,rgb=None,None
    try:
        for i in range(FRAMES):
            phase=phase_at(i/FPS)
            if phase!=key:
                rgb=frame(i/FPS).tobytes()
                key=phase
            proc.stdin.write(rgb)
            if i%(3*FPS)==0:
                print(f"{i/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-started:.1f}s",flush=True)
        proc.stdin.close()
        error=proc.stderr.read().decode(errors="replace")
        if proc.wait():
            raise RuntimeError(error)
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    print(str(output),flush=True)


def encoded_check():
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta=next(reader)
    assert tuple(meta["size"])==(WIDTH,HEIGHT) and abs(meta["fps"]-FPS)<1e-8
    samples={0,round((INTRO+MOVE)*FPS),round((INTRO+2*(MOVE+HOLD)-HOLD)*FPS),
        round((INTRO+3*(MOVE+HOLD)-HOLD)*FPS),round((INTRO+4*(MOVE+HOLD)-HOLD)*FPS),FRAMES-1}
    sheet=Image.new("RGB",(1440,1620),BG)
    count,errors=0,[]
    for i,raw in enumerate(reader):
        count+=1
        if i not in samples:
            continue
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        expected=np.asarray(frame(i/FPS))
        error=float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
        assert error<2.5
        pic=Image.fromarray(decoded.copy())
        slot=len(errors)
        sheet.paste(pic.resize((720,540),Image.Resampling.LANCZOS),((slot%2)*720,(slot//2)*540))
        if i==round((INTRO+MOVE)*FPS):
            pic.save(OUT/f"{NAME}-encoded-sample.png")
        errors.append(error)
    assert count==FRAMES and len(errors)==len(samples)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration":count/FPS,"size":meta["size"],"fps":meta["fps"],
        "max_decoded_rgb_error":max(errors)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    args=parser.parse_args()
    if args.check: check()
    if args.preview: preview()
    if args.render: render()
    if args.encoded_check: encoded_check()
