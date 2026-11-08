"""Translation of two distinct, normalized, square-integrable wave packets.

Both functions have smooth compact support on R, wholly inside the plotted
domain for every displayed translation. Each is normalized once, at preparation.
The full spatial inner product is calculated by quadrature, not from one-mode
coefficients. A common carrier makes psi_1* psi_2 real and positive, permitting
its actual integral to be shown as a shaded area. Different envelopes ensure
the two states are not proportional, even up to a global phase.

This is a standalone replacement proposal; it changes no existing animation
or manuscript. Run --render --check to produce and verify its MP4.
"""
from symmetry_exponential_desktop_common import *

NAME = 'symmetry-normalized-translation'
DURATION = 28
XMIN, XMAX = -6., 6.
CENTERS = np.array([-1.8, -.2])
RADII = np.array([2.2, 1.55])
K = 6.
COLORS = ('#2b659b', '#bc7520')
PURPLE = '#79518f'
VIEW = np.exp(-1j*math.radians(25))
MOMENTS = [0, 4, 7, 10, 13, 17, 21, 24, 27]
INTEGRATION_X = np.linspace(XMIN, XMAX, 8193)
PLOT_X = np.linspace(XMIN, XMAX, 1801)


def bump(u):
    u = np.asarray(u,dtype=float)
    result = np.zeros(u.shape)
    inside = np.abs(u)<1.
    result[inside] = np.exp(1.-1./(1.-u[inside]**2))
    return result


# Normalize the two envelopes once. The quadrature variable u lies in [-1,1].
QUAD_X, QUAD_W = np.polynomial.legendre.leggauss(256)
BASE_NORM_SQUARED = np.dot(QUAD_W,bump(QUAD_X)**2)
NORMALIZERS = 1./np.sqrt(RADII*BASE_NORM_SQUARED)


def shift(t):
    if t<4: return 0.
    if t<12: return 3.*progress(t,4,12)
    if t<15: return 3.
    if t<23: return 3.*(1.-progress(t,15,23))
    return 0.


def states(x,a=0.):
    x = np.asarray(x)
    q = x-a
    envelopes = NORMALIZERS[:,None]*bump((q[None,:]-CENTERS[:,None])/RADII[:,None])
    return envelopes*np.exp(1j*K*q)[None,:]


def integrate(values,x):
    # Composite trapezoidal quadrature; compact smooth support is resolved.
    return np.sum((values[...,1:]+values[...,:-1])*.5*np.diff(x),axis=-1)


def measured(a):
    psi = states(INTEGRATION_X,a)
    norms = integrate(np.abs(psi)**2,INTEGRATION_X)
    overlap = integrate(psi[0].conj()*psi[1],INTEGRATION_X)
    return norms,overlap


def xp(x):
    return 110.+(np.asarray(x)-XMIN)/(XMAX-XMIN)*1000.


def wave_points(x,z):
    w = z*VIEW
    return np.stack((xp(x)+39*w.imag,350.-112*w.real),axis=-1)


def tint(color,amount):
    a=np.array([int(color[i:i+2],16) for i in (1,3,5)])
    b=np.array([int(BG[i:i+2],16) for i in (1,3,5)])
    return tuple(np.round(a*(1-amount)+b*amount).astype(int))


def draw_waves(s,a):
    # Render the curve geometry at 3x resolution to preserve thin rear arcs.
    scale=3
    origin=np.array([65.,225.])
    layer=Image.new('RGBA',(1090*scale,250*scale))
    d=ImageDraw.Draw(layer)
    psi=states(PLOT_X,a)
    segments=[]
    for values,color in zip(psi,COLORS):
        active=np.abs(values)>1e-5
        front=(values*VIEW).imag>=0
        valid=np.flatnonzero(active)
        first,last=int(valid[0]),int(valid[-1])
        breaks=np.r_[first, np.flatnonzero(front[1:]!=front[:-1])+1, last]
        breaks=np.unique(breaks[(breaks>=first)&(breaks<=last)])
        points=wave_points(PLOT_X,values)
        for start,end in zip(breaks[:-1],breaks[1:]):
            segments.append((bool(front[start]),points[start:end+1],color))
    for side in (False,True):
        for front,curve,color in segments:
            if front!=side: continue
            p=np.round((curve-origin)*scale).astype(int)
            d.line([tuple(v) for v in p],fill=tint(color,0 if side else .43)+(255,),
                   width=round((3.8 if side else 2.6)*scale),joint='curve')
    # One identifiable point on each packet follows the translation itself.
    for j,color in enumerate(COLORS):
        x=CENTERS[j]+a
        value=states(np.array([x]),a)[j,0]
        p=(wave_points(x,value)-origin)*scale
        r=4.3*scale
        d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=color)
    layer=layer.resize((1090,250),Image.Resampling.LANCZOS)
    s.im.paste(layer,tuple(origin.astype(int)),layer)


def draw_product(s,a):
    psi=states(PLOT_X,a)
    product=psi[0].conj()*psi[1]
    assert np.max(np.abs(product.imag))<1e-12
    curve=np.c_[xp(PLOT_X),737.-270.*product.real]
    scale=3
    origin=np.array([85.,555.])
    layer=Image.new('RGBA',(1050*scale,210*scale))
    d=ImageDraw.Draw(layer)
    points=np.round((curve-origin)*scale).astype(int)
    polygon=np.vstack(([(xp(XMIN)-origin[0])*scale,(737-origin[1])*scale],
                       points,[(xp(XMAX)-origin[0])*scale,(737-origin[1])*scale]))
    d.polygon([tuple(v) for v in polygon],fill=tint(PURPLE,.80)+(255,))
    d.line([tuple(v) for v in points],fill=PURPLE,width=3*scale,joint='curve')
    layer=layer.resize((1050,210),Image.Resampling.LANCZOS)
    s.im.paste(layer,tuple(origin.astype(int)),layer)


