try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from tests.functional import test_base
from trovebox.objects.album import Album

class TestAlbums(test_base.TestBase):
    testcase_name = "album API"

    def test_create_delete(self):
        """ Create an album then delete it """
        album_name = "create_delete_album"
        album = self.client.album.create(album_name)

        # Check the return value
        self.assertEqual(album.name, album_name)
        # Check that the album now exists
        self.assertIn(album_name,
                      [a.name for a in self.client.albums.list()])

        # Delete the album
        self.assertTrue(self.client.album.delete(album.id))
        # Check that the album is now gone
        self.assertNotIn(album_name,
                         [a.name for a in self.client.albums.list()])

        # Create it again, and delete it using the Album object
        album = self.client.album.create(album_name)
        self.assertTrue(album.delete())
        # Check that the album is now gone
        self.assertNotIn(album_name,
                         [a.name for a in self.client.albums.list()])

    def test_update(self):
        """ Test that an album can be updated """
        # Update the album using the Trovebox class,
        # passing in the album object
        new_name = "New Name"
        self.client.album.update(self.albums[0], name=new_name)

        # Check that the album is updated
        self.albums = self.client.albums.list()
        self.assertEqual(self.albums[0].name, new_name)

        # Update the album using the Trovebox class, passing in the album id
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

    @unittest.skipIf(test_base.get_test_server_api() == 1,
                     "update_cover was introduced in APIv2")
    def test_update_cover(self):
        """ Test that an album cover can be updated """
        self.albums[0].cover_update(self.photos[0])
        self.assertNotEqual(self.albums[0].cover.id, self.photos[1].id)
        self.albums[0].cover_update(self.photos[1])
        self.assertEqual(self.albums[0].cover.id, self.photos[1].id)

    @unittest.skipIf(test_base.get_test_server_api() == 1,
                     "includeElements was introduced in APIv2")
    def test_view(self):
        """ Test the album view """
        # Do a view() with includeElements=False, using a fresh Album object
        album = Album(self.client, {"id": self.albums[0].id})
        album.view()
        # Make sure there are no photos reported
        self.assertEqual(album.photos, None)

        # Get the photos with includeElements=True
        album.view(includeElements=True)
        # Make sure all photos are in the album
        for photo in self.photos:
            self.assertIn(photo.id, [p.id for p in album.photos])

    def test_add_remove(self):
        """ Test that photos can be added and removed from an album """
        # Make sure all photos are in the album
        album = self.albums[0]
        album.view(includeElements=True)
        for photo in self.photos:
            self.assertIn(photo.id, [p.id for p in album.photos])

        # Remove two photos and check that they're gone
        album.remove(self.photos[:2])
        album.view(includeElements=True)
        self.assertEqual([p.id for p in album.photos], [self.photos[2].id])

        # Add a photo and check that it's there
        album.add(self.photos[1])
        album.view(includeElements=True)
        self.assertNotIn(self.photos[0].id, [p.id for p in album.photos])
        self.assertIn(self.photos[1].id, [p.id for p in album.photos])
        self.assertIn(self.photos[2].id, [p.id for p in album.photos])

        # Put the environment back the way we found it
        album.add(self.photos[0])
