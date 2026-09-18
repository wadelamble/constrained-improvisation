"""Refresh burned-in titles without recomputing accepted animation frames.

Only the fixed header strip is replaced. Captions and publishing receipts are
preserved. Run --prepare to inspect layouts, then --render for MP4s and previews.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import shutil

from render import *
from validate_retime import metadata

NUMBERS = (4, 5, 7, 8, 9, 10, 11, 12, 13)
BACKUP = ROOT / '.tools/buffer-staging/title-refresh-20260917'
REVIEW = OUT / 'review/title-refresh'
TOP, BOTTOM = 260, 414


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def preserve(path):
    target = BACKUP / 'files' / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(path, target)
    return target


def frame(path, at=0):
    raw = subprocess.check_output([
        imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-ss', str(at),
        '-i', str(path), '-frames:v', '1', '-f', 'rawvideo',
        '-pix_fmt', 'rgb24', '-threads', '2', '-'])
    return Image.frombytes('RGB', (W, H), raw)


def prepare():
    REVIEW.mkdir(parents=True, exist_ok=True)
    entries = episodes()
    layouts = []
    sheet = Image.new('RGB', (1080, 5 * 272), BG)
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(NUMBERS):
        e = entries[n]
        title = e.get('video_title', e['title'])
        strip = Image.new('RGB', (W, BOTTOM - TOP), BG)
        layout = fitted_title(ImageDraw.Draw(strip), title, y=269-TOP)
        assert all(70 <= box[0] and box[2] <= 950 and 0 <= box[1]
                   and box[3] < strip.height for box in layout['boxes'])
        strip.save(REVIEW / f'{slug(n)}-title.png')
        source = preserve(OUT / f'{slug(n)}.mp4')
        pic = frame(source)
        pic.paste(strip, (0, TOP))
        pic.save(REVIEW / f'{slug(n)}-proposed.png')
        x, y = (i % 2) * 540, (i // 2) * 272
        sheet.paste(pic.crop((0, 150, W, 630)).resize((540, 240)), (x, y+28))
        d.text((x+35, y), f'{n:02d}', font=font(23), fill=GOLD)
        layouts.append(dict(order=n, title=title, **layout))
    sheet.save(REVIEW / 'proposed-title-sheet.jpg', quality=95)
    (REVIEW / 'layouts.json').write_text(json.dumps(layouts, ensure_ascii=False, indent=2), encoding='utf8')
    print('Prepared nine title layouts.', flush=True)


def encode_title(n):
    target = OUT / f'{slug(n)}.mp4'
    source = preserve(target)
    temp = OUT / f'{slug(n)}.titles.mp4'
    before = metadata(source)
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(source),
        '-i', str(REVIEW / f'{slug(n)}-title.png'),
        '-filter_complex', f'[0:v][1:v]overlay=0:{TOP}:format=auto,format=yuv420p[v]',
        '-map', '[v]', '-an', '-fps_mode', 'passthrough', '-c:v', 'libx264',
        '-preset', 'fast', '-crf', '16', '-threads', '4',
        '-movflags', '+faststart', str(temp)], check=True)
    after = metadata(temp)
    assert before['frames'] == after['frames']
    assert abs(before['duration'] - after['duration']) < 1e-6
    assert before['timing_runs'] == after['timing_runs'] and after['faststart']
    # Inspect first, middle and final frames. Outside the header, differences
    # should be limited to the small error from re-encoding the existing video.
    errors = []
    for i, at in enumerate((0, before['duration']/2, before['duration']-1/FPS)):
        a, b = frame(source, at), frame(temp, at)
        aa, bb = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        delta = np.concatenate((aa[:TOP-8]-bb[:TOP-8], aa[BOTTOM+8:]-bb[BOTTOM+8:]))
        errors.append(float(np.sqrt(np.mean(delta*delta))))
        assert errors[-1] < 3, (n, at, errors[-1])
        b.save(REVIEW / f'{slug(n)}-verified-{i}.jpg', quality=94)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(temp),
                    '-f', 'null', '-'], check=True)
    temp.replace(target)
    preview_path = OUT / f'{slug(n)}-preview.webm'
    if preview_path.exists():
        preserve(preview_path)
    preview(n)
    e = episodes()[n]
    cover_path = OUT / f'{slug(n)}-cover.jpg'
    preserve(cover_path)
    cover = Image.open(cover_path).convert('RGB')
    draw = ImageDraw.Draw(cover)
    draw.rectangle((0, 540, W, 707), fill=BG)
    fitted_title(draw, e.get('video_title', e['title']), x=90, y=550,
                 width=860, max_height=145, size=56)
    cover.save(cover_path, quality=95)
    print(f'Title {n:02d} complete, {before["frames"]} frames retained.', flush=True)
    return dict(order=n, source_sha256=sha(source), video_sha256=sha(target),
                frames=after['frames'], duration=after['duration'],
                outside_header_rmse=errors, full_decode='pass')


def sync(rows):
    entries = episodes()
    path = OUT / 'manifest.json'
    preserve(path)
    manifest = json.loads(path.read_text(encoding='utf8'))
    for e in manifest['episodes']:
        n = e['order']
        if n not in NUMBERS:
            continue
        row = next(row for row in rows if row['order'] == n)
        e['published_video_sha256'] = e.get('published_video_sha256', row['source_sha256'])
        e['published_status'] = e.get('published_status', e['status'])
        e['status'] = 'revised_locally'
        e['video_title'] = entries[n].get('video_title', entries[n]['title'])
        e['video_sha256'] = row['video_sha256']
        e['video_bytes'] = (OUT/e['video']).stat().st_size
        e['video_revision'] = row['video_sha256'][:12]
    manifest['publishing_status'] = 'Nine video titles revised locally. Existing Instagram videos have not been replaced in this pass.'
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
    path = OUT / 'manifest.csv'; preserve(path)
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f); fields = reader.fieldnames; records = list(reader)
    if 'video_title' not in fields:
        fields.append('video_title')
    for row in records:
        n = int(row['order'])
        row['video_title'] = entries[n].get('video_title', entries[n]['title'])
        if n in NUMBERS:
            row['status'] = 'revised_locally'
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(records)
    path = OUT / 'index.html'; preserve(path)
    page = path.read_text(encoding='utf8')
    page, count = re.subn(r'const items=.*?;let current=0;',
        lambda _: 'const items='+json.dumps(manifest['episodes'], ensure_ascii=False).replace('</','<\\/')+';let current=0;',
        page, count=1, flags=re.S)
    assert count == 1
    page = page.replace("q('player').src=e.preview||e.video;", "q('player').src=(e.preview||e.video)+'?v='+(e.video_revision||e.video_sha256||'');")
    page = page.replace("+' · '+e.title", "+' · '+(e.video_title||e.title)")
    page = page.replace("+'  '+e.title", "+'  '+(e.video_title||e.title)")
    page = page.replace("q('player').poster=e.cover;", "q('player').poster=e.cover+'?v='+(e.video_revision||'');")
    note = '<p class="muted">Titles revised locally for reels 4, 5 and 7–13. These videos have not yet replaced the Instagram versions.</p>'
    page = page.replace('</header>', note+'</header>', 1)
    path.write_text(page, encoding='utf8')
    path = OUT / 'README.md'; preserve(path)
    text = path.read_text(encoding='utf8')
    text += '\nTitle refresh. Reels 4, 5 and 7–13 have revised headers and covers. Animation frames and 1.75× timing are preserved. These revisions are local only. Caption text and publishing receipts are unchanged. Run `retitle.py --prepare` then `retitle.py --render` to reproduce from the preserved inputs. The portable ZIP predates these revisions.\n'
    path.write_text(text, encoding='utf8')
    (REVIEW/'validation.json').write_text(json.dumps(rows, indent=2), encoding='utf8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    caption_paths = list(OUT.glob('*-caption.txt')) + [ROOT/'notes/reels/ccr2-series/reel-text.md']
    captions_before = {str(p): sha(p) for p in caption_paths}
    if args.prepare:
        prepare()
    if args.render:
        with ThreadPoolExecutor(max_workers=2) as pool:
            rows = list(pool.map(encode_title, NUMBERS))
        sync(rows)
    assert captions_before == {str(p): sha(p) for p in caption_paths}


if __name__ == '__main__':
    main()
