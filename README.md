# A Coffee with CompBio - Self-Hosted Podcast

Self-hosted podcast RSS feed using Internet Archive for audio hosting and Netlify for RSS deployment.

- **Audio Hosting**: [Internet Archive](https://archive.org/details/acoffeewithcompbio)
- **RSS / Web**: [podcast.boston-wib.org](https://podcast.boston-wib.org)
- **Feed**: https://podcast.boston-wib.org/feed.xml

---

## Setup

Install [Pixi](https://pixi.sh) if you don't have it:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.zshrc
```

Then install dependencies:

```bash
pixi install
```

---

## Pixi Commands

| Command | Description |
|---------|-------------|
| `pixi run parse-episode <file>` | Parse a markdown episode file into `episode_metadata.json` |
| `pixi run upload-single <file>` | Upload a single audio file to Internet Archive |
| `pixi run upload` | Upload all audio files to Internet Archive |
| `pixi run generate-rss` | Generate `feed.xml` from metadata |
| `pixi run generate-season2` | Regenerate `season2.html` from metadata |
| `pixi run preview` | Start local preview server at localhost:8000 |
| `pixi run download` | Download episodes from Ausha (migration only) |
| `pixi run ia configure` | Configure Internet Archive credentials |

---

## Adding a New Episode

### 1. Place the audio file

Copy the audio file into the `audio/` directory. Any filename works — it just needs to match exactly what you put in the markdown metadata.

### 2. Create the episode markdown file

```bash
cp episodes_markdown/TEMPLATE.md episodes_markdown/S02E03_your-title.md
```

Fill in all sections:

```markdown
## Metadata

- **Season:** 2
- **Episode:** 3
- **Title:** Your Episode Title
- **Published:** Mon, 30 Mar 2026 12:00:00 +0000
- **Duration:** 20:15
- **Audio File:** Season_2_Episode_3.mp3

## Description

Write your episode description here in markdown.

## Links

- [Resource Name](https://example.com)

## Footer

Thanks to **Amulya Shastry** for editing and management support and **Dina Issakova** for social media support and the cover art!

Follow us on LinkedIn: [Saba Nafees](https://www.linkedin.com/in/saba-nafees/) and [Sharvari Narendra](https://www.linkedin.com/in/sharvarinarendra/)
```

See `episodes_markdown/S02E01_example.md` for a complete reference.

**Date format** must be RFC 2822: `Day, DD Mon YYYY HH:MM:SS +0000`
Examples: `Mon, 27 Jan 2026 12:00:00 +0000`, `Tue, 15 Feb 2026 09:30:00 +0000`

### 3. Parse the markdown into metadata

```bash
pixi run parse-episode episodes_markdown/S02E03_your-title.md
```

This converts the markdown to HTML and prepends the new episode entry to `episode_metadata.json`. It will error if the episode already exists (by season + number).

### 4. Upload audio to Internet Archive

First-time only — configure credentials:
```bash
pixi run ia configure
```

Then upload the new episode:
```bash
pixi run upload-single "audio/Season_2_Episode_3.mp3"
```

This automatically updates `archive_url` in `episode_metadata.json`.

### 5. Generate the RSS feed and season page

```bash
pixi run generate-rss
pixi run generate-season2
```

### 6. Preview locally (optional)

```bash
pixi run preview
```

Open http://localhost:8000/feed.xml in your browser to verify the episode looks correct.

### 7. Deploy

```bash
git add episode_metadata.json feed.xml season2.html
git commit -m "Add S02E03: Your Episode Title"
git push
```

Netlify auto-deploys on push.

---

## Project Structure

```
AcoffeeWCompbio/
├── audio/                          # Audio files (gitignored, hosted on Internet Archive)
├── episodes_markdown/              # Human-friendly episode authoring
│   ├── TEMPLATE.md                 # Copy this to start a new episode
│   ├── S02E01_example.md           # Complete example
│   └── S02E02.md                   # ...
├── episode_metadata.json           # Central data store (all episode metadata)
├── feed.xml                        # Generated RSS feed (committed to git)
├── rss.xslt                        # XSLT stylesheet (RSS → beautiful webpage in browsers)
├── rss-styles.css                  # CSS for the browser RSS view
├── index.html                      # Podcast landing page
├── podcast-artwork-2026.jpg        # Cover art
├── parse_episode_markdown.py       # Converts episode .md → episode_metadata.json entry
├── generate_rss.py                 # Generates feed.xml from episode_metadata.json
├── upload_single_file.py           # Uploads one audio file to Internet Archive
├── upload_to_archive.py            # Uploads all audio files to Internet Archive
├── download_podcast_audio.py       # Migration tool: downloads from Ausha RSS
├── preview-server.py               # Local HTTP server for testing
├── pixi.toml                       # Pixi environment and task config
└── netlify.toml                    # Netlify deployment config
```

---

## RSS Feed Web Rendering

The feed uses XSLT to display as a polished webpage when opened in a browser, while remaining a standard RSS feed for podcast apps.

**In a browser** (`feed.xml`):
- Podcast artwork and description
- All episodes with embedded audio players and download buttons
- Copyable feed URL for easy subscription
- Responsive layout

**In a podcast app**: standard RSS — works with Apple Podcasts, Spotify, Google Podcasts, etc.

Files involved: `feed.xml`, `rss.xslt`, `rss-styles.css` — all three must be deployed.

To customize colors, edit `rss-styles.css` line 14:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## Deployment

The repo is connected to Netlify — pushing to `main` triggers an automatic deploy. Audio files are gitignored and hosted on Internet Archive.

To deploy from scratch:

1. Push to GitHub
2. In Netlify: "New site from Git" → connect repo → build command: *(empty)*, publish directory: `.`
3. Update URLs in `generate_rss.py` (lines ~13–16) with your Netlify URL, then `pixi run generate-rss` and push

---

## Troubleshooting

**Audio not in feed** — verify `local_file` in `episode_metadata.json` matches the actual filename exactly, then re-run `pixi run generate-rss`.

**Internet Archive upload fails** — re-run `pixi run ia configure`, check credentials and storage quota.

**RSS not rendering in browser** — ensure `rss.xslt` and `rss-styles.css` are deployed; check browser console. Some browsers show raw XML — the feed still works in podcast apps.

**Feed not updating in podcast apps** — most apps refresh every 1–24 hours. Validate at https://podba.se/validate/. Apple Podcasts Connect can force a refresh.

**Netlify deploy fails** — confirm `audio/` is in `.gitignore` and all other files are committed.

---

## Resources

- [Pixi documentation](https://pixi.sh)
- [Internet Archive API](https://archive.org/services/docs/api/)
- [Apple Podcasts RSS spec](https://help.apple.com/itc/podcasts_connect/#/itcb54353390)
- [Netlify documentation](https://docs.netlify.com/)
- [Feed validator](https://podba.se/validate/)

---

Podcast content: Copyright Boston-area Women in Bioinformatics
Scripts: MIT License
