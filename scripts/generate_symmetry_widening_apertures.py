"""Two widening apertures: diffraction develops into nearly straight beams.

One fixed plane-wave illumination, wavelength, camera, and real-field palette.
Successive thin-screen, monochromatic steady states are calculated at changing
aperture widths; this is not a transient moving-boundary simulation. The two
finite intervals are integrated in full, with a normalized forward scalar
angular-spectrum kernel including the carrier phase and evanescent decay.
Reflection, polarization, and material thickness are outside this model.

The periodic impulse response is integrated once for each downstream x. Its
antiderivative G gives a rectangle [a,b] as G(y-a)-G(y-b)+(b-a)*H(0)/L.
This evaluates the actual aperture integral as the edges move, rather than
morphing endpoint pictures or replacing each opening with a point emitter.
Only a central strip of G is retained; no full multi-frame field cache is used.

Reel colors are retained exactly. A single time-independent |Re U|^0.72 mapping
is shared by incident and transmitted fields, for every width. No per-frame
normalization, phase alignment, or separately brightened transmitted field.
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
import time

ROOT=Path(__file__).resolve().parents[1]
PACKAGES=ROOT/".tools"/"animation-python-packages"
if PACKAGES.is_dir():
    sys.path.insert(0,str(PACKAGES))
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

NAME="symmetry-widening-apertures"
OUT=ROOT/"content"/"drafts"/"animations"
CACHE=ROOT/".tools"/"animation-review"/NAME
WIDTH,HEIGHT=1440,1120
BOX=(70,88,1370,1048)
PW,PH=BOX[2]-BOX[0],BOX[3]-BOX[1]
XMIN,XMAX,YHALF=-3.,10.,4.8
WAVELENGTH=.2
K=2*math.pi/WAVELENGTH
CENTERS=(-2.7,2.7)
OPENINGS=(.12,.35,.75,1.4,2.4,3.4)
PERIOD,N=512.,131072
FPS,DURATION,WAVE_PERIOD=30,20.,1.2
FRAMES=round(FPS*DURATION)
# Every new width receives two seconds of motion and one second to read it.
# The first configuration gets two seconds; the final beams get four.
TRANSITIONS=((2.,4.),(5.,7.),(8.,10.),(11.,13.),(14.,16.))
SAMPLES=(.7,4.5,7.5,10.5,13.5,18.5)
BG=(3,3,8)
POSITIVE=(255,42,91)
NEGATIVE=(37,137,255)
INK=(249,239,229)
MUTED=(162,153,174)
GOLD=(255,211,148)


def ease(s):
    s=float(np.clip(s,0,1))
    return s*s*(3-2*s)


def width_at(seconds):
    previous=OPENINGS[0]
    for (begin,end),target in zip(TRANSITIONS,OPENINGS[1:]):
        if seconds<begin:
            return previous
        if seconds<end:
            return previous+(target-previous)*ease((seconds-begin)/(end-begin))
        previous=target
    return previous


def map_xy(x,y):
    return (BOX[0]+(x-XMIN)/(XMAX-XMIN)*PW,
            (BOX[1]+BOX[3])/2-y/(2*YHALF)*PH)


@lru_cache(None)
def font(size,bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf","DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name,size)
        except OSError:
            pass
    return ImageFont.load_default()


class Apertures:
    def __init__(self,period=PERIOD,n=N):
        self.period,self.n=period,n
        self.dy=period/n
        self.y=(np.arange(n)-n//2)*self.dy
        self.q=2*np.pi*np.fft.fftfreq(n,d=self.dy)
        self.kx=np.sqrt((K*K-self.q*self.q).astype(complex))
        self.iq_inverse=np.zeros(n,complex)
        self.iq_inverse[1:]=1/(1j*self.q[1:])

    def transfer(self,distance):
        return np.exp(1j*distance*self.kx)

    def spectrum(self,width):
        # np.sinc(z)=sin(pi*z)/(pi*z). These are exact interval Fourier
        # coefficients, scaled for NumPy's inverse FFT normalization.
        return (width/self.dy*np.sinc(self.q*width/(2*np.pi))
                *sum(np.exp(-1j*self.q*c) for c in CENTERS))

    def direct(self,distance,width):
        return np.fft.fftshift(np.fft.ifft(self.spectrum(width)*self.transfer(distance)))


class FieldSampler:
    def __init__(self,verbose=True):
        self.model=Apertures()
        self.x=np.linspace(XMIN,XMAX,PW)
        self.y=np.linspace(-YHALF,YHALF,PH)
        self.downstream=np.flatnonzero(self.x>0)
        self.z=self.x[self.downstream]
        # Every shifted evaluation y-(center +/- width/2) lies in this band.
        band=YHALF+max(abs(c) for c in CENTERS)+max(OPENINGS)/2+4*self.model.dy
        self.crop=np.flatnonzero(abs(self.model.y)<=band)
        self.g_origin=self.model.y[self.crop[0]]
        self.h0=np.exp(1j*K*self.z)
        self.incident=np.exp(1j*K*self.x)
        self.last_width,self.last_field=None,None
        CACHE.mkdir(parents=True,exist_ok=True)
        specification=("interval-kernel-v1",PERIOD,N,WAVELENGTH,XMIN,XMAX,
                       YHALF,PW,PH,CENTERS,max(OPENINGS))
        digest=hashlib.sha256(repr(specification).encode()).hexdigest()[:16]
        path=CACHE/f"antiderivative-{digest}.npy"
        if path.exists():
            self.g=np.load(path,mmap_mode="r")
            assert self.g.shape==(len(self.crop),len(self.z))
            return
        self.g=np.empty((len(self.crop),len(self.z)),np.complex64)
        start=time.perf_counter()
        for begin in range(0,len(self.z),12):
            end=min(begin+12,len(self.z))
            h=np.exp(1j*self.z[begin:end,None]*self.model.kx[None,:])
            g=np.fft.fftshift(np.fft.ifft(h*self.model.iq_inverse,axis=1),axes=1)/self.model.dy
            self.g[:,begin:end]=g[:,self.crop].T
            if verbose and begin%240==0:
                print(f"Propagation kernels {begin}/{len(self.z)}; {time.perf_counter()-start:.1f}s",flush=True)
        np.save(path,self.g)

    def shifted(self,edge):
        position=(self.y-edge-self.g_origin)/self.model.dy
        indices=np.floor(position).astype(int)
        fraction=(position-indices).astype(np.float32)[:,None]
        assert indices.min()>=0 and indices.max()+1<len(self.crop)
        return (1-fraction)*self.g[indices,:]+fraction*self.g[indices+1,:]

    def field(self,width):
        if width==self.last_width:
            return self.last_field
        result=np.zeros((PH,len(self.z)),np.complex64)
        for center in CENTERS:
            result+=self.shifted(center-width/2)-self.shifted(center+width/2)
            result+=width/self.model.period*self.h0[None,:]
        self.last_width,self.last_field=width,result
        return result


@lru_cache(None)
def color_table():
    signed=np.linspace(-1,1,8193)
    strength=abs(signed)**.72
    target=np.where(signed[:,None]>=0,POSITIVE,NEGATIVE)
    return np.rint(np.asarray(BG)+(target-np.asarray(BG))*strength[:,None]).astype(np.uint8)


def arrow(draw,start,end,alpha):
    a,b=np.array(start),np.array(end)
    u=(b-a)/np.linalg.norm(b-a)
    v=np.array((-u[1],u[0]))
    draw.line((*a,*b),fill=(*BG,round(alpha*.6)),width=4)
    draw.line((*a,*b),fill=(*GOLD,alpha),width=2)
    draw.polygon((tuple(b),tuple(b-10*u+4*v),tuple(b-10*u-4*v)),fill=(*GOLD,alpha))


def frame(seconds,sampler,clock_seconds=None):
    width=width_at(seconds)
    time_factor=np.exp(-2j*np.pi*(seconds if clock_seconds is None else clock_seconds)/WAVE_PERIOD)
    real=np.broadcast_to((sampler.incident*time_factor).real,(PH,PW)).copy()
    z=sampler.field(width)
    real[:,sampler.downstream]=z.real*time_factor.real-z.imag*time_factor.imag
    indices=np.rint((np.clip(real,-1,1)+1)*4096).astype(np.int32)
    picture=Image.new("RGB",(WIDTH,HEIGHT),BG)
    picture.paste(Image.fromarray(color_table()[indices[::-1]]),BOX[:2])
    d=ImageDraw.Draw(picture,"RGBA")
    sx=map_xy(0,0)[0]
    segments=((-YHALF,CENTERS[0]-width/2),
              (CENTERS[0]+width/2,CENTERS[1]-width/2),
              (CENTERS[1]+width/2,YHALF))
    for bottom,top in segments:
        d.line((sx,map_xy(0,bottom)[1],sx,map_xy(0,top)[1]),fill=(*INK,255),width=6)

    # Fixed ray guides label the limiting geometrical approximation. They do
    # not alter, replace or suppress any calculated field or edge diffraction.
    ray_opacity=round(185*ease((seconds-16.8)/1.0))
    if ray_opacity:
        for center in CENTERS:
            for offset in (-.82,0.,.82):
                arrow(d,map_xy(-.8,center+offset),map_xy(9.4,center+offset),ray_opacity)
        d.text((1370,59),"Ray approximation",font=font(21),fill=(*GOLD,ray_opacity),anchor="ra")
    d.text((70,28),"Widening the openings",font=font(32,True),fill=INK)
    d.text((1370,31),"Same incoming wave · fixed wavelength",font=font(22),fill=MUTED,anchor="ra")
    d.text((70,1070),"Real part of the wave",font=font(20),fill=MUTED)
    d.text((283,1070),"−",font=font(21),fill=NEGATIVE)
    d.text((319,1070),"0",font=font(21),fill=MUTED)
    d.text((356,1070),"+",font=font(21),fill=POSITIVE)
    d.text((1370,1070),f"Opening width: {width/WAVELENGTH:.1f} wavelengths",
           font=font(22),fill=INK,anchor="ra")
    return picture


def previews(sampler):
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,3*596),BG)
    for j,seconds in enumerate(SAMPLES):
        pic=frame(seconds,sampler,clock_seconds=.23)
        pic.save(OUT/f"{NAME}-check-{seconds:g}.png")
        x,y=(j%2)*720,(j//2)*596
        sheet.paste(pic.resize((720,560),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+35,y+568),f"{seconds:g} s",fill=MUTED,font=font(18))
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(18.5,sampler).save(OUT/f"{NAME}-poster.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def validate(sampler):
    model=sampler.model
    indices=[int(np.argmin(abs(sampler.z-z))) for z in (.2,3.,9.8)]
    errors=[]
    for width in (OPENINGS[0],OPENINGS[2],OPENINGS[-1]):
        sampled=sampler.field(width)
        for col in indices:
            direct=model.direct(sampler.z[col],width)
            reference=np.interp(sampler.y,model.y,direct)
            errors.append(float(np.max(abs(sampled[:,col]-reference))))
    assert max(errors)<.0015,errors
    # Constant field must propagate with unchanged magnitude and carrier phase.
    unit=np.ones(model.n,complex)
    propagated=np.fft.ifft(np.fft.fft(unit)*model.transfer(3.25))
    plane_error=float(np.max(abs(propagated-np.exp(1j*K*3.25))))
    assert plane_error<1e-12
    assert np.max(abs(model.transfer(.2)))<=1+1e-12
    assert min(np.diff([width_at(t) for t in np.linspace(0,DURATION,1001)]))>=0
    assert max(OPENINGS)<CENTERS[1]-CENTERS[0]
    assert abs(PW/(XMAX-XMIN)-PH/(2*YHALF))<1e-12
    # In the final view, measure concentration inside the two geometric beams
    # relative to the central opaque divider, keeping every diffraction fringe.
    last=sampler.field(OPENINGS[-1])[:,-1]
    core=np.minimum(abs(sampler.y-CENTERS[0]),abs(sampler.y-CENTERS[1]))<.7
    shadow=abs(sampler.y)<.45
    report={"interval_integration_max_complex_error":max(errors),
            "plane_wave_complex_error":plane_error,
            "final_core_mean_intensity":float(np.mean(abs(last[core])**2)),
            "final_central_shadow_mean_intensity":float(np.mean(abs(last[shadow])**2)),
            "wavelength":WAVELENGTH,"width_range":list((OPENINGS[0],OPENINGS[-1])),
            "fixed_color_mapping":"signed real part; |value|^0.72; no variable gain",
            "period":PERIOD,"n":N,"dy":model.dy,"duration":DURATION,
            "model":"forward scalar, finite-interval thin aperture; steady states",
            "size":[WIDTH,HEIGHT],"fps":FPS}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def render(sampler):
    output=OUT/f"{NAME}.mp4"
    temporary=OUT/f"{NAME}-rendering.mp4"
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-f","rawvideo",
         "-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),"-i","-",
         "-an","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
         "-movflags","+faststart",str(temporary)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start=time.perf_counter()
    try:
        for index in range(FRAMES):
            process.stdin.write(frame(index/FPS,sampler).tobytes())
            if index%(2*FPS)==0:
                print(f"{index/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-start:.1f}s",flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    temporary.replace(output)
    print(str(output),flush=True)


def encoded_check(sampler):
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata=next(reader)
    assert tuple(metadata["size"])==(WIDTH,HEIGHT) and metadata["fps"]==FPS
    selected={round(t*FPS) for t in SAMPLES}
    sheet=Image.new("RGB",(1440,1680),BG)
    errors=[]
    chroma_errors=[]
    codec_errors=[]
    # Browser-compatible 4:2:0 averages neighboring chroma samples. Compare
    # compression against that same color conversion, while reporting the
    # total RGB difference too. Saturated narrow stripes make the distinction
    # substantial even when the decoded wave geometry is visually faithful.
    color_conversion=[imageio_ffmpeg.get_ffmpeg_exe(),"-v","error","-f","rawvideo",
        "-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-i","pipe:0",
        "-vf","format=yuv420p,format=rgb24","-frames:v","1",
        "-f","rawvideo","-pix_fmt","rgb24","pipe:1"]
    for index,data in enumerate(reader):
        if index in selected:
            decoded=np.frombuffer(data,np.uint8).reshape(HEIGHT,WIDTH,3)
            reference=frame(index/FPS,sampler)
            rgb=np.asarray(reference).astype(float)
            converted=subprocess.run(color_conversion,input=reference.tobytes(),
                                     capture_output=True,check=True)
            rgb420=np.frombuffer(converted.stdout,np.uint8).reshape(HEIGHT,WIDTH,3).astype(float)
            errors.append(float(np.mean(abs(decoded.astype(float)-rgb))))
            chroma_errors.append(float(np.mean(abs(rgb420-rgb))))
            codec_errors.append(float(np.mean(abs(decoded.astype(float)-rgb420))))
            pic=Image.fromarray(decoded.copy())
            j=len(errors)-1
            sheet.paste(pic.resize((720,560),Image.Resampling.LANCZOS),((j%2)*720,(j//2)*560))
            if j==len(SAMPLES)-1:
                pic.save(OUT/f"{NAME}-encoded-final.png")
                reference.save(OUT/f"{NAME}-encoded-reference-final.png")
    assert index+1==FRAMES and len(errors)==len(SAMPLES)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":index+1,"size":metadata["size"],"fps":FPS,
            "duration":(index+1)/FPS,"sample_times":SAMPLES,
            "mean_rgb_errors":errors,"mean_chroma_conversion_errors":chroma_errors,
            "mean_codec_errors_after_chroma_conversion":codec_errors,
            "max_mean_rgb_error":max(errors),
            "max_mean_codec_error_after_chroma_conversion":max(codec_errors)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)
    assert max(codec_errors)<3.,report


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    args=parser.parse_args()
    sampler=FieldSampler()
    if args.check: validate(sampler)
    if args.preview: previews(sampler)
    if args.render: render(sampler)
    if args.encoded_check: encoded_check(sampler)
