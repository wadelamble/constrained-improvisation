"""Map six complex wave packets to their means and transport a fine patch.

The left-hand curves are actual complex states under one common unitary,
not sketches inferred from the right-hand points. The right-hand grid moves
by the same exact affine symplectic mean map. Cells follow subsets of a
displaced-packet family; they are neither single states nor uncertainty cells.

Run --preview for source frames, --render for the MP4, --check for decoded QA.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess

import generate_symmetry_packet_phase_modes as art
import symmetry_mean_patch as model

np, Image, ImageDraw = art.np, art.Image, art.ImageDraw
ROOT, OUT = art.ROOT, art.OUT
NAME = 'symmetry-mean-patch'
REVIEW = ROOT / '.tools' / (NAME + '-review')
W, H, SS, FPS, DURATION = 1600, 900, 2, 24, 42
BG, PANEL, INK, MUTED, BORDER = art.BG, art.PANEL, art.INK, art.MUTED, art.BORDER
COLORS = ((43, 93, 145), (180, 108, 29), (41, 124, 111),
          (125, 85, 146), (176, 73, 61), (109, 119, 48))
GRID_COLOR, OUTLINE = (165, 154, 134), (114, 101, 81)
X = np.linspace(-7.5, 7.5, 1501)
XLEFT, XRIGHT = 105., 717.
BASELINES = np.arange(6) * 88. + 278.
WAVE_GAIN, WAVE_DEPTH = 34., .48
CAMERA = np.exp(-1j * math.radians(22))
PLANE_CENTER = np.array([1186., 487.])
PLANE_SCALE = np.array([58., -58.])
TAU_MAX, R_MAX = .42, math.log(1.32)
GRID = model.initial_grid(18, 18)
GRID_LINES = [GRID[j] for j in range(19)] + [GRID[:, j] for j in range(19)]
HIGHLIGHT_CELL = (11, 13)
POSTER_TIME = 30.
MOMENTS = (0., 3., 8., 11., 14., 18., 23., 27., 32., 35., 38., 41.9)


def ease(u):
    u = float(np.clip(u, 0., 1.))
    return u*u*(3.-2.*u)


def parameters(seconds):
    """The pauses and reversals are smooth reparameterizations of exact U."""
    if seconds < 15.: return 0., 0.
    if seconds < 22.: return TAU_MAX*ease((seconds-15.)/7.), 0.
    if seconds < 24.: return TAU_MAX, 0.
    if seconds < 31.: return TAU_MAX, R_MAX*ease((seconds-24.)/7.)
    if seconds < 33.: return TAU_MAX, R_MAX
    if seconds < 36.5: return TAU_MAX, R_MAX*(1.-ease((seconds-33.)/3.5))
    if seconds < 40.: return TAU_MAX*(1.-ease((seconds-36.5)/3.5)), 0.
    return 0., 0.


def scene(seconds):
    if seconds < 9.: return 0, 'Map each wave to its average position and wave number'
    if seconds < 15.: return 1, 'Each moving cell follows a group of states'
    if seconds < 24.: return 2, 'Shear the patch; evolve every wave by the same transformation'
    if seconds < 33.: return 3, 'Stretch in one direction, compress in the other'
    return 4, 'Reverse the evolution; recover the waves and their mapped patch'


def plane(points):
    return PLANE_CENTER + np.asarray(points)*PLANE_SCALE


def wave_x(x):
    return XLEFT+(np.asarray(x)+7.5)/15.*(XRIGHT-XLEFT)


def fade(color, amount=1., background=PANEL):
    return tuple(round(amount*c+(1.-amount)*b) for c,b in zip(color,background))


def line(d, points, color, width=1.):
    art.curve(d, np.asarray(points), color, width)


def dashed(d, a, b, color, width=1., dash=5., gap=5.):
    a, b = np.asarray(a), np.asarray(b)
    length = float(np.linalg.norm(b-a))
    if length < 1e-9: return
    unit = (b-a)/length
    for start in np.arange(0., length, dash+gap):
        line(d, [a+start*unit, a+min(start+dash,length)*unit], color, width)


def number(d, xy, value, color, radius=12., alpha=1.):
    color=fade(color,alpha)
    art.dot(d,xy,color,radius)
    art.text(d,xy,str(value),15,PANEL,True,anchor='mm')


@lru_cache(None)
def background():
    im=Image.new('RGB',(W*SS,H*SS),BG)
    d=ImageDraw.Draw(im,'RGBA')
    art.text(d,(39,25),'States, averages, and a moving patch',36,INK,True)
    for box in ((28,139,759,810),(786,139,1572,810)):
        d.rounded_rectangle(art.px(box),radius=12*SS,fill=PANEL,outline=BORDER,width=SS)
    art.text(d,(49,156),'Wave functions',26,INK,True)
    art.text(d,(49,197),'Six samples from the same family',18,MUTED)
    art.text(d,(810,156),'Average position and wave number',26,INK,True)
    art.paste_formula(im,(1180,193),r'$\psi\;\longmapsto\;(\langle\hat X\rangle_\psi,\,\langle\hat K\rangle_\psi)$',23,INK,centered=True)
    # Fixed axes. Equal x/k screen scales make the shearing geometry legible.
    for v in range(-5,6):
        px=float(plane([v,0])[0])
        py=float(plane([0,v])[1])
        if v:
            line(d,[(px,PLANE_CENTER[1]-3),(px,PLANE_CENTER[1]+3)],(*BORDER,190),.85)
            line(d,[(PLANE_CENTER[0]-3,py),(PLANE_CENTER[0]+3,py)],(*BORDER,190),.85)
            if v%2==0:
                art.text(d,(px,PLANE_CENTER[1]+9),str(v).replace('-','−'),14,fade(MUTED,.68),anchor='ma')
                art.text(d,(PLANE_CENTER[0]-11,py),str(v).replace('-','−'),14,fade(MUTED,.68),anchor='rm')
    art.arrow(d,plane([-5.75,0]),plane([5.9,0]),BORDER,1.3,7.)
    art.arrow(d,plane([0,-4.2]),plane([0,4.2]),BORDER,1.3,7.)
    art.paste_formula(im,(1523,499),r'$\langle\hat X\rangle$',21,MUTED,centered=True)
    art.paste_formula(im,(1231,234),r'$\langle\hat K\rangle$',21,MUTED,centered=True)
    for base in BASELINES:
        line(d,[(XLEFT,base),(XRIGHT,base)],(*BORDER,100),.7)
        for x in (-6,-3,0,3,6):
            sx=wave_x(x)
            line(d,[(sx,base-2),(sx,base+2)],(*BORDER,150),.7)
    for x in (-6,-3,0,3,6):
        art.text(d,(float(wave_x(x)),772),str(x).replace('-','−'),14,MUTED,anchor='ma')
    art.text(d,(XRIGHT+12,777),'x',18,MUTED,anchor='lm')
    # A small fixed projection key explains how a complex curve is seen.
    art.text(d,(50,837),'Complex waves',17,MUTED)
    o=np.array([228.,853.])
    for label,vec in (('x',(30.,0.)),('Re',(0.,-25.)),('Im',(18.,-11.))):
        art.arrow(d,o,o+vec,MUTED,1.,4.)
        art.text(d,o+vec+np.array([5.,-3.]),label,13,MUTED,anchor='lm')
    art.text(d,(1561,844),'An area-preserving example',17,MUTED,anchor='ra')
    return im


def draw_wave(d, values, row, color, emphasis):
    baseline=BASELINES[row]
    z=values*CAMERA
    coords=np.column_stack((wave_x(X)+WAVE_GAIN*WAVE_DEPTH*z.imag,baseline-WAVE_GAIN*z.real))
    # A faint envelope gives the widening and squeezing a visible reference.
    amp=np.abs(values)
    for side in (-1,1):
        line(d,np.column_stack((wave_x(X),baseline+side*WAVE_GAIN*amp)),fade(color,.24*emphasis),.9)
    front=z.imag[:-1]+z.imag[1:]>=0
    cuts=np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
    for side,weight in ((False,.43),(True,1.)):
        for a,b in zip(cuts[:-1],cuts[1:]):
            if bool(front[a])==side:
                line(d,coords[a:b+1],fade(color,weight*emphasis),2.)


def grid_outline(grid):
    return np.vstack((grid[0,0],grid[0,-1],grid[-1,-1],grid[-1,0],grid[0,0]))


def frame(seconds):
    tau,r=parameters(seconds)
    scene_id,subtitle=scene(seconds)
    values=model.waves(X,tau,r)
    means=model.means(tau,r)
    im=background().copy()
    d=ImageDraw.Draw(im,'RGBA')
    art.text(d,(41,83),subtitle,22,MUTED)

    # Map one sample at a time, then retain all six samples throughout.
    map_progress=(seconds-1.)/1.05
    active=int(map_progress) if 0.<=map_progress<6. else -1
    points_visible=0 if seconds<1. else (6 if seconds>=7.3 else max(0,min(6,int(map_progress)+1)))
    for j,(color,base,mean) in enumerate(zip(COLORS,BASELINES,means)):
        emphasis=1. if active<0 or j==active else .36
        draw_wave(d,values[j],j,color,emphasis)
        number(d,(67.,base-42.),j+1,color,11.,emphasis)
        art.paste_formula(im,(90,base-52),r'$\psi_{'+str(j+1)+r'}(x)$',19,fade(color,emphasis))
        art.paste_formula(im,(345,base-52),r'$\langle\hat X\rangle=$',17,fade(MUTED,emphasis))
        art.text(d,(413,base-51),f'{mean[0]:+.2f}'.replace('-','−'),17,fade(color,emphasis))
        art.paste_formula(im,(516,base-52),r'$\langle\hat K\rangle=$',17,fade(MUTED,emphasis))
        art.text(d,(585,base-51),f'{mean[1]:+.2f}'.replace('-','−'),17,fade(color,emphasis))
        mx=float(wave_x(mean[0]))
        dashed(d,(mx,base-29),(mx,base+29),fade(color,.42*emphasis),.9,3,4)
        art.dot(d,(mx,base+31),fade(color,emphasis),2.7)

    outline_alpha=ease((seconds-9.)/1.)
    grid_alpha=ease((seconds-10.)/1.8)
    current_grid=model.evolve_points(GRID,tau,r)
    if outline_alpha:
        outline=plane(grid_outline(current_grid))
        d.polygon([art.px(p) for p in outline[:-1]],fill=(*GRID_COLOR,round(12*outline_alpha)))
        if grid_alpha:
            # Track one complete material cell, without asserting that it is
            # a minimal quantum cell or a fixed number of physical states.
            i,j=HIGHLIGHT_CELL
            cell=current_grid[[i,i,i+1,i+1],[j,j+1,j+1,j]]
            d.polygon([art.px(p) for p in plane(cell)],fill=(*COLORS[3],round(65*grid_alpha)))
            for points in GRID_LINES:
                line(d,plane(model.evolve_points(points,tau,r)),(*GRID_COLOR,round(155*grid_alpha)),.85)
            line(d,plane(np.vstack((cell,cell[:1]))),(*COLORS[3],round(210*grid_alpha)),1.3)
        line(d,outline,(*OUTLINE,round(255*outline_alpha)),2.)

    # The mapping connector is a guide, not a trajectory through state space.
    if active>=0:
        frac=map_progress-active
        start=np.array([727.,BASELINES[active]-42.])
        end=plane(means[active])
        elbow=np.array([775.,BASELINES[active]-42.])
        line(d,[start,elbow,end],(*COLORS[active],85),1.)
        t=ease(frac/.7)
        # Pulse the destination after the guide arrives, not the wave itself.
        if t>.95:
            radius=12.+5.*(1.-ease((frac-.65)/.35))
            d.ellipse(art.px((* (end-radius),* (end+radius))),outline=(*COLORS[active],130),width=SS)
        dashed(d,end,[end[0],PLANE_CENTER[1]],(*COLORS[active],110),.8)
        dashed(d,end,[PLANE_CENTER[0],end[1]],(*COLORS[active],110),.8)

    for j in range(points_visible):
        pos=plane(means[j])
        number(d,pos,j+1,COLORS[j],10.5)

    if grid_alpha>0:
        # These readouts come from the current transported coordinates.
        corners=grid_outline(current_grid)[:-1]
        area=.5*abs(np.dot(corners[:,0],np.roll(corners[:,1],-1))-np.dot(corners[:,1],np.roll(corners[:,0],-1)))
        a=current_grid[0,1]-current_grid[0,0]
        b=current_grid[1,0]-current_grid[0,0]
        cell_area=abs(a[0]*b[1]-a[1]*b[0])
        art.text(d,(829,748),f'Patch area  {area:.2f}',20,INK,True)
        art.text(d,(1237,748),f'Cell area  {cell_area:.2f}',20,INK,True)
        if seconds<15:
            note='Each cell follows a group of states'
        elif seconds<24:
            note='The cells shear together; their areas stay fixed'
        elif seconds<33:
            note='Wider in x, narrower in k; the area stays fixed'
        elif seconds<40:
            note='The same cells return with the same states'
        else:
            note='The original waves and patch are recovered'
        art.text(d,(1182,782),note,17,MUTED,anchor='mm')
    else:
        art.text(d,(1182,767),'Each colored point is one wave\u2019s pair of averages',18,MUTED,anchor='mm')

    # A small scene strip orients a long animation without covering the plots.
    labels=('Map','Patch','Shear','Stretch','Return')
    for j,label in enumerate(labels):
        xpos=543+j*111
        if scene_id==j:
            d.rounded_rectangle(art.px((xpos-10,833,xpos+87,866)),radius=6*SS,fill=(*OUTLINE,18))
        art.text(d,(xpos+38,848),label,17,INK if j==scene_id else MUTED,bold=j==scene_id,anchor='mm')
    return im.resize((W,H),Image.Resampling.LANCZOS)


def preview():
    REVIEW.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1600,675),BG)
    for i,t in enumerate(MOMENTS):
        im=frame(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        thumb=im.resize((400,225),Image.Resampling.LANCZOS)
        sheet.paste(thumb,((i%4)*400,(i//4)*225))
    sheet.save(REVIEW/'contact.png')
    frame(POSTER_TIME).save(OUT/f'{NAME}-poster.png')


def encode():
    REVIEW.mkdir(parents=True,exist_ok=True)
    temp=REVIEW/f'{NAME}.rendering.mp4'
    cmd=[art.imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
         '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(temp)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        try:
            for n in range(FPS*DURATION):
                process.stdin.write(frame(n/FPS).tobytes())
                if n%(FPS*2)==0: print(f'{n/FPS:.0f}/{DURATION}s rendered',flush=True)
            process.stdin.close()
            if process.wait(): raise RuntimeError('Video encoding failed')
        except BaseException:
            process.kill()
            raise
    temp.replace(OUT/f'{NAME}.mp4')


def check():
    path=OUT/f'{NAME}.mp4'
    ffmpeg=art.imageio_ffmpeg.get_ffmpeg_exe()
    frames,seconds=art.imageio_ffmpeg.count_frames_and_secs(str(path))
    reader=art.imageio_ffmpeg.read_frames(str(path))
    try: meta=next(reader)
    finally: reader.close()
    assert frames==FPS*DURATION and abs(seconds-DURATION)<.001
    assert meta['size']==(W,H) and meta['fps']==FPS
    subprocess.run([ffmpeg,'-v','error','-i',str(path),'-f','null','-'],check=True)
    indices=[round(t*FPS) for t in MOMENTS]
    selection='+'.join(f'eq(n\\,{i})' for i in indices)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(path),'-vf',
                    f'select={selection},scale=400:225,tile=4x3','-frames:v','1',
                    str(OUT/f'{NAME}-contact-sheet.png')],check=True)
    for t in (3.,11.,23.,30.,41.9):
        subprocess.run([ffmpeg,'-y','-v','error','-i',str(path),'-vf',
                        f'select=eq(n\\,{round(t*FPS)})','-frames:v','1',
                        str(REVIEW/f'decoded-{t:05.1f}.png')],check=True)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(path),'-vf',
                    f'select=eq(n\\,{round(POSTER_TIME*FPS)})','-frames:v','1',
                    str(OUT/f'{NAME}-poster.png')],check=True)
    report=dict(video_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                duration_seconds=seconds,frame_count=frames,size=meta['size'],fps=meta['fps'],
                decoded='passed',contact_sheet_frame_indices=indices,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                model_sha256=hashlib.sha256((ROOT/'scripts/symmetry_mean_patch.py').read_bytes()).hexdigest(),
                mean_map='Squeeze(r) @ Shear(tau), shared by every wave and grid point',
                cells='Moving subsets of the displaced-packet family, not single states or uncertainty cells',
                amplitude_scale='fixed; no frame-by-frame normalization',
                scenes=[0,9,15,24,33],restricted_evolution=True)
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.preview or not(args.render or args.check): preview()
    if args.render: encode()
    if args.check: check()
