"""A Casimir construction in the ordinary three-dimensional vector representation.

All three fixed-axis squared-generator actions are recomputed as the input
rotates. They are output vectors, not squared components or expectation values.
"""
from __future__ import annotations

from core import *

DURATION = 34
TITLE = "Building a Casimir operator"
SCREEN_TEXT = [
    "Three generators, one invariant", "Add the three contributions", "Turn the vector",
    r"C=-(J_x^2+J_y^2+J_z^2)",
    r"-J_x^2\mathbf{v}", r"-J_y^2\mathbf{v}", r"-J_z^2\mathbf{v}",
    r"x\to0", r"y\to0", r"z\to0", "x", "y", "z",
    "Input", "Sum", r"\mathbf{v}", r"2\mathbf{v}",
    r"C\mathbf{v}=2\mathbf{v}", r"C=2I", "Ordinary 3D vector representation",
]

GENERATORS = np.array([
    [[0,0,0], [0,0,-1], [0,1,0]],
    [[0,0,1], [0,0,0], [-1,0,0]],
    [[0,-1,0], [1,0,0], [0,0,0]],
], dtype=float)
TERMS = np.array([-j @ j for j in GENERATORS])
RIGHT = np.array([.8, -.6, 0.])
# Fixed orthographic view, x and y below the horizon, z above it.
UP = np.array([-.3, -.4, math.sqrt(.75)])
CAMERA = np.array([RIGHT, -UP])
COLORS = (BLUE, RED, GREEN)


def state(t):
    initial = np.array([.72, -.5, .62])
    radius = float(np.linalg.norm(initial))
    polar = math.acos(initial[2]/radius)
    azimuth = math.atan2(initial[1], initial[0])
    turn = 2*math.pi*float(ease(window(t, 16, 31)))
    # Keep the input away from the camera's sightline so its projected
    # arrow never collapses into an unreadable dot during the turn.
    polar -= .30*math.sin(turn)
    azimuth += turn
    return radius*np.array([math.sin(polar)*math.cos(azimuth),
                            math.sin(polar)*math.sin(azimuth), math.cos(polar)])


def project(origin, scale, v):
    return np.asarray(origin)+scale*(CAMERA @ np.asarray(v))


def dashed(scene, a, b, color=MUTED, width=2):
    a, b = np.asarray(a), np.asarray(b)
    length = float(np.linalg.norm(b-a))
    for start in np.arange(0, length, 12):
        scene.line([a+(b-a)*start/length,
                    a+(b-a)*min(start+6, length)/length], color, width)


def backed_text(scene, x, y, label, size=28, color=INK, anchor="mm"):
    actual = TEXT_REPLACEMENTS.get(label, label)
    b = scene.d.textbbox((x,y), actual, font=font(size), anchor=anchor)
    scene.d.rounded_rectangle((b[0]-4,b[1]-2,b[2]+4,b[3]+2), radius=3, fill=BG)
    scene.text(x,y,label,size,color,anchor=anchor)


def backed_math(scene, x, y, tex, size=30, color=GOLD):
    actual = TEXT_REPLACEMENTS.get(tex,tex)
    pic = equation(actual,size,color)
    left, top = round(x-pic.width/2), round(y-pic.height/2)
    scene.d.rounded_rectangle((left-4,top-3,left+pic.width+4,top+pic.height+3),
                              radius=3,fill=BG)
    scene.im.paste(pic,(left,top),pic)


def axes3(scene, origin, scale, labels=True):
    for axis, name in zip(np.eye(3), ("x","y","z")):
        scene.line([project(origin,scale,-axis*.95), project(origin,scale,axis*1.13)], GRID, 2)
        if labels:
            pos = project(origin,scale,axis*1.3)
            backed_text(scene,*pos,name,23,MUTED)


def vector_arrow(scene, origin, scale, tail, tip, color, width=6):
    start, end = project(origin,scale,tail), project(origin,scale,tip)
    scene.arrow(start,end,BG,width+4,19)
    scene.arrow(start,end,color,width,16)


