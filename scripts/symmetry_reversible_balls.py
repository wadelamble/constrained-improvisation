"""Exact free flight and elastic collision histories for the reversibility scene.

The two histories are independent systems.  Overlaying their samples never
introduces collisions between them.  Velocities in ``sample(t)`` are the
post-collision values at an event; positions are continuous.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/animation-python-packages'))
import numpy as np

BOX = (1.0, 0.66)
RADIUS = 0.022
DURATION = 8.0
BALL_COUNT = 8


@dataclass
class Event:
    time: float
    kind: str
    i: int
    j: int = -1
    axis: int = -1
    positions: np.ndarray | None = None
    velocities_before: np.ndarray | None = None
    velocities_after: np.ndarray | None = None


class History:
    """Piecewise affine positions, with an event log for every reflection."""

    def __init__(self, positions, velocities, duration=DURATION,
                 radius=RADIUS, box=BOX, name=''):
        self.initial_positions = np.array(positions, dtype=float, copy=True)
        self.initial_velocities = np.array(velocities, dtype=float, copy=True)
        self.duration = float(duration)
        self.radius = float(radius)
        self.box = np.array(box, dtype=float)
        self.name = name
        if (self.initial_positions.shape != self.initial_velocities.shape
                or self.initial_positions.ndim != 2
                or self.initial_positions.shape[1] != 2):
            raise ValueError('positions and velocities must both have shape (N, 2)')
        if self.duration <= 0 or self.radius <= 0:
            raise ValueError('duration and radius must be positive')
        if not (np.isfinite(self.initial_positions).all()
                and np.isfinite(self.initial_velocities).all()):
            raise ValueError('initial state must be finite')
        p = self.initial_positions
        if np.any(p < self.radius - 1e-12) or np.any(p > self.box-self.radius+1e-12):
            raise ValueError('initial positions must lie inside the box')
        for i in range(len(p)):
            for j in range(i+1, len(p)):
                if np.linalg.norm(p[j]-p[i]) < 2*self.radius-1e-12:
                    raise ValueError('initial disks overlap')
        self.events: list[Event] = []
        self._integrate()

    def _integrate(self):
        p = self.initial_positions.copy()
        v = self.initial_velocities.copy()
        t = 0.0
        times, positions, velocities = [t], [p.copy()], [v.copy()]
        for _ in range(10000):
            dt, collision = np.inf, None
            for i in range(len(p)):
                for axis in range(2):
                    if v[i, axis] == 0:
                        continue
                    edge = self.box[axis]-self.radius if v[i, axis] > 0 else self.radius
                    candidate = (edge-p[i, axis])/v[i, axis]
                    if -1e-12 <= candidate < dt:
                        dt, collision = max(0., candidate), ('wall', i, axis)
                for j in range(i+1, len(p)):
                    r, u = p[j]-p[i], v[j]-v[i]
                    b = float(r @ u)
                    if b >= -1e-15:
                        continue
                    a = float(u @ u)
                    c = float(r @ r)-(2*self.radius)**2
                    disc = b*b-a*c
                    if disc <= 0 or a == 0:
                        continue
                    # Rationalized near root avoids cancellation near contact.
                    candidate = c/(-b+np.sqrt(disc))
                    if -1e-12 <= candidate < dt:
                        dt, collision = max(0., candidate), ('ball', i, j)
            if collision is None or t+dt > self.duration:
                break
            p += v*dt
            t += dt
            before = v.copy()
            kind, i, other = collision
            if kind == 'wall':
                # Snap only rounding error in the solved contact coordinate.
                p[i, other] = self.box[other]-self.radius if v[i, other] > 0 else self.radius
                v[i, other] *= -1
                event = Event(t, kind, i, axis=other)
            else:
                normal = p[other]-p[i]
                normal /= np.linalg.norm(normal)
                exchange = float((v[i]-v[other]) @ normal)*normal
                v[i] -= exchange
                v[other] += exchange
                event = Event(t, kind, i, j=other)
            event.positions = p.copy()
            event.velocities_before = before
            event.velocities_after = v.copy()
            self.events.append(event)
            times.append(t)
            positions.append(p.copy())
            velocities.append(v.copy())
        else:
            raise RuntimeError('event budget exceeded; check simultaneous contacts')
        self.times = np.array(times)
        self.positions = np.array(positions)
        self.velocities = np.array(velocities)

    def sample(self, t):
        """Return positions and velocities at a scalar time or array of times."""
        t = np.asarray(t, dtype=float)
        if (not np.isfinite(t).all() or np.any(t < -1e-12)
                or np.any(t > self.duration+1e-12)):
            raise ValueError(f't must lie in [0, {self.duration}]')
        t = np.clip(t, 0., self.duration)
        index = np.searchsorted(self.times, t, side='right')-1
        p = self.positions[index]+(t-self.times[index])[..., None, None]*self.velocities[index]
        return p, self.velocities[index].copy()

    def reverse(self):
        """Re-integrate independently after reversing every final velocity."""
        p, v = self.sample(self.duration)
        return History(p, -v, self.duration, self.radius, self.box,
                       name=f'{self.name} reversed')


def seeded_initial_state(seed, energy):
    """Make repeatable, separated starting states with prescribed total energy."""
    rng = np.random.default_rng(seed)
    positions = []
    while len(positions) < BALL_COUNT:
        p = rng.uniform((.075, .065), (.925, .595))
        if all(np.linalg.norm(p-q) > .13 for q in positions):
            positions.append(p)
    angles = rng.uniform(0., 2*np.pi, BALL_COUNT)
    speeds = rng.uniform(.105, .165, BALL_COUNT)
    velocities = speeds[:, None]*np.column_stack((np.cos(angles), np.sin(angles)))
    velocities *= np.sqrt(energy/(.5*np.sum(velocities**2)))
    return np.array(positions), velocities


@lru_cache(8)
def build_histories(duration=DURATION):
    """Return two independent eight-disk histories under the same collision law."""
    return tuple(History(*seeded_initial_state(seed, energy), duration=duration, name=name)
                 for seed, energy, name in [(19, .076, 'A'), (156, .083, 'B')])


def _continuous_clearance(history):
    """Minimize pair separation analytically on every straight flight segment."""
    pair_clearance = np.inf
    wall_clearance = np.inf
    ends = np.r_[history.times[1:], history.duration]
    for start, end, p, v in zip(history.times, ends, history.positions, history.velocities):
        length = end-start
        endpoint = p+length*v
        wall_clearance = min(wall_clearance, float(np.min(p-history.radius)),
                             float(np.min(history.box-history.radius-p)),
                             float(np.min(endpoint-history.radius)),
                             float(np.min(history.box-history.radius-endpoint)))
        for i in range(len(p)):
            for j in range(i+1, len(p)):
                r, u = p[j]-p[i], v[j]-v[i]
                u2 = float(u @ u)
                s = np.clip(-float(r @ u)/u2, 0., length) if u2 else 0.
                pair_clearance = min(pair_clearance, float(np.linalg.norm(r+s*u)-2*history.radius))
    return {'minimum_wall_clearance': wall_clearance,
            'minimum_disk_surface_clearance': pair_clearance,
            'method': 'analytic minima over every complete free-flight interval'}


def validate_history(history):
    reverse = history.reverse()
    grid = np.linspace(0., history.duration, 1601)
    # Event positions are continuous; include all event times in both directions.
    times = np.unique(np.r_[grid, history.times, history.duration-reverse.times])
    p, _ = history.sample(times)
    pr, _ = reverse.sample(history.duration-times)
    position_error = float(np.max(np.abs(p-pr)))
    # At exactly an event the right-continuous velocity convention reverses sides.
    smooth = np.array([t for t in grid if all(abs(t-e.time) > 1e-9 for e in history.events)])
    _, v = history.sample(smooth)
    _, vr = reverse.sample(history.duration-smooth)
    velocity_error = float(np.max(np.abs(v+vr)))
    energies = .5*np.sum(history.velocities**2, axis=(1, 2))
    ball_events = [e for e in history.events if e.kind == 'ball']
    momentum_errors = [float(np.max(np.abs(
        e.velocities_before[[e.i,e.j]].sum(axis=0)-
        e.velocities_after[[e.i,e.j]].sum(axis=0)))) for e in ball_events]
    ball_energy_errors = [float(abs(np.sum(e.velocities_before[[e.i,e.j]]**2)-
                                    np.sum(e.velocities_after[[e.i,e.j]]**2))*.5)
                          for e in ball_events]
    clearance = _continuous_clearance(history)
    forward_events = [(e.kind, e.i, e.j, e.axis) for e in history.events]
    backward_events = [(e.kind, e.i, e.j, e.axis) for e in reversed(reverse.events)]
    event_times_error = (max(abs(e.time-(history.duration-r.time))
                             for e, r in zip(history.events, reversed(reverse.events)))
                         if forward_events == backward_events else np.inf)
    assert np.max(np.abs(energies-energies[0])) < 1e-12
    assert max(momentum_errors, default=0.) < 1e-12
    assert max(ball_energy_errors, default=0.) < 1e-12
    assert clearance['minimum_wall_clearance'] > -1e-10
    assert clearance['minimum_disk_surface_clearance'] > -1e-10
    assert position_error < 1e-8 and velocity_error < 1e-8
    assert forward_events == backward_events
    return {
        'name': history.name,
        'initial_positions': history.initial_positions.tolist(),
        'initial_velocities': history.initial_velocities.tolist(),
        'initial_speeds': np.linalg.norm(history.initial_velocities, axis=1).tolist(),
        'total_energy': float(energies[0]),
        'maximum_energy_error': float(np.max(np.abs(energies-energies[0]))),
        'maximum_ball_collision_momentum_error': max(momentum_errors, default=0.),
        'maximum_ball_collision_energy_error': max(ball_energy_errors, default=0.),
        'wall_collision_count': len(history.events)-len(ball_events),
        'ball_collision_count': len(ball_events),
        'collision_times': [e.time for e in history.events],
        'clearance': clearance,
        'independent_reverse_position_error': position_error,
        'independent_reverse_velocity_error': velocity_error,
        'independent_reverse_event_time_error': event_times_error,
        'independent_reverse_events_match': forward_events == backward_events,
        'reversal_method': 'new event-driven integration from final positions and negated final velocities',
        'checked_times_count': len(times),
        'passed': True,
    }


def validation_report(duration=DURATION):
    histories = build_histories(duration)
    reports = [validate_history(h) for h in histories]
    energies = [report['total_energy'] for report in reports]
    gap = abs(energies[0]-energies[1])
    assert gap > 1e-3
    # Reverse triangle inequality for the concatenated velocity vectors gives
    # a strictly positive lower bound under every permutation of ball labels.
    velocity_distance_bound = abs(np.sqrt(2*energies[0])-np.sqrt(2*energies[1]))
    return {
        'model': 'equal-mass hard disks; exact free flight; specular walls; elastic binary collisions',
        'duration_seconds': duration, 'box': list(BOX), 'radius': RADIUS,
        'ball_count_per_history': BALL_COUNT, 'histories': reports,
        'independent_systems': True, 'inter_history_collisions': False,
        'unordered_full_states_are_distinct_for_all_times': True,
        'distinctness_certificate': 'different conserved energies forbid equality under any permutation',
        'conserved_energy_difference': gap,
        'minimum_unordered_full_velocity_distance_lower_bound': velocity_distance_bound,
        'passed': True,
    }


def main():
    report = validation_report()
    path = ROOT/'content/drafts/animations/symmetry-reversible-histories-validation.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'output': str(path.relative_to(ROOT)), 'passed': report['passed'],
                      'histories': [{k:h[k] for k in ('name', 'ball_collision_count',
                                    'wall_collision_count', 'independent_reverse_position_error')}
                                    for h in report['histories']]}, indent=2))


if __name__ == '__main__':
    main()
