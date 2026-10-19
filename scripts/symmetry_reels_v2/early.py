"""Faithful portrait reconstructions of the early manuscript visuals.

Every scene is a pure function of time.  Original manuscript assets and the
first reel series remain read-only.  D3 and surface geometry reuse their
desktop mathematical definitions; only the projection layout is adapted.
"""
from __future__ import annotations

from core import *
import importlib.util


SCREEN_TEXT = {
    4: ['Vertex labels', 'Ordered components', 'A', 'B', 'C'],
    6: ['Equal-components axis', 'Rotation', 'Reflection', 'Reflection plane',
        'v₁', 'v₂', 'v₃', r'R^3=I', r'S^2=I'],
    9: ['SO(2): rotation', 'Translation', r'\theta\in\mathbb{R}',
        r'a\in\mathbb{R}', r'R(\theta)', r'T(a)'],
    10: ['Curved surface', 'Tangent plane', 'Two independent tangent directions',
         r'\mathbf{e}_1', r'\mathbf{e}_2'],
    12: ['One state', 'Every state', 'Flow', 'Tangent',
         r'J(x,y)=(-y,x)', r'\mathbf{v}(\theta)=e^{\theta J}\mathbf{v}(0)',
         'x', 'y'],
}


def faded(color, alpha, background=PANEL):
    """Opaque color mixed into its actual drawing background."""
    alpha = float(np.clip(alpha, 0, 1))
    foreground = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    base = tuple(int(background[i:i+2], 16) for i in (1, 3, 5))
    return tuple(round(a+(b-a)*alpha) for a, b in zip(base, foreground))


@lru_cache(3)
def source_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def d3_geometry():
    return source_module('early_d3_geometry', 'symmetry_d3_rendering.py')


def surface_geometry():
    return source_module('early_surface_geometry', 'generate_tangent_plane_surface_diagram.py')


def ring(scene, center, radius, color=GRID, width=3):
    a = np.linspace(0, 2*np.pi, 181)
    scene.line(np.asarray(center)+np.c_[np.cos(a), -np.sin(a)]*radius, color, width)


def cubic(a, b, c, d, progress):
    p = progress
    return (1-p)**3*np.array(a)+3*(1-p)**2*p*np.array(b)+3*(1-p)*p*p*np.array(c)+p**3*np.array(d)


def vertices_scene(t, entry):
    duration = entry['duration']
    time = t*22/duration
    scene = Scene(4, entry['title'], '', t, duration)
    scene.panel((70, 480, 950, 1510))
    scene.text(110, 520, SCREEN_TEXT[4][0], 32, MUTED)
    center = np.array([510., 750.])
    angles = np.deg2rad([90, 210, 330])
    points = center+np.c_[np.cos(angles), -np.sin(angles)]*190
    scene.line(np.vstack([points, points[0]]), INK, 5)
    colors = [BLUE, GOLD, RED]
    label_offsets = [(0, -37), (-35, 27), (35, 27)]
    for index, point in enumerate(points):
        scene.dot(point, 9, colors[index])
        label_point = point+label_offsets[index]
        scene.text(*label_point, SCREEN_TEXT[4][index+2], 44, colors[index], True, 'mm')

    # The source's explicit triangle -> column arrow remains visible.  Each
    # colored label is copied from its vertex into the corresponding row.
    scene.arrow((510, 932), (510, 1030), MUTED, 4, 17)
    scene.text(510, 1084, SCREEN_TEXT[4][1], 32, MUTED, anchor='mm')
    rows = [1190, 1290, 1390]
    for edge, sign in ((448, 1), (572, -1)):
        scene.line([(edge+sign*16, 1140), (edge, 1140),
                    (edge, 1440), (edge+sign*16, 1440)], INK, 4)
    for index, (point, row) in enumerate(zip(points, rows)):
        start_time = 2+4.4*index
        p = float(ease(window(time, start_time, start_time+2.8)))
        if time < start_time:
            scene.dot((510, row), 3, GRID)
            continue
        start = point+label_offsets[index]
        # Broad outside paths keep the moving glyph separate from the
        # triangle edges, down-arrow and completed column entries.
        controls = [((70, 560), (150, 1185)),
                    ((160, 990), (160, 1290)),
                    ((870, 990), (870, 1390))]
        moving = cubic(start, controls[index][0], controls[index][1], (510, row), p)
        scene.text(*moving, SCREEN_TEXT[4][index+2], 49, colors[index], True, 'mm')
    return scene.im


