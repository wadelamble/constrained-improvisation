"""Translation as independent scaling in a two-exponential eigenbasis.

First compare translating one exponential with rescaling a fresh copy.
Then independently rescale e^(x/2) and e^(-x/2). Their pointwise sum is
computed at every frame and equals the rigidly translated initial sum.
"""
from symmetry_exponential_desktop_common import *

NAME = 'symmetry-translation-eigenfunctions'
DURATION = 34
SHIFT = 1.8
LAMBDA = 0.5
SCALE = 2
PLOT = (125, 300, 1475, 735)
XMIN, XMAX = -3.0, 4.0
MOMENTS = [0, 3, 6, 9, 13, 17, 21, 26, 32.5]
REVIEW = ROOT / '.tools' / (NAME + '-review')


def tint(color, alpha):
    c = tuple(int(color[i:i+2],16) for i in (1,3,5))
    b = tuple(int(BG[i:i+2],16) for i in (1,3,5))
    return tuple(round(y + alpha*(x-y)) for x,y in zip(c,b))


class SmoothCanvas(Canvas):
    def __init__(self):
        self.im = Image.new('RGB', (W*SCALE, H*SCALE), BG)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []

    def text(self, x, y, value, size=26, color=INK, bold=False, anchor='la', alpha=1):
        f = font(round(size*SCALE),bold)
        box = self.d.textbbox((x*SCALE,y*SCALE),value,font=f,anchor=anchor)
        self.track(tuple(v/SCALE for v in box),value)
        self.d.text((x*SCALE,y*SCALE),value,font=f,fill=tint(color,alpha),anchor=anchor)

    def math(self,x,y,tex,size=35,color=INK,center=False,label=False,alpha=1):
        pic=equation(tex,size*SCALE,color).copy()
        if alpha < 1:
            pic.putalpha(pic.getchannel('A').point(lambda a: round(a*alpha)))
        px=round(x*SCALE-pic.width/2) if center else round(x*SCALE)
        py=round(y*SCALE-pic.height/2)
        self.track((px/SCALE,py/SCALE,(px+pic.width)/SCALE,(py+pic.height)/SCALE),tex)
        if label:
            self.d.rectangle((px-6*SCALE,py-4*SCALE,px+pic.width+6*SCALE,py+pic.height+4*SCALE),fill=BG)
        self.im.paste(pic,(px,py),pic)

    def line(self,points,color=GRID,width=2,alpha=1):
        self.d.line([tuple(np.asarray(p)*SCALE) for p in points],fill=tint(color,alpha),
                    width=max(1,round(width*SCALE)),joint='curve')

    def arrow(self,a,b,color=INK,width=3,head=12,alpha=1):
        a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
        delta=b-a
        length=np.linalg.norm(delta)
        if length < 1:
            return
        unit=delta/length
        normal=np.array([-unit[1],unit[0]])
        head=min(head,.4*length)
        self.line([a,b],color,width,alpha)
        vertices=[b,b-head*unit+.4*head*normal,b-head*unit-.4*head*normal]
        self.d.polygon([tuple(v*SCALE) for v in vertices],fill=tint(color,alpha))

    def dot(self,p,r=5,color=INK,alpha=1):
        x,y=np.asarray(p)*SCALE
        r*=SCALE
        self.d.ellipse((x-r,y-r,x+r,y+r),fill=tint(color,alpha))

    def finish(self):
        for i,(a,aname) in enumerate(self.boxes):
            for b,bname in self.boxes[i+1:]:
                dx=min(a[2],b[2])-max(a[0],b[0])
                dy=min(a[3],b[3])-max(a[1],b[1])
                assert dx <= 0 or dy <= 0, ('text collision',aname,bname)
        return self.im.resize((W,H),Image.Resampling.LANCZOS)


def point(x,y,ymax):
    x,y=np.broadcast_arrays(np.asarray(x),np.asarray(y))
    l,t,r,b=PLOT
    return np.stack((l+(x-XMIN)/(XMAX-XMIN)*(r-l),b-y/ymax*(b-t)),axis=-1)


def axes(s,ymax):
    for y in range(2,round(ymax)+1,2):
        s.line(point([XMIN,XMAX],[y,y],ymax),FAINT,1)
        s.text(PLOT[0]-20,point(XMIN,y,ymax)[1],str(y),20,MUTED,anchor='rm')
    s.arrow(point(XMIN,0,ymax),point(XMAX+.12,0,ymax),MUTED,2,10)
    s.math(PLOT[2]+34,PLOT[3]+1,'x',25,MUTED)
    for x in (-3,-2,-1,0,1,2,3,4):
        p=point(x,0,ymax)
        s.line([p,p+[0,6]],MUTED,1.5)
        s.text(*(p+[0,15]),str(x),20,MUTED,anchor='ma')


def header(s,subtitle,a):
    s.text(52,36,'Translation rescales exponential components',38,INK,True)
    s.text(52,102,subtitle,27,MUTED)
    s.text(1548,107,f'a = {a:.2f}',26,INK,anchor='ra')


