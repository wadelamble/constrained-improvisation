"""Portrait episodes 1–4: translations, unitarity, phase, and the x/k loop.

All moving curves are complex functions under the displayed transformations.
Playback changes transformation parameters; it is not physical time evolution.
The two own-representation experiments in episodes 1/2 are independent.
"""
from core import *


X = np.linspace(-4.5, 9.0, 1001)
C = 3.6
DEPTH = .31
VIEW = np.exp(-.38j)


def _dim(color, amount=.45):
    from PIL import ImageColor
    a = np.array(ImageColor.getrgb(color) if isinstance(color,str) else color)
    b = np.array(ImageColor.getrgb(PANEL))
    return tuple(np.rint(amount*a+(1-amount)*b).astype(int))


def _complex(s, grid, values, box, gain, color=BLUE, width=4):
    """Parallel projection of (q, Re f, Im f), with fixed front/back shading."""
    left, top, right, bottom = box
    cy = (top+bottom)/2
    sx = left+(grid-grid[0])/(grid[-1]-grid[0])*(right-left)
    w = values*VIEW
    pts = np.c_[sx+DEPTH*gain*w.imag, cy-gain*w.real]
    s.line([(left,cy),(right,cy)],GRID,2)
    front = (w[:-1].imag+w[1:].imag)>=0
    breaks=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
    for side in (False,True):
        for a,b in zip(breaks[:-1],breaks[1:]):
            if front[a]==side:
                s.line(pts[a:b+1],color if side else _dim(color),width)
    return pts


@lru_cache(32)
def _gaussian_outline(scale, gain, sigma=1.0):
    # Exact projected silhouette of the circular magnitude cross sections.
    q=np.linspace(-5*sigma,5*sigma,901)
    radius=gain*np.pi**(-.25)*np.exp(-.5*(q/sigma)**2)
    xx=np.linspace(-5*sigma*scale,5*sigma*scale,901)
    h2=np.max(radius[:,None]**2-((xx[None,:]-scale*q[:,None])/DEPTH)**2,axis=0)
    return xx,np.sqrt(np.maximum(0,h2))


def _gaussian_envelope(s, center, box, gain, color=GOLD, domain=(-4.5,9)):
    left,top,right,bottom=box
    scale=(right-left)/(domain[1]-domain[0]); cy=(top+bottom)/2
    xx,h=_gaussian_outline(scale,gain)
    xx=xx+left+scale*(center-domain[0])
    keep=(xx>=left)&(xx<=right)
    s.line(np.c_[xx[keep],cy-h[keep]],color,2)
    s.line(np.c_[xx[keep],cy+h[keep]],color,2)


def _state(q, center=C, sign=1, shift=0):
    u=np.asarray(q)-shift
    return np.pi**(-.25)*np.exp(-.5*(u-center)**2+sign*1j*center*(u-center/2))


def _axis(s, box, symbol, domain=(-4.5,9), ticks=(-3,0,3,6)):
    l,y,r,_=box
    s.arrow((l,y),(r,y),GRID,2,10)
    for tick in ticks:
        x=l+(tick-domain[0])/(domain[1]-domain[0])*(r-l)
        s.line([(x,y-6),(x,y+6)],MUTED,2)
        s.text(x,y+11,str(tick).replace('-','−'),30,MUTED,anchor='ma')
    s.text(r+8,y-16,symbol,31,MUTED)


def _translation_schedule(t):
    if t<12:
        return 1.7*ease(window(t,.6,10.8)),0.0,'Translate in position'
    if t<24:
        return 1.7,1.7*ease(window(t,12,22.8)),'Translate in wave number'
    if t<35:
        v=1.7-3.2*ease(window(t,24,34))
        return v,v,'The same operation in dual spaces'
    v=-1.5+1.5*ease(window(t,35,43))
    return v,v,'Move the whole complex function'


def episode_1(t):
    a,b,stage=_translation_schedule(t)
    s=Scene(1, EPISODES[1].get('video_title', EPISODES[1]['title']),stage,t,44)
    for i,(q,amount,sgn,color,label) in enumerate((
        ('x',a,1,BLUE,'POSITION'),('k',b,-1,RED,'WAVE NUMBER'))):
        top=485+i*475
        s.panel((70,top,950,top+450),label)
        plot=(115,top+82,895,top+282)
        _gaussian_envelope(s,C+amount,plot,132)
        _complex(s,X,_state(X,sign=sgn,shift=amount),plot,132,color)
        _axis(s,(115,top+318,895,0),q)
        s.math(r'\psi(x-a)' if i==0 else r'\widetilde\psi(k-b)',
               x=267,y=top+405,size=39,color=color,maxwidth=300)
        name='a' if i==0 else 'b'
        s.text(685,top+383,f'{name} = {amount:+.2f}'.replace('-','−'),36,GOLD)
    s.math(r'T_x(a)\psi(x)=\psi(x-a)',y=1480,size=43)
    s.math(r'T_k(b)\widetilde\psi(k)=\widetilde\psi(k-b)',y=1536,size=43)
    s.note('Two separate experiments. Gold marks magnitude.',size=30)
    return s.im


