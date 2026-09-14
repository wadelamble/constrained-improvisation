"""Render corrected standalone and three-pane versions without changing old films."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import shutil
import subprocess

import corrected_tip_to_tail_model as model
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg
import generate_symmetry_many_slit_paths_phasors_interference as old

wave = old.wave
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-tip-to-tail-corrected"
DESKTOP = "symmetry-many-slit-corrected"
CENTERED_PRESENTATION = False
DISPLAY_ROTATION = 1.0 + 0.0j
FPS, DURATION = old.FPS, old.DURATION
SCALE = 2
SAMPLES = (1.8, 3.7, 6.5, 7.5, 8.7, 10.0, 11.85, 13.7, 17.0)
B_VALUES = np.linspace(3.2, -3.2, 257)
TOTALS = np.array([model.total(float(b)) for b in B_VALUES])
INTENSITIES = abs(TOTALS) ** 2
FREE_INTENSITIES = abs(model.free_amplitude(B_VALUES)) ** 2
IMAX = max(1.0, float(np.max(INTENSITIES)), float(np.max(abs(model.chain(0.0)) ** 2))) * 1.06
RADIUS = max(
    max(float(np.max(abs(model.chain(float(b))))), abs(model.free_amplitude(float(b))))
    for b in np.linspace(-3.2, 3.2, 1025)
)


def center_presentation():
    """User-requested presentation 'cheat'; leave the physical model intact.

    The finite aperture gives total(0) a real ~-5.058 degree phase relative
    to the unobstructed central wave. For this presentation ONLY, choose the
    completed finite-aperture sum at B=0 as phase zero. Apply the SAME unit
    complex factor to every contribution and partial sum at every B and t.
    This is a fixed change of display reference, not a phase correction to
    the physics, and not a B-dependent straightening of the resultant.

    Arrow magnitudes, tip-to-tail addition, subsequent angular motion, and
    detector intensities are unchanged. Omit the gray no-screen phasor in
    this copy: retaining it would show the same ~5 degree relative offset,
    merely on the other side of the axis. The unadjusted film remains the
    explicit comparison with unobstructed propagation. The gray INTENSITY
    curve in pane three is unaffected and remains useful.
    """
    global CENTERED_PRESENTATION, DISPLAY_ROTATION, NAME, DESKTOP
    CENTERED_PRESENTATION = True
    DISPLAY_ROTATION = complex(np.exp(-1j * np.angle(model.total(0.0))))
    NAME = "symmetry-tip-to-tail-corrected-centered"
    DESKTOP = "symmetry-many-slit-corrected-centered"


def text(draw, xy, message, fill=old.INK, font=old.LABEL, anchor=None):
    wave.draw_text(draw, xy, message, fill=fill, font_obj=font, anchor=anchor)


def line(draw, a, b, color, width=1):
    draw.line(tuple(wave.s(v) for v in (*a, *b)), fill=color, width=wave.s(width))


def arrow(draw, a, b, color, width=2, head=5):
    length = math.dist(a, b)
    if length < 0.08:
        return
    line(draw, a, b, color, width)
    head = min(head, 0.42 * length)
    theta = math.atan2(b[1] - a[1], b[0] - a[0])
    vertices = [b] + [(b[0] - head * math.cos(theta + t), b[1] - head * math.sin(theta + t)) for t in (-0.5, 0.5)]
    draw.polygon([(wave.s(x), wave.s(y)) for x, y in vertices], fill=color)


def mapper(bounds):
    left, top, right, bottom = bounds
    origin = ((left + right) / 2, (top + bottom) / 2)
    scale = (min(right - left, bottom - top) / 2 - 20) / RADIUS
    return lambda value: (origin[0] + value.real * scale, origin[1] - value.imag * scale), scale


def phasors(draw, seconds, bounds, compact=False):
    b, count, active, fraction, complete, *_ = old.animation_state(seconds)
    terms = DISPLAY_ROTATION * model.contributions(float(b))
    values = DISPLAY_ROTATION * model.chain(b)
    point, scale = mapper(bounds)
    origin = point(0j)
    left, top, right, bottom = bounds
    line(draw, (left, origin[1]), (right, origin[1]), wave.rgba(old.MUTED, .25))
    line(draw, (origin[0], top), (origin[0], bottom), wave.rgba(old.MUTED, .25))
    text(draw, (right, origin[1] - 24), "Re", old.MUTED, old.SMALL, "ra")
    text(draw, (origin[0] + 8, top), "Im", old.MUTED, old.SMALL)
    if not CENTERED_PRESENTATION:
        reference_end = point(DISPLAY_ROTATION * model.free_amplitude(b))
        wave.dashed_line(draw, origin, reference_end, wave.rgba(old.MUTED, .57), width=2, dash=5, gap=4)
        # A hollow marker keeps the reference distinguishable when nearly aligned.
        wave.circle(draw, reference_end, 4.2, old.PANEL, outline=wave.rgba(old.MUTED, .75), width=1)
    for index in range(count):
        arrow(draw, point(values[index]), point(values[index + 1]), wave.rgba(old.BLUE, .86), width=2, head=3.6 if compact else 5)
    current = values[count]
    if active is not None:
        current = values[active] + fraction * terms[active]
        arrow(draw, point(values[active]), point(current), old.GOLD, width=3 if compact else 4, head=6)
    if count or active is not None:
        if complete:
            arrow(draw, origin, point(current), old.GREEN, width=4 if compact else 5, head=9)
        else:
            wave.dashed_line(draw, origin, point(current), wave.rgba(old.GREEN, .43), width=2, dash=5, gap=4)
        wave.circle(draw, point(current), 2.6, old.GREEN if complete else old.GOLD)
    wave.circle(draw, origin, 2.2, old.MUTED)
    return b, current, complete


def standalone(seconds):
    image = Image.new("RGB", (960 * SCALE, 840 * SCALE), old.BG)
    draw = ImageDraw.Draw(image, "RGBA")
    wave.panel(draw, (24, 20, 936, 820))
    text(draw, (48, 39), "Tip-to-tail · normalized propagation", font=old.TITLE)
    text(draw, (48, 83), "49 aperture contributions · lengths carry amplitude", old.MUTED, old.SUBTITLE)
    b, count, active, _, complete, *_ = old.animation_state(seconds)
    status = "Complete sum" if complete else ("Ready" if active is None else f"Adding element {active + 1} / 49")
    text(draw, (48, 116), status, old.GREEN if complete else old.GOLD)
    text(draw, (912, 116), f"B = {b:+.2f}", old.MUTED, anchor="ra")
    phasors(draw, seconds, (72, 153, 888, 692))
    if CENTERED_PRESENTATION:
        text(draw, (48, 711), "Phase zero: the complete sum at central B. Reference and scale stay fixed.", old.MUTED, old.SMALL)
        text(draw, (48, 770), "Blue: contributions", old.BLUE)
        text(draw, (480, 770), "Gold: adding one", old.GOLD, anchor="ma")
        text(draw, (912, 770), "Green: sum", old.GREEN, anchor="ra")
    else:
        text(draw, (48, 711), "Phase zero: unobstructed A → central B. Reference and scale stay fixed.", old.MUTED, old.SMALL)
        text(draw, (48, 746), "Blue: aperture contributions", old.BLUE)
        text(draw, (912, 746), "Gray: without the screen", old.MUTED, anchor="ra")
        text(draw, (48, 777), "Gold: adding one contribution", old.GOLD)
        text(draw, (912, 777), "Green: their sum", old.GREEN, anchor="ra")
    return image.convert("RGB").resize((960, 840), Image.Resampling.LANCZOS)


def route_panel(draw, seconds):
    b, count, active, fraction, complete, *_ = old.animation_state(seconds)
    wave.panel(draw, old.ROUTE_PANEL)
    text(draw, (58, 145), "routes through the aperture", font=old.PANE_TITLE)
    text(draw, (58, 172), "49 elements · one contribution per element", old.MUTED, old.SMALL)
    for y in model.CENTERS[:count]:
        old.draw_route(draw, float(y), b, wave.rgba(old.BLUE, .13), 2)
    # The interval is one opening, not 49 arbitrary zero-width holes.
    x = old.ROUTE_SCREEN_X
    opening_top, opening_bottom = old.route_y(model.HALF_APERTURE), old.route_y(-model.HALF_APERTURE)
    line(draw, (x, old.ROUTE_TOP), (x, opening_top), old.INK, 5)
    line(draw, (x, opening_bottom), (x, old.ROUTE_BOTTOM), old.INK, 5)
    line(draw, (x, opening_top), (x, opening_bottom), wave.rgba(old.MUTED, .20), 1)
    for y in model.CENTERS:
        wave.circle(draw, (x, old.route_y(float(y))), 1.6, wave.rgba(old.BLUE, .6))
    old.draw_detector_line(draw, b)
    if complete:
        y = old.stationary_opening_y(b)
        old.draw_route(draw, y, b, wave.rgba(old.GOLD, .9), 3)
    elif active is not None:
        y = float(model.CENTERS[active])
        old.draw_route(draw, y, b, old.GOLD, 4)
        wave.circle(draw, (x, old.route_y(y)), 4, old.GOLD)
    wave.circle(draw, old.ROUTE_A, 7.5, old.INK)
    text(draw, (old.ROUTE_A[0] - 12, old.ROUTE_A[1]), "A", font=old.LABEL_BOLD, anchor="rm")
    text(draw, (x, 591), "finite aperture", old.MUTED, anchor="ma")
    text(draw, (old.ROUTE_DETECTOR_X, 591), "detector", old.MUTED, anchor="ma")


def detector_panel(draw, seconds, b, current, complete):
    wave.panel(draw, old.DETECTOR_PANEL)
    text(draw, (1052, 145), "intensity at detector", font=old.PANE_TITLE)
    text(draw, (1052, 172), "I = |sum|²", old.MUTED, old.SMALL)
    x0, x1 = 1065, 1218
    x_at = lambda value: x0 + (x1 - x0) * max(0, min(1, float(value) / IMAX))
    line(draw, (x0, 190), (x0, 568), wave.rgba(old.MUTED, .5))
    for j in range(0, len(B_VALUES) - 3, 7):
        a = (x_at(FREE_INTENSITIES[j]), old.detector_y(float(B_VALUES[j])))
        c = (x_at(FREE_INTENSITIES[j + 3]), old.detector_y(float(B_VALUES[j + 3])))
        line(draw, a, c, wave.rgba(old.MUTED, .45), 1)
    _, _, _, _, _, reveal, scanning, _ = old.animation_state(seconds)
    final_hold = seconds >= old.SETTLE_END
    if scanning or final_hold:
        visited = len(B_VALUES) if final_hold else max(2, round(reveal * len(B_VALUES)))
        pts = [(wave.s(x_at(v)), wave.s(old.detector_y(float(y)))) for y, v in zip(B_VALUES[:visited], INTENSITIES[:visited])]
        draw.line(pts, fill=old.BLUE, width=wave.s(2))
    value = abs(model.total(float(b)) if complete else current) ** 2
    marker = (x_at(value), old.detector_y(b))
    line(draw, (x0, marker[1]), marker, old.GOLD, 2)
    wave.circle(draw, marker, 4, old.GREEN)
    text(draw, (1140, 591), "gray: no screen", old.MUTED, old.SMALL, "ma")


def desktop(seconds):
    image = Image.new("RGB", (1280 * SCALE, 720 * SCALE), old.BG)
    draw = ImageDraw.Draw(image, "RGBA")
    text(draw, (42, 27), "Many paths · one consistent wave amplitude", font=old.TITLE)
    text(draw, (42, 68), "Complete propagation phases and weights · the same sum drives the detector", old.MUTED, old.SUBTITLE)
    route_panel(draw, seconds)
    wave.panel(draw, old.PHASOR_PANEL)
    text(draw, (625, 145), "complex contributions at B", font=old.PANE_TITLE)
    text(draw, (625, 172), "fixed phase reference and scale", old.MUTED, old.SMALL)
    b, current, complete = phasors(draw, seconds, (625, 202, 991, 557), True)
    text(draw, (810, 591), "green: sum" if CENTERED_PRESENTATION else "green: sum · gray: no screen", old.MUTED, old.SMALL, "ma")
    detector_panel(draw, seconds, b, current, complete)
    if CENTERED_PRESENTATION:
        text(draw, (42, 650), "Phase zero: the complete sum at central B. The reference stays fixed as B moves.", old.MUTED, old.SUBTITLE)
        text(draw, (42, 682), "2D scalar diffraction · 49 integrated aperture elements · lengths carry amplitude", old.MUTED, old.SMALL)
    else:
        text(draw, (42, 650), "Phase zero: the unobstructed field at central B. Moving B retains the travel phase.", old.MUTED, old.SUBTITLE)
        text(draw, (42, 682), "2D scalar diffraction · 49 integrated aperture elements · finite-aperture phase is retained", old.MUTED, old.SMALL)
    return image.convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)


def visual_checks():
    minimum_margin = float("inf")
    for bounds in ((72, 153, 888, 692), (625, 202, 991, 557)):
        point, _ = mapper(bounds)
        left, top, right, bottom = bounds
        for frame_index in range(round(DURATION * FPS)):
            b = old.animation_state(frame_index / FPS)[0]
            for value in DISPLAY_ROTATION * np.r_[model.chain(b), model.free_amplitude(b)]:
                x, y = point(value)
                minimum_margin = min(minimum_margin, x - left, right - x, y - top, bottom - y)
    assert minimum_margin > 18
    return {"minimum_plot_margin_pixels": minimum_margin, "same_scale_all_frames": True}


def previews():
    for name, render_frame, size in ((NAME, standalone, (480, 420)), (DESKTOP, desktop, (640, 360))):
        sheet = Image.new("RGB", (size[0] * 3, (size[1] + 26) * 3), old.BG)
        label = ImageDraw.Draw(sheet)
        for i, seconds in enumerate(SAMPLES):
            picture = render_frame(seconds)
            picture.save(OUT / f"{name}-check-{seconds:g}.png")
            x, y = i % 3 * size[0], i // 3 * (size[1] + 26)
            sheet.paste(picture.resize(size, Image.Resampling.LANCZOS), (x, y))
            label.text((x + 16, y + size[1] + 4), f"{seconds:g} s", fill=old.INK)
        sheet.save(OUT / f"{name}-contact-sheet.png")


def render(name, render_frame, size):
    video = OUT / f"{name}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-", "-an",
               "-c:v", "libx264", "-threads", "2", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(video)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for index in range(round(DURATION * FPS)):
        process.stdin.write(render_frame(index / FPS).tobytes())
        if index % (4 * FPS) == 0:
            print(f"{name}: {index / FPS:g}/{DURATION:g} seconds", flush=True)
    process.stdin.close()
    error = process.stderr.read().decode("utf-8", errors="replace")
    if process.wait():
        raise RuntimeError(error)
    count, seconds = imageio_ffmpeg.count_frames_and_secs(str(video))
    assert count == round(DURATION * FPS) and abs(seconds - DURATION) < .001
    decoded = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(video), "-f", "null", "-"], capture_output=True, check=True)
    assert not decoded.stderr
    return {"file": video.name, "frames": count, "seconds": seconds, "bytes": video.stat().st_size, "full_decode": "passed"}


def render_canonical_desktop():
    """Regenerate the named desktop asset with the approved centered treatment.

    The old generator's main() delegates here; its legacy geometry helpers
    remain importable by the historical reel and standalone experiments.
    Save the previous media before rendering, render and validate a separate
    version, then promote that version. A failed render cannot replace the
    current canonical video with a partial MP4.
    """
    center_presentation()
    canonical = old.NAME
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    versions = OUT / "iterations"
    versions.mkdir(parents=True, exist_ok=True)
    archived = []
    for suffix in (".mp4", "-contact-sheet.png", "-final.png", "-validation.json"):
        current = OUT / f"{canonical}{suffix}"
        if current.exists():
            backup = versions / f"{canonical}-{stamp}-previous{suffix}"
            shutil.copy2(current, backup)
            archived.append(backup.relative_to(ROOT).as_posix())

    prefix = f"iterations/{canonical}-{stamp}-centered"
    video = render(prefix, desktop, (1280, 720))
    sheet = Image.new("RGB", (1920, 1158), old.BG)
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(SAMPLES):
        x, y = index % 3 * 640, index // 3 * 386
        sheet.paste(desktop(seconds).resize((640, 360), Image.Resampling.LANCZOS), (x, y))
        draw.text((x + 16, y + 364), f"{seconds:g} s", fill=old.INK)
    sheet.save(OUT / f"{prefix}-contact-sheet.png")
    desktop(DURATION - 1 / FPS).save(OUT / f"{prefix}-final.png")
    report = {
        "canonical_video": f"{canonical}.mp4",
        "versioned_video": f"{prefix}.mp4",
        "video_checks": video,
        "fixed_display_rotation_degrees": float(np.angle(DISPLAY_ROTATION, deg=True)),
        "layout": visual_checks(),
        "previous_assets": archived,
    }
    for suffix in (".mp4", "-contact-sheet.png", "-final.png"):
        shutil.copy2(OUT / f"{prefix}{suffix}", OUT / f"{canonical}{suffix}")
    for name in (canonical, prefix):
        (OUT / f"{name}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--center-phase", action="store_true", help="presentation copy: set the complete central sum's phase to zero with one fixed display rotation")
    args = parser.parse_args()
    if args.center_phase:
        center_presentation()
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    if args.center_phase:
        report["display"] = {
            "fixed_rotation_degrees": float(np.angle(DISPLAY_ROTATION, deg=True)),
            "center_sum_after_rotation": [float((DISPLAY_ROTATION * model.total(0.0)).real), float((DISPLAY_ROTATION * model.total(0.0)).imag)],
            "gray_phase_comparison_omitted": True,
            "underlying_physics_validation": "symmetry-tip-to-tail-corrected-validation.json",
        }
        report["layout"] = visual_checks()
    if args.check:
        report["physics"] = model.checks()
        report["layout"] = visual_checks()
        print(json.dumps(report, indent=2), flush=True)
        (OUT / f"{NAME}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.preview:
        previews()
    if args.render:
        report["videos"] = [render(NAME, standalone, (960, 840)), render(DESKTOP, desktop, (1280, 720))]
    if report:
        (OUT / f"{NAME}-validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if not any((args.check, args.preview, args.render)):
        parser.print_help()


if __name__ == "__main__":
    main()
