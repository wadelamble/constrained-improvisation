"""Faithful portrait adaptations of the later pre-Fourier desktop visuals.

The desktop source functions, boost orbit and eigencomponent coefficients are
retained. Each ordered operation gets its own interval and a readable hold.
All coordinates are native portrait coordinates; nothing is cropped footage.
"""
from __future__ import annotations

from core import *


SCREEN_TEXT = {
    14: ["Two points under the same boost", r"(ct)^2-x^2=1\qquad(c=1)",
         "η", "x", "ct", "A", "B", "Ordinary tip distance", r"B(\eta)=",
         r"\cosh\eta", r"\sinh\eta", r"A:\ (ct_A)^2-x_A^2=1",
         r"B:\ (ct_B)^2-x_B^2=1"],
    16: ["The same inputs, two orders", r"T_{10}(x)=x+10", "Add, then translate",
         "Translate, then add", r"2+3=5", r"T_{10}(2+3)=15",
         r"T_{10}(2)=12,\qquad T_{10}(3)=13", r"12+13=25",
         r"T_{10}(2)+T_{10}(3)=25", "+10", "2", "3", "5", "12", "13", "15", "25", "0", "10", "20",
         r"T_{10}(2+3)\ne T_{10}(2)+T_{10}(3)", r"15\ne25"],
    17: ["The same functions, two orders", r"(T_af)(x)=f(x-a),\qquad a=1.35",
         "Add, then translate", "Translate, then add", r"f", r"g", r"f+g",
         r"T_a(f+g)", r"T_af", r"T_ag", r"T_af+T_ag", "x", "+a",
         r"T_a(f+g)=T_af+T_ag"],
    18: ["The same starting shape", r"(T_af)(x)=f(x-a)", "Translation",
         "Translation + deformation", "Shape preserved", "Shape distorted",
         "Same values, new position", "New position and new shape", "x", "+a"],
    21: ["Resolve the vector into its components", "Scale each component independently",
         r"\mathbf{r}_{\mathrm{in}}=u\hat{\mathbf{u}}+v\hat{\mathbf{v}}", "s", "u", "v",
         "u component", "v component", "Result", r"\mathbf{r}_{\mathrm{in}}", r"\mathbf{r}",
         r"\mathbf{r}=su\hat{\mathbf{u}}+s^{-1}v\hat{\mathbf{v}}",
         r"\mathbf{r}=", r"s", r"s^{-1}", "0"],
    23: ["A sum in the complex plane", r"z=x+iy", "Re", "Im", "x", "iy", "z",
         "Complex form", "Vector form", r"z=x+iy\quad\longleftrightarrow\quad(x,y)"],
    24: ["At the identity", "At every point on the circle", r"z=1,\qquad iz=i",
         r"z=e^{i\theta},\qquad iz=ie^{i\theta}", "Re", "Im", "1", "i", "z", "iz",
         r"|z|=|iz|=1", r"\frac{dz}{d\theta}=iz(\theta)"],
}


def _q(t, entry):
    return 24 * float(np.clip(t / entry["duration"], 0, 1))


def _scene(number, t, entry, stage):
    return Scene(number, entry["title"], stage, t, entry["duration"])


def _faint(color, amount=.3):
    base = np.array(tuple(int(BG[i:i+2], 16) for i in (1, 3, 5)))
    ink = np.array(tuple(int(color[i:i+2], 16) for i in (1, 3, 5)))
    return tuple(np.rint(base + amount * (ink-base)).astype(int))


def _dashed(s, start, end, color=GRID, width=2, dash=10, gap=8):
    a, b = np.asarray(start, float), np.asarray(end, float)
    delta = b-a
    length = float(np.linalg.norm(delta))
    if length < .01:
        return
    for d in np.arange(0, length, dash+gap):
        s.line([a+delta*d/length, a+delta*min(d+dash, length)/length], color, width)


def _masked_text(s, pos, value, size, color, anchor="mm"):
    label = TEXT_REPLACEMENTS.get(str(value), str(value))
    bounds = s.d.textbbox(tuple(pos), label, font=font(size), anchor=anchor)
    s.d.rectangle((bounds[0]-5, bounds[1]-4, bounds[2]+5, bounds[3]+4), fill=BG)
    s.text(*pos, value, size, color, anchor=anchor)