PAIR=(2.0,3.2)
OVERLAP=float(np.exp(-.5*(PAIR[1]-PAIR[0])**2))
PAIR_ANGLE=float(np.arccos(OVERLAP))


def _dash(s,a,b,color=GOLD):
    a,b=np.asarray(a),np.asarray(b); dist=np.linalg.norm(b-a)
    for j in np.arange(0,dist,11):
        s.line([a+(b-a)*j/dist,a+(b-a)*min(j+6,dist)/dist],color,2)


def _geometry(s,center,shift):
    cx,cy=center; r=128; ang=-.32+.38*shift
    s.d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=GRID,width=2)
    s.d.ellipse((cx-r,cy-r*.23,cx+r,cy+r*.23),outline=GRID,width=1)
    u=np.array([np.cos(ang),-np.sin(ang)])
    v=np.array([np.cos(ang+PAIR_ANGLE),-np.sin(ang+PAIR_ANGLE)])
    start=np.array([cx,cy]); tip=start+r*v; foot=start+r*OVERLAP*u
    s.arrow(start,start+r*u,BLUE,5,14)
    s.arrow(start,tip,RED,5,14)
    _dash(s,tip,foot)
    s.line([start,foot],GOLD,7)
    s.dot(foot,5,GOLD)
    s.text(cx,cy+r+24,'projection = 0.487',30,GOLD,anchor='ma')


def episode_2(t):
    a,b,_=_translation_schedule(t)
    stage=('Move both functions together' if t<12 else
           'Wave-number translation does it too' if t<24 else
           'Their overlap stays the same')
    s=Scene(2, EPISODES[2].get('video_title', EPISODES[2]['title']),stage,t,44)
    for i,(symbol,shift,sgn) in enumerate((('x',a,1),('k',b,-1))):
        left=70+i*450; right=left+430; mid=(left+right)/2
        s.panel((left,485,right,905),f'Translate in {symbol}')
        box=(left+28,577,right-30,757)
        for j,c in enumerate(PAIR):
            color=(BLUE,RED)[j]
            _gaussian_envelope(s,c+shift,box,107,_dim(color,.55))
            _complex(s,X,_state(X,c,sgn,shift),box,107,color,3)
        _axis(s,(left+28,793,right-35,0),symbol,ticks=(0,3,6))
        s.panel((left,936,right,1430))
        s.text(mid,963,'Overlap geometry',30,MUTED,anchor='ma')
        _geometry(s,(mid,1177),shift)
    s.math(r'\langle T\psi,T\chi\rangle=\langle\psi,\chi\rangle',y=1490,size=45)
    s.text(510,1532,'UNITARITY',32,GREEN,bold=True,anchor='ma')
    s.note('Real, positive overlap chosen. Vector view schematic.',size=30)
    return s.im


MODE_X=np.linspace(-np.pi,np.pi,1601)
MODE_K=np.arange(11,20)
MODE_M=np.arange(-4,5)
MODE_WEIGHT=np.exp(-MODE_M**2/(2*2.2**2))
MODE_PHASE=.10*MODE_M**2+.012*MODE_M**3
_fine=np.linspace(-np.pi,np.pi,32769)
MODE_NORMALIZER=float(abs(np.sum(MODE_WEIGHT[:,None]*np.exp(
    1j*(MODE_K[:,None]*_fine+MODE_PHASE[:,None])),axis=0)).max())
MODE_A=MODE_WEIGHT/MODE_NORMALIZER
MODE_BASE=MODE_A[:,None]*np.exp(1j*(MODE_K[:,None]*MODE_X+MODE_PHASE[:,None]))
SUM_BASE=MODE_BASE.sum(axis=0)


@lru_cache(1)
def _sum_silhouette():
    gain=137; scale=348/(2*np.pi)
    centers=110+(MODE_X+np.pi)*scale
    radius=gain*abs(SUM_BASE)
    xx=np.linspace(110,458,801)
    h2=np.max(radius[:,None]**2-((xx[None,:]-centers[:,None])/DEPTH)**2,axis=0)
    return xx,np.sqrt(np.maximum(h2,0))


