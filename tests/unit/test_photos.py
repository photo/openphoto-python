from __future__ import unicode_literals
import os
import base64
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestPhotos(unittest.TestCase):
    TEST_HOST = "test.example.com"
    TEST_FILE = os.path.join("tests", "unit", "data", "test_file.txt")
    TEST_PHOTOS_DICT = [{"id": "1a", "tags": ["tag1", "tag2"],
                         "totalPages": 1, "totalRows": 2},
                        {"id": "2b", "tags": ["tag3", "tag4"],
                         "totalPages": 1, "totalRows": 2}]
    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST)
        self.TEST_PHOTOS = [openphoto.objects.Photo(self.client, photo)
                            for photo in self.TEST_PHOTOS_DICT]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestPhotosList(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photos_list(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT)

        result = self.client.photos.list()
        mock.assert_called_with("/photos/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1a")
        self.assertEqual(result[0].tags, ["tag1", "tag2"])
        self.assertEqual(result[1].id, "2b")
        self.assertEqual(result[1].tags, ["tag3", "tag4"])

class TestPhotosUpdate(TestPhotos):
    # TODO: photos.update should accept a list of Photo objects
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_update(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photos.update(self.TEST_PHOTOS, title="Test")
        mock.assert_called_with("/photos/update.json",
                                     ids=["1a", "2b"], title="Test")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_update_ids(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photos.update(["1a", "2b"], title="Test")
        mock.assert_called_with("/photos/update.json",
                                     ids=["1a", "2b"], title="Test")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_update_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photos.update(self.TEST_PHOTOS, title="Test")

class TestPhotosDelete(TestPhotos):
    # TODO: photos.delete should accept a list of Photo objects
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_delete(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photos.delete(self.TEST_PHOTOS)
        mock.assert_called_with("/photos/delete.json", ids=["1a", "2b"])
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_delete_ids(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photos.delete(["1a", "2b"])
        mock.assert_called_with("/photos/delete.json", ids=["1a", "2b"])
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photos_delete_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photos.delete(self.TEST_PHOTOS)

class TestPhotoDelete(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_delete(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photo.delete(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_delete_id(self, mock):
        mock.return_value = self._return_value(True)
        result = self.client.photo.delete("1a")
        mock.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    # TODO: photo.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_delete_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.photo.delete(self.TEST_PHOTOS[0])

    # TODO: after deleting object fields, name and id should be set to None
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_delete(self, mock):
        mock.return_value = self._return_value(True)
        photo = self.TEST_PHOTOS[0]
        result = photo.delete()
        mock.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(photo.get_fields(), {})
        # self.assertEqual(photo.id, None)

    # TODO: photo.delete should raise exception on failure
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_delete_failure_raises_exception(self, mock):
        mock.return_value = self._return_value(False)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.TEST_PHOTOS[0].delete()

class TestPhotoEdit(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_edit(self, mock):
        mock.return_value = self._return_value({"markup": "<form/>"})
        result = self.client.photo.edit(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_edit_id(self, mock):
        mock.return_value = self._return_value({"markup": "<form/>"})
        result = self.client.photo.edit("1a")
        mock.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_object_edit(self, mock):
        mock.return_value = self._return_value({"markup": "<form/>"})
        result = self.TEST_PHOTOS[0].edit()
        mock.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

class TestPhotoReplace(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_replace(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace(self.TEST_PHOTOS[0], self.TEST_FILE)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_replace_id(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace("1a", self.TEST_FILE)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_replace(self, mock):
        with self.assertRaises(NotImplementedError):
            self.TEST_PHOTOS[0].replace(self.TEST_FILE)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_replace_encoded(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace_encoded(self.TEST_PHOTOS[0], self.TEST_FILE)

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_replace_encoded_id(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace_encoded("1a", self.TEST_FILE)

    # TODO: replace_encoded parameter should be called photo_file,
    #       not encoded_photo
    @unittest.expectedFailure
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_replace_encoded(self, mock):
        with self.assertRaises(NotImplementedError):
            self.TEST_PHOTOS[0].replace_encoded(photo_file=self.TEST_FILE)

class TestPhotoUpdate(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_update(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.update(self.TEST_PHOTOS[0], title="Test")
        mock.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_update_id(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.update("1a", title="Test")
        mock.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_update(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        photo = self.TEST_PHOTOS[0]
        photo.update(title="Test")
        mock.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(photo.get_fields(), self.TEST_PHOTOS_DICT[1])

class TestPhotoView(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_view(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.view(self.TEST_PHOTOS[0], returnSizes="20x20")
        mock.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_view_id(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.view("1a", returnSizes="20x20")
        mock.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_object_view(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        photo = self.TEST_PHOTOS[0]
        photo.view(returnSizes="20x20")
        mock.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(photo.get_fields(), self.TEST_PHOTOS_DICT[1])

class TestPhotoUpload(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_upload(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[0])
        result = self.client.photo.upload(self.TEST_FILE, title="Test")
        # It's not possible to compare the file object,
        # so check each parameter individually
        endpoint = mock.call_args[0]
        title = mock.call_args[1]["title"]
        files = mock.call_args[1]["files"]
        self.assertEqual(endpoint, ("/photo/upload.json",))
        self.assertEqual(title, "Test")
        self.assertIn("photo", files)
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[0])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_upload_encoded(self, mock):
        encoded_file = base64.b64encode(open(self.TEST_FILE, "rb").read())
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[0])
        result = self.client.photo.upload_encoded(self.TEST_FILE, title="Test")
        mock.assert_called_with("/photo/upload.json",
                                    photo=encoded_file, title="Test")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[0])

class TestPhotoDynamicUrl(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_dynamic_url(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.dynamic_url(self.TEST_PHOTOS[0])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_dynamic_url_id(self, mock):
        with self.assertRaises(NotImplementedError):
            self.client.photo.dynamic_url("1a")

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_object_dynamic_url(self, mock):
        with self.assertRaises(NotImplementedError):
            self.TEST_PHOTOS[0].dynamic_url()

class TestPhotoNextPrevious(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_next_previous(self, mock):
        mock.return_value = self._return_value(
            {"next": [self.TEST_PHOTOS_DICT[0]],
             "previous": [self.TEST_PHOTOS_DICT[1]]})
        result = self.client.photo.next_previous(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_next_previous_id(self, mock):
        mock.return_value = self._return_value(
            {"next": [self.TEST_PHOTOS_DICT[0]],
             "previous": [self.TEST_PHOTOS_DICT[1]]})
        result = self.client.photo.next_previous("1a")
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_object_next_previous(self, mock):
        mock.return_value = self._return_value(
            {"next": [self.TEST_PHOTOS_DICT[0]],
             "previous": [self.TEST_PHOTOS_DICT[1]]})
        result = self.TEST_PHOTOS[0].next_previous()
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_next(self, mock):
        mock.return_value = self._return_value(
            {"next": [self.TEST_PHOTOS_DICT[0]]})
        result = self.client.photo.next_previous(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertNotIn("previous", result)

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_previous(self, mock):
        mock.return_value = self._return_value(
            {"previous": [self.TEST_PHOTOS_DICT[1]]})
        result = self.client.photo.next_previous(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["previous"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[1])
        self.assertNotIn("next", result)

    @mock.patch.object(openphoto.OpenPhoto, 'get')
    def test_photo_multiple_next_previous(self, mock):
        mock.return_value = self._return_value(
            {"next": [self.TEST_PHOTOS_DICT[0], self.TEST_PHOTOS_DICT[0]],
             "previous": [self.TEST_PHOTOS_DICT[1], self.TEST_PHOTOS_DICT[1]]})
        result = self.client.photo.next_previous(self.TEST_PHOTOS[0])
        mock.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertEqual(result["next"][1].get_fields(),
                         self.TEST_PHOTOS_DICT[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.TEST_PHOTOS_DICT[1])
        self.assertEqual(result["previous"][1].get_fields(),
                         self.TEST_PHOTOS_DICT[1])

class TestPhotoTransform(TestPhotos):
    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_transform(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.transform(self.TEST_PHOTOS[0], rotate="90")
        mock.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_transform_id(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        result = self.client.photo.transform("1a", rotate="90")
        mock.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(result.get_fields(), self.TEST_PHOTOS_DICT[1])

    @mock.patch.object(openphoto.OpenPhoto, 'post')
    def test_photo_object_transform(self, mock):
        mock.return_value = self._return_value(self.TEST_PHOTOS_DICT[1])
        photo = self.TEST_PHOTOS[0]
        photo.transform(rotate="90")
        mock.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(photo.get_fields(), self.TEST_PHOTOS_DICT[1])