def _map(box, xlim, ylim):
    left, top, right, bottom = box
    def xy(x, y):
        x, y = np.broadcast_arrays(np.asarray(x), np.asarray(y))
        return np.stack((left+(x-xlim[0])/(xlim[1]-xlim[0])*(right-left),
                         bottom-(y-ylim[0])/(ylim[1]-ylim[0])*(bottom-top)), axis=-1)
    return xy


def _plot(s, box, xlim, ylim):
    xy = _map(box, xlim, ylim)
    for y in (.4, .8, 1.2):
        if ylim[0] < y < ylim[1]:
            s.line([xy(xlim[0], y), xy(xlim[1], y)], _faint(GRID, .55), 1)
    s.arrow(xy(xlim[0], 0), xy(xlim[1], 0), MUTED, 2, 10)
    s.line([xy(0, ylim[0]), xy(0, ylim[1])], GRID, 2)
    s.text(box[2]+13, float(xy(0, 0)[1])+10, "x", 30, MUTED)
    return xy


def _matrix(s, rows, x, y, dx=144, dy=64, size=37, colors=None):
    left, right = x-dx, x+dx
    top, bottom = y-dy, y+dy
    for edge, sign in ((left-15, 1), (right+15, -1)):
        s.line([(edge+12*sign, top), (edge, top), (edge, bottom),
                (edge+12*sign, bottom)], INK, 3)
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            s.math(item, x=x+(j-.5)*dx, y=y+(i-.5)*dy, size=size,
                   color=colors[i][j] if colors else INK, maxwidth=dx-8)


def _fourteen(t, entry):
    q = _q(t, entry)
    s = _scene(14, t, entry, SCREEN_TEXT[14][0])
    # Exactly the desktop orbit: eta in [0,1.28], with fixed rapidity gap .42.
    eta = 1.28*float(ease(window(q, 3, 20)))
    gap = .42
    origin, scale = np.array([380., 1250.]), 170.
    def p(x, ct):
        return origin+scale*np.array([x, -ct])
    pairs = [(math.sinh(r), math.cosh(r)) for r in (eta, eta+gap)]
    a, b = (p(*pair) for pair in pairs)
    dist = math.dist(pairs[0], pairs[1])
    s.math(r"(ct)^2-x^2=1\qquad(c=1)", y=535, size=52)
    s.text(427, 602, "η", 35, MUTED, anchor="ra")
    s.text(456, 600, f"{eta:.2f}", 38, GOLD)
    s.arrow(p(-1.65, 0), p(3.2, 0), MUTED, 2, 12)
    s.arrow(p(0, -.12), p(0, 3.32), MUTED, 2, 12)
    s.text(944, 1262, "x", 31, MUTED, anchor="ra")
    s.text(400, 674, "ct", 31, MUTED)
    for xx in (-1, 1, 2, 3):
        s.line([p(xx, -.035), p(xx, .035)], MUTED, 2)
    for ct in (1, 2, 3):
        s.line([p(-.035, ct), p(.035, ct)], MUTED, 2)
    for xx, ct in ((-1.6, 1.6), (3.15, 3.15)):
        _dashed(s, origin, p(xx, ct), GRID)
    rr = np.linspace(-1.03, 1.78, 241)
    s.line([p(math.sinh(r), math.cosh(r)) for r in rr], _faint(INK, .5), 3)
    # The actual changing pair separation is a third, independent object.
    s.line([a, b], GOLD, 7)
    s.arrow(origin, a, BLUE, 6, 20)
    s.arrow(origin, b, RED, 6, 20)
    s.dot(a, 8, BLUE)
    s.dot(b, 8, RED)
    _masked_text(s, (a[0]-25, a[1]-22), "A", 34, BLUE, anchor="ra")
    _masked_text(s, (b[0]+24, b[1]+17), "B", 34, RED, anchor="la")
    s.text(170, 1324, "Ordinary tip distance", 34, GOLD)
    s.text(863, 1318, f"{dist:.2f}", 43, GOLD, anchor="ra")
    s.math(r"B(\eta)=", x=270, y=1450, size=45, maxwidth=210)
    _matrix(s, [[r"\cosh\eta", r"\sinh\eta"],
                [r"\sinh\eta", r"\cosh\eta"]], 620, 1450, dx=154, dy=58, size=37)
    s.math(r"A:\ (ct_A)^2-x_A^2=1", x=300, y=1587, size=35, color=BLUE, maxwidth=420)
    s.math(r"B:\ (ct_B)^2-x_B^2=1", x=744, y=1587, size=35, color=RED, maxwidth=420)
    return s.im


