"""Fourier spread and propagation, with fixed physical scales."""
from core import *
from functools import lru_cache

FOURIER_MIN_WIDTH = .07
FOURIER_MAX_WIDTH = 1/(2*FOURIER_MIN_WIDTH)
FOURIER_GAIN = 46

def widths(t):
    # Finite normalized Gaussians at every frame, including both held ends.
    # A logarithmic sweep keeps reciprocal narrowing/spreading legible.
    if t<14:
        sx=np.exp(lerp(np.log(1/np.sqrt(2)),np.log(FOURIER_MIN_WIDTH),ease(t/14)))
    elif t<17.5:
        sx=FOURIER_MIN_WIDTH
    elif t<38.5:
        sx=np.exp(lerp(np.log(FOURIER_MIN_WIDTH),np.log(FOURIER_MAX_WIDTH),ease((t-17.5)/21)))
    else:
        sx=FOURIER_MAX_WIDTH
    return sx,1/(2*sx)

def episode5(t):
    sx,sk=widths(t)
    stage='Narrow in x. Broad in k.' if t<17.5 else 'Broad in x. Narrow in k.'
    s=Scene(5, EPISODES[5].get('video_title', EPISODES[5]['title']),stage,t,42)
    q=np.linspace(-5,5,2401)
    x0=k0=np.sqrt(10*np.pi)
    z=(2*np.pi*sx*sx)**(-.25)*np.exp(-q*q/(4*sx*sx)+1j*k0*q)
    # Both axes show offsets from fixed, nonzero centers. These are exact
    # Fourier partners, including the nonzero phase ramp in the k picture.
    fk=np.sqrt(2)*sx*(2*np.pi*sx*sx)**(-.25)*np.exp(-sx*sx*q*q-1j*(q+k0)*x0)
    for box,label,value,color in [((70,490,950,920),'Position representation',z,BLUE),((70,960,950,1390),'Wave-number representation',fk,RED)]:
        s.panel(box,label)
        helix(s,q,value,(125,box[1]+95,890,box[3]-90),color,gain=FOURIER_GAIN)
        center=0
        sig=sx if color==BLUE else sk
        cx=125+(center+5)*765/10
        y=box[3]-70
        half=sig*765/10
        left,right=max(125,cx-half),min(890,cx+half)
        s.line([(left,y),(right,y)],GOLD,4)
        if half>765/2:
            # The one-sigma endpoints lie outside the unchanged viewport.
            s.arrow((left+17,y),(left,y),GOLD,3,11)
            s.arrow((right-17,y),(right,y),GOLD,3,11)
        else:
            s.line([(left,y-8),(left,y+8)],GOLD,3)
            s.line([(right,y-8),(right,y+8)],GOLD,3)
        s.text(895,box[3]-43,'x − x₀' if color==BLUE else 'k − k₀',30,MUTED,anchor='ra')
    s.math(r'\sigma_x\,\sigma_k=\frac{1}{2}',y=1480,size=55)
    s.text(510,1538,f'σx = {sx:.2f}       σk = {sk:.2f}',34,GOLD,anchor='ma')
    s.note('Gaussian example · fixed axes · normalized functions',y=1595,size=29)
    return s.im

