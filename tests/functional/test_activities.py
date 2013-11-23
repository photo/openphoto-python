try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from tests.functional import test_base

@unittest.skipIf(test_base.get_test_server_api() == 1,
                 ("Activities never get deleted in v1, which makes "
                  "these tests too hard to write"))
class TestActivities(test_base.TestBase):
    testcase_name = "activity API"

    def test_list(self):
        """
        Upload three photos, and check that three corresponding activities
        are created.
        """
        self._delete_all()
        self._create_test_photos(tag=False)
        photos = self.client.photos.list()

        # Check that each activity is for a valid test photo
        activities = self.client.activities.list()
        self.assertEqual(len(activities), len(photos))
        for activity in activities:
            self.assertIn(activity.data.id, [photo.id for photo in photos])

        # Put the environment back the way we found it
        for photo in photos:
            photo.update(tags=self.TEST_TAG)

    def test_list_option(self):
        """
        Check that the activity list options parameter works correctly
        """
        self._delete_all()
        self._create_test_photos(tag=False)
        photos = self.client.photos.list()

        # Dummy photo update activity
        photos[0].update(tags=photos[0].tags)

        # Check that the activities can be filtered
        upload_activities = self.client.activities.list(options={"type": "photo-upload"})
        update_activities = self.client.activities.list(options={"type": "photo-update"})
        self.assertEqual(len(upload_activities), len(photos))
        self.assertEqual(len(update_activities), 1)

        # Put the environment back the way we found it
        for photo in photos:
            photo.update(tags=self.TEST_TAG)

    # The purge endpoint currently reports a 500: Internal Server Error
    # PHP Fatal error:
    #   Call to undefined method DatabaseMySql::postActivitiesPurge()
    #   in /var/www/openphoto-master/src/libraries/models/Activity.php
    #   on line 66
    # Tracked in frontend/#1368
    @unittest.expectedFailure
    def test_purge(self):
        """ Test that the purge endpoint deletes all activities """
        activities = self.client.activities.list()
        self.assertNotEqual(activities, [])
        self.client.activities.purge()
        activities = self.client.activities.list()
        self.assertEqual(activities, [])

    def test_view(self):
        """ Test that the view endpoint is working correctly """
        activity = self.client.activities.list()[0]
        fields = activity.get_fields().copy()

        # Check that the view method returns the same data as the list
        activity.view()
        self.assertEqual(fields, activity.get_fields())

        # Check using the Trovebox class
        activity = self.client.activity.view(activity)
        self.assertEqual(fields, activity.get_fields())

        # Check passing the activity ID to the Trovebox class
        activity = self.client.activity.view(activity.id)
        self.assertEqual(fields, activity.get_fields())
