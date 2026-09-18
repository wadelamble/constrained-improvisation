"""The physical interpretation and calibrated mechanical units: reels 11–13.

All samples are reproducible. Curves use fixed axes and fixed vertical gains.
The calibration diagram is explicitly schematic, not measured laboratory data.
"""
from core import *


HBAR = 1.054571817e-34
RNG = np.random.default_rng(73921)
DETECTIONS = RNG.normal(size=340)
DOT_Y = RNG.uniform(0, 1, size=340)


def gaussian_density(q, sigma):
    return np.exp(-np.asarray(q)**2/(2*sigma*sigma))/(np.sqrt(2*np.pi)*sigma)


def detector_state(q, k, distance=4.0, source_sigma=.20):
    """Normalized paraxial free Gaussian, with common longitudinal phase removed.

    The input has intensity variance source_sigma**2. The exact transverse
    Fresnel factor gives sigma(L)^2=sigma(0)^2+[L/(2*k*sigma(0))]^2.
    """
    stretch = 1 + 1j*distance/(2*k*source_sigma**2)
    amp = (2*np.pi*source_sigma**2)**(-.25)/np.sqrt(stretch)
    return amp*np.exp(-np.asarray(q)**2/(4*source_sigma**2*stretch))


def episode_11(t):
    duration = 46
    if t < 7:
        stage = 'The amplitude is a complex function.'
    elif t < 25:
        stage = 'Its squared magnitude predicts detections.'
    elif t < 33:
        stage = 'Repeat with a shorter wavelength.'
    else:
        stage = 'The probability concentrates near the ray.'
    s = Scene(11, EPISODES[11].get('video_title', EPISODES[11]['title']), stage, t, duration)
    k = 8*np.exp(np.log(20)*ease(window(t,25,33)))
    q = np.linspace(-4.5,4.5,1800)
    z = detector_state(q,k)*np.exp(-.85j*t)
    density = abs(z)**2
    sigma = np.sqrt(.20**2+(4/(2*k*.20))**2)
    s.panel((70,490,950,910),'Complex amplitude at a detector')
    helix(s,q,z,(145,585,865,825),BLUE,gain=76,depth=.30)
    s.text(122,848,'Gold: magnitude     Cyan: complex function',30,MUTED)
    s.panel((70,950,950,1425),'Probability density and repeated detections')
    xx = 135+(q+4.5)*750/9
    baseline = 1260
    pts=np.c_[xx,baseline-125*density]
    s.d.polygon([(135,baseline)]+[tuple(p) for p in pts]+[(885,baseline)],fill='#143c38')
    s.line(pts,GREEN,5)
    s.line([(135,baseline),(885,baseline)],GRID,2)
    s.text(882,1269,'position',30,MUTED,anchor='ra')
    if t < 25:
        count = int(340*ease(window(t,5,25)))
    elif t < 33:
        count = 0
    else:
        count = int(340*ease(window(t,33,45)))
    s.d.rounded_rectangle((135,1315,885,1378),radius=12,fill='#071519')
    for i in range(count):
        px = 510+750*sigma*DETECTIONS[i]/9
        if 139<px<881:
            s.dot((px,1321+51*DOT_Y[i]),3,GREEN)
    s.text(120,1390,f'{count} detections',30,GREEN)
    s.text(900,1390,f'λ / λ₀ = {8/k:.2f}',30,GOLD,anchor='ra')
    if t < 7:
        s.math(r'\psi(x)\ \in\ \mathbb{C}',y=1482,size=56)
    else:
        s.math(r'\rho(x)=|\psi(x)|^2,\qquad\int\rho(x)\,dx=1',y=1482,size=45)
    s.note('One prepared state. Many repetitions.',y=1565,size=32)
    s.note('Fixed axes · the same opening at both wavelengths',y=1606,size=30)
    return s.im


def clock_face(s, center, theta, color, radius=94, label=''):
    cx,cy=center
    s.d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=GRID,width=3)
    s.line([(cx-radius-8,cy),(cx+radius+8,cy)],GRID,2)
    s.line([(cx,cy-radius-8),(cx,cy+radius+8)],GRID,2)
    phasor(s,center,np.exp(1j*theta),radius*.86,color,width=5)
    if label:s.text(cx,cy+radius+21,label,30,color,anchor='ma')


