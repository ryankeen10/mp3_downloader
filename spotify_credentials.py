import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "8e4cb6d057a14ebdafea5f2c48d6d48f"
CLIENT_SECRET = "2eaabe2b06d54e6bb3e4c963c9ef534b"

# Set up the client credentials manager to authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
