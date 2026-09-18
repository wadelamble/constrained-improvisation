"""Portrait reels 7–10: composition, interference, and dense path sums.

All coordinates are native portrait pixels.  Episode 10 imports the accepted
scalar-propagation model without modifying it or its earlier output assets.
"""
from core import *
from PIL import ImageColor

# The accepted propagation generators keep SciPy in this project-local bundle.
_SCIPY_BUNDLE = ROOT / '.tools' / 'tip-to-tail-corrected-python-packages'
if _SCIPY_BUNDLE.is_dir() and str(_SCIPY_BUNDLE) not in sys.path:
    sys.path.insert(0, str(_SCIPY_BUNDLE))


def _mix(a, b, f):
    aa = np.array(ImageColor.getrgb(a) if isinstance(a, str) else a)
    bb = np.array(ImageColor.getrgb(b) if isinstance(b, str) else b)
    return tuple(np.rint(aa * (1-f) + bb * f).astype(int))


def _dash(s, a, b, color=GRID, width=2, step=14):
    a, b = np.array(a, float), np.array(b, float)
    delta = b-a
    distance = np.linalg.norm(delta)
    if distance == 0:
        return
    for v in np.arange(0, distance, step):
        s.line([a+delta*v/distance, a+delta*min(v+step*.48, distance)/distance], color, width)


def _circle(s, p, radius, color=GRID, width=2):
    s.d.ellipse((p[0]-radius, p[1]-radius, p[0]+radius, p[1]+radius), outline=color, width=width)


def _route(s, a, c, b, color, progress=1., width=5):
    """Draw the same route on both sides of a sampling screen."""
    progress = np.clip(progress, 0, 1)
    if progress <= .5:
        s.line([a, np.array(a)+(np.array(c)-a)*progress*2], color, width)
    else:
        s.line([a, c, np.array(c)+(np.array(b)-c)*(progress*2-1)], color, width)


def _two_vectors(target_y):
    ys = np.array([1.5, -1.5])
    lengths = np.hypot(4.5, ys) + np.hypot(4.5, target_y-ys)
    return .5*np.exp(2j*np.pi*lengths/2.4)


def _target7(t):
    if t < 29:
        return .55
    if t < 34:
        return lerp(.55, -1.8, ease(window(t, 29, 34)))
    if t < 41:
        return lerp(-1.8, 1.8, ease(window(t, 34, 41)))
    return lerp(1.8, .55, ease(window(t, 41, 44)))


def render7(t):
    duration = 45
    if t < 14:
        stage = 'First route: A → C → B'
    elif t < 23:
        stage = 'Second route: A → D → B'
    else:
        stage = 'Add the two complex contributions'
    s = Scene(7, EPISODES[7].get('video_title', EPISODES[7]['title']), stage, t, duration)
    s.panel((70, 480, 950, 960), 'Two candidate routes')
    ay, cy, dy = 745., 640., 850.
    target_y = _target7(t)
    a, c, d, b = (185., ay), (500., cy), (500., dy), (815., ay-70*target_y)
    # Equal physical scale in x and y: 70 pixels per geometric length unit.
    for y0, y1 in ((570, cy-11), (cy+11, dy-11), (dy+11, 905)):
        s.line([(500, y0), (500, y1)], MUTED, 7)
    _dash(s, a, (815, ay))
    _route(s, a, c, b, _mix(BLUE, PANEL, .62), width=3)
    _route(s, a, d, b, _mix(RED, PANEL, .62), width=3)
    if t < 14:
        active = 0
        u1, u2 = ease(window(t, 3, 8)), ease(window(t, 8, 13))
        _route(s, a, c, b, BLUE, .5*(u1+u2))
    elif t < 23:
        active = 1
        u1, u2 = ease(window(t, 14, 18)), ease(window(t, 18, 22))
        _route(s, a, c, b, BLUE, 1., 3)
        _route(s, a, d, b, RED, .5*(u1+u2))
    else:
        _route(s, a, c, b, BLUE)
        _route(s, a, d, b, RED)
    for point, label, color, offset in ((a, 'A', INK, (-20, 24)), (b, 'B', GREEN, (12, 18)),
                                        (c, 'C', BLUE, (17, -45)), (d, 'D', RED, (17, 15))):
        s.dot(point, 8, color)
        s.text(point[0]+offset[0], point[1]+offset[1], label, 36, color, bold=True)
    s.text(500, 914, 'screen', 30, MUTED, anchor='ma')
    if t < 23:
        name, mid_y, color = ('C', 1.5, BLUE) if active == 0 else ('D', -1.5, RED)
        s.panel((70, 990, 950, 1430), 'Phase factors multiply')
        r1, r2 = np.hypot(4.5, mid_y), np.hypot(4.5, target_y-mid_y)
        theta1, theta2 = 2*np.pi*r1/2.4*u1, 2*np.pi*r2/2.4*u2
        for origin, z, label in (((220, 1230), np.exp(1j*theta1), 'A'+name),
                                 ((510, 1230), np.exp(1j*theta2), name+'B'),
                                 ((800, 1230), np.exp(1j*(theta1+theta2)), 'A'+name+'B')):
            _circle(s, origin, 94)
            _dash(s, (origin[0]-98, origin[1]), (origin[0]+98, origin[1]))
            phasor(s, origin, z, 87, color, 5)
            s.text(origin[0], 1354, label, 32, color, anchor='ma')
        s.text(365, 1200, '×', 45, INK, anchor='ma')
        s.text(655, 1200, '=', 45, INK, anchor='ma')
        s.math(r'e^{ik\ell_{A'+name+r'}}e^{ik\ell_{'+name+r'B}}=e^{ik(\ell_{A'+name+r'}+\ell_{'+name+r'B})}', y=1500, size=43)
        s.note('The segment phases add in the exponent.')
    else:
        s.panel((70, 990, 950, 1430), 'The two route amplitudes add')
        q = _two_vectors(target_y)
        origin, scale = (500., 1222.), 158.
        _circle(s, origin, scale, GRID)
        _dash(s, (305, 1222), (695, 1222))
        first = phasor(s, origin, q[0], scale, BLUE, 6)
        end = phasor(s, first, q[1], scale, RED, 6)
        phasor(s, origin, q.sum(), scale, GREEN, 7)
        s.text(105, 1372, 'ACB', 30, BLUE)
        s.text(243, 1372, 'ADB', 30, RED)
        s.text(915, 1372, 'sum at B', 30, GREEN, anchor='ra')
        s.math(r'\Psi_B=\Psi_{ACB}+\Psi_{ADB}', y=1500, size=49)
        s.note('Move B: both lengths and both phases change.')
    return s.im


