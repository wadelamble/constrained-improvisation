"""Forward scalar diffraction through thin transmission screens.

The incident field is a unit plane wave. Exact angular-spectrum propagation
includes its carrier phase and evanescent decay. Screens multiply the complex
field by real transmission masks; no stage-dependent renormalization is used.
The transverse FFT domain is periodic and substantially larger than the view.
Changing masks depicts successive monochromatic steady states, not a causal
simulation of the transient caused by inserting a physical screen.
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

WAVELENGTH = 0.72
K = 2 * math.pi / WAVELENGTH
X_MAX = 14.4
VIEW_HALF_HEIGHT = 3.6
SCREEN_X = np.linspace(3.0, 11.0, 15)
DURATION = 52.0
WAVE_PERIOD = 3.0
FPS = 24
SOURCE_X = 0.0
ENDPOINT_X = X_MAX
ENDPOINT_Y = 0.0
# A transition starts at the first time and reaches its target at the second.
TRANSITIONS = ((5.0, 7.0, 1), (10.0, 12.0, 2), (14.5, 17.0, 3),
               (19.5, 22.0, 4), (24.5, 28.0, 5), (30.0, 32.0, 6),
               (34.0, 36.0, 7), (38.0, 40.0, 8), (42.0, 46.0, 9))
LABELS = ("Plane wave", "1 screen · 1 slit", "1 screen · 3 slits",
          "1 screen · 7 slits", "1 screen · 15 slits", "The barrier opens away",
          "3 screens · many slits", "7 screens · finer slits",
          "15 screens · nearly open", "Open slices · the same plane wave")


def ease(x: float) -> float:
    x = float(np.clip(x, 0.0, 1.0))
    return x * x * (3.0 - 2.0 * x)


def temporal_phase(seconds: float) -> complex:
    """Multiply the spatial field by this shared e^-iwt clock factor."""
    return complex(np.exp(-2j * np.pi * seconds / WAVE_PERIOD))


def state_at(seconds: float) -> tuple[int, int, float]:
    previous = 0
    for begin, end, target in TRANSITIONS:
        if seconds < begin:
            return previous, previous, 0.0
        if seconds < end:
            return previous, target, ease((seconds - begin) / (end - begin))
        previous = target
    return previous, previous, 0.0


def label_at(seconds: float) -> str:
    """Only claim complete recovery after every physical mask is identity."""
    if 42.0 <= seconds < 46.0:
        return "Opening the remaining barriers"
    a, b, _ = state_at(seconds)
    return LABELS[b if a != b else a]


@dataclass(frozen=True)
class WaveScreensModel:
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
        return 2.0 * np.pi * np.fft.fftfreq(self.n, d=self.dy)

    @cached_property
    def kx(self):
        return np.sqrt((K * K - self.q * self.q).astype(complex))

    def propagate(self, field: np.ndarray, distance: float):
        if distance < 0:
            raise ValueError("Forward propagation requires a nonnegative distance")
        return np.fft.ifft(np.fft.fft(field) * np.exp(1j * distance * self.kx))

    def openings(self, centers, width):
        """Cell-averaged exact overlap of nonoverlapping interval apertures."""
        left, right = self.y - self.dy / 2, self.y + self.dy / 2
        mask = np.zeros(self.n)
        for center in centers:
            overlap = np.maximum(0.0, np.minimum(right, center + width / 2)
                                 - np.maximum(left, center - width / 2))
            mask += overlap / self.dy
        return np.clip(mask, 0.0, 1.0)

    def comb(self, pitch: float, fill: float):
        if fill >= 1.0:
            return np.ones(self.n)
        # Exact integrated periodic indicator, with one opening centered at 0.
        # Its phase is independent of computational padding. Cell averaging
        # resolves opaque remnants smaller than one mesh cell.
        width = pitch * fill
        def integral(y):
            shifted = y + width / 2
            turns = np.floor(shifted / pitch)
            remainder = shifted - turns * pitch
            return turns * width + np.minimum(remainder, width)
        return np.clip((integral(self.y + self.dy / 2)
                        - integral(self.y - self.dy / 2)) / self.dy, 0.0, 1.0)

    @cached_property
    def targets(self):
        masks = np.ones((10, len(SCREEN_X), self.n))
        centers = ((0.0,), (-0.9, 0.0, 0.9), np.arange(-3, 4) * 0.45,
                   np.arange(-7, 8) * 0.45)
        for stage, positions in enumerate(centers, 1):
            masks[stage, 0] = self.openings(positions, 0.24)
        masks[6, (0, 7, 14), :] = self.comb(0.45, 0.86)
        masks[7, (0, 3, 5, 7, 9, 11, 14), :] = self.comb(0.225, 0.97)
        masks[8, :, :] = self.comb(0.1125, 0.995)
        return masks

    def masks_at(self, seconds):
        a, b, amount = state_at(seconds)
        if a == b:
            return self.targets[a]
        return self.targets[a] + amount * (self.targets[b] - self.targets[a])

    def screen_fields(self, masks):
        result = []
        field = np.ones(self.n, complex)
        previous = 0.0
        for position, mask in zip(SCREEN_X, masks):
            field = self.propagate(field, position - previous) * mask
            result.append(field)
            previous = position
        return result

    def field_at(self, x, masks):
        field = np.ones(self.n, complex)
        previous = 0.0
        for position, mask in zip(SCREEN_X, masks):
            if position > x:
                break
            field = self.propagate(field, position - previous) * mask
            previous = position
        return self.propagate(field, x - previous)


class FieldSampler:
    """Cache distance kernels; recompute actual field for every aperture state."""
    def __init__(self, model: WaveScreensModel, width=800):
        self.model = model
        self.x = np.linspace(0.0, X_MAX, width)
        self.indices = np.flatnonzero(np.abs(model.y) <= VIEW_HALF_HEIGHT)
        self.y = model.y[self.indices]
        self.sections = []
        edges = np.r_[0.0, SCREEN_X, X_MAX + 1e-8]
        for i, (start, end) in enumerate(zip(edges[:-1], edges[1:])):
            columns = np.flatnonzero((self.x >= start) & (self.x < end))
            # Keep each transverse FFT contiguous in memory.
            kernel = np.exp(1j * (self.x[columns] - start)[:, None] * model.kx[None, :])
            self.sections.append((columns, kernel))

    def sample(self, masks):
        model = self.model
        boundary_fields = [np.ones(model.n, complex)] + model.screen_fields(masks)
        out = np.empty((len(self.indices), len(self.x)), complex)
        for (columns, kernel), boundary in zip(self.sections, boundary_fields):
            spectrum = np.fft.fft(boundary)
            field = np.fft.ifft(spectrum[None, :] * kernel, axis=1)
            out[:, columns] = field[:, self.indices].T
        return out


def run_checks():
    model = WaveScreensModel()
    unit = np.ones(model.n, complex)
    after = model.field_at(X_MAX, model.targets[9])
    plane_error = float(np.max(np.abs(after - np.exp(1j * K * X_MAX))))
    q_index = 3
    mode = np.exp(1j * model.q[q_index] * model.y)
    once = model.propagate(mode, 11.0)
    twice = model.propagate(model.propagate(mode, 4.0), 7.0)
    composition_error = float(np.max(np.abs(once - twice)))
    attenuated = model.field_at(X_MAX, model.targets[6])
    q0_error = float(np.max(np.abs(model.propagate(unit, 7.0) - np.exp(1j * K * 7))))
    result = {"plane_wave_full_complex_error": plane_error,
              "q0_phase_error": q0_error, "composition_error": composition_error,
              "three_screen_output_mean_magnitude": float(np.mean(np.abs(attenuated))),
              "minimum_transmission": float(model.targets.min()),
              "maximum_transmission": float(model.targets.max()),
              "first_last_masks_identical": bool(np.array_equal(model.targets[0], model.targets[9]))}
    assert plane_error < 1e-12 and q0_error < 1e-12 and composition_error < 1e-12
    assert result["first_last_masks_identical"]
    assert result["three_screen_output_mean_magnitude"] < 0.9
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run_checks()
