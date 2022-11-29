#!/usr/bin/python3
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative,ugc-image-upload"

client_id = input('Enter Client ID: ')
client_secret = input('Enter Client Secret: ')

client_id = client_id if client_id else os.environ.get('SPOTIPY_CLIENT_ID', client_id)
client_secret = client_secret if client_secret else os.environ.get('SPOTIPY_CLIENT_SECRET', client_secret)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=rf'data/{os.getenv("USER")}_token.txt', client_id=client_id, client_secret=client_secret, redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))

print('Logged in as: ' + spotify.me()['display_name'])

print(spotify.current_user_saved_tracks())
