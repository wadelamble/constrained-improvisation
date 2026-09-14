"""Three-second blue/red wave bookends for the corrected desktop animation.

The wave is the SAME complex scalar field as the phasors: the same outgoing
cylindrical source, aperture, Rayleigh--Sommerfeld kernel, amplitude units,
and fixed central-sum display phase. Only the carrier is animated. The color
map is one fixed signed-field map everywhere; there is no independent gain
on the transmitted side and no coherence/intensity contrast enhancement.

The middle video is stream-copied, and every decoded middle-frame hash is
checked against the input. This guarantees the accepted three-pane sequence
is retained exactly while adding 72 wave frames on each side at 24 fps.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess

import corrected_tip_to_tail_model as physics
import numpy as np
from numpy.polynomial.legendre import leggauss
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import generate_symmetry_tip_to_tail_corrected as desktop

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"
CACHE = ROOT / ".tools" / "corrected-wave-bookends"
CANONICAL = "symmetry-many-slit-paths-phasors-interference"
VERSION = f"{CANONICAL}-v3-wave-bookends"
WIDTH, HEIGHT = 1280, 720
NX, NY = 640, 360
FPS = 24
BOOKEND_SECONDS = 3.0
BOOKEND_FRAMES = round(BOOKEND_SECONDS * FPS)
MIDDLE_FRAMES = round(desktop.DURATION * FPS)
TOTAL_FRAMES = MIDDLE_FRAMES + 2 * BOOKEND_FRAMES
TOTAL_SECONDS = TOTAL_FRAMES / FPS
X_MIN, X_MAX = -6.5, 5.5
Y_MIN, Y_MAX = -3.375, 3.375
X_VALUES = X_MIN + (np.arange(NX) + .5) * (X_MAX - X_MIN) / NX
Y_VALUES = Y_MAX - (np.arange(NY) + .5) * (Y_MAX - Y_MIN) / NY
DISPLAY_ROTATION = complex(np.exp(-1j * np.angle(physics.total(0.0))))
NEUTRAL = np.asarray((3.0, 3.0, 8.0))
POSITIVE = np.asarray((255.0, 42.0, 91.0))
NEGATIVE = np.asarray((37.0, 137.0, 255.0))
COLOR_SCALE = 1.3
COLOR_POWER = .75


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=8)
def quadrature(order):
    nodes, weights = leggauss(order)
    half = np.diff(physics.EDGES)[:, None] / 2
    y = (physics.EDGES[:-1, None] + physics.EDGES[1:, None]) / 2 + half * nodes
    weighted_incident = physics.source(physics.Z1, y) * half * weights / physics.REFERENCE
    return y.ravel(), weighted_incident.ravel()


def transmitted_field(z, y, order=12):
    """The same 49 element integrals, evaluated at arbitrary downstream points."""
    y = np.atleast_1d(y)
    samples, weighted_incident = quadrature(order)
    return np.sum(physics.kernel(z, y[:, None] - samples[None, :]) * weighted_incident, axis=1)


def order_for_distance(z):
    # Resolve the sharply localized kernel immediately after the aperture.
    # The nearest right-hand raster column is z=0.015625, not z=0.
    return 64 if z < .04 else 24 if z < .12 else 12


def field_key():
    material = (ROOT / "scripts" / "corrected_tip_to_tail_model.py").read_bytes()
    config = ("RS-direct-grid-v1", NX, NY, X_MIN, X_MAX, Y_MIN, Y_MAX, "64/24/12 at .04/.12")
    return hashlib.sha256(material + repr(config).encode()).hexdigest()[:20]


def complex_wave_field():
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"field-{field_key()}.npz"
    if path.exists():
        with np.load(path) as saved:
            field = saved["field"]
        assert field.shape == (NY, NX) and np.isfinite(field).all()
        print("Using cached complex wave field", flush=True)
        return field
    xx, yy = np.meshgrid(X_VALUES, Y_VALUES)
    field = physics.source(xx + physics.Z1, yy) / physics.REFERENCE
    columns = np.flatnonzero(X_VALUES > 0)
    for index, column in enumerate(columns):
        z = float(X_VALUES[column])
        field[:, column] = transmitted_field(z, Y_VALUES, order_for_distance(z))
        if index % 32 == 0 or index + 1 == len(columns):
            print(f"Wave field: {index + 1}/{len(columns)} downstream columns", flush=True)
    assert np.isfinite(field).all()
    np.savez_compressed(path, field=field)
    return field


def full_resolution_field(field):
    # Interpolate the complex field BEFORE applying the signed color map.
    # Pixel-center coordinates and equal x/y scale preserve circular fronts.
    real = Image.fromarray(np.asarray(field.real, dtype=np.float32)).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
    imag = Image.fromarray(np.asarray(field.imag, dtype=np.float32)).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
    return DISPLAY_ROTATION * (np.asarray(real) + 1j * np.asarray(imag))


def font(size):
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


LABEL_FONT = font(23)


def xy(x, y):
    scale = WIDTH / (X_MAX - X_MIN)
    assert abs(scale - HEIGHT / (Y_MAX - Y_MIN)) < 1e-12
    return ((x - X_MIN) * scale, (Y_MAX - y) * scale)


def wave_frame(field, index, opening):
    # The phasors are frequency-domain quantities, not a running optical clock.
    # End the opening on phase zero; begin the closing on phase zero. This
    # makes the colors at the adjacent B equal Re(the displayed sum).
    phase_index = index - (BOOKEND_FRAMES - 1) if opening else index
    phase = 2 * math.pi * phase_index / BOOKEND_FRAMES
    signed = np.real(field * np.exp(-1j * phase))
    strength = np.tanh(np.abs(signed) / COLOR_SCALE) ** COLOR_POWER
    target = np.where((signed >= 0)[..., None], POSITIVE, NEGATIVE)
    rgb = NEUTRAL + (target - NEUTRAL) * strength[..., None]
    image = Image.fromarray(np.asarray(np.clip(rgb, 0, 255), dtype=np.uint8))
    draw = ImageDraw.Draw(image, "RGBA")
    wall_x, aperture_top = xy(0, physics.HALF_APERTURE)
    _, aperture_bottom = xy(0, -physics.HALF_APERTURE)
    # Exactly the finite opening from the middle sequence; no artificial
    # separate opaque bars are introduced between its 49 integration elements.
    for y0, y1 in ((0, aperture_top), (aperture_bottom, HEIGHT)):
        draw.line((wall_x, y0, wall_x, y1), fill=(3, 3, 8, 245), width=9)
        draw.line((wall_x, y0, wall_x, y1), fill=(239, 232, 226, 245), width=4)
    detector_x, _ = xy(physics.Z2, 0)
    draw.line((detector_x, 0, detector_x, HEIGHT), fill=(238, 232, 226, 65), width=1)
    b = 0.0 if opening else desktop.old.SELECTED_B
    for label, point in (("A", xy(-physics.Z1, 0)), ("B", xy(physics.Z2, b))):
        x, y = point
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(3, 3, 8, 235))
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 244, 232, 255))
        draw.text((x + 15, y - 15), label, font=LABEL_FONT, fill=(255, 244, 232), stroke_width=2, stroke_fill=(3, 3, 8))
    return image


def model_checks(field):
    positions = np.linspace(-3.2, 3.2, 129)
    expected = np.array([physics.total(float(b)) for b in positions])
    actual = transmitted_field(physics.Z2, positions)
    detector_error = float(np.max(abs(actual - expected)))
    phase_error = float(np.max(abs(np.angle(actual / expected))))
    intensity_error = float(np.max(abs(abs(actual) ** 2 - abs(expected) ** 2)))
    near_error = 0.0
    for z in X_VALUES[(X_VALUES > 0) & (X_VALUES < .15)]:
        standard = transmitted_field(float(z), Y_VALUES[::7], order_for_distance(float(z)))
        refined = transmitted_field(float(z), Y_VALUES[::7], 96)
        near_error = max(near_error, float(np.max(abs(standard - refined))))
    assert detector_error < 1e-12 and phase_error < 1e-12 and intensity_error < 1e-12
    assert near_error < 1e-7
    # A few far-side grid columns must also reproduce the integral rather than
    # a synthetic wave pattern or a field computed from the old raw weights.
    grid_error = max(float(np.max(abs(field[:, column] - transmitted_field(float(X_VALUES[column]), Y_VALUES))))
                     for column in (400, 500, 586, 620))
    assert grid_error < 1e-12
    return {
        "detector_complex_sum_max_error": detector_error,
        "detector_phase_max_error_radians": phase_error,
        "detector_intensity_max_error": intensity_error,
        "near_aperture_quadrature_refinement_max_error": near_error,
        "display_grid_vs_same_integral_error": grid_error,
        "equal_xy_scale": True,
        "fixed_display_phase_degrees": float(np.angle(DISPLAY_ROTATION, deg=True)),
        "color_map": "one fixed signed-field map: tanh(abs(Re(E))/1.3)^0.75; red positive, blue negative",
        "source_aperture_wavelength": "identical to corrected_tip_to_tail_model.py",
        "bookend_B": [0.0, float(desktop.old.SELECTED_B)],
    }


def save_wave_previews(field, prefix):
    sheet = Image.new("RGB", (1920, 772), (3, 3, 8))
    draw = ImageDraw.Draw(sheet)
    for row, opening in enumerate((True, False)):
        for col, index in enumerate((0, 24, 71)):
            picture = wave_frame(field, index, opening)
            name = f"{prefix}-{'opening' if opening else 'closing'}-{index:02d}.png"
            picture.save(OUT / name)
            sheet.paste(picture.resize((640, 360), Image.Resampling.LANCZOS), (col * 640, row * 386))
            draw.text((col * 640 + 14, row * 386 + 365), f"{'opening' if opening else 'closing'}: frame {index}", fill=(240, 235, 230))
    sheet.save(OUT / f"{prefix}-wave-contact-sheet.png")


def encode_wave(field, path, opening):
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-", "-an",
               "-c:v", "libx264", "-threads", "2", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for index in range(BOOKEND_FRAMES):
        process.stdin.write(wave_frame(field, index, opening).tobytes())
    process.stdin.close()
    error = process.stderr.read().decode("utf-8", errors="replace")
    if process.wait():
        raise RuntimeError(error)
    frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(path))
    assert frames == BOOKEND_FRAMES and abs(seconds - BOOKEND_SECONDS) < .001
    print(f"Encoded {'opening' if opening else 'closing'}: {frames} frames / {seconds:g} seconds", flush=True)


def decoded_hashes(path, start=None, stop=None):
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(path)]
    if start is not None:
        command += ["-vf", f"trim=start_frame={start}:end_frame={stop},setpts=PTS-STARTPTS"]
    command += ["-f", "framemd5", "-"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return [line.rsplit(",", 1)[1].strip() for line in result.stdout.splitlines() if line and not line.startswith("#")]


def combined_previews(video, prefix):
    times = (0.0, 1.5, 3.0, 6.7, 10.5, 13.0, 20.0, 21.5, 23.0)
    selected = {round(t * FPS): (i, t) for i, t in enumerate(times)}
    reader = imageio_ffmpeg.read_frames(str(video), pix_fmt="rgb24", output_params=["-threads", "1"])
    metadata = next(reader)
    assert metadata["size"] == (WIDTH, HEIGHT)
    sheet = Image.new("RGB", (1920, 1158), desktop.old.BG)
    draw = ImageDraw.Draw(sheet)
    found = 0
    for index, data in enumerate(reader):
        if index in selected or index == TOTAL_FRAMES - 1:
            picture = Image.frombytes("RGB", (WIDTH, HEIGHT), data)
            if index in selected:
                slot, seconds = selected[index]
                x, y = slot % 3 * 640, slot // 3 * 386
                sheet.paste(picture.resize((640, 360), Image.Resampling.LANCZOS), (x, y))
                draw.text((x + 16, y + 364), f"{seconds:g} s (encoded)", fill=desktop.old.INK)
                found += 1
            if index == TOTAL_FRAMES - 1:
                picture.save(OUT / f"{prefix}-final.png")
    assert index + 1 == TOTAL_FRAMES and found == len(selected)
    sheet.save(OUT / f"{prefix}-contact-sheet.png")


def build(reuse_middle=None, preview_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = complex_wave_field()
    checks = model_checks(raw)
    print(json.dumps(checks, indent=2), flush=True)
    field = full_resolution_field(raw)
    save_wave_previews(field, VERSION)
    if preview_only:
        return
    desktop.center_presentation()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if reuse_middle is None:
        body_prefix = f"iterations/{CANONICAL}-{stamp}-centered-body"
        desktop.render(body_prefix, desktop.desktop, (WIDTH, HEIGHT))
        middle = OUT / f"{body_prefix}.mp4"
    else:
        middle = Path(reuse_middle).resolve()
    frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(middle))
    assert frames == MIDDLE_FRAMES and abs(seconds - desktop.DURATION) < .001, "The middle must be the 18.5-second three-pane video, without existing bookends."
    opening, closing = CACHE / "opening.mp4", CACHE / "closing.mp4"
    encode_wave(field, opening, True)
    encode_wave(field, closing, False)
    manifest = CACHE / "concat.txt"
    paths = (opening.resolve(), middle.resolve(), closing.resolve())
    manifest.write_text("".join("file '" + p.as_posix().replace("'", "'\\''") + "'\n" for p in paths), encoding="utf-8")
    versions = OUT / "iterations"
    versions.mkdir(parents=True, exist_ok=True)
    version_prefix = "iterations/" + VERSION
    if (OUT / f"{version_prefix}.mp4").exists():
        version_prefix = f"iterations/{CANONICAL}-{stamp}-wave-bookends"
    output = OUT / f"{version_prefix}.mp4"
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(manifest), "-c", "copy", "-movflags", "+faststart", str(output)], check=True)
    frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(output))
    assert frames == TOTAL_FRAMES and abs(seconds - TOTAL_SECONDS) < .001
    original_hashes = decoded_hashes(middle)
    preserved_hashes = decoded_hashes(output, BOOKEND_FRAMES, BOOKEND_FRAMES + MIDDLE_FRAMES)
    assert len(original_hashes) == MIDDLE_FRAMES and preserved_hashes == original_hashes
    combined_previews(output, version_prefix)
    archived = []
    for suffix in (".mp4", "-final.png", "-contact-sheet.png", "-validation.json"):
        current = OUT / f"{CANONICAL}{suffix}"
        if current.exists():
            target = versions / f"{CANONICAL}-{stamp}-previous{suffix}"
            shutil.copy2(current, target)
            archived.append(target.relative_to(ROOT).as_posix())
    report = {"canonical_video": f"{CANONICAL}.mp4", "versioned_video": f"{version_prefix}.mp4",
              "frames": frames, "seconds": seconds, "resolution": [WIDTH, HEIGHT], "fps": FPS,
              "bookend_frames_each": BOOKEND_FRAMES, "middle_frames": MIDDLE_FRAMES,
              "middle_decoded_frames_identical": True, "middle_source": middle.relative_to(ROOT).as_posix(),
              "middle_sha256": sha256(middle), "video_sha256": sha256(output), "wave_model_checks": checks,
              "previous_assets": archived, "full_decode_and_encoded_preview": "passed"}
    for suffix in (".mp4", "-contact-sheet.png", "-final.png"):
        shutil.copy2(OUT / f"{version_prefix}{suffix}", OUT / f"{CANONICAL}{suffix}")
    for name in (CANONICAL, version_prefix):
        (OUT / f"{name}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for filename in ("generate_symmetry_desktop_wave_bookends.py", "generate_symmetry_many_slit_paths_phasors_interference.py"):
        snapshot = ROOT / "scripts" / "iterations" / f"{Path(filename).stem}-{stamp}-v3.py"
        shutil.copy2(ROOT / "scripts" / filename, snapshot)
    print(json.dumps(report, indent=2), flush=True)


def render_canonical_desktop():
    build()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="calculate and inspect the wave without replacing the canonical movie")
    parser.add_argument("--reuse-middle", type=Path, help="reuse an already approved 18.5-second centered desktop video")
    args = parser.parse_args()
    build(args.reuse_middle, args.preview)
