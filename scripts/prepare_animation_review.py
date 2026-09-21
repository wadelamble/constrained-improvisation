"""Extract review evidence from the delivered MP4s, without rerendering them.

Run locally with Pillow and imageio-ffmpeg available. The website build itself
uses only the standard library and copies these checked-in evidence files.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools' / 'animation-python-packages'))
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

CATALOG = ROOT / 'site_src' / 'animation-sources.json'
FRAME_ROOT = ROOT / 'content' / 'review' / 'animation-frames'
RECIPE = 'encoded-frames-v1-12-uniform-inclusive-native-resolution'


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def cached(directory: Path, digest: str) -> dict | None:
    manifest_path = directory / 'manifest.json'
    if not manifest_path.exists():
        return None
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    if data.get('recipe') != RECIPE or data.get('video_sha256') != digest:
        return None
    for item in data['frames'] + [data['contact_sheet']]:
        path = directory / item['file']
        if not path.exists() or sha256(path) != item['sha256']:
            return None
    return data


def font(size: int):
    for name in ('C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default(size=size)


def extract(name: str) -> dict:
    if Path(name).name != name or not name.endswith('.mp4'):
        raise ValueError(f'Invalid video basename: {name}')
    movie = ROOT / 'content' / 'drafts' / 'animations' / name
    digest = sha256(movie)
    destination = FRAME_ROOT / movie.stem
    prior = cached(destination, digest)
    if prior:
        return prior

    reader = imageio_ffmpeg.read_frames(str(movie))
    try:
        meta = next(reader)
    finally:
        reader.close()
    frame_count, measured_seconds = imageio_ffmpeg.count_frames_and_secs(str(movie))
    fps = meta['fps']
    width, height = meta['size']
    indices = sorted({round(i * (frame_count - 1) / 11) for i in range(12)})
    select = '+'.join(f'eq(n\\,{i})' for i in indices)
    FRAME_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f'{movie.stem}-', dir=FRAME_ROOT) as temporary:
        stage = Path(temporary)
        command = [imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-nostdin',
                   '-threads', '2', '-i', str(movie), '-an',
                   '-vf', f'select={select},showinfo', '-fps_mode', 'vfr',
                   '-q:v', '2', str(stage / 'frame-%02d.jpg')]
        process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if process.returncode:
            raise RuntimeError(f'{name}: {process.stderr[-3000:]}')
        timestamps = [float(x) for x in re.findall(r'pts_time:([\d.eE+-]+)', process.stderr)]
        files = sorted(stage.glob('frame-*.jpg'))
        if len(files) != len(indices) or len(timestamps) != len(indices):
            raise ValueError(f'{name}: expected {len(indices)} frames; got {len(files)} / {len(timestamps)} timestamps')
        frames = []
        sheet = Image.new('RGB', (1600, 3 * 275), '#faf7f0')
        draw = ImageDraw.Draw(sheet)
        for j, (path, index, seconds) in enumerate(zip(files, indices, timestamps)):
            frames.append({'file': path.name, 'index': index, 'time_seconds': seconds, 'sha256': sha256(path)})
            with Image.open(path) as im:
                if im.size != (width, height):
                    raise ValueError(f'{name}: unexpected decoded geometry {im.size}')
                thumbnail = im.copy()
                thumbnail.thumbnail((390, 240), Image.Resampling.LANCZOS)
                x, y = (j % 4) * 400, (j // 4) * 275
                sheet.paste(thumbnail, (x + (400 - thumbnail.width) // 2, y + (240 - thumbnail.height) // 2))
                draw.text((x + 12, y + 245), f'{seconds:.3f} s  |  frame {index}', fill='#252628', font=font(17))
        sheet_path = stage / 'contact-sheet.jpg'
        sheet.save(sheet_path, quality=90)
        if sha256(movie) != digest:
            raise RuntimeError(f'{name} changed during extraction; rerun when the renderer has finished.')
        data = {
            'schema_version': 1, 'recipe': RECIPE,
            'video': movie.relative_to(ROOT).as_posix(), 'video_sha256': digest,
            'duration_seconds': measured_seconds, 'fps': fps, 'frame_count': frame_count,
            'width': width, 'height': height,
            'method': 'Twelve evenly spaced decoded frame indices, including first and last. Native-resolution JPEGs from the encoded MP4; timestamps read from FFmpeg showinfo. No source rerendering. Frame indices are zero-based. Sparse samples do not establish continuous motion or capture every transition.',
            'frames': frames,
            'contact_sheet': {'file': sheet_path.name, 'sha256': sha256(sheet_path)},
        }
        (stage / 'manifest.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        destination.mkdir(exist_ok=True)
        for item in stage.iterdir():
            shutil.copy2(item, destination / item.name)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', help='One catalogued video basename, including .mp4')
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    names = [args.only] if args.only else list(catalog)
    if any(name not in catalog for name in names):
        parser.error('--only must name a catalogued video')
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(extract, name): name for name in names}
        for future in as_completed(futures):
            data = future.result()
            print(f"{futures[future]}: {data['frame_count']} encoded frames; {len(data['frames'])} sampled", flush=True)


if __name__ == '__main__':
    main()