def single_motion(t):
    return SHIFT*progress(t,1.2,4.3),progress(t,5.2,8.2)


def single_scene(t):
    a,scaled=single_motion(t)
    factor=math.exp(-LAMBDA*a)
    s=SmoothCanvas()
    if t < 5.2:
        subtitle='One exponential: slide a copy to the right'
    elif t < 8.2:
        subtitle='Rescale a fresh copy to reach the same curve'
    else:
        subtitle='Translation and rescaling give the same result'
    header(s,subtitle,a)
    s.math(430,205,r'f_1(x)=e^{x/2}',38,BLUE,center=True)
    s.math(1190,205,r'T_a f_1=e^{-a/2}f_1',38,GREEN,center=True)
    axes(s,8)
    x=np.linspace(XMIN,XMAX,1100)
    f1=np.exp(x/2)
    s.line(point(x,f1,8),BLUE,5)
    if t >= 1.2:
        s.line(point(x,np.exp((x-a)/2),8),GREEN,5)
        for anchor in (-1.4,.4,1.9):
            val=math.exp(anchor/2)
            start,end=point(anchor,val,8),point(anchor+a,val,8)
            s.arrow(start,end,GREEN,2,10)
            s.dot(end,5,GREEN)
    if t >= 5.2:
        working_scale=1+(factor-1)*scaled
        s.line(point(x,working_scale*f1,8),INK,2.5)
        for anchor in (-.8,1.2,3.1):
            val=math.exp(anchor/2)
            s.arrow(point(anchor,val,8),point(anchor,working_scale*val,8),INK,2,10)
    s.line([(235,826),(280,826)],BLUE,4)
    s.text(292,826,'Original',23,BLUE,anchor='lm')
    s.line([(650,826),(695,826)],GREEN,4)
    s.text(707,826,'Translated copy',23,GREEN,anchor='lm')
    if t >= 5.2:
        s.line([(1170,826),(1215,826)],INK,2.5)
        s.text(1227,826,'Rescaled copy',23,INK,anchor='lm')
    return s.finish()


def pair_motion(t):
    return SHIFT*progress(t,20,29)


def components(x,a):
    x=np.asarray(x)
    return math.exp(-a/2)*np.exp(x/2), math.exp(a/2)*np.exp(-x/2)


def pair_scene(t):
    a=pair_motion(t)
    c1,c2=math.exp(-a/2),math.exp(a/2)
    s=SmoothCanvas()
    if t < 20:
        subtitle='Two exponential components and their sum'
    elif t < 29:
        subtitle='Rescale each component; their sum translates'
    else:
        subtitle='Different scale factors. The same translated shape.'
    header(s,subtitle,a)
    axes(s,12)
    second_alpha=progress(t,12,13.5)
    sum_alpha=progress(t,14,15.5)
    s.math(420,189,r'c_1 e^{x/2}',36,BLUE,center=True)
    s.math(1140,189,r'c_2 e^{-x/2}',36,GOLD,center=True,alpha=second_alpha)
    s.math(315,250,r'c_1=e^{-a/2}',28,BLUE)
    s.text(540,250,f'= {c1:.3f}',29,BLUE,anchor='lm')
    s.math(1035,250,r'c_2=e^{a/2}',28,GOLD,alpha=second_alpha)
    s.text(1260,250,f'= {c2:.3f}',29,GOLD,anchor='lm',alpha=second_alpha)
    x=np.linspace(XMIN,XMAX,1300)
    rising,falling=components(x,a)
    if t >= 20:
        reference=np.exp(x/2)+np.exp(-x/2)
        s.line(point(x,reference,12),GRID,3)
    s.line(point(x,rising,12),BLUE,4.5)
    s.line(point(x,falling,12),GOLD,4.5,second_alpha)
    # The sum is computed pointwise, never morphed or scaled as a whole.
    if sum_alpha > 0:
        s.line(point(x,rising+falling,12),INK,5.5,sum_alpha)
        # Three addition witnesses briefly stack component heights.
        stack_alpha=progress(t,14,15)*(1-progress(t,18,19.5))
        if stack_alpha > 0:
            for x0 in (-1.2,.6,2.3):
                v1,v2=components(x0,a)
                p0,p1,p2=point(x0,0,12),point(x0,v1,12),point(x0,v1+v2,12)
                s.line([p0,p1],BLUE,6,stack_alpha)
                s.line([p1,p2],GOLD,6,stack_alpha)
                s.dot(p1,5,BLUE,stack_alpha)
                s.dot(p2,5,INK,stack_alpha)
        s.dot(point(a,2,12),6,INK,sum_alpha)
    if a > .01:
        initial=point(0,2,12)
        moving=point(a,2,12)
        s.dot(initial,4,MUTED)
        s.arrow(initial,moving,MUTED,2,11)
        s.math((initial[0]+moving[0])/2,initial[1]-29,'a',25,MUTED,label=True)
    if t < 20:
        s.math(800,829,r'f(x)=e^{x/2}+e^{-x/2}',36,INK,center=True,alpha=sum_alpha)
    else:
        s.math(800,829,r'(T_a f)(x)=c_1 e^{x/2}+c_2 e^{-x/2}=f(x-a)',34,INK,center=True)
    return s.finish()


