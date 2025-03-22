from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

# ✅ Load .env file for client ID, secret, and redirect URI
load_dotenv()

def get_selected_playlists():
    # ✅ Include scope to allow access to private playlists
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private"))

    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(response['items'])
        if response['next'] is None:
            break
        offset += 50

    # ✅ Sort alphabetically (case-insensitive)
    sorted_playlists = sorted(playlists, key=lambda x: x['name'].lower())

    print("\n🎧 Available Spotify Playlists (A–Z):")
    for i, playlist in enumerate(sorted_playlists):
        print(f"{i + 1}. {playlist['name']}")

    selection = input("\nWhich playlists would you like to download? (e.g. 1,3,5): ")
    selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
    selected_playlists = [sorted_playlists[i] for i in selected_indices]

    print("\n✅ Selected Playlists:")
    for p in selected_playlists:
        print(f"- {p['name']}")

    return selected_playlists