def d3_progress(time):
    """Three discrete turns with endpoint holds, then a long return hold."""
    if time < 2:
        return 0., 0.
    if time >= 20:
        return 360., 1.
    step = min(2, int((time-2)/6))
    local = (time-2)-6*step
    p = float(ease(window(local, .5, 4.3)))
    return 120*(step+p), (step+p)/3


def d3_axes(scene, geom, projection):
    def project(point):
        return np.array(projection.project(tuple(point))[:2])
    axis_length = 2.12
    offsets = [(28, -3), (22, -16), (0, -23)]
    for index in range(3):
        endpoint = np.zeros(3); endpoint[index] = axis_length
        tip = project(endpoint)
        scene.arrow(project(-endpoint*.07), tip, faded(MUTED, .52), 2, 12)
        scene.text(*(tip+offsets[index]), SCREEN_TEXT[6][4+index], 32, MUTED, anchor='mm')
    scene.arrow(project(geom.mul(-.1, geom.U)), project(geom.mul(2.65, geom.U)), INK, 4, 17)
    scene.dot(project((0, 0, 0)), 6, INK)
    return project


def d3_scene(t, entry):
    duration = entry['duration']; time = t*30/duration
    scene = Scene(6, entry['title'], '', t, duration)
    scene.arrow((72, 437), (112, 437), INK, 3, 11)
    scene.text(132, 437, SCREEN_TEXT[6][0], 30, INK, anchor='lm')
    geom = d3_geometry()
    scene.panel((70, 480, 950, 1005), SCREEN_TEXT[6][1])
    scene.panel((70, 1040, 950, 1575), SCREEN_TEXT[6][2])
    angle, trace = d3_progress(time)
    projection = geom.Projection.from_view((300., 762.), 159.)
    project = d3_axes(scene, geom, projection)
    state = geom.state_vector(1.34, 1.04, 45.)
    orbit = [tuple(project(p)) for p in geom.orbit(state)]
    scene.line(geom.closed_partial(orbit, trace), GOLD, 4)
    for index, point in enumerate(orbit):
        if trace+1e-9 >= index/3:
            scene.dot(point, 6, GOLD)
    tip = project(geom.rotate_about_axis(state, angle))
    scene.arrow(project((0, 0, 0)), tip, BLUE, 5, 18)
    scene.dot(tip, 8, BLUE)
    scene.math(SCREEN_TEXT[6][7], x=786, y=731, size=48, maxwidth=210)

    projection = geom.Projection.from_view((300., 1322.), 159.)
    project = lambda p: np.array(projection.project(tuple(p))[:2])
    in_plane = geom.normalize(geom.sub((1., 0., 0.), geom.mul(geom.dot((1., 0., 0.), geom.U), geom.U)))
    plane = [geom.add(geom.mul(height, geom.U), geom.mul(side, in_plane))
             for height, side in [(-.15, -.66), (2.25, -.66), (2.25, .66), (-.15, .66)]]
    plane_points = [tuple(project(p)) for p in plane]
    scene.d.polygon(plane_points, fill=faded(BLUE, .11))
    scene.line(plane_points+[plane_points[0]], faded(BLUE, .5), 2)
    project = d3_axes(scene, geom, projection)
    state = geom.state_vector(1.34, 1.04, 125.)
    mirror = geom.reflect_in_a_plane(state)
    # Both reflections include a settled endpoint: 0 -> 1 -> 0.
    if time < 3:
        flip = 0.
    elif time < 11:
        flip = window(time, 3, 9)
    elif time < 21:
        flip = 1-window(time, 15, 21)
    else:
        flip = 0.
    first, second = project(state), project(mirror)
    scene.line([first, second], faded(GOLD, .7), 4)
    scene.dot(first, 6, GOLD); scene.dot(second, 6, GOLD)
    scene.arrow(project((0, 0, 0)), first, faded(GOLD, .35), 2, 12)
    tip = project(geom.reflect_progress(state, flip))
    scene.arrow(project((0, 0, 0)), tip, BLUE, 5, 18)
    scene.dot(tip, 8, BLUE)
    scene.math(SCREEN_TEXT[6][8], x=786, y=1246, size=48, maxwidth=210)
    scene.text(713, 1440, SCREEN_TEXT[6][3], 30, MUTED, anchor='mm')
    anchor = project(plane[2])
    scene.line([anchor+np.array([7., 0.]), (661, 1402), (713, 1416)], faded(MUTED, .65), 2)
    return scene.im


