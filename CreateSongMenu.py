from pprint import pprint

import InputHandler
from spotify_credentials import sp


class CreateSongMenu:

    def get_albums_by_artist(self, artist_name):
        offset = 0
        limit = 50
        iteration = 1

        # Step 1: Search for the artist to get their Spotify ID
        artist_results = sp.search(q="artist:" + artist_name, type="artist", limit=1)
        items = artist_results["artists"]["items"]

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
                # break

            for album in albums:
                # Ensure artist is the primary artist (first listed)
                if (
                    album["album_type"] != "compilation"
                    and album["artists"]
                    and album["artists"][0]["id"] == artist_id
                ):
                    album_dict[album["id"]] = {
                        "id": album["id"],
                        "name": album["name"],
                        "release_date": album["release_date"],
                    }

            if (len(album_dict)) == (limit * iteration):
                offset = limit * iteration
                iteration += 1
            else:
                break

        sorted_dict = sorted(album_dict.items(), key=lambda x: x[1]["release_date"])
        final_dict = {i + 1: value[1] for i, value in enumerate(sorted_dict)}
        return final_dict

    def get_songs_by_artist(self, artist_name):
        album_dict = self.get_albums_by_artist(artist_name)
        track_set = set()
        for value in album_dict.values():
            album_id = value["id"]
            tracks = sp.album_tracks(album_id=album_id)
            for track in tracks["items"]:
                track_set.add(track["name"])

        sorted_track_list = sorted(list(track_set))
        track_dict = {i + 1: track for i, track in enumerate(sorted_track_list)}
        return track_dict
