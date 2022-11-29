import base64
import datetime
import os
import random
import re

import pandas as pd
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# https://englishstudyhere.com/grammar/adjectives/150-most-common-adjectives/
word_list = ['macabre', 'unequaled', 'brawny', 'wicked', 'obscene', 'stupendous', 'spiteful', 'quarrelsome', 'naive',
             'pushy', 'classy', 'crooked', 'obtainable', 'cute', 'highfalutin', 'well-groomed', 'smiling', 'previous',
             'excited', 'black-and-white', 'burly', 'vast', 'tense', 'pleasant', 'wasteful', 'noiseless', 'shallow',
             'available', 'dusty', 'gabby', 'barbarous', 'instinctive', 'wandering', 'merciful', 'cumbersome',
             'omniscient', 'maniacal', 'entertaining', 'exciting', 'relieved', 'grotesque', 'heavy', 'amusing',
             'doubtful', 'daffy', 'upbeat', 'picayune', 'versed', 'tasteless', 'hypnotic', 'furry', 'brown',
             'wholesale', 'well-made', 'roasted', 'petite', 'tiresome', 'gentle', 'full', 'grieving', 'abhorrent',
             'unused', 'ludicrous', 'enchanted', 'hesitant', 'rainy', 'sick', 'raspy', 'strong', 'cut', 'angry',
             'cultured', 'wealthy', 'fine', 'political', 'vulgar', 'awake', 'plucky', 'truthful', 'rampant', 'future',
             'uninterested', 'slippery', 'zippy', 'automatic', 'sad', 'ill-informed', 'obnoxious', 'tangy', 'cool',
             'flashy', 'frail', 'swanky', 'crowded', 'sincere', 'unequal', 'equal', 'cooing', 'aboard', 'whole',
             'godly', 'silent', 'acidic', 'excellent', 'dependent', 'beneficial', 'upset', 'sleepy', 'probable',
             'disagreeable', 'narrow', 'waggish', 'super', 'addicted', 'abrasive', 'silent', 'wiry', 'square',
             'healthy', 'thoughtless', 'skinny', 'new', 'vagabond', 'useful', 'onerous', 'humorous', 'weary',
             'grateful', 'acrid', 'resolute', 'zany', 'diligent', 'hard', 'concerned', 'testy', 'accessible',
             'adjoining', 'tight', 'medical', 'enchanting', 'scarce', 'easy', 'ragged', 'luxuriant', 'greedy', 'odd',
             'steady', 'lavish', 'ten', 'ablaze', 'chilly', 'cloistered', 'invincible', 'longing', 'uptight', 'tenuous',
             'miniature', 'good', 'best', 'ambitious', 'white', 'marvelous', 'breezy', 'trite', 'colossal',
             'harmonious', 'cynical', 'depressed', 'fretful', 'tired', 'recondite', 'selective', 'direful', 'economic',
             'clammy', 'agonizing', 'smelly', 'torpid', 'aquatic', 'safe', 'lame', 'kaput', 'old-fashioned', 'fabulous',
             'wise', 'evasive', 'belligerent', 'famous', 'remarkable', 'powerful', 'abashed', 'fragile', 'subsequent',
             'nippy', 'cruel', 'gray', 'moldy', 'unwieldy', 'tacky', 'breakable', 'anxious', 'fanatical', 'volatile',
             'stupid', 'true', 'determined', 'rebel', 'warm', 'massive', 'unruly', 'exotic', 'jumbled', 'splendid',
             'waiting', 'inexpensive', 'sudden', 'hissing', 'rural', 'combative', 'pumped', 'watery', 'second-hand',
             'fixed', 'historical', 'scary', 'royal', 'endurable', 'spotless', 'common', 'bewildered', 'foamy',
             'deadpan', 'guarded', 'enormous', 'friendly', 'soft', 'dry', 'tranquil', 'statuesque', 'snotty', 'dull',
             'chief', 'hallowed', 'tasteful', 'gruesome', 'giddy', 'hushed', 'gaudy', 'subdued', 'cheerful',
             'hard-to-find', 'black', 'madly', 'bawdy', 'bite-sized', 'innocent', 'premium', 'functional',
             'substantial', 'handy', 'wrathful', 'teeny-tiny', 'simplistic', 'abundant', 'ratty', 'wide', 'boorish',
             'mammoth', 'stormy', 'nimble', 'useless', 'red', 'gratis', 'shiny', 'macho', 'daily', 'melodic', 'warlike',
             'piquant', 'unusual', 'wacky', 'tidy', 'bustling', 'lyrical', 'cautious', 'guttural', 'acoustic', 'cute',
             'curved', 'ugly', 'woebegone', 'righteous', 'irate', 'workable', 'ethereal', 'scientific', 'heartbreaking',
             'mountainous', 'used', 'psychotic', 'pastoral', 'amused', 'broken', 'long', 'modern', 'erect', 'capable',
             'obese', 'astonishing', 'elated', 'cluttered', 'fast', 'scared', 'sore', 'lewd', 'itchy', 'willing',
             'enthusiastic', 'flaky', 'sordid', 'difficult', 'magnificent', 'shocking', 'various', 'gamy', 'proud',
             'unwritten', 'short', 'clean', 'blue', 'aspiring', 'lowly', 'absorbed', 'many', 'big', 'slimy', 'purring',
             'tasty', 'rare', 'industrious', 'graceful', 'wry', 'grouchy', 'plausible', 'cloudy', 'pathetic', 'lively',
             'deep', 'five', 'next', 'dashing', 'windy', 'cagey', 'accurate', 'amazing', 'conscious', 'whimsical',
             'filthy', 'fair', 'supreme', 'aloof', 'lucky', 'eatable', 'soggy', 'erratic', 'simple', 'third', 'labored',
             'violent', 'understood', 'insidious', 'sweltering', 'jealous', 'devilish', 'brief', 'gorgeous', 'ugliest',
             'possessive', 'silky', 'abnormal', 'mushy', 'tense', 'creepy', 'repulsive', 'noisy', 'ripe', 'gigantic',
             'teeny', 'dangerous', 'voracious', 'alluring', 'extra-small', 'sticky', 'shut', 'ill-fated', 'dirty',
             'vengeful', 'afraid', 'grandiose', 'material', 'rustic', 'finicky', 'alcoholic', 'dynamic', 'abortive',
             'elastic', 'strange', 'broad', 'outrageous', 'limping', 'blushing', 'glib', 'nice', 'joyous', 'arrogant',
             'nervous', 'six', 'mixed', 'small', 'embarrassed', 'flat', 'careful', 'ceaseless', 'awful', 'calm',
             'unsightly', 'thin', 'evanescent', 'disillusioned', 'redundant', 'synonymous', 'silly', 'worried',
             'heavenly', 'wide-eyed', 'periodic', 'average', 'towering', 'bouncy', 'solid', 'smoggy', 'unbecoming',
             'glossy', 'quack', 'nutritious', 'aback', 'female', 'dispensable', 'disgusting', 'illustrious', 'half',
             'ignorant', 'first', 'rude', 'eight', 'educated', 'malicious', 'incredible', 'living', 'hilarious',
             'funny', 'loud', 'sneaky', 'discreet', 'eager', 'normal', 'childlike', 'spiky', 'condemned', 'exclusive',
             'resonant', 'great', 'happy', 'yummy', 'ancient', 'private', 'ruthless', 'lamentable', 'weak', 'ashamed',
             'imperfect', 'divergent', 'symptomatic', 'flowery', 'pretty', 'sloppy', 'gleaming', 'jaded', 'knotty',
             'messy', 'hellish', 'lovely', 'handsomely', 'unnatural', 'amuck', 'taboo', 'alert', 'optimal',
             'questionable', 'fantastic', 'witty', 'judicious', 'elderly', 'few', 'halting', 'ajar', 'drunk',
             'yielding', 'groovy', 'wary', 'unhealthy', 'squeamish', 'long-term', 'damp', 'special', 'disgusted',
             'complex', 'right', 'early', 'slow', 'hollow', 'faded', 'whispering', 'even', 'bright', 'past', 'alleged',
             'obsequious', 'habitual', 'billowy', 'glistening', 'victorious', 'stingy', 'delirious', 'gifted',
             'jittery', 'rabid', 'steadfast', 'outstanding', 'defiant', 'unbiased', 'spicy', 'minor', 'laughable',
             'electric', 'feeble', 'open', 'physical', 'disastrous', 'humdrum', 'scattered', 'quizzical', 'poor',
             'secret', 'materialistic', 'alike', 'harsh', 'sable', 'skillful', 'slim', 'separate', 'kind', 'pointless',
             'alive', 'zonked', 'beautiful', 'detailed', 'demonic', 'furtive', 'greasy', 'fertile', 'dramatic',
             'trashy', 'violet', 'obedient', 'moaning', 'huge', 'numberless', 'uneven', 'callous', 'horrible',
             'scintillating', 'puzzling', 'jumpy', 'lethal', 'serious', 'well-to-do', 'deeply', 'last', 'hysterical',
             'present', 'tearful', 'acceptable', 'festive', 'sophisticated', 'lacking', 'two', 'shaky', 'nauseating',
             'ossified', 'tacit', 'adamant', 'somber', 'phobic', 'damaged', 'impartial', 'striped', 'earthy',
             'befitting', 'flagrant', 'motionless', 'same', 'blue-eyed', 'earsplitting', 'penitent', 'hapless',
             'spiritual', 'internal', 'psychedelic', 'poised', 'naughty', 'quiet', 'faithful', 'womanly', 'nondescript',
             'annoying', 'curious', 'cooperative', 'abject', 'shaggy', 'crazy', 'panicky', 'uttermost', 'exuberant',
             'chivalrous', 'meaty', 'worthless', 'young', 'juicy', 'boundless', 'garrulous', 'makeshift', 'puny',
             'likeable', 'wild', 'wonderful', 'cuddly', 'reflective', 'high', 'zesty', 'pale', 'awesome', 'chemical',
             'verdant', 'certain', 'icky', 'glorious', 'changeable', 'peaceful', 'rambunctious', 'charming', 'tart',
             'therapeutic', 'legal', 'ordinary', 'superb', 'jagged', 'unique', 'brainy', 'smooth', 'quick', 'far-flung',
             'organic', 'hateful', 'defective', 'domineering', 'knowing', 'momentous', 'wakeful', 'caring', 'absurd',
             'ambiguous', 'three', 'literate', 'stiff', 'foregoing', 'kindhearted', 'public', 'deranged', 'draconian',
             'salty', 'oafish', 'nonchalant', 'immense', 'quaint', 'frightening', 'forgetful', 'apathetic',
             'delightful', 'wanting', 'icy', 'sulky', 'mundane', 'encouraging', 'obeisant', 'neighborly', 'lying',
             'better', 'decorous', 'flimsy', 'incandescent', 'auspicious', 'deserted', 'uncovered', 'well-off',
             'hanging', 'nasty', 'one', 'spotty', 'melted', 'fresh', 'adventurous', 'perfect', 'aware', 'needy',
             'nifty', 'honorable', 'tall', 'attractive', 'overjoyed', 'energetic', 'shrill', 'nappy', 'miscreant',
             'rhetorical', 'rich', 'fearful', 'paltry', 'ritzy', 'efficacious', 'tested', 'productive', 'overconfident',
             'meek', 'fluttering', 'null', 'prickly', 'elegant', 'handsome', 'milky', 'real', 'imminent', 'fearless',
             'oval', 'painful', 'bashful', 'puffy', 'undesirable', 'helpful', 'lush', 'typical', 'lively', 'nutty',
             'mere', 'disturbed', 'scandalous', 'late', 'foolish', 'bitter', 'agreeable', 'nosy', 'interesting',
             'curvy', 'selfish', 'colorful', 'possible', 'ready', 'responsible', 'frantic', 'aggressive', 'temporary',
             'cold', 'adhesive', 'homely', 'fortunate', 'rapid', 'learned', 'gusty', 'unknown', 'thoughtful', 'elfin',
             'reminiscent', 'outgoing', 'aboriginal', 'ahead', 'marked', 'seemly', 'plastic', 'idiotic', 'hulking',
             'dapper', 'old', 'grey', 'zealous', 'ubiquitous', 'tremendous', 'lumpy', 'knowledgeable', 'mature',
             'obsolete', 'steep', 'faulty', 'bumpy', 'stimulating', 'threatening', 'hideous', 'goofy', 'bad', 'mute',
             'annoyed', 'delicate', 'untidy', 'permissible', 'intelligent', 'abrupt', 'overt', 'hungry', 'rough',
             'bloody', 'tan', 'lean', 'decisive', 'tawdry', 'flawless', 'holistic', 'bizarre', 'tiny', 'imaginary',
             'magical', 'heady', 'quixotic', 'empty', 'thankful', 'languid', 'terrible', 'cowardly', 'irritating',
             'didactic', 'dusty', 'majestic', 'courageous', 'numerous', 'fuzzy', 'hospitable', 'false', 'coordinated',
             'racial', 'abaft', 'quickest', 'inquisitive', 'clever', 'bright', 'clumsy', 'infamous', 'petite', 'like',
             'jolly', 'large', 'mellow', 'tender', 'troubled', 'important', 'abiding', 'scrawny', 'wistful', 'careless',
             'wiggly', 'utopian', 'assorted', 'rightful', 'receptive', 'capricious', 'thinkable', 'loving', 'able',
             'dysfunctional', 'free', 'bent', 'elite', 'protective', 'efficient', 'lonely', 'impolite', 'overwrought',
             'envious', 'homeless', 'nonstop', 'plant', 'precious', 'abstracted', 'ad', 'hoc', 'accidental', 'dark',
             'yellow', 'nostalgic', 'glamorous', 'romantic', 'loutish', 'freezing', 'unable', 'drab', 'tame', 'ultra',
             'impossible', 'deafening', 'straight', 'secretive', 'clear', 'satisfying', 'ill', 'familiar', 'terrific',
             'dead', 'overrated', 'sweet', 'valuable', 'tough', 'aberrant', 'needless', 'voiceless', 'tangible',
             'vivacious', 'absorbing', 'axiomatic', 'lackadaisical', 'painstaking', 'hot', 'squealing', 'gainful',
             'pink', 'imported', 'truculent', 'placid', 'giant', 'profuse', 'exultant', 'stale', 'male', 'brave',
             'animated', 'second', 'squalid', 'curly', 'kindly', 'dear', 'fat', 'thundering', 'frequent', 'shy',
             'screeching', 'gullible', 'polite', 'abandoned', 'measly', 'flippant', 'quirky', 'panoramic', 'debonair',
             'incompetent', 'dizzy', 'futuristic', 'busy', 'inconclusive', 'chunky', 'fancy', 'abounding', 'uppity',
             'juvenile', 'acid', 'parched', 'mindless', 'savory', 'lazy', 'unkempt', 'sore', 'far', 'eminent', 'purple',
             'orange', 'keen', 'complete', 'lopsided', 'parallel', 'robust', 'swift', 'murky', 'pricey', 'unarmed',
             'calculating', 'expensive',
             'Jacketed', 'Jacobean', 'Jaded', 'Jaggy', 'Jamaican', 'Jammed', 'Jangling', 'Jarred', 'Jaunty',
             'Jawed', 'Jealous', 'Jeering', 'Jerky', 'Jestful', 'Jiggish', 'Jocular', 'Jointed', 'Jolly',
             'Journalistic', 'Jovial', 'Joyful', 'Joyless', 'Jubilant', 'Judaic', 'Judge', 'Judgmental', 'Judicial',
             'Jugular', 'Juiceless', 'Junior', 'Jurassic', 'Jurist', 'Just', 'Justifiable', 'Jutting', 'Juvenile']
word_list = [word.lower() for word in word_list]

REQUEST_SIZE = 50
MANUAL_CREATE_PLAYLIST = os.getenv('MANUAL_CREATE_PLAYLIST', False).lower() == 'true'
scope = "user-library-read,playlist-modify-public,playlist-modify-private,playlist-read-private,playlist-read-collaborative,ugc-image-upload"

try:
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=scope, cache_path=rf'/data/{os.getenv("USER")}_token.txt', client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                  client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                  redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI')))
except:
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope=scope, cache_path=rf'data/{os.getenv("USER")}_token.txt', client_id=os.getenv('SPOTIFY_CLIENT_ID'),
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
            # spotify.current_user_unfollow_playlist(playlist_id=playlist['id'])


def make_creative_name(month, year):
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

    if not MANUAL_CREATE_PLAYLIST:
        name = make_creative_name(month, year_month)
        playlist = spotify.user_playlist_create(user=user_id, name=name, public=True, collaborative=False,
                                                description=description)
        print(f'Created playlist {name}')
        return playlist['id']
    else:
        return None
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
    if MANUAL_CREATE_PLAYLIST:
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
            if playlist_id is None:
                continue

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
