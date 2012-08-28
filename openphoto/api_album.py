from openphoto_http import OpenPhotoHttp, OpenPhotoError
from objects import Album

class ApiAlbum(OpenPhotoHttp):
    def album_create(self, name, **kwds):
        """ Create a new album and return it"""
        result = self.post("/album/create.json", name=name, **kwds)["result"]
        return Album(self, result)

    def album_delete(self, album_id, **kwds):
        """ Delete an album """
        album = Album(self, {"id": album_id})
        album.delete(**kwds)
        
    def album_form(self, album_id, **kwds):
        raise NotImplementedError()

    def album_add_photos(self, album_id, photo_ids, **kwds):
        raise NotImplementedError()

    def album_remove_photos(self, album_id, photo_ids, **kwds):
        raise NotImplementedError()

    def albums_list(self, **kwds):
        """ Return a list of Album objects """
        results = self.get("/albums/list.json", **kwds)["result"]
        return [Album(self, album) for album in results]

    def album_update(self, album_id, **kwds):
        """ Update an album """
        album = Album(self, {"id": album_id})
        album.update(**kwds)
        # Don't return the album, since the API doesn't give us the modified album
