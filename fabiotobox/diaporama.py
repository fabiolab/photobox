from loguru import logger
from pathlib import Path, PosixPath
import random


class Diaporama:
    def __init__(self, photo_folder: str):
        self.dirs = Diaporama.list_dirs(photo_folder)

    @staticmethod
    def list_dirs(folder: str, max_depth: int = 2):
        logger.debug("Loading dirs and subdirs from {}".format(folder))
        path = Path(folder)
        
        dirs = [
            str(PosixPath(folder)) for folder in path.glob("*/" * max_depth)
        ]

        return dirs

    # Get a random photo from the self.dirs directory list
    def pick_photo(self):
        random_dir = random.choice(self.dirs)
        path = Path(random_dir)
        photos = [
            str(filename)
            for filename in path.glob("*.[jJ][pP]*[gG]")
            if filename.is_file()
        ]
        
        if not photos:
            logger.error("No photo in this path {}".format(random_dir))

        return random.choice(photos)
