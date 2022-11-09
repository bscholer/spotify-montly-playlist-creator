#!/usr/bin/python3
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative,ugc-image-upload"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=r'data/token.txt', client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'), redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))

print('Logged in as: ' + spotify.me()['display_name'])

print(spotify.current_user_saved_tracks())
