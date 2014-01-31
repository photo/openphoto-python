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

        result = self.client.photos.list(foo="bar")
        mock_get.assert_called_with("/photos/list.json", foo="bar")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1a")
        self.assertEqual(result[0].tags, ["tag1", "tag2"])
        self.assertEqual(result[1].id, "2b")
        self.assertEqual(result[1].tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_empty_result(self, mock_get):
        """Check that an empty result is transformed into an empty list """
        mock_get.return_value = self._return_value("")
        result = self.client.photos.list(foo="bar")
        mock_get.assert_called_with("/photos/list.json", foo="bar")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_zero_rows(self, mock_get):
        """Check that totalRows=0 is transformed into an empty list """
        mock_get.return_value = self._return_value([{"totalRows": 0}])
        result = self.client.photos.list(foo="bar")
        mock_get.assert_called_with("/photos/list.json", foo="bar")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_options(self, mock_get):
        """Check that the activity list options are applied properly"""
        mock_get.return_value = self._return_value(self.test_photos_dict)
        self.client.photos.list(options={"foo": "bar",
                                         "test1": "test2"},
                                foo="bar")
        # Dict element can be any order
        self.assertIn(mock_get.call_args[0],
                      [("/photos/foo-bar/test1-test2/list.json",),
                       ("/photos/test1-test2/foo-bar/list.json",)])
        self.assertEqual(mock_get.call_args[1], {"foo": "bar"})

class TestPhotosShare(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_share(self, mock_post):
        self.client.photos.share(options={"foo": "bar",
                                          "test1": "test2"},
                                 foo="bar")
        # Dict element can be any order
        self.assertIn(mock_post.call_args[0],
                      [("/photos/foo-bar/test1-test2/share.json",),
                       ("/photos/test1-test2/foo-bar/share.json",)])
        self.assertEqual(mock_post.call_args[1], {"foo": "bar"})

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

class TestPhotosDelete(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_delete(self, mock_post):
        """Check that multiple photos can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.delete(self.test_photos, foo="bar")
        mock_post.assert_called_with("/photos/delete.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photos_delete_ids(self, mock_post):
        """Check that multiple photos can be deleted using their IDs"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photos.delete(["1a", "2b"], foo="bar")
        mock_post.assert_called_with("/photos/delete.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result, True)

class TestPhotoDelete(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete(self, mock_post):
        """Check that a photo can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete(self.test_photos[0], foo="bar")
        mock_post.assert_called_with("/photo/1a/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete_id(self, mock_post):
        """Check that a photo can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete("1a", foo="bar")
        mock_post.assert_called_with("/photo/1a/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete(self, mock_post):
        """
        Check that a photo can be deleted when using
        the photo object directly
        """
        mock_post.return_value = self._return_value(True)
        photo = self.test_photos[0]
        result = photo.delete(foo="bar")
        mock_post.assert_called_with("/photo/1a/delete.json", foo="bar")
        self.assertEqual(result, True)
        self.assertEqual(photo.get_fields(), {})
        self.assertEqual(photo.id, None)

class TestPhotoDeleteSource(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete_source(self, mock_post):
        """Check that photo source files can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete_source(self.test_photos[0], foo="bar")
        mock_post.assert_called_with("/photo/1a/source/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_delete_source_id(self, mock_post):
        """Check that photo source files can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.photo.delete_source("1a", foo="bar")
        mock_post.assert_called_with("/photo/1a/source/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete_source(self, mock_post):
        """
        Check that photo source files can be deleted when using
        the photo object directly
        """
        mock_post.return_value = self._return_value(True)
        photo = self.test_photos[0]
        result = photo.delete_source(foo="bar")
        mock_post.assert_called_with("/photo/1a/source/delete.json", foo="bar")
        self.assertEqual(result, True)

class TestPhotoReplace(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace(self, mock_post):
        """Check that an existing photo can be replaced"""
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace(self.test_photos[1],
                                           self.test_file, title="Test")
        # It's not possible to compare the file object,
        # so check each parameter individually
        endpoint = mock_post.call_args[0]
        title = mock_post.call_args[1]["title"]
        files = mock_post.call_args[1]["files"]
        self.assertEqual(endpoint,
                         ("/photo/%s/replace.json" % self.test_photos[1].id,))
        self.assertEqual(title, "Test")
        self.assertIn("photo", files)
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_id(self, mock_post):
        """Check that an existing photo can be replaced using its ID"""
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace(self.test_photos[1].id,
                                           self.test_file, title="Test")
        # It's not possible to compare the file object,
        # so check each parameter individually
        endpoint = mock_post.call_args[0]
        title = mock_post.call_args[1]["title"]
        files = mock_post.call_args[1]["files"]
        self.assertEqual(endpoint,
                         ("/photo/%s/replace.json" % self.test_photos[1].id,))
        self.assertEqual(title, "Test")
        self.assertIn("photo", files)
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_replace(self, mock_post):
        """
        Check that an existing photo can be replaced when using the
        Photo object directly.
        """
        photo_id = self.test_photos[1].id
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        self.test_photos[1].replace(self.test_file, title="Test")
        # It's not possible to compare the file object,
        # so check each parameter individually
        endpoint = mock_post.call_args[0]
        title = mock_post.call_args[1]["title"]
        files = mock_post.call_args[1]["files"]
        self.assertEqual(endpoint, ("/photo/%s/replace.json" % photo_id,))
        self.assertEqual(title, "Test")
        self.assertIn("photo", files)
        self.assertEqual(self.test_photos[1].get_fields(),
                         self.test_photos_dict[0])

class TestPhotoReplaceEncoded(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_encoded(self, mock_post):
        """
        Check that a photo can be uploaded using Base64 encoding to
        replace an existing photo.
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace_encoded(self.test_photos[1],
                                                   self.test_file, title="Test")
        with open(self.test_file, "rb") as in_file:
            encoded_file = base64.b64encode(in_file.read())
            mock_post.assert_called_with("/photo/%s/replace.json"
                                         % self.test_photos[1].id,
                                         photo=encoded_file, title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_encoded_id(self, mock_post):
        """
        Check that a photo can be uploaded using Base64 encoding to
        replace an existing photo using its ID.
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace_encoded(self.test_photos[1].id,
                                                   self.test_file, title="Test")
        with open(self.test_file, "rb") as in_file:
            encoded_file = base64.b64encode(in_file.read())
            mock_post.assert_called_with("/photo/%s/replace.json"
                                         % self.test_photos[1].id,
                                         photo=encoded_file, title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_replace_encoded(self, mock_post):
        """
        Check that a photo can be uploaded using Base64 encoding to
        replace an existing photo when using the Photo object directly.
        """
        photo_id = self.test_photos[1].id
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        self.test_photos[1].replace_encoded(self.test_file, title="Test")
        with open(self.test_file, "rb") as in_file:
            encoded_file = base64.b64encode(in_file.read())
            mock_post.assert_called_with("/photo/%s/replace.json"
                                         % photo_id,
                                         photo=encoded_file, title="Test")
        self.assertEqual(self.test_photos[1].get_fields(),
                         self.test_photos_dict[0])

class TestPhotoReplaceFromUrl(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_replace_from_url(self, mock_post):
        """
        Check that a photo can be imported from a url to
        replace an existing photo.
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace_from_url(self.test_photos[1],
                                                    "test_url", title="Test")
        mock_post.assert_called_with("/photo/%s/replace.json"
                                     % self.test_photos[1].id,
                                     photo="test_url", title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_id_replace_from_url(self, mock_post):
        """
        Check that a photo can be imported from a url to
        replace an existing photo using its ID.
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.replace_from_url(self.test_photos[1].id,
                                                    "test_url", title="Test")
        mock_post.assert_called_with("/photo/%s/replace.json"
                                     % self.test_photos[1].id,
                                     photo="test_url", title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_replace_from_url(self, mock_post):
        """
        Check that a photo can be imported from a url to
        replace an existing photo when using the Photo object directly.
        """
        photo_id = self.test_photos[1].id
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        self.test_photos[1].replace_from_url("test_url", title="Test")
        mock_post.assert_called_with("/photo/%s/replace.json"
                                     % photo_id,
                                     photo="test_url", title="Test")
        self.assertEqual(self.test_photos[1].get_fields(),
                         self.test_photos_dict[0])

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
                                        options={"foo": "bar",
                                                 "test1": "test2"},
                                        returnSizes="20x20")
        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/foo-bar/test1-test2/view.json",),
                       ("/photo/1a/test1-test2/foo-bar/view.json",)])
        self.assertEqual(mock_get.call_args[1], {"returnSizes": "20x20"})
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_view_id(self, mock_get):
        """Check that a photo can be viewed using its ID"""
        mock_get.return_value = self._return_value(self.test_photos_dict[1])
        result = self.client.photo.view("1a",
                                        options={"foo": "bar",
                                                 "test1": "test2"},
                                        returnSizes="20x20")

        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/foo-bar/test1-test2/view.json",),
                       ("/photo/1a/test1-test2/foo-bar/view.json",)])
        self.assertEqual(mock_get.call_args[1], {"returnSizes": "20x20"})
        self.assertEqual(result.get_fields(), self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_object_view(self, mock_get):
        """
        Check that a photo can be viewed
        when using the photo object directly
        """
        mock_get.return_value = self._return_value(self.test_photos_dict[1])
        photo = self.test_photos[0]
        photo.view(returnSizes="20x20", options={"foo": "bar",
                                                 "test1": "test2"})

        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/foo-bar/test1-test2/view.json",),
                       ("/photo/1a/test1-test2/foo-bar/view.json",)])
        self.assertEqual(mock_get.call_args[1], {"returnSizes": "20x20"})
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

class TestPhotoUploadEncoded(TestPhotos):
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

class TestPhotoUploadFromUrl(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_upload_from_url(self, mock_post):
        """
        Check that a photo can be imported from a url.
        """
        mock_post.return_value = self._return_value(self.test_photos_dict[0])
        result = self.client.photo.upload_from_url("test_url", title="Test")
        mock_post.assert_called_with("/photo/upload.json",
                                     photo="test_url", title="Test")
        self.assertEqual(result.get_fields(), self.test_photos_dict[0])

class TestPhotoNextPrevious(TestPhotos):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_next_previous(self, mock_get):
        """Check that the next/previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0],
                                                 options={"foo": "bar",
                                                          "test1": "test2"},
                                                 foo="bar")
        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/nextprevious/foo-bar/test1-test2.json",),
                       ("/photo/1a/nextprevious/test1-test2/foo-bar.json",)])
        self.assertEqual(mock_get.call_args[1], {"foo": "bar"})
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
        result = self.client.photo.next_previous("1a",
                                                 options={"foo": "bar",
                                                          "test1": "test2"},
                                                 foo="bar")
        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/nextprevious/foo-bar/test1-test2.json",),
                       ("/photo/1a/nextprevious/test1-test2/foo-bar.json",)])
        self.assertEqual(mock_get.call_args[1], {"foo": "bar"})
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
        result = self.test_photos[0].next_previous(options={"foo": "bar",
                                                            "test1": "test2"},
                                                   foo="bar")
        # Dict elemet can be in any order
        self.assertIn(mock_get.call_args[0],
                      [("/photo/1a/nextprevious/foo-bar/test1-test2.json",),
                       ("/photo/1a/nextprevious/test1-test2/foo-bar.json",)])
        self.assertEqual(mock_get.call_args[1], {"foo": "bar"})
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_next(self, mock_get):
        """Check that the next photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0]]})
        result = self.client.photo.next_previous(self.test_photos[0],
                                                 foo="bar")
        mock_get.assert_called_with("/photo/1a/nextprevious.json",
                                    foo="bar")
        self.assertEqual(result["next"][0].get_fields(),
                         self.test_photos_dict[0])
        self.assertNotIn("previous", result)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_previous(self, mock_get):
        """Check that the previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"previous": [self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0],
                                                 foo="bar")
        mock_get.assert_called_with("/photo/1a/nextprevious.json",
                                    foo="bar")
        self.assertEqual(result["previous"][0].get_fields(),
                         self.test_photos_dict[1])
        self.assertNotIn("next", result)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_photo_multiple_next_previous(self, mock_get):
        """Check that multiple next/previous photos are returned"""
        mock_get.return_value = self._return_value(
            {"next": [self.test_photos_dict[0], self.test_photos_dict[0]],
             "previous": [self.test_photos_dict[1], self.test_photos_dict[1]]})
        result = self.client.photo.next_previous(self.test_photos[0],
                                                 foo="bar")
        mock_get.assert_called_with("/photo/1a/nextprevious.json",
                                    foo="bar")
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

    def test_photo_object_repr_with_unicode_id(self):
        """ Ensure that a unicode id is correctly represented """
        photo = trovebox.objects.photo.Photo(self.client, {"id": "\xfcmlaut"})
        self.assertIn(repr(photo), [b"<Photo id='\xc3\xbcmlaut'>", "<Photo id='\xfcmlaut'>"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_create_attribute(self, _):
        """
        Check that attributes are created when creating a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"attribute": "test"})
        self.assertEqual(photo.attribute, "test")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete_attribute(self, _):
        """
        Check that attributes are deleted when creating a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"attribute": "test"})
        photo.delete()
        with self.assertRaises(AttributeError):
            value = photo.attribute
        self.assertEqual(photo.get_fields(), {})

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_update_attribute(self, mock_post):
        """
        Check that attributes are updated when creating a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"attribute": "test"})
        mock_post.return_value = self._return_value({"attribute": "test2"})
        photo.update()
        self.assertEqual(photo.attribute, "test2")
        self.assertEqual(photo.get_fields(), {"attribute": "test2"})

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_create_illegal_attribute(self, _):
        """
        Check that illegal attributes are ignored when creating a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"_illegal_attribute": "test"})
        # The object's attribute shouldn't be created
        with self.assertRaises(AttributeError):
            value = photo._illegal_attribute
        # The field dict gets created correctly, however.
        self.assertEqual(photo.get_fields(), {"_illegal_attribute": "test"})

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_delete_illegal_attribute(self, _):
        """
        Check that illegal attributes are ignored when deleting a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"_illegal_attribute": "test"})
        photo.delete()
        with self.assertRaises(AttributeError):
            value = photo._illegal_attribute
        self.assertEqual(photo.get_fields(), {})

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_photo_object_update_illegal_attribute(self, mock_post):
        """
        Check that illegal attributes are ignored when updating a
        Photo object
        """
        photo = trovebox.objects.photo.Photo(self.client, {"_illegal_attribute": "test"})
        mock_post.return_value = self._return_value({"_illegal_attribute": "test2"})
        photo.update()
        # The object's attribute shouldn't be created
        with self.assertRaises(AttributeError):
            value = photo._illegal_attribute
        # The field dict gets updated correctly, however.
        self.assertEqual(photo.get_fields(), {"_illegal_attribute": "test2"})
