import base64
import datetime
import os
import random
import re
from typing import List

import pandas as pd
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from config import load_config, Config
from date_injection import DateInjection

load_dotenv()

# https://englishstudyhere.com/grammar/adjectives/150-most-common-adjectives/

REQUEST_SIZE = 50
ONLY_PROCESS_CURRENT_MONTH = os.getenv('ONLY_PROCESS_CURRENT_MONTH', 'false').lower() == 'true'
scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative,ugc-image-upload"

try:
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=scope, cache_path=r'data/token.txt', client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                  client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                  redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))
except:
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=scope, cache_path=r'/data/token.txt', client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                  client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                  redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))

user_id = spotify.current_user()['id']
print("Logged in as " + spotify.me()['display_name'])


def get_saved_tracks(full_query=False):
    print('Getting {} saved tracks'.format('all' if full_query else 'first {} tracks'.format(REQUEST_SIZE)))
    results = spotify.current_user_saved_tracks(limit=REQUEST_SIZE)
    tracks = results['items']
    if full_query:
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])

    df = pd.DataFrame(tracks)
    # group df by added_at by month
    df['added_at'] = pd.to_datetime(df['added_at'])
    df['added_at'] = df['added_at'].apply(lambda x: x.replace(tzinfo=None))
    df['year_month'] = df['added_at'].dt.to_period('M')
    df['year_month'] = df['year_month'].astype(str)
    return df


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


def get_all_playlists():
    results = spotify.current_user_playlists(limit=REQUEST_SIZE)
    playlists = results['items']
    while results['next']:
        results = spotify.next(results)
        playlists.extend(results['items'])
    return playlists


def get_playlist_tracks(playlist_id):
    results = spotify.playlist_items(playlist_id, limit=REQUEST_SIZE)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks


def load_and_filter_playlists(word_list):
    playlists = get_all_playlists()
    # remove duplicate fun words from the word list
    for playlist in playlists:
        if re.match(r'.+📆\d{4}-\d{2}', playlist['description']):
            # get the fun word with \s([A-Za-z-]+)\s
            fun_word = re.search(r'\s([A-Za-z-]+)\s', playlist['name']).group(1)
            if fun_word in word_list:
                word_list.remove(fun_word)
    playlist_names = [playlist['name'] for playlist in playlists]
    playlist_descriptions = [playlist['description'] for playlist in playlists]


def get_description_key(year_month):
    return f"📆{year_month}"


def make_description(year_month):
    return f"🤖 generated playlist for {get_description_key(year_month)}"


# delete YYYY-MM playlists
def delete_playlists():
    for playlist in playlists:
        if re.match(r'.+📆\d{4}-\d{2}', playlist['description']):
            print(f"Deleting playlist {playlist['name']}")
            spotify.current_user_unfollow_playlist(playlist_id=playlist['id'])


def make_creative_name(month, year, word_list):
    # print(f"Making creative name for {month} {year}")
    # find a random word from the list whose first letter is the same as the first letter of the month
    filtered_word_list = [word for word in word_list if word[0] == month.lower()[0]]
    # print(f"Filtered word list: {filtered_word_list}")
    random_word = random.choice(filtered_word_list)
    # remove the word from the list, so it can't be used again
    word_list.remove(random_word)
    return f'{year[2:4]} {random_word.capitalize()} {month}'
    # return f'{word} {month}'


# Gets the ID of an existing playlist based on name, or creates a new playlist if it doesn't exist
def get_playlist_id_by_key(year_month=''):
    month = datetime.datetime.strptime(year_month, '%Y-%m').strftime('%B')
    description = make_description(year_month)
    description_key = get_description_key(year_month)

    for playlist in playlists:
        if description_key in playlist['description']:
            # print(f"Found existing playlist {playlist['name']}")
            return playlist['id']


    name = make_creative_name(month, year_month)
    playlist = spotify.user_playlist_create(user=user_id, name=name, public=True, collaborative=False,
                                            description=description)
    print(f'Created playlist {name}')
    return playlist['id']
    # else:
    #     print(f"Playlist for {year_month} already exists")
    #     return [playlist['id'] for playlist in playlists if playlist['description'] == description][0]


