"""Apply the current playback speed to an immutable original-speed package.

No mathematical frames are rendered here. The original MP4s are decoded in
order and encoded at SOURCE_FPS * PLAYBACK_SPEED without dropping frames.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from render import *

BACKUP=ROOT/'.tools'/'buffer-staging'/'original-speed-v1'/'ccr2-series'

def retime(number):
    source=BACKUP/f'{slug(number)}.mp4'
    target=OUT/f'{slug(number)}.mp4'
    temporary=OUT/f'{slug(number)}.retiming.mp4'
    assert source.is_file(), f'Missing preserved original: {source}'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(source),
        '-map','0:v:0','-an','-vf',f'setpts=PTS/{PLAYBACK_SPEED}',
        '-r',str(FPS),'-fps_mode','cfr','-c:v','libx264','-preset','fast',
        '-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','4',
        str(temporary)],check=True)
    temporary.replace(target)
    preview(number)
    print(f'Retimed {number:02d} to {PLAYBACK_SPEED:g}x / {FPS}fps',flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--episodes',nargs='+',type=int)
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    original=json.loads((BACKUP/'manifest.json').read_text(encoding='utf8'))
    assert len(original['episodes'])==13
    assert all(row['fps']==SOURCE_FPS and row.get('playback_speed',1)==1
               for row in original['episodes']), 'Backup must be the original-speed package.'
    for row in original['episodes']:
        with (BACKUP/row['video']).open('rb') as handle:
            assert hashlib.file_digest(handle,'sha256').hexdigest()==row['video_sha256']
    numbers=args.episodes or list(episodes())
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(retime,numbers))
    package(episodes())

if __name__=='__main__':main()
