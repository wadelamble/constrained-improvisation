"""A visual refresh of the two introductory wave-propagation examples.

The original radial and two-point-source models are retained. Both panes show
real parts, not intensity. Positive, position-dependent display gains preserve
phase and cancellation while keeping distant fronts visible; the footer labels
this contrast enhancement. These are illustrative fields, not a quantitative
finite-aperture boundary-value solution.

Four full wave cycles play continuously over six seconds. Geometry, wavelength,
source phase relation, and camera stay fixed. Headers live outside the fields.
The older generator, movie, and manuscript insertion remain untouched.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

import generate_symmetry_packet_phase_modes as art

np, Image, ImageDraw = art.np, art.Image, art.ImageDraw
ROOT, OUT = art.ROOT, art.OUT
NAME = "symmetry-rays-and-double-slit-refined"
WIDTH, HEIGHT, SS = 1440, 760, art.SS
FPS, DURATION, CYCLES = 30, 6., 4
FRAMES = round(FPS * DURATION)
CYCLE_FRAMES = FRAMES // CYCLES
BG, INK, MUTED = art.BG, art.INK, art.MUTED
BORDER = (219, 214, 205)
BLUE, RUST = (82, 134, 168), (194, 131, 102)
GOLD = (148, 93, 30)
SOURCE = (87, 75, 60)
PLOT_X = (36, 744)
PLOT_Y, PLOT_W, PLOT_H = 124, 660, 495
XMIN, XMAX, YMIN, YMAX = -4., 4., -3., 3.
SOURCE_X, BARRIER_X = -.75, -.82
SLIT_Y, HALF_GAP = (-.72, .72), .18
SAMPLE_FRAMES = (0, 7, 15, 22, 30, 38)
LABEL_BOXES = []


def field_coefficients(x, y):
    """Complex fields before the common exp(-i*phase) time factor."""
    radius = np.hypot(x - SOURCE_X, y)
    radial = ((1 - np.exp(-(radius / .22) ** 2)) / np.sqrt(.45 + radius)
              * np.exp(2j * np.pi * radius / .62) / 1.15)
    k = 2 * np.pi / .58
    incident = .82 * np.exp(1j * k * (x - BARRIER_X))
    transmitted = np.zeros_like(x + y, dtype=complex)
    available = np.zeros_like(x + y, dtype=float)
    for center in SLIT_Y:
        radius = np.hypot(x - BARRIER_X, y - center)
        attenuation = .78 / np.sqrt(radius + .34)
        transmitted += attenuation * np.exp(1j * k * radius)
        available += attenuation
    double_slit = np.where(x <= BARRIER_X, incident,
                           transmitted / np.maximum(available, 1e-9))
    return radial, double_slit


@lru_cache(None)
def grid_fields():
    x = np.linspace(XMIN, XMAX, PLOT_W * SS)[None, :]
    y = np.linspace(YMAX, YMIN, PLOT_H * SS)[:, None]
    return field_coefficients(x, y)


@lru_cache(None)
def palette():
    v = np.linspace(-1, 1, 4097)
    target = np.where(v[:, None] < 0, BLUE, RUST)
    colors = np.asarray(BG) + np.abs(v[:, None]) * (target - np.asarray(BG))
    return np.rint(colors).astype(np.uint8)


def colored_field(values):
    indices = np.rint((np.clip(values, -1, 1) + 1) * 2048).astype(np.int32)
    return Image.fromarray(palette()[indices])


def project(pane, x, y):
    return (PLOT_X[pane] + (x-XMIN)/(XMAX-XMIN)*PLOT_W,
            PLOT_Y + (YMAX-y)/(YMAX-YMIN)*PLOT_H)


def label(draw, position, value, size=20, color=MUTED, bold=False, anchor=None):
    art.text(draw, position, value, size, color, bold, anchor)
    box = draw.textbbox(art.px(position), value, font=art.font(size,bold), anchor=anchor)
    LABEL_BOXES.append((value, tuple(q/SS for q in box)))


def dot(draw, pane, x, y, radius):
    u,v = project(pane,x,y)
    draw.ellipse(art.px((u-radius,v-radius,u+radius,v+radius)),
                 fill=SOURCE, outline=BG, width=round(1.4*SS))


def ray(draw, pane, start, end):
    a,b = project(pane,*start),project(pane,*end)
    # A narrow cream edge keeps the arrow legible over both signs of the field.
    art.line(draw,a,b,BG,3.7)
    art.arrow(draw,a,b,GOLD,2.0,8.)


@lru_cache(None)
def fixed_overlay():
    layer = Image.new("RGBA", (WIDTH*SS,HEIGHT*SS), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    LABEL_BOXES.clear()
    label(d,(36,33),"Rays and wavefronts",30,INK,True)
    label(d,(36,79),"Rays are perpendicular to the wavefronts.",21)
    label(d,(744,33),"Diffraction and interference",30,INK,True)
    label(d,(744,79),"Spreading waves reinforce and cancel.",21)
    for pane in (0,1):
        d.rectangle(art.px((PLOT_X[pane],PLOT_Y,
                           PLOT_X[pane]+PLOT_W,PLOT_Y+PLOT_H)),
                    outline=BORDER,width=SS)

    for angle in np.arange(8)*math.pi/4:
        dx,dy = math.cos(angle),math.sin(angle)
        distances = [3.3]
        if abs(dx)>1e-9:
            distances.append(((XMAX-.26 if dx>0 else XMIN+.26)-SOURCE_X)/dx)
        if abs(dy)>1e-9:
            distances.append((YMAX-.26 if dy>0 else YMIN+.26)/dy)
        length = min(distances)
        ray(d,0,(SOURCE_X+.52*dx,.52*dy),
            (SOURCE_X+length*dx,length*dy))
    dot(d,0,SOURCE_X,0,4.8)

    for y in (-1.65,-.55,.55,1.65):
        ray(d,1,(-3.6,y),(BARRIER_X-.24,y))
    segments = ((YMIN,SLIT_Y[0]-HALF_GAP),
                (SLIT_Y[0]+HALF_GAP,SLIT_Y[1]-HALF_GAP),
                (SLIT_Y[1]+HALF_GAP,YMAX))
    for y0,y1 in segments:
        art.line(d,project(1,BARRIER_X,y0),project(1,BARRIER_X,y1),INK,6.)
    for y in SLIT_Y:
        dot(d,1,BARRIER_X,y,3.8)

    label(d,(36,660),"Real part of the wave",21,INK)
    bar = Image.fromarray(palette()[None,:,:]).resize((204*SS,14*SS))
    layer.paste(bar,art.px((266,666)))
    for x,value in ((266,"−"),(368,"0"),(470,"+")):
        label(d,(x,685),value,18,MUTED,anchor="mt")
    art.arrow(d,(565,675),(602,675),GOLD,2,8)
    label(d,(616,660),"Ray direction",21,INK)
    label(d,(1404,662),"Contrast enhanced to keep wavefronts visible.",18,
          MUTED,anchor="ra")
    return layer


def frame(index):
    phase = 2*math.pi*(index % CYCLE_FRAMES)/CYCLE_FRAMES
    rotation = np.exp(-1j*phase)
    picture = Image.new("RGB",(WIDTH*SS,HEIGHT*SS),BG)
    for pane,z in enumerate(grid_fields()):
        field = z.real*rotation.real-z.imag*rotation.imag
        picture.paste(colored_field(field),art.px((PLOT_X[pane],PLOT_Y)))
    overlay = fixed_overlay()
    picture.paste(overlay,(0,0),overlay)
    return picture.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def validate():
    import generate_symmetry_rays_diffraction_animation as original
    x,y = np.meshgrid(np.linspace(-3.9,3.9,171),np.linspace(-2.9,2.9,131))
    a,b = field_coefficients(x,y)
    errors = []
    for phase in (0.,.43,2.4,5.7):
        rotation = np.exp(-1j*phase)
        expected_a,_ = original.radial_field(x,y,phase)
        expected_b = original.slit_field(x,y,phase)
        errors.extend((float(np.max(abs((a*rotation).real-expected_a/1.15))),
                       float(np.max(abs((b*rotation).real-expected_b)))))
    assert max(errors)<1e-12
    assert FRAMES % CYCLES == 0
    fixed_overlay()
    overlaps=[]
    for i,(name,(x0,y0,x1,y1)) in enumerate(LABEL_BOXES):
        assert 0<=x0<x1<=WIDTH and 0<=y0<y1<=HEIGHT, name
        for other,(a0,b0,a1,b1) in LABEL_BOXES[i+1:]:
            if min(x1,a1)>max(x0,a0) and min(y1,b1)>max(y0,b0):
                overlaps.append((name,other))
    assert not overlaps, overlaps
    report = {"original_field_max_error":max(errors),"duration":DURATION,
              "cycles":CYCLES,"frames_per_cycle":CYCLE_FRAMES,
              "display":"real part, with time-independent positive contrast gains",
              "label_collisions":overlaps,"size":[WIDTH,HEIGHT]}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    frame(7).save(OUT/f"{NAME}-poster.png")
    sheet=Image.new("RGB",(1440,3*380),BG)
    for j,index in enumerate(SAMPLE_FRAMES):
        pic=frame(index)
        sheet.paste(pic.resize((720,380),Image.Resampling.LANCZOS),((j%2)*720,(j//2)*380))
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-poster.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output=OUT/f"{NAME}.mp4"
    temporary=OUT/f"{NAME}-rendering.mp4"
    cmd=[art.imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-f","rawvideo",
         "-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),"-i","-",
         "-an","-c:v","libx264","-preset","fast","-crf","18",
         "-pix_fmt","yuv420p","-movflags","+faststart",str(temporary)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    cache=[]
    start=time.perf_counter()
    try:
        for i in range(FRAMES):
            if i<CYCLE_FRAMES:
                cache.append(frame(i).tobytes())
            process.stdin.write(cache[i%CYCLE_FRAMES])
            if i%FPS==0:
                print(f"{i/FPS:g}/{DURATION:g}s, elapsed {time.perf_counter()-start:.1f}s",flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    temporary.replace(output)
    print(str(output),flush=True)


def encoded_check():
    reader=art.imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata=next(reader)
    assert tuple(metadata["size"])==(WIDTH,HEIGHT)
    assert metadata["fps"]==FPS
    errors=[]
    sheet=Image.new("RGB",(1440,1140),BG)
    selected=(0,7,22,60,112,179)
    for index,data in enumerate(reader):
        if index in selected:
            decoded=np.frombuffer(data,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
            error=float(np.mean(abs(decoded.astype(float)-np.asarray(frame(index)).astype(float))))
            assert error<2.5, error
            pic=Image.fromarray(decoded.copy())
            j=len(errors)
            sheet.paste(pic.resize((720,380),Image.Resampling.LANCZOS),((j%2)*720,(j//2)*380))
            if index==7:
                pic.save(OUT/f"{NAME}-encoded-poster.png")
            errors.append(error)
    assert index+1==FRAMES
    assert len(errors)==len(selected)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":index+1,"fps":FPS,"duration":(index+1)/FPS,
            "size":metadata["size"],"max_mean_rgb_error":max(errors)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    options=parser.parse_args()
    if options.check: validate()
    if options.preview: preview()
    if options.render: render()
    if options.encoded_check: encoded_check()
