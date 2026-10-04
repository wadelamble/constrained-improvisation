"""A spatial snapshot under a continuous family of U(1) gauge changes.

Reuses the accepted exact nine-mode complex function and cream/blue/gold idiom.
The playback parameter s is NOT physical time. On the displayed interval,
psi_s = exp(i alpha_s) psi_0, alpha_s = c(s) + g(s) f(x),
f(x) = 5 sin(x) + 2 sin(2x). Write a=(q/hbar) A_x = g f'(x),
so D_{x,s} = partial_x - i a and D_{x,s} psi_s = exp(i alpha_s) partial_x psi_0.
This is a pure-gauge connection, not a generated electromagnetic field.

The inset uses unit phase arrows at two fixed positions (not particles).
Transport from x1 to x2 rotates by beta = integral a dx.
arg[psi_s(x2) / (exp(i beta) psi_s(x1))] is gauge invariant.
The envelope, density, covariant-gradient norm and probability current are
checked independently using analytic derivatives and numerical quadrature.

Run --check --preview --render --encoded-check with the project Python runtime.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

import generate_symmetry_complex_phase_modes as source

np = source.np
Image, ImageDraw = source.Image, source.ImageDraw
root, out = source.ROOT, source.OUT
NAME = "symmetry-local-gauge-preview"
W, H, SS = 1600, 1000, 2
FPS, DURATION = 30, 24
FRAMES = FPS * DURATION
BG, PANEL = source.BG, source.PANEL
INK, MUTED, BORDER = source.INK, source.MUTED, source.BORDER
BLUE, GOLD = source.BLUE, source.GOLD
RED, GREEN = (175, 76, 66), (43, 124, 116)
FAINT = (218, 213, 203)
X = source.X
BASE = source.BASE_FUNCTION
RADIUS = np.abs(BASE)
X1, X2 = -.25, .25
LEFT, RIGHT, BASELINE, GAIN, DEPTH = 83., 878., 479., 160., .33
VIEW = np.exp(-1j * math.radians(25))
SAMPLES = (0., 3., 8., 12.5, 18., 23.)


def base_at(x):
    return np.sum(source.A * np.exp(1j * (source.K * x + source.original.INITIAL_PHASES)))


Z1, Z2 = base_at(X1), base_at(X2)
THETA1, THETA2 = np.angle(Z1), np.angle(Z2)
DELTA = np.angle(Z2 / Z1)


def f(x):
    return 5 * np.sin(x) + 2 * np.sin(2 * x)


def fp(x):
    return 5 * np.cos(x) + 4 * np.cos(2 * x)


def smooth(u):
    u = float(np.clip(u, 0, 1))
    return u * u * (3 - 2 * u)


def state(seconds):
    if seconds < 6:
        return 2 * np.pi * smooth((seconds - .6) / 4.6), 0., "One angle everywhere"
    if seconds < 14:
        return 2 * np.pi, smooth((seconds - 6) / 6), "Different angles at different positions"
    if seconds < 21:
        return 2 * np.pi, 1 - 2 * smooth((seconds - 14) / 5.5), "The comparison stays unchanged"
    return 2 * np.pi, -1 + smooth((seconds - 21) / 2), "The same physical situation"


def px(seq):
    return tuple(round(float(v) * SS) for v in seq)


def text(d, xy, value, size=20, color=INK, bold=False, anchor=None):
    d.text(px(xy), value, font=source.original.font(size, bold), fill=color, anchor=anchor)


def line(d, a, b, color=FAINT, width=1):
    d.line(px((*a, *b)), fill=color, width=max(1, round(width * SS)))


def curve(d, points, color, width=2):
    d.line(np.rint(np.asarray(points) * SS).astype(int).ravel().tolist(),
           fill=color, width=max(1, round(width * SS)), joint="curve")


def arrow(d, a, b, color, width=2.5, head=9):
    source.original.arrow(d, a, b, color, width, head)


def formula(img, xy, value, size=22, color=INK, center=False):
    source.original.paste_formula(img, xy, value, size, color, centered=center)


def screen_x(x):
    return LEFT + (np.asarray(x) - X[0]) / (X[-1] - X[0]) * (RIGHT - LEFT)


def project(x, z):
    z = np.asarray(z) * VIEW
    return np.stack((screen_x(x) + GAIN * DEPTH * z.imag, BASELINE - GAIN * z.real), axis=-1)


def tip(center, r, angle):
    return np.asarray(center) + r * np.array([np.cos(angle), -np.sin(angle)])


def arc(d, center, r, start, sweep, color, width=2, head=False):
    if abs(sweep) < 1e-5:
        return
    angles = np.linspace(start, start + sweep, max(12, math.ceil(abs(sweep) * 45)))
    points = np.array([tip(center, r, a) for a in angles])
    curve(d, points, color, width)
    if head:
        arrow(d, points[-3], points[-1], color, width, 6)


def dashed_arrow(d, center, r, angle, color):
    for t in np.arange(0, .92, .13):
        line(d, tip(center, r * t, angle), tip(center, r * min(t + .07, .94), angle), color, 1.6)
    arrow(d, tip(center, r * .91, angle), tip(center, r, angle), color, 1.6, 7)


def phase_circle(d, center, r):
    d.ellipse(px((center[0]-r, center[1]-r, center[0]+r, center[1]+r)), outline=FAINT, width=SS)
    line(d, (center[0]-r-8, center[1]), (center[0]+r+8, center[1]))
    line(d, (center[0], center[1]-r-8), (center[0], center[1]+r+8))


@lru_cache(None)
def background():
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img, "RGBA")
    text(d, (36, 25), "Local phase symmetry", 34, bold=True)
    text(d, (38, 75), "The spiral changes. The connection preserves the phase comparison.", 21, MUTED)
    for box in ((30, 142, 926, 926), (948, 142, 1570, 926)):
        d.rounded_rectangle(px(box), radius=14*SS, fill=PANEL, outline=BORDER, width=SS)
    text(d, (54, 165), "Complex function", 26, bold=True)
    formula(img, (478, 216), r"$\psi_s(x)=e^{i\alpha_s(x)}\,\psi_0(x)$", 25, center=True)

    # Exact projected silhouette of the fixed magnitude surface.
    centers, r = screen_x(X), RADIUS * GAIN
    sx = np.linspace(float(np.min(centers-DEPTH*r)), float(np.max(centers+DEPTH*r)), 1801)
    heights = np.sqrt(np.maximum(0, np.max(r[:, None]**2 - ((sx[None,:]-centers[:,None])/DEPTH)**2, axis=0)))
    curve(d, np.vstack((np.c_[sx,BASELINE-heights], np.c_[sx[::-1],BASELINE+heights[::-1]])), (*GOLD,155), 1.2)
    line(d, (LEFT-6, BASELINE), (RIGHT+6, BASELINE), (*FAINT,180))
    for xx, label, color, shift in ((X1,"x₁",BLUE,-10),(X2,"x₂",RED,10)):
        xp = float(screen_x(xx))
        for yy in np.arange(286, 674, 9):
            line(d, (xp, yy), (xp, yy+4), (*color,60), .8)
        text(d, (xp+shift, 679), label, 21, color, anchor="ma")
        # A thin fixed cross section identifies each sampled position; no beads.
        z = abs(base_at(xx)) * np.exp(1j*np.linspace(0,2*np.pi,151))
        curve(d, project(np.full_like(z.real,xx),z), (*color,80), .9)
    text(d, (RIGHT+11, BASELINE), "x", 19, MUTED, anchor="lm")
    # The key follows the same parallel projection as the actual curve.
    origin=np.array([111.,355.])
    for label,unit,length in (("Re ψ",1+0j,45),("Im ψ",1j,60)):
        z=unit*VIEW
        end=origin+length*np.array([DEPTH*z.imag,-z.real])
        arrow(d,origin,end,MUTED,1,5)
        offset=(-31,-22) if label=="Re ψ" else (6,-14)
        text(d,end+np.array(offset),label,15,MUTED)
    line(d, (63, 725), (89, 725), GOLD, 1.4)
    text(d, (99, 714), "Fixed magnitude envelope", 18, GOLD)
    text(d, (62, 765), "Added phase α(x)", 18, MUTED)
    line(d, (LEFT, 859), (RIGHT, 859), FAINT)
    text(d, (RIGHT+11, 859), "x", 17, MUTED, anchor="lm")
    text(d, (58, 884), "Position and radius stay fixed. Each complex value turns.", 17, MUTED)

    text(d, (971, 165), "Compare two fixed positions", 25, bold=True)
    text(d, (973, 207), "Unit arrows show phase only", 18, MUTED)
    for center, label, color in (((1090,338),"At x₁",BLUE),((1420,338),"At x₂",RED)):
        phase_circle(d, center, 72)
        text(d, (center[0],242), label, 20, color, anchor="ma")
    text(d, (1255,432), "Raw phase difference", 17, MUTED, anchor="ma")
    line(d, (976, 492), (1542, 492), BORDER)
    text(d, (971, 511), "Include the connection", 24, bold=True)
    formula(img, (1255,555), r"$\beta=\frac{q}{\hbar}\int_{x_1}^{x_2} A_x\,dx$", 22, GOLD, center=True)
    phase_circle(d, (1255,726), 96)
    text(d, (982, 638), "x₁ phase", 17, BLUE)
    text(d, (982, 663), "+ connection", 17, GOLD)
    text(d, (1412, 638), "x₂ phase", 17, RED)
    text(d, (1255, 867), "Corrected phase difference", 18, GREEN, anchor="ma")
    text(d, (36, 947), "Changing gauge s · not physical time", 18, MUTED)
    text(d, (1565, 947), "One spatial snapshot · no electromagnetic field is created", 17, MUTED, anchor="ra")
    return img


def frame(seconds):
    c,g,stage = state(seconds)
    alpha = c + g * f(X)
    values = BASE * np.exp(1j*alpha)
    img = background().copy()
    d = ImageDraw.Draw(img, "RGBA")
    text(d, (1560, 37), stage, 21, BLUE, anchor="ra")
    pts = project(X, values)
    depth = (values * VIEW).imag
    front = depth[:-1]+depth[1:] >= 0
    cuts = np.r_[0, np.flatnonzero(front[1:] != front[:-1])+1, len(front)]
    for side, col in ((False,tuple(round(.45*b+.55*p) for b,p in zip(BLUE,PANEL))), (True,BLUE)):
        for a,b in zip(cuts[:-1],cuts[1:]):
            if bool(front[a])==side:
                curve(d,pts[a:b+1],col,2.5)
    # Added phase is unwrapped; identical x scale ties profile to the spiral.
    curve(d,np.c_[screen_x(X),859-7*alpha],GREEN,2)
    for xx,col in ((X1,BLUE),(X2,RED)):
        line(d,(float(screen_x(xx)),859),(float(screen_x(xx)),859-7*(c+g*f(xx))),(*col,130),1)
    a1,a2 = THETA1+c+g*f(X1), THETA2+c+g*f(X2)
    beta = g*(f(X2)-f(X1))
    for center,angle,col in (((1090,338),a1,BLUE),((1420,338),a2,RED)):
        arrow(d,center,tip(center,67,angle),col,3.2,10)
    raw = float(np.angle(np.exp(1j*(a2-a1))))
    text(d,(1255,456),f"{math.degrees(raw):+.1f}°",24,INK,anchor="ma")
    center=(1255,726)
    dashed_arrow(d,center,90,a1,(*BLUE,110))
    arc(d,center,119,a1,beta,GOLD,2,True)
    arrow(d,center,tip(center,91,a1+beta),GOLD,3.5,10)
    arrow(d,center,tip(center,91,a2),RED,3.5,10)
    # Wedge is calculated from the actual transported comparison, not forced.
    corrected = float(np.angle(np.exp(1j*(a2-a1-beta))))
    angles=np.linspace(a1+beta,a1+beta+corrected,42)
    wedge=[center,*[tip(center,46,a) for a in angles]]
    d.polygon([px(p) for p in wedge],fill=(*GREEN,35))
    arc(d,center,46,a1+beta,corrected,GREEN,2)
    text(d,(1539,575),f"β = {math.degrees(beta):+.0f}°",16,GOLD,anchor="ra")
    text(d,(1255,891),f"{math.degrees(corrected):.1f}°  ·  unchanged",21,GREEN,anchor="ma")
    return img.resize((W,H),Image.Resampling.LANCZOS)


def check():
    derivative=np.sum(1j*source.K[:,None]*source.BASE_MODES,axis=0)
    base_current=np.imag(np.conj(BASE)*derivative)
    errors={k:0. for k in ("density","covariant_derivative","current","finite_phase_comparison","link_quadrature")}
    xx=np.linspace(X1,X2,10001)
    trap=np.trapezoid
    for seconds in np.linspace(0,DURATION,241):
        c,g,_=state(seconds)
        phase=np.exp(1j*(c+g*f(X)))
        psi=phase*BASE
        dpsi=phase*(derivative+1j*g*fp(X)*BASE)
        covariant=dpsi-1j*g*fp(X)*psi
        beta=g*(f(X2)-f(X1))
        link=np.exp(1j*beta)
        z1=Z1*np.exp(1j*(c+g*f(X1)))
        z2=Z2*np.exp(1j*(c+g*f(X2)))
        e={"density":np.max(abs(abs(psi)**2-abs(BASE)**2)),
           "covariant_derivative":np.max(abs(covariant-phase*derivative)),
           "current":np.max(abs(np.imag(np.conj(psi)*covariant)-base_current)),
           "finite_phase_comparison":abs(z2/(link*z1)-Z2/Z1),
           "link_quadrature":abs(trap(g*fp(xx),xx)-beta)}
        for key,val in e.items(): errors[key]=max(errors[key],float(val))
        coords=project(X,psi)
        assert np.all(coords[:,0]>45) and np.all(coords[:,0]<911)
        assert np.all(coords[:,1]>275) and np.all(coords[:,1]<675)
    assert max(errors.values())<1e-7,errors
    # A negative control: keeping A_x=0 under local rephasing changes current.
    phase=np.exp(1j*f(X))
    uncompensated=np.imag(np.conj(phase*BASE)*phase*(derivative+1j*fp(X)*BASE))
    assert np.max(abs(uncompensated-base_current))>1
    report={"max_errors":errors,"current_units":"hbar/m",
      "x1":X1,"x2":X2,"fixed_corrected_angle_degrees":float(np.degrees(DELTA)),
      "definition":"D=partial-i(q/hbar)A, alpha=c+g f, (q/hbar)A=g fprime",
      "transport":"exp(+i beta), beta=(q/hbar) integral A dx",
      "interpretation":"Gauge parameter, not time evolution; pure gauge on a spatial interval; no EM field generated.",
      "input_function":"Exact accepted nine-mode sum, unchanged normalization.",
      "fps":FPS,"duration":DURATION,"frames":FRAMES,"size":[W,H]}
    out.mkdir(parents=True,exist_ok=True)
    (out/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new("RGB",(1600,1500),BG)
    for i,s in enumerate(SAMPLES):
        sheet.paste(frame(s).resize((800,500),Image.Resampling.LANCZOS),((i%2)*800,(i//2)*500))
    sheet.save(out/f"{NAME}-contact-sheet.png")
    frame(10).save(out/f"{NAME}-poster.png")
    print(str(out/f"{NAME}-poster.png"),flush=True)


def render():
    out.mkdir(parents=True,exist_ok=True)
    target=out/f"{NAME}.mp4"
    args=[source.imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats","-f","rawvideo","-pix_fmt","rgb24",
          "-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast","-crf","18",
          "-pix_fmt","yuv420p","-movflags","+faststart",str(target)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    started=time.perf_counter()
    try:
        for i in range(FRAMES):
            proc.stdin.write(frame(i/FPS).tobytes())
            if i%(FPS*4)==0: print(f"{i/FPS:.0f}/{DURATION}s; render {time.perf_counter()-started:.1f}s",flush=True)
        proc.stdin.close()
        error=proc.stderr.read().decode(errors="replace")
        if proc.wait(): raise RuntimeError(error)
    except BaseException:
        proc.kill(); proc.wait(); raise
    print(str(target),flush=True)


def encoded_check():
    reader=source.imageio_ffmpeg.read_frames(str(out/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta=next(reader)
    assert tuple(meta["size"])==(W,H) and abs(meta["fps"]-FPS)<1e-8
    wanted={round(s*FPS) for s in SAMPLES}
    sheet=Image.new("RGB",(1600,1500),BG)
    errors=[]
    count=0
    for i,raw in enumerate(reader):
        count+=1
        if i not in wanted: continue
        pic=Image.frombytes("RGB",(W,H),raw)
        err=float(np.mean(abs(np.asarray(pic).astype(float)-np.asarray(frame(i/FPS)).astype(float))))
        assert err<2.5
        n=len(errors)
        sheet.paste(pic.resize((800,500),Image.Resampling.LANCZOS),((n%2)*800,(n//2)*500))
        errors.append(err)
    assert count==FRAMES and len(errors)==len(wanted)
    sheet.save(out/f"{NAME}-encoded-contact-sheet.png")
    report={"frames":count,"duration":count/FPS,"max_encoded_pixel_error":max(errors),"size":meta["size"]}
    (out/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"): p.add_argument("--"+flag,action="store_true")
    args=p.parse_args()
    if args.check: check()
    if args.preview: preview()
    if args.render: render()
    if args.encoded_check: encoded_check()
