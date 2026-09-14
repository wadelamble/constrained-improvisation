"""Geometric, continuously repeatable Huygens construction.

These arcs are construction wavelets, not complex amplitudes. All generations
have the same current forward tangent. A camera follows that advancing front;
older construction rows recede downward in the drawing. Points sample a
continuous wavefront. The straight line is its common tangent, not the exact
scalloped boundary of a finite set of circles.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math

WIDTH, HEIGHT, FPS = 1280, 720, 24
DURATION = 12.0
STEP_TIME = 1.5
VISIBLE_GENERATIONS = 3
SPEED = 1.0
# One physical unit spans 100 pixels; each construction step advances 1.5 units.
PIXELS_PER_UNIT = 100.0
FRONT_PIXEL_Y = 170.0
SOURCE_SPACING = 1.45
LEFT, RIGHT, TOP, BOTTOM = 40.0, 1240.0, 145.0, 665.0


def ease(value):
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


@dataclass(frozen=True)
class Generation:
    index: int
    construction_time: float
    age: float
    radius: float
    source_height: float
    offset: float
    opacity: float

    def forward_height(self):
        return self.source_height + self.radius


def generations_at(seconds):
    current = math.floor(seconds / STEP_TIME)
    result = []
    for index in range(current - VISIBLE_GENERATIONS + 1, current + 1):
        construction_time = index * STEP_TIME
        age = seconds - construction_time
        radius = SPEED * age
        fade = 1.0 - ease((age - 2 * STEP_TIME) / STEP_TIME)
        emphasis = math.exp(-0.34 * age / STEP_TIME)
        result.append(Generation(index, construction_time, age, radius,
                                 SPEED * construction_time,
                                 (index % 2) * SOURCE_SPACING / 2,
                                 fade * emphasis))
    return result


def source_centers(generation):
    # Continue beyond both crop edges so the construction does not look bounded.
    spacing_pixels = SOURCE_SPACING * PIXELS_PER_UNIT
    return [WIDTH / 2 + (j * SOURCE_SPACING + generation.offset) * PIXELS_PER_UNIT
            for j in range(-7, 8)]


def source_row_pixel_y(generation):
    return FRONT_PIXEL_Y + generation.radius * PIXELS_PER_UNIT


def run_checks():
    max_tangent_error = 0.0
    for n in range(1201):
        seconds = DURATION * n / 1200
        for generation in generations_at(seconds):
            max_tangent_error = max(max_tangent_error,
                                    abs(generation.forward_height() - SPEED * seconds))
    loop_error = 0.0
    offset_error = 0.0
    for seconds in (0.0, 0.1, 0.375, 0.75, 1.125, 1.499):
        for a, b in zip(generations_at(seconds), generations_at(seconds + DURATION)):
            loop_error = max(loop_error, abs(a.radius-b.radius), abs(a.opacity-b.opacity))
            offset_error = max(offset_error, abs(a.offset-b.offset))
    result = {"maximum_common_tangent_error": max_tangent_error,
              "following_camera_loop_geometry_error": loop_error,
              "loop_stagger_error": offset_error,
              "construction_steps_per_loop": DURATION / STEP_TIME,
              "simultaneous_generations": VISIBLE_GENERATIONS}
    assert max_tangent_error < 1e-12 and loop_error < 1e-12 and offset_error == 0
    assert int(DURATION / STEP_TIME) % 2 == 0
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run_checks()
