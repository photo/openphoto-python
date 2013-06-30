from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestTags(unittest.TestCase):
    test_host = "test.example.com"
    test_tags = None
    test_tags_dict = [{"count": 11, "id":"tag1"},
                      {"count": 5, "id":"tag2"}]

    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.test_host)
        self.test_tags = [openphoto.objects.Tag(self.client, tag)
                          for tag in self.test_tags_dict]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestTagsList(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_tags_list(self, mock_get):
        """Check that the the tag list is returned correctly"""
        mock_get.return_value = self._return_value(self.test_tags_dict)
        result = self.client.tags.list()
        mock_get.assert_called_with("/tags/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "tag1")
        self.assertEqual(result[0].count, 11)
        self.assertEqual(result[1].id, "tag2")
        self.assertEqual(result[1].count, 5)

class TestTagCreate(TestTags):
    # TODO: should return a tag object, not a result dict
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_create(self, mock_post):
        """Check that a tag can be created"""
        mock_post.return_value = self._return_value(self.test_tags_dict[0])
        result = self.client.tag.create(tag="Test", foo="bar")
        mock_post.assert_called_with("/tag/create.json", tag="Test", foo="bar")
        self.assertEqual(result.id, "tag1")
        self.assertEqual(result.count,  11)

class TestTagDelete(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete(self, mock_post):
        """Check that a tag can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.tag.delete(self.test_tags[0])
        mock_post.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete_id(self, mock_post):
        """Check that a tag can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.tag.delete("tag1")
        mock_post.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete_failure(self, mock_post):
        """Check that an exception is raised if a tag cannot be deleted"""
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.tag.delete(self.test_tags[0])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_delete(self, mock_post):
        """Check that a tag can be deleted when using the tag object directly"""
        mock_post.return_value = self._return_value(True)
        tag = self.test_tags[0]
        result = tag.delete()
        mock_post.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(tag.get_fields(), {})
        self.assertEqual(tag.id, None)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_delete_failure(self, mock_post):
        """
        Check that an exception is raised if a tag cannot be deleted
        when using the tag object directly
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.test_tags[0].delete()

class TestTagUpdate(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_update(self, mock_post):
        """Check that a tag can be updated"""
        mock_post.return_value = self._return_value(self.test_tags_dict[1])
        result = self.client.tag.update(self.test_tags[0], name="Test")
        mock_post.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(result.id, "tag2")
        self.assertEqual(result.count, 5)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_update_id(self, mock_post):
        """Check that a tag can be updated using its ID"""
        mock_post.return_value = self._return_value(self.test_tags_dict[1])
        result = self.client.tag.update("tag1", name="Test")
        mock_post.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(result.id, "tag2")
        self.assertEqual(result.count, 5)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_update(self, mock_post):
        """Check that a tag can be updated when using the tag object directly"""
        mock_post.return_value = self._return_value(self.test_tags_dict[1])
        tag = self.test_tags[0]
        tag.update(name="Test")
        mock_post.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(tag.id, "tag2")
        self.assertEqual(tag.count, 5)

