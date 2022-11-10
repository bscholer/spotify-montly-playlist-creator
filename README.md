# Spotify Tools 🤖

A collection of tools for automating Spotify playlist tasks

## Period Playlists

Period playlists are playlists that are created on a regular basis, and are populated with songs from your liked
songs. You can then specify how often new playlists are created, and how many songs are added to the playlist. 

Period options are:

* `daily`
* `weekly`
* `monthly`
* `yearly`

Playlist names can be customized with [`{date injections}`](/example/#date-injections) and an [`|alliteration|`](#alliterations), resulting in depressing names like "22 Anxious April".

The aim is to allow as much customization as possible, so you can **specify the playlist name**, **description**, **date key**, and even the **alliteration word list**.

## Running

### Prerequisites
* Docker
* Python

### Generate a Spotify API token

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Create a new application
3. Click "Edit Settings" and add `http://localhost:8080` to the "Redirect URIs" list
4. Click "Show Client Secret" and copy the value
5. Click "Copy" to copy the Client ID
6. Run `python3 generate_token.py` and paste the Client ID and Client Secret when prompted
7. Follow the link in the output and paste the code when prompted