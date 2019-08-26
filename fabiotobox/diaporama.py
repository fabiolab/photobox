from loguru import logger
from pathlib import Path, PosixPath
import random


class Diaporama:
    def __init__(self, photo_folder: str):
        self.dirs = Diaporama.list_subdirs(photo_folder)

    @staticmethod
    def list_subdirs(folder: str):
        logger.debug("Loading dirs from {}".format(folder))
        path = Path(folder)
        dirs = [str(PosixPath(folder)) for folder in path.rglob("*") if folder.is_dir()]
        return dirs

    # Get a random photo from the self.dirs directory list
    def pick_photo(self):
        random_dir = random.choice(self.dirs)
        path = Path(random_dir)
        photos = [
            str(filename)
            for filename in path.glob("*.[jJ][pP]*[gG]") if filename.is_file()
        ]

        return random.choice(photos)
