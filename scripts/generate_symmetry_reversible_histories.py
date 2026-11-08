"""Two reversible billiard histories, compared side by side and in overlay.

The shared clock runs forward and backward twice in the separate panes.
During the last third the clock pauses while the views coincide, then both
histories run forward and backward once more. Overlay is a comparison of
independent histories; balls in different histories do not interact.

Run with --render --check. Omitting flags creates source-frame previews.
Playback is uniformly accelerated by PLAYBACK_SPEED; the physics is unchanged.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from symmetry_reversible_balls import build_histories

NAME = 'symmetry-reversible-histories'
OUT = ROOT / 'content/drafts/animations'
REVIEW = ROOT / '.tools' / f'{NAME}-review'
W, H, SS, FPS = 1600, 900, 2, 24
STORY_DURATION, PLAYBACK_SPEED = 36, 1.5
DURATION = STORY_DURATION / PLAYBACK_SPEED
BG, TABLE, INK, MUTED, BORDER = '#fffcf6', '#f5f1e9', '#232426', '#78746e', '#bdb6aa'
COLORS = ('#2b659b', '#bc7520')
HISTORIES = None
# screen start/end, physical start/end. No easing of physical motion.
BEATS = (
    (0., 1., 0., 0.), (1., 6., 0., 8.), (6., 6.5, 8., 8.),
    (6.5, 11.5, 8., 0.), (11.5, 12., 0., 0.),
    (12., 17., 0., 8.), (17., 17.5, 8., 8.),
    (17.5, 22.5, 8., 0.), (22.5, 26., 0., 0.),
    (26., 30.25, 0., 8.), (30.25, 30.75, 8., 8.),
    (30.75, 35., 8., 0.), (35., 36., 0., 0.),
)
MOMENTS = tuple(t/PLAYBACK_SPEED for t in (0., 3.5, 6., 9., 12., 20., 25., 28.4, 35.5))
POSTER_TIME = 28.4/PLAYBACK_SPEED


def ease(u):
    u = min(1., max(0., u))
    return u*u*(3-2*u)


def rgb(color):
    return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))


def mix(a, b, u):
    return tuple(round((1-u)*x + u*y) for x,y in zip(rgb(a), rgb(b)))


@lru_cache(32)
def font(size, bold=False):
    names = [Path('C:/Windows/Fonts') / ('seguisb.ttf' if bold else 'segoeui.ttf'),
             Path('/usr/share/fonts/truetype/dejavu') /
             ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in names:
        if path.exists():
            return ImageFont.truetype(str(path), round(size*SS))
    raise FileNotFoundError('A Unicode font is required')


def xy(values):
    return tuple(round(float(v)*SS) for v in values)


def text(draw, x, y, label, size, color=INK, bold=False, alpha=255):
    fill = rgb(color)+(alpha,) if isinstance(color,str) else tuple(color)+(alpha,)
    draw.text(xy((x,y)), label, font=font(size,bold), fill=fill, anchor='mm')


def timeline(screen_time):
    s = min(max(float(screen_time), 0.), STORY_DURATION)
    for a,b,ta,tb in BEATS:
        if a <= s < b or (s == STORY_DURATION and b == STORY_DURATION):
            t = ta+(tb-ta)*(s-a)/(b-a)
            direction = int(np.sign(tb-ta))
            # Trail tails follow the displayed motion; they do not redefine
            # the physical velocity stored in the exact history.
            trail_direction = direction
            if not direction:
                trail_direction = 1 if ta == 8. else -1
            if s < 1.:
                trail_direction = 1
            return t, direction, trail_direction
    raise AssertionError(s)


def geometry(screen_time, which):
    merged = ease((screen_time-24.)/2.)
    start_x = (80., 840.)[which]
    return (start_x+(390.-start_x)*merged,
            244.-22.*merged,
            680.+140.*merged,
            merged)


def project(points, x, y, width, box):
    points = np.asarray(points)
    return np.stack((x+width*points[...,0]/box[0],
                     y+width*(box[1]-points[...,1])/box[0]),axis=-1)


def draw_table(image, x, y, width, box, alpha=255):
    layer = Image.new('RGBA', image.size)
    d = ImageDraw.Draw(layer)
    height = width*box[1]/box[0]
    d.rounded_rectangle(xy((x-9,y-9,x+width+9,y+height+9)), radius=17*SS,
                        fill=rgb(TABLE)+(alpha,), outline=rgb(BORDER)+(alpha,), width=2*SS)
    d.rectangle(xy((x,y,x+width,y+height)),outline=rgb(BORDER)+(alpha,),width=SS)
    image.alpha_composite(layer)


def draw_history(image, history, t, direction, x, y, width, merged, color):
    layer = Image.new('RGBA',image.size)
    d = ImageDraw.Draw(layer)
    p, velocity = history.sample(t)
    radius = history.radius*width/history.box[0]
    # Fading short trajectories make exact retracing and collisions legible.
    samples = np.linspace(.32,0,13)
    traces = np.array([history.sample(float(np.clip(t-direction*tau,0,history.duration)))[0]
                       for tau in samples])
    traces = project(traces,x,y,width,history.box)
    for ball in range(len(p)):
        for j in range(len(samples)-1):
            alpha = round(18+84*j/(len(samples)-2))
            d.line([xy(traces[j,ball]),xy(traces[j+1,ball])],
                   fill=rgb(color)+(alpha,),width=round(2.4*SS))
    centers = project(p,x,y,width,history.box)
    fill_alpha = round(255-95*merged)
    edge = mix(color,INK,.22)
    for px,py in centers:
        d.ellipse(xy((px-radius,py-radius,px+radius,py+radius)),
                  fill=rgb(color)+(fill_alpha,),outline=edge+(255,),width=round(1.35*SS))
        # A restrained, fixed highlight reads as a ball rather than a data dot.
        rr=radius*.19
        cx,cy=px-radius*.28,py-radius*.28
        d.ellipse(xy((cx-rr,cy-rr,cx+rr,cy+rr)),fill=(255,255,255,round(110*(1-.3*merged))))
    image.alpha_composite(layer)


def render(screen_time):
    global HISTORIES
    screen_time *= PLAYBACK_SPEED
    if HISTORIES is None:
        HISTORIES = build_histories(duration=8.)
    im = Image.new('RGBA',(W*SS,H*SS),BG)
    d = ImageDraw.Draw(im)
    text(d,800,67,'Reversible and distinguishable histories',43,INK,True)
    text(d,800,120,'Different initial conditions, the same laws',25,MUTED)
    t,direction,trail_direction = timeline(screen_time)
    merged = geometry(screen_time,0)[3]
    tables = [geometry(screen_time,i) for i in range(2)]
    # During the merge both outlines stay visible; draw floors before balls
    # so one comparison pane cannot conceal the other state's trajectories.
    for i,(x,y,width,_) in enumerate(tables):
        if i==1 and merged==1.: continue
        draw_table(im,x,y,width,HISTORIES[i].box)
    for i,(x,y,width,_) in enumerate(tables):
        draw_history(im,HISTORIES[i],t,trail_direction,x,y,width,merged,COLORS[i])
    d = ImageDraw.Draw(im)
    for i in range(2):
        label_x = (420.,1180.)[i] + ((688.,912.)[i]-(420.,1180.)[i])*merged
        text(d,label_x,204.-33.*merged,f'State {i+1}',33,COLORS[i],True)
    if merged>.75:
        text(d,800,170,'≠',42,INK,alpha=round(255*ease((merged-.75)/.25)))
    # One time readout serves both states, including the overlay.
    text(d,800,810,f't = {t:.1f}',31,INK)
    if direction:
        text(d,1100,810,'Time runs forward' if direction>0 else 'Time runs backward',22,MUTED)
        ax=505
        sign=direction
        d.line([xy((ax-25*sign,810)),xy((ax+25*sign,810))],fill=rgb(MUTED),width=2*SS)
        d.polygon([xy((ax+25*sign,810)),xy((ax+13*sign,803)),xy((ax+13*sign,817))],fill=rgb(MUTED))
    a,b,y = 565.,1035.,855.
    d.line([xy((a,y)),xy((b,y))],fill=rgb('#d8d1c6'),width=2*SS)
    for value in range(9):
        px=a+(b-a)*value/8
        d.line([xy((px,y-4)),xy((px,y+4))],fill=rgb(BORDER),width=SS)
    marker=a+(b-a)*t/8
    d.ellipse(xy((marker-5,y-5,marker+5,y+5)),fill=rgb(INK))
    text(d,a-24,y,'0',17,MUTED)
    text(d,b+24,y,'8',17,MUTED)
    return im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)


def verify_timeline():
    assert BEATS[0][0]==0 and BEATS[-1][1]==STORY_DURATION
    for first,second in zip(BEATS,BEATS[1:]):
        assert first[1]==second[0] and first[3]==second[2]
    for s in np.linspace(24,26,100):
        assert timeline(s)[0]==0
    for s in np.linspace(0,STORY_DURATION,1000):
        t,_,_=timeline(s)
        assert 0<=t<=8
        for i in range(2):
            x,y,w,_=geometry(s,i)
            assert x>=50 and x+w<=1550 and y>=180 and y+w*.66<780
    return dict(duration_seconds=DURATION,size=[W,H],fps=FPS,
                separate_playback_cycles=2,overlay_playback_cycles=1,
                playback_speed=PLAYBACK_SPEED,
                merge_seconds=[24/PLAYBACK_SPEED,26/PLAYBACK_SPEED],merge_clock_paused=True,
                simultaneous_clock=True,independent_comparison_histories=True,
                colors=COLORS,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                physics_source_sha256=hashlib.sha256((ROOT/'scripts/symmetry_reversible_balls.py').read_bytes()).hexdigest())


def encode():
    path=REVIEW/f'{NAME}.rendering.mp4'
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast',
         '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(path)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as process:
        try:
            for frame in range(round(DURATION*FPS)):
                process.stdin.write(render(frame/FPS).tobytes())
                if frame%(FPS*4)==0: print(f'{frame/FPS:.0f}/{DURATION} seconds rendered',flush=True)
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
                decoded='passed',contact_sheet_frame_indices=indices)
    (OUT/f'{NAME}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    REVIEW.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    report=verify_timeline()
    (OUT/f'{NAME}-timing-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    sheet=Image.new('RGB',(1200,3*225),BG)
    for i,t in enumerate(MOMENTS):
        im=render(t)
        im.save(REVIEW/f'{t:05.1f}.png')
        sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),((i%3)*400,(i//3)*225))
    sheet.save(REVIEW/'contact.png')
    render(POSTER_TIME).save(OUT/f'{NAME}-poster.png')
    print(json.dumps(report),flush=True)
    if args.render: encode()
    if args.check: print(json.dumps(check()),flush=True)


if __name__=='__main__': main()
