from pprint import pprint

import CreateSongMenu
import InputHandler


class process_input:
    def start(self):
        try:
            song_menu = CreateSongMenu.CreateSongMenu()
        except ValueError as e:
            print(f"❌ Error initializing Spotify: {e}")
            return None
        
        while True:  # Main loop for the entire process
            # Get artist name input
            artist_input = InputHandler.InputHandler.get_artist()
            
            # Check if user wants to exit
            if artist_input.lower() in ['exit', 'quit', 'q']:
                print("Exiting program.")
                return None
            
            # Loop for artist selection
            while True:
                # Select the correct artist from search results
                artist_info = song_menu.select_artist(artist_input)
                
                # If user selected "back", go back to artist input
                if not artist_info:
                    break
                
                # After artist is selected, ask for album or song preference
                choice = InputHandler.InputHandler.album_or_song()
                
                # Check if user wants to go back to artist selection
                if choice.lower() in ['back', 'b']:
                    continue
                
                # Process album choice
                if choice == "1":
                    # Search by album
                    print(f"\nSearching for albums by {artist_info['name']}...\n")
                    print("Album list:")
                    
                    # Initialize a dictionary to hold album data
                    album_dict = {}
                    
                    # Add each item in the album data to the dictionary and print items
                    for key, value in song_menu.get_album_data(artist_info).items():
                        print(f"\t{key}: {value['name']}")
                        album_dict[key] = value
                    
                    if not album_dict:
                        print("No albums found. Please try a different artist.")
                        break
                    
                    # Get user input for album selection
                    selection_input = input("\nSelect the album numbers you want to download, separated by commas (or 'back' to go back): ")
                    
                    # Check if user wants to go back
                    if selection_input.lower() in ['back', 'b']:
                        continue
                    
                    # Process album selection
                    selection_nums = selection_input.split(",")
                    selection_nums = [num.strip() for num in selection_nums if num.strip().isdigit()]
                    album_list = [album_dict[int(num)] for num in selection_nums if int(num) in album_dict]
                    
                    if not album_list:
                        print("No valid albums selected. Please try again.")
                        continue
                    
                    # Create a list of selected songs with their album metadata
                    selected_songs_with_metadata = []
                    for value in album_dict.values():
                        if value in album_list:
                            for track_name in value["tracks"]:
                                selected_songs_with_metadata.append({
                                    'name': track_name,
                                    'album': value['name'],
                                    'release_date': value['release_date'],
                                    'album_id': value['id']
                                })
                    
                    # Remove duplicates based on song name
                    seen_songs = set()
                    unique_songs = []
                    for song in selected_songs_with_metadata:
                        if song['name'] not in seen_songs:
                            unique_songs.append(song)
                            seen_songs.add(song['name'])
                    selected_songs_with_metadata = unique_songs
                    
                    # Display the selected albums
                    print("Attempting to download the following albums:")
                    for album in album_list:
                        print(f"\t{album['name']}")
                    
                    # Create a dictionary with song info including Spotify metadata
                    search_dict = {
                        "artist": artist_info['name'], 
                        "artist_id": artist_info['id'],
                        "songs": selected_songs_with_metadata,
                        "is_album_download": True  # Flag to indicate this is an album download
                    }
                    return search_dict
                
                # Process song choice
                elif choice == "2":
                    # Search by song
                    print(f"\nSearching for songs by {artist_info['name']}..\n")
                    
                    # Get songs directly using the artist info
                    songs_dict = song_menu.get_songs_by_artist(artist_info)
                    
                    if not songs_dict:
                        print("No songs found. Please try a different artist.")
                        break
                    
                    # Get user input for song selection
                    selection_input = input("\nSelect the song numbers you want to download, separated by commas (or 'back' to go back): ")
                    
                    # Check if user wants to go back
                    if selection_input.lower() in ['back', 'b']:
                        continue
                    
                    # Process song selection
                    selection_nums = selection_input.split(",")
                    selection_nums = [num.strip() for num in selection_nums if num.strip().isdigit()]
                    
                    # Collect selected songs with their Spotify metadata
                    selected_songs_with_metadata = []
                    for num in selection_nums:
                        if int(num) in songs_dict:
                            song_data = songs_dict[int(num)]
                            selected_songs_with_metadata.append({
                                'name': song_data['name'],
                                'album': song_data['album'],
                                'release_date': song_data['release_date'],
                                'spotify_id': song_data['id']
                            })
                    
                    if not selected_songs_with_metadata:
                        print("No valid songs selected. Please try again.")
                        continue
                    
                    # Display the selected songs
                    print("Attempting to download the following songs:")
                    for song in selected_songs_with_metadata:
                        print(f"\t{song['name']}")
                    
                    # Create a dictionary with song info including Spotify metadata
                    search_dict = {
                        "artist": artist_info['name'], 
                        "artist_id": artist_info['id'],
                        "songs": selected_songs_with_metadata,
                        "is_album_download": False  # Flag to indicate this is individual song download
                    }
                    return search_dict
                
                else:
                    print("Please enter 1 or 2.")
                    continue
                    
            # End of artist selection loop
