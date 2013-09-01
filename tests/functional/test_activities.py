try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from tests.functional import test_base

class TestActivities(test_base.TestBase):
    testcase_name = "activity API"

    @unittest.skipIf(test_base.get_test_server_api() == 1,
                     "The activity/list endpoint behaves differenty at v1")
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
        self.assertEqual(len(activities), len(self.photos))
        for activity in activities:
            self.assertIn(activity.data.id, [photo.id for photo in photos])

    # The purge endpoint currently reports a 500: Internal Server Error
    @unittest.expectedFailure
    def test_purge(self):
        """ Test that the purge endpoint deletes all activities """
        activities = self.client.activities.list()
        self.assertNotEqual(activities, [])
        self.client.activities.purge()
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
