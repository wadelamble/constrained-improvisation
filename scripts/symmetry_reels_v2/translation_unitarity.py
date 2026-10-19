"""Translation factors in one-dimensional exponential representations.

Two states in each representation are specified by coefficients c1 and c2.
Their inner product is conjugate(c1)*c2. The graphs show the associated
exponential functions. The fixed x=0 section displays their coefficients.
The real exponentials are formal eigenmodes, not normalizable L2(R) states.
This is not a comparison of full-line spatial integrals or moving windows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from core import *
import imageio_ffmpeg

OUT = ROOT / 'content/reels/symmetry-series-v2/translation-unitarity'
TITLE = 'Translation of complex exponentials preserves the inner product'
DURATION = 32
RATE = .24
K = 2*math.pi/3
REAL_C = np.array([.60, .95], dtype=complex)
COMPLEX_C = np.array([.60, .95*np.exp(.8j)])
COLORS = (BLUE, RED)
STAGES = [
    (0, 'Two copies of one exponential. Translate them together.'),
    (3, 'Real exponential factors stretch both amplitudes.'),
    (8, 'Their inner product changes with the translation.'),
    (12, 'Now translate the two complex exponentials.'),
    (15, 'Their lengths and relative angle stay the same.'),
    (25, 'Their inner product is unchanged. This is unitarity.'),
]


def shifts(t):
    return (-3*float(ease(window(t, 3, 10))),
            -3*float(ease(window(t, 14, 26))))


def coefficients(t):
    a, b = shifts(t)
    return REAL_C*np.exp(-RATE*a), COMPLEX_C*np.exp(-1j*K*b)


def project_wave(x, z):
    x, z = np.asarray(x), np.asarray(z)
    # Orthographic view of a cylinder along x. No moving camera.
    return np.stack((110+(x+3)/6*525 + 28*z.imag,
                     1290-86*z.real-32*z.imag), axis=-1)


def real_point(x, value):
    return np.array([110+(np.asarray(x)+3)/6*525,
                     960-np.asarray(value)/4.6*260]).T


def cross_section(s, origin, cs, complex_case=False):
    o = np.asarray(origin, dtype=float)
    gain = 82
    s.line([o+[-48, 0], o+[175, 0]], GRID, 2)
    if complex_case:
        s.line([o+[0, -108], o+[0, 108]], GRID, 2)
        for radius in (.6, .95):
            theta = np.linspace(0, 2*math.pi, 121)
            s.line(o+gain*radius*np.c_[np.cos(theta), -np.sin(theta)], GRID, 2)
        theta0, theta1 = np.angle(cs[0]), np.angle(cs[0])+.8
        theta = np.linspace(theta0, theta1, 30)
        s.line(o+27*np.c_[np.cos(theta), -np.sin(theta)], GOLD, 4)
    ends=[]
    for c, color in zip(cs, COLORS):
        end=o+gain*np.array([c.real,-c.imag])
        s.arrow(o,end,color,4,13)
        s.dot(end,6,color)
        ends.append(end)
    # An offset bracket shows the growing gap for the real pair.
    if not complex_case:
        start, end = ends
        s.line([start+[0,15],start+[0,25],end+[0,25],end+[0,15]], GOLD, 3)
    else:
        s.line(ends, GOLD, 2)


def render(t):
    s=Scene(0,TITLE,'',t,DURATION)
    s.d.rectangle((60,205,970,262),fill=BG)
    s.text(70,217,'SYMMETRY TO WAVES',27,GOLD,bold=True)
    s.d.rectangle((60,1692,975,1790),fill=BG)
    s.text(70,1717,'VARIATIONS ON SYMMETRY',25,MUTED)
    stage=next(text for start,text in reversed(STAGES) if t>=start)
    s.wrap(stage,70,430,880,size=32,leading=39)
    a,b=shifts(t)
    cr,cc=coefficients(t)

    s.text(80,555,'REAL EXPONENTIALS',29,MUTED,bold=True)
    s.math(r'f(x)=c_1e^{\lambda x},\qquad g(x)=c_2e^{\lambda x}',y=630,size=37)
    s.text(800,690,'At x = 0',27,MUTED,anchor='ma')
    x=np.linspace(-3,3,700)
    for level in (1,2,3,4):
        s.line([real_point(-3,level),real_point(3,level)],GRID,1)
    s.arrow(real_point(-3,0),real_point(3.15,0),MUTED,2,10)
    s.text(652,953,'x',27,MUTED)
    cut=real_point(0,0)[0]
    s.line([(cut,700),(cut,960)],GOLD,2)
    for c,color in zip(cr,COLORS):
        y=c.real*np.exp(RATE*x)
        s.line(real_point(x,y),color,5)
        s.dot(real_point(0,c.real),6,color)
    # A tracked feature slides left without changing height.
    for c,color in zip(REAL_C,COLORS):
        s.dot(real_point(2+a,c.real*np.exp(RATE*2)),7,color)
    cross_section(s,(755,825),cr)
    s.line([(cut+10,740),(680,740),(713,790)],GRID,2)
    s.math(r'c_1^*c_2=',x=355,y=1020,size=40,color=MUTED,maxwidth=200)
    s.text(470,1020,f'{(cr[0].conjugate()*cr[1]).real:.3f}',39,GOLD,anchor='lm')

    s.text(80,1100,'COMPLEX EXPONENTIALS',29,MUTED,bold=True)
    s.math(r'f(x)=c_1e^{ikx},\qquad g(x)=c_2e^{ikx}',y=1170,size=37)
    s.text(800,1200,'At x = 0',27,MUTED,anchor='ma')
    # A fixed cylindrical guide makes constant radii visible.
    for r in (.6,.95):
        for sign in (-1,1):
            s.line([(110,1290+sign*r*92),(635,1290+sign*r*92)],GRID,1)
    s.arrow((100,1290),(655,1290),MUTED,2,10)
    s.text(661,1296,'x',27,MUTED)
    th=np.linspace(0,2*math.pi,101)
    s.line(project_wave(np.zeros_like(th),.98*np.exp(1j*th)),GOLD,2)
    for c,color in zip(cc,COLORS):
        z=c*np.exp(1j*K*x)
        s.line(project_wave(x,z),color,5)
        s.dot(project_wave(0,c),6,color)
    for c,color in zip(COMPLEX_C,COLORS):
        s.dot(project_wave(2+b,c*np.exp(1j*K*2)),7,color)
    cross_section(s,(800,1320),cc,True)
    s.line([(400,1210),(690,1210),(730,1250)],GRID,2)
    product=cc[0].conjugate()*cc[1]
    s.math(r'c_1^*c_2=',x=310,y=1475,size=40,color=MUTED,maxwidth=200)
    s.text(420,1475,f'{product.real:.3f} + {product.imag:.3f}i',39,GREEN,anchor='lm')
    s.text(510,1535,'Inner product of the amplitudes',27,MUTED,anchor='ma')
    if t>=25:
        s.math(r'\langle Tf,Tg\rangle=\langle f,g\rangle',y=1605,size=42,color=GREEN)
    return s.im


def checks():
    times=np.linspace(0,DURATION,193)
    pairs=[coefficients(t) for t in times]
    real=np.array([p[0][0].conjugate()*p[0][1] for p in pairs])
    complex_products=np.array([p[1][0].conjugate()*p[1][1] for p in pairs])
    assert np.all(np.diff(real.real)>=-1e-12)
    assert np.max(abs(complex_products-COMPLEX_C[0].conjugate()*COMPLEX_C[1]))<1e-12
    assert all(np.allclose(abs(p[1]),abs(COMPLEX_C)) for p in pairs)
    x=np.linspace(-3,3,41)
    for t in times[::8]:
        a,b=shifts(t)
        r,c=coefficients(t)
        assert np.allclose(r[:,None]*np.exp(RATE*x), REAL_C[:,None]*np.exp(RATE*(x-a)))
        assert np.allclose(c[:,None]*np.exp(1j*K*x), COMPLEX_C[:,None]*np.exp(1j*K*(x-b)))
    return dict(samples=len(times),max_inner_product_error=float(max(abs(complex_products-complex_products[0]))),
                real_inner_product=[float(real[0].real),float(real[-1].real)])


def review():
    OUT.mkdir(parents=True,exist_ok=True)
    folder=OUT/'review'
    folder.mkdir(exist_ok=True)
    times=[0,3,6,9,12,16,20,25,30]
    sheet=Image.new('RGB',(810,1530),BG)
    draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        pic=render(t)
        pic.save(folder/f'{t:02d}.jpg',quality=94)
        px,py=(i%3)*270,(i//3)*510
        sheet.paste(pic.resize((270,480),Image.Resampling.LANCZOS),(px,py))
        draw.text((px+10,py+484),f'{t}s',font=font(18),fill=INK)
    sheet.save(folder/'contact-sheet.jpg',quality=94)
    render(22).save(OUT/'poster.jpg',quality=95)
    (OUT/'checks.json').write_text(json.dumps(checks(),indent=2),encoding='utf8')


def encode():
    path=OUT/'translation-unitarity.rendering.mp4'
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
             '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
             '-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-threads','3',str(path)]
    with subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
        try:
            for i in range(DURATION*FPS):
                proc.stdin.write(render(i/FPS).tobytes())
                if i%300==0:
                    print(f'{i}/{DURATION*FPS} frames',flush=True)
            proc.stdin.close()
            err=proc.stderr.read().decode()
            if proc.wait():
                raise RuntimeError(err)
        except BaseException:
            proc.kill()
            raise
    target=OUT/'translation-unitarity.mp4'
    path.replace(target)
    stream=imageio_ffmpeg.read_frames(str(target))
    metadata=next(stream)
    stream.close()
    assert metadata['size']==(W,H) and metadata['fps']==FPS
    assert abs(metadata['duration']-DURATION)<.1
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(target),
        '-vf',f'fps={12/DURATION},scale=270:480,tile=4x3','-frames:v','1','-q:v','2',
        str(OUT/'review/decoded.jpg')],check=True)
    result=dict(title=TITLE,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                media=metadata,math=checks())
    (OUT/'render-record.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--encode',action='store_true')
    args=parser.parse_args()
    review()
    if args.encode:
        encode()
