"""Desktop adaptation of reel 8: the two invariants of the D3 plane.

Three 120-degree turns return the vector to its start. Interpolated motion
is explicitly distinguished from the allowed endpoints. A live trace
shows that length alone permits all rotations while the cubic invariant
returns at each discrete endpoint. --render --check encodes and verifies.
"""
from symmetry_desktop_d3 import *

NAME='symmetry-d3-invariants'
DURATION=30
MOMENTS=[0,4,7,9,13,16,18,22,25,27,28.5,29.8]
THETA0=np.pi/12
U0=np.cos(3*THETA0)
CENTER=np.array([410.,450.])
RADIUS=260


def phase(t):
    if t>=27:return 2*np.pi,True
    step=min(int(max(t,0)/9),2)
    p=ease((t-step*9-1.8)/4.8)
    return (step+p)*2*np.pi/3,p<1e-8 or p>1-1e-8


def pxy(angle):
    return CENTER+RADIUS*np.array([math.cos(angle),-math.sin(angle)])


def render(t):
    s=Canvas()
    a,endpoint=phase(t)
    theta=THETA0+a
    x,y=math.cos(theta),math.sin(theta)
    u=x**3-3*x*y*y
    s.text(55,40,'What the Triangle’s Symmetries Preserve',36,INK,True)
    s.text(55,99,'Three successive 120° rotations',25,MUTED)
    s.line([(780,180),(780,790)],FAINT,2)
    s.d.ellipse((*tuple(CENTER-RADIUS),*tuple(CENTER+RADIUS)),outline=FAINT,width=3)
    s.arrow(CENTER+[-310,0],CENTER+[315,0],GRID,2)
    s.arrow(CENTER+[0,305],CENTER+[0,-285],GRID,2)
    s.math(744,450,'x',27)
    s.math(439,166,'y',27,center=True)
    for i in range(3):
        p=pxy(THETA0+i*2*np.pi/3)
        s.dot(p,14,BG,GOLD,3)
    # Light chord lines mark the three discrete endpoints, not a continuous orbit.
    vertices=np.array([pxy(THETA0+i*2*np.pi/3) for i in range(4)])
    s.line(vertices,FAINT,2)
    q=pxy(theta)
    s.arrow(CENTER,q,BLUE,6)
    s.dot(q,9,BLUE)
    status='Allowed rotation endpoint' if endpoint else 'Between the allowed rotation endpoints'
    s.text(410,795,status,24,GREEN if endpoint else MUTED,anchor='mm')
    s.text(825,202,'Squared length',27,INK,True)
    s.math(825,273,r'r^2=x^2+y^2',37)
    s.text(1460,273,'1.000',36,GREEN,True,'mm')
    s.text(825,344,'Cubic invariant',27,INK,True)
    s.math(825,414,r'u=x^3-3xy^2=r^3\cos(3\theta)',34)
    s.text(825,478,'Current',23,MUTED)
    s.text(1460,478,'At the start',23,MUTED,anchor='ra')
    s.text(825,523,f'{u:+.3f}',36,GREEN if endpoint else BLUE,True)
    s.text(1460,523,f'{U0:+.3f}',36,MUTED,anchor='ra')
    # A trace makes the recurring equality visible instead of only counting numbers.
    left,right,top,bottom=860,1480,625,755
    mid=(top+bottom)/2
    amp=(bottom-top)/2
    qangle=np.linspace(0,2*np.pi,300)
    fullu=np.cos(3*(THETA0+qangle))
    trace=np.c_[left+(right-left)*qangle/(2*np.pi),mid-amp*fullu]
    s.line([(left,top),(left,bottom),(right,bottom)],GRID,2)
    s.math(832,625,'u',24,center=True)
    s.line([(left,mid-amp*U0),(right,mid-amp*U0)],FAINT,2)
    n=max(1,int(a/(2*np.pi)*299))
    s.line(trace[:n+1],BLUE,3)
    for i in range(4):
        xx=left+(right-left)*i/3
        s.dot((xx,mid-amp*U0),5,GOLD)
        s.text(xx,780,f'{i*120}°',21,MUTED,anchor='mm')
    current=(left+(right-left)*a/(2*np.pi),mid-amp*u)
    s.dot(current,7,GREEN if endpoint else BLUE)
    s.text(1170,834,'Rotation from the starting vector',23,MUTED,anchor='mm')
    s.check()
    return s.im


def validate():
    errors=[]
    for x,y in np.random.default_rng(84).normal(size=(100,2)):
        r2=x*x+y*y;u=x**3-3*x*y*y
        for turn in range(3):
            a=turn*2*np.pi/3
            rot=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])
            for reflection in (np.eye(2),np.diag([1,-1])):
                xx,yy=rot@reflection@np.array([x,y])
                errors.append(max(abs(xx*xx+yy*yy-r2),abs(xx**3-3*xx*yy*yy-u)))
    assert max(errors)<1e-12
    for i in range(4):
        a=THETA0+i*2*np.pi/3
        assert abs(math.cos(3*a)-U0)<1e-12
    lengths=[]
    for t in np.linspace(0,DURATION,200):
        a,_=phase(t)
        lengths.append(float(np.linalg.norm(pxy(THETA0+a)-CENTER)/RADIUS))
    assert max(abs(np.array(lengths)-1))<1e-14
    return {'full_D3_actions_checked':600,'max_invariant_error':max(errors),
            'rotation_step_degrees':120,'initial_angle_degrees':15,
            'fixed_r_squared':1,'endpoint_cubic_value':float(U0),
            'interpolated_motions_are_not_group_actions':True,
            'length_max_error':float(max(abs(np.array(lengths)-1)))}


if __name__=='__main__':
    run(NAME,DURATION,MOMENTS,7,render,validate,__file__)
