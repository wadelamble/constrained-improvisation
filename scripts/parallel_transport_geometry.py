"""Exact Levi-Civita parallel transport on great-circle spherical triangles.

Independent geometry for the parallel-transport animation. This module has
no rendering side effects. Run directly to print its invariant checks.
"""
from __future__ import annotations

import json
import math

import numpy as np


CENTER = np.ones(3, dtype=float) / math.sqrt(3.0)
OCTANT_VERTICES = np.array([[0., 0., 1.], [1., 0., 0.], [0., 1., 0.]])


def unit(vector):
    vector = np.asarray(vector, dtype=float)
    length = np.linalg.norm(vector)
    if length <= 1e-15:
        raise ValueError('A nonzero direction is required.')
    return vector / length


def arc_angle(a, b):
    a, b = unit(a), unit(b)
    return float(math.atan2(np.linalg.norm(np.cross(a, b)), np.dot(a, b)))


def rotate(vector, axis, angle):
    """Rodrigues rotation; axis is normalized internally."""
    vector, axis = np.asarray(vector, dtype=float), unit(axis)
    cosine, sine = math.cos(angle), math.sin(angle)
    return (cosine * vector + sine * np.cross(axis, vector)
            + (1. - cosine) * np.dot(axis, vector) * axis)


def slerp(a, b, u):
    """Point on the minor great-circle arc, with scalar or array parameter."""
    a, b = unit(a), unit(b)
    angle = arc_angle(a, b)
    u = np.asarray(u, dtype=float)
    if angle < 1e-12:
        result = (1. - u[..., None]) * a + u[..., None] * b
        return result / np.linalg.norm(result, axis=-1, keepdims=True)
    if math.pi - angle < 1e-10:
        raise ValueError('Antipodal endpoints do not define one minor arc.')
    return ((np.sin((1. - u[..., None]) * angle) * a
             + np.sin(u[..., None] * angle) * b) / math.sin(angle))


def vertices(scale=1.0):
    """Equilateral triangle shrunk geodesically toward the octant center.

    scale=1 gives the z, x, y unit-axis vertices, enclosing pi/2 steradians.
    scale->0 shrinks the loop to CENTER without moving its center.
    """
    scale = float(scale)
    if not 0. < scale <= 1.:
        raise ValueError('Triangle scale must lie in (0, 1].')
    return np.array([slerp(CENTER, point, scale) for point in OCTANT_VERTICES])


def tangent_projection(position, direction):
    """Normalize the projection of an ambient direction into a tangent plane."""
    position = unit(position)
    direction = np.asarray(direction, dtype=float)
    return unit(direction - np.dot(direction, position) * position)


def first_leg_tangent(verts):
    verts = np.asarray(verts, dtype=float)
    return tangent_projection(verts[0], verts[1])


def leg_lengths(verts):
    verts = np.asarray(verts, dtype=float)
    return np.array([arc_angle(verts[i], verts[(i + 1) % len(verts)])
                     for i in range(len(verts))])


def transport_leg(start, end, vector, fraction=1.):
    """Transport along one minor geodesic, including partial traversal.

    Rotating about start x end keeps both the point and arrow tangent.
    The arrow's ambient derivative is purely normal to the sphere, so its
    tangential (covariant) derivative vanishes: this is parallel transport.
    """
    start, end = unit(start), unit(end)
    axis = np.cross(start, end)
    angle = arc_angle(start, end)
    if angle < 1e-12:
        return start.copy(), np.asarray(vector, dtype=float).copy()
    if math.pi - angle < 1e-10:
        raise ValueError('Antipodal endpoints do not define one minor arc.')
    fraction = float(np.clip(fraction, 0., 1.))
    travelled = fraction * angle
    return rotate(start, axis, travelled), rotate(vector, axis, travelled)


def transport_position_vector(verts, v0, progress):
    """Return (point, transported arrow), with progress by total arc length.

    The vector is neither reset nor turned at polygon corners. At progress
    1 the point is the exact original vertex and the holonomy remains in
    the returned vector.
    """
    verts = np.asarray(verts, dtype=float)
    progress = float(np.clip(progress, 0., 1.))
    lengths = leg_lengths(verts)
    remaining = progress * float(np.sum(lengths))
    vector = np.asarray(v0, dtype=float).copy()
    position = verts[0].copy()
    for index, length in enumerate(lengths):
        fraction = min(remaining / length, 1.) if length > 1e-15 else 1.
        position, vector = transport_leg(
            verts[index], verts[(index + 1) % len(verts)], vector, fraction)
        if remaining <= length:
            if progress == 1.:
                position = verts[0].copy()
            return position, vector
        remaining -= length
    return verts[0].copy(), vector


