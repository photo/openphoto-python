try:
    import unittest2 as unittest
except ImportError:
    import unittest
import openphoto
from . import test_base

class TestAlbums(test_base.TestBase):
    testcase_name = "album API"

    def test_create_delete(self):
        """ Create an album then delete it """
        album_name = "create_delete_album"
        album = self.client.album.create(album_name)

        # Check the return value
        self.assertEqual(album.name, album_name)
        # Check that the album now exists
        self.assertIn(album_name, [a.name for a in self.client.albums.list()])

        # Delete the album
        self.assertTrue(self.client.album.delete(album.id))
        # Check that the album is now gone
        self.assertNotIn(album_name, [a.name for a in self.client.albums.list()])

        # Create it again, and delete it using the Album object
        album = self.client.album.create(album_name)
        self.assertTrue(album.delete())
        # Check that the album is now gone
        self.assertNotIn(album_name, [a.name for a in self.client.albums.list()])

    def test_update(self):
        """ Test that an album can be updated """
        # Update the album using the OpenPhoto class, passing in the album object
        new_name = "New Name"
        self.client.album.update(self.albums[0], name=new_name)

        # Check that the album is updated
        self.albums = self.client.albums.list()
        self.assertEqual(self.albums[0].name, new_name)

        # Update the album using the OpenPhoto class, passing in the album id
        new_name = "Another New Name"
        self.client.album.update(self.albums[0].id, name=new_name)

        # Check that the album is updated
        self.albums = self.client.albums.list()
        self.assertEqual(self.albums[0].name, new_name)

        # Update the album using the Album object directly
        self.albums[0].update(name=self.TEST_ALBUM)

        # Check that the album is updated
        self.albums = self.client.albums.list()
        self.assertEqual(self.albums[0].name, self.TEST_ALBUM)

    def test_view(self):
        """ Test the album view """
        album = self.albums[0]
        self.assertFalse(hasattr(album, "photos"))

        # Get the photos in the album using the Album object directly
        album.view(includeElements=True)
        # Make sure all photos are in the album
        for photo in self.photos:
            self.assertIn(photo.id, [p.id for p in album.photos])

    def test_form(self):
        """ If album.form gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.album.form(None)

    def test_add_photos(self):
        """ If album.add_photos gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.album.add_photos(None, None)

    def test_remove_photos(self):
        """ If album.remove_photos gets implemented, write a test! """
        with self.assertRaises(openphoto.NotImplementedError):
            self.client.album.remove_photos(None, None)
