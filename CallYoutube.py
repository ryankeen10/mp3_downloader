import argparse
from pprint import pprint
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ProcessInput
from credentials_helper import get_youtube_api_key


class CallYoutube:

    YOUTUBE_URL_PREFIX = "https://www.youtube.com/watch?v="
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self, search_dict):
        self.artist = search_dict.get("artist", "")
        self.songs = search_dict.get("songs", [])
        self.is_album_download = search_dict.get("is_album_download", False)  # Track if this is an album download
        
        # Get API key safely
        api_key = get_youtube_api_key()
        if not api_key:
            raise ValueError("YouTube API key not available. Please check your credentials.")
        
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=api_key,
        )

    def search_youtube(self, artist, song) -> tuple:
        """Search YouTube for a specific artist and song"""
        url_list = []

        # Call the search.list method to retrieve results matching the specified query term.
        search_response = (
            self.youtube.search().list(q=f"{artist} - {song}", part="snippet").execute()
        )
        response_items = search_response.get("items", [])

        for item in response_items:
            if item["id"]["kind"] == "youtube#video":
                # Print the title and video ID of each search result
                title = item["snippet"]["title"]
                video_id = item["id"].get("videoId")
                if video_id:
                    print(f"Title: {title}, Video ID: {video_id}")
                    url = f"{self.YOUTUBE_URL_PREFIX}{video_id}"
                    url_list.append(url)
                    break

        return url_list, artist, song
    
    def process_songs(self, download=True):
        """
        Process all songs in the search_dict and find YouTube URLs
        
        Args:
            download (bool): Deprecated - downloading is now handled separately
            
        Returns:
            list: List of tuples (urls, artist, song_name, spotify_metadata)
        """
        if not self.songs:
            print("No songs to process.")
            return []
        
        # Ask once for the entire batch at the beginning
        print(f"\n📋 Ready to process {len(self.songs)} song(s):")
        for i, song_data in enumerate(self.songs, 1):
            if isinstance(song_data, str):
                song_name = song_data
            else:
                song_name = song_data.get('name', song_data)
            print(f"  {i}. {song_name}")
        
        proceed = input(f"\nDo you want to download all {len(self.songs)} song(s)? (y/n): ").lower()
        if proceed != 'y' and proceed != 'yes':
            print("Download cancelled.")
            return []
        
        print(f"\n🚀 Starting batch download of {len(self.songs)} song(s)...")
        
        results = []
        print(f"\n🔍 Searching YouTube for {len(self.songs)} songs by {self.artist}...")
        
        for i, song_data in enumerate(self.songs, 1):
            # Handle both old string format and new metadata format
            if isinstance(song_data, str):
                song_name = song_data
                spotify_metadata = {}
            else:
                song_name = song_data.get('name', song_data)
                spotify_metadata = {
                    'album': song_data.get('album'),
                    'release_date': song_data.get('release_date'),
                    'spotify_id': song_data.get('spotify_id'),
                    'album_id': song_data.get('album_id')
                }
            
            print(f"\n📋 Processing song {i}/{len(self.songs)}: {song_name}")
            urls, artist, _ = self.search_youtube(self.artist, song_name)
            results.append((urls, artist, song_name, spotify_metadata))
            
            if urls:
                print(f"✅ Found: {urls[0]}")
            else:
                print("❌ No video found")
        
        print(f"\n✅ Batch processing complete! Found videos for {sum(1 for r in results if r[0])} out of {len(results)} songs.")
        return results


if __name__ == "__main__":
    # Initialize the ProcessInput class
    processor = ProcessInput.process_input()
    
    # Get user selections
    search_dict = processor.start()
    
    if search_dict:
        # Initialize YouTube searcher with the search dictionary
        youtube_searcher = CallYoutube(search_dict)
        
        # Ask user if they want to download MP3s
        download_mp3 = input("\nDo you want to download MP3s for these songs? (y/n): ").lower() in ['y', 'yes']
        
        # Process all songs
        results = youtube_searcher.process_songs(download=download_mp3)
        
        # Display final results
        if results:
            print("\nSummary of YouTube search results:")
            for i, (urls, artist, song) in enumerate(results, 1):
                if urls:
                    print(f"{i}. {artist} - {song}: {urls[0]}")
                else:
                    print(f"{i}. {artist} - {song}: No video found")
        else:
            print("No YouTube videos were found or the process was canceled.")
    else:
        print("No search criteria provided. Exiting.")