# days of week: 0 = Monday, 6 = Sunday
# backup_playlist("Discover Weekly", "DW <date_here>", "🤖 generated backup playlist for Discover Weekly", 4, False)
def backup_playlist(original_name, backup_name, backup_description, day_of_week, use_cover_image):
    print(f"Backing up playlist {original_name} to {backup_name}")
    # check day of week
    if pd.Timestamp.today().dayofweek != day_of_week:
        print(f"  Today is not day {day_of_week}, skipping backup")
        return
    # get the playlist ID of the original playlist, this is an array but should only have zero or one item
    playlist_id = [playlist['id'] for playlist in playlists if playlist['name'] == original_name]
    if not len(playlist_id):
        return

    playlist_id = playlist_id[0]
    # check if the backup playlist already exists, this is an array but should only have zero or one item
    if len([playlist['id'] for playlist in playlists if playlist['name'] == backup_name]):
        print(f"    Backup playlist {backup_name} already exists")
        return
    new_playlist = spotify.user_playlist_create(user=user_id, name=backup_name, public=False, collaborative=False,
                                                description=backup_description)

    backup_id = new_playlist['id']

    if use_cover_image:
        image = spotify.playlist_cover_image(playlist_id)[0]['url']
        spotify.playlist_upload_cover_image(backup_id, get_as_base64(image))

    print(f"    Created backup playlist {backup_name}")
    # get the tracks from the original playlist
    tracks = get_playlist_tracks(playlist_id)
    # add the tracks to the backup playlist
    spotify.playlist_add_items(backup_id, [track['track']['id'] for track in tracks])

    print(f"    Added {len(tracks)} tracks to backup playlist {backup_name}")


def main():
    config: Config = load_config()
    print(config)

    # find all date injections in the config
    raw_date_injections = re.findall(r'\{(.*?)>(.*?)\}', config.period_playlists[0].playlist_name)

    date_injections: List[DateInjection] = []
    for raw_date_injection in raw_date_injections:
        date_injections.append(DateInjection(date=raw_date_injection[0], formatter=raw_date_injections[1]))
    unique_date_injections = list(set(date_injections))
    print(unique_date_injections)

    print(f"Found {len(date_injections)} date injections, {len(unique_date_injections)} unique")
    parsed = requests.get(
        f"http://localhost:3000/parse-dates/{','.join([date_injection.date for date_injection in unique_date_injections])}/{','.join([date_injection.formatter for date_injection in unique_date_injections])}")
    for i in range(len(date_injections)):
        date_injections[i].parsed = parsed.text.split(',')[i]
    print(date_injections)


    global spotify
    for period_playlist in config.period_playlists:
        load_and_filter_playlists(period_playlist.alliteration_word_list)
    # delete_playlists()
    # playlists = get_all_playlists()
    # playlist_names = [playlist['name'] for playlist in playlists]
    # playlist_descriptions = [playlist['description'] for playlist in playlists]
    # return

    today = pd.Timestamp.today()
    monday = today - pd.Timedelta(days=today.dayofweek)
    dw_name = f'DW {str(monday)[:10]}'
    dw_description = '🤖 generated backup playlist for Discover Weekly'
    backup_playlist("Discover Weekly", dw_name, dw_description, 2, False)

    rr_name = f'RR {str(monday)[:10]}'
    rr_description = '🤖 generated backup playlist for Release Radar'
    backup_playlist("Release Radar", rr_name, rr_description, 2, True)

    # only do a full query if it's in the first 9 minutes of the hour
    # if it runs every 5 minutes, this will only run once per hour
    full_query = False
    if today.minute < 9:
        full_query = True

    tracks_df = get_saved_tracks(full_query)
    if ONLY_PROCESS_CURRENT_MONTH:
        tracks_df = tracks_df[tracks_df['added_at'] >= datetime.datetime.today().replace(day=1)]
    print(f"Found {len(tracks_df)} tracks")

    df_grouped = tracks_df.groupby('year_month')

    # name is YYYY-MM
    total_added = 0
    for name, group in df_grouped:
        group_len = group.shape[0]
        if group_len > 1:
            # make a new playlist if one with name doesn't exist
            playlist_id = get_playlist_id_by_key(year_month=name)

            # get the track ids in the playlist
            playlist_tracks = get_playlist_tracks(playlist_id)
            playlist_track_ids = [track['track']['id'] for track in playlist_tracks]

            # make a list of track ids
            track_ids = [x['id'] for x in group['track'].tolist()]
            # filter out the tracks that are already in the playlist
            track_ids = [track_id for track_id in track_ids if track_id not in playlist_track_ids]
            # remove duplicates
            track_ids = list(set(track_ids))

            if track_ids:
                spotify.playlist_add_items(playlist_id=playlist_id, items=track_ids)
                print(f"Added {len(track_ids)} tracks to {name}")
                total_added += len(track_ids)

    print(f"Added {total_added} tracks to playlists")


if __name__ == '__main__':
    main()
