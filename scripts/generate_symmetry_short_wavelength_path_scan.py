"""Link an aperture scan to its actual cumulative Fresnel tip-to-tail sum.

Three equal-duration scans at fixed geometry and fixed complex-plane scale.
Only wavelength changes. The aperture has uniform incident plane-wave phase;
the observation point is on axis. No grouping, endpoint alignment, or zoom.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
import subprocess
import time

from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line, arrow, cumulative,
)

NAME = "symmetry-short-wavelength-path-scan"
WIDTH, HEIGHT = 1440, 960
FPS = 60
F_NUMBERS = (2.0, 32.0, 512.0)
SETTLE, SCAN, HOLD = 1.0, 10.0, 1.0
PASS = SETTLE + SCAN + HOLD
DURATION = len(F_NUMBERS) * PASS
SCALE = 650.0
ORIGIN = (365.0, 677.0)
APERTURE_X, APERTURE_HALF, APERTURE_Y = 720.0, 455.0, 202.0
OBSERVER = (APERTURE_X, 385.0)
Z_OVER_A = 1000.0


def state(seconds):
    seconds = float(np.clip(seconds, 0, DURATION - 1 / FPS))
    stage = min(int(seconds // PASS), len(F_NUMBERS) - 1)
    local = seconds - stage * PASS
    fraction = float(np.clip((local - SETTLE) / SCAN, 0, 1))
    return stage, -1 + 2 * fraction


def point(value):
    return (ORIGIN[0] + SCALE * value.real, ORIGIN[1] - SCALE * value.imag)


def dot(draw, xy, color, radius):
    x, y = xy
    draw.ellipse(pixels((x-radius, y-radius, x+radius, y+radius)), fill=color)


def dashed(draw, first, last, color, width=1.2, dash=6, gap=6):
    delta = np.asarray(last, dtype=float) - first
    length = float(np.linalg.norm(delta))
    unit = delta / length
    for begin in np.arange(0, length, dash + gap):
        line(draw, np.asarray(first) + begin * unit,
             np.asarray(first) + min(begin + dash, length) * unit, color, width)


@lru_cache(None)
def geometry(stage):
    """Resolve the curve spatially, independently of the video frame rate."""
    f_number = F_NUMBERS[stage]
    umax = math.sqrt(f_number)
    # In u=y/sqrt(lambda*z), |dC/du|=1. Every chord is at most 0.45 px.
    intervals = math.ceil(2 * umax * SCALE / 0.45)
    u = np.linspace(-umax, umax, intervals + 1)
    sources = u / umax
    values = cumulative(f_number, sources)
    coordinates = np.column_stack((ORIGIN[0] + SCALE * values.real,
                                   ORIGIN[1] - SCALE * values.imag))
    flat = (coordinates * SUPERSAMPLE).ravel().tolist()

    # Small tangent heads indicate direction along the curve; they do not
    # substitute chords or group the contributions into larger arrows.
    heads = []
    for marker_u in np.arange(-umax, umax, 0.035):
        curvature_radius = SCALE / (2 * math.pi * max(abs(marker_u), 0.05))
        size = min(4.4, 0.10 * curvature_radius)
        if size < 1.5:
            continue
        source = float(marker_u / umax)
        position = point(complex(cumulative(f_number, [source])[0]))
        angle = math.pi * marker_u**2 - math.pi / 4
        tangent = (math.cos(angle), -math.sin(angle))
        normal = (-tangent[1], tangent[0])
        triangle = [position] + [
            (position[0] - size * tangent[0] + side * 0.43 * size * normal[0],
             position[1] - size * tangent[1] + side * 0.43 * size * normal[1])
            for side in (-1, 1)
        ]
        heads.append((source, [pixels(p) for p in triangle]))
    return sources, values, coordinates, flat, heads


@lru_cache(None)
def background(stage):
    image = Image.new("RGB", (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), BG)
    d = ImageDraw.Draw(image, "RGBA")
    text(d, (37, 24), "Where the sum is built", 31, bold=True)
    text(d, (39, 70), "Shorter wavelength · same geometry · same scanning speed", 19, MUTED)
    ratio = round(F_NUMBERS[stage] / F_NUMBERS[0])
    wavelength = "λ = λ₀" if ratio == 1 else f"λ = λ₀ / {ratio}"
    text(d, (1401, 24), wavelength, 29, INK, bold=True, anchor="ra")
    text(d, (1400, 70), f"Pass {stage+1} of {len(F_NUMBERS)}", 18, MUTED, anchor="ra")

    for box in ((30, 115, 1410, 428), (30, 449, 1410, 902)):
        d.rounded_rectangle(pixels(box), radius=round(14 * SUPERSAMPLE),
                            fill=PANEL, outline=BORDER, width=round(SUPERSAMPLE))
    text(d, (51, 129), "Candidate paths", 22, bold=True)
    text(d, (1387, 133), "Plane-wave illumination", 17, MUTED, anchor="ra")

    left, right = APERTURE_X - APERTURE_HALF, APERTURE_X + APERTURE_HALF
    # Dark end pieces mark the finite opening. The thin line across the
    # opening is a coordinate guide, not another partly transmitting screen.
    line(d, (155, APERTURE_Y), (left, APERTURE_Y), MUTED, 5)
    line(d, (right, APERTURE_Y), (1285, APERTURE_Y), MUTED, 5)
    line(d, (left, APERTURE_Y), (right, APERTURE_Y), BORDER, 1.4)
    for location, label in ((left, "−a"), (right, "+a")):
        line(d, (location, APERTURE_Y - 5), (location, APERTURE_Y + 6), MUTED, 1)
        text(d, (location, APERTURE_Y + 13), label, 17, MUTED, anchor="ma")

    # This marks the characteristic phase scale, not a region whose
    # contribution alone equals the final sum. All outer terms are retained.
    half = APERTURE_HALF / math.sqrt(F_NUMBERS[stage])
    d.rectangle(pixels((APERTURE_X-half, APERTURE_Y-12,
                        APERTURE_X+half, APERTURE_Y+12)), fill=(*BLUE, 24))
    for x in (APERTURE_X-half, APERTURE_X+half):
        line(d, (x, APERTURE_Y-13), (x, APERTURE_Y+13), (*BLUE, 140), 1)
    text(d, (APERTURE_X, 157), "Stationary-phase scale", 17, BLUE, anchor="ma")
    dashed(d, (APERTURE_X, APERTURE_Y+18), OBSERVER, (*MUTED, 145))
    line(d, (APERTURE_X+8, 310), (1080, 310), (*BORDER, 180), 0.8)
    text(d, (1095, 298), "Stationary path", 17, MUTED)
    text(d, (APERTURE_X+19, OBSERVER[1]-11), "Observation point", 17, INK)
    text(d, (53, 365), "Scan position", 15, MUTED)
    text(d, (1385, 393), "Geometry schematic", 14, MUTED, anchor="ra")

    text(d, (52, 466), "Tip to tail", 22, bold=True)
    arrow(d, (1000, 481), (1030, 481), BLUE, 1.8, 5)
    text(d, (1040, 469), "contributions", 17, BLUE)
    arrow(d, (1216, 481), (1246, 481), GOLD, 2.8, 7)
    text(d, (1257, 469), "sum so far", 17, GOLD)

    line(d, (160, ORIGIN[1]), (1260, ORIGIN[1]), AXIS, 0.8)
    text(d, (1386, 869), "Fixed arrow scale", 16, MUTED, anchor="ra")
    text(d, (37, 924), "The scan orders the addition; it is not a particle's travel time.", 16, MUTED)
    text(d, (1401, 924), "Phase reference: unobstructed plane wave", 16, MUTED, anchor="ra")
    return image


def frame(seconds):
    stage, source = state(seconds)
    f_number = F_NUMBERS[stage]
    image = background(stage).copy()
    d = ImageDraw.Draw(image, "RGBA")
    aperture_point = (APERTURE_X + APERTURE_HALF * source, APERTURE_Y)
    line(d, aperture_point, OBSERVER, BLUE, 2.2)
    dot(d, aperture_point, (*BLUE, 25), 10)
    dot(d, aperture_point, BLUE, 4.4)
    dot(d, OBSERVER, INK, 4)
    text(d, (53, 388), f"y / a = {source:+.2f}", 19, BLUE)

    sources, values, coordinates, flat, heads = geometry(stage)
    endpoint = complex(cumulative(f_number, [source])[0])
    tip = point(endpoint)
    cutoff = int(np.searchsorted(sources, source, side="right"))
    # Append the exact current sum, rather than snapping its endpoint to a
    # drawing sample. The entire ordered prefix is drawn, including curls.
    prefix = flat[:2 * cutoff] + list(pixels(tip))
    if len(prefix) >= 4:
        d.line(prefix, fill=BLUE, width=round(1.7 * SUPERSAMPLE))
    for location, triangle in heads:
        if location > source:
            break
        d.polygon(triangle, fill=BLUE)
    arrow(d, ORIGIN, tip, GOLD, width=3.1, head=10)
    dot(d, ORIGIN, MUTED, 2.8)
    dot(d, tip, (*BLUE, 22), 10)
    dot(d, tip, BLUE, 4.0)
    # Integer supersampling gives area-averaged antialiasing without a costly
    # general-purpose resample of every full-resolution video frame.
    return image.reduce(SUPERSAMPLE)


def checks():
    from numpy.polynomial.legendre import leggauss
    nodes, weights = leggauss(24)
    edges = np.linspace(-1, 1, round(SCAN * FPS)+1)
    middle, half = (edges[1:]+edges[:-1])/2, np.diff(edges)/2
    x = middle[:, None] + half[:, None] * nodes
    data = []
    worst_error = 0.0
    for stage, f_number in enumerate(F_NUMBERS):
        integrals = (math.sqrt(f_number) * np.exp(-0.25j*np.pi) * half *
                     np.sum(weights * np.exp(1j*np.pi*f_number*x*x), axis=1))
        numerical = np.r_[0j, np.cumsum(integrals)]
        exact = cumulative(f_number, edges)
        error = float(np.max(np.abs(numerical-exact)))
        worst_error = max(worst_error, error)
        assert error < 1e-10, (f_number, error)
        sources, values, coordinates, flat, heads = geometry(stage)
        assert np.max(np.abs(np.diff(values))) * SCALE <= 0.45001
        assert np.min(coordinates[:, 0]) > 55
        assert np.max(coordinates[:, 0]) < WIDTH-55
        assert np.min(coordinates[:, 1]) > 511
        assert np.max(coordinates[:, 1]) < 893
        times = stage * PASS + SETTLE + np.arange(len(edges)) / FPS
        sampled = np.asarray([state(t)[1] for t in times])
        assert np.max(np.abs(sampled-edges)) < 1e-13
        endpoint = complex(exact[-1])
        data.append({
            "F": f_number, "lambda_over_initial_lambda": F_NUMBERS[0]/f_number,
            "scan_start_seconds": stage*PASS+SETTLE,
            "scan_stop_seconds": stage*PASS+SETTLE+SCAN,
            "phase_scale_half_width_over_a": 1/math.sqrt(f_number),
            "phase_scale_crossing_seconds": SCAN/math.sqrt(f_number),
            "phase_scale_crossing_frames": SCAN*FPS/math.sqrt(f_number),
            "curve_samples": len(sources), "endpoint": [endpoint.real, endpoint.imag],
            "quadrature_error_all_scan_frames": error,
        })
    report = {
        "description": "Ordered cumulative Fresnel sum linked to physical aperture position",
        "stages": data, "same_linear_scan_speed": 2/SCAN,
        "duration_seconds": DURATION, "fps": FPS, "resolution": [WIDTH, HEIGHT],
        "pixels_per_amplitude_unit": SCALE,
        "phase_reference": "U / exp(ikz); normalized 1D Fresnel kernel retained",
        "grouped": False, "endpoint_rotation_or_rescaling": False,
        "geometry_z_over_a": Z_OVER_A,
        "max_omitted_quartic_phase_radians": math.pi*max(F_NUMBERS)/(4*Z_OVER_A**2),
        "max_independent_quadrature_error": worst_error,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report), flush=True)


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    # Columns bracket the central crossing. Use identical physical scan
    # positions on every row so localization can be checked directly.
    fractions = (-0.35, 0.0, 0.35, 1.0)
    sheet = Image.new("RGB", (1440, 792), BG)
    draw = ImageDraw.Draw(sheet)
    for stage in range(len(F_NUMBERS)):
        for column, source in enumerate(fractions):
            seconds = stage*PASS + SETTLE + (source+1)*SCAN/2
            rendered = frame(seconds)
            rendered.save(OUT/f"{NAME}-check-{seconds:g}.png")
            x, y = column*360, stage*264
            sheet.paste(rendered.resize((360,240),Image.Resampling.LANCZOS),(x,y))
            draw.text((x+9, y+244), f"{seconds:g} s    y/a = {source:+.2f}", fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    frame(DURATION-0.5).save(OUT/f"{NAME}-final.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"), flush=True)


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
               "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast",
               "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    start = time.perf_counter()
    last_state, last_rgb = None, None
    try:
        for index in range(round(FPS*DURATION)):
            current_state = state(index/FPS)
            if current_state != last_state:
                last_rgb = frame(index/FPS).tobytes()
                last_state = current_state
            process.stdin.write(last_rgb)
            if index % (FPS*3) == 0:
                print(f"{index/FPS:g}/{DURATION:g} s; elapsed {time.perf_counter()-start:.1f} s", flush=True)
        process.stdin.close()
        error = process.stderr.read().decode(errors="replace")
        if process.wait():
            raise RuntimeError(error)
    except BaseException:
        process.kill()
        process.wait()
        raise
    print(json.dumps({"video":str(output), "bytes":output.stat().st_size}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    if args.check:
        checks()
    if args.preview:
        previews()
    if args.render:
        render()
