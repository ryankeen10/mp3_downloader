from pprint import pprint

import CreateSongMenu
import InputHandler


class Run:
    def start(self):
        song_menu = CreateSongMenu.CreateSongMenu()
        artist = InputHandler.InputHandler.get_artist()
        choice = InputHandler.InputHandler.album_or_song()

        download_list = []
        if choice == "1":
            print(f"\nSearching for albums by {artist}...\n")
            print("Album list:")
            album_dict = {}
            for key, value in song_menu.get_album_data(artist).items():
                print(f"\t{key}: {value['name']}")
                album_dict[key] = value["name"]
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
            print("Attempting to download the following albums:")
            for album in album_list:
                print(f"\t{album}")
            # search_dict = {"artist": artist, "songs": album_list}

        elif choice == "2":
            track_list = []

            for album in song_menu.get_album_data(artist).values():
                track_list.extend(album.get("tracks", []))

            track_list_sorted = sorted(set(track_list))

            print(f"\nSearching for songs by {artist}..\n")
            print("Song list:")
            song_dict = {}
            for index, value in enumerate(track_list_sorted):
                print(f"\t{index + 1}: {value}")
                song_dict[index + 1] = value
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
            print("Attempting to download the following songs:")
            for song in song_list:
                print(f"\t{song}")
            search_dict = {"artist": artist, "songs": song_list}

        else:
            print("Please enter 1 or 2.")
