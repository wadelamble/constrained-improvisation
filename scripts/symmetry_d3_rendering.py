from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


BG = (255, 255, 255)
INK = (14, 14, 14)
COORD = (178, 178, 178)
COORD_FAINT = (215, 215, 215)
AXIS = (16, 16, 16)
TRACE = (176, 83, 52)
TEAL = (34, 107, 128)
RUST = (176, 83, 52)
PURPLE = (91, 92, 154)
PLANE = (232, 240, 242)
PLANE_EDGE = (150, 174, 181)

Vec3 = tuple[float, float, float]
Vec2 = tuple[float, float]


def add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(s: float, v: Vec3) -> Vec3:
    return (s * v[0], s * v[1], s * v[2])


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(v: Vec3) -> float:
    return math.sqrt(dot(v, v))


def normalize(v: Vec3) -> Vec3:
    size = length(v)
    return (v[0] / size, v[1] / size, v[2] / size)


def mix(a: Vec3, b: Vec3, t: float) -> Vec3:
    return (
        a[0] * (1.0 - t) + b[0] * t,
        a[1] * (1.0 - t) + b[1] * t,
        a[2] * (1.0 - t) + b[2] * t,
    )


def mix2(a: Vec2, b: Vec2, t: float) -> Vec2:
    return (a[0] * (1.0 - t) + b[0] * t, a[1] * (1.0 - t) + b[1] * t)


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


U = normalize((1.0, 1.0, 1.0))
E1 = normalize((1.0, -1.0, 0.0))
E2 = normalize(cross(U, E1))


def camera_basis(view: Vec3, right_hint: Vec3 | None = None) -> tuple[Vec3, Vec3, Vec3]:
    view = normalize(view)
    if right_hint is None:
        right_hint = cross(view, (0.0, 0.0, 1.0))
        if length(right_hint) < 0.001:
            right_hint = E1
    right = normalize(sub(right_hint, mul(dot(right_hint, view), view)))
    up = normalize(cross(view, right))
    return view, right, up


def camera_from_view(view: Vec3, right_hint: Vec3 | None = None) -> tuple[Vec3, Vec3, Vec3]:
    view, right, up = camera_basis(view, right_hint)
    return view, mul(-1.0, right), mul(-1.0, up)


def blended_camera(blend: float) -> tuple[Vec3, Vec3, Vec3]:
    start_view, start_right, _start_up = camera_from_view((3.2, -2.2, 4.6))
    end_view = U
    end_right = E1
    t = ease(blend)
    view = normalize(mix(start_view, end_view, t))
    right_hint = mix(start_right, end_right, t)
    return camera_basis(view, right_hint)


def rotate_about_axis(v: Vec3, degrees: float) -> Vec3:
    theta = math.radians(degrees)
    return add(
        add(mul(math.cos(theta), v), mul(math.sin(theta), cross(U, v))),
        mul(dot(U, v) * (1.0 - math.cos(theta)), U),
    )


def reflect_in_a_plane(v: Vec3) -> Vec3:
    normal = normalize(cross(U, (1.0, 0.0, 0.0)))
    return sub(v, mul(2.0 * dot(v, normal), normal))


def reflect_progress(v: Vec3, progress: float) -> Vec3:
    normal = normalize(cross(U, (1.0, 0.0, 0.0)))
    perpendicular = mul(dot(v, normal), normal)
    parallel = sub(v, perpendicular)
    return add(parallel, mul(math.cos(math.pi * ease(progress)), perpendicular))


def state_vector(height: float, radius: float, phase_degrees: float = 14.0, collapse: float = 0.0) -> Vec3:
    theta = math.radians(phase_degrees)
    radial = add(mul(radius * math.cos(theta), E1), mul(radius * math.sin(theta), E2))
    return add(mul(height * (1.0 - collapse), U), radial)


def orbit(v: Vec3) -> list[Vec3]:
    return [rotate_about_axis(v, angle) for angle in (0.0, 120.0, 240.0)]