def mass_shell_panel(s,t):
    s.panel((70,490,950,950),'A fixed invariant labels the shell')
    kappa=1.35
    settle=ease(window(t,10,12))
    eta=(1-settle)*.82*np.sin(np.pi*t/6)+settle*.60 if t<12 else .60
    q=np.linspace(-3.3,3.3,650)
    px=lambda k:510+108*k
    py=lambda w:884-77*w
    s.arrow((135,884),(905,884),GRID,3,12)
    s.arrow((510,891),(510,580),GRID,3,12)
    for ka in [.70,2.05]:
        s.line(np.c_[px(q),py(np.sqrt(q*q+ka*ka))],GRID,2)
    s.line(np.c_[px(q),py(np.sqrt(q*q+kappa*kappa))],BLUE,5)
    kval=kappa*np.sinh(eta);omega=kappa*np.cosh(eta)
    end=(px(kval),py(omega))
    s.arrow((510,884),end,GOLD,4,14)
    s.dot(end,9,GOLD)
    s.text(891,891,'k',31,MUTED,anchor='ma')
    s.text(529,580,'ω',31,MUTED)
    s.text(120,906,'κ stays fixed as the frame changes',30,BLUE)
    return eta,kappa


def proper_time_panel(s,t,eta,kappa):
    s.panel((70,990,950,1415),'Proper time advances the phase')
    tau=2.0*(1-ease(window(t,10,12))) if t<12 else lerp(0,7.0,ease(window(t,12,28)))
    x0,y0=265,1344
    scale=24
    s.arrow((120,y0),(450,y0),GRID,3,12)
    s.arrow((x0,y0+5),(x0,1077),GRID,3,12)
    # A timelike segment and its endpoint in the currently displayed frame.
    xmax=7*np.sinh(eta);tmax=7*np.cosh(eta)
    end=(x0+scale*xmax,y0-scale*tmax)
    s.line([(x0,y0),end],BLUE,3)
    now=(x0+scale*tau*np.sinh(eta),y0-scale*tau*np.cosh(eta))
    s.dot(now,8,GOLD)
    s.text(451,1344,'x',30,MUTED)
    s.text(x0+16,1074,'t',30,MUTED)
    s.text(320,1370,f'τ = {tau:.1f}',31,GOLD,anchor='ma')
    s.line([(510,1063),(510,1387)],GRID,2)
    clock_face(s,(738,1215),-kappa*tau,GOLD,radius=90,label='exp(−iκτ)')
    return tau


def calibration_panel(s,t):
    s.panel((70,490,950,950),'Compare mass and wave scales')
    left,bottom=210,851
    right,top=844,580
    s.arrow((left,bottom),(right+28,bottom),GRID,3,12)
    s.arrow((left,bottom),(left,top-5),GRID,3,12)
    s.text(left-40,top-2,'m',32,GOLD)
    s.text(right+18,bottom+7,'κ',32,BLUE)
    u=window(t,28,41)
    s.line([(left,bottom),(left+(right-left)*u,bottom-(bottom-top)*u)],GREEN,4)
    for index in range(7):
        f=(index+1)/8
        if u>=f:s.dot((lerp(left,right,f),lerp(bottom,top,f)),8,GOLD)
    s.text(345,596,'m / κ = constant',35,GREEN)
    s.text(127,899,'Schematic calibration · one ratio across shells',30,MUTED)
    s.panel((70,990,950,1415),'The same advance, expressed in two units')
    theta=-1.35*(7+.57*(t-28))
    clock_face(s,(305,1203),theta,BLUE,radius=95,label='phase  φ')
    clock_face(s,(735,1203),theta,GOLD,radius=95,label='action  S / ħ')
    s.text(518,1184,'=',43,INK,anchor='ma')