_MANY_Y = np.linspace(2.8, -2.8, 17)
_DETECTOR_Y = np.linspace(-3.15, 3.15, 321)


def _many_vectors(target_y):
    target = np.asarray(target_y)
    lengths = np.hypot(4.5, _MANY_Y) + np.hypot(4.5, target[..., None]-_MANY_Y)
    # One fixed phase reference is common to every route and target.
    return np.exp(2j*np.pi*(lengths-9)/.62)/len(_MANY_Y)


@lru_cache(None)
def _many_model():
    vectors = _many_vectors(_DETECTOR_Y)
    prefixes = np.c_[np.zeros(len(_DETECTOR_Y), complex), np.cumsum(vectors, axis=1)]
    xr = (prefixes.real.min(), prefixes.real.max())
    yr = (prefixes.imag.min(), prefixes.imag.max())
    scale = min(730/(xr[1]-xr[0]), 260/(yr[1]-yr[0]))
    origin = (510-scale*(xr[0]+xr[1])/2, 1225+scale*(yr[0]+yr[1])/2)
    intensity = np.abs(prefixes[:, -1])**2
    return vectors, prefixes, scale, origin, intensity, float((abs(prefixes)**2).max())


def _target8(t):
    if t < 19:
        return .65
    if t < 24:
        return lerp(.65, -2.9, ease(window(t, 19, 24)))
    if t < 39:
        return lerp(-2.9, 2.9, ease(window(t, 24, 39)))
    return lerp(2.9, 0., ease(window(t, 39, 44)))


