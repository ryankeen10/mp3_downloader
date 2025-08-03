class InputHandler:
    def get_artist():
        print("\nAt any prompt, type 'back' or 'b' to return to the previous step.")
        return input("What artist would you like to search for? ")

    def album_or_song():
        return input(
            "\nWould you like to search for \n\t1. album\n\t2. song\n(Enter 1 or 2, or 'back' to select a different artist): "
        )
    
    def select_from_list(prompt, max_num):
        """Generic function to handle selection with back option"""
        while True:
            selection = input(prompt + " (or 'back'/'b' to go back): ")
            
            # Check for back command
            if selection.lower() in ['back', 'b']:
                return 'back'
                
            # Check for valid number
            try:
                num = int(selection)
                if 1 <= num <= max_num:
                    return num
                else:
                    print(f"Please enter a number between 1 and {max_num}.")
            except ValueError:
                print("Please enter a valid number or 'back'.")
    
    def confirm_artist(artist_name):
        confirmation = input(f"You entered '{artist_name}'. Is this correct? (y/n): ").lower()
        return confirmation == 'y' or confirmation == 'yes'

    # def get_path():
    #     return input("Please enter the folder path you want to save the files to: ")
