"""Check the built Wave Symmetry code-and-frames review package (stdlib only).

This checks delivery, links and recorded hashes. It does not assess physics,
reproduce an animation, or establish that sparse frames represent all motion.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "notes" / "worked" / "symmetry-ccr-2.md"
CATALOG = ROOT / "site_src" / "animation-sources.json"
EXTERNAL_SCHEMES = {"https", "http", "mailto", "tel", "data"}
PUBLIC_SITE = "https://wadelamble.github.io/constrained-improvisation"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass
class Link:
    tag: str
    attribute: str
    url: str
    line: int
    text: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return " ".join("".join(self.text).split())


@dataclass
class Figure:
    identifier: str
    sources: list[str] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: Counter[str] = Counter()
        self.links: list[Link] = []
        self.figures: list[Figure] = []
        self._figures: list[Figure] = []
        self._anchors: list[Link] = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids[values["id"]] += 1
        if tag == "a" and values.get("name") and not values.get("id"):
            self.ids[values["name"]] += 1
        if tag == "figure":
            figure = Figure(values.get("id", ""))
            self.figures.append(figure)
            self._figures.append(figure)
        for attribute in ("href", "src", "poster", "data-src"):
            if attribute not in values:
                continue
            link = Link(tag, attribute, values[attribute] or "", self.getpos()[0])
            self.links.append(link)
            if tag == "a" and attribute == "href":
                self._anchors.append(link)
                if self._figures:
                    self._figures[-1].links.append(link)
            if tag in {"source", "video"} and attribute == "src" and self._figures:
                self._figures[-1].sources.append(link.url)

    def handle_endtag(self, tag):
        if tag == "a" and self._anchors:
            self._anchors.pop()
        if tag == "figure" and self._figures:
            self._figures.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, text):
        for link in self._anchors:
            link.text.append(text)


class Checker:
    def __init__(self, site: Path, base_path: str):
        self.site = site.resolve()
        self.base = "/" + base_path.strip("/") if base_path.strip("/") else ""
        self.errors: list[str] = []
        self.pages: dict[Path, Page] = {}
        self.hashes: dict[Path, str] = {}
        self.local_links = 0
        self.checked_hashes = 0

    def fail(self, message: str):
        self.errors.append(message)

    def relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.site).as_posix()
        except ValueError:
            return str(path)

    def read_json(self, path: Path):
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, ValueError) as exc:
            self.fail(f"Cannot read JSON {self.relative(path)}: {exc}")
            return None

    def page(self, path: Path) -> Page | None:
        path = path.resolve()
        if path not in self.pages:
            try:
                self.pages[path] = Page(path)
            except (OSError, UnicodeError) as exc:
                self.fail(f"Cannot read HTML {self.relative(path)}: {exc}")
                return None
        return self.pages[path]

    def resolve(self, page: Path, url: str, context: str = "") -> tuple[Path, str] | None:
        """Resolve a rendered URL while enforcing the supplied deployment prefix."""
        try:
            parsed = urlsplit(url)
        except ValueError as exc:
            self.fail(f"{context}: invalid URL {url!r}: {exc}")
            return None
        if parsed.scheme in EXTERNAL_SCHEMES or (not parsed.scheme and parsed.netloc):
            return None
        if parsed.scheme:
            self.fail(f"{context}: unexpected URL scheme in {url!r}")
            return None
        path = unquote(parsed.path)
        if "\\" in path:
            self.fail(f"{context}: URL uses backslashes: {url!r}")
            return None
        if path.startswith("/"):
            if self.base and path != self.base and not path.startswith(self.base + "/"):
                self.fail(f"{context}: local URL {url!r} omits deployment prefix {self.base!r}")
                return None
            target = self.site / path[len(self.base):].lstrip("/")
        elif path:
            target = page.parent / path
        else:
            target = page
        target = target.resolve()
        if not target.is_relative_to(self.site):
            self.fail(f"{context}: local URL escapes the built site: {url!r}")
            return None
        if target.is_dir():
            target = target / "index.html"
        return target, unquote(parsed.fragment)

    def check_links(self, page: Page):
        for identifier, count in page.ids.items():
            if count > 1:
                self.fail(f"{self.relative(page.path)}: duplicate fragment id {identifier!r} ({count} occurrences)")
        for link in page.links:
            context = f"{self.relative(page.path)}:{link.line} {link.attribute}"
            resolved = self.resolve(page.path, link.url, context)
            if resolved is None:
                continue
            self.local_links += 1
            target, fragment = resolved
            if not target.is_file():
                self.fail(f"{context}: {link.url!r} resolves to missing {self.relative(target)}")
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                destination = self.page(target)
                if destination and fragment not in destination.ids:
                    self.fail(f"{context}: {link.url!r} has missing fragment #{fragment}")
            elif fragment and not (
                target.suffix.lower() in {".mp4", ".webm", ".mp3", ".wav"}
                and re.fullmatch(r"t=(?:npt:)?[\d:.,]+", fragment)
            ):
                self.fail(f"{context}: cannot verify fragment #{fragment} in non-HTML {self.relative(target)}")

    def check_hash(self, path: Path, expected: str, context: str):
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            self.fail(f"{context}: missing or invalid SHA-256")
            return
        if not path.is_file():
            self.fail(f"{context}: missing file {self.relative(path)}")
            return
        try:
            key = path.resolve()
            if key not in self.hashes:
                self.hashes[key] = sha256(path)
            actual = self.hashes[key]
        except OSError as exc:
            self.fail(f"{context}: cannot hash {self.relative(path)}: {exc}")
            return
        self.checked_hashes += 1
        if actual != expected:
            self.fail(f"{context}: SHA-256 mismatch for {self.relative(path)}; expected {expected}, found {actual}")

    def chapter_names(self) -> list[str]:
        text = CHAPTER.read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^\s)]+\.mp4)\)", text)
        names = list(dict.fromkeys(PurePosixPath(link).name for link in links))
        if len(names) != 14:
            self.fail(f"{CHAPTER.relative_to(ROOT)}: expected 14 linked MP4s, found {len(names)}; update coverage expectation if chapter intentionally changed")
        return names

    def check_chapter(self, names: list[str]):
        chapter = self.page(self.site / "symmetry" / "index.html")
        if chapter is None:
            return
        for name in names:
            stem = PurePosixPath(name).stem
            matches = [figure for figure in chapter.figures if any(
                PurePosixPath(unquote(urlsplit(source).path)).name == name
                for source in figure.sources)]
            if len(matches) != 1:
                self.fail(f"symmetry/index.html: expected one video figure for {name}, found {len(matches)}")
                continue
            figure = matches[0]
            expected_id = f"animation-{stem}"
            if figure.identifier != expected_id:
                self.fail(f"symmetry/index.html: {name} figure id must be {expected_id!r}, found {figure.identifier!r}")
            review_links = [link for link in figure.links if link.label.casefold() == "code and frames"]
            if len(review_links) != 1:
                self.fail(f"symmetry/index.html: {name} needs one 'Code and frames' link, found {len(review_links)}")
                continue
            target = self.resolve(chapter.path, review_links[0].url, f"{name} review link")
            expected_page = self.site / "animation-review" / stem / "index.html"
            if target is None or target[0] != expected_page:
                self.fail(f"symmetry/index.html: {name} review link must target animation-review/{stem}/")
            if not expected_page.is_file():
                self.fail(f"{name}: missing review page {self.relative(expected_page)}")

    def packet_path(self, value, context: str) -> Path | None:
        if not isinstance(value, str) or not value or "\\" in value or ":" in value:
            self.fail(f"{context}: invalid relative packet path {value!r}")
            return None
        relative = PurePosixPath(value)
        if relative.is_absolute() or any(part in {"", ".", ".."} for part in value.split("/")):
            self.fail(f"{context}: unsafe relative packet path {value!r}")
            return None
        target = (self.site / "animation-review" / value).resolve()
        if not target.is_relative_to(self.site / "animation-review"):
            self.fail(f"{context}: path escapes animation-review: {value!r}")
            return None
        return target

    def check_record_file(self, record: dict, context: str, expected_path: str,
                          expected_file: str, packet_files: set[str]):
        """Compare a published source/check record with both delivered and original bytes."""
        if record.get("path") != expected_path or record.get("file") != expected_file:
            self.fail(f"{context}: expected path={expected_path!r}, file={expected_file!r}; "
                      f"found path={record.get('path')!r}, file={record.get('file')!r}")
            return
        copied = self.packet_path(expected_file, context)
        if copied is None:
            return
        packet_files.add(expected_file)
        self.check_hash(copied, record.get("sha256"), context + " copied file")
        self.check_hash(ROOT / expected_path, record.get("sha256"), context + " repository file")
        if copied.is_file() and copied.stat().st_size != record.get("bytes"):
            self.fail(f"{context}: byte count differs from index for {expected_file}")

    def check_animation_record(self, record: dict, catalog: dict, packet_files: set[str]):
        name = record["basename"]
        slug = PurePosixPath(name).stem
        video = f"content/drafts/animations/{name}"
        if record.get("slug") != slug or record.get("video") != video:
            self.fail(f"{name}: index slug/video does not identify its original movie")
        manifest_file = f"{slug}/manifest.json"
        frame_directory = f"{slug}/frames/"
        if record.get("manifest") != manifest_file or record.get("frame_directory") != frame_directory:
            self.fail(f"{name}: index manifest/frame_directory must be {manifest_file!r} and {frame_directory!r}")
        manifest_path = self.site / "animation-review" / manifest_file
        packet_files.update({manifest_file, f"{slug}/context.md"})
        self.check_hash(manifest_path, record.get("manifest_sha256"), f"{name} manifest")
        self.check_hash(ROOT / "content/review/animation-frames" / slug / "manifest.json",
                        record.get("manifest_sha256"), f"{name} original extraction manifest")
        manifest = self.read_json(manifest_path)
        if not isinstance(manifest, dict):
            self.fail(f"{name}: frame manifest must be a JSON object")
            return
        if manifest.get("schema_version") != 1 or manifest.get("video") != video:
            self.fail(f"{name}: frame manifest has incorrect schema_version/video")
        if record.get("media") != manifest:
            self.fail(f"{name}: index media does not equal the delivered frame manifest")
        self.check_hash(ROOT / video, manifest.get("video_sha256"), f"{name} original MP4")
        self.check_hash(self.site / "assets/animations" / name, manifest.get("video_sha256"), f"{name} copied MP4")
        for key in ("duration_seconds", "fps", "frame_count", "width", "height"):
            value = manifest.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value <= 0:
                self.fail(f"{name}: manifest {key} must be a finite positive number")
        frames = manifest.get("frames")
        sheet = manifest.get("contact_sheet")
        if not isinstance(frames, list) or len(frames) != 12 or not all(isinstance(frame, dict) for frame in frames):
            self.fail(f"{name}: expected 12 frame records in manifest")
            return
        if not isinstance(sheet, dict):
            self.fail(f"{name}: contact_sheet record missing from manifest")
            return
        count, fps = manifest.get("frame_count"), manifest.get("fps")
        if isinstance(count, int) and count > 0:
            expected_indices = sorted({round(i * (count - 1) / 11) for i in range(12)})
            if [frame.get("index") for frame in frames] != expected_indices:
                self.fail(f"{name}: sampled indices do not match 12 evenly spaced first-through-last decoded frames")
        seen_files = set()
        for asset in [*frames, sheet]:
            filename = asset.get("file")
            if not isinstance(filename, str) or not re.fullmatch(r"(?:frame-\d{2}|contact-sheet)\.(?:jpg|jpeg|png|webp)", filename):
                self.fail(f"{name}: unexpected extracted image filename {filename!r}")
                continue
            if filename in seen_files:
                self.fail(f"{name}: duplicate extracted image filename {filename}")
            seen_files.add(filename)
            relative = frame_directory + filename
            packet_files.add(relative)
            self.check_hash(self.site / "animation-review" / relative, asset.get("sha256"), f"{name} copied image")
            self.check_hash(ROOT / "content/review/animation-frames" / slug / filename,
                            asset.get("sha256"), f"{name} original extracted image")
            if "index" in asset:
                index, seconds = asset.get("index"), asset.get("time_seconds")
                if (not isinstance(index, int) or not isinstance(seconds, (int, float))
                        or not math.isfinite(seconds) or seconds < 0):
                    self.fail(f"{name}: invalid index/timestamp in {filename}")
                elif isinstance(fps, (int, float)) and fps > 0 and abs(seconds - index / fps) > 0.002:
                    self.fail(f"{name}: timestamp/index mismatch in {filename}: index={index}, seconds={seconds}, fps={fps}")
        mapping = catalog.get(name, {})
        expected_sources = mapping.get("sources", [])
        records = record.get("source_files")
        if record.get("sources") != expected_sources:
            self.fail(f"{name}: source mapping differs from site_src/animation-sources.json")
        if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
            self.fail(f"{name}: source_files must contain source records")
        elif [item.get("path") for item in records] != expected_sources:
            self.fail(f"{name}: source_files paths/order do not match the approved source catalog")
        else:
            for item in records:
                source = item["path"]
                if not isinstance(source, str) or not source.startswith("scripts/") or ".." in PurePosixPath(source).parts:
                    self.fail(f"{name}: source is outside approved scripts directory: {source!r}")
                    continue
                self.check_record_file(item, f"{name} source {source}", source, f"sources/{source}.txt", packet_files)
        checks = record.get("generator_checks", [])
        if not isinstance(checks, list) or not all(isinstance(item, dict) for item in checks):
            self.fail(f"{name}: generator_checks must be a list of report records")
        else:
            seen_checks = set()
            for item in checks:
                path = item.get("path", "")
                allowed = {f"content/drafts/animations/{slug}-validation.json",
                           f"content/drafts/animations/{slug}-encoded-validation.json"}
                if path not in allowed or path in seen_checks:
                    self.fail(f"{name}: unexpected or duplicate generator check path {path!r}")
                    continue
                seen_checks.add(path)
                self.check_record_file(item, f"{name} existing check", path,
                                       f"{slug}/checks/{PurePosixPath(path).name}", packet_files)
        expected_urls = {
            "chapter_url": (self.site / "symmetry/index.html", f"animation-{slug}"),
            "review_url": (self.site / "animation-review" / slug / "index.html", ""),
        }
        for key, expected in expected_urls.items():
            url = record.get(key)
            if not isinstance(url, str) or self.resolve(manifest_path, url, f"{name} index {key}") != expected:
                self.fail(f"{name}: index {key} does not point to the expected local page/anchor")

    def check_zip(self, packet_files: set[str]):
        folder = self.site / "animation-review"
        archive_path = folder / "symmetry-review.zip"
        try:
            with zipfile.ZipFile(archive_path) as archive:
                entries = [info.filename for info in archive.infolist()]
                for name, count in Counter(entries).items():
                    if count > 1:
                        self.fail(f"symmetry-review.zip: duplicate entry {name!r}")
                actual = set(entries)
                for name in sorted(actual - packet_files):
                    kind = "MP4s are excluded" if name.lower().endswith(".mp4") else "not in explicit chapter/frame/source/report allowlist"
                    self.fail(f"symmetry-review.zip: unexpected entry {name!r} ({kind})")
                for name in sorted(packet_files - actual):
                    self.fail(f"symmetry-review.zip: missing required entry {name!r}")
                for name in sorted(actual & packet_files):
                    path = self.packet_path(name, "symmetry-review.zip")
                    if path is None or not path.is_file():
                        self.fail(f"symmetry-review.zip: entry {name!r} has no delivered file")
                        continue
                    data = archive.read(name)
                    if hashlib.sha256(data).hexdigest() != sha256(path):
                        self.fail(f"symmetry-review.zip: entry {name!r} differs from delivered file")
                    self.checked_hashes += 1
        except (OSError, zipfile.BadZipFile, RuntimeError, KeyError) as exc:
            self.fail(f"Cannot check animation-review/symmetry-review.zip: {exc}")

    def check_portable_chapter(self, index: dict, chapter_text: str,
                               records: list[dict], packet_files: set[str]):
        folder = self.site / "animation-review"
        for key, expected in (("portable_chapter", "chapter-portable.md"),
                              ("chapter_media_map", "chapter-media.md")):
            if index.get(key) != expected:
                self.fail(f"animation-review/index.json: {key} must name {expected}")
            packet_files.add(expected)
        if index.get("public_chapter_url") != PUBLIC_SITE + "/symmetry/":
            self.fail("animation-review/index.json: public_chapter_url does not identify the published chapter")
        image_references = list(dict.fromkeys(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", chapter_text)))
        assets = index.get("chapter_assets")
        if not isinstance(assets, list) or not all(isinstance(asset, dict) for asset in assets):
            self.fail("animation-review/index.json: chapter_assets must be a list of image records")
            return
        if [asset.get("original_reference") for asset in assets] != image_references:
            self.fail("animation-review/index.json: chapter_assets do not cover the chapter's static images in order")
        portable = chapter_text
        for asset in assets:
            original = asset.get("original_reference")
            if not isinstance(original, str) or original not in image_references or not original.startswith("../../content/drafts/"):
                self.fail(f"chapter asset: unexpected original reference {original!r}")
                continue
            path = original.removeprefix("../../")
            if (not path.startswith(("content/drafts/animations/", "content/drafts/diagrams/"))
                    or ".." in PurePosixPath(path).parts
                    or PurePosixPath(path).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}):
                self.fail(f"chapter asset: path is outside chapter image directories/formats: {path!r}")
                continue
            filename = "chapter-assets/" + path
            self.check_record_file(asset, f"chapter image {path}", path, filename, packet_files)
            expected_public = PUBLIC_SITE + "/assets/" + path.removeprefix("content/drafts/")
            if asset.get("public_url") != expected_public:
                self.fail(f"chapter image {path}: incorrect public_url")
            portable = portable.replace(f"({original})", f"({filename})")
        for record in records:
            name = record.get("basename")
            if not isinstance(name, str):
                continue
            public_video = PUBLIC_SITE + "/assets/animations/" + name
            public_chapter = PUBLIC_SITE + "/symmetry/#animation-" + PurePosixPath(name).stem
            if record.get("public_video_url") != public_video or record.get("public_chapter_url") != public_chapter:
                self.fail(f"{name}: incorrect absolute public movie/chapter URL in index")
            portable = portable.replace(f"(../../content/drafts/animations/{name})", f"({public_video})")
        try:
            actual = (folder / "chapter-portable.md").read_text(encoding="utf-8")
            if actual != portable:
                self.fail("animation-review/chapter-portable.md differs from chapter.md beyond the declared image/MP4 link rewrites")
        except (OSError, UnicodeError) as exc:
            self.fail(f"Cannot read animation-review/chapter-portable.md: {exc}")

    def check_packet(self, names: list[str]):
        folder = self.site / "animation-review"
        index = self.read_json(folder / "index.json")
        catalog = self.read_json(CATALOG)
        if not isinstance(index, dict) or not isinstance(catalog, dict):
            self.fail("Review index and approved source catalog must be JSON objects")
            return
        if index.get("schema_version") != 1:
            self.fail("animation-review/index.json: expected schema_version 1")
        if set(catalog) != set(names):
            self.fail("site_src/animation-sources.json: catalog coverage differs from the 14 chapter MP4s")
        copied_catalog = self.read_json(folder / "animation-sources.json")
        if copied_catalog != catalog:
            self.fail("animation-review/animation-sources.json differs from the approved source catalog")
        packet_files = {"index.json", "chapter.md", "review.md", "animation-sources.json"}
        if index.get("chapter") != "chapter.md" or index.get("chapter_source") != CHAPTER.relative_to(ROOT).as_posix():
            self.fail("animation-review/index.json: chapter/chapter_source identifies the wrong manuscript")
        self.check_hash(folder / "chapter.md", index.get("chapter_sha256"), "copied chapter")
        # The existing site promotes source headings by three levels and uses
        # the article title for level one. Body prose/equations stay verbatim.
        chapter_text = CHAPTER.read_text(encoding="utf-8")
        def promote_heading(match):
            depth = max(1, len(match[1]) - 3)
            title = "Wave Symmetry" if depth == 1 else match[2].strip()
            return "#" * depth + " " + title
        chapter_text = re.sub(r"^(#{1,6})[ \t]+(.+)$", promote_heading, chapter_text, flags=re.MULTILINE)
        chapter_digest = hashlib.sha256(chapter_text.encode("utf-8")).hexdigest()
        if chapter_digest != index.get("chapter_sha256"):
            self.fail("animation-review/chapter.md: chapter hash differs from current manuscript after the site's heading normalization")
        records = index.get("animations")
        if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
            self.fail("animation-review/index.json: animations must be a list of animation records")
            return
        record_names = [record.get("basename") for record in records]
        if record_names != names:
            self.fail(f"animation-review/index.json: MP4 coverage/order differs from chapter; expected {names!r}, found {record_names!r}")
        for record in records:
            if record.get("basename") not in names:
                self.fail(f"animation-review/index.json: unexpected animation {record.get('basename')!r}")
                continue
            self.check_animation_record(record, catalog, packet_files)
        self.check_portable_chapter(index, chapter_text, records, packet_files)
        self.check_zip(packet_files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "site", help="Built site directory")
    parser.add_argument("--base-path", default="", help="Deployment URL prefix, e.g. /constrained-improvisation")
    args = parser.parse_args()
    checker = Checker(args.site, args.base_path)
    names = checker.chapter_names()
    checker.check_chapter(names)
    checker.check_packet(names)
    paths = [checker.site / "symmetry" / "index.html"]
    paths += sorted((checker.site / "animation-review").rglob("*.html"))
    for path in paths:
        page = checker.page(path)
        if page:
            checker.check_links(page)
    if checker.errors:
        for error in checker.errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Animation review delivery failed: {len(checker.errors)} issue(s).", file=sys.stderr)
        return 1
    print(f"Animation review delivery passed: {len(names)} videos, {len(paths)} HTML pages, "
          f"{checker.local_links} local links, {checker.checked_hashes} hash comparisons. "
          "This is a packaging check, not a physics or continuous-motion verdict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