def _number_line(s, y):
    left, right = 130., 910.
    s.arrow((left, y), (right, y), MUTED, 2, 11)
    def pos(x):
        return left+(right-left)*x/28
    for x in range(0, 26, 5):
        s.line([(pos(x), y-7), (pos(x), y+7)], MUTED, 2)
        s.text(pos(x), y+19, str(x), 30, MUTED, anchor="ma")
    return pos


def _scalar_sum(s, pos, baseline, a, b, progress):
    """Scalar addition as genuine tip-to-tail displacement, not dot merging.

    The blue displacement has length a. The red displacement always has
    length b while its tail moves from 0 to a. At completion its tip is a+b.
    """
    y1 = baseline-74
    y2 = lerp(baseline-135, y1, progress)
    tail = progress*a
    s.arrow((pos(0), y1), (pos(a), y1), BLUE, 6, 15)
    s.arrow((pos(tail), y2), (pos(tail+b), y2), RED, 6, 15)
    s.text((pos(0)+pos(a))/2, y1+22, str(a), 33, BLUE, anchor="ma")
    s.text((pos(tail)+pos(tail+b))/2, y2-21, str(b), 33, RED, anchor="ms")
    _dashed(s, (pos(a), y1), (pos(a), baseline), _faint(BLUE, .6), 2, 6, 5)
    _dashed(s, (pos(tail+b), y2), (pos(tail+b), baseline), _faint(RED, .6), 2, 6, 5)
    if progress >= .999:
        s.dot((pos(a+b), baseline), 10, PURPLE)
        s.text(pos(a+b)+17, baseline-24, str(a+b), 36, PURPLE, anchor="ls")


def _sixteen(t, entry):
    q = _q(t, entry)
    s = _scene(16, t, entry, SCREEN_TEXT[16][0])
    first = float(ease(window(q, 3, 9)))
    second = float(ease(window(q, 13, 20)))
    s.math(r"T_{10}(x)=x+10", y=530, size=55)
    s.text(100, 615, "Add, then translate", 34, MUTED)
    s.text(100, 1060, "Translate, then add", 34, MUTED)
    ptop, pbottom = _number_line(s, 909), _number_line(s, 1398)
    if q < 11:
        s.math(r"2+3=5", x=707, y=681, size=48, color=PURPLE)
        _scalar_sum(s, ptop, 909, 2, 3, first)
    else:
        value = 5+10*second
        s.math(r"T_{10}(2+3)=15", y=690, size=49, color=PURPLE)
        s.dot((ptop(5), 909), 7, GRID)
        s.arrow((ptop(5), 817), (ptop(15), 817), GOLD, 4, 14)
        s.text((ptop(5)+ptop(15))/2, 777, "+10", 35, GOLD, anchor="mm")
        s.dot((ptop(value), 909), 11, PURPLE)
        label = "5" if second == 0 else ("15" if second == 1 else f"{value:.1f}")
        s.text(ptop(value), 862, label, 38, PURPLE, anchor="mm")
    if q < 12:
        s.math(r"T_{10}(2)=12,\qquad T_{10}(3)=13", y=1140, size=43)
        for initial, color, y, dx in ((2, BLUE, 1270, -12), (3, RED, 1327, 14)):
            current = initial+10*first
            s.arrow((pbottom(initial), y), (pbottom(initial+10), y), color, 4, 14)
            s.text((pbottom(initial)+pbottom(initial+10))/2, y-18, "+10", 32, color, anchor="ms")
            s.dot((pbottom(current), 1398), 9, color)
            if first in (0., 1.):
                s.text(pbottom(current)+dx, 1435+(0 if initial == 2 else 42),
                       str(round(current)), 34, color, anchor="mm")
    else:
        s.math(r"12+13=25", x=720, y=1160, size=47, color=PURPLE)
        _scalar_sum(s, pbottom, 1398, 12, 13, second)
    if q >= 21:
        s.math(r"T_{10}(2)+T_{10}(3)=25", y=1495, size=42, color=PURPLE)
        s.math(r"15\ne25", y=1590, size=59, color=GOLD)
    else:
        s.math(r"T_{10}(2+3)\ne T_{10}(2)+T_{10}(3)", y=1585, size=43, maxwidth=860)
    return s.im


