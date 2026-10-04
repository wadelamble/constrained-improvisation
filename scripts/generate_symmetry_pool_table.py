"""One exact billiard collision under four Galilean spacetime symmetries.

The two panels replay the same equal-mass, perfectly elastic disk collision.
The model omits friction and spin and ends before a cushion is reached. This
illustrates symmetry of a specified dynamics; it is not a derivation of inertia.
World coordinates obey x' = R x + a + u t and t' = t + b. Setup transformations
are eased only while playback is paused. During each shot, elapsed time and
the boosted table's displacement advance linearly. Colored trails are paths
marked on the table, not world-space tracks left behind by the moving table.

Run with the scientific Python runtime:
    python scripts/generate_symmetry_pool_table.py --check --preview
    python scripts/generate_symmetry_pool_table.py --render --encoded-check
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
sys.path.insert(0, str(ROOT / ".tools" / "animation-python-packages"))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import matplotlib
matplotlib.use("Agg")
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-pool-table"
W, H, SS, FPS = 1600, 960, 2, 30
PLAYBACK_SPEED = 2.0
STAGE_TIME, PREPARE, PLAY_TIME = (t / PLAYBACK_SPEED for t in (7.0, 1.1, 4.8))
DURATION = STAGE_TIME * 4
FRAMES = round(DURATION * FPS)
BG, PANEL = "#fdfaf4", "#faf7f0"
INK, MUTED, BORDER = "#252628", "#6f6c66", "#dad3c8"
BLUE, GOLD = "#2b5d91", "#c08019"
BLUE_FAINT, GOLD_FAINT = "#9baec1", "#d7bd8a"
FELT, RAIL = "#eef1e7", "#bdb6a8"
COLORS, TRAIL_COLORS = (BLUE, GOLD), (BLUE_FAINT, GOLD_FAINT)
PANEL_BOXES = ((40, 170, 780, 788), (820, 170, 1560, 788))
SCALE = 76.0
RADIUS = .14
CONTACT_TIME, END_TIME = 1.48, 2.78
Q0 = np.array([[-2.0, -.45], [0.0, -.282]])
V0 = np.array([[1.2, 0.0], [0.0, 0.0]])
NORMAL = np.array([.8, .6])
IMPULSE = float((V0[0] - V0[1]) @ NORMAL) * NORMAL
V1 = V0 + np.array([-IMPULSE, IMPULSE])
QC = Q0 + V0 * CONTACT_TIME
SCENES = ("Position translation", "Time translation", "Rotation", "Velocity boost")
PANE_LABELS = ("Moved elsewhere", "Started later", "Turned", "Moving steadily")
FORMULAS = (
    r"\mathbf{x}'(t)=\mathbf{x}(t)+\mathbf{a}",
    r"\mathbf{x}'(t+b)=\mathbf{x}(t)",
    r"\mathbf{x}'(t)=R\,\mathbf{x}(t)",
    r"\mathbf{x}'(t)=\mathbf{x}(t)+\mathbf{u}t",
)
CHECK_TIMES = tuple(t / PLAYBACK_SPEED for t in (2.0, 5.0, 9.0, 12.0, 16.0, 19.0, 23.0, 26.0))


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf",
                 str(Path(matplotlib.get_data_path()) / "fonts" / "ttf" /
                     ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"))):
        try:
            return ImageFont.truetype(name, round(size * SS))
        except OSError:
            pass
    return ImageFont.load_default()


def px(seq):
    return tuple(round(float(v) * SS) for v in seq)


def text(d, xy, label, size=24, color=INK, bold=False, anchor="la"):
    d.text(px(xy), label, font=font(size, bold), fill=color, anchor=anchor)


def line(d, points, color, width=2):
    d.line([px(p) for p in points], fill=color,
           width=max(1, round(width * SS)), joint="curve")


def arrow(d, start, end, color, width=2.3, head=9):
    start, end = np.asarray(start), np.asarray(end)
    delta = end - start
    length = np.linalg.norm(delta)
    if length < .1:
        return
    e = delta / length
    n = np.array([-e[1], e[0]])
    head = min(head, .4 * length)
    line(d, [start, end], color, width)
    d.polygon([px(end), px(end - e * head + n * head * .43),
               px(end - e * head - n * head * .43)], fill=color)


@lru_cache(None)
def math_image(tex, size=32):
    stream = BytesIO()
    math_to_image("$" + tex + "$", stream, format="png", dpi=150,
                  color=INK, prop=FontProperties(size=size * SS * 72 / 150))
    stream.seek(0)
    return Image.open(stream).convert("RGBA")


def formula(im, tex, center, size=32):
    pic = math_image(tex, size)
    xy = px(center)
    im.paste(pic, (xy[0] - pic.width // 2, xy[1] - pic.height // 2), pic)


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s], [s, c]])


def trajectory(t):
    t = np.asarray(t)
    return (Q0 + np.minimum(t, CONTACT_TIME)[..., None, None] * V0
            + np.maximum(t - CONTACT_TIME, 0)[..., None, None] * V1)


def velocities(t):
    return V0 if t < CONTACT_TIME else V1


def transform(stage, prepare=1.0):
    r, a, u, b = np.eye(2), np.zeros(2), np.zeros(2), 0.0
    if stage == 0:
        a = np.array([.85, .4]) * prepare
    elif stage == 1:
        b = 10.0 * prepare
    elif stage == 2:
        r = rotation(math.radians(32) * prepare)
    else:
        u = np.array([.65, 0.0])
    return r, a, u, b


def movie_state(seconds):
    stage = min(int(seconds / STAGE_TIME), 3)
    local = seconds - stage * STAGE_TIME
    s = min(max(local / PREPARE, 0), 1)
    setup = s * s * (3 - 2 * s)
    elapsed = float(np.clip((local - PREPARE) / PLAY_TIME, 0, 1)) * END_TIME
    return stage, local, setup, elapsed


def screen(points, panel, stage):
    origin = np.array([410 + panel * 780, 494.0])
    if stage == 3:
        origin[0] -= 45
    return origin + np.asarray(points) * np.array([SCALE, -SCALE])


def table_points(points, stage, elapsed, setup, transformed):
    if not transformed:
        return np.asarray(points)
    r, a, u, _ = transform(stage, setup)
    return np.asarray(points) @ r.T + a + u * elapsed


def draw_world_grid(d, panel, stage):
    left, top, right, bottom = PANEL_BOXES[panel]
    # Stationary world marks make the continuously moving table visible.
    for gx in range(-6, 7):
        for gy in range(-3, 4):
            x, y = screen([gx, gy], panel, stage)
            if left + 20 < x < right - 20 and 247 < y < 733:
                line(d, [(x-3, y), (x+3, y)], "#e4dfd5", 1)
                line(d, [(x, y-3), (x, y+3)], "#e4dfd5", 1)
    origin = screen([0, 0], panel, stage)
    d.ellipse(px((origin[0]-3, origin[1]-3, origin[0]+3, origin[1]+3)),
              fill=BORDER)


def draw_table(d, stage, elapsed, setup, panel):
    transformed = panel == 1
    def project(p):
        return screen(table_points(p, stage, elapsed, setup, transformed), panel, stage)

    outer = np.array([[-3.15, -1.65], [3.15, -1.65], [3.15, 1.65], [-3.15, 1.65]])
    inner = np.array([[-3., -1.5], [3., -1.5], [3., 1.5], [-3., 1.5]])
    d.polygon([px(p) for p in project(outer)], fill="#e2ddd2")
    d.polygon([px(p) for p in project(inner)], fill=FELT)
    line(d, list(project(outer)) + [project(outer)[0]], RAIL, 2)
    line(d, list(project(inner)) + [project(inner)[0]], "#9da892", 1.6)

    # Six small diamonds establish the table's own coordinates without
    # introducing pockets, which this idealized collision does not model.
    for x in (-1.5, 0.0, 1.5):
        for y in (-1.58, 1.58):
            p = project([x, y])
            d.ellipse(px((p[0]-2.2, p[1]-2.2, p[0]+2.2, p[1]+2.2)), fill=MUTED)

    if elapsed < .03:
        cue = np.array([[-2.92, -.45], [-2.20, -.45]])
        line(d, project(cue), "#aa9173", 5)
        line(d, project(cue[-1:] + [[-.05, 0]]) .tolist() + [project(cue[-1])], BLUE, 5)

    times = np.unique(np.r_[np.linspace(0, elapsed, 70),
                              [CONTACT_TIME] if elapsed >= CONTACT_TIME else []])
    trails = trajectory(times)
    for ball in range(2):
        if len(times) > 1:
            line(d, project(trails[:, ball]), TRAIL_COLORS[ball], 2.4)
        start = project(Q0[ball])
        d.ellipse(px((start[0]-3.1, start[1]-3.1, start[0]+3.1, start[1]+3.1)),
                  fill=TRAIL_COLORS[ball])

    q = trajectory(elapsed)
    for ball, color in enumerate(COLORS):
        p = project(q[ball])
        rr = RADIUS * SCALE
        d.ellipse(px((p[0]-rr, p[1]-rr, p[0]+rr, p[1]+rr)), fill=color,
                  outline=INK, width=SS)
        d.ellipse(px((p[0]-rr*.43, p[1]-rr*.45, p[0]-rr*.08, p[1]-rr*.10)),
                  fill="#f8f6ec")

    if panel == 1 and stage == 3:
        a = project([-1.0, -1.93])
        z = project([.65, -1.93])
        arrow(d, a, z, INK, 2.2, 10)
        text(d, ((a[0]+z[0])/2, a[1]+11), "constant velocity", 19, MUTED, anchor="ma")


def frame(seconds):
    stage, local, setup, elapsed = movie_state(seconds)
    im = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(im)
    text(d, (48, 31), "The same experiment", 40, INK, True)
    text(d, (1552, 48), "SYMMETRY", 21, MUTED, anchor="ra")
    for i, label in enumerate(SCENES):
        x0 = 40 + 390 * i
        active = i == stage
        d.rounded_rectangle(px((x0, 98, x0 + 360, 143)), radius=13*SS,
                            fill="#ebe4d8" if active else PANEL)
        text(d, (x0 + 180, 106), label, 23,
             INK if active else MUTED, active, anchor="ma")

    r, a, u, offset = transform(stage, setup)
    for panel, box in enumerate(PANEL_BOXES):
        d.rounded_rectangle(px(box), radius=20*SS, fill=PANEL, outline=BORDER, width=SS)
        text(d, (box[0]+27, 190), "Reference" if panel == 0 else PANE_LABELS[stage],
             27, INK, True)
        clock = elapsed + (offset if panel else 0)
        text(d, (box[2]-26, 194), f"clock  {clock:05.2f} s", 22, MUTED, anchor="ra")
        draw_world_grid(d, panel, stage)
        draw_table(d, stage, elapsed, setup, panel)
        separation = float(np.linalg.norm(trajectory(elapsed)[1] - trajectory(elapsed)[0]))
        text(d, (box[0]+27, 752), f"Elapsed after shot   {elapsed:.2f} s", 20, MUTED)
        text(d, (box[2]-26, 752), f"separation   {separation:.2f}", 20, MUTED, anchor="ra")

    formula(im, FORMULAS[stage], (800, 827), 33)
    message = "Preparing the comparison" if local < PREPARE else "Same collision. Same paths relative to the table."
    text(d, (800, 868), message, 23, MUTED, anchor="ma")
    line(d, [(50, 921), (1550, 921)], BORDER, 2)
    line(d, [(50, 921), (50+1500*min(seconds/DURATION, 1), 921)], BLUE, 2.5)
    return im.resize((W, H), Image.Resampling.LANCZOS)


def check():
    times = np.unique(np.r_[np.linspace(0, END_TIME, 501), CONTACT_TIME])
    q = trajectory(times)
    distances = np.linalg.norm(q[:, 1] - q[:, 0], axis=1)
    assert abs(np.linalg.norm(QC[1] - QC[0]) - 2*RADIUS) < 1e-12
    assert distances.min() >= 2*RADIUS - 1e-12
    clearance = np.array([3.0, 1.5]) - np.abs(q) - RADIUS
    assert clearance.min() > 0
    assert abs(float(V1[0] @ V1[1])) < 1e-12
    max_reconstruction, max_energy, max_momentum = 0.0, 0.0, 0.0
    for stage in range(4):
        r, a, u, b = transform(stage)
        world = q @ r.T + a + times[:, None, None]*u
        recovered = (world - a - times[:, None, None]*u) @ r
        max_reconstruction = max(max_reconstruction, float(np.max(abs(recovered-q))))
        pre, post = V0 @ r.T + u, V1 @ r.T + u
        max_momentum = max(max_momentum, float(np.max(abs(pre.sum(axis=0)-post.sum(axis=0)))))
        max_energy = max(max_energy, abs(float((pre**2).sum() - (post**2).sum())/2))
        for t in (.3, 1.0, 2.0, 2.5):
            eps = 1e-5
            numeric = ((trajectory(t+eps) @ r.T + a + u*(t+eps))
                       - (trajectory(t-eps) @ r.T + a + u*(t-eps))) / (2*eps)
            assert np.max(abs(numeric-(velocities(t) @ r.T+u))) < 1e-9
        # Rails and ball centers remain within each drawing panel throughout.
        for t in np.linspace(0, END_TIME, 51):
            corners = np.array([[-3.15,-1.65],[3.15,-1.65],[3.15,1.65],[-3.15,1.65]])
            for panel in (0, 1):
                pts = screen(table_points(corners,stage,t,1,panel==1),panel,stage)
                x0,y0,x1,y1 = PANEL_BOXES[panel]
                assert pts[:,0].min()>x0+15 and pts[:,0].max()<x1-15
                assert pts[:,1].min()>236 and pts[:,1].max()<740
        assert np.max(abs((times+b)-times-b)) < 1e-12
    assert max_reconstruction < 1e-12 and max_energy < 1e-12 and max_momentum < 1e-12
    report = dict(model="equal-mass elastic disks, no friction or spin, no rail contact",
                  transformation="x'=R x+a+u t; t'=t+b", trails="table-relative",
                  role="illustration of dynamical symmetry, not derivation of Newton's first law",
                  contact_elapsed=CONTACT_TIME, end_elapsed=END_TIME,
                  minimum_separation=float(distances.min()), ball_diameter=2*RADIUS,
                  minimum_rail_clearance=float(clearance.min()),
                  inverse_transform_error=max_reconstruction,
                  within_trial_energy_error=max_energy, within_trial_momentum_error=max_momentum,
                  outgoing_velocities=V1.tolist(), fps=FPS, duration=DURATION, size=[W,H])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report), flush=True)


def preview():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1600, 4*500), BG)
    for i,t in enumerate(CHECK_TIMES):
        pic = frame(t)
        sheet.paste(pic.resize((800,480),Image.Resampling.LANCZOS),((i%2)*800,(i//2)*500))
        ImageDraw.Draw(sheet).text(((i%2)*800+12,(i//2)*500+482),f"{t:g} s",fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(19 / PLAYBACK_SPEED).save(OUT/f"{NAME}-poster.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    video = OUT/f"{NAME}.mp4"
    args = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-f","rawvideo",
            "-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an",
            "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
            "-movflags","+faststart",str(video)]
    proc = subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    started = time.perf_counter()
    try:
        for i in range(FRAMES):
            proc.stdin.write(frame(i/FPS).tobytes())
            if i % (FPS*3) == 0:
                print(f"{i/FPS:g}/{DURATION:g} s; elapsed {time.perf_counter()-started:.1f}s",flush=True)
        proc.stdin.close()
        error = proc.stderr.read().decode(errors="replace")
        if proc.wait():
            raise RuntimeError(error)
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    print(str(video),flush=True)


def encoded_check():
    reader = imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata = next(reader)
    assert tuple(metadata["size"]) == (W,H) and abs(metadata["fps"]-FPS)<1e-8
    indices = {round(t*FPS) for t in CHECK_TIMES}
    sheet = Image.new("RGB",(1600,4*480),BG)
    errors, count = [], 0
    for i,raw in enumerate(reader):
        count += 1
        if i in indices:
            decoded = np.frombuffer(raw,dtype=np.uint8).reshape(H,W,3)
            expected = np.asarray(frame(i/FPS))
            errors.append(float(np.mean(abs(decoded.astype(float)-expected.astype(float)))))
            slot = len(errors)-1
            pic = Image.fromarray(decoded.copy())
            sheet.paste(pic.resize((800,480),Image.Resampling.LANCZOS),((slot%2)*800,(slot//2)*480))
    assert count == FRAMES and len(errors)==len(indices) and max(errors)<2.0
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    result = dict(decoded_frames=count, duration=count/FPS, max_mean_rgb_error=max(errors),
                  size=metadata["size"],fps=metadata["fps"])
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for flag in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+flag,action="store_true")
    options = parser.parse_args()
    if options.check: check()
    if options.preview: preview()
    if options.render: render()
    if options.encoded_check: encoded_check()
