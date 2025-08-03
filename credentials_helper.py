"""
Safe credential loading with fallbacks
Handles missing credentials gracefully and provides helpful error messages
"""

import os
import sys

def get_youtube_api_key():
    """Safely get YouTube API key from environment or credentials file"""
    # Try environment variable first
    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key:
        return api_key
    
    # Try credentials file
    try:
        from youtube_credentials import YOUTUBE_API_KEY
        return YOUTUBE_API_KEY
    except ImportError:
        print("⚠️  YouTube credentials not found!")
        print("📝 Please copy youtube_credentials.py.template to youtube_credentials.py")
        print("🔑 And add your YouTube API key")
        print("📖 See SETUP.md for detailed instructions")
        return None

def get_spotify_credentials():
    """Safely get Spotify credentials from environment or credentials file"""
    # Try environment variables first
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if client_id and client_secret:
        return client_id, client_secret
    
    # Try credentials file
    try:
        from spotify_credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
        return SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
    except ImportError:
        print("⚠️  Spotify credentials not found!")
        print("📝 Please copy spotify_credentials.py.template to spotify_credentials.py")
        print("🔑 And add your Spotify credentials")
        print("📖 See SETUP.md for detailed instructions")
        return None, None

def check_credentials():
    """Check if all credentials are available"""
    youtube_key = get_youtube_api_key()
    spotify_id, spotify_secret = get_spotify_credentials()
    
    missing_creds = []
    
    if not youtube_key:
        missing_creds.append("YouTube API")
    
    if not spotify_id or not spotify_secret:
        missing_creds.append("Spotify API")
    
    if missing_creds:
        print(f"❌ Missing credentials: {', '.join(missing_creds)}")
        print("🔧 Please set up your API credentials first!")
        print("📖 See SETUP.md for instructions")
        return False
    
    print("✅ All credentials configured!")
    return True

def get_credentials_status():
    """Get detailed status of all credentials"""
    youtube_key = get_youtube_api_key()
    spotify_id, spotify_secret = get_spotify_credentials()
    
    status = {
        'youtube': youtube_key is not None,
        'spotify': spotify_id is not None and spotify_secret is not None,
        'all_ready': youtube_key is not None and spotify_id is not None and spotify_secret is not None
    }
    
    return status