def continuous_scene(t, entry):
    duration = entry['duration']; time = t*24/duration
    phase = float(ease(window(time, 2, 21)))
    angle = 2*np.pi*phase
    scene = Scene(9, entry['title'], '', t, duration)
    scene.panel((70, 480, 950, 1085), SCREEN_TEXT[9][0])
    center = np.array([510., 795.]); radius = 176.
    ring(scene, center, radius, MUTED, 3)
    for a in np.linspace(0, 2*np.pi, 11, endpoint=False):
        for current, color, width, length in ((a, faded(MUTED, .45), 4, 37),
                                              (a+angle, GOLD, 5, 37)):
            direction = np.array([np.cos(current), -np.sin(current)])
            scene.line([center+(radius-length/2)*direction,
                        center+(radius+length/2)*direction], color, width)
    if phase > .001:
        arc = np.linspace(np.pi/2, np.pi/2+angle, max(3, round(180*phase)))
        arc_points = center+np.c_[np.cos(arc), -np.sin(arc)]*238
        scene.line(arc_points, GOLD, 3)
        scene.arrow(arc_points[-2], arc_points[-1], GOLD, 3, 16)
    scene.math(SCREEN_TEXT[9][4], x=812, y=789, size=42, maxwidth=150)
    scene.panel((70, 1130, 950, 1450), SCREEN_TEXT[9][1])
    y = 1284; left, right = 122, 898
    scene.arrow((510, y), (left, y), MUTED, 3, 13)
    scene.arrow((510, y), (right, y), MUTED, 3, 13)
    spacing = 91.
    amount = 3*phase
    for value in range(-9, 10):
        x = 510+value*spacing
        if left+10 < x < right-10:
            scene.line([(x, y-21), (x, y+21)], faded(MUTED, .5), 4)
        x = 510+(value+amount)*spacing
        if left+10 < x < right-10:
            scene.line([(x, y-34), (x, y+34)], BLUE, 5)
    scene.math(SCREEN_TEXT[9][5], x=510, y=1386, size=43)
    scene.math(SCREEN_TEXT[9][2], x=310, y=1554, size=45, maxwidth=360)
    scene.math(SCREEN_TEXT[9][3], x=710, y=1554, size=45, maxwidth=360)
    return scene.im