def render(t):
    if t < 10.7:
        return single_scene(t)
    if t < 11.3:
        return Image.blend(single_scene(10.7),pair_scene(11.3),progress(t,10.7,11.3))
    return pair_scene(t)


def validate():
    x=np.linspace(XMIN,XMAX,1001)
    factor_error=translation_error=shape_error=minimum_error=0.0
    for a in np.linspace(0,SHIFT,181):
        c1,c2=math.exp(-a/2),math.exp(a/2)
        v1,v2=components(x,a)
        actual=np.exp((x-a)/2)+np.exp(-(x-a)/2)
        factor_error=max(factor_error,abs(c1*c2-1))
        translation_error=max(translation_error,float(np.max(abs(v1+v2-actual))))
        r1,r2=components(x+a,a)
        original=np.exp(x/2)+np.exp(-x/2)
        shape_error=max(shape_error,float(np.max(abs(r1+r2-original))))
        m1,m2=components(a,a)
        minimum_error=max(minimum_error,abs(float(m1+m2)-2))
        assert float(np.max(v1+v2)) < 12
    assert max(factor_error,translation_error,shape_error,minimum_error) < 1e-12
    for t in (0,3,6,9,11,12,13.5,14,15.5,17,19,20.01,22,26,29,33.95):
        render(t)
    return dict(translation_samples=181,component_factor_product_error=factor_error,
                translation_identity_max_error=translation_error,shape_preservation_max_error=shape_error,
                minimum_height_error=minimum_error,minimum_motion='x=a, f=2',
                text_bounds_and_text_collisions='checked on every rendered frame')


def contact_sheet(directory):
    sheet=Image.new('RGB',(1440,3*298),BG)
    draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(MOMENTS):
        im=render(t)
        x,y=(i%3)*480,(i//3)*298
        sheet.paste(im.resize((480,270),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+274),f'{t:g} s',font=font(17),fill=MUTED)
    path=directory/'contact.png'
    sheet.save(path)
    return path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    REVIEW.mkdir(parents=True,exist_ok=True)
    report=validate()
    print(contact_sheet(REVIEW),flush=True)
    for t in (6,17,25,32):
        render(t).save(REVIEW/f'{t:02d}.png')
    if args.render:
        destination=OUT/f'{NAME}.mp4'
        temporary=REVIEW/f'{NAME}.rendering.mp4'
        writer=imageio_ffmpeg.write_frames(str(temporary),(W,H),fps=FPS,codec='libx264',
                    pix_fmt_in='rgb24',pix_fmt_out='yuv420p',quality=None,macro_block_size=1,
                    output_params=['-crf','18','-preset','fast','-movflags','+faststart','-threads','2'])
        writer.send(None)
        try:
            for i in range(DURATION*FPS):
                writer.send(render(i/FPS).tobytes())
                if i%(FPS*6)==0:
                    print(f'Rendered {i/FPS:.0f}/{DURATION} seconds',flush=True)
        finally:
            writer.close()
        temporary.replace(destination)
        render(31).save(OUT/f'{NAME}-poster.png')
        source=Path(__file__)
        helper=ROOT/'scripts/symmetry_exponential_desktop_common.py'
        report.update(size=[W,H],fps=FPS,duration_seconds=DURATION,
                      source_sha256=hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                      helper_sha256=hashlib.sha256(helper.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                      source_hash_normalization='UTF-8 source and helper with LF line endings')
        (OUT/f'{NAME}-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    if args.check:
        destination=OUT/f'{NAME}.mp4'
        ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
        reader=imageio_ffmpeg.read_frames(str(destination))
        meta=next(reader)
        reader.close()
        assert meta['size']==(W,H) and meta['fps']==FPS, meta
        count,seconds=imageio_ffmpeg.count_frames_and_secs(str(destination))
        assert count==DURATION*FPS and abs(seconds-DURATION)<.05
        subprocess.run([ffmpeg,'-v','error','-i',str(destination),'-f','null','-'],check=True)
        indices=[min(round(t*FPS),count-1) for t in MOMENTS]
        selection='+'.join(f'eq(n\\,{i})' for i in indices)
        subprocess.run([ffmpeg,'-y','-v','error','-i',str(destination),'-vf',
                        f'select={selection},scale=480:270,tile=3x3','-frames:v','1',
                        str(OUT/f'{NAME}-contact-sheet.png')],check=True)
        encoded=dict(video_sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),
                     frame_count=count,duration_seconds=seconds,size=[W,H],fps=FPS,
                     decode='passed',contact_sheet_frame_indices=indices)
        (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(encoded,indent=2)+'\n',encoding='utf8')
        print(json.dumps(encoded),flush=True)


if __name__=='__main__':
    main()
