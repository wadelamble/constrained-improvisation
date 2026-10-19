"""Local visual review of the early v2 scenes; no manuscript side effects."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw
import early
from core import ROOT, BG, INK, font

SAMPLES = {
    4: [0, 3.4, 5.0, 7.9, 10, 12.5, 15, 18, 21.9],
    6: [0, 5, 7, 10, 12, 16, 19, 23, 29.9],
    9: [0, 3, 6, 9, 12, 15, 18, 21, 23.9],
    10: [0, 5.5, 7.9, 9.7, 11.5, 13.5, 15.5, 20, 23.9],
    12: [0, 3, 6, 9.5, 11, 14, 19, 23, 29.9],
}


def main():
    out = ROOT/'content/reels/symmetry-series-v2/review/early'
    out.mkdir(parents=True, exist_ok=True)
    entries = {entry['number']: entry for entry in json.loads((Path(__file__).with_name('series.json')).read_text(encoding='utf-8'))}
    result = early.validate()
    for number, samples in SAMPLES.items():
        sheet = Image.new('RGB', (1080, 2034), BG)
        draw = ImageDraw.Draw(sheet)
        for index, time in enumerate(samples):
            im = early.render(number, time, entries[number])
            assert im.size == (1080, 1920) and im.mode == 'RGB'
            im.save(out/f'early-{number:02d}-{time:04.1f}.png')
            col, row = index % 3, index // 3
            sheet.paste(im.resize((360, 640), Image.Resampling.LANCZOS), (col*360, row*678))
            draw.text((col*360+12, row*678+645), f'{time:g} s', font=font(23), fill=INK)
        sheet.save(out/f'early-{number:02d}-contact.jpg', quality=93)
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'validated': result, 'episodes': list(SAMPLES), 'review': str(out)}))


if __name__ == '__main__':
    main()
