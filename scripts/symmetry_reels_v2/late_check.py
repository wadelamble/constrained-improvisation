"""Check the source functions and geometry actually passed to portrait drawing."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import numpy as np
import late
from core import ROOT, Scene


def source(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name+".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RecordedScene(Scene):
    last = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arrows = []
        RecordedScene.last = self
    def arrow(self, start, end, *args, **kwargs):
        self.arrows.append((np.asarray(start, float), np.asarray(end, float)))
        return super().arrow(start, end, *args, **kwargs)


def main():
    out = ROOT / "content/reels/symmetry-series-v2/review/late"
    out.mkdir(parents=True, exist_ok=True)
    entries = {e["number"]: e for e in json.loads(Path(__file__).with_name("series.json").read_text(encoding="utf-8"))}
    linearity = source("generate_symmetry_translation_linearity_animations")
    shape = source("generate_symmetry_function_translation_shape_animation")
    xs = np.linspace(-4, 6, 503)
    errors = {}
    errors["source_f"] = float(np.max(abs(late._source_f(xs)-[linearity.f_value(x) for x in xs])))
    errors["source_g"] = float(np.max(abs(late._source_g(xs)-[linearity.g_value(x) for x in xs])))
    errors["source_shape"] = float(np.max(abs(late._source_shape(xs)-[shape.base_shape(x) for x in xs])))
    errors["source_deformation"] = max(float(np.max(abs(late._source_distortion(xs,a)-[shape.distorted_shape(x,a) for x in xs]))) for a in np.linspace(0,1,11))
    late.Scene = RecordedScene
    errors.update(boost_interval=0., boost_gap=0., eigen_recombination=0., eigen_reciprocity=0., tangent_attachment=0., tangent_orthogonality=0., tangent_norm=0.)
    distances=[]
    for q in np.linspace(0,24,49):
        e=entries[14]
        late.render(14,q*e["duration"]/24,e)
        a,b = RecordedScene.last.arrows[-2:]
        points=[(end-start)/170*[1,-1] for start,end in (a,b)]
        errors["boost_interval"]=max(errors["boost_interval"],*(abs(ct*ct-x*x-1) for x,ct in points))
        errors["boost_gap"]=max(errors["boost_gap"],abs(np.arcsinh(points[1][0])-np.arcsinh(points[0][0])-.42))
        distances.append(float(np.linalg.norm(points[1]-points[0])))
        e=entries[24]
        late.render(24,q*e["duration"]/24,e)
        radial,tangent=RecordedScene.last.arrows[-2:]
        rv,tv=radial[1]-radial[0],tangent[1]-tangent[0]
        errors["tangent_attachment"]=max(errors["tangent_attachment"],float(np.linalg.norm(radial[1]-tangent[0])))
        errors["tangent_orthogonality"]=max(errors["tangent_orthogonality"],abs(float(rv@tv))/235**2)
        errors["tangent_norm"]=max(errors["tangent_norm"],abs(float(np.linalg.norm(rv)-np.linalg.norm(tv)))/235)
        if q >= 11:
            e=entries[21]
            late.render(21,q*e["duration"]/24,e)
            result,u,v=RecordedScene.last.arrows[-3:]
            uv,vv=u[1]-u[0],v[1]-v[0]
            errors["eigen_recombination"]=max(errors["eigen_recombination"],float(np.linalg.norm(result[1]-result[0]-uv-vv)))
            errors["eigen_reciprocity"]=max(errors["eigen_reciprocity"],abs(float(np.linalg.norm(uv)*np.linalg.norm(vv))/(235**2*.75)-1))
    assert min(np.diff(distances)) >= -1e-12
    assert max(errors.values()) < 1e-10, errors
    report={"status":"pass","samples_per_motion":49,"maximum_errors":errors,
            "ordinary_tip_distance_start":distances[0],"ordinary_tip_distance_end":distances[-1],
            "note":"Checks use the actual arrows passed to the renderer; function shapes match the desktop scalar source functions."}
    (out/"mathematical-checks.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
