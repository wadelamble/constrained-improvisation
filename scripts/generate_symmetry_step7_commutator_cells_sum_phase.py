from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

import generate_symmetry_step2_packet_summary_point as base
import generate_symmetry_step4_alternate_summary_histories as candidates


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "content" / "drafts" / "animations"
FFMPEG = base.FFMPEG
FFPROBE = base.FFPROBE

WIDTH = 1280
HEIGHT = 720
SCALE = 2
FPS = 24
DURATION = 13.5
FRAMES = round(DURATION * FPS)

BG = base.BG
PANEL = base.PANEL
INK = base.INK
MUTED = base.MUTED
FAINT = base.FAINT
GREEN = base.GREEN
PURPLE = (117, 85, 145)
GOLD = (198, 138, 45)
LIGHT_GOLD = (238, 216, 170)
LIGHT_BLUE = (172, 199, 221)

TITLE = base.TITLE
SUBTITLE = base.SUBTITLE
PANE_TITLE = base.PANE_TITLE
LABEL = base.LABEL
LABEL_BOLD = base.LABEL_BOLD
SMALL = base.SMALL
FINAL = base.FINAL

X_MIN = candidates.X_MIN
X_MAX = candidates.X_MAX
K_MIN = candidates.K_MIN
K_MAX = candidates.K_MAX
PLOT = (102.0, 188.0, 815.0, 565.0)


def s(value: float) -> int:
    return int(round(value * SCALE))


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return color[0], color[1], color[2], max(0, min(255, round(alpha * 255)))


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def interval(seconds: float, start: float, end: float) -> float:
    if end <= start:
        return 1.0 if seconds >= end else 0.0
    return smoothstep((seconds - start) / (end - start))


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fill=INK,
    font_obj=LABEL,
    anchor: str | None = None,
) -> None:
    draw.text((s(xy[0]), s(xy[1])), text, fill=fill, font=font_obj, anchor=anchor)


def panel(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float]) -> None:
    draw.rounded_rectangle(
        tuple(s(v) for v in bounds),
        radius=s(13),
        fill=PANEL,
        outline=FAINT,
        width=s(2),
    )


def map_x(x: float) -> float:
    left, _, right, _ = PLOT
    return left + (x - X_MIN) / (X_MAX - X_MIN) * (right - left)


def map_k(k: float) -> float:
    _, top, _, bottom = PLOT
    return bottom - (k - K_MIN) / (K_MAX - K_MIN) * (bottom - top)


def point(candidate, u: float) -> tuple[float, float]:
    x, k = candidate(u)
    return map_x(x), map_k(k)


def path(candidate, start: float, end: float, samples: int = 320) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    for index in range(samples):
        u = start + (end - start) * index / (samples - 1)
        px, py = point(candidate, u)
        points.append((s(px), s(py)))
    return points


def region_polygon() -> list[tuple[int, int]]:
    return path(candidates.candidate_a, 0.0, 1.0) + path(candidates.candidate_b, 1.0, 0.0)


