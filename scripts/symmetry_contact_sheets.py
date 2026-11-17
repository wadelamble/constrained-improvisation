"""Render the illustrated Symmetry chapter using its print review's frame selections."""

from html import escape
from pathlib import PurePosixPath


SUPPLEMENT_PATH = "/symmetry/contact-sheets/"
BARBER_GIF = "https://i.pinimg.com/originals/bc/5f/5d/bc5f5d496a9cf2a7bd6038541b4501f2.gif"

# Each pair is a zero-based position in the 12-sample archive and its print annotation.
WIDE_STILLS = {
    "symmetry-pool-table": ((8, "Rotation"), (11, "Velocity boost")),
    "symmetry-casimir-operator": (
        (6, "Applying the three squared generators to v gives three vectors that sum to −2v."),
        (11, "The Casimir acts as twice the identity."),
    ),
    "symmetry-translation-unitarity": (
        (0, "Before translation, the coefficient products are 0.570 and 0.397 + 0.409i."),
        (7, "After translation, the products are 15.454 and 0.397 + 0.409i."),
    ),
}

# These six decoded movie indices show the triangle actions in progress. Four lie
# between the uniform archive samples and are shipped alongside the chapter.
TRIANGLE_INDICES = (0, 76, 135, 196, 249, 332)
TRIANGLE_MOVIE_SHA256 = "e3ef96d8b5a6065fd1f208d26e79647ed639f6e68065279a094e0ffc369862bb"


def _selected_frames(slug, frames):
    if slug in WIDE_STILLS:
        return [(frames[i], note) for i, note in WIDE_STILLS[slug]]
    if slug == "symmetry-operator-sandwich":
        return [(frames[i], "") for i in (0, 1, 4, 7, 9, 10)]

    # One distinct image per successive pair. Later pairs favor their later
    # frame, matching the printed chapter's progression through each action.
    selected = []
    seen = set()
    for i in range(0, len(frames), 2):
        pair = frames[i:i + 2]
        if i >= len(frames) // 2:
            pair = reversed(pair)
        for frame in pair:
            if frame["sha256"] not in seen:
                selected.append((frame, ""))
                seen.add(frame["sha256"])
                break
    return selected


def _tile(url, alt, seconds, width, height, note=""):
    label = f"{seconds:.2f} s"
    description = escape(f"{alt}. {seconds:.2f} seconds.")
    if note:
        label += " · " + escape(note)
    url = escape(url)
    return (f'<div class="contact-tile"><a href="{url}"><img src="{url}" alt="{description}" '
            f'width="{width}" height="{height}" loading="lazy" decoding="async"></a>'
            f'<span>{label}</span></div>')


class ContactSheets:
    def __init__(self, animations, site_path, inline, rewrite_asset_path):
        self.media = {record["slug"]: record["media"] for record in animations}
        self.site_path = site_path
        self.inline = inline
        self.rewrite_asset_path = rewrite_asset_path
        self.figure_number = 0

    def _figure(self, content, caption, footnotes, layout=""):
        self.figure_number += 1
        number = self.figure_number
        classes = "contact-figure" + (" " + layout if layout else "")
        return (f'<figure id="figure-{number}" class="{classes}">'
                f'<figcaption><small>Figure {number}</small> {self.inline(caption, footnotes)}'
                f'</figcaption>{content}</figure>')

    def image(self, alt, path, caption=None, footnotes=None):
        if path == BARBER_GIF:
            tile = _tile(self.site_path(SUPPLEMENT_PATH + "barbershop-0.jpg"), alt, 0, 384, 480)
            return self._figure(f'<div class="contact-grid">{tile}</div>',
                                caption or alt, footnotes, "contact-photo")
        url = escape(self.rewrite_asset_path(path))
        description = escape(alt or caption or "Diagram")
        diagram = (f'<a href="{url}"><img src="{url}" alt="{description}" '
                   f'loading="lazy" decoding="async"></a>')
        return self._figure(diagram, caption or alt, footnotes, "contact-static")

    def video(self, alt, poster_path, video_path, caption=None, footnotes=None):
        slug = PurePosixPath(video_path).stem
        media = self.media[slug]
        archive_path = f"/animation-review/{slug}/frames/"
        tiles = []
        if slug == "symmetry-triangle-actions" and media["video_sha256"] == TRIANGLE_MOVIE_SHA256:
            archived = {frame["index"]: frame for frame in media["frames"]}
            for index in TRIANGLE_INDICES:
                path = (archive_path + archived[index]["file"] if index in archived
                        else SUPPLEMENT_PATH + f"triangle-{index}.jpg")
                tiles.append(_tile(self.site_path(path), alt, index / media["fps"],
                                   media["width"], media["height"]))
        else:
            for frame, note in _selected_frames(slug, media["frames"]):
                url = self.site_path(archive_path + frame["file"])
                tiles.append(_tile(url, alt, frame["time_seconds"], media["width"], media["height"], note))
        layout = "contact-wide" if slug in WIDE_STILLS else ""
        return self._figure('<div class="contact-grid">' + "".join(tiles) + '</div>',
                            caption or alt, footnotes, layout)
