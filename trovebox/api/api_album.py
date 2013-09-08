"""
api_album.py : Trovebox Album API Classes
"""
import collections

from trovebox.objects.trovebox_object import TroveboxObject
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

    def add(self, album, objects, object_type=None, **kwds):
        """
        Endpoint: /album/<id>/<type>/add.json

        Add objects (eg. Photos) to an album.
        The objects are a list of either IDs or Trovebox objects.
        If Trovebox objects are used, the object type is inferred
        automatically.
        Returns True if the album was updated successfully.
        """
        return self._add_remove("add", album, objects, object_type,
                                **kwds)

    def remove(self, album, objects, object_type=None, **kwds):
        """
        Endpoint: /album/<id>/<type>/remove.json

        Remove objects (eg. Photos) to an album.
        The objects are a list of either IDs or Trovebox objects.
        If Trovebox objects are used, the object type is inferred
        automatically.
        Returns True if the album was updated successfully.
        """
        return self._add_remove("remove", album, objects, object_type,
                                **kwds)

    def _add_remove(self, action, album, objects, object_type=None,
                    **kwds):
        """Common code for the add and remove endpoints."""
        # Extract the id of the album
        if isinstance(album, Album):
            album = album.id

        # Ensure we have an iterable of objects
        if not isinstance(objects, collections.Iterable):
            objects = [objects]

        # Extract the type of the objects
        if object_type is None:
            object_type = objects[0].get_type()

        for i, obj in enumerate(objects):
            if isinstance(obj, TroveboxObject):
                # Ensure all objects are the same type
                if obj.get_type() != object_type:
                    raise ValueError("Not all objects are of type '%s'"
                                     % object_type)
                # Extract the ids of the objects
                objects[i] = obj.id

        return self._client.post("/album/%s/%s/%s.json" %
                                 (album, object_type, action),
                                 ids=objects, **kwds)["result"]

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
