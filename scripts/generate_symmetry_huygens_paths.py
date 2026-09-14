"""Paths and coherent amplitudes for the shared Huygens construction.

A route identifies a weighted wavefront-element group. Its exact amplitude
is an integrated kernel contribution, never inferred from the center-line
length. All displayed phasors use one labelled plane-wave phase reference.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from huygens_construction_model import (HuygensModel, WIDTH, HEIGHT, FPS, BOX,
    DURATION, X_MAX, VIEW_HALF_HEIGHT, CONSTRUCTION_X, ENDPOINT_X, ENDPOINT_Y,
    K, ELEMENT_CENTERS, ELEMENT_SIGMA, REMAINDER_INDEX, N_GROUPS,
    coefficients_at, temporal_phase, label_at, construction_visibility,
    tracking_visibility, tracked_front_x, group_index, ease)

OUT = ROOT / "content" / "drafts" / "animations"
NAME = "symmetry-huygens-paths"
SCALE = 2
BG, INK, MUTED = (3, 3, 8), (245, 237, 232), (168, 160, 177)
BLUE, GOLD, GREEN, REST = (84, 147, 204), (233, 182, 79), (87, 204, 159), (186, 164, 220)
POSITIVE, NEGATIVE = np.array((255, 42, 91)), np.array((37, 137, 255))
ORDER = tuple(group_index(j) for j in (0, -3, 3, -1, 1, -2, 2, -4, 4, -5, 5)) + (REMAINDER_INDEX,)
SAMPLES = (2, 5, 9, 12, 14, 17, 19, 22, 25.5, 29, 34, 39)
PHASOR_ORIGIN, PHASOR_SCALE = (55, 429), 164


@lru_cache(None)
def font(size, bold=False):
    for name in ("seguisb.ttf" if bold else "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, round(SCALE*size))
        except OSError:
            pass
    return ImageFont.load_default()


def text(draw, xy, value, size=17, color=INK, bold=False, anchor=None):
    draw.text(tuple(SCALE*v for v in xy), value, font=font(size, bold),
              fill=color, anchor=anchor)


def point(x, y):
    return (BOX[0] + (BOX[2]-BOX[0])*x/X_MAX,
            (BOX[1]+BOX[3])/2 - (BOX[3]-BOX[1])*y/(2*VIEW_HALF_HEIGHT))


def line(draw, points, color, width=1.0):
    draw.line([tuple(SCALE*v for v in p) for p in points], fill=color,
              width=max(1, round(SCALE*width)), joint="curve")


def arrow(draw, start, end, color, width=2, head=5):
    line(draw, [start,end], color, width)
    start, end = np.asarray(start), np.asarray(end)
    delta = end-start
    length = np.linalg.norm(delta)
    if length < .6:
        return
    unit = delta/length
    normal = np.array((-unit[1],unit[0]))
    h = min(head,length*.55)
    draw.polygon([tuple(SCALE*v for v in p) for p in
                  (end,end-h*unit+.42*h*normal,end-h*unit-.42*h*normal)], fill=color)


def phasor_point(value):
    return (PHASOR_ORIGIN[0]+PHASOR_SCALE*value.real,
            PHASOR_ORIGIN[1]-PHASOR_SCALE*value.imag)


class Renderer:
    def __init__(self):
        self.model = HuygensModel()
        self.groups = self.model.endpoint_contributions()
        self.reference = complex(np.exp(1j*K*ENDPOINT_X))
        # This is one phase-only change of basis, applied to every term.
        self.relative_groups = self.groups/self.reference
        self.x = np.linspace(0,X_MAX,(BOX[2]-BOX[0])*SCALE)
        self.visible = np.flatnonzero(np.abs(self.model.y) <= VIEW_HALF_HEIGHT)
        self.source_shapes = []
        for j,center in enumerate(ELEMENT_CENTERS):
            selected = np.flatnonzero(np.abs(self.model.y-center) < .54)
            self.source_shapes.append([(point(CONSTRUCTION_X,float(self.model.y[k]))[0]
                + 9*float(self.model.weights[j,k]), point(CONSTRUCTION_X,float(self.model.y[k]))[1])
                for k in selected if abs(self.model.y[k]) <= VIEW_HALF_HEIGHT])

    def quantities(self, seconds):
        coefficients = coefficients_at(seconds)
        absolute = coefficients*self.groups*temporal_phase(seconds)
        reference = self.reference*temporal_phase(seconds)
        return coefficients, absolute, reference

    def plane(self, seconds, opacity):
        values = np.real(np.exp(1j*K*self.x)*temporal_phase(seconds))
        strength = np.abs(values)**.72
        target = np.where((values>=0)[:,None],POSITIVE,NEGATIVE)
        colors = np.array(BG)+(target-np.array(BG))*strength[:,None]*opacity
        row = np.clip(colors,0,255).astype(np.uint8)[None,:,:]
        return Image.fromarray(row).resize(((BOX[2]-BOX[0])*SCALE,
                                            (BOX[3]-BOX[1])*SCALE))

    def routes(self, draw, seconds, coefficients, visibility):
        if visibility <= 0:
            return
        plane_x = point(CONSTRUCTION_X,0)[0]
        b = point(ENDPOINT_X,ENDPOINT_Y)
        alpha = round(105*visibility)
        for y in range(BOX[1],BOX[3],16):
            line(draw,[(plane_x,y),(plane_x,y+5)],(*MUTED,alpha),.8)
        for j,center in enumerate(ELEMENT_CENTERS):
            weight = float(coefficients[j])
            if weight <= 0:
                continue
            # The central group remains the anchor; a partly revealed group is
            # highlighted while its corresponding complex arrow is added.
            active = j == group_index(0) or .001 < weight < .999
            color = GOLD if active else BLUE
            source = point(CONSTRUCTION_X,float(center))
            opacity = visibility*weight
            # A narrow fan identifies the finite wavefront element. It is not
            # a set of equal-weight point rays used to calculate the phasor.
            for offset in (-.16,-.08,.08,.16):
                line(draw,[point(CONSTRUCTION_X,float(center+offset)),b],
                     (*color,round(23*opacity)),.7)
            line(draw,[source,b],(*color,round(175*opacity)),1.4 if active else 1.05)
            line(draw,self.source_shapes[j],(*color,round(235*opacity)),1.8)
            radius = 3.3
            draw.ellipse(tuple(SCALE*v for v in (source[0]-radius,source[1]-radius,
                                               source[0]+radius,source[1]+radius)),
                         fill=(*color,round(255*opacity)))
        remaining = float(coefficients[REMAINDER_INDEX])
        if remaining > 0:
            # The remainder is a weighted field extending beyond these marks;
            # its exact amplitude is the purple final arrow in the sum.
            for y in (BOX[1]+5,BOX[3]-5):
                for shift in (0,5,10):
                    yy = y+shift if y < (BOX[1]+BOX[3])/2 else y-shift
                    line(draw,[(plane_x-6,yy),(plane_x+6,yy)],
                         (*REST,round(150*visibility*remaining)),.8)
        radius = 4
        draw.ellipse(tuple(SCALE*v for v in (b[0]-radius,b[1]-radius,b[0]+radius,b[1]+radius)),
                     fill=(*GREEN,round(255*visibility)))
        text(draw,(1251,380),"B",size=20,color=(*GREEN,round(255*visibility)),anchor="lm")
        text(draw,(plane_x+22,88),"wavefront elements",size=16,
             color=(*MUTED,round(245*visibility)))

    def sum_diagram(self, draw, coefficients, visibility):
        if visibility <= 0:
            return
        alpha = round(255*visibility)
        terms = self.relative_groups*coefficients
        text(draw,(55,270),"Coherent sum at B",size=20,bold=True,color=(*INK,alpha))
        text(draw,(55,301),"One arrow per element",size=15,color=(*MUTED,alpha))
        # A permanently horizontal complete-plane reference fixes orientation
        # and unit amplitude. It is not the phase of a raw center-line ray.
        arrow(draw,PHASOR_ORIGIN,phasor_point(1+0j),(*GREEN,round(58*visibility)),width=1,head=6)
        text(draw,(phasor_point(1+0j)[0],491),"plane wave",size=14,
             color=(*GREEN,round(125*visibility)),anchor="mt")
        cumulative = 0j
        for j in ORDER:
            value = terms[j]
            next_value = cumulative+value
            if abs(value) > 1e-8:
                active = j == group_index(0) or .001 < coefficients[j] < .999
                color = REST if j == REMAINDER_INDEX else GOLD if active else BLUE
                arrow(draw,phasor_point(cumulative),phasor_point(next_value),
                      (*color,alpha),width=2.4,head=5.5)
            cumulative = next_value
        # The resultant is drawn alongside the chain on the same coordinates,
        # with a small bright tip. Nothing is renormalized as terms are added.
        arrow(draw,PHASOR_ORIGIN,phasor_point(cumulative),(*GREEN,alpha),width=2,head=6)
        tip = phasor_point(cumulative)
        draw.ellipse(tuple(SCALE*v for v in (tip[0]-2.8,tip[1]-2.8,tip[0]+2.8,tip[1]+2.8)),
                     fill=(*GREEN,alpha))
        text(draw,(55,515),"Phase relative to the",size=16,color=(*MUTED,alpha))
        text(draw,(55,538),"plane wave at B",size=16,color=(*MUTED,alpha))
        if coefficients[REMAINDER_INDEX] > 0:
            text(draw,(55,593),"+ remaining wavefront",size=16,
                 color=(*REST,round(alpha*coefficients[REMAINDER_INDEX])))

    def frame(self, seconds):
        coefficients, absolute, reference = self.quantities(seconds)
        focus = ease((seconds-4)/2)*(1-ease((seconds-30)/2))
        image = Image.new("RGB",(WIDTH*SCALE,HEIGHT*SCALE),BG)
        image.paste(self.plane(seconds,1-focus),tuple(SCALE*v for v in BOX[:2]))
        overlay = Image.new("RGBA",image.size,(0,0,0,0))
        draw = ImageDraw.Draw(overlay,"RGBA")
        self.routes(draw,seconds,coefficients,focus)
        self.sum_diagram(draw,coefficients,focus)
        # During decomposition the exact selected sum, not the full reference,
        # supplies the small color sample at B using the common wave clock.
        if focus > 0:
            value = float(np.real(absolute.sum()))
            target = POSITIVE if value>=0 else NEGATIVE
            rgb = np.array(BG)+(target-np.array(BG))*min(1,abs(value))**.72
            x,y = point(ENDPOINT_X,ENDPOINT_Y)
            line(draw,[(x,y-26),(x,y+26)],(*tuple(int(v) for v in rgb),round(255*focus)),3)
        tracking = tracking_visibility(seconds)
        if tracking:
            x = point(tracked_front_x(seconds),0)[0]
            for y in (BOX[1]-7,BOX[3]+7):
                line(draw,[(x-6,y),(x+6,y)],(*INK,round(220*tracking)),1.3)
        text(draw,(40,27),label_at(seconds),size=28,bold=True)
        text(draw,(1240,33),"Huygens · paths and amplitudes",size=19,color=MUTED,anchor="ra")
        footer = "Each route identifies a weighted wavefront contribution."
        if seconds < 4 or seconds >= 32:
            footer = "The same plane wave, reconstructed from its wavefront contributions."
        text(draw,(40,691),footer,size=15,color=MUTED)
        text(draw,(1240,691),"A decomposition · no physical barrier",size=15,color=MUTED,anchor="ra")
        image = Image.alpha_composite(image.convert("RGBA"),overlay).convert("RGB")
        return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def checks(renderer):
    selected_error = 0.0
    reference_error = 0.0
    b_index = int(np.argmin(np.abs(renderer.model.y-ENDPOINT_Y)))
    for seconds in np.linspace(0,DURATION,81):
        coefficients,absolute,reference = renderer.quantities(float(seconds))
        direct = renderer.model.field_at(ENDPOINT_X,coefficients)[b_index]*temporal_phase(seconds)
        selected_error = max(selected_error,float(abs(absolute.sum()-direct)))
        relative = renderer.relative_groups*coefficients
        reference_error = max(reference_error,float(abs(relative.sum()*reference-direct)))
    # Direct real-space kernel integration, independent of spectral endpoint
    # evaluation, validates every weighted group and its complex normalization.
    impulse = np.zeros(renderer.model.n,complex)
    impulse[0] = 1
    kernel = renderer.model.propagate(impulse,ENDPOINT_X-CONSTRUCTION_X)
    row = kernel[(b_index-np.arange(renderer.model.n))%renderer.model.n]
    integrated = (renderer.model.weights*renderer.model.incident_phase) @ row
    group_error = float(np.max(np.abs(integrated-renderer.groups)))
    full_error = float(abs(renderer.groups.sum()-renderer.reference))
    assert max(selected_error,reference_error,group_error,full_error)<1e-12
    result = {"selected_sum_matches_wave_max_error":selected_error,
              "labelled_phase_reference_max_error":reference_error,
              "real_space_group_integral_max_error":group_error,
              "full_plane_absolute_complex_error":full_error,
              "remaining_wavefront_magnitude":float(abs(renderer.groups[REMAINDER_INDEX])),
              "frames":round(DURATION*FPS),"fps":FPS,"duration":DURATION}
    print(json.dumps(result,indent=2),flush=True)
    return result


def previews(renderer):
    OUT.mkdir(parents=True,exist_ok=True)
    sheet = Image.new("RGB",(1536,4*316),(17,17,21))
    draw = ImageDraw.Draw(sheet)
    for index,seconds in enumerate(SAMPLES):
        frame = renderer.frame(seconds)
        frame.save(OUT/f"{NAME}-check-{seconds:g}.png")
        x,y = index%3*512,index//3*316
        sheet.paste(frame.resize((512,288)),(x,y))
        draw.text((x+12,y+292),f"{seconds:g} s",fill=INK)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")
    renderer.frame(29).save(OUT/f"{NAME}-final.png")
    print(str(OUT/f"{NAME}-contact-sheet.png"),flush=True)


def render(renderer):
    OUT.mkdir(parents=True,exist_ok=True)
    path = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-loglevel","error","-nostats",
        "-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}",
        "-r",str(FPS),"-i","-","-an","-c:v","libx264","-preset","medium","-crf","18",
        "-pix_fmt","yuv420p","-movflags","+faststart",str(path)]
    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    start = time.perf_counter()
    for index in range(round(DURATION*FPS)):
        process.stdin.write(renderer.frame(index/FPS).tobytes())
        if index%(FPS*4)==0:
            print(f"{index/FPS:.0f}/{DURATION:g} seconds; elapsed {time.perf_counter()-start:.1f}s",flush=True)
    process.stdin.close()
    error = process.stderr.read().decode("utf-8",errors="replace")
    if process.wait():
        raise RuntimeError(error)
    print(json.dumps({"video":str(path),"bytes":path.stat().st_size}),flush=True)


def qa():
    path = OUT/f"{NAME}.mp4"
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-loglevel","error","-i",str(path),
        "-vf",f"select=not(mod(n\\,{FPS//2})),scale=320:180","-fps_mode","vfr",
        "-f","rawvideo","-pix_fmt","rgb24","-"]
    result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    assert not result.stderr,result.stderr.decode("utf-8",errors="replace")
    frames = np.frombuffer(result.stdout,np.uint8).reshape((-1,180,320,3))
    assert len(frames)==round(DURATION*2)
    directory = ROOT/".tools"/"huygens-paths-qa"
    directory.mkdir(parents=True,exist_ok=True)
    for page,start in enumerate(range(0,len(frames),16),1):
        sheet = Image.new("RGB",(1280,816),(17,17,21))
        draw = ImageDraw.Draw(sheet)
        for slot,frame in enumerate(frames[start:start+16]):
            x,y = slot%4*320,slot//4*204
            sheet.paste(Image.fromarray(frame),(x,y))
            draw.text((x+9,y+184),f"{(start+slot)/2:g} s",fill=INK)
        sheet.save(directory/f"motion-{page:02d}.png")
    print(json.dumps({"decoded_samples":len(frames),"qa_directory":str(directory)}),flush=True)


def main():
    parser = argparse.ArgumentParser()
    for option in ("check","preview","render","qa"):
        parser.add_argument(f"--{option}",action="store_true")
    args = parser.parse_args()
    renderer = Renderer()
    if args.check:
        checks(renderer)
    if args.preview or not any((args.check,args.render,args.qa)):
        previews(renderer)
    if args.render:
        render(renderer)
    if args.qa:
        qa()


if __name__=="__main__":
    main()