def _source_f(x):
    return .92*np.exp(-((np.asarray(x)+1.15)**2)/.34)


def _source_g(x):
    return .62*np.exp(-((np.asarray(x)-.62)**2)/.22)


def _seventeen(t, entry):
    q = _q(t, entry)
    s = _scene(17, t, entry, SCREEN_TEXT[17][0])
    first = float(ease(window(q, 3, 9)))
    second = float(ease(window(q, 13, 20)))
    shift = 1.35
    x = np.linspace(-3.2, 4.2, 650)
    s.math(r"(T_af)(x)=f(x-a),\qquad a=1.35", y=535, size=45)
    s.text(100, 622, "Add, then translate", 34, MUTED)
    s.text(100, 1085, "Translate, then add", 34, MUTED)
    xy1 = _plot(s, (110, 745, 910, 996), (-3.2, 4.2), (-.12, 1.35))
    xy2 = _plot(s, (110, 1207, 910, 1458), (-3.2, 4.2), (-.12, 1.35))
    if q < 11:
        s.math(r"f", x=700, y=680, size=42, color=BLUE)
        s.math(r"g", x=765, y=680, size=42, color=RED)
        s.math(r"f+g", x=857, y=680, size=42, color=PURPLE, maxwidth=100)
        s.line(xy1(x, _source_f(x)), _faint(BLUE, .7), 4)
        s.line(xy1(x, _source_g(x)), _faint(RED, .7), 4)
        # Scan the pointwise sum across x; at the end the entire sum remains.
        n = round(first*(len(x)-1))+1
        if first > 0:
            s.line(xy1(x[:n], _source_f(x[:n])+_source_g(x[:n])), PURPLE, 6)
    else:
        s.math(r"T_a(f+g)", x=789, y=680, size=43, color=PURPLE, maxwidth=245)
        s.line(xy1(x, _source_f(x)+_source_g(x)), GRID, 2)
        s.line(xy1(x, _source_f(x-shift*second)+_source_g(x-shift*second)), PURPLE, 6)
        s.arrow((450, 715), (596, 715), GOLD, 3, 12)
        s.text(523, 684, "+a", 31, GOLD, anchor="mm")
    lower_shift = shift*first
    sum_progress = second if q >= 12 else 0
    component_opacity = .5 if second >= .999 else 1
    s.line(xy2(x, _source_f(x-lower_shift)), _faint(BLUE, component_opacity), 4)
    s.line(xy2(x, _source_g(x-lower_shift)), _faint(RED, component_opacity), 4)
    if q < 12:
        s.math(r"T_af", x=731, y=1145, size=42, color=BLUE)
        s.math(r"T_ag", x=856, y=1145, size=42, color=RED)
        s.arrow((450, 1178), (596, 1178), GOLD, 3, 12)
        s.text(523, 1147, "+a", 31, GOLD, anchor="mm")
    else:
        s.math(r"T_af+T_ag", x=783, y=1145, size=43, color=PURPLE, maxwidth=256)
        n = round(sum_progress*(len(x)-1))+1
        if sum_progress > 0:
            s.line(xy2(x[:n], _source_f(x[:n]-shift)+_source_g(x[:n]-shift)), PURPLE, 6)
    if q >= 21:
        s.math(r"T_a(f+g)=T_af+T_ag", y=1585, size=51, color=GREEN)
    return s.im


def _source_shape(x):
    x = np.asarray(x)
    return (.82*np.exp(-((x+1.18)**2)/.42)
            +.48*np.exp(-((x-.35)**2)/.15)
            +.26*np.exp(-((x-1.18)**2)/.28))


def _source_distortion(x, amount):
    # The source's stretch, skew, height change and localized wobble, unchanged.
    x = np.asarray(x)
    stretch, skew, height = 1+.42*amount, .28*amount, 1-.28*amount
    wobble = .12*amount*np.exp(-((x-.5)**2)/1.8)*np.sin(3.2*x)
    return np.maximum(0, height*_source_shape((x-skew)/stretch)+wobble)


