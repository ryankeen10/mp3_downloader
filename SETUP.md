# 🔑 API Setup Instructions

## Required Credentials

Both API credentials are **required** for the application to function properly.

## Setup Methods

### Docker Setup (Recommended)

If using Docker, you only need to create the credential files in your project directory:

```bash
# Copy template files
cp youtube_credentials.py.template youtube_credentials.py
cp spotify_credentials.py.template spotify_credentials.py

# Edit the files with your API keys
nano youtube_credentials.py
nano spotify_credentials.py
```

Docker will automatically mount these files and handle all dependencies for you!

### Local Python Setup

For local installation without Docker:

### YouTube Data API (Required)
**Without this, the app cannot search for videos and will not work.**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Go to Credentials → Create Credentials → API Key
5. Copy `youtube_credentials.py.template` to `youtube_credentials.py`
6. Replace `your_youtube_api_key_here` with your actual API key

### Spotify API (Required)
**Without this, the app cannot search for artists/albums and will not work.**

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Log in and create an app
3. Copy Client ID and Client Secret
4. Copy `spotify_credentials.py.template` to `spotify_credentials.py`
5. Replace the placeholder values with your actual credentials

## Quick Setup Commands

```bash
# Copy template files
cp youtube_credentials.py.template youtube_credentials.py
cp spotify_credentials.py.template spotify_credentials.py

# Edit the files with your API keys
nano youtube_credentials.py
nano spotify_credentials.py
```

## Verification

### Docker
```bash
docker-compose up
```
If you see the search menu, APIs are working!

### Local Python
```bash
python main.py
```
If you see the search menu, APIs are working!

## Alternative: Environment Variables
You can also set credentials as environment variables:
```bash
export YOUTUBE_API_KEY="your_key_here"
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```