def render(t, entry):
    title = entry.get('title', TITLE)
    stage = SCREEN_TEXT[0 if t<8 else 1 if t<16 else 2]
    s = Scene(entry.get('order',16),title,stage,t,DURATION)
    s.math(SCREEN_TEXT[3],y=512,size=46)
    s.text(70,583,'Input',27,GOLD)
    s.arrow((161,602),(213,602),GOLD,5,13)
    s.math(r'\mathbf{v}',x=239,y=601,size=32,color=GOLD)

    v = state(t)
    outputs = np.array([term @ v for term in TERMS])
    for axis, (cx, color, output) in enumerate(zip((210,510,810),COLORS,outputs)):
        s.panel((cx-140,647,cx+140,996))
        s.math(SCREEN_TEXT[4+axis],x=cx,y=690,size=35,color=color,maxwidth=240)
        origin, scale = np.array([cx,831.]), 99.
        retained = [i for i in range(3) if i!=axis]
        plane = []
        for aa,bb in ((-1,-1),(1,-1),(1,1),(-1,1)):
            q = np.zeros(3)
            q[retained] = (aa*.82,bb*.82)
            plane.append(project(origin,scale,q))
        s.d.polygon([tuple(p) for p in plane],fill=('#162b3c','#331c2b','#13352f')[axis])
        s.line(plane+plane[:1],('#2b5c7b','#78425a','#2c735e')[axis],2)
        axes3(s,origin,scale)
        vector_arrow(s,origin,scale,np.zeros(3),v,GOLD,4)
        reveal = float(ease(window(t,2+axis*1.55,3+axis*1.55)))
        if reveal>0:
            current = lerp(v,output,reveal)
            dashed(s,project(origin,scale,v),project(origin,scale,current),MUTED)
            vector_arrow(s,origin,scale,np.zeros(3),current,color,6)
        if t>=3+axis*1.55:
            s.math(SCREEN_TEXT[7+axis],x=cx,y=958,size=32,color=color,maxwidth=210)

    s.text(70,1040,'Sum',30,MUTED)
    # Start with all three outputs at one origin, then move copies tip to tail.
    origin, scale = np.array([510.,1422.]), 155.
    axes3(s,origin,scale*.88,labels=False)
    if t>=7:
        add = float(ease(window(t,7,8)))
        tail = np.zeros(3)
        for i,(output,color) in enumerate(zip(outputs,COLORS)):
            assembled = 1. if i==0 else float(ease(window(t,8.5+(i-1)*2.1,10.5+(i-1)*2.1)))
            displayed_tail = tail*assembled
            vector_arrow(s,origin,scale,displayed_tail,displayed_tail+output*add,color,6)
            if assembled==1:
                s.dot(project(origin,scale,displayed_tail+output*add),5,color)
            tail += output
        if t>=13:
            reveal = float(ease(window(t,13,14)))
            vector_arrow(s,origin,scale,np.zeros(3),2*v*reveal,GOLD,4)
            s.dot(project(origin,scale,v),7,GOLD)
            halfway = project(origin,scale,v)
            backed_math(s,halfway[0]-18,halfway[1]+20,r'\mathbf{v}',27)
            end = project(origin,scale,2*v)
            backed_math(s,end[0]+23,end[1]-23,r'2\mathbf{v}',30)
            s.math(r'C\mathbf{v}=2\mathbf{v}',x=280,y=1567,size=46,color=GOLD,maxwidth=400)
            s.math(r'C=2I',x=754,y=1567,size=46,color=GOLD,maxwidth=260)
    s.text(510,1623,'Ordinary 3D vector representation',27,MUTED,anchor='ma')
    return s.im


def validate():
    assert np.allclose(sum(TERMS),2*np.eye(3))
    assert np.allclose(CAMERA @ CAMERA.T,np.eye(2))
    for t in np.linspace(0,DURATION,205):
        v = state(t)
        outputs = np.array([term @ v for term in TERMS])
        assert np.allclose(outputs.sum(axis=0),2*v)
        assert np.allclose(np.diag(outputs),0)
        assert abs(np.linalg.norm(v)-np.linalg.norm(state(0)))<1e-12
        chain = np.cumsum(np.vstack((np.zeros(3),outputs)),axis=0)
        points = np.array([project((510,1422),155,q) for q in chain])
        assert points[:,0].min()>100 and points[:,0].max()<935
        assert points[:,1].min()>1080 and points[:,1].max()<1525, (t,points)
    return {'matrix_sum':'2I','rotation_samples':205,'vector_sum':'2v','sum_in_bounds':True}
