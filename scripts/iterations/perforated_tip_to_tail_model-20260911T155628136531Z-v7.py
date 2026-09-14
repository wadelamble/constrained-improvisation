"""Forty-nine finite slits with opaque gaps, using the corrected propagator.

This restores the original slit centers at y=linspace(-2.8, 2.8, 49).
Each opening is 60% of the center spacing wide; the remaining 40% is opaque.
The finite width is now part of the integrals, not just painted on the screen.
All views use SLIT_BOUNDS as their sole source of open/blocked geometry.

The underlying 2D scalar thin-mask approximation and outgoing kernel are
unchanged. Source and amplitude reference remain H0^(1)(kr) and G(9,0).
Earlier continuous-aperture experiments remain in corrected_tip_to_tail_model.
"""
from __future__ import annotations

from functools import lru_cache

import corrected_tip_to_tail_model as propagation
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad_vec

Z1, Z2 = propagation.Z1, propagation.Z2
DISTANCE = propagation.DISTANCE
WAVELENGTH, K = propagation.WAVELENGTH, propagation.K
REFERENCE = propagation.REFERENCE
source, kernel = propagation.source, propagation.kernel
free_amplitude = propagation.free_amplitude

SLIT_COUNT = ELEMENTS = 49
CENTER_EXTENT = 2.8
PITCH = 2 * CENTER_EXTENT / (SLIT_COUNT - 1)
OPEN_FRACTION = .60
SLIT_WIDTH = OPEN_FRACTION * PITCH
GAP_WIDTH = PITCH - SLIT_WIDTH
ASCENDING_CENTERS = np.linspace(-CENTER_EXTENT, CENTER_EXTENT, SLIT_COUNT)
CENTERS = ASCENDING_CENTERS[::-1].copy()
SLIT_BOUNDS = np.column_stack((ASCENDING_CENTERS - SLIT_WIDTH / 2,
                               ASCENDING_CENTERS + SLIT_WIDTH / 2))
HALF_APERTURE = float(SLIT_BOUNDS[-1, 1])
for array in (ASCENDING_CENTERS, CENTERS, SLIT_BOUNDS):
    array.flags.writeable = False


def transmission(y):
    """One inside any physical slit; zero on every opaque bar and outside."""
    y = np.asarray(y)
    return np.any((y[..., None] >= SLIT_BOUNDS[:, 0]) &
                  (y[..., None] <= SLIT_BOUNDS[:, 1]), axis=-1).astype(float)


def opaque_intervals(y_min, y_max):
    """Complement of the slit mask, for both screen drawings."""
    intervals = []
    cursor = float(y_min)
    for lower, upper in SLIT_BOUNDS:
        if upper <= y_min or lower >= y_max:
            continue
        if lower > cursor:
            intervals.append((cursor, min(float(lower), float(y_max))))
        cursor = max(cursor, float(upper))
    if cursor < y_max:
        intervals.append((cursor, float(y_max)))
    return intervals


@lru_cache(maxsize=8)
def slit_quadrature(order=12):
    nodes, weights = leggauss(order)
    half = np.diff(SLIT_BOUNDS, axis=1) / 2
    positions = SLIT_BOUNDS.mean(axis=1)[:, None] + half * nodes
    return positions, half * weights


@lru_cache(maxsize=4096)
def contributions(b: float, order: int = 12) -> np.ndarray:
    """One integral per finite slit, in top-to-bottom display order."""
    y, weights = slit_quadrature(order)
    integrand = source(Z1, y) * kernel(Z2, b - y) / REFERENCE
    result = np.sum(integrand * weights, axis=1)[::-1].copy()
    result.flags.writeable = False
    return result


def transmitted_field(z, y, order=12):
    positions, weights = slit_quadrature(order)
    incident_weights = (source(Z1, positions) * weights / REFERENCE).ravel()
    return np.sum(kernel(z, np.atleast_1d(y)[:, None] - positions.ravel()[None, :]) *
                  incident_weights, axis=1)


def chain(b):
    return np.r_[0j, np.cumsum(contributions(float(b)))]


def total(b):
    return complex(np.sum(contributions(float(b))))


def checks():
    assert len(SLIT_BOUNDS) == 49
    assert np.all(SLIT_BOUNDS[1:, 0] > SLIT_BOUNDS[:-1, 1])
    assert np.all(transmission(CENTERS) == 1)
    gap_centers = (SLIT_BOUNDS[:-1, 1] + SLIT_BOUNDS[1:, 0]) / 2
    assert np.all(transmission(gap_centers) == 0)
    assert np.all(transmission(np.array([-4., 4.])) == 0)
    assert len(opaque_intervals(-4, 4)) == 50
    quadrature_error = max(float(np.max(abs(contributions(float(b), 12) -
                                           contributions(float(b), 24))))
                           for b in np.linspace(-3.2, 3.2, 33))
    independent_error = 0.
    for b in (0., .94, 3.2):
        independent = 0j
        for lower, upper in SLIT_BOUNDS:
            term, _ = quad_vec(lambda y: source(Z1, y) * kernel(Z2, b-y) / REFERENCE,
                               lower, upper, epsabs=2e-13, epsrel=2e-13)
            independent += term
        independent_error = max(independent_error, abs(total(b) - independent))
    symmetry_error = max(abs(total(float(b)) - total(float(-b)))
                         for b in np.linspace(-3.2, 3.2, 33))
    # The finite bars must change the result relative to a single open span.
    continuous, _ = quad_vec(lambda y: source(Z1, y) * kernel(Z2, -y) / REFERENCE,
                             -HALF_APERTURE, HALF_APERTURE,
                             epsabs=1e-12, epsrel=1e-12)
    mask_difference = abs(total(0.) - continuous)
    display_rotation = np.exp(-1j * np.angle(total(0.)))
    centered = display_rotation * total(0.)
    assert quadrature_error < 1e-12 and independent_error < 1e-11
    assert symmetry_error < 1e-12 and mask_difference > .25
    assert centered.real > 0 and abs(centered.imag) < 1e-14
    return {
        "status": "passed",
        "geometry": "49 disjoint finite slits separated by 48 opaque bars, plus opaque outer screen",
        "slit_count": SLIT_COUNT,
        "slit_width": SLIT_WIDTH,
        "center_spacing": PITCH,
        "opaque_gap_width": GAP_WIDTH,
        "open_fraction_of_pitch": OPEN_FRACTION,
        "slit_bounds_bottom_to_top": SLIT_BOUNDS.tolist(),
        "quadrature_12_vs_24_max_error": quadrature_error,
        "independent_integral_over_49_slits_error": float(independent_error),
        "symmetry_error": float(symmetry_error),
        "difference_from_one_continuous_opening_at_center": float(mask_difference),
        "center_physical_phase_degrees": float(np.angle(total(0.), deg=True)),
        "fixed_display_rotation_degrees": float(np.angle(display_rotation, deg=True)),
        "center_intensity_relative_to_free_center": float(abs(total(0.))**2),
        "propagation_model": "same validated outgoing 2D scalar thin-mask kernel; finite opaque gaps now included",
    }
