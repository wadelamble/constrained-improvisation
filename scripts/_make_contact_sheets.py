from pathlib import Path
import imageio.v3 as iio
from PIL import Image, ImageOps, ImageDraw

root = Path(r'C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\drafts\animations')
files = ['liouville-permutation-3card.mp4', 'liouville-contours-quartic.mp4']

for name in files:
    path = root / name
    all_frames = list(iio.imiter(path))
    n = len(all_frames)
    idxs = [0, max(0, n // 4), max(0, n // 2), max(0, 3 * n // 4), n - 1]
    frames = []
    for idx in idxs:
        arr = all_frames[idx]
        img = Image.fromarray(arr).convert('RGB')
        img = ImageOps.contain(img, (360, 260))
        canvas = Image.new('RGB', (380, 300), 'white')
        canvas.paste(img, ((380 - img.width) // 2, 20))
        d = ImageDraw.Draw(canvas)
        d.text((12, 270), f'frame {idx}', fill='black')
        frames.append(canvas)
    sheet = Image.new('RGB', (380 * len(frames), 300), '#f4f4f4')
    for i, frame in enumerate(frames):
        sheet.paste(frame, (380 * i, 0))
    out = root / (path.stem + '-contact-sheet.png')
    sheet.save(out)
    print(out)
