"""Complex Fourier partners sweep between the two localization limits.

The finite states are normalized Gaussians under the unitary Fourier transform:
psi(x) = (2*pi*sigma_x^2)^(-1/4) exp(-(x-x0)^2/(4*sigma_x^2))
         exp(i*k0*(x-x0)).
psi_tilde(k) = sqrt(2)*sigma_x*(2*pi*sigma_x^2)^(-1/4)
               exp(-sigma_x^2*(k-k0)^2) exp(-i*k*x0).
sigma_k = 1/(2*sigma_x). Both coordinate centers remain fixed.

Only display heights are peak-rescaled, explicitly labeled in the movie.
Horizontal scales and the camera stay fixed. Endpoint delta spikes are
schematic; generalized plane waves and deltas are not normalized L2 states.
Gold traces the outer silhouette of the magnitude surface, without a mesh.
There are no beads, real-part-only curves, or extra phase rotations.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

import generate_symmetry_packet_phase_modes as art

np, Image, ImageDraw = art.np, art.Image, art.ImageDraw
OUT = art.OUT
NAME = "symmetry-xk-fourier-complex"
WIDTH, HEIGHT, SS = 1440, 900, art.SS
FPS, DURATION = 30, 12.
FRAMES = round(FPS*DURATION)
BG, PANEL, INK, MUTED = art.BG, art.PANEL, art.INK, art.MUTED
BLUE, GOLD, AXIS, BORDER = art.BLUE, art.GOLD, art.AXIS, art.BORDER
GREEN = (48,119,98)
COLORS = (BLUE,GREEN)
text, line, curve, arrow, px = art.text, art.line, art.curve, art.arrow, art.px
X0, K0 = 8., 3*math.pi  # Both phase ramps are nonzero; x0*k0 is a whole turn.
MAX_LOG = 3.6
Q = np.linspace(-4.8,4.8,4801)
LEFT = (84.,792.)
SPAN = 560.
BASELINE, GAIN, DEPTH = 420., 125., .26
CAMERA = np.exp(-1j*math.radians(25))
SAMPLES = (0.,2.45,3.25,5.9,8.75,10.4)


def state(t):
    if t<=1.2: return MAX_LOG,"k",0
    if t<5.3: return MAX_LOG*(1-2*art.eased((t-1.2)/4.1)),None,1
    if t<=6.7: return -MAX_LOG,"x",2
    if t<10.8: return MAX_LOG*(2*art.eased((t-6.7)/4.1)-1),None,3
    return MAX_LOG,"k",4


def widths(log_width):
    sx=math.exp(log_width)/math.sqrt(2)
    return sx,.5/sx


def psi(x,sigma):
    return (2*np.pi*sigma**2)**(-.25)*np.exp(
        -(x-X0)**2/(4*sigma**2)+1j*K0*(x-X0))


def fourier(k,sigma):
    return np.sqrt(2)*sigma*(2*np.pi*sigma**2)**(-.25)*np.exp(
        -sigma**2*(k-K0)**2-1j*k*X0)


def screen_x(q,col):
    return LEFT[col]+(np.asarray(q)+4.8)*SPAN/9.6


def project(q,z,col):
    w=np.asarray(z)*CAMERA
    return np.column_stack((screen_x(q,col)+GAIN*DEPTH*w.imag,
                            BASELINE-GAIN*w.real))


def spiral(d,z,col,alpha=1.):
    points=project(Q,z,col)
    front=(z[:-1]*CAMERA+z[1:]*CAMERA).imag>=0
    cuts=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
    color=COLORS[col]
    pale=tuple(round(.45*c+.55*p) for c,p in zip(color,PANEL))
    for side,ink in ((False,pale),(True,color)):
        for start,end in zip(cuts[:-1],cuts[1:]):
            if bool(front[start])==side:
                curve(d,points[start:end+1],(*ink,round(255*alpha)),2.5)


@lru_cache(384)
def envelope(width):
    # Silhouette of the union of projected transverse disks. Adaptive sampling
    # resolves narrow Gaussians without scanning a huge uniform disk grid.
    q=np.unique(np.r_[np.linspace(-4.8,4.8,801),
        np.clip(np.linspace(-8*width,8*width,801),-4.8,4.8)])
    radius=GAIN*np.exp(-q*q/(4*width*width))
    centers=screen_x(q,0)
    low=float(np.min(centers-DEPTH*radius))
    high=float(np.max(centers+DEPTH*radius))
    sx=low+(high-low)*(1-np.cos(np.linspace(0,np.pi,1401)))/2
    h=np.sqrt(np.maximum(0,np.max(radius[:,None]**2-
        ((sx[None,:]-centers[:,None])/DEPTH)**2,axis=0)))
    return np.vstack((np.column_stack((sx,BASELINE-h)),
        np.column_stack((sx[::-1],BASELINE+h[::-1]))))


def key(d,col):
    origin=np.array([LEFT[col]+35,640.])
    theta=math.radians(25)
    for label,delta,offset,anchor in (
        ("x" if col==0 else "k",np.array([61.,0.]),(9.,0.),"lm"),
        ("Re",np.array([-DEPTH*math.sin(theta),-math.cos(theta)])*45,(-4.,-5.),"rb"),
        ("Im",np.array([DEPTH*math.cos(theta),-math.sin(theta)])*45,(8.,-5.),"lb"),
    ):
        tip=origin+delta
        arrow(d,origin,tip,(*MUTED,175),1.1,5)
        text(d,tip+offset,label,14,MUTED,anchor=anchor)


@lru_cache(None)
def background():
    image=Image.new("RGB",(WIDTH*SS,HEIGHT*SS),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,25),"Fourier duality works in both directions",32,bold=True)
    text(d,(40,79),"One complex function, two representations",20,MUTED)
    line(d,(1078,94),(1113,94),GOLD,1.3)
    text(d,(1125,81),"magnitude envelope",18,GOLD)
    for col,(title,symbol) in enumerate((("Position representation","x"),("Wave-number representation","k"))):
        offset=708*col
        d.rounded_rectangle(px((28+offset,136,704+offset,804)),radius=14*SS,
            fill=PANEL,outline=BORDER,width=SS)
        text(d,(54+offset,158),title,25,bold=True)
        art.paste_formula(image,(54+offset,210),r"$\psi(x)$" if col==0 else r"$\widetilde\psi(k)$",25,COLORS[col])
        line(d,(LEFT[col]-4,BASELINE),(LEFT[col]+SPAN+4,BASELINE),(*AXIS,150),.8)
        # A separate coordinate ruler makes it clear that the transverse tilt
        # is complex amplitude, not a shift of the coordinate center.
        ruler=577.
        arrow(d,(LEFT[col],ruler),(LEFT[col]+SPAN,ruler),AXIS,1.,6)
        center=float(screen_x(0,col))
        line(d,(center,ruler-4),(center,ruler+4),AXIS,1.)
        art.paste_formula(image,(center,ruler+10),r"$x_0$" if col==0 else r"$k_0$",18,MUTED,centered=True)
        text(d,(LEFT[col]+SPAN+10,ruler),symbol,18,MUTED,anchor="lm")
        key(d,col)
    text(d,(40,833),"Curve heights rescaled; horizontal scales fixed. Ideal spikes are schematic.",16,MUTED)
    return image


def draw_representation(d,col,width,ideal):
    phase=K0*Q if col==0 else -X0*(Q+K0)
    target_spike=(ideal=="x" and col==0) or (ideal=="k" and col==1)
    target_wave=ideal is not None and not target_spike
    if target_spike:
        phase0=0. if col==0 else -X0*K0
        origin=project(np.array([0.]),np.array([0j]),col)[0]
        tip=project(np.array([0.]),np.array([np.exp(1j*phase0)]),col)[0]
        arrow(d,origin,tip,COLORS[col],2.7,10)
        return
    amp=np.ones_like(Q) if target_wave else np.exp(-Q*Q/(4*width*width))
    # Let the nonphysical, independently rotated silhouette fade before the
    # narrow function tends to a delta. Keep the actual complex curve intact.
    opacity=float(np.clip((math.log(width)+3.5)/1.3,0,1))
    outline=envelope(1e5 if target_wave else width).copy()
    outline[:,0]+=LEFT[col]-LEFT[0]
    curve(d,outline,(*GOLD,round(205*opacity)),1.15)
    spiral(d,amp*np.exp(1j*phase),col)


def frame(t):
    log_width,ideal,stage=state(t)
    sx,sk=widths(log_width)
    image=background().copy()
    d=ImageDraw.Draw(image,"RGBA")
    for col,width in enumerate((sx,sk)):
        draw_representation(d,col,width,ideal)
    if ideal=="k":
        labels=("One wave number · spread throughout x","Localized at one wave number")
        formula=(r"$\psi(x)\propto e^{ik_0(x-x_0)}$",r"$\widetilde\psi(k)\propto\delta(k-k_0)$")
    elif ideal=="x":
        labels=("Localized at one position","One position · spread throughout k")
        formula=(r"$\psi(x)\propto\delta(x-x_0)$",r"$\widetilde\psi(k)\propto e^{-ikx_0}$")
    else:
        labels=("Narrower in position","Broader in wave number") if stage==1 else (
            "Broader in position","Narrower in wave number")
        formula=(r"$\Delta x$",r"$\Delta k$")
    for col in range(2):
        center=366+708*col
        text(d,(center,681),labels[col],21,COLORS[col],anchor="ma")
        if ideal:
            art.paste_formula(image,(center,727),formula[col],24,centered=True)
        else:
            # Compact live readout; sigma is the spread of squared magnitude.
            art.paste_formula(image,(center-38,730),formula[col],23,COLORS[col])
            text(d,(center+11,727),f"= {(sx,sk)[col]:.2f}",23,MUTED)
    status="Ideal Fourier limit" if ideal else "Gaussian Fourier partners"
    text(d,(1379,256),status,16,MUTED,anchor="ra")
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def check():
    errors,norms,products=[],[],[]
    for log_width in np.linspace(-MAX_LOG,MAX_LOG,13):
        sx,sk=widths(float(log_width))
        q=np.linspace(-12*sx,12*sx,32768,endpoint=False)
        dx=q[1]-q[0]
        kk=2*np.pi*np.fft.fftshift(np.fft.fftfreq(len(q),d=dx))
        values=psi(q+X0,sx)
        numerical=dx/np.sqrt(2*np.pi)*np.fft.fftshift(np.fft.fft(np.fft.ifftshift(values)))*np.exp(-1j*kk*X0)
        analytic=fourier(kk,sx)
        errors.append(float(np.max(abs(numerical-analytic))/np.max(abs(analytic))))
        norms.append(abs(float(np.trapezoid(abs(values)**2,q))-1))
        norms.append(abs(float(np.trapezoid(abs(analytic)**2,kk))-1))
        vx=float(np.trapezoid(q*q*abs(values)**2,q))
        vk=float(np.trapezoid((kk-K0)**2*abs(analytic)**2,kk))
        products.append(abs(np.sqrt(vx*vk)-.5))
    assert max(errors)<1e-9 and max(norms)<1e-9 and max(products)<1e-9
    assert abs(np.exp(-1j*X0*K0)-1)<1e-12
    assert state(0)==state(1.2) and state(5.3)==state(6.7)
    report={"max_relative_complex_fourier_error":max(errors),"max_norm_error":max(norms),
        "max_uncertainty_product_error":max(products),"x0":X0,"k0":K0,
        "sigma_x_range":list(widths(-MAX_LOG)),"display_peak_rescaled":True,
        "fixed_horizontal_scales":True,"full_complex_curve":True,
        "endpoint_deltas_schematic":True,"duration":DURATION,"fps":FPS,"frames":FRAMES,
        "size":[WIDTH,HEIGHT]}
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
    frame(3.25).save(OUT/f"{NAME}-poster.png")
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
    previous,raw=None,None
    try:
        for i in range(FRAMES):
            t=i/FPS
            current=state(t)
            if current!=previous:
                raw=frame(t).tobytes()
                previous=current
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