def closed_partial(points: list[Vec2], progress: float) -> list[Vec2]:
    progress = max(0.0, min(1.0, progress))
    if progress <= 0.0:
        return []
    closed = points + [points[0]]
    scaled = progress * (len(closed) - 1)
    full = min(len(closed) - 1, int(scaled))
    frac = scaled - full
    out = [closed[0]]
    for idx in range(full):
        out.append(closed[idx + 1])
    if full < len(closed) - 1:
        out.append(mix2(closed[full], closed[full + 1], frac))
    return out


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


@dataclass
class Projection:
    origin: Vec2
    scale: float
    view: Vec3
    right: Vec3
    up: Vec3

    @classmethod
    def from_view(cls, origin: Vec2, scale: float, view: Vec3 = (3.2, -2.2, 4.6)) -> "Projection":
        camera = camera_from_view(view)
        return cls(origin, scale, *camera)

    @classmethod
    def from_blend(cls, origin: Vec2, scale: float, camera_blend: float) -> "Projection":
        return cls(origin, scale, *blended_camera(camera_blend))

    def project(self, point: Vec3) -> tuple[float, float, float]:
        return (
            self.origin[0] + dot(point, self.right) * self.scale,
            self.origin[1] - dot(point, self.up) * self.scale,
            dot(point, self.view),
        )


