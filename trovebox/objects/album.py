"""
Representation of an Album object
"""
from trovebox.errors import TroveboxError
from .trovebox_object import TroveboxObject
from .photo import Photo

class Album(TroveboxObject):
    """ Representation of an Album object """
    def __init__(self, trovebox, json_dict):
        self.photos = None
        self.cover = None
        TroveboxObject.__init__(self, trovebox, json_dict)
        self._type = "album"
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the cover with a photo object
        try:
            if isinstance(self.cover, dict):
                self.cover = Photo(self._trovebox, self.cover)
        except AttributeError:
            pass # No cover

        # Update the photo list with photo objects
        try:
            for i, photo in enumerate(self.photos):
                if isinstance(photo, dict):
                    self.photos[i] = Photo(self._trovebox, photo)
        except (AttributeError, TypeError):
            pass # No photos, or not a list

    def cover_update(self, photo, **kwds):
        """
        Endpoint: /album/<album_id>/cover/<photo_id>/update.json

        Update the cover photo of this album.
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._trovebox, {"id": photo})

        result = self._trovebox.post("/album/%s/cover/%s/update.json" %
                                     (self.id, photo.id),
                                     **kwds)["result"]

        # API currently doesn't return the updated album
        # (frontend issue #1369)
        if isinstance(result, bool): # pragma: no cover
            result = self._trovebox.get("/album/%s/view.json" %
                                        self.id)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()

    def delete(self, **kwds):
        """
        Endpoint: /album/<id>/delete.json

        Deletes this album.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._trovebox.post("/album/%s/delete.json" %
                                     self.id, **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
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
        result = self._trovebox.album.add(self, objects, object_type, **kwds)

        # API currently doesn't return the updated album
        # (frontend issue #1369)
        if isinstance(result, bool): # pragma: no cover
            result = self._trovebox.get("/album/%s/view.json" %
                                        self.id)["result"]
        self._replace_fields(result)
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
        result = self._trovebox.album.remove(self, objects, object_type,
                                             **kwds)
        # API currently doesn't return the updated album
        # (frontend issue #1369)
        if isinstance(result, bool): # pragma: no cover
            result = self._trovebox.get("/album/%s/view.json" %
                                        self.id)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()

    def update(self, **kwds):
        """
        Endpoint: /album/<id>/update.json

        Updates this album with the specified parameters.
        """
        result = self._trovebox.post("/album/%s/update.json" %
                                     self.id, **kwds)["result"]

        # APIv1 doesn't return the updated album (frontend issue #937)
        if isinstance(result, bool): # pragma: no cover
            result = self._trovebox.get("/album/%s/view.json" %
                                        self.id)["result"]

        self._replace_fields(result)
        self._update_fields_with_objects()

    def view(self, **kwds):
        """
        Endpoint: /album/<id>/view.json

        Requests all properties of an album.
        Updates the album's fields with the response.
        """
        result = self._trovebox.get("/album/%s/view.json" %
                                    self.id, **kwds)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()
