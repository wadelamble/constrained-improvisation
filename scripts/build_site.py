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

TITLE = "Nature's Improvisation on Form"
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
    Article("Differential Mechanics", "differential-mechanics", DIFFERENTIAL_MECHANICS_DRAFT),
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
        "Physical motion as geometric simplicity.",
        status="",
        href="/path-mechanics/",
        disabled=False,
    ),
    Section(
        "Field Theories",
        "field-theories",
        "General Relativity and Gauge Fields.",
    ),
    Section(
        "Differential Mechanics",
        "differential-mechanics",
        "Mechanics as state flow.",
        status="",
        href="/differential-mechanics/",
        outline=["Evolution of ensembles", "Phase-space geometry", "Hamiltonian flows", "Poisson algebra"],
        disabled=False,
    ),
    Section(
        "Unitarity",
        "unitarity",
        "Preserving the identity of distributions over time.",
        outline=["Norm preservation", "Time evolution"],
    ),
    Section(
        "Quantum Mechanics",
        "quantum-mechanics",
        "From objects to patterns.",
        outline=["State and measurement", "Operators", "Commutators"],
    ),
    Section(
        "Quantum Field Theory",
        "quantum-field-theory",
        "Giving statistical patterns causal structure.",
        outline=["Fields", "Quantization", "Particle interpretation"],
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


def inline(text: str) -> str:
    parts = re.split(r"(`[^`]+`|\$[^$\n]+\$)", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        if part.startswith("$") and part.endswith("$"):
            out.append(html.escape(part))
            continue
        escaped = html.escape(part)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
        escaped = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{html.escape(rewrite_asset_path(m.group(2)), quote=True)}">{m.group(1)}</a>',
            escaped,
        )
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


def figure_for_image(alt: str, path: str, caption: str | None = None) -> str:
    copy_asset(path)
    src = rewrite_asset_path(path)
    safe_alt = html.escape(alt, quote=True)
    caption_text = caption or alt
    figure_class = f"media-figure media-figure--{slugify(Path(path).stem)}"
    return f"""<figure class="{figure_class}">
  <img src="{html.escape(src, quote=True)}" alt="{safe_alt}">
  <figcaption>{inline(caption_text)}</figcaption>
  <div class="media-actions">
    <button type="button" data-popout data-kind="image" data-src="{html.escape(src, quote=True)}" data-alt="{safe_alt}">Enlarge</button>
    <a href="{html.escape(src, quote=True)}" target="_blank" rel="noreferrer">Open file</a>
  </div>
</figure>"""


def figure_for_video(alt: str, poster_path: str, video_path: str, caption: str | None = None) -> str:
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
  <figcaption>{inline(caption_text)}</figcaption>
  <div class="media-actions">
    <button type="button" data-popout data-kind="video" data-src="{html.escape(video, quote=True)}" data-alt="{safe_alt}">Pop out video</button>
    <a href="{html.escape(video, quote=True)}" target="_blank" rel="noreferrer">Open MP4</a>
    {review_link}
  </div>
</figure>"""


def render_markdown(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    html_blocks: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_ids: dict[str, int] = {}

    def unique_id(text: str) -> str:
        base = slugify(re.sub(r"`([^`]+)`", r"\1", text))
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
            sidebar_html, _ = render_markdown("\n".join(sidebar_lines))
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
            detail_html, _ = render_markdown("\n".join(detail_lines))
            html_blocks.append(
                '<details class="manuscript-details">'
                f"<summary>{inline(summary)}</summary>"
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
                html_blocks.append(figure_for_video(alt, image_path, video_path, caption))
                i = end_index
            else:
                html_blocks.append(figure_for_image(alt, image_path, caption))
                i = next_index if caption is not None else i + 1
            continue

        open_mp4_match = re.fullmatch(r"\[Open MP4: ([^\]]+)\]\(([^)]+)\)", stripped)
        if open_mp4_match:
            label, video_path = open_mp4_match.groups()
            html_blocks.append(figure_for_video(label, "", video_path))
            i += 1
            continue

        heading_match = re.fullmatch(r"(#{1,6})\s+(.+)", stripped)
        if heading_match:
            depth = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            hid = unique_id(text)
            if depth >= 2:
                toc.append((depth, text, hid))
            html_blocks.append(f'<h{depth} id="{hid}">{inline(text)}</h{depth}>')
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
            header_html = "".join(f"<th>{inline(cell)}</th>" for cell in headers)
            body_rows = []
            for row in rows:
                padded = row + [""] * max(0, len(headers) - len(row))
                cells = "".join(f"<td>{inline(cell)}</td>" for cell in padded[: len(headers)])
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
                items.append(f"<li>{inline(match.group(1))}</li>")
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
        html_blocks.append(f"<p>{inline(' '.join(paragraph_lines))}</p>")

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
