"""Fixed narrow openings, shorter wavelength, then an explicit intensity view.

Each frame is a monochromatic steady state of the same two finite apertures.
The scalar forward angular spectrum includes evanescent decay. The axial
carrier is factored out for accurate sampling of the envelope at tiny lambda;
it is restored whenever the real part is drawn. This is not a moving-frequency
transient. Reflection, polarization, and mask thickness are outside the model.
The labeled transition to |U|^2 is a change of displayed observable, not an
average of the red/blue colors and not a replacement of diffraction by rays.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time

import generate_symmetry_widening_apertures as style

np,Image,ImageDraw=style.np,style.Image,style.ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content'/'drafts'/'animations'
NAME='symmetry-short-wave-beams'
WIDTH,HEIGHT=1440,1120
BOX=style.BOX
PW,PH=style.PW,style.PH
XMIN,XMAX,YHALF=-3.,10.,4.8
CENTERS=(-2.4,2.4)
OPENING=.5
PERIOD,N=128.,16384
NX=301
FPS,DURATION=30,20.
FRAMES=round(FPS*DURATION)
LAMBDAS=(.5,.2,.08,.015,.001)
TRANSITIONS=((2.,5.),(6.,9.),(10.,13.),(14.,17.))
SAMPLES=(.8,5.5,8.4,11.5,15.4,18.5)
BG,INK,MUTED=style.BG,style.INK,style.MUTED
INTENSITY_COLOR=(255,181,77)
PHASE_ANCHOR=(XMIN+XMAX)/2
FADE_BEGIN,FADE_END=.30,.18
font=style.font


def wavelength_at(seconds):
    previous=LAMBDAS[0]
    for (begin,end),target in zip(TRANSITIONS,LAMBDAS[1:]):
        if seconds<begin:
            return previous
        if seconds<end:
            s=style.ease((seconds-begin)/(end-begin))
            return float(np.exp((1-s)*np.log(previous)+s*np.log(target)))
        previous=target
    return previous


def intensity_mix(wavelength):
    # Switch before changing k moves the visible crests more than half a cycle
    # per movie frame. This deliberate observable change avoids temporal as
    # well as spatial aliasing; the caption names cycle-averaged intensity.
    return style.ease(np.log(FADE_BEGIN/wavelength)/np.log(FADE_BEGIN/FADE_END))


class FieldSampler:
    def __init__(self,period=PERIOD,n=N,nx=NX):
        self.period,self.n,self.nx=period,n,nx
        self.dy=period/n
        self.q=2*np.pi*np.fft.fftfreq(n,d=self.dy)
        self.ygrid=(np.arange(n)-n//2)*self.dy
        self.spectrum=(OPENING/self.dy*np.sinc(self.q*OPENING/(2*np.pi))
                       *sum(np.exp(-1j*self.q*c) for c in CENTERS))
        self.z=np.linspace(0,XMAX,nx)
        self.y=np.linspace(-YHALF,YHALF,PH)
        self.x=np.linspace(XMIN,XMAX,PW)
        self.down=np.flatnonzero(self.x>0)
        py=(self.y-self.ygrid[0])/self.dy
        self.yi=np.floor(py).astype(int)
        self.yf=(py-self.yi).astype(np.float32)[:,None]
        px=self.x[self.down]/XMAX*(nx-1)
        self.xi=np.minimum(np.floor(px).astype(int),nx-2)
        self.xf=(px-self.xi).astype(np.float32)[None,:]
        self.last_lambda,self.last_envelope=None,None

    def envelope(self,wavelength):
        if wavelength==self.last_lambda:
            return self.last_envelope
        k=2*np.pi/wavelength
        root=np.sqrt((k*k-self.q*self.q).astype(complex))
        # Algebraically root-k, without cancellation for k >> |q|.
        delta=-self.q*self.q/(root+k)
        crop=np.empty((PH,self.nx),np.complex64)
        for begin in range(0,self.nx,24):
            end=min(begin+24,self.nx)
            h=np.exp(1j*self.z[begin:end,None]*delta[None,:])
            u=np.fft.fftshift(np.fft.ifft(h*self.spectrum,axis=1),axes=1).T
            crop[:,begin:end]=(1-self.yf)*u[self.yi,:]+self.yf*u[self.yi+1,:]
        downstream=(1-self.xf)*crop[:,self.xi]+self.xf*crop[:,self.xi+1]
        self.last_lambda,self.last_envelope=wavelength,downstream
        return downstream


def intensity_rgb(values):
    # One fixed intensity map for incoming and outgoing |U|^2. Low diffracted
    # intensity is plum/red, beam cores gold, and Fresnel peaks pale yellow.
    # No normalization by stage, by beam, or by local maximum.
    levels=(0.,.025,.1,.25,.5,1.,1.7,2.5)
    colors=np.array((BG,(15,7,20),(63,15,51),(146,30,58),
                     (241,79,36),(255,186,81),(255,239,165),(255,252,222)))
    return np.rint(np.stack([np.interp(values,levels,colors[:,c])
                            for c in range(3)],axis=-1)).astype(np.uint8)


def frame(seconds,sampler,clock_seconds=None):
    wavelength=wavelength_at(seconds)
    mix=intensity_mix(wavelength)
    env=sampler.envelope(wavelength)
    intensity=np.ones((PH,PW),np.float32)
    intensity[:,sampler.down]=abs(env)**2
    rgb=intensity_rgb(intensity)
    if mix<1:
        clock=seconds if clock_seconds is None else clock_seconds
        # Playback clock is chosen for legibility, not a physical frequency
        # sweep. The spatial wavelength is always the stated value.
        carrier=np.exp(1j*(2*np.pi/wavelength*(sampler.x-PHASE_ANCHOR)-2*np.pi*clock/1.2))
        real=np.broadcast_to(carrier.real,(PH,PW)).copy()
        real[:,sampler.down]=(env*carrier[None,sampler.down]).real
        indices=np.rint((np.clip(real,-1,1)+1)*4096).astype(np.int32)
        waves=style.color_table()[indices]
        rgb=np.rint((1-mix)*waves+mix*rgb).astype(np.uint8)
    picture=Image.new('RGB',(WIDTH,HEIGHT),BG)
    picture.paste(Image.fromarray(rgb[::-1]),BOX[:2])
    d=ImageDraw.Draw(picture,'RGBA')
    sx=style.map_xy(0,0)[0]
    segments=((-YHALF,CENTERS[0]-OPENING/2),
              (CENTERS[0]+OPENING/2,CENTERS[1]-OPENING/2),
              (CENTERS[1]+OPENING/2,YHALF))
    for bottom,top in segments:
        d.line((sx,style.map_xy(0,bottom)[1],sx,style.map_xy(0,top)[1]),
               fill=(*INK,255),width=6)
    d.text((70,28),'Shortening the wavelength',font=font(32,True),fill=INK)
    d.text((1370,31),'Same two openings',font=font(22),fill=MUTED,anchor='ra')
    if mix==0:
        d.text((70,1070),'Real part of the wave',font=font(20),fill=MUTED)
        for x,s,color in ((283,'−',style.NEGATIVE),(319,'0',MUTED),(356,'+',style.POSITIVE)):
            d.text((x,1070),s,font=font(21),fill=color)
    elif mix<1:
        d.text((70,1070),'Wave crests → intensity',font=font(20),fill=INK)
    else:
        d.text((70,1070),'Intensity',font=font(20),fill=INTENSITY_COLOR)
        d.text((180,1070),'Averaged over a wave cycle',font=font(20),fill=MUTED)
    ratio=OPENING/wavelength
    d.text((1370,1070),f'Opening width: {ratio:.1f} wavelengths',
           font=font(22),fill=INK,anchor='ra')
    return picture


def previews(sampler):
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1440,3*596),BG)
    for j,seconds in enumerate(SAMPLES):
        pic=frame(seconds,sampler)
        pic.save(OUT/f'{NAME}-check-{seconds:g}.png')
        x,y=(j%2)*720,(j//2)*596
        sheet.paste(pic.resize((720,560),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+35,y+568),f'{seconds:g} s',fill=MUTED,font=font(18))
    sheet.save(OUT/f'{NAME}-contact-sheet.png')
    frame(18.5,sampler).save(OUT/f'{NAME}-poster.png')
    print(str(OUT/f'{NAME}-contact-sheet.png'),flush=True)


def validate(sampler):
    errors=[]
    for wavelength in (LAMBDAS[0],.08,LAMBDAS[-1]):
        sampled=sampler.envelope(wavelength)
        k=2*np.pi/wavelength
        root=np.sqrt((k*k-sampler.q*sampler.q).astype(complex))
        for requested in (.2,3.25,9.8):
            col=int(np.argmin(abs(sampler.x[sampler.down]-requested)))
            z=sampler.x[sampler.down[col]]
            reference=np.fft.fftshift(np.fft.ifft(sampler.spectrum*np.exp(1j*z*(root-k))))
            reference=np.interp(sampler.y,sampler.ygrid,reference)
            errors.append(float(np.max(abs(sampled[:,col]-reference))))
    assert max(errors)<.02,errors
    assert np.all(np.diff([wavelength_at(t) for t in np.linspace(0,DURATION,601)])<=0)
    assert intensity_mix(LAMBDAS[-1])==1 and intensity_mix(LAMBDAS[0])==0
    steps=[]
    for i in range(FRAMES-1):
        wa,wb=wavelength_at(i/FPS),wavelength_at((i+1)/FPS)
        if intensity_mix(wa)==1: continue
        phase_step=(2*np.pi/wb-2*np.pi/wa)*(np.array((XMIN,XMAX))-PHASE_ANCHOR)-2*np.pi/(1.2*FPS)
        steps.append(float(max(abs(phase_step))))
    assert max(steps)<np.pi,steps
    final=abs(sampler.envelope(LAMBDAS[-1])[:,-1])**2
    distance=np.minimum(abs(sampler.y-CENTERS[0]),abs(sampler.y-CENTERS[1]))
    report={'model':'finite intervals; forward scalar angular spectrum; steady states',
            'fixed_opening':OPENING,'centers':CENTERS,'wavelengths':LAMBDAS,
            'period':PERIOD,'n':N,'axial_samples':NX,'max_sampling_complex_error':max(errors),
            'final_visible_intensity_fraction_within_geometric_beams':float(final[distance<OPENING/2].sum()/final.sum()),
            'intensity_transition_wavelengths':[FADE_BEGIN,FADE_END],
            'max_visible_carrier_phase_step_per_frame':max(steps),
            'fixed_intensity_color_levels':[0.,.025,.1,.25,.5,1.,1.7,2.5],
            'duration':DURATION,'size':[WIDTH,HEIGHT],'fps':FPS}
    (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


def render(sampler):
    output=OUT/f'{NAME}.mp4'
    temporary=OUT/f'{NAME}-rendering.mp4'
    cmd=[style.imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
         '-pix_fmt','rgb24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(temporary)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start=time.perf_counter()
    try:
        for index in range(FRAMES):
            process.stdin.write(frame(index/FPS,sampler).tobytes())
            if index%(2*FPS)==0:
                print(f'{index/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-start:.1f}s',flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors='replace')
        if process.wait(): raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    temporary.replace(output)
    print(str(output),flush=True)


def encoded_check(sampler):
    reader=style.imageio_ffmpeg.read_frames(str(OUT/f'{NAME}.mp4'),pix_fmt='rgb24')
    meta=next(reader)
    selected={round(t*FPS) for t in SAMPLES}
    sheet=Image.new('RGB',(1440,1680),BG)
    errors=[]
    for index,data in enumerate(reader):
        if index not in selected: continue
        decoded=np.frombuffer(data,np.uint8).reshape(HEIGHT,WIDTH,3)
        reference=frame(index/FPS,sampler)
        errors.append(float(np.mean(abs(decoded.astype(float)-np.asarray(reference).astype(float)))))
        j=len(errors)-1
        pic=Image.fromarray(decoded.copy())
        sheet.paste(pic.resize((720,560),Image.Resampling.LANCZOS),((j%2)*720,(j//2)*560))
        if j==len(SAMPLES)-1: pic.save(OUT/f'{NAME}-encoded-final.png')
    assert index+1==FRAMES and len(errors)==len(SAMPLES)
    assert tuple(meta['size'])==(WIDTH,HEIGHT) and meta['fps']==FPS
    sheet.save(OUT/f'{NAME}-encoded-contact-sheet.png')
    report={'decoded_frames':index+1,'size':meta['size'],'fps':FPS,
            'duration':(index+1)/FPS,'mean_rgb_errors':errors}
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for flag in ('check','preview','render','encoded-check'):
        parser.add_argument('--'+flag,action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    sampler=FieldSampler()
    if args.check: validate(sampler)
    if args.preview: previews(sampler)
    if args.render: render(sampler)
    if args.encoded_check: encoded_check(sampler)
