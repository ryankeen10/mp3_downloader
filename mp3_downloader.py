import sys
import re
import os
import subprocess
import time
from pathlib import Path

# Try to load configuration, fall back to defaults if not available
try:
    from config import PARENT_FOLDER_NAME, AUDIO_QUALITY, USE_ARTIST_FOLDERS
except ImportError:
    # Default configuration if config.py doesn't exist
    PARENT_FOLDER_NAME = "Audio Downloads"
    AUDIO_QUALITY = "192K"
    USE_ARTIST_FOLDERS = True

class MP3Downloader:
    """
    A simplified class for downloading MP3s from YouTube videos using yt-dlp only
    """
    
    def __init__(self, download_folder=None, parent_folder_name=None):
        """
        Initialize the downloader with a target folder
        
        Args:
            download_folder (str): Custom download path. If None, uses ~/Downloads/[parent_folder_name]
            parent_folder_name (str): Name of the parent folder in Downloads. If None, uses config default
        """
        # Use configuration defaults if not specified
        if parent_folder_name is None:
            parent_folder_name = PARENT_FOLDER_NAME
            
        # Use user's Downloads folder by default
        if download_folder is None:
            download_folder = os.path.join(Path.home(), "Downloads", parent_folder_name)
        
        self.base_download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        
        # Check if yt-dlp is available
        self._check_ytdlp_availability()
    
    def _check_ytdlp_availability(self):
        """Check if yt-dlp is available"""
        try:
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                         capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.ytdlp_available = True
                print(f"✅ yt-dlp is available (version: {result.stdout.strip()})")
            else:
                self.ytdlp_available = False
                print("❌ yt-dlp is not working properly")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            self.ytdlp_available = False
            print("❌ yt-dlp is not installed")
            print("Install with: pip install yt-dlp")
    
    def download_mp3(self, youtube_url, artist_name=None, song_name=None):
        """
        Download an MP3 from a YouTube URL using yt-dlp
        
        Args:
            youtube_url (str): The YouTube video URL
            artist_name (str, optional): Artist name for file naming
            song_name (str, optional): Song name for file naming
            
        Returns:
            str: Path to the downloaded file or None if download failed
        """
        if not self.ytdlp_available:
            print("❌ yt-dlp is not available. Please install it first:")
            print("pip install yt-dlp")
            return None
        
        try:
            print(f"🎵 Downloading: {youtube_url}")
            
            # Validate YouTube URL
            if not self._is_valid_youtube_url(youtube_url):
                print("❌ Invalid YouTube URL")
                return None
            
            # Determine artist folder and create if needed
            if artist_name and USE_ARTIST_FOLDERS:
                clean_artist = self._clean_filename(artist_name)
                artist_folder = os.path.join(self.base_download_folder, clean_artist)
                if not os.path.exists(artist_folder):
                    os.makedirs(artist_folder)
                download_folder = artist_folder
            else:
                download_folder = self.base_download_folder
            
            # Generate filename
            if artist_name and song_name:
                # Clean names for filename
                clean_artist = self._clean_filename(artist_name)
                clean_song = self._clean_filename(song_name)
                output_template = f"{clean_artist} - {clean_song}.%(ext)s"
            else:
                # Use video title
                output_template = "%(title)s.%(ext)s"
            
            output_path = os.path.join(download_folder, output_template)
            
            # yt-dlp command
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--extract-audio',              # Extract audio only
                '--audio-format', 'mp3',        # Convert to MP3
                '--audio-quality', AUDIO_QUALITY, # Configurable quality
                '--output', output_path,        # Output path
                '--no-playlist',                # Single video only
                '--ignore-errors',              # Continue on errors
                youtube_url
            ]
            
            print("🔄 Converting to MP3...")
            
            # Run yt-dlp
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Find the downloaded file
                downloaded_file = self._find_downloaded_file(download_folder, artist_name, song_name)
                if downloaded_file:
                    print(f"✅ Download successful: {downloaded_file}")
                    return downloaded_file
                else:
                    print("❌ File was converted but not found in expected location")
                    print("Check the downloads folder manually")
                    return None
            else:
                print(f"❌ yt-dlp failed:")
                print(result.stderr)
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Download timed out after 5 minutes")
            return None
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    def _is_valid_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL"""
        youtube_patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([0-9A-Za-z_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([0-9A-Za-z_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([0-9A-Za-z_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in youtube_patterns:
            if re.search(pattern, url):
                return True
        return False
    
    def _clean_filename(self, filename):
        """Clean filename to remove invalid characters"""
        # Remove or replace invalid characters for filenames
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid chars
        filename = re.sub(r'[^\w\s\-_\.]', '', filename)  # Keep only alphanumeric, spaces, hyphens, underscores, dots
        filename = filename.strip()  # Remove leading/trailing spaces
        return filename
    
    def _find_downloaded_file(self, search_folder, artist_name=None, song_name=None):
        """Find the most recently downloaded MP3 file in the specified folder"""
        try:
            # Get all MP3 files in search folder
            mp3_files = []
            for file in os.listdir(search_folder):
                if file.lower().endswith('.mp3'):
                    file_path = os.path.join(search_folder, file)
                    mp3_files.append((file_path, os.path.getctime(file_path)))
            
            if not mp3_files:
                return None
            
            # Sort by creation time (most recent first)
            mp3_files.sort(key=lambda x: x[1], reverse=True)
            
            # If we have artist and song name, try to find exact match first
            if artist_name and song_name:
                clean_artist = self._clean_filename(artist_name).lower()
                clean_song = self._clean_filename(song_name).lower()
                
                for file_path, _ in mp3_files:
                    filename = os.path.basename(file_path).lower()
                    if clean_artist in filename and clean_song in filename:
                        return file_path
            
            # Return the most recent file
            return mp3_files[0][0]
            
        except Exception as e:
            print(f"Error finding downloaded file: {e}")
            return None
    
    def download_multiple(self, urls_with_metadata):
        """
        Download multiple songs
        
        Args:
            urls_with_metadata (list): List of tuples (url, artist, song) or just urls
            
        Returns:
            list: List of downloaded file paths
        """
        downloaded_files = []
        
        for item in urls_with_metadata:
            if isinstance(item, tuple):
                url, artist, song = item
            else:
                url, artist, song = item, None, None
            
            print(f"\n📥 Downloading {len(downloaded_files) + 1}/{len(urls_with_metadata)}")
            
            file_path = self.download_mp3(url, artist, song)
            if file_path:
                downloaded_files.append(file_path)
            
            # Small delay between downloads to be respectful
            if len(urls_with_metadata) > 1:
                time.sleep(2)
        
        print(f"\n🎉 Download complete! {len(downloaded_files)}/{len(urls_with_metadata)} files downloaded successfully")
        return downloaded_files
    
    def get_video_info(self, youtube_url):
        """
        Get information about a YouTube video without downloading
        
        Args:
            youtube_url (str): The YouTube video URL
            
        Returns:
            dict: Video information or None if failed
        """
        if not self.ytdlp_available:
            return None
        
        try:
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--dump-json',
                '--no-playlist',
                youtube_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown')
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

# Example usage and CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("YouTube to MP3 Downloader")
        print("=" * 40)
        print("Usage:")
        print(f"  {sys.argv[0]} <youtube_url>")
        print(f"  {sys.argv[0]} <youtube_url> \"Artist Name\" \"Song Name\"")
        print()
        print("Examples:")
        print(f"  {sys.argv[0]} 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        print(f"  {sys.argv[0]} 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' 'Rick Astley' 'Never Gonna Give You Up'")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    artist_name = sys.argv[2] if len(sys.argv) > 2 else None
    song_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Create downloader
    downloader = MP3Downloader()
    
    # Show video info first
    print("📺 Video Information:")
    info = downloader.get_video_info(youtube_url)
    if info:
        print(f"   Title: {info['title']}")
        print(f"   Uploader: {info['uploader']}")
        if info['duration']:
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            print(f"   Duration: {minutes}:{seconds:02d}")
        print()
    
    # Download the MP3
    file_path = downloader.download_mp3(youtube_url, artist_name, song_name)
    
    if file_path:
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"📁 File saved: {file_path}")
        print(f"💾 File size: {file_size:.1f} MB")
    else:
        print("❌ Download failed")
        sys.exit(1)
