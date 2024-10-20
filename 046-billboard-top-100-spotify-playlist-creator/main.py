from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests
import json

# Enter your own Spotify App's client ID, client secret, and redirect URI.
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""


class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist


def strip_artist_name(artist_name):
    artist_name = artist_name.strip()
    artist_separators = ["Featuring", "With", "&", "X"]

    for separator in artist_separators:
        artist_name = artist_name.split(f" {separator} ")[0]

    return artist_name


date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}
response = requests.get(
    f"https://www.billboard.com/charts/hot-100/{date}", headers=headers
)
soup = BeautifulSoup(response.text, "html.parser")

song_elements = soup.select(".o-chart-results-list__item .c-title")
songs = []

for element in song_elements:
    song_title = element.getText().strip()
    song_artist = strip_artist_name(element.find_next_sibling("span").getText())

    songs.append(Song(song_title, song_artist))

# Copy the URL of the webpage pop-up and paste it into the console.
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private",
    )
)

song_spotify_uris = []

for index, song in enumerate(songs):
    query = f'track:"{song.title}" artist:"{song.artist}"'
    result = sp.search(q=query, type="track")

    print(f"{index + 1}: Searching for {song.title} by {song.artist}...")

    try:
        song_spotify_uris.append(result["tracks"]["items"][0]["uri"])
        print(f"\t{song.title} by {song.artist} found.")
    except:
        print(f"\tERROR: {song.title} by {song.artist} was not found.")

print(f"{len(song_spotify_uris)}/{len(songs)} songs were found.")
playlist_name = f"{date} Billboard 100"

print(f'Creating playlist "{playlist_name}" now...')
user_id = sp.current_user()["id"]
playlist_id = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)[
    "id"
]
sp.playlist_add_items(playlist_id=playlist_id, items=song_spotify_uris)

print(f"Done! The playlist should be added to your profile.")
