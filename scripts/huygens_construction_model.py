"""A coherent Huygens construction from localized elements of one free wave.

This model decomposes one unchanged plane wave. The reveal selects terms of its
complex amplitude; it does not insert physical apertures or switch sources on.
Smooth localized weights plus an outside-view remainder form a partition of
unity on the entire numerical plane. All terms retain the incident phase and
use the same normalized forward angular-spectrum propagator and time clock.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
import json
import math
from pathlib import Path
import sys

LOCAL = Path(__file__).resolve().parents[1] / ".tools" / "animation-python-packages"
if LOCAL.is_dir():
    sys.path.insert(0, str(LOCAL))
import numpy as np

WIDTH, HEIGHT, FPS = 1280, 720, 24
BOX = (40, 80, 1240, 680)
DURATION = 40.0
X_MAX = 14.4
VIEW_HALF_HEIGHT = 3.6
CONSTRUCTION_X = 3.2
SOURCE_X = 0.0
ENDPOINT_X, ENDPOINT_Y = X_MAX, 0.0
WAVELENGTH = 0.9
K = 2.0 * math.pi / WAVELENGTH
WAVE_PERIOD = 3.0
ELEMENT_SPACING = 0.64
ELEMENT_SIGMA = 0.20
ELEMENT_INDICES = np.arange(-5, 6)
ELEMENT_CENTERS = ELEMENT_INDICES * ELEMENT_SPACING
REMAINDER_INDEX = len(ELEMENT_INDICES)
N_GROUPS = REMAINDER_INDEX + 1


def ease(value):
    value = float(np.clip(value, 0.0, 1.0))
    return value * value * (3.0 - 2.0 * value)


def temporal_phase(seconds):
    return complex(np.exp(-2j * np.pi * seconds / WAVE_PERIOD))


def group_index(element_index):
    return int(element_index + 5)


def coefficients_at(seconds):
    """Visual selection of terms; the underlying complete field stays fixed."""
    result = np.ones(N_GROUPS)
    if seconds < 6.0:
        return result
    if seconds < 8.0:
        result *= 1.0 - ease((seconds - 6.0) / 2.0)
        result[group_index(0)] = 1.0
        return result
    result[:] = 0.0
    result[group_index(0)] = 1.0
    pair = ease((seconds - 11.0) / 2.0)
    result[group_index(-3)] = pair
    result[group_index(3)] = pair
    # Fill the gaps symmetrically; no individual element has a new clock.
    for begin, pair_indices in ((16.0, (-1, 1)), (17.8, (-2, 2)),
                                 (19.6, (-4, 4)), (21.4, (-5, 5))):
        amount = ease((seconds - begin) / 1.6)
        for index in pair_indices:
            result[group_index(index)] = amount
    result[REMAINDER_INDEX] = ease((seconds - 23.0) / 5.0)
    return result


def label_at(seconds):
    if seconds < 4:
        return "A plane wave"
    if seconds < 6:
        return "One wavefront"
    if seconds < 11:
        return "One secondary contribution"
    if seconds < 16:
        return "Neighboring parts contribute"
    if seconds < 28:
        return "Their amplitudes add"
    if seconds < 32:
        return "The wavefront is reconstructed"
    return "The wavefront advances"


def selection_caption_at(seconds):
    if 23.0 <= seconds < 28.0:
        return "including the remaining wavefront"
    if np.any(coefficients_at(seconds) < 1.0 - 1e-10):
        return "selected contributions to the same wave"
    return "the complete wave"


def construction_visibility(seconds):
    return ease((seconds - 4.0) / 1.5) * (1.0 - ease((seconds - 30.0) / 2.0))


def tracked_front_x(seconds):
    """A real positive crest, kx-wt=-12pi, followed in the final section."""
    return WAVELENGTH * (seconds / WAVE_PERIOD - 6.0)


def tracking_visibility(seconds):
    return ease((seconds - 32.0) / 1.0)


@dataclass(frozen=True)
class HuygensModel:
    n: int = 16384
    period: float = 512.0

    @property
    def dy(self):
        return self.period / self.n

    @cached_property
    def y(self):
        return (np.arange(self.n) - self.n // 2) * self.dy

    @cached_property
    def q(self):
        return 2 * np.pi * np.fft.fftfreq(self.n, self.dy)

    @cached_property
    def kx(self):
        return np.sqrt((K * K - self.q * self.q).astype(complex))

    @cached_property
    def weights(self):
        if abs(self.period / ELEMENT_SPACING - round(self.period / ELEMENT_SPACING)) > 1e-8:
            raise ValueError("The periodic domain must contain an integer number of elements")
        residual = (self.y + ELEMENT_SPACING / 2) % ELEMENT_SPACING - ELEMENT_SPACING / 2
        denominator = sum(np.exp(-0.5 * ((residual - j * ELEMENT_SPACING) / ELEMENT_SIGMA) ** 2)
                          for j in range(-3, 4))
        visible = []
        for center in ELEMENT_CENTERS:
            distance = (self.y - center + self.period / 2) % self.period - self.period / 2
            visible.append(np.exp(-0.5 * (distance / ELEMENT_SIGMA) ** 2) / denominator)
        visible = np.asarray(visible)
        remainder = np.maximum(0.0, 1.0 - visible.sum(axis=0))
        weights = np.vstack((visible, remainder))
        # Remove machine-roundoff drift while keeping all groups nonnegative.
        return weights / weights.sum(axis=0)

    def propagate(self, field, distance):
        if distance < 0:
            raise ValueError("Only forward propagation is defined")
        return np.fft.ifft(np.fft.fft(field, axis=-1)
                           * np.exp(1j * distance * self.kx), axis=-1)

    @cached_property
    def incident_phase(self):
        return complex(np.exp(1j * K * CONSTRUCTION_X))

    def contributions_at(self, x):
        """One complete complex field per partition element, before time phase."""
        return self.propagate(self.weights * self.incident_phase, x - CONSTRUCTION_X)

    def endpoint_contributions(self, x=ENDPOINT_X, y=ENDPOINT_Y):
        """Exact spectral evaluation at an endpoint, including non-grid y."""
        spectra = np.fft.fft(self.weights * self.incident_phase, axis=-1)
        phase = np.exp(1j * (x - CONSTRUCTION_X) * self.kx)
        sample = np.exp(1j * self.q * (y - self.y[0]))
        return np.sum(spectra * phase * sample, axis=-1) / self.n

    def field_at(self, x, coefficients=None):
        if coefficients is None:
            return np.full(self.n, np.exp(1j * K * x), complex)
        source = np.asarray(coefficients) @ self.weights
        return self.propagate(source * self.incident_phase, x - CONSTRUCTION_X)


class FieldSampler:
    def __init__(self, model, width=800):
        self.model = model
        self.x = np.linspace(0, X_MAX, width)
        self.indices = np.flatnonzero(np.abs(model.y) <= VIEW_HALF_HEIGHT)
        self.y = model.y[self.indices]
        self.right = np.flatnonzero(self.x >= CONSTRUCTION_X)
        self.plane = np.broadcast_to(np.exp(1j * K * self.x), (len(self.y), width)).copy()
        self.fields = np.zeros((N_GROUPS, len(self.y), len(self.right)), complex)
        spectra = np.fft.fft(model.weights * model.incident_phase, axis=-1)
        # Chunk longitudinal samples so no dense global transfer matrix exists.
        for start in range(0, len(self.right), 24):
            columns = self.right[start:start + 24]
            kernel = np.exp(1j * (self.x[columns] - CONSTRUCTION_X)[:, None] * model.kx[None, :])
            for group in range(N_GROUPS):
                values = np.fft.ifft(spectra[group][None, :] * kernel, axis=-1)
                self.fields[group, :, start:start + len(columns)] = values[:, self.indices].T

    def sample(self, coefficients):
        field = self.plane.copy()
        right = np.zeros_like(self.fields[0])
        for weight, contribution in zip(coefficients, self.fields):
            right += weight * contribution
        field[:, self.right] = right
        return field


def run_checks():
    model = HuygensModel()
    partition_error = float(np.max(np.abs(model.weights.sum(axis=0) - 1)))
    groups = model.endpoint_contributions()
    expected = np.exp(1j * K * ENDPOINT_X)
    full_error = float(abs(groups.sum() - expected))
    source_sum = model.contributions_at(ENDPOINT_X).sum(axis=0)
    whole_plane_error = float(np.max(np.abs(source_sum - expected)))
    clock_error = float(abs(groups.sum() * temporal_phase(17.31)
                            - expected * temporal_phase(17.31)))
    result = {"partition_of_unity_error": partition_error,
              "endpoint_sum_error": full_error, "whole_plane_sum_error": whole_plane_error,
              "common_clock_error": clock_error, "minimum_weight": float(model.weights.min()),
              "remainder_center_magnitude": float(abs(groups[REMAINDER_INDEX])),
              "initial_final_selection_identical": bool(np.array_equal(coefficients_at(0), coefficients_at(39)))}
    assert partition_error < 1e-14 and full_error < 1e-12 and whole_plane_error < 1e-12
    assert result["minimum_weight"] >= 0 and result["initial_final_selection_identical"]
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run_checks()
