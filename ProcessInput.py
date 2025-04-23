from pprint import pprint

import CreateSongMenu
import InputHandler


class process_input:
    def start(self):
        song_menu = CreateSongMenu.CreateSongMenu()
        artist = InputHandler.InputHandler.get_artist()
        choice = InputHandler.InputHandler.album_or_song()

        if choice == "1":
            # Search by album
            print(f"\nSearching for albums by {artist}...\n")
            print("Album list:")

            # Initialize a dictionary to hold album data
            album_dict = {}

            # Add each item in the album data to the dictionary and print items
            for key, value in song_menu.get_album_data(artist).items():
                print(f"\t{key}: {value['name']}")
                album_dict[key] = value
                # print(album_dict[key]["tracks"])

            # Get user input for album selection and process it
            selection_nums = input(
                "\nSelect the album numbers you want to download, separated by commas: "
            )
            selection_nums = selection_nums.split(",")
            selection_nums = [
                num.strip() for num in selection_nums if num.strip().isdigit()
            ]
            album_list = [
                album_dict[int(num)] for num in selection_nums if int(num) in album_dict
            ]

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
            search_dict = {"artist": artist, "songs": song_list}

        elif choice == "2":
            # Search by song
            print(f"\nSearching for songs by {artist}..\n")
            print("Song list:")

            # Get a list of all tracks from the artist's albums
            track_list = []
            for album in song_menu.get_album_data(artist).values():
                track_list.extend(album.get("tracks", []))
            track_list_sorted = sorted(set(track_list))

            # Put songs into dictionary and print items
            song_dict = {}
            for index, value in enumerate(track_list_sorted):
                print(f"\t{index + 1}: {value}")
                song_dict[index + 1] = value

            # Get user input for song selection and process it
            selection_nums = input(
                "\nSelect the song numbers you want to download, separated by commas: "
            )
            selection_nums = selection_nums.split(",")
            selection_nums = [
                num.strip() for num in selection_nums if num.strip().isdigit()
            ]
            song_list = [
                song_dict[int(num)] for num in selection_nums if int(num) in song_dict
            ]

            # Display the selected songs
            print("Attempting to download the following songs:")
            for song in song_list:
                print(f"\t{song}")

            # Create a dictionary with song info which will be passed to the downloader
            search_dict = {"artist": artist, "songs": song_list}

        else:
            print("Please enter 1 or 2.")

        return search_dict