def episode_12(t):
    duration=46
    if t<12:stage='Spacetime gives us invariant quantities.'
    elif t<28:stage='Follow proper time along a free path.'
    else:stage='Experiment connects the two scales.'
    s=Scene(12, EPISODES[12].get('video_title', EPISODES[12]['title']),stage,t,duration)
    if t<28:
        eta,kappa=mass_shell_panel(s,t)
        proper_time_panel(s,t,eta,kappa)
    else:
        calibration_panel(s,t)
    if t<12:
        s.math(r'\omega^2-k^2=\kappa^2',y=1480,size=52)
    elif t<28:
        s.math(r'\phi=-\kappa\tau\qquad S=-m\tau',y=1480,size=49)
    elif t<36:
        s.math(r'\frac{S}{\phi}=\frac{m}{\kappa}=\hbar',y=1480,size=56)
    else:
        s.math(r'\hbar\approx1.055\times10^{-34}\ \mathrm{J\,s}',y=1480,size=48)
    s.note('A preview of spacetime · free motion · c = 1',y=1590,size=30)
    return s.im


def uncertainty_panel(s,sx,sp):
    s.panel((70,990,950,1440),'Spreads about the mean')
    domains=np.linspace(-4,4,650)
    for center,sigma,color,label,unit in [
            (296,sx,BLUE,'x − ⟨x⟩','nanometers'),
            (724,sp,RED,'p − ⟨p⟩','10⁻²⁵ kg m/s')]:
        base=1259
        xx=center+domains*40
        yy=base-128*gaussian_density(domains,sigma)
        s.d.polygon([(center-160,base)]+list(map(tuple,np.c_[xx,yy]))+[(center+160,base)],fill='#142334' if color==BLUE else '#311b2b')
        s.line(np.c_[xx,yy],color,4)
        s.line([(center-160,base),(center+160,base)],GRID,2)
        ybar=1300
        s.line([(center-40*sigma,ybar),(center+40*sigma,ybar)],GOLD,4)
        for dx in [-40*sigma,40*sigma]:s.line([(center+dx,ybar-8),(center+dx,ybar+8)],GOLD,3)
        s.text(center,1324,f'σ = {sigma:.2f}',32,GOLD,anchor='ma')
        s.text(center,1370,label,31,color,anchor='ma')
        s.text(center,1402,unit,30,MUTED,anchor='ma')
    s.line([(510,1063),(510,1415)],GRID,2)


def episode_13(t):
    duration=46
    if t<13:stage='Wave number gains mechanical units.'
    elif t<27:stage='The translation itself is unchanged.'
    elif t<36:stage='The commutator gains the scale ħ.'
    else:stage='The Fourier tradeoff becomes quantum uncertainty.'
    s=Scene(13, EPISODES[13].get('video_title', EPISODES[13]['title']),stage,t,duration)
    sx=.82+.40*np.cos(2*np.pi*t/22)
    sp=HBAR/(2*sx*1e-9)/1e-25
    a=1.15*np.sin(2*np.pi*t/14)
    q=np.linspace(-5,5,1400)
    z=(2*np.pi*sx*sx)**(-.25)*np.exp(-(q-a)**2/(4*sx*sx)+4j*(q-a))
    s.panel((70,490,950,950),'One translation, written two ways')
    helix(s,q,z,(185,548,875,706),BLUE,gain=69)
    helix(s,q,z,(185,749,875,908),BLUE,gain=69)
    s.math(r'\hat K',x=126,y=628,size=42,color=BLUE,maxwidth=100)
    s.math(r'\hat P/\hbar',x=126,y=830,size=42,color=GOLD,maxwidth=110)
    uncertainty_panel(s,sx,sp)
    if t<13:
        s.math(r'\hat P:=\hbar\hat K',y=1500,size=58)
    elif t<27:
        s.math(r'T_x(a)=e^{-ia\hat K}=e^{-ia\hat P/\hbar}',y=1500,size=46)
    elif t<36:
        s.math(r'[\hat X,\hat P]=i\hbar I',y=1500,size=55)
    else:
        s.math(r'\sigma_x\,\sigma_p\geq\frac{\hbar}{2}',y=1500,size=60)
    s.note('Same wave structure. Physical units.',y=1600,size=32)
    return s.im