def render8(t):
    duration = 45
    count = min(17, 2+int(15*window(t, 3, 15)))
    by = _target8(t)
    vectors, prefixes, scale, origin, intensity, imax = _many_model()
    stage = 'Add more openings' if t < 17 else 'Move the observation point along the detector'
    s = Scene(8, EPISODES[8].get('video_title', EPISODES[8]['title']), stage, t, duration)
    s.panel((70, 480, 950, 930), 'Geometry and detector intensity')
    a, b, screen_x, middle = (205., 710.), (655., 710.-50*by), 430., 710.
    _dash(s, (180, middle), (710, middle))
    s.line([(screen_x, 550), (screen_x, 870)], GRID, 6)
    for j, yy in enumerate(_MANY_Y):
        p = (screen_x, middle-50*yy)
        color = spectrum_color(j/16)
        s.d.rectangle((screen_x-7, p[1]-4, screen_x+7, p[1]+4), fill=PANEL)
        if j < count:
            _route(s, a, p, b, _mix(color, PANEL, .3), width=2)
            s.dot(p, 4, color)
    s.line([(655, 545), (655, 875)], MUTED, 3)
    s.dot(a, 8, INK)
    s.dot(b, 8, GREEN)
    s.text(a[0]-12, a[1]+25, 'A', 35, INK)
    s.text(b[0]+15, b[1]-17, 'B', 35, GREEN)
    s.text(430, 881, 'screen', 30, MUTED, anchor='ma')
    s.text(900, 545, 'I', 34, GREEN, anchor='ra')
    active_intensity = np.abs(prefixes[:, count])**2
    # The profile and the selected marker both use the same current sum.
    profile_x = 746 + 154*active_intensity/imax
    profile_y = middle - 50*_DETECTOR_Y
    s.line(np.c_[profile_x, profile_y], GREEN, 4)
    s.line([(746, 550), (746, 868)], GRID, 2)
    q = _many_vectors(by)[:count]
    value = q.sum()
    selected_i = abs(value)**2
    _dash(s, b, (746+154*selected_i/imax, b[1]), _mix(GREEN, PANEL, .4), 2)
    s.dot((746+154*selected_i/imax, b[1]), 7, GREEN)
    s.panel((70, 958, 950, 1430), 'Add the same contributions tip to tail')
    s.text(914, 1030, f'{count} openings', 30, MUTED, anchor='ra')
    for j, z in enumerate(q):
        start = sum(q[:j])
        point = (origin[0]+scale*start.real, origin[1]-scale*start.imag)
        phasor(s, point, z, scale, spectrum_color(j/16), 4)
    phasor(s, origin, value, scale, GREEN, 7)
    s.dot(origin, 5, MUTED)
    s.text(105, 1373, 'Colored arrows: routes', 30, MUTED)
    s.text(914, 1373, 'Green: Ψ(B)', 30, GREEN, anchor='ra')
    s.math(r'\Psi(B)=\sum_j\Psi_j(B),\qquad I(B)=|\Psi(B)|^2', y=1500, size=43)
    s.note('The intensity comes from this exact complex sum.')
    return s.im


# Episode 9 uses an angular-spectrum solution of the scalar Helmholtz equation.
# A wide periodic transverse domain keeps the visible crop away from its seam.
# Dense screens become the transparent continuum before more planes are added.
_HUYGENS_LAMBDA = 1.2
_HUYGENS_PERIOD = 24.
_HUYGENS_N = 512
_HUYGENS_Y = np.linspace(-12, 12, _HUYGENS_N, endpoint=False)
_HUYGENS_Z = np.linspace(.035, 8.2, 232)
_HUYGENS_CROP = np.flatnonzero(abs(_HUYGENS_Y) <= 4.65)


@lru_cache(None)
def _huygens_model():
    k = 2*np.pi/_HUYGENS_LAMBDA
    q = 2*np.pi*np.fft.fftfreq(_HUYGENS_N, d=_HUYGENS_PERIOD/_HUYGENS_N)
    kz = np.sqrt((k*k-q*q).astype(complex))
    transfer = np.exp(1j*_HUYGENS_Z[:, None]*kz)
    masks = []
    for number, fill in ((3, .18), (9, .34), (27, .70)):
        centers = np.linspace(-10, 10, number)
        spacing = 20/max(number-1, 1)
        width = min(.55 if number == 3 else 1.2, spacing*fill)
        dist = np.min(abs(_HUYGENS_Y[:, None]-centers), axis=1)
        mask = (dist <= width/2).astype(float)
        masks.append(mask)
    masks.append(np.ones(_HUYGENS_N))
    fields = [np.fft.ifft(np.fft.fft(mask)[None, :]*transfer, axis=1) for mask in masks]
    return masks, fields, kz


def _huygens_state(t):
    if t < 5:
        return 0, 0, 0.
    if t < 9:
        return 0, 1, float(ease(window(t, 5, 9)))
    if t < 11:
        return 1, 1, 0.
    if t < 15:
        return 1, 2, float(ease(window(t, 11, 15)))
    if t < 17:
        return 2, 2, 0.
    if t < 22:
        return 2, 3, float(ease(window(t, 17, 22)))
    return 3, 3, 0.


_CONTOUR_EDGES = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
    5: ((3, 0), (1, 2)), 6: ((0, 2),), 7: ((3, 2),),
    8: ((2, 3),), 9: ((0, 2),), 10: ((0, 1), (2, 3)),
    11: ((1, 2),), 12: ((1, 3),), 13: ((0, 1),), 14: ((3, 0),),
}


