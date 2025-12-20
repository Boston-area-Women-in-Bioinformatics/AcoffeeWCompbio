#!/usr/bin/env python3
"""
Download all audio files from A Coffee with CompBio podcast RSS feed.
"""

import os
import sys
import requests
import feedparser
from pathlib import Path
from urllib.parse import urlparse

# RSS feed URL
RSS_FEED_URL = "https://feed.ausha.co/Gdv6mfJNJ2M7"

# Create directory for audio files
AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

def sanitize_filename(filename):
    """Remove or replace characters that are problematic in filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_audio_file(url, episode_title, episode_number):
    """Download a single audio file."""
    try:
        print(f"Downloading Episode {episode_number}: {episode_title}")

        # Get file extension from URL
        parsed_url = urlparse(url)
        ext = os.path.splitext(parsed_url.path)[1] or '.mp3'

        # Create filename
        safe_title = sanitize_filename(episode_title)
        filename = f"episode_{episode_number:02d}_{safe_title}{ext}"
        filepath = AUDIO_DIR / filename

        # Skip if already downloaded
        if filepath.exists():
            print(f"  ✓ Already exists: {filename}")
            return filepath

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Progress: {percent:.1f}%", end='')

        print(f"\n  ✓ Downloaded: {filename}")
        return filepath

    except Exception as e:
        print(f"  ✗ Error downloading {episode_title}: {e}")
        return None

def main():
    """Main function to download all podcast episodes."""
    print(f"Fetching RSS feed from: {RSS_FEED_URL}\n")

    # Parse RSS feed
    feed = feedparser.parse(RSS_FEED_URL)

    if not feed.entries:
        print("Error: No episodes found in feed!")
        sys.exit(1)

    print(f"Found {len(feed.entries)} episodes\n")

    # Download each episode
    downloaded_files = []
    for idx, entry in enumerate(feed.entries, 1):
        title = entry.get('title', f'Episode {idx}')

        # Find the audio enclosure
        audio_url = None
        if hasattr(entry, 'enclosures') and entry.enclosures:
            audio_url = entry.enclosures[0].get('href')
        elif hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('audio/'):
                    audio_url = link.get('href')
                    break

        if audio_url:
            filepath = download_audio_file(audio_url, title, idx)
            if filepath:
                downloaded_files.append({
                    'number': idx,
                    'title': title,
                    'filepath': filepath,
                    'original_url': audio_url
                })
        else:
            print(f"⚠ No audio URL found for: {title}")

        print()  # Empty line between episodes

    # Print summary
    print("=" * 60)
    print(f"Download complete! {len(downloaded_files)}/{len(feed.entries)} episodes downloaded")
    print(f"Audio files saved in: {AUDIO_DIR.absolute()}")
    print("=" * 60)

    # Save metadata
    import json
    metadata_file = Path("episode_metadata.json")
    metadata = {
        'podcast_title': feed.feed.get('title', 'A Coffee with CompBio'),
        'podcast_description': feed.feed.get('description', ''),
        'episodes': []
    }

    for idx, entry in enumerate(feed.entries, 1):
        episode_data = {
            'number': idx,
            'title': entry.get('title', ''),
            'description': entry.get('description', ''),
            'published': entry.get('published', ''),
            'duration': entry.get('itunes_duration', ''),
            'original_audio_url': None,
            'local_file': None
        }

        # Find audio URL
        if hasattr(entry, 'enclosures') and entry.enclosures:
            episode_data['original_audio_url'] = entry.enclosures[0].get('href')

        # Find matching downloaded file
        for df in downloaded_files:
            if df['number'] == idx:
                episode_data['local_file'] = str(df['filepath'])
                break

        metadata['episodes'].append(episode_data)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nMetadata saved to: {metadata_file.absolute()}")

if __name__ == "__main__":
    main()