def validate():
    """Independent quadratures and invariant checks for the displayed models."""
    report = {}
    q = np.linspace(-20,20,40001)
    detector_checks = []
    for k in (8.,32.,160.):
        density = abs(detector_state(q,k))**2
        norm = float(np.trapezoid(density,q))
        mean = float(np.trapezoid(q*density,q))
        variance = float(np.trapezoid((q-mean)**2*density,q))
        expected_variance = .20**2 + (4/(2*k*.20))**2
        assert abs(norm-1) < 1e-12
        assert abs(mean) < 1e-12
        assert abs(variance-expected_variance) < 1e-12
        detector_checks.append(dict(k=k,norm=norm,mean=mean,
                                    integrated_variance=variance,
                                    expected_variance=expected_variance))
    report['11'] = dict(model='normalized paraxial free Gaussian',
                        independent_detector_quadratures=detector_checks,
                        random_seed=73921,fixed_axes=True)

    rapidity = np.linspace(-.82,.82,51)
    shell_errors=[]
    for kappa in (.70,1.35,2.05):
        omega = kappa*np.cosh(rapidity)
        wave_number = kappa*np.sinh(rapidity)
        shell_errors.append(float(np.max(abs(omega**2-wave_number**2-kappa**2))))
    proper_time_errors=[]
    for tau in (0.,.5,2.,7.):
        coordinate_time=tau*np.cosh(rapidity)
        coordinate_position=tau*np.sinh(rapidity)
        proper_time_errors.append(float(np.max(abs(coordinate_time**2-coordinate_position**2-tau**2))))
    assert max(shell_errors) < 1e-12
    assert max(proper_time_errors) < 1e-11
    report['12'] = dict(shell_invariant_max_error=max(shell_errors),
                        proper_time_invariant_max_error=max(proper_time_errors),
                        units='c=1',calibration='schematic empirical ratio, not laboratory data')

    uncertainty_checks=[]
    for sx_nm in (.42,.82,1.22):
        sp_units=HBAR/(2*sx_nm*1e-9)/1e-25
        dx=gaussian_density(q,sx_nm)
        dp=gaussian_density(q,sp_units)
        nx=float(np.trapezoid(dx,q));np_=float(np.trapezoid(dp,q))
        vx=float(np.trapezoid((q*1e-9)**2*dx,q))
        vp=float(np.trapezoid((q*1e-25)**2*dp,q))
        product=float(np.sqrt(vx*vp))
        relative_error=abs(product/(HBAR/2)-1)
        assert abs(nx-1)<1e-12 and abs(np_-1)<1e-12
        assert relative_error<1e-12
        uncertainty_checks.append(dict(sigma_x_nm=sx_nm,sigma_p_units_1e_25=sp_units,
                                        norm_x=nx,norm_p=np_,
                                        integrated_width_product_SI=product,
                                        relative_error=relative_error))
    wave_number=np.linspace(-8e9,8e9,2001)
    momentum=HBAR*wave_number
    translation_errors=[]
    for shift in (-1.15e-9,0.,1.15e-9):
        via_k=np.exp(-1j*shift*wave_number)
        via_p=np.exp(-1j*shift*momentum/HBAR)
        translation_errors.append(float(np.max(abs(via_k-via_p))))
    assert max(translation_errors)<1e-12
    report['13'] = dict(hbar_Js=HBAR,independent_SI_width_quadratures=uncertainty_checks,
                        identical_translation_multiplier_max_error=max(translation_errors))
    return report


