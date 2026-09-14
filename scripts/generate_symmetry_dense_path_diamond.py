"""Fixed point-source path family, linked to its actual cumulative phasor sum.

This is the equal-weight geometric-phase model discussed with the user, not
an absolute diffraction-field calculation. No finite-slit integral, detector
intensity, wavelength-dependent gain, or imposed straightening is used.
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

NAME = "symmetry-dense-path-diamond-wavelength-scan"
WIDTH, HEIGHT, FPS = 1440, 1080, 60
N, HALF_EXTENT, DISTANCE = 20001, 2.8, 4.5
WAVELENGTHS = (0.5, 0.05, 0.005)
# Midpoint samples, in the same top-to-bottom order in BOTH panes.
PITCH = 2 * HALF_EXTENT / N
POSITIONS = (HALF_EXTENT - (np.arange(N) + 0.5) * PITCH)
POSITIONS[N // 2] = 0.0
WEIGHTS = np.full(N, 1.0 / N)
EXCESS_LENGTHS = 2 * POSITIONS**2 / (np.hypot(DISTANCE, POSITIONS) + DISTANCE)
# The earlier desktop film used its initial completed sum as phase zero.
# Keep that ONE display-reference rotation at all wavelengths and scan times.
REFERENCE_ANGLE = float(np.angle(np.sum(WEIGHTS * np.exp(2j * np.pi * EXCESS_LENGTHS / WAVELENGTHS[0]))))
ROTATION = np.exp(-1j * REFERENCE_ANGLE)
for values in (POSITIONS, WEIGHTS, EXCESS_LENGTHS):
    values.setflags(write=False)

SETTLE_FRAMES, SCAN_FRAMES, HOLD_FRAMES = 48, 576, 96
PASS_FRAMES = SETTLE_FRAMES + SCAN_FRAMES + HOLD_FRAMES
TOTAL_FRAMES = PASS_FRAMES * len(WAVELENGTHS)
DURATION = TOTAL_FRAMES / FPS
ORIGIN, PHASOR_SCALE = (240.0, 786.0), 4300.0
A, B, SCREEN_X, CENTER_Y, SCREEN_HALF = (200.0, 302.0), (1240.0, 302.0), 720.0, 302.0, 118.0
TRACE_BOUNDS = (95, 586, 1270, 967)


def state(index):
    index = min(max(int(index), 0), TOTAL_FRAMES - 1)
    stage, local = divmod(index, PASS_FRAMES)
    if local < SETTLE_FRAMES:
        count = 0
    elif local < SETTLE_FRAMES + SCAN_FRAMES:
        count = min(N, ((local - SETTLE_FRAMES + 1) * N) // SCAN_FRAMES)
    else:
        count = N
    return stage, count


def point(value):
    return (ORIGIN[0] + PHASOR_SCALE * value.real,
            ORIGIN[1] - PHASOR_SCALE * value.imag)


def crossing(y):
    return (SCREEN_X, CENTER_Y - SCREEN_HALF * float(y) / HALF_EXTENT)


def dot(draw, xy, color, radius):
    x, y = xy
    draw.ellipse(pixels((x-radius, y-radius, x+radius, y+radius)), fill=color)


def dash(draw, first, last, color, width=1, length=5, gap=5):
    delta = np.asarray(last, dtype=float) - first
    distance = float(np.linalg.norm(delta))
    direction = delta / distance
    for start in np.arange(0, distance, length+gap):
        line(draw, np.asarray(first)+direction*start,
             np.asarray(first)+direction*min(start+length, distance), color, width)


@lru_cache(None)
def model(stage):
    phase = 2 * np.pi * EXCESS_LENGTHS / WAVELENGTHS[stage]
    vectors = ROTATION * WEIGHTS * np.exp(1j * phase)
    vertices = np.r_[0j, np.cumsum(vectors)]
    coords = tuple(point(value) for value in vertices)
    raster = tuple(pixels(xy) for xy in coords)
    return phase, vectors, vertices, coords, raster


@lru_cache(None)
def background(stage):
    image = Image.new("RGB", (WIDTH*SUPERSAMPLE, HEIGHT*SUPERSAMPLE), BG)
    d = ImageDraw.Draw(image, "RGBA")
    text(d, (38, 23), "Same paths · shorter wavelength", 31, bold=True)
    text(d, (39, 67), "Point source A · fixed observation point B · one screen", 19, MUTED)
    ratio = round(WAVELENGTHS[0]/WAVELENGTHS[stage])
    label = "λ = λ₀" if ratio == 1 else f"λ = λ₀ / {ratio}"
    text(d, (1400, 23), label, 31, bold=True, anchor="ra")
    text(d, (1400, 69), f"{stage+1} / {len(WAVELENGTHS)}", 18, MUTED, anchor="ra")
    for box in ((30, 111, 1410, 475), (30, 494, 1410, 1021)):
        d.rounded_rectangle(pixels(box), radius=14*SUPERSAMPLE,
                            fill=PANEL, outline=BORDER, width=SUPERSAMPLE)
    text(d, (53, 129), "Path diamond", 23, bold=True)
    text(d, (1387, 134), "20,001 fixed paths", 19, MUTED, anchor="ra")
    # The fill represents the envelope of unresolved paths, not a wave field
    # or probability density. The user explicitly requested this painted view.
    upper, lower = crossing(HALF_EXTENT), crossing(-HALF_EXTENT)
    d.polygon([pixels(xy) for xy in (A, upper, B, lower)], fill=(*BLUE, 12))
    for end in (upper, lower):
        line(d, A, end, (*BLUE, 35), 0.7)
        line(d, end, B, (*BLUE, 35), 0.7)
    text(d, (53, 512), "Tip to tail", 23, bold=True)
    text(d, (1068, 517), "Blue: contributions", 18, BLUE, anchor="ra")
    text(d, (1387, 517), "Gold: sum so far", 18, GOLD, anchor="ra")
    text(d, (53, 551), "One continuous trace of the same 20,001 arrows", 16, MUTED)
    dash(d, (101, ORIGIN[1]), (1300, ORIGIN[1]), AXIS, 0.8, 3, 5)
    # This is the real axis of the fixed DISPLAY reference, not an assertion
    # that the bare geometric sum has zero stationary-phase offset.
    text(d, (1312, ORIGIN[1]-10), "Re", 14, MUTED)
    x0, x1, bar_y = 1250, 1250+0.02*PHASOR_SCALE, 966
    line(d, (x0, bar_y), (x1, bar_y), MUTED, 1)
    for x in (x0, x1):
        line(d, (x, bar_y-4), (x, bar_y+4), MUTED, 1)
    text(d, ((x0+x1)/2, bar_y+9), "0.02", 14, MUTED, anchor="ma")
    text(d, (53, 992), "Phase zero: completed sum at λ₀", 16, MUTED)
    text(d, (1387, 992), "Same reference · same scale", 16, MUTED, anchor="ra")
    text(d, (39, 1041), "Equal-weight path phasors · |vⱼ| = 1/20,001", 17, MUTED)
    text(d, (1400, 1041), "λ₀ = 0.5 · A–screen = screen–B = 4.5", 17, MUTED, anchor="ra")
    return image


def frame(index):
    stage, count = state(index)
    image = background(stage).copy()
    d = ImageDraw.Draw(image, "RGBA")
    if count:
        # Pixel-sized bands contain many candidate rays. Fill their envelope
        # rather than drawing an arbitrary reduced set of visible fake paths.
        current = crossing(POSITIONS[count-1])
        upper = crossing(HALF_EXTENT)
        d.polygon([pixels(xy) for xy in (A, upper, current)], fill=(*BLUE, 37))
        d.polygon([pixels(xy) for xy in (B, upper, current)], fill=(*BLUE, 37))
        if count < N:
            line(d, A, current, BLUE, 2.0)
            line(d, current, B, BLUE, 2.0)
            dot(d, current, BLUE, 4.1)
    # Same screen location and same schematic dotted glyph in every frame.
    for y in np.arange(CENTER_Y-SCREEN_HALF, CENTER_Y+SCREEN_HALF+0.1, 3.8):
        dot(d, (SCREEN_X, float(y)), (*INK, 165), 0.95)
    for start, end in ((CENTER_Y-SCREEN_HALF-12, CENTER_Y-SCREEN_HALF-3),
                       (CENTER_Y+SCREEN_HALF+3, CENTER_Y+SCREEN_HALF+12)):
        line(d, (SCREEN_X, start), (SCREEN_X, end), INK, 3)
    dash(d, A, B, (*MUTED, 90), 0.75, 4, 6)
    if count and count < N:
        dot(d, crossing(POSITIONS[count-1]), BLUE, 4.1)
    for xy, label in ((A, "A"), (B, "B")):
        dot(d, xy, INK, 5.8)
        text(d, (xy[0], xy[1]+17), label, 20, INK, bold=True, anchor="ma")
    text(d, (SCREEN_X, 440), "screen", 16, MUTED, anchor="ma")
    text(d, (54, 441), f"Added {count:,} / {N:,}", 17, BLUE)
    text(d, (1387, 441), "Top → bottom", 17, MUTED, anchor="ra")

    _, _, vertices, coords, raster = model(stage)
    dot(d, ORIGIN, MUTED, 2.7)
    if count:
        # Every segment is used, even when its ~0.215 px arrowhead cannot be
        # resolved. No grouping, decorative direction arrows, or fitted curve.
        d.line(raster[:count+1], fill=BLUE, width=round(1.8*SUPERSAMPLE))
        arrow(d, ORIGIN, coords[count], GOLD, width=2.8, head=8)
        dot(d, coords[count], GOLD, 3.1)
    return image.reduce(SUPERSAMPLE)


def frame_for_count(stage, count):
    if count == 0:
        return stage*PASS_FRAMES
    local = SETTLE_FRAMES + math.ceil(count*SCAN_FRAMES/N)-1
    return stage*PASS_FRAMES+local


def checks():
    from scipy.integrate import quad
    assert N == 20001 and len(POSITIONS) == len(WEIGHTS) == N
    assert POSITIONS[N//2] == 0
    assert np.max(np.abs(POSITIONS+POSITIONS[::-1])) < 2e-15
    assert np.all(WEIGHTS == 1/N)
    path_hash = hashlib.sha256(POSITIONS.tobytes()+WEIGHTS.tobytes()).hexdigest()
    reports = []
    for stage, wavelength in enumerate(WAVELENGTHS):
        phase, vectors, vertices, coords, _ = model(stage)
        assert len(vertices) == N+1
        assert np.max(np.abs(np.abs(vectors)-1/N)) < 5e-20
        assert np.max(np.abs(np.diff(vertices)-vectors)) < 1e-16
        assert np.max(np.abs(vectors-vectors[::-1])) < 3e-16
        phase_step = float(np.max(np.abs(np.diff(phase))))
        assert phase_step < np.pi/8
        # Independent scalar geometric calculation, separate summation, and
        # adaptive continuous integral check both endpoints and scan prefixes.
        def phasor(y):
            excess = 2*y*y/(math.hypot(DISTANCE,y)+DISTANCE)
            angle = 2*math.pi*excess/wavelength-REFERENCE_ANGLE
            return complex(math.cos(angle), math.sin(angle))/N
        independent = np.array([phasor(float(y)) for y in POSITIONS])
        independent_error = float(np.max(np.abs(np.r_[0j,np.cumsum(independent)]-vertices)))
        assert independent_error < 2e-13
        def integrand(y):
            return phasor(y)/PITCH
        adaptive_checks = []
        for fraction in (.25, .49, .5, .51, .75, 1.0):
            count = round(N*fraction)
            lower = HALF_EXTENT-count*PITCH
            exact = complex(quad(lambda y: integrand(y).real, lower, HALF_EXTENT,
                                 epsabs=2e-11, limit=6000)[0],
                            quad(lambda y: integrand(y).imag, lower, HALF_EXTENT,
                                 epsabs=2e-11, limit=6000)[0])
            err = abs(vertices[count]-exact)
            assert err < 2e-6
            adaptive_checks.append({"count":count,"absolute_error":err})
        xy = np.asarray(coords)
        left, top, right, bottom = TRACE_BOUNDS
        margin = float(min(np.min(xy[:,0])-left, right-np.max(xy[:,0]),
                           np.min(xy[:,1])-top, bottom-np.max(xy[:,1])))
        assert margin > 8, margin
        # Exact temporal links: one count supplies the upper fan and lower sum.
        sequence = np.array([state(stage*PASS_FRAMES+i)[1] for i in range(PASS_FRAMES)])
        assert np.all(np.diff(sequence)>=0)
        assert sequence[0] == 0 and sequence[-1] == N
        assert sequence[SETTLE_FRAMES+SCAN_FRAMES-1] == N
        endpoint = complex(vertices[-1])
        reports.append({"wavelength":wavelength,"path_count":N,"path_weights_sha256":path_hash,
                        "max_adjacent_phase_step_degrees":math.degrees(phase_step),
                        "endpoint":[endpoint.real,endpoint.imag],"magnitude":abs(endpoint),
                        "display_angle_degrees":math.degrees(np.angle(endpoint)),
                        "independent_scalar_sum_max_error":independent_error,
                        "adaptive_integral_checks":adaptive_checks,"trace_margin_pixels":margin})
    report = {"model":"equal-weight exact-geometric point-path phasors",
              "source":[-DISTANCE,0],"screen_x":0,"observer":[DISTANCE,0],
              "transverse_interval":[-HALF_EXTENT,HALF_EXTENT],"midpoint_spacing":PITCH,
              "fixed_count":N,"weight_each":1/N,"same_positions_weights_every_stage":True,
              "fixed_display_rotation_degrees":-math.degrees(REFERENCE_ANGLE),
              "reference":"completed first-wavelength sum; one constant rotation for entire film",
              "fixed_pixels_per_phasor_unit":PHASOR_SCALE,"path_vector_length_pixels":PHASOR_SCALE/N,
              "absolute_propagation_kernel":False,"intensity_panel":False,
              "grouped_arrows":False,"endpoint_normalization":False,"forced_straightening":False,
              "path_fill":"schematic envelope of unresolved candidate rays, not probability or field",
              "screen_glyph":"schematic dots; not one visible dot per computational position",
              "sampling_order":"top to bottom; every term included in the cumulative trace",
              "settle_seconds_each":SETTLE_FRAMES/FPS,"scan_seconds_each":SCAN_FRAMES/FPS,
              "hold_seconds_each":HOLD_FRAMES/FPS,"fps":FPS,"frames":TOTAL_FRAMES,
              "duration_seconds":DURATION,"resolution":[WIDTH,HEIGHT],"stages":reports}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"duration":DURATION,"reference_rotation_degrees":report["fixed_display_rotation_degrees"],
                      "stages":reports}),flush=True)


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1440,1152), BG)
    d = ImageDraw.Draw(sheet)
    for stage in range(3):
        for column, fraction in enumerate((.25,.49,.51,1.0)):
            index = frame_for_count(stage, round(N*fraction))
            still = frame(index)
            if fraction == 1.0:
                still.save(OUT/f"{NAME}-lambda-{stage+1}.png")
            x,y = column*360,stage*384
            sheet.paste(still.resize((360,270),Image.Resampling.LANCZOS),(x,y))
            # Taller lower-pane crop makes endpoint details legible in QA.
            crop = still.crop((85,580,1355,975)).resize((360,112),Image.Resampling.LANCZOS)
            sheet.paste(crop,(x,y+272))
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    output = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
               "-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
               "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","fast",
               "-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start = time.perf_counter()
    previous, rgb = None, None
    try:
        for index in range(TOTAL_FRAMES):
            current = state(index)
            if current != previous:
                rgb = frame(index).tobytes()
                previous = current
            process.stdin.write(rgb)
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
    wanted = {frame_for_count(stage,round(N*fraction)) for stage in range(3)
              for fraction in (0,.25,.49,.5,.51,.75,1)} | {TOTAL_FRAMES-1}
    reader = imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata = next(reader)
    assert tuple(metadata["size"]) == (WIDTH,HEIGHT)
    assert abs(metadata["fps"]-FPS) < 1e-8
    checked, selected, decoded_count = [], {}, 0
    for index,raw in enumerate(reader):
        decoded_count += 1
        if index not in wanted:
            continue
        decoded = np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        reference = np.asarray(frame(index))
        mae = float(np.mean(np.abs(decoded.astype(float)-reference.astype(float))))
        assert mae < 2.5
        stage,count = state(index)
        # Check the visible end marker against the actual prefix of the same
        # 20,001 terms, not merely against an unrelated generated reference.
        gold_pixels = None
        if count:
            x,y = map(round,model(stage)[3][count])
            crop = decoded[y-5:y+6,x-5:x+6].astype(float)
            gold_pixels = int(np.sum(np.linalg.norm(crop-np.asarray(GOLD),axis=2)<65))
            assert gold_pixels > 8,(index,gold_pixels)
        checked.append({"frame":index,"stage":stage+1,"count":count,
                        "mean_absolute_rgb_error":mae,"gold_tip_pixels":gold_pixels})
        if count == N:
            selected[stage] = Image.fromarray(decoded.copy())
    assert decoded_count == TOTAL_FRAMES
    assert len(selected) == 3
    sheet = Image.new("RGB", (1440,1110), BG)
    d = ImageDraw.Draw(sheet)
    for stage in range(3):
        x=stage*480
        sheet.paste(selected[stage].resize((480,360),Image.Resampling.LANCZOS),(x,0))
        # Below, full-size lower-pane crops show the actual encoded linework.
        crop=selected[stage].crop((90,590,1350,980)).resize((1260,390),Image.Resampling.LANCZOS)
        if stage == 0:
            sheet.paste(crop,(90,365))
        else:
            detail=selected[stage].crop((105,650,720,920))
            sheet.paste(detail,(45+(stage-1)*710,795))
            d.text((45+(stage-1)*710,770),f"Pass {stage+1}, encoded detail at native scale",fill=INK)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":decoded_count,"duration_seconds":decoded_count/FPS,
            "fps":metadata["fps"],"resolution":metadata["size"],"representative_checks":checked}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_frames":decoded_count,"representative_checks":len(checked),
                      "max_frame_rgb_error":max(x["mean_absolute_rgb_error"] for x in checked)}),flush=True)


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args=parser.parse_args()
    if args.check:
        checks()
    if args.preview:
        previews()
    if args.render:
        render()
    if args.encoded_check:
        encoded_checks()