def axes(s,y,labels=True):
    s.arrow((100,y),(1127,y),MUTED,2,9)
    for v in (-6,-3,0,3,6):
        px=float(xp(v))
        s.line([(px,y-4),(px,y+4)],GRID,1)
        if labels:
            s.text(px,y+11,str(v),18,MUTED,anchor='ma')
    s.math(1143,y,'x',24,MUTED)


def render(t):
    s=Canvas()
    a=shift(t)
    norms,overlap=measured(a)
    s.text(56,35,'Translation preserves the inner product',42,INK,True)
    if t<4:
        caption='Two different wave packets, each normalized to one.'
    elif t<15:
        caption='Translate both wave packets by the same distance.'
    elif t<23:
        caption='Reverse the translation. The shaded area remains unchanged.'
    else:
        caption='Both normalizations and their inner product are preserved.'
    s.text(56,100,caption,26,MUTED)
    s.line([(56,151),(1544,151)],FAINT,2)
    s.text(111,176,'State 1',28,COLORS[0],True)
    s.text(280,176,'State 2',28,COLORS[1],True)
    s.math(850,193,r'(T_a\psi)(x)=\psi(x-a)',29,INK,center=True)
    axes(s,350,labels=False)
    draw_waves(s,a)
    s.text(1210,190,'Normalization',26,INK,True)
    for j in range(2):
        y=285+j*125
        s.math(1205,y,rf'\int |\psi_{j+1}|^2\,dx',29,COLORS[j])
        s.text(1515,y,f'= {norms[j]:.3f}',30,COLORS[j],True,anchor='rm')
    s.line([(56,509),(1544,509)],FAINT,2)
    s.text(111,531,'Their overlap',28,INK,True)
    s.math(820,551,r'\psi_1^*(x-a)\,\psi_2(x-a)',28,PURPLE,center=True)
    draw_product(s,a)
    axes(s,737)
    s.text(1210,558,'Shaded area',26,INK,True)
    s.math(1358,623,r'\langle\psi_1,\psi_2\rangle',34,PURPLE,center=True)
    s.text(1358,666,f'{overlap.real:.3f}',42,PURPLE,True,anchor='mm')
    s.text(800,815,f'Translation a = {a:.2f}',26,INK,anchor='mm')
    s.line([(56,852),(1544,852)],FAINT,2)
    s.line([(56,852),(56+1488*min(t/DURATION,1),852)],GOLD,3)
    return s.im


def validate():
    dense=np.linspace(XMIN,XMAX,32769)
    norm_error=overlap_error=imaginary_error=gram_error=0.
    ref=measured(0)[1]
    maximum_height=0.
    for a in np.linspace(0,3,121):
        psi=states(dense,a)
        n=integrate(np.abs(psi)**2,dense)
        product=psi[0].conj()*psi[1]
        ov=integrate(product,dense)
        norm_error=max(norm_error,float(np.max(abs(n-1))))
        overlap_error=max(overlap_error,float(abs(ov-ref)))
        imaginary_error=max(imaginary_error,float(np.max(abs(product.imag))))
        measured_norms,measured_overlap=measured(a)
        gram_error=max(gram_error,float(np.max(abs(measured_norms-n))),float(abs(measured_overlap-ov)))
        maximum_height=max(maximum_height,float(np.max(product.real)))
        # Confirm direct function translation on a separately sampled grid.
        assert np.allclose(states(dense,a),states(dense-a,0),atol=1e-13)
    assert norm_error<1e-11 and overlap_error<1e-11 and gram_error<1e-11
    assert imaginary_error<1e-12 and .1<ref.real<.95
    assert 737-270*maximum_height>575
    assert np.min(CENTERS-RADII)>XMIN and np.max(CENTERS+RADII+3)<XMAX
    for t in MOMENTS: render(t)
    return dict(model='Two distinct smooth compact-support complex wave packets in L2(R)',
                inner_product='Integral conjugate(psi_1(x-a))*psi_2(x-a) dx',
                norm_squared='Integral abs(psi_j(x-a))^2 dx',
                norm_squared_max_error=norm_error,complex_inner_product_max_error=overlap_error,
                display_quadrature_max_error=gram_error,pointwise_product_imaginary_max=imaginary_error,
                complex_overlap=[float(ref.real),float(ref.imag)],
                squared_overlap=float(abs(ref)**2),nonproportional_states=True,
                initial_centers=CENTERS.tolist(),support_radii=RADII.tolist(),carrier_wavenumber=K,
                fixed_normalizers=NORMALIZERS.tolist(),normalization='At preparation only, never per frame',
                domain=[XMIN,XMAX],translation_range=[0,3],
                support_fully_visible_at_all_shifts=True,validation_grid_points=len(dense),
                display_integration_grid_points=len(INTEGRATION_X),layout_checked_frames=len(MOMENTS))


if __name__=='__main__':
    run(NAME,DURATION,render,validate,MOMENTS,10,__file__)