def episode_3(t):
    # Five full common-phase turns; each return is exact, with one fixed scale.
    phi=10*np.pi*min(t,44)/44
    stage=('Turn every complex value' if t<14 else
           'Every mode turns by the same angle' if t<29 else
           'The magnitude envelope stays put')
    s=Scene(3, EPISODES[3].get('video_title', EPISODES[3]['title']),stage,t,44)
    s.panel((70,485,500,1430),'Their exact sum',BLUE)
    s.panel((520,485,950,1430),'Nine modes',RED)
    xx,hh=_sum_silhouette()
    s.line(np.c_[xx,942-hh],GOLD,2)
    s.line(np.c_[xx,942+hh],GOLD,2)
    z=np.exp(1j*phi)
    _complex(s,MODE_X,SUM_BASE*z,(110,780,458,1104),137,BLUE,4)
    _axis(s,(110,1230,458,0),'x',domain=(-np.pi,np.pi),ticks=(-3,0,3))
    s.text(285,579,'Phase factor',31,GOLD,anchor='ma')
    s.d.ellipse((229,641,341,753),outline=GRID,width=2)
    phasor(s,(285,697),z,56,GOLD,4)
    s.text(285,1158,'Fixed envelope',31,GOLD,anchor='ma')
    s.text(285,1321,'One spatial period',30,MUTED,anchor='ma')
    for j,k in enumerate(MODE_K):
        cy=610+86*j
        s.text(545,cy-17,str(int(k)),30,MUTED)
        # Same amplitude scale as the exact sum. Small amplitudes stay small.
        _complex(s,MODE_X,MODE_BASE[j]*z,(598,cy-33,915,cy+33),137,RED,3)
    s.text(545,547,'k',30,MUTED)
    s.math(r'\psi(x)\ \longmapsto\ e^{i\phi}\psi(x)',y=1485,size=47)
    s.text(510,1528,f'φ = {phi/np.pi:.2f}π',37,GOLD,anchor='ma')
    s.note('A full turn restores every mode—and their sum.',size=30)
    return s.im


LOOP_A=1.5
LOOP_B=np.pi/3
LOOP_X=np.linspace(-5,5,1601)


def _loop_base(x):
    return np.pi**(-.25)*np.exp(-.5*x*x+3.5j*x)


def _loop_state(t):
    """Return position shift, k shift, central phase, completed leg progress."""
    leg=np.clip((t-.6)/7.8,0,4)
    if leg<1:
        u=ease(leg); return 0,LOOP_B*u,0,float(leg)
    if leg<2:
        u=ease(leg-1); a=LOOP_A*u
        return a,LOOP_B,-a*LOOP_B,float(leg)
    if leg<3:
        u=ease(leg-2)
        return LOOP_A,LOOP_B*(1-u),-LOOP_A*LOOP_B,float(leg)
    u=ease(leg-3)
    return LOOP_A*(1-u),0,-LOOP_A*LOOP_B,float(leg)


def _loop_points(a,b):
    return (155+255*a/LOOP_A,1325-235*b/LOOP_B)


