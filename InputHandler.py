class InputHandler:
    def get_artist():
        return input("What artist would you like to search for? ").lower()

    def album_or_song():
        return input(
            "Would you like to search for \n\t1. album\n\t2. song\n(Enter 1 or 2): "
        ).lower()

    # def get_path():
    #     return input("Please enter the folder path you want to save the files to: ")
