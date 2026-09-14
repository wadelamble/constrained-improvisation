"""Fixed physical-position colors link paths to their ungrouped phasors.

Same normalized model, 20,001 paths, wavelengths, scan timing, and plot scale.
Only the visual correspondence changes. Earlier generators/media are kept.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json

import generate_symmetry_normalized_path_diamond as physical
from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow,
)

drawing=physical.drawing
NAME="symmetry-spectrum-path-diamond-wavelength-scan"
WIDTH,HEIGHT,FPS=physical.WIDTH,physical.HEIGHT,physical.FPS
N,Y,HALF_EXTENT=physical.N,physical.Y,physical.HALF_EXTENT
WAVELENGTHS=physical.WAVELENGTHS
ORIGIN,SCALE=physical.ORIGIN,physical.PIXELS_PER_UNIT
PALETTE=np.array([(43,86,161),(12,144,166),(38,147,86),
                  (181,158,30),(224,116,32),(198,49,45)],dtype=float)


def color_at(y):
    """Blue at either physical edge, through the spectrum to red at y=0."""
    t=np.clip(1-np.abs(np.asarray(y,dtype=float))/HALF_EXTENT,0,1)
    return np.rint(np.stack([np.interp(t,np.linspace(0,1,len(PALETTE)),PALETTE[:,c])
                              for c in range(3)],axis=-1)).astype(np.uint8)


COLORS=color_at(Y)
COLORS.setflags(write=False)
RGB=tuple(tuple(int(c) for c in row) for row in COLORS)
# This only batches adjacent line segments with identical 8-bit colors.
# Every original vertex is retained; no subchain is replaced by a chord.
COLOR_CUTS=np.r_[0,np.flatnonzero(np.any(COLORS[1:]!=COLORS[:-1],axis=1))+1,N]


@lru_cache(None)
def fan():
    """Rasterize the dense family by the crossing position of each pixel.

    Each pixel belongs to A→(0,y)→B for one y, except at the point endpoints.
    This is the established unresolved path paint, not a wave/intensity map.
    """
    s=SUPERSAMPLE
    left,top=int(drawing.A[0]*s),int((drawing.CENTER_Y-drawing.SCREEN_HALF)*s)
    right,bottom=int(drawing.B[0]*s),int((drawing.CENTER_Y+drawing.SCREEN_HALF)*s)+1
    xx=np.arange(left,right+1,dtype=float)[None,:]/s
    yy=np.arange(top,bottom,dtype=float)[:,None]/s
    spread=np.where(xx<=drawing.SCREEN_X,
                    (xx-drawing.A[0])/(drawing.SCREEN_X-drawing.A[0]),
                    (drawing.B[0]-xx)/(drawing.B[0]-drawing.SCREEN_X))
    crossing_y=-(yy-drawing.CENTER_Y)/np.maximum(spread,1e-12)*HALF_EXTENT/drawing.SCREEN_HALF
    valid=(np.abs(crossing_y)<=HALF_EXTENT)&(spread>0)
    # Select the actual nearest sampled path so both panes share one table.
    indices=np.clip(np.rint((HALF_EXTENT-crossing_y)/physical.DY-.5),0,N-1).astype(int)
    indices=np.where(valid,indices,-1)
    colors=COLORS[np.maximum(indices,0)].astype(float)
    paper=np.asarray(PANEL,dtype=float)
    faint=np.rint(.13*colors+.87*paper).astype(np.uint8)
    painted=np.rint(.62*colors+.38*paper).astype(np.uint8)
    faint[~valid]=paper.astype(np.uint8)
    painted[~valid]=paper.astype(np.uint8)
    return (left,top),indices,Image.fromarray(faint),Image.fromarray(painted)


@lru_cache(None)
def background(stage):
    image=Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,23),"Same path · same color",31,bold=True)
    text(d,(39,67),"Point source A · fixed observation point B · one screen",19,MUTED)
    ratio=round(WAVELENGTHS[0]/WAVELENGTHS[stage])
    label="λ = λ₀" if ratio==1 else f"λ = λ₀ / {ratio}"
    text(d,(1400,23),label,31,bold=True,anchor="ra")
    text(d,(1400,69),f"{stage+1} / 3",18,MUTED,anchor="ra")
    for box in ((30,111,1410,475),(30,494,1410,1021)):
        d.rounded_rectangle(pixels(box),radius=14*SUPERSAMPLE,fill=PANEL,
                            outline=BORDER,width=SUPERSAMPLE)
    text(d,(53,129),"Path diamond",23,bold=True)
    text(d,(1387,134),"20,001 fixed paths",19,MUTED,anchor="ra")
    origin,_,faint,_=fan()
    image.paste(faint,origin)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(1053,438),"edge",15,RGB[0],anchor="ra")
    for column in range(230):
        color=tuple(int(c) for c in color_at(HALF_EXTENT*(1-column/229)))
        line(d,(1065+column,442),(1065+column,451),color,1)
    text(d,(1307,438),"center",15,RGB[N//2])
    text(d,(53,512),"Tip to tail",23,bold=True)
    text(d,(1387,517),"Gold: sum so far",18,GOLD,anchor="ra")
    text(d,(53,551),"Each segment has the color of its path above",18,MUTED)
    drawing.dash(d,(101,ORIGIN[1]),(1300,ORIGIN[1]),AXIS,.8,3,5)
    text(d,(1312,ORIGIN[1]-10),"Re",14,MUTED)
    x,y=physical.point(1+0j)
    d.ellipse(pixels((x-5,y-5,x+5,y+5)),outline=(*MUTED,180),width=SUPERSAMPLE)
    text(d,(53,992),"Reference: unobstructed A → B = 1",16,MUTED)
    text(d,(1387,992),"Same colors · same phase reference · same scale",16,MUTED,anchor="ra")
    x0,x1,bar_y=1210,1210+.2*SCALE,966
    line(d,(x0,bar_y),(x1,bar_y),MUTED,1)
    for x in (x0,x1):
        line(d,(x,bar_y-4),(x,bar_y+4),MUTED,1)
    text(d,((x0+x1)/2,bar_y+9),"0.2",14,MUTED,anchor="ma")
    text(d,(39,1041),"Scalar propagation · 20,001 individual path contributions",17,MUTED)
    text(d,(1400,1041),"λ₀ = 0.5 · A–screen = screen–B = 4.5",17,MUTED,anchor="ra")
    return image


def frame(index):
    stage,count=drawing.state(index)
    image=background(stage).copy()
    if count:
        origin,indices,_,painted=fan()
        mask=Image.fromarray(((indices>=0)&(indices<count)).astype(np.uint8)*255)
        image.paste(painted,origin,mask)
    d=ImageDraw.Draw(image,"RGBA")
    # Dotted sampling screen and its fixed spectrum. The colors encode only y.
    for yy in np.arange(drawing.CENTER_Y-drawing.SCREEN_HALF,
                         drawing.CENTER_Y+drawing.SCREEN_HALF+.1,3.8):
        physical_y=(drawing.CENTER_Y-yy)*HALF_EXTENT/drawing.SCREEN_HALF
        drawing.dot(d,(drawing.SCREEN_X,float(yy)),tuple(int(c) for c in color_at(physical_y)),1.4)
    for first,last in ((drawing.CENTER_Y-drawing.SCREEN_HALF-12,drawing.CENTER_Y-drawing.SCREEN_HALF-3),
                       (drawing.CENTER_Y+drawing.SCREEN_HALF+3,drawing.CENTER_Y+drawing.SCREEN_HALF+12)):
        line(d,(drawing.SCREEN_X,first),(drawing.SCREEN_X,last),INK,3)
    drawing.dash(d,drawing.A,drawing.B,(*MUTED,100),.75,4,6)
    if 0<count<N:
        current=drawing.crossing(Y[count-1])
        line(d,drawing.A,current,RGB[count-1],2.4)
        line(d,current,drawing.B,RGB[count-1],2.4)
        drawing.dot(d,current,RGB[count-1],4.5)
    for xy,label in ((drawing.A,"A"),(drawing.B,"B")):
        drawing.dot(d,xy,INK,5.8)
        text(d,(xy[0],xy[1]+17),label,20,INK,bold=True,anchor="ma")
    text(d,(drawing.SCREEN_X,440),"screen",16,MUTED,anchor="ma")
    text(d,(54,441),f"Added {count:,} / {N:,}",17,RGB[count-1] if count else MUTED)
    _,_,_,coords,raster=physical.model(stage)
    if count:
        for first,last in zip(COLOR_CUTS[:-1],COLOR_CUTS[1:]):
            if first>=count:
                break
            end=min(int(last),count)
            d.line(raster[int(first):end+1],fill=RGB[int(first)],width=round(2.3*SUPERSAMPLE))
    drawing.dot(d,ORIGIN,MUTED,2.7)
    if count:
        arrow(d,ORIGIN,coords[count],GOLD,width=2.5,head=8)
        # A colored ring ties the active physical route to this exact subtotal.
        if count<N:
            x,y=coords[count]
            d.ellipse(pixels((x-6.5,y-6.5,x+6.5,y+6.5)),
                      outline=RGB[count-1],width=round(1.5*SUPERSAMPLE))
        drawing.dot(d,coords[count],GOLD,3.1)
    return image.reduce(SUPERSAMPLE)


def configure_renderer():
    drawing.NAME=NAME
    drawing.frame=frame


def checks():
    assert np.array_equal(COLORS,COLORS[::-1])
    assert np.array_equal(COLORS[N//2],PALETTE[-1])
    assert np.array_equal(color_at([-HALF_EXTENT,HALF_EXTENT]),np.repeat(PALETTE[:1],2,axis=0))
    coverage=np.zeros(N,dtype=int)
    for a,b in zip(COLOR_CUTS[:-1],COLOR_CUTS[1:]):
        coverage[a:b]+=1
        assert np.all(COLORS[a:b]==COLORS[a])
    assert np.all(coverage==1)
    # Raster family: reconstruct screen crossings at several interior columns.
    origin,indices,_,_=fan()
    mapping_errors=[]
    for path in (1000,5000,9000,10000,11000,15000,19000):
        screen_xy=drawing.crossing(Y[path])
        for fraction in (.4,.75,1.):
            x=drawing.A[0]+fraction*(screen_xy[0]-drawing.A[0])
            y=drawing.A[1]+fraction*(screen_xy[1]-drawing.A[1])
            xi,yi=round(x*SUPERSAMPLE)-origin[0],round(y*SUPERSAMPLE)-origin[1]
            chosen=int(indices[yi,xi])
            assert chosen>=0
            # Pixel resolution mixes neighboring, unresolved physical paths.
            err=float(max(abs(COLORS[chosen].astype(int)-COLORS[path].astype(int))))
            assert err<=5
            mapping_errors.append(err)
    reports=[]
    for stage,wavelength in enumerate(WAVELENGTHS):
        _,vectors,vertices,coords,_=physical.model(stage)
        assert max(abs(np.diff(vertices)-vectors))<3e-16
        for fraction in (0,.25,.49,.5,.51,.75,1):
            index=drawing.frame_for_count(stage,round(N*fraction))
            actual_stage,count=drawing.state(index)
            assert actual_stage==stage
            assert np.allclose(coords[count],physical.point(vertices[count]),atol=0,rtol=0)
            if count:
                assert RGB[count-1]==tuple(int(c) for c in color_at(Y[count-1]))
        reports.append({"wavelength":wavelength,"endpoint":[vertices[-1].real,vertices[-1].imag],
                        "vectors_sha256":hashlib.sha256(vectors.tobytes()).hexdigest()})
    report={"model":"unchanged normalized scalar propagation, no grouping",
            "path_count":N,"path_positions_sha256":hashlib.sha256(Y.tobytes()).hexdigest(),
            "color_mapping":"linear palette coordinate 1 - abs(y)/2.8, independent of wavelength",
            "palette_edge_to_center":PALETTE.astype(int).tolist(),
            "path_colors_sha256":hashlib.sha256(COLORS.tobytes()).hexdigest(),
            "all_original_segments_retained":True,"color_run_count":len(COLOR_CUTS)-1,
            "maximum_fan_pixel_color_discretization_error":max(mapping_errors),
            "current_path_index":"count - 1","current_segment":"vertices[count-1] to vertices[count]",
            "gold_sum":"vertices[count]", "scale":SCALE,
            "timing":"unchanged: 0.8s prelude, 9.6s scan, 1.6s hold per wavelength",
            "fps":FPS,"frames":drawing.TOTAL_FRAMES,"duration_seconds":drawing.DURATION,
            "stages":reports}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def previews():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,1368),BG)
    for stage in range(3):
        for column,fraction in enumerate((.25,.49,.51,1.)):
            still=frame(drawing.frame_for_count(stage,round(N*fraction)))
            if fraction==1:
                still.save(OUT/f"{NAME}-lambda-{stage+1}.png")
            sheet.paste(still.resize((360,270),Image.Resampling.LANCZOS),(column*360,stage*456))
            crop=still.crop((85,580,1355,965)).resize((360,109),Image.Resampling.LANCZOS)
            sheet.paste(crop,(column*360,stage*456+273))
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def encoded_checks():
    wanted={drawing.frame_for_count(stage,round(N*fraction)) for stage in range(3)
            for fraction in (0,.25,.49,.5,.51,.75,1)}|{drawing.TOTAL_FRAMES-1}
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata=next(reader)
    assert tuple(metadata["size"])==(WIDTH,HEIGHT) and abs(metadata["fps"]-FPS)<1e-8
    checked,selected,decoded_count=[],{},0
    for index,raw in enumerate(reader):
        decoded_count+=1
        if index not in wanted:
            continue
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        expected=np.asarray(frame(index))
        mae=float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
        assert mae<2.5
        stage,count=drawing.state(index)
        if 0<count<N:
            xy=drawing.crossing(Y[count-1])
            x,y=map(round,xy)
            crop=decoded[y-4:y+5,x-4:x+5].astype(float)
            matching=int(np.sum(np.linalg.norm(crop-np.asarray(RGB[count-1]),axis=2)<70))
            assert matching>8
        else:
            matching=None
        if count:
            x,y=map(round,physical.model(stage)[3][count])
            crop=decoded[y-5:y+6,x-5:x+6].astype(float)
            gold_pixels=int(np.sum(np.linalg.norm(crop-np.asarray(GOLD),axis=2)<65))
            assert gold_pixels>8
        else:
            gold_pixels=None
        checked.append({"frame":index,"count":count,"mean_absolute_rgb_error":mae,
                        "matching_active_path_pixels":matching,"gold_tip_pixels":gold_pixels})
        if count==N:
            selected[stage]=Image.fromarray(decoded.copy())
    assert decoded_count==drawing.TOTAL_FRAMES and len(selected)==3
    sheet=Image.new("RGB",(1440,1080),BG)
    for stage in range(3):
        sheet.paste(selected[stage].resize((480,360),Image.Resampling.LANCZOS),(stage*480,0))
        crop=selected[stage].crop((30,565,1410,970)).resize((768,225),Image.Resampling.LANCZOS)
        sheet.paste(crop,(336,370+stage*230))
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":decoded_count,"duration_seconds":decoded_count/FPS,
            "resolution":metadata["size"],"fps":metadata["fps"],"checks":checked}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_frames":decoded_count,"checked":len(checked),
                      "max_rgb_error":max(c["mean_absolute_rgb_error"] for c in checked)}),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args=parser.parse_args()
    configure_renderer()
    if args.check: checks()
    if args.preview: previews()
    if args.render: drawing.render()
    if args.encoded_check: encoded_checks()
