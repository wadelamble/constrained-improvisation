"""One exact finite x-k loop, drawn as a full complex function.

Chronology: Tk(b), Tx(a), Tk(-b), Tx(-a), with Tx(a)f(x)=f(x-a).
The terminal function is exp(-iab)f0; ab=pi/2. No residual-phase replay.
The camera is fixed. The gray reference is always the original function.
Gold is the silhouette of the magnitude surface; there is no internal mesh.
No beads, tracked curve points, renormalization, or physical-time evolution.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

import generate_symmetry_packet_phase_modes as art

np = art.np
Image, ImageDraw = art.Image, art.ImageDraw
OUT = art.OUT
NAME = "symmetry-ccr-loop-complex"
WIDTH, HEIGHT, SS = 1440, 900, art.SS
FPS = 30
INTRO, LEG, END_HOLD = 1., 3., 3.
CLOSE = INTRO+4*LEG
DURATION = CLOSE+END_HOLD
FRAMES = round(DURATION*FPS)
A = 1.25
B = math.pi/(2*A)
SIGMA, K0 = .85, 10.
XMIN, XMAX = -4.8, 5.8
X = np.linspace(XMIN, XMAX, 2401)
PLOT_LEFT, PLOT_RIGHT = 403., 1367.
BASELINE, GAIN, DEPTH = 413., 122., .30
CAMERA = np.exp(-1j*math.radians(25))
BG, PANEL = art.BG, art.PANEL
INK, MUTED, BORDER = art.INK, art.MUTED, art.BORDER
BLUE, GOLD, AXIS = art.BLUE, art.GOLD, art.AXIS
PURPLE = (111,78,143)
GRAY = (163,158,148)
BACK_BLUE = tuple(round(.38*c+.62*p) for c,p in zip(BLUE,PANEL))
text, line, curve = art.text, art.line, art.curve
arrow, px = art.arrow, art.px
SAMPLES = (0., 3.9, 6.9, 9.9, 12.3, 15.5)


def initial(x):
    x=np.asarray(x)
    return np.exp(-x*x/(4*SIGMA**2)+1j*K0*x)


def parameters(seconds):
    if seconds<=INTRO:
        return 0.,0.,0.,0,0.
    if seconds>=CLOSE:
        return 0.,0.,-A*B,5,1.
    elapsed=seconds-INTRO
    leg=min(3,int(elapsed//LEG))
    s=art.eased((elapsed-leg*LEG)/LEG)
    if leg==0: return 0.,B*s,0.,1,s
    if leg==1: return A*s,B,-A*B*s,2,s
    if leg==2: return A,B*(1-s),-A*B,3,s
    return A*(1-s),0.,-A*B,4,s


def value(x,u,v,gamma):
    return np.exp(1j*(v*np.asarray(x)+gamma))*initial(np.asarray(x)-u)


def screen_x(x):
    return PLOT_LEFT+(np.asarray(x)-XMIN)/(XMAX-XMIN)*(PLOT_RIGHT-PLOT_LEFT)


def project(x,z):
    w=np.asarray(z)*CAMERA
    return np.column_stack((screen_x(x)+GAIN*DEPTH*w.imag,
                            BASELINE-GAIN*w.real))


def dashed(d,points,color,width=1.1,dash=7.,gap=6.):
    # Use screen arc length, so the dashes stay consistent along a helix.
    drawing=True
    remaining=dash
    for p,q in zip(points[:-1],points[1:]):
        delta=q-p
        length=float(np.linalg.norm(delta))
        if length<1e-9: continue
        unit=delta/length
        used=0.
        while used<length-1e-8:
            take=min(remaining,length-used)
            if drawing: line(d,p+used*unit,p+(used+take)*unit,color,width)
            used+=take
            remaining-=take
            if remaining<=1e-8:
                drawing=not drawing
                remaining=dash if drawing else gap


def complex_curve(d,z):
    points=project(X,z)
    depth=(z*CAMERA).imag
    front=depth[:-1]+depth[1:]>=0
    cuts=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
    for side,color in ((False,BACK_BLUE),(True,BLUE)):
        for start,end in zip(cuts[:-1],cuts[1:]):
            if bool(front[start])==side:
                curve(d,points[start:end+1],color,2.8)


@lru_cache(None)
def magnitude_outline():
    # Outline of the projected union of all transverse magnitude disks.
    xs=np.linspace(-4.8,4.8,1601)
    radius=GAIN*np.exp(-xs*xs/(4*SIGMA**2))
    centers=screen_x(xs)
    lo=float(np.min(centers-DEPTH*radius))
    hi=float(np.max(centers+DEPTH*radius))
    unit=(1-np.cos(np.linspace(0,np.pi,1801)))/2
    sx=lo+(hi-lo)*unit
    h=np.sqrt(np.maximum(0,np.max(radius[:,None]**2-
        ((sx[None,:]-centers[:,None])/DEPTH)**2,axis=0)))
    return np.vstack((np.column_stack((sx,BASELINE-h)),
        np.column_stack((sx[::-1],BASELINE+h[::-1]))))


def key(d):
    # Complex-plane axes are amplitude directions, not two extra spatial axes.
    origin=np.array([453.,578.])
    theta=math.radians(25)
    for label,delta,offset,anchor in (
        ("x",np.array([61.,0.]),(10.,0.),"lm"),
        ("Re",np.array([-DEPTH*math.sin(theta),-math.cos(theta)])*49,(-5.,-5.),"rb"),
        ("Im",np.array([DEPTH*math.cos(theta),-math.sin(theta)])*49,(9.,-6.),"lb"),
    ):
        tip=origin+delta
        arrow(d,origin,tip,(*MUTED,190),1.2,5)
        text(d,tip+offset,label,15,MUTED,anchor=anchor)


@lru_cache(None)
def background():
    image=Image.new("RGB",(WIDTH*SS,HEIGHT*SS),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,25),"A closed loop leaves a phase",32,bold=True)
    text(d,(40,77),"The shifts return to zero. The complex function retains a turn.",19,MUTED)
    for box in ((28,136,343,817),(363,136,1412,817)):
        d.rounded_rectangle(px(box),radius=14*SS,fill=PANEL,outline=BORDER,width=SS)
    text(d,(50,157),"The x–k loop",25,bold=True)
    text(d,(389,157),"Complex wave function",25,bold=True)
    # Compact legend, with the actual visual styles.
    for x,label,color in ((391,"original",GRAY),(607,"current",BLUE),(823,"magnitude envelope",GOLD)):
        if color==GRAY: dashed(d,np.array([[x,209.],[x+30,209.]]),color,1.2)
        else: line(d,(x,209),(x+30,209),color,2 if color==BLUE else 1.3)
        text(d,(x+42,197),label,17,color)
    line(d,(PLOT_LEFT,BASELINE),(PLOT_RIGHT,BASELINE),(*AXIS,120),.8)
    # Reference curve and envelope are stationary throughout the entire movie.
    dashed(d,magnitude_outline(),(*GRAY,100),.8,dash=5,gap=7)
    dashed(d,project(X,initial(X)),(*GRAY,220),1.2)
    key(d)
    ruler=624.
    line(d,(PLOT_LEFT,ruler),(PLOT_RIGHT,ruler),AXIS,1.)
    for x in (-4,-2,0,2,4):
        sx=float(screen_x(x))
        line(d,(sx,ruler-4),(sx,ruler+4),AXIS,1.)
        text(d,(sx,ruler+12),str(x).replace("-","−"),15,MUTED,anchor="ma")
    text(d,(PLOT_RIGHT+12,ruler),"x",18,MUTED,anchor="lm")
    # Fixed parameter rectangle; its cursor is not a marker on the function.
    left,right,top,bottom=87.,277.,252.,420.
    line(d,(left-18,bottom),(right+13,bottom),AXIS,1.2)
    line(d,(left,bottom+15),(left,top-18),AXIS,1.2)
    d.rectangle(px((left,top,right,bottom)),outline=(*GRAY,110),width=SS)
    text(d,(left-13,bottom+12),"0",15,MUTED,anchor="ra")
    text(d,(right,bottom+12),"a",18,MUTED,anchor="ma")
    text(d,(left-13,top),"b",18,MUTED,anchor="rm")
    text(d,(right+20,bottom),"Δx",17,MUTED,anchor="lm")
    text(d,(left,top-35),"Δk",17,MUTED,anchor="mm")
    text(d,(40,848),"Continuous translations along the four sides; a fixed view of (x, Re ψ, Im ψ).",15,MUTED)
    return image


def draw_loop(d,u,v,leg,s):
    vertices=np.array([[87.,420.],[87.,252.],[277.,252.],[277.,420.],[87.,420.]])
    completed=4 if leg==5 else max(0,leg-1)
    for j in range(completed):
        arrow(d,vertices[j],vertices[j+1],GOLD if j%2==0 else BLUE,3.,9)
    cursor=np.array([87.+190*u/A,420.-168*v/B])
    if 1<=leg<=4:
        arrow(d,vertices[leg-1],cursor,GOLD if leg%2 else BLUE,3.,9)
    art.dot(d,cursor,PURPLE,5.5,outline=PANEL)
    text(d,(58,463),f"Δx = {u:.2f}",19,BLUE)
    text(d,(204,463),f"Δk = {v:.2f}",19,GOLD)
    formulas=(r"$T_k(b)$",r"$T_x(a)$",r"$T_k(-b)$",r"$T_x(-a)$")
    labels=("shift in k","shift in x","return in k","return in x")
    for j in range(4):
        y=521+j*57
        active=(leg==j+1)
        color=GOLD if j%2==0 else BLUE
        if active:
            d.rounded_rectangle(px((48,y-4,324,y+43)),radius=6*SS,
                fill=(*color,15),outline=(*color,120),width=SS)
        text(d,(61,y+6),str(j+1),16,color if active or j<completed else MUTED,bold=active)
        text(d,(171,y+6),labels[j],17,INK if active else MUTED)
    text(d,(184,779),"loop closed" if leg==5 else "",19,PURPLE,bold=True,anchor="mm")


def frame(seconds):
    u,v,gamma,leg,s=parameters(seconds)
    image=background().copy()
    d=ImageDraw.Draw(image,"RGBA")
    outline=magnitude_outline().copy()
    outline[:,0]+=u*(PLOT_RIGHT-PLOT_LEFT)/(XMAX-XMIN)
    curve(d,outline,(*GOLD,205),1.2)
    complex_curve(d,value(X,u,v,gamma))
    draw_loop(d,u,v,leg,s)
    for j,formula in enumerate((r"$T_k(b)$",r"$T_x(a)$",r"$T_k(-b)$",r"$T_x(-a)$")):
        art.paste_formula(image,(91,521+j*57),formula,18,GOLD if j%2==0 else BLUE)
    if leg==5:
        text(d,(885,681),"Same envelope. A quarter-turn of phase remains.",22,PURPLE,anchor="ma")
        art.paste_formula(image,(887,732),r"$\psi_{\rm final}(x)=e^{-i\pi/2}\psi_0(x)$",27,centered=True)
    else:
        caption=("Start", "Shift in wave number", "Shift in position", "Return in wave number", "Return in position")[leg]
        text(d,(885,681),caption,22,MUTED,anchor="ma")
        art.paste_formula(image,(887,732),r"$T_x(-a)\,T_k(-b)\,T_x(a)\,T_k(b)\,\psi_0$",25,centered=True)
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def check():
    # Check intermediate states against direct operator composition, not just endpoints.
    xx=np.linspace(-7,8,5001)
    errors=[]
    norm_errors=[]
    for t in np.linspace(0,DURATION,161):
        u,v,gamma,leg,s=parameters(t)
        z=value(xx,u,v,gamma)
        if leg==0: direct=initial(xx)
        elif leg==1: direct=np.exp(1j*B*s*xx)*initial(xx)
        elif leg==2: direct=np.exp(1j*B*(xx-A*s))*initial(xx-A*s)
        elif leg==3: direct=np.exp(-1j*B*s*xx)*np.exp(1j*B*(xx-A))*initial(xx-A)
        elif leg==4:
            w=xx+A*s
            direct=np.exp(-1j*B*w)*np.exp(1j*B*(w-A))*initial(w-A)
        else: direct=np.exp(-1j*A*B)*initial(xx)
        errors.append(float(np.max(abs(z-direct))))
        norm_errors.append(abs(float(np.trapezoid(abs(z)**2,xx))-math.sqrt(2*np.pi)*SIGMA))
        assert np.max(abs(abs(z)-abs(initial(xx-u))))<1e-12
    # Fourier check separately verifies that the spectral envelope only translates by v.
    grid=np.linspace(-16,16,32768,endpoint=False)
    dx=grid[1]-grid[0]
    kk=2*np.pi*np.fft.fftshift(np.fft.fftfreq(len(grid),d=dx))
    spectral_errors=[]
    for t in (0.,2.5,5.5,8.5,11.5,13.):
        u,v,gamma,_,_=parameters(t)
        ft=dx*np.fft.fftshift(np.fft.fft(np.fft.ifftshift(value(grid,u,v,gamma))))
        analytic=2*SIGMA*np.sqrt(np.pi)*np.exp(-SIGMA**2*(kk-v-K0)**2)*np.exp(1j*(gamma-(kk-v)*u))
        spectral_errors.append(float(np.max(abs(ft-analytic))))
    assert max(errors)<1e-12 and max(spectral_errors)<1e-10
    assert max(norm_errors)<1e-9
    assert abs(A*B-np.pi/2)<1e-14
    assert parameters(CLOSE)==parameters(DURATION)
    assert np.max(abs(value(X,*parameters(CLOSE)[:3])+1j*initial(X)))<1e-12
    report={"loop_order":["+k","+x","-k","-x"],"a":A,"b":B,
        "residual_phase_radians":-A*B,"initial_function":"exp(-x^2/(4 sigma^2))*exp(i k0 x)",
        "sigma":SIGMA,"k0":K0,"max_direct_composition_error":max(errors),
        "max_fourier_error":max(spectral_errors),"max_norm_error":max(norm_errors),
        "duration":DURATION,"fps":FPS,"frames":FRAMES,"size":[WIDTH,HEIGHT],
        "loop_closes_seconds":CLOSE,"final_state_is_held_without_replay":True,
        "intermediate_gamma_is_not_presented_as_residual_phase":True,
        "full_complex_curve":True,"camera_fixed":True,"curve_beads":False}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,1350),BG)
    for i,t in enumerate(SAMPLES):
        pic=frame(t)
        pic.save(OUT/f"{NAME}-check-{i}.png")
        sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),((i%2)*720,(i//2)*450))
    frame(15.5).save(OUT/f"{NAME}-poster.png")
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    output=OUT/f"{NAME}.mp4"
    cmd=[art.imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-f","rawvideo",
        "-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),"-i","-",
        "-an","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
        "-movflags","+faststart",str(output)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start=time.perf_counter()
    key,raw=None,None
    try:
        for i in range(FRAMES):
            t=i/FPS
            state=parameters(t)
            if state!=key:
                raw=frame(t).tobytes()
                key=state
            process.stdin.write(raw)
            if i%(3*FPS)==0: print(f"{t:g}/{DURATION:g}s, elapsed {time.perf_counter()-start:.1f}s",flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors="replace")
        if process.wait(): raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    print(str(output),flush=True)


def encoded_check():
    reader=art.imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta=next(reader)
    assert tuple(meta["size"])==(WIDTH,HEIGHT) and abs(meta["fps"]-FPS)<1e-8
    samples={round(t*FPS) for t in SAMPLES}
    sheet=Image.new("RGB",(1440,1350),BG)
    count,errors=0,[]
    for i,raw in enumerate(reader):
        count+=1
        if i not in samples: continue
        decoded=np.frombuffer(raw,np.uint8).reshape(HEIGHT,WIDTH,3)
        error=float(np.mean(abs(decoded.astype(float)-np.asarray(frame(i/FPS)).astype(float))))
        assert error<2.5
        pic=Image.fromarray(decoded.copy())
        slot=len(errors)
        sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),((slot%2)*720,(slot//2)*450))
        if slot==len(samples)-1: pic.save(OUT/f"{NAME}-encoded-final.png")
        errors.append(error)
    assert count==FRAMES and len(errors)==len(SAMPLES)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration":count/FPS,"size":meta["size"],
        "fps":meta["fps"],"max_decoded_rgb_error":max(errors)}
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
