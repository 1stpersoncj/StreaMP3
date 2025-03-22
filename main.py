import os
import sys
from dotenv import load_dotenv

# ✅ Detect base directory for PyInstaller and normal environments
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# ✅ Full paths for .env and .env.template
env_path = os.path.join(base_dir, ".env")
template_path = os.path.join(base_dir, ".env.template")

# ✅ Auto-copy .env from template if missing
if not os.path.exists(env_path) and os.path.exists(template_path):
    with open(template_path, "r") as template_file:
        with open(env_path, "w") as env_file:
            env_file.write(template_file.read())

# ✅ Load environment variables from the resolved .env path
load_dotenv(dotenv_path=env_path)

# ✅ Print to confirm (for testing — safe to remove later)
print("SPOTIPY_CLIENT_ID:", os.getenv("SPOTIPY_CLIENT_ID"))
print("SPOTIPY_CLIENT_SECRET:", os.getenv("SPOTIPY_CLIENT_SECRET"))
print("SPOTIPY_REDIRECT_URI:", os.getenv("SPOTIPY_REDIRECT_URI"))

from spotify_scraper import get_selected_playlists
from audio_downloader import AudioDownloader
from organizer import Organizer

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_tracks_for_playlist(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-read-private"))
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def main():
    selected_playlists = get_selected_playlists()
    downloader = AudioDownloader()
    organizer = Organizer()

    for playlist in selected_playlists:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        print(f"\n🎯 Processing Playlist: {playlist_name}")

        tracks = get_tracks_for_playlist(playlist_id)

        for item in tracks:
            track_data = item['track']
            if not track_data:
                continue

            track = {
                'name': track_data['name'],
                'artist': track_data['artists'][0]['name']
            }

            print(f"🎵 Downloading: {track['artist']} - {track['name']}")
            audio_file = downloader.download_audio(track)

            if audio_file:
                print(f"✅ Sending to organizer: {audio_file} → {playlist_name}")
                organizer.organize_file(audio_file, [playlist_name])
            else:
                print(f"❌ Skipping organization for: {track['artist']} - {track['name']}")

if __name__ == "__main__":
    main()
