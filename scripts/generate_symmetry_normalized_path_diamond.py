"""The dense path diamond with complete scalar propagation, / the free field.

Retains the raw film's 20,001 crossing positions, timing, and paired drawing.
Restores the source and Rayleigh--Sommerfeld weights used in the established
desktop propagation model. The reference is independently specified H0(k*9),
never the computed finite-aperture endpoint. Earlier files are preserved.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math

import generate_symmetry_dense_path_diamond as drawing
from generate_symmetry_two_tip_to_tail_limits import (
    np, Image, ImageDraw, imageio_ffmpeg, OUT, BG, PANEL, INK, MUTED,
    BORDER, BLUE, GOLD, AXIS, SUPERSAMPLE, pixels, text, line,
)
from scipy.special import hankel1
from scipy.integrate import quad_vec

NAME = "symmetry-normalized-path-diamond-wavelength-scan"
N, Y, DY = drawing.N, drawing.POSITIONS, drawing.PITCH
Z1 = Z2 = drawing.DISTANCE
HALF_EXTENT, WAVELENGTHS = drawing.HALF_EXTENT, drawing.WAVELENGTHS
WIDTH, HEIGHT, FPS = drawing.WIDTH, drawing.HEIGHT, drawing.FPS
ORIGIN, PIXELS_PER_UNIT = (300.0, 770.0), 620.0
TRACE_BOUNDS = (95, 586, 1270, 967)


def source(z, y, wavelength):
    return hankel1(0, (2*np.pi/wavelength)*np.hypot(z,y))


def kernel(z, y, wavelength):
    k = 2*np.pi/wavelength
    r = np.hypot(z,y)
    return .5j*k*z/r*hankel1(1,k*r)


def reference(wavelength):
    return complex(source(Z1+Z2,0.0,wavelength))


def integrand(y, wavelength):
    return source(Z1,y,wavelength)*kernel(Z2,-np.asarray(y),wavelength)/reference(wavelength)


def point(z):
    return (ORIGIN[0]+PIXELS_PER_UNIT*z.real, ORIGIN[1]-PIXELS_PER_UNIT*z.imag)


@lru_cache(None)
def model(stage):
    wavelength = WAVELENGTHS[stage]
    vectors = DY*integrand(Y,wavelength)
    vertices = np.r_[0j,np.cumsum(vectors)]
    phases = np.unwrap(np.angle(vectors))
    coords = tuple(point(z) for z in vertices)
    return phases,vectors,vertices,coords,tuple(pixels(xy) for xy in coords)


@lru_cache(None)
def background(stage):
    image = Image.new("RGB",(WIDTH*SUPERSAMPLE,HEIGHT*SUPERSAMPLE),BG)
    d = ImageDraw.Draw(image,"RGBA")
    text(d,(38,23),"Same paths · normalized propagation",31,bold=True)
    text(d,(39,67),"Point source A · fixed observation point B · one screen",19,MUTED)
    ratio = round(WAVELENGTHS[0]/WAVELENGTHS[stage])
    label = "λ = λ₀" if ratio == 1 else f"λ = λ₀ / {ratio}"
    text(d,(1400,23),label,31,bold=True,anchor="ra")
    text(d,(1400,69),f"{stage+1} / 3",18,MUTED,anchor="ra")
    for box in ((30,111,1410,475),(30,494,1410,1021)):
        d.rounded_rectangle(pixels(box),radius=14*SUPERSAMPLE,
                            fill=PANEL,outline=BORDER,width=SUPERSAMPLE)
    text(d,(53,129),"Path diamond",23,bold=True)
    text(d,(1387,134),"20,001 fixed paths",19,MUTED,anchor="ra")
    upper,lower = drawing.crossing(HALF_EXTENT),drawing.crossing(-HALF_EXTENT)
    d.polygon([pixels(xy) for xy in (drawing.A,upper,drawing.B,lower)],fill=(*BLUE,12))
    for end in (upper,lower):
        line(d,drawing.A,end,(*BLUE,35),.7)
        line(d,end,drawing.B,(*BLUE,35),.7)
    text(d,(53,512),"Tip to tail",23,bold=True)
    text(d,(1068,517),"Blue: contributions",18,BLUE,anchor="ra")
    text(d,(1387,517),"Gold: sum so far",18,GOLD,anchor="ra")
    text(d,(53,551),"Propagation weights included in every contribution",16,MUTED)
    drawing.dash(d,(101,ORIGIN[1]),(1300,ORIGIN[1]),AXIS,.8,3,5)
    text(d,(1312,ORIGIN[1]-10),"Re",14,MUTED)
    # Independently known free propagation is a fixed reference at (1,0).
    # Draw it below the moving gold tip so it never hides a small difference.
    x,y = point(1+0j)
    d.ellipse(pixels((x-5,y-5,x+5,y+5)),outline=(*MUTED,180),width=SUPERSAMPLE)
    text(d,(53,992),"Reference: unobstructed A → B = 1",16,MUTED)
    text(d,(1387,992),"Same phase reference · same plot scale",16,MUTED,anchor="ra")
    x0,x1,bar_y = 1210,1210+.2*PIXELS_PER_UNIT,966
    line(d,(x0,bar_y),(x1,bar_y),MUTED,1)
    for x in (x0,x1):
        line(d,(x,bar_y-4),(x,bar_y+4),MUTED,1)
    text(d,((x0+x1)/2,bar_y+9),"0.2",14,MUTED,anchor="ma")
    text(d,(39,1041),"Scalar wave propagation · 20,001 fixed paths",17,MUTED)
    text(d,(1400,1041),"λ₀ = 0.5 · A–screen = screen–B = 4.5",17,MUTED,anchor="ra")
    return image


def configure_renderer():
    """Use the previous paired renderer with an explicitly replaced model.

    This configures only this Python process. It neither edits the previous
    generator nor writes to any previous movie's output paths.
    """
    drawing.NAME = NAME
    drawing.ORIGIN = ORIGIN
    drawing.PHASOR_SCALE = PIXELS_PER_UNIT
    drawing.model = model
    drawing.background = background


def spectral_kernel(z,y,wavelength,order):
    """Independent angular-spectrum evaluation, including evanescent waves."""
    nodes,weights = np.polynomial.legendre.leggauss(order)
    k = 2*np.pi/wavelength
    theta = nodes*np.pi/2
    propagating = k/4*np.sum(weights*np.cos(theta)*np.exp(1j*k*(z*np.cos(theta)+y*np.sin(theta))))
    t_max = np.arcsinh(45/(k*z))
    t = (nodes+1)*t_max/2
    evanescent = k/np.pi*t_max/2*np.sum(weights*np.sinh(t)*np.exp(-k*z*np.sinh(t))*np.cos(k*y*np.cosh(t)))
    return propagating+evanescent


def checks():
    assert N == 20001 and Y[N//2] == 0.0
    assert np.max(np.abs(Y+Y[::-1])) < 2e-15
    path_hash=hashlib.sha256(Y.tobytes()).hexdigest()
    # Verify kernel amplitude AND phase independently in the angular spectrum.
    spectral_errors=[]
    for wavelength in WAVELENGTHS:
        # Keep k*z fixed for a well-resolved independent quadrature at every λ.
        z,y = 1.4*wavelength,.6*wavelength
        expected=kernel(z,y,wavelength)
        actual=spectral_kernel(z,y,wavelength,192)
        error=float(abs(actual-expected)/abs(expected))
        assert error < 2e-11
        spectral_errors.append(error)
    # A transparent intermediate plane must reproduce the independently
    # known free field. Integrate a much wider plane with 8-point Gaussian
    # panels; the small residual is from the finite |y| <= 256 cutoff.
    plane_errors=[]
    nodes,gauss_weights=np.polynomial.legendre.leggauss(8)
    plane_extent=256.0
    for wavelength in WAVELENGTHS:
        panels=math.ceil(plane_extent/(wavelength/2))
        width=plane_extent/panels
        plane_y=(np.arange(panels)[:,None]+.5)*width+nodes[None,:]*width/2
        reconstructed=2*np.sum(integrand(plane_y,wavelength)*gauss_weights[None,:]*width/2)
        error=float(abs(reconstructed-1))
        assert error<3e-5
        plane_errors.append(error)
    reports=[]
    for stage,wavelength in enumerate(WAVELENGTHS):
        phases,vectors,vertices,coords,_=model(stage)
        assert len(vectors)==N and len(vertices)==N+1
        assert np.max(np.abs(np.diff(vertices)-vectors)) < 3e-16
        assert np.max(np.abs(vectors-vectors[::-1])) < 3e-14
        max_step=float(np.max(np.abs(np.diff(phases))))
        assert max_step < np.pi/8
        # Three times as many midpoint nodes, reduced to the SAME prefix edges.
        fine_count=3*N
        fine_y=HALF_EXTENT-(np.arange(fine_count)+.5)*2*HALF_EXTENT/fine_count
        fine_vectors=integrand(fine_y,wavelength)*2*HALF_EXTENT/fine_count
        fine_chain=np.r_[0j,np.cumsum(fine_vectors.reshape(N,3).sum(axis=1))]
        refinement=float(np.max(np.abs(vertices-fine_chain)))
        assert refinement < 1e-4
        adaptive=[]
        for fraction in (.25,.49,.5,.51,.75,1.0):
            count=round(fraction*N)
            lower=HALF_EXTENT-count*DY
            value,_=quad_vec(lambda y:integrand(y,wavelength),lower,HALF_EXTENT,
                             epsabs=1e-10,epsrel=1e-10,limit=5000)
            error=float(abs(vertices[count]-value))
            assert error < 1e-4
            adaptive.append({"count":count,"absolute_error":error})
        xy=np.asarray(coords)
        left,top,right,bottom=TRACE_BOUNDS
        margin=float(min(xy[:,0].min()-left,right-xy[:,0].max(),
                         xy[:,1].min()-top,bottom-xy[:,1].max()))
        assert margin > 8,margin
        assert abs(source(Z1+Z2,0,wavelength)/reference(wavelength)-1)<1e-15
        endpoint=complex(vertices[-1])
        reports.append({"wavelength":wavelength,"path_count":N,"positions_sha256":path_hash,
                        "reference_real_imag":[reference(wavelength).real,reference(wavelength).imag],
                        "endpoint":[endpoint.real,endpoint.imag],"magnitude":abs(endpoint),
                        "phase_degrees":float(np.angle(endpoint,deg=True)),
                        "vector_magnitude_min_max":[float(abs(vectors).min()),float(abs(vectors).max())],
                        "max_adjacent_phase_step_degrees":math.degrees(max_step),
                        "all_prefix_refinement_max_error":refinement,"adaptive_prefix_checks":adaptive,
                        "trace_margin_pixels":margin})
    report={"model":"one-transverse-coordinate scalar Rayleigh--Sommerfeld propagation",
            "source":"outgoing H0^(1)(k*r)","kernel":"i*k*z*H1^(1)(k*r)/(2*r)",
            "reference":"independent unobstructed source H0^(1)(k*(z1+z2)) at each wavelength",
            "source_position":[-Z1,0],"screen_x":0,"observer_position":[Z2,0],
            "permitted_transverse_span":[-HALF_EXTENT,HALF_EXTENT],"midpoint_spacing":DY,
            "same_crossing_positions_every_pass":True,"fixed_path_count":N,
            "wavelength_dependent_source_and_kernel_weights":True,"equal_vector_lengths":False,
            "normalizes_all_vectors_and_prefixes":True,"endpoint_dependent_scaling":False,
            "additional_display_rotation":False,"fixed_pixels_per_reference_amplitude":PIXELS_PER_UNIT,
            "fixed_origin":ORIGIN,"grouping_or_artificial_straightening":False,
            "intensity_or_arrival_probability_claim":False,"spectral_kernel_relative_errors":spectral_errors,
            "transparent_plane_extent":plane_extent,"transparent_plane_reference_errors":plane_errors,
            "path_paint":"schematic envelope of added routes, not amplitude or probability",
            "screen":"schematic sampling plane; no new finite-hole width or opaque fill fraction",
            "timing":{"settle":drawing.SETTLE_FRAMES/FPS,"scan":drawing.SCAN_FRAMES/FPS,
                      "hold":drawing.HOLD_FRAMES/FPS,"duration":drawing.DURATION},
            "resolution":[WIDTH,HEIGHT],"fps":FPS,"frames":drawing.TOTAL_FRAMES,"stages":reports}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{NAME}-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"spectral_errors":spectral_errors,"transparent_plane_errors":plane_errors,
                      "stages":reports}),flush=True)


def encoded_checks():
    wanted={drawing.frame_for_count(stage,round(N*fraction)) for stage in range(3)
            for fraction in (0,.25,.49,.5,.51,.75,1)}|{drawing.TOTAL_FRAMES-1}
    reader=imageio_ffmpeg.read_frames(str(OUT/f"{NAME}.mp4"),pix_fmt="rgb24")
    metadata=next(reader)
    assert tuple(metadata["size"])==(WIDTH,HEIGHT) and abs(metadata["fps"]-FPS)<1e-8
    checked,selected,decoded_count=[],{},0
    for index,raw in enumerate(reader):
        decoded_count+=1
        if index not in wanted:
            continue
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(HEIGHT,WIDTH,3)
        expected=np.asarray(drawing.frame(index))
        mae=float(np.mean(np.abs(decoded.astype(float)-expected.astype(float))))
        assert mae<2.5,(index,mae)
        stage,count=drawing.state(index)
        tip_pixels=None
        if count:
            x,y=map(round,model(stage)[3][count])
            crop=decoded[y-5:y+6,x-5:x+6].astype(float)
            tip_pixels=int(np.sum(np.linalg.norm(crop-np.asarray(GOLD),axis=2)<65))
            assert tip_pixels>8,(index,tip_pixels)
        checked.append({"frame":index,"stage":stage+1,"count":count,
                        "mean_absolute_rgb_error":mae,"gold_tip_pixels":tip_pixels})
        if count==N:
            selected[stage]=Image.fromarray(decoded.copy())
    assert decoded_count==drawing.TOTAL_FRAMES and len(selected)==3
    sheet=Image.new("RGB",(1440,1200),BG)
    for stage in range(3):
        sheet.paste(selected[stage].resize((480,360),Image.Resampling.LANCZOS),(stage*480,0))
        crop=selected[stage].crop((95,590,1270,975)).resize((840,275),Image.Resampling.LANCZOS)
        sheet.paste(crop,(300,370+stage*275))
    sheet.save(OUT/f"{NAME}-encoded-contact-sheet.png")
    report={"decoded_frames":decoded_count,"duration_seconds":decoded_count/FPS,
            "fps":metadata["fps"],"resolution":metadata["size"],"representative_checks":checked}
    (OUT/f"{NAME}-encoded-validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_frames":decoded_count,"checked_frames":len(checked),
                      "maximum_rgb_error":max(x["mean_absolute_rgb_error"] for x in checked)}),flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for option in ("check","preview","render","encoded-check"):
        parser.add_argument("--"+option,action="store_true")
    args=parser.parse_args()
    configure_renderer()
    if args.check:
        checks()
    if args.preview:
        drawing.previews()
    if args.render:
        drawing.render()
    if args.encoded_check:
        encoded_checks()
