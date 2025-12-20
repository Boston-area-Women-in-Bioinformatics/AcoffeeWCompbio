# 🧪 Local Testing Guide

## Testing RSS Feed Rendering

The RSS feed is now configured to work **identically** in local testing and on Netlify!

### Start the Preview Server

```bash
pixi run preview
```

### Test the RSS Feed

Open in your browser:
- **RSS Feed with styling**: http://localhost:8000/feed.xml
- **Landing page**: http://localhost:8000/
- **Direct artwork access**: http://localhost:8000/podcast-artwork.jpeg

### What You Should See

When you open `http://localhost:8000/feed.xml`:

1. ✅ **Podcast artwork** displayed (752KB JPEG image)
2. ✅ **Podcast title and description**
3. ✅ **All 12 episodes** listed with:
   - Episode artwork (same as podcast artwork)
   - Episode titles
   - Descriptions
   - Publication dates and durations
   - Audio players (will show placeholder URLs until uploaded to Internet Archive)
   - Download buttons

### Troubleshooting

**Artwork not showing?**
1. Check that `podcast-artwork.jpeg` exists in the project root
2. Verify the file size: `ls -lh podcast-artwork.jpeg` (should be ~752KB)
3. Check browser console for errors (F12)
4. Try hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)

**Raw XML showing instead of styled page?**
1. Ensure `rss.xslt` exists in the project root
2. Ensure `rss-styles.css` exists in the project root
3. Check browser console for errors
4. Some browsers may not support XSLT - try Chrome or Firefox

**Audio players not working?**
- This is expected! The audio URLs point to Internet Archive placeholder URLs
- Audio will work after you upload to Internet Archive

## How It Works

The RSS feed uses **relative URLs** for the artwork:

```xml
<image>
    <url>podcast-artwork.jpeg</url>
    ...
</image>
```

This means:
- ✅ Works locally: `http://localhost:8000/podcast-artwork.jpeg`
- ✅ Works on Netlify: `https://your-site.netlify.app/podcast-artwork.jpeg`
- ✅ No URL updates needed between environments!

## Switching to Absolute URLs

If you need absolute URLs (some podcast directories require them), edit `generate_rss.py`:

```python
# Change this line from True to False
USE_RELATIVE_URLS = False
```

Then update the production URLs:
```python
PODCAST_LINK = "https://your-actual-site.netlify.app"
FEED_URL = "https://your-actual-site.netlify.app/feed.xml"
ARTWORK_URL_ABSOLUTE = "https://your-actual-site.netlify.app/podcast-artwork.jpeg"
```

And regenerate:
```bash
pixi run generate-rss
```

**But you probably don't need to do this!** Relative URLs work fine for most cases.

## Comparison: Local vs Netlify

| Feature | Local (localhost:8000) | Netlify |
|---------|------------------------|---------|
| RSS rendering | ✅ Works | ✅ Works |
| Artwork display | ✅ Works | ✅ Works |
| Episode list | ✅ Works | ✅ Works |
| Audio players | ⚠️ Placeholder URLs | ✅ After IA upload |
| HTTPS | ❌ HTTP only | ✅ HTTPS |
| Public access | ❌ Local only | ✅ Public |

## Ready for Netlify?

Your setup will work exactly the same way on Netlify as it does locally!

Just deploy and everything will work:
1. Same artwork loading
2. Same RSS rendering
3. Same episode display

The only difference will be:
- HTTPS instead of HTTP
- Public URLs instead of localhost
- Working audio players (after you upload to Internet Archive)

---

**Next step**: Deploy to Netlify! Your local preview is a perfect representation of what users will see.