@lru_cache(65)
def aperture_field(index):
    """Paraxial Fresnel propagation on a padded transverse grid.

    Same incident amplitude, masks, and display gain at every wavelength.
    Fourier propagation conserves the transverse norm on this periodic grid.
    """
    lam=float(np.exp(np.linspace(np.log(.9),np.log(.006),65)[index]))
    ny=2048;dy=24/ny;y=(np.arange(ny)-ny//2)*dy
    ky=2*np.pi*np.fft.fftfreq(ny,dy)
    mask=((abs(y-1.65)<.43)|(abs(y+1.65)<.43)).astype(float)
    x=np.linspace(0,6.3,360)
    k=2*np.pi/lam
    modes=np.fft.fft(mask)
    field=np.fft.ifft(modes[:,None]*np.exp(-.5j*ky[:,None]**2*x[None,:]/k),axis=0)
    keep=abs(y)<=4.2
    return lam,y[keep],x,field[keep]*np.exp(1j*k*x)[None,:]

def episode6(t):
    u=window(t,5,35)
    index=int(round(64*ease(u)))
    lam,y,x,out=aperture_field(index)
    stage='A travelling wave reaches two openings.' if t<8 else ('Shorten the wavelength. Keep the openings fixed.' if t<31 else 'Narrow beams: the ray limit comes into view.')
    s=Scene(6, EPISODES[6].get('video_title', EPISODES[6]['title']),stage,t,42)
    s.panel((70,490,950,1410),'Same apertures · decreasing wavelength')
    # Pixel image: propagation to the right, upper y at the top.
    xin=np.linspace(-1.9,0,108,endpoint=False)
    incoming=np.broadcast_to(np.exp(2j*np.pi*xin/lam),(len(y),len(xin)))
    full=np.concatenate([incoming,out],axis=1)[::-1]
    phase=2*np.pi*.24*t/max(lam,.1)
    signed=(full*np.exp(-1j*phase)).real
    absolute=np.clip(abs(signed),0,1)**.74
    rgb=np.empty((*signed.shape,3),dtype=float)
    dark=np.array([3,3,8.]);blue=np.array([37,137,255.]);red=np.array([255,42,91.])
    rgb[:]=dark
    positive=signed>=0
    rgb+=absolute[...,None]*(np.where(positive[...,None],red,blue)-dark)
    intensity=np.clip(abs(full)**2,0,1.3)/1.3
    beam=dark+intensity[...,None]**.7*(np.array([255,180,94])-dark)
    blend=float(ease(np.clip((.18-lam)/.13,0,1)))
    rgb=(1-blend)*rgb+blend*beam
    pic=Image.fromarray(np.uint8(np.clip(rgb,0,255))).resize((790,790),Image.Resampling.LANCZOS)
    s.im.paste(pic,(115,580))
    # Screen placed on the same coordinate mapping as the propagated field.
    screen=115+790*108/(108+360)
    center=975
    gap_centers=[center-790*1.65/8.4,center+790*1.65/8.4]
    half=790*.43/8.4
    cursor=580
    for c in gap_centers:
        s.line([(screen,cursor),(screen,c-half)],MUTED,5);cursor=c+half
    s.line([(screen,cursor),(screen,1370)],MUTED,5)
    if blend>.8:
        for cy in gap_centers:s.arrow((screen+40,cy),(858,cy),GOLD,3,14)
        s.arrow((140,975),(screen-25,975),GOLD,4,14)
    if t<10:s.math(r'\psi(x,t)=e^{i(kx-\omega t)}',y=1480,size=48)
    elif blend<.5:s.math(r'k=\frac{2\pi}{\lambda}',y=1480,size=54)
    else:s.math(r'I=|\psi|^2',y=1480,size=55)
    s.text(510,1540,f'λ / opening width = {lam/.86:.3f}',32,GOLD,anchor='ma')
    s.note('Red / blue: real part' if blend<.5 else 'Gold: cycle-averaged intensity',y=1595)
    return s.im

def validate():
    report={}
    checks=[]
    for sx in (FOURIER_MIN_WIDTH,.4,1/np.sqrt(2),1.6,FOURIER_MAX_WIDTH):
        sk=1/(2*sx)
        extent=12*max(sx,sk)
        count=int(np.ceil(2*extent/(min(sx,sk)/32)))+1
        q=np.linspace(-extent,extent,count)
        density=np.exp(-q*q/(2*sx*sx))/np.sqrt(2*np.pi*sx*sx)
        spectral=np.sqrt(2/np.pi)*sx*np.exp(-2*sx*sx*q*q)
        nx=float(np.trapezoid(density,q));nk=float(np.trapezoid(spectral,q))
        vx=float(np.trapezoid(q*q*density,q));vk=float(np.trapezoid(q*q*spectral,q))
        assert abs(nx-1)<1e-12 and abs(nk-1)<1e-12
        assert abs(vx-sx*sx)<1e-12 and abs(vk-sk*sk)<1e-12
        # Independently integrate the complex Fourier transform, including
        # the nonzero centers responsible for the spiral in each pane.
        x0=k0=np.sqrt(10*np.pi)
        amplitude=(2*np.pi*sx*sx)**(-.25)
        psi=amplitude*np.exp(-q*q/(4*sx*sx)+1j*k0*q)
        errors=[]
        for dk in (-2*sk,0,2*sk):
            numeric=np.trapezoid(psi*np.exp(-1j*(k0+dk)*(q+x0)),q)/np.sqrt(2*np.pi)
            exact=np.sqrt(2)*sx*amplitude*np.exp(-sx*sx*dk*dk-1j*(dk+k0)*x0)
            errors.append(float(abs(numeric-exact)))
        assert max(errors)<1e-11
        checks.append(dict(sigma_x=sx,sigma_k=sk,norm_x=nx,norm_k=nk,width_product=np.sqrt(vx*vk),fourier_error=max(errors)))
    report['5']=dict(normalized_fourier_partners=True,gaussian_checks=checks,
                     fixed_coordinate_axes=True,fixed_amplitude_gain=FOURIER_GAIN,
                     finite_width_range=[FOURIER_MIN_WIDTH,FOURIER_MAX_WIDTH])
    ny=2048;dy=24/ny;y=(np.arange(ny)-ny//2)*dy
    mask=((abs(y-1.65)<.43)|(abs(y+1.65)<.43)).astype(float)
    qy=2*np.pi*np.fft.fftfreq(ny,dy)
    initial=float(np.sum(mask*mask)*dy);errors=[]
    for lam in (.9,.1,.006):
        z=np.fft.ifft(np.fft.fft(mask)*np.exp(-.5j*qy*qy*6.3/(2*np.pi/lam)))
        errors.append(abs(float(np.sum(abs(z)**2)*dy)-initial))
    assert max(errors)<1e-12
    report['6']=dict(model='scalar paraxial thin-mask propagation',periodic_domain=24,
                     norm_conservation_max_error=max(errors),constant_incident_amplitude=True,
                     display_switch='signed real component to cycle-averaged intensity, explicitly labeled')
    return report

EPISODES={
5:dict(title='Where is a wave?',duration=42,render=episode5,checkpoints=[0,7,15.5,28,35,40.5],cover_time=15.5,
caption='A single wave number represents an infinitely extended wave in position space. Conversely, a function localized at a single position is represented by an infinitely extended wave in wave-number space. The two representations describe the same function. Up to overall normalization, exp(ik₀x) ↔ δ(k − k₀), and δ(x − x₀) ↔ exp(−ix₀k), where δ denotes an ideal spike.\n\nHere the cyan and red curves are complex functions drawn as spirals, while gold traces their magnitudes. Their axes and vertical scales stay fixed. The width bars show one standard deviation on either side of the center, calculated from the normalized squared magnitude.\n\nThese particular functions are Gaussian, so σx σk = 1/2 throughout. Other functions can only have a larger product so that bound is σx σk ≥ 1/2. This is Fourier mathematics before it is quantum physics. Both axes show offsets from their fixed centers, x₀ and k₀.'),
6:dict(title='When waves look like rays',duration=42,render=episode6,checkpoints=[2,13,24,39],cover_time=24,
caption='Keep two openings fixed and shorten the incoming wavelength. The transmitted wave spreads less, interference lessens, and, in the limit, the two beams behave like rays.\n\nAt first, red and blue show the real part of the wave, with the familiar travelling phase kx − ωt. As a complex function, the incoming wave is ψ(x,t) = exp[i(kx − ωt)]. Once individual cycles become too fine to draw, the picture changes continuously to gold: the cycle-averaged intensity I = |ψ|².\n\nIn the next several reels, we will explore why this transition from interference pattern to ray happens and how it relates to the variational approach to physics known as the principle of least action.')
}
