"""Screen-legibility revision; the normalized wave calculations are unchanged.

The first 24 seconds use the preserved renderer directly. Later comb remnants
are enlarged symmetrically about their real centers, with every slit retained.
These display dimensions never enter the propagation masks.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time

import generate_symmetry_schematic_screens as original
from generate_symmetry_schematic_screens import (
    np, Image, ImageDraw, imageio_ffmpeg, ROOT, OUT, WIDTH, HEIGHT, SCALE, BOX,
    BG, INK, BLUE, GOLD, MUTED, SCREEN_X, VIEW_HALF_HEIGHT, DURATION, FPS,
    font, pixels, phase_contours, temporal_phase, state_at, label_at, ease,
    construction_visibility, COMPONENT_ZERO, COMBINED_ZERO,
)

NAME = "symmetry-schematic-screens-v2"
SAMPLES = (23.0,33.0,37.0,41.0,44.0,48.0)
LATE_BLUE_OPACITY = 45.0
LATE_STROKE_WIDTH = 3.0
MIN_STRIP_PIXELS = 12.0
MAX_STRIP_FRACTION = 0.55
COMBS = {6:(0.45,0.86,(0,7,14)),
         7:(0.225,0.97,(0,3,5,7,9,11,14)),
         8:(0.1125,0.995,tuple(range(15)))}


def enlarged_strip_height(pitch,fill):
    """Display-only transverse thickness, capped to preserve every opening."""
    pixels_per_unit = (BOX[3]-BOX[1])/(2*VIEW_HALF_HEIGHT)
    pitch_pixels = pitch*pixels_per_unit
    true_height = (1-fill)*pitch_pixels
    return min(MAX_STRIP_FRACTION*pitch_pixels,max(MIN_STRIP_PIXELS,true_height))


def periodic_opacity(y,dy,pitch,opaque_fraction):
    """Exact display-pixel overlap, with gaps centered at integer*pitch.

    Consequently every enlarged opaque strip retains the real comb center at
    (integer+1/2)*pitch; no new slit or shifted remnant is invented.
    """
    opening_width = pitch*(1-opaque_fraction)
    def integral(values):
        shifted = values+opening_width/2
        turns = np.floor(shifted/pitch)
        remainder = shifted-turns*pitch
        return turns*opening_width+np.minimum(remainder,opening_width)
    return np.clip(1-(integral(y+dy/2)-integral(y-dy/2))/dy,0,1)


class Renderer(original.Renderer):
    def __init__(self):
        super().__init__()
        self.display_cache = {}

    def display_target(self,stage):
        if stage not in self.display_cache:
            height = (BOX[3]-BOX[1])*SCALE
            target = np.zeros((len(SCREEN_X),height))
            if stage in COMBS:
                pitch,fill,screens = COMBS[stage]
                dy = 2*VIEW_HALF_HEIGHT/height
                y = VIEW_HALF_HEIGHT-(np.arange(height)+0.5)*dy
                pitch_pixels = pitch*(BOX[3]-BOX[1])/(2*VIEW_HALF_HEIGHT)
                fraction = enlarged_strip_height(pitch,fill)/pitch_pixels
                row = periodic_opacity(y,dy,pitch,fraction)
                target[list(screens)] = row
            else:
                # The coarse-screen treatment matches the original raster.
                for screen,mask in enumerate(self.model.targets[stage]):
                    opacity = np.clip(1-mask[self.sampler.indices],0,1)[::-1]
                    target[screen] = np.interp(np.linspace(0,len(opacity)-1,height),
                                               np.arange(len(opacity)),opacity)
            self.display_cache[stage] = target
        return self.display_cache[stage]

    def display_opacity(self,seconds):
        a,b,amount = state_at(seconds)
        if a == b:
            return self.display_target(a)
        return (1-amount)*self.display_target(a)+amount*self.display_target(b)

    def frame(self,seconds,phase_seconds=None,include_components=True):
        if seconds <= 24.0:
            return super().frame(seconds,phase_seconds,include_components)

        masks,field = self.physics.complex_field(seconds)
        phase = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        image = Image.new("RGB",(WIDTH*SCALE,HEIGHT*SCALE),BG)
        draw = ImageDraw.Draw(image,"RGBA")
        a,b,amount = state_at(seconds)
        active_a = (np.max(1-self.model.targets[a],axis=1)>1e-8).astype(float)
        active_b = (np.max(1-self.model.targets[b],axis=1)>1e-8).astype(float)
        visibility = active_a+amount*(active_b-active_a)
        guide_visibility = np.ones(len(SCREEN_X)) if seconds>=42 else visibility
        guide_visibility = guide_visibility*construction_visibility(seconds)
        late_style = ease((seconds-24.0)/5.0)
        source_count = max(1.0,float(np.sum(masks[0,self.selected_indices(seconds)])))
        old_ink = 110*min(1.0,np.sqrt(3.0/source_count))*(1-0.5*ease((source_count-7)/8))
        blue_ink = old_ink+late_style*(min(old_ink,LATE_BLUE_OPACITY)-old_ink)
        markers = []
        if include_components and np.max(guide_visibility)>0:
            for screen,source,columns,component in self.components(seconds,masks):
                curves = phase_contours(component,self.sampler.x[columns],self.sampler.y,phase,COMPONENT_ZERO)
                alpha = guide_visibility[screen]*masks[screen,source]
                self.draw_curves(draw,curves,(*BLUE,round(blue_ink*alpha)),1.0)
                markers.append((screen,source,alpha*(1-late_style)))

        combined = phase_contours(field,self.sampler.x,self.sampler.y,phase,COMBINED_ZERO)
        self.draw_curves(draw,combined,(*GOLD,238),1.6)

        # Real masks fade into identity at exactly the unchanged model times.
        # Only strip dimensions are exaggerated. Draw these over both wave
        # layers so the screen columns retain their visual identity.
        visual_masks = self.display_opacity(seconds)
        stroke_width = 4.0+late_style*(LATE_STROKE_WIDTH-4.0)
        for screen,position in enumerate(SCREEN_X):
            x = pixels([[position,0]])[0,0]
            half = stroke_width*SCALE/2
            for row,alpha in enumerate(visual_masks[screen]):
                if alpha>1e-5:
                    draw.line((x-half,BOX[1]*SCALE+row,x+half,BOX[1]*SCALE+row),
                              fill=(*INK,round(245*alpha)),width=1)
            if visibility[screen]>0:
                for y in (BOX[1]-7,BOX[3]+7):
                    draw.line((x-4*SCALE,y*SCALE,x+4*SCALE,y*SCALE),
                              fill=(*INK,round(180*visibility[screen])),width=2*SCALE)

        imaginary = ease((seconds-46)/1.5)
        if imaginary>0:
            for position in SCREEN_X:
                x = pixels([[position,0]])[0,0]
                for y in range(BOX[1],BOX[3],20):
                    draw.line((x,y*SCALE,x,(y+6)*SCALE),fill=(*BLUE,round(25*imaginary)),width=SCALE)

        for screen,source,alpha in markers:
            if alpha<=1e-6:
                continue
            x,y = pixels([[SCREEN_X[screen],self.model.y[source]]])[0]
            r = 2*SCALE
            draw.ellipse((x-r,y-r,x+r,y+r),fill=(*BLUE,round(210*alpha)))

        draw.text((40*SCALE,25*SCALE),label_at(seconds),font=font(27,True),fill=INK)
        draw.text((1240*SCALE,31*SCALE),"Plane-wave illumination",font=font(18),fill=MUTED,anchor="ra")
        footer = 702*SCALE
        if seconds<30:
            labels = ((76,"combined wavefronts"),(301,"selected wavelets"))
            blue_left = 265
        else:
            labels = ((76,"total wavefronts (all sources)"),(391,"sample wavelets"))
            blue_left = 355
        draw.line((40*SCALE,footer,66*SCALE,footer),fill=GOLD,width=round(1.6*SCALE))
        draw.text((labels[0][0]*SCALE,footer),labels[0][1],font=font(14),fill=MUTED,anchor="lm")
        draw.line((blue_left*SCALE,footer,(blue_left+26)*SCALE,footer),fill=BLUE,width=SCALE)
        draw.text((labels[1][0]*SCALE,footer),labels[1][1],font=font(14),fill=MUTED,anchor="lm")
        if 30<=seconds<46:
            draw.text((1240*SCALE,footer),"screen strips enlarged",font=font(14),fill=MUTED,anchor="rm")
        elif seconds>=46:
            draw.text((1240*SCALE,footer),"imaginary slices",font=font(14),fill=MUTED,anchor="rm")
        return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


def previews(renderer,times):
    OUT.mkdir(parents=True,exist_ok=True)
    sheet = Image.new("RGB",(1536,316*((len(times)+2)//3)),BG)
    draw = ImageDraw.Draw(sheet)
    for index,seconds in enumerate(times):
        start = time.perf_counter()
        frame = renderer.frame(seconds)
        path = OUT/f"{NAME}-check-{seconds:g}.png"
        frame.save(path)
        x,y = index%3*512,index//3*316
        sheet.paste(frame.resize((512,288),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+292),f"{seconds:g} s",fill=INK)
        print(json.dumps({"preview":str(path),"elapsed":round(time.perf_counter()-start,2)}),flush=True)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")


def render(renderer):
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
        if index%(4*FPS)==0:
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


if __name__=="__main__":
    main()