def _field_fronts(s, field, phase, x0=227.5, y0=993., pixels_per_unit=72.5):
    """Marching squares on Im(psi exp(-i omega t))=0, Re>0.

    The gold curves are therefore actual equal-phase fronts of the displayed
    scalar solution, rather than circular fronts being manually straightened.
    """
    value = field[:, _HUYGENS_CROP]*np.exp(-1j*phase)
    yy = _HUYGENS_Y[_HUYGENS_CROP]
    f = value.imag
    corners = (f[:-1, :-1], f[1:, :-1], f[1:, 1:], f[:-1, 1:])
    case = sum((v > 0).astype(np.uint8)*(1 << j) for j, v in enumerate(corners))
    realmean = (value.real[:-1, :-1]+value.real[1:, :-1]+value.real[1:, 1:]+value.real[:-1, 1:])/4
    dz, dy = np.diff(_HUYGENS_Z)[0], np.diff(yy)[0]
    edge_corners = ((0, 1), (1, 2), (2, 3), (3, 0))
    offsets = np.array(((0., 0.), (1., 0.), (1., 1.), (0., 1.)))
    for code, pairs in _CONTOUR_EDGES.items():
        rows, cols = np.where((case == code) & (realmean > .045))
        if len(rows) == 0:
            continue
        for e1, e2 in pairs:
            points = []
            for edge in (e1, e2):
                a, b = edge_corners[edge]
                va, vb = corners[a][rows, cols], corners[b][rows, cols]
                u = va/(va-vb)
                xy = offsets[a]+u[:, None]*(offsets[b]-offsets[a])
                xx = x0+pixels_per_unit*(_HUYGENS_Z[rows]+dz*xy[:, 0])
                sy = y0-pixels_per_unit*(yy[cols]+dy*xy[:, 1])
                points.append(np.c_[xx, sy])
            for a, b in zip(*points):
                s.line((a, b), GOLD, 3)


@lru_cache(None)
def _wavelet_phase_table():
    from scipy.special import hankel1
    rr = np.linspace(.04, 12, 8000)
    phase = np.unwrap(np.angle(1j*hankel1(1, 2*np.pi*rr/_HUYGENS_LAMBDA)))
    return rr, phase


def _wavelets(s, screen_z, centers, phase, end_z, color=BLUE):
    """True kernel phase contours: arg(i H1(k r)) + incident phase."""
    rr, phases = _wavelet_phase_table()
    incident = 2*np.pi*(screen_z-1.5)/_HUYGENS_LAMBDA
    targets = np.arange(-10, 20)*2*np.pi+phase-incident
    radii = np.interp(targets[(targets > phases[0]) & (targets < phases[-1])], phases, rr)
    xx = np.linspace(screen_z+.045, end_z, 135)
    for cy in centers:
        for radius in radii:
            valid_x = xx[(xx-screen_z) < radius]
            if len(valid_x) < 2:
                continue
            off = np.sqrt(np.maximum(0, radius**2-(valid_x-screen_z)**2))
            for sign in (-1, 1):
                yy = cy+sign*off
                valid = abs(yy) < 4.65
                if valid.sum() >= 2:
                    s.line(np.c_[118.75+72.5*valid_x[valid], 993-72.5*yy[valid]], color, 2)


def render9(t):
    duration = 48
    if t < 17:
        stage = 'More openings supply more secondary waves'
    elif t < 26:
        stage = 'Let the transmitting plane become continuous'
    else:
        stage = 'Insert more already continuous planes'
    s = Scene(9, EPISODES[9].get('video_title', EPISODES[9]['title']), stage, t, duration)
    s.panel((70, 480, 950, 1430), 'Blue: component fronts', BLUE)
    s.text(94, 548, 'Gold: fronts of the complex sum', 30, GOLD)
    masks, fields, kz = _huygens_model()
    lo, hi, blend = _huygens_state(t)
    mask = lerp(masks[lo], masks[hi], blend)
    field = lerp(fields[lo], fields[hi], blend)
    phase = 2*np.pi*(t-1.0)/4.8
    # Incoming plane fronts have the same phase reference as the screen field.
    wave_x = 1.5+(phase+2*np.pi*np.arange(-15, 15))/(2*np.pi/_HUYGENS_LAMBDA)
    for xx in wave_x[(wave_x >= 0) & (wave_x < 1.5)]:
        s.line([(118.75+72.5*xx, 656), (118.75+72.5*xx, 1330)], GOLD, 3)
    screens = [1.5]
    if t >= 28:
        screens.append(4.15)
    if t >= 36:
        screens.append(6.8)
    # Component wavelets are selected terms of the same continuum construction.
    # Their fronts are clipped at the next integration plane for legibility.
    if lo == 0 and hi == 0:
        centers = [0.]
    elif hi == 1 or (lo == 1 and hi == 1):
        centers = [-2.5, 0., 2.5]
    else:
        available = np.linspace(-10, 10, 27)
        centers = available[abs(available) <= 4.65][::2]
    dim_blue = _mix(BLUE, PANEL, .49)
    for j, zz in enumerate(screens):
        end = screens[j+1] if j+1 < len(screens) else 9.65
        _wavelets(s, zz, centers, phase, end, dim_blue)
    _field_fronts(s, field, phase)
    for i, zz in enumerate(screens):
        xp = 118.75+72.5*zz
        if lo < 3 and i == 0:
            for index in _HUYGENS_CROP:
                yy = 993-72.5*_HUYGENS_Y[index]
                color = _mix(MUTED, PANEL, float(mask[index]))
                s.line([(xp, yy-1.9), (xp, yy+1.9)], color, 5)
        else:
            _dash(s, (xp, 647), (xp, 1338), MUTED, 2, 12)
        s.text(xp, 1350, str(i+1), 30, MUTED, anchor='ma')
        for cy in centers:
            s.dot((xp, 993-72.5*cy), 4, BLUE)
    if lo == 3:
        s.math(r'K(z_2)K(z_1)\psi=K(z_1+z_2)\psi', y=1500, size=44)
        s.note('Continuous transparent planes leave free propagation unchanged.')
    else:
        s.math(r'\Psi(z,y)=\int K(z,y-y^\prime)\Psi(0,y^\prime)\,dy^\prime', y=1500, size=40)
        s.note('A scalar-wave construction; the gold fronts follow the sum.')
    return s.im


