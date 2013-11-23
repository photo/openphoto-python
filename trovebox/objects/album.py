"""
Representation of an Album object
"""
from .trovebox_object import TroveboxObject
from .photo import Photo

class Album(TroveboxObject):
    """ Representation of an Album object """
    _type = "album"

    def __init__(self, client, json_dict):
        self.photos = None
        self.cover = None
        TroveboxObject.__init__(self, client, json_dict)
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the cover with a photo object
        if isinstance(self.cover, dict):
            self.cover = Photo(self._client, self.cover)

        # Update the photo list with photo objects
        try:
            for i, photo in enumerate(self.photos):
                if isinstance(photo, dict):
                    self.photos[i] = Photo(self._client, photo)
        except (AttributeError, TypeError):
            pass # No photos, or not a list

    def cover_update(self, photo, **kwds):
        """
        Endpoint: /album/<album_id>/cover/<photo_id>/update.json

        Update the cover photo of this album.
        """
        result = self._client.album.cover_update(self, photo, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()

    def delete(self, **kwds):
        """
        Endpoint: /album/<id>/delete.json

        Deletes this album.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._client.album.delete(self, **kwds)
        self._delete_fields()
        return result

    def add(self, objects, object_type=None, **kwds):
        """
        Endpoint: /album/<id>/<type>/add.json

        Add objects (eg. Photos) to this album.
        The objects are a list of either IDs or Trovebox objects.
        If Trovebox objects are used, the object type is inferred
        automatically.
        Updates the album's fields with the response.
        """
        result = self._client.album.add(self, objects, object_type, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()

    def remove(self, objects, object_type=None, **kwds):
        """
        Endpoint: /album/<id>/<type>/remove.json

        Remove objects (eg. Photos) from this album.
        The objects are a list of either IDs or Trovebox objects.
        If Trovebox objects are used, the object type is inferred
        automatically.
        Updates the album's fields with the response.
        """
        result = self._client.album.remove(self, objects, object_type,
                                           **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()

    def update(self, **kwds):
        """
        Endpoint: /album/<id>/update.json

        Updates this album with the specified parameters.
        """
        result = self._client.album.update(self, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()

    def view(self, **kwds):
        """
        Endpoint: /album/<id>/view.json

        Requests all properties of an album.
        Updates the album's fields with the response.
        """
        result = self._client.album.view(self, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()
