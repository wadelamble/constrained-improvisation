"""Build a public, source-and-decoded-frame review packet for Wave Symmetry.

Uses only the explicitly catalogued scripts and the chapter supplied by the site
builder. Frame extraction is a separate operation; this module never renders an
animation or treats a source mapping as proof of an earlier render's provenance.
"""
from __future__ import annotations

import hashlib
import html
import json
import math
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "site_src" / "animation-sources.json"
FRAME_ROOT = ROOT / "content" / "review" / "animation-frames"
CHAPTER_PATH = "notes/worked/symmetry-ccr-2.md"
PUBLIC_SITE_URL = "https://wadelamble.github.io/constrained-improvisation"
LIMITS = (
    "These are sparse samples decoded from the current MP4, not newly rendered "
    "illustrations. They can support checks of the sampled states and labels, but "
    "cannot establish continuous motion, timing, transitions, or the absence of "
    "problems between samples. Use the full MP4 when judging those properties."
)
PROVENANCE = (
    "Source SHA-256 values identify the exact downloadable bytes in this packet. "
    "The source mapping and recorded checks explain the likely generation pipeline; "
    "they do not prove that these exact source bytes produced the movie. "
    "A GitHub link pinned to a commit is provided only when the delivered source "
    "bytes exactly match that path at the build's Git HEAD."
)
CHECKS_NOTE = (
    "These are existing author-produced generator reports, copied without changes. "
    "Their checks were not rerun for this packet and are not independent certification. "
    "A report may describe an earlier generation run; inspect its contents before "
    "applying its claims to the current movie."
)
VIDEO_LINK = re.compile(r"^\[Open MP4: [^\]]+\]\(([^)]+\.mp4)\)\s*$")
IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _public(path: str) -> str:
    return PUBLIC_SITE_URL + "/" + path.lstrip("/")


