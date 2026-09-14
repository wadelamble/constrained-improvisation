"""A finite 49-opening, 49-path, 49-vector wavelength comparison.

Display units are normalized equal-weight phasor units. This is not a
continuous-aperture Fresnel integral or an absolute propagator amplitude.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
import subprocess
import time

from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow,
)

NAME = "symmetry-49-aperture-wavelength-scan"
WIDTH, HEIGHT, FPS = 1440, 960, 60
N, HALF_EXTENT, DISTANCE = 49, 2.8, 4.5
CENTERS = np.linspace(-HALF_EXTENT, HALF_EXTENT, N)
POSITIONS = CENTERS / HALF_EXTENT
WEIGHTS = np.full(N, 1.0/N)
PITCH = 2*HALF_EXTENT/(N-1)
OPENING_WIDTH = 0.60*PITCH
OPENING_BOUNDS = np.column_stack((CENTERS-OPENING_WIDTH/2, CENTERS+OPENING_WIDTH/2))
PATH_LENGTHS = np.sqrt(DISTANCE**2+CENTERS**2)
# Rationalization avoids subtracting nearly equal lengths near the axis.
EXCESS_LENGTHS = CENTERS**2/(PATH_LENGTHS+DISTANCE)
F_NUMBERS = (0.25, 1.0, 4.0)
WAVELENGTHS = tuple(HALF_EXTENT**2/(f*DISTANCE) for f in F_NUMBERS)
for values in (CENTERS, POSITIONS, WEIGHTS, OPENING_BOUNDS, PATH_LENGTHS, EXCESS_LENGTHS):
    values.setflags(write=False)
SETTLE_FRAMES, FRAMES_PER_PATH, HOLD_FRAMES = 60, 12, 60
SCAN_FRAMES = N*FRAMES_PER_PATH
PASS_FRAMES = SETTLE_FRAMES+SCAN_FRAMES+HOLD_FRAMES
TOTAL_FRAMES = 3*PASS_FRAMES
DURATION = TOTAL_FRAMES/FPS
SCALE, ORIGIN = 700.0, (390.0, 850.0)
SCREEN_X, SCREEN_HALF, SCREEN_Y = 720.0, 455.0, 190.0
OBSERVER = (SCREEN_X, 346.0)


def state(frame_index):
    frame_index = min(max(int(frame_index),0),TOTAL_FRAMES-1)
    stage,local = divmod(frame_index,PASS_FRAMES)
    count = 0 if local < SETTLE_FRAMES else min(N,1+(local-SETTLE_FRAMES)//FRAMES_PER_PATH)
    return stage,count


def point(value):
    return (ORIGIN[0]+SCALE*value.real,ORIGIN[1]-SCALE*value.imag)


def dot(draw,xy,color,radius):
    x,y = xy
    draw.ellipse(pixels((x-radius,y-radius,x+radius,y+radius)),fill=color)


def dashed(draw,first,last,color,width=1.1,dash=6,gap=6):
    delta = np.asarray(last,dtype=float)-first
    length = float(np.linalg.norm(delta))
    unit = delta/length
    for begin in np.arange(0,length,dash+gap):
        line(draw,np.asarray(first)+begin*unit,
             np.asarray(first)+min(begin+dash,length)*unit,color,width)


@lru_cache(None)
def model(stage):
    phases = (2*np.pi/WAVELENGTHS[stage])*EXCESS_LENGTHS
    vectors = WEIGHTS*np.exp(1j*phases)
    vertices = np.r_[0j,np.cumsum(vectors)]
    return phases,vectors,vertices,tuple(point(value) for value in vertices)


@lru_cache(None)
def background(stage):
    image = Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d = ImageDraw.Draw(image,"RGBA")
    text(d,(37,24),"49 openings, 49 paths, 49 arrows",31,bold=True)
    text(d,(39,70),"Same geometry · same path weights · only wavelength changes",19,MUTED)
    ratio = round(WAVELENGTHS[0]/WAVELENGTHS[stage])
    wavelength = "λ = λ₀" if ratio == 1 else f"λ = λ₀ / {ratio}"
    text(d,(1401,24),wavelength,29,INK,bold=True,anchor="ra")
    text(d,(1400,70),f"Pass {stage+1} of 3",18,MUTED,anchor="ra")
    for box in ((30,115,1410,382),(30,401,1410,906)):
        d.rounded_rectangle(pixels(box),radius=14*SUPERSAMPLE,
                            fill=PANEL,outline=BORDER,width=SUPERSAMPLE)
    text(d,(51,129),"One screen · 49 distinct openings",22,bold=True)
    text(d,(1387,133),"Uniform plane-wave illumination",17,MUTED,anchor="ra")

    # The 49 physical openings and all 48 intervening opaque bars are literal.
    # Each opening supplies one center path; its width is not subdivided.
    line(d,(155,SCREEN_Y),(1285,SCREEN_Y),MUTED,8)
    for lower,upper in OPENING_BOUNDS:
        x0 = SCREEN_X+SCREEN_HALF*lower/HALF_EXTENT
        x1 = SCREEN_X+SCREEN_HALF*upper/HALF_EXTENT
        d.rectangle(pixels((x0,SCREEN_Y-5,x1,SCREEN_Y+5)),fill=PANEL)
        line(d,(x0,SCREEN_Y-5),(x0,SCREEN_Y+5),MUTED,0.7)
        line(d,(x1,SCREEN_Y-5),(x1,SCREEN_Y+5),MUTED,0.7)
    for source in POSITIONS:
        xy = (SCREEN_X+SCREEN_HALF*source,SCREEN_Y)
        line(d,xy,OBSERVER,(*MUTED,43),0.6)
        dot(d,xy,(*MUTED,150),1.3)
    for x,label in ((SCREEN_X-SCREEN_HALF,"−a"),(SCREEN_X+SCREEN_HALF,"+a")):
        text(d,(x,SCREEN_Y+17),label,17,MUTED,anchor="ma")
    dashed(d,(SCREEN_X,SCREEN_Y+18),OBSERVER,(*MUTED,160))
    line(d,(SCREEN_X+9,287),(1058,287),BORDER,0.8)
    text(d,(1075,276),"Central path",17,MUTED)
    text(d,(SCREEN_X+19,OBSERVER[1]-10),"B",20,INK)
    text(d,(1385,353),"Geometry schematic",14,MUTED,anchor="ra")
    dot(d,OBSERVER,INK,4)

    text(d,(52,417),"Tip to tail · normalized phasor units",22,bold=True)
    text(d,(1095,421),"blue: one arrow per path",17,BLUE,anchor="ra")
    text(d,(1387,421),"gold: sum so far",17,GOLD,anchor="ra")
    text(d,(1387,452),"Phase relative to the straight path",16,MUTED,anchor="ra")
    line(d,(143,ORIGIN[1]),(1295,ORIGIN[1]),AXIS,0.8)
    text(d,(1308,ORIGIN[1]-9),"Re",14,MUTED)
    for x in (1200,1340):
        line(d,(x,812),(x,820),MUTED,1)
    line(d,(1200,816),(1340,816),MUTED,1)
    text(d,(1270,823),"0.2",13,MUTED,anchor="ma")
    text(d,(1386,875),"Same phasor scale in every pass",16,MUTED,anchor="ra")
    text(d,(38,925),"|vⱼ| = 1/49    ·    φⱼ = (2π/λ)(Lⱼ − z)",16,MUTED)
    text(d,(1400,925),"Finite 49-path sum · scan = addition order",16,MUTED,anchor="ra")
    return image


def draw_polygon(draw,stage,count):
    _,vectors,vertices,coordinates = model(stage)
    if count:
        arrow(draw,ORIGIN,coordinates[count],GOLD,width=2.8,head=9)
    drawn = 0
    for j in range(count):
        active = j == count-1
        arrow(draw,coordinates[j],coordinates[j+1],BLUE,
              width=2.6 if active else 1.55,head=4.8 if active else 3.5)
        drawn += 1
    dot(draw,ORIGIN,MUTED,2.6)
    if count:
        x,y = coordinates[count]
        draw.ellipse(pixels((x-7,y-7,x+7,y+7)),outline=(*BLUE,125),width=SUPERSAMPLE)
    return drawn


def frame(frame_index):
    stage,count = state(frame_index)
    image = background(stage).copy()
    d = ImageDraw.Draw(image,"RGBA")
    for source in POSITIONS[:count]:
        dot(d,(SCREEN_X+SCREEN_HALF*source,SCREEN_Y),BLUE,1.6)
    if count:
        source = POSITIONS[count-1]
        xy = (SCREEN_X+SCREEN_HALF*source,SCREEN_Y)
        line(d,xy,OBSERVER,BLUE,2.3)
        dot(d,xy,(*BLUE,28),8)
        dot(d,xy,BLUE,3.9)
        dot(d,OBSERVER,INK,4)
        text(d,(53,322),f"Opening {count} / {N}",21,BLUE)
        text(d,(53,352),f"y / a = {source:+.3f}",16,MUTED)
        text(d,(52,451),f"Added {count} / {N}   ·   current arrow: {count}",16,BLUE)
    else:
        text(d,(53,322),"49 fixed paths",20,BLUE)
        text(d,(53,352),"One through each opening",16,MUTED)
        text(d,(52,451),f"Added 0 / {N}",16,BLUE)
    assert draw_polygon(d,stage,count) == count
    return image.reduce(SUPERSAMPLE)


def checks():
    assert len(CENTERS) == len(WEIGHTS) == len(OPENING_BOUNDS) == N == 49
    assert CENTERS[N//2] == 0.0
    assert np.all(OPENING_BOUNDS[1:,0] > OPENING_BOUNDS[:-1,1])
    assert np.allclose(np.diff(CENTERS),PITCH,rtol=0,atol=8e-16)
    assert np.all(WEIGHTS == 1/N)
    assert abs(float(WEIGHTS.sum())-1) < 1e-15
    identity = hashlib.sha256(CENTERS.tobytes()+WEIGHTS.tobytes()).hexdigest()
    data = []
    for stage,f_number in enumerate(F_NUMBERS):
        phases,vectors,vertices,coordinates = model(stage)
        scalar_vectors = [complex(math.cos(2*math.pi/WAVELENGTHS[stage]*(math.hypot(DISTANCE,float(y))-DISTANCE)),
                                  math.sin(2*math.pi/WAVELENGTHS[stage]*(math.hypot(DISTANCE,float(y))-DISTANCE)))/N
                          for y in CENTERS]
        independent = [sum(scalar_vectors[:j]) for j in range(N+1)]
        error = float(np.max(np.abs(vertices-independent)))
        assert error < 1e-13
        assert len(vectors) == N and len(vertices) == N+1
        assert np.max(np.abs(np.diff(vertices)-vectors)) < 2e-16
        assert np.max(np.abs(np.abs(vectors)-1/N)) < 1e-17
        assert np.max(np.abs(vectors-vectors[::-1])) < 4e-16
        assert phases[N//2] == 0 and vectors[N//2] == complex(1/N)
        phase_step = float(np.max(np.abs(np.diff(phases))))
        assert phase_step < math.pi/3
        screen = np.asarray(coordinates)
        assert screen[:,0].min() > 330 and screen[:,0].max() < 1055
        assert screen[:,1].min() > 481 and screen[:,1].max() < 892
        start = stage*PASS_FRAMES+SETTLE_FRAMES
        counts = [state(start+i)[1] for i in range(SCAN_FRAMES)]
        assert counts == np.repeat(np.arange(1,N+1),FRAMES_PER_PATH).tolist()
        assert state(stage*PASS_FRAMES)[1] == 0
        assert state((stage+1)*PASS_FRAMES-1)[1] == N
        image = Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
        assert draw_polygon(ImageDraw.Draw(image,"RGBA"),stage,N) == N
        endpoint = complex(vertices[-1])
        data.append({"F_parameter":f_number,"wavelength":WAVELENGTHS[stage],
                     "wavelength_ratio":WAVELENGTHS[stage]/WAVELENGTHS[0],
                     "opening_count":N,"candidate_path_count":N,"blue_vector_count":N,
                     "positions_weights_sha256":identity,"arrow_length_pixels":SCALE/N,
                     "scan_start_seconds":start/FPS,"scan_end_seconds":(start+SCAN_FRAMES)/FPS,
                     "endpoint":[endpoint.real,endpoint.imag],"endpoint_magnitude":abs(endpoint),
                     "max_adjacent_phase_difference_radians":phase_step,
                     "independent_scalar_sum_max_error":error,
                     "screen_vertex_bounds":[screen.min(axis=0).tolist(),screen.max(axis=0).tolist()]})
    report = {"model":"finite equal-weight 49-path normalized phasor sum",
              "amplitude_convention":"each path has fixed weight 1/49; all-in-phase total equals 1",
              "absolute_propagator_amplitude":False,"continuum_quadrature":False,
              "phase_reference":"central path exp(ikz)","exact_geometric_path_lengths":True,
              "centers":CENTERS.tolist(),"weights":WEIGHTS.tolist(),
              "opening_width":OPENING_WIDTH,"opening_bounds":OPENING_BOUNDS.tolist(),
              "screen_to_observer_distance":DISTANCE,"display_geometry_schematic":True,
              "stages":data,"frames_per_path":FRAMES_PER_PATH,
              "scan_seconds_per_pass":SCAN_FRAMES/FPS,"hold_seconds_per_pass":HOLD_FRAMES/FPS,
              "settle_seconds_per_pass":SETTLE_FRAMES/FPS,"duration_seconds":DURATION,
              "total_frames":TOTAL_FRAMES,"fps":FPS,"resolution":[WIDTH,HEIGHT],
              "same_scale_pixels_per_unit":SCALE,"hidden_endpoint_rotation_or_normalization":False,
              "grouping_or_omission":False,"analytic_curve_or_decorative_heads":False,
              "arbitrary_short_wavelength_stationary_dominance_claim":False}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"duration":DURATION,"stages":data}),flush=True)


def selected_frame(stage,count):
    return stage*PASS_FRAMES+(SETTLE_FRAMES//2 if count == 0 else SETTLE_FRAMES+(count-1)*FRAMES_PER_PATH+5)


def previews():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet = Image.new("RGB",(1440,792),BG)
    d = ImageDraw.Draw(sheet)
    for stage in range(3):
        for column,count in enumerate((16,25,34,N)):
            rendered = frame(selected_frame(stage,count))
            rendered.save(OUT/f"{NAME}-pass-{stage+1}-path-{count}.png")
            x,y = column*360,stage*264
            sheet.paste(rendered.resize((360,240),Image.Resampling.LANCZOS),(x,y))
            d.text((x+9,y+244),f"Pass {stage+1}    path {count}/{N}",fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(0).save(OUT/f"{NAME}-initial.png")
    frame(TOTAL_FRAMES-1).save(OUT/f"{NAME}-final.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    output = OUT/f"{NAME}.mp4"
    OUT.mkdir(parents=True,exist_ok=True)
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
               "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
               "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast",
               "-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start = time.perf_counter()
    last_state,last_rgb = None,None
    try:
        for index in range(TOTAL_FRAMES):
            current = state(index)
            if current != last_state:
                last_rgb = frame(index).tobytes()
                last_state = current
            process.stdin.write(last_rgb)
            if index % (FPS*3) == 0:
                print(f"{index/FPS:g}/{DURATION:g} s; elapsed {time.perf_counter()-start:.1f} s",flush=True)
        process.stdin.close()
        error = process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    print(json.dumps({"video":str(output),"bytes":output.stat().st_size}),flush=True)


def encoded_checks():
    wanted = sorted({selected_frame(stage,count) for stage in range(3)
                     for count in (0,1,16,24,25,26,34,N)}|{TOTAL_FRAMES-1})
    reader = imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata = next(reader)
    assert tuple(metadata["size"]) == (WIDTH,HEIGHT)
    assert abs(metadata["fps"]-FPS) < 1e-8
    checked,decoded_selected,decoded_count = [],{},0
    for index,raw in enumerate(reader):
        decoded_count += 1
        if index not in wanted:
            continue
        decoded = np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        reference = np.asarray(frame(index))
        mae = float(np.mean(np.abs(decoded.astype(float)-reference.astype(float))))
        assert mae < 2.5,(index,mae)
        stage,added = state(index)
        blue_pixels = None
        if added:
            x = round(SCREEN_X+SCREEN_HALF*POSITIONS[added-1]); y = round(SCREEN_Y)
            crop = decoded[y-4:y+5,x-4:x+5].astype(float)
            blue_pixels = int(np.sum(np.linalg.norm(crop-np.asarray(BLUE),axis=2)<55))
            assert blue_pixels > 15,(index,blue_pixels)
        checked.append({"frame":index,"stage":stage+1,"added_vectors":added,
                        "mean_absolute_rgb_error":mae,"active_opening_blue_pixels":blue_pixels})
        if added in (16,25,N):
            decoded_selected[(stage,added)] = Image.fromarray(decoded.copy())
        if index == TOTAL_FRAMES-1:
            Image.fromarray(decoded.copy()).save(OUT/f"{NAME}-encoded-final.png")
    assert decoded_count == TOTAL_FRAMES
    sheet = Image.new("RGB",(1440,1032),BG)
    d = ImageDraw.Draw(sheet)
    for stage in range(3):
        for column,added in enumerate((16,25,N)):
            x,y = column*480,stage*344
            sheet.paste(decoded_selected[(stage,added)].resize((480,320),Image.Resampling.LANCZOS),(x,y))
            d.text((x+9,y+324),f"Encoded: pass {stage+1}, path {added}/{N}",fill=INK)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report = {"decoded_frames":decoded_count,"duration_seconds":decoded_count/FPS,
              "fps":metadata["fps"],"resolution":metadata["size"],"representative_checks":checked,
              "max_frame_mean_absolute_rgb_error":max(item["mean_absolute_rgb_error"] for item in checked)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args = parser.parse_args()
    if args.check:
        checks()
    if args.preview:
        previews()
    if args.render:
        render()
    if args.encoded_check:
        encoded_checks()
