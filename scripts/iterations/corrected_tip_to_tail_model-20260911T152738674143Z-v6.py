"""Normalized 2D scalar propagation for the standalone 49-element diagram.

Time convention: exp(-i omega t). A is an outgoing cylindrical source,
G(z,y)=H0^(1)(k hypot(z,y)). The screen-to-detector propagator is the exact
one-transverse-coordinate Rayleigh--Sommerfeld kernel, not exp(i k r) alone.

The aperture [-2.8,2.8] is partitioned into 49 adjacent elements. Each arrow
is the integral over one element, not a zero-width physical hole. This keeps
the old diagram's finely divided aperture interpretation while making the
integration weights explicit. The screen is a scalar thin transmission mask;
material, polarization, and multiple scattering are outside this model.

All amplitudes are divided by G(9,0), ONCE: the unobstructed central field
defines both phase zero and amplitude one. B-dependent phase is retained.
This reference is not a claim that an individual path summand has zero phase.
"""
from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
for folder in ("animation-python-packages", "tip-to-tail-corrected-python-packages"):
    candidate = ROOT / ".tools" / folder
    if candidate.is_dir():
        sys.path.insert(0, str(candidate))

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad_vec
from scipy.special import hankel1

Z1 = Z2 = 4.5
DISTANCE = Z1 + Z2
WAVELENGTH = 0.5
K = 2 * math.pi / WAVELENGTH
HALF_APERTURE = 2.8
ELEMENTS = 49
EDGES = np.linspace(-HALF_APERTURE, HALF_APERTURE, ELEMENTS + 1)
CENTERS = ((EDGES[1:] + EDGES[:-1]) / 2)[::-1]


def source(z, y):
    return hankel1(0, K * np.hypot(z, y))


def kernel(z, y):
    """Inverse Fourier transform of exp(i z sqrt(k^2-q^2)), outgoing branch."""
    r = np.hypot(z, y)
    return 0.5j * K * z / r * hankel1(1, K * r)


REFERENCE = complex(source(DISTANCE, 0.0))


def free_amplitude(b):
    return source(DISTANCE, b) / REFERENCE


@lru_cache(maxsize=4096)
def contributions(b: float, order: int = 12) -> np.ndarray:
    """49 finite-element integrals, ordered from the top to the bottom."""
    nodes, weights = leggauss(order)
    half_width = np.diff(EDGES)[:, None] / 2
    y = (EDGES[:-1, None] + EDGES[1:, None]) / 2 + half_width * nodes
    integrand = source(Z1, y) * kernel(Z2, b - y) / REFERENCE
    result = np.sum(integrand * half_width * weights, axis=1)[::-1].copy()
    result.flags.writeable = False
    return result


def chain(b):
    return np.r_[0j, np.cumsum(contributions(float(b)))]


def total(b):
    return complex(np.sum(contributions(float(b))))


def large_open_plane(z, b, extent=2048.0):
    """Direct spatial integral for an independent source repropagation check."""
    edges = np.linspace(-extent, extent, round(2 * extent / 0.25) + 1)
    nodes, weights = leggauss(12)
    half = np.diff(edges)[:, None] / 2
    y = (edges[1:, None] + edges[:-1, None]) / 2 + half * nodes
    return np.sum(source(z, y) * kernel(DISTANCE - z, b - y) * half * weights)


def spectral_kernel(z, y):
    """Independent angular-spectrum quadrature, including evanescent waves."""
    nodes, weights = leggauss(512)
    theta = nodes * math.pi / 2
    propagating = K / 4 * np.sum(
        weights * np.cos(theta) * np.exp(1j * K * (z * np.cos(theta) + y * np.sin(theta)))
    )
    t_max = np.arcsinh(45 / (K * z))
    t = (nodes + 1) * t_max / 2
    evanescent = K / math.pi * t_max / 2 * np.sum(
        weights * np.sinh(t) * np.exp(-K * z * np.sinh(t)) * np.cos(K * y * np.cosh(t))
    )
    return propagating + evanescent


def checks():
    samples = np.linspace(-3.2, 3.2, 33)
    quadrature_error = max(
        float(np.max(np.abs(contributions(float(b), 12) - contributions(float(b), 24))))
        for b in samples
    )
    independent_sum_error = 0.0
    for b in (0.0, 0.94, 3.2):
        integral, _ = quad_vec(
            lambda y: source(Z1, y) * kernel(Z2, b - y) / REFERENCE,
            -HALF_APERTURE, HALF_APERTURE, epsabs=1e-12, epsrel=1e-12,
        )
        independent_sum_error = max(independent_sum_error, abs(total(b) - integral))

    spectral_error = max(
        abs(spectral_kernel(z, y) - kernel(z, y)) / abs(kernel(z, y))
        for z, y in ((0.7, 0.0), (4.5, -3.2), (4.5, 0.0), (9.0, 2.1))
    )
    composition = []
    for z, b in ((1.5, 0.0), (4.5, 0.0), (7.5, 0.0), (4.5, 0.94), (4.5, 3.2)):
        expected = source(DISTANCE, b)
        composition.append(float(abs(large_open_plane(z, b) - expected) / abs(expected)))

    # The spectral multiplier has the semigroup property. q=0 is a plane
    # wave; nonzero q includes oblique and evanescent components.
    q = np.linspace(-1.1 * K, 1.1 * K, 1001)
    kz = np.sqrt((K * K - q * q).astype(complex))
    composition_spectral = max(
        float(np.max(np.abs(np.exp(1j * DISTANCE / n * kz) ** n - np.exp(1j * DISTANCE * kz))))
        for n in (1, 2, 7, 63)
    )
    plane_wave_error = max(
        abs(np.exp(1j * K * DISTANCE / n) ** n - np.exp(1j * K * DISTANCE))
        for n in (1, 2, 7, 63)
    )
    symmetry_error = max(abs(total(float(b)) - total(float(-b))) for b in samples)
    assert quadrature_error < 1e-12
    assert independent_sum_error < 1e-11
    assert spectral_error < 1e-10
    assert max(composition) < 2e-6
    assert composition_spectral < 1e-11 and plane_wave_error < 1e-11
    assert symmetry_error < 1e-12
    assert abs(free_amplitude(0.0) - 1) < 1e-14
    return {
        "status": "passed",
        "quadrature_12_vs_24_max_absolute_error": quadrature_error,
        "independent_aperture_integral_error": float(independent_sum_error),
        "kernel_vs_angular_spectrum_max_relative_error": float(spectral_error),
        "open_plane_repropagation_relative_errors_extent_2048": composition,
        "spectral_1_2_7_63_steps_max_error": composition_spectral,
        "plane_wave_1_2_7_63_steps_error": float(plane_wave_error),
        "symmetric_detector_error": float(symmetry_error),
        "center_finite_aperture_phase_degrees": float(np.angle(total(0.0), deg=True)),
        "center_intensity_relative_to_free_center": abs(total(0.0)) ** 2,
        "center_element_magnitudes_min_max": [float(np.min(abs(contributions(0.0)))), float(np.max(abs(contributions(0.0))))],
        "phase_reference": "unobstructed field from A at central B; fixed for all frames",
        "source": "outgoing cylindrical wave, H0^(1)(kr), in a 2D scalar model",
        "aperture": "one open interval [-2.8,2.8], partitioned into 49 finite elements",
        "limitations": "Scalar thin-mask diffraction, not a full electromagnetic material-screen calculation. Open-plane spatial checks truncate at |y|=2048; spectral composition is untruncated.",
    }
