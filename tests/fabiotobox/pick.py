from fabiotobox.diaporama import Diaporama
from loguru import logger

if __name__ == "__main__":
    logger.info("Run ...")
    diapo = Diaporama(photo_folder="/media/kvjw3322/2078B0CD25633F53/Backup/Photos")

    logger.info("Init done !")

    for i in range(5):
        logger.info(diapo.pick_photo())