def _eighteen(t, entry):
    q = _q(t, entry)
    s = _scene(18, t, entry, SCREEN_TEXT[18][0])
    amount = float(ease(window(q, 3, 20)))
    shift = 2.1*amount
    x = np.linspace(-3.4, 6., 800)
    s.math(r"(T_af)(x)=f(x-a)", y=535, size=56)
    for top, color, title, subtitle, footer, deformed in (
        (620, BLUE, "Translation", "Shape preserved", "Same values, new position", False),
        (1110, RED, "Translation + deformation", "Shape distorted", "New position and new shape", True),
    ):
        s.text(100, top, title, 36, INK)
        s.text(100, top+48, subtitle, 31, color)
        box = (110, top+127, 910, top+385)
        xy = _plot(s, box, (-3.4, 6.), (-.18, 1.2))
        s.line(xy(x, _source_shape(x)), _faint(color, .28), 3)
        values = _source_distortion(x-shift, amount) if deformed else _source_shape(x-shift)
        s.line(xy(x, values), color, 6)
        s.arrow((682, top+76), (861, top+76), GOLD, 3, 12)
        s.text(772, top+38, "+a", 32, GOLD, anchor="mm")
        s.text(510, top+420, footer, 32, color, anchor="mm")
    return s.im


def _twenty_one(t, entry):
    q = _q(t, entry)
    changing = q >= 11
    s = _scene(21, t, entry, SCREEN_TEXT[21][1 if changing else 0])
    progress = float(ease(window(q, 11, 20)))
    stretch = 1+progress
    root2 = math.sqrt(2)
    uhat, vhat = np.array([1., 1.])/root2, np.array([1., -1.])/root2
    origin, scale = np.array([235., 1080.]), 235.
    def p(v):
        return origin+scale*np.asarray(v)*[1, -1]
    initial = uhat+.75*vhat
    # Keep the source endpoints; use the displayed reciprocal action at every
    # intermediate frame, rather than interpolating the coefficients separately.
    u_component = stretch*uhat
    v_component = (.75/stretch)*vhat
    current = u_component+v_component
    s.math(r"\mathbf{r}_{\mathrm{in}}=u\hat{\mathbf{u}}+v\hat{\mathbf{v}}", y=540, size=51)
    s.text(430, 607, "s", 34, MUTED, anchor="ra")
    s.text(461, 601, f"{stretch:.2f}", 39, GOLD)
    s.line([p(-.8*uhat), p(2.65*uhat)], GRID, 2)
    s.line([p(-.85*vhat), p(.9*vhat)], GRID, 2)
    s.text(*p(2.8*uhat), "u", 32, MUTED, anchor="mm")
    s.text(*(p(.94*vhat)+[19, 8]), "v", 32, MUTED, anchor="mm")
    s.dot(origin, 5, MUTED)
    if progress > 0:
        s.arrow(origin, p(initial), GRID, 3, 14)
        s.math(r"\mathbf{r}_{\mathrm{in}}", x=p(initial)[0]+44, y=p(initial)[1]+24,
               size=35, color=MUTED, maxwidth=95)
    # Start with the whole vector; resolve its two components before scaling.
    s.arrow(origin, p(current), BLUE, 5, 19)
    first = float(ease(window(q, 2.5, 5.5)))
    second = float(ease(window(q, 6, 9)))
    if first > 0:
        s.arrow(origin, p(first*u_component), GREEN, 7, 20)
    if second > 0:
        s.arrow(p(u_component), p(u_component+second*v_component), GOLD, 7, 20)
    label = r"\mathbf{r}" if changing else r"\mathbf{r}_{\mathrm{in}}"
    s.math(label, x=p(current)[0]+45, y=p(current)[1]-25, size=39, color=BLUE, maxwidth=102)
    for yy, text_value, color in ((908, "u component", GREEN), (956, "v component", GOLD), (1004, "Result", BLUE)):
        s.text(728, yy, text_value, 30, color)
    if changing:
        s.math(r"\mathbf{r}=su\hat{\mathbf{u}}+s^{-1}v\hat{\mathbf{v}}", y=1330, size=50)
    if q >= 21:
        s.math(r"\mathbf{r}=", x=319, y=1490, size=52, maxwidth=135)
        _matrix(s, [[r"s", "0"], ["0", r"s^{-1}"]], 540, 1490, dx=95, dy=62, size=42,
                colors=[[GREEN, MUTED], [MUTED, GOLD]])
        s.math(r"\mathbf{r}_{\mathrm{in}}", x=776, y=1490, size=47, maxwidth=160)
    return s.im


