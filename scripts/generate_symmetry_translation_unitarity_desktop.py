"""One-mode translation representations and their coefficient inner product.

Each row is a one-dimensional representation: c maps to c times an exponential.
The inner product is conjugate(c1)*c2. Real exponential modes are not L2(R)
states, and this animation does not calculate a fixed-window spatial integral.
The plots show how shifting the same mode changes its coefficient at x=0.
"""
from symmetry_exponential_desktop_common import *

NAME='symmetry-translation-unitarity'
DURATION=34
RATE=.55
K=math.pi
REAL_XMIN,REAL_XMAX=-3.,2.
REAL_YMAX=15.5
VIEW_ROTATION=np.exp(-1j*math.radians(25))
REAL_C=np.array([.60,.95],dtype=complex)
COMPLEX_C=np.array([.60,.95*np.exp(.8j)])
COLORS=(BLUE,RED)
MOMENTS=[0,4,7,11,15,18,22,27,33]
STAGES=[(0,'Translate two states in the same one-mode representation.'),
        (3,'A real exponential translation stretches both coefficients.'),
        (10,'Their coefficient inner product changes.'),
        (14,'Now translate the complex exponentials.'),
        (17,'The coefficients turn together, preserving their lengths and relative angle.'),
        (28,'The complex inner product stays fixed. This representation is unitary.')]


def shifts(t):
    return -3*progress(t,3,10),-2*progress(t,15,27)


def coefficients(t):
    a,b=shifts(t)
    return REAL_C*np.exp(-RATE*a),COMPLEX_C*np.exp(-1j*K*b)


def real_point(x,value):
    x,y=np.broadcast_arrays(np.asarray(x),np.asarray(value))
    return np.stack((100+(x-REAL_XMIN)/(REAL_XMAX-REAL_XMIN)*800,
                     458-y/REAL_YMAX*200),axis=-1)


def wave_point(x,z):
    x,z=np.broadcast_arrays(np.asarray(x),np.asarray(z))
    # Fixed linear view of x, Re(z), Im(z), matching the established complex
    # plane-wave animation. Enough transverse depth makes BOTH coils loop.
    w=z*VIEW_ROTATION
    return np.stack((200+(x+3)/6*600+80*w.imag,685-90*w.real),axis=-1)


def tint(color,amount):
    a=np.array([int(color[i:i+2],16) for i in (1,3,5)])
    b=np.array([int(BG[i:i+2],16) for i in (1,3,5)])
    return tuple(np.round(a*(1-amount)+b*amount).astype(int))


def draw_spirals(s,x,cs,shift):
    # Supersample just this graphic so the thin rear curves stay smooth.
    origin=np.array([70.,580.])
    scale=3
    layer=Image.new('RGBA',(900*scale,205*scale))
    d=ImageDraw.Draw(layer)
    def points(p):
        return [tuple(v) for v in np.round((np.asarray(p)-origin)*scale).astype(int)]
    segments=[]
    for c,color in zip(cs,COLORS):
        values=c*np.exp(1j*K*x)
        projected=wave_point(x,values)
        front=(values*VIEW_ROTATION).imag>=0
        breaks=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(x)-1]
        for a,b in zip(breaks[:-1],breaks[1:]):
            segments.append((bool(front[a]),projected[a:b+1],color))
    # Rear portions first, then the nearer arcs of both colored helices.
    for side in (False,True):
        for front,curve,color in segments:
            if front != side: continue
            d.line(points(curve),fill=tint(color,0 if front else .49)+(255,),
                   width=round((4.3 if front else 3.)*scale))
    for c,color in zip(cs,COLORS):
        center=points([wave_point(0,c)])[0]
        radius=4.5*scale
        d.ellipse((center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius),fill=color)
    for c,color in zip(COMPLEX_C,COLORS):
        center=points([wave_point(2+shift,c*np.exp(1j*K*2))])[0]
        radius=6.5*scale
        d.ellipse((center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius),fill=color)
    layer=layer.resize((900,205),Image.Resampling.LANCZOS)
    s.im.paste(layer,tuple(origin.astype(int)),layer)


def coefficients_picture(s,origin,cs,complex_case):
    o=np.asarray(origin,dtype=float)
    gain=88 if complex_case else 42
    s.line([o+[-115,0],o+[210,0]],GRID,2)
    if complex_case:
        s.line([o+[0,-90],o+[0,90]],GRID,2)
        theta=np.linspace(0,2*math.pi,100)
        for radius in (.6,.95):
            s.line(o+gain*radius*np.c_[np.cos(theta),-np.sin(theta)],FAINT,2)
        theta=np.linspace(np.angle(cs[0]),np.angle(cs[0])+.8,35)
        s.line(o+30*np.c_[np.cos(theta),-np.sin(theta)],GOLD,4)
    ends=[]
    for c,color in zip(cs,COLORS):
        end=o+gain*np.array([c.real,-c.imag])
        s.arrow(o,end,color,4,13)
        s.dot(end,5,color)
        ends.append(end)
    if complex_case:
        s.line(ends,GOLD,2)
    else:
        a,b=ends
        s.line([a+[0,12],a+[0,24],b+[0,24],b+[0,12]],GOLD,3)


