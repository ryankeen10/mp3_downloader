# YouTube to MP3 Downloader

A Python application for downloading YouTube videos and converting them to MP3 format using yt-dlp.

## Features

- **Smart Organization**: Downloads are saved to `~/Downloads/Audio Downloads/[Artist Name]/`
- **Configurable**: Customize folder names, audio quality, and organization in `config.py`
- **Artist Folders**: Each artist gets their own folder for better organization
- **Multiple Input Methods**: Search by song name or use direct YouTube URLs
- **Batch Downloads**: Download multiple songs at once
- **High Quality**: 192K MP3 conversion with yt-dlp
- **Clean Interface**: Simple command-line interface with progress indicators
- **Reliable**: Uses yt-dlp for consistent, high-quality downloads

## Requirements

- Python 3.7+
- yt-dlp (for downloading and converting)
- ffmpeg (for audio processing)
- Google API key for YouTube search (optional - only needed for search functionality)

## Installation

1. Clone this repository
2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install yt-dlp google-api-python-client
```

4. Install ffmpeg:
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt install ffmpeg`
   - On Windows: Download from https://ffmpeg.org/

5. (Optional) Set up your YouTube API credentials in `youtube_credentials.py` for search functionality

## Usage

### Interactive Mode (with search)
```bash
python main.py
```

### Direct URL Download
```bash
python mp3_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Direct URL Download with Custom Names
```bash
python mp3_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" "Artist Name" "Song Title"
```

### Batch Download
```bash
python mp3_downloader.py "URL1" "URL2" "URL3"
```

### Run Tests
```bash
python test_simple_downloader.py
```

## File Organization

Files are automatically organized in your Downloads folder:

```
~/Downloads/Audio Downloads/
├── Rick Astley/
│   ├── Rick Astley - Never Gonna Give You Up.mp3
│   └── Rick Astley - Together Forever.mp3
├── Queen/
│   ├── Queen - Bohemian Rhapsody.mp3
│   └── Queen - We Will Rock You.mp3
└── Unknown Artist/
    └── Video Title.mp3
```

- **With Artist Name**: `~/Downloads/Audio Downloads/[Artist]/[Artist] - [Song].mp3`
- **Without Artist**: `~/Downloads/Audio Downloads/[Video Title].mp3`

## Configuration

You can customize the downloader behavior by editing `config.py`:

```python
# Parent folder name in ~/Downloads/
PARENT_FOLDER_NAME = "Audio Downloads"  # Change to "Music", "MP3s", etc.

# Audio quality (128K, 192K, 256K, 320K)
AUDIO_QUALITY = "192K"

# Whether to create artist subfolders
USE_ARTIST_FOLDERS = True
```

**Popular folder name options:**
- `"Audio Downloads"` (default) - Generic, platform-agnostic
- `"Music"` - Simple and clean
- `"MP3 Downloads"` - Descriptive of file type
- `"Downloaded Audio"` - Clear purpose

- **Downloads Folder**: Uses `~/Downloads/[PARENT_FOLDER_NAME]/` by default
- **YouTube API**: Set up your API key in `youtube_credentials.py` for search functionality:
```python
YOUTUBE_API_KEY = "your_api_key_here"
```

## How It Works

This application uses **yt-dlp** as the sole method for downloading and converting YouTube videos to MP3. yt-dlp is a reliable, open-source tool that:

- Handles YouTube's changing formats automatically
- Provides high-quality audio extraction
- Works without external APIs for downloading
- Includes built-in ffmpeg integration

## Project Structure

- `mp3_downloader.py` - Main downloader class with CLI interface
- `main.py` - Interactive mode with YouTube search
- `CallYoutube.py` - YouTube search functionality
- `config.py` - Configuration file for customizing behavior
- `test_simple_downloader.py` - Test suite
- `requirements.txt` - Python dependencies
