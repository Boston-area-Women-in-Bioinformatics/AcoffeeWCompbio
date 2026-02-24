#!/usr/bin/env python3
"""
Parse an episode markdown file and add it to episode_metadata.json.

Usage:
    python parse_episode_markdown.py episodes_markdown/S02E02.md
"""

import json
import re
import sys
from pathlib import Path

METADATA_FILE = Path(__file__).parent / "episode_metadata.json"


def parse_sections(md_text):
    """Split markdown into named sections (## Heading → content)."""
    sections = {}
    current_section = None
    lines = []

    for line in md_text.splitlines():
        heading = re.match(r"^## (.+)", line)
        if heading:
            if current_section is not None:
                sections[current_section] = "\n".join(lines).strip()
            current_section = heading.group(1).strip()
            lines = []
        elif line.strip() == "---":
            continue
        else:
            if current_section is not None:
                lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(lines).strip()

    return sections


def parse_metadata(metadata_text):
    """Extract key-value pairs from the Metadata section."""
    result = {}
    for line in metadata_text.splitlines():
        m = re.match(r"^-\s+\*\*(.+?):\*\*\s*(.+)", line)
        if m:
            result[m.group(1).strip()] = m.group(2).strip()
    return result


def md_inline_to_html(text):
    """Convert inline markdown (bold, links) to HTML."""
    # [text](url) → <a href="url">text</a>
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # **text** → <b>text</b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text


def md_block_to_html(text):
    """Convert a markdown block (paragraphs, lists) to HTML."""
    html_parts = []
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line → paragraph separator
        if not line.strip():
            if html_parts and html_parts[-1] != "<p><br /></p>":
                html_parts.append("<p><br /></p>")
            i += 1
            continue

        # Bullet list block
        if line.strip().startswith("- "):
            list_items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item = lines[i].strip()[2:]
                list_items.append(f"<li>{md_inline_to_html(item)}</li>")
                i += 1
            html_parts.append("<ul>" + "".join(list_items) + "</ul>")
            continue

        # Regular paragraph line — collect consecutive non-blank, non-list lines
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("- "):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        html_parts.append(f"<p>{md_inline_to_html(para_text)}</p>")

    return "".join(html_parts)


def build_description(description_text, links_text, footer_text):
    """Combine Description, Links, and Footer sections into one HTML string."""
    html = md_block_to_html(description_text)

    # Links section
    if links_text.strip():
        html += "<p><br /></p><p><b>Links:</b></p>"
        list_items = []
        for line in links_text.splitlines():
            line = line.strip()
            if line.startswith("- "):
                item = line[2:]
                list_items.append(f"<li>{md_inline_to_html(item)}</li>")
        if list_items:
            html += "<ul>" + "".join(list_items) + "</ul>"

    # Footer section
    if footer_text.strip():
        html += "<p><br /></p>" + md_block_to_html(footer_text)

    return html


def update_metadata_file(episode):
    """Prepend new episode entry to episodes[] in episode_metadata.json."""
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check for duplicate (same season + episode number)
    for existing in data["episodes"]:
        if existing.get("season") == episode["season"] and existing.get("number") == episode["number"]:
            print(f"WARNING: Season {episode['season']} Episode {episode['number']} already exists in metadata.")
            print("Aborting to avoid duplicate. Remove the existing entry first if you want to replace it.")
            sys.exit(1)

    data["episodes"].insert(0, episode)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Added S{episode['season']:02d}E{episode['number']:02d}: {episode['title']}")
    print(f"episode_metadata.json updated ({len(data['episodes'])} episodes total)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_episode_markdown.py <path/to/episode.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: File not found: {md_path}")
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")
    sections = parse_sections(md_text)

    required = {"Metadata", "Description", "Links", "Footer"}
    missing = required - sections.keys()
    if missing:
        print(f"Error: Missing sections in markdown: {', '.join(missing)}")
        sys.exit(1)

    meta = parse_metadata(sections["Metadata"])

    required_fields = {"Season", "Episode", "Title", "Published", "Duration", "Audio File"}
    missing_fields = required_fields - meta.keys()
    if missing_fields:
        print(f"Error: Missing metadata fields: {', '.join(missing_fields)}")
        sys.exit(1)

    description_html = build_description(
        sections["Description"],
        sections["Links"],
        sections["Footer"],
    )

    audio_filename = meta["Audio File"]
    episode = {
        "season": int(meta["Season"]),
        "number": int(meta["Episode"]),
        "title": meta["Title"],
        "description": description_html,
        "published": meta["Published"],
        "duration": meta["Duration"],
        "original_audio_url": "",
        "local_file": f"audio/{audio_filename}",
        "archive_url": "",
    }

    print(f"\nParsed episode:")
    print(f"  Season:    {episode['season']}")
    print(f"  Episode:   {episode['number']}")
    print(f"  Title:     {episode['title']}")
    print(f"  Published: {episode['published']}")
    print(f"  Duration:  {episode['duration']}")
    print(f"  Audio:     {episode['local_file']}")
    print()

    update_metadata_file(episode)


if __name__ == "__main__":
    main()
