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
            results = self.sp.artist_albums(
                artist_id=artist_id,
                limit=limit,
                offset=offset,
            )

            albums = results["items"]
            if not albums:
                print(f"No albums found for: {artist_name}")
                break

        while True:
            results = self.sp.artist_albums(
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
                    tracks = self.sp.album_tracks(album_id=album["id"])["items"]
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
            results = self.sp.artist_albums(
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
                    tracks = self.sp.album_tracks(album_id=album["id"])["items"]
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
        print(f"🔍 Searching for artist: {artist_name}")
        
        # Try different search strategies for better relevance
        all_items = []
        search_strategies = [
            f'artist:"{artist_name}"',  # Exact artist name match
            f'artist:{artist_name}',    # Artist name match
            f'"{artist_name}"',         # Quoted exact match
            artist_name                 # Basic search as fallback
        ]
        
        seen_ids = set()
        for strategy in search_strategies:
            try:
                results = self.sp.search(q=strategy, type="artist", limit=10)
                items = results["artists"]["items"]
                
                for item in items:
                    if item["id"] not in seen_ids:
                        # Only include if the artist name actually contains our search term
                        # This filters out irrelevant results like "Morgan Wallen" when searching "SZA"
                        if self._is_relevant_match(item["name"], artist_name):
                            all_items.append(item)
                            seen_ids.add(item["id"])
                
                # If we found good exact matches, don't need broader searches
                if len(all_items) >= 5 and strategy.startswith('artist:"'):
                    break
                    
            except Exception as e:
                print(f"Search strategy '{strategy}' failed: {e}")
                continue
        
        # Sort by relevance score (combination of name similarity and popularity)
        all_items = sorted(all_items, key=lambda x: self._calculate_relevance_score(x, artist_name), reverse=True)
        
        # Limit to top 10 most relevant results
        items = all_items[:10]
        
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
            artist_results = self.sp.search(q="artist:" + artist_name, type="artist", limit=1)
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
            results = self.sp.artist_albums(
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
                album_tracks = self.sp.album_tracks(album['id'])
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
    
    def _is_relevant_match(self, artist_name, search_term):
        """
        Check if an artist name is relevant to the search term.
        Filters out completely unrelated artists.
        """
        artist_lower = artist_name.lower()
        search_lower = search_term.lower()
        
        # Exact match
        if artist_lower == search_lower:
            return True
        
        # Artist name starts with search term
        if artist_lower.startswith(search_lower):
            return True
        
        # Search term is contained in artist name
        if search_lower in artist_lower:
            return True
        
        # Check if any word in artist name starts with search term
        artist_words = artist_lower.split()
        for word in artist_words:
            if word.startswith(search_lower):
                return True
        
        # For very short search terms (like "SZA"), be more strict
        if len(search_term) <= 3:
            # Only allow if search term appears as a complete word or at start of word
            return search_lower in artist_words or any(word.startswith(search_lower) for word in artist_words)
        
        return False
    
    def _calculate_relevance_score(self, artist, search_term):
        """
        Calculate a relevance score for an artist based on name similarity and popularity.
        Higher score = more relevant.
        """
        artist_name = artist['name'].lower()
        search_lower = search_term.lower()
        popularity = artist.get('popularity', 0)
        
        score = 0
        
        # Exact match gets highest score
        if artist_name == search_lower:
            score += 1000
        
        # Starts with search term
        elif artist_name.startswith(search_lower):
            score += 500
        
        # Contains search term
        elif search_lower in artist_name:
            score += 200
        
        # Word starts with search term
        elif any(word.startswith(search_lower) for word in artist_name.split()):
            score += 100
        
        # Add popularity bonus (scaled down so it doesn't override relevance)
        score += popularity / 10
        
        # Penalty for very long names that don't closely match (likely irrelevant)
        if len(artist_name) > len(search_term) * 3:
            score -= 50
        
        return score