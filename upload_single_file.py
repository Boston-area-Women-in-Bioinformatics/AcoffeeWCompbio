#!/usr/bin/env python3
"""
Upload a single audio file to Internet Archive and update episode_metadata.json
"""
import json
import sys
from pathlib import Path
from internetarchive import get_item

def upload_single_file(audio_file_path):
    """Upload a single audio file to Internet Archive"""
    
    # Configuration
    ARCHIVE_IDENTIFIER = "acoffeewithcompbio"
    METADATA_FILE = Path("episode_metadata.json")
    
    audio_file = Path(audio_file_path)
    
    if not audio_file.exists():
        print(f"❌ Error: File not found: {audio_file}")
        sys.exit(1)
    
    # Get relative path from audio/ directory
    if audio_file.is_absolute():
        try:
            relative_path = audio_file.relative_to(Path.cwd() / "audio")
            local_file = f"audio/{relative_path}"
        except ValueError:
            # Not in audio directory
            local_file = str(audio_file)
    else:
        local_file = str(audio_file)
    
    print(f"Uploading file: {audio_file.name}")
    print(f"To collection: {ARCHIVE_IDENTIFIER}")
    
    # Get the Internet Archive item
    item = get_item(ARCHIVE_IDENTIFIER)
    
    # Prepare metadata for the file
    file_metadata = {
        'collection': ARCHIVE_IDENTIFIER,
        'mediatype': 'audio',
    }
    
    # Upload the file
    try:
        print(f" uploading {audio_file.name}...")
        result = item.upload(
            str(audio_file),
            metadata=file_metadata,
            verbose=True
        )
        
        archive_url = f"https://archive.org/download/{ARCHIVE_IDENTIFIER}/{audio_file.name}"
        print(f"  ✓ Uploaded: {archive_url}")
        
        # Update episode_metadata.json with the archive_url
        if METADATA_FILE.exists():
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Find the episode with matching local_file
            updated = False
            for episode in metadata['episodes']:
                if episode['local_file'] == local_file or episode['local_file'].endswith(audio_file.name):
                    episode['archive_url'] = archive_url
                    updated = True
                    print(f"  ✓ Updated metadata for: {episode['title']}")
                    break
            
            if updated:
                with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                print(f"  ✓ Saved updated metadata to {METADATA_FILE}")
            else:
                print(f"  ⚠ Warning: No matching episode found in metadata for {local_file}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Upload failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_single_file.py <audio_file_path>")
        print("Example: python upload_single_file.py audio/episode_01_202601_12-New-Year-Resolutions-For-Computational-Biologists.m4a")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    success = upload_single_file(audio_file)
    sys.exit(0 if success else 1)
