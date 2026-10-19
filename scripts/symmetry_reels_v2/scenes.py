"""Desktop-complete scene routing. The first series remains read-only."""
from __future__ import annotations
import importlib.util
import json
import core
from core import *

SPECS = json.loads((Path(__file__).parent/'series.json').read_text(encoding='utf8'))


@lru_cache(2)
def legacy_module(which):
    path=ROOT/'scripts/symmetry_reels'/f'episodes_{which}.py'
    spec=importlib.util.spec_from_file_location(f'symmetry_v2_legacy_{which}',path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module


def inventory(number):
    spec=SPECS[number-1]
    kind=spec['renderer']
    if kind in ('early','late'):
        module=__import__(kind)
        return list(module.SCREEN_TEXT[spec.get('scene_number',number)])
    if kind in ('casimir','lie_commutator'):
        return list(__import__(kind).SCREEN_TEXT)
    if kind=='carriers':
        return ['The same actions on different objects','120° rotation','Reflection',
                r'D_3=\{e,r,r^2,s,rs,r^2s\}',r'r^3=e',r's^2=e']
    old=2 if kind=='triangle' else 16 if kind=='wave' else int(kind.split(':')[1])
    if old==15:
        return list(__import__('eigenfunctions').SCREEN_TEXT)
    module=legacy_module('first' if old<=8 else 'second')
    result=list(module.SCREEN_TEXT[old])
    if kind=='wave':
        result += [r'\lambda=\frac{2\pi}{k}']
    return result


def reused(number,t,entry,old,source_duration=None):
    module=legacy_module('first' if old<=8 else 'second')
    display_t=t
    def new_scene(_number,_title,stage='',*args,**kwargs):
        return Scene(number,entry['title'],stage,display_t,entry['duration'],total=TOTAL)
    # The legacy renderer evaluates its exact existing mathematics. All text
    # replacement is applied centrally by the new Scene, so slot counts stay
    # independent of where this scene now appears in the expanded sequence.
    inner=dict(entry)
    inner.pop('screen_text',None)
    inner.pop('on_screen_text',None)
    if source_duration is not None:
        inner['duration']=source_duration
        t=t*source_duration/entry['duration']
    original_scene=module.Scene
    module.Scene=new_scene
    try:
        return module.render(old,t,inner)
    finally:
        module.Scene=original_scene


def carriers(t,entry):
    duration=entry['duration']
    q=t/duration*22
    labels=inventory(3)
    act='rotation' if q<12 else 'reflection'
    s=Scene(3,entry['title'],labels[0],t,duration)
    s.panel((70,490,950,1360))
    s.text(510,525,labels[1 if act=='rotation' else 2],34,GOLD,anchor='ma')
    if act=='rotation':
        matrix=rotation(2*np.pi/3*float(ease(window(q,2,9))))
    else:
        matrix=np.diag([math.cos(np.pi*float(ease(window(q,14,20)))),1])
    centers=[(290,800),(730,800),(290,1150),(730,1150)]
    for center,paths in zip(centers,legacy_module('first').d3_carrier_paths()):
        center=np.array(center,dtype=float)
        for path in paths:
            s.line(center+path*[135,-135],GRID,2)
        for path in paths:
            s.line(center+(path@matrix.T)*[135,-135],INK,4)
    s.math(labels[3],y=1450,size=46)
    s.math(labels[4],x=320,y=1545,size=49,maxwidth=300)
    s.math(labels[5],x=710,y=1545,size=49,maxwidth=300)
    return s.im


def wave(t,entry):
    s = Scene(25, entry["title"], "A complex wave", t, entry["duration"])
    q = 24*t/entry["duration"]
    _dashed = legacy_module("second")._dashed
    physical_t = float(np.clip(q-2, 0, 20))
    k, omega, x0 = math.pi/2, math.pi/3, 4.
    x = np.linspace(0, 8, 850)
    z = np.exp(1j*(k*x-omega*physical_t))
    z0 = complex(np.exp(1j*(k*x0-omega*physical_t)))
    left, right, center_y, gain, depth = 160., 860., 815., 115., .65
    rotation = np.exp(-.38j)

    def project(xx, zz):
        xx, zz = np.broadcast_arrays(np.asarray(xx), np.asarray(zz))
        transverse = zz*rotation
        return np.stack((left+xx/8*(right-left)+depth*gain*transverse.imag,
                         center_y-gain*transverse.real), axis=-1)

    s.math(r"z(x,t)=e^{i(kx-\omega t)}", y=540, size=60)
    s.line([project(0, 0), project(8, 0)], MUTED, 2)
    s.text(882, 813, "x", 32, MUTED)
    for value in (0, 4, 8):
        pos = project(value, 0)
        s.line([(pos[0], center_y-7), (pos[0], center_y+7)], MUTED, 2)
        s.text(pos[0], center_y+119, str(value), 30, MUTED, anchor="ma")
    # A real fixed spatial slice: only its complex vector rotates.
    phase = np.linspace(0, 2*math.pi, 181)
    # Stationary amplitude cylinder, present in the desktop source.
    for end_x in (0, 8):
        s.line(project(end_x, np.exp(1j*phase)), GRID, 2)
    for rim_z in (np.exp(.38j), -np.exp(.38j)):
        s.line([project(0, rim_z), project(8, rim_z)], GRID, 2)
    s.line(project(x0, np.exp(1j*phase)), MUTED, 2)
    s.line(project(x, z), BLUE, 5)
    p0 = project(x0, z0)
    s.arrow(project(x0, 0), p0, GOLD, 5, 17)
    s.dot(p0, 9, GOLD)
    for zz, label, color, label_x in ((1, "Re z", BLUE, 85),
                                     (1j, "Im z", RED, 235)):
        end = project(0, zz)
        s.arrow(project(0, 0), end, color, 3, 12)
        s.text(label_x, 646, label, 30, color)
    # Both scalar component plots use the same spatial coordinates as the helix.
    mid, amp = 1120., 70.
    xx = left+x/8*(right-left)
    s.line([(left, mid), (right, mid)], GRID, 2)
    s.line(np.c_[xx, mid-amp*z.real], BLUE, 4)
    s.line(np.c_[xx, mid-amp*z.imag], RED, 4)
    _dashed(s, (510, 1004), (510, 1204), GOLD, 2)
    s.dot((510, mid-amp*z0.real), 7, BLUE)
    s.dot((510, mid-amp*z0.imag), 7, RED)
    s.math(r"\cos(kx-\omega t)", x=285, y=1010, size=42, color=BLUE, maxwidth=390)
    s.math(r"\sin(kx-\omega t)", x=745, y=1010, size=42, color=RED, maxwidth=390)
    # Unit-circle dial of exactly the same selected complex value.
    center, radius = np.array([510., 1370.]), 112.
    s.d.ellipse((398, 1258, 622, 1482), outline=GRID, width=3)
    s.arrow((365, 1370), (665, 1370), MUTED, 2, 10)
    s.arrow((510, 1492), (510, 1228), MUTED, 2, 10)
    s.text(681, 1368, "Re", 31, MUTED)
    s.text(529, 1210, "Im", 31, MUTED)
    end = center + radius*np.array([z0.real, -z0.imag])
    _dashed(s, end, (end[0], center[1]), BLUE, 2)
    _dashed(s, end, (center[0], end[1]), RED, 2)
    real_end = np.array([end[0], center[1]])
    imag_end = np.array([center[0], end[1]])
    s.line([center, real_end], BLUE, 5)
    s.line([center, imag_end], RED, 5)
    s.dot(real_end, 6, BLUE)
    s.dot(imag_end, 6, RED)
    s.arrow(center, end, GOLD, 6, 18)
    s.dot(end, 8, GOLD)
    s.math(r"x_0=4", x=210, y=1320, size=45, color=GOLD, maxwidth=250)
    s.math(r"|z|=1", x=805, y=1455, size=47, color=GOLD, maxwidth=260)
    s.math(r"z(x-a,t)=e^{-ika}z(x,t)", y=1538, size=47)
    # One spatial period in the synchronized component plot, k=pi/2.
    xa, xb, y = 160, 510, 1215
    s.line([(xa,y),(xb,y)], MUTED, 2)
    for xx in (xa,xb):
        s.line([(xx,y-6),(xx,y+6)], MUTED, 2)
    s.math(r"\lambda=\frac{2\pi}{k}", x=(xa+xb)/2, y=1241, size=32, color=MUTED)
    return s.im


def render(number,t,entry):
    defaults=inventory(number)
    edited=entry.get('on_screen_text') or defaults
    if len(edited)!=len(defaults):
        raise ValueError(f'Reel {number}: keep the {len(defaults)} on-screen entries in order.')
    previous_replacements=dict(core.TEXT_REPLACEMENTS)
    core.TEXT_REPLACEMENTS.clear()
    core.TEXT_REPLACEMENTS.update(zip(defaults,edited))
    spec=SPECS[number-1]
    kind=spec['renderer']
    try:
        if kind in ('early','late'):
            frame=__import__(kind).render(spec.get('scene_number',number),t,entry)
        elif kind in ('casimir','lie_commutator'):
            frame=__import__(kind).render(t,entry)
        elif kind=='triangle':
            frame=reused(number,t,entry,2,24)
        elif kind=='carriers':
            frame=carriers(t,entry)
        elif kind=='wave':
            frame=wave(t,entry)
        else:
            old=int(kind.split(':')[1])
            if old==14:
                frame=__import__('eigenbasis').render(t,entry)
            elif old==15:
                frame=__import__('eigenfunctions').render(t,entry)
            else:
                frame=reused(number,t,entry,old,24 if old==4 else None)
        # Scientific renderers retain their original scene IDs. Only these
        # reserved strips express the reel's position in the current series.
        return core.apply_series_numbering(frame,number)
    finally:
        core.TEXT_REPLACEMENTS.clear()
        core.TEXT_REPLACEMENTS.update(previous_replacements)
