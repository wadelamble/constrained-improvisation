"""Continuous screen buildup with complete local wavelet partitions.

All distances use the established scalar angular-spectrum model. This module
changes the aperture sequence and timing, never the normalized propagator.
Visible bins plus the outside-view remainder partition every numerical cell.
"""
from __future__ import annotations

from functools import cached_property

from plane_wave_screens_model import (
    np, WaveScreensModel as OriginalModel, FieldSampler, SCREEN_X,
    WAVELENGTH, K, X_MAX, VIEW_HALF_HEIGHT, FPS, temporal_phase, ease,
)

DURATION = 52.0
TRANSITIONS = tuple((2.0 + 4 * (stage - 1),
                     2.0 + 4 * (stage - 1) + (2.0 if stage == 12 else 1.4),
                     stage) for stage in range(1, 13))
COARSE_CENTERS = {
    1: np.array([0.0]),
    2: np.array([-0.9, 0.0, 0.9]),
    3: np.arange(-3, 4) * 0.45,
    4: np.arange(-7, 8) * 0.45,
}
SCREEN_SETS = {
    0: (), 1: (0,), 2: (0,), 3: (0,), 4: (0,), 5: (0,),
    6: (0, 14), 7: (0, 7, 14), 8: (0, 3, 7, 11, 14),
    9: (0, 1, 3, 5, 7, 9, 11, 13, 14),
    10: tuple(range(15)), 11: tuple(range(15)), 12: tuple(range(15)),
}
COMBS = {stage: (0.225, 0.995, SCREEN_SETS[stage]) for stage in range(5, 11)}
COMBS[11] = (0.1125, 0.9995, SCREEN_SETS[11])
LABELS = (
    "Plane wave", "1 screen · 1 slit", "1 screen · 3 slits",
    "1 screen · 7 slits", "1 screen · 15 slits", "1 screen · dense slits",
    "2 screens · dense slits", "3 screens · dense slits",
    "5 screens · dense slits", "9 screens · dense slits",
    "15 screens · dense slits", "15 screens · finer slits",
    "Open slices · the same plane wave",
)


def state_at(seconds):
    previous = 0
    for begin, end, target in TRANSITIONS:
        if seconds < begin:
            return previous, previous, 0.0
        if seconds < end:
            return previous, target, ease((seconds - begin) / (end - begin))
        previous = target
    return previous, previous, 0.0


def label_at(seconds):
    a, b, _ = state_at(seconds)
    if a != b and b == 12:
        return "Opening the remaining barriers"
    return LABELS[b]


def group_centers(seconds):
    """One bin per visible opening; refine the basis when new slits appear.

    Basis refinement is an explanatory change. The complete coherent field
    does not depend on which partition is used.
    """
    a, b, _ = state_at(seconds)
    stage = max(a, b)
    if stage in COARSE_CENTERS:
        return COARSE_CENTERS[stage].copy()
    pitch = 0.1125 if stage >= 11 else 0.225
    count = round(VIEW_HALF_HEIGHT / pitch)
    return np.arange(-count, count + 1) * pitch


def bin_edges(centers):
    centers = np.asarray(centers)
    if len(centers) == 1:
        return np.array([-VIEW_HALF_HEIGHT - 0.1125,
                         VIEW_HALF_HEIGHT + 0.1125])
    middle = (centers[:-1] + centers[1:]) / 2
    edges = np.r_[centers[0] - (centers[1] - centers[0]) / 2,
                  middle, centers[-1] + (centers[-1] - centers[-2]) / 2]
    if len(centers) <= 15:
        # During insertion the nominally opaque area can still transmit.
        # Keep that whole visible field in the displayed partition, not in
        # a remainder misleadingly called "outside view".
        edges[0] = min(edges[0], -VIEW_HALF_HEIGHT - 0.1125)
        edges[-1] = max(edges[-1], VIEW_HALF_HEIGHT + 0.1125)
    return edges


class WaveScreensModel(OriginalModel):
    @cached_property
    def targets(self):
        masks = np.ones((13, len(SCREEN_X), self.n))
        for stage, centers in COARSE_CENTERS.items():
            masks[stage, 0] = self.openings(centers, 0.24)
        for stage, (pitch, fill, screens) in COMBS.items():
            masks[stage, list(screens)] = self.comb(pitch, fill)
        return masks

    def masks_at(self, seconds):
        a, b, amount = state_at(seconds)
        if a == b:
            return self.targets[a]
        return (1 - amount) * self.targets[a] + amount * self.targets[b]

    def group_indices(self, seconds):
        """Visible aperture bins followed by the exact off-view remainder.

        Assign whole numerical cells, including partially transmitting cells,
        once each. Transmission has already been cell-averaged by the model.
        """
        centers = group_centers(seconds)
        edges = bin_edges(centers)
        labels = np.searchsorted(edges, self.y, side="right") - 1
        visible = (labels >= 0) & (labels < len(centers))
        groups = [np.flatnonzero(visible & (labels == i))
                  for i in range(len(centers))]
        groups.append(np.flatnonzero(~visible))
        return groups

    def group_masks(self, seconds):
        groups = self.group_indices(seconds)
        masks = np.zeros((len(groups), self.n))
        for row, indices in enumerate(groups):
            masks[row, indices] = 1.0
        return masks

    def grouped_inputs(self, boundary, seconds):
        return self.group_masks(seconds) * np.asarray(boundary)[None, :]


if __name__ == "__main__":
    import json
    model = WaveScreensModel()
    partition_error = 0.0
    for t in (4, 8, 12, 16, 20, 24, 32, 40, 44, 50):
        partition_error = max(partition_error,
                              float(np.max(abs(model.group_masks(t).sum(axis=0) - 1))))
    free_error = float(np.max(abs(model.field_at(X_MAX, model.targets[12])
                                  - np.exp(1j * K * X_MAX))))
    assert partition_error == 0 and free_error < 1e-12
    print(json.dumps({"partition_error": partition_error,
                      "free_plane_complex_error": free_error,
                      "intro_seconds": 2, "duration_seconds": DURATION,
                      "dense_visible_groups": len(group_centers(20)),
                      "fine_visible_groups": len(group_centers(44))}, indent=2))
