"""A very-short-wavelength grouped tip-to-tail sum, with fixed aperture bins.

This is a still for agreeing on the visual before any further animation.
It displays exact group integrals, not an artificially straightened Cornu
curve. The complete propagation prefactor is retained, as in the prior
two-limit model. The carrier exp(ikz) defines the declared phase reference.
"""
from __future__ import annotations

import json
import math

from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, OUT, BG, PANEL, INK, MUTED, BORDER, BLUE, GOLD,
    SUPERSAMPLE, pixels, text, line, arrow, cumulative,
)

NAME = "symmetry-short-wavelength-grouped-limit"
WIDTH, HEIGHT = 1280, 790
F_NUMBER = 100_000_000.0
GROUPS = 21
EDGES = np.linspace(-1.0, 1.0, GROUPS+1)
CENTRAL = GROUPS//2
VALUES = cumulative(F_NUMBER, EDGES)
TERMS = np.diff(VALUES)
TOTAL = complex(VALUES[-1])
CENTRAL_SUM = complex(TERMS[CENTRAL])
OUTER_SUM = complex(np.sum(np.delete(TERMS, CENTRAL)))
SCALE = 910.0
ORIGIN_X, CHAIN_Y, TOTAL_Y = 176.0, 395.0, 532.0


def point(value, baseline=CHAIN_Y):
    return (ORIGIN_X + SCALE*value.real, baseline - SCALE*value.imag)


def dot(draw, xy, color, radius=2.7):
    x,y=xy
    draw.ellipse(pixels((x-radius,y-radius,x+radius,y+radius)),fill=color)


def leader(draw, first, last):
    line(draw,first,last,(*MUTED,150),1)


def independent_check():
    # Independent large-argument endpoint expansion, valid at every group
    # boundary (the closest boundary is |u|=1/21). Integrate by parts three
    # times rather than calling Fresnel special functions a second time.
    a = np.pi*F_NUMBER
    u = np.abs(EDGES)
    tail = np.exp(1j*a*u*u)*(1j/(2*a*u)+1/(4*a*a*u**3)-3j/(8*a**3*u**5))
    primitive = np.sign(EDGES)*(.5-np.exp(-.25j*np.pi)*math.sqrt(F_NUMBER)*tail)
    independent_terms = np.diff(primitive)
    error = float(np.max(np.abs(independent_terms-TERMS)))
    assert error < 1e-9, error
    assert abs(sum(TERMS)-TOTAL) < 1e-14
    assert abs(CENTRAL_SUM+OUTER_SUM-TOTAL) < 1e-14
    assert abs(OUTER_SUM)/abs(TOTAL) < .001
    assert max(abs(np.delete(TERMS,CENTRAL))) * SCALE < 1
    report = {
        "F_a_squared_over_lambda_z":F_NUMBER,
        "fixed_equal_aperture_groups":GROUPS,
        "central_interval_y_over_a":[float(EDGES[CENTRAL]),float(EDGES[CENTRAL+1])],
        "central_amplitude":[CENTRAL_SUM.real,CENTRAL_SUM.imag],
        "outer_groups_combined":[OUTER_SUM.real,OUTER_SUM.imag],
        "total_amplitude":[TOTAL.real,TOTAL.imag],
        "outer_combined_magnitude_over_total":abs(OUTER_SUM)/abs(TOTAL),
        "largest_individual_outer_group_magnitude":float(max(abs(np.delete(TERMS,CENTRAL)))),
        "independent_endpoint_expansion_max_error":error,
        "pixels_per_amplitude_unit":SCALE,
        "central_group_dy_pixels":CENTRAL_SUM.imag*SCALE,
        "phase_reference":"unobstructed plane wave exp(ikz) at B; full Fresnel prefactor retained",
        "gold_resultant_display":"translated down; same scale and actual angle",
        "individual_path_claim":False,
    }
    return report


