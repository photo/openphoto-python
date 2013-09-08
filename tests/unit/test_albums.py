from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestAlbums(unittest.TestCase):
    test_host = "test.example.com"
    test_photo_dict = {"id": "1a", "tags": ["tag1", "tag2"]}
    test_albums_dict = [{"cover": {"id": "1a", "tags": ["tag1", "tag2"]},
                         "id": "1",
                         "name": "Album 1",
                         "photos": [test_photo_dict],
                         "totalRows": 2},
                        {"cover": {"id": "2b", "tags": ["tag3", "tag4"]},
                         "id": "2",
                         "name": "Album 2",
                         "photos": [test_photo_dict],
                         "totalRows": 2}]
    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)
        self.test_photo = trovebox.objects.photo.Photo(self.client,
                                                       self.test_photo_dict)
        self.test_albums = [trovebox.objects.album.Album(self.client, album)
                            for album in self.test_albums_dict]

    @staticmethod
    def _return_value(result, message="", code=200):
        return {"message": message, "code": code, "result": result}

class TestAlbumsList(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_albums_list(self, mock_get):
        """Check that the album list is returned correctly"""
        mock_get.return_value = self._return_value(self.test_albums_dict)
        result = self.client.albums.list()
        mock_get.assert_called_with("/albums/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].name, "Album 1")
        self.assertEqual(result[1].id, "2")
        self.assertEqual(result[1].name, "Album 2")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_empty_result(self, mock_get):
        """Check that an empty result is transformed into an empty list """
        mock_get.return_value = self._return_value("")
        result = self.client.albums.list()
        mock_get.assert_called_with("/albums/list.json")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_zero_rows(self, mock_get):
        """Check that totalRows=0 is transformed into an empty list """
        mock_get.return_value = self._return_value([{"totalRows": 0}])
        result = self.client.albums.list()
        mock_get.assert_called_with("/albums/list.json")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_albums_list_returns_cover_photos(self, mock_get):
        """Check that the album list returns cover photo objects"""
        mock_get.return_value = self._return_value(self.test_albums_dict)
        result = self.client.albums.list()
        mock_get.assert_called_with("/albums/list.json")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].name, "Album 1")
        self.assertEqual(result[0].cover.id, "1a")
        self.assertEqual(result[0].cover.tags, ["tag1", "tag2"])
        self.assertEqual(result[1].id, "2")
        self.assertEqual(result[1].name, "Album 2")
        self.assertEqual(result[1].cover.id, "2b")
        self.assertEqual(result[1].cover.tags, ["tag3", "tag4"])

