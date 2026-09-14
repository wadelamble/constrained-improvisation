"""Three nearby path lengths, two wavelengths, and the phase left after turns.

This standalone insert shows deterministic remainder-angle sensitivity.
It does not use random stopping angles or claim three examples prove general
interference cancellation. Existing path-diamond films remain unchanged.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import time
from functools import lru_cache

from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow,
)

NAME="symmetry-phase-remainder-spinners"
WIDTH,HEIGHT,FPS=1440,870,60
PATH_LENGTHS=np.array([3.125,3.165,3.205])
WAVELENGTHS=np.array([36.,1./9.])
TURNS=PATH_LENGTHS[:,None]/WAVELENGTHS[None,:]
PHASES=2*np.pi*TURNS
REMAINDERS=PHASES%(2*np.pi)
PRELUDE,SPIN,HOLD=.8,3.6,1.8
PASS_SECONDS=SPIN+HOLD
DURATION=PRELUDE+3*PASS_SECONDS
TOTAL_FRAMES=round(DURATION*FPS)
PRELUDE_FRAMES=round(PRELUDE*FPS)
PASS_FRAMES=round(PASS_SECONDS*FPS)
SPIN_FRAMES=round(SPIN*FPS)
CENTERS=((367.,415.),(1073.,415.))
RADIUS=144.
PANELS=((30,126,704,790),(736,126,1410,790))


def endpoint(center,angle,radius=RADIUS):
    return (center[0]+radius*math.cos(angle),center[1]-radius*math.sin(angle))


def circle(draw,center,radius,color,width=1):
    x,y=center
    draw.ellipse(pixels((x-radius,y-radius,x+radius,y+radius)),
                 outline=color,width=max(1,round(width*SUPERSAMPLE)))


def dot(draw,xy,color,radius=3):
    x,y=xy
    draw.ellipse(pixels((x-radius,y-radius,x+radius,y+radius)),fill=color)


def arc(draw,center,angle,radius,color,width=2):
    if angle<=0:
        return
    angles=np.linspace(0,angle,max(2,int(angle*radius/2)+1))
    points=[pixels(endpoint(center,a,radius)) for a in angles]
    draw.line(points,fill=color,width=round(width*SUPERSAMPLE))


def state(index):
    index=min(max(int(index),0),TOTAL_FRAMES-1)
    if index<PRELUDE_FRAMES:
        return 0,0.,False
    stage,within=divmod(index-PRELUDE_FRAMES,PASS_FRAMES)
    p=float(np.clip(within/SPIN_FRAMES,0,1))
    # Display pacing: easing makes the starting and remainder angles readable.
    # The total advance remains exactly 2π L/λ; playback is not optical time.
    eased=p*p*(3-2*p)
    return stage,eased,within>=SPIN_FRAMES


def final_frame(stage):
    return PRELUDE_FRAMES+(stage+1)*PASS_FRAMES-1


@lru_cache(None)
def background():
    image=Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,23),"Same paths · different wavelengths",31,bold=True)
    text(d,(39,68),"Three nearby path lengths · the same change in L on both sides",19,MUTED)
    text(d,(1400,26),"φ = 2πL / λ",27,INK,anchor="ra")
    for pane,box in enumerate(PANELS):
        d.rounded_rectangle(pixels(box),radius=16*SUPERSAMPLE,
                            fill=PANEL,outline=BORDER,width=SUPERSAMPLE)
        left,_,right,_=box
        title="Slower phase advance" if pane==0 else "Faster phase advance"
        subtitle="Longer wavelength · λ = 36" if pane==0 else "Shorter wavelength · λ = 1/9"
        text(d,(left+25,147),title,26,bold=True)
        text(d,(left+26,190),subtitle,19,MUTED)
        center=CENTERS[pane]
        line(d,(center[0]-RADIUS-19,center[1]),(center[0]+RADIUS+24,center[1]),AXIS,1)
        line(d,(center[0],center[1]-RADIUS-20),(center[0],center[1]+RADIUS+20),AXIS,1)
        circle(d,center,RADIUS,BORDER,1.1)
        text(d,(center[0]+RADIUS+34,center[1]-9),"Re",16,MUTED)
        text(d,(center[0]+8,center[1]-RADIUS-39),"Im",16,MUTED)
        for deg in range(0,360,30):
            angle=math.radians(deg)
            line(d,endpoint(center,angle,RADIUS-4),endpoint(center,angle,RADIUS+4),BORDER,1)
        if pane==0:
            text(d,(center[0],614),"Phase advance",17,MUTED,anchor="ma")
            text(d,(center[0],708),"Less than one turn",19,MUTED,anchor="ma")
        else:
            text(d,(center[0],614),"Completed turns",17,MUTED,anchor="ma")
            text(d,(center[0],697),"Remainder angle",17,MUTED,anchor="ma")
    text(d,(39,818),"Each run starts from the real axis",20,MUTED)
    text(d,(1400,821),"θ = φ mod 2π   ·   θ determines the final direction",20,GOLD,anchor="ra")
    return image


def frame(index):
    stage,progress,stopped=state(index)
    image=background().copy()
    d=ImageDraw.Draw(image,"RGBA")
    length=PATH_LENGTHS[stage]
    text(d,(1400,72),f"Path {stage+1} / 3    L = {length:.3f}",20,INK,anchor="ra")
    for pane,center in enumerate(CENTERS):
        phase=float(PHASES[stage,pane]*progress)
        whole=int(math.floor(phase/(2*np.pi)+1e-12))
        theta=phase%(2*np.pi)
        # Historical endpoints remain where those earlier runs actually ended.
        for previous in range(stage):
            old_angle=float(REMAINDERS[previous,pane])
            old_tip=endpoint(center,old_angle)
            arrow(d,center,old_tip,(*BLUE,72),width=1.8,head=8)
            circle(d,old_tip,4,(*BLUE,165),1.4)
            if pane==1:
                text(d,endpoint(center,old_angle,RADIUS+25),str(previous+1),17,MUTED,anchor="mm")
        # A short trail exposes rotation direction without drawing extra turns.
        trail_angle=min(.44,phase)
        if progress>0 and not stopped:
            angles=np.linspace(phase-trail_angle,phase,24)
            for a,b in zip(angles[:-1],angles[1:]):
                line(d,endpoint(center,a,RADIUS-5),endpoint(center,b,RADIUS-5),(*BLUE,75),2.)
        # The final remainder sector appears after the complete phase advance.
        if stopped and pane==1:
            arc(d,center,theta,45,GOLD,2.2)
            dot(d,endpoint(center,theta,45),GOLD,2.8)
        tip=endpoint(center,phase)
        arrow(d,center,tip,BLUE,width=3.7,head=12)
        dot(d,center,INK,3.5)
        dot(d,tip,GOLD if stopped else BLUE,4.5)
        if stopped and pane==1:
            text(d,endpoint(center,theta,RADIUS+25),str(stage+1),17,BLUE,bold=True,anchor="mm")
        if pane==0:
            text(d,(center[0],640),f"{math.degrees(phase):.2f}°",36,BLUE,bold=True,anchor="ma")
        else:
            text(d,(center[0],640),str(whole),36,INK,bold=True,anchor="ma")
            remainder_label=f"{math.degrees(theta):.1f}°" if stopped else "…"
            text(d,(center[0],724),remainder_label,29,GOLD,bold=stopped,anchor="ma")
    return image.reduce(SUPERSAMPLE)


def checks():
    assert np.allclose(np.diff(PATH_LENGTHS),.04,rtol=0,atol=1e-14)
    assert np.allclose(PHASES[:,1],324*PHASES[:,0],rtol=0,atol=6e-14)
    assert np.all((TURNS[:,0]>0)&(TURNS[:,0]<.1))
    assert np.allclose(np.exp(1j*PHASES),np.exp(1j*REMAINDERS),atol=2e-14)
    assert np.allclose(np.degrees(REMAINDERS),[[31.25,45],[31.65,174.6],[32.05,304.2]],atol=2e-11)
    max_step=0.
    for stage in range(3):
        start=PRELUDE_FRAMES+stage*PASS_FRAMES
        assert state(start)==(stage,0.,False)
        phases=np.array([PHASES[stage]*state(i)[1]
                         for i in range(start,start+round(SPIN*FPS)+1)])
        max_step=max(max_step,float(np.max(np.diff(phases,axis=0))))
        assert state(final_frame(stage))[0]==stage and state(final_frame(stage))[2]
    assert max_step<np.pi
    report={"path_lengths":PATH_LENGTHS.tolist(),"wavelengths":WAVELENGTHS.tolist(),
            "phase_rule":"2*pi*L/lambda","whole_turns":np.floor(TURNS).astype(int).tolist(),
            "remainders_degrees":np.degrees(REMAINDERS).tolist(),
            "same_path_increment":.04,"deterministic_no_random_angles":True,
            "left_full_phase_degrees":np.degrees(PHASES[:,0]).tolist(),
            "left_no_completed_turns_or_remainder_display":True,
            "three_examples_are_not_a_cancellation_proof":True,
            "playback":"phase advance with smooth display pacing, not optical time",
            "largest_phase_advance_per_frame_degrees":math.degrees(max_step),
            "timing":{"prelude":PRELUDE,"spin_each":SPIN,"hold_each":HOLD},
            "duration_seconds":DURATION,"fps":FPS,"frames":TOTAL_FRAMES,
            "resolution":[WIDTH,HEIGHT]}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def previews():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,1305),BG)
    for stage in range(3):
        still=frame(final_frame(stage))
        still.save(OUT/f"{NAME}-run-{stage+1}.png")
        mid=frame(round((PRELUDE+stage*PASS_SECONDS+SPIN*.55)*FPS))
        sheet.paste(mid.resize((720,435),Image.Resampling.LANCZOS),(0,stage*435))
        sheet.paste(still.resize((720,435),Image.Resampling.LANCZOS),(720,stage*435))
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output=OUT/f"{NAME}.mp4"
    command=[imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
             "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
             "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast",
             "-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    started=time.perf_counter()
    key,rgb=None,None
    try:
        for index in range(TOTAL_FRAMES):
            new_key=state(index)
            if new_key!=key:
                rgb=frame(index).tobytes()
                key=new_key
            process.stdin.write(rgb)
            if index%(3*FPS)==0:
                print(f"{index/FPS:g}/{DURATION:g} s; elapsed {time.perf_counter()-started:.1f} s",flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    print(json.dumps({"video":str(output),"bytes":output.stat().st_size}),flush=True)


def encoded_checks():
    wanted={round((PRELUDE+stage*PASS_SECONDS+fraction*SPIN)*FPS)
            for stage in range(3) for fraction in (0,.25,.5,.75,1)}
    wanted.update(final_frame(stage) for stage in range(3))
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata=next(reader)
    assert tuple(metadata["size"])==(WIDTH,HEIGHT) and abs(metadata["fps"]-FPS)<1e-8
    checked,selected,count=[],{},0
    for index,raw in enumerate(reader):
        count+=1
        if index not in wanted:
            continue
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        expected=np.asarray(frame(index))
        error=float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
        assert error<2.5
        stage,p,stopped=state(index)
        tip_errors=[]
        for pane,center in enumerate(CENTERS):
            x,y=map(round,endpoint(center,PHASES[stage,pane]*p))
            crop=decoded[y-4:y+5,x-4:x+5].astype(float)
            color=GOLD if stopped else BLUE
            matches=int(np.sum(np.linalg.norm(crop-np.array(color),axis=2)<65))
            assert matches>10
            tip_errors.append(matches)
        checked.append({"frame":index,"mean_absolute_rgb_error":error,"matching_tip_pixels":tip_errors})
        if index==final_frame(stage):
            selected[stage]=Image.fromarray(decoded.copy())
    assert count==TOTAL_FRAMES and len(selected)==3
    sheet=Image.new("RGB",(1440,1305),BG)
    for stage in range(3):
        sheet.paste(selected[stage].resize((720,435),Image.Resampling.LANCZOS),(360,stage*435))
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration_seconds":count/FPS,"checks":checked}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_frames":count,"checked":len(checked),
                      "max_rgb_error":max(x["mean_absolute_rgb_error"] for x in checked)}),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args=parser.parse_args()
    if args.check: checks()
    if args.preview: previews()
    if args.render: render()
    if args.encoded_check: encoded_checks()
