"""Desktop adaptation of reel 5: permutation matrices acting on components.

Run with --render --check to write a silent MP4 and decoded contact sheet.
Three applications of R and two of S recover the starting state. Values
remain attached to their colors while they are routed to different slots.
"""
from symmetry_desktop_d3 import *

NAME='symmetry-d3-transformation-matrices'
DURATION=34
R=np.array([[0,0,1],[1,0,0],[0,1,0]])
S=np.array([[1,0,0],[0,0,1],[0,1,0]])
BASE=np.array([1,3,5])
COLORS={1:BLUE,3:GOLD,5:RED}
MOMENTS=[0,3,5.5,9,11.5,17.5,21,23.5,27,29.5,31,33.8]


def state(t):
    rotation=t<18
    local=t if rotation else min(t-18,11.999999)
    step=min(int(local/6),2 if rotation else 1)
    phase=local-step*6
    matrix=R if rotation else S
    before=np.linalg.matrix_power(matrix,step)@BASE
    return rotation,step,phase,matrix,before,matrix@before


def bracket(s,x,y0,y1,left=True):
    cap=14 if left else -14
    s.line([(x+cap,y0),(x,y0),(x,y1),(x+cap,y1)],INK,3)


def render(t):
    s=Canvas()
    rotation,step,phase,matrix,before,after=state(t)
    symbol='R' if rotation else 'S'
    settled=phase>=4.5
    s.text(55,40,'Representing Symmetry with Matrices',36,INK,True)
    s.text(55,99,'The entries move to new slots. Their values stay the same.',25,MUTED)
    s.line([(630,180),(630,715)],FAINT,2)
    s.text(315,205,'120° rotation' if rotation else 'Flip',29,INK,True,'mm')
    s.math(125,430,symbol+'=',47)
    # The colored unit entry tells which input value each output row selects.
    xs=[300,390,480]
    ys=[330,430,530]
    for row in range(3):
        for col in range(3):
            value=int(matrix[row,col])
            color=COLORS[int(before[col])] if value else MUTED
            if value:
                s.d.rounded_rectangle((xs[col]-29,ys[row]-32,xs[col]+29,ys[row]+32),12,
                                       fill='#f1eadf')
            s.text(xs[col],ys[row],str(value),45,color,bool(value),'mm')
    bracket(s,250,288,574)
    bracket(s,530,288,574,False)
    s.math(320,655,r'R^3=I' if rotation else r'S^2=I',42,center=True)
    s.text(795,215,'Before',28,MUTED,anchor='mm')
    s.text(1420,215,'After',28,MUTED,anchor='mm')
    # The visible curved routes execute exactly the permutation encoded above.
    row_y=np.array([330.,450.,570.])
    perm=np.argmax(matrix,axis=0)
    for i in range(3):
        j=perm[i]
        color=COLORS[int(before[i])]
        s.text(720,row_y[i],str(i+1),23,MUTED,anchor='mm')
        s.text(795,row_y[i],str(before[i]),48,color,True,'mm')
        s.text(1495,row_y[j],str(j+1),23,MUTED,anchor='mm')
        q=np.linspace(0,1,80)
        yy=row_y[i]+(row_y[j]-row_y[i])*(3*q*q-2*q*q*q)
        points=np.c_[885+445*q,yy]
        s.line(points,FAINT,3)
        # Slightly offset start times keep crossing values visually separable.
        p=ease((phase-1.05-.22*i)/2.75)
        xy=(885+445*p,row_y[i]+(row_y[j]-row_y[i])*(3*p*p-2*p*p*p))
        s.dot(xy,21,BG)
        s.dot(xy,14,color)
        if p>=1:
            s.text(1420,row_y[j],str(before[i]),48,color,True,'mm')
        else:
            s.text(1420,row_y[j],'·',42,MUTED,anchor='mm')
    bracket(s,755,288,613)
    bracket(s,835,288,613,False)
    bracket(s,1380,288,613)
    bracket(s,1460,288,613,False)
    s.text(720,660,'slot',20,MUTED,anchor='mm')
    s.text(1495,660,'slot',20,MUTED,anchor='mm')
    s.math(1110,680,f'{symbol}'+('^'+str(step+1) if step else '')+r'\mathbf{v}',40,center=True)
    if t>=30:
        s.math(800,783,r'R^3\mathbf{v}=S^2\mathbf{v}=\mathbf{v}',39,center=True)
    else:
        s.math(800,783,r'D(g_1g_2)=D(g_1)D(g_2)',39,center=True)
    s.check()
    return s.im


def validate():
    assert np.array_equal(np.linalg.matrix_power(R,3),np.eye(3))
    assert np.array_equal(S@S,np.eye(3))
    assert np.array_equal(S@R@S,R.T)
    samples=0
    for matrix in (R,S):
        for v in np.random.default_rng(42).normal(size=(100,3)):
            mapping=np.argmax(matrix,axis=0)
            routed=np.empty(3)
            for i,j in enumerate(mapping):routed[j]=v[i]
            assert np.array_equal(routed,matrix@v)
            assert np.isclose(np.sum(v),np.sum(matrix@v))
            assert np.isclose(v@v,(matrix@v)@(matrix@v))
            samples+=1
    return {'rotation_matrix':R.tolist(),'reflection_matrix':S.tolist(),
            'relations':['R^3=I','S^2=I','SRS=R^-1'],
            'route_matrix_comparisons':samples,'values_preserved':True}


if __name__=='__main__':
    run(NAME,DURATION,MOMENTS,5.5,render,validate,__file__)
