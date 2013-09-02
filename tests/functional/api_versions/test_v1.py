from tests.functional import test_activities, test_actions
from tests.functional import test_albums, test_photos, test_tags

class TestActivitiesV1(test_activities.TestActivities):
    api_version = 1

class TestActionsV1(test_actions.TestActions):
    api_version = 1

class TestAlbumsV1(test_albums.TestAlbums):
    api_version = 1

class TestPhotosV1(test_photos.TestPhotos):
    api_version = 1

class TestTagsV1(test_tags.TestTags):
    api_version = 1
