#!/usr/bin/env python3
"""
Generate a new RSS feed for the podcast matching the Ausha format.
Uses placeholder URLs for Internet Archive audio hosting.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

# Configuration - Update these with your actual values
#
# IMPORTANT: USE_RELATIVE_URLS should normally be True
# - True: Uses relative URLs (podcast-artwork.jpeg) - works for local testing AND Netlify
# - False: Uses absolute URLs - only needed if submitting to some podcast directories
#
# Relative URLs work perfectly fine on Netlify and in most podcast apps!
USE_RELATIVE_URLS = False

# Production URLs (update these after deploying to Netlify)
PODCAST_LINK = "https://podcast.boston-wib.org"
FEED_URL = "https://podcast.boston-wib.org/feed.xml"
ARTWORK_URL_ABSOLUTE = "https://podcast.boston-wib.org/podcast-artwork-2026.jpg"
AUDIO_BASE_URL = "https://archive.org/download/acoffeewithcompbio"

# Relative URLs for local testing and Netlify deployment
ARTWORK_URL_RELATIVE = "podcast-artwork-2026.jpg"

# Choose which artwork URL to use
ARTWORK_URL = ARTWORK_URL_RELATIVE if USE_RELATIVE_URLS else ARTWORK_URL_ABSOLUTE

def generate_guid(title):
    """Generate a GUID from episode title."""
    return hashlib.sha1(title.encode()).hexdigest()

def escape_cdata(text):
    """Escape text for CDATA sections."""
    if not text:
        return ""
    # Remove the "Hosted on Ausha" message if present
    text = text.replace('Hosted on Ausha. See ausha.co/privacy-policy for more information.', '').strip()
    return text

def create_rss_header():
    """Create the RSS XML header."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="rss.xslt" ?>
<rss
    xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
    xmlns:googleplay="http://www.google.com/schemas/play-podcasts/1.0"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:spotify="http://www.spotify.com/ns/rss"
    xmlns:podcast="https://podcastindex.org/namespace/1.0"
    version="2.0">
'''

def create_channel_header(metadata):
    """Create the channel metadata section."""
    description = escape_cdata(metadata.get('podcast_description', ''))
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    return f'''    <channel>
        <title>A Coffee with CompBio</title>
        <link>{PODCAST_LINK}</link>
        <atom:link rel="self" type="application/rss+xml" href="{FEED_URL}"/>
        <description>{description}</description>
        <language>en</language>
        <copyright>Lorena Pantano</copyright>
        <lastBuildDate>{now}</lastBuildDate>
        <pubDate>{now}</pubDate>
        <generator>Self-hosted podcast feed</generator>
        <spotify:countryOfOrigin>us</spotify:countryOfOrigin>

        <itunes:author>Lorena Pantano</itunes:author>
        <itunes:owner>
            <itunes:name>Lorena Pantano</itunes:name>
            <itunes:email>lorena.pantano@gmail.com</itunes:email>
        </itunes:owner>
        <itunes:summary>{description}</itunes:summary>
        <itunes:explicit>false</itunes:explicit>
        <itunes:block>no</itunes:block>
        <podcast:block>no</podcast:block>
        <itunes:type>episodic</itunes:type>

        <googleplay:author>Lorena Pantano</googleplay:author>
        <googleplay:email>lorena.pantano@gmail.com</googleplay:email>
        <googleplay:description>{description}</googleplay:description>
        <googleplay:explicit>false</googleplay:explicit>

        <category>Science</category>
        <itunes:category text="Science">
            <itunes:category text="Life Sciences"/>
        </itunes:category>
        <category>Business</category>
        <itunes:category text="Business">
            <itunes:category text="Careers"/>
        </itunes:category>

        <image>
            <url>{ARTWORK_URL}</url>
            <title>A Coffee with CompBio</title>
            <link>{PODCAST_LINK}</link>
        </image>
        <itunes:image href="{ARTWORK_URL}"/>
        <googleplay:image href="{ARTWORK_URL}"/>

