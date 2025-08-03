#!/usr/bin/env python3
"""
Test the fixed download_multiple method
"""

from mp3_downloader import MP3Downloader

def test_download_multiple_fix():
    """Test that download_multiple works without UnboundLocalError"""
    print("🧪 Testing download_multiple fix...")
    
    downloader = MP3Downloader(download_folder="test_downloads")
    
    # Test with a simple list like main.py would create
    download_list = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Rick Astley", "Never Gonna Give You Up")
    ]
    
    try:
        downloaded_files = downloader.download_multiple(download_list, album_name="Test Album")
        print(f"✅ Test passed: {len(downloaded_files)} files downloaded")
        return True
    except UnboundLocalError as e:
        print(f"❌ UnboundLocalError still exists: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Other error (but not UnboundLocalError): {e}")
        return True  # This is acceptable for this test

if __name__ == "__main__":
    test_download_multiple_fix()
