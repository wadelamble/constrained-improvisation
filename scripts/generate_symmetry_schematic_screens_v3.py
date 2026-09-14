"""Continuous screen buildup; gold is the sum of the displayed wavelet groups.

Visible aperture bins and the directly propagated outside-view remainder form
an exact partition. Every transmitting cell belongs to one component. Physical
fields are never normalized individually or replaced by a drawn envelope.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
from dataclasses import dataclass
import json
import subprocess
import time

from generate_symmetry_schematic_screens import (
    np, contourpy, Image, ImageDraw, imageio_ffmpeg, ROOT, OUT, WIDTH, HEIGHT, SCALE, BOX,
    BG, INK, BLUE, GOLD, MUTED, font, pixels, phase_contours,
    COMPONENT_ZERO, COMBINED_ZERO,
)
from generate_symmetry_schematic_screens_v2 import (
    enlarged_strip_height, periodic_opacity,
)
from schematic_screens_v3_model import (
    WaveScreensModel, SCREEN_X, SCREEN_SETS, COMBS, X_MAX, VIEW_HALF_HEIGHT,
    DURATION, FPS, K, state_at, label_at, temporal_phase, ease, group_centers,
)

NAME = "symmetry-schematic-screens-v3"
SAMPLES = (4,12,20,24,28,32,36,40,44,50)
BASIS_CHANGES = (6,10,14,18,22,26,30,34,38,42)


@dataclass
class Slab:
    screen: int
    columns: np.ndarray
    kernel: np.ndarray
    green: np.ndarray


@dataclass
class GroupedSlab:
    screen: int
    columns: np.ndarray
    visible: np.ndarray
    remainder: np.ndarray


@dataclass
class Scene:
    masks: np.ndarray
    total: np.ndarray
    slabs: list
    centers: np.ndarray


def annotation_visibility(seconds):
    # A different local partition or slab boundary is explanatory. Hide the
    # change at zero blue opacity, while the calculated gold sum keeps moving.
    return min(ease(abs(seconds-boundary)/0.3) for boundary in BASIS_CHANGES)


class Renderer:
    def __init__(self,width=800):
        self.model = WaveScreensModel()
        self.x = np.linspace(0,X_MAX,width)
        self.indices = np.flatnonzero(abs(self.model.y)<=VIEW_HALF_HEIGHT)
        self.y = self.model.y[self.indices]
        self.offsets = np.arange(-256,257)
        self.geometry_key = None
        self.geometry = []
        self.scene_cache = OrderedDict()
        self.transition_cache = None
        self.display_cache = {}

    def slab_geometry(self,planes):
        key = tuple(planes)
        if key == self.geometry_key:
            return self.geometry
        # Only current geometry retains the large full-spectrum kernels.
        self.geometry = []
        self.geometry_key = key
        for order,screen in enumerate(planes):
            stop = SCREEN_X[planes[order+1]] if order+1<len(planes) else X_MAX+1e-8
            columns = np.flatnonzero((self.x>=SCREEN_X[screen]) & (self.x<stop))
            distance = self.x[columns]-SCREEN_X[screen]
            kernel = np.exp(1j*distance[:,None]*self.model.kx[None,:])
            green = np.empty((len(self.offsets),len(columns)),complex)
            for begin in range(0,len(columns),24):
                part = np.fft.ifft(kernel[begin:begin+24],axis=1)
                green[:,begin:begin+len(part)] = part[:,self.offsets%self.model.n].T
            self.geometry.append(Slab(int(screen),columns,kernel,green))
        return self.geometry

    def propagate_remainder(self,boundary,indices,slab):
        values = np.zeros(self.model.n,complex)
        values[indices] = boundary[indices]
        result = np.zeros((len(self.indices),len(slab.columns)),complex)
        if not np.any(values):
            return result
        spectrum = np.fft.fft(values)
        for begin in range(0,len(slab.columns),24):
            part = np.fft.ifft(slab.kernel[begin:begin+24]*spectrum[None,:],axis=1)
            result[:,begin:begin+len(part)] = part[:,self.indices].T
        return result

    def propagate_visible_group(self,boundary,indices,slab):
        result = np.zeros((len(self.indices),len(slab.columns)),complex)
        # Do not drop small material terms: only exact numerical zeros skip.
        for source in indices:
            amplitude = boundary[source]
            if amplitude == 0:
                continue
            rows = self.indices-source-self.offsets[0]
            if rows.min()<0 or rows.max()>=len(self.offsets):
                raise ValueError("Visible-bin support exceeded the cached Green range")
            result += amplitude*slab.green[rows]
        return result

    def build_scene(self,masks,centers,planes,groups):
        """Direct grouped solve, with fixed partition and slab geometry."""
        total = np.broadcast_to(np.exp(1j*K*self.x),(len(self.y),len(self.x))).copy()
        grouped_slabs = []
        if planes:
            boundary_fields = self.model.screen_fields(masks)
            for slab in self.slab_geometry(planes):
                boundary = boundary_fields[slab.screen]
                visible = np.empty((len(groups)-1,len(self.y),len(slab.columns)),complex)
                combined = np.zeros((len(self.y),len(slab.columns)),complex)
                for index,indices in enumerate(groups[:-1]):
                    contribution = self.propagate_visible_group(boundary,indices,slab)
                    visible[index] = contribution
                    combined += contribution
                remainder = self.propagate_remainder(boundary,groups[-1],slab)
                combined += remainder
                total[:,slab.columns] = combined
                grouped_slabs.append(GroupedSlab(slab.screen,slab.columns,visible,remainder))
        return Scene(masks,total,grouped_slabs,centers)

    def interpolate_scenes(self,masks,scenes,factors):
        """Interpolate every complex component, then explicitly sum to gold."""
        first = scenes[0]
        total = np.broadcast_to(np.exp(1j*K*self.x),(len(self.y),len(self.x))).copy()
        slabs = []
        for index,base in enumerate(first.slabs):
            visible = np.zeros_like(base.visible)
            remainder = np.zeros_like(base.remainder)
            for factor,scene in zip(factors,scenes):
                visible += factor*scene.slabs[index].visible
                remainder += factor*scene.slabs[index].remainder
            total[:,base.columns] = visible.sum(axis=0)+remainder
            slabs.append(GroupedSlab(base.screen,base.columns,visible,remainder))
        return Scene(masks,total,slabs,first.centers)

    def scene(self,seconds):
        a,b,amount = state_at(seconds)
        if a==b:
            if self.transition_cache is not None:
                key,_,_,scenes = self.transition_cache
                if a==key[1]:
                    self.scene_cache[a] = scenes[-1]
                self.transition_cache = None
            if a in self.scene_cache:
                self.scene_cache.move_to_end(a)
                while len(self.scene_cache)>2:
                    self.scene_cache.popitem(last=False)
                return self.scene_cache[a]
            scene = self.build_scene(self.model.targets[a],group_centers(seconds),
                                     SCREEN_SETS[a],self.model.group_indices(seconds))
            self.scene_cache[a] = scene
            while len(self.scene_cache)>2:
                self.scene_cache.popitem(last=False)
            return scene

        key = (a,b)
        masks = self.model.masks_at(seconds)
        if self.transition_cache is None or self.transition_cache[0]!=key:
            self.transition_cache = None
            # Each changing mask is affine in amount. After N changing masks,
            # every fixed-partition group field has polynomial degree <= N.
            changed = np.max(abs(self.model.targets[a]-self.model.targets[b]),axis=1)>1e-12
            degree = int(np.count_nonzero(changed))
            nodes = (1-np.cos(np.pi*np.arange(degree+1)/degree))/2
            weights = (-1.0)**np.arange(degree+1)
            weights[[0,-1]] *= 0.5
            centers = group_centers(seconds)
            groups = self.model.group_indices(seconds)
            scenes = []
            start = time.perf_counter()
            for node in nodes:
                state = (1-node)*self.model.targets[a]+node*self.model.targets[b]
                scenes.append(self.build_scene(state,centers,SCREEN_SETS[b],groups))
            self.transition_cache = (key,nodes,weights,scenes)
            print(f"transition {a}->{b}: {degree+1} exact grouped nodes cached in {time.perf_counter()-start:.1f}s",flush=True)
        _,nodes,weights,scenes = self.transition_cache
        exact = np.flatnonzero(abs(nodes-amount)<1e-14)
        if len(exact):
            return scenes[int(exact[0])]
        factors = weights/(amount-nodes)
        factors /= factors.sum()
        return self.interpolate_scenes(masks,scenes,factors)

    def display_target(self,stage):
        if stage in self.display_cache:
            return self.display_cache[stage]
        height = (BOX[3]-BOX[1])*SCALE
        target = np.zeros((len(SCREEN_X),height))
        if stage in COMBS:
            pitch,fill,screens = COMBS[stage]
            dy = 2*VIEW_HALF_HEIGHT/height
            y = VIEW_HALF_HEIGHT-(np.arange(height)+0.5)*dy
            pitch_pixels = pitch*(BOX[3]-BOX[1])/(2*VIEW_HALF_HEIGHT)
            row = periodic_opacity(y,dy,pitch,enlarged_strip_height(pitch,fill)/pitch_pixels)
            target[list(screens)] = row
        else:
            for screen,mask in enumerate(self.model.targets[stage]):
                opacity = np.clip(1-mask[self.indices],0,1)[::-1]
                target[screen] = np.interp(np.linspace(0,len(opacity)-1,height),np.arange(len(opacity)),opacity)
        self.display_cache[stage] = target
        return target

    @staticmethod
    def draw_curves(draw,curves,color,width=1.0):
        for curve in curves:
            if len(curve)>1:
                draw.line(pixels(curve).ravel().tolist(),fill=color,
                          width=round(width*SCALE),joint="curve")

    def dense_local_curves(self,slab,centers,phase):
        """Batch independent local contour grids, separated by masked rows."""
        halfwidth = 0.45 if len(centers)==33 else 0.225
        ranges = [(int(np.searchsorted(self.y,center-halfwidth)),
                   int(np.searchsorted(self.y,center+halfwidth,side="right"))) for center in centers]
        stride = max(end-begin for begin,end in ranges)+1
        z = np.full((len(centers)*stride,len(slab.columns)),np.nan)
        for group,((begin,end),contribution) in enumerate(zip(ranges,slab.visible)):
            local = contribution[begin:end]
            moving = local*phase
            valid = (moving.real>0)&(np.abs(local)>=COMPONENT_ZERO)
            z[group*stride:group*stride+end-begin] = np.where(valid,moving.imag,np.nan)
        synthetic_y = np.arange(len(z))*self.model.dy
        generator = contourpy.contour_generator(x=self.x[slab.columns],y=synthetic_y,z=z,
                                                corner_mask=False,line_type="Separate")
        curves = generator.lines(0.0)
        for curve in curves:
            group = int(np.floor(float(curve[:,1].mean())/(stride*self.model.dy)))
            curve[:,1] += self.y[ranges[group][0]]-group*stride*self.model.dy
        return curves

    def frame(self,seconds,phase_seconds=None,include_components=True):
        scene = self.scene(seconds)
        phase = temporal_phase(seconds if phase_seconds is None else phase_seconds)
        image = Image.new("RGB",(WIDTH*SCALE,HEIGHT*SCALE),BG)
        draw = ImageDraw.Draw(image,"RGBA")
        a,b,amount = state_at(seconds)
        active_a = (np.max(1-self.model.targets[a],axis=1)>1e-8).astype(float)
        active_b = (np.max(1-self.model.targets[b],axis=1)>1e-8).astype(float)
        visibility = active_a+amount*(active_b-active_a)
        guide_visibility = np.ones(len(SCREEN_X)) if seconds>=46 else visibility
        guide_visibility *= annotation_visibility(seconds)
        dense = len(scene.centers)>15
        blue_ink = float(np.interp(len(scene.centers),[1,3,7,15,33,65],[90,70,45,28,48,42]))

        if include_components:
            for slab in scene.slabs:
                alpha = guide_visibility[slab.screen]
                if alpha<=0:
                    continue
                if dense:
                    # Crop only drawn curves; the gold sum keeps every field.
                    curves = self.dense_local_curves(slab,scene.centers,phase)
                    self.draw_curves(draw,curves,(*BLUE,round(blue_ink*alpha)))
                else:
                    for contribution in slab.visible:
                        curves = phase_contours(contribution,self.x[slab.columns],self.y,phase,COMPONENT_ZERO)
                        self.draw_curves(draw,curves,(*BLUE,round(blue_ink*alpha)))
        combined = phase_contours(scene.total,self.x,self.y,phase,COMBINED_ZERO)
        self.draw_curves(draw,combined,(*GOLD,238),1.6)

        display = (1-amount)*self.display_target(a)+amount*self.display_target(b)
        stroke = 4.0 if b<=4 else 3.0
        for screen,position in enumerate(SCREEN_X):
            x = pixels([[position,0]])[0,0]
            for row,alpha in enumerate(display[screen]):
                if alpha>1e-5:
                    draw.line((x-stroke*SCALE/2,BOX[1]*SCALE+row,x+stroke*SCALE/2,BOX[1]*SCALE+row),
                              fill=(*INK,round(245*alpha)),width=1)
            if visibility[screen]>0:
                for y in (BOX[1]-7,BOX[3]+7):
                    draw.line((x-4*SCALE,y*SCALE,x+4*SCALE,y*SCALE),
                              fill=(*INK,round(180*visibility[screen])),width=2*SCALE)
        imaginary = ease((seconds-48)/1.5)
        if imaginary>0:
            for position in SCREEN_X:
                x = pixels([[position,0]])[0,0]
                for y in range(BOX[1],BOX[3],20):
                    draw.line((x,y*SCALE,x,(y+6)*SCALE),fill=(*BLUE,round(25*imaginary)),width=SCALE)

        draw.text((40*SCALE,25*SCALE),label_at(seconds),font=font(27,True),fill=INK)
        draw.text((1240*SCALE,31*SCALE),"Plane-wave illumination",font=font(18),fill=MUTED,anchor="ra")
        footer = 702*SCALE
        draw.line((40*SCALE,footer,66*SCALE,footer),fill=GOLD,width=round(1.6*SCALE))
        draw.text((76*SCALE,footer),"complete coherent sum",font=font(14),fill=MUTED,anchor="lm")
        draw.line((300*SCALE,footer,326*SCALE,footer),fill=BLUE,width=SCALE)
        draw.text((336*SCALE,footer),"local wavelet arcs" if dense else "wavelet contributions",font=font(14),fill=MUTED,anchor="lm")
        if seconds>=2:
            note = "full fields summed"
            if 18<=seconds<48:
                note += " · screen strips enlarged"
            elif seconds>=48:
                note += " · imaginary slices"
            draw.text((1240*SCALE,footer),note,font=font(14),fill=MUTED,anchor="rm")
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
        elapsed = time.perf_counter()-start
        # One second frame at a new phase measures a static scene's hot path.
        start = time.perf_counter()
        renderer.frame(seconds+1/FPS)
        cached_elapsed = time.perf_counter()-start
        x,y = index%3*512,index//3*316
        sheet.paste(frame.resize((512,288),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+12,y+292),f"{seconds:g} s",fill=INK)
        print(json.dumps({"preview":str(path),"first_frame_seconds":round(elapsed,3),
                          "cached_frame_seconds":round(cached_elapsed,3)}),flush=True)
    sheet.save(OUT/f"{NAME}-contact-sheet.png")


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