'''

def create_episode_item(episode):
    """Create an episode item in the RSS feed."""
    title = episode.get('title', '')
    guid = generate_guid(title)
    description = escape_cdata(episode.get('description', ''))
    pub_date = episode.get('published', '')
    duration = episode.get('duration', '')
    episode_num = episode.get('number', 1)
    season_num = episode.get('season', 1)

    # Use Internet Archive URL if available, otherwise construct placeholder
    local_file = Path(episode.get('local_file', ''))

    if episode.get('archive_url'):
        audio_url = episode['archive_url']
    else:
        audio_filename = local_file.name if local_file.exists() else f"episode_{episode_num:02d}.mp3"
        audio_url = f"{AUDIO_BASE_URL}/{audio_filename}"

    # Get file size
    file_size = local_file.stat().st_size if local_file.exists() else 0

    # Create subtitle (first 125 chars of description without HTML)
    import re
    subtitle_text = re.sub('<[^<]+?>', '', description)
    subtitle = subtitle_text[:125] + '...' if len(subtitle_text) > 125 else subtitle_text

    item = f'''        <item>
            <title>{title}</title>
            <guid isPermaLink="false">{guid}</guid>
            <description><![CDATA[{description}]]></description>
            <content:encoded><![CDATA[{description}]]></content:encoded>
            <pubDate>{pub_date}</pubDate>
            <enclosure url="{audio_url}" length="{file_size}" type="audio/mpeg"/>
            <link>{PODCAST_LINK}</link>

            <itunes:author>Lorena Pantano</itunes:author>
            <itunes:explicit>false</itunes:explicit>
            <itunes:keywords>life science,data science,bioinformatics,computational biology</itunes:keywords>
            <itunes:duration>{duration}</itunes:duration>
            <itunes:episodeType>full</itunes:episodeType>
            <itunes:season>{season_num}</itunes:season>
            <podcast:season>{season_num}</podcast:season>
            <itunes:episode>{episode_num}</itunes:episode>
            <podcast:episode>{episode_num}</podcast:episode>
            <itunes:subtitle>{subtitle}</itunes:subtitle>

            <googleplay:author>Lorena Pantano</googleplay:author>
            <googleplay:explicit>false</googleplay:explicit>

            <itunes:image href="{ARTWORK_URL}"/>
            <googleplay:image href="{ARTWORK_URL}"/>
        </item>
'''
    return item

def generate_rss():
    """Generate RSS feed from metadata."""

    # Load metadata
    metadata_file = Path("episode_metadata.json")
    if not metadata_file.exists():
        print("Error: episode_metadata.json not found!")
        return

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    # Start building the RSS feed
    rss_content = create_rss_header()
    rss_content += create_channel_header(metadata)

    # Add episodes (reverse order so newest first)
    episodes = metadata['episodes']
    for episode in episodes:
        rss_content += create_episode_item(episode)

    # Close tags
    rss_content += '''    </channel>
</rss>'''

    # Write to file
    output_file = Path('feed.xml')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rss_content)

    print(f"✓ RSS feed generated: {output_file.absolute()}")
    print(f"  Episodes included: {len(episodes)}")
    print()
    print("Placeholder URLs used:")
    print(f"  - Podcast link: {PODCAST_LINK}")
    print(f"  - Feed URL: {FEED_URL}")
    print(f"  - Artwork: {ARTWORK_URL}")
    print(f"  - Audio base: {AUDIO_BASE_URL}")
    print()
    print("Next steps:")
    print("1. Upload audio files to Internet Archive")
    print("2. Update URLs in generate_rss.py with your actual Netlify URL")
    print("3. Re-run this script after deploying to Netlify")
    print("4. Commit feed.xml and deploy via Netlify")

if __name__ == "__main__":
    generate_rss()
