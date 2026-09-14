"""Isolate the original 49-path phasor pane, using k L rather than k (L-AB).

Preserves the original path lengths, weights, slit order, and 18.5-second
timeline. Existing generators and media are neither modified nor patched.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))

import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg

import generate_symmetry_many_slit_paths_phasors_interference as original

wave = original.wave
WIDTH, HEIGHT, SCALE = 960, 840, 2
FPS, DURATION = original.FPS, original.DURATION
NAME = "symmetry-tip-to-tail-source-phase"
OUT = ROOT / "content" / "drafts" / "animations"
PLOT = (72.0, 147.0, 888.0, 740.0)
ORIGIN = ((PLOT[0] + PLOT[2]) / 2, (PLOT[1] + PLOT[3]) / 2)
SAMPLES = (1.8, 3.7, 6.5, 7.5, 8.7, 10.0, 11.85, 13.7, 17.0)


def contributions(b_value):
    """Only the phase convention changes: theta_j = k L_j, referenced to A."""
    result = []
    for item in original.build_contributions(b_value):
        phase = original.WAVE_NUMBER * item.length
        result.append(replace(item, phase=phase,
                              value=item.weight * complex(math.cos(phase), math.sin(phase))))
    return tuple(result)


def chain_at(b_value):
    return np.asarray(original.cumulative_values(contributions(b_value)))


def fixed_scale():
    # One scale and origin for the entire film. No reorientation or following
    # of the total arrow is permitted as B changes.
    radius = max(float(np.max(np.abs(chain_at(float(b)))))
                 for b in np.linspace(-original.DETECTOR_HALF_HEIGHT,
                                      original.DETECTOR_HALF_HEIGHT, 1025))
    return (min(PLOT[2]-PLOT[0], PLOT[3]-PLOT[1])/2 - 24) / radius


PIXELS_PER_UNIT = fixed_scale()


def point(value):
    return (ORIGIN[0] + PIXELS_PER_UNIT * value.real,
            ORIGIN[1] - PIXELS_PER_UNIT * value.imag)


def frame(seconds):
    b, count, active, fraction, complete, _, _, _ = original.animation_state(seconds)
    terms = contributions(b)
    chain = np.asarray(original.cumulative_values(terms))
    image = Image.new("RGBA", (WIDTH*SCALE, HEIGHT*SCALE), (*original.BG, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    wave.panel(draw, (24, 20, WIDTH-24, HEIGHT-20))
    wave.draw_text(draw, (48, 39), "Tip-to-tail · phase relative to A", font_obj=original.TITLE)
    wave.draw_text(draw, (48, 82), "θⱼ = kLⱼ      phase at A = 0", font_obj=original.SUBTITLE)
    wave.draw_text(draw, (WIDTH-48, 83), f"B = {b:+.2f}",
                   fill=original.MUTED, font_obj=original.SUBTITLE, anchor="ra")
    if not complete:
        status = "49 paths · top opening to bottom opening"
        progress = "Ready" if active is None else f"Path {active+1} / 49"
    else:
        status = "49 paths · total amplitude"
        progress = ("Fixed B" if seconds < original.CENTER_HOLD_END
                    or seconds >= original.SETTLE_END else "Sweeping B")
    wave.draw_text(draw, (48, 114), status, fill=original.MUTED, font_obj=original.LABEL)
    wave.draw_text(draw, (WIDTH-48, 114), progress,
                   fill=original.GREEN if complete else original.GOLD,
                   font_obj=original.LABEL_BOLD, anchor="ra")

    draw.line(tuple(wave.s(v) for v in (PLOT[0], ORIGIN[1], PLOT[2], ORIGIN[1])),
              fill=wave.rgba(original.MUTED, .23), width=SCALE)
    draw.line(tuple(wave.s(v) for v in (ORIGIN[0], PLOT[1], ORIGIN[0], PLOT[3])),
              fill=wave.rgba(original.MUTED, .23), width=SCALE)
    wave.draw_text(draw, (PLOT[2], ORIGIN[1]-26), "Re", fill=original.MUTED,
                   font_obj=original.LABEL, anchor="ra")
    wave.draw_text(draw, (ORIGIN[0]+9, PLOT[1]), "Im", fill=original.MUTED,
                   font_obj=original.LABEL)
    wave.circle(draw, ORIGIN, 2.5, original.MUTED)

    for index in range(count):
        original.draw_small_arrow(draw, point(chain[index]), point(chain[index+1]),
                                  wave.rgba(original.BLUE, .83), width=2, head=4.2)
    current = chain[count]
    if active is not None:
        current = chain[active] + fraction * terms[active].value
        if fraction > 0:
            original.draw_small_arrow(draw, point(chain[active]), point(current),
                                      original.GOLD, width=4, head=6.2)
    if count > 0 or active is not None:
        if complete:
            wave.draw_arrow(draw, ORIGIN, point(current), wave.rgba(original.GREEN, .96), 6)
        else:
            wave.dashed_line(draw, ORIGIN, point(current), wave.rgba(original.GREEN, .38),
                             width=2, dash=6, gap=5)
        wave.circle(draw, point(current), 3.3, original.GREEN if complete else original.GOLD)

    wave.draw_text(draw, (48, 770), "Blue: path contributions", fill=original.BLUE,
                   font_obj=original.LABEL)
    wave.draw_text(draw, (480, 770), "Gold: adding one path", fill=original.GOLD,
                   font_obj=original.LABEL, anchor="ma")
    wave.draw_text(draw, (WIDTH-48, 770), "Green: sum", fill=original.GREEN,
                   font_obj=original.LABEL_BOLD, anchor="ra")
    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def check_model():
    phase_error = 0.0
    intensity_error = 0.0
    smallest_margin = float("inf")
    for b in np.linspace(-original.DETECTOR_HALF_HEIGHT, original.DETECTOR_HALF_HEIGHT, 257):
        old = np.asarray([item.value for item in original.build_contributions(float(b))])
        new = np.asarray([item.value for item in contributions(float(b))])
        factor = np.exp(1j * original.WAVE_NUMBER * original.reference_length(float(b)))
        phase_error = max(phase_error, float(np.max(np.abs(new - old * factor))))
        intensity_error = max(intensity_error,
                              float(abs(abs(new.sum())**2 - abs(old.sum())**2)))
    for index in range(round(DURATION*FPS)):
        b = original.animation_state(index/FPS)[0]
        for value in chain_at(b):
            x, y = point(value)
            smallest_margin = min(smallest_margin, x-PLOT[0], PLOT[2]-x, y-PLOT[1], PLOT[3]-y)
    assert phase_error < 1e-12
    assert intensity_error < 1e-9
    assert smallest_margin > 18
    result = {"max_common_rotation_error": phase_error,
              "max_intensity_difference": intensity_error,
              "smallest_plot_margin_pixels": smallest_margin,
              "center_AB_wavelengths": original.reference_length(0)/original.WAVELENGTH,
              "phase_rule": "k * path_length; no AB subtraction",
              "original_timing_seconds": DURATION}
    print(json.dumps(result, indent=2), flush=True)
    return result


def previews():
    sheet = Image.new("RGB", (1440, 1296), original.BG)
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(SAMPLES):
        picture = frame(seconds)
        picture.save(OUT/f"{NAME}-check-{seconds:g}.png")
        x, y = index%3*480, index//3*432
        sheet.paste(picture.resize((480, 420), Image.Resampling.LANCZOS), (x, y))
        draw.text((x+20, y+417), f"{seconds:g} s", fill=original.INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")


def render():
    video = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
               "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium",
               "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    for index in range(round(DURATION*FPS)):
        process.stdin.write(frame(index/FPS).tobytes())
        if index % (4*FPS) == 0:
            print(f"Rendered {index/FPS:g}/{DURATION:g} seconds", flush=True)
    process.stdin.close()
    error = process.stderr.read().decode("utf-8", errors="replace")
    if process.wait():
        raise RuntimeError(error)
    count, seconds = imageio_ffmpeg.count_frames_and_secs(str(video))
    assert count == round(DURATION*FPS) and abs(seconds-DURATION) < .001
    decode = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(video),
                             "-f", "null", "-"], capture_output=True, check=True)
    assert not decode.stderr
    print(json.dumps({"video": str(video), "frames": count, "seconds": seconds,
                      "bytes": video.stat().st_size, "decode": "passed"}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    check_model()
    previews()
    if args.render:
        render()


if __name__ == "__main__":
    main()
