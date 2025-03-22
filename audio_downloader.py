import os
import glob
import sys
import unicodedata
import re
from yt_dlp import YoutubeDL

class AudioDownloader:
    def __init__(self, download_dir='downloads', organized_dir='organized'):
        # ✅ Handle PyInstaller or source run
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        self.download_dir = os.path.join(base_dir, download_dir)
        self.organized_dir = os.path.join(base_dir, organized_dir)

        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.organized_dir, exist_ok=True)

        self.ffmpeg_path = os.path.join(base_dir, "ffmpeg")

    def clean_filename(self, text):
        """Simplify and normalize names for fuzzy matching."""
        text = unicodedata.normalize("NFKD", text)
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', '', text)
        return text.strip()

    def already_organized(self, track):
        """Check all playlist folders in 'organized' for a matching mp3."""
        expected_name = self.clean_filename(f"{track['artist']}{track['name']}")

        for root, dirs, files in os.walk(self.organized_dir):
            for file in files:
                if file.endswith(".mp3"):
                    cleaned = self.clean_filename(file)
                    if expected_name in cleaned:
                        return os.path.join(root, file)

        return None

    def download_audio(self, track):
        search_query = f"{track['name']} {track['artist']}"
        output_template = os.path.join(self.download_dir, "%(autonumber)03d - %(title).80s.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'noplaylist': True,
            'default_search': 'ytsearch1',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            'ffmpeg_location': self.ffmpeg_path,
            'nocache': True
        }

        # ✅ Skip download if already exists
        existing = self.already_organized(track)
        if existing:
            print(f"⏩ Skipping (already organized): {track['artist']} - {track['name']}")
            return existing

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_query])

            downloaded_files = glob.glob(os.path.join(self.download_dir, "*.mp3"))
            if not downloaded_files:
                print(f"ERROR: No MP3 file found after downloading {search_query}")
                return None

            downloaded_file = max(downloaded_files, key=os.path.getmtime)
            return downloaded_file

        except Exception as e:
            print(f"ERROR: Failed to download {search_query}. Reason: {e}")
            return None
