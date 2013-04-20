import unittest
import openphoto
import test_base

class TestPhotos(test_base.TestBase):
    def test_delete_upload(self):
        """ Test photo deletion and upload """
        # Delete one photo using the OpenPhoto class, passing in the id
        self.assertTrue(self.client.photo.delete(self.photos[0].id))
        # Delete one photo using the OpenPhoto class, passing in the object
        self.assertTrue(self.client.photo.delete(self.photos[1]))
        # And another using the Photo object directly
        self.assertTrue(self.photos[2].delete())

        # Check that they're gone
        self.assertEqual(self.client.photos.list(), [])

        # Re-upload the photos, one of them using Bas64 encoding
        ret_val = self.client.photo.upload("tests/test_photo1.jpg",
                                           title=self.TEST_TITLE)
        self.client.photo.upload("tests/test_photo2.jpg",
                                 title=self.TEST_TITLE)
        self.client.photo.upload_encoded("tests/test_photo3.jpg",
                                         title=self.TEST_TITLE)

        # Check there are now three photos with the correct titles
        self.photos = self.client.photos.list()
        self.assertEqual(len(self.photos), 3)
        for photo in self.photos:
            self.assertEqual(photo.title, self.TEST_TITLE)

        # Check that the upload return value was correct
        pathOriginals = [photo.pathOriginal for photo in self.photos]
        self.assertIn(ret_val.pathOriginal, pathOriginals)

        # Delete all photos in one go
        self.assertTrue(self.client.photos.delete(self.photos))

        # Check they're gone
        self.photos = self.client.photos.list()
        self.assertEqual(len(self.photos), 0)

        # Regenerate the original test photos
        self._delete_all()
        self._create_test_photos()

    def test_edit(self):
        """ Check that the edit request returns an HTML form """
        # Test using the OpenPhoto class
        html = self.client.photo.edit(self.photos[0])
        self.assertIn("<form", html.lower())

        # And the Photo object directly
        html = self.photos[0].edit()
        self.assertIn("<form", html.lower())

    def test_upload_duplicate(self):
        """ Ensure that duplicate photos are rejected """
        # Attempt to upload a duplicate
        with self.assertRaises(openphoto.OpenPhotoDuplicateError):
            self.client.photo.upload("tests/test_photo1.jpg",
                                     title=self.TEST_TITLE)

        # Check there are still three photos
        self.photos = self.client.photos.list()
        self.assertEqual(len(self.photos), 3)

    def test_update(self):
        """ Update a photo by editing the title """
        title = u"\xfcmlaut" # umlauted umlaut
        # Get a photo and check that it doesn't have the magic title
        photo = self.photos[0]
        self.assertNotEqual(photo.title, title)

        # Add the title to a photo using the OpenPhoto class
        ret_val = self.client.photo.update(photo, title=title)

        # Check that it's there
        self.photos = self.client.photos.list()
        photo = self.photos[0]
        self.assertEqual(photo.title, title)

        # Check that the return value was correct
        self.assertEqual(ret_val.pathOriginal, photo.pathOriginal)

        # Revert the title using the Photo object directly
        photo.update(title=self.TEST_TITLE)

        # Check that it's gone back
        self.photos = self.client.photos.list()
        self.assertEqual(self.photos[0].title, self.TEST_TITLE)

    def test_update_multiple(self):
        """ Update multiple photos by adding tags """
        tag_id = "update_photo_tag"
        # Get a couple of photos
        photos = self.photos[:2]

        # Add the tag using a list of photo objects
        self.client.photos.update(photos, tagsAdd=tag_id)

        # Check that it's there
        for photo in self.client.photos.list()[:2]:
            self.assertIn(tag_id, photo.tags)

        # Remove the tags using a list of photo ids
        self.client.photos.update([photo.id for photo in photos],
                                  tagsRemove=tag_id)

    def test_view(self):
        """ Test photo view """
        # Check that our magic sizes aren't present
        photo = self.photos[0]
        self.assertFalse(hasattr(photo, "path9x9"))
        self.assertFalse(hasattr(photo, "path19x19"))

        # View at a particular size using the OpenPhoto class
        photo = self.client.photo.view(photo, returnSizes="9x9")
        self.assertTrue(hasattr(photo, "path9x9"))

        # View at a particular size using the Photo object directly
        photo.view(returnSizes="19x19")
        self.assertTrue(hasattr(photo, "path19x19"))

    def test_next_previous(self):
        """ Test the next/previous links of the middle photo """
        next_prev = self.client.photo.next_previous(self.photos[1])
        self.assertEqual(next_prev["previous"][0].id, self.photos[0].id)
        self.assertEqual(next_prev["next"][0].id, self.photos[2].id)

        # Do the same using the Photo object directly
        next_prev = self.photos[1].next_previous()
        self.assertEqual(next_prev["previous"][0].id, self.photos[0].id)
        self.assertEqual(next_prev["next"][0].id, self.photos[2].id)

    def test_replace(self):
        """ If photo.replace gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.photo.replace(None, None)

    def test_replace_encoded(self):
        """ If photo.replace_encoded gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.photo.replace_encoded(None, None)

    def test_dynamic_url(self):
        """ If photo.dynamic_url gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.photo.dynamic_url(None)

    def test_transform(self):
        """ If photo.transform gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.photo.transform(None)
