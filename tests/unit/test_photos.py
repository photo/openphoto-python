from __future__ import unicode_literals
import os
import base64
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestPhotos(unittest.TestCase):
    test_host = "test.example.com"
    test_file = os.path.join("tests", "unit", "data", "test_file.txt")
    test_photos_dict = [{"id": "1a", "tags": ["tag1", "tag2"],
                         "totalPages": 1, "totalRows": 2},
                        {"id": "2b", "tags": ["tag3", "tag4"],
                         "totalPages": 1, "totalRows": 2}]
    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)
        self.test_photos = [trovebox.objects.photo.Photo(self.client, photo)
                            for photo in self.test_photos_dict]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestPhotosList(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photos_list(self, mock_get):
        """Check that the photo list is returned correctly"""
        mock_get.return_value = self._return_value(self.test_photos_dict)

        result = self.client.photos.list()
        mock_get.assert_called_with("/photos/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1a")
        self.assertEqual(result[0].tags, ["tag1", "tag2"])
        self.assertEqual(result[1].id, "2b")
        self.assertEqual(result[1].tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_empty_result(self, mock_get):
        """Check that an empty result is transformed into an empty list """
        mock_get.return_value = self._return_value("")
        result = self.client.photos.list()
        mock_get.assert_called_with("/photos/list.json")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_zero_rows(self, mock_get):
        """Check that totalRows=0 is transformed into an empty list """
        mock_get.return_value = self._return_value([{"totalRows": 0}])
        result = self.client.photos.list()
        mock_get.assert_called_with("/photos/list.json")
        self.assertEqual(result, [])

class TestPhotosUpdate(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_update(self, mock_post):
        """Check that multiple photos can be updated"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.update(self.test_photos, title="Test")
        mock_post.assert_called_with("/photos/update.json",
                                     ids=["1a", "2b"], title="Test")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_update_ids(self, mock_post):
        """Check that multiple photos can be updated using their IDs"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.update(["1a", "2b"], title="Test")
        mock_post.assert_called_with("/photos/update.json",
                                     ids=["1a", "2b"], title="Test")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_update_failure(self, mock_post):
        """
        Check that an exception is raised if multiple photos
        cannot be updated
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.photos.update(self.test_photos, title="Test")

class TestPhotosDelete(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_delete(self, mock_post):
        """Check that multiple photos can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.delete(self.test_photos)
        mock_post.assert_called_with("/photos/delete.json", ids=["1a", "2b"])
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_delete_ids(self, mock_post):
        """Check that multiple photos can be deleted using their IDs"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.delete(["1a", "2b"])
        mock_post.assert_called_with("/photos/delete.json", ids=["1a", "2b"])
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_delete_failure(self, mock_post):
        """
        Check that an exception is raised if multiple photos
        cannot be deleted
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.photos.delete(self.test_photos)

class TestPhotoDelete(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete(self, mock_post):
        """Check that a photo can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete(self.test_photos[0])
        mock_post.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete_id(self, mock_post):
        """Check that a photo can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete("1a")
        mock_post.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete_failure(self, mock_post):
        """Check that an exception is raised if a photo cannot be deleted"""
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.photo.delete(self.test_photos[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete(self, mock_post):
        """
        Check that a photo can be deleted when using
        the photo object directly
        """
        mock_post.return_value = self._return_value(True)
        photo = self.test_photos[0]
        result = photo.delete()
        mock_post.assert_called_with("/photo/1a/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(photo.get_fields(), {})
        self.assertEqual(photo.id, None)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete_failure(self, mock_post):
        """
        Check that an exception is raised if a photo cannot be deleted
        when using the photo object directly
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.test_photos[0].delete()

class TestPhotoEdit(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_edit(self, mock_get):
        """Check that a the photo edit endpoint is working"""
        mock_get.return_value = self._return_value({"markup": "<form/>"})
        result = self.client.photo.edit(self.test_photos[0])
        mock_get.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_edit_id(self, mock_get):
        """Check that a the photo edit endpoint is working when using an ID"""
        mock_get.return_value = self._return_value({"markup": "<form/>"})
        result = self.client.photo.edit("1a")
        mock_get.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_object_edit(self, mock_get):
        """
        Check that a the photo edit endpoint is working
        when using the photo object directly
        """
        mock_get.return_value = self._return_value({"markup": "<form/>"})
        result = self.test_photos[0].edit()
        mock_get.assert_called_with("/photo/1a/edit.json")
        self.assertEqual(result, "<form/>")

class TestPhotoReplace(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace(self, _):
        """ If photo.replace gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace(self.test_photos[0], self.test_file)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_id(self, _):
        """ If photo.replace gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace("1a", self.test_file)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_replace(self, _):
        """ If photo.replace gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.test_photos[0].replace(self.test_file)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_encoded(self, _):
        """ If photo.replace_encoded gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace_encoded(self.test_photos[0],
                                              self.test_file)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_encoded_id(self, _):
        """ If photo.replace_encoded gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.replace_encoded("1a", self.test_file)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_replace_encoded(self, _):
        """ If photo.replace_encoded gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.test_photos[0].replace_encoded(photo_file=self.test_file)

class TestPhotoUpdate(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_update(self, mock_post):
        """Check that a photo can be updated"""
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.update(self.test_photos[0], title="Test")
        mock_post.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_update_id(self, mock_post):
        """Check that a photo can be updated using its ID"""
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.update("1a", title="Test")
        mock_post.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_update(self, mock_post):
        """
        Check that a photo can be updated
        when using the photo object directly
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        photo = self.test_photos[0]
        photo.update(title="Test")
        mock_post.assert_called_with("/photo/1a/update.json", title="Test")
        self.assertEqual(photo.get_fields(), self.test_photos_dict[1])

class TestPhotoView(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_view(self, mock_get):
        """Check that a photo can be viewed"""
        mock_get.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.view(self.test_photos[0],
                                        returnSizes="20x20")
        mock_get.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_view_id(self, mock_get):
        """Check that a photo can be viewed using its ID"""
        mock_get.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.view("1a", returnSizes="20x20")
        mock_get.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_object_view(self, mock_get):
        """
        Check that a photo can be viewed
        when using the photo object directly
        """
        mock_get.return_value = self._return_value(self.test_photos_dict[1])
        photo = self.test_photos[0]
        photo.view(returnSizes="20x20")
        mock_get.assert_called_with("/photo/1a/view.json", returnSizes="20x20")
        self.assertEqual(photo.get_fields(), self.test_photos_dict[1])

class TestPhotoUpload(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_upload(self, mock_post):
        """Check that a photo can be uploaded"""
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.upload(self.test_file, title="Test")
        # It's not possible to compare the file object,
        # so check each parameter individually
        endpoint = mock_post.call_args[0]
        title = mock_post.call_args[1]["title"]
        files = mock_post.call_args[1]["files"]
        self.assertEqual(endpoint, ("/photo/upload.json",))
        self.assertEqual(title, "Test")
        self.assertIn("photo", files)
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_upload_encoded(self, mock_post):
        """Check that a photo can be uploaded using Base64 encoding"""
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.upload_encoded(self.test_file, title="Test")
        with open(self.test_file, "rb") as in_file:
            encoded_file = base64.b64encode(in_file.read())
            mock_post.assert_called_with("/photo/upload.json",
                                         photo=encoded_file, title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

class TestPhotoDynamicUrl(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_dynamic_url(self, _):
        """ If photo.dynamic_url gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.dynamic_url(self.test_photos[0])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_dynamic_url_id(self, _):
        """ If photo.dynamic_url gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.photo.dynamic_url("1a")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_object_dynamic_url(self, _):
        """ If photo.dynamic_url gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.test_photos[0].dynamic_url()

class TestPhotoNextPrevious(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_next_previous(self, mock_get):
        """Check that the next/previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0])
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_next_previous_id(self, mock_get):
        """
        Check that the next/previous photos are returned
        when using the photo ID
        """
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1]]})
        result = self.client.photo.next_previous("1a")
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_object_next_previous(self, mock_get):
        """
        Check that the next/previous photos are returned
        when using the photo object directly
        """
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1]]})
        result = self.test_photos[0].next_previous()
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_next(self, mock_get):
        """Check that the next photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]]})
        result = self.client.photo.next_previous(self.test_photos[0])
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertNotIn("previous", result)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_previous(self, mock_get):
        """Check that the previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"previous": [self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0])
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])
        self.assertNotIn("next", result)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_multiple_next_previous(self, mock_get):
        """Check that multiple next/previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0], self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1], self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0])
        mock_get.assert_called_with("/photo/1a/nextprevious.json")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["next"][1].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])
        self.assertEqual(result["previous"][1].get_fields(),
                         self.test_photos_dict[1])

class TestPhotoTransform(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_transform(self, mock_post):
        """Check that a photo can be transformed"""
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.transform(self.test_photos[0], rotate="90")
        mock_post.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_transform_id(self, mock_post):
        """Check that a photo can be transformed using its ID"""
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.transform("1a", rotate="90")
        mock_post.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_transform(self, mock_post):
        """
        Check that a photo can be transformed
        when using the photo object directly
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[1])
        photo = self.test_photos[0]
        photo.transform(rotate="90")
        mock_post.assert_called_with("/photo/1a/transform.json", rotate="90")
        self.assertEqual(photo.get_fields(), self.test_photos_dict[1])

class TestPhotoObject(TestPhotos):
    def test_photo_object_repr_without_id_or_name(self):
        """
        Ensure the string representation on an object includes its class name
        if the ID and Name attributes don't exist.
        """
        photo = trovebox.objects.photo.Photo(self.client, {})
        self.assertEqual(repr(photo), "<Photo>")

    def test_photo_object_repr_with_id(self):
        """ Ensure the string representation on an object includes its id, if present """
        photo = trovebox.objects.photo.Photo(self.client, {"id": "Test ID"})
        self.assertEqual(repr(photo), "<Photo id='Test ID'>")

    def test_photo_object_repr_with_id_and_name(self):
        """ Ensure the string representation on an object includes its name, if present """
        photo = trovebox.objects.photo.Photo(self.client, {"id": "Test ID",
                                                           "name": "Test Name"})
        self.assertEqual(repr(photo), "<Photo name='Test Name'>")

    def test_photo_object_illegal_attribute(self):
        """
        Check that an exception is raised when creating an Photo object
        with an illegal attribute
        """
        with self.assertRaises(ValueError):
            photo = trovebox.objects.photo.Photo(self.client, {"_illegal_attribute": "test"})
