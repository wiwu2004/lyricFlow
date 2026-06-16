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


def get_musica_atual():
    current = sp.current_playback()

    if not current or not current.get("item"):
        return None

    nome = current["item"]["name"]
    artista = current["item"]["artists"][0]["name"]
    progress_ms = current["progress_ms"]

    return {
        "nome": nome,
        "artista": artista,
        "tempo": progress_ms / 1000
    }
