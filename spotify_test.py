import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state"
))

current = sp.current_playback()

if current and current['is_playing']:
    track = current['item']
    print("Música:", track['name'])
    print("Artista:", track['artists'][0]['name'])
    print("Tempo:", current['progress_ms'])
else:
    print("Nada tocando")
