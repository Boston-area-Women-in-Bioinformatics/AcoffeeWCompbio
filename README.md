# A Coffee with CompBio - Self-Hosted Podcast

This repository contains the scripts and RSS feed for self-hosting the "A Coffee with CompBio" podcast, migrating from Ausha to a self-hosted solution using Internet Archive for audio hosting and Netlify for RSS feed deployment.

## Overview

- **Original Feed**: Ausha (https://feed.ausha.co/Gdv6mfJNJ2M7)
- **Audio Hosting**: Internet Archive
- **RSS Hosting**: Netlify
- **Episodes**: 12 total (11 episodes + 1 trailer)
- **RSS Web Rendering**: Feed displays as a beautiful webpage in browsers!

## Features

✨ **RSS Feed Web Rendering** - Your RSS feed renders as a beautiful, interactive webpage when opened in a browser (just like the original Ausha feed), while still working perfectly in podcast apps.

🎨 **Professional Landing Page** - Custom homepage for your podcast

🎙️ **All Episodes Downloaded** - Complete archive of all 12 episodes

📦 **Easy Management** - Pixi environment manager for simple setup

## Quick Start

### 1. Environment Setup (Using Pixi)

Pixi manages all dependencies automatically. If you don't have Pixi installed:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.zshrc  # or restart your terminal
```

Then install dependencies:

```bash
pixi install
```

That's it! No need to install Python packages manually.

### 2. Preview Your RSS Feed Locally

Test the RSS feed rendering in your browser:

```bash
pixi run preview
```

Then open in your browser:
- **RSS Feed**: http://localhost:8000/feed.xml ← Beautiful webpage!
- **Website**: http://localhost:8000/

Press `Ctrl+C` to stop the server.

### 3. Download All Audio Files (Already Done!)

The audio files have already been downloaded. If you need to re-download:

```bash
pixi run download
```

This will:
- Create an `audio/` directory
- Download all 12 episode audio files (198MB)
- Generate `episode_metadata.json` with episode information

### 4. Configure Internet Archive

Before uploading, you need to configure your Internet Archive credentials:

```bash
pixi run ia configure
```

You'll need:
- An Internet Archive account (create at https://archive.org)
- Your email and password

### 5. Upload to Internet Archive

```bash
pixi run upload
```

This will:
- Upload all audio files to Internet Archive
- Create a collection at: `https://archive.org/details/acoffeewithcompbio`
- Update `episode_metadata.json` with Internet Archive URLs

**Note**: You can customize the Internet Archive identifier by editing `ARCHIVE_IDENTIFIER` in `upload_to_archive.py`

### 6. Generate RSS Feed

```bash
pixi run generate-rss
```

This creates `feed.xml` with:
- All episode metadata
- Internet Archive audio URLs (or placeholder URLs)
- iTunes/Spotify/Google Play compatible tags
- XSLT stylesheet reference for web rendering

**Important**: After deploying to Netlify, edit `generate_rss.py` (lines 13-16) to update:
- Your Netlify deployment URL
- Feed URL
- Artwork URL

Then regenerate: `pixi run generate-rss`

## Deployment to Netlify

### Option 1: GitHub + Netlify Auto-Deploy (Recommended)

1. Create a new GitHub repository at https://github.com/new
   - Repository name: `acoffeewithcompbio`

2. Push this code:
   ```bash
   git init
   git add .
   git commit -m "Initial podcast RSS setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/acoffeewithcompbio.git
   git push -u origin main
   ```

3. In Netlify (https://app.netlify.com):
   - Click "New site from Git"
   - Connect your GitHub repository
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `.`
   - Click "Deploy site"

4. Your site will be live at: `https://YOUR-SITE-NAME.netlify.app`
   - RSS Feed: `https://YOUR-SITE-NAME.netlify.app/feed.xml`
   - Website: `https://YOUR-SITE-NAME.netlify.app/`

5. Update URLs in `generate_rss.py` and regenerate:
   ```bash
   # Edit generate_rss.py lines 13-16 with your Netlify URL
   pixi run generate-rss
   git add feed.xml generate_rss.py
   git commit -m "Update URLs with Netlify deployment"
   git push
   ```

### Option 2: Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod
```

### Option 3: Manual Drag & Drop

1. Go to https://app.netlify.com/drop
2. Drag the entire project folder
3. Your feed will be live instantly!

## File Structure

```
AcoffeeWCompbio/
├── audio/                      # Downloaded audio files (198MB)
│   ├── episode_01_*.mp3
│   ├── episode_02_*.mp3
│   └── ...
├── feed.xml                    # RSS feed with web rendering
├── rss.xslt                    # XSLT stylesheet (XML → HTML)
├── rss-styles.css              # Beautiful CSS styling
├── index.html                  # Landing page
├── podcast-artwork.jpeg        # Podcast cover art
├── episode_metadata.json       # Episode metadata and URLs
├── download_podcast_audio.py   # Downloads audio from Ausha RSS
├── upload_to_archive.py        # Uploads to Internet Archive
├── generate_rss.py             # Generates RSS feed
├── preview-server.py           # Local preview server
├── pixi.toml                   # Pixi environment config
├── netlify.toml                # Netlify deployment config
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore (excludes audio/)
└── README.md                   # This file
```

## Pixi Commands

All commands use Pixi for consistent environment:

```bash
pixi run preview       # Preview RSS feed in browser
pixi run download      # Download all episodes from Ausha
pixi run upload        # Upload audio to Internet Archive
pixi run generate-rss  # Generate RSS feed
pixi run ia configure  # Configure Internet Archive credentials
```

## RSS Feed Web Rendering

Your RSS feed uses XSLT to render as a beautiful webpage in browsers while remaining compatible with all podcast apps!

**When opened in a browser** (`feed.xml`):
- ✅ Displays podcast artwork and description
- ✅ Shows all episodes with titles and descriptions
- ✅ Embedded audio players for each episode
- ✅ Download buttons
- ✅ Copyable feed URL for easy subscription
- ✅ Responsive design for mobile/desktop

**When opened in a podcast app**:
- ✅ Works perfectly as a standard RSS feed
- ✅ All episodes load correctly
- ✅ Metadata preserved

See `RSS_WEB_RENDERING.md` for technical details.

## Updating Your Podcast

When you publish new episodes:

1. Download new episodes: `pixi run download`
2. Upload to Internet Archive: `pixi run upload`
3. Regenerate RSS feed: `pixi run generate-rss`
4. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Add new episode"
   git push
   ```

Netlify will automatically redeploy!

## Episode List

1. **Trailer: About Us** (6:19) - May 27, 2025
2. **Episode 1: Nine Samples and Zero Cells** (16:13) - May 27, 2025
3. **Episode 2: The Thousand-Dollar Alignment** (22:00) - June 10, 2025
4. **Episode 3: R Markdown for RNA-seq** (21:35) - June 26, 2025
5. **Episode 4: Spatial Transcriptomics App Development** (26:39) - July 10, 2025
6. **Episode 5: R You Doing It Right?** (21:27) - July 29, 2025
7. **Episode 6: A Coffee with Katie Hughes** (20:04) - August 12, 2025
8. **Episode 7: Spatial Transcriptomics Toolkit** (18:05) - September 2, 2025
9. **Episode 8: (Dry) Lab Notebooks** (16:11) - September 23, 2025
10. **Episode 9: A Coffee with Saranya Canchi** (13:55) - October 14, 2025
11. **Episode 10: Collaboration Survival Guide for CompBio** (16:59) - November 11, 2025
12. **Episode 11: A Comp-bio Holiday Calendar** (14:02) - December 16, 2025

## Customization

### Change Internet Archive Identifier

Edit `upload_to_archive.py` (line 16):
```python
ARCHIVE_IDENTIFIER = "your-custom-identifier"
```

### Change RSS Feed Colors

Edit `rss-styles.css` (line 14):
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Replace with your brand colors!

### Update Deployment URLs

Edit `generate_rss.py` (lines 13-16):
```python
PODCAST_LINK = "https://YOUR-SITE.netlify.app"
FEED_URL = "https://YOUR-SITE.netlify.app/feed.xml"
ARTWORK_URL = "https://YOUR-SITE.netlify.app/podcast-artwork.jpeg"
AUDIO_BASE_URL = "https://archive.org/download/acoffeewithcompbio"
```

## Troubleshooting

### Pixi Issues
```bash
# Reinstall environment
pixi install --force

# Check Pixi version
pixi --version
```

### Download Issues
- Check your internet connection
- Verify the RSS feed is still accessible
- Some files may be large, be patient during downloads

### Internet Archive Upload Issues
- Ensure you've run `pixi run ia configure`
- Check your credentials are correct
- Verify you have enough storage quota

### RSS Feed Not Updating
- Clear your podcast app's cache
- Some apps take 24-48 hours to refresh
- Validate your feed at: https://podba.se/validate/

### RSS Not Rendering in Browser
- Ensure `rss.xslt` and `rss-styles.css` are deployed
- Check browser console for errors
- Some browsers may show raw XML (this is normal, the feed still works!)

## Submit to Podcast Directories

Once your RSS feed is live:

- **Apple Podcasts**: https://podcastsconnect.apple.com
- **Spotify**: https://podcasters.spotify.com
- **Google Podcasts**: https://podcastsmanager.google.com
- **Other directories**: Use your feed URL

Your RSS feed URL: `https://YOUR-SITE.netlify.app/feed.xml`

## Resources

- [Pixi Documentation](https://pixi.sh)
- [Internet Archive Documentation](https://archive.org/services/docs/api/)
- [Podcast RSS Spec](https://help.apple.com/itc/podcasts_connect/#/itcb54353390)
- [Netlify Documentation](https://docs.netlify.com/)
- [XSLT Tutorial](https://www.w3schools.com/xml/xsl_intro.asp)

## License

Podcast content: Copyright Lorena Pantano and Alex Bartlett
Scripts: MIT License
