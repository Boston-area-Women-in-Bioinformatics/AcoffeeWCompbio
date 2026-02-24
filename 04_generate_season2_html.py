#!/usr/bin/env python3
"""
Generate season2.html from episode_metadata.json.

Reads all season 2 episodes and produces a static HTML archive page
matching the style of season1.html.

Usage:
    python generate_season2_html.py
    # or:
    pixi run generate-season2
"""

import json
import re
from datetime import datetime
from pathlib import Path

METADATA_FILE = Path(__file__).parent / "episode_metadata.json"
OUTPUT_FILE = Path(__file__).parent / "season2.html"


def format_date(rfc2822):
    """Convert 'Mon, 27 Jan 2026 12:00:00 +0000' → 'Jan 27, 2026'."""
    try:
        dt = datetime.strptime(rfc2822.strip(), "%a, %d %b %Y %H:%M:%S %z")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return rfc2822


def html_to_plain_summary(html, max_chars=200):
    """Strip HTML tags and truncate to a short summary."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "…"
    return text


def build_episode_block(ep, is_newest):
    new_badge = '<span class="new-badge">NEW</span>' if is_newest else ""
    date_str = format_date(ep["published"])
    duration = ep["duration"]
    title = ep["title"]
    number = ep["number"]
    archive_url = ep.get("archive_url", "")
    summary = html_to_plain_summary(ep["description"])

    listen_btn = ""
    if archive_url:
        listen_btn = f'\n                    <a href="{archive_url}" class="listen-link">&#127911; Listen</a>'

    return f"""
                <div class="episode">
                    <h3>Episode {number}: {title} {new_badge}</h3>
                    <div class="episode-meta">Published: {date_str} | Duration: {duration}</div>
                    <div class="episode-description">
                        <p>{summary}</p>
                    </div>{listen_btn}
                </div>"""


def generate():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    season2 = [ep for ep in data["episodes"] if ep.get("season") == 2]
    # Sort by episode number ascending for display (newest at top already from JSON ordering)
    season2_sorted = sorted(season2, key=lambda e: e["number"])

    if not season2_sorted:
        print("No season 2 episodes found in episode_metadata.json")
        return

    newest_number = max(ep["number"] for ep in season2_sorted)
    episode_blocks = "".join(
        build_episode_block(ep, ep["number"] == newest_number)
        for ep in reversed(season2_sorted)  # newest first on the page
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Season 2 - A Coffee with CompBio</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .tagline {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .back-link {{
            display: inline-block;
            color: white;
            text-decoration: none;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 5px;
            transition: background 0.2s;
        }}

        .back-link:hover {{
            background: rgba(255,255,255,0.3);
        }}

        .content {{
            padding: 40px;
        }}

        .hosts-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .hosts-info h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .new-badge {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }}

        .episode-list {{
            margin-top: 30px;
        }}

        .episode {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }}

        .episode h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .episode-meta {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}

        .episode-description {{
            color: #555;
            line-height: 1.6;
        }}

        .listen-link {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 0.9em;
            margin-top: 10px;
            transition: transform 0.2s;
        }}

        .listen-link:hover {{
            transform: translateY(-2px);
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="index.html" class="back-link">&larr; Back to Home</a>
            <h1>Season 2 <span class="new-badge">NEW</span></h1>
            <p class="tagline">A Coffee with CompBio</p>
        </div>

        <div class="content">
            <div class="hosts-info">
                <h2>Season 2 Hosts</h2>
                <p><strong>Sharvari Narendra</strong> and <strong>Saba Nafees</strong></p>
                <p>Follow them on LinkedIn:
                    <a href="https://www.linkedin.com/in/sharvarinarendra/" style="color: #667eea;">Sharvari</a> |
                    <a href="https://www.linkedin.com/in/saba-nafees/" style="color: #667eea;">Saba</a>
                </p>
            </div>

            <div class="episode-list">
                <h2 style="color: #667eea; margin-bottom: 20px;">All Episodes</h2>
{episode_blocks}
            </div>
        </div>

        <div class="footer">
            <p>&copy; 2026 A Coffee with CompBio &bull; Hosted independently</p>
        </div>
    </div>
</body>
</html>
"""

    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(season2_sorted)} episode(s):")
    for ep in reversed(season2_sorted):
        print(f"  S02E{ep['number']:02d}: {ep['title']}")


if __name__ == "__main__":
    generate()
