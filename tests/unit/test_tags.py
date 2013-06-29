from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestTags(unittest.TestCase):
    TEST_HOST = "test.example.com"
    TEST_TAGS_DICT = [{"count": 11, "id":"tag1"},
                      {"count": 5, "id":"tag2"}]

    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST)
        self.TEST_TAGS = [openphoto.objects.Tag(self.client, tag)
                            for tag in self.TEST_TAGS_DICT]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestTagsList(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_tags_list(self, mock):
        mock.return_value = self._return_value(self.TEST_TAGS_DICT)
        result = self.client.tags.list()
        mock.assert_called_with("/tags/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "tag1")
        self.assertEqual(result[0].count, 11)
        self.assertEqual(result[1].id, "tag2")
        self.assertEqual(result[1].count, 5)

class TestTagCreate(TestTags):
    # TODO: should return a tag object, not a result dict
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_create(self, mock):
        mock.return_value = self._return_value(self.TEST_TAGS_DICT[0])
        result = self.client.tag.create(tag="Test", foo="bar")
        mock.assert_called_with("/tag/create.json", tag="Test", foo="bar")
        self.assertEqual(result.id, "tag1")
        self.assertEqual(result.count,  11)

class TestTagDelete(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.tag.delete(self.TEST_TAGS[0])
        mock.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete_id(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.tag.delete("tag1")
        mock.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)

    # TODO: tag.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_delete_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.tag.delete(self.TEST_TAGS[0])

    # TODO: after deleting object fields, id should be set to None
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_delete(self, mock):
        mock.return_value = self._return_value(True)
        tag = self.TEST_TAGS[0]
        result = tag.delete()
        mock.assert_called_with("/tag/tag1/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(tag.get_fields(), {})
        # self.assertEqual(tag.id, None)

    # TODO: tag.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_delete_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.TEST_TAGS[0].delete()

class TestTagUpdate(TestTags):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_update(self, mock):
        mock.return_value = self._return_value(self.TEST_TAGS_DICT[1])
        result = self.client.tag.update(self.TEST_TAGS[0], name="Test")
        mock.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(result.id, "tag2")
        self.assertEqual(result.count, 5)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_update_id(self, mock):
        mock.return_value = self._return_value(self.TEST_TAGS_DICT[1])
        result = self.client.tag.update("tag1", name="Test")
        mock.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(result.id, "tag2")
        self.assertEqual(result.count, 5)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_tag_object_update(self, mock):
        mock.return_value = self._return_value(self.TEST_TAGS_DICT[1])
        tag = self.TEST_TAGS[0]
        tag.update(name="Test")
        mock.assert_called_with("/tag/tag1/update.json", name="Test")
        self.assertEqual(tag.id, "tag2")
        self.assertEqual(tag.count, 5)

