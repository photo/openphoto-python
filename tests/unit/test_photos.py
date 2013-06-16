from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestPhotos(unittest.TestCase):
    TEST_HOST = "test.example.com"

    TEST_PHOTOS = [{"id": "1a",
                    "tags": ["tag1", "tag2"],
                    "totalPages": 1,
                    "totalRows": 2},
                   {"id": "2b",
                    "tags": ["tag3", "tag4"],
                    "totalPages": 1,
                    "totalRows": 2}]

    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST)

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestPhotosList(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_list(self, mock_get):
        photos = self.TEST_PHOTOS
        mock_get.return_value = self._return_value(photos)

        result = self.client.photos.list()
        mock_get.assert_called_with("/photos/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1a")
        self.assertEqual(result[0].tags, ["tag1", "tag2"])
        self.assertEqual(result[1].id, "2b")
        self.assertEqual(result[1].tags, ["tag3", "tag4"])

class TestPhotosUpdate(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_update(self, mock_post):
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.update(["1a", "2b"], title="Test")
        mock_post.assert_called_with("/photos/update.json",
                                     ids=["1a", "2b"], title="Test")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_update_failure_raises_exception(self, mock_post):
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photos.update(["1a", "2b"], title="Test")

class TestPhotosDelete(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_delete(self, mock_post):
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.delete(["1a", "2b"])
        mock_post.assert_called_with("/photos/delete.json", ids=["1a", "2b"])
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_delete_failure_raises_exception(self, mock_post):
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photos.delete(["1a", "2b"])

class TestPhotoDelete(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_delete(self, mock_post):
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete("1a")
        mock_post.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    # TODO: photo.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_delete_failure_raises_exception(self, mock_post):
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photo.delete("1a")

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_object_delete(self, mock_post):
        mock_post.return_value = self._return_value(True)
        photo = openphoto.objects.Photo(self.client, self.TEST_PHOTOS[0])
        result = photo.delete()
        mock_post.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    # TODO: photo.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_object_delete_failure_raises_exception(self, mock_post):
        mock_post.return_value = self._return_value(False)
        photo = openphoto.objects.Photo(self.client, self.TEST_PHOTOS[0])
        with self.assertRaises(openphoto.OpenPhotoError):
            photo.delete()

