"""Exact finite periodic Weyl basis for the operator-completeness animation.

WARNING: this is the FINITE, periodic analogue of position and momentum
displacements.  It is not an exact finite-dimensional realization of
[X, K] = i I, which is impossible by taking the trace.  The continuum limit
shown by a renderer is schematic; this module proves the finite statement.

For sample indices j=0,...,n-1 and integer displacement indices a,b,
    (Tx(a) psi)[j] = psi[(j-a) % n]
    (Tk(b) psi)[j] = exp(2 pi i b j/n) psi[j]
    W(a,b) = Tk(b) Tx(a).
Every complex n-by-n matrix has the exact expansion
    A = sum_{a,b} c[a,b] W(a,b),
    c[a,b] = fft(A[j,(j-a) % n], over j)[b] / n.

The weights and coefficients depend on A, never on the input vector.
Importing this module writes no files.  Only the explicit --check command
writes the validation JSON, at a path resolved relative to this repository.
"""
from __future__ import annotations

import argparse
from collections.abc import Iterable
import json
import operator
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np

N = 8
SAMPLE_INDICES = np.arange(N)
# Plot coordinates only.  The phases below use integer indices j, not these.
SAMPLE_POS = SAMPLE_INDICES.astype(float) - (N - 1) / 2
# Storage order matches numpy.fft.fft; negative labels denote modular indices.
FREQS = np.array([0, 1, 2, 3, -4, -3, -2, -1])
SHIFT_LABELS = FREQS.copy()
ALL_TERMS = tuple((a, b) for a in range(N) for b in range(N))

# Fixed real, dense, asymmetric example.  Both signs occur in each row and
# every modular diagonal.  Its condition number is about 2.309 and all 64
# displacement coefficients are nonzero.  It is a generic linear operator,
# not a unitary operator: no norm preservation is implied for A psi.
TARGET_MATRIX = 0.9 * np.array([
    [ .372,  .804,  .452,  .048,  .374,  .299, -.153, -.286],
    [ .235,  .454, -.317,  .829,  .171,  .031, -.149, -.077],
    [ .101, -.490,  .457,  .435, -.578,  .593,  .101, -.029],
    [-.305, -.123,  .523,  .275, -.045, -.721,  .340,  .285],
    [ .176, -.257,  .580, -.199,  .234, -.545, -.690, -.259],
    [-.312,  .634,  .002, -.245, -.483, -.289, -.306, -.072],
    [ .634,  .331, -.023,  .138, -.343, -.435, -.153,  .572],
    [-.769, -.077,  .164, -.066,  .390,  .344, -.322,  .612],
], dtype=float)

# Visibly different inputs; normalization is performed only at construction.
INPUT_NAMES = ('localized packet', 'signed two-lobe pattern')
INPUT_VECTORS = np.array([
    [0.04, 0.20, 0.60, 1.00, 0.78, 0.32, 0.08, 0.02],
    [0.52, 0.92, 0.38, -0.44, -0.88, -0.30, 0.48, 0.16],
], dtype=float)
INPUT_VECTORS /= np.linalg.norm(INPUT_VECTORS, axis=1, keepdims=True)

VALIDATION_PATH = (ROOT / 'content/drafts/animations'
                   / 'symmetry-operator-completeness-validation.json')
VALIDATION_TOLERANCE = 1e-11

for _constant in (SAMPLE_INDICES, SAMPLE_POS, FREQS, SHIFT_LABELS,
                  TARGET_MATRIX, INPUT_VECTORS):
    _constant.setflags(write=False)

__all__ = [
    'N', 'SAMPLE_INDICES', 'SAMPLE_POS', 'FREQS', 'SHIFT_LABELS', 'ALL_TERMS',
    'TARGET_MATRIX', 'INPUT_NAMES', 'INPUT_VECTORS', 'VALIDATION_PATH',
    'shift_matrix', 'phase_matrix', 'displacement', 'band_weights',
    'coefficients', 'reconstruct', 'validate',
]


def _size(n: int) -> int:
    n = operator.index(n)
    if n < 1:
        raise ValueError('matrix size must be positive')
    return n


def _square(values, name: str) -> np.ndarray:
    values = np.asarray(values, dtype=complex)
    if (values.ndim != 2 or values.shape[0] != values.shape[1]
            or values.shape[0] == 0):
        raise ValueError(f'{name} must be a nonempty square matrix')
    if not np.isfinite(values).all():
        raise ValueError(f'{name} must contain only finite values')
    return values