class Renderer:
    def __init__(self, width: int, height: int, scale: int = 2) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.image = Image.new("RGB", (width * scale, height * scale), BG)
        self.draw = ImageDraw.Draw(self.image)

    def blend(self, color: tuple[int, int, int], alpha: float) -> tuple[int, int, int]:
        alpha = max(0.0, min(1.0, alpha))
        return (
            round(BG[0] * (1.0 - alpha) + color[0] * alpha),
            round(BG[1] * (1.0 - alpha) + color[1] * alpha),
            round(BG[2] * (1.0 - alpha) + color[2] * alpha),
        )

    def xy(self, point: Vec2) -> tuple[int, int]:
        return (round(point[0] * self.scale), round(point[1] * self.scale))

    def line(
        self,
        points: list[Vec2],
        color: tuple[int, int, int],
        width: float,
        alpha: float = 1.0,
        joint: str | None = "curve",
    ) -> None:
        if alpha <= 0.0 or len(points) < 2:
            return
        self.draw.line(
            [self.xy(point) for point in points],
            fill=self.blend(color, alpha),
            width=max(1, round(width * self.scale)),
            joint=joint,
        )

    def circle(self, center: Vec2, radius: float, color: tuple[int, int, int], alpha: float = 1.0) -> None:
        if alpha <= 0.0:
            return
        x, y = self.xy(center)
        r = round(radius * self.scale)
        self.draw.ellipse((x - r, y - r, x + r, y + r), fill=self.blend(color, alpha))

    def polygon(
        self,
        points: list[Vec2],
        fill: tuple[int, int, int],
        fill_alpha: float,
        outline: tuple[int, int, int] | None = None,
        outline_alpha: float = 0.0,
    ) -> None:
        if fill_alpha > 0.0:
            self.draw.polygon([self.xy(point) for point in points], fill=self.blend(fill, fill_alpha))
        if outline is not None and outline_alpha > 0.0:
            self.line(points + [points[0]], outline, 1.4, outline_alpha)

    def text(
        self,
        label: str,
        position: Vec2,
        size: int,
        color: tuple[int, int, int],
        alpha: float = 1.0,
        anchor: str = "mm",
        bold: bool = False,
    ) -> None:
        if alpha <= 0.0:
            return
        self.draw.text(
            (position[0] * self.scale, position[1] * self.scale),
            label,
            fill=self.blend(color, alpha),
            font=font(size * self.scale, bold),
            anchor=anchor,
        )

    def arrow(
        self,
        start: Vec3,
        end: Vec3,
        projection: Projection,
        color: tuple[int, int, int],
        width: float,
        alpha: float = 1.0,
        head: float = 14.0,
    ) -> None:
        if alpha <= 0.0:
            return
        p0 = projection.project(start)
        p1 = projection.project(end)
        a = (p0[0], p0[1])
        b = (p1[0], p1[1])
        self.line([a, b], color, width, alpha, joint=None)
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        size = math.hypot(dx, dy)
        if size < 4.0:
            return
        angle = math.atan2(dy, dx)
        spread = 2.62
        pts = [
            b,
            (b[0] + math.cos(angle + spread) * head, b[1] + math.sin(angle + spread) * head),
            (b[0] + math.cos(angle - spread) * head, b[1] + math.sin(angle - spread) * head),
        ]
        self.draw.polygon([self.xy(point) for point in pts], fill=self.blend(color, alpha))

    def coordinate_axes(self, projection: Projection, alpha: float = 1.0, length_pos: float = 2.55) -> None:
        for endpoint in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)):
            self.arrow(mul(-0.16, endpoint), mul(length_pos, endpoint), projection, COORD, 1.8, alpha, head=10.0)

    def diagonal_axis(self, projection: Projection, alpha: float = 1.0, length_pos: float = 2.55) -> None:
        self.arrow(mul(-0.10, U), mul(length_pos, U), projection, AXIS, 3.2, alpha, head=15.0)
        origin = projection.project((0.0, 0.0, 0.0))
        self.circle((origin[0], origin[1]), 4.0, AXIS, alpha)

    def orbit_trace(
        self,
        points_3: list[Vec3],
        projection: Projection,
        color: tuple[int, int, int],
        alpha: float = 1.0,
        progress: float = 1.0,
        width: float = 2.8,
        dots: bool = True,
        fill_alpha: float = 0.0,
    ) -> None:
        points_2 = [(projection.project(point)[0], projection.project(point)[1]) for point in points_3]
        if fill_alpha > 0.0:
            self.polygon(points_2, color, fill_alpha)
        path = closed_partial(points_2, progress)
        self.line(path, color, width, alpha)
        if dots:
            for idx, point in enumerate(points_2):
                if progress >= idx / 3.0:
                    self.circle(point, 4.4, color, alpha)

    def vector(self, point: Vec3, projection: Projection, color: tuple[int, int, int] = TEAL, alpha: float = 1.0) -> None:
        self.arrow((0.0, 0.0, 0.0), point, projection, color, 3.6, alpha, head=16.0)
        tip = projection.project(point)
        self.circle((tip[0], tip[1]), 5.0, color, alpha)

    def reflection_plane(self, projection: Projection, alpha: float = 0.30) -> None:
        in_plane = normalize(sub((1.0, 0.0, 0.0), mul(dot((1.0, 0.0, 0.0), U), U)))
        low = -0.15
        high = 2.25
        half_width = 0.66
        corners = [
            add(mul(low, U), mul(-half_width, in_plane)),
            add(mul(high, U), mul(-half_width, in_plane)),
            add(mul(high, U), mul(half_width, in_plane)),
            add(mul(low, U), mul(half_width, in_plane)),
        ]
        points = [(projection.project(point)[0], projection.project(point)[1]) for point in corners]
        self.polygon(points, PLANE, alpha, PLANE_EDGE, min(1.0, alpha * 1.8))

    def sum_zero_plane(self, projection: Projection, alpha: float = 0.18) -> None:
        radius = 1.72
        corners = [
            add(mul(-radius, E1), mul(-radius, E2)),
            add(mul(radius, E1), mul(-radius, E2)),
            add(mul(radius, E1), mul(radius, E2)),
            add(mul(-radius, E1), mul(radius, E2)),
        ]
        points = [(projection.project(point)[0], projection.project(point)[1]) for point in corners]
        self.polygon(points, PLANE, alpha, PLANE_EDGE, min(1.0, alpha * 1.8))

    def output(self) -> Image.Image:
        return self.image.resize((self.width, self.height), Image.Resampling.LANCZOS).convert("RGB")
