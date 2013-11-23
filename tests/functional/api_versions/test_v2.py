try:
    import unittest2 as unittest
except ImportError:
    import unittest

from tests.functional import test_base, test_activities, test_actions
from tests.functional import test_albums, test_photos, test_tags

@unittest.skipIf(test_base.get_test_server_api() < 2,
                 "Don't test future API versions")
class TestActivitiesV2(test_activities.TestActivities):
    api_version = 2

@unittest.skipIf(test_base.get_test_server_api() < 2,
                 "Don't test future API versions")
class TestActionsV2(test_actions.TestActions):
    api_version = 2

@unittest.skipIf(test_base.get_test_server_api() < 2,
                 "Don't test future API versions")
class TestAlbumsV2(test_albums.TestAlbums):
    api_version = 2

@unittest.skipIf(test_base.get_test_server_api() < 2,
                 "Don't test future API versions")
class TestPhotosV2(test_photos.TestPhotos):
    api_version = 2

@unittest.skipIf(test_base.get_test_server_api() < 2,
                 "Don't test future API versions")
class TestTagsV2(test_tags.TestTags):
    api_version = 2
