"""
api_album.py : Trovebox Album API Classes
"""
from .objects import Album

class ApiAlbums(object):
    def __init__(self, client):
        self._client = client

    def list(self, **kwds):
        """ Return a list of Album objects """
        results = self._client.get("/albums/list.json", **kwds)["result"]
        return [Album(self._client, album) for album in results]

class ApiAlbum(object):
    def __init__(self, client):
        self._client = client

    def create(self, name, **kwds):
        """ Create a new album and return it"""
        result = self._client.post("/album/create.json",
                                   name=name, **kwds)["result"]
        return Album(self._client, result)

    def delete(self, album, **kwds):
        """
        Delete an album.
        Returns True if successful.
        Raises an TroveboxError if not.
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
