#!/usr/bin/python3
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main():
    scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative,ugc-image-upload"

    if os.path.exists('data/token.txt'):
        print('Token exists')
        return

    client_id = input('Enter Client ID: ')
    client_secret = input('Enter Client Secret: ')

    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=r'data/token.txt', client_id=client_id,
                                                        client_secret=client_secret,
                                                        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))

    print('Logged in as: ' + spotify.me()['display_name'])

    print("#### Top 10 Saved Tracks ####")
    results = spotify.current_user_saved_tracks(limit=10)
    print(results)


if __name__ == '__main__':
    main()
