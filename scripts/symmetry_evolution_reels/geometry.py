"""Portrait view of the verified six-state Gaussian mean-patch model."""
from __future__ import annotations
from core import *
import symmetry_mean_patch as model

DURATION=42
MOMENTS=(0,3,7.5,12,18,23,28,32,35,38,41.9)
COLORS=(BLUE,GOLD,GREEN,PURPLE,RED,'#d8df73')
X=np.linspace(-7.5,7.5,801)
INITIAL_GRID=model.initial_grid(18,18)

def parameters(t):
    if t<15: return 0.,0.
    if t<22: return model.TAU_MAX*ease((t-15)/7),0.
    if t<24: return model.TAU_MAX,0.
    if t<31: return model.TAU_MAX,model.R_MAX*ease((t-24)/7)
    if t<33: return model.TAU_MAX,model.R_MAX
    if t<36.5: return model.TAU_MAX,model.R_MAX*(1-ease((t-33)/3.5))
    if t<40: return model.TAU_MAX*(1-ease((t-36.5)/3.5)),0.
    return 0.,0.

def plane(points):
    return np.array([510.,1298.])+np.asarray(points)*np.array([70.,-59.])

def color_mix(color,amount):
    from PIL import ImageColor
    a=np.array(ImageColor.getrgb(color)); b=np.array(ImageColor.getrgb(PANEL))
    return tuple(np.round(amount*a+(1-amount)*b).astype(int))

def line(d,p,color,width=2):
    d.line([tuple(v) for v in p],fill=color,width=width)

def dot(d,p,n,color,r=15):
    x,y=p
    d.ellipse((x-r,y-r,x+r,y+r),fill=color)
    text(d,(x,y-1),str(n),21,BG,anchor='mm',bold=True)

def render(index,t):
    assert index==5
    if t<9: stage='Map the waves to their averages'
    elif t<15: stage='Each cell follows a family of states'
    elif t<24: stage='Shear the patch and evolve the waves'
    elif t<33: stage='Stretch one direction, compress the other'
    else: stage='Reverse the evolution'
    im,d=frame(TITLES[5],5,t,DURATION,stage)
    math(im,r'\psi\ \longmapsto\ (\langle\hat X\rangle_\psi,\langle\hat K\rangle_\psi)',(510,515),40)
    d.rounded_rectangle((70,555,950,993),radius=16,fill=PANEL)
    d.rounded_rectangle((70,1030,950,1548),radius=16,fill=PANEL)
    tau,r=parameters(t)
    waves=model.waves(X,tau,r); means=model.means(tau,r)
    active=min(5,max(0,int((t-1)/1.05))) if t<7.3 else -1
    for j,(wave,c) in enumerate(zip(waves,COLORS)):
        base=601+j*67
        opacity=1 if active in (-1,j) else .45
        dot(d,(96,base),j+1,color_mix(c,opacity),13)
        xx=140+(X+7.5)/15*770
        line(d,[(140,base),(910,base)],GRID,1)
        z=wave*np.exp(-1j*np.pi*22/180)
        for sign in (-1,1):
            line(d,np.c_[xx,base+sign*38*np.abs(z)],color_mix(c,.23*opacity),1)
        p=np.c_[xx+17*z.imag,base-38*z.real]
        front=z.imag[:-1]+z.imag[1:]>=0
        changes=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
        for a,b in zip(changes[:-1],changes[1:]):
            line(d,p[a:b+1],color_mix(c,opacity*(1 if front[a] else .45)),3)
    text(d,(910,969),'position x →',23,MUTED,anchor='rt')
    # A single map arrow connects the wave panel to the means panel.
    line(d,[(510,996),(510,1024)],GOLD,3)
    d.polygon([(502,1016),(518,1016),(510,1027)],fill=GOLD)
    for v in range(-5,6):
        p=plane([v,0]); line(d,[p+[-0, -4],p+[0,4]],GRID,1)
    for v in range(-4,5):
        p=plane([0,v]); line(d,[p+[-4,0],p+[4,0]],GRID,1)
    line(d,plane([[-5.8,0],[5.8,0]]),GRID,2)
    line(d,plane([[0,-3.95],[0,3.95]]),GRID,2)
    math(im,r'\langle\hat X\rangle',(913,1329),28,MUTED)
    math(im,r'\langle\hat K\rangle',(554,1064),28,MUTED)
    reveal=float(ease((t-8)/2))
    if reveal:
        grid=model.evolve_points(INITIAL_GRID,tau,r)
        corners=plane(np.array([grid[0,0],grid[0,-1],grid[-1,-1],grid[-1,0]]))
        d.polygon([tuple(p) for p in corners],fill=color_mix(BLUE,.045*reveal))
        for j in range(19):
            line(d,plane(grid[j]),color_mix(MUTED,.43*reveal),1)
            line(d,plane(grid[:,j]),color_mix(MUTED,.43*reveal),1)
        line(d,np.vstack([corners,corners[0]]),color_mix(BLUE,.85*reveal),3)
        cell=grid[11:13,13:15]
        cp=plane(np.array([cell[0,0],cell[0,1],cell[1,1],cell[1,0],cell[0,0]]))
        line(d,cp,GOLD,3)
    count=6 if t>=7.3 else max(0,min(6,int((t-1)/1.05)+1))
    for j in range(count):
        p=plane(means[j]); dot(d,p,j+1,COLORS[j])
        if j==active:
            d.ellipse((p[0]-21,p[1]-21,p[0]+21,p[1]+21),outline=COLORS[j],width=2)
    area=model._polygon_area(model.evolve_points(model.INITIAL_CORNERS,tau,r))
    text(d,(95,1515),f'Patch area  {area:.2f}',26,GOLD)
    text(d,(925,1515),'same throughout',25,MUTED,anchor='rt')
    text(d,(510,1585),'A family whose averages shear and stretch together',27,MUTED,anchor='mm')
    return im

def validate():
    result=model.validate()
    assert result['passed']
    # Confirm every mapped corner stays within the visible scientific panel.
    pts=np.concatenate([plane(model.evolve_points(model.INITIAL_CORNERS,*parameters(t)))
                        for t in np.linspace(0,DURATION,300)])
    assert pts[:,0].min()>80 and pts[:,0].max()<940
    assert pts[:,1].min()>1060 and pts[:,1].max()<1515
    result['portrait_patch_bounds']=[*pts.min(axis=0).tolist(),*pts.max(axis=0).tolist()]
    return result
