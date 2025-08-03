from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import InputHandler
from credentials_helper import get_spotify_credentials


class CreateSongMenu:
    youtube_search_dict = {}
    
    def __init__(self):
        # Initialize Spotify client safely
        client_id, client_secret = get_spotify_credentials()
        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not available. Please check your credentials.")
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def call_spotify_api(self, artist_name, offset, limit):
        artist_results = self.sp.search(q="artist:" + artist_name, type="artist", limit=1)
        items = artist_results["artists"]["items"][:3]
        if not items:
            print(f"No artist found for: {artist_name}")
            return []

        print("Select the correct artist:")
        for idx, artist in enumerate(items, 1):
            print(f"{idx}: {artist['name']} (Followers: {artist['followers']['total']}, Genres: {', '.join(artist['genres'])})")

        while True:
            try:
                selection = int(input("Enter the number of the correct artist: "))
                if 1 <= selection <= len(items):
                    break
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a valid number.")

        artist_id = items[selection - 1]["id"]

        if not items:
            print(f"No artist found for: {artist_name}")
            return []

        artist_id = items[0]["id"]
        album_dict = {}

        while True:
            results = sp.artist_albums(
                artist_id=artist_id,
                limit=limit,
                offset=offset,
            )

            albums = results["items"]
            if not albums:
                print(f"No albums found for: {artist_name}")
                break

        while True:
            results = sp.artist_albums(
                artist_id=artist_id,
                limit=limit,
                offset=offset,
            )

            albums = results["items"]
            if not albums:
                print(f"No albums found for: {artist_name}")
                # break

            for album in albums:
                # Ensure artist is the primary artist (first listed)
                if (
                    album["album_type"] != "compilation"
                    and album["artists"]
                    and album["artists"][0]["id"] == artist_id
                ):
                    # Create set of tracks for each record
                    tracks = sp.album_tracks(album_id=album["id"])["items"]
                    track_names = [track["name"] for track in tracks]
                    album_dict[album["id"]] = {
                        "id": album["id"],
                        "name": album["name"],
                        "release_date": album["release_date"],
                        "tracks": track_names,
                    }
            # pprint(album_dict)

            # If the api limit has been reached, call again with new offset
            if (len(album_dict)) == (limit * self.iteration):
                offset = limit * self.iteration
                iteration += 1
            else:
                break

        sorted_dict = sorted(album_dict.items(), key=lambda x: x[1]["release_date"])
        final_dict = {i + 1: value[1] for i, value in enumerate(sorted_dict)}

        return final_dict

    def get_album_data(self, artist_info):
        self.offset = 0
        self.limit = 50
        self.iteration = 1
        
        # Extract artist_id from artist_info
        artist_id = artist_info["id"] if isinstance(artist_info, dict) else None
        
        # If we don't have an ID, get albums using the old method
        if not artist_id:
            input_collected = False
            while not input_collected:
                artist_data = self.call_spotify_api(artist_info, self.offset, self.limit)
                if not artist_data:
                    print("No albums found. Please try a different artist.")
                else:
                    input_collected = True
            return artist_data
            
        # If we have an ID, get albums directly
        album_dict = {}
        
        while True:
            results = sp.artist_albums(
                artist_id=artist_id,
                limit=self.limit,
                offset=self.offset,
            )

            albums = results["items"]
            if not albums:
                break
                
            for album in albums:
                # Ensure artist is the primary artist (first listed)
                if (
                    album["album_type"] != "compilation"
                    and album["artists"]
                    and album["artists"][0]["id"] == artist_id
                ):
                    # Create set of tracks for each record
                    tracks = sp.album_tracks(album_id=album["id"])["items"]
                    track_names = [track["name"] for track in tracks]
                    album_dict[album["id"]] = {
                        "id": album["id"],
                        "name": album["name"],
                        "release_date": album["release_date"],
                        "tracks": track_names,
                    }
            
            # If the api limit has been reached, call again with new offset
            if (len(album_dict)) == (self.limit * self.iteration):
                self.offset = self.limit * self.iteration
                self.iteration += 1
            else:
                break
                
        sorted_dict = sorted(album_dict.items(), key=lambda x: x[1]["release_date"])
        final_dict = {i + 1: value[1] for i, value in enumerate(sorted_dict)}
        
        return final_dict
        
    def select_artist(self, artist_name):
        """
        Displays a list of artists matching the search query and lets the user select one.
        Returns the selected artist name.
        """
        # Search for artists matching the name
        artist_results = sp.search(q="artist:" + artist_name, type="artist", limit=3)
        items = artist_results["artists"]["items"]
        if not items:
            print(f"No artist found for: {artist_name}")
            return None

        print("\nSelect the correct artist:")
        for idx, artist in enumerate(items, 1):
            print(f"{idx}: {artist['name']} (Followers: {artist['followers']['total']}, Genres: {', '.join(artist['genres'])})")

        selection = InputHandler.InputHandler.select_from_list("Enter the number of the correct artist:", len(items))
        
        # If user wants to go back
        if selection == 'back':
            return None

        # Return the selected artist's name and ID
        selected_artist = items[selection - 1]
        return {
            "name": selected_artist["name"],
            "id": selected_artist["id"]
        }
        
    def get_songs_by_artist(self, artist_info):
        # Extract artist ID if a dictionary was passed
        if isinstance(artist_info, dict):
            artist_id = artist_info["id"]
            artist_name = artist_info["name"]
        else:
            # For backward compatibility, search for the artist
            artist_name = artist_info
            artist_results = sp.search(q="artist:" + artist_name, type="artist", limit=1)
            items = artist_results["artists"]["items"]
            if not items:
                print(f"No artist found for: {artist_name}")
                return {}
            artist_id = items[0]["id"]
        
        # Get all albums for the artist
        all_albums = []
        offset = 0
        limit = 50
        
        while True:
            results = sp.artist_albums(
                artist_id=artist_id,
                album_type='album,single',
                limit=limit,
                offset=offset
            )
            
            albums = results['items']
            if not albums:
                break
                
            all_albums.extend(albums)
            
            if len(albums) < limit:
                break
                
            offset += limit
        
        # Get all tracks from all albums
        all_tracks = []
        track_ids = set()  # To prevent duplicates
        
        for album in all_albums:
            # Only include albums where this artist is the primary artist
            if album['artists'] and album['artists'][0]['id'] == artist_id:
                album_tracks = sp.album_tracks(album['id'])
                for track in album_tracks['items']:
                    # Only add if we haven't seen this track ID before
                    if track['id'] not in track_ids:
                        all_tracks.append({
                            'name': track['name'],
                            'id': track['id'],
                            'album': album['name'],
                            'release_date': album.get('release_date', '')
                        })
                        track_ids.add(track['id'])
        
        # Sort tracks by name for better display
        all_tracks.sort(key=lambda x: x['name'])
        
        # Print song list
        print("\nSong list:")
        songs_dict = {}
        for i, track in enumerate(all_tracks, 1):
            print(f"{i}. {track['name']}")
            songs_dict[i] = track
        
        return songs_dict  # Return the songs dictionary for further processing