def draw_axes(draw: ImageDraw.ImageDraw) -> None:
    left, top, right, bottom = PLOT
    draw.line((s(left), s(top), s(left), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw.line((s(left), s(bottom), s(right), s(bottom)), fill=rgba(MUTED, 0.70), width=s(2))
    draw_text(draw, (right + 1, bottom + 22), "x-shift", fill=MUTED, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (left - 8, top), "k-shift", fill=MUTED, font_obj=LABEL_BOLD, anchor="rs")


def draw_endpoints(draw: ImageDraw.ImageDraw) -> None:
    start = point(candidates.candidate_a, 0.0)
    finish = point(candidates.candidate_a, 1.0)
    for p in (start, finish):
        draw.ellipse((s(p[0] - 7), s(p[1] - 7), s(p[0] + 7), s(p[1] + 7)), fill=INK)
    draw_text(draw, (start[0] - 11, start[1] + 15), "A", fill=INK, font_obj=LABEL_BOLD, anchor="ra")
    draw_text(draw, (finish[0] + 11, finish[1] - 10), "B", fill=INK, font_obj=LABEL_BOLD)


def make_region_mask() -> Image.Image:
    mask = Image.new("L", (WIDTH * SCALE, HEIGHT * SCALE), 0)
    ImageDraw.Draw(mask).polygon(region_polygon(), fill=255)
    return mask


REGION_MASK = make_region_mask()


def tile_rectangles() -> list[tuple[int, int, int, int]]:
    left, top, right, bottom = PLOT
    cell_w = 52.0
    cell_h = 39.0
    rects: list[tuple[int, int, int, int]] = []
    y = top
    while y < bottom:
        x = left
        while x < right:
            rect = (s(x), s(y), s(min(x + cell_w, right)), s(min(y + cell_h, bottom)))
            crop = REGION_MASK.crop(rect)
            if crop.getbbox() is not None:
                rects.append(rect)
            x += cell_w
        y += cell_h

    focus_x = s(525.0)
    focus_y = s(388.0)
    rects.sort(key=lambda r: ((r[0] + r[2]) / 2 - focus_x) ** 2 + ((r[1] + r[3]) / 2 - focus_y) ** 2)
    return rects


TILES = tile_rectangles()


def draw_tiled_region(image: Image.Image, reveal: float, show_focus: bool) -> None:
    region_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    region_draw = ImageDraw.Draw(region_layer, "RGBA")
    region_draw.polygon(region_polygon(), fill=rgba(LIGHT_GOLD, 0.23))
    image.alpha_composite(region_layer)

    if reveal <= 0 and not show_focus:
        return

    count = min(len(TILES), max(0, math.ceil(reveal * len(TILES))))
    if show_focus:
        count = max(count, 1)

    tile_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    tile_draw = ImageDraw.Draw(tile_layer, "RGBA")
    for index, rect in enumerate(TILES[:count]):
        fill = rgba(GOLD if index == 0 else LIGHT_BLUE, 0.38 if index == 0 else 0.24)
        outline = rgba(GOLD if index == 0 else MUTED, 0.95 if index == 0 else 0.46)
        tile_draw.rectangle(rect, fill=fill, outline=outline, width=s(2 if index == 0 else 1))

    clipped_alpha = ImageChops.multiply(tile_layer.getchannel("A"), REGION_MASK)
    tile_layer.putalpha(clipped_alpha)
    image.alpha_composite(tile_layer)


def arrow_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color,
    width: int = 4,
) -> None:
    draw.line((s(start[0]), s(start[1]), s(end[0]), s(end[1])), fill=color, width=s(width))
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 9.0
    p1 = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    p2 = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon([(s(end[0]), s(end[1])), (s(p1[0]), s(p1[1])), (s(p2[0]), s(p2[1]))], fill=color)


def draw_cell_inset(draw: ImageDraw.ImageDraw, progress: float, formula_alpha: float) -> None:
    panel(draw, (875, 108, 1245, 379))
    draw_text(draw, (897, 129), "one commutator cell", font_obj=PANE_TITLE)
    draw_text(draw, (897, 157), "close the local x-k loop", fill=MUTED, font_obj=SMALL)

    left, top, right, bottom = 954.0, 187.0, 1167.0, 267.0
    points = [
        (right, top),
        (right, bottom),
        (left, bottom),
        (left, top),
        (right, top),
    ]
    draw.rectangle((s(left), s(top), s(right), s(bottom)), fill=rgba(LIGHT_GOLD, 0.18), outline=rgba(MUTED, 0.34), width=s(2))
    for index in range(4):
        color = GOLD if progress >= (index + 1) / 4 else rgba(MUTED, 0.30)
        arrow_segment(draw, points[index], points[index + 1], color, width=4 if progress >= (index + 1) / 4 else 2)
    draw.ellipse((s(right - 6), s(top - 6), s(right + 6), s(top + 6)), fill=GREEN)
    draw_text(draw, ((left + right) / 2, bottom + 15), "δx", fill=MUTED, font_obj=SMALL, anchor="ma")
    draw_text(draw, (left - 12, (top + bottom) / 2), "δk", fill=MUTED, font_obj=SMALL, anchor="rm")

    if formula_alpha > 0:
        color = rgba(INK, formula_alpha)
        draw_text(draw, (1060, 303), "T(δx) M(δk) T(−δx) M(−δk)", fill=color, font_obj=SMALL, anchor="mm")
        draw_text(draw, (1060, 329), "= exp(−i δx δk) I", fill=color, font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (1060, 355), "same x and k shifts; common phase changed", fill=rgba(MUTED, formula_alpha), font_obj=SMALL, anchor="mm")


def draw_phase_dial(draw: ImageDraw.ImageDraw, reveal: float) -> None:
    cx, cy, radius = 1060.0, 556.0, 50.0
    draw.ellipse((s(cx - radius), s(cy - radius), s(cx + radius), s(cy + radius)), outline=rgba(MUTED, 0.56), width=s(2))
    draw.line((s(cx - radius - 7), s(cy), s(cx + radius + 7), s(cy)), fill=rgba(MUTED, 0.28), width=s(1))
    draw.line((s(cx), s(cy - radius - 7), s(cx), s(cy + radius + 7)), fill=rgba(MUTED, 0.28), width=s(1))
    draw.line((s(cx), s(cy), s(cx + radius * 0.82), s(cy)), fill=rgba(MUTED, 0.52), width=s(3))

    # The chosen orientation gives a negative phase angle, so the hand turns clockwise.
    angle = -0.56 * reveal
    end = (cx + radius * 0.82 * math.cos(angle), cy - radius * 0.82 * math.sin(angle))
    arrow_segment(draw, (cx, cy), end, GOLD, width=4)
    draw.ellipse((s(cx - 4), s(cy - 4), s(cx + 4), s(cy + 4)), fill=INK)
    draw_text(draw, (1060, 622), "cell phase angles add", fill=MUTED, font_obj=SMALL, anchor="mm")


def draw_sum_panel(draw: ImageDraw.ImageDraw, reveal: float, alpha: float) -> None:
    panel(draw, (875, 395, 1245, 643))
    draw_text(draw, (897, 416), "all cells", font_obj=PANE_TITLE)
    if alpha > 0:
        draw_text(draw, (1060, 458), "∏ exp(−i δx δk)", fill=rgba(INK, alpha), font_obj=LABEL_BOLD, anchor="mm")
        draw_text(draw, (1060, 486), "= exp(−i Aₓₖ)", fill=rgba(INK, alpha), font_obj=LABEL_BOLD, anchor="mm")
    draw_phase_dial(draw, reveal)


def draw_frame(frame: int) -> Image.Image:
    seconds = min(DURATION - 1 / FPS, frame / FPS)
    focus_alpha = interval(seconds, 1.2, 2.0)
    cell_progress = interval(seconds, 2.0, 4.5)
    formula_alpha = interval(seconds, 4.2, 5.0)
    tile_reveal = interval(seconds, 5.0, 9.7)
    sum_alpha = interval(seconds, 8.2, 9.7)
    final_hold = seconds >= 10.0

    image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), BG + (255,))
    draw = ImageDraw.Draw(image, "RGBA")
    draw_text(draw, (42, 31), "Step 7 — Tile the x-k region with commutator cells", font_obj=TITLE)
    draw_text(
        draw,
        (42, 72),
        "Each closed cell returns to the same x and k shifts while changing the common phase.",
        fill=MUTED,
        font_obj=SUBTITLE,
    )

    panel(draw, (35, 108, 850, 643))
    draw_text(draw, (58, 129), "the region agreed on in Step 6", font_obj=PANE_TITLE)
    draw_text(draw, (58, 157), "many local loops fill the two-dimensional x-k area", fill=MUTED, font_obj=SMALL)
    draw_axes(draw)
    draw_tiled_region(image, tile_reveal, focus_alpha > 0)
    draw = ImageDraw.Draw(image, "RGBA")
    draw.line(path(candidates.candidate_a, 0.0, 1.0), fill=GREEN, width=s(4), joint="curve")
    draw.line(path(candidates.candidate_b, 0.0, 1.0), fill=PURPLE, width=s(4), joint="curve")
    draw_endpoints(draw)
    if tile_reveal <= 0.02:
        draw_text(draw, (458, 605), "one highlighted cell first", fill=GOLD if focus_alpha > 0 else MUTED, font_obj=SMALL, anchor="mm")
    else:
        draw_text(draw, (458, 605), "shared cell edges cancel; the outer boundary remains", fill=MUTED, font_obj=SMALL, anchor="mm")

    draw_cell_inset(draw, cell_progress, formula_alpha)
    draw_sum_panel(draw, tile_reveal, sum_alpha)

    if final_hold:
        footer = "The cells sum to the x-k/CCR contribution—not yet the complete history phase difference."
        draw_text(draw, (640, 681), footer, fill=GREEN, font_obj=FINAL, anchor="mm")
    elif seconds < 5.0:
        footer = "One local cell contributes a common phase whose sign reverses with the loop orientation."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")
    else:
        footer = "Multiplying cell phases adds their phase angles."
        draw_text(draw, (640, 681), footer, fill=MUTED, font_obj=SMALL, anchor="mm")

    return image.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def make_contact_sheet(name: str) -> Path:
    sample_seconds = (0.9, 3.0, 5.0, 7.4, 11.4)
    labels = ("agreed region", "one closed cell", "one cell phase", "tiles accumulate", "CCR contribution")
    thumb_w = 384
    thumb_h = 216
    label_h = 26
    margin = 15
    sheet = Image.new("RGB", (3 * thumb_w + 4 * margin, 2 * (thumb_h + label_h) + 3 * margin), BG)
    sheet_draw = ImageDraw.Draw(sheet)
    for index, (seconds, label) in enumerate(zip(sample_seconds, labels)):
        col = index % 3
        row = index // 3
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_h + margin)
        frame = min(FRAMES - 1, round(seconds * FPS))
        thumb = draw_frame(frame).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        sheet_draw.text((x + 4, y + thumb_h + 4), label, fill=MUTED)
    output = OUTPUT_DIR / f"{name}-contact-sheet.png"
    sheet.save(output)
    return output


def verify_video(video: Path) -> str:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "stream=codec_name,pix_fmt,width,height,r_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def render() -> tuple[Path, Path, Path]:
    name = "symmetry-step7-commutator-cells-sum-phase"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scratch = OUTPUT_DIR / f"_{name}_frames"
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir()
    video = OUTPUT_DIR / f"{name}.mp4"
    final_still = OUTPUT_DIR / f"{name}-final.png"
    try:
        for index in range(FRAMES):
            draw_frame(index).save(scratch / f"frame_{index:04d}.png")
        draw_frame(FRAMES - 1).save(final_still)
        encoded = subprocess.run(
            [
                str(FFMPEG),
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(scratch / "frame_%04d.png"),
                "-c:v",
                "libx264",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(video),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if encoded.returncode != 0 or not video.exists() or video.stat().st_size == 0:
            raise RuntimeError("ffmpeg failed to encode the animation")
        contact = make_contact_sheet(name)
        return video, contact, final_still
    finally:
        if scratch.exists():
            shutil.rmtree(scratch)


def main() -> None:
    video, contact, final_still = render()
    print(video)
    print(contact)
    print(final_still)
    print(verify_video(video))


if __name__ == "__main__":
    main()