EPISODES={
    11:dict(title='From Intensity to probability',duration=46,render=episode_11,
        checkpoints=[1,9,23,29,35,44],cover_time=23,
        caption='So far, we have calculated wave amplitudes. Quantum mechanics gives that calculation a physical interpretation. The normalized squared magnitude tells us the probability density for a position measurement. Writing that density as ρ(x), we have ρ(x) = |ψ(x)|², with ∫ρ(x) dx = 1.\n\nThe upper curve is a complex amplitude at a detector. Below it, green shows |ψ|². Individual detections are unpredictable. Repeat the same preparation, and the ensuing distribution builds toward that density. The dots here are reproducible simulated samples from the displayed function.\n\nWe then repeat the experiment with a shorter wavelength and the same Gaussian opening. Its calculated diffraction spread is smaller, so the outcomes concentrate near the transmitted ray. Both panels keep fixed scales. The animation compares two preparations. The dots are not particles being steered between outcomes.\n\nThe path sum calculates the amplitude. The quantum interpretation tells us what its squared magnitude predicts.',
        validation={'state':'Exact normalized paraxial free Gaussian',
                    'source_intensity_sigma':.2,'distance':4.,'k_initial':8.,'k_final':160.,
                    'detector_sigma_initial':float(np.sqrt(.04+(4/(2*8*.2))**2)),
                    'detector_sigma_final':float(np.sqrt(.04+(4/(2*160*.2))**2)),
                    'random_seed':73921}),
    12:dict(title='Relativity maps phase to mechanical action through \u0127',video_title='Relativity maps phase to mechanical action through \u0127',duration=46,render=episode_12,
        checkpoints=[2,9,19,27,32,43],cover_time=19,
        caption="Action, the quantity made stationary by the physical path, can be constructed from the structure of spacetime, as articulated in special relativity, the topic of our next chapter. Because this quantity must be agreed upon by all observers, it is natural that it should be an invariant of symmetry actions on spacetime. For free motion, action is proportional to an invariant built from translations — the time elapsed along a path as measured in a body's rest frame — times a dual invariant built from translation generators. The former is called proper time while the latter is mass. We use units with c = 1.\n\nS = −mτ\n\nAt the same time, we can calculate how phase advances along a path in spacetime. Introducing κ, the invariant built from wave function spacetime-translation generators, the phase factor along a free path is\n\nexp(−iκτ).\n\nThe blue curve is a mass shell. Moving along it changes k and ω while κ stays fixed.\n\nWe then have\n\nconstant = S/φ = m/κ.\n\nWe can measure this constant in the lab by comparing mass, as measured through collisions, to wavelength, as measured through interference. The calibration plot is schematic. We find\n\nS/φ := ħ ≈ 1.055 × 10⁻³⁴ J s.\n\nThe smaller ħ is, the more phase cycles a given path variation produces. This is exactly our condition for the path sum to be dominated by stationary paths. Through m/κ = ħ, mass sets the phase accumulation per unit proper time. For everyday bodies, action differences are enormous compared with ħ, and their motion is effectively deterministic. Are we saying that the laws of motion we learn in high school physics are an approximation? Yes, a very good approximation.",
        validation={'scope':'Free proper-time comparison; c=1; schematic empirical calibration',
                    'shell_relation':'omega**2-k**2=kappa**2',
                    'proper_time_relation':'t**2-x**2=tau**2',
                    'hbar_Js':HBAR}),
    13:dict(title='The uncertainty principle',duration=46,render=episode_13,
        checkpoints=[2,11,20,32,40,45],cover_time=40,
        caption='The scale that converts phase to action also converts wave number to momentum. P̂ = ħK̂. The two spirals show the same translation written with either generator. Tₓ(a) = exp(−iaK̂) = exp(−iaP̂/ħ). Changing units does not change the operation.\n\nThe wave commutator becomes [X̂,P̂] = iħI. The position/wave-number tradeoff becomes σx σp ≥ ħ/2. The lower plots show normalized squared magnitudes for a Gaussian family, which reaches equality. The position axis uses nanometers, and the momentum axis uses 10⁻²⁵ kg m/s. Both scales remain fixed while the widths trade places.\n\nWe began with ways to move a wave function. We found phase, interference, a short-wavelength route to ray behavior, and the structure of quantum uncertainty. With quantum probabilities and the measured scale ħ, that structure acquires a physical meaning. The next series will develop its spacetime setting.',
        validation={'hbar_Js':HBAR,'gaussian_product':'sigma_x_m * sigma_p_SI = hbar / 2',
                    'translation':'Both displayed rows are identical complex samples.'})
}
