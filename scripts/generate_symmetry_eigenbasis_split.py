"""Separate the existing eigenbasis animation into its two explanatory acts.

Reuse the original drawing functions and all motion timings. The original
30-frame crossfade becomes a final hold in the first clip, keeping the total
duration at 14.5 seconds. The original combined movie is not modified.
Run --render --check to write the two movies and decoded review evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'.tools/animation-python-packages'))
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
import generate_symmetry_eigenbasis_stretch_animation as source

OUT = ROOT/'content/drafts/animations'
REVIEW = ROOT/'.tools/eigenbasis-split-review'
FPS, W, H = source.FPS, source.WIDTH, source.HEIGHT
FIRST_END = source.FIRST_ACT_FRAMES+source.FIRST_HOLD_FRAMES
SECOND_START = FIRST_END+source.TRANSITION_FRAMES
CLIPS = [
    {'name':'symmetry-eigenbasis-comparison', 'frames':SECOND_START,
     'poster_frame':source.FIRST_ACT_FRAMES-1, 'source_start':0},
    {'name':'symmetry-eigenbasis-components', 'frames':source.FRAMES-SECOND_START,
     'poster_frame':source.FRAMES-SECOND_START-1, 'source_start':SECOND_START},
]


def source_frame(clip, frame):
    return min(frame,FIRST_END-1) if clip['source_start']==0 else clip['source_start']+frame


def render(clip, frame):
    return source.draw_frame(source_frame(clip,frame))


def validate(clip):
    assert sum(c['frames'] for c in CLIPS)==source.FRAMES==348
    assert FPS==24 and (W,H)==(1280,720)
    root2=np.sqrt(2)
    basis=np.array([[1,1],[1,-1]],dtype=float)/root2
    stretch=source.STRETCH_PARAMETER
    diagonal=np.diag([stretch,1/stretch])
    matrix=basis@diagonal@basis.T
    ordinary=np.array([[(stretch+1/stretch)/2,(stretch-1/stretch)/2],
                       [(stretch-1/stretch)/2,(stretch+1/stretch)/2]])
    assert np.allclose(matrix,ordinary)
    assert np.allclose(matrix@basis[:,0],stretch*basis[:,0])
    assert np.allclose(matrix@basis[:,1],basis[:,1]/stretch)
    rng=np.random.default_rng(31)
    error=0.
    for coordinates in rng.normal(size=(100,2)):
        error=max(error,float(np.max(abs(matrix@(basis@coordinates)-basis@(diagonal@coordinates)))))
    assert error<1e-12
    mapping=[source_frame(clip,i) for i in range(clip['frames'])]
    assert not any(FIRST_END<=i<SECOND_START for i in mapping)
    return dict(size=[W,H],fps=FPS,frame_count=clip['frames'],duration_seconds=clip['frames']/FPS,
                combined_duration_seconds=sum(c['frames'] for c in CLIPS)/FPS,
                original_duration_seconds=source.FRAMES/FPS,
                original_motion_unchanged=True,source_frame_indices=mapping,
                transition='Original crossfade replaced by final hold in basis-comparison clip',
                basis_change_max_error=error,random_vector_checks=100,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                drawing_source_sha256=hashlib.sha256(Path(source.__file__).read_bytes()).hexdigest())


def encode(clip):
    temporary=REVIEW/f"{clip['name']}.rendering.mp4"
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo',
             '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an',
             '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
             '-movflags','+faststart','-threads','2',str(temporary)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
        try:
            for i in range(clip['frames']):
                process.stdin.write(render(clip,i).tobytes())
                if i%48==0: print(f"{clip['name']}: {i}/{clip['frames']} frames",flush=True)
            process.stdin.close()
            if process.wait(): raise RuntimeError('FFmpeg failed')
        except BaseException:
            process.kill()
            raise
    temporary.replace(OUT/f"{clip['name']}.mp4")


def check(clip):
    name=clip['name']
    video=OUT/f'{name}.mp4'
    count,seconds=imageio_ffmpeg.count_frames_and_secs(str(video))
    assert count==clip['frames'] and abs(seconds-count/FPS)<.001
    reader=imageio_ffmpeg.read_frames(str(video))
    try: meta=next(reader)
    finally: reader.close()
    assert meta['size']==(W,H) and meta['fps']==FPS
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
    indices=sorted({round(i*(count-1)/5) for i in range(6)})
    selection='+'.join(f'eq(n\\,{i})' for i in indices)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                    f'select={selection},scale=480:270,tile=3x2','-frames:v','1',
                    str(OUT/f'{name}-contact-sheet.png')],check=True)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(video),'-vf',
                    f"select=eq(n\\,{clip['poster_frame']})",'-frames:v','1',
                    str(OUT/f'{name}-poster.png')],check=True)
    report=dict(video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),
                frame_count=count,duration_seconds=seconds,size=meta['size'],fps=meta['fps'],
                decode='passed',contact_sheet_frame_indices=indices,
                source_frame_indices=[source_frame(clip,i) for i in indices])
    (OUT/f'{name}-encoded-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    REVIEW.mkdir(parents=True,exist_ok=True)
    for clip in CLIPS:
        report=validate(clip)
        (OUT/f"{clip['name']}-validation.json").write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
        render(clip,clip['poster_frame']).save(REVIEW/f"{clip['name']}-preview.png")
        if args.render: encode(clip)
        if args.check: print(json.dumps(check(clip)),flush=True)


if __name__=='__main__': main()