def episode_4(t):
    a,b,phase,leg=_loop_state(t)
    loop_scale=1-.75*ease(window(t,39,45))
    if t>=39:
        phase=-LOOP_A*LOOP_B*loop_scale**2
    stage=('1. Shift in wave number' if leg<1 else
           '2. Shift in position' if leg<2 else
           '3. Undo the wave-number shift' if leg<3 else
           '4. Undo the position shift' if t<33 else
           'The loop closes. A phase remains.' if t<39 else
           'Shrink the loop: the same phase generator')
    s=Scene(4, EPISODES[4].get('video_title', EPISODES[4]['title']),stage,t,46)
    s.panel((70,485,950,911),'The full complex function')
    box=(119,575,902,815)
    _gaussian_envelope(s,0,box,139,_dim(GOLD,.45),domain=(-5,5))
    _complex(s,LOOP_X,_loop_base(LOOP_X),box,139,_dim(INK,.36),3)
    _gaussian_envelope(s,a,box,139,GOLD,domain=(-5,5))
    values=np.exp(1j*(b*LOOP_X+phase))*_loop_base(LOOP_X-a)
    _complex(s,LOOP_X,values,box,139,BLUE,4)
    s.text(115,844,'Gray: initial function',30,MUTED)
    s.text(899,844,'Gold: magnitude',30,GOLD,anchor='ra')
    s.panel((70,935,505,1430),'Translation parameters')
    origin=_loop_points(0,0)
    s.arrow((126,1344),(466,1344),GRID,2,12)
    s.arrow((126,1344),(126,1043),GRID,2,12)
    s.text(471,1320,'x',32,MUTED)
    s.text(111,1003,'k',32,MUTED)
    vertices=[_loop_points(0,0),_loop_points(0,LOOP_B*loop_scale),
              _loop_points(LOOP_A*loop_scale,LOOP_B*loop_scale),
              _loop_points(LOOP_A*loop_scale,0),origin]
    s.line(vertices,GRID,3)
    current=_loop_points(a,b)
    idx=min(int(leg),3)
    s.line(vertices[:idx+1]+[current],GOLD,5)
    s.dot(current,9,GOLD)
    s.text(300,1371,'+k → +x → −k → −x',30,INK,anchor='ma')
    s.panel((525,935,950,1430),'What comes back?')
    if t<31.8:
        s.text(737,1068,'Position shift',30,MUTED,anchor='ma')
        s.text(737,1120,f'{a:+.2f}'.replace('-','−'),40,BLUE,anchor='ma')
        s.text(737,1210,'Wave-number shift',30,MUTED,anchor='ma')
        s.text(737,1262,f'{b:+.2f}'.replace('-','−'),40,RED,anchor='ma')
    else:
        cx,cy,r=737,1174,111
        s.d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=GRID,width=2)
        s.arrow((cx,cy),(cx+r,cy),_dim(INK,.5),3,13)
        phasor(s,(cx,cy),np.exp(1j*phase),r,GOLD,6)
        if t<39:
            # The traced angle explains the already-completed loop result.
            arc=np.linspace(0,-phase*ease(window(t,31.8,35.5)),120)
            s.line(np.c_[cx+.72*r*np.cos(arc),cy+.72*r*np.sin(arc)],GOLD,3)
        label='φ = −ab = −π/2' if t<39 else f'φ = {phase/np.pi:.3f}π'.replace('-','−')
        s.text(cx,1323,label,33,GOLD,anchor='ma')
    if t<39:
        s.math(r'U_{\rm loop}\psi=e^{-iab}\psi',y=1490,size=47)
        s.note('The position and wave number return. Phase does not.',size=30)
    else:
        s.math(r'[\hat X,\hat K]=iI',y=1470,size=49)
        s.math(r'[\hat X,I]=[\hat K,I]=0',y=1535,size=45)
        s.note('Position, wave number, phase: the group H₃.',size=30)
    return s.im


def validate():
    """Independent quadratures and exact identities; no image-based asserts."""
    q=np.linspace(-18,22,24001)
    overlaps=[]; norms=[]
    for sign in (1,-1):
        for shift in (-1.5,0,1.7):
            f=_state(q,PAIR[0],sign,shift);g=_state(q,PAIR[1],sign,shift)
            overlaps.append(np.trapezoid(np.conj(f)*g,q))
            norms.extend([np.trapezoid(abs(f)**2,q),np.trapezoid(abs(g)**2,q)])
    max_overlap_error=float(max(abs(v-OVERLAP) for v in overlaps))
    max_norm_error=float(max(abs(v-1) for v in norms))
    k=np.linspace(-1,8,51)
    fourier=np.array([np.trapezoid(_state(q)*np.exp(-1j*kv*q),q)/np.sqrt(2*np.pi)
                      for kv in k])
    fourier_error=float(np.max(abs(fourier-_state(k,sign=-1))))
    # Direct application of +k,+x,-k,-x, independently of the frame state.
    x=np.linspace(-4,4,503)
    translated=np.exp(-1j*LOOP_B*(x+LOOP_A))*np.exp(1j*LOOP_B*x)*_loop_base(x)
    loop_error=float(np.max(abs(translated-np.exp(-1j*LOOP_A*LOOP_B)*_loop_base(x))))
    modes_error=float(max(np.max(abs((MODE_BASE*np.exp(1j*p)).sum(0)-SUM_BASE*np.exp(1j*p)))
                           for p in (.25,1.3,4.7)))
    magnitude_error=float(max(np.max(abs(abs(SUM_BASE*np.exp(1j*p))-abs(SUM_BASE)))
                               for p in (.25,1.3,4.7)))
    assert max_overlap_error<1e-12 and max_norm_error<1e-12 and fourier_error<1e-12
    assert loop_error<1e-12 and modes_error<1e-12 and magnitude_error<1e-12
    return {'overlap':OVERLAP,'overlap_quadrature_error':max_overlap_error,
            'fourier_pair_quadrature_error':fourier_error,
            'unit_norm_error':max_norm_error,'loop_residual_error':loop_error,
            'exact_mode_sum_error':modes_error,'phase_magnitude_error':magnitude_error,
            'loop_area':float(LOOP_A*LOOP_B)}