def path_samples(verts, samples_per_leg=100):
    """Closed minor-arc polygon; each shared corner appears once."""
    verts = np.asarray(verts, dtype=float)
    samples = []
    for i in range(len(verts)):
        samples.extend(slerp(verts[i], verts[(i + 1) % len(verts)],
                             np.linspace(0., 1., samples_per_leg, endpoint=False)))
    return np.vstack((samples, verts[0]))


def spherical_area(verts, signed=False):
    """Solid angle / area on unit sphere for a minor spherical triangle."""
    a, b, c = (unit(point) for point in np.asarray(verts, dtype=float))
    numerator = float(np.dot(a, np.cross(b, c)))
    denominator = float(1. + np.dot(a, b) + np.dot(b, c) + np.dot(c, a))
    result = 2. * math.atan2(numerator, denominator)
    return result if signed else abs(result)


def signed_tangent_angle(position, before, after):
    position, before, after = unit(position), unit(before), unit(after)
    return float(math.atan2(np.dot(position, np.cross(before, after)),
                            np.dot(before, after)))


def validate():
    """Check mathematical invariants and curvature/holonomy independently."""
    metrics = {'max_position_norm_error': 0., 'max_vector_norm_error': 0.,
               'max_tangency_error': 0., 'max_tangential_derivative': 0.,
               'max_holonomy_area_error': 0., 'max_return_position_error': 0.,
               'max_finite_difference_parallel_error': 0., 'cases': []}
    camera_right = unit(np.array([1., -1., 0.]))
    for scale in (1., .8, .5, .2, .04):
        verts = vertices(scale)
        v0 = tangent_projection(verts[0], camera_right)
        for progress in np.linspace(0., 1., 151):
            position, vector = transport_position_vector(verts, v0, progress)
            metrics['max_position_norm_error'] = max(
                metrics['max_position_norm_error'], abs(np.linalg.norm(position) - 1.))
            metrics['max_vector_norm_error'] = max(
                metrics['max_vector_norm_error'], abs(np.linalg.norm(vector) - 1.))
            metrics['max_tangency_error'] = max(
                metrics['max_tangency_error'], abs(np.dot(position, vector)))
        vector = v0.copy()
        for i in range(3):
            start, end = verts[i], verts[(i + 1) % 3]
            axis = unit(np.cross(start, end))
            angle = arc_angle(start, end)
            for fraction in (.1, .4, .8):
                position, at_vector = transport_leg(start, end, vector, fraction)
                derivative = np.cross(axis, at_vector)
                tangential = derivative - np.dot(derivative, position) * position
                metrics['max_tangential_derivative'] = max(
                    metrics['max_tangential_derivative'], np.linalg.norm(tangential))
                h = 1e-5
                _, before = transport_leg(start, end, vector, fraction - h / angle)
                _, after = transport_leg(start, end, vector, fraction + h / angle)
                finite = (after - before) / (2. * h)
                tangent_finite = finite - np.dot(finite, position) * position
                metrics['max_finite_difference_parallel_error'] = max(
                    metrics['max_finite_difference_parallel_error'],
                    np.linalg.norm(tangent_finite))
            _, vector = transport_leg(start, end, vector)
        returned, final = transport_position_vector(verts, v0, 1.)
        signed_angle = signed_tangent_angle(verts[0], v0, final)
        area = spherical_area(verts, signed=True)
        metrics['max_holonomy_area_error'] = max(
            metrics['max_holonomy_area_error'], abs(signed_angle - area))
        metrics['max_return_position_error'] = max(
            metrics['max_return_position_error'], np.linalg.norm(returned - verts[0]))
        metrics['cases'].append({'scale': scale, 'area_steradians': area,
                                 'residual_angle_radians': signed_angle})
    assert abs(spherical_area(vertices(1.)) - math.pi / 2.) < 1e-12
    for key, value in metrics.items():
        if key.startswith('max_'):
            assert value < 1e-8, (key, value)
            metrics[key] = float(value)
    metrics['passed'] = True
    return metrics


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
