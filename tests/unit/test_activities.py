from __future__ import unicode_literals
import json
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestActivities(unittest.TestCase):
    test_host = "test.example.com"
    test_photos_dict = [{"id": "photo1"},
                        {"id": "photo2"}]
    test_activities_dict = [{"id": "1",
                             "data": test_photos_dict[0],
                             "type": "photo_upload"},
                            {"id": "2",
                             "data": test_photos_dict[1],
                             "type": "photo_update"}]

    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)
        self.test_photos = [trovebox.objects.photo.Photo(self.client, photo)
                           for photo in self.test_photos_dict]
        self.test_activities = [trovebox.objects.activity.Activity(self.client, activity)
                                for activity in self.test_activities_dict]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

    @staticmethod
    def _view_wrapper(result):
        """ The view method returns data enclosed in a dict and JSON encoded """
        result["data"] = json.dumps(result["data"])
        return {"0": result}

class TestActivitiesList(TestActivities):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_activities_list(self, mock_get):
        """Check that the activity list is returned correctly"""
        mock_get.return_value = self._return_value(self.test_activities_dict)

        result = self.client.activities.list()
        mock_get.assert_called_with("/activities/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].type, "photo_upload")
        self.assertEqual(result[0].data.id, "photo1")
        self.assertEqual(result[1].id, "2")
        self.assertEqual(result[1].type, "photo_update")
        self.assertEqual(result[1].data.id, "photo2")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_empty_result(self, mock_get):
        """Check that an empty result is transformed into an empty list """
        mock_get.return_value = self._return_value("")
        result = self.client.activities.list()
        mock_get.assert_called_with("/activities/list.json")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_zero_rows(self, mock_get):
        """Check that totalRows=0 is transformed into an empty list """
        mock_get.return_value = self._return_value([{"totalRows": 0}])
        result = self.client.activities.list()
        mock_get.assert_called_with("/activities/list.json")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_filters(self, mock_get):
        """Check that the activity list filters are applied properly"""
        mock_get.return_value = self._return_value(self.test_activities_dict)
        self.client.activities.list(filters={"foo": "bar",
                                             "test1": "test2"})
        # Dict element can be any order
        self.assertIn(mock_get.call_args[0],
                      [("/activities/foo-bar/test1-test2/list.json",),
                       ("/activities/test1-test2/foo-bar/list.json",)])

class TestActivitiesPurge(TestActivities):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_activity_purge(self, mock_get):
        """Test activity purging """
        mock_get.return_value = self._return_value(True)

        result = self.client.activities.purge(foo="bar")
        mock_get.assert_called_with("/activities/purge.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_activity_purge_failure(self, mock_post):
        """Test activity purging """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            result = self.client.activities.purge(foo="bar")

class TestActivityView(TestActivities):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_activity_view(self, mock_get):
        """Check that a activity can be viewed"""
        mock_get.return_value = self._return_value(self._view_wrapper(
                                self.test_activities_dict[1]))
        result = self.client.activity.view(self.test_activities[0],
                                           foo="bar")
        mock_get.assert_called_with("/activity/1/view.json", foo="bar")
        self.assertEqual(result.get_fields(), self.test_activities_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_activity_view_id(self, mock_get):
        """Check that a activity can be viewed using its ID"""
        mock_get.return_value = self._return_value(self._view_wrapper(
                                self.test_activities_dict[1]))
        result = self.client.activity.view("1", foo="bar")
        mock_get.assert_called_with("/activity/1/view.json", foo="bar")
        self.assertEqual(result.get_fields(), self.test_activities_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_activity_object_view(self, mock_get):
        """
        Check that a activity can be viewed
        when using the activity object directly
        """
        mock_get.return_value = self._return_value(self._view_wrapper(
                                self.test_activities_dict[1]))
        activity = self.test_activities[0]
        activity.view(foo="bar")
        mock_get.assert_called_with("/activity/1/view.json", foo="bar")
        self.assertEqual(activity.get_fields(), self.test_activities_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_activity_view_invalid_type(self, mock_get):
        """Check that an invalid activity type raises an exception"""
        mock_get.return_value = self._return_value(self._view_wrapper(
                                {"data": "", "type": "invalid"}))
        with self.assertRaises(NotImplementedError):
            self.client.activity.view(self.test_activities[0], foo="bar")
