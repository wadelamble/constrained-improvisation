"""Horizontal stretch, rotation, then the operator sandwich."""
from symmetry_stretch_operator_scenes import StretchScenes
from symmetry_exponential_desktop_common import run

if __name__ == '__main__':
    scenes = StretchScenes()
    run(scenes.name, scenes.duration, scenes.render, scenes.validate,
        scenes.moments, scenes.poster, __file__)
