from fabiotobox.diaporama import Diaporama

PHOTO_FOLDER = "photos"
diapo = Diaporama(photo_folder=PHOTO_FOLDER)


def test_listsubdirs():
    dirs = diapo.list_dirs(PHOTO_FOLDER, include_subdirs=True)

    assert dirs == ["photos/test", "photos/test/foo"]


def test_listdirs():
    dirs = diapo.list_dirs(PHOTO_FOLDER)

    assert dirs == ["photos/test"]


def test_pickphoto():
    photo = diapo.pick_photo()

    assert photo in [
        "photos/test/foo/test01.jpg",
        "photos/test/test02.JPEG",
        "photos/test/test03.jPg",
    ]
    assert photo not in ["photos/test/test04.png"]


def test_createcache():
    diapo.create_photo_cache(PHOTO_FOLDER)
    photos = list()
    with open(diapo.photo_cache) as f:
        for line in f.readlines():
            photos.append(line.strip())

    photos.sort()
    assert [
        "photos/test/foo/test01.jpg",
        "photos/test/test02.JPEG",
        "photos/test/test03.jPg",
    ] == photos
