import InputHandler


class Run:
    def start(self):
        artist = InputHandler.InputHandler.get_artist()
        choice = InputHandler.InputHandler.album_or_song()
        if choice == "1":
            print(f"Searching for albums by {artist}...")
            # Add code to search for albums
        elif choice == "2":
            print(f"Searching for songs by {artist}...")
            # Add code to search for songs
        else:
            print("Please enter 1 or 2.")
