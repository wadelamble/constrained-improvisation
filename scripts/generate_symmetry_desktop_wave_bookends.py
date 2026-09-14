"""Four-second wave-and-intensity introduction to the corrected desktop movie.

The wave is the SAME complex scalar field as the phasors: the same outgoing
cylindrical source, aperture, Rayleigh--Sommerfeld kernel, amplitude units,
and fixed central-sum display phase. The carrier animates hue; local
intensity controls ink strength. One common exposure is used everywhere,
with no independent gain on the transmitted side. The strongest source
region reaches the display limit; detector variations remain unclipped.

Hue carries the carrier phase and ink strength carries local |E(x,y)|^2
throughout the wave itself. There is no detector strip or separate curve.
The validated 49-slit body follows the four-second wave intro, with no
closing wave segment. Every decoded body frame matches its input render.
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

import perforated_tip_to_tail_model as physics
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import generate_symmetry_slit_tip_to_tail as desktop

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"
CACHE = ROOT / ".tools" / "corrected-wave-bookends"
CANONICAL = "symmetry-many-slit-paths-phasors-interference"
VERSION_NUMBER = 7
VERSION = f"{CANONICAL}-v{VERSION_NUMBER}-intensity-in-the-wave"
WIDTH, HEIGHT = 1280, 720
NX, NY = 640, 360
FPS = 24
INTRO_SECONDS = 4.0
INTRO_FRAMES = round(INTRO_SECONDS * FPS)
CARRIER_PERIOD_FRAMES = 2 * FPS
MIDDLE_FRAMES = round(desktop.DURATION * FPS)
TOTAL_FRAMES = MIDDLE_FRAMES + INTRO_FRAMES
TOTAL_SECONDS = TOTAL_FRAMES / FPS
# Pull back equally in x and y so the opaque screen ends are clearly visible.
# This changes framing only, not source/aperture/detector geometry.
Y_MIN, Y_MAX = -4.0, 4.0
WORLD_WIDTH = (Y_MAX - Y_MIN) * WIDTH / HEIGHT
# Half a raster sample offsets the view so x=0 falls between sample columns.
WORLD_CENTER_X = -.5 + WORLD_WIDTH / NX / 2
X_MIN, X_MAX = WORLD_CENTER_X - WORLD_WIDTH / 2, WORLD_CENTER_X + WORLD_WIDTH / 2
X_VALUES = X_MIN + (np.arange(NX) + .5) * (X_MAX - X_MIN) / NX
Y_VALUES = Y_MAX - (np.arange(NY) + .5) * (Y_MAX - Y_MIN) / NY
DISPLAY_ROTATION = complex(np.exp(-1j * np.angle(physics.total(0.0))))
# Equal-luma inks make phase mostly a hue change. Their common contrast
# against paper is then controlled by local intensity, not the optical clock.
# These are graphic color values, not a claim about electromagnetic color.
LUMA_WEIGHTS = np.asarray((.2126, .7152, .0722))
INK_LUMA = 106.
def equal_luma_ink(red, blue):
    green = (INK_LUMA - LUMA_WEIGHTS[0]*red - LUMA_WEIGHTS[2]*blue) / LUMA_WEIGHTS[1]
    return np.asarray((red, green, blue))
POSITIVE = equal_luma_ink(174., 85.)
NEGATIVE = equal_luma_ink(62., 150.)
PHASE_NEUTRAL = np.full(3, INK_LUMA)
NEUTRAL = np.asarray(desktop.old.PANEL, dtype=float)
INTENSITY_EXPOSURE = 1.6
MAX_INK_STRENGTH = .90
PAPER = tuple(desktop.old.BG)
SCREEN_INK = tuple(desktop.old.INK)
COLOR_DESCRIPTION = "equal-luma red/gray/blue carrier phase; ink strength min(1.6*abs(E)^2, .90) throughout the field; no detector overlay"
# The wave occupies the whole scene. Preserve equal physical x/y scales
# and show the complete -3.2..3.2 detector range used by the schematic.
WAVE_LEFT, WAVE_TOP, WAVE_RIGHT, WAVE_BOTTOM = 90, 95, 1190, 680
WAVE_WIDTH, WAVE_HEIGHT = WAVE_RIGHT - WAVE_LEFT, WAVE_BOTTOM - WAVE_TOP
VIEW_Y_MIN, VIEW_Y_MAX = -3.2, 3.2
PIXELS_PER_UNIT = WAVE_HEIGHT / (VIEW_Y_MAX - VIEW_Y_MIN)
VIEW_X_MAX = physics.Z2
VIEW_X_MIN = VIEW_X_MAX - WAVE_WIDTH / PIXELS_PER_UNIT
DETECTOR_Y = VIEW_Y_MAX - (np.arange(WAVE_HEIGHT) + .5) / PIXELS_PER_UNIT
DETECTOR_FIELD = physics.transmitted_field(physics.Z2, DETECTOR_Y)
DETECTOR_INTENSITY = abs(DETECTOR_FIELD) ** 2
# This profile is retained for validation ONLY; it is never drawn or used
# to impose an envelope elsewhere. Every wave pixel uses its own local E.


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=8)
def quadrature(order):
    y, weights = physics.slit_quadrature(order)
    weighted_incident = physics.source(physics.Z1, y) * weights / physics.REFERENCE
    return y.ravel(), weighted_incident.ravel()


def transmitted_field(z, y, order=12):
    """The same 49 disjoint slit integrals at arbitrary downstream points."""
    y = np.atleast_1d(y)
    samples, weighted_incident = quadrature(order)
    return np.sum(physics.kernel(z, y[:, None] - samples[None, :]) * weighted_incident, axis=1)


def order_for_distance(z):
    # Resolve the sharply localized kernel immediately after the aperture.
    # The raster uses pixel centers; no downstream column is at z=0.
    return 64 if z < .04 else 24 if z < .12 else 12


def model_fingerprint():
    material = b"".join((ROOT / "scripts" / name).read_bytes() for name in
                        ("corrected_tip_to_tail_model.py", "perforated_tip_to_tail_model.py"))
    return hashlib.sha256(material).hexdigest()


def field_key():
    material = model_fingerprint().encode()
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
    # Crop the existing physical field, then interpolate complex values
    # BEFORE coloring. The detector is at the right edge of this crop.
    extent = ((VIEW_X_MIN-X_MIN)*NX/(X_MAX-X_MIN), (Y_MAX-VIEW_Y_MAX)*NY/(Y_MAX-Y_MIN),
              (VIEW_X_MAX-X_MIN)*NX/(X_MAX-X_MIN), (Y_MAX-VIEW_Y_MIN)*NY/(Y_MAX-Y_MIN))
    real = Image.fromarray(np.asarray(field.real, dtype=np.float32)).transform(
        (WAVE_WIDTH, WAVE_HEIGHT), Image.Transform.EXTENT, extent, Image.Resampling.BICUBIC)
    imag = Image.fromarray(np.asarray(field.imag, dtype=np.float32)).transform(
        (WAVE_WIDTH, WAVE_HEIGHT), Image.Transform.EXTENT, extent, Image.Resampling.BICUBIC)
    return DISPLAY_ROTATION * (np.asarray(real) + 1j * np.asarray(imag))


def font(size):
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


LABEL_FONT = font(23)
SMALL_FONT = font(17)
TITLE_FONT = font(26)
CAPTION_FONT = font(16)


def xy(x, y):
    return (WAVE_LEFT + (x - VIEW_X_MIN) * PIXELS_PER_UNIT,
            WAVE_TOP + (VIEW_Y_MAX - y) * PIXELS_PER_UNIT)


def wave_ink(field, phase):
    """Local intensity is visible everywhere without a grafted detector map.

    The former signed-field opacity allowed each phase zero crossing to
    wipe out the displayed intensity. Here the carrier only changes hue.
    The colored ink's strength is a global linear exposure of |E|^2. The
    finite display range clips the strongest region near A and the mask;
    detector intensities are all below the clipping threshold. There is no
    subtraction of a background, column normalization, mask change, or
    copying of the detector profile into the travelling field.
    """
    intensity = np.abs(field)**2
    phase_cosine = np.cos(np.angle(field) - phase)
    endpoint = np.where((phase_cosine >= 0)[..., None], POSITIVE, NEGATIVE)
    hue = PHASE_NEUTRAL + (endpoint - PHASE_NEUTRAL) * np.abs(phase_cosine)[..., None]
    strength = np.minimum(INTENSITY_EXPOSURE * intensity, MAX_INK_STRENGTH)
    rgb = NEUTRAL + (hue - NEUTRAL) * strength[..., None]
    return rgb, strength


def wave_frame(field, index):
    # Two slow carrier cycles in four seconds; end on the diagram's fixed
    # phase reference. Detector intensity remains steady under this clock.
    phase_index = index - (INTRO_FRAMES - 1)
    phase = 2 * math.pi * phase_index / CARRIER_PERIOD_FRAMES
    rgb, _ = wave_ink(field, phase)
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((73, 79, 1207, 689), radius=17,
                           fill=desktop.old.PANEL, outline=(215, 209, 199), width=2)
    image.paste(Image.fromarray(np.asarray(np.clip(rgb, 0, 255), dtype=np.uint8)), (WAVE_LEFT, WAVE_TOP))
    draw.text((73, 22), "49 slits · interference in the travelling wave", font=TITLE_FONT, fill=SCREEN_INK)
    draw.text((73, 57), "Stronger color marks greater local intensity", font=SMALL_FONT, fill=desktop.old.MUTED)
    wall_x, _ = xy(0, 0)
    # The opaque complement comes from the same 49 finite slit bounds that
    # determine the integrals. Leave all 49 openings genuinely clear.
    for lower, upper in physics.opaque_intervals(VIEW_Y_MIN, VIEW_Y_MAX):
        _, y0 = xy(0, upper)
        _, y1 = xy(0, lower)
        draw.rectangle((wall_x - 5, y0, wall_x + 5, y1), fill=SCREEN_INK + (255,))
    draw.text((wall_x-27, 57), "49 slits", font=CAPTION_FONT, fill=SCREEN_INK)
    detector_x, _ = xy(physics.Z2, 0)
    # A thin location marker only: no brightness strip, curve, or side panel.
    draw.line((detector_x, WAVE_TOP, detector_x, WAVE_BOTTOM), fill=desktop.old.MUTED+(180,), width=1)
    draw.text((detector_x-37, 57), "detector", font=CAPTION_FONT, fill=SCREEN_INK)
    b = 0.0
    for label, point in (("A", xy(-physics.Z1, 0)), ("B", xy(physics.Z2, b))):
        x, y = point
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=PAPER + (255,))
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=SCREEN_INK + (255,))
        offset = -24 if label == "B" else -28
        draw.text((x + offset, y - 15), label, font=LABEL_FONT, fill=SCREEN_INK)
    draw.text((73, 696), "Color: wave phase    ·    Color strength: local intensity", font=CAPTION_FONT, fill=desktop.old.MUTED)
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
    profile_error = float(np.max(abs(abs(transmitted_field(physics.Z2, desktop.B_VALUES))**2 - desktop.INTENSITIES)))
    assert profile_error < 1e-12
    # Validate the actual color encoding, not just the wave calculation.
    # At the detector its contrast against paper must be proportional to
    # |E|^2 at every carrier phase, without clipping or an imposed profile.
    assert INTENSITY_EXPOSURE * float(np.max(DETECTOR_INTENSITY)) < MAX_INK_STRENGTH
    color_error = 0.
    for phase in (0., .8, 2.1, 3.4):
        rgb, strength = wave_ink(DISPLAY_ROTATION * DETECTOR_FIELD, phase)
        actual_strength = (NEUTRAL @ LUMA_WEIGHTS - rgb @ LUMA_WEIGHTS) / (NEUTRAL @ LUMA_WEIGHTS - INK_LUMA)
        expected_strength = INTENSITY_EXPOSURE * DETECTOR_INTENSITY
        color_error = max(color_error, float(np.max(abs(actual_strength-expected_strength))))
    assert color_error < 1e-12
    return {
        "detector_complex_sum_max_error": detector_error,
        "detector_phase_max_error_radians": phase_error,
        "detector_intensity_max_error": intensity_error,
        "near_aperture_quadrature_refinement_max_error": near_error,
        "display_grid_vs_same_integral_error": grid_error,
        "equal_xy_scale": True,
        "fixed_display_phase_degrees": float(np.angle(DISPLAY_ROTATION, deg=True)),
        "color_map": COLOR_DESCRIPTION,
        "world_bounds": [X_MIN, X_MAX, Y_MIN, Y_MAX],
        "screen_opening_bounds": [-float(physics.HALF_APERTURE), float(physics.HALF_APERTURE)],
        "source_aperture_wavelength": "identical to perforated_tip_to_tail_model.py",
        "slit_count": physics.SLIT_COUNT,
        "slit_width": physics.SLIT_WIDTH,
        "opaque_gap_width": physics.GAP_WIDTH,
        "intro_B": 0.0,
        "view_bounds": [VIEW_X_MIN, VIEW_X_MAX, VIEW_Y_MIN, VIEW_Y_MAX],
        "wave_intensity_vs_schematic_profile_max_error": profile_error,
        "color_strength_vs_local_intensity_max_error": color_error,
        "intensity_encoding": "ink strength follows local |E(x,y)|^2 everywhere; equal-luma phase inks; no detector strip or curve",
        "global_intensity_exposure": INTENSITY_EXPOSURE,
        "intensity_display_clipping_threshold": MAX_INK_STRENGTH / INTENSITY_EXPOSURE,
        "detector_intensity_unclipped": True,
        "detector_intensity_min_max": [float(np.min(DETECTOR_INTENSITY)), float(np.max(DETECTOR_INTENSITY))],
    }


def save_wave_previews(field, prefix):
    sheet = Image.new("RGB", (1920, 772), desktop.old.BG)
    draw = ImageDraw.Draw(sheet)
    for slot, index in enumerate((0, 16, 32, 48, 64, 95)):
        row, col = divmod(slot, 3)
        picture = wave_frame(field, index)
        picture.save(OUT / f"{prefix}-intro-{index:02d}.png")
        sheet.paste(picture.resize((640, 360), Image.Resampling.LANCZOS), (col * 640, row * 386))
        draw.text((col * 640 + 14, row * 386 + 365), f"intro: frame {index}", fill=desktop.old.INK)
    sheet.save(OUT / f"{prefix}-wave-contact-sheet.png")


def encode_wave(field, path):
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-", "-an",
               "-c:v", "libx264", "-threads", "2", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for index in range(INTRO_FRAMES):
        process.stdin.write(wave_frame(field, index).tobytes())
    process.stdin.close()
    error = process.stderr.read().decode("utf-8", errors="replace")
    if process.wait():
        raise RuntimeError(error)
    frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(path))
    assert frames == INTRO_FRAMES and abs(seconds - INTRO_SECONDS) < .001
    print(f"Encoded wave intro: {frames} frames / {seconds:g} seconds", flush=True)


def decoded_hashes(path, start=None, stop=None):
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(path)]
    if start is not None:
        command += ["-vf", f"trim=start_frame={start}:end_frame={stop},setpts=PTS-STARTPTS"]
    command += ["-f", "framemd5", "-"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return [line.rsplit(",", 1)[1].strip() for line in result.stdout.splitlines() if line and not line.startswith("#")]


def combined_previews(video, prefix):
    times = (0.0, 1.25, 3.75, 4.0, 7.7, 11.5, 14.0, 20.0, 22.0)
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
    desktop.center_presentation()
    mask_checks = physics.checks()
    layout_checks = desktop.visual_checks()
    raw = complex_wave_field()
    checks = model_checks(raw)
    print(json.dumps(checks, indent=2), flush=True)
    field = full_resolution_field(raw)
    save_wave_previews(field, VERSION)
    for seconds in (3.7, 7.5, 17.0):
        desktop.desktop(seconds).save(OUT / f"{VERSION}-body-check-{seconds:g}.png")
    if preview_only:
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if reuse_middle is None:
        body_prefix = f"iterations/{CANONICAL}-{stamp}-centered-body"
        desktop.render(body_prefix, desktop.desktop, (WIDTH, HEIGHT))
        middle = OUT / f"{body_prefix}.mp4"
        middle.with_suffix(".model.json").write_text(json.dumps({
            "model_fingerprint": model_fingerprint(), "video_sha256": sha256(middle),
            "slit_count": physics.SLIT_COUNT, "geometry": "49 physical slits with opaque gaps"
        }, indent=2) + "\n", encoding="utf-8")
    else:
        middle = Path(reuse_middle).resolve()
        record = middle.with_suffix(".model.json")
        if not record.exists():
            raise ValueError("The reusable body needs a matching .model.json record. Render a fresh 49-slit body; the old continuous-aperture video is incompatible.")
        body_model = json.loads(record.read_text(encoding="utf-8"))
        assert body_model["model_fingerprint"] == model_fingerprint(), "Body and wave use different slit models"
        assert body_model["video_sha256"] == sha256(middle), "Reusable body differs from its model record"
    frames, seconds = imageio_ffmpeg.count_frames_and_secs(str(middle))
    assert frames == MIDDLE_FRAMES and abs(seconds - desktop.DURATION) < .001, "The middle must be the 18.5-second three-pane video, without existing bookends."
    opening = CACHE / f"opening-v{VERSION_NUMBER}.mp4"
    encode_wave(field, opening)
    manifest = CACHE / "concat.txt"
    paths = (opening.resolve(), middle.resolve())
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
    preserved_hashes = decoded_hashes(output, INTRO_FRAMES, INTRO_FRAMES + MIDDLE_FRAMES)
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
              "intro_frames": INTRO_FRAMES, "intro_seconds": INTRO_SECONDS,
              "closing_wave_frames": 0, "middle_frames": MIDDLE_FRAMES,
              "middle_decoded_frames_identical": True, "middle_source": middle.relative_to(ROOT).as_posix(),
              "middle_sha256": sha256(middle), "video_sha256": sha256(output), "wave_model_checks": checks,
              "slit_model_checks": mask_checks, "layout_checks": layout_checks,
              "body_geometry": "recalculated with the same 49 physical slits as the waves",
              "previous_assets": archived, "full_decode_and_encoded_preview": "passed"}
    for suffix in (".mp4", "-contact-sheet.png", "-final.png"):
        shutil.copy2(OUT / f"{version_prefix}{suffix}", OUT / f"{CANONICAL}{suffix}")
    for name in (CANONICAL, version_prefix):
        (OUT / f"{name}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for filename in ("generate_symmetry_desktop_wave_bookends.py", "generate_symmetry_many_slit_paths_phasors_interference.py",
                     "generate_symmetry_slit_tip_to_tail.py", "perforated_tip_to_tail_model.py",
                     "corrected_tip_to_tail_model.py"):
        snapshot = ROOT / "scripts" / "iterations" / f"{Path(filename).stem}-{stamp}-v{VERSION_NUMBER}.py"
        shutil.copy2(ROOT / "scripts" / filename, snapshot)
    print(json.dumps(report, indent=2), flush=True)


def render_canonical_desktop():
    build()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="calculate and inspect the wave without replacing the canonical movie")
    parser.add_argument("--reuse-middle", type=Path, help="reuse a matching 49-slit body with its .model.json record")
    args = parser.parse_args()
    build(args.reuse_middle, args.preview)
