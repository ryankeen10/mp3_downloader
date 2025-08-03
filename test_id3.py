#!/usr/bin/env python3
"""
Simple test for ID3 functionality
"""

from mp3_downloader import MP3Downloader

def test_id3_simple():
    """Test ID3 functionality with a simple download"""
    print("🧪 Testing ID3 tagging...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    # Download with full metadata
    file_path = downloader.download_mp3(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        artist_name="Rick Astley",
        song_name="Never Gonna Give You Up",
        album_name="Whenever You Need Somebody"
    )
    
    if file_path:
        print(f"✅ Download completed: {file_path}")
        
        # Check the ID3 tags
        try:
            from mutagen.mp3 import MP3
            audio = MP3(file_path)
            
            if audio.tags:
                print("\n🏷️  ID3 Tags found:")
                artist = audio.tags.get('TPE1')
                title = audio.tags.get('TIT2')
                album = audio.tags.get('TALB')
                genre = audio.tags.get('TCON')
                
                print(f"   Artist: {artist.text[0] if artist else 'Not set'}")
                print(f"   Title: {title.text[0] if title else 'Not set'}")
                print(f"   Album: {album.text[0] if album else 'Not set'}")
                print(f"   Genre: {genre.text[0] if genre else 'Not set'}")
                
                return True
            else:
                print("❌ No ID3 tags found")
                return False
                
        except Exception as e:
            print(f"❌ Error checking ID3 tags: {e}")
            return False
    else:
        print("❌ Download failed")
        return False

if __name__ == "__main__":
    test_id3_simple()
