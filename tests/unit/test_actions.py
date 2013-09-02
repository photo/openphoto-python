from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestActions(unittest.TestCase):
    test_host = "test.example.com"
    test_photos_dict = [{"id": "photo1"},
                        {"id": "photo2"}]
    test_actions_dict = [{"id": "1",
                          "target": test_photos_dict[0],
                          "target_type": "photo",
                          "type": "comment",
                          "totalRows": 2},
                         {"id": "2",
                          "target": test_photos_dict[1],
                          "target_type": "photo",
                          "type": "comment",
                          "totalRows": 2}]

    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)
        self.test_photos = [trovebox.objects.photo.Photo(self.client, photo)
                           for photo in self.test_photos_dict]
        self.test_actions = [trovebox.objects.action.Action(self.client, action)
                             for action in self.test_actions_dict]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestActionCreate(TestActions):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_create(self, mock_post):
        """Check that an action can be created on a photo object"""
        mock_post.return_value = self._return_value(self.test_actions_dict[0])
        result = self.client.action.create(target=self.test_photos[0], type="comment", foo="bar")
        mock_post.assert_called_with("/action/%s/photo/create.json" %
                                     self.test_photos[0].id,
                                     type="comment",
                                     foo="bar")
        self.assertEqual(result.id, "1")
        self.assertEqual(result.target.id, "photo1")
        self.assertEqual(result.target_type, "photo")
        self.assertEqual(result.type, "comment")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_create_id(self, mock_post):
        """Check that an action can be created using a photo id"""
        mock_post.return_value = self._return_value(self.test_actions_dict[0])
        result = self.client.action.create(target=self.test_photos[0].id,
                                           target_type="photo", type="comment",
                                           foo="bar")
        mock_post.assert_called_with("/action/%s/photo/create.json" %
                                     self.test_photos[0].id,
                                     type="comment",
                                     foo="bar")
        self.assertEqual(result.id, "1")
        self.assertEqual(result.target.id, "photo1")
        self.assertEqual(result.target_type, "photo")
        self.assertEqual(result.type, "comment")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_create_invalid_type(self, mock_post):
        """Check that an exception is raised if an action is created on a non photo object"""
        with self.assertRaises(NotImplementedError):
            self.client.action.create(target=object(), foo="bar")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_create_invalid_return_type(self, mock_post):
        """Check that an exception is raised if an non photo object is returned"""
        mock_post.return_value = self._return_value({"target": "test",
                                                     "target_type": "invalid"})
        with self.assertRaises(NotImplementedError):
            self.client.action.create(target=self.test_photos[0], foo="bar")

class TestActionDelete(TestActions):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_delete(self, mock_post):
        """Check that an action can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.action.delete(self.test_actions[0])
        mock_post.assert_called_with("/action/1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_delete_id(self, mock_post):
        """Check that an action can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.action.delete("1")
        mock_post.assert_called_with("/action/1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_delete_failure(self, mock_post):
        """Check that an exception is raised if an action cannot be deleted"""
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.action.delete(self.test_actions[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_object_delete(self, mock_post):
        """Check that an action can be deleted using the action object directly"""
        mock_post.return_value = self._return_value(True)
        action = self.test_actions[0]
        result = action.delete()
        mock_post.assert_called_with("/action/1/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(action.get_fields(), {})
        self.assertEqual(action.id, None)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_action_object_delete_failure(self, mock_post):
        """
        Check that an exception is raised if an action cannot be deleted
        when using the action object directly
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.test_actions[0].delete()

class TestActionView(TestActions):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_action_view(self, mock_get):
        """Check that an action can be viewed"""
        mock_get.return_value = self._return_value(self.test_actions_dict[1])
        result = self.client.action.view(self.test_actions[0], name="Test")
        mock_get.assert_called_with("/action/1/view.json", name="Test")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.target.id, "photo2")
        self.assertEqual(result.target_type, "photo")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_action_view_id(self, mock_get):
        """Check that an action can be viewed using its ID"""
        mock_get.return_value = self._return_value(self.test_actions_dict[1])
        result = self.client.action.view("1", name="Test")
        mock_get.assert_called_with("/action/1/view.json", name="Test")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.target.id, "photo2")
        self.assertEqual(result.target_type, "photo")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_action_object_view(self, mock_get):
        """Check that an action can be viewed using the action object directly"""
        mock_get.return_value = self._return_value(self.test_actions_dict[1])
        action = self.test_actions[0]
        action.view(name="Test")
        mock_get.assert_called_with("/action/1/view.json", name="Test")
        self.assertEqual(action.id, "2")
        self.assertEqual(action.target.id, "photo2")
        self.assertEqual(action.target_type, "photo")

