"""Two translations preserve the overlap of a pair of wave functions.

The columns are independent experiments, starting from the same normalized
pair: x translations shown in x space; k translations shown in k space. They
are not two Fourier views of one evolving doubly transformed state.

The initial states are Weyl-displaced unit-width Gaussians with q_j=p_j.
Their full Hermitian overlap is real and positive, exp(-0.72). Both columns
use direct argument shifts, retaining every state-dependent global phase.

The lower spheres show an explicitly schematic real-overlap example, not a
Bloch sphere or a fixed 3D embedding of the infinite-dimensional dynamics.
The projection triangle moves in a camera-facing great-circle plane under
orthographic projection, so lengths, angle and projection are exact on screen.
Playback follows translation parameters, not physical time.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / ".tools" / "animation-python-packages"
if PACKAGES.is_dir():
    sys.path.insert(0, str(PACKAGES))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-ccr-unitarity"
WIDTH, HEIGHT, SS = 1440, 1040, 2
FPS, DURATION = 30, 17.0
FRAMES = round(FPS * DURATION)
CONTROLS_SAFE_TOP, CONTENT_BOTTOM = 940, 929
BG, PANEL = (253, 250, 244), (250, 247, 240)
INK, MUTED, BORDER = (37, 38, 40), (111, 108, 102), (218, 211, 200)
BLUE, CORAL, GOLD = (43, 93, 145), (177, 77, 60), (192, 128, 25)
AXIS = (210, 206, 198)
TOPS = ((28, 108, 704, 427), (736, 108, 1412, 427))
BOTTOMS = ((28, 447, 704, 891), (736, 447, 1412, 891))
CENTERS = (1.1, 2.3)
OVERLAP = math.exp(-0.5 * (CENTERS[1] - CENTERS[0]) ** 2)
ALPHA = math.acos(OVERLAP)
RADIUS = 143.0
XMIN, XMAX = -5.1, 8.5
SAMPLES = np.linspace(XMIN, XMAX, 1001)
COLORS = (BLUE, CORAL)


@lru_cache(None)
def font(size, bold=False):
    names = ("seguisb.ttf" if bold else "segoeui.ttf",
             "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    for name in names:
        try:
            return ImageFont.truetype(name, round(size * SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(v * SS) for v in values)


def text(draw, pos, value, size=20, fill=INK, bold=False, anchor=None):
    typeface = formula_font(size) if any(c in value for c in "⟨⟩‖") else font(size, bold)
    draw.text(px(pos), value, font=typeface, fill=fill, anchor=anchor)


@lru_cache(None)
def formula_font(size):
    # Segoe UI omits mathematical angle brackets on this Windows install.
    import matplotlib
    path = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans.ttf"
    return ImageFont.truetype(str(path), round(size * SS))


def line(draw, a, b, color, width=1):
    draw.line(px((*a, *b)), fill=color, width=max(1, round(width * SS)))


def polyline(draw, points, color, width=1):
    draw.line([px(p) for p in points], fill=color,
              width=max(1, round(width * SS)), joint="curve")


def arrow(draw, start, end, color, width=2, head=9):
    delta = np.asarray(end) - start
    length = float(np.linalg.norm(delta))
    if length < 0.1:
        return
    direction = delta / length
    side = np.array([-direction[1], direction[0]])
    head = min(head, length * 0.5)
    line(draw, start, end, color, width)
    draw.polygon([px(end), px(np.asarray(end) - head * direction + head * .43 * side),
                  px(np.asarray(end) - head * direction - head * .43 * side)], fill=color)


def dash(draw, a, b, color, width=1.3, length=6, gap=5):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    distance = float(np.linalg.norm(b-a))
    if distance < 1e-12:
        return
    unit = (b-a) / distance
    for first in np.arange(0, distance, length + gap):
        line(draw, a + unit * first, a + unit * min(first+length, distance), color, width)


def ease(t):
    # Mostly linear motion with short velocity ramps at the ends.
    t = float(np.clip(t, 0, 1))
    ramp = .12
    if t < ramp:
        return t*t / (2*ramp*(1-ramp))
    if t > 1-ramp:
        return 1-(1-t)**2 / (2*ramp*(1-ramp))
    return (t-ramp/2)/(1-ramp)


def displacement(seconds):
    if seconds <= 1.5:
        return 0.0
    if seconds < 5.5:
        return 2.0 * ease((seconds-1.5)/4)
    if seconds < 6.5:
        return 2.0
    if seconds < 12.5:
        return 2.0 - 4.0 * ease((seconds-6.5)/6)
    if seconds < 13.5:
        return -2.0
    if seconds < 16.5:
        return -2.0 + 2.0 * ease((seconds-13.5)/3)
    return 0.0


def wave(grid, center, representation=0, shift=0):
    u = np.asarray(grid) - shift
    # Do not replace the center with center+shift: that loses phase factors.
    sign = 1 if representation == 0 else -1
    return np.pi**(-.25) * np.exp(-.5*(u-center)**2) * np.exp(sign*1j*center*(u-center/2))


def geometry(shift):
    theta = -.28 + .48 * shift
    blue = np.array([math.cos(theta), math.sin(theta)])
    coral = np.array([math.cos(theta+ALPHA), math.sin(theta+ALPHA)])
    foot = OVERLAP * blue
    return blue, coral, foot


@lru_cache(None)
def backdrop():
    image = Image.new("RGB", (WIDTH*SS, HEIGHT*SS), BG)
    d = ImageDraw.Draw(image, "RGBA")
    text(d, (37, 24), "Translation preserves overlap", 32, bold=True)
    text(d, (39, 70), "The same translation acts on both wave functions.", 19, MUTED)
    text(d, (1400, 35), "Two separate transformations", 17, MUTED, anchor="ra")
    for col, (top, bottom) in enumerate(zip(TOPS, BOTTOMS)):
        for box in (top, bottom):
            d.rounded_rectangle(px(box), radius=14*SS, fill=PANEL, outline=BORDER, width=SS)
        left, _, right, _ = top
        variable = "x" if col == 0 else "k"
        text(d, (left+24, 125), f"Translate in {variable}", 25, bold=True)
        formula = "ψ(x − a),  χ(x − a)" if col == 0 else "ψ̃(k − b),  χ̃(k − b)"
        text(d, (left+25, 164), formula, 20, MUTED)
        xleft, xright, baseline = left+37, right-31, 292
        line(d, (xleft, baseline), (xright, baseline), AXIS, 1.0)
        for value in (-4, -2, 0, 2, 4, 6, 8):
            x = xleft + (value-XMIN)/(XMAX-XMIN)*(xright-xleft)
            line(d, (x, baseline-4), (x, baseline+4), AXIS)
            text(d, (x, 370), str(value), 14, MUTED, anchor="ma")
        text(d, (xright+10, baseline-2), variable, 17, MUTED, anchor="lm")
        line(d, (left+27, 405), (left+52, 405), BLUE, 2.7)
        text(d, (left+61, 393), "ψ", 19, BLUE)
        line(d, (left+115, 405), (left+140, 405), CORAL, 2.7)
        text(d, (left+149, 393), "χ", 19, CORAL)
        text(d, (right-25, 395), "real parts · faint curves: ±magnitude", 14, MUTED, anchor="ra")
        text(d, (left+24, 465), "The same pair as vectors in function representation space", 23, bold=True)
        op = "Tₓ" if col == 0 else "Tₖ"
        text(d, (left+25, 501), f"⟨{op}ψ, {op}χ⟩ = ⟨ψ, χ⟩", 21, MUTED)
        # Fixed wireframe sphere. Screen-space motion is on its central
        # camera-facing great circle, avoiding perspective foreshortening.
        center = np.array([left+223., 688.])
        circle = [center + RADIUS*np.array([math.cos(t), math.sin(t)])
                  for t in np.linspace(0, 2*math.pi, 361)]
        d.ellipse(px((* (center-RADIUS), * (center+RADIUS))), fill=(*BG,255), outline=(*BORDER,220), width=SS)
        for tilt in (-.6, .6):
            basis1 = np.array([math.cos(tilt), math.sin(tilt)])
            basis2 = np.array([-math.sin(tilt), math.cos(tilt)])
            points = [center+RADIUS*(math.cos(t)*basis1+.30*math.sin(t)*basis2)
                      for t in np.linspace(0,2*math.pi,241)]
            polyline(d, points, (*BORDER,100), .8)
        polyline(d, circle, (*MUTED,130), 1.1)
        text(d, (left+422, 584), "Unit lengths", 18, MUTED)
        text(d, (left+422, 615), "‖ψ‖ = ‖χ‖ = 1", 23)
        text(d, (left+422, 682), "Projection / overlap", 18, MUTED)
        text(d, (left+422, 711), f"{OVERLAP:.3f}", 37, GOLD, bold=True)
        text(d, (left+422, 778), f"Angle  {math.degrees(ALPHA):.1f}°", 19, MUTED)
        text(d, (left+223, 848), "Lengths, angle and projection stay fixed", 16, MUTED, anchor="ma")
    text(d, (39, 907), "Real, positive overlap chosen; state-space motion is schematic.", 16, MUTED)
    text(d, (1400, 907), "Playback follows a and b, not physical time.", 16, MUTED, anchor="ra")
    return image


def draw_wave_pair(d, col, shift):
    left, _, right, _ = TOPS[col]
    x = left+37 + (SAMPLES-XMIN)/(XMAX-XMIN)*(right-left-68)
    baseline, amplitude = 292., 90.
    for center, color in zip(CENTERS, COLORS):
        values = wave(SAMPLES, center, col, shift)
        for sign in (-1, 1):
            points = np.column_stack((x, baseline-sign*amplitude*abs(values)))
            polyline(d, points, (*color,65), 1)
    for center, color in zip(CENTERS, COLORS):
        values = wave(SAMPLES, center, col, shift)
        polyline(d, np.column_stack((x, baseline-amplitude*values.real)), color, 2.8)
    param = "a" if col == 0 else "b"
    text(d, (right-25, 130), f"{param} = {shift:+.2f}", 23, GOLD, anchor="ra")


def draw_geometry(d, col, shift):
    left = BOTTOMS[col][0]
    origin = np.array([left+223., 688.])
    blue, coral, foot = geometry(shift)
    def screen(v):
        return origin + RADIUS*np.array([v[0], -v[1]])
    b, r, f = map(screen, (blue, coral, foot))
    dash(d, r, f, (*MUTED,200), 1.5)
    # Right angle marker lies inside the projection triangle.
    along = -blue
    perp = (coral-foot)/np.linalg.norm(coral-foot)
    side = 9.0/RADIUS
    square = [screen(foot+side*along), screen(foot+side*(along+perp)), screen(foot+side*perp)]
    polyline(d, square, (*MUTED,210), 1.1)
    theta = math.atan2(blue[1],blue[0])
    arc = [origin+42*np.array([math.cos(t),-math.sin(t)])
           for t in np.linspace(theta,theta+ALPHA,81)]
    polyline(d, arc, (*MUTED,155), 1.15)
    arrow(d, origin, b, BLUE, 3.4, 12)
    arrow(d, origin, r, CORAL, 3.4, 12)
    arrow(d, origin, f, GOLD, 5.0, 10)
    for point, color, radius in ((origin,INK,3.), (f,GOLD,3.5)):
        d.ellipse(px((* (point-radius), * (point+radius))), fill=color)
    op = "Tₓ" if col == 0 else "Tₖ"
    for vector, symbol, color in ((blue, "ψ", BLUE), (coral, "χ", CORAL)):
        tip = screen(vector)
        # All tips remain in a compact right-facing sector. A fixed side
        # avoids an artificial label jump when the coral vector passes vertical.
        text(d, tip+np.array([13., -8.]), op+symbol, 19, color, anchor="lm")


def frame(seconds):
    image = backdrop().copy()
    d = ImageDraw.Draw(image, "RGBA")
    shift = displacement(seconds)
    for col in range(2):
        draw_wave_pair(d, col, shift)
        draw_geometry(d, col, shift)
    return image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


def check():
    q = np.linspace(-18,18,18001)
    integrate = np.trapezoid
    largest_norm_error = largest_overlap_error = 0.
    for col in range(2):
        for shift in np.linspace(-2.5,2.5,11):
            psi, chi = (wave(q, center, col, shift) for center in CENTERS)
            norms = [integrate(abs(v)**2,q) for v in (psi,chi)]
            overlap = integrate(psi.conj()*chi,q)
            largest_norm_error = max(largest_norm_error, *(abs(n-1) for n in norms))
            largest_overlap_error = max(largest_overlap_error, abs(overlap-OVERLAP))
    fourier_error = 0.
    for center in CENTERS:
        psi = wave(q,center)
        for k in np.linspace(-3,6,13):
            calculated = integrate(np.exp(-1j*k*q)*psi,q)/math.sqrt(2*math.pi)
            fourier_error = max(fourier_error, abs(calculated-wave(k,center,1)))
    max_geometry_error = max_clipped_mass = 0.
    view = np.linspace(XMIN,XMAX,7001)
    for shift in np.linspace(-2.,2.,41):
        b,r,f = geometry(shift)
        max_geometry_error = max(max_geometry_error, abs(np.linalg.norm(b)-1),
             abs(np.linalg.norm(r)-1), abs(np.dot(b,r)-OVERLAP),
             abs(np.linalg.norm(f)-OVERLAP), abs(np.dot(r-f,b)))
        for center in CENTERS:
            max_clipped_mass=max(max_clipped_mass,1-integrate(abs(wave(view,center,0,shift))**2,view))
    assert largest_norm_error<1e-12 and largest_overlap_error<1e-12
    assert fourier_error<1e-12 and max_geometry_error<1e-12
    assert max_clipped_mass<2e-8
    assert CONTENT_BOTTOM<CONTROLS_SAFE_TOP
    report={"full_complex_overlap":OVERLAP,"angle_degrees":math.degrees(ALPHA),
        "max_norm_error":float(largest_norm_error),"max_complex_overlap_error":float(largest_overlap_error),
        "max_fourier_pair_error":float(fourier_error),"max_geometry_error":float(max_geometry_error),
        "max_probability_mass_outside_plot":float(max_clipped_mass),
        "initial_states":"q_j=p_j in {1.1,2.3}; normalized unit-width coherent Gaussians",
        "translation":"direct argument shift; full phases retained",
        "columns":"independent translations of the same initial pair, each in its own representation",
        "geometry":"schematic real-positive overlap; face-on great circle, orthographic projection; not a Bloch sphere",
        "duration":DURATION,"fps":FPS,"size":[WIDTH,HEIGHT],"frames":FRAMES,
        "content_bottom":CONTENT_BOTTOM,"controls_safe_top":CONTROLS_SAFE_TOP}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    times = (0,4,7,10,13,15.5)
    sheet=Image.new("RGB",(1440,1608),BG)
    for index,t in enumerate(times):
        pic=frame(t)
        sheet.paste(pic.resize((720,520),Image.Resampling.LANCZOS),((index%2)*720,(index//2)*536))
        d=ImageDraw.Draw(sheet)
        d.text(((index%2)*720+14,(index//2)*536+520),f"{t:g} s",fill=MUTED)
    frame(4).save(OUT/f"{NAME}-poster.png")
    frame(DURATION-1/FPS).save(OUT/f"{NAME}-final.png")
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output=OUT/f"{NAME}.mp4"
    command=[imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
             "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
             "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast",
             "-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    started=time.perf_counter()
    key,rgb=None,None
    try:
        for i in range(FRAMES):
            shift=displacement(i/FPS)
            if shift!=key:
                rgb=frame(i/FPS).tobytes()
                key=shift
            process.stdin.write(rgb)
            if i%(3*FPS)==0:
                print(f"{i/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-started:.1f}s",flush=True)
        process.stdin.close()
        error=process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    print(str(output),flush=True)


def encoded_check():
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta=next(reader)
    assert tuple(meta["size"])==(WIDTH,HEIGHT) and abs(meta["fps"]-FPS)<1e-8
    indices={0,120,210,300,390,FRAMES-1}
    sheet=Image.new("RGB",(1440,1560),BG)
    count=0
    errors=[]
    for i,raw in enumerate(reader):
        count+=1
        if i in indices:
            decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
            expected=np.asarray(frame(i/FPS))
            error=float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
            assert error<2.0
            slot=len(errors)
            image=Image.fromarray(decoded.copy())
            sheet.paste(image.resize((720,520),Image.Resampling.LANCZOS),((slot%2)*720,(slot//2)*520))
            if i==120:
                image.save(OUT/f"{NAME}-encoded-sample.png")
            errors.append(error)
    assert count==FRAMES and len(errors)==len(indices)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":count,"duration":count/FPS,"size":meta["size"],
            "fps":meta["fps"],"max_decoded_rgb_error":max(errors)}
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
