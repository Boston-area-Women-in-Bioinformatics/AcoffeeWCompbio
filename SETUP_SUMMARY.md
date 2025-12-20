# A Coffee with CompBio - Self-Hosting Setup Summary

## ✅ What's Been Completed

### 1. Environment Setup
- ✅ Pixi installed and configured
- ✅ Python dependencies installed (feedparser, requests, internetarchive)
- ✅ `pixi.toml` created for environment management

### 2. Audio Files
- ✅ All 12 episodes downloaded (198MB total)
- ✅ Podcast artwork downloaded
- ✅ Files stored in `audio/` directory
- ✅ Metadata saved to `episode_metadata.json`

### 3. RSS Feed
- ✅ RSS feed generated matching Ausha format
- ✅ All 12 episodes included
- ✅ Placeholder URLs ready for update
- ✅ File: `feed.xml`

### 4. Website
- ✅ Landing page created (`index.html`)
- ✅ Netlify configuration (`netlify.toml`)
- ✅ Git ignore file (`.gitignore`)

### 5. Scripts
- ✅ `download_podcast_audio.py` - Downloads episodes
- ✅ `upload_to_archive.py` - Uploads to Internet Archive
- ✅ `generate_rss.py` - Generates RSS feed
- ✅ All scripts runnable via Pixi tasks

---

## 📋 Next Steps

### Step 1: Upload Audio to Internet Archive

1. Configure Internet Archive credentials:
   ```bash
   pixi run ia configure
   ```

   You'll need:
   - An account at https://archive.org
   - Your email and password

2. Upload all audio files:
   ```bash
   pixi run upload
   ```

   This will create: `https://archive.org/details/acoffeewithcompbio`

### Step 2: Deploy to Netlify

**Option A: GitHub + Netlify (Recommended)**

1. Initialize Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial podcast RSS setup"
   git branch -M main
   ```

2. Create a GitHub repository at https://github.com/new
   - Repository name: `acoffeewithcompbio`
   - Keep it public or private
   - Don't initialize with README

3. Push to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/acoffeewithcompbio.git
   git push -u origin main
   ```

4. Deploy on Netlify:
   - Go to https://app.netlify.com
   - Click "New site from Git"
   - Connect your GitHub repository
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `.`
   - Click "Deploy site"

5. Your site will be live at: `https://YOUR-SITE-NAME.netlify.app`

**Option B: Netlify CLI**

```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

**Option C: Drag & Drop**

- Go to https://app.netlify.com/drop
- Drag your project folder
- Instant deployment!

### Step 3: Update URLs

After deploying to Netlify, update the URLs:

1. Open `generate_rss.py`
2. Update these lines (around line 13-16):
   ```python
   PODCAST_LINK = "https://YOUR-ACTUAL-SITE.netlify.app"
   FEED_URL = "https://YOUR-ACTUAL-SITE.netlify.app/feed.xml"
   ARTWORK_URL = "https://YOUR-ACTUAL-SITE.netlify.app/podcast-artwork.jpeg"
   ```

3. Regenerate the RSS feed:
   ```bash
   pixi run generate-rss
   ```

4. Commit and push changes:
   ```bash
   git add feed.xml generate_rss.py
   git commit -m "Update URLs with actual Netlify deployment"
   git push
   ```

### Step 4: Submit Your RSS Feed

Once your feed is live, submit it to podcast directories:

- **Apple Podcasts**: https://podcastsconnect.apple.com
- **Spotify**: https://podcasters.spotify.com
- **Google Podcasts**: https://podcastsmanager.google.com
- **Other directories**: Use your feed URL

Your RSS feed will be at: `https://YOUR-SITE.netlify.app/feed.xml`

---

## 📁 Project Structure

```
AcoffeeWCompbio/
├── audio/                          # Downloaded audio files (198MB)
│   ├── episode_01_*.mp3
│   ├── episode_02_*.mp3
│   └── ...
├── podcast-artwork.jpeg            # Podcast artwork (751KB)
├── index.html                      # Landing page
├── feed.xml                        # RSS feed
├── episode_metadata.json           # Episode metadata
├── download_podcast_audio.py       # Download script
├── upload_to_archive.py            # Upload script
├── generate_rss.py                 # RSS generation script
├── pixi.toml                       # Environment config
├── netlify.toml                    # Netlify config
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore
└── README.md                       # Full documentation
```

---

## 🎯 Quick Commands

```bash
# Download episodes
pixi run download

# Upload to Internet Archive
pixi run upload

# Generate RSS feed
pixi run generate-rss

# Deploy to Netlify
netlify deploy --prod
```

---

## 🔗 Important URLs

- **Original Feed**: https://feed.ausha.co/Gdv6mfJNJ2M7
- **New Feed** (after deployment): https://YOUR-SITE.netlify.app/feed.xml
- **Internet Archive**: https://archive.org/details/acoffeewithcompbio
- **Landing Page**: https://YOUR-SITE.netlify.app

---

## 📊 Episode List

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
11. **Episode 10: Collaboration Survival Guide** (16:59) - November 11, 2025
12. **Episode 11: A Comp-bio Holiday Calendar** (14:02) - December 16, 2025

**Total**: 12 episodes, ~198MB

---

## 🆘 Troubleshooting

### Issue: Audio files won't upload to Internet Archive
- Ensure you've run `ia configure`
- Check your credentials
- Verify storage quota

### Issue: RSS feed not updating in podcast apps
- Clear the podcast app's cache
- Some apps take 24-48 hours to refresh
- Validate your feed at: https://podba.se/validate/

### Issue: Netlify deployment fails
- Check `.gitignore` excludes `audio/` folder
- Verify all files are committed to git
- Check build logs in Netlify dashboard

---

## 📝 Notes

- The `audio/` directory is excluded from git (.gitignore)
- Audio files are hosted on Internet Archive (free, permanent)
- RSS feed and website are hosted on Netlify (free tier)
- Podcast artwork is included in the repository

---

## 🎉 You're All Set!

Your podcast is ready to be self-hosted! Just complete the three steps above and you'll have full control over your podcast RSS feed.

**Questions?** Check the README.md for detailed instructions.
