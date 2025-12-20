#!/usr/bin/env python3
"""
Upload podcast audio files to Internet Archive.
Requires: internetarchive package (pip install internetarchive)
Configure: ia configure (to set up credentials)
"""

import json
import sys
from pathlib import Path
try:
    from internetarchive import get_item, upload
except ImportError:
    print("Error: internetarchive package not installed")
    print("Install with: pip install internetarchive")
    sys.exit(1)

# Internet Archive identifier for your podcast
# This should be unique and URL-friendly
ARCHIVE_IDENTIFIER = "acoffeewithcompbio"

def upload_to_archive():
    """Upload all audio files to Internet Archive."""

    # Load metadata
    metadata_file = Path("episode_metadata.json")
    if not metadata_file.exists():
        print("Error: episode_metadata.json not found!")
        print("Run download_podcast_audio.py first.")
        sys.exit(1)

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    audio_dir = Path("audio")
    if not audio_dir.exists():
        print("Error: audio directory not found!")
        sys.exit(1)

    # Prepare Internet Archive metadata
    ia_metadata = {
        'title': metadata.get('podcast_title', 'A Coffee with CompBio'),
        'description': metadata.get('podcast_description', ''),
        'mediatype': 'audio',
        'collection': 'opensource_audio',
        'creator': 'Lorena Pantano and Alex Bartlett',
        'subject': ['podcast', 'computational biology', 'bioinformatics', 'science'],
    }

    print(f"Uploading to Internet Archive identifier: {ARCHIVE_IDENTIFIER}")
    print(f"URL will be: https://archive.org/details/{ARCHIVE_IDENTIFIER}")
    print()

    # Get or create the item
    item = get_item(ARCHIVE_IDENTIFIER)

    # Upload each audio file
    uploaded_urls = {}
    for episode in metadata['episodes']:
        if not episode.get('local_file'):
            print(f"⚠ Skipping episode {episode['number']}: No local file")
            continue

        local_file = Path(episode['local_file'])
        if not local_file.exists():
            print(f"⚠ Skipping episode {episode['number']}: File not found: {local_file}")
            continue

        print(f"Uploading Episode {episode['number']}: {episode['title']}")

        # Prepare file metadata
        file_metadata = {
            'title': f"{episode['number']:02d} - {episode['title']}",
            'description': episode.get('description', ''),
            'date': episode.get('published', ''),
            'track': str(episode['number'])
        }

        try:
            # Upload the file (convert Path to string for internetarchive library)
            result = item.upload(
                str(local_file),
                metadata=file_metadata,
                verbose=True
            )

            # Store the URL for this file
            archive_url = f"https://archive.org/download/{ARCHIVE_IDENTIFIER}/{local_file.name}"
            uploaded_urls[episode['number']] = archive_url
            episode['archive_url'] = archive_url

            print(f"  ✓ Uploaded: {archive_url}\n")

        except Exception as e:
            print(f"  ✗ Error uploading: {e}\n")

    # Update metadata with archive URLs
    with open('episode_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("=" * 60)
    print(f"Upload complete!")
    print(f"View at: https://archive.org/details/{ARCHIVE_IDENTIFIER}")
    print("=" * 60)
    print("\nUpdated episode_metadata.json with Internet Archive URLs")

    return uploaded_urls

if __name__ == "__main__":
    # Check if user is logged in to Internet Archive
    print("Note: You need to configure Internet Archive credentials first.")
    print("Run: ia configure")
    print("You'll need to create an account at https://archive.org if you don't have one.")
    print()

    response = input("Have you configured your IA credentials? (y/n): ")
    if response.lower() != 'y':
        print("\nPlease run 'ia configure' first, then run this script again.")
        sys.exit(0)

    upload_to_archive()
