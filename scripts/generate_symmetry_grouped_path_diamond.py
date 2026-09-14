"""Replace neighboring path chains by their exact regional resultants.

The seven physical regions, 20,001 paths, full scalar propagation weights,
three wavelengths, reference, and plot scale stay fixed. Grouping changes
the representation only. Earlier generators and media are untouched.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
import subprocess
import time

import generate_symmetry_normalized_path_diamond as physical
from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow,
)

NAME = "symmetry-grouped-path-diamond-wavelength-scan"
WIDTH, HEIGHT, FPS = 1440, 1080, 30
GROUPS = 7
N, Y, DY = physical.N, physical.Y, physical.DY
WAVELENGTHS = physical.WAVELENGTHS
EDGES = np.linspace(physical.HALF_EXTENT, -physical.HALF_EXTENT, GROUPS+1)
# Boundaries are chosen in physical space, not fitted to a phasor turn.
CUTS = np.r_[0, [np.count_nonzero(Y >= edge) for edge in EDGES[1:-1]], N]
CENTRAL = GROUPS // 2
INTRO, PER_GROUP, HOLD = .6, .7, 2.5
PASS_SECONDS = INTRO + GROUPS*PER_GROUP + HOLD
PASS_FRAMES = round(PASS_SECONDS*FPS)
TOTAL_FRAMES = PASS_FRAMES*len(WAVELENGTHS)
ORIGIN, SCALE = physical.ORIGIN, physical.PIXELS_PER_UNIT
A, B, SCREEN_X, CENTER_Y, SCREEN_HALF = (200.,292.), (1240.,292.), 720.,292.,112.
CENTRAL_BLUE = (24, 67, 113)


def point(value):
    return (ORIGIN[0]+SCALE*value.real, ORIGIN[1]-SCALE*value.imag)


def crossing(y):
    return (SCREEN_X, CENTER_Y-SCREEN_HALF*float(y)/physical.HALF_EXTENT)


def dot(draw, xy, color, radius):
    x,y=xy
    draw.ellipse(pixels((x-radius,y-radius,x+radius,y+radius)),fill=color)


def state(index):
    index=min(max(int(index),0),TOTAL_FRAMES-1)
    stage,local=divmod(index,PASS_FRAMES)
    seconds=local/FPS
    p=(seconds-INTRO)/PER_GROUP
    done=int(np.clip(math.floor(p),0,GROUPS))
    active=done if 0<=p<GROUPS else None
    fraction=p-done if active is not None else 0.
    return stage,done,active,fraction


@lru_cache(None)
def model(stage):
    _,vectors,vertices,_,_=physical.model(stage)
    # Explicit sums provide an independent check against prefix differences.
    groups=np.array([np.sum(vectors[a:b]) for a,b in zip(CUTS[:-1],CUTS[1:])])
    corners=vertices[CUTS]
    raster=tuple(pixels(point(z)) for z in vertices)
    return vectors,vertices,groups,corners,raster


@lru_cache(None)
def background(stage):
    image=Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,23),"Same paths · sum them in groups",31,bold=True)
    text(d,(39,67),"Point source A · fixed B · seven fixed regions of one screen",19,MUTED)
    ratio=round(WAVELENGTHS[0]/WAVELENGTHS[stage])
    label="λ = λ₀" if ratio==1 else f"λ = λ₀ / {ratio}"
    text(d,(1400,23),label,31,bold=True,anchor="ra")
    text(d,(1400,69),f"{stage+1} / 3",18,MUTED,anchor="ra")
    for box in ((30,111,1410,455),(30,474,1410,1021)):
        d.rounded_rectangle(pixels(box),radius=14*SUPERSAMPLE,fill=PANEL,
                            outline=BORDER,width=SUPERSAMPLE)
    text(d,(53,129),"Path diamond",23,bold=True)
    text(d,(1387,134),"Same 20,001 paths",19,MUTED,anchor="ra")
    for group in range(GROUPS):
        upper,lower=crossing(EDGES[group]),crossing(EDGES[group+1])
        for source in (A,B):
            d.polygon([pixels(xy) for xy in (source,upper,lower)],fill=(*BLUE,14))
    for edge in EDGES:
        xy=crossing(edge)
        line(d,A,xy,(*BLUE,43),.65)
        line(d,xy,B,(*BLUE,43),.65)
    text(d,(53,431),"Regions stay the same size as λ decreases",17,MUTED)
    text(d,(1387,431),"Each region contains about 2,857 paths",17,MUTED,anchor="ra")
    text(d,(53,492),"Tip to tail",23,bold=True)
    text(d,(1387,497),"Gold: total of all 20,001 paths",18,GOLD,anchor="ra")
    physical.drawing.dash(d,(101,ORIGIN[1]),(1300,ORIGIN[1]),AXIS,.8,3,5)
    text(d,(1312,ORIGIN[1]-10),"Re",14,MUTED)
    ref=point(1+0j)
    d.ellipse(pixels((ref[0]-5,ref[1]-5,ref[0]+5,ref[1]+5)),outline=(*MUTED,180),width=SUPERSAMPLE)
    text(d,(53,992),"Unobstructed A → B = 1 · same scale throughout",16,MUTED)
    text(d,(1387,992),"Grouping preserves the gold arrow exactly",16,GOLD,anchor="ra")
    text(d,(39,1041),"Full propagation weights · no change to the path sum",17,MUTED)
    text(d,(1400,1041),"λ₀ = 0.5 · A–screen = screen–B = 4.5",17,MUTED,anchor="ra")
    return image


def frame(index):
    stage,done,active,fraction=state(index)
    image=background(stage).copy()
    d=ImageDraw.Draw(image,"RGBA")
    _,vertices,groups,corners,raster=model(stage)
    # Highlight is a correspondence marker, never an intensity or probability.
    highlight=active if active is not None else (CENTRAL if done==GROUPS else None)
    if highlight is not None:
        upper,lower=crossing(EDGES[highlight]),crossing(EDGES[highlight+1])
        for source in (A,B):
            d.polygon([pixels(xy) for xy in (source,upper,lower)],fill=(*BLUE,40))
        for end in (upper,lower):
            line(d,A,end,(*BLUE,150),1.)
            line(d,end,B,(*BLUE,150),1.)
    physical.drawing.dash(d,A,B,(*MUTED,100),.9,4,6)
    for group in range(GROUPS):
        upper,lower=crossing(EDGES[group]),crossing(EDGES[group+1])
        color=CENTRAL_BLUE if group==CENTRAL else BLUE
        line(d,upper,lower,(*color,220),4 if group==highlight else 2)
        # Tiny neutral marks distinguish a sampling screen from a solid wall.
        for y in np.arange(upper[1]+2,lower[1],4):
            dot(d,(SCREEN_X,float(y)),PANEL,.7)
        mid=(upper[1]+lower[1])/2
        d.rounded_rectangle(pixels((SCREEN_X+10,mid-11,SCREEN_X+33,mid+11)),
                            radius=3*SUPERSAMPLE,fill=PANEL)
        text(d,(SCREEN_X+21,mid),str(group+1),15,color,
             bold=group==highlight,anchor="mm")
    for edge in EDGES:
        x,y=crossing(edge)
        line(d,(x-6,y),(x+6,y),INK,.9)
    for xy,label in ((A,"A"),(B,"B")):
        dot(d,xy,INK,5.8)
        text(d,(xy[0],xy[1]+17),label,20,INK,bold=True,anchor="ma")

    if active is not None:
        caption=f"Region {active+1}: its path chain → one net arrow"
    elif done==GROUPS:
        caption="Seven regional sums · region 4 contains the straight path"
    else:
        caption="Before grouping: every path arrow, tip to tail"
    text(d,(53,534),caption,19,BLUE)

    for group,(start,end) in enumerate(zip(CUTS[:-1],CUTS[1:])):
        color=CENTRAL_BLUE if group==CENTRAL else BLUE
        if group<done:
            arrow(d,point(corners[group]),point(corners[group+1]),color,
                  width=3.8 if group==CENTRAL else 2.8,head=10)
        elif group==active:
            # Change of representation at fixed λ: the regional chain keeps
            # its true endpoints. The chord is the exact regional sum. Its
            # reveal is drawing progress, not a new physical partial sum.
            raw_alpha=round(255*(1-np.clip((fraction-.35)/.45,0,1)))
            if raw_alpha:
                d.line(raster[start:end+1],fill=(*BLUE,raw_alpha),width=2*SUPERSAMPLE)
            reveal=float(np.clip(fraction/.4,0,1))
            endpoint=corners[group]+reveal*groups[group]
            arrow(d,point(corners[group]),point(endpoint),color,width=3.8,head=10)
        else:
            d.line(raster[start:end+1],fill=BLUE,width=round(1.5*SUPERSAMPLE))
    # This is always the complete, unchanged total at the current wavelength.
    dot(d,ORIGIN,MUTED,2.7)
    arrow(d,ORIGIN,point(vertices[-1]),GOLD,width=1.9,head=9)
    dot(d,point(vertices[-1]),GOLD,3.2)

    if done==GROUPS:
        # Compact quantitative labels identify exactly what the arrows mean.
        # They describe amplitude magnitudes, never endpoint probabilities.
        text(d,(53,944),f"Central region: |sum| = {abs(groups[CENTRAL]):.3f}",18,CENTRAL_BLUE)
        outer=np.delete(groups,CENTRAL)
        text(d,(1387,944),f"Largest outer region: |sum| = {max(abs(outer)):.3f}",18,MUTED,anchor="ra")
    return image.reduce(SUPERSAMPLE)


def final_frame(stage):
    return (stage+1)*PASS_FRAMES-1


def checks():
    assert np.all(np.diff(CUTS)>0) and CUTS[0]==0 and CUTS[-1]==N
    assert np.allclose(EDGES,-EDGES[::-1],atol=1e-15)
    assert np.array_equal(np.diff(CUTS),np.diff(CUTS)[::-1])
    reports=[]
    for stage,wavelength in enumerate(WAVELENGTHS):
        vectors,vertices,groups,corners,_=model(stage)
        prefix_error=float(max(abs(np.r_[0j,np.cumsum(groups)]-corners)))
        total_error=float(abs(np.sum(groups)-vertices[-1]))
        assert prefix_error<1e-12 and total_error<1e-12
        assert max(abs(groups-groups[::-1]))<1e-12
        # Independent refined quadrature over exactly the same midpoint cells.
        fine_n=3*N
        fine_y=physical.HALF_EXTENT-(np.arange(fine_n)+.5)*2*physical.HALF_EXTENT/fine_n
        fine=physical.integrand(fine_y,wavelength)*DY/3
        refined=np.array([sum(fine[3*a:3*b]) for a,b in zip(CUTS[:-1],CUTS[1:])])
        refinement=float(max(abs(groups-refined)))
        assert refinement<1e-4
        xy=np.asarray([point(z) for z in vertices])
        assert xy[:,0].min()>95 and xy[:,0].max()<1270
        assert xy[:,1].min()>580 and xy[:,1].max()<960
        reports.append({"wavelength":wavelength,"groups_real_imag":[[z.real,z.imag] for z in groups],
                        "central_magnitude":abs(groups[CENTRAL]),
                        "largest_outer_magnitude":float(max(abs(np.delete(groups,CENTRAL)))),
                        "total_real_imag":[vertices[-1].real,vertices[-1].imag],
                        "prefix_identity_error":prefix_error,"total_identity_error":total_error,
                        "threefold_refinement_max_error":refinement})
    report={"path_count":N,"path_positions_sha256":hashlib.sha256(Y.tobytes()).hexdigest(),
            "physical_region_edges":EDGES.tolist(),"sample_cuts":CUTS.tolist(),
            "paths_per_region":np.diff(CUTS).tolist(),"same_regions_all_wavelengths":True,
            "same_scalar_model_as_previous_movie":True,"endpoint_dependent_scaling":False,
            "reference":"independent unobstructed A to B field", "scale":SCALE,
            "gold":"complete sum at each wavelength, unchanged throughout regrouping",
            "reveal":"drawing a regional resultant; not summing fractional physical paths",
            "timing_seconds":{"initial_raw":INTRO,"per_region":PER_GROUP,"grouped_hold":HOLD},
            "fps":FPS,"frames":TOTAL_FRAMES,"duration_seconds":TOTAL_FRAMES/FPS,"stages":reports}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def previews():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,1254),BG)
    for stage in range(3):
        still=frame(final_frame(stage))
        still.save(OUT/f"{NAME}-lambda-{stage+1}.png")
        sheet.paste(still.resize((480,360),Image.Resampling.LANCZOS),(stage*480,0))
        crop=still.crop((30,565,1410,986)).resize((960,292),Image.Resampling.LANCZOS)
        sheet.paste(crop,(240,369+stage*294))
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
    start=time.perf_counter()
    cached_key,cached_rgb=None,None
    try:
        for index in range(TOTAL_FRAMES):
            key=state(index)
            if key!=cached_key:
                cached_rgb=frame(index).tobytes()
                cached_key=key
            process.stdin.write(cached_rgb)
            if index%(FPS*3)==0:
                print(f"{index/FPS:g}/{TOTAL_FRAMES/FPS:g} s; elapsed {time.perf_counter()-start:.1f} s",flush=True)
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
    wanted={stage*PASS_FRAMES+round(t*FPS) for stage in range(3)
            for t in (0,INTRO+.28,INTRO+3*PER_GROUP+.28,INTRO+6*PER_GROUP+.28)}
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
        stage=state(index)[0]
        x,y=map(round,point(model(stage)[1][-1]))
        crop=decoded[y-5:y+6,x-5:x+6].astype(float)
        gold_pixels=int(np.sum(np.linalg.norm(crop-np.asarray(GOLD),axis=2)<65))
        assert gold_pixels>8
        checked.append({"frame":index,"mean_absolute_rgb_error":error,"gold_tip_pixels":gold_pixels})
        if index==final_frame(stage):
            selected[stage]=Image.fromarray(decoded.copy())
    assert count==TOTAL_FRAMES and len(selected)==3
    sheet=Image.new("RGB",(1440,1080),BG)
    for stage in range(3):
        sheet.paste(selected[stage].resize((480,360),Image.Resampling.LANCZOS),(stage*480,0))
        crop=selected[stage].crop((30,565,1410,986)).resize((768,233),Image.Resampling.LANCZOS)
        sheet.paste(crop,(336,370+stage*235))
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration_seconds":count/FPS,"checks":checked}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_frames":count,"checked":len(checked),
                      "max_rgb_error":max(c["mean_absolute_rgb_error"] for c in checked)}),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args=parser.parse_args()
    if args.check: checks()
    if args.preview: previews()
    if args.render: render()
    if args.encoded_check: encoded_checks()
