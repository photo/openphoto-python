"""
api_album.py : Trovebox Album API Classes
"""
from trovebox.objects.album import Album
from trovebox import http
from .api_base import ApiBase

class ApiAlbums(ApiBase):
    """ Definitions of /albums/ API endpoints """
    def list(self, **kwds):
        """
        Endpoint: /albums/list.json

        Returns a list of Album objects.
        """
        albums = self._client.get("/albums/list.json", **kwds)["result"]
        albums = http.result_to_list(albums)
        return [Album(self._client, album) for album in albums]

class ApiAlbum(ApiBase):
    """ Definitions of /album/ API endpoints """
    def cover_update(self, album, photo, **kwds):
        """
        Endpoint: /album/<album_id>/cover/<photo_id>/update.json

        Update the cover photo of an album.
        Returns the updated album object.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        album.cover_update(photo, **kwds)
        return album

    def create(self, name, **kwds):
        """
        Endpoint: /album/create.json

        Creates a new album and returns it.
        """
        result = self._client.post("/album/create.json",
                                   name=name, **kwds)["result"]
        return Album(self._client, result)

    def delete(self, album, **kwds):
        """
        Endpoint: /album/<id>/delete.json

        Deletes an album.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        return album.delete(**kwds)

    # TODO: Should be just "add"
    def add_photos(self, album, photos, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    # TODO: Should be just "remove"
    def remove_photos(self, album, photos, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def update(self, album, **kwds):
        """
        Endpoint: /album/<id>/update.json

        Updates an album with the specified parameters.
        Returns the updated album object.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        album.update(**kwds)
        return album

    def view(self, album, **kwds):
        """
        Endpoint: /album/<id>/view.json

        Requests all properties of an album.
        Returns the requested album object.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        album.view(**kwds)
        return album
