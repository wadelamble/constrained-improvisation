"""Plain, ungrouped short-wavelength Fresnel tip-to-tail curve.

No path-bin regrouping, substituted chords, or resultant-dependent rotation.
The infinitesimal contributions trace the complete cumulative Fresnel sum.
"""
from __future__ import annotations

import json
import math
from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, OUT, BG, INK, MUTED, BLUE, GOLD,
    SUPERSAMPLE, pixels, text, line, arrow, cumulative,
)

NAME = "symmetry-short-wavelength-plain-tip-to-tail"
WIDTH, HEIGHT = 1200, 600
F_NUMBER = 100_000_000.0
SCALE, ORIGIN_X, ORIGIN_Y = 830.0, 183.0, 307.0


def point(value):
    return (ORIGIN_X+SCALE*value.real, ORIGIN_Y-SCALE*value.imag)


def values(u):
    return cumulative(F_NUMBER, np.asarray(u)/math.sqrt(F_NUMBER))


def draw():
    image=Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d=ImageDraw.Draw(image,"RGBA")
    text(d,(36,27),"Very short wavelength",27,bold=True)
    arrow(d,(895,47),(927,47),BLUE,1.7,5)
    text(d,(936,34),"contributions",16,BLUE)
    arrow(d,(1083,47),(1115,47),GOLD,2.7,7)
    text(d,(1124,34),"sum",16,GOLD)

    # Parameter u=y/sqrt(lambda*z) makes the Fresnel phase pi*u^2.
    # Resolve every visible loop with at least ~14 edges per revolution.
    # More distant loops fit within 0.54 output pixels of their endpoint;
    # they remain as calculated samples, with only their sampling coarsened.
    visible_u=250.0
    dense=np.sqrt(np.linspace(0.0,visible_u**2,436334))
    tail=np.geomspace(visible_u,math.sqrt(F_NUMBER),4097)[1:]
    # Phase-uniform sampling alone is sparse at u=0. Resolve the central
    # connecting curve independently in u so the drawing has no long chords.
    positive=np.unique(np.r_[dense,tail,np.linspace(0.0,12.0,24001)])
    u=np.r_[-positive[:0:-1],positive]
    chain=values(u)
    coords=np.empty((len(chain),2))
    coords[:,0]=(ORIGIN_X+SCALE*chain.real)*SUPERSAMPLE
    coords[:,1]=(ORIGIN_Y-SCALE*chain.imag)*SUPERSAMPLE
    d.line(coords.ravel().tolist(),fill=BLUE,width=round(1.6*SUPERSAMPLE))

    # Direction markers sit on the actual curve, rather than replacing
    # stretches of it with grouped-resultant chords. Omit markers that
    # would be smaller than a pixel in the tightly packed endpoint coils.
    marker_u=np.arange(-12.0,12.001,.030)
    marker_values=values(marker_u)
    for position,t in zip(marker_values,marker_u):
        radius_px=SCALE/(2*math.pi*max(abs(float(t)),.05))
        head=min(4.6,.11*radius_px)
        if head<1.0:
            continue
        angle=math.pi*t*t-math.pi/4
        x,y=point(position)
        tangent=(math.cos(angle),-math.sin(angle))
        normal=(-tangent[1],tangent[0])
        triangle=[(x,y)]+[(x-head*tangent[0]+side*.42*head*normal[0],
                           y-head*tangent[1]+side*.42*head*normal[1]) for side in (-1,1)]
        d.polygon([pixels(p) for p in triangle],fill=BLUE)

    endpoint=complex(chain[-1])
    arrow(d,point(0j),point(endpoint),GOLD,width=3.1,head=11)
    for z,color in ((0j,MUTED),(endpoint,GOLD)):
        x,y=point(z)
        d.ellipse(pixels((x-2.8,y-2.8,x+2.8,y+2.8)),fill=color)
    assert np.min(coords[:,0])/SUPERSAMPLE>25
    assert np.max(coords[:,0])/SUPERSAMPLE<WIDTH-25
    assert np.min(coords[:,1])/SUPERSAMPLE>95
    assert np.max(coords[:,1])/SUPERSAMPLE<HEIGHT-45
    assert abs(endpoint-values([1e4])[-1])<1e-12
    metadata={"F":F_NUMBER,"phase_reference":"U / exp(ikz); normalized Fresnel kernel retained",
              "grouped":False,"curve_samples":len(u),"pixels_per_amplitude_unit":SCALE,
              "tail_sampling_changes_below_radius_px":SCALE/(2*math.pi*visible_u),
              "endpoint":[endpoint.real,endpoint.imag],"image_size":[WIDTH,HEIGHT]}
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS),metadata


if __name__ == "__main__":
    OUT.mkdir(parents=True,exist_ok=True)
    image,metadata=draw()
    image.save(OUT/f"{NAME}.png")
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"image":str(OUT/f"{NAME}.png"),**metadata}),flush=True)
