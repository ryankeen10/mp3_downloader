from pprint import pprint

import CreateSongMenu
import InputHandler


class Run:
    def start(self):
        song_menu = CreateSongMenu.CreateSongMenu()
        artist = InputHandler.InputHandler.get_artist()
        choice = InputHandler.InputHandler.album_or_song()
        if choice == "1":
            print(f"Searching for albums by {artist}...\t")
            print("Album list: \t")
            for key, value in song_menu.get_albums_by_artist(artist).items():
                print(f"{key}: {value['name']}")
            input("Select an album number: ")

        elif choice == "2":
            print(f"Searching for songs by {artist}...")
            pprint(song_menu.get_songs_by_artist(artist))
            # Add code to search for songs
        else:
            print("Please enter 1 or 2.")
