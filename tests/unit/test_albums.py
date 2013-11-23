from __future__ import unicode_literals
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestAlbums(unittest.TestCase):
    test_host = "test.example.com"
    test_photos_dict = [{"id": "1a", "tags": ["tag1", "tag2"]},
                        {"id": "2b", "tags": ["tag3", "tag4"]}]
    test_albums_dict = [{"cover": {"id": "1a", "tags": ["tag1", "tag2"]},
                         "id": "1",
                         "name": "Album 1",
                         "photos": [test_photos_dict[0]],
                         "totalRows": 2},
                        {"cover": {"id": "2b", "tags": ["tag3", "tag4"]},
                         "id": "2",
                         "name": "Album 2",
                         "photos": [test_photos_dict[1]],
                         "totalRows": 2}]
    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)
        self.test_photos = [trovebox.objects.photo.Photo(self.client, photo)
                            for photo in self.test_photos_dict]
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
        result = self.client.albums.list(foo="bar")
        mock_get.assert_called_with("/albums/list.json", foo="bar")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].name, "Album 1")
        self.assertEqual(result[1].id, "2")
        self.assertEqual(result[1].name, "Album 2")

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_empty_result(self, mock_get):
        """Check that an empty result is transformed into an empty list """
        mock_get.return_value = self._return_value("")
        result = self.client.albums.list(foo="bar")
        mock_get.assert_called_with("/albums/list.json", foo="bar")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_zero_rows(self, mock_get):
        """Check that totalRows=0 is transformed into an empty list """
        mock_get.return_value = self._return_value([{"totalRows": 0}])
        result = self.client.albums.list(foo="bar")
        mock_get.assert_called_with("/albums/list.json", foo="bar")
        self.assertEqual(result, [])

    @mock.patch.object(trovebox.Trovebox, 'get')
    def test_albums_list_returns_cover_photos(self, mock_get):
        """Check that the album list returns cover photo objects"""
        mock_get.return_value = self._return_value(self.test_albums_dict)
        result = self.client.albums.list(foo="bar")
        mock_get.assert_called_with("/albums/list.json", foo="bar")
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
                                                self.test_photos[0],
                                                foo="bar")
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
        album.cover_update(self.test_photos[1], foo="bar")
        mock_post.assert_called_with("/album/1/cover/2b/update.json",
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
        result = self.client.album.delete(self.test_albums[0], foo="bar")
        mock_post.assert_called_with("/album/1/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_delete_id(self, mock_post):
        """Check that an album can be deleted using its ID"""
        mock_post.return_value = self._return_value(True)
        result = self.client.album.delete("1", foo="bar")
        mock_post.assert_called_with("/album/1/delete.json", foo="bar")
        self.assertEqual(result, True)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_delete(self, mock_post):
        """Check that an album can be deleted using the album object directly"""
        mock_post.return_value = self._return_value(True)
        album = self.test_albums[0]
        result = album.delete(foo="bar")
        mock_post.assert_called_with("/album/1/delete.json", foo="bar")
        self.assertEqual(result, True)
        self.assertEqual(album.get_fields(), {})
        self.assertEqual(album.id, None)
        self.assertEqual(album.name, None)

class TestAlbumAdd(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add(self, mock_post):
        """ Check that photos can be added to an album """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.add(self.test_albums[0], self.test_photos,
                                       foo="bar")
        mock_post.assert_called_with("/album/1/photo/add.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_id(self, mock_post):
        """ Check that photos can be added to an album using IDs """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.add(self.test_albums[0].id,
                                       objects=["1a", "2b"],
                                       object_type="photo",
                                       foo="bar")
        mock_post.assert_called_with("/album/1/photo/add.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_add(self, mock_post):
        """
        Check that photos can be added to an album using the
        album object directly
        """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        album = self.test_albums[0]
        album.add(self.test_photos, foo="bar")
        mock_post.assert_called_with("/album/1/photo/add.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(album.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_single(self, mock_post):
        """ Check that a single photo can be added to an album """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        self.test_albums[0].add(self.test_photos[0], foo="bar")
        mock_post.assert_called_with("/album/1/photo/add.json",
                                     ids=["1a"], foo="bar")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_invalid_type(self, _):
        """
        Check that an exception is raised if an invalid object is added
        to an album.
        """
        with self.assertRaises(AttributeError):
            self.test_albums[0].add([object()])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_add_multiple_types(self, _):
        """
        Check that an exception is raised if multiple types are added
        to an album.
        """
        with self.assertRaises(ValueError):
            self.test_albums[0].add(self.test_photos+self.test_albums)

class TestAlbumRemovePhotos(TestAlbums):
    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove(self, mock_post):
        """ Check that photos can be removed from an album """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.remove(self.test_albums[0], self.test_photos,
                                          foo="bar")
        mock_post.assert_called_with("/album/1/photo/remove.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_id(self, mock_post):
        """ Check that photos can be removed from an album using IDs """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        result = self.client.album.remove(self.test_albums[0].id,
                                          objects=["1a", "2b"],
                                          object_type="photo",
                                          foo="bar")
        mock_post.assert_called_with("/album/1/photo/remove.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(result.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_object_remove(self, mock_post):
        """
        Check that photos can be removed from an album using the
        album object directly
        """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        album = self.test_albums[0]
        album.remove(self.test_photos, foo="bar")
        mock_post.assert_called_with("/album/1/photo/remove.json",
                                     ids=["1a", "2b"], foo="bar")
        self.assertEqual(album.id, self.test_albums[1].id)

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_single(self, mock_post):
        """ Check that a single photo can be removed from an album """
        mock_post.return_value = self._return_value(self.test_albums_dict[1])
        self.test_albums[0].remove(self.test_photos[0], foo="bar")
        mock_post.assert_called_with("/album/1/photo/remove.json",
                                     ids=["1a"], foo="bar")

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_invalid_type(self, _):
        """
        Check that an exception is raised if an invalid object is removed
        from an album.
        """
        with self.assertRaises(AttributeError):
            self.test_albums[0].remove([object()])

    @mock.patch.object(trovebox.Trovebox, 'post')
    def test_album_remove_multiple_types(self, _):
        """
        Check that an exception is raised if multiple types are removed
        from an album.
        """
        with self.assertRaises(ValueError):
            self.test_albums[0].remove(self.test_photos+self.test_albums)

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
        self.assertEqual(result.photos[0].id, self.test_photos[1].id)

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
        self.assertEqual(result.photos[0].id, self.test_photos[1].id)

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
        self.assertEqual(album.photos[0].id, self.test_photos[1].id)

class TestAlbumMisc(TestAlbums):
    def test_update_fields_with_no_cover(self):
        """Check that an album object can be updated with no cover"""
        album = self.test_albums[0]
        album.cover = None
        album.photos = None
        # Check that no exception is raised
        album._update_fields_with_objects()
