import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=r'C:\Users\bscholer\Documents\Projects\spotify-montly-playlist\data\token.txt'))

print(spotify.current_user_saved_tracks())