def _twenty_three(t, entry):
    q = _q(t, entry)
    s = _scene(23, t, entry, SCREEN_TEXT[23][0])
    origin = np.array([265., 1130.])
    # Preserve the source diagram's 270:190 component ratio.
    xvec, yvec = np.array([400., 0.]), np.array([0., -400*190/270])
    real = float(ease(window(q, 2, 6)))
    imaginary = float(ease(window(q, 7, 11)))
    result = float(ease(window(q, 12, 16)))
    for xx in np.arange(97, 930, 84):
        s.line([(xx, 687), (xx, 1250)], _faint(GRID, .6), 1)
    for yy in np.arange(710, 1240, 84):
        s.line([(105, yy), (905, yy)], _faint(GRID, .6), 1)
    s.arrow((105, 1130), (915, 1130), MUTED, 3, 12)
    s.arrow((265, 1250), (265, 670), MUTED, 3, 12)
    s.text(925, 1145, "Re", 31, MUTED, anchor="ra")
    s.text(287, 659, "Im", 31, MUTED)
    s.math(r"z=x+iy", y=540, size=63, color=GREEN)
    if real > 0:
        s.arrow(origin, origin+real*xvec, BLUE, 7, 22)
        s.text(465, 1169, "x", 37, BLUE, anchor="mm")
    if imaginary > 0:
        end = origin+xvec+imaginary*yvec
        s.arrow(origin+xvec, end, RED, 7, 22)
        s.text(699, 988, "iy", 37, RED)
        _dashed(s, end, origin+imaginary*yvec, _faint(BLUE, .7), 2)
    if result > 0:
        end = origin+result*(xvec+yvec)
        s.arrow(origin, end, GREEN, 8, 24)
        s.dot(end, 9, GREEN)
        if result >= .999:
            s.text(end[0]+26, end[1]-31, "z", 38, GREEN)
    if q >= 17:
        s.text(263, 1360, "Complex form", 33, MUTED, anchor="mm")
        s.text(764, 1360, "Vector form", 33, MUTED, anchor="mm")
        s.math(r"z=x+iy\quad\longleftrightarrow\quad(x,y)", y=1455, size=58)
    return s.im


def _twenty_four(t, entry):
    q = _q(t, entry)
    general = q >= 8
    s = _scene(24, t, entry, SCREEN_TEXT[24][1 if general else 0])
    theta = 2*math.pi*float(ease(window(q, 9, 21)))
    z = np.array([math.cos(theta), math.sin(theta)])
    iz = np.array([-math.sin(theta), math.cos(theta)])
    center, radius = np.array([470., 1030.]), 235.
    def p(v):
        return center+radius*np.asarray(v)*[1, -1]
    s.math(r"z=e^{i\theta},\qquad iz=ie^{i\theta}" if general else r"z=1,\qquad iz=i",
           y=540, size=56)
    s.arrow((109, 1030), (916, 1030), MUTED, 2, 12)
    s.arrow((470, 1380), (470, 665), MUTED, 2, 12)
    s.text(929, 1053, "Re", 31, MUTED, anchor="ra")
    s.text(491, 649, "Im", 31, MUTED)
    a = np.linspace(0, 2*math.pi, 250)
    s.line(np.array([p([math.cos(v), math.sin(v)]) for v in a]), GRID, 4)
    # iz has the same norm as z and is anchored at z's tip, as a tangent.
    s.arrow(center, p(z), BLUE, 7, 22)
    s.arrow(p(z), p(z+iz), RED, 7, 22)
    s.dot(p(z), 8, INK)
    # The square remains perpendicular under the exact same rotation.
    marker = 23/radius
    s.line([p(z-marker*z), p(z-marker*z+marker*iz), p(z+marker*iz)], MUTED, 2)
    radial_label = p(.55*z-.15*iz)
    tangent_label = p(1.16*z+.52*iz)
    _masked_text(s, radial_label, "z" if general else "1", 40, BLUE)
    _masked_text(s, tangent_label, "iz" if general else "i", 40, RED)
    s.math(r"|z|=|iz|=1", y=1450, size=48, color=MUTED)
    s.math(r"\frac{dz}{d\theta}=iz(\theta)", y=1560, size=59)
    return s.im


_RENDERERS = {14: _fourteen, 16: _sixteen, 17: _seventeen, 18: _eighteen,
              21: _twenty_one, 23: _twenty_three, 24: _twenty_four}


def render(number, t, entry):
    """Render one native 1080×1920 RGB frame at playback time t."""
    return _RENDERERS[int(number)](t, entry)

