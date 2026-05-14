from __future__ import annotations

import html
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_SRC = ROOT / "site_src"
OUT_DIR = ROOT / "site"
DRAFT = ROOT / "content" / "drafts" / "Differential-Mechanics-With-Diagrams.md"
ANIMATION_DIR = ROOT / "content" / "drafts" / "animations"

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
    status: str = "draft"
    href: str | None = None
    outline: list[str] = field(default_factory=list)


SECTIONS = [
    Section(
        "Principles",
        "principles",
        "Starting assumptions and the order of explanation.",
        outline=["Invariant structure", "State, law, and observation"],
    ),
    Section(
        "Symmetry",
        "symmetry",
        "How transformations organize physical law.",
        outline=["Transformation groups", "Conserved quantities"],
    ),
    Section(
        "Spacetime",
        "spacetime",
        "The arena in which motion and causal structure are stated.",
        outline=["Galilean structure", "Relativistic structure"],
    ),
    Section(
        "Curvature",
        "curvature",
        "Geometry when flat structure is no longer enough.",
        outline=["Parallel transport", "Curved manifolds"],
    ),
    Section(
        "Action Optimization",
        "action-extremal-paths",
        "The global formulation of mechanics through stationary action.",
        outline=["Action", "Euler-Lagrange equations", "Boundary terms"],
    ),
    Section(
        "Differential Mechanics",
        "differential-mechanics",
        "Hamiltonian mechanics, ensembles, phase space, and Poisson structure.",
        status="",
        href="/differential-mechanics/",
        outline=["Evolution of ensembles", "Phase-space geometry", "Hamiltonian flows", "Poisson algebra"],
    ),
    Section(
        "Unitarity",
        "unitarity",
        "Information-preserving evolution in quantum theory.",
        outline=["Norm preservation", "Time evolution"],
    ),
    Section(
        "Quantum Mechanics",
        "quantum-mechanics",
        "The change from classical states to quantum states.",
        outline=["State and measurement", "Operators", "Commutators"],
    ),
    Section(
        "Gravitation",
        "free-fall",
        "Motion under gravity as a statement about geometry.",
        outline=["Equivalence principle", "Geodesic motion"],
    ),
    Section(
        "Gauge Coupling",
        "connection-coupling",
        "How fields enter through local comparison rules.",
        outline=["Connections", "Gauge structure"],
    ),
    Section(
        "Quantum Field Theory",
        "quantum-field-theory",
        "Fields, particles, and quantization.",
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


def page_shell(title: str, body: str, toc: str = "") -> str:
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
          <a href="{site_path('/differential-mechanics/')}">Differential Mechanics</a>
        </nav>
      </div>
    </header>
    {body}
    {toc}
    <footer class="site-footer">
      Draft manuscript site. Structure, titles, and section order remain provisional.
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
        card_class = "section-card" if section.href else "section-card section-card--disabled"
        label = html.escape(section.title)
        title = f'<a href="{site_path(section.href)}">{label}</a>{status}{new_badge}' if section.href else f"<span>{label}</span>{status}"
        outline = ""
        if section.outline:
            outline_items = "\n".join(f"<li>{html.escape(item)}</li>" for item in section.outline)
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
  <p class="home-intro">A work in progress on the principles that constrain physical possibility and the wave-like picture that emerges.</p>
  <p class="home-note">For reasons, the site is beginning in the middle and will work its way out.</p>
  <h2 class="contents-heading">Contents</h2>
  <ol class="section-list">
    {''.join(items)}
  </ol>
</main>"""
    return page_shell("Contents", body)


def inline(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        escaped = html.escape(part)
        escaped = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{html.escape(rewrite_asset_path(m.group(2)), quote=True)}">{m.group(1)}</a>',
            escaped,
        )
        out.append(escaped)
    return "".join(out)


def rewrite_asset_path(path: str) -> str:
    if path.startswith("animations/"):
        return site_path(f"/assets/{path}")
    return path


def copy_asset(path: str) -> None:
    if not path.startswith("animations/"):
        return
    source = ROOT / "content" / "drafts" / path
    dest = OUT_DIR / "assets" / path
    if source.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)


def figure_for_image(alt: str, path: str, caption: str | None = None) -> str:
    copy_asset(path)
    src = rewrite_asset_path(path)
    safe_alt = html.escape(alt, quote=True)
    caption_text = caption or alt
    return f"""<figure class="media-figure">
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
    return f"""<figure class="media-figure">
  <video controls preload="metadata" poster="{html.escape(poster, quote=True)}">
    <source src="{html.escape(video, quote=True)}" type="video/mp4">
  </video>
  <figcaption>{inline(caption_text)}</figcaption>
  <div class="media-actions">
    <button type="button" data-popout data-kind="video" data-src="{html.escape(video, quote=True)}" data-alt="{safe_alt}">Pop out video</button>
    <a href="{html.escape(video, quote=True)}" target="_blank" rel="noreferrer">Open MP4</a>
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
                html_blocks.append(figure_for_video(alt, image_path, video_path, caption))
                i = next_index + 1
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


def render_article() -> str:
    markdown = DRAFT.read_text(encoding="utf-8")
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
    return page_shell("Differential Mechanics", body)


def build() -> None:
    clean_dir(OUT_DIR)
    shutil.copy2(SITE_SRC / "styles.css", OUT_DIR / "styles.css")
    shutil.copy2(SITE_SRC / "main.js", OUT_DIR / "main.js")
    (OUT_DIR / "index.html").write_text(render_home(), encoding="utf-8")
    article_dir = OUT_DIR / "differential-mechanics"
    article_dir.mkdir(parents=True, exist_ok=True)
    (article_dir / "index.html").write_text(render_article(), encoding="utf-8")


if __name__ == "__main__":
    build()