def surface_scene(t, entry):
    duration = entry['duration']; time = t*24/duration
    scene = Scene(10, entry['title'], '', t, duration)
    scene.panel((70, 480, 950, 1455), SCREEN_TEXT[10][0])
    geom = surface_geometry()
    def project(p):
        x, y, _ = geom.rotate(tuple(p))
        return np.array([510+126*x, 990-126*y])
    xs = np.linspace(-2.4, 2.4, 13)
    ys = np.linspace(-1.8, 1.8, 10)
    plane_alpha = float(ease(window(time, 4, 7)))
    mesh_alpha = 1-.38*plane_alpha
    cells = []
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            quad = [(x, y, geom.surface_z(x, y)) for x, y in
                    [(xs[i], ys[j]), (xs[i+1], ys[j]),
                     (xs[i+1], ys[j+1]), (xs[i], ys[j+1])]]
            cells.append((sum(geom.depth(p) for p in quad)/4, quad))
    for _, quad in sorted(cells):
        scene.d.polygon([tuple(project(p)) for p in quad], fill=faded(GREEN, .12))
    for y in ys:
        line = [project((x, y, geom.surface_z(x, y))) for x in np.linspace(xs[0], xs[-1], 100)]
        scene.line(line, faded(GREEN, .50*mesh_alpha), 2)
    for x in xs:
        line = [project((x, y, geom.surface_z(x, y))) for y in np.linspace(ys[0], ys[-1], 100)]
        scene.line(line, faded(GREEN, .50*mesh_alpha), 2)
    p0 = np.array([.25, -.25, geom.surface_z(.25, -.25)])
    normal = geom.normalize((-geom.dzdx(.25, -.25), -geom.dzdy(.25, -.25), 1.))
    e1 = np.array(geom.normalize((1., 0., geom.dzdx(.25, -.25))))
    e2 = np.array(geom.normalize(geom.cross(normal, tuple(e1))))
    if plane_alpha > 0:
        plane = [p0+.92*(a*e1+b*e2) for a, b in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
        pts = [tuple(project(p)) for p in plane]
        # Composite onto the visible surface so the plane really fades in;
        # an opaque background-colored polygon would prematurely hide it.
        layer = Image.new('RGBA', scene.im.size, (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        plane_rgb = faded(GOLD, .21)
        layer_draw.polygon(pts, fill=plane_rgb+(round(255*plane_alpha),))
        scene.im.paste(layer, (0, 0), layer)
        scene.line(pts+[pts[0]], faded(GOLD, .9*plane_alpha), 3)
        scene.text(760, 680, SCREEN_TEXT[10][1], 34, faded(GOLD, plane_alpha), anchor='mm')
        corner = project(p0+.78*e1+.70*e2)
        scene.line([(760, 711), tuple(corner)], faded(GOLD, .8*plane_alpha), 2)
    origin = project(p0)
    first = float(ease(window(time, 8.5, 11)))
    second = float(ease(window(time, 12.5, 15)))
    for direction, amount, color, label, offset in [
        (e1, first, RED, SCREEN_TEXT[10][3], (40, 30)),
        (e2, second, BLUE, SCREEN_TEXT[10][4], (24, -37)),
    ]:
        if amount > 0:
            tip = project(p0+1.2*amount*direction)
            scene.arrow(origin, tip, color, 7, 21)
            if amount > .98:
                scene.math(label, x=tip[0]+offset[0], y=tip[1]+offset[1], size=39, color=color, maxwidth=95)
    if second > .98:
        marker = [project(p0+.18*e1), project(p0+.18*(e1+e2)), project(p0+.18*e2)]
        scene.line(marker, INK, 3)
        scene.text(510, 1360, SCREEN_TEXT[10][2], 33, INK, anchor='mm')
    scene.dot(origin, 9, INK)
    return scene.im


def single_angle(time):
    if time < 1:
        return 0.
    if time >= 9:
        return 2*np.pi
    step = min(3, int((time-1)/2))
    local = time-1-step*2
    return (step+float(ease(window(local, .15, 1.25))))*np.pi/2


def flow_scene(t, entry):
    duration = entry['duration']; time = t*30/duration
    field_alpha = float(ease(window(time, 10, 12)))
    phase = float(ease(window(time, 16, 27)))
    stage = 0 if time < 10 else 1 if time < 16 else 2
    scene = Scene(12, entry['title'], '', t, duration)
    scene.panel((70, 480, 950, 1450), SCREEN_TEXT[12][stage])
    center = np.array([510., 954.]); scale = 131.
    axes(scene, center, (-335, 335), (-350, 350), color=faded(MUTED, .35))
    if field_alpha < 1:
        alpha = 1-field_alpha
        angle = single_angle(time)
        radius = 231.
        ring(scene, center, radius, faded(MUTED, alpha), 4)
        point = center+np.array([np.cos(angle), -np.sin(angle)])*radius
        tangent = np.array([-np.sin(angle), -np.cos(angle)])*172
        scene.arrow(point, point+tangent, faded(GOLD, alpha), 6, 20)
        scene.dot(point, 10, faded(BLUE, alpha))
        scene.text(112, 554, SCREEN_TEXT[12][3], 31, faded(GOLD, alpha))
    if field_alpha > 0:
        # A single scale factor relates every displayed arrow to J(x,y).
        for x in np.linspace(-2.25, 2.25, 7):
            for y in np.linspace(-2.25, 2.25, 7):
                if .18 < math.hypot(x, y) < 2.56:
                    point = center+np.array([x, -y])*scale
                    arrow = np.array([-y, -x])*24
                    scene.arrow(point-.38*arrow, point+.62*arrow,
                                faded(MUTED, .67*field_alpha), 3, 9)
        specs = [(.78, .08*np.pi, BLUE), (1.18, .82*np.pi, RED),
                 (1.62, 1.42*np.pi, GOLD), (2.06, .36*np.pi, GREEN),
                 (2.34, 1.1*np.pi, PURPLE)]
        shift = 1.85*np.pi*phase
        for radius, start, color in specs:
            if phase > 0:
                angles = np.linspace(start, start+shift, max(2, round(130*phase)))
                trail = center+np.c_[np.cos(angles), -np.sin(angles)]*(radius*scale)
                scene.line(trail, faded(color, .72*field_alpha), 4)
                scene.dot(trail[0], 4, faded(color, .5*field_alpha))
            point = center+np.array([np.cos(start+shift), -np.sin(start+shift)])*(radius*scale)
            scene.dot(point, 10, faded(color, field_alpha))
    scene.math(SCREEN_TEXT[12][4], x=510, y=1519, size=46)
    if time >= 12:
        scene.math(SCREEN_TEXT[12][5], x=510, y=1603, size=43)
    return scene.im


RENDERERS = {4: vertices_scene, 6: d3_scene, 9: continuous_scene,
             10: surface_scene, 12: flow_scene}


def render(number, t, entry):
    return RENDERERS[number](t, entry)


def validate():
    """Meaningful geometry checks, independent of screen coordinates."""
    geom = d3_geometry()
    vector = geom.state_vector(1.34, 1.04, 45.)
    assert np.allclose(geom.rotate_about_axis(vector, 360), vector)
    assert np.allclose(geom.reflect_in_a_plane(geom.reflect_in_a_plane(vector)), vector)
    for angle in (0, 120, 240):
        rotated = geom.rotate_about_axis(vector, angle)
        assert np.isclose(geom.dot(rotated, geom.U), geom.dot(vector, geom.U))
        assert np.isclose(geom.length(rotated), geom.length(vector))
    assert np.allclose(geom.reflect_in_a_plane(geom.U), geom.U)
    surface = surface_geometry()
    normal = np.array(surface.normalize((-surface.dzdx(.25, -.25), -surface.dzdy(.25, -.25), 1.)))
    e1 = np.array(surface.normalize((1., 0., surface.dzdx(.25, -.25))))
    e2 = np.array(surface.normalize(surface.cross(tuple(normal), tuple(e1))))
    assert abs(np.dot(e1, normal)) < 1e-12
    assert abs(np.dot(e2, normal)) < 1e-12
    assert abs(np.dot(e1, e2)) < 1e-12
    return {'d3_closure': True, 'fixed_diagonal': True, 'tangent_basis': True}
