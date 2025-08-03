#!/usr/bin/env python3
"""
Test Spotify metadata integration
"""

from mp3_downloader import MP3Downloader

def test_spotify_metadata():
    """Test Spotify metadata enhancement"""
    print("🧪 Testing Spotify metadata integration...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    # Test with a well-known song that should be on Spotify
    file_path = downloader.download_mp3(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        artist_name="Rick Astley",
        song_name="Never Gonna Give You Up"
        # Note: Not providing album name to test Spotify lookup
    )
    
    if file_path:
        print(f"✅ Download completed: {file_path}")
        
        # Check the enhanced ID3 tags
        try:
            from mutagen.mp3 import MP3
            audio = MP3(file_path)
            
            if audio.tags:
                print("\n🏷️  Enhanced ID3 Tags:")
                artist = audio.tags.get('TPE1')
                title = audio.tags.get('TIT2')
                album = audio.tags.get('TALB')
                genre = audio.tags.get('TCON')
                year = audio.tags.get('TDRC')
                track = audio.tags.get('TRCK')
                
                print(f"   Artist: {artist.text[0] if artist else 'Not set'}")
                print(f"   Title: {title.text[0] if title else 'Not set'}")
                print(f"   Album: {album.text[0] if album else 'Not set'}")
                print(f"   Genre: {genre.text[0] if genre else 'Not set'}")
                print(f"   Year: {year.text[0] if year else 'Not set'}")
                print(f"   Track: {track.text[0] if track else 'Not set'}")
                
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
    test_spotify_metadata()
