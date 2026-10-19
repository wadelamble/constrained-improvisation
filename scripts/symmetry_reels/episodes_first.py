"""Portrait-first mathematical scenes 1–8; no media or manuscript side effects.

The collision state reuses the accepted chapter model. Other scenes evaluate
the same matrices, orbits and vector fields directly in portrait coordinates.
Discrete-group interpolation is shown as motion, never as an extra D3 action.
"""
from __future__ import annotations
from core import *

# Ordered strings are copied into the editable reel document. Label/equation
# edits in that document flow into the renderer by the same stable positions.
SCREEN_TEXT = {
    1: ['Position translation', 'Time translation', 'Rotation', 'Velocity boost',
        'Reference experiment', 'Transformed experiment',
        r"\mathbf{x}'=\mathbf{x}+\mathbf{a}", r"t'=t+b", r"\mathbf{x}'=R\mathbf{x}",
        r"\mathbf{x}'=\mathbf{x}+\mathbf{u}t", 'Equal masses · elastic collision'],
    2: ['Discrete symmetry actions', 'Identity', '120° rotation', '240° rotation',
        'Reflection', 'Reflection + 120°', 'Reflection + 240°',
        r'D_3=\{e,r,r^2,s,rs,r^2s\}', r'r^3=e', r's^2=e',
        'D₃ is more general than triangles'],
    3: ['Matrices act on component values', 'Rotation', 'Reflection',
        'Before', 'After', r'D(g_1g_2)=D(g_1)D(g_2)', r'R^3=I', r'S^2=I'],
    4: ['Common part and zero-sum part', 'Common part', 'Zero-sum part',
        r'\mathbf{v}=\overline{v}(1,1,1)+\mathbf{w}', r'w_1+w_2+w_3=0',
        r'\mathbf{3}=\mathbf{1}\oplus\mathbf{2}'],
    5: ['Invariants of discrete rotations', 'Allowed D₃ endpoints', 'Between endpoints',
        r'r^2=x^2+y^2', r'u=x^3-3xy^2=r^3\cos(3\theta)',
        'Squared length', 'Cubic invariant', 'Current', 'Reference'],
    6: ['Continuously varying parameters', 'Rotation', 'Translation',
        r'R(\theta)', r'T(a)', r'\theta\in\mathbb{R}', r'a\in\mathbb{R}'],
    7: ['Infinitesimal rotation', 'State', 'Tangent',
        r'\frac{d\mathbf{v}}{d\theta}=J\mathbf{v}', r'J^2=-I',
        r'e^{\theta J}=\cos\theta\,I+\sin\theta\,J', r'R(\theta)=e^{\theta J}'],
    8: ['The same generator at every state', 'Vector field', 'Flow',
        r'J(x,y)=(-y,x)', r'\frac{d\mathbf{v}}{d\theta}=J\mathbf{v}',
        r'\mathbf{v}(\theta)=e^{\theta J}\mathbf{v}(0)'],
}


def words(number, entry):
    supplied = entry.get('screen_text', entry.get('on_screen_text'))
    if supplied is not None and len(supplied) != len(SCREEN_TEXT[number]):
        raise ValueError(f'Reel {number}: expected {len(SCREEN_TEXT[number])} ordered on-screen text entries, found {len(supplied)}. Preserve the label slots when editing.')
    return SCREEN_TEXT[number] if supplied is None else supplied


def eq(scene, value, **kwargs):
    scene.math(value.strip('$'), **kwargs)


def circle(scene, center, radius, color=GRID, width=2):
    x, y = center
    scene.d.ellipse((x-radius,y-radius,x+radius,y+radius),outline=color,width=width)


