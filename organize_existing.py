import os
import logging
import shutil
from spotify_scraper import SpotifyScraper

# Configure logging
logging.basicConfig(
    filename='logs/organizer.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    logging.info("Starting organizer for existing downloads.")
    downloads_dir = 'downloads'
    organized_dir = 'organized'

    # Ensure directories exist
    if not os.path.exists(downloads_dir):
        logging.error("Downloads folder not found.")
        return

    if not os.path.exists(organized_dir):
        os.makedirs(organized_dir)

    try:
        # Initialize the Spotify scraper to fetch playlist metadata
        scraper = SpotifyScraper()
        playlists = scraper.scrape_playlists()

        # Map each track to its playlist(s)
        track_to_playlists = {}
        for playlist_name, tracks in playlists.items():
            for track in tracks:
                track_key = (track['name'], track['artist'])
                if track_key not in track_to_playlists:
                    track_to_playlists[track_key] = []
                track_to_playlists[track_key].append(playlist_name)

        # Process files in the downloads folder
        for file_name in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, file_name)

            # Skip non-MP3 files
            if not file_name.endswith('.mp3'):
                logging.info(f"Skipping non-MP3 file: {file_name}")
                continue

            # Try to match the file to a track in Spotify playlists
            matched_playlists = []
            for (track_name, artist), playlist_names in track_to_playlists.items():
                if track_name in file_name:
                    matched_playlists.extend(playlist_names)

            if matched_playlists:
                # Organize file into matched playlists
                for i, playlist_name in enumerate(set(matched_playlists)):
                    playlist_dir = os.path.join(organized_dir, playlist_name)
                    os.makedirs(playlist_dir, exist_ok=True)
                    destination = os.path.join(playlist_dir, file_name)

                    if not os.path.exists(destination):
                        if i == 0:
                            shutil.move(file_path, destination)
                            logging.info(f"Moved {file_name} to {playlist_name}")
                        else:
                            shutil.copy(destination, playlist_dir)
                            logging.info(f"Copied {file_name} to {playlist_name}")
                    else:
                        logging.info(f"File {file_name} already exists in {playlist_name}. Skipping.")

            else:
                logging.warning(f"No matching playlist found for {file_name}. Skipping.")

    except Exception as e:
        logging.error(f"Error occurred during organization: {e}")

    logging.info("Finished organizing existing downloads.")

if __name__ == "__main__":
    main()
