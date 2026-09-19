"""Replace reel headers and cover titles from an explicit, captured title list.

This is a media-only workflow. It never regenerates animation frames, retimes
videos, builds captions, or changes manifests and publication receipts.

Use --snapshot to preserve the current media before other synchronization work.
Then pass --titles path/to/captured.json --prepare, inspect the proposed contact
sheets, and run the same command with --render. The JSON may be a list of rows or
an object with an ``episodes`` list; every row needs ``order`` and ``title``.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from render import BG, FPS, H, OUT, ROOT, W, GOLD, INK, Image, ImageDraw, ImageFont, font, fitted_title, imageio_ffmpeg, matplotlib, np, slug
from validate_retime import metadata


TOP, BOTTOM = 260, 414
DEFAULT_RUN = 'live-title-refresh-20260919'
MEDIA_SUFFIXES = ('.mp4', '-cover.jpg', '-preview.webm')


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def source_files(number):
    return [f'{slug(number)}{suffix}' for suffix in MEDIA_SUFFIXES]


def snapshot(backup):
    """Copy each current master once; existing inventories must verify exactly."""
    inventory_path = backup / 'source-inventory.json'
    if inventory_path.exists():
        inventory = json.loads(inventory_path.read_text(encoding='utf8'))
        assert inventory['run_id'] == backup.name
        for item in inventory['episodes']:
            for record in item['files']:
                assert sha(backup / 'media' / record['name']) == record['sha256'], record['name']
        return inventory
    media = backup / 'media'
    assert not media.exists(), f'Unrecorded media backup already exists: {media}'
    media.mkdir(parents=True)
    rows = []
    for number in range(1, 14):
        files = []
        for name in source_files(number):
            source, target = OUT / name, media / name
            assert source.is_file(), source
            original_sha = sha(source)
            shutil.copy2(source, target)
            assert sha(target) == original_sha, name
            files.append(dict(name=name, sha256=original_sha, bytes=target.stat().st_size))
        info = metadata(media / f'{slug(number)}.mp4')
        assert info['faststart']
        assert all(abs(delta / info['timescale'] - 1 / FPS) < 1e-9
                   for count, delta in info['timing_runs'])
        rows.append(dict(order=number, files=files, video_metadata=info))
    inventory = dict(run_id=backup.name, captured_at=utcnow(), fps=FPS,
                     playback_speed=1.75, episodes=rows)
    write_json(inventory_path, inventory)
    print(f'Preserved all 13 current masters, covers and previews: {backup}', flush=True)
    return inventory


def read_titles(path, selected):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    rows = data['episodes'] if isinstance(data, dict) else data
    assert isinstance(rows, list), 'Expected a list or an object with an episodes list.'
    titles = {}
    for row in rows:
        number, title = int(row['order']), row['title']
        assert 1 <= number <= 13 and number not in titles
        assert isinstance(title, str) and title.strip() == title and title
        assert '\n' not in title and '\r' not in title, (number, 'Title must be one line.')
        titles[number] = title
    numbers = sorted(selected if selected else titles)
    assert numbers and len(set(numbers)) == len(numbers)
    assert all(number in titles for number in numbers)
    return {number: titles[number] for number in numbers}


def live_title(draw, title, x=70, y=269, width=880, max_height=138, size=54):
    """Retain Segoe styling, with a real mathematical h-bar glyph where needed."""
    if '\u210f' not in title:
        return fitted_title(draw, title, x=x, y=y, width=width, max_height=max_height, size=size)
    fallback_path = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf' / 'DejaVuSans-Bold.ttf'
    for chosen in range(size, 29, -1):
        normal = font(chosen, True)
        fallback = ImageFont.truetype(str(fallback_path), chosen)

        def runs(value):
            return [(part, fallback if part == '\u210f' else normal)
                    for part in re.split('(\u210f)', value) if part]

        def length(value):
            return sum(draw.textlength(part, font=face) for part, face in runs(value))

        lines, line = [], ''
        for word in title.split():
            candidate = (line + ' ' + word).strip()
            if line and length(candidate) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
        leading, boxes, placements = round(chosen * 1.13), [], []
        for index, line in enumerate(lines):
            cursor, line_boxes = x, []
            for part, face in runs(line):
                # Match baselines despite the fonts' different ascent metrics.
                yy = y + index * leading + normal.getmetrics()[0] - face.getmetrics()[0]
                box = draw.textbbox((cursor, yy), part, font=face, anchor='la')
                line_boxes.append(box)
                placements.append((cursor, yy, part, face))
                cursor += draw.textlength(part, font=face)
            boxes.append((min(b[0] for b in line_boxes), min(b[1] for b in line_boxes),
                          max(b[2] for b in line_boxes), max(b[3] for b in line_boxes)))
        if max(b[3] for b in boxes) <= y + max_height:
            break
    else:
        raise ValueError(f'Title does not fit: {title}')
    for xx, yy, part, face in placements:
        draw.text((xx, yy), part, font=face, fill=INK, anchor='la')
    return dict(size=chosen, lines=lines, boxes=boxes, glyph_fallback='U+210F: DejaVuSans-Bold')


def frame(path, at=0):
    raw = subprocess.check_output([
        imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-ss', str(at),
        '-i', str(path), '-frames:v', '1', '-f', 'rawvideo',
        '-pix_fmt', 'rgb24', '-threads', '2', '-'])
    return Image.frombytes('RGB', (W, H), raw)


def samples(path, count):
    """Decode the whole stream and return exact first, middle and final frames."""
    indices = [0, count // 2, count - 1]
    select = '+'.join(f'eq(n\\,{index})' for index in indices)
    raw = subprocess.check_output([
        imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(path),
        '-vf', f'select={select}', '-fps_mode', 'passthrough', '-an',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-threads', '2', '-'])
    return np.frombuffer(raw, dtype=np.uint8).reshape((3, H, W, 3))


def prepare(titles, backup, review):
    review.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1080, ((len(titles) + 1) // 2) * 272), BG)
    cover_sheet = Image.new('RGB', (1080, ((len(titles) + 3) // 4) * 500), BG)
    draw = ImageDraw.Draw(sheet)
    layouts = []
    for index, (number, title) in enumerate(titles.items()):
        strip = Image.new('RGB', (W, BOTTOM - TOP), BG)
        layout = live_title(ImageDraw.Draw(strip), title, y=269 - TOP)
        assert all(70 <= b[0] and b[2] <= 950 and 0 <= b[1]
                   and b[3] < strip.height for b in layout['boxes']), (number, layout)
        strip_path = review / f'{slug(number)}-title.png'
        strip.save(strip_path)
        picture = frame(backup / 'media' / f'{slug(number)}.mp4')
        picture.paste(strip, (0, TOP))
        picture.save(review / f'{slug(number)}-proposed.png')
        x, y = (index % 2) * 540, (index // 2) * 272
        sheet.paste(picture.crop((0, 150, W, 630)).resize((540, 240)), (x, y + 28))
        draw.text((x + 35, y), f'{number:02d}', font=font(23), fill=GOLD)

        cover = Image.open(backup / 'media' / f'{slug(number)}-cover.jpg').convert('RGB')
        cover_draw = ImageDraw.Draw(cover)
        cover_draw.rectangle((0, 540, W, 707), fill=BG)
        cover_layout = live_title(cover_draw, title, x=90, y=550,
                                 width=860, max_height=145, size=56)
        assert all(90 <= b[0] and b[2] <= 950 and 540 <= b[1]
                   and b[3] < 708 for b in cover_layout['boxes']), (number, cover_layout)
        cover_path = review / f'{slug(number)}-proposed-cover.jpg'
        cover.save(cover_path, quality=95)
        cover_sheet.paste(cover.resize((270, 480), Image.Resampling.LANCZOS),
                          ((index % 4) * 270, (index // 4) * 500))
        layouts.append(dict(order=number, title=title, header=layout, cover=cover_layout,
                            strip_sha256=sha(strip_path), cover_sha256=sha(cover_path)))
    sheet.save(review / 'proposed-title-sheet.jpg', quality=95)
    cover_sheet.save(review / 'proposed-cover-sheet.jpg', quality=95)
    write_json(review / 'layouts.json', layouts)
    print(f'Prepared {len(layouts)} complete title and cover layouts: {review}', flush=True)


def render_one(number, title, source_row, layout, backup, review):
    assert layout['title'] == title
    source = backup / 'media' / f'{slug(number)}.mp4'
    target = OUT / f'{slug(number)}.mp4'
    strip_path = review / f'{slug(number)}-title.png'
    proposed_cover = review / f'{slug(number)}-proposed-cover.jpg'
    assert sha(strip_path) == layout['strip_sha256']
    assert sha(proposed_cover) == layout['cover_sha256']
    source_hash = next(row['sha256'] for row in source_row['files'] if row['name'] == source.name)
    assert sha(source) == source_hash
    result_path = review / f'{slug(number)}-result.json'
    previous = json.loads(result_path.read_text(encoding='utf8')) if result_path.exists() else {}
    allowed_hashes = {source_hash}
    if previous:
        assert previous['source_sha256'] == source_hash
        allowed_hashes.add(previous['video_sha256'])
    assert sha(target) in allowed_hashes, f'Current master changed outside this run: {target}'
    temporary = review / f'{slug(number)}.rendering.mp4'
    before = metadata(source)
    assert json.dumps(before, sort_keys=True) == json.dumps(source_row['video_metadata'], sort_keys=True)
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(source),
        '-i', str(strip_path), '-filter_complex',
        f'[0:v][1:v]overlay=0:{TOP}:format=auto,format=yuv420p[v]',
        '-map', '[v]', '-an', '-fps_mode', 'passthrough', '-c:v', 'libx264',
        '-preset', 'fast', '-crf', '16', '-threads', '4',
        '-movflags', '+faststart', str(temporary)], check=True)
    after = metadata(temporary)
    assert before['frames'] == after['frames']
    assert abs(before['duration'] - after['duration']) < 1e-9
    assert before['timescale'] == after['timescale']
    assert before['timing_runs'] == after['timing_runs'] and after['faststart']
    old, new = samples(source, before['frames']), samples(temporary, after['frames'])
    errors = []
    for index, (a, b) in enumerate(zip(old, new)):
        delta = np.concatenate((a[:TOP-8].astype(float)-b[:TOP-8],
                                a[BOTTOM+8:].astype(float)-b[BOTTOM+8:]))
        error = float(np.sqrt(np.mean(delta * delta)))
        assert error < 3, (number, index, error)
        errors.append(error)
        Image.fromarray(b).save(review / f'{slug(number)}-verified-{index}.jpg', quality=94)
    probe = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', str(temporary)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE).stderr.decode('utf8', errors='replace')
    assert 'Audio:' not in probe and 'h264' in probe and 'yuv420p' in probe
    assert '1080x1920' in probe and '42 fps' in probe
    preview_temp = review / f'{slug(number)}-preview.webm'
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(temporary),
        '-vf', 'scale=720:1280', '-an', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30',
        '-deadline', 'realtime', '-cpu-used', '8', '-threads', '4', str(preview_temp)], check=True)
    reader = imageio_ffmpeg.read_frames(str(preview_temp))
    preview_info = next(reader)
    reader.close()
    assert tuple(preview_info['size']) == (720, 1280)
    assert abs(preview_info['duration'] - before['duration']) < .1
    row = dict(order=number, title=title, source_sha256=source_hash, video_sha256=sha(temporary),
               video_bytes=temporary.stat().st_size, frames=after['frames'], duration=after['duration'],
               fps=FPS, playback_speed=1.75, video_metadata=after, outside_header_rmse=errors,
               full_decode='pass; exact first, middle and final frames selected from full stream',
               audio_tracks=0, preview_sha256=sha(preview_temp), cover_sha256=sha(proposed_cover),
               completed_at=utcnow())
    # Record provenance before replacing masters, so an interrupted install can be resumed.
    write_json(result_path, row)
    temporary.replace(target)
    preview_temp.replace(OUT / f'{slug(number)}-preview.webm')
    shutil.copy2(proposed_cover, OUT / f'{slug(number)}-cover.jpg')
    print(f'Retitle {number:02d}: {after["frames"]} frames / {after["duration"]:.6f}s retained.', flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--titles', type=Path)
    parser.add_argument('--episodes', nargs='+', type=int)
    parser.add_argument('--run-id', default=DEFAULT_RUN)
    parser.add_argument('--snapshot', action='store_true')
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    assert re.fullmatch(r'[a-z0-9][a-z0-9-]*', args.run_id), 'Run ID must be a simple directory name.'
    assert args.snapshot or args.prepare or args.render, 'Choose --snapshot, --prepare or --render.'
    assert 1 <= args.workers <= 4
    backup = ROOT / '.tools' / 'buffer-staging' / args.run_id
    review = OUT / 'review' / args.run_id
    inventory = snapshot(backup)
    if not (args.prepare or args.render):
        return
    assert args.titles, '--titles is required for preparation/rendering.'
    titles = read_titles(args.titles, args.episodes)
    if args.prepare:
        prepare(titles, backup, review)
    if args.render:
        layouts = {row['order']: row for row in json.loads((review / 'layouts.json').read_text(encoding='utf8'))}
        sources = {row['order']: row for row in inventory['episodes']}
        assert all(number in layouts and layouts[number]['title'] == title for number, title in titles.items()), 'Run --prepare with these exact titles first.'
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            jobs = [pool.submit(render_one, number, title, sources[number], layouts[number], backup, review)
                    for number, title in titles.items()]
            rows = [job.result() for job in jobs]
        write_json(review / 'validation.json', dict(run_id=args.run_id,
                   source_backup=backup.relative_to(ROOT).as_posix(),
                   title_input_sha256=sha(args.titles), episodes=rows))
        print(f'Media refreshed and verified for {len(rows)} reels. Captions and manifests were not written.', flush=True)


if __name__ == '__main__':
    main()