def shift_matrix(a: int, n: int = N) -> np.ndarray:
    """Return Tx(a): positive a moves input sample j to output (j+a) % n."""
    n = _size(n)
    a = operator.index(a) % n
    rows = np.arange(n)
    result = np.zeros((n, n), dtype=complex)
    result[rows, (rows - a) % n] = 1.0
    return result


def phase_matrix(b: int, n: int = N) -> np.ndarray:
    """Return Tk(b), with the positive-exponent Fourier convention."""
    n = _size(n)
    b = operator.index(b) % n
    return np.diag(np.exp(2j * np.pi * b * np.arange(n) / n))


def displacement(a: int, b: int, n: int = N) -> np.ndarray:
    """Return W(a,b)=Tk(b) Tx(a): first shift, then phase multiplication."""
    return phase_matrix(b, n) @ shift_matrix(a, n)


def band_weights(matrix) -> np.ndarray:
    """Return weights[a,j]=matrix[j,(j-a)%n], shape (displacement, sample).

    The a-th modular diagonal is diag(weights[a]) @ Tx(a).  The periodic
    wrap is part of the finite model, not a discarded edge effect.
    """
    matrix = _square(matrix, 'matrix')
    n = matrix.shape[0]
    a, j = np.arange(n)[:, None], np.arange(n)[None, :]
    return matrix[j, (j - a) % n]


def coefficients(matrix) -> np.ndarray:
    """Return c[a,b] for matrix=sum c[a,b] Tk(b) Tx(a).

    The forward FFT uses the negative exponent; dividing it by n supplies
    coefficients for reconstruction with positive-exponent phase patterns.
    """
    weights = band_weights(matrix)
    return np.fft.fft(weights, axis=1) / weights.shape[1]


def reconstruct(c, terms: Iterable[tuple[int, int]] | None = None) -> np.ndarray:
    """Sum selected c[a,b] W(a,b), or all terms when terms is None.

    Terms are (a,b) pairs, accepting either signed labels or modular indices.
    An empty iterable returns zero.  Repeated pairs are added repeatedly.
    The returned matrix is complex: partial sums need not be real, even when
    the complete reconstructed target is real.
    """
    c = _square(c, 'coefficients')
    n = c.shape[0]
    if terms is None:
        terms = ((a, b) for a in range(n) for b in range(n))
    result = np.zeros((n, n), dtype=complex)
    for a, b in terms:
        a, b = operator.index(a) % n, operator.index(b) % n
        result += c[a, b] * displacement(a, b, n)
    return result


