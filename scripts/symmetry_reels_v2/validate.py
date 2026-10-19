"""Check the encoded offline first cuts and make decoded review sheets."""
from __future__ import annotations

import argparse
import json
import subprocess
import render
import imageio_ffmpeg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=int, nargs='+')
    parser.add_argument('--decode', action='store_true')
    args = parser.parse_args()
    entries = render.entries()
    folder = render.OUT / 'review' / 'decoded'
    folder.mkdir(parents=True, exist_ok=True)
    results = []
    for number in args.episodes or entries:
        entry = entries[number]
        video = render.OUT / f'{render.slug(number)}.mp4'
        if not video.is_file():
            raise FileNotFoundError(video)
        reader = imageio_ffmpeg.read_frames(str(video))
        try:
            meta = next(reader)
        finally:
            reader.close()
        assert tuple(meta['size']) == (render.W, render.H), (number, meta)
        assert abs(meta['fps'] - render.FPS) < .01, (number, meta)
        assert abs(meta['duration'] - entry['duration']) < .15, (number, meta)
        assert render.buffer_count(entry['caption']) <= 2196
        if args.decode:
            target = folder / f'{render.slug(number)}-decoded.jpg'
            subprocess.run([
                imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error',
                '-i', str(video), '-vf',
                f'fps={12 / entry["duration"]},scale=270:480,tile=4x3',
                '-frames:v', '1', '-q:v', '2', str(target)
            ], check=True)
        results.append(dict(number=number, title=entry['title'],
                            duration=meta['duration'], fps=meta['fps'],
                            size=meta['size'], codec=meta.get('codec'),
                            pixel_format=meta.get('pix_fmt'),
                            caption_buffer_count=entry['buffer_count']))
        print(f'Validated reel {number:02d}', flush=True)
    (folder / 'validation.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')


if __name__ == '__main__':
    main()
