from pprint import pprint

import CreateSongMenu
import InputHandler


class process_input:
    def start(self):
        song_menu = CreateSongMenu.CreateSongMenu()
        
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
                    
                    # Create a unique list of the selected songs from the selected albums
                    song_list = []
                    for value in album_dict.values():
                        if value in album_list:
                            song_list.extend(value["tracks"])
                    song_list = list(set(song_list))  # Remove duplicates
                    
                    # Display the selected albums
                    print("Attempting to download the following albums:")
                    for album in album_list:
                        print(f"\t{album['name']}")
                    
                    # Create a dictionary with song info which will be passed to the downloader
                    search_dict = {"artist": artist_info['name'], "songs": song_list}
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
                    song_list = [songs_dict[int(num)]['name'] for num in selection_nums if int(num) in songs_dict]
                    
                    if not song_list:
                        print("No valid songs selected. Please try again.")
                        continue
                    
                    # Display the selected songs
                    print("Attempting to download the following songs:")
                    for song in song_list:
                        print(f"\t{song}")
                    
                    # Create a dictionary with song info which will be passed to the downloader
                    search_dict = {"artist": artist_info['name'], "songs": song_list}
                    return search_dict
                
                else:
                    print("Please enter 1 or 2.")
                    continue
                    
            # End of artist selection loop
