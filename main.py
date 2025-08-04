from ProcessInput import process_input
from CallYoutube import CallYoutube
from mp3_downloader import MP3Downloader
from credentials_helper import check_credentials

if __name__ == "__main__":
    print("🎵 YouTube to MP3 Downloader")
    print("=" * 40)
    
    # Check credentials before starting
    if not check_credentials():
        print("\n🔧 Please set up your API credentials first!")
        print("📖 See SETUP.md for instructions")
        exit(1)
    
    print("This program lets you search for artists, albums, and songs, then find them on YouTube and convert them to MP3.")
    
    # Get user selections for artist and songs
    processor = process_input()
    search_dict = processor.start()
    
    if search_dict:
        # Initialize YouTube searcher with the search dictionary
        youtube_searcher = CallYoutube(search_dict)
        
        # Process all songs (this now includes user confirmation)
        results = youtube_searcher.process_songs(download=False)  # Just get URLs for now
        
        if results:
            # Use the new MP3 downloader
            downloader = MP3Downloader()
            
            print(f"\n🎵 Starting download of {len(results)} songs...")
            
            # Ask if all songs are from the same album
            album_name = None
            if len(results) > 1:
                same_album = input("Are all these songs from the same album? (y/n): ").lower() in ['y', 'yes']
                if same_album:
                    album_name = input("Enter the album name: ").strip()
                    album_name = album_name if album_name else None
            
            # Prepare download list with Spotify metadata
            download_list = []
            for urls, artist, song, spotify_metadata in results:
                if urls:  # If we found a YouTube URL
                    # Use album from Spotify metadata if available, otherwise use user input
                    song_album = spotify_metadata.get('album') or album_name
                    download_list.append((urls[0], artist, song, song_album, spotify_metadata))
            
            if download_list:
                downloaded_files = downloader.download_multiple_with_metadata(download_list)
                print(f"\n🎉 Downloaded {len(downloaded_files)} MP3 files successfully!")
                print("🏷️  Files enhanced with Spotify metadata!")
            else:
                print("❌ No valid YouTube URLs found for download")
        
        # Display final results
        if results:
            print("\n📋 Summary of results:")
            for i, (urls, artist, song, spotify_metadata) in enumerate(results, 1):
                if urls:
                    album_info = f" (Album: {spotify_metadata.get('album')})" if spotify_metadata.get('album') else ""
                    print(f"{i}. {artist} - {song}{album_info}: ✅ Found")
                else:
                    print(f"{i}. {artist} - {song}: ❌ No video found")
            
            print("\n💿 MP3 files have been saved to the 'downloads' folder.")
        else:
            print("❌ No YouTube videos were found or the process was canceled.")
    else:
        print("❌ No search criteria provided. Exiting.")
