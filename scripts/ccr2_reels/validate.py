"""Focused numerical and exported-media validation for the reel package."""
from __future__ import annotations
from render import *
import re

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--media',action='store_true')
    args=parser.parse_args()
    report={'mathematics':{},'media':[]}
    entries=episodes()
    for name in MODULES:
        module=importlib.import_module(name)
        if hasattr(module,'validate'):report['mathematics'].update(module.validate())
    for number,e in entries.items():
        assert 30<=e['source_duration']<=60
        assert abs(e['duration']*PLAYBACK_SPEED-e['source_duration'])<1e-9
        assert round(e['duration']*FPS)==round(e['source_duration']*SOURCE_FPS)
        for t in [0,*e['checkpoints'],e['duration']-1/FPS]:
            im=e['render'](t)
            assert im.size==(W,H)
        if args.media:
            path=OUT/f'{slug(number)}.mp4'
            reader=imageio_ffmpeg.read_frames(str(path))
            info=next(reader);reader.close()
            assert tuple(info['size'])==(W,H)
            assert abs(info['fps']-FPS)<.01
            assert abs(info['duration']-e['duration'])<.1
            proc=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-f','null','-'],
                                stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            assert proc.returncode==0,proc.stderr.decode('utf8',errors='replace')
            probe=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',str(path)],
                                 stdout=subprocess.DEVNULL,stderr=subprocess.PIPE).stderr.decode('utf8',errors='replace')
            assert 'Audio:' not in probe
            assert 'h264' in probe and 'yuv420p' in probe
            caption=(OUT/f'{slug(number)}-caption.txt').read_text(encoding='utf8')
            assert len(caption)<=2200
            assert Image.open(OUT/f'{slug(number)}-cover.jpg').size==(W,H)
            report['media'].append(dict(episode=number,seconds=info['duration'],fps=info['fps'],
                   bytes=path.stat().st_size,caption_characters=len(caption),full_decode='pass',audio_tracks=0))
        print(f'Validated {number:02d}',flush=True)
    destination=OUT/('validation.json' if args.media else 'numerical-validation.json')
    destination.write_text(json.dumps(report,indent=2,default=lambda x:float(x)),encoding='utf8')
    print(destination,flush=True)

if __name__=='__main__':main()
