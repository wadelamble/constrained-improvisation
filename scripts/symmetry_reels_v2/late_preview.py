"""Render a compact review of the late portrait adaptations, without encoding."""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image, ImageDraw
from core import ROOT, BG, INK, font
from late import render, SCREEN_TEXT

OUT = ROOT / "content/reels/symmetry-series-v2/review/late"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    series = json.loads((Path(__file__).with_name("series.json")).read_text(encoding="utf-8"))
    samples = [0, 4, 8, 11, 15, 18, 21, 23.99]
    for entry in series:
        number = entry["number"]
        if number not in SCREEN_TEXT:
            continue
        sheet = Image.new("RGB", (4*360, 2*685), BG)
        d = ImageDraw.Draw(sheet)
        for i, q in enumerate(samples):
            t = entry["duration"]*q/24
            frame = render(number, t, entry)
            assert frame.size == (1080, 1920) and frame.mode == "RGB"
            frame.save(OUT / f"symmetry-{number:02d}-{q:05.2f}.png")
            col, row = i % 4, i // 4
            sheet.paste(frame.resize((360, 640), Image.Resampling.LANCZOS), (360*col, 685*row))
            d.text((360*col+16, 685*row+650), f"{t:.2f} s", font=font(24), fill=INK)
        sheet.save(OUT / f"symmetry-{number:02d}-contact-sheet.jpg", quality=92)
        print(number, entry["title"])


if __name__ == "__main__":
    main()
