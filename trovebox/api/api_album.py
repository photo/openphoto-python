"""
api_album.py : Trovebox Album API Classes
"""
from trovebox.objects.album import Album
from trovebox import http
from .api_base import ApiBase

class ApiAlbums(ApiBase):
    """ Definitions of /albums/ API endpoints """
    def list(self, **kwds):
        """ Return a list of Album objects """
        albums = self._client.get("/albums/list.json", **kwds)["result"]
        albums = http.result_to_list(albums)
        return [Album(self._client, album) for album in albums]

class ApiAlbum(ApiBase):
    """ Definitions of /album/ API endpoints """
    def create(self, name, **kwds):
        """ Create a new album and return it"""
        result = self._client.post("/album/create.json",
                                   name=name, **kwds)["result"]
        return Album(self._client, result)

    def delete(self, album, **kwds):
        """
        Delete an album.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        return album.delete(**kwds)

    def form(self, album, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def add_photos(self, album, photos, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def remove_photos(self, album, photos, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def update(self, album, **kwds):
        """ Update an album """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        album.update(**kwds)
        return album

    def view(self, album, **kwds):
        """
        View an album's contents.
        Returns the requested album object.
        """
        if not isinstance(album, Album):
            album = Album(self._client, {"id": album})
        album.view(**kwds)
        return album
