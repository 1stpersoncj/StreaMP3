import os
import shutil
import logging
import re
import sys

# ✅ Enable terminal logging (INFO level)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Organizer:
    def __init__(self, base_dir='organized'):
        # ✅ Handle both source run and PyInstaller bundle run
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))

        self.base_dir = os.path.join(script_dir, base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    @staticmethod
    def clean_name(name):
        return re.sub(r'[^a-z0-9]', '', name.lower())

    def organize_file(self, file_path, playlist_names):
        try:
            if not os.path.exists(file_path):
                logging.error(f"File not found: {file_path}. Skipping organization.")
                return

            for i, playlist_name in enumerate(playlist_names):
                playlist_dir = os.path.join(self.base_dir, playlist_name)
                os.makedirs(playlist_dir, exist_ok=True)

                destination = os.path.join(playlist_dir, os.path.basename(file_path))
                if os.path.exists(destination):
                    logging.info(f"File already exists in {playlist_dir}. Skipping.")
                    continue

                if i == 0:
                    shutil.move(file_path, destination)
                    logging.info(f"Moved {file_path} into {playlist_dir}")
                else:
                    if os.path.exists(destination):
                        shutil.copy(destination, playlist_dir)
                        logging.info(f"Copied {file_path} into {playlist_name}")
                    else:
                        logging.warning(f"File {file_path} not found for copying. Skipping.")

        except Exception as e:
            logging.error(f"Error while organizing file {file_path}: {e}")
            raise
