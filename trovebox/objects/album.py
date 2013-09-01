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
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the cover with a photo object
        if isinstance(self.cover, dict):
            self.cover = Photo(self._trovebox, self.cover)
        # Update the photo list with photo objects
        if isinstance(self.photos, list):
            for i, photo in enumerate(self.photos):
                if isinstance(photo, dict):
                    self.photos[i] = Photo(self._trovebox, photo)

    def delete(self, **kwds):
        """
        Delete this album.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._trovebox.post("/album/%s/delete.json" %
                                     self.id, **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    def form(self, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def add_photos(self, photos, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def remove_photos(self, photos, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def update(self, **kwds):
        """ Update this album with the specified parameters """
        result = self._trovebox.post("/album/%s/update.json" %
                                     self.id, **kwds)["result"]

        # APIv1 doesn't return the updated album (frontend issue #937)
        if isinstance(result, bool):
            result = self._trovebox.get("/album/%s/view.json" %
                                        self.id)["result"]

        self._replace_fields(result)
        self._update_fields_with_objects()

    def view(self, **kwds):
        """
        Requests the full contents of the album.
        Updates the album's fields with the response.
        """
        result = self._trovebox.get("/album/%s/view.json" %
                                    self.id, **kwds)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()
