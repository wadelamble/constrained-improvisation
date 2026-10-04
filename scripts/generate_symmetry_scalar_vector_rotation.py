"""Active rotations of a scalar field and a vector field on a fixed plane.

The same positive asymmetric function f supplies the left scalar field and
the magnitude of the right vector field. Contours therefore mark f on the
left and |V| on the right. This is a deliberately chosen pair of examples,
not a claim that vector fields are determined by scalar fields.

Governing actions: f_R(x)=f(R^-1 x), V_R(x)=R V(R^-1 x).
The tracked point p moves to Rp. Its scalar value and vector norm are
invariant; its vector direction and fixed-axis components rotate. Playback
follows the rotation parameter, not a solution evolving in physical time.

Timing: 0 degrees 0--3 s; turn to 90 degrees 3--8 s; hold 8--11 s;
turn to 180 degrees 11--16 s; hold 16--20 s. No manuscript is edited.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from io import BytesIO
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-scalar-vector-rotation"
WIDTH, HEIGHT, SS = 1440, 900, 2
FPS, DURATION = 30, 20.0
FRAMES = round(FPS * DURATION)
BG, PANEL = (253, 250, 244), (250, 247, 240)
INK, MUTED, BORDER = (37, 38, 40), (105, 103, 98), (217, 211, 201)
BLUE, GOLD, AXIS = (43, 93, 145), (181, 118, 22), (209, 204, 196)
CENTERS = (np.array([366., 451.]), np.array([1074., 451.]))
PLOT_SCALE = 87.0
AXIS_EXTENT = 2.62
ARROW_SCALE = 93.0
P = np.array([1.02, .34])
LEVELS = (.12, .24, .40, .58, .76)
TIMES = (0.0, 5.5, 9.5, 13.5, 17.0, 19.9666666667)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf",
                 "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, round(size * SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(values):
    return tuple(round(v * SS) for v in values)


def text(draw, pos, value, size=20, color=INK, bold=False, anchor=None):
    draw.text(px(pos), value, font=font(size, bold), fill=color, anchor=anchor)


def line(draw, a, b, color, width=1):
    draw.line(px((*a, *b)), fill=color, width=max(1, round(width * SS)))


def polyline(draw, points, color, width=1):
    draw.line([px(p) for p in points], fill=color,
              width=max(1, round(width * SS)), joint="curve")


def arrow(draw, start, end, color, width=2, head=8):
    start, end = np.asarray(start), np.asarray(end)
    delta = end - start
    length = float(np.linalg.norm(delta))
    if length < .4:
        return
    direction = delta / length
    side = np.array([-direction[1], direction[0]])
    head = min(head, length * .42)
    line(draw, start, end, color, width)
    draw.polygon([px(end), px(end - head*direction + .43*head*side),
                  px(end - head*direction - .43*head*side)], fill=color)


@lru_cache(None)
def formula(value, size=25, color=INK):
    buffer = BytesIO()
    math_to_image("$" + value + "$", buffer, dpi=144,
                  prop=FontProperties(size=size), format="png",
                  color=tuple(c/255 for c in color))
    image = Image.open(buffer).convert("RGBA")
    # math_to_image uses a white opaque canvas. Recover antialiased text
    # opacity, then tint it explicitly to avoid a white formula rectangle.
    rgba = np.asarray(image).copy()
    alpha = 255 - np.min(rgba[:, :, :3], axis=2)
    darkest = 255 - min(color)
    rgba[:, :, 3] = np.minimum(255, np.round(alpha * (255. / darkest))).astype(np.uint8)
    rgba[:, :, :3] = color
    image = Image.fromarray(rgba)
    box = image.getbbox()
    return image.crop(box)


def put_formula(image, at, value, size=25, color=INK):
    art = formula(value, size, color)
    image.paste(art, px(at), art)
    return art.size


def rotation(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]])


def scalar(q):
    q = np.asarray(q)
    x, y = q[..., 0], q[..., 1]
    c, s = math.cos(.35), math.sin(.35)
    u, v = c*(x-.8) + s*(y-.35), -s*(x-.8) + c*(y-.35)
    return .86*np.exp(-.5*((u/.72)**2 + (v/.42)**2)) + \
        .48*np.exp(-.5*(((x+.85)/.44)**2 + ((y+.62)/.61)**2))


def vector(q):
    q = np.asarray(q)
    phase = .3*(q[..., 0] - P[0]) - .2*(q[..., 1] - P[1])
    return scalar(q)[..., None] * np.stack((np.cos(phase), np.sin(phase)), axis=-1)


def transformed_scalar(q, theta):
    return scalar(np.asarray(q) @ rotation(theta))


def transformed_vector(q, theta):
    r = rotation(theta)
    return vector(np.asarray(q) @ r) @ r.T


def ease(t):
    t = float(np.clip(t, 0, 1))
    return t*t*(3-2*t)


def angle(seconds):
    if seconds <= 3:
        return 0.
    if seconds < 8:
        return math.pi/2 * ease((seconds-3)/5)
    if seconds <= 11:
        return math.pi/2
    if seconds < 16:
        return math.pi/2 * (1 + ease((seconds-11)/5))
    return math.pi


def screen(q, col):
    return CENTERS[col] + np.asarray(q)*np.array([PLOT_SCALE, -PLOT_SCALE])


@lru_cache(None)
def contours():
    x = np.linspace(-2.7, 2.7, 701)
    xx, yy = np.meshgrid(x, x)
    z = scalar(np.stack((xx, yy), axis=-1))
    fig, ax = plt.subplots()
    cs = ax.contour(xx, yy, z, levels=LEVELS)
    paths = tuple(tuple(seg.copy() for seg in level) for level in cs.allsegs)
    plt.close(fig)
    return paths


@lru_cache(None)
def arrow_nodes():
    points = np.array([(x, y) for x in np.arange(-1.6, 1.81, .44)
                       for y in np.arange(-1.45, 1.51, .44)])
    # Avoid an unreadable forest in the tails and leave room for the gold
    # tracked arrow. Selection happens once; nodes travel with the field.
    mask = (scalar(points) > .17) & (np.linalg.norm(points-P, axis=1) > .43)
    return points[mask]


@lru_cache(None)
def backdrop():
    image = Image.new("RGB", (WIDTH*SS, HEIGHT*SS), BG)
    draw = ImageDraw.Draw(image, "RGBA")
    text(draw, (38, 22), "Rotating scalar and vector fields", 32, bold=True)
    text(draw, (40, 73), "Active rotation · fixed coordinate axes", 19, MUTED)
    for col, title in enumerate(("Scalar field", "Vector field")):
        left = 28 + 708*col
        draw.rounded_rectangle(px((left, 117, left+676, 809)), radius=14*SS,
                               fill=PANEL, outline=BORDER, width=SS)
        text(draw, (left+24, 135), title, 26, bold=True)
        value = r"f_R(\mathbf{x})=f(R^{-1}\mathbf{x})" if col == 0 else \
            r"\mathbf{V}_R(\mathbf{x})=R\,\mathbf{V}(R^{-1}\mathbf{x})"
        put_formula(image, (left+25, 179), value, 25)
        cx, cy = CENTERS[col]
        # Axes and labels are fixed while all field samples rotate.
        for dim in range(2):
            a = np.zeros(2); b = np.zeros(2)
            a[dim], b[dim] = -AXIS_EXTENT, AXIS_EXTENT
            arrow(draw, screen(a,col), screen(b,col), AXIS, 1.1, 6)
        for tick in (-2, -1, 1, 2):
            x, y = screen((tick, 0), col)
            line(draw, (x,y-3), (x,y+3), AXIS)
            x, y = screen((0, tick), col)
            line(draw, (x-3,y), (x+3,y), AXIS)
        text(draw, (cx+244, cy-2), "x", 18, MUTED, anchor="mm")
        text(draw, (cx, cy-246), "y", 18, MUTED, anchor="mm")
        text(draw, (left+27, 689), "Tracked point  p → Rp", 18, MUTED)
        line(draw, (left+24, 729), (left+652, 729), BORDER, .9)
        contour_text = "Contours: f" if col == 0 else "Contours: |V| = f"
        text(draw, (left+651, 689), contour_text, 17, MUTED, anchor="ra")
    put_formula(image, (55, 751), r"f_R(R\mathbf{p})=f(\mathbf{p})", 24)
    put_formula(image, (763, 748), r"\mathbf{V}_R(R\mathbf{p})=R\,\mathbf{V}(\mathbf{p})", 22)
    text(draw, (40, 831), "The marked point moves with the field.", 17, MUTED)
    text(draw, (1400, 831), "Playback follows the rotation angle.", 17, MUTED, anchor="ra")
    return image


def signed(value):
    if abs(value) < .0005:
        value = 0.
    return f"{value:+.2f}".replace("-", "−")


def frame(seconds):
    theta = angle(seconds)
    r = rotation(theta)
    image = backdrop().copy()
    draw = ImageDraw.Draw(image, "RGBA")
    degrees = math.degrees(theta)
    text(draw, (1399, 39), f"θ = {degrees:05.1f}°", 30, GOLD, anchor="ra")
    # Directly rotate all contour vertices: this is exactly the inverse-
    # argument field rule, without interpolating a rotated raster image.
    for col in range(2):
        for level, paths in zip(LEVELS, contours()):
            opacity = 155 if col == 0 else 89
            for path in paths:
                polyline(draw, screen(path @ r.T, col), (*BLUE, opacity), 1.45)
        # The original point is a faint, fixed reference ring. The dotted
        # circular track makes corresponding positions unmistakable.
        arc = np.array([rotation(t) @ P for t in np.linspace(0, math.pi, 181)])
        for i in range(0, len(arc)-3, 6):
            polyline(draw, screen(arc[i:i+3], col), (*GOLD, 70), 1.0)
        old = screen(P, col)
        draw.ellipse(px((* (old-5.5), * (old+5.5))), outline=(*GOLD, 90), width=SS)
        if col:
            nodes = arrow_nodes()
            locations = nodes @ r.T
            vectors = vector(nodes) @ r.T
            for q, v in zip(locations, vectors):
                tail = screen(q, col)
                end = tail + ARROW_SCALE*v*np.array([1.,-1.])
                arrow(draw, tail, end, (*BLUE, 225), 1.9, 7)
        moved = r @ P
        point = screen(moved, col)
        if col:
            v = transformed_vector(moved, theta)
            tip = point + ARROW_SCALE*v*np.array([1., -1.])
            arrow(draw, point, tip, (*PANEL, 255), 8.5, 15)
            arrow(draw, point, tip, GOLD, 4.5, 14)
        draw.ellipse(px((* (point-6.2), * (point+6.2))), fill=GOLD,
                     outline=PANEL, width=round(1.5*SS))
        # The label stays radially inward, away from the gold arrow and
        # outside header/readout areas, rather than jumping between sides.
        radial = moved/np.linalg.norm(moved)
        label_at = point - 27*radial*np.array([1.,-1.])
        label = "p" if theta < 1e-12 else "Rp"
        box = draw.textbbox(px(label_at), label, font=font(17), anchor="mm")
        draw.rounded_rectangle((box[0]-5*SS, box[1]-2*SS, box[2]+5*SS, box[3]+2*SS),
                               radius=3*SS, fill=(*PANEL, 240))
        text(draw, label_at, label, 17, GOLD, anchor="mm")
    value = float(scalar(P))
    text(draw, (676, 749), f"= {value:.2f}", 29, GOLD, bold=True, anchor="ra")
    v = transformed_vector(r @ P, theta)
    text(draw, (1380, 748), f"= ({signed(v[0])}, {signed(v[1])})", 23, GOLD, bold=True, anchor="ra")
    text(draw, (1380, 781), f"|V| = {value:.2f}", 15, MUTED, anchor="ra")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def check():
    rng = np.random.default_rng(8410)
    q = rng.uniform(-2.2, 2.2, (300, 2))
    scalar_error = vector_error = norm_error = group_error = 0.
    point_errors = []
    for theta in np.linspace(-2*math.pi, 2*math.pi, 129):
        r = rotation(theta)
        moved = q @ r.T
        scalar_error = max(scalar_error, float(np.max(abs(transformed_scalar(moved,theta)-scalar(q)))))
        vector_error = max(vector_error, float(np.max(abs(transformed_vector(moved,theta)-vector(q)@r.T))))
        norm_error = max(norm_error, float(np.max(abs(np.linalg.norm(transformed_vector(moved,theta),axis=1)-scalar(q)))))
        point_errors.append(abs(float(transformed_scalar(r@P,theta))-float(scalar(P))))
        phi = .71
        # Apply S after R at fixed x, including both component matrices.
        combined = transformed_vector(q @ rotation(phi), theta) @ rotation(phi).T
        direct = transformed_vector(q, theta+phi)
        group_error = max(group_error, float(np.max(abs(combined-direct))))
    assert max(scalar_error,vector_error,norm_error,group_error,*point_errors) < 2e-14
    expected = float(scalar(P))*np.array([[1,0],[0,1],[-1,0]])
    actual = np.array([transformed_vector(rotation(t)@P,t) for t in (0,math.pi/2,math.pi)])
    assert np.max(abs(actual-expected)) < 1e-14
    # All drawn field vertices and arrow tips stay inside the panel plot
    # zone throughout the turn. Text has separate reserved bands.
    all_paths = np.concatenate([p for paths in contours() for p in paths])
    nodes, vv = arrow_nodes(), vector(arrow_nodes())
    margin = math.inf
    for theta in np.linspace(0,math.pi,181):
        r = rotation(theta)
        for col in range(2):
            verts = screen(all_paths @ r.T, col)
            tails = screen(nodes @ r.T, col)
            tips = tails + ARROW_SCALE*(vv @ r.T)*np.array([1.,-1.])
            gold = screen(r@P,col) + ARROW_SCALE*(r@vector(P))*np.array([1.,-1.])
            points = np.vstack((verts, tails, tips, gold))
            left = 28 + col*708
            margins = np.column_stack((points[:,0]-(left+24), (left+652)-points[:,0],
                                       points[:,1]-235, 676-points[:,1]))
            margin = min(margin,float(np.min(margins)))
    assert margin > 5
    assert abs(angle(3)) < 1e-15 and angle(8)==angle(11)==math.pi/2
    assert angle(16)==angle(20)==math.pi
    report = {"action":"active rotation on fixed coordinate axes",
              "scalar_rule":"f_R(x)=f(R^-1 x)", "vector_rule":"V_R(x)=R V(R^-1 x)",
              "scalar_correspondence_error":scalar_error,"vector_correspondence_error":vector_error,
              "vector_norm_error":norm_error,"vector_group_composition_error":group_error,
              "tracked_scalar":float(scalar(P)),"tracked_vector_at_0_90_180_degrees":actual.tolist(),
              "minimum_field_geometry_margin_px":margin,"vector_sample_count":len(nodes),
              "contour_levels":LEVELS,"duration":DURATION,"fps":FPS,"size":[WIDTH,HEIGHT],
              "frames":FRAMES,"note":"Chosen example has |V(x)|=f(x). All spatial patterns rotate; only vector values carry direction."}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet = Image.new("RGB", (1440, 1404), BG)
    for i, t in enumerate(TIMES):
        pic = frame(t)
        x,y = (i%2)*720,(i//2)*468
        sheet.paste(pic.resize((720,450),Image.Resampling.LANCZOS),(x,y))
        ImageDraw.Draw(sheet).text((x+14,y+451),f"{t:.1f} s",fill=MUTED)
    frame(9.5).save(OUT/f"{NAME}-poster.png")
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True,exist_ok=True)
    output = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
               "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
               "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast",
               "-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    started = time.perf_counter()
    key,rgb = None,None
    try:
        for i in range(FRAMES):
            theta = angle(i/FPS)
            if theta != key:
                rgb = frame(i/FPS).tobytes()
                key = theta
            process.stdin.write(rgb)
            if i%(3*FPS)==0:
                print(f"{i/FPS:g}/{DURATION:g}s; elapsed {time.perf_counter()-started:.1f}s",flush=True)
        process.stdin.close()
        error = process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill(); process.wait()
        raise
    print(str(output),flush=True)


def encoded_check():
    reader = imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    meta = next(reader)
    assert tuple(meta["size"]) == (WIDTH,HEIGHT) and meta["fps"] == FPS
    indices = {min(FRAMES-1,round(t*FPS)) for t in TIMES}
    sheet = Image.new("RGB", (1440,1350), BG)
    count, errors, moves = 0, [], []
    previous = None
    for i,raw in enumerate(reader):
        count += 1
        if i in indices:
            decoded = np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
            expected = np.asarray(frame(i/FPS))
            error = float(np.mean(abs(decoded.astype(float)-expected.astype(float))))
            assert error < 2.0
            slot = len(errors)
            art = Image.fromarray(decoded.copy())
            sheet.paste(art.resize((720,450),Image.Resampling.LANCZOS),((slot%2)*720,(slot//2)*450))
            if previous is not None:
                moves.append(float(np.mean(abs(decoded.astype(float)-previous.astype(float)))))
            previous = decoded.copy()
            errors.append(error)
            if i == round(9.5*FPS):
                art.save(OUT/f"{NAME}-encoded-sample.png")
    assert count == FRAMES and len(errors)==len(indices)
    assert min(moves[:4]) > .25
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report = {"decoded_frames":count,"duration":count/FPS,"size":meta["size"],
              "fps":meta["fps"],"max_decoded_rgb_error":max(errors),
              "sample_frame_differences":moves}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    args = parser.parse_args()
    if args.check: check()
    if args.preview: preview()
    if args.render: render()
    if args.encoded_check: encoded_check()