def render(t):
    s=Canvas()
    s.text(52,35,'Translation of Complex Exponentials Preserves the Inner Product',34,INK,True)
    s.text(52,95,next(text for start,text in reversed(STAGES) if t>=start),26,MUTED)
    s.line([(52,142),(1548,142)],FAINT,2)
    a,b=shifts(t)
    cr,cc=coefficients(t)
    x=np.linspace(REAL_XMIN,REAL_XMAX,650)
    s.text(75,170,'Real exponentials',27,INK,True)
    s.math(440,195,r'f(x)=c_1e^{\lambda x},\quad g(x)=c_2e^{\lambda x}',31)
    s.math(1110,195,r'c\ \mapsto\ e^{-\lambda a}c',32,GOLD)
    for level in (4,8,12):
        s.line(real_point([REAL_XMIN,REAL_XMAX],[level,level]),FAINT,1)
    s.arrow(real_point(REAL_XMIN,0),real_point(REAL_XMAX+.15,0),MUTED,2,10)
    s.math(930,458,'x',24,MUTED)
    cut=real_point(0,0)[0]
    s.line([(cut,255),(cut,458)],GOLD,2)
    s.text(cut,472,'0',19,MUTED,anchor='ma')
    for c,color in zip(REAL_C,COLORS):
        s.d.line([tuple(p) for p in real_point(x,c.real*np.exp(RATE*x))],fill=tint(color,.72),width=2)
    for c,color in zip(cr,COLORS):
        s.d.line([tuple(p) for p in real_point(x,c.real*np.exp(RATE*x))],fill=color,width=5)
        s.dot(real_point(0,c.real),5,color)
    for c,color in zip(REAL_C,COLORS):
        s.dot(real_point(2+a,c.real*np.exp(RATE*2)),7,color)
    coefficients_picture(s,(1170,345),cr,False)
    s.line([(cut+9,240),(1010,240),(1090,312)],GRID,2)
    s.math(1110,425,r'c_1^*c_2=',31,MUTED)
    s.text(1245,425,f'{(cr[0].conjugate()*cr[1]).real:.3f}',31,GOLD,anchor='lm')
    s.line([(52,505),(1548,505)],FAINT,2)
    s.text(75,527,'Complex exponentials',27,INK,True)
    s.math(440,550,r'f(x)=c_1e^{ikx},\quad g(x)=c_2e^{ikx}',31)
    s.math(1110,550,r'c\ \mapsto\ e^{-ika}c',32,GREEN)
    s.arrow((95,685),(930,685),MUTED,2,10)
    s.math(942,685,'x',24,MUTED)
    draw_spirals(s,np.linspace(-3,3,1100),cc,b)
    coefficients_picture(s,(1250,700),cc,True)
    s.line([(520,584),(1050,584),(1140,644)],GRID,2)
    p=cc[0].conjugate()*cc[1]
    s.math(1030,812,r'c_1^*c_2=',29,MUTED)
    s.text(1154,812,f'{p.real:.3f} + {p.imag:.3f}i',29,GREEN,anchor='lm')
    s.math(490,790,r'\langle c_1,c_2\rangle=c_1^*c_2',29,MUTED,center=True)
    footer(s,t,DURATION,'The inner product here compares coefficients of one mode, not spatial integrals of the plotted curves.')
    return s.im


def validate():
    times=np.linspace(0,DURATION,205)
    pairs=[coefficients(t) for t in times]
    real=np.array([r[0].conjugate()*r[1] for r,c in pairs])
    products=np.array([c[0].conjugate()*c[1] for r,c in pairs])
    error=float(np.max(abs(products-products[0])))
    assert error<1e-12
    assert np.all(np.diff(real.real)>=-1e-12)
    assert all(np.allclose(abs(c),abs(COMPLEX_C)) for r,c in pairs)
    function_error=0.
    x=np.linspace(-3,3,121)
    for t in times:
        a,b=shifts(t)
        r,c=coefficients(t)
        function_error=max(function_error,float(np.max(abs(r[:,None]*np.exp(RATE*x)-
                            REAL_C[:,None]*np.exp(RATE*(x-a))))),
                            float(np.max(abs(c[:,None]*np.exp(1j*K*x)-
                            COMPLEX_C[:,None]*np.exp(1j*K*(x-b))))))
    assert function_error<1e-12
    real_gain=float(np.exp(RATE*3))
    assert real_gain>5
    assert float(REAL_C[-1].real*np.exp(RATE*(REAL_XMAX+3)))<REAL_YMAX
    # Non-monotone screen x is necessary for visibly open helix loops.
    minimum_loop_margin=80*min(abs(COMPLEX_C))*K-600/6
    assert minimum_loop_margin>45
    assert np.allclose(coefficients(DURATION)[1],COMPLEX_C)
    for t in np.linspace(0,DURATION,69):
        render(t)
    return dict(model='One-dimensional coefficient representations, inner product conjugate(c1)*c2',
                not_a_spatial_integral=True,samples=len(times),
                complex_inner_product_max_error=error,
                translation_function_identity_max_error=function_error,
                real_inner_product=[float(real[0].real),float(real[-1].real)],
                real_amplitude_gain=real_gain,
                real_plot_fixed_ymax=REAL_YMAX,
                helix_visible_turns=3,
                helix_loop_derivative_margin=float(minimum_loop_margin),
                complex_translation_full_turns=1,
                fixed_complex_magnitudes=True,layout_bounds_frames=69)


if __name__=='__main__':
    run(NAME,DURATION,render,validate,MOMENTS,24,__file__)
