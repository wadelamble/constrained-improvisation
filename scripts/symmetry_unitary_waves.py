"""Two complex wave states under one exact unitary evolution.

The domain is the unit square.  The finite orthonormal basis is
    b_nm(x, y) = 2 sin(n pi x) sin(m pi y),  1 <= n,m <= MODE_COUNT.
Both states evolve with the same diagonal, self-adjoint generator:
    c_nm(t) = c_nm(0) exp[-i ENERGY_SCALE (n*n + m*m) t].

There is no normalization, damping, or interpolation during evolution.
Plotting a real component does not turn this into a real wave model: overlap
and all validation use the complete complex states.
"""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np

MODE_COUNT = 16
ENERGY_SCALE = 0.055
DURATION = 8.0
TARGET_OVERLAP = 0.40
VALIDATION_PATH = (ROOT / 'content/drafts/animations'
                   / 'symmetry-unitary-histories-validation.json')


def _basis(coordinates, modes):
    """The normalized one-dimensional sine basis, shape (mode, coordinate)."""
    a = np.asarray(coordinates, dtype=float)
    if a.ndim != 1 or not np.isfinite(a).all():
        raise ValueError('coordinates must be a finite one-dimensional array')
    return np.sqrt(2.0) * np.sin(np.pi * modes[:, None] * a[None, :])


def _initial_pattern(x, y, packets):
    """Smooth complex packets used only to choose the initial coefficients."""
    xx, yy = np.meshgrid(x, y)
    result = np.zeros(xx.shape, dtype=complex)
    for cx, cy, sx, sy, kx, ky, weight, phase in packets:
        envelope = np.exp(-0.5 * (((xx-cx)/sx)**2 + ((yy-cy)/sy)**2))
        carrier = np.exp(1j * (np.pi*(kx*(xx-cx) + ky*(yy-cy)) + phase))
        result += weight * envelope * carrier
    # Match the boundary condition before projecting into the sine basis.
    return result * np.sin(np.pi*xx) * np.sin(np.pi*yy)


class WaveHistories:
    """Pair of normalized states, with fixed real overlap and exact evolution.

    evaluate(t, x, y) returns (state, y, x), for scalar t.
    coefficients(t), norms(t), and overlap(t) also accept arrays of times.
    """

    def __init__(self, initial_coefficients, energies, duration=DURATION):
        c = np.array(initial_coefficients, dtype=complex, copy=True)
        e = np.array(energies, dtype=float, copy=True)
        if c.ndim != 3 or c.shape[0] != 2 or c.shape[1:] != e.shape:
            raise ValueError('coefficients must have shape (2, n, n) matching energies')
        if e.ndim != 2 or e.shape[0] != e.shape[1]:
            raise ValueError('the basis must be square')
        if not np.isfinite(c).all() or not np.isfinite(e).all():
            raise ValueError('coefficients and energies must be finite')
        self.initial_coefficients = c
        self.energies = e
        self.duration = float(duration)
        self.modes = np.arange(1, e.shape[0]+1, dtype=float)
        # This is a rigorous (deliberately loose) bound at every point and time.
        self.absolute_bound = 2.0 * np.sum(np.abs(c), axis=(-2, -1))
        self.initial_coefficients.setflags(write=False)
        self.energies.setflags(write=False)
        self.modes.setflags(write=False)

    def coefficients(self, t):
        t = np.asarray(t, dtype=float)
        if not np.isfinite(t).all():
            raise ValueError('time must be finite')
        phase = np.exp(-1j * t[..., None, None] * self.energies)
        return self.initial_coefficients * phase[..., None, :, :]

    def evaluate(self, t, x, y):
        if np.ndim(t) != 0:
            raise ValueError('evaluate expects one time; loop over times for frames')
        bx, by = _basis(x, self.modes), _basis(y, self.modes)
        c = self.coefficients(t)
        return np.einsum('my,snm,nx->syx', by, c, bx, optimize=True)

    def norms(self, t):
        return np.sqrt(np.sum(np.abs(self.coefficients(t))**2, axis=(-2, -1)))

    def overlap(self, t):
        c = self.coefficients(t)
        return np.sum(c[..., 0, :, :].conj() * c[..., 1, :, :], axis=(-2, -1))

    def probability_overlap(self, t):
        """Squared overlap of the full complex states, not spatial density overlap."""
        return np.abs(self.overlap(t))**2


@lru_cache(maxsize=1)
def build_histories():
    modes = np.arange(1, MODE_COUNT+1, dtype=float)
    # Midpoint quadrature resolves the packet profiles before projection.
    q = (np.arange(256)+0.5)/256.0
    basis = _basis(q, modes)
    packets = (
        ((0.25, 0.30, 0.115, 0.13, 3.2, 1.0, 1.0, 0.0),
         (0.66, 0.60, 0.125, 0.11, -1.5, 2.4, 0.80, 0.55),
         (0.36, 0.78, 0.105, 0.09, 2.0, -2.0, 0.55, -0.85)),
        ((0.73, 0.26, 0.11, 0.115, -2.8, 1.5, 1.0, -0.25),
         (0.29, 0.64, 0.135, 0.12, 2.0, -2.7, 0.85, 0.90),
         (0.72, 0.78, 0.10, 0.095, -1.8, -1.0, 0.60, -0.65)),
    )
    projected = []
    for arrangement in packets:
        values = _initial_pattern(q, q, arrangement)
        # values[y,x]; coefficients[n,m] use the x mode first.
        projected.append((basis @ values.T @ basis.T) / len(q)**2)
    a, b = projected
    a = a / np.linalg.norm(a)
    b = b - np.vdot(a, b)*a
    b = b / np.linalg.norm(b)
    second = TARGET_OVERLAP*a + np.sqrt(1.0-TARGET_OVERLAP**2)*b
    energies = ENERGY_SCALE*(modes[:, None]**2 + modes[None, :]**2)
    return WaveHistories(np.stack((a, second)), energies)


