"""Two wave states follow the same unitary evolution, then share one view.

Surface height depicts Re(psi), not a material displacement. A fixed vertical
scale is used throughout. The overlap readout is calculated from the complete
complex states. The final overlay compares alternatives; it does not add them.

Run with --render --check; without flags, render representative source frames.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
from generate_symmetry_reversible_histories import (
    BG, INK, MUTED, BORDER, COLORS, SS, W, H, FPS, DURATION,
    PLAYBACK_SPEED, MOMENTS, POSTER_TIME, ease, rgb, xy, text, timeline,
)
from symmetry_unitary_waves import build_histories

NAME = 'symmetry-unitary-histories'
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools' / f'{NAME}-review'
WAVES = None
GRID = np.linspace(0., 1., 97)
GX, GY = np.meshgrid(GRID, GRID)
VERTICAL_SCALE = 0.040


def geometry(story_time, which):
    m = ease((story_time - 24.) / 2.)
    cx = (420., 1180.)[which] + (800. - (420., 1180.)[which]) * m
    return cx, 491. - 18.*m, 680. + 210.*m, m


def project(x, y, z, cx, cy, width):
    x, y = np.asarray(x) - .5, np.asarray(y) - .5
    return np.stack((cx + width * (.68*x - .28*y),
                     cy + width * (.18*x + .28*y - VERTICAL_SCALE*np.asarray(z))), axis=-1)


def line(draw, points, fill, width):
    draw.line([xy(p) for p in points], fill=fill, width=max(1, round(width*SS)), joint='curve')


def draw_floor(image, cx, cy, width, alpha=255):
    layer = Image.new('RGBA', image.size)
    d = ImageDraw.Draw(layer)
    corners = project(np.array([0., 1., 1., 0.]), np.array([0., 0., 1., 1.]), 0., cx, cy, width)
    d.polygon([xy(p) for p in corners], fill=rgb('#f6f1e8')+(round(alpha*.72),))
    # Sparse neutral grid anchors the changing surface in its common domain.
    for f in np.linspace(0., 1., 5):
        for x,y in ((np.array([0.,1.]),np.array([f,f])),
                    (np.array([f,f]),np.array([0.,1.]))):
            line(d, project(x,y,0.,cx,cy,width), rgb('#d8d0c3')+(round(alpha*.48),), .8)
    line(d, np.vstack((corners,corners[:1])), rgb(BORDER)+(round(alpha*.75),), 1.1)
    image.alpha_composite(layer)


def draw_surface_fill(image, height, cx, cy, width, merged, color):
    # Each surface becomes nearly transparent in the comparison. The opaque
    # colored mesh, drawn separately after both fills, keeps identities legible.
    alpha = round(34*(1.-merged) + 5*merged)
    layer = Image.new('RGBA', image.size)
    d = ImageDraw.Draw(layer)
    points = project(GX, GY, height, cx, cy, width)[::3,::3]
    z = height[::3,::3]
    count = len(points)-1
    for row,col in sorted(((r,c) for r in range(count) for c in range(count)), key=lambda q: sum(q)):
        polygon = points[[row,row,row+1,row+1],[col,col+1,col+1,col]]
        strength = min(1., abs(float(np.mean(z[row:row+2,col:col+2])))/3.)
        d.polygon([xy(p) for p in polygon], fill=rgb(color)+(round(alpha*(.3+.7*strength)),))
    image.alpha_composite(layer)


def draw_surface_mesh(image, height, cx, cy, width, merged, color):
    layer = Image.new('RGBA',image.size)
    d = ImageDraw.Draw(layer)
    points = project(GX,GY,height,cx,cy,width)
    # A finer cross direction lets the waves read as surfaces, not graphs.
    # No white backing: both meshes remain visible through the comparison.
    for row in range(0,len(GRID),6):
        line(d, points[row], rgb(color)+(232,), 1.6 + .15*merged)
    for col in range(0,len(GRID),8):
        line(d, points[:,col], rgb(color)+(112,), .85)
    image.alpha_composite(layer)


def render(screen_time):
    global WAVES
    if WAVES is None:
        WAVES = build_histories()
    story_time = screen_time*PLAYBACK_SPEED
    t,direction,_ = timeline(story_time)
    states = WAVES.evaluate(t,GRID,GRID)
    geometries = [geometry(story_time,i) for i in range(2)]
    merged = geometries[0][3]
    im = Image.new('RGBA',(W*SS,H*SS),BG)
    d = ImageDraw.Draw(im)
    text(d,800,67,'Unitary and distinguishable histories',43,INK,True)
    text(d,800,120,'Different initial states, the same evolution',25,MUTED)
    for i,(cx,cy,width,m) in enumerate(geometries):
        if i==1 and m==1.: continue
        draw_floor(im,cx,cy,width)
    for i,(cx,cy,width,m) in enumerate(geometries):
        draw_surface_fill(im,states[i].real,cx,cy,width,m,COLORS[i])
    for i,(cx,cy,width,m) in enumerate(geometries):
        draw_surface_mesh(im,states[i].real,cx,cy,width,m,COLORS[i])
    d = ImageDraw.Draw(im)
    for i in range(2):
        lx=(420.,1180.)[i]+((688.,912.)[i]-(420.,1180.)[i])*merged
        text(d,lx,204.-20.*merged,f'State {i+1}',33,COLORS[i],True)
    if merged>.75:
        text(d,800,184,'≠',42,INK,alpha=round(255*ease((merged-.75)/.25)))
    overlap = WAVES.overlap(t)
    assert abs(overlap.imag)<1e-10
    text(d,800,730,f'Inner product = {overlap.real:.2f}',29,INK,True)
    text(d,800,768,'Surface height shows the real part of each wave amplitude',20,MUTED)
    text(d,800,813,f't = {t:.1f}',29,INK)
    if direction:
        text(d,1100,813,'Time runs forward' if direction>0 else 'Time runs backward',22,MUTED)
        ax=505
        d.line([xy((ax-25*direction,813)),xy((ax+25*direction,813))],fill=rgb(MUTED),width=2*SS)
        d.polygon([xy((ax+25*direction,813)),xy((ax+13*direction,806)),xy((ax+13*direction,820))],fill=rgb(MUTED))
    a,b,y=565.,1035.,855.
    line(d,[(a,y),(b,y)],rgb('#d8d1c6'),2)
    for value in range(9):
        px=a+(b-a)*value/8
        line(d,[(px,y-4),(px,y+4)],rgb(BORDER),1)
    marker=a+(b-a)*t/8
    d.ellipse(xy((marker-5,y-5,marker+5,y+5)),fill=rgb(INK))
    text(d,a-24,y,'0',17,MUTED)
    text(d,b+24,y,'8',17,MUTED)
    return im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)


def preview():
    REVIEW.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(1200,675),BG)
    for i,t in enumerate(MOMENTS):
        im=render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),((i%3)*400,(i//3)*225))
    sheet.save(REVIEW/'contact.png')
    render(POSTER_TIME).save(OUT/f'{NAME}-poster.png')


def encode():
    path=REVIEW/f'{NAME}.rendering.mp4'
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
         '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(path)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        try:
            for frame in range(round(DURATION*FPS)):
                process.stdin.write(render(frame/FPS).tobytes())
                if frame%(FPS*2)==0: print(f'{frame/FPS:.0f}/{DURATION:g} seconds rendered',flush=True)
            process.stdin.close()
            if process.wait(): raise RuntimeError('Video encoding failed')
        except BaseException:
            process.kill()
            raise
    path.replace(OUT/f'{NAME}.mp4')


def check():
    path=OUT/f'{NAME}.mp4'
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    reader=imageio_ffmpeg.read_frames(str(path))
    try: meta=next(reader)
    finally: reader.close()
    count,seconds=imageio_ffmpeg.count_frames_and_secs(str(path))
    assert count==FPS*DURATION and abs(seconds-DURATION)<.001
    assert meta['size']==(W,H) and meta['fps']==FPS
    subprocess.run([ffmpeg,'-v','error','-i',str(path),'-f','null','-'],check=True)
    indices=[round(t*FPS) for t in MOMENTS]
    selection='+'.join(f'eq(n\\,{i})' for i in indices)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(path),'-vf',
                    f'select={selection},scale=480:270,tile=3x3','-frames:v','1',
                    str(OUT/f'{NAME}-contact-sheet.png')],check=True)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(path),'-vf',
                    f'select=eq(n\\,{round(POSTER_TIME*FPS)})','-frames:v','1',
                    str(OUT/f'{NAME}-poster.png')],check=True)
    report=dict(video_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                duration_seconds=seconds,frame_count=count,size=meta['size'],fps=meta['fps'],
                decoded='passed',contact_sheet_frame_indices=indices,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                math_source_sha256=hashlib.sha256((ROOT/'scripts/symmetry_unitary_waves.py').read_bytes()).hexdigest(),
                surface='Real part of complex amplitude; fixed height scale',
                overlay='Comparison of alternatives, not a superposition',
                merge_seconds=[16,26/1.5],separate_playback_cycles=2,overlay_playback_cycles=1)
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    preview()
    if args.render: encode()
    if args.check: print(json.dumps(check()),flush=True)


if __name__=='__main__': main()
