from pprint import pprint

import InputHandler
from spotify_credentials import sp


class CreateSongMenu:

    def get_songs_by_artist(self, artist_name):
        results = sp.search(q="artist:" + artist_name, type="track", limit=50)

        # Print song details
        # pprint(results["tracks"]["items"])
        for idx, track in enumerate(
            sorted(results["tracks"]["items"], key=lambda x: x["name"])
        ):
            if track["name"] is not None:
                print(f"{idx+1}. {track['name']}")
        # Add code that will make another api call if there are more than 50 songs
        return ""

    def get_albums_by_artist(self, artist_name):
        results = sp.search(q="artist:" + artist_name, type="album", limit=50)
        pprint(results["albums"]["items"])

        # Print album details
        for idx, album in enumerate(
            sorted(results["albums"]["items"], key=lambda x: x["release_date"])
        ):
            print(f"{idx+1}. {album['name']}")
        # Add code that will make another api call if there are more than 50 albums
        return ""