build_waves = build_histories


def validate():
    waves = build_histories()
    times = np.linspace(0.0, waves.duration, 257)
    norms = waves.norms(times)
    overlaps = waves.overlap(times)
    norm_error = float(np.max(np.abs(norms-1)))
    overlap_error = float(np.max(np.abs(overlaps-TARGET_OVERLAP)))

    c = waves.coefficients(times)
    reversed_coefficients = c * np.exp(1j*times[:, None, None, None]*waves.energies)
    reverse_error = float(np.max(np.abs(reversed_coefficients-waves.initial_coefficients)))
    group_error = 0.0
    for s, t in ((0.25, 1.75), (2.3, -1.1), (4.0, 4.0), (8.0, -8.0)):
        composed = waves.coefficients(s)*np.exp(-1j*t*waves.energies)
        group_error = max(group_error, float(np.max(np.abs(composed-waves.coefficients(s+t)))))

    # A separate real-space integral verifies both basis normalization and
    # reconstruction orientation. The grid resolves all retained sine modes.
    grid = np.linspace(0, 1, 193)
    weights = np.ones(len(grid))/(len(grid)-1)
    weights[[0, -1]] *= 0.5
    area_weights = weights[:, None]*weights[None, :]
    quadrature_norm_error = quadrature_overlap_error = boundary_error = 0.0
    real_part_peaks = np.zeros(2)
    complex_peaks = np.zeros(2)
    samples = []
    for t in np.linspace(0, waves.duration, 129):
        psi = waves.evaluate(t, grid, grid)
        qnorms = np.sum(np.abs(psi)**2*area_weights, axis=(-2, -1))
        qoverlap = np.sum(psi[0].conj()*psi[1]*area_weights)
        quadrature_norm_error = max(quadrature_norm_error, float(np.max(np.abs(qnorms-1))))
        quadrature_overlap_error = max(quadrature_overlap_error, float(abs(qoverlap-TARGET_OVERLAP)))
        boundary_error = max(boundary_error, float(np.max(np.abs(psi[:, [0, -1], :]))),
                             float(np.max(np.abs(psi[:, :, [0, -1]]))))
        real_part_peaks = np.maximum(real_part_peaks, np.max(np.abs(psi.real), axis=(-2, -1)))
        complex_peaks = np.maximum(complex_peaks, np.max(np.abs(psi), axis=(-2, -1)))
        if abs(t-round(t)) < 1e-12:
            samples.append({'time': float(t), 'norm_squared': qnorms.tolist(),
                            'overlap_real': float(qoverlap.real),
                            'overlap_imaginary': float(qoverlap.imag)})

    tolerance = 2e-12
    errors = {'norm': norm_error, 'complex_overlap': overlap_error,
              'reverse_evolution': reverse_error, 'group_composition': group_error,
              'quadrature_norm_squared': quadrature_norm_error,
              'quadrature_complex_overlap': quadrature_overlap_error,
              'dirichlet_boundary': boundary_error}
    result = {
        'passed': bool(max(errors.values()) < tolerance),
        'model': 'Two complex functions in the same orthonormal Dirichlet sine basis',
        'basis': '2 sin(n*pi*x) sin(m*pi*y), 1 <= n,m <= 16',
        'domain': '[0,1] x [0,1]',
        'generator_eigenvalues': '0.055 * (n^2 + m^2)',
        'evolution': 'c_nm(t) = c_nm(0) exp(-i E_nm t)',
        'duration': waves.duration,
        'mode_count_per_axis': MODE_COUNT,
        'normalization': 'Once at preparation only; never per frame',
        'target_complex_overlap': {'real': TARGET_OVERLAP, 'imaginary': 0.0},
        'squared_overlap': TARGET_OVERLAP**2,
        'errors': errors,
        'tolerance': tolerance,
        'quadrature': {'points_per_axis': len(grid), 'time_samples': 129},
        'sampled_real_component_peaks': real_part_peaks.tolist(),
        'sampled_complex_magnitude_peaks': complex_peaks.tolist(),
        'rigorous_all_time_magnitude_bounds': waves.absolute_bound.tolist(),
        'recommended_fixed_real_height_denominator': float(np.max(real_part_peaks)*1.08),
        'samples': samples,
        'source': str(Path(__file__).relative_to(ROOT)).replace('\\', '/'),
    }
    if not result['passed']:
        raise AssertionError(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    result = validate()
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'errors': result['errors'],
                      'real_peaks': result['sampled_real_component_peaks'],
                      'fixed_height_denominator': result['recommended_fixed_real_height_denominator'],
                      'output': str(VALIDATION_PATH.relative_to(ROOT))}, indent=2))
