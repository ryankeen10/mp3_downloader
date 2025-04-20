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
            for key, value in song_menu.get_album_data(artist).items():
                print(f"\t{key}: {value['name']}")
            selection_nums = input(
                "\nSelect the album numbers you want to download, separated by commas: "
            )
            selection_nums = selection_nums.split(",")
            selection_nums = [
                num.strip() for num in selection_nums if num.strip().isdigit()
            ]
            pprint(selection_nums)
            # for num in selection_nums:
            #     num = num.strip()
            #     if num.isdigit() and int(num) in song_menu.get_album_data(artist):
            #         download_list.append(song_menu.get_album_data(artist)[int(num)]["id"])
            #     else:
            #         print(f"Invalid selection: {num}")

        elif choice == "2":
            track_list = []

            for album in song_menu.get_album_data(artist).values():
                track_list.extend(album.get("tracks", []))
            track_list_sorted = sorted(set(track_list))
            print(f"\nSearching for songs by {artist}..\n")
            print("Song list:")
            for index, value in enumerate(track_list_sorted):
                print(f"\t{index + 1}: {value}")
            selection_nums = input(
                "\nSelect the song numbers you want to download, separated by commas: "
            )
            selection_nums = selection_nums.split(",")
            selection_nums = [
                num.strip() for num in selection_nums if num.strip().isdigit()
            ]
            pprint(selection_nums)
            # Next time, create a list input and return the details of the selection
        else:
            print("Please enter 1 or 2.")
