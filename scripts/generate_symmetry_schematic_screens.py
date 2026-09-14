"""Schematic wavefronts for the established plane-wave / screen progression.

Gold lines are positive-real phase contours of the complete normalized field.
Blue lines are contours of selected single-cell contributions, retaining their
actual local incident phase. Their line weights do not encode amplitude.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))

import numpy as np
import contourpy
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

from generate_symmetry_plane_wave_screens import Renderer as FieldRenderer
from plane_wave_screens_model import (
    SCREEN_X, X_MAX, VIEW_HALF_HEIGHT, DURATION, FPS, label_at, state_at,
    temporal_phase, ease,
)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-schematic-screens"
WIDTH, HEIGHT, SCALE = 1280, 720, 2
BOX = (40, 80, 1240, 680)
BG = (255, 252, 246)
INK = (37, 39, 42)
BLUE = (51, 91, 133)
GOLD = (190, 126, 34)
MUTED = (118, 113, 106)
COMBINED_ZERO = 0.003
COMPONENT_ZERO = 1e-5
ELEMENT_Y = (-0.9, 0.0, 0.9)
SAMPLES = (2.0, 8.5, 13.0, 18.0, 23.0, 29.0, 33.0, 37.0, 41.0, 44.0, 48.0)


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, round(size * SCALE))
        except OSError:
            pass
    return ImageFont.load_default()


def pixels(points):
    """Equal physical x/y scale, matching the original landscape wave pane."""
    points = np.asarray(points)
    x = BOX[0] + points[..., 0] / X_MAX * (BOX[2] - BOX[0])
    y = (BOX[1] + BOX[3]) / 2 - points[..., 1] / (2 * VIEW_HALF_HEIGHT) * (BOX[3] - BOX[1])
    return np.stack((x, y), axis=-1) * SCALE


def phase_contours(field, x, y, phase, zero):
    """No angle branch cut: retain the positive-real half of Im(U clock)=0."""
    moving = field * phase
    valid = (np.real(moving) > 0.0) & (np.abs(field) >= zero)
    if len(x) < 2 or not np.any(valid):
        return []
    z = np.ma.array(np.imag(moving), mask=~valid)
    generator = contourpy.contour_generator(x=x, y=y, z=z,
                                            corner_mask=False, line_type="Separate")
    return generator.lines(0.0)


def construction_visibility(seconds):
    """Hide a change of local decomposition at zero annotation opacity.

    At 34 and 38 seconds new physical planes subdivide the previous slabs.
    This short fade concerns only selected blue guides, never the total field.
    """
    return min(ease(abs(seconds-boundary)/0.4) for boundary in (34.0,38.0))


class Renderer:
    def __init__(self):
        # Reuse the reviewed complete-field solver and its exact polynomial
        # transition cache. No original physical parameter or mask is changed.
        self.physics = FieldRenderer()
        self.model = self.physics.model
        self.sampler = self.physics.sampler
        self.element_indices = np.array([np.argmin(abs(self.model.y-y)) for y in ELEMENT_Y])
        early_centers = ((0.0,),(-0.9,0.0,0.9),np.arange(-3,4)*0.45,np.arange(-7,8)*0.45)
        self.early_element_indices = {
            stage: np.array([np.argmin(abs(self.model.y-y)) for y in centers])
            for stage,centers in enumerate(early_centers,1)
        }
        self.relative_indices = np.arange(-256, 257)
        self.response_cache = {}
        self.boundary_cache = {}

    def unit_responses(self, screen):
        """Normalized discrete Green response; store only visible offsets.

        P(d)[i,j] = ifft(exp(i d kx))[(i-j) mod n]. Computing chunks avoids
        retaining a full n-by-image-width complex response matrix.
        """
        if screen not in self.response_cache:
            columns = np.flatnonzero(self.sampler.x >= SCREEN_X[screen])
            response = np.empty((len(self.relative_indices), len(columns)), complex)
            for begin in range(0, len(columns), 24):
                part = columns[begin:begin+24]
                distance = self.sampler.x[part] - SCREEN_X[screen]
                full = np.fft.ifft(np.exp(1j * distance[:, None] * self.model.kx[None, :]), axis=1)
                response[:, begin:begin+len(part)] = full[:, self.relative_indices % self.model.n].T
            self.response_cache[screen] = columns, response
        return self.response_cache[screen]

    def boundary_fields(self, seconds, masks):
        a, b, _ = state_at(seconds)
        if a == b:
            if a not in self.boundary_cache:
                self.boundary_cache[a] = self.model.screen_fields(masks)
            return self.boundary_cache[a]
        return self.model.screen_fields(masks)

    def construction_planes(self, seconds, masks):
        # Before recovery, components terminate at the next physical screen.
        # Once all masks are identity, retain the same 15 positions as chosen
        # Huygens construction planes, not material walls or extra masks.
        if seconds >= 46.0:
            return np.arange(len(SCREEN_X))
        return np.flatnonzero(np.max(1.0 - masks, axis=1) > 1e-8)

    def selected_indices(self, seconds):
        # Early coarse slits each receive their own visible cell contribution.
        # Center sets are nested; the next set plus actual transmission gives
        # the new elements their continuous appearance during a transition.
        a,b,_ = state_at(seconds)
        early = [stage for stage in (a,b) if stage in self.early_element_indices]
        return self.early_element_indices[max(early)] if early else self.element_indices

    def components(self, seconds, masks):
        """Yield (screen, source index, columns, true complex cell response)."""
        planes = self.construction_planes(seconds, masks)
        if not len(planes):
            return
        boundary = self.boundary_fields(seconds, masks)
        for order, screen in enumerate(planes):
            end = SCREEN_X[planes[order+1]] if order+1 < len(planes) else X_MAX + 1e-8
            columns, response = self.unit_responses(int(screen))
            keep = self.sampler.x[columns] < end
            columns = columns[keep]
            if len(columns) < 2:
                continue
            for source in self.selected_indices(seconds):
                amplitude = boundary[screen][source]
                if masks[screen, source] <= 1e-8 or abs(amplitude) <= 1e-8:
                    continue
                rows = self.sampler.indices - source - self.relative_indices[0]
                assert rows.min() >= 0 and rows.max() < len(self.relative_indices)
                yield int(screen), int(source), columns, response[rows][:, keep] * amplitude

    @staticmethod
    def draw_curves(draw, curves, color, width):
        for curve in curves:
            if len(curve) > 1:
                draw.line([tuple(point) for point in pixels(curve)], fill=color,
                          width=round(width*SCALE), joint="curve")

    def frame(self, seconds, phase_seconds=None, include_components=True):
        masks, field = self.physics.complex_field(seconds)
        phase = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        image = Image.new("RGB", (WIDTH*SCALE, HEIGHT*SCALE), BG)
        draw = ImageDraw.Draw(image, "RGBA")

        a, b, amount = state_at(seconds)
        active_a = (np.max(1.0-self.model.targets[a], axis=1) > 1e-8).astype(float)
        active_b = (np.max(1.0-self.model.targets[b], axis=1) > 1e-8).astype(float)
        visibility = active_a + amount*(active_b-active_a)
        # Fade construction annotations with screen introduction/removal.
        # At final recovery the same decomposition intentionally continues on
        # imaginary slices, so those annotations retain full visibility.
        guide_visibility = np.ones(len(SCREEN_X)) if seconds >= 42.0 else visibility
        guide_visibility = guide_visibility * construction_visibility(seconds)

        markers = []
        # Effective count varies continuously while the next slit set opens.
        # Keep line width fixed; alter only explanatory ink density smoothly.
        source_count = max(1.0,float(np.sum(masks[0,self.selected_indices(seconds)])))
        line_opacity = 110*min(1.0,np.sqrt(3.0/source_count))*(1.0-0.5*ease((source_count-7.0)/8.0))
        line_width = 1.0
        if include_components and np.max(guide_visibility) > 0:
            for screen, source, columns, component in self.components(seconds, masks):
                curves = phase_contours(component, self.sampler.x[columns], self.sampler.y,
                                        phase, COMPONENT_ZERO)
                alpha = guide_visibility[screen] * masks[screen,source]
                self.draw_curves(draw, curves, (*BLUE, round(line_opacity*alpha)), line_width)
                markers.append((screen, source, alpha))

        combined = phase_contours(field, self.sampler.x, self.sampler.y, phase, COMBINED_ZERO)
        self.draw_curves(draw, combined, (*GOLD, 238), 1.6)

        for screen, (position, mask) in enumerate(zip(SCREEN_X, masks)):
            x = pixels([[position, 0]])[0, 0]
            opacity = np.clip(1.0-mask[self.sampler.indices], 0, 1)[::-1]
            height = (BOX[3]-BOX[1])*SCALE
            sampled = np.interp(np.linspace(0, len(opacity)-1, height), np.arange(len(opacity)), opacity)
            for row, alpha in enumerate(sampled):
                if alpha > 1e-5:
                    draw.line((x-2*SCALE, BOX[1]*SCALE+row, x+2*SCALE, BOX[1]*SCALE+row),
                              fill=(*INK, round(245*alpha)), width=1)
            if visibility[screen] > 0:
                for y in (BOX[1]-7, BOX[3]+7):
                    draw.line((x-4*SCALE,y*SCALE,x+4*SCALE,y*SCALE),
                              fill=(*INK,round(180*visibility[screen])),width=2*SCALE)

        imaginary = ease((seconds-46.0)/1.5)
        if imaginary > 0:
            for position in SCREEN_X:
                x = pixels([[position,0]])[0,0]
                for y in range(BOX[1], BOX[3], 20):
                    draw.line((x,y*SCALE,x,(y+6)*SCALE), fill=(*BLUE,round(38*imaginary)),width=SCALE)

        for screen, source, alpha in markers:
            x, y = pixels([[SCREEN_X[screen], self.model.y[source]]])[0]
            r = 2*SCALE
            draw.ellipse((x-r,y-r,x+r,y+r), fill=(*BLUE,round(210*alpha)))

        draw.text((40*SCALE,25*SCALE), label_at(seconds),font=font(27,True),fill=INK)
        draw.text((1240*SCALE,31*SCALE), "Plane-wave illumination",font=font(18),fill=MUTED,anchor="ra")
        footer = 702*SCALE
        draw.line((40*SCALE,footer,66*SCALE,footer),fill=GOLD,width=round(1.6*SCALE))
        draw.text((76*SCALE,footer),"combined wavefronts",font=font(14),fill=MUTED,anchor="lm")
        draw.line((265*SCALE,footer,291*SCALE,footer),fill=BLUE,width=SCALE)
        draw.text((301*SCALE,footer),"selected wavelets",font=font(14),fill=MUTED,anchor="lm")
        if seconds >= 46:
            draw.text((1240*SCALE,footer),"imaginary slices",font=font(14),fill=MUTED,anchor="rm")
        return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def previews(renderer, seconds):
    OUT.mkdir(parents=True,exist_ok=True)
    thumbnails = []
    for value in seconds:
        start = time.perf_counter()
        frame = renderer.frame(value)
        path = OUT/f"{NAME}-check-{value:g}.png"
        frame.save(path)
        thumbnails.append(frame.resize((512,288),Image.Resampling.LANCZOS))
        print(json.dumps({"preview":str(path),"elapsed":round(time.perf_counter()-start,2)}),flush=True)
    contact = Image.new("RGB",(1536,316*((len(thumbnails)+2)//3)),BG)
    draw = ImageDraw.Draw(contact)
    for index,(value,thumb) in enumerate(zip(seconds,thumbnails)):
        x,y = index%3*512,index//3*316
        contact.paste(thumb,(x,y))
        draw.text((x+12,y+292),f"{value:g} s",fill=INK)
    contact.save(OUT/f"{NAME}-contact-sheet.png")


def render(renderer):
    OUT.mkdir(parents=True,exist_ok=True)
    path = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-nostats",
               "-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24",
               "-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),"-i","-","-an",
               "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
               "-movflags","+faststart",str(path)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(DURATION*FPS)):
        process.stdin.write(renderer.frame(index/FPS).tobytes())
        if index % (4*FPS) == 0:
            print(f"{index/FPS:.0f}/{DURATION:g} seconds; elapsed {time.perf_counter()-start:.1f}s",flush=True)
    process.stdin.close()
    error = process.stderr.read().decode("utf-8",errors="replace")
    if process.wait():
        raise RuntimeError(error)
    print(json.dumps({"video":str(path),"bytes":path.stat().st_size}),flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview",action="store_true")
    parser.add_argument("--render",action="store_true")
    parser.add_argument("--times",default=",".join(map(str,SAMPLES)))
    args = parser.parse_args()
    renderer = Renderer()
    if args.preview or not args.render:
        previews(renderer,[float(value) for value in args.times.split(",")])
    if args.render:
        render(renderer)


if __name__ == "__main__":
    main()
