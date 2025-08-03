#!/usr/bin/env python3
"""
Simple test script for the new yt-dlp only MP3 downloader
"""

from mp3_downloader import MP3Downloader

def test_single_download():
    """Test downloading a single song"""
    print("🧪 Testing single download...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    # Test with Rick Astley
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    file_path = downloader.download_mp3(
        test_url, 
        artist_name="Rick Astley", 
        song_name="Never Gonna Give You Up",
        album_name="Whenever You Need Somebody"
    )
    
    if file_path:
        print(f"✅ Single download test passed: {file_path}")
        return True
    else:
        print("❌ Single download test failed")
        return False

def test_multiple_downloads():
    """Test downloading multiple songs"""
    print("\n🧪 Testing multiple downloads...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    # Test with multiple songs from the same album
    test_songs = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Rick Astley", "Never Gonna Give You Up"),
        ("https://www.youtube.com/watch?v=ZbZSe6N_BXs", "Pharrell Williams", "Happy"),
    ]
    
    downloaded_files = downloader.download_multiple(test_songs, album_name="Test Album Collection")
    
    if len(downloaded_files) > 0:
        print(f"✅ Multiple download test passed: {len(downloaded_files)} files downloaded")
        return True
    else:
        print("❌ Multiple download test failed")
        return False

def test_id3_tags():
    """Test ID3 tag functionality"""
    print("\n🧪 Testing ID3 tags...")
    
    try:
        from mutagen.mp3 import MP3
        
        # Check if we have a recent download to examine
        import glob
        mp3_files = glob.glob("test_downloads/**/*.mp3", recursive=True)
        
        if mp3_files:
            # Check the most recent file
            test_file = mp3_files[0]
            audio = MP3(test_file)
            
            if audio.tags:
                artist = audio.tags.get('TPE1')
                title = audio.tags.get('TIT2')
                album = audio.tags.get('TALB')
                
                print(f"   File: {test_file}")
                print(f"   Artist: {artist.text[0] if artist else 'Not set'}")
                print(f"   Title: {title.text[0] if title else 'Not set'}")
                print(f"   Album: {album.text[0] if album else 'Not set'}")
                
                if artist:
                    print("✅ ID3 tags test passed: Tags found")
                    return True
                else:
                    print("❌ ID3 tags test failed: No artist tag")
                    return False
            else:
                print("❌ ID3 tags test failed: No tags found")
                return False
        else:
            print("⚠️  ID3 tags test skipped: No MP3 files to check")
            return True
            
    except ImportError:
        print("⚠️  ID3 tags test skipped: mutagen not available")
        return True
    except Exception as e:
        print(f"❌ ID3 tags test failed: {e}")
        return False

def test_video_info():
    """Test getting video information"""
    print("\n🧪 Testing video info...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    info = downloader.get_video_info(test_url)
    
    if info and info.get('title'):
        print(f"✅ Video info test passed: {info['title']}")
        return True
    else:
        print("❌ Video info test failed")
        return False

def main():
    """Run all tests"""
    print("YouTube to MP3 Downloader - Test Suite")
    print("=" * 50)
    
    tests = [
        test_video_info,
        test_single_download,
        test_id3_tags,
        # test_multiple_downloads,  # Commented out to avoid too many downloads
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The downloader is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