@lru_cache(None)
def _accepted():
    import importlib
    scripts_path = str(ROOT / 'scripts')
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    physical = importlib.import_module('generate_symmetry_normalized_path_diamond')
    spectrum = importlib.import_module('generate_symmetry_spectrum_path_diamond')
    return physical, spectrum


_DIAMOND_A, _DIAMOND_B = (150., 762.), (870., 762.)
_DIAMOND_SCREEN, _DIAMOND_HALF = 510., 160.
_TRACE_ORIGIN, _TRACE_SCALE = (255., 1245.), 430.


@lru_cache(None)
def _diamond_raster():
    physical, spectrum = _accepted()
    left, top, right, bottom = 150, 602, 870, 923
    xx = np.arange(left, right+1)[None, :].astype(float)
    yy = np.arange(top, bottom+1)[:, None].astype(float)
    spread = np.where(xx <= _DIAMOND_SCREEN,
                      (xx-_DIAMOND_A[0])/(_DIAMOND_SCREEN-_DIAMOND_A[0]),
                      (_DIAMOND_B[0]-xx)/(_DIAMOND_B[0]-_DIAMOND_SCREEN))
    crossing_y = -((yy-762)/np.maximum(spread, 1e-12))*physical.HALF_EXTENT/_DIAMOND_HALF
    valid = (abs(crossing_y) <= physical.HALF_EXTENT) & (spread > 0)
    indices = np.clip(np.rint((physical.HALF_EXTENT-crossing_y)/physical.DY-.5), 0, physical.N-1).astype(int)
    indices[~valid] = -1
    rgb = spectrum.COLORS[np.maximum(indices, 0)].astype(float)
    paper = np.array(ImageColor.getrgb(PANEL), float)
    faint = np.rint(.14*rgb+.86*paper).astype(np.uint8)
    painted = np.rint(.70*rgb+.30*paper).astype(np.uint8)
    faint[~valid] = paper
    painted[~valid] = paper
    return (left, top), indices, Image.fromarray(faint), Image.fromarray(painted)


@lru_cache(None)
def _diamond_trace(stage):
    physical, spectrum = _accepted()
    vertices = physical.model(stage)[2]
    coords = np.c_[_TRACE_ORIGIN[0]+_TRACE_SCALE*vertices.real,
                   _TRACE_ORIGIN[1]-_TRACE_SCALE*vertices.imag]
    return vertices, coords, [tuple(p) for p in coords]