def triangle(scene, points, colors=(BLUE,GOLD,RED), labels=('A','B','C'), ghost=False):
    scene.line(np.vstack([points,points[0]]), GRID if ghost else INK, 3 if ghost else 5)
    if not ghost:
        center=np.mean(points,axis=0)
        for point,color,label in zip(points,colors,labels):
            scene.dot(point,13,color)
            delta=point-center
            delta=delta/(np.linalg.norm(delta)+1e-10)*38
            scene.text(*(point+delta),label,36,color,True,'mm')


def number_vector(scene, values, x, y, color=INK, size=40, cell=62, colors=None):
    scene.matrix([[f'{v:g}' if isinstance(v,(int,float,np.integer,np.floating)) else v] for v in values],x,y,cell,size,color)
    if colors:
        for i,(v,c) in enumerate(zip(values,colors)):
            scene.text(x,y+(i-(len(values)-1)/2)*cell,str(v),size,c,anchor='mm')


@lru_cache(1)
def billiards():
    # Import a pure mathematical source module; do not run its main().
    import importlib.util
    spec=importlib.util.spec_from_file_location('symmetry_pool_source',ROOT/'scripts/generate_symmetry_pool_table.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pool_scene(t, entry):
    txt=words(1,entry)
    duration=entry['duration']; segment=duration/4
    stage=min(int(t/segment),3); local=t-stage*segment
    setup=float(ease(window(local,0,.65)))
    elapsed=window(local,.9,segment-1)*2.78
    source=billiards()
    r,a,u,b=source.transform(stage,setup)
    scene=Scene(1,entry['title'],txt[stage],t,duration)
    for index,cy in enumerate((740,1240)):
        box=(70,480+500*index,950,950+500*index)
        scene.panel(box,txt[4+index])
        origin=np.array([480.,cy]); scale=64.
        def transform(points):
            points=np.asarray(points)
            if not index:return points
            return points@r.T+a+u*elapsed
        # Both table and ball geometry transform together. Trails are attached
        # to the table, so the boost is applied at the current elapsed time.
        rails=np.array([[-3.15,-1.65],[3.15,-1.65],[3.15,1.65],[-3.15,1.65]])
        corners=origin+transform(rails)*[scale,-scale]
        scene.d.polygon([tuple(p) for p in corners],fill='#182d2c',outline=GRID,width=8)
        inner=origin+transform(rails*.97)*[scale,-scale]
        scene.line(np.vstack([inner,inner[0]]),MUTED,2)
        if elapsed<.03:
            cue=origin+transform(np.array([[-2.92,-.45],[-2.20,-.45]]))*[scale,-scale]
            scene.line(cue,MUTED,4)
        history=source.trajectory(np.linspace(0,elapsed,80))
        for j,color in enumerate((BLUE,GOLD)):
            trail=origin+transform(history[:,j,:])*[scale,-scale]
            scene.line(trail,color,3)
            q=source.trajectory(elapsed)[j]
            p=origin+transform(q)*[scale,-scale]
            scene.dot(p,source.RADIUS*scale,color)
        clock=elapsed+(b if index and stage==1 else 0)
        scene.text(912,box[1]+26,f't = {clock:4.1f}',30,MUTED,anchor='ra')
    eq(scene,txt[6+stage],y=1524,size=46)
    scene.text(510,1604,txt[10],30,MUTED,anchor='mm')
    return scene.im


@lru_cache(1)
def d3_carrier_paths():
    """Animated geometry of the chapter's symmetry-d3-carriers.svg.

    The repeated motifs are identical within each object. Circle centers use
    exact 120-degree rotations instead of the SVG's rounded 50.2 coordinate.
    Coordinates here are mathematical (positive y points upward).
    """
    angles=np.linspace(0,2*np.pi,97)
    unit=np.c_[np.cos(angles),np.sin(angles)]
    turns=[rotation(k*2*np.pi/3) for k in range(3)]
    circles=[(unit*38+np.array([0,58]))@r.T/96 for r in turns]
    u=np.linspace(0,1,65)[:,None]
    def bezier(a,b,c,d):
        return (1-u)**3*np.array(a)+3*(1-u)**2*u*np.array(b)+3*(1-u)*u*u*np.array(c)+u**3*np.array(d)
    petal=np.vstack([bezier((0,24),(34,58),(48,104),(0,130)),
                     bezier((0,130),(-48,104),(-34,58),(0,24))[1:]])
    petals=[petal@r.T/130 for r in turns]+[unit*18/130]
    right=np.linspace(-np.pi/2,np.pi/2,49)
    left=np.linspace(np.pi/2,3*np.pi/2,49)
    capsule=np.vstack([np.c_[42+14*np.cos(right),78+14*np.sin(right)],
                       np.c_[-42+14*np.cos(left),78+14*np.sin(left)]])
    capsule=np.vstack([capsule,capsule[0]])
    bars=[capsule@r.T/110 for r in turns]+[unit*18/110]
    theta=np.array([90,210,330])*np.pi/180
    base=np.c_[np.cos(theta),np.sin(theta)]
    return [[np.vstack([base,base[0]])],circles,petals,bars]


def triangle_scene(t, entry):
    txt=words(2,entry);duration=entry['duration']
    examples=t>=24
    if not examples:
        segment=4
        action=min(int(t/segment),5);local=t-action*segment
        progress=float(ease(window(local,.6,segment-1)))
    else:
        action=0 if t<26 else 1 if t<30.2 else 3
    scene=Scene(2,entry['title'],txt[10] if examples else txt[0],t,duration)
    scene.panel((70,480,950,1240),txt[action+1])
    if not examples:
        theta=np.array([90,210,330])*np.pi/180
        base=np.c_[np.cos(theta),np.sin(theta)]
        center=np.array([510,890]);scale=238
        ghost=center+base*[scale,-scale]
        triangle(scene,ghost,ghost=True)
        if action<3:
            q=base@rotation(action*2*np.pi/3*progress).T
        else:
            k=action-3
            fold=math.cos(np.pi*min(progress*2,1))
            q=base*np.array([fold,1])
            q=q@rotation(k*2*np.pi/3*max(2*progress-1,0)).T
            scene.line([(510,580),(510,1170)],GRID,2)
        triangle(scene,center+q*[scale,-scale])
    else:
        reveal=float(ease(window(t,24,25.5)))
        if action==1:
            transform=rotation(2*np.pi/3*float(ease(window(t,26.4,29))))
        elif action==3:
            transform=np.diag([math.cos(np.pi*float(ease(window(t,30.6,33.4)))),1])
        else:
            transform=np.eye(2)
        centers=[(290,755),(730,755),(290,1080),(730,1080)]
        for index,(center,paths) in enumerate(zip(centers,d3_carrier_paths())):
            center=np.array(center,dtype=float);scale=125.
            if index==0:
                center=lerp(np.array([510.,890.]),center,reveal)
                scale=lerp(238.,scale,reveal)
                color=INK
            else:
                if reveal<=0:
                    continue
                rgb=[int(INK[i:i+2],16) for i in (1,3,5)]
                bg=[int(PANEL[i:i+2],16) for i in (1,3,5)]
                color=tuple(round(b+(c-b)*reveal) for b,c in zip(bg,rgb))
            if action:
                for path in paths:
                    scene.line(center+path*[scale,-scale],GRID,2)
            for path in paths:
                scene.line(center+(path@transform.T)*[scale,-scale],color,4)
    labels=['e','r','r²','s','rs','r²s']
    for i,label in enumerate(labels):
        x=141+i*148
        scene.d.rounded_rectangle((x-52,1280,x+52,1370),radius=12,fill=PANEL,outline=GOLD if i==action else GRID,width=3)
        scene.text(x,1325,label,40,GOLD if i==action else MUTED,anchor='mm')
    eq(scene,txt[7],y=1465,size=43)
    eq(scene,txt[8],x=330,y=1552,size=44,maxwidth=350)
    eq(scene,txt[9],x=710,y=1552,size=44,maxwidth=350)
    return scene.im


def matrices_scene(t, entry):
    txt=words(3,entry);duration=entry['duration']
    scene=Scene(3,entry['title'],txt[0],t,duration)
    is_rotation=t<duration*.6
    base=np.array([1,3,5])
    if is_rotation:
        local=t/(duration*.6)*3
        step=min(int(local),2);p=float(ease(window(local-step,.15,.70)))
        before=np.roll(base,step);after=np.roll(before,1)
        matrix=np.array([[0,0,1],[1,0,0],[0,1,0]])
        symbol='R';perm=[1,2,0]
    else:
        local=(t-duration*.6)/(duration*.4)*2
        step=min(int(local),1);p=float(ease(window(local-step,.15,.70)))
        before=base if step==0 else base[[0,2,1]];after=before[[0,2,1]]
        matrix=np.array([[1,0,0],[0,0,1],[0,1,0]])
        symbol='S';perm=[0,2,1]
    scene.panel((70,480,950,955),txt[1 if is_rotation else 2])
    scene.text(205,711,symbol+' =',47,INK,anchor='mm')
    scene.matrix(matrix.tolist(),480,718,70,43,highlights=list(zip(*np.where(matrix==1))))
    eq(scene,txt[6 if is_rotation else 7],x=805,y=718,size=46,maxwidth=230)
    scene.panel((70,995,950,1410))
    scene.text(213,1034,txt[3],30,MUTED,anchor='ma')
    scene.text(811,1034,txt[4],30,MUTED,anchor='ma')
    ys=np.array([1140,1225,1310])
    colors=[{1:BLUE,3:GOLD,5:RED}[int(value)] for value in before]
    for i in range(3):
        scene.text(190,ys[i],str(before[i]),46,colors[i],True,'mm')
        target=perm[i]
        path=np.array([[270,ys[i]],[720,ys[target]]])
        scene.line(path,GRID,3)
        moving=lerp(path[0],path[1],p)
        scene.dot(moving,18,colors[i])
        if p>.98:
            scene.text(830,ys[target],str(before[i]),46,colors[i],True,'mm')
        else:
            scene.text(830,ys[target],'·',46,MUTED,True,'mm')
    eq(scene,txt[5],y=1530,size=43)
    return scene.im


@lru_cache(1)
def decomposition_geometry():
    # Reuse the desktop's geometry and camera instead of replacing its orbit
    # construction with a different visual argument. Importing is read-only.
    import importlib.util
    spec=importlib.util.spec_from_file_location(
        'reel_d3_geometry',ROOT/'scripts/symmetry_d3_rendering.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def decomposition_scene(t, entry):
    txt=words(4,entry);duration=entry['duration']
    scene=Scene(4,entry['title'],txt[0],t,duration)
    geom=decomposition_geometry()
    # The three desktop sample orbits have different heights AND radii.
    # Their planes coincide after subtracting the common component, but the
    # three triangles remain distinct. Their radial parts never change.
    samples=((1.96,1.06,BLUE),(1.38,.78,GOLD),(.86,.54,PURPLE))
    collapse=geom.ease(window(t,13,17))
    face=window(t,18,21.5)
    blend=geom.ease(face)
    origin=geom.mix2((280.,900.),(510.,890.),blend)
    projection=geom.Projection.from_blend(origin,235+25*blend,face)
    def project(q):
        return np.array(projection.project(tuple(q))[:2])
    def faded(color, alpha):
        rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
        bg=tuple(int(PANEL[i:i+2],16) for i in (1,3,5))
        return tuple(round(b+(c-b)*alpha) for b,c in zip(bg,rgb))
    scene.panel((70,480,950,1180))
    axes_alpha=1-blend
    if axes_alpha>.001:
        for i in range(3):
            endpoint=np.zeros(3);endpoint[i]=1.55
            tip=project(endpoint)
            scene.arrow(project((0,0,0)),tip,faded(MUTED,.55*axes_alpha),2,12)
            label_offset=(22,-17) if i==0 else (0,-25)
            scene.text(*(tip+label_offset),('x₁','x₂','x₃')[i],27,
                       faded(MUTED,axes_alpha),anchor='mm')
        scene.arrow(project(geom.mul(-.18,geom.U)),
                    project(geom.mul(2.65,geom.U)),
                    faded(INK,axes_alpha),3,14)
        if face<.5:
            scene.line([(115,540),(165,540)],INK,3)
            scene.text(185,540,txt[1],30,INK,anchor='lm')
    if face>=.5:
        scene.text(115,540,txt[2],30,BLUE,anchor='lm')

    # Draw each orbit through three 120-degree steps, retaining completed
    # triangles. Holds at each vertex distinguish the discrete group actions.
    vectors=[]
    for index,(height,radius,color) in enumerate(samples):
        local=t-(.6+3.6*index)
        if local<0 and index>0:
            continue
        if local<=0:
            progress=0.
        elif local>=3.6:
            progress=1.
        else:
            step=min(2,int(local/1.2))
            turn=geom.ease(window(local-1.2*step,.08,.98))
            progress=(step+turn)/3
        state=geom.state_vector(height,radius,45.,collapse)
        points=[tuple(project(point)) for point in geom.orbit(state)]
        if progress>=1:
            scene.d.polygon(points,fill=faded(color,.045))
        trace=geom.closed_partial(points,progress)
        scene.line(trace,color,5)
        for vertex,point in enumerate(points):
            if progress+1e-9>=vertex/3:
                scene.dot(point,6,color)
        vector_alpha=(1-geom.ease(window(t,11.4,12.3)))
        if local>=3.6:
            vector_alpha*=.35
        if vector_alpha>.001:
            point=project(geom.rotate_about_axis(state,360*progress))
            vectors.append((point,color,vector_alpha))
    for point,color,alpha in vectors:
        scene.arrow(project((0,0,0)),point,faded(color,alpha),3,13)
        scene.dot(point,7,faded(color,alpha))

    # This fixed numerical example illustrates the same decomposition as all
    # three orbit families. It is not a live coordinate readout of one orbit.
    number_vector(scene,[1,3,5],210,1323,cell=60)
    scene.text(293,1323,'=',44,INK,anchor='mm')
    number_vector(scene,[3,3,3],401,1323,GOLD,cell=60)
    scene.text(495,1323,'+',44,INK,anchor='mm')
    number_vector(scene,[-2,0,2],598,1323,BLUE,cell=60)
    eq(scene,txt[5],x=819,y=1323,size=43,maxwidth=245)
    eq(scene,txt[3],y=1489,size=42)
    eq(scene,txt[4],y=1578,size=42,color=BLUE)
    return scene.im


def invariants_scene(t, entry):
    txt=words(5,entry);duration=entry['duration']
    interval=(duration-2)/3
    local=max(0,t-1)/interval;step=min(int(local),2)
    within=local-step
    p=float(ease(window(within,.18,.72)))
    theta0=np.pi/12
    theta=theta0+2*np.pi/3*(step+p)
    endpoint=p<1e-5 or p>1-1e-5
    xy=np.array([np.cos(theta),np.sin(theta)])
    r2=float(xy@xy);u=float(xy[0]**3-3*xy[0]*xy[1]**2)
    u0=math.cos(3*theta0)
    scene=Scene(5,entry['title'],txt[0],t,duration)
    scene.panel((70,480,950,1180))
    c=np.array([510,845]);radius=258
    axes(scene,c,(-330,330),(-235,280))
    circle(scene,c,radius)
    for a in theta0+np.arange(3)*2*np.pi/3:
        q=c+np.array([np.cos(a),-np.sin(a)])*radius
        circle(scene,q,16,GOLD,3)
    point=c+xy*[radius,-radius]
    scene.arrow(c,point,BLUE,5)
    scene.dot(point,10,BLUE)
    scene.text(510,530,txt[1 if endpoint else 2],31,GREEN if endpoint else MUTED,anchor='ma')
    scene.math(r'\theta='+f'{math.degrees(theta):.0f}'+r'^\circ',y=1153,size=40)
    eq(scene,txt[3],x=510,y=1250,size=43)
    eq(scene,txt[4],x=510,y=1342,size=43)
    scene.panel((70,1408,950,1620))
    scene.text(570,1424,txt[7],27,MUTED,anchor='ma')
    scene.text(825,1424,txt[8],27,MUTED,anchor='ma')
    scene.text(100,1470,txt[5],29,MUTED)
    scene.text(100,1550,txt[6],29,MUTED)
    scene.text(570,1489,f'{r2:.3f}',40,GREEN,anchor='mm')
    scene.text(570,1569,f'{u:+.3f}',40,GREEN if endpoint else BLUE,anchor='mm')
    # Reference remains visible: cubic value varies during non-group motion.
    scene.text(825,1489,'1.000',30,MUTED,anchor='mm')
    scene.text(825,1569,f'{u0:+.3f}',30,MUTED,anchor='mm')
    return scene.im


def continuous_scene(t, entry):
    txt=words(6,entry);duration=entry['duration']
    angle=2*np.pi*window(t,1,duration-1)
    amount=3.5*np.sin(angle*.75)
    scene=Scene(6,entry['title'],txt[0],t,duration)
    scene.panel((70,480,950,1045),txt[1])
    center=np.array([510,770]);radius=177
    circle(scene,center,radius,MUTED,3)
    for a in np.linspace(0,2*np.pi,24,endpoint=False):
        radial=np.array([np.cos(a),-np.sin(a)])
        scene.line([center+radial*(radius-9),center+radial*(radius+9)],GRID,3)
    ray=np.array([np.cos(angle),-np.sin(angle)])
    scene.arrow(center,center+ray*radius,BLUE,5)
    scene.dot(center+ray*radius,11,BLUE)
    eq(scene,txt[3],x=805,y=770,size=48,maxwidth=180)
    eq(scene,txt[5],y=991,size=39)
    scene.panel((70,1080,950,1420),txt[2])
    y=1255
    scene.arrow((125,y),(893,y),GRID,3)
    for value in np.arange(-4,5):
        x=510+value*82
        scene.line([(x,y-18),(x,y+18)],GRID,3)
    for value in np.arange(-8,9):
        x=510+(value+amount)*82
        if 125<x<895:
            scene.line([(x,y-36),(x,y+36)],GOLD,4)
    eq(scene,txt[4],x=805,y=1365,size=44,maxwidth=200)
    scene.math(r'a='+f'{amount:+.2f}',x=360,y=1365,size=40,maxwidth=350)
    eq(scene,txt[6],y=1530,size=44)
    return scene.im


def generator_scene(t, entry):
    txt=words(7,entry);duration=entry['duration']
    angle=2*np.pi*window(t,3,duration-3)
    state=np.array([np.cos(angle),np.sin(angle)])
    tangent=np.array([-state[1],state[0]])
    scene=Scene(7,entry['title'],txt[0],t,duration)
    scene.panel((70,480,950,1090))
    center=np.array([510,792]);radius=170
    axes(scene,center,(-318,318),(-275,235))
    circle(scene,center,radius)
    p=center+state*[radius,-radius]
    scene.arrow(center,p,BLUE,5)
    scene.arrow(p,p+tangent*[radius,-radius],GOLD,5)
    scene.dot(p,10,BLUE)
    scene.text(110,520,txt[1],31,BLUE)
    scene.text(110,565,txt[2],31,GOLD)
    scene.math(r'\mathbf{v}',x=805,y=552,size=44,color=BLUE,maxwidth=80)
    scene.math(r'J\mathbf{v}',x=805,y=618,size=44,color=GOLD,maxwidth=140)
    scene.text(198,1240,'J =',48,INK,anchor='mm')
    scene.matrix([[0,-1],[1,0]],427,1240,73,45)
    eq(scene,txt[4],x=771,y=1240,size=44,maxwidth=250)
    eq(scene,txt[3],y=1400,size=47)
    eq(scene,txt[5],y=1510,size=42)
    eq(scene,txt[6],y=1597,size=41)
    return scene.im


def flow_scene(t, entry):
    txt=words(8,entry);duration=entry['duration']
    scene=Scene(8,entry['title'],txt[0],t,duration)
    scene.panel((70,480,950,1380))
    center=np.array([510,933]);scale=123
    angle=2*np.pi*window(t,2,duration-2)
    scene.text(112,522,txt[1],30,MUTED)
    scene.text(910,522,txt[2],30,BLUE,anchor='ra')
    axes(scene,center,(-325,325),(-337,337))
    for x in np.linspace(-2.1,2.1,7):
        for y in np.linspace(-2.1,2.1,7):
            q=np.array([x,y]);r=np.linalg.norm(q)
            if .1<r<2.7:
                p=center+q*[scale,-scale]
                tangent=np.array([-y,x])
                scene.arrow(p,p+tangent*[19,-19],'#8297b5',3,10)
    for radius in (1.,1.65,2.35):
        circle(scene,center,radius*scale,'#6c809d',2)
    for ring,radius in enumerate((1.,1.65,2.35)):
        for i in range(4):
            a=angle+i*np.pi/2+ring*.18
            p=center+np.array([np.cos(a),-np.sin(a)])*radius*scale
            scene.dot(p,8,(BLUE,GOLD,GREEN)[ring])
    # A material quadrilateral follows exactly the common SO(2) action.
    initial=np.array([[1.25,.05],[1.8,.05],[1.8,.48],[1.25,.48]])
    moving=initial@rotation(angle).T
    polygon=center+moving*[scale,-scale]
    scene.line(np.vstack([polygon,polygon[0]]),GOLD,4)
    eq(scene,txt[3],y=1448,size=43)
    eq(scene,txt[4],y=1525,size=43)
    eq(scene,txt[5],y=1600,size=42)
    return scene.im


RENDERERS = {1:pool_scene,2:triangle_scene,3:matrices_scene,4:decomposition_scene,
             5:invariants_scene,6:continuous_scene,7:generator_scene,8:flow_scene}


def render(number,t,entry):
    return RENDERERS[number](t,entry)


def validate():
    r=np.array([[0,0,1],[1,0,0],[0,1,0]])
    s=np.array([[1,0,0],[0,0,1],[0,1,0]])
    assert np.array_equal(np.linalg.matrix_power(r,3),np.eye(3))
    assert np.array_equal(s@s,np.eye(3))
    assert np.array_equal(s@r@s,r.T)
    assert np.array_equal(r@np.array([1,3,5]),[5,1,3])
    x=np.array([1.,3.,5.]);w=x-x.mean()
    assert abs(w.sum())<1e-12 and np.allclose(r@x,x.mean()+r@w)
    angles=np.linspace(0,2*np.pi,401)
    cubic=lambda a: np.cos(a)**3-3*np.cos(a)*np.sin(a)**2
    assert np.max(abs(cubic(angles)-cubic(angles+2*np.pi/3)))<1e-12
    assert np.max(abs(cubic(angles)-cubic(-angles)))<1e-12
    source=billiards()
    assert np.allclose(source.V0.sum(axis=0),source.V1.sum(axis=0))
    assert np.isclose(np.sum(source.V0**2),np.sum(source.V1**2))
    return dict(d3_relations='pass',decomposition='pass',cubic_endpoints='pass',
                collision_momentum_and_energy='pass')
