# Adding New Episodes

This guide explains how to upload a new episode to a new season and update the archive and feed.xml.

## Overview

The workflow for adding a new episode involves:
1. Preparing the audio file
2. Creating a markdown file with episode info (for AI agent processing)
3. Adding episode metadata to `episode_metadata.json`
4. Uploading to Internet Archive
5. Regenerating the RSS feed
6. Deploying to Netlify

---

## Step 1: Prepare the Audio File

### File Naming Convention

Name your audio file following this pattern:
```
episode_NN_[Episode Title].mp3
```

Where:
- `NN` = Episode number with zero-padding (01, 02, 03, etc.)
- Episode title can include special characters (they'll be preserved)

**Examples:**
```
episode_01_Season 2 Premiere - What's New in CompBio.mp3
episode_02_Deep Dive into Single-Cell Analysis.mp3
```

### Place the File

Copy the MP3 file to the `audio/` directory:
```bash
cp /path/to/your/episode.mp3 audio/episode_01_Your Title Here.mp3
```

---

## Step 2: Create Episode Markdown File

Create a markdown file in `episodes_markdown/` with your episode details. This makes it easy for AI agents to process and add to the metadata.

### Using the Template

1. Copy the template:
```bash
cp episodes_markdown/TEMPLATE.md episodes_markdown/S02E01_your-episode-title.md
```

2. Fill in the metadata section:
```markdown
## Metadata

- **Season:** 2
- **Episode:** 1
- **Title:** Your Episode Title Here
- **Published:** Mon, 27 Jan 2026 12:00:00 +0000
- **Duration:** 25:30
- **Audio File:** episode_01_Your Episode Title Here.mp3
```

3. Write your description in markdown (it will be converted to HTML)

4. Add any relevant links

See `episodes_markdown/S02E01_example.md` for a complete example.

### AI Agent Processing

Once you have the markdown file ready, you can ask an AI agent:

> "Add the episode from episodes_markdown/S02E01_your-episode-title.md to episode_metadata.json"

The agent will:
- Parse the markdown file
- Convert the description to HTML
- Add the standard footer
- Insert the episode at the beginning of the `episodes` array

---

## Step 3: Update Episode Metadata (Manual Alternative)

Edit `episode_metadata.json` and add a new episode entry at the **beginning** of the `episodes` array (newest episodes first).

### Episode Entry Template

```json
{
  "season": 2,
  "number": 1,
  "title": "Your Episode Title",
  "description": "<p>Your episode description in HTML format.</p><p>You can use <b>bold</b>, <em>italics</em>, <a href=\"https://example.com\">links</a>, and lists.</p>",
  "published": "Mon, 27 Jan 2026 12:00:00 +0000",
  "duration": "25:30",
  "original_audio_url": "",
  "local_file": "audio/episode_01_Your Episode Title.mp3",
  "archive_url": ""
}
```

### Field Reference

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `season` | Yes | Season number | `2` |
| `number` | Yes | Episode number within the season | `1` |
| `title` | Yes | Episode title (no HTML) | `"Season 2 Premiere"` |
| `description` | Yes | HTML-formatted description | `"<p>Episode summary...</p>"` |
| `published` | Yes | RFC 2822 date format | `"Mon, 27 Jan 2026 12:00:00 +0000"` |
| `duration` | Yes | Episode length in MM:SS format | `"25:30"` |
| `original_audio_url` | No | Source URL if migrating from another platform | `""` |
| `local_file` | Yes | Relative path to audio file | `"audio/episode_01_Title.mp3"` |
| `archive_url` | No | Leave empty - auto-populated after upload | `""` |

### Date Format

The `published` field must use RFC 2822 format:
```
Day, DD Mon YYYY HH:MM:SS +0000
```

**Examples:**
- `Mon, 27 Jan 2026 12:00:00 +0000`
- `Tue, 15 Feb 2026 09:30:00 +0000`

**Day abbreviations:** Mon, Tue, Wed, Thu, Fri, Sat, Sun

**Month abbreviations:** Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec

### Description Formatting

Use HTML tags in descriptions:
- `<p>` - Paragraphs
- `<br />` - Line breaks
- `<b>` or `<strong>` - Bold
- `<em>` or `<i>` - Italics
- `<a href="url">text</a>` - Links
- `<ul><li>` - Bullet lists

**Standard Footer Template:**
```html
<p>Send us your comments, questions, and suggestions using this form: <a href="https://forms.gle/ncwo6HZeN4uA9gPg7">https://forms.gle/ncwo6HZeN4uA9gPg7</a></p>
<p>Thanks to <a href="https://www.linkedin.com/in/amulya-shastry/"><b>Amulya Shastry</b></a> for editing and management support.</p>
<p>Follow us on LinkedIn: <a href="https://www.linkedin.com/in/lpantano/">https://www.linkedin.com/in/lpantano/</a> and <a href="https://www.linkedin.com/in/alexandra-bartlett-926b32109/">https://www.linkedin.com/in/alexandra-bartlett-926b32109/</a></p>
```

---

## Step 4: Upload to Internet Archive

### Option A: Upload a Single File (Recommended)

Upload just the new episode's audio file:

```bash
pixi run upload-single "audio/episode_01_Your Episode Title.mp3"
```

This command:
- Uploads only the specified file to the `acoffeewithcompbio` collection
- Automatically updates `episode_metadata.json` with the `archive_url` for that episode
- Faster and safer than uploading all files

**Example:**
```bash
pixi run upload-single "audio/episode_01_202601_12-New-Year-Resolutions-For-Computational-Biologists.m4a"
```

### Option B: Upload All Files

Upload all audio files at once (use with caution):

```bash
pixi run upload
```

This command:
- Uploads all files in `audio/` directory to the `acoffeewithcompbio` collection
- Automatically updates `episode_metadata.json` with the `archive_url` for each episode
- Skips files that are already uploaded
- Can be slow if you have many files

**First-time setup:** If you haven't configured Internet Archive credentials:
```bash
pixi run ia configure
```

---

## Step 5: Regenerate the RSS Feed

Generate a new `feed.xml` with the updated episodes:

```bash
pixi run generate-rss
```

This reads `episode_metadata.json` and creates the RSS feed with all episodes.

---

## Step 6: Preview Locally (Optional)

Test the feed before deploying:

```bash
pixi run preview
```

Open http://localhost:8000/feed.xml in your browser to verify the feed renders correctly.

---

## Step 7: Deploy

Commit and push changes to trigger a Netlify deployment:

```bash
git add feed.xml episode_metadata.json
git commit -m "Add S02E01: Your Episode Title"
git push
```

Note: Audio files in `audio/` are gitignored and hosted on Internet Archive.

---

## Complete Example: Adding Season 2 Episode 1

### 1. Copy audio file
```bash
cp ~/Downloads/season2_ep1.mp3 "audio/episode_01_Welcome to Season 2.mp3"
```

### 2. Create episode markdown
```bash
cp episodes_markdown/TEMPLATE.md episodes_markdown/S02E01_welcome-to-season-2.md
# Edit the file with your episode details
```

### 3. Add to metadata (via AI agent or manually)

**Option A - AI-single "audio/episode_01_202601_12-New-Year-Resolutions-For-Computational-Biologists.m4a" Agent:**
> "Add the episode from episodes_markdown/S02E01_welcome-to-season-2.md to episode_metadata.json"

**Option B - Manual:**
Add at the beginning of the `episodes` array:
```json
{
  "season": 2,
  "number": 1,
  "title": "Welcome to Season 2 - New Year, New Topics",
  "description": "<p>We're back for Season 2! In this episode, Alex and Lorena share what's in store for the new season and reflect on highlights from Season 1.</p><p><br /></p><p>Send us your comments, questions, and suggestions using this form: <a href=\"https://forms.gle/ncwo6HZeN4uA9gPg7\">https://forms.gle/ncwo6HZeN4uA9gPg7</a></p><p><br /></p><p>Thanks to <a href=\"https://www.linkedin.com/in/amulya-shastry/\"><b>Amulya Shastry</b></a> for editing and management support.</p><p><br /></p><p>Follow us on LinkedIn: <a href=\"https://www.linkedin.com/in/lpantano/\">https://www.linkedin.com/in/lpantano/</a> and <a href=\"https://www.linkedin.com/in/alexandra-bartlett-926b32109/\">https://www.linkedin.com/in/alexandra-bartlett-926b32109/</a></p>",
  "published": "Mon, 27 Jan 2026 12:00:00 +0000",
  "duration": "18:45",
  "original_audio_url": "",
  "local_file": "audio/episode_01_Welcome to Season 2 - New Year, New Topics.mp3",
  "archive_url": ""
}
```

### 4. Upload and generate
```bash
pixi run upload
pixi run generate-rss
```

### 5. Preview (optional)
```bash
pixi run preview
# Open http://localhost:8000/feed.xml
```

### 6. Deploy
```bash
git add feed.xml episode_metadata.json
git commit -m "Add S02E01: Welcome to Season 2 - New Year, New Topics"
git push
```

---

## Quick Reference: All Commands

| Command | Description |
|---------|-------------|
| `pixi run upload-single <file>` | Upload a single audio file to Internet Archive |
| `pixi run upload` | Upload all audio files to Internet Archive |
| `pixi run generate-rss` | Generate feed.xml from metadata |
| `pixi run preview` | Start local preview server |
| `pixi run ia configure` | Configure Internet Archive credentials |
| `pixi run download` | Download episodes from Ausha (migration only) |

---

## Troubleshooting

### Audio file not appearing in feed
- Verify the `local_file` path matches the actual filename exactly
- Run `pixi run generate-rss` after adding metadata
- Check that the file exists in `audio/` directory

### Internet Archive upload fails
- Run `pixi run ia configure` to re-authenticate
- Check your internet connection
- Verify the file isn't corrupted

### RSS validation errors
- Validate at https://podba.se/validate/
- Check that dates are in RFC 2822 format
- Ensure HTML in descriptions is properly escaped

### Feed not updating on podcast apps
- Most podcast apps check feeds every 1-24 hours
- Apple Podcasts Connect can force a refresh
- Verify the Netlify deployment completed successfully

---

## Season Management

Episodes are organized by `season` and `number` fields in the metadata. The RSS feed correctly tags episodes with:
- `<itunes:season>` and `<podcast:season>` for season number
- `<itunes:episode>` and `<podcast:episode>` for episode number

When starting a new season:
1. Set `"season": 2` (or appropriate number)
2. Reset episode numbering: `"number": 1`
3. Continue incrementing `number` for subsequent episodes in that season