def _diamond_state(t):
    stage = min(2, max(0, int(t//15)))
    local = min(15., max(0., t-stage*15))
    physical, _ = _accepted()
    return stage, min(physical.N, max(0, round(physical.N*window(local, 1, 12.5))))


def render10(t):
    physical, spectrum = _accepted()
    stage, count = _diamond_state(t)
    label = ('λ = λ₀', 'λ = λ₀ / 10', 'λ = λ₀ / 100')[stage]
    s = Scene(10, EPISODES[10].get('video_title', EPISODES[10]['title']), label, t, 45)
    s.panel((70, 480, 950, 983), 'Path position fixes the color')
    origin, indices, faint, painted = _diamond_raster()
    s.im.paste(faint, origin)
    if count:
        mask = Image.fromarray(((indices >= 0) & (indices < count)).astype(np.uint8)*255)
        s.im.paste(painted, origin, mask)
    s.d = ImageDraw.Draw(s.im)
    _dash(s, _DIAMOND_A, _DIAMOND_B, _mix(MUTED, PANEL, .35))
    for yy in np.linspace(-physical.HALF_EXTENT, physical.HALF_EXTENT, 107):
        color = tuple(map(int, spectrum.color_at(yy)))
        p = (_DIAMOND_SCREEN, 762-_DIAMOND_HALF*yy/physical.HALF_EXTENT)
        s.dot(p, 2, color)
    if 0 < count < physical.N:
        yy = physical.Y[count-1]
        p = (_DIAMOND_SCREEN, 762-_DIAMOND_HALF*yy/physical.HALF_EXTENT)
        color = spectrum.RGB[count-1]
        s.line([_DIAMOND_A, p, _DIAMOND_B], color, 4)
        s.dot(p, 6, color)
    for p, label2 in ((_DIAMOND_A, 'A'), (_DIAMOND_B, 'B')):
        s.dot(p, 7, INK)
        s.text(p[0], p[1]+21, label2, 35, INK, anchor='ma')
    s.text(95, 939, f'{count:,} / 20,001', 30, MUTED)
    s.text(920, 939, 'fixed paths', 30, MUTED, anchor='ra')
    s.panel((70, 1003, 950, 1430), 'Ungrouped phasors')
    s.text(920, 1060, 'Gold: sum so far', 30, GOLD, anchor='ra')
    vertices, coords, raster = _diamond_trace(stage)
    _dash(s, (113, _TRACE_ORIGIN[1]), (887, _TRACE_ORIGIN[1]), GRID)
    reference = (_TRACE_ORIGIN[0]+_TRACE_SCALE, _TRACE_ORIGIN[1])
    _circle(s, reference, 6, MUTED, 2)
    if count:
        for first, last in zip(spectrum.COLOR_CUTS[:-1], spectrum.COLOR_CUTS[1:]):
            if first >= count:
                break
            end = min(int(last), count)
            s.d.line(raster[int(first):end+1], fill=spectrum.RGB[int(first)], width=3)
        s.arrow(_TRACE_ORIGIN, coords[count], GOLD, 5, 13)
        s.dot(coords[count], 5, GOLD)
        if count < physical.N:
            _circle(s, coords[count], 10, spectrum.RGB[count-1], 3)
    s.dot(_TRACE_ORIGIN, 4, MUTED)
    s.text(95, 1375, 'Free-field reference = 1', 30, MUTED)
    s.math(r'\Psi_B/\Psi_{\rm free}=\sum_j v_j', y=1500, size=48)
    s.note('Same paths, phase reference, and display scale.')
    return s.im


def validate():
    """Numerical checks for the relationships actually drawn in these reels."""
    import hashlib
    report = {}
    q = _two_vectors(.55)
    ys = np.array([1.5, -1.5])
    factors = .5*np.exp(2j*np.pi*np.hypot(4.5, ys)/2.4)*np.exp(2j*np.pi*np.hypot(4.5, .55-ys)/2.4)
    assert np.max(abs(q-factors)) < 1e-14
    report['7'] = {'multiplication_error': float(np.max(abs(q-factors))), 'route_magnitudes': abs(q).tolist()}
    vectors, prefixes, scale, origin, intensity, imax = _many_model()
    err = float(np.max(abs(intensity-abs(vectors.sum(axis=1))**2)))
    assert err < 1e-14
    # Include all intermediate sums: the intensity panel uses the same subset.
    for n in range(1, 18):
        assert np.max(abs(prefixes[:, n]-vectors[:, :n].sum(axis=1))) < 1e-14
    report['8'] = {'intensity_sum_error': err, 'fixed_phasor_scale': scale, 'fixed_origin': list(origin),
                   'maximum_detector_intensity': imax, 'slits': 17}
    masks, fields, kz = _huygens_model()
    plane = np.exp(2j*np.pi*_HUYGENS_Z/_HUYGENS_LAMBDA)[:, None]
    plane_error = float(np.max(abs(fields[-1]-plane)))
    transfer_error = float(np.max(abs(np.exp(1j*kz*2.65)**2-np.exp(1j*kz*5.3))))
    assert plane_error < 1e-12 and transfer_error < 1e-12
    report['9'] = {'plane_front_error': plane_error, 'transparent_plane_composition_error': transfer_error,
                   'field_model': 'scalar Helmholtz angular spectrum; evanescent terms retained',
                   'periodic_transverse_span': _HUYGENS_PERIOD,
                   'continuous_screen_reached_before_adding_planes': True,
                   'gold_fronts': 'Im(field exp(-i phase)) = 0 with Re > 0',
                   'blue_fronts': 'constant arg(i H1(k r)) of selected scalar propagation kernels'}
    physical, spectrum = _accepted()
    stages = []
    for stage in range(3):
        _, vec, vertices, _, _ = physical.model(stage)
        p = _diamond_trace(stage)[1]
        assert len(vec) == 20001 and len(p) == 20002
        assert max(abs(np.diff(vertices)-vec)) < 3e-16
        assert p[:, 0].min() > 100 and p[:, 0].max() < 915
        assert p[:, 1].min() > 1090 and p[:, 1].max() < 1370
        stages.append({'wavelength': physical.WAVELENGTHS[stage],
                       'vectors_sha256': hashlib.sha256(vec.tobytes()).hexdigest(),
                       'endpoint': [vertices[-1].real, vertices[-1].imag],
                       'trace_pixel_bounds': [p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]})
    report['10'] = {'same_original_model': True, 'segments': physical.N, 'fixed_display_scale': _TRACE_SCALE,
                    'grouped_segments': False, 'endpoint_normalization': False, 'stages': stages}
    return report


EPISODES = {
    7: {
        'title': 'Compose symmetry operators along a route. Add amplitudes across candidate routes.', 'duration': 45, 'render': render7,
        'checkpoints': [5, 12.5, 20.5, 27, 34, 39.5, 44],
        'caption': '7/13 — A phase factor belongs to each segment of a route. For a monochromatic wave, the spatial part is exp(ikℓ): wave number times length gives the phase angle. Along A→C→B, the two factors multiply, so their angles add. The same calculation gives the contribution along A→D→B. The contributions from the two routes then add as complex numbers. These are two different operations: multiplication along a route, addition across routes. The first part follows the two segment factors and their product; the final part places the complete route amplitudes tip to tail. Moving B changes the geometric lengths and therefore the displayed phases. Equal route magnitudes isolate the phase effect in this example. A common source and observation-time phase has been suppressed. Next: more openings, and the intensity obtained from their sum.',
        'validation': {'geometry_drives_phase': True, 'route_amplitude': .5, 'wavelength': 2.4},
    },
    8: {
        'title': 'The emergence of stationary paths', 'duration': 45, 'render': render8,
        'checkpoints': [3, 10, 16, 24, 31.5, 38.5, 44],
        'caption': '8/13 — Add more openings and the rule stays the same. Each colored route supplies a complex contribution at the selected point B. The lower panel adds those contributions tip to tail; the green arrow is their sum. The detector profile is computed from that same sum at every detector position, then squared in magnitude. Its moving marker uses exactly the amplitudes drawn below. Contributions can oppose one another or reinforce one another as their relative phases change. This example gives all seventeen openings equal weights and uses their geometric lengths to determine phase; the overall scale remains fixed throughout. The colored routes label terms in a wave calculation, not observed particle trajectories. More openings create a more detailed sum, not a new rule. Next: let a transmitting plane become continuous and follow the secondary wavelets.',
        'validation': {'slits': 17, 'intensity_from_identical_sum': True, 'all_prefixes_preserved': True},
    },
    9: {
        'title': 'Huygens’ principle -- path formulation in the continuous limit', 'duration': 48, 'render': render9,
        'checkpoints': [3, 9.5, 16, 23.5, 31, 39, 47],
        'caption': '9/13 — A transmitting plane can be used as a new source of secondary waves. The blue curves show selected component wavefronts; the gold curves follow the phase of their complex sum. Begin with separated openings, increase their density, and then pass to a fully transmitting continuum. Only after that limit is reached do additional continuous planes enter. A plane wave remains a plane wave because free propagation composes consistently across these intermediate planes. This is a scalar Helmholtz construction, computed with an angular-spectrum propagator on a wide periodic transverse domain. The blue fronts use the corresponding cylindrical propagation kernel; the gold fronts are extracted from the calculated field. A finite set of displayed wavelets is not being declared an exact plane wave. The final planes represent the continuum integral. Next: inspect how individual path contributions change as wavelength decreases.',
        'validation': {'scalar_angular_spectrum': True, 'gold_fronts_from_computed_field': True,
                       'continuum_before_more_planes': True},
    },
    10: {
        'title': 'Converging on the stationary path in the short wavelength limit', 'duration': 45, 'render': render10,
        'checkpoints': [3.9, 6.6, 6.9, 13.5, 18.9, 21.6, 21.9, 28.5, 33.9, 36.6, 36.9, 44],
        'caption': '10/13 — Keep the source, observation point, and 20,001 sampled routes fixed. Repeat the sum at three wavelengths. Each route has the same color as its individual segment in the phasor chain, so the central red paths and outer blue paths can be located in both panels. Shorter wavelength makes phase vary more rapidly away from the straight route. Those contributions wind into loops; near the stationary route, the chain makes a more coherent advance. Every segment remains in the sum. This uses the established scalar propagation model, including source and propagation weights, divided by an independently specified unobstructed field. The finite-aperture endpoint is not forced to one. All three passes use one display scale and phase reference. The painted diamond marks the routes already included, not intensity or probability. Next: the additional physical interpretation supplied by quantum mechanics.',
        'validation': {'accepted_model': 'generate_symmetry_normalized_path_diamond.py', 'path_count': 20001,
                       'no_grouping': True, 'wavelengths': [.5, .05, .005], 'fixed_scale': _TRACE_SCALE},
    },
}

# Post copy is separate from the numerical production notes above.
EPISODES[7]['caption'] = 'Along a route, phase-shift operators compose, or multiply, stitching each straight line segment to the next. Across routes, complex amplitudes add.\n\nFor a monochromatic wave, a segment of length ℓ accumulates phase Δφ = kℓ. Following A→C→B means multiplying the factors for AC and CB. Multiplication adds their angles: exp(ikℓAC) exp(ikℓCB) = exp[ik(ℓAC + ℓCB)]. The three little clocks show the two factors and their product. Repeat the calculation through D.\n\nWe now have two contributions at B: ψ₁ from ACB and ψ₂ from ADB. Draw one after the other, tip to tail. The green arrow that joins the beginning to the end is their complex sum, ψ(B) = ψ₁ + ψ₂. As B moves, the route lengths change and the arrows turn accordingly. We give the two route contributions equal magnitudes to isolate the phase effect.'
EPISODES[8]['caption'] = 'With a larger number of openings, we see a pattern emerge. Near the straight path to B, neighboring paths accumulate nearly the same phase, so their contributions reinforce one another. Farther away, the phases change more rapidly and the contributions tend to cancel.\n\nEach colored route supplies a complex arrow at the selected point B. The lower panel adds those arrows tip to tail. The green arrow is their sum: ψ(B) = ψ₁ + ψ₂ + … + ψ₁₇. Its squared length gives the intensity, I(B) = |ψ(B)|². Repeating the calculation across the detector produces the green intensity profile above.\n\nMove B and the route lengths change. The arrows turn, some reinforce, others cancel, and the detector intensity changes with them. Both pictures come from the same calculation.\n\nThis example uses seventeen idealized narrow openings with equal contribution magnitudes. Their geometric lengths determine their phases. The display scale stays fixed, so a larger green arrow represents a larger amplitude. Each drawn route identifies a term in the wave calculation.'
EPISODES[9]['caption'] = 'A plane wave reaches a screen. Each opening contributes secondary waves. The blue arcs show some of their fronts, while gold follows the fronts of their complex sum.\n\nIncrease the openings until the transmitting plane becomes continuous. The original plane wave returns. We can then insert another continuous plane, and another, and so on. The wavelets recombine at every step. Each plane gives us a new way to calculate the same propagation.\n\nWriting K(z) for propagation through distance z, the wave changes as ψ_z = K(z)ψ₀. The composition rule K(z₁ + z₂) = K(z₂)K(z₁) says that splitting a distance into successive steps leaves the result unchanged. The added planes represent this continuous construction. The blue arcs are selected components, and the gold fronts come from the full calculated field.\n\nThis is the essence of Huygens’ principle and Feynman’s path integral formulation of quantum mechanics. The amplitude at a point is the sum of contributions from all possible paths leading to it.'
EPISODES[10]['caption'] = 'The transition from waves to rays in the short wavelength limit occurs as the net amplitude comes from an increasingly narrow range of paths around the stationary path.\n\nWatch which colors move the sum forward.\n\nThe source, target, and 20,001 sampled routes stay fixed. Each route has the same color as its individual segment in the tip-to-tail chain. Repeat the sum at three progressively shorter wavelengths.\n\nA path of length L accumulates phase φ(L) = 2πL/λ. Full turns bring an arrow back to the same orientation, while its final direction depends on the remainder. For nearby routes, Δφ = 2πΔL/λ. Shorter wavelengths make that direction vary faster as the route changes.\n\nThe outer paths wind into loops. Near the straight, stationary route, neighboring contributions point more nearly together and carry the sum forward. As wavelength shrinks, that coherent advance comes from a narrower range of routes. The color correspondence makes it visible.\n\nEvery contribution is retained, with its propagation weight. The fixed reference at 1 is unobstructed propagation, and all three passes use the same scale.'


if __name__ == '__main__':
    import json
    print(json.dumps(validate(), indent=2))
