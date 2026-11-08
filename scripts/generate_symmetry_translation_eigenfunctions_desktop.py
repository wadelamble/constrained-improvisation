"""Desktop adaptation of the single-pass exponential eigenfunction reel.

The blue exponential stays fixed. A black working copy first scales onto its
derivative. In the second panel a copy translates, then another copy scales
onto the translated result. All intermediate black curves are constructions.
"""
from symmetry_exponential_desktop_common import *

NAME='symmetry-translation-eigenfunctions'
DURATION=28
LAMBDA=.5
SHIFT=1.8
MOMENTS=[0,3,6,9,12,16,19,23,27]
STAGES=[(0,'Differentiation scales an exponential.'),
        (2,'Halve every height of a copy. It meets the derivative at every point.'),
        (8,'The derivative is the original function multiplied by one number.'),
        (10,'Now slide a copy of the exponential to the right.'),
        (16,'Keep the translated curve in place.'),
        (18,'Scale a fresh copy vertically until it meets the translated curve.'),
        (24,'Translation is also multiplication by one number.')]
LEFT=(100,355,710,690)
RIGHT=(900,355,1510,690)


def motion(t):
    return progress(t,2,8),progress(t,10,16),progress(t,18,24)


def point(box,x,y):
    x,y=np.broadcast_arrays(np.asarray(x),np.asarray(y))
    l,t,r,b=box
    return np.stack((l+(x+2)/5*(r-l),b-y/5.2*(b-t)),axis=-1)


def axes(s,box):
    for y in (1,2,3,4):
        s.line(point(box,[-2,3],[y,y]),FAINT,2)
        s.text(box[0]-18,point(box,-2,y)[1],str(y),20,MUTED,anchor='rm')
    s.arrow(point(box,-2,0),point(box,3.08,0),MUTED,2,10)
    s.math(box[2]+26,box[3]+1,'x',25,MUTED)
    for x in (-2,0,2):
        p=point(box,x,0)
        s.line([p,p+[0,6]],MUTED,2)
        s.text(*p+[0,13],str(x),20,MUTED,anchor='ma')


def render(t):
    scaling,translation,comparison=motion(t)
    s=Canvas()
    s.text(52,39,'Translation Eigenfunctions Are Exponentials',36,INK,True)
    s.text(52,102,next(text for start,text in reversed(STAGES) if t>=start),27,MUTED)
    s.line([(800,185),(800,793)],FAINT,2)
    s.text(80,185,'Differentiation',28,INK,True)
    s.text(880,185,'Translation',28,INK,True)
    s.math(405,270,r'\frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}',36,center=True)
    s.math(1205,270,r'f(x-a)=e^{-\lambda a}f(x)',36,GREEN,center=True)
    s.text(405,312,'λ = ½',23,GOLD,anchor='ma')
    s.text(1205,312,f'a = {SHIFT*translation:.2f}',23,GREEN,anchor='ma')
    x=np.linspace(-2,3,600)
    f=np.exp(LAMBDA*x)
    axes(s,LEFT)
    axes(s,RIGHT)
    s.line(point(LEFT,x,f),BLUE,6)
    s.line(point(LEFT,x,LAMBDA*f),GOLD,6)
    multiplier=1+(LAMBDA-1)*scaling
    if t>=2:
        s.line(point(LEFT,x,multiplier*f),INK,2)
        for anchor in (-.4,1.1,2.5):
            val=math.exp(LAMBDA*anchor)
            a,b=point(LEFT,anchor,val),point(LEFT,anchor,multiplier*val)
            s.arrow(a,b,INK,2,10)
            s.dot(a,5,BLUE)
            s.dot(b,4,INK)
    s.line(point(RIGHT,x,f),BLUE,6)
    a=SHIFT*translation
    factor=math.exp(-LAMBDA*a)
    if t>=10:
        s.line(point(RIGHT,x,factor*f),GREEN,6)
        for anchor in (-.7,.65):
            val=math.exp(LAMBDA*anchor)
            start,end=point(RIGHT,anchor,val),point(RIGHT,anchor+a,val)
            s.arrow(start,end,GREEN,2,11)
            s.dot(start,5,BLUE)
            s.dot(end,6,GREEN)
    if t>=18:
        scale=1+(factor-1)*comparison
        s.line(point(RIGHT,x,scale*f),INK,2)
        for anchor in (-.4,1.1,2.5):
            val=math.exp(LAMBDA*anchor)
            s.arrow(point(RIGHT,anchor,val),point(RIGHT,anchor,scale*val),INK,2,10)
    s.math(405,766,r'f^\prime=\frac{1}{2}f',35,GOLD,center=True)
    if t>=16:
        s.math(1205,766,r'T_a f=e^{-0.9}f\approx0.407f',33,GREEN,center=True)
    else:
        s.math(1205,766,r'(T_a f)(x)=f(x-a)',33,GREEN,center=True)
    footer(s,t,DURATION,'Blue: original function     Gold: derivative     Green: translated function     Black: scaling a copy')
    return s.im


def validate():
    x=np.linspace(-2,3,1001)
    f=np.exp(LAMBDA*x)
    h=1e-5
    finite_difference=(np.exp(LAMBDA*(x+h))-np.exp(LAMBDA*(x-h)))/(2*h)
    derivative_error=float(np.max(abs(finite_difference-LAMBDA*f)))
    assert derivative_error<1e-9
    errors=[]
    for a in np.linspace(0,SHIFT,101):
        errors.append(float(np.max(abs(np.exp(LAMBDA*(x-a))-np.exp(-LAMBDA*a)*f))))
    assert max(errors)<1e-12
    samples=np.array([motion(t) for t in np.linspace(0,DURATION,281)])
    assert np.all(np.diff(samples,axis=0)>=-1e-12)
    assert np.allclose(samples[-1],1)
    for t in np.linspace(0,DURATION,57):
        render(t)
    return dict(derivative_finite_difference_error=derivative_error,
                translation_scaling_max_error=max(errors),translation_samples=101,
                monotone_single_pass=True,layout_bounds_frames=57)


if __name__=='__main__':
    run(NAME,DURATION,render,validate,MOMENTS,24,__file__)
