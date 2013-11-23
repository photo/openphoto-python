from __future__ import unicode_literals

try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import requests
import trovebox
from tests.functional import test_base

class TestPhotos(test_base.TestBase):
    testcase_name = "photo API"

    def test_list_option(self):
        """
        Check that the photo list options parameter works correctly
        """
        option_tag = "Filter"
        # Assign a photo with a new tag
        self.photos[0].update(tagsAdd=option_tag)

        # Check that the photos can be filtered
        photos = self.client.photos.list(options={"tags": option_tag})
        self.assertEqual(len(photos), 1)
        self.assertEqual(photos[0].id, self.photos[0].id)

        # Put the environment back the way we found it
        photos[0].update(tagsRemove=option_tag)

    # Photo share endpoint is currently not implemented
    @unittest.expectedFailure
    def test_share(self):
        """ Test photo sharing (currently not implemented) """
        self.client.photos.share()

    def test_delete_upload(self):
        """ Test photo deletion and upload """
        # Delete one photo using the Trovebox class, passing in the id
        self.assertTrue(self.client.photo.delete(self.photos[0].id))
        # Delete one photo using the Trovebox class, passing in the object
        self.assertTrue(self.client.photo.delete(self.photos[1]))
        # And another using the Photo object directly
        self.assertTrue(self.photos[2].delete())

        # Check that they're gone
        self.assertEqual(self.client.photos.list(), [])

        # Re-upload the photos, one of them using Base64 encoding
        ret_val = self.client.photo.upload("tests/data/test_photo1.jpg",
                                           title=self.TEST_TITLE)
        self.client.photo.upload("tests/data/test_photo2.jpg",
                                 title=self.TEST_TITLE)
        self.client.photo.upload_encoded("tests/data/test_photo3.jpg",
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

    def test_delete_source(self):
        """ Test that photo source files can be deleted """
        # Upload a new (duplicate) public photo
        photo = self.client.photo.upload("tests/data/test_photo1.jpg",
                                         allowDuplicate=True,
                                         permission=True)
        # Check that the photo can be downloaded
        self.assertEqual(requests.get(photo.pathOriginal).status_code, 200)

        # Delete the source and check that the source file no longer exists
        photo.delete_source()
        self.assertIn(requests.get(photo.pathOriginal).status_code,
                      [403, 404])

        # Put the environment back the way we found it
        photo.delete()

    def test_upload_duplicate(self):
        """ Ensure that duplicate photos are rejected """
        # Attempt to upload a duplicate
        with self.assertRaises(trovebox.TroveboxDuplicateError):
            self.client.photo.upload("tests/data/test_photo1.jpg",
                                     title=self.TEST_TITLE)

        # Check there are still three photos
        self.photos = self.client.photos.list()
        self.assertEqual(len(self.photos), 3)

    def test_upload_from_url(self):
        """ Ensure that a photo can be imported from a URL """
        # Make an existing photo public
        self.photos[0].update(permission=True)
        # Upload a duplicate of an existing photo
        self.client.photo.upload_from_url(self.photos[0].pathOriginal,
                                          allowDuplicate=True)
        # Check there are now four photos
        photos = self.client.photos.list()
        self.assertEqual(len(photos), 4)
        # Check that the new one is a duplicate
        self.assertEqual(photos[0].hash, photos[1].hash)

        # Put the environment back the way we found it
        photos[1].delete()
        self.photos[0].update(permission=False)

    def test_update(self):
        """ Update a photo by editing the title """
        title = "\xfcmlaut" # umlauted umlaut
        # Get a photo and check that it doesn't have the magic title
        photo = self.photos[0]
        self.assertNotEqual(photo.title, title)

        # Add the title to a photo using the Trovebox class
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

        # View at a particular size using the Trovebox class
        photo = self.client.photo.view(photo, returnSizes="9x9")
        self.assertTrue(hasattr(photo, "path9x9"))

        # View at a particular size using the Photo object directly
        photo.view(returnSizes="19x19")
        self.assertTrue(hasattr(photo, "path19x19"))

    def test_next_previous(self):
        """ Test the next/previous links of the middle photo """
        next_prev = self.client.photo.next_previous(self.photos[1],
                                                    sortBy="dateTaken,asc")
        self.assertEqual(next_prev["previous"][0].id, self.photos[0].id)
        self.assertEqual(next_prev["next"][0].id, self.photos[2].id)

        # Do the same using the Photo object directly
        next_prev = self.photos[1].next_previous(sortBy="dateTaken,asc")
        self.assertEqual(next_prev["previous"][0].id, self.photos[0].id)
        self.assertEqual(next_prev["next"][0].id, self.photos[2].id)

    def test_replace(self):
        """ Test that a photo can be replaced with another """
        # Replace the first photo with a copy of the second
        original_hash = self.photos[0].hash
        self.assertNotEqual(original_hash, self.photos[1].hash)
        self.photos[0].replace("tests/data/test_photo2.jpg",
                               allowDuplicate=True)
        # Check that its new hash is correct
        self.assertEqual(self.photos[0].hash, self.photos[1].hash)
        # Put it back using base64 encoding
        self.photos[0].replace_encoded("tests/data/test_photo1.jpg",
                                       allowDuplicate=True)
        self.assertEqual(self.photos[0].hash, original_hash)

    def test_transform(self):
        """ Test photo rotation """
        photo = self.photos[0]
        self.assertEqual(photo.rotation, "0")
        photo = self.client.photo.transform(photo, rotate=90)
        self.assertEqual(photo.rotation, "90")

        # Do the same using the Photo object directly
        photo.transform(rotate=90)
        self.assertEqual(photo.rotation, "180")