EPISODES={
    1:{'title':'A wave can shift two ways','duration':44,'render':episode_1,
       'checkpoints':[0,5,11,18,27,33,41],
       'caption':"We can slide a wave function in position. We can also slide it in wave number (inversely proportional to wavelength), which shifts the collection of spatial frequencies that compose it. While shifting the wave number isn't a translation in the familiar physical space we live in, from a mathematical perspective, wave-number-space is the dual, or equivalent up to role reversal, of position-space.\n\nThese are separate transformations of the same starting function. Position translation is shown in position space, while wave-number translation is shown in wave-number space. In these respective representations, the operations appear as a simple shift of the function. For shifts a and b, ψ(x) → ψ(x − a) and ψ̃(k) → ψ̃(k − b). The gold outline tracks the wave function's magnitude. The coiled curve includes both real and imaginary components.\n\nThe two spaces are related by Fourier transformation. The moving control is a translation amount, not the passage of physical time.",
       'validation':{'representations':'Exact normalized Weyl-displaced Gaussian Fourier pair; separate experiments.'}},
    2:{'title':'What a translation preserves','duration':44,'render':episode_2,
       'checkpoints':[0,6,13,20,28,36,43],
       'caption':"A symmetry is defined by what it leaves unchanged. Translate two wave functions by the same amount, and their inner product — intuitively, their overlap — stays the same. This is unitarity, an extension of orthogonal transformations to complex functions. Writing either translation as T, ⟨Tψ, Tχ⟩ = ⟨ψ, χ⟩.\n\nThe upper panels show two independent translations -- position translations in position space, and wave-number translations in wave-number space. Both preserve the overlap of the cyan and red functions.\n\nBelow, the same relationship is shown schematically as a pair of unit vectors in wave function representation space. Their common motion preserves the angle between them and the length of one vector's projection onto the other. We chose functions with real, positive overlap so that this ordinary projection picture applies. If the angle between these unit vectors is θ, ⟨ψ, χ⟩ = cos θ. A general complex overlap is preserved as well.",
       'validation':{'overlap':OVERLAP,'geometry':'Real-positive overlap schematic, not a 3D embedding of the full function space.'}},
    3:{'title':'Phase turns the function','duration':44,'render':episode_3,
       'checkpoints':[0,2.2,8.8,14,23,33,43],
       'caption':'Multiply a complex wave function by eⁱᵠ, and every complex value rotates by the same angle φ. That is a global phase shift: ψ → eⁱᵠψ.\n\nOn the right are nine modes. On the left is their exact sum, drawn at the same amplitude scale. All nine turn by the same fraction of a cycle. Their sum turns with them, while its magnitude envelope stays fixed. In symbols, |eⁱᵠψ(x)| = |ψ(x)|. Five full turns are shown.\n\nWhile phase translation and position translation result in the same transformation for pure modes, phase translation acting on the wave packet as a whole leaves its position unchanged.',
       'validation':{'modes':9,'sum':'Exact finite complex Fourier sum, single fixed normalization, common display amplitude scale.'}},
    4:{'title':'Phase in the symmetry group structure','duration':46,'render':episode_4,
       'checkpoints':[0,5,12,20,28,33,38,44],
       'caption':'A commutator is defined by [X̂, Ŷ] = X̂Ŷ − ŶX̂. The corresponding test for finite translations is to move the function around a loop and examine what changes when the loop closes. Here we shift a function by b in wave number, then by a in position. Then, undo the wave-number shift, undo the position shift, and observe the effect of turning the function.\n\nThe whole loop multiplies it by e⁻ⁱᵃᵇ. Here ab = π/2, so a quarter-turn of phase remains. The gray curve is the starting function. The gold magnitude envelope returns exactly. This residual phase is shared by every mode, so the result applies to their sum.\n\nAs the loop shrinks, its phase shrinks with its area. The infinitesimal relation is [X̂,K̂] = iI. Commuting either generator with I gives zero so that position, wave number, and phase close into the three-dimensional Heisenberg group H₃. To be clear, this is a loop in translation parameters, not physical space.',
       'validation':{'chronological_loop':['+k','+x','-k','-x'],'a':LOOP_A,'b':float(LOOP_B),'residual_phase':float(-LOOP_A*LOOP_B)}}
}
