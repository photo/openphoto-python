from tests import test_albums, test_photos, test_tags

class TestAlbumsV2(test_albums.TestAlbums):
    api_version = 2

class TestPhotosV2(test_photos.TestPhotos):
    api_version = 2

class TestTagsV2(test_tags.TestTags):
    api_version = 2
