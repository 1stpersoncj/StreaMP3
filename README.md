Copyright © 2025. All rights reserved. For personal or educational use only.
# StreaMP3 🎧

**StreaMP3 Lite** is a playlist downloader for DJs. It lets you:
- Select specific Spotify playlists from your account
- Automatically download the corresponding tracks from YouTube
- Convert them to `.mp3`
- Organize songs into folders named after each playlist

It’s a smart, offline-friendly tool for DJs who want to prep sets fast — even without Spotify Premium.

---

## 🔧 Features
- 🎯 Playlist-based downloads
- 🧠 Duplicate detection (no re-downloads)
- 🗂 Songs auto-organized into folders
- 💻 Works fully offline after login
- 🍎 Built for macOS (Windows support coming soon)

---

## 🚀 How to Use

### 1. Clone or Download

\`\`\`bash
git clone https://github.com/1stpersoncj/StreaMP3.git
cd StreaMP3
\`\`\`

Or just [download the zipped release](#) (coming soon)

---

### 2. Add Your Spotify Credentials

Create a `.env` file in the root folder with:

\`\`\`env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
\`\`\`

> You can register an app for free at: https://developer.spotify.com/dashboard

---

### 3. Run It

If you're using the Python source:

\`\`\`bash
python3 main.py
\`\`\`

If you're using the compiled `.app` or binary:  
Just double-click and follow the prompts in the terminal window.

---

## ⚠️ Disclaimer

This tool is for educational purposes only. It does not bypass any Spotify or YouTube protections and relies on public YouTube search for matches.

---

## 🧠 Credits

Built with:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotipy](https://github.com/plamere/spotipy)
- [ffmpeg](https://ffmpeg.org/)
- Python 3.13
- macOS

---

## 💡 Future Ideas

- Windows/Linux builds
- GUI version
- Smart filename matching improvements
- Watch folder / auto-sync
- File tagging + BPM detection

---

## 📫 Contact

**Made by [@1stpersoncj](https://github.com/1stpersoncj)**  
Drop issues, suggestions, or playlist memes via GitHub Issues 🙃

Copyright © 2025. All rights reserved. For personal or educational use only.