def draw():
    image = Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d = ImageDraw.Draw(image,"RGBA")
    d.rounded_rectangle(pixels((24,20,1256,765)),radius=24,fill=PANEL,
                        outline=BORDER,width=3)
    text(d,(50,43),"Very short wavelength · grouped tip-to-tail sum",29,bold=True)
    text(d,(51,91),"Each arrow sums a fixed region of the opening.",21,MUTED)

    # A single aperture coordinate strip identifies what the vector groups
    # refer to. No physical ray trajectories or spatial wavefronts are drawn.
    bar_x,bar_y,bar_w,bar_h=176,170,910,34
    cell_w=bar_w/GROUPS
    text(d,(bar_x,137),"21 fixed regions across the opening",17,MUTED)
    for j in range(GROUPS):
        x0=bar_x+j*cell_w
        fill=BLUE if j==CENTRAL else (226,222,214)
        d.rectangle(pixels((x0+1,bar_y,x0+cell_w-1,bar_y+bar_h)),fill=fill)
    middle=bar_x+bar_w/2
    line(d,(middle,bar_y-5),(middle,bar_y+bar_h+9),GOLD,2)
    text(d,(bar_x,217),"−a",17,MUTED,anchor="ma")
    text(d,(bar_x+bar_w,217),"+a",17,MUTED,anchor="ma")
    text(d,(middle,220),"y = 0 · stationary path",18,BLUE,anchor="ma")
    text(d,(middle,253),"The blue region contains neighboring paths, not one isolated path.",17,MUTED,anchor="ma")
    line(d,(50,295),(1230,295),BORDER,1)

    text(d,(61,315),"Group sums, added tip to tail",21,bold=True)
    # Every vector is drawn at its computed magnitude and direction. Tiny
    # outer arrows are not enlarged. Their common endpoint clusters are
    # identified by thin leaders and a quantitative residual below.
    for j,(first,last) in enumerate(zip(VALUES[:-1],VALUES[1:])):
        arrow(d,point(first),point(last),BLUE,
              width=3.3 if j==CENTRAL else 1.35,head=12 if j==CENTRAL else 3)
    dot(d,point(0j),MUTED)
    dot(d,point(TOTAL),BLUE)
    text(d,(631,355),"Central region",20,BLUE,anchor="ma")
    text(d,(176,435),"10 outer groups",17,MUTED,anchor="ma")
    text(d,(1086,435),"10 outer groups",17,MUTED,anchor="ma")
    leader(d,(176,428),point(VALUES[CENTRAL]))
    leader(d,(1086,428),point(VALUES[CENTRAL+1]))

    # A translated copy makes the gold total distinguishable without hiding
    # the central blue vector. Both rows have the same units and direction.
    arrow(d,point(0j,TOTAL_Y),point(TOTAL,TOTAL_Y),GOLD,width=3.4,head=12)
    dot(d,point(0j,TOTAL_Y),MUTED)
    dot(d,point(TOTAL,TOTAL_Y),GOLD)
    text(d,(631,487),"Total of all 21 groups",21,GOLD,anchor="ma")
    text(d,(176,552),"0",16,MUTED,anchor="ma")
    text(d,(1086,552),"≈ 1",16,MUTED,anchor="ma")
    text(d,(631,602),f"Outer groups combined: {100*abs(OUTER_SUM)/abs(TOTAL):.3f}% of the total amplitude",22,INK,anchor="ma")
    text(d,(631,640),"Their tiny arrows remain at the two ends; the central group supplies nearly the whole sum.",17,MUTED,anchor="ma")

    line(d,(50,693),(1230,693),BORDER,1)
    text(d,(51,714),"Fixed geometry · λz/a² = 10⁻⁸",17,MUTED)
    text(d,(1230,714),"Phase relative to the unobstructed wave · one amplitude scale",17,MUTED,anchor="ra")
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(parents=True,exist_ok=True)
    validation=independent_check()
    output=OUT/f"{NAME}.png"
    draw().save(output)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(validation,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"image":str(output),**validation}),flush=True)
