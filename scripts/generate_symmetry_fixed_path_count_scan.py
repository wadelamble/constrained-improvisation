"""One fixed midpoint path set; one literal contribution arrow per path.

The displayed polygon is a finite midpoint sum, not a sampled analytic
Fresnel curve. The analytic integral is used only as a validation benchmark.
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
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow, cumulative,
)

NAME = "symmetry-fixed-path-count-scan"
WIDTH, HEIGHT, FPS = 1440, 960, 60
N = 121
F_NUMBERS = (1.0, 4.0, 9.0)
# All passes use these identical objects, positions, and quadrature weights.
POSITIONS = np.arange(-(N // 2), N // 2 + 1, dtype=float) * (2.0 / N)
WEIGHTS = np.full(N, 2.0 / N)
EDGES = np.linspace(-1.0, 1.0, N + 1)
POSITIONS.setflags(write=False)
WEIGHTS.setflags(write=False)
SETTLE_FRAMES, FRAMES_PER_PATH, HOLD_FRAMES = 60, 5, 60
SCAN_FRAMES = N * FRAMES_PER_PATH
PASS_FRAMES = SETTLE_FRAMES + SCAN_FRAMES + HOLD_FRAMES
TOTAL_FRAMES = len(F_NUMBERS) * PASS_FRAMES
DURATION = TOTAL_FRAMES / FPS
SCALE, ORIGIN = 640.0, (350.0, 694.0)
APERTURE_X, APERTURE_HALF, APERTURE_Y = 720.0, 455.0, 190.0
OBSERVER = (APERTURE_X, 346.0)
Z_OVER_A = 1000.0


def state(frame_index):
    frame_index = min(max(int(frame_index), 0), TOTAL_FRAMES - 1)
    stage, local = divmod(frame_index, PASS_FRAMES)
    if local < SETTLE_FRAMES:
        count = 0
    else:
        count = min(N, 1 + (local - SETTLE_FRAMES) // FRAMES_PER_PATH)
    return stage, count


def point(value):
    return (ORIGIN[0] + SCALE * value.real, ORIGIN[1] - SCALE * value.imag)


def dot(draw, xy, color, radius):
    x, y = xy
    draw.ellipse(pixels((x-radius, y-radius, x+radius, y+radius)), fill=color)


def dashed(draw, first, last, color, width=1.1, dash=6, gap=6):
    delta = np.asarray(last, dtype=float) - first
    length = float(np.linalg.norm(delta))
    unit = delta / length
    for begin in np.arange(0, length, dash + gap):
        line(draw, np.asarray(first) + begin * unit,
             np.asarray(first) + min(begin + dash, length) * unit, color, width)


@lru_cache(None)
def model(stage):
    f_number = F_NUMBERS[stage]
    vectors = (math.sqrt(f_number) * np.exp(-0.25j * np.pi) *
               np.exp(1j * np.pi * f_number * POSITIONS**2) * WEIGHTS)
    vertices = np.r_[0j, np.cumsum(vectors)]
    coordinates = tuple(point(value) for value in vertices)
    return vectors, vertices, coordinates


@lru_cache(None)
def background(stage):
    image = Image.new("RGB", (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), BG)
    d = ImageDraw.Draw(image, "RGBA")
    text(d, (37, 24), "121 paths, 121 arrows", 31, bold=True)
    text(d, (39, 70), "Fixed geometry · fixed arrow scale · same aperture positions", 19, MUTED)
    ratio = round(F_NUMBERS[stage] / F_NUMBERS[0])
    wavelength = "λ = λ₀" if ratio == 1 else f"λ = λ₀ / {ratio}"
    text(d, (1401, 24), wavelength, 29, INK, bold=True, anchor="ra")
    text(d, (1400, 70), f"Pass {stage+1} of 3     F = {F_NUMBERS[stage]:g}", 18, MUTED, anchor="ra")

    for box in ((30, 115, 1410, 382), (30, 401, 1410, 906)):
        d.rounded_rectangle(pixels(box), radius=round(14 * SUPERSAMPLE),
                            fill=PANEL, outline=BORDER, width=SUPERSAMPLE)
    text(d, (51, 129), "Candidate paths", 22, bold=True)
    text(d, (1387, 133), "Uniform plane-wave illumination", 17, MUTED, anchor="ra")

    left, right = APERTURE_X - APERTURE_HALF, APERTURE_X + APERTURE_HALF
    line(d, (155, APERTURE_Y), (left, APERTURE_Y), MUTED, 5)
    line(d, (right, APERTURE_Y), (1285, APERTURE_Y), MUTED, 5)
    line(d, (left, APERTURE_Y), (right, APERTURE_Y), BORDER, 1.1)
    # A visual phase scale, not a truncation window; every path is retained.
    half = APERTURE_HALF / math.sqrt(F_NUMBERS[stage])
    d.rectangle(pixels((APERTURE_X-half, APERTURE_Y-11,
                        APERTURE_X+half, APERTURE_Y+11)), fill=(*BLUE, 21))
    for x in (APERTURE_X-half, APERTURE_X+half):
        line(d, (x, APERTURE_Y-12), (x, APERTURE_Y+12), (*BLUE, 135), 1)
    text(d, (APERTURE_X, 152), "Phase scale: |y| ≤ √(λz)", 16, BLUE, anchor="ma")
    for source in POSITIONS:
        xy = (APERTURE_X + APERTURE_HALF * source, APERTURE_Y)
        line(d, xy, OBSERVER, (*MUTED, 28), 0.55)
        dot(d, xy, (*MUTED, 150), 1.4)
    for location, label in ((left, "−a"), (right, "+a")):
        text(d, (location, APERTURE_Y+14), label, 17, MUTED, anchor="ma")
    dashed(d, (APERTURE_X, APERTURE_Y+18), OBSERVER, (*MUTED, 160))
    line(d, (APERTURE_X+9, 287), (1058, 287), BORDER, 0.8)
    text(d, (1075, 276), "Stationary path", 17, MUTED)
    text(d, (APERTURE_X+19, OBSERVER[1]-10), "B", 20, INK)
    text(d, (1385, 353), "Geometry schematic", 14, MUTED, anchor="ra")
    dot(d, OBSERVER, INK, 4)

    text(d, (52, 417), "One contribution per path", 22, bold=True)
    text(d, (1095, 421), "blue: contributions", 17, BLUE, anchor="ra")
    text(d, (1387, 421), "gold: sum so far", 17, GOLD, anchor="ra")
    line(d, (143, ORIGIN[1]), (1295, ORIGIN[1]), AXIS, 0.8)
    text(d, (1308, ORIGIN[1]-9), "Re", 14, MUTED)
    # Keep labels outside all three polygons, including their completed coils.
    # This separate ruler uses the same fixed 640 px/unit as the vectors.
    for x in (1210, 1338):
        line(d, (x, 840), (x, 848), MUTED, 1)
    line(d, (1210, 844), (1338, 844), MUTED, 1)
    text(d, (1274, 851), "0.2", 13, MUTED, anchor="ma")
    text(d, (1386, 875), "Fixed complex-amplitude scale", 16, MUTED, anchor="ra")
    text(d, (38, 925), "vⱼ = √F exp[i(πFsⱼ² − π/4)] Δs     ·     Δs = 2/121", 16, MUTED)
    text(d, (1400, 925), "Scan = addition order", 16, MUTED, anchor="ra")
    return image


def draw_polygon(draw, stage, count):
    """Draw exactly count actual vectors, each with one endpoint arrowhead."""
    _, vertices, coordinates = model(stage)
    if count:
        # The resultant goes underneath, so none of the blue arrows is hidden
        # merely because the gold line crosses it.
        arrow(draw, ORIGIN, coordinates[count], GOLD, width=2.8, head=9)
    for j in range(count):
        active = j == count - 1
        arrow(draw, coordinates[j], coordinates[j+1], BLUE,
              width=2.5 if active else 1.45, head=4.8 if active else 3.4)
    dot(draw, ORIGIN, MUTED, 2.6)
    if count:
        tip = coordinates[count]
        draw.ellipse(pixels((tip[0]-7, tip[1]-7, tip[0]+7, tip[1]+7)),
                     outline=(*BLUE, 125), width=SUPERSAMPLE)
    return count


def frame(frame_index):
    stage, count = state(frame_index)
    image = background(stage).copy()
    d = ImageDraw.Draw(image, "RGBA")
    for source in POSITIONS[:count]:
        dot(d, (APERTURE_X + APERTURE_HALF * source, APERTURE_Y), BLUE, 1.5)
    if count:
        source = POSITIONS[count-1]
        aperture_point = (APERTURE_X + APERTURE_HALF * source, APERTURE_Y)
        line(d, aperture_point, OBSERVER, BLUE, 2.3)
        dot(d, aperture_point, (*BLUE, 28), 8)
        dot(d, aperture_point, BLUE, 3.9)
        dot(d, OBSERVER, INK, 4)
        text(d, (53, 322), f"Path {count} / {N}", 21, BLUE)
        text(d, (53, 352), f"y / a = {source:+.3f}", 16, MUTED)
        text(d, (52, 451), f"Added {count} / {N}   ·   current arrow: {count}", 16, BLUE)
    else:
        text(d, (53, 322), f"{N} fixed midpoint paths", 20, BLUE)
        text(d, (53, 352), "Left to right · same cadence", 16, MUTED)
        text(d, (52, 451), f"Added 0 / {N}", 16, BLUE)
    drawn_count = draw_polygon(d, stage, count)
    assert drawn_count == count
    return image.reduce(SUPERSAMPLE)


def checks():
    assert len(POSITIONS) == len(WEIGHTS) == N
    assert np.max(np.abs(POSITIONS - (EDGES[:-1]+EDGES[1:])/2)) < 3e-16
    assert POSITIONS[N//2] == 0.0
    assert np.all(WEIGHTS == 2/N)
    assert abs(float(WEIGHTS.sum()) - 2) < 1e-14
    assert np.all(np.diff(POSITIONS) > 0)
    identity = hashlib.sha256(POSITIONS.tobytes()+WEIGHTS.tobytes()).hexdigest()
    data = []
    for stage, f_number in enumerate(F_NUMBERS):
        vectors, vertices, coordinates = model(stage)
        exact = cumulative(f_number, EDGES)
        error = np.abs(vertices-exact)
        phase_steps = np.diff(np.pi*f_number*POSITIONS**2)
        max_step = float(np.max(np.abs(phase_steps)))
        assert max_step < math.pi/3
        assert float(error.max()) < 0.0041
        assert len(vectors) == N and len(vertices) == N+1
        assert np.max(np.abs(np.diff(vertices)-vectors)) < 3e-16
        assert np.max(np.abs(np.abs(vectors)-2*math.sqrt(f_number)/N)) < 1e-16
        screen = np.asarray(coordinates)
        assert screen[:,0].min() > 180 and screen[:,0].max() < 1210
        assert screen[:,1].min() > 476 and screen[:,1].max() < 887
        length = 2*math.sqrt(f_number)/N*SCALE
        assert length > 10
        scan_begin = stage*PASS_FRAMES + SETTLE_FRAMES
        indices = [state(scan_begin+i)[1] for i in range(SCAN_FRAMES)]
        assert indices == np.repeat(np.arange(1, N+1), FRAMES_PER_PATH).tolist()
        assert state(stage*PASS_FRAMES)[1] == 0
        assert state((stage+1)*PASS_FRAMES-1)[1] == N
        final = complex(vertices[-1])
        benchmark = complex(exact[-1])
        data.append({
            "F": f_number, "lambda_over_initial_lambda": 1/f_number,
            "candidate_count": N, "completed_blue_arrow_count": len(vectors),
            "positions_and_weights_sha256": identity,
            "scan_start_seconds": scan_begin/FPS,
            "scan_end_seconds": (scan_begin+SCAN_FRAMES)/FPS,
            "first_to_last_midpoint_seconds": (N-1)*FRAMES_PER_PATH/FPS,
            "phase_scale_half_width_over_a": 1/math.sqrt(f_number),
            "max_adjacent_unwrapped_phase_step_radians": max_step,
            "arrow_length_pixels": length,
            "finite_sum_endpoint": [final.real, final.imag],
            "analytic_endpoint": [benchmark.real, benchmark.imag],
            "max_absolute_prefix_error_vs_analytic": float(error.max()),
            "relative_endpoint_error_vs_analytic": float(error[-1]/abs(benchmark)),
            "vertex_screen_bounds_xy": [screen.min(axis=0).tolist(), screen.max(axis=0).tolist()],
        })
    report = {
        "description": "One literal midpoint contribution vector for every fixed candidate path",
        "stages": data, "N": N, "positions_y_over_a": POSITIONS.tolist(),
        "quadrature_weights": WEIGHTS.tolist(), "path_order": "increasing aperture coordinate",
        "frames_per_path": FRAMES_PER_PATH, "scan_seconds_per_pass": SCAN_FRAMES/FPS,
        "settle_seconds_per_pass": SETTLE_FRAMES/FPS,
        "hold_seconds_per_pass": HOLD_FRAMES/FPS,
        "duration_seconds": DURATION, "fps": FPS, "total_frames": TOTAL_FRAMES,
        "resolution": [WIDTH, HEIGHT], "pixels_per_amplitude_unit": SCALE,
        "phase_reference": "U / exp(ikz); normalized 1D Fresnel prefactor retained",
        "analytic_curve_rendered": False, "decorative_arrowheads": False,
        "grouped_or_omitted_vectors": False, "endpoint_rotation_or_normalization": False,
        "geometry_z_over_a": Z_OVER_A,
        "max_omitted_quartic_phase_radians": math.pi*max(F_NUMBERS)/(4*Z_OVER_A**2),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"N":N,"stages":data,"duration":DURATION}),flush=True)


def selected_frame(stage, count):
    if count == 0:
        return stage*PASS_FRAMES + SETTLE_FRAMES//2
    return stage*PASS_FRAMES + SETTLE_FRAMES + (count-1)*FRAMES_PER_PATH + 2


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    counts = (40, 61, 82, N)
    sheet = Image.new("RGB", (1440, 792), BG)
    draw = ImageDraw.Draw(sheet)
    for stage in range(len(F_NUMBERS)):
        for column, count in enumerate(counts):
            index = selected_frame(stage, count)
            rendered = frame(index)
            rendered.save(OUT/f"{NAME}-pass-{stage+1}-path-{count}.png")
            x, y = column*360, stage*264
            sheet.paste(rendered.resize((360,240),Image.Resampling.LANCZOS),(x,y))
            draw.text((x+9,y+244),f"F={F_NUMBERS[stage]:g}    path {count}/{N}",fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(TOTAL_FRAMES-1).save(OUT/f"{NAME}-final.png")
    frame(0).save(OUT/f"{NAME}-initial.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
               "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast",
               "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    start = time.perf_counter()
    last_state, last_rgb = None, None
    try:
        for index in range(TOTAL_FRAMES):
            current_state = state(index)
            if current_state != last_state:
                last_rgb = frame(index).tobytes()
                last_state = current_state
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
    """Decode the complete MP4 and compare representative literal-arrow frames."""
    output = OUT/f"{NAME}.mp4"
    wanted = sorted({selected_frame(stage,count) for stage in range(3)
                     for count in (0,1,40,60,61,62,82,N)} | {TOTAL_FRAMES-1})
    reader = imageio_ffmpeg.read_frames(str(output), pix_fmt="rgb24")
    metadata = next(reader)
    assert tuple(metadata["size"]) == (WIDTH,HEIGHT), metadata
    assert abs(metadata["fps"]-FPS) < 1e-8, metadata
    checked, count = [], 0
    decoded_selected = {}
    for index, raw in enumerate(reader):
        count += 1
        if index not in wanted:
            continue
        decoded = np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        reference = np.asarray(frame(index))
        mae = float(np.mean(np.abs(decoded.astype(float)-reference.astype(float))))
        assert mae < 2.5, (index,mae)
        stage, added = state(index)
        active_pixels = None
        if added:
            # An active physical marker at the prescribed candidate position.
            x = round(APERTURE_X+APERTURE_HALF*POSITIONS[added-1])
            y = round(APERTURE_Y)
            crop = decoded[y-4:y+5,x-4:x+5].astype(float)
            active_pixels = int(np.sum(np.linalg.norm(crop-np.asarray(BLUE),axis=2)<55))
            assert active_pixels > 15, (index,active_pixels)
        checked.append({"frame":index,"stage":stage+1,"added_vectors":added,
                        "mean_absolute_rgb_error":mae,"active_marker_blue_pixels":active_pixels})
        if added in (40,61,N):
            decoded_selected[(stage,added)] = Image.fromarray(decoded.copy())
    assert count == TOTAL_FRAMES, (count,TOTAL_FRAMES)
    sheet = Image.new("RGB",(1440,1032),BG)
    draw = ImageDraw.Draw(sheet)
    for stage in range(3):
        for column,added in enumerate((40,61,N)):
            rendered = decoded_selected[(stage,added)]
            x,y = column*480,stage*344
            sheet.paste(rendered.resize((480,320),Image.Resampling.LANCZOS),(x,y))
            draw.text((x+9,y+324),f"Encoded: F={F_NUMBERS[stage]:g}, path {added}/{N}",fill=INK)
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report = {"decoded_frames":count,"fps":metadata["fps"],"resolution":metadata["size"],
              "duration_seconds":count/FPS,"representative_checks":checked,
              "maximum_frame_mean_absolute_rgb_error":max(x["mean_absolute_rgb_error"] for x in checked)}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--preview",action="store_true")
    parser.add_argument("--render",action="store_true")
    parser.add_argument("--encoded-check",action="store_true")
    args = parser.parse_args()
    if args.check:
        checks()
    if args.preview:
        previews()
    if args.render:
        render()
    if args.encoded_check:
        encoded_checks()
