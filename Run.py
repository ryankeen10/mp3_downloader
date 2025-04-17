from pprint import pprint

import CreateSongMenu
import InputHandler


class Run:
    def start(self):
        song_menu = CreateSongMenu.CreateSongMenu()
        artist = InputHandler.InputHandler.get_artist()
        choice = InputHandler.InputHandler.album_or_song()
        if choice == "1":
            print(f"\nSearching for albums by {artist}...\n")
            print("Album list:")
            for key, value in song_menu.get_album_data(artist).items():
                print(f"\t{key}: {value['name']}")
            input("\nSelect an album number: ")
            # Next time, create a list input and return the details of the selection

        elif choice == "2":
            track_list = []

            for album in song_menu.get_album_data(artist).values():
                track_list.extend(album.get("tracks", []))
            track_list_sorted = sorted(set(track_list))
            print(f"\nSearching for songs by {artist}..\n")
            print("Song list:")
            for index, value in enumerate(track_list_sorted):
                print(f"\t{index + 1}: {value}")
            input("\nSelect a song number: ")
            # Next time, create a list input and return the details of the selection
        else:
            print("Please enter 1 or 2.")
