"""Rebuild the review deck using the existing videos and current revised additions.

This only packages the gallery. It does not render videos or edit the author's
Markdown. Original media filenames remain stable when gallery positions change.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import html
import json
import re

import render as series

OUT = series.OUT
REVISIONS = {
    17: ('casimir-stepwise/casimir-stepwise.mp4', 'casimir-stepwise/poster.jpg', 66),
    16: ('commutator-sphere/commutator-sphere.mp4', 'commutator-sphere/poster.jpg', 54),
    24: ('translation-eigenfunctions/symmetry-24.mp4',
         'translation-eigenfunctions/symmetry-24-cover.jpg', 26),
}

SCRIPT = r'''
const q = id => document.getElementById(id);
const video = q('video');
const assetUrl = (entry, key) => entry[key] + '?v=' + (entry[key + '_sha256'] || '').slice(0, 12);
let selected = 0;

function choose(index) {
  selected = Math.max(0, Math.min(items.length - 1, index));
  const entry = items[selected];
  video.pause();
  video.poster = assetUrl(entry, 'cover');
  video.src = assetUrl(entry, entry.preview_available && !entry.preview_stale ? 'preview' : 'video');
  q('title').textContent = String(entry.order).padStart(2, '0') + ' · ' + entry.title;
  q('caption').textContent = entry.caption;
  q('visual-argument').textContent = entry.required_visual_argument;
  q('desktop-links').replaceChildren();
  entry.desktop_sources.forEach((source, index) => {
    const link = document.createElement('a');
    link.href = '../../drafts/' + source;
    link.target = '_blank';
    link.textContent = 'Desktop original' + (entry.desktop_sources.length > 1 ? ' ' + (index + 1) : '');
    q('desktop-links').append(link);
  });
  q('count').textContent = entry.duration_seconds + ' seconds · Caption count ' + entry.caption_buffer_count + ' / 2196';
  q('availability').textContent = entry.video_available ? '' : 'Video is being prepared.';
  q('mp4').href = assetUrl(entry, 'video');
  q('cover').href = assetUrl(entry, 'cover');
  q('txt').href = assetUrl(entry, 'caption_file');
  q('elapsed').textContent = '0.0 / ' + entry.duration_seconds + ' s';
  q('previous').disabled = selected === 0;
  q('next').disabled = selected === items.length - 1;
  q('copy').textContent = 'Copy caption';
  document.querySelectorAll('nav button').forEach((button, index) => {
    button.classList.toggle('active', index === selected);
    if (index === selected) button.setAttribute('aria-current', 'true');
    else button.removeAttribute('aria-current');
  });
  history.replaceState(null, '', '#' + entry.order);
}

items.forEach((entry, index) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = String(entry.order).padStart(2, '0') + ' ' + entry.title;
  button.onclick = () => choose(index);
  q('nav').append(button);
});
q('previous').onclick = () => choose(selected - 1);
q('next').onclick = () => choose(selected + 1);
video.ontimeupdate = () => {
  q('elapsed').textContent = video.currentTime.toFixed(1) + ' / ' + items[selected].duration_seconds + ' s';
};
q('copy').onclick = async () => {
  try {
    await navigator.clipboard.writeText(items[selected].caption);
    q('copy').textContent = 'Copied';
    setTimeout(() => q('copy').textContent = 'Copy caption', 1800);
  } catch {
    const range = document.createRange();
    range.selectNodeContents(q('caption'));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    q('copy').textContent = 'Selected — press Ctrl+C';
  }
};
function chooseHash() {
  const number = Number(location.hash.slice(1));
  const index = items.findIndex(entry => entry.order === number);
  choose(index < 0 ? 0 : index);
}
window.addEventListener('hashchange', chooseHash);
chooseHash();
'''


def build():
    entries = series.entries()
    manifest_path = OUT / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    existing = {item['video']: item for item in manifest['episodes']}
    caption_dir = OUT / 'gallery-captions'
    caption_dir.mkdir(exist_ok=True)
    items = []
    for number, entry in entries.items():
        spec = series.SPEC_BY_NUMBER[number]
        if number in REVISIONS:
            video, cover, duration = REVISIONS[number]
            item = dict(video=video, cover=cover, duration_seconds=duration,
                        preview='', preview_available=False, preview_stale=True,
                        video_stale=False, cover_stale=False,
                        width=1080, height=1920, fps=30, audio='silent')
        else:
            source_video = f'symmetry-{spec["scene_number"]:02d}.mp4'
            item = copy.deepcopy(existing[source_video])
        item.update(order=number, title=entry['title'], caption=entry['caption'],
                    caption_buffer_count=entry['buffer_count'], source=entry['source'],
                    desktop_sources=spec['sources'], required_visual_argument=spec['required'],
                    on_screen_text=entry['on_screen_text'], status='offline review')
        # Derived captions have their own filenames, so adding entries cannot
        # overwrite caption files paired with the original numbered media.
        item['caption_file'] = f'gallery-captions/reel-{number:02d}.txt'
        (OUT / item['caption_file']).write_text(entry['caption'], encoding='utf8')
        for key in ('video', 'cover', 'caption_file'):
            path = OUT / item[key]
            if not path.is_file():
                raise FileNotFoundError(path)
            item[key + '_available'] = True
            item[key + '_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        items.append(item)
    assert [item['order'] for item in items] == list(range(1, 28))
    manifest['episodes'] = items
    manifest['text_source'] = 'notes/reels/symmetry-series-v2/reel-text.md'
    manifest['status'] = 'Offline review gallery with current revised Casimir and commutator videos'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf8')
    columns = ['order', 'title', 'video', 'cover', 'caption_file', 'duration_seconds', 'caption_buffer_count', 'status', 'caption']
    with (OUT / 'manifest.csv').open('w', newline='', encoding='utf-8-sig') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows({key: item[key] for key in columns} for item in items)

    # Preserve the existing review-page layout, replacing its data and routing.
    page = (OUT / 'index.html').read_text(encoding='utf8').split('<script>', 1)[0]
    page = re.sub(r'(<h1>Symmetry to Waves</h1>)<p>.*?</p>',
                  r'\1<p>27 reels from the pool table to complex waves, including the updated Casimir and commutator animations.</p>', page, count=1)
    data = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
    page += '<script>const items=' + data + ';' + SCRIPT + '</script></html>\n'
    (OUT / 'index.html').write_text(page, encoding='utf8')
    version = hashlib.sha256(page.encode()).hexdigest()[:12]
    for alias, number in [('casimir.html', 17), ('lie.html', 16)]:
        target = f'index.html?v={version}#{number}'
        title = html.escape(entries[number]['title'])
        redirect = (f'<!doctype html><html lang="en"><meta charset="utf-8">'
                    f'<meta http-equiv="refresh" content="0;url={target}">'
                    f'<title>{title}</title><p><a href="{target}">{title}</a></p>'
                    f'<script>location.replace({json.dumps(target)});</script></html>')
        (OUT / alias).write_text(redirect, encoding='utf8')
    print(f'Built {len(items)} entries in one viewer. Gallery version {version}', flush=True)


if __name__ == '__main__':
    build()
