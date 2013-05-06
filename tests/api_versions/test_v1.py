import unittest
from tests import test_albums, test_photos, test_tags

class TestAlbumsV1(test_albums.TestAlbums):
    api_version = 1

class TestPhotosV1(test_photos.TestPhotos):
    api_version = 1

# The tag API didn't work at v1 - see frontend issue #927
# class TestTagsV1(test_tags.TestTags):
    # api_version = 1
