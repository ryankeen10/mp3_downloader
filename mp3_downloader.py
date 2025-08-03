import sys
import re
import os
import subprocess
import time
from pathlib import Path

# Try to load configuration, fall back to defaults if not available
try:
    from config import PARENT_FOLDER_NAME, AUDIO_QUALITY, USE_ARTIST_FOLDERS, USE_SPOTIFY_METADATA, FALLBACK_GENRE, FALLBACK_YEAR
except ImportError:
    # Default configuration if config.py doesn't exist
    PARENT_FOLDER_NAME = "Audio Downloads"
    AUDIO_QUALITY = "192K"
    USE_ARTIST_FOLDERS = True
    USE_SPOTIFY_METADATA = True
    FALLBACK_GENRE = None
    FALLBACK_YEAR = None

# Import for ID3 tag manipulation
try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, TPE2, TRCK
    ID3_AVAILABLE = True
except ImportError:
    ID3_AVAILABLE = False
    print("⚠️  Warning: mutagen not available. ID3 tags will not be added.")

# Import for Spotify metadata
try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    from credentials_helper import get_spotify_credentials
    SPOTIFY_AVAILABLE = True
except ImportError:
    SPOTIFY_AVAILABLE = False
    if USE_SPOTIFY_METADATA:
        print("⚠️  Warning: Spotify credentials not available. Metadata enhancement disabled.")

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
    
    def download_mp3(self, youtube_url, artist_name=None, song_name=None, album_name=None):
        """
        Download an MP3 from a YouTube URL using yt-dlp
        
        Args:
            youtube_url (str): The YouTube video URL
            artist_name (str, optional): Artist name for file naming and ID3 tags
            song_name (str, optional): Song name for file naming and ID3 tags
            album_name (str, optional): Album name for ID3 tags
            
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
                    # Add ID3 tags to the file
                    self._add_id3_tags(downloaded_file, artist_name, song_name, album_name, youtube_url)
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
    
    def _add_id3_tags(self, file_path, artist_name=None, song_name=None, album_name=None, youtube_url=None):
        """
        Add ID3 tags to the MP3 file (legacy method for direct downloads)
        
        Args:
            file_path (str): Path to the MP3 file
            artist_name (str, optional): Artist name
            song_name (str, optional): Song/track name
            album_name (str, optional): Album name
            youtube_url (str, optional): Original YouTube URL (for reference)
        """
        if not ID3_AVAILABLE:
            return
        
        try:
            # Load the MP3 file
            audio = MP3(file_path)
            
            # Add ID3 tags if they don't exist
            if audio.tags is None:
                audio.add_tags()
            
            # Get video info for fallback data
            video_info = self.get_video_info(youtube_url) if youtube_url else {}
            
            # Determine the best values to use (User Input > Video Info > Fallback)
            final_artist = (artist_name or 
                          video_info.get('uploader') or 
                          "Unknown Artist")
            
            final_title = (song_name or 
                         (self._clean_video_title_for_song(video_info['title']) if video_info.get('title') else None) or
                         "Unknown Title")
            
            final_album = album_name
            
            # Leave genre and year blank (no Spotify lookup)
            final_year = FALLBACK_YEAR
            final_genre = FALLBACK_GENRE
            
            # Set the ID3 tags
            audio.tags.add(TIT2(encoding=3, text=final_title))
            audio.tags.add(TPE1(encoding=3, text=final_artist))
            audio.tags.add(TPE2(encoding=3, text=final_artist))  # Album artist
            
            if final_album:
                audio.tags.add(TALB(encoding=3, text=final_album))
            
            if final_genre:
                audio.tags.add(TCON(encoding=3, text=final_genre))
            
            if final_year:
                audio.tags.add(TDRC(encoding=3, text=str(final_year)))
            
            # Save the tags
            audio.save()
            
            # Show what was added
            tag_info = f"Artist: {final_artist}, Title: {final_title}"
            if final_album:
                tag_info += f", Album: {final_album}"
            if final_genre:
                tag_info += f", Genre: {final_genre}"
            if final_year:
                tag_info += f", Year: {final_year}"
            
            print(f"🏷️  ID3 tags added: {tag_info}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not add ID3 tags: {e}")
    
    def _add_id3_tags_with_metadata(self, file_path, artist_name=None, song_name=None, album_name=None, spotify_metadata=None):
        """
        Add ID3 tags using pre-cached Spotify metadata (no API calls needed)
        
        Args:
            file_path (str): Path to the MP3 file
            artist_name (str, optional): Artist name
            song_name (str, optional): Song name
            album_name (str, optional): Album name
            spotify_metadata (dict, optional): Pre-cached Spotify metadata
        """
        if not ID3_AVAILABLE:
            return
        
        try:
            # Load the MP3 file
            audio = MP3(file_path)
            
            # Add ID3 tags if they don't exist
            if audio.tags is None:
                audio.add_tags()
            
            # Use cached Spotify metadata if available
            if not spotify_metadata:
                spotify_metadata = {}
            
            # Get video info for fallback data
            video_info = {}  # Skip YouTube API call since we have Spotify data
            
            # Determine the best values to use (Cached Spotify > User Input > Fallback)
            final_artist = artist_name or "Unknown Artist"
            final_title = song_name or "Unknown Title"
            final_album = album_name or spotify_metadata.get('album')
            
            # Extract year from Spotify release date
            final_year = None
            if spotify_metadata.get('release_date'):
                try:
                    final_year = spotify_metadata['release_date'][:4]
                except (IndexError, TypeError):
                    pass
            
            # Set genre to None (leave blank) since we don't have it in our cached data
            # This avoids the "Downloaded" generic tag
            final_genre = None
            
            # Set the ID3 tags
            audio.tags.add(TIT2(encoding=3, text=final_title))
            audio.tags.add(TPE1(encoding=3, text=final_artist))
            audio.tags.add(TPE2(encoding=3, text=final_artist))  # Album artist
            
            if final_album:
                audio.tags.add(TALB(encoding=3, text=final_album))
            
            if final_year:
                audio.tags.add(TDRC(encoding=3, text=str(final_year)))
            
            # Save the tags
            audio.save()
            
            # Show what was added
            tag_info = f"Artist: {final_artist}, Title: {final_title}"
            if final_album:
                tag_info += f", Album: {final_album}"
            if final_year:
                tag_info += f", Year: {final_year}"
            
            print(f"🏷️  ID3 tags added (from cached Spotify data): {tag_info}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not add ID3 tags: {e}")
    
    def _clean_video_title_for_song(self, title):
        """
        Clean up a YouTube video title to make it suitable as a song name
        
        Args:
            title (str): Original video title
            
        Returns:
            str: Cleaned song name
        """
        # Remove common patterns from YouTube titles
        title = re.sub(r'\[.*?\]', '', title)  # Remove [Official Video], [Lyrics], etc.
        title = re.sub(r'\(.*?[Oo]fficial.*?\)', '', title)  # Remove (Official Video), etc.
        title = re.sub(r'\(.*?[Vv]ideo.*?\)', '', title)  # Remove (Video), (Music Video), etc.
        title = re.sub(r'\(.*?[Ll]yrics.*?\)', '', title)  # Remove (Lyrics), (With Lyrics), etc.
        title = re.sub(r'\(.*?[Aa]udio.*?\)', '', title)  # Remove (Audio), (Official Audio), etc.
        title = re.sub(r'\|.*', '', title)  # Remove everything after |
        title = re.sub(r'-.*[Yy]ou[Tt]ube.*', '', title)  # Remove "- YouTube" and similar
        title = re.sub(r'HD$|4K$', '', title)  # Remove HD, 4K suffixes
        title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
        title = title.strip(' -')  # Remove leading/trailing spaces and dashes
        
        return title if title else "Unknown Title"
    
    def download_multiple(self, urls_with_metadata, album_name=None):
        """
        Download multiple songs
        
        Args:
            urls_with_metadata (list): List of tuples (url, artist, song) or just urls
            album_name (str, optional): Album name to apply to all downloads
            
        Returns:
            list: List of downloaded file paths
        """
        downloaded_files = []
        
        for item in urls_with_metadata:
            current_album = album_name  # Initialize with default album
            
            if isinstance(item, tuple):
                if len(item) == 3:
                    url, artist, song = item
                elif len(item) == 4:
                    url, artist, song, item_album = item
                    # Use item-specific album if provided, otherwise use batch album
                    current_album = item_album if item_album else album_name
                else:
                    url = item[0]
                    artist = item[1] if len(item) > 1 else None
                    song = item[2] if len(item) > 2 else None
            else:
                url, artist, song = item, None, None
            
            print(f"\n📥 Downloading {len(downloaded_files) + 1}/{len(urls_with_metadata)}")
            
            file_path = self.download_mp3(url, artist, song, current_album)
            if file_path:
                downloaded_files.append(file_path)
            
            # Small delay between downloads to be respectful
            if len(urls_with_metadata) > 1:
                time.sleep(2)
        
        print(f"\n🎉 Download complete! {len(downloaded_files)}/{len(urls_with_metadata)} files downloaded successfully")
        return downloaded_files
    
    def download_multiple_with_metadata(self, urls_with_metadata):
        """
        Download multiple songs using cached Spotify metadata
        
        Args:
            urls_with_metadata (list): List of tuples (url, artist, song, album, spotify_metadata)
            
        Returns:
            list: List of downloaded file paths
        """
        downloaded_files = []
        
        for item in urls_with_metadata:
            url, artist, song, album, spotify_metadata = item
            
            print(f"\n📥 Downloading {len(downloaded_files) + 1}/{len(urls_with_metadata)}")
            print(f"🎵 Using cached Spotify metadata for enhanced tags")
            
            file_path = self.download_mp3_with_metadata(url, artist, song, album, spotify_metadata)
            if file_path:
                downloaded_files.append(file_path)
            
            # Small delay between downloads to be respectful
            if len(urls_with_metadata) > 1:
                time.sleep(2)
        
        print(f"\n🎉 Download complete! {len(downloaded_files)}/{len(urls_with_metadata)} files downloaded successfully")
        return downloaded_files
    
    def download_mp3_with_metadata(self, youtube_url, artist_name=None, song_name=None, album_name=None, spotify_metadata=None):
        """
        Download an MP3 using pre-cached Spotify metadata
        
        Args:
            youtube_url (str): The YouTube video URL
            artist_name (str, optional): Artist name
            song_name (str, optional): Song name
            album_name (str, optional): Album name
            spotify_metadata (dict, optional): Pre-cached Spotify metadata
            
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
                    # Add ID3 tags using cached Spotify metadata
                    self._add_id3_tags_with_metadata(downloaded_file, artist_name, song_name, album_name, spotify_metadata)
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
        print(f"  {sys.argv[0]} <youtube_url> \"Artist Name\" \"Song Name\" \"Album Name\"")
        print()
        print("Examples:")
        print(f"  {sys.argv[0]} 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        print(f"  {sys.argv[0]} 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' 'Rick Astley' 'Never Gonna Give You Up'")
        print(f"  {sys.argv[0]} 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' 'Rick Astley' 'Never Gonna Give You Up' 'Whenever You Need Somebody'")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    artist_name = sys.argv[2] if len(sys.argv) > 2 else None
    song_name = sys.argv[3] if len(sys.argv) > 3 else None
    album_name = sys.argv[4] if len(sys.argv) > 4 else None
    
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
    file_path = downloader.download_mp3(youtube_url, artist_name, song_name, album_name)
    
    if file_path:
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"📁 File saved: {file_path}")
        print(f"💾 File size: {file_size:.1f} MB")
    else:
        print("❌ Download failed")
        sys.exit(1)
