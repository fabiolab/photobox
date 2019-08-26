from fabiotobox.diaporama import Diaporama

PHOTO_FOLDER = "photos"


def test_listsubdirs():
    diapo = Diaporama(PHOTO_FOLDER)
    dirs = diapo.list_subdirs(PHOTO_FOLDER)

    assert dirs == ["photos/test"]


def test_pickphoto():
    diapo = Diaporama(PHOTO_FOLDER)
    photo = diapo.pick_photo()

    assert photo in [
        "photos/test/test01.jpg",
        "photos/test/test02.JPEG",
        "photos/test/test03.jPg",
    ]
    assert photo not in ["photos/test/test04.png"]
