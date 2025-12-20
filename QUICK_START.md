# 🚀 Quick Start Guide

## One-Time Setup

```bash
# 1. Install Pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.zshrc  # or restart terminal

# 2. Install dependencies
pixi install

# 3. Preview locally (test the RSS rendering!)
pixi run preview
# Open: http://localhost:8000/feed.xml
```

## Deploy Your Podcast

### Step 1: Upload Audio to Internet Archive

```bash
# Configure credentials (one time only)
pixi run ia configure

# Upload all episodes
pixi run upload
```

### Step 2: Deploy to Netlify

**Via GitHub:**
```bash
# Initialize git repo
git init
git add .
git commit -m "Initial podcast setup"
git branch -M main

# Create repo on GitHub, then push
git remote add origin https://github.com/YOUR_USERNAME/acoffeewithcompbio.git
git push -u origin main

# Connect on Netlify.com → "New site from Git"
```

**Or via Drag & Drop:**
- Go to https://app.netlify.com/drop
- Drag project folder
- Done!

### Step 3: Update URLs

```bash
# Edit generate_rss.py (lines 13-16) with your Netlify URL
# Then regenerate:
pixi run generate-rss

# Push changes
git add .
git commit -m "Update URLs"
git push
```

## 📋 All Pixi Commands

```bash
pixi run preview       # Preview RSS feed in browser (localhost:8000)
pixi run download      # Download episodes from Ausha
pixi run upload        # Upload to Internet Archive
pixi run generate-rss  # Generate RSS feed
pixi run ia configure  # Configure Internet Archive
```

## 🎯 What You Get

- **Landing Page**: `https://YOUR-SITE.netlify.app/`
- **RSS Feed**: `https://YOUR-SITE.netlify.app/feed.xml`
  - Opens as beautiful webpage in browsers
  - Works perfectly in podcast apps
- **Audio Hosting**: Internet Archive (free, permanent)
- **All 12 episodes** ready to stream

## ✅ Final Steps

1. Submit RSS feed to podcast directories:
   - Apple Podcasts: https://podcastsconnect.apple.com
   - Spotify: https://podcasters.spotify.com
   - Google Podcasts: https://podcastsmanager.google.com

2. Test your feed at: https://podba.se/validate/

3. Share your new feed URL with listeners!

---

**Need help?** Check the full README.md for detailed instructions.