class TestAlbumUpdateCover(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_cover_update(self, mock_post):
        """Check that an album cover can be updated"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.cover_update(self.test_albums[0],
                                                self.test_photo, foo="bar")
        mock_post.assert_called_with("/album/1/cover/1a/update.json",
                                     foo="bar")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_cover_update_id(self, mock_post):
        """Check that an album cover can be updated using IDs"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.cover_update("1", "1a", foo="bar")
        mock_post.assert_called_with("/album/1/cover/1a/update.json",
                                     foo="bar")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_cover_update(self, mock_post):
        """Check that an album cover can be updated using the album object directly"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        album = self.test_albums[0]
        album.cover_update(self.test_photo, foo="bar")
        mock_post.assert_called_with("/album/1/cover/1a/update.json",
                                     foo="bar")
        self.assertEqual(album.id, "2")
        self.assertEqual(album.name, "Album 2")
        self.assertEqual(album.cover.id, "2b")
        self.assertEqual(album.cover.tags, ["tag3", "tag4"])

class TestAlbumCreate(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_create(self, mock_post):
        """Check that an album can be created"""
        mock_post.return_value = self._return_value(self.test_albums_dict[0])
        result = self.client.album.create(name="Test", foo="bar")
        mock_post.assert_called_with("/album/create.json", name="Test",
                                     foo="bar")
        self.assertEqual(result.id, "1")
        self.assertEqual(result.name, "Album 1")
        self.assertEqual(result.cover.id, "1a")
        self.assertEqual(result.cover.tags, ["tag1", "tag2"])

class TestAlbumDelete(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_delete(self, mock_post):
        """Check that an album can be deleted"""
        mock_post.return_value = self._return_value(True)
        result = self.client.album.delete(self.test_albums[0])
        mock_post.assert_called_with("/album/1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_delete_id(self, mock_post):
        """Check that an album can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.album.delete("1")
        mock_post.assert_called_with("/album/1/delete.json")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_delete_failure(self, mock_post):
        """Check that an exception is raised if an album cannot be deleted"""
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.album.delete(self.test_albums[0])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_delete(self, mock_post):
        """Check that an album can be deleted using the album object directly"""
        mock_post.return_value = self._return_value(True)
        album = self.test_albums[0]
        result = album.delete()
        mock_post.assert_called_with("/album/1/delete.json")
        self.assertEqual(result, True)
        self.assertEqual(album.get_fields(), {})
        self.assertEqual(album.id, None)
        self.assertEqual(album.name, None)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_delete_failure(self, mock_post):
        """
        Check that an exception is raised if an album cannot be deleted
        when using the album object directly
        """
        mock_post.return_value = self._return_value(False)
        with self.assertRaises(trovebox.TroveboxError):
            self.test_albums[0].delete()

class TestAlbumAddPhotos(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_photos(self, _):
        """ If album.add_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.album.add_photos(self.test_albums[0], ["Photo Objects"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_photos_id(self, _):
        """ If album.add_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.album.add_photos("1", ["Photo Objects"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_add_photos(self, _):
        """ If album.add_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.test_albums[0].add_photos(["Photo Objects"])

class TestAlbumRemovePhotos(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_photos(self, _):
        """ If album.remove_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.album.remove_photos(self.test_albums[0],
                                            ["Photo Objects"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_photos_id(self, _):
        """ If album.remove_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.client.album.remove_photos("1", ["Photo Objects"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_remove_photos(self, _):
        """ If album.remove_photos gets implemented, write a test! """
        with self.assertRaises(NotImplementedError):
            self.test_albums[0].remove_photos(["Photo Objects"])

class TestAlbumUpdate(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_update(self, mock_post):
        """Check that an album can be updated"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.update(self.test_albums[0], name="Test")
        mock_post.assert_called_with("/album/1/update.json", name="Test")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_update_id(self, mock_post):
        """Check that an album can be updated using its ID"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.update("1", name="Test")
        mock_post.assert_called_with("/album/1/update.json", name="Test")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_update(self, mock_post):
        """Check that an album can be updated using the album object directly"""
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        album = self.test_albums[0]
        album.update(name="Test")
        mock_post.assert_called_with("/album/1/update.json", name="Test")
        self.assertEqual(album.id, "2")
        self.assertEqual(album.name, "Album 2")
        self.assertEqual(album.cover.id, "2b")
        self.assertEqual(album.cover.tags, ["tag3", "tag4"])

class TestAlbumView(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_album_view(self, mock_get):
        """Check that an album can be viewed"""
        mock_get.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.view(self.test_albums[0], includeElements=True)
        mock_get.assert_called_with("/album/1/view.json", includeElements=True)
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])
        self.assertEqual(result.photos[0].id, self.test_photo.id)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_album_view_id(self, mock_get):
        """Check that an album can be viewed using its ID"""
        mock_get.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.view("1", includeElements=True)
        mock_get.assert_called_with("/album/1/view.json", includeElements=True)
        self.assertEqual(result.id, "2")
        self.assertEqual(result.name, "Album 2")
        self.assertEqual(result.cover.id, "2b")
        self.assertEqual(result.cover.tags, ["tag3", "tag4"])
        self.assertEqual(result.photos[0].id, self.test_photo.id)

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_album_object_view(self, mock_get):
        """Check that an album can be viewed using the album object directly"""
        mock_get.return_value = self._return_value(self.test_albums_dict[1])
        album = self.test_albums[0]
        album.view(includeElements=True)
        mock_get.assert_called_with("/album/1/view.json", includeElements=True)
        self.assertEqual(album.id, "2")
        self.assertEqual(album.name, "Album 2")
        self.assertEqual(album.cover.id, "2b")
        self.assertEqual(album.cover.tags, ["tag3", "tag4"])
        self.assertEqual(album.photos[0].id, self.test_photo.id)
