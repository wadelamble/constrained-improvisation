from __future__ import annotations

import html
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from animation_review import build_review_pages, review_slug


ROOT = Path(__file__).resolve().parents[1]
SITE_SRC = ROOT / "site_src"
OUT_DIR = ROOT / "site"
PATH_MECHANICS_DRAFT = ROOT / "content" / "drafts" / "lm-draft-polished.md"
DIFFERENTIAL_MECHANICS_DRAFT = ROOT / "content" / "drafts" / "Differential-Mechanics-With-Diagrams.md"
WAVE_SYMMETRY_DRAFT = ROOT / "notes" / "worked" / "symmetry-ccr-2.md"
ANIMATION_DIR = ROOT / "content" / "drafts" / "animations"
REEL_DIR = ROOT / "content" / "reels" / "ccr2-series"

TITLE = "Nature's Improvisation on Symmetry"
BASE_PATH = os.environ.get("SITE_BASE_PATH", "").rstrip("/")


def site_path(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{BASE_PATH}{path}" if BASE_PATH else path


@dataclass
class Section:
    title: str
    slug: str
    description: str
    status: str = "Coming soon"
    href: str | None = None
    outline: list[str] = field(default_factory=list)
    disabled: bool = True


@dataclass(frozen=True)
class Article:
    title: str
    slug: str
    draft: Path
    heading_offset: int = 0


ARTICLES = [
    Article("Wave Symmetry", "symmetry", WAVE_SYMMETRY_DRAFT, heading_offset=3),
    Article("The Principle of Least Action", "path-mechanics", PATH_MECHANICS_DRAFT),
    Article("State flow", "differential-mechanics", DIFFERENTIAL_MECHANICS_DRAFT),
]

ARTICLE_BY_SLUG = {article.slug: article for article in ARTICLES}


SECTIONS = [
    Section(
        "Principles",
        "principles",
        "A priori principles and seminal observations.",
        outline=["Invariant structure", "State, law, and observation"],
    ),
    Section(
        "Wave Symmetry",
        "symmetry",
        "Wave symmetry, interference, and the connection to quantum mechanics.",
        status="",
        href="/symmetry/",
        disabled=False,
    ),
    Section(
        "Spacetime",
        "spacetime",
        "The geometry of events and causality.",
        outline=["Galilean structure", "Relativistic structure"],
    ),
    Section(
        "The Principle of Least Action",
        "path-mechanics",
        "Evolution reducing surprise.",
        status="",
        href="/path-mechanics/",
        disabled=False,
    ),
    Section(
        "Fields and Interactions",
        "field-theories",
        "General Relativity and Gauge Fields.",
    ),
    Section(
        "State flow",
        "differential-mechanics",
        "The evolution of ensembles.",
        status="",
        href="/differential-mechanics/",
        outline=["Evolution of ensembles", "Phase-space geometry", "Hamiltonian flows", "Poisson algebra"],
        disabled=False,
    ),
    Section(
        "Zooming into the Stochastic",
        "zooming-into-the-stochastic",
        "From paths to observations.",
        outline=["State and measurement", "Operators", "Commutators", "Fields", "Quantization", "Particle interpretation"],
    ),
]


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def article_markdown(article: Article) -> str:
    markdown = article.draft.read_text(encoding="utf-8")
    if article.heading_offset:
        def adjust_heading(match: re.Match[str]) -> str:
            depth = max(1, len(match.group(1)) - article.heading_offset)
            text = article.title if depth == 1 else match.group(2).strip()
            return f"{'#' * depth} {text}"

        markdown = re.sub(r"^(#{1,6})[ \t]+(.+)$", adjust_heading, markdown, flags=re.MULTILINE)
    # The public chapter title may differ from its working manuscript title.
    markdown = re.sub(r"^#[ \t]+[^\n]+$", lambda _: f"# {article.title}",
                      markdown, count=1, flags=re.MULTILINE)
    return markdown


def article_outline(article: Article) -> list[str]:
    markdown = article_markdown(article)
    return [
        line.removeprefix("## ").strip()
        for line in markdown.splitlines()
        if line.startswith("## ") and not line.startswith("### ")
    ]


def outline_for_section(section: Section) -> list[str]:
    article = ARTICLE_BY_SLUG.get(section.slug)
    if article is not None:
        return article_outline(article)
    return section.outline


def page_shell(title: str, body: str, toc: str = "") -> str:
    nav_links = "\n".join(
        f'          <a href="{site_path("/" + article.slug + "/")}">{html.escape(article.title)}</a>'
        for article in ARTICLES
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | {html.escape(TITLE)}</title>
  <link rel="stylesheet" href="{site_path('/styles.css')}">
  <script>
  window.MathJax = {{
    tex: {{
      inlineMath: [['$', '$']],
      displayMath: [['$$', '$$']],
      processEscapes: true
    }}
  }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <script defer src="{site_path('/main.js')}"></script>
</head>
<body>
  <div class="site-shell">
    <header class="site-header">
      <div class="site-header__inner">
        <a class="site-mark" href="{site_path('/')}">{html.escape(TITLE)}</a>
        <nav class="site-nav" aria-label="Site">
          <a href="{site_path('/')}">Contents</a>
{nav_links}
        </nav>
      </div>
    </header>
    {body}
    {toc}
    <footer class="site-footer">
      Draft manuscript site. Structure, titles, and section order remain provisional.
      <a href="{site_path('/animation-review/')}">Wave Symmetry code and frames</a>
    </footer>
  </div>
  <div class="lightbox" data-lightbox aria-hidden="true">
    <div class="lightbox__inner" data-lightbox-inner>
      <button class="lightbox__close" type="button" data-lightbox-close>Close</button>
    </div>
  </div>
</body>
</html>
"""


def render_home() -> str:
    items = []
    for section in SECTIONS:
        status = f'<span class="status">{html.escape(section.status)}</span>' if section.status else ""
        new_badge = '<span class="new-splatter">NEW</span>' if section.href else ""
        card_class = "section-card" if not section.disabled else "section-card section-card--disabled"
        label = html.escape(section.title)
        title = f'<a href="{site_path(section.href)}">{label}</a>{status}{new_badge}' if section.href else f"<span>{label}</span>{status}"
        outline = ""
        section_outline = outline_for_section(section)
        if section_outline:
            outline_items = "\n".join(f"<li>{html.escape(item)}</li>" for item in section_outline)
            outline = f"<details><summary>Outline</summary><ol>{outline_items}</ol></details>"
        items.append(
            f"""<li class="{card_class}">
  {title}
  <p>{html.escape(section.description)}</p>
  {outline}
</li>"""
        )

    body = f"""<main class="home">
  <h1 class="home-title">{html.escape(TITLE)}</h1>
  <p class="home-intro">A work in progress on the wave description of nature that emerges from physical principles and seminal observations.</p>
  <h2 class="contents-heading">Contents</h2>
  <ol class="section-list">
    {''.join(items)}
  </ol>
</main>"""
    return page_shell("Contents", body)


INLINE_LITERAL = re.compile(r"(?P<ticks>`+)(?P<code>.+?)(?P=ticks)(?!`)|\$[^$\n]+\$")
FOOTNOTE_DEFINITION = re.compile(r"^ {0,3}\[\^([^\]\s]+)\]:[ \t]*(.*)$")


@dataclass
class Footnote:
    markdown: str
    number: int = 0
    identifier: str = ""
    references: list[str] = field(default_factory=list)


class Footnotes:
    """Keep definition groups at their source locations, with page-wide links."""

    def __init__(self, markdown: str):
        self.notes: dict[str, Footnote] = {}
        self.groups: dict[str, list[str]] = {}
        self.ids: set[str] = set()
        self.number = 0
        self.marker = "\x00footnote-"
        while self.marker in markdown:
            self.marker += "-"
        lines = markdown.splitlines()
        output: list[str] = []
        i = 0
        in_fence = False
        while i < len(lines):
            if lines[i].strip().startswith("```"):
                in_fence = not in_fence
            match = None if in_fence else FOOTNOTE_DEFINITION.match(lines[i])
            if match is None:
                output.append(lines[i])
                i += 1
                continue
            labels: list[str] = []
            while match:
                label, first_line = match.groups()
                if label in self.notes:
                    raise ValueError(f"Duplicate footnote definition: {label}")
                body = [first_line]
                i += 1
                while i < len(lines):
                    if lines[i].startswith(("    ", "\t")):
                        body.append(lines[i][1:] if lines[i].startswith("\t") else lines[i][4:])
                        i += 1
                    elif not lines[i].strip():
                        body.append("")
                        i += 1
                    else:
                        break
                self.notes[label] = Footnote("\n".join(body).strip("\n"))
                labels.append(label)
                match = FOOTNOTE_DEFINITION.match(lines[i]) if i < len(lines) else None
            marker = f"{self.marker}{len(self.groups)}\x00"
            self.groups[marker] = labels
            output.extend(["", marker, ""])
        self.markdown = "\n".join(output)

    def unique_id(self, base: str) -> str:
        identifier = base
        suffix = 2
        while identifier in self.ids:
            identifier = f"{base}-{suffix}"
            suffix += 1
        self.ids.add(identifier)
        return identifier

    def numbered(self, label: str) -> Footnote:
        note = self.notes[label]
        if not note.number:
            self.number += 1
            note.number = self.number
            note.identifier = self.unique_id(f"fn-{note.number}")
        return note

    def reference(self, label: str) -> str | None:
        if label not in self.notes:
            return None
        note = self.numbered(label)
        identifier = self.unique_id(f"fnref-{note.number}")
        note.references.append(identifier)
        return (
            f'<sup class="footnote-ref" id="{identifier}">'
            f'<a href="#{note.identifier}" role="doc-noteref" '
            f'aria-label="Footnote {note.number}">{note.number}</a></sup>'
        )

    def insert_groups(self, rendered: str) -> str:
        # Render every body before adding return links, so later references work.
        bodies = {label: _render_markdown(note.markdown, self)[0]
                  for label, note in self.notes.items()}
        for marker, labels in self.groups.items():
            items = []
            for label in labels:
                note = self.numbered(label)
                backlinks = " ".join(
                    f'<a class="footnote-backref" href="#{identifier}" '
                    f'role="doc-backlink" aria-label="Back to reference {index} '
                    f'for footnote {note.number}">↩{index if len(note.references) > 1 else ""}</a>'
                    for index, identifier in enumerate(note.references, 1)
                )
                body = bodies[label]
                if backlinks:
                    if body.endswith("</p>"):
                        body = body[:-4] + " " + backlinks + "</p>"
                    else:
                        body += f'<p class="footnote-backlinks">{backlinks}</p>'
                items.append(f'<li id="{note.identifier}" value="{note.number}">{body}</li>')
            group = ('<section class="footnotes" role="doc-endnotes" aria-label="Footnotes">'
                     f'<ol>{"".join(items)}</ol></section>')
            rendered = rendered.replace(marker, group)
        return rendered


def inline(text: str, footnotes: Footnotes | None = None) -> str:
    parts: list[tuple[str, re.Match[str] | None]] = []
    start = 0
    for match in INLINE_LITERAL.finditer(text):
        parts.extend([(text[start:match.start()], None), (match.group(), match)])
        start = match.end()
    parts.append((text[start:], None))
    out: list[str] = []
    for part, literal in parts:
        if not part:
            continue
        if literal and literal.group("ticks"):
            out.append(f'<code>{html.escape(literal.group("code"))}</code>')
            continue
        if literal:
            out.append(html.escape(part))
            continue
        escaped = html.escape(part)
        references: dict[str, str] = {}
        if footnotes:
            def replace_reference(match: re.Match[str]) -> str:
                # Existing links consume their whole match; never nest an anchor.
                if match.group(1) is None:
                    return match.group()
                reference = footnotes.reference(html.unescape(match.group(1)))
                if reference is None:
                    return match.group()
                marker = f"{footnotes.marker}inline-{len(references)}\x00"
                references[marker] = reference
                return marker

            escaped = re.sub(r"\[[^\]]+\]\([^)]+\)|(?<!\\)\[\^([^\]\s]+)\]",
                             replace_reference, escaped)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
        escaped = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{html.escape(rewrite_asset_path(m.group(2)), quote=True)}">{m.group(1)}</a>',
            escaped,
        )
        for marker, reference in references.items():
            escaped = escaped.replace(marker, reference)
        out.append(escaped)
    return "".join(out)


def local_asset_path(path: str) -> str | None:
    relative = path.removeprefix("../../content/drafts/")
    if relative.startswith(("animations/", "diagrams/")):
        return relative
    return None


def rewrite_asset_path(path: str) -> str:
    relative = local_asset_path(path)
    if relative is not None:
        return site_path(f"/assets/{relative}")
    return path


def copy_asset(path: str) -> None:
    relative = local_asset_path(path)
    if relative is None:
        return
    source = ROOT / "content" / "drafts" / relative
    dest = OUT_DIR / "assets" / relative
    if not source.is_file():
        raise FileNotFoundError(f"Missing manuscript asset: {source}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def figure_for_image(alt: str, path: str, caption: str | None = None, footnotes: Footnotes | None = None) -> str:
    copy_asset(path)
    src = rewrite_asset_path(path)
    safe_alt = html.escape(alt, quote=True)
    caption_text = caption or alt
    figure_class = f"media-figure media-figure--{slugify(Path(path).stem)}"
    return f"""<figure class="{figure_class}">
  <img src="{html.escape(src, quote=True)}" alt="{safe_alt}">
  <figcaption>{inline(caption_text, footnotes)}</figcaption>
  <div class="media-actions">
    <button type="button" data-popout data-kind="image" data-src="{html.escape(src, quote=True)}" data-alt="{safe_alt}">Enlarge</button>
    <a href="{html.escape(src, quote=True)}" target="_blank" rel="noreferrer">Open file</a>
  </div>
</figure>"""


def figure_for_video(alt: str, poster_path: str, video_path: str, caption: str | None = None, footnotes: Footnotes | None = None) -> str:
    copy_asset(poster_path)
    copy_asset(video_path)
    poster = rewrite_asset_path(poster_path)
    video = rewrite_asset_path(video_path)
    safe_alt = html.escape(alt, quote=True)
    caption_text = caption or alt
    slug = review_slug(video_path)
    figure_id = f' id="animation-{slug}"' if slug else ""
    review_link = (
        f'<a href="{site_path("/animation-review/" + slug + "/")}">Code and frames</a>'
        if slug else ""
    )
    return f"""<figure class="media-figure"{figure_id}>
  <video controls preload="metadata" poster="{html.escape(poster, quote=True)}">
    <source src="{html.escape(video, quote=True)}" type="video/mp4">
  </video>
  <figcaption>{inline(caption_text, footnotes)}</figcaption>
  <div class="media-actions">
    <button type="button" data-popout data-kind="video" data-src="{html.escape(video, quote=True)}" data-alt="{safe_alt}">Pop out video</button>
    <a href="{html.escape(video, quote=True)}" target="_blank" rel="noreferrer">Open MP4</a>
    {review_link}
  </div>
</figure>"""


def render_markdown(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    footnotes = Footnotes(markdown)
    if not footnotes.notes:
        return _render_markdown(markdown)
    rendered, toc = _render_markdown(footnotes.markdown, footnotes)
    return footnotes.insert_groups(rendered), toc


def _render_markdown(markdown: str, footnotes: Footnotes | None = None) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    html_blocks: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_ids: dict[str, int] = {}

    def unique_id(text: str) -> str:
        base = slugify(re.sub(r"`([^`]+)`", r"\1", text))
        if footnotes:
            return footnotes.unique_id(base)
        count = used_ids.get(base, 0)
        used_ids[base] = count + 1
        return base if count == 0 else f"{base}-{count + 1}"

    def is_table_row(text: str) -> bool:
        return text.startswith("|") and text.endswith("|") and text.count("|") >= 2

    def is_table_separator(text: str) -> bool:
        if not is_table_row(text):
            return False
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)

    def table_cells(text: str) -> list[str]:
        return [cell.strip() for cell in text.strip("|").split("|")]

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if footnotes and stripped in footnotes.groups:
            html_blocks.append(stripped)
            i += 1
            continue

        if stripped.startswith("```"):
            info = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(code_lines)
            if info == "math":
                html_blocks.append(f'<div class="math-block">$$\n{html.escape(code)}\n$$</div>')
            else:
                html_blocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
            continue

        if stripped == "::: sidebar":
            i += 1
            sidebar_lines = []
            while i < len(lines) and lines[i].strip() != ":::":
                sidebar_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            sidebar_html, _ = _render_markdown("\n".join(sidebar_lines), footnotes)
            html_blocks.append(f'<aside class="manuscript-sidebar">{sidebar_html}</aside>')
            continue

        if stripped.startswith("::: details"):
            summary = stripped.removeprefix("::: details").strip() or "Optional"
            i += 1
            detail_lines = []
            while i < len(lines) and lines[i].strip() != ":::":
                detail_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            detail_html, _ = _render_markdown("\n".join(detail_lines), footnotes)
            html_blocks.append(
                '<details class="manuscript-details">'
                f"<summary>{inline(summary, footnotes)}</summary>"
                f'<div class="manuscript-details__body">{detail_html}</div>'
                "</details>"
            )
            continue

        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            alt, image_path = image_match.groups()
            caption = None
            next_line = ""
            next_index = i + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            if next_index < len(lines):
                next_line = lines[next_index].strip()
            caption_match = re.fullmatch(r"\*(.+)\*", next_line)
            if caption_match:
                caption = caption_match.group(1).strip()
                next_index += 1
                while next_index < len(lines) and not lines[next_index].strip():
                    next_index += 1
                next_line = lines[next_index].strip() if next_index < len(lines) else ""
            mp4_match = re.fullmatch(r"\[Open MP4: ([^\]]+)\]\(([^)]+)\)", next_line)
            if mp4_match:
                _, video_path = mp4_match.groups()
                end_index = next_index + 1
                if caption is None:
                    caption_index = end_index
                    while caption_index < len(lines) and not lines[caption_index].strip():
                        caption_index += 1
                    if caption_index < len(lines):
                        trailing_caption = re.fullmatch(r"\*(.+)\*", lines[caption_index].strip())
                        if trailing_caption:
                            caption = trailing_caption.group(1).strip()
                            end_index = caption_index + 1
                html_blocks.append(figure_for_video(alt, image_path, video_path, caption, footnotes))
                i = end_index
            else:
                html_blocks.append(figure_for_image(alt, image_path, caption, footnotes))
                i = next_index if caption is not None else i + 1
            continue

        open_mp4_match = re.fullmatch(r"\[Open MP4: ([^\]]+)\]\(([^)]+)\)", stripped)
        if open_mp4_match:
            label, video_path = open_mp4_match.groups()
            html_blocks.append(figure_for_video(label, "", video_path, footnotes=footnotes))
            i += 1
            continue

        heading_match = re.fullmatch(r"(#{1,6})\s+(.+)", stripped)
        if heading_match:
            depth = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            hid = unique_id(text)
            if depth >= 2:
                toc.append((depth, text, hid))
            html_blocks.append(f'<h{depth} id="{hid}">{inline(text, footnotes)}</h{depth}>')
            i += 1
            continue

        if (
            is_table_row(stripped)
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1].strip())
        ):
            headers = table_cells(stripped)
            i += 2
            rows = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                rows.append(table_cells(lines[i].strip()))
                i += 1
            header_html = "".join(f"<th>{inline(cell, footnotes)}</th>" for cell in headers)
            body_rows = []
            for row in rows:
                padded = row + [""] * max(0, len(headers) - len(row))
                cells = "".join(f"<td>{inline(cell, footnotes)}</td>" for cell in padded[: len(headers)])
                body_rows.append(f"<tr>{cells}</tr>")
            html_blocks.append(
                f'<div class="table-wrap"><table><thead><tr>{header_html}</tr></thead>'
                f"<tbody>{''.join(body_rows)}</tbody></table></div>"
            )
            continue

        list_match = re.fullmatch(r"\d+\.\s+(.+)", stripped)
        if list_match:
            items = []
            while i < len(lines):
                match = re.fullmatch(r"\d+\.\s+(.+)", lines[i].strip())
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1), footnotes)}</li>")
                i += 1
            html_blocks.append(f"<ol>{''.join(items)}</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if (
                not candidate
                or candidate.startswith("#")
                or candidate.startswith("```")
                or candidate.startswith(":::")
                or re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", candidate)
                or re.fullmatch(r"\[Open MP4: ([^\]]+)\]\(([^)]+)\)", candidate)
                or re.fullmatch(r"\d+\.\s+.+", candidate)
                or (
                    is_table_row(candidate)
                    and i + 1 < len(lines)
                    and is_table_separator(lines[i + 1].strip())
                )
            ):
                break
            paragraph_lines.append(candidate)
            i += 1
        html_blocks.append(f"<p>{inline(' '.join(paragraph_lines), footnotes)}</p>")

    return "\n".join(html_blocks), toc


def render_article(article: Article) -> str:
    markdown = article_markdown(article)
    article_html, toc_items = render_markdown(markdown)
    toc_links = "\n".join(
        f'<a class="depth-{depth}" href="#{hid}">{html.escape(text)}</a>'
        for depth, text, hid in toc_items
        if depth <= 4
    )
    body = f"""<main class="article-layout">
  <article class="article">
    {article_html}
  </article>
  <aside class="page-toc" aria-label="Page contents">
    <strong>On This Page</strong>
    {toc_links}
  </aside>
</main>"""
    return page_shell(article.title, body)


def build() -> None:
    clean_dir(OUT_DIR)
    shutil.copy2(SITE_SRC / "styles.css", OUT_DIR / "styles.css")
    shutil.copy2(SITE_SRC / "main.js", OUT_DIR / "main.js")
    (OUT_DIR / "index.html").write_text(render_home(), encoding="utf-8")
    for article in ARTICLES:
        article_dir = OUT_DIR / article.slug
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "index.html").write_text(render_article(article), encoding="utf-8")
    build_review_pages(OUT_DIR, site_path, page_shell, render_markdown,
                       article_markdown(ARTICLE_BY_SLUG['symmetry']))
    # Stable public MP4 URLs for the unpublished Buffer drafts. Keep the review
    # gallery, manifests, and publishing records out of the public site.
    for video in sorted(REEL_DIR.glob("ccr2-*.mp4")):
        media_dir = OUT_DIR / "media" / "reels" / "waves-to-quanta"
        media_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video, media_dir / video.name)


if __name__ == "__main__":
    build()
