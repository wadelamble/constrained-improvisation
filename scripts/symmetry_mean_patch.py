"""Gaussian states and their mean-value patch under one common unitary.

Units have hbar = 1, X psi = x psi, and K psi = -i d(psi)/dx.  Each initial
state is a normalized Weyl-displaced Gaussian with position standard deviation
SIGMA.  Every state undergoes the same ordered operation

    U(tau, r) = S(r) exp(-i tau K**2 / 2),
    (S(r) psi)(x) = exp(-r/2) psi(exp(-r) x).

The mean pair therefore follows diag(exp(r), exp(-r)) @ [[1,tau],[0,1]].
The full complex wavefunctions retain the propagator and displacement phases;
there is no per-frame normalization or state-dependent phase adjustment.

Run this module to write its independent numerical validation report.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np

SIGMA = 0.65
INITIAL_SHEAR = 0.16
TAU_MAX = 0.42
R_MAX = float(np.log(1.32))
A_LIMITS = (-1.8, 1.8)
B_LIMITS = (-3.6, 3.6)
PATCH_AREA = (A_LIMITS[1] - A_LIMITS[0]) * (B_LIMITS[1] - B_LIMITS[0])
VALIDATION_PATH = (ROOT / 'content/drafts/animations'
                   / 'symmetry-mean-patch-validation.json')

_INITIAL_AB = np.array([
    (-1.3, -3.0), (0.5, -2.0), (-0.6, -0.6),
    (0.9, 0.9), (-1.1, 2.0), (1.1, 3.0),
], dtype=float)
INITIAL_SAMPLES = _INITIAL_AB.copy()
INITIAL_SAMPLES[:, 0] += INITIAL_SHEAR * INITIAL_SAMPLES[:, 1]
INITIAL_SAMPLES.setflags(write=False)
INITIAL_CORNERS = np.array([
    (a + INITIAL_SHEAR * b, b)
    for a, b in ((A_LIMITS[0], B_LIMITS[0]),
                 (A_LIMITS[1], B_LIMITS[0]),
                 (A_LIMITS[1], B_LIMITS[1]),
                 (A_LIMITS[0], B_LIMITS[1]))
], dtype=float)
INITIAL_CORNERS.setflags(write=False)
PATCH_CORNERS = INITIAL_CORNERS


def _parameters(tau, r):
    """Require finite scalar parameters without restricting reverse evolution."""
    if np.ndim(tau) != 0 or np.ndim(r) != 0:
        raise ValueError('tau and r must be scalar')
    tau, r = float(tau), float(r)
    if not np.isfinite((tau, r)).all():
        raise ValueError('tau and r must be finite')
    return tau, r


def initial_grid(nu=18, nv=18):
    """Return the initial patch grid, shape (nv+1, nu+1, 2).

    The last axis stores (mean X, mean K).  The u direction follows a and the
    v direction follows b before the initial shear q = a + INITIAL_SHEAR*b.
    """
    if (isinstance(nu, bool) or isinstance(nv, bool)
            or not isinstance(nu, (int, np.integer))
            or not isinstance(nv, (int, np.integer)) or nu < 1 or nv < 1):
        raise ValueError('nu and nv must be positive integers')
    a, b = np.meshgrid(np.linspace(*A_LIMITS, nu + 1),
                       np.linspace(*B_LIMITS, nv + 1))
    return np.stack((a + INITIAL_SHEAR * b, b), axis=-1)


def transformation(tau, r):
    """Return the real 2 by 2 map on the mean pair (X, K)."""
    tau, r = _parameters(tau, r)
    scale = np.exp(r)
    return np.array(((scale, scale * tau), (0.0, 1.0 / scale)))


def evolve_points(points, tau, r):
    """Apply the common mean map to any array whose final axis has length 2."""
    points = np.asarray(points, dtype=float)
    if points.ndim < 1 or points.shape[-1] != 2 or not np.isfinite(points).all():
        raise ValueError('points must be finite with final axis length 2')
    return points @ transformation(tau, r).T


def means(tau, r):
    """Return the six evolved mean pairs, shape (6, 2)."""
    return evolve_points(INITIAL_SAMPLES, tau, r)


def waves(x, tau, r):
    """Evaluate six full complex states at one-dimensional coordinates x.

    At tau=r=0, each state is
    exp(-(x-q)**2/(4*SIGMA**2) + i*p*(x-q/2))/(2*pi*SIGMA**2)**.25.
    The square root of z uses its continuous principal branch, valid for every
    real tau because Re(z)=1.  The returned shape is (6, len(x)).
    """
    tau, r = _parameters(tau, r)
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not np.isfinite(x).all():
        raise ValueError('x must be a finite one-dimensional array')
    q, p = INITIAL_SAMPLES.T[:, :, None]
    y = np.exp(-r) * x[None, :]
    center = q + tau * p
    z = 1.0 + 1j * tau / (2.0 * SIGMA**2)
    normalization = (2.0 * np.pi * SIGMA**2)**(-0.25)
    return (normalization * np.exp(-r / 2.0) / np.sqrt(z)
            * np.exp(-(y - center)**2 / (4.0 * SIGMA**2 * z)
                     + 1j * p * (y - center / 2.0)))


def covariance(tau, r):
    """Common symmetrized covariance of X and K, shape (2, 2)."""
    matrix = transformation(tau, r)
    initial = np.diag((SIGMA**2, 1.0 / (4.0 * SIGMA**2)))
    return matrix @ initial @ matrix.T


def initial_gram():
    """Analytic full complex overlaps G_ij = <psi_i | psi_j>."""
    q, p = INITIAL_SAMPLES.T
    dq = q[None, :] - q[:, None]
    dp = p[None, :] - p[:, None]
    phase = (q[:, None] * p[None, :] - p[:, None] * q[None, :]) / 2.0
    return np.exp(-dq**2 / (8.0 * SIGMA**2)
                  - SIGMA**2 * dp**2 / 2.0 + 1j * phase)


def _cell_areas(grid):
    edge_u = grid[:-1, 1:] - grid[:-1, :-1]
    edge_v = grid[1:, :-1] - grid[:-1, :-1]
    return edge_u[..., 0] * edge_v[..., 1] - edge_u[..., 1] * edge_v[..., 0]


def _polygon_area(points):
    following = np.roll(points, -1, axis=0)
    return 0.5 * np.sum(points[:, 0] * following[:, 1]
                        - points[:, 1] * following[:, 0])


def validate():
    """Check the analytic model against real-space quadrature and FFT evolution.

    FFT momentum supplies an independent derivative for <K> and covariance.
    Free propagation is independently reconstructed by the spectral multiplier
    exp(-i*tau*k**2/2), and the actual inverse order (unsqueeze, reverse free
    propagation) is checked on the complete complex states.
    """
    count = 8192
    x = np.linspace(-24.0, 24.0, count, endpoint=False)
    dx = float(x[1] - x[0])
    k = 2.0 * np.pi * np.fft.fftfreq(count, d=dx)
    initial = waves(x, 0.0, 0.0)
    initial_spectrum = np.fft.fft(initial, axis=-1)
    expected_gram = initial_gram()
    grid = initial_grid()
    initial_areas = _cell_areas(grid)
    errors = {name: 0.0 for name in (
        'norm_squared', 'complex_gram', 'mean_X', 'mean_K', 'covariance',
        'spectral_free_then_squeeze', 'inverse_unsqueeze_then_free',
        'matrix_determinant', 'each_grid_cell_area', 'patch_area',
        'inverse_point_map',
    )}

    def record(name, value):
        errors[name] = max(errors[name], float(np.max(np.abs(value))))

    parameters = [(float(tau), float(r))
                  for tau in np.linspace(0.0, TAU_MAX, 9)
                  for r in np.linspace(0.0, R_MAX, 9)]
    # Negative parameters also exercise the inverse elementary operations.
    parameters.extend([(-TAU_MAX, 0.0), (0.0, -R_MAX),
                       (-TAU_MAX, -R_MAX), (TAU_MAX, -R_MAX)])
    samples = []
    boundary_amplitude = 0.0
    real_peaks = np.zeros(len(INITIAL_SAMPLES))
    complex_peaks = np.zeros(len(INITIAL_SAMPLES))
    for tau, r in parameters:
        psi = waves(x, tau, r)
        density = np.abs(psi)**2
        gram = psi.conj() @ psi.T * dx
        record('norm_squared', np.sum(density, axis=-1) * dx - 1.0)
        record('complex_gram', gram - expected_gram)
        predicted = means(tau, r)
        mean_x = np.sum(density * x, axis=-1) * dx
        k_psi = np.fft.ifft(k * np.fft.fft(psi, axis=-1), axis=-1)
        mean_k = np.sum(psi.conj() * k_psi, axis=-1) * dx
        record('mean_X', mean_x - predicted[:, 0])
        record('mean_K', mean_k - predicted[:, 1])

        centered_x = (x[None, :] - predicted[:, 0, None]) * psi
        centered_k = k_psi - predicted[:, 1, None] * psi
        var_x = np.sum(np.abs(centered_x)**2, axis=-1) * dx
        var_k = np.sum(np.abs(centered_k)**2, axis=-1) * dx
        cov_xk = np.sum(centered_x.conj() * centered_k, axis=-1).real * dx
        measured_cov = np.stack((var_x, cov_xk, cov_xk, var_k), axis=-1)
        record('covariance', measured_cov - covariance(tau, r).reshape(4))

        # On the squeezed grid x_s=exp(r)*x, inverse squeezing is evaluated
        # directly.  No interpolation or renormalization is involved.
        squeezed_grid = np.exp(r) * x
        squeezed_values = waves(squeezed_grid, tau, r)
        free_by_fft = np.fft.ifft(
            initial_spectrum * np.exp(-0.5j * tau * k**2), axis=-1)
        record('spectral_free_then_squeeze',
               squeezed_values - np.exp(-r / 2.0) * free_by_fft)
        unsqueezed = np.exp(r / 2.0) * squeezed_values
        recovered = np.fft.ifft(
            np.fft.fft(unsqueezed, axis=-1) * np.exp(0.5j * tau * k**2), axis=-1)
        record('inverse_unsqueeze_then_free', recovered - initial)

        matrix = transformation(tau, r)
        evolved_grid = evolve_points(grid, tau, r)
        record('matrix_determinant', np.linalg.det(matrix) - 1.0)
        record('each_grid_cell_area', _cell_areas(evolved_grid) - initial_areas)
        corners = evolve_points(INITIAL_CORNERS, tau, r)
        record('patch_area', _polygon_area(corners) - PATCH_AREA)
        # U^{-1} reverses the order: first inverse squeeze, then inverse shear.
        unsqueezed_points = evolve_points(evolved_grid, 0.0, -r)
        recovered_points = evolve_points(unsqueezed_points, -tau, 0.0)
        record('inverse_point_map', recovered_points - grid)
        boundary_amplitude = max(boundary_amplitude,
                                 float(np.max(np.abs(psi[:, [0, -1]]))))
        if tau >= 0.0 and r >= 0.0:
            real_peaks = np.maximum(real_peaks, np.max(np.abs(psi.real), axis=-1))
            complex_peaks = np.maximum(complex_peaks, np.max(np.abs(psi), axis=-1))
        if ((tau, r) in ((0.0, 0.0), (TAU_MAX, 0.0), (TAU_MAX, R_MAX))):
            samples.append({'tau': tau, 'r': r, 'means': predicted.tolist(),
                            'norm_squared': np.diag(gram).real.tolist()})

    tolerance = 5e-11
    result = {
        'passed': bool(max(errors.values()) < tolerance),
        'model': 'Six normalized Weyl Gaussian states under one common unitary',
        'operators': 'hbar=1; X=x; K=-i*d/dx',
        'sigma': SIGMA,
        'initial_shear': INITIAL_SHEAR,
        'initial_samples': INITIAL_SAMPLES.tolist(),
        'initial_patch_corners': INITIAL_CORNERS.tolist(),
        'initial_patch_area': PATCH_AREA,
        'common_unitary': 'U(tau,r)=S(r)*exp(-i*tau*K^2/2)',
        'squeeze': '(S(r)*psi)(x)=exp(-r/2)*psi(exp(-r)*x)',
        'mean_map': 'diag(exp(r),exp(-r)) @ [[1,tau],[0,1]]',
        'inverse_order': 'U^-1=exp(+i*tau*K^2/2)*S(-r)',
        'normalization': 'Analytic initial normalization; no per-frame normalization',
        'phase': 'Complete complex phases retained in every state and overlap',
        'initial_complex_gram': {'real': expected_gram.real.tolist(),
                                 'imaginary': expected_gram.imag.tolist()},
        'errors': errors,
        'tolerance': tolerance,
        'quadrature': {'x_domain': [-24.0, 24.0], 'points': count,
                       'dx': dx, 'parameter_pairs': len(parameters),
                       'tau_range': [0.0, TAU_MAX], 'r_range': [0.0, R_MAX],
                       'negative_parameter_pairs': 4,
                       'momentum_derivative': 'FFT spectral derivative'},
        'grid': {'nu': grid.shape[1] - 1, 'nv': grid.shape[0] - 1,
                  'cells': int(initial_areas.size)},
        'maximum_boundary_amplitude': boundary_amplitude,
        'sampled_real_component_peaks': real_peaks.tolist(),
        'sampled_complex_magnitude_peaks': complex_peaks.tolist(),
        'samples': samples,
        'source': Path(__file__).relative_to(ROOT).as_posix(),
    }
    if not result['passed']:
        raise AssertionError(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate', action='store_true',
                        help='Run validation (the default action).')
    parser.add_argument('--output', type=Path, default=VALIDATION_PATH,
                        help='Validation report path; relative paths use the repository root.')
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'errors': result['errors'],
                      'output': str(output)}, indent=2))