def validate() -> dict:
    """Check the finite basis against independent matrix and state actions.

    This function returns a report and performs no filesystem writes.
    The Gram matrix verifies independence of all n**2 basis operators;
    direct matrix-unit reconstruction and random complex matrices exercise
    completeness beyond the single real target used by the animation.
    """
    tol = VALIDATION_TOLERANCE
    identity = np.eye(N, dtype=complex)
    basis = np.array([displacement(a, b) for a, b in ALL_TERMS])
    flat = basis.reshape(N * N, N * N)
    gram = flat.conj() @ flat.T / N
    c = coefficients(TARGET_MATRIX)
    recovered = reconstruct(c)
    weights = band_weights(TARGET_MATRIX)
    rng = np.random.default_rng(620853)
    random_states = rng.normal(size=(128, N)) + 1j * rng.normal(size=(128, N))
    random_states /= np.linalg.norm(random_states, axis=1, keepdims=True)
    all_states = np.concatenate((INPUT_VECTORS.astype(complex), random_states))
    checks = {}

    def check(name, error):
        error = float(error)
        checks[name] = {'max_abs_error': error, 'passed': error < tol}

    check('hilbert_schmidt_gram', np.max(np.abs(gram - np.eye(N * N))))
    check('basis_unitarity', max(
        np.max(np.abs(w.conj().T @ w - identity)) for w in basis))
    check('target_reconstruction', np.max(np.abs(recovered - TARGET_MATRIX)))
    # Independent coefficient extraction uses the Hilbert-Schmidt inner product.
    trace_coefficients = np.array([
        np.trace(w.conj().T @ TARGET_MATRIX) / N for w in basis]).reshape(N, N)
    check('fft_coefficients_vs_trace', np.max(np.abs(c - trace_coefficients)))

    band_error = 0.0
    band_sum = np.zeros_like(identity)
    for a in range(N):
        expected = np.zeros_like(identity)
        for j in range(N):
            expected[j, (j - a) % N] = TARGET_MATRIX[j, (j - a) % N]
        actual = reconstruct(c, ((a, b) for b in range(N)))
        band_error = max(band_error, float(np.max(np.abs(actual - expected))))
        band_sum += np.diag(weights[a]) @ shift_matrix(a)
    check('each_band_reconstruction', band_error)
    check('weighted_shift_band_sum', np.max(np.abs(band_sum - TARGET_MATRIX)))

    # Compare reconstructed action with direct dense multiplication, using the
    # two visible inputs and 128 independent complex states, not just one fit.
    direct_actions = (TARGET_MATRIX @ all_states.T).T
    reconstructed_actions = (recovered @ all_states.T).T
    check('operator_action_130_states',
          np.max(np.abs(reconstructed_actions - direct_actions)))
    alpha, beta = 0.37 + 0.61j, -0.42 + 0.19j
    combined = alpha * random_states[0] + beta * random_states[1]
    expected_combined = (alpha * (TARGET_MATRIX @ random_states[0])
                         + beta * (TARGET_MATRIX @ random_states[1]))
    check('complex_linearity', np.max(np.abs(recovered @ combined - expected_combined)))

    # Directly inspect column action, independent of shift_matrix's row indexing.
    shift_error = 0.0
    weyl_error = 0.0
    loop_error = 0.0
    for a in range(N):
        for j in range(N):
            expected = np.zeros(N, dtype=complex)
            expected[(j + a) % N] = 1
            shift_error = max(shift_error, float(np.max(
                np.abs(shift_matrix(a) @ identity[:, j] - expected))))
        for b in range(N):
            tx, tk = shift_matrix(a), phase_matrix(b)
            weyl_error = max(weyl_error, float(np.max(np.abs(
                tx @ tk - np.exp(-2j * np.pi * a * b / N) * tk @ tx))))
            loop = tk @ tx @ phase_matrix(-b) @ shift_matrix(-a)
            loop_error = max(loop_error, float(np.max(np.abs(
                loop - np.exp(2j * np.pi * a * b / N) * identity))))
    check('positive_shift_column_action', shift_error)
    check('finite_weyl_relation', weyl_error)
    check('finite_loop_uniform_phase', loop_error)

    matrix_unit_error = 0.0
    for row in range(N):
        for col in range(N):
            unit = np.zeros_like(identity)
            unit[row, col] = 1
            matrix_unit_error = max(matrix_unit_error, float(np.max(
                np.abs(reconstruct(coefficients(unit)) - unit))))
    check('all_64_matrix_units', matrix_unit_error)
    random_matrix_error = 0.0
    for _ in range(16):
        matrix = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        random_matrix_error = max(random_matrix_error, float(np.max(
            np.abs(reconstruct(coefficients(matrix)) - matrix))))
    check('16_random_complex_matrices', random_matrix_error)
    check('real_target_coefficient_conjugacy', max(
        np.max(np.abs(c[:, (-b) % N] - c[:, b].conj())) for b in range(N)))
    check('visible_input_normalization',
          np.max(np.abs(np.linalg.norm(INPUT_VECTORS, axis=1) - 1)))

    return {
        'model': 'exact finite periodic Weyl operator basis',
        'continuum_caveat': (
            'Finite periodic analogue only; no finite exact [X,K]=iI is claimed. '
            'Any continuum limit displayed by the animation is schematic.'),
        'n': N,
        'basis_operator_count': N * N,
        'complex_matrix_space_dimension': N * N,
        'convention': 'Tx(a)psi[j]=psi[(j-a)%N]; Tk(b)psi[j]=exp(2pi*i*b*j/N)psi[j]',
        'coefficient_convention': 'c[a,b]=fft(A[j,(j-a)%N], over j)[b]/N',
        'partial_sums_may_be_complex': True,
        'target_is_unitary': False,
        'target_max_absolute_entry': float(np.max(np.abs(TARGET_MATRIX))),
        'target_condition_number': float(np.linalg.cond(TARGET_MATRIX)),
        'target_max_asymmetry': float(np.max(np.abs(TARGET_MATRIX - TARGET_MATRIX.T))),
        'minimum_coefficient_magnitude': float(np.min(np.abs(c))),
        'nonzero_coefficient_count': int(np.count_nonzero(np.abs(c) > tol)),
        'selected_band_a2_weights': weights[2].real.tolist(),
        'input_names': list(INPUT_NAMES),
        'random_complex_states_checked': len(random_states),
        'random_complex_matrices_checked': 16,
        'tolerance': tol,
        'checks': checks,
        'passed': all(result['passed'] for result in checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='validate the finite model and write its JSON report')
    args = parser.parse_args()
    if not args.check:
        parser.print_help()
        return 0
    report = validate()
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'],
                      'checks': len(report['checks']),
                      'report': VALIDATION_PATH.relative_to(ROOT).as_posix()}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
