"""Build the local reviewed series without replacing earlier previews or publishing.

Run from the project root with the project's Python runtime. Source reel labels
stay stable in the editable Markdown. Export order is consecutive after removals.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from core import ROOT, W, H, FPS, BG, INK, MUTED, GOLD, font, fitted_title, numbering_overlay, equation
from PIL import Image, ImageDraw
import imageio_ffmpeg
from render import buffer_count, caption_math_text

TEXT = ROOT / 'notes/reels/symmetry-series-v2/reel-text.md'
OLD = ROOT / 'content/reels/symmetry-series-v2'
OUT = ROOT / 'content/reels/symmetry-series-stage'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def read_entries():
    raw = TEXT.read_bytes()
    document = raw.decode('utf-8-sig').replace('\r\n', '\n')
    parts = re.split(r'^## Reel\s+(.+?)\s*$', document, flags=re.M)
    entries = []
    excluded = []
    for index in range(1, len(parts), 2):
        label, section = parts[index:index+2]
        if '[remove]' in label.lower():
            excluded.append(label)
            continue
        source_id = label.lstrip('0') or '0'
        fields = re.split(r'^###\s+(.+?)\s*$', section, flags=re.M)
        fields = {fields[i].strip().lower(): fields[i+1].strip().removesuffix('---').rstrip()
                  for i in range(1, len(fields), 2)}
        title, body = fields['title'], fields['caption']
        assert title and '\n' not in title and body, source_id
        entries.append(dict(order=len(entries)+1, source_id=source_id, title=title, body=body,
                            on_screen_text=[s[2:].strip() for s in fields.get('on-screen text', '').splitlines() if s.startswith('- ')],
                            source=fields.get('source', ''), visual_check=fields.get('visual check', '')))
    assert len(entries) == 27 and excluded == ['20 [remove]'], (len(entries), excluded)
    assert len({e['source_id'] for e in entries}) == len(entries)
    for i, e in enumerate(entries):
        next_line = f'Next: {entries[i+1]["title"]}' if i+1 < len(entries) else 'Continue with Waves to Quanta'
        text = (f'Symmetry to Waves · {e["order"]}/{len(entries)}\n{e["title"]}\n\n{e["body"]}\n\n'
                f'{next_line}\nFull chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/\n\n'
                '#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics')
        text = caption_math_text(text)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text, flags=re.S)
        e['caption'] = text
        e['caption_buffer_count'] = buffer_count(text)
        assert e['caption_buffer_count'] <= 2196, (e['order'], e['caption_buffer_count'])
        assert '**' not in text and '[remove]' not in text
    (OUT/'source/reel-text.md').write_bytes(raw)
    save_json(OUT/'source/entries.json', entries)
    return entries, hashlib.sha256(raw).hexdigest()


def metadata(path):
    frames = imageio_ffmpeg.read_frames(str(path))
    try:
        return next(frames)
    finally:
        frames.close()


def sources(entries):
    previous = {str(e['order']): e for e in json.loads((OLD/'manifest.json').read_text(encoding='utf8'))['episodes']}
    overrides = {
        '16': 'commutator-sphere/commutator-sphere.mp4',
        '17': 'casimir-stepwise/casimir-stepwise.mp4',
        '24': 'translation-eigenfunctions/symmetry-24.mp4',
        '24a': 'translation-unitarity/translation-unitarity.mp4',
    }
    for e in entries:
        source_id = e['source_id']
        path = OLD/(overrides[source_id] if source_id in overrides else previous[source_id]['video'])
        assert path.exists(), path
        info = metadata(path)
        assert info['size'] == (W, H) and info['fps'] == FPS, (path, info)
        e['source_video'] = path.relative_to(ROOT).as_posix()
        e['source_video_sha256'] = sha(path)
        e['duration_seconds'] = info['duration']
        if source_id == '24a':
            baseline = (OUT/'source/reel-text-before-staging.md').read_text(encoding='utf-8-sig')
            section = re.search(r'^## Reel 24a\s*\n(.*?)(?=^## Reel |\Z)', baseline, re.M|re.S).group(1)
            inventory = re.search(r'^### On-screen text\s*\n(.*?)(?=^### |\Z)', section, re.M|re.S).group(1)
            expected_text = [s[2:].strip() for s in inventory.splitlines() if s.startswith('- ')]
        else:
            expected_text = previous[source_id]['on_screen_text']
        if source_id == '27':
            expected_text = [r'(T_a z)(x,t)=z(x-a,t)=e^{-ika}z(x,t)' if s == r'z(x-a,t)=e^{-ika}z(x,t)' else s for s in expected_text]
        assert e['on_screen_text'] == expected_text, f'Reel {source_id}: on-screen text changed. Update its scientific render before staging.'
    return entries


def create_overlay(e):
    im = numbering_overlay(e['order'], 27)
    d = ImageDraw.Draw(im)
    d.rectangle((60, 263, 975, 410), fill=BG)
    layout = fitted_title(d, e['title'])
    if e['source_id'] == '16':
        # This standalone scene uses a lower, wider progress/footer area.
        # Leave its moving rule at y=1708 visible and clear the whole timer.
        d.rectangle((60, 1692, 975, 1790), fill=(0, 0, 0, 0))
        d.rectangle((60, 1736, 1025, 1800), fill=BG)
        d.text((70, 1750), 'A series in 27 parts', font=font(25), fill=MUTED, anchor='la')
        d.text((950, 1750), '16 / 27', font=font(25), fill=MUTED, anchor='ra')
    if e['source_id'] == '17':
        d.rectangle((60, 1692, 800, 1790), fill=BG)
        d.text((70, 1717), 'Ordinary 3D vector representation', font=font(25), fill=MUTED, anchor='la')
    if e['source_id'] == '27':
        d.rectangle((70, 1504, 950, 1572), fill=BG)
        pic = equation(r'(T_a z)(x,t)=z(x-a,t)=e^{-ika}z(x,t)', size=47)
        im.paste(pic, (round(510-pic.width/2), round(1538-pic.height/2)), pic)
    path = OUT/'overlays'/f'reel-{e["order"]:02d}.png'
    im.save(path)
    return path, layout


def run(command):
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf8', errors='replace'))


def build_one(e):
    start = time.time()
    n = e['order']
    stem = f'reel-{n:02d}'
    source = ROOT/e['source_video']
    overlay, layout = create_overlay(e)
    video = OUT/f'{stem}.mp4'
    record_path = OUT/'records'/f'{stem}.json'
    key = dict(source=e['source_video_sha256'], overlay=sha(overlay), encoder='overlay-v1-crf18')
    previous = json.loads(record_path.read_text(encoding='utf8')) if record_path.exists() else {}
    reused = video.exists() and previous.get('render_key') == key
    if not reused:
        temporary = OUT/f'{stem}.rendering.mp4'
        run([FFMPEG, '-y', '-v', 'error', '-i', str(source), '-loop', '1', '-i', str(overlay),
             '-filter_complex', '[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]',
             '-map', '[v]', '-an', '-t', str(e['duration_seconds']), '-r', str(FPS),
             '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-threads', '2',
             '-filter_complex_threads', '1', '-movflags', '+faststart', str(temporary)])
        temporary.replace(video)
    info = metadata(video)
    assert info['size'] == (W, H) and info['fps'] == FPS
    assert abs(info['duration']-e['duration_seconds']) < .1
    assert info.get('audio_codec') is None or (reused and previous.get('audio_render_key')), info
    # Decode the exported file, rather than looking only at generator images.
    frame = OUT/'review'/f'{stem}-frame.png'
    run([FFMPEG, '-y', '-v', 'error', '-ss', str(.76*e['duration_seconds']), '-i', str(video),
         '-frames:v', '1', str(frame)])
    decoded = Image.open(frame).convert('RGB')
    cover_fraction = {'2': .98, '9': .65, '14': .50, '26': .67}.get(e['source_id'], .94)
    cover_frame = OUT/'review'/f'{stem}-cover-frame.png'
    run([FFMPEG, '-y', '-v', 'error', '-ss', str(cover_fraction*e['duration_seconds']), '-i', str(video),
         '-frames:v', '1', str(cover_frame)])
    cover_decoded = Image.open(cover_frame).convert('RGB')
    cover = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(cover)
    d.text((90, 405), 'VARIATIONS ON SYMMETRY', font=font(27, True), fill=MUTED)
    d.text((90, 464), f'{n:02d}  /  SYMMETRY TO WAVES', font=font(30, True), fill=GOLD)
    cover_layout = fitted_title(d, e['title'], x=90, y=525, width=860, max_height=158, size=56)
    cover.paste(cover_decoded.crop((70,470,950,1640)).resize((660,878), Image.Resampling.LANCZOS), (210,709))
    cover.save(OUT/f'{stem}-cover.jpg', quality=95)
    run([FFMPEG, '-y', '-v', 'error', '-i', str(video), '-vf',
         f'fps={9/e["duration_seconds"]},scale=270:480,tile=3x3', '-frames:v', '1',
         '-q:v', '2', str(OUT/'review'/f'{stem}-contact-sheet.jpg')])
    (OUT/'captions'/f'{stem}.txt').write_text(e['caption'], encoding='utf8')
    e.update(video=video.name, cover=f'{stem}-cover.jpg', caption_file=f'captions/{stem}.txt',
             width=W, height=H, fps=FPS, audio='embedded AAC soundtrack' if info.get('audio_codec') else 'silent', status='local staged review')
    for name in ('video', 'cover', 'caption_file'):
        e[f'{name}_sha256'] = sha(OUT/e[name])
    record = dict(render_key=key, metadata=info, title_layout=layout,
                  cover_title_layout=cover_layout, cover_time_seconds=cover_fraction*e['duration_seconds'])
    if reused:
        record.update({name: value for name, value in previous.items() if name.startswith('audio_')})
    save_json(record_path, record)
    print(f'{n:02d}/27  {e["duration_seconds"]:g}s  {e["caption_buffer_count"]} caption characters  {time.time()-start:.1f}s build', flush=True)
    return e


def package(entries, text_hash):
    cursor = 0.
    for e in entries:
        e['music_start_seconds'] = cursor
        cursor += e['duration_seconds']
        if e['source_id'] in ('16', '17'):
            e['authored_on_screen_inventory'] = e.pop('on_screen_text')
            e['on_screen_inventory_note'] = 'The authoring inventory describes an earlier version. The staged video preserves the latest approved commutator-sphere or casimir-stepwise visual, including its intentional label removals.'
        elif e['source_id'] == '27':
            e['on_screen_text'] = [r'(T_a z)(x,t)=z(x-a,t)=e^{-ika}z(x,t)' if s == r'z(x-a,t)=e^{-ika}z(x,t)' else s for s in e['on_screen_text']]
    music_path = OUT/'source/music.json'
    music = json.loads(music_path.read_text(encoding='utf8')) if music_path.exists() else dict(status='pending')
    baked = all(e.get('audio') == 'embedded AAC soundtrack' for e in entries)
    music.update(mode='embedded soundtrack' if baked else 'linked preview only', baked_into_exports=baked)
    if music.get('local_source') and not baked:
        music['status'] = 'pending'
    manifest = dict(series='Symmetry to Waves', status='local staged review', created_at=datetime.now(timezone.utc).isoformat(),
                    text_source=TEXT.relative_to(ROOT).as_posix(), text_sha256=text_hash,
                    music=music,
                    episodes=entries)
    save_json(OUT/'manifest.json', manifest)
    with (OUT/'manifest.csv').open('w', newline='', encoding='utf-8-sig') as f:
        fields = ['order', 'source_id', 'title', 'duration_seconds', 'caption_buffer_count', 'video', 'cover', 'caption_file', 'music_start_seconds']
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader(); writer.writerows(entries)
    review = ['# Symmetry to Waves — staged captions\n',
              'This is the sequential export snapshot. Edit the authoritative `notes/reels/symmetry-series-v2/reel-text.md` and rebuild. Its original labels stay stable while review is in progress.\n']
    for e in entries:
        review.extend([f'## Reel {e["order"]:02d}\n', f'Original source label: {e["source_id"]}. Caption count including footer: {e["caption_buffer_count"]}/2196.\n',
                       f'### Title\n\n{e["title"]}\n', f'### Caption\n\n{e["body"]}\n'])
    (OUT/'reel-text-staged.md').write_text('\n'.join(review), encoding='utf8')
    readme = '''# Local staged reels

Open `index.html` through the project HTTP server. The series contains 27 reels numbered consecutively. Original reel 20 is omitted. Original 24a becomes staged reel 24. The latest commutator and Casimir animations are staged reels 16 and 17.

Titles, numbering, covers, captions, and next-reel pointers come from the current editable text. Scientific motion is preserved from the latest reviewed MP4s. The source snapshot and mechanical edit record are in `source/`. Original reel labels remain in the editable source to avoid disrupting ongoing review.

## Music

The MP4 exports are silent. The selected recording in `source/music.json` supplies quiet linked music in the preview, with excerpt positions and fades. A local audio source is required to mix music into the actual exports. Nothing has been uploaded or scheduled.

## Rebuild

Run `scripts/symmetry_reels_v2/stage.py` with the project Python runtime from the repository root. It reads `notes/reels/symmetry-series-v2/reel-text.md`, preserves the earlier previews, and caches videos when their source footage and title overlays are unchanged. The CSV is a local inventory, not a social-platform import template.
'''
    (OUT/'README.md').write_text(readme, encoding='utf8')
    for group in range(3):
        sheet = Image.new('RGB', (900, 1710), BG)
        d = ImageDraw.Draw(sheet)
        for i, e in enumerate(entries[group*9:(group+1)*9]):
            x,y=(i%3)*300,(i//3)*570
            image = Image.open(OUT/'review'/f'reel-{e["order"]:02d}-frame.png')
            sheet.paste(image.resize((300,533), Image.Resampling.LANCZOS), (x,y))
            d.text((x+12,y+537),f'Reel {e["order"]:02d}',font=font(20),fill=INK)
        sheet.save(OUT/'review'/f'overview-{group+1}.jpg',quality=94)
    assert sha(TEXT) == text_hash, 'The editable source changed during staging. Rebuild to incorporate the newest edits.'
    save_json(OUT/'validation.json', dict(status='passed', count=len(entries), dimensions=[W,H], fps=FPS,
             max_caption_count=max(e['caption_buffer_count'] for e in entries), caption_limit=2196,
             total_duration_seconds=sum(e['duration_seconds'] for e in entries),
             sources_unchanged=True, text_sha256=text_hash,
             tests=['source and exported dimensions, frame rate, and duration', 'all captions within limit',
                    'consecutive ordering and current next-title pointers', 'unique source mapping with 20 removed and 24a included',
                    'decoded contact sheets and frames generated for every export', 'asset hashes recorded',
                    'source text unchanged during build'],
             audio='embedded AAC soundtrack' if baked else 'silent exports; music is linked preview only'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    for folder in ('source','captions','records','overlays','review'):
        (OUT/folder).mkdir(parents=True, exist_ok=True)
    entries, text_hash = read_entries()
    entries = sources(entries)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = [future.result() for future in as_completed([pool.submit(build_one, e) for e in entries])]
    package(sorted(results, key=lambda e:e['order']), text_hash)
    music = json.loads((OUT/'source/music.json').read_text(encoding='utf8')) if (OUT/'source/music.json').exists() else {}
    if music.get('local_source'):
        from stage_audio import mix_stage
        mix_stage(workers=args.workers)
    print('Local stage complete. No accounts contacted or publishing performed.', flush=True)


if __name__ == '__main__':
    main()
