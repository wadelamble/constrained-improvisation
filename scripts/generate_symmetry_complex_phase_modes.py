"""Full complex view of the accepted nine-mode common-phase animation.

Use the original mode amplitudes, phases, normalization, and five-turn timing.
Shift all nine wave numbers by +8 to wind more turns through the main envelope;
this multiplies the previous sum by exp(8ix), preserving its exact magnitude.
Each curve represents (x, Re f(x), Im f(x)), viewed through a fixed parallel
projection. The gold surface has radius |f(x)| at every x; phase rotates the
curve on this stationary surface. Only its projected outer boundary is drawn.
The pure-mode envelopes are cylinders.
No beads, curve markers, camera motion, or physical time evolution are used.
One spatial period is shown; the finite Fourier sum repeats outside the view.

Run with the project's Python runtime and --check --preview --render
--encoded-check. Output paths are relative to this repository.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

import generate_symmetry_packet_phase_modes as original

np = original.np
Image, ImageDraw = original.Image, original.ImageDraw
imageio_ffmpeg = original.imageio_ffmpeg
ROOT, OUT = original.ROOT, original.OUT
NAME = "symmetry-complex-phase-modes"
WIDTH, HEIGHT, SS = original.WIDTH, original.HEIGHT, original.SS
FPS, FRAMES, DURATION = original.FPS, original.FRAMES, original.DURATION
X, A = original.X, original.A
CARRIER_SHIFT = 8
K = original.K+CARRIER_SHIFT
BASE_MODES = original.BASE_MODES*np.exp(1j*CARRIER_SHIFT*X)
BASE_FUNCTION = BASE_MODES.sum(axis=0)
RADIUS = abs(BASE_FUNCTION)
BG, PANEL = original.BG, original.PANEL
INK, MUTED, BORDER = original.INK, original.MUTED, original.BORDER
BLUE, GOLD, AXIS = original.BLUE, original.GOLD, original.AXIS
px, text, line, curve = original.px, original.text, original.line, original.curve
arrow, paste_formula = original.arrow, original.paste_formula
phase_at = original.phase_at

GAIN = 110.
DEPTH_SCALE = .30
VIEW_ANGLE = math.radians(25)
VIEW_ROTATION = np.exp(-1j*VIEW_ANGLE)
PLOT_LEFT = (91., 810.)
PLOT_WIDTH = 550.
BASELINE = 537.
ROW_Y = original.ROW_Y
AXIS_Y = original.AXIS_Y
BACK_BLUE = tuple(round(.48*b+.52*p) for b,p in zip(BLUE,PANEL))
SAMPLE_TIMES = (0., 2., 4.5, 8.5, 12.5, DURATION-1/FPS)


def project(x, value, col, baseline):
    """Fixed parallel view; equal scales in both panes and all nine rows.

    The transverse complex plane is rotated only to set the camera orientation.
    Its horizontal foreshortening is fixed; this is not a changing wave phase.
    """
    transverse = np.asarray(value)*VIEW_ROTATION
    sx = PLOT_LEFT[col]+(np.asarray(x)-original.XMIN)/(original.XMAX-original.XMIN)*PLOT_WIDTH
    return np.stack((sx+GAIN*DEPTH_SCALE*transverse.imag,
                     baseline-GAIN*transverse.real),axis=-1)


def envelope_outline(radius, col, *, samples=1801):
    """Projected silhouette of the magnitude surface, with no internal mesh.

    A cross section at x projects to an ellipse of vertical radius GAIN*|f(x)|
    and horizontal radius DEPTH_SCALE times that. The outer boundary is the
    union of these projected disks, not merely two meridians on the surface.
    """
    radius=np.broadcast_to(radius,X.shape)*GAIN
    centers=project(X,np.zeros_like(X),col,0.)[:,0]
    left=float(np.min(centers-DEPTH_SCALE*radius))
    right=float(np.max(centers+DEPTH_SCALE*radius))
    # Resolve the steep slopes of the projected end caps without a dense mesh.
    unit=(1-np.cos(np.linspace(0,np.pi,samples)))/2
    sx=left+(right-left)*unit
    height2=np.max(radius[:,None]**2-((sx[None,:]-centers[:,None])/DEPTH_SCALE)**2,axis=0)
    return sx,np.sqrt(np.maximum(height2,0.))


def envelope(d, radius, col, baseline):
    sx,height=envelope_outline(radius,col)
    top=np.column_stack((sx,baseline-height))
    bottom=np.column_stack((sx[::-1],baseline+height[::-1]))
    boundary=np.vstack((top,bottom,top[:1]))
    curve(d,boundary,(*GOLD,168),1.0)


def draw_complex_curve(d, values, col, baseline, width):
    """Draw the full curve, with fixed front/back depth cues at crossings."""
    points = project(X,values,col,baseline)
    depth = (values*VIEW_ROTATION).imag
    front = (depth[:-1]+depth[1:])>=0
    breaks = np.r_[0,np.flatnonzero(front[1:]!=front[:-1])+1,len(front)]
    runs = [(int(a),int(b),bool(front[a])) for a,b in zip(breaks[:-1],breaks[1:])]
    for side,color in ((False,BACK_BLUE),(True,BLUE)):
        for start,end,is_front in runs:
            if is_front==side:
                curve(d,points[start:end+1],color,width)


def orientation_key(d):
    # One fixed reference triad: the other two axes are amplitude, not space.
    origin = np.array([139.,304.])
    for label,delta in (
        ("x",np.array([62.,0.])),
        ("Re",np.array([-DEPTH_SCALE*math.sin(VIEW_ANGLE),-math.cos(VIEW_ANGLE)])*47),
        ("Im",np.array([DEPTH_SCALE*math.cos(VIEW_ANGLE),-math.sin(VIEW_ANGLE)])*47),
    ):
        tip=origin+delta
        arrow(d,origin,tip,(*MUTED,190),1.2,5)
        if label=="x":
            text(d,tip+np.array([9.,0.]),label,15,MUTED,anchor="lm")
        elif label=="Re":
            text(d,tip+np.array([-3.,-7.]),label,15,MUTED,anchor="rb")
        else:
            text(d,tip+np.array([7.,-4.]),label,15,MUTED,anchor="lb")


@lru_cache(None)
def background():
    image=Image.new("RGB",(WIDTH*SS,HEIGHT*SS),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(38,25),"One phase change, nine complex modes",32,bold=True)
    text(d,(40,77),"The complex function turns; its magnitude envelope stays fixed.",19,MUTED)
    for box in original.PANELS:
        d.rounded_rectangle(px(box),radius=14*SS,fill=PANEL,outline=BORDER,width=SS)
    text(d,(52,153),"Complex function · exact sum",25,bold=True)
    text(d,(54,192),"The gold envelope stays fixed",19,GOLD)
    text(d,(760,153),"Nine pure modes",25,bold=True)
    text(d,(762,191),"The same phase is added to every mode",17,MUTED)
    envelope(d,RADIUS,0,BASELINE)
    line(d,(PLOT_LEFT[0]-4,BASELINE),(PLOT_LEFT[0]+PLOT_WIDTH+4,BASELINE),(*AXIS,165),1)
    for j,(k,y) in enumerate(zip(K,ROW_Y)):
        envelope(d,A[j],1,y)
        line(d,(PLOT_LEFT[1]-3,y),(PLOT_LEFT[1]+PLOT_WIDTH+3,y),(*AXIS,150),.8)
        text(d,(749,y),f"k={k}",14,MUTED,anchor="lm")
    orientation_key(d)
    line(d,(79,786),(109,786),BLUE,2.7)
    text(d,(120,773),"complex function",18,BLUE)
    line(d,(370,786),(400,786),GOLD,1.1)
    text(d,(411,773),"envelope: |Ψ|",18,GOLD)
    paste_formula(image,(366,829),r"$\Psi_{\phi}(x)=e^{i\phi}\,\Psi_0(x)$",24,centered=True)
    for col in range(2):
        line(d,(PLOT_LEFT[col],AXIS_Y),(PLOT_LEFT[col]+PLOT_WIDTH,AXIS_Y),AXIS,1)
        for x,label in ((-np.pi,"−π"),(-np.pi/2,"−π/2"),(0,"0"),(np.pi/2,"π/2"),(np.pi,"π")):
            xp=project(x,0.,col,0.)[0]
            line(d,(xp,AXIS_Y-4),(xp,AXIS_Y+4),AXIS,1)
            text(d,(xp,AXIS_Y+9),label,14,MUTED,anchor="ma")
        text(d,(PLOT_LEFT[col]+PLOT_WIDTH+13,AXIS_Y),"x",17,MUTED,anchor="lm")
    text(d,(39,955),"One spatial period · the same view and x / amplitude scales in both panes.",16,MUTED)
    text(d,(1400,955),"φ changes; this is not time evolution.",16,MUTED,anchor="ra")
    return image


def frame(seconds):
    phase=phase_at(seconds)
    modes=BASE_MODES*np.exp(1j*phase)
    image=background().copy()
    d=ImageDraw.Draw(image,"RGBA")
    draw_complex_curve(d,modes.sum(axis=0),0,BASELINE,2.8)
    for j,y in enumerate(ROW_Y):
        draw_complex_curve(d,modes[j],1,y,1.9)
    original.draw_counter(d,phase)
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def check():
    max_sum=max_radius=max_projection=0.
    max_outline_excess=0.
    outlines=[envelope_outline(RADIUS,0)]+[envelope_outline(amplitude,1) for amplitude in A]
    for phase in np.linspace(0,10*np.pi,91):
        direct=A[:,None]*np.exp(1j*(K[:,None]*X+original.INITIAL_PHASES[:,None]+phase))
        total=direct.sum(axis=0)
        max_sum=max(max_sum,float(np.max(abs(total-np.exp(1j*phase)*BASE_FUNCTION))))
        max_radius=max(max_radius,float(np.max(abs(abs(total)-RADIUS))))
        # A linear camera must preserve the displayed vector addition at each x.
        mode_vectors=sum(project(X,direct[j],1,0.)-project(X,np.zeros_like(X),1,0.) for j in range(9))
        sum_vectors=project(X,total,0,0.)-project(X,np.zeros_like(X),0,0.)
        max_projection=max(max_projection,float(np.max(abs(mode_vectors-sum_vectors))))
        for j,values in enumerate([total,*direct]):
            col=0 if j==0 else 1
            baseline=BASELINE if j==0 else ROW_Y[j-1]
            points=project(X,values,col,baseline)
            outline_x,outline_height=outlines[j]
            max_outline_excess=max(max_outline_excess,float(np.max(
                abs(points[:,1]-baseline)-np.interp(points[:,0],outline_x,outline_height))))
            box=original.PANELS[col]
            assert np.min(points[:,0])>box[0]+10 and np.max(points[:,0])<box[2]-10
            assert np.min(points[:,1])>box[1]+70 and np.max(points[:,1])<AXIS_Y-25
            if j>0:
                assert np.max(abs(points[:,1]-baseline))<.5*np.min(np.diff(ROW_Y))-4
    assert max_sum<1e-12 and max_radius<1e-12 and max_projection<1e-10
    assert max_outline_excess<.75,max_outline_excess
    preserved_envelope_error=float(np.max(abs(RADIUS-original.ENVELOPE)))
    assert preserved_envelope_error<1e-12
    assert phase_at(DURATION)==10*np.pi
    assert np.all(np.diff([phase_at(i/FPS) for i in range(FRAMES)])>=0)
    assert np.max(abs(BASE_MODES*np.exp(10j*np.pi)-BASE_MODES))<1e-12
    report={"wave_numbers":K.tolist(),"amplitudes":A.tolist(),
        "initial_phases":original.INITIAL_PHASES.tolist(),"exactly_nine_modes":True,
        "max_direct_sum_error":max_sum,"max_envelope_error":max_radius,
        "common_wave_number_shift":CARRIER_SHIFT,"envelope_change_from_original":preserved_envelope_error,
        "max_projected_addition_error_pixels":max_projection,
        "max_outline_sampling_excess_pixels":max_outline_excess,
        "phase_turns":5,"duration":DURATION,"fps":FPS,"frames":FRAMES,"size":[WIDTH,HEIGHT],
        "no_curve_markers":True,"camera_is_fixed":True,
        "projection":{"transverse_rotation_degrees":25,"depth_scale":DEPTH_SCALE},
        "common_amplitude_pixels_per_unit":GAIN,"common_x_plot_width":PLOT_WIDTH,
        "envelope":"Projected outer boundary of stationary surface of revolution with exact radius |sum of nine complex modes|; no internal grid.",
        "interpretation":"Common phase parameter, not physical time evolution; one period of a finite Fourier sum."}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1440,1620),BG)
    for i,seconds in enumerate(SAMPLE_TIMES):
        pic=frame(seconds)
        sheet.paste(pic.resize((720,540),Image.Resampling.LANCZOS),((i%2)*720,(i//2)*540))
    frame(4.5).save(OUT/f"{NAME}-poster.png")
    frame(0.).save(OUT/f"{NAME}-initial.png")
    frame(DURATION-1/FPS).save(OUT/f"{NAME}-final.png")
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-poster.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output=OUT/f"{NAME}.mp4"
    command=[imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
        "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),
        "-i","-","-an","-c:v","libx264","-preset","fast","-crf","18",
        "-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start=time.perf_counter()
    key,rgb=None,None
    try:
        for i in range(FRAMES):
            phase=phase_at(i/FPS)
            if phase!=key:
                rgb=frame(i/FPS).tobytes()
                key=phase
            proc.stdin.write(rgb)
            if i%(3*FPS)==0:
                print(f"{i/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-start:.1f}s",flush=True)
        proc.stdin.close()
        error=proc.stderr.read().decode(errors="replace")
        if proc.wait():
            raise RuntimeError(error)
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    print(str(output),flush=True)


def encoded_check():
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta=next(reader)
    assert tuple(meta["size"])==(WIDTH,HEIGHT) and abs(meta["fps"]-FPS)<1e-8
    samples={round(t*FPS) for t in SAMPLE_TIMES}
    sheet=Image.new("RGB",(1440,1620),BG)
    count,errors=0,[]
    for i,raw in enumerate(reader):
        count+=1
        if i not in samples:
            continue
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        expected=np.asarray(frame(i/FPS))
        error=float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
        assert error<2.5
        pic=Image.fromarray(decoded.copy())
        slot=len(errors)
        sheet.paste(pic.resize((720,540),Image.Resampling.LANCZOS),((slot%2)*720,(slot//2)*540))
        if i==round(4.5*FPS):
            pic.save(OUT/f"{NAME}-encoded-sample.png")
        errors.append(error)
    assert count==FRAMES and len(errors)==len(samples)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration":count/FPS,"size":meta["size"],"fps":meta["fps"],
        "max_decoded_rgb_error":max(errors)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    args=parser.parse_args()
    if args.check: check()
    if args.preview: preview()
    if args.render: render()
    if args.encoded_check: encoded_check()
