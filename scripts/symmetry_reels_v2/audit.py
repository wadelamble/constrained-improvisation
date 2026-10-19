"""Inventory the actual manuscript visuals and verify the offline review package."""
from __future__ import annotations

import argparse
import json
import re
import render


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-media', action='store_true')
    args = parser.parse_args()
    draft = render.ROOT/'content/drafts/symmetry-draft.md'
    text = draft.read_text(encoding='utf8').split('## The Fourier Structure of Waves')[0]
    source_assets = []
    for reference in re.findall(r'\]\(([^)]+\.(?:mp4|svg|png))\)', text):
        path = (draft.parent/reference).resolve()
        relative = path.relative_to(draft.parent).as_posix()
        # Posters and contact sheets accompany their movies, not separate scenes.
        if relative.startswith('animations/') and path.suffix == '.png':
            continue
        assert path.is_file(), relative
        if relative not in source_assets:
            source_assets.append(relative)
    mapped = {source for spec in render.SPECS for source in spec['sources']}
    assert mapped == set(source_assets), {'unmapped': sorted(set(source_assets)-mapped),
                                         'extra': sorted(mapped-set(source_assets))}
    entries = render.entries()
    import scenes
    for n, entry in entries.items():
        assert len(entry['on_screen_text']) == len(scenes.inventory(n)), n
    if args.require_media:
        manifest = json.loads((render.OUT/'manifest.json').read_text(encoding='utf8'))
        assert len(manifest['episodes']) == len(entries)
        for e in manifest['episodes']:
            assert e['video_available'] and e['cover_available'], e['order']
            assert not e['video_stale'] and not e['cover_stale'], e['order']
            assert e['caption'] == entries[e['order']]['caption'], e['order']
    rows = ['# Desktop-to-reel coverage', '',
            f'{len(source_assets)} desktop animations and diagrams before Fourier are adapted across {len(entries)} reels.', '',
            'Posters and contact sheets are counted with their associated movie. Added equation demonstrations supplement the source visuals. The source manuscript, desktop media and first reel series remain unchanged.', '',
            '| Desktop original | Reel | Visual argument retained |',
            '|---|---|---|']
    for source in source_assets:
        specs = [s for s in render.SPECS if source in s['sources']]
        label = source.rsplit('/', 1)[-1]
        links = ', '.join(f'[{s["number"]:02d}](../../../content/reels/symmetry-series-v2/index.html#{s["number"]})' for s in specs)
        rows.append(f'| [{label}](../../../content/drafts/{source}) | {links} | ' + ' '.join(s['required'] for s in specs) + ' |')
    rows += ['', 'Additional reels explain the representation matrices (05), discrete invariants (08) and exponential eigenfunctions (22).', '',
             'Visual QA compares rendered sequences with the desktop sources. The final checks include encoded-video frames, label placement, caption limits, dimensions, frame rate and duration. Geometry checks cover D₃ closure, the invariant diagonal, tangent directions, boost intervals, eigencomponent recombination and reciprocal scaling.', '',
             'Reel 25 retains the fixed amplitude cylinder, fixed spatial slice, synchronized real and imaginary components, colored dial projections and wavelength bracket. Reels 20 and 21 use the same eigenbasis orientation.', '',
             'The gallery links each reel directly to its desktop source. Titles, captions and on-screen wording are editable in [reel-text.md](reel-text.md).', '']
    if (render.OUT/'casimir.html').exists():
        rows += ['A new [Casimir construction](../../../content/reels/symmetry-series-v2/casimir.html) is staged as Reel 15a. It supplements the 25 numbered reels without shifting their review numbers. Its caption and on-screen text are in the same editable document.', '']
    if (render.OUT/'lie.html').exists():
        rows += ['The new [Lie algebra continuation](../../../content/reels/symmetry-series-v2/lie.html), Reel 15b, follows the two rotation orders into their infinitesimal commutator. Its caption and on-screen text are also in the editable document.', '']
    (render.TEXT.parent/'desktop-coverage.md').write_text('\n'.join(rows), encoding='utf8')
    print(json.dumps({'desktop_visuals':len(source_assets), 'reels':len(entries),
                      'maximum_caption_count':max(e['buffer_count'] for e in entries.values()),
                      'duration_seconds':sum(e['duration'] for e in entries.values()),
                      'media_verified':args.require_media}))


if __name__ == '__main__':
    main()
