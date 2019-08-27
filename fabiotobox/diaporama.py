from loguru import logger
from pathlib import Path, PosixPath
import random


class Diaporama:
    def __init__(self, photo_folder: str, cache_folder: str = '/tmp'):
        path = Path(cache_folder)
        self.photo_cache = path.joinpath("listphotos.txt")
        self.dirs = Diaporama.list_dirs(photo_folder, True)

    @staticmethod
    def list_dirs(folder: str, include_subdirs: bool = False):
        logger.debug("Loading dirs and subdirs from {}".format(folder))
        path = Path(folder)
        if include_subdirs:
            dirs = [
                str(PosixPath(folder)) for folder in path.rglob("*") if folder.is_dir()
            ]
        else:
            dirs = [
                str(PosixPath(folder)) for folder in path.glob("*") if folder.is_dir()
            ]

        return dirs

    def create_photo_cache(self, folder: str):
        logger.info("Creating photo cache ...")
        path = Path(folder)
        with open(self.photo_cache, "w") as f:
            for filename in path.rglob("**/*.[jJ][pP]*[gG]"):
                f.write(str(filename) + "\n")

    # Get a random photo from the self.dirs directory list
    def pick_photo(self):
        random_dir = random.choice(self.dirs)
        path = Path(random_dir)
        photos = [
            str(filename)
            for filename in path.glob("*.[jJ][pP]*[gG]")
            if filename.is_file()
        ]

        return random.choice(photos)
