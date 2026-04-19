from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_DIR = ROOT / "data" / "chat_summaries"
CONTEXT_DIGEST = ROOT / "workspace" / "context_digest.md"
OUTLINE_PATH = ROOT / "workspace" / "outline.md"

SECTION_NAMES = [
    "Project",
    "Audience",
    "Principles",
    "Structural Decisions",
    "Terminology Preferences",
    "Reusable Phrasing",
    "Open Questions",
    "Evidence Notes",
]

TOPIC_STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "into",
    "your",
    "have",
    "will",
    "about",
    "should",
    "without",
    "only",
    "more",
    "than",
    "when",
    "they",
    "them",
    "their",
    "what",
    "where",
    "while",
    "does",
    "each",
    "keep",
    "much",
    "much",
    "agent",
    "writing",
    "chat",
    "chats",
    "summary",
    "summaries",
}


def parse_summary(path: Path) -> dict[str, list[str] | str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = path.stem
    current_section = None
    data: dict[str, list[str] | str] = {"title": title}

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("# "):
            data["title"] = line[2:].strip()
            continue

        if line.startswith("## "):
            current_section = line[3:].strip()
            if current_section in SECTION_NAMES:
                data.setdefault(current_section, [])
            continue

        if current_section not in SECTION_NAMES:
            continue

        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip()
        else:
            item = stripped

        section_items = data.setdefault(current_section, [])
        if isinstance(section_items, list):
            section_items.append(item)

    return data


def load_summaries() -> list[dict[str, list[str] | str]]:
    files = sorted(SUMMARY_DIR.glob("*.md"))
    return [parse_summary(path) for path in files]


def unique_items(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def gather_section_items(
    summaries: list[dict[str, list[str] | str]],
) -> dict[str, list[str]]:
    collected: dict[str, list[str]] = defaultdict(list)
    for summary in summaries:
        for section in SECTION_NAMES:
            items = summary.get(section, [])
            if isinstance(items, list):
                collected[section].extend(items)
    return {section: unique_items(items) for section, items in collected.items()}


def derive_topics(section_items: dict[str, list[str]]) -> list[str]:
    corpus = []
    for section in ("Principles", "Structural Decisions", "Audience", "Open Questions"):
        corpus.extend(section_items.get(section, []))

    words = []
    for item in corpus:
        words.extend(re.findall(r"[A-Za-z][A-Za-z\\-]{2,}", item.lower()))

    counts = Counter(word for word in words if word not in TOPIC_STOPWORDS)
    topics = [word.replace("-", " ").title() for word, _ in counts.most_common(6)]
    return unique_items(topics)


def build_context_digest(
    summaries: list[dict[str, list[str] | str]], section_items: dict[str, list[str]]
) -> str:
    lines = [
        "# Context Digest",
        "",
        f"Generated from {len(summaries)} summary file(s).",
        "",
        "## Source Summaries",
        "",
    ]

    for summary in summaries:
        lines.append(f"- {summary['title']}")

    for section in SECTION_NAMES:
        items = section_items.get(section, [])
        if not items:
            continue
        lines.extend(["", f"## {section}", ""])
        for item in items:
            lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def build_auto_outline(section_items: dict[str, list[str]]) -> str:
    topics = derive_topics(section_items)
    principles = section_items.get("Principles", [])[:5]
    open_questions = section_items.get("Open Questions", [])[:5]

    lines = []
    if topics:
        lines.append("### Suggested Sections")
        lines.append("")
        for topic in topics:
            lines.append(f"- {topic}")

    if principles:
        lines.extend(["", "### Writing Priorities", ""])
        for principle in principles:
            lines.append(f"- {principle}")

    if open_questions:
        lines.extend(["", "### Questions To Resolve", ""])
        for question in open_questions:
            lines.append(f"- {question}")

    if not lines:
        lines = ["Add summary files in `data/chat_summaries/` to build an outline."]

    return "\n".join(lines).strip()


def update_outline(auto_outline: str) -> None:
    text = OUTLINE_PATH.read_text(encoding="utf-8")
    start_marker = "<!-- AUTO:START -->"
    end_marker = "<!-- AUTO:END -->"

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        flags=re.DOTALL,
    )
    replacement = f"{start_marker}\n{auto_outline}\n{end_marker}"
    updated = pattern.sub(replacement, text)
    OUTLINE_PATH.write_text(updated, encoding="utf-8")


def command_rebuild() -> None:
    summaries = load_summaries()
    section_items = gather_section_items(summaries)
    CONTEXT_DIGEST.write_text(
        build_context_digest(summaries, section_items), encoding="utf-8"
    )
    update_outline(build_auto_outline(section_items))
    print(
        f"Rebuilt context from {len(summaries)} summary file(s) into "
        f"{CONTEXT_DIGEST.name} and {OUTLINE_PATH.name}."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Refresh a local writing-agent workspace from chat summaries."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "rebuild",
        help="Rebuild the context digest and auto-managed outline from summaries.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "rebuild":
        command_rebuild()


if __name__ == "__main__":
    main()
