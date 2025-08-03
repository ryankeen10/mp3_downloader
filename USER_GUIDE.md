# 🎵 User Guide - MP3 Downloader

## Quick Setup for New Users

### 1. Get the Code
```bash
git clone https://github.com/ryankeen10/mp3_downloader.git
cd mp3_downloader
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install ffmpeg
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Linux**: `sudo apt install ffmpeg`

### 4. Setup API Keys
```bash
# Copy the templates
cp youtube_credentials.py.template youtube_credentials.py
cp spotify_credentials.py.template spotify_credentials.py

# Edit with your actual API keys
nano youtube_credentials.py  # Add your YouTube API key
nano spotify_credentials.py # Add your Spotify credentials
```

See [SETUP.md](SETUP.md) for detailed API key instructions.

### 5. Run the App
```bash
python main.py
```

## How to Use

### Interactive Mode (Recommended)

1. Run `python main.py`
2. Search for an artist (e.g., "Radiohead")
3. Choose to browse:
   - **Songs** - Individual tracks
   - **Albums** - Complete albums
4. Select what you want to download
5. The app will:
   - Find each song on YouTube
   - Download high-quality audio
   - Add rich metadata (artist, album, year, etc.)
   - Organize files by artist and album

### Direct Download Mode

```bash
# Simple download
python mp3_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"

# With custom metadata
python mp3_downloader.py "URL" "Artist Name" "Song Title" "Album Name"
```

## File Organization

Your downloads are saved to:
```
~/Downloads/Audio Downloads/
├── Artist Name/
│   ├── Album Name/
│   │   ├── Artist - Song 1.mp3
│   │   └── Artist - Song 2.mp3
│   └── Artist - Single Song.mp3
```

## Metadata Tags

Each MP3 file gets professional ID3 tags:
- **Artist** (TPE1/TPE2): From Spotify data or your input
- **Title** (TIT2): Song name
- **Album** (TALB): Album name (when available)
- **Year** (TDRC): Release year from Spotify (when available)

**Note**: Genre and track number are intentionally left blank to avoid issues with Apple Music and other players that prefer you to set these manually.

Perfect for:
- Apple Music (will display artist, title, album, year)
- Spotify (local files)
- Any music player that reads ID3 tags

## Configuration

Edit `config.py` to customize:
```python
PARENT_FOLDER_NAME = "Audio Downloads"  # Main download folder
AUDIO_QUALITY = "192"                   # Bitrate in kbps
USE_ARTIST_FOLDERS = True               # Organize by artist
USE_SPOTIFY_METADATA = True             # Enhanced metadata
```

## Troubleshooting

### "YouTube API key not found"
- Make sure `youtube_credentials.py` exists
- Check that your API key is valid
- Verify YouTube Data API v3 is enabled

### "Spotify credentials not found"
- Make sure `spotify_credentials.py` exists  
- Check Client ID and Secret are correct
- Verify your Spotify app is active

### "ffmpeg not found"
- Install ffmpeg for your platform
- Make sure it's in your system PATH
- Try running `ffmpeg -version` in terminal

### Poor Search Results
- Try more specific search terms
- Check spelling of artist/song names
- Some content may not be available on YouTube

### Download Fails
- Check your internet connection
- Some videos may be region-restricted
- Try a different video if one fails

## Tips for Best Results

1. **Use full artist names** - "The Beatles" vs "Beatles"
2. **Search albums first** - Better organization and metadata
3. **Check your selections** - Review before downloading
4. **Be patient** - High-quality downloads take time
5. **Respect copyright** - Only download content you have rights to

## Advanced Usage

### Environment Variables
Instead of credential files, you can use environment variables:
```bash
export YOUTUBE_API_KEY="your_key_here"
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
python main.py
```

### Batch Processing
The interactive mode supports:
- Multiple song selections
- Complete album downloads
- Artist discography browsing

### Custom Folder Structure
Modify folder names in `config.py`:
```python
PARENT_FOLDER_NAME = "My Music"  # Changes main folder
USE_ARTIST_FOLDERS = False       # Flat structure
```

---

## Need Help?

1. Check this guide first
2. Read [SETUP.md](SETUP.md) for API setup
3. Open an issue on GitHub with:
   - Your operating system
   - Python version (`python --version`)
   - Full error message
   - Steps you tried

Enjoy your perfectly organized music library! 🎵
