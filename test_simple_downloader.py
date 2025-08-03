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
        song_name="Never Gonna Give You Up"
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
    
    # Test with multiple songs
    test_songs = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Rick Astley", "Never Gonna Give You Up"),
        ("https://www.youtube.com/watch?v=ZbZSe6N_BXs", "Pharrell Williams", "Happy"),
    ]
    
    downloaded_files = downloader.download_multiple(test_songs)
    
    if len(downloaded_files) > 0:
        print(f"✅ Multiple download test passed: {len(downloaded_files)} files downloaded")
        return True
    else:
        print("❌ Multiple download test failed")
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
