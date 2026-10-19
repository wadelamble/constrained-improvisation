"""Initialize the editable review document once. Never overwrite author edits."""
import json
from pathlib import Path
import render
import scenes


def main():
    if render.TEXT.exists():
        raise FileExistsError(f'Preserving the editable document: {render.TEXT}')
    captions=json.loads((render.TEXT.parent/'captions.json').read_text(encoding='utf8'))
    by_number={e['number']:e for e in captions}
    assert sorted(by_number)==list(range(1,len(render.SPECS)+1))
    chunks=['''# Symmetry to Waves — complete desktop adaptation

Twenty-five offline reels follow the manuscript from the pool table through complex exponentials. Every desktop animation and diagram before Fourier has a place in this series. The previous sixteen-reel version remains available separately.

Edit the **Title** and **Caption** fields below. The gallery generates the series number, next-reel pointer, website link and hashtags automatically. Their characters count toward the caption limit. Titles and on-screen text are baked into the video and require a new render after editing.

The on-screen entries use stable ordered slots. Edit wording in place and preserve the number and order of entries. Equations use TeX for video rendering. Numeric readings are calculated from the animation. Source notes and visual checks are for offline review and are not posted.

Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/

#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics
''']
    for spec in render.SPECS:
        n=spec['number']; row=by_number[n]
        screen='\n'.join('- '+s for s in scenes.inventory(n))
        sources='\n'.join('- '+s for s in spec['sources']) or 'Additional animation of the manuscript’s equations.'
        chunks.append(f'''---

## Reel {n:02d}

### Title

{row['title']}

### Caption

{row['body']}

### On-screen text

{screen}

### Source

{row['source_note']}

{sources}

### Visual check

{spec['required']}
''')
    render.TEXT.write_text('\n'.join(chunks),encoding='utf8')
    entries=render.entries()
    print(f'Created editable document for {len(entries)} reels. Maximum full caption count: {max(e["buffer_count"] for e in entries.values())}')


if __name__=='__main__':
    main()