def _json(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _relative(value: str) -> str:
    """Accept portable, relative file paths, never parent traversal or URLs."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"Invalid review path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in (".", "..") for part in value.split("/")):
        raise ValueError(f"Invalid review path: {value!r}")
    return path.as_posix()


def _inside(base: Path, relative: str) -> Path:
    path = base / _relative(relative)
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f"Review path escapes its directory: {relative}")
    return path


def _catalog() -> dict:
    value = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not value:
        raise ValueError("The animation source catalog must be a nonempty object")
    for name, entry in value.items():
        if not re.fullmatch(r"[a-z0-9-]+\.mp4", name):
            raise ValueError(f"Invalid catalog movie basename: {name}")
        if not isinstance(entry, dict) or not entry.get("sources"):
            raise ValueError(f"Missing source mapping for {name}")
        for source in entry["sources"]:
            path = _relative(source)
            if not path.startswith("scripts/"):
                raise ValueError(f"Only explicitly catalogued scripts may be published: {path}")
        for field in ("generation_note", "evidence"):
            if not isinstance(entry.get(field), str):
                raise ValueError(f"Missing {field} for {name}")
    return value


def review_slug(video_path: str) -> str | None:
    """Return a review slug only for an MP4 present in the public catalog."""
    name = PurePosixPath(urlsplit(video_path).path).name
    return name[:-4] if name in _catalog() else None


def _blocks(markdown: str) -> list[dict]:
    lines = markdown.splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        start = i
        fence = re.match(r"^\s*(`{3,}|~{3,})", lines[i])
        i += 1
        if fence:
            while i < len(lines):
                end = re.match(r"^\s*" + re.escape(fence[1]) + r"\s*$", lines[i])
                i += 1
                if end:
                    break
        elif not re.match(r"^\s*#{1,6}\s", lines[start]):
            while i < len(lines) and lines[i].strip():
                if re.match(r"^\s*(?:#{1,6}\s|`{3,}|~{3,})", lines[i]):
                    break
                i += 1
        text = "".join(lines[start:i]).rstrip("\r\n")
        result.append({"start_line": start + 1, "end_line": i, "markdown": text})
    return result


def _chapter_entries(markdown: str) -> list[dict]:
    blocks = _blocks(markdown)
    entries = []
    heading = "Wave Symmetry"
    for index, block in enumerate(blocks):
        text = block["markdown"].strip()
        title = re.match(r"^#{1,6}\s+([^\n]+)", text)
        if title:
            heading = title[1].strip()
        match = VIDEO_LINK.fullmatch(text)
        if not match:
            continue
        video_path = match[1].removeprefix("../../")
        if not video_path.startswith("content/drafts/animations/"):
            raise ValueError(f"Unexpected chapter video path: {match[1]}")
        video_path = _relative(video_path)
        name = PurePosixPath(video_path).name
        start, end = index, index
        caption = None
        alt = name
        # Match the manuscript renderer's image/caption/video grouping.
        if start and re.fullmatch(r"\*(.+)\*", blocks[start - 1]["markdown"].strip()):
            caption = blocks[start - 1]["markdown"].strip()[1:-1]
            start -= 1
        image_match = IMAGE.fullmatch(blocks[start - 1]["markdown"].strip()) if start else None
        if image_match:
            alt = image_match[1]
            start -= 1
        if caption is None and end + 1 < len(blocks):
            trailing = re.fullmatch(r"\*(.+)\*", blocks[end + 1]["markdown"].strip())
            if trailing:
                caption = trailing[1]
                end += 1

        def nearby(at: int, step: int) -> list[dict]:
            selected = []
            while 0 <= at < len(blocks) and len(selected) < 2:
                candidate = blocks[at]
                raw = candidate["markdown"].strip()
                if IMAGE.fullmatch(raw) or VIDEO_LINK.fullmatch(raw):
                    break
                if re.match(r"^#{1,6}\s", raw):
                    break
                # Do not borrow the caption of an adjacent figure.
                if re.fullmatch(r"\*(.+)\*", raw):
                    break
                selected.append(candidate.copy())
                at += step
            return selected[::-1] if step < 0 else selected

        entries.append({
            "video": video_path, "basename": name, "slug": name[:-4],
            "chapter_section": heading, "caption": caption,
            "image_description": alt, "video_link_line": block["start_line"],
            "context_before": nearby(start - 1, -1),
            "context_after": nearby(end + 1, 1),
        })
    return entries


def _git() -> tuple[str | None, str | None]:
    def read(*args: str) -> str:
        result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True)
        return result.stdout.decode("utf-8").strip()
    try:
        head = read("rev-parse", "HEAD")
        origin = read("remote", "get-url", "origin")
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        return None, None
    if not re.fullmatch(r"[0-9a-f]{40,64}", head):
        return None, None
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:)([\w.-]+/[\w.-]+?)(?:\.git)?/?", origin)
    return head, "https://github.com/" + match[1] if match else None


def _source_record(path: str, data: bytes, head: str | None, github: str | None) -> dict:
    matches = False
    if head:
        try:
            result = subprocess.run(["git", "-C", str(ROOT), "show", f"{head}:{path}"],
                                    capture_output=True, check=False)
            matches = result.returncode == 0 and result.stdout == data
        except OSError:
            pass
    return {
        "path": path, "file": f"sources/{path}.txt", "sha256": _sha(data),
        "bytes": len(data), "matches_git_head": matches,
        "github_url": f"{github}/blob/{head}/{quote(path, safe='/')}" if matches and github else None,
    }


def _existing_checks(entries: list[dict]) -> dict[str, list[tuple[dict, bytes]]]:
    try:
        result = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--",
                                 "content/drafts/animations"], capture_output=True, check=True)
        tracked = set(result.stdout.decode("utf-8").split("\0"))
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        tracked = set()
    reports = {}
    for entry in entries:
        slug = entry["slug"]
        reports[slug] = []
        for suffix in ("-validation.json", "-encoded-validation.json"):
            path = f"content/drafts/animations/{slug}{suffix}"
            if path not in tracked or not (ROOT / path).is_file():
                continue
            data = _inside(ROOT, path).read_bytes()
            json.loads(data)  # Reject unreadable reports rather than publish broken files.
            record = {"path": path, "file": f"{slug}/checks/{slug}{suffix}",
                      "sha256": _sha(data), "bytes": len(data)}
            reports[slug].append((record, data))
    return reports


def _chapter_assets(markdown: str) -> list[tuple[dict, bytes]]:
    assets = []
    seen = set()
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", markdown):
        original = match[1]
        path = _relative(original.removeprefix("../../"))
        if not path.startswith(("content/drafts/animations/", "content/drafts/diagrams/")):
            raise ValueError(f"Unexpected chapter image path: {original}")
        if PurePosixPath(path).suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
            raise ValueError(f"Unexpected chapter image format: {path}")
        if path in seen:
            continue
        seen.add(path)
        data = _inside(ROOT, path).read_bytes()
        record = {"path": path, "original_reference": original,
                  "file": f"chapter-assets/{path}", "sha256": _sha(data), "bytes": len(data),
                  "public_url": _public("/assets/" + path.removeprefix("content/drafts/"))}
        assets.append((record, data))
    return assets


def _verify_manifest(entry: dict) -> tuple[dict, bytes, dict[str, bytes]]:
    folder = FRAME_ROOT / entry["slug"]
    raw = (folder / "manifest.json").read_bytes()
    manifest = json.loads(raw)
    if manifest.get("schema_version") != 1 or manifest.get("video") != entry["video"]:
        raise ValueError(f"Frame manifest does not identify the chapter movie: {entry['basename']}")
    actual_hash = _sha(_inside(ROOT, entry["video"]).read_bytes())
    if actual_hash != manifest.get("video_sha256"):
        raise ValueError(f"MP4 has changed since frame extraction: {entry['basename']}")
    for key in ("duration_seconds", "fps", "frame_count", "width", "height"):
        value = manifest.get(key)
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"Invalid {key} in {entry['basename']} frame manifest")
    if not manifest.get("method") or not manifest.get("frames") or not manifest.get("contact_sheet"):
        raise ValueError(f"Incomplete frame manifest: {entry['basename']}")
    assets = {}
    previous_index = -1
    for frame in manifest["frames"]:
        index, time = frame.get("index"), frame.get("time_seconds")
        if not isinstance(index, int) or not previous_index < index < manifest["frame_count"]:
            raise ValueError(f"Invalid or unordered sampled frame: {entry['basename']}")
        if not isinstance(time, (int, float)) or not math.isfinite(time) or time < 0:
            raise ValueError(f"Invalid sampled timestamp: {entry['basename']}")
        if abs(time - index / manifest["fps"]) > 0.002:
            raise ValueError(f"Timestamp/index mismatch: {entry['basename']}")
        previous_index = index
    for asset in [*manifest["frames"], manifest["contact_sheet"]]:
        relative = _relative(asset["file"])
        if PurePosixPath(relative).suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            raise ValueError(f"Unexpected extracted image format: {relative}")
        if relative in assets:
            raise ValueError(f"Duplicate extracted image path: {relative}")
        data = _inside(folder, relative).read_bytes()
        if _sha(data) != asset.get("sha256"):
            raise ValueError(f"Extracted image hash mismatch: {entry['slug']}/{relative}")
        assets[relative] = data
    return manifest, raw, assets


def _timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    minutes, remainder = divmod(milliseconds, 60000)
    whole, fraction = divmod(remainder, 1000)
    return f"{minutes:02d}:{whole:02d}.{fraction:03d}"


def _context_markdown(entry: dict) -> str:
    caption = entry["caption"]
    parts = [f"# {entry['basename']}", f"Chapter section: {entry['chapter_section']}",
             "Caption (verbatim):\n\n" + (caption if caption is not None else "No separate caption in the chapter."),
             "Image description (verbatim):\n\n" + entry["image_description"]]
    for label, field in (("Before the animation", "context_before"), ("After the animation", "context_after")):
        parts.append("## " + label)
        for block in entry[field]:
            parts.extend([f"Chapter lines {block['start_line']}–{block['end_line']}:", block["markdown"]])
    return "\n\n".join(parts) + "\n"


def build_review_pages(out_dir, site_path, page_shell, render_markdown, chapter_markdown):
    """Write the review site and portable ZIP; reject stale or incomplete inputs.

    Call after the chapter assets have been copied. ``site_path`` and
    ``page_shell`` are the existing site helpers; ``render_markdown`` may return
    either HTML or the site's ``(HTML, toc)`` pair. Returns the generated index.
    """
    catalog = _catalog()
    entries = _chapter_entries(chapter_markdown)
    names = [entry["basename"] for entry in entries]
    if len(names) != len(set(names)) or set(names) != set(catalog):
        raise ValueError("Animation catalog must cover each chapter MP4 exactly once; "
                         f"missing={sorted(set(names) - set(catalog))}, "
                         f"extra={sorted(set(catalog) - set(names))}")
    head, github = _git()
    # Validate every input before writing any review output.
    verified = {entry["slug"]: _verify_manifest(entry) for entry in entries}
    existing_checks = _existing_checks(entries)
    chapter_assets = _chapter_assets(chapter_markdown)
    sources = {}
    source_data = {}
    for entry in catalog.values():
        for path in entry["sources"]:
            if path not in sources:
                data = _inside(ROOT, path).read_bytes()
                sources[path] = _source_record(path, data, head, github)
                source_data[path] = data
    target = Path(out_dir) / "animation-review"
    written = set()

    def write(relative: str, data: bytes | str):
        path = _inside(target, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
        written.add(relative)

    def url(relative: str) -> str:
        return html.escape(site_path("/animation-review/" + quote(relative, safe="/")), quote=True)

    def md(text: str) -> str:
        result = render_markdown(text)
        return result[0] if isinstance(result, tuple) else result

    def link(relative: str, label: str) -> str:
        return f'<a href="{url(relative)}">{html.escape(label)}</a>'

    chapter_bytes = chapter_markdown.encode("utf-8")
    write("chapter.md", chapter_bytes)
    portable_chapter = chapter_markdown
    media_map = ["# Chapter media map", "The verbatim chapter.md retains its repository-relative media "
                 "references. chapter-portable.md changes only media link targets: images point to "
                 "the included chapter-assets files and MP4s point to the public site."]
    for asset, data in chapter_assets:
        write(asset["file"], data)
        portable_chapter = portable_chapter.replace(f"({asset['original_reference']})",
                                                     f"({asset['file']})")
        media_map.append(f"- `{asset['original_reference']}`: [included image]({asset['file']}); "
                         f"[public image]({asset['public_url']}); SHA-256 `{asset['sha256']}`")
    for entry in entries:
        public_video = _public("/assets/animations/" + entry["basename"])
        portable_chapter = portable_chapter.replace(f"(../../{entry['video']})", f"({public_video})")
        media_map.append(f"- `../../{entry['video']}`: [full MP4 online]({public_video}); "
                         "not included in the ZIP.")
    write("chapter-portable.md", portable_chapter)
    write("chapter-media.md", "\n\n".join(media_map) + "\n")
    write("animation-sources.json", _json(catalog))
    for path, record in sources.items():
        write(record["file"], source_data[path])
    records, cards = [], []
    packet = ["# Wave Symmetry: chapter and animation review packet",
              "Review the complete Wave Symmetry section, including its prose, equations, "
              "static figures, and animations, using the supplied source and sampled movie frames. "
              "This packet supplies evidence and context; it contains no review findings or grades.",
              "The intended reader is an interested non-specialist with high-school mathematics. "
              "Assess how the explanation builds from its stated starting points; identify "
              "additional prerequisites when they occur.",
              LIMITS, PROVENANCE,
              "The ZIP contains frames, contact sheets, manifests, source text, all chapter images, "
              "and chapter/context markdown. MP4s are excluded. "
              f"[Read the complete chapter and play its movies online]({_public('/symmetry/')}).",
              "[Read the chapter with portable media links](chapter-portable.md) · "
              "[Verbatim chapter markdown](chapter.md) · [Media map](chapter-media.md) · "
              "[Machine-readable index](index.json) · "
              "[Source mapping](animation-sources.json)",
              "chapter.md retains the repository's original relative media references. "
              "chapter-portable.md preserves its prose and equations and adjusts only media link "
              "targets to included images and absolute public MP4 URLs.",
              "Consider physical and mathematical correctness; whether the argument supports its "
              "claims and makes imported assumptions explicit; teaching clarity; and whether the "
              "figures and animations faithfully show the stated mathematics. Assess the whole "
              "section's sequence as well as individual visuals.",
              "For each observation, identify the animation and timestamp or source lines, describe "
              "the issue and its effect on the chapter's claim, and distinguish direct observation "
              "from inference. Leave unexamined properties unassessed."]
    for number, entry in enumerate(entries, 1):
        slug = entry["slug"]
        manifest, manifest_bytes, assets = verified[slug]
        for filename, data in assets.items():
            write(f"{slug}/frames/{filename}", data)
        write(f"{slug}/manifest.json", manifest_bytes)
        context_md = _context_markdown(entry)
        write(f"{slug}/context.md", context_md)
        source_records = [sources[path] for path in catalog[entry["basename"]]["sources"]]
        check_records = []
        for check_record, data in existing_checks[slug]:
            write(check_record["file"], data)
            check_records.append(check_record)
        record = {**entry, **catalog[entry["basename"]], "source_files": source_records,
                  "generator_checks": check_records,
                  "manifest": f"{slug}/manifest.json", "manifest_sha256": _sha(manifest_bytes),
                  "frame_directory": f"{slug}/frames/", "media": manifest,
                  "chapter_url": site_path(f"/symmetry/#animation-{slug}"),
                  "public_chapter_url": _public(f"/symmetry/#animation-{slug}"),
                  "public_video_url": _public("/assets/animations/" + entry["basename"]),
                  "review_url": site_path(f"/animation-review/{slug}/")}
        records.append(record)
        caption = entry["caption"] or entry["image_description"]
        chapter_url = html.escape(record["chapter_url"], quote=True)
        video_url = html.escape(site_path("/assets/animations/" + entry["basename"]), quote=True)
        sheet_file = f"{slug}/frames/{manifest['contact_sheet']['file']}"
        source_items = []
        for source in source_records:
            pinned = (f' · <a href="{html.escape(source["github_url"], quote=True)}">GitHub at {head[:12]}</a>'
                      if source["github_url"] else " · No byte-identical pinned GitHub link available.")
            source_items.append(f'<li>{link(source["file"], source["path"])}{pinned}'
                                f'<br><code class="review-hash">SHA-256 {source["sha256"]}</code></li>')
        context_parts = []
        for label, field in (("Before the animation", "context_before"), ("After the animation", "context_after")):
            pieces = "".join(f'<p class="review-location">Chapter lines {b["start_line"]}–{b["end_line"]}</p>'
                             + md(b["markdown"]) for b in entry[field])
            context_parts.append(f'<section class="review-context"><h3>{label}</h3>{pieces}</section>')
        frames_html = []
        for frame in manifest["frames"]:
            filename = f"{slug}/frames/{frame['file']}"
            label = f"{_timestamp(frame['time_seconds'])} · frame {frame['index']}"
            frames_html.append(f'<figure class="review-frame"><a href="{url(filename)}">'
                               f'<img src="{url(filename)}" loading="lazy" '
                               f'width="{manifest["width"]}" height="{manifest["height"]}" '
                               f'alt="Decoded frame from {html.escape(entry["basename"])} at {label}"></a>'
                               f'<figcaption>{label} · {link(filename, "Full-size frame")}</figcaption></figure>')
        note, evidence = catalog[entry["basename"]]["generation_note"], catalog[entry["basename"]]["evidence"]
        checks_html = ""
        if check_records:
            checks_links = "".join(f'<li>{link(c["file"], PurePosixPath(c["path"]).name)}'
                                   f'<br><code class="review-hash">SHA-256 {c["sha256"]}</code></li>'
                                   for c in check_records)
            checks_html = (f'<details class="manuscript-details review-checks"><summary>'
                           f'Existing generator checks ({len(check_records)} reports)</summary>'
                           f'<p>{html.escape(CHECKS_NOTE)}</p><ul>{checks_links}</ul></details>')
        body = f'''<main class="article-layout review-layout"><article class="article animation-review">
<p class="review-links">{link('', 'All animations')} · <a href="{chapter_url}">In the chapter</a> · <a href="{video_url}">Open full MP4</a></p>
<h1>Animation {number}</h1>
<div class="review-intro">{md(caption)}</div>
<p class="review-links"><a href="#decoded-contact-sheet">Frames</a><a href="#generation-source">Code</a><a href="#chapter-context">Chapter context</a></p>
<p><code>{html.escape(entry['basename'])}</code></p>
<p>{html.escape(LIMITS)}</p>
<p class="review-facts">{manifest['width']} × {manifest['height']} · {manifest['fps']:g} fps · {manifest['duration_seconds']:g} s · {manifest['frame_count']} frames · {len(manifest['frames'])} samples</p>
<p><code class="review-hash">MP4 SHA-256 {manifest['video_sha256']}</code></p>
<p>{link(f'{slug}/manifest.json', 'Frame manifest')} · {link(f'{slug}/context.md', 'Context markdown')} · {link('symmetry-review.zip', 'Download complete review packet')}</p>
<h2 id="chapter-context">Chapter context</h2><p>Section: {html.escape(entry['chapter_section'])}. Excerpts are verbatim; line numbers refer to {link('chapter.md', 'the included chapter markdown')}.</p>
<h3>Caption</h3>{md(entry['caption']) if entry['caption'] is not None else '<p>No separate caption in the chapter.</p>'}
<h3>Image description</h3>{md(entry['image_description'])}
{''.join(context_parts)}
<h2 id="generation-source">Generation source</h2><p>{html.escape(note)}</p>
<h3>Mapping evidence and limits</h3><p>{html.escape(evidence)}</p><p>{html.escape(PROVENANCE)}</p>
<ul class="review-source-list">{''.join(source_items)}</ul>
{checks_html}
<h2 id="decoded-contact-sheet">Decoded contact sheet</h2><p>Extraction method: {html.escape(str(manifest['method']))}. Frame indices are zero-based.</p>
<figure class="review-contact-sheet"><a href="{url(sheet_file)}"><img src="{url(sheet_file)}" loading="lazy" alt="Timestamped decoded frames from {html.escape(entry['basename'])}"></a><figcaption>{link(sheet_file, 'Open contact sheet at full size')}</figcaption></figure>
<h2>Full-size sampled frames</h2><div class="review-frames">{''.join(frames_html)}</div>
</article></main>'''
        write(f"{slug}/index.html", page_shell("Animation review: " + entry["basename"], body))
        thumbnail = manifest['frames'][len(manifest['frames']) // 2]
        thumbnail_file = f"{slug}/frames/{thumbnail['file']}"
        cards.append(f'<li class="review-card"><h2>{link(slug + "/", f"Animation {number}")}</h2>'
                     f'{md(caption)}<a href="{url(slug + "/")}"><img src="{url(thumbnail_file)}" loading="lazy" '
                     f'alt="Sample at {_timestamp(thumbnail["time_seconds"])} from {html.escape(entry["basename"])}"></a>'
                     f'<p>{manifest["duration_seconds"]:g} s · {len(manifest["frames"])} decoded samples · '
                     f'{len(source_records)} source file{"s" if len(source_records) != 1 else ""}</p></li>')
        packet.extend([f"## {number}. {entry['basename']}",
                       f"Chapter section: {entry['chapter_section']}",
                       f"[In the public chapter]({record['public_chapter_url']}) · "
                       f"[Play or download the full MP4]({record['public_video_url']})",
                       "Caption (verbatim): " + (entry["caption"] or "No separate caption in the chapter."),
                       f"[Verbatim surrounding context]({slug}/context.md) · [Frame manifest]({slug}/manifest.json)",
                       f"Video: `{entry['video']}`; SHA-256 `{manifest['video_sha256']}`.",
                       f"{manifest['width']} × {manifest['height']}; {manifest['fps']:g} fps; "
                       f"{manifest['duration_seconds']:g} s; {manifest['frame_count']} frames. "
                       "Extraction: " + str(manifest["method"]),
                       "Generation: " + note, "Mapping evidence and limits: " + evidence,
                       f"[Decoded contact sheet]({sheet_file})", "Source files:"])
        for source in source_records:
            pinned_md = f"; [GitHub pinned source]({source['github_url']})" if source["github_url"] else ""
            packet.append(f"- [{source['path']}]({source['file']}): SHA-256 `{source['sha256']}`{pinned_md}")
        if check_records:
            packet.extend(["Existing generator checks:", CHECKS_NOTE])
            for check in check_records:
                packet.append(f"- [{PurePosixPath(check['path']).name}]({check['file']}): "
                              f"SHA-256 `{check['sha256']}`")
        packet.append("Sampled frames (zero-based indices):")
        for frame in manifest["frames"]:
            packet.append(f"- [{_timestamp(frame['time_seconds'])}, frame {frame['index']}]"
                          f"({slug}/frames/{frame['file']})")
    index = {"schema_version": 1, "scope": "Wave Symmetry / symmetry-ccr-2",
             "chapter": "chapter.md", "chapter_source": CHAPTER_PATH,
             "portable_chapter": "chapter-portable.md", "chapter_media_map": "chapter-media.md",
             "chapter_assets": [asset for asset, _ in chapter_assets],
             "public_chapter_url": _public("/symmetry/"),
             "chapter_sha256": _sha(chapter_bytes), "git_head": head,
             "frame_limitations": LIMITS, "source_provenance_limitations": PROVENANCE,
             "generator_check_limitations": CHECKS_NOTE,
             "animations": records}
    write("index.json", _json(index))
    write("review.md", "\n\n".join(packet) + "\n")
    index_body = f'''<main class="article-layout review-layout"><article class="article animation-review">
<p><a href="{html.escape(site_path('/symmetry/'), quote=True)}">Wave Symmetry</a></p><h1>Wave Symmetry review</h1>
<p class="review-intro">Review the complete Wave Symmetry section and its {len(entries)} animations. The packet includes the chapter, static images, exact surrounding context, generation source, and sampled frames decoded from the current movies. No review findings or grades are supplied.</p>
<p>Consider physical and mathematical correctness, support for the argument and its assumptions, teaching clarity, and the fidelity of the visuals to the stated mathematics.</p>
<details class="manuscript-details"><summary>What this evidence can establish</summary><p>{html.escape(LIMITS)}</p><p>{html.escape(PROVENANCE)}</p></details>
<p class="review-links">{link('symmetry-review.zip', 'Download review packet (ZIP, no MP4s)')} {link('review.md', 'Reviewer guide')} {link('index.json', 'Machine-readable index')} {link('chapter-portable.md', 'Full chapter markdown')}</p>
<ol class="review-grid">{''.join(cards)}</ol></article></main>'''
    write("index.html", page_shell("Animation review", index_body))
    with zipfile.ZipFile(target / "symmetry-review.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        # Only files created by this build are eligible. Never sweep the repo,
        # output directory, earlier packets, or unrelated private material.
        for relative in sorted(written):
            if not relative.endswith(".html"):
                archive.write(_inside(target, relative), relative)
    return index
