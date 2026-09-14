"""A short looping schematic of wavefronts continually seeding wavelets."""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))
from PIL import Image, ImageDraw, ImageFont, ImageChops
import imageio_ffmpeg

from huygens_relay_model import (WIDTH, HEIGHT, FPS, DURATION, STEP_TIME,
    FRONT_PIXEL_Y, PIXELS_PER_UNIT, LEFT, RIGHT, TOP, BOTTOM,
    generations_at, source_centers, source_row_pixel_y)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-huygens-relay"
SCALE = 2
BG = (255, 252, 246)
INK = (37, 39, 42)
MUTED = (118, 113, 106)
BLUE = (51, 91, 133)
GOLD = (198, 138, 45)


def s(value):
    return round(value * SCALE)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, s(size))
        except OSError:
            pass
    return ImageFont.load_default()


def frame(seconds):
    image = Image.new("RGB", (s(WIDTH), s(HEIGHT)), BG)
    layer = Image.new("RGBA", (s(RIGHT-LEFT), s(BOTTOM-TOP)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    generations = generations_at(seconds)
    for generation in generations:
        radius = generation.radius * PIXELS_PER_UNIT
        center_y = source_row_pixel_y(generation)
        opacity = generation.opacity
        if opacity <= 0:
            continue
        # Earlier wavefronts are construction guides, not material screens.
        guide_alpha = round(40 * opacity)
        for x in range(round(LEFT), round(RIGHT), 16):
            draw.line((s(x-LEFT), s(center_y-TOP), s(x+6-LEFT), s(center_y-TOP)),
                      fill=(*BLUE, guide_alpha), width=s(0.7))
        if radius > 0.2:
            for center_x in source_centers(generation):
                bounds = (s(center_x-radius-LEFT), s(center_y-radius-TOP),
                          s(center_x+radius-LEFT), s(center_y+radius-TOP))
                draw.arc(bounds, 180, 360, fill=(*BLUE, round(205 * opacity)), width=s(1.55))
    image.paste(layer, (s(LEFT), s(TOP)), layer)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.line((s(LEFT), s(FRONT_PIXEL_Y), s(RIGHT), s(FRONT_PIXEL_Y)), fill=GOLD, width=s(2.1))
    for generation in generations:
        if generation.opacity <= 0:
            continue
        center_y = source_row_pixel_y(generation)
        if center_y > BOTTOM:
            continue
        for center_x in source_centers(generation):
            if LEFT <= center_x <= RIGHT:
                radius = 2.65
                draw.ellipse((s(center_x-radius), s(center_y-radius),
                              s(center_x+radius), s(center_y+radius)),
                             fill=(*BLUE, round(235 * generation.opacity)))

    draw.text((s(40), s(27)), "Huygens construction", font=font(28, True), fill=INK)
    draw.text((s(1240), s(35)), "following the advancing front", font=font(19), fill=MUTED, anchor="ra")
    # Upward propagation and camera motion are explicit while the tracked front
    # stays fixed in this view.
    ax = 640
    draw.line((s(ax), s(127), s(ax), s(89)), fill=(*GOLD, 225), width=s(1.7))
    draw.polygon(((s(ax-5), s(95)), (s(ax+5), s(95)), (s(ax), s(86))), fill=GOLD)
    draw.text((s(654), s(98)), "advance", font=font(16), fill=MUTED)
    draw.text((s(44), s(143)), "wavefront", font=font(16), fill=GOLD)
    draw.text((s(40), s(687)), "Every new front seeds the next generation", font=font(18), fill=INK)
    draw.text((s(1240), s(690)), "geometric schematic", font=font(15), fill=MUTED, anchor="ra")
    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def previews():
    OUT.mkdir(parents=True, exist_ok=True)
    times = (0.0, 0.375, 0.75, 1.125, 1.5, 2.25)
    contact = Image.new("RGB", (1536, 632), BG)
    draw = ImageDraw.Draw(contact)
    for index, seconds in enumerate(times):
        rendered = frame(seconds)
        rendered.save(OUT / f"{NAME}-check-{seconds:g}.png")
        x, y = (index % 3)*512, (index // 3)*316
        contact.paste(rendered.resize((512,288)), (x,y))
        draw.text((x+12,y+291), f"{seconds:g} s", fill=INK, font=ImageFont.truetype("segoeui.ttf",17))
    contact.save(OUT / f"{NAME}-contact-sheet.png")
    frame(0.75).save(OUT / f"{NAME}-still.png")
    identical = ImageChops.difference(frame(0), frame(DURATION)).getbbox() is None
    print(json.dumps({"contact_sheet": str(OUT / f"{NAME}-contact-sheet.png"),
                      "loop_endpoint_pixels_identical": identical}), flush=True)
    assert identical


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-nostats",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE)
    for index in range(round(DURATION * FPS)):
        process.stdin.write(frame(index/FPS).tobytes())
        if index % (FPS*3) == 0:
            print(f"{index/FPS:g}/{DURATION:g} s", flush=True)
    process.stdin.close()
    error = process.stderr.read().decode(errors="replace")
    if process.wait():
        raise RuntimeError(error)
    print(json.dumps({"video":str(output),"bytes":output.stat().st_size}), flush=True)


def render_gif():
    """The three-second fundamental cycle, with one fixed palette and clock."""
    OUT.mkdir(parents=True, exist_ok=True)
    colors = [BG]
    for target, count in ((BLUE, 80), (GOLD, 48), (INK, 80), (MUTED, 32)):
        for index in range(1, count + 1):
            amount = index / count
            colors.append(tuple(round(BG[i] + amount * (target[i]-BG[i])) for i in range(3)))
    colors += [BG] * (256-len(colors))
    palette = Image.new("P", (1,1))
    palette.putpalette([channel for color in colors for channel in color])
    frames = []
    gif_fps = 20
    for index in range(3 * gif_fps):
        reduced = frame(index / gif_fps).resize((960,540), Image.Resampling.LANCZOS)
        frames.append(reduced.quantize(palette=palette, dither=Image.Dither.NONE))
    output = OUT / f"{NAME}-loop.gif"
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=50,
                   loop=0, disposal=2, optimize=False)
    print(json.dumps({"loop_gif":str(output),"bytes":output.stat().st_size}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--gif", action="store_true")
    args = parser.parse_args()
    if args.preview or not (args.render or args.gif):
        previews()
    if args.render:
        render()
    if args.gif:
        render_gif()


if __name__ == "__main__":
    main()
