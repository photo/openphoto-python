"""
objects.py : Basic Trovebox API Objects
"""
try:
    from urllib.parse import quote # Python3
except ImportError:
    from urllib import quote # Python2

from .errors import TroveboxError

class TroveboxObject(object):
    """ Base object supporting the storage of custom fields as attributes """
    def __init__(self, trovebox, json_dict):
        self.id = None
        self.name = None
        self._trovebox = trovebox
        self._json_dict = json_dict
        self._set_fields(json_dict)

    def _set_fields(self, json_dict):
        """ Set this object's attributes specified in json_dict """
        for key, value in json_dict.items():
            if key.startswith("_"):
                raise ValueError("Illegal attribute: %s" % key)
            setattr(self, key, value)

    def _replace_fields(self, json_dict):
        """
        Delete this object's attributes, and replace with
        those in json_dict.
        """
        for key in self._json_dict.keys():
            delattr(self, key)
        self._json_dict = json_dict
        self._set_fields(json_dict)

    def _delete_fields(self):
        """
        Delete this object's attributes, including name and id
        """
        for key in self._json_dict.keys():
            delattr(self, key)
        self._json_dict = {}
        self.id = None
        self.name = None

    def __repr__(self):
        if self.name is not None:
            return "<%s name='%s'>" % (self.__class__, self.name)
        elif self.id is not None:
            return "<%s id='%s'>" % (self.__class__, self.id)
        else:
            return "<%s>" % (self.__class__)

    def get_fields(self):
        """ Returns this object's attributes """
        return self._json_dict


class Photo(TroveboxObject):
    def delete(self, **kwds):
        """
        Delete this photo.
        Returns True if successful.
        Raises an TroveboxError if not.
        """
        result = self._trovebox.post("/photo/%s/delete.json" %
                                     self.id, **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    def edit(self, **kwds):
        """ Returns an HTML form to edit the photo """
        result = self._trovebox.get("/photo/%s/edit.json" %
                                    self.id, **kwds)["result"]
        return result["markup"]

    def replace(self, photo_file, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def replace_encoded(self, photo_file, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def update(self, **kwds):
        """ Update this photo with the specified parameters """
        new_dict = self._trovebox.post("/photo/%s/update.json" %
                                       self.id, **kwds)["result"]
        self._replace_fields(new_dict)

    def view(self, **kwds):
        """
        Used to view the photo at a particular size.
        Updates the photo's fields with the response.
        """
        new_dict = self._trovebox.get("/photo/%s/view.json" %
                                      self.id, **kwds)["result"]
        self._replace_fields(new_dict)

    def dynamic_url(self, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def next_previous(self, **kwds):
        """
        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned).
        """
        result = self._trovebox.get("/photo/%s/nextprevious.json" %
                                     self.id, **kwds)["result"]
        value = {}
        if "next" in result:
            # Workaround for APIv1
            if not isinstance(result["next"], list):
                result["next"] = [result["next"]]

            value["next"] = []
            for photo in result["next"]:
                value["next"].append(Photo(self._trovebox, photo))

        if "previous" in result:
            # Workaround for APIv1
            if not isinstance(result["previous"], list):
                result["previous"] = [result["previous"]]

            value["previous"] = []
            for photo in result["previous"]:
                value["previous"].append(Photo(self._trovebox, photo))

        return value

    def transform(self, **kwds):
        """
        Performs transformation specified in **kwds
        Example: transform(rotate=90)
        """
        new_dict = self._trovebox.post("/photo/%s/transform.json" %
                                       self.id, **kwds)["result"]

        # APIv1 doesn't return the transformed photo (frontend issue #955)
        if isinstance(new_dict, bool):
            new_dict = self._trovebox.get("/photo/%s/view.json" %
                                          self.id)["result"]

        self._replace_fields(new_dict)

class Tag(TroveboxObject):
    def delete(self, **kwds):
        """
        Delete this tag.
        Returns True if successful.
        Raises an TroveboxError if not.
        """
        result = self._trovebox.post("/tag/%s/delete.json" %
                                     quote(self.id), **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    def update(self, **kwds):
        """ Update this tag with the specified parameters """
        new_dict = self._trovebox.post("/tag/%s/update.json" % quote(self.id),
                                       **kwds)["result"]
        self._replace_fields(new_dict)


class Album(TroveboxObject):
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
        Raises an TroveboxError if not.
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
        new_dict = self._trovebox.post("/album/%s/update.json" %
                                       self.id, **kwds)["result"]

        # APIv1 doesn't return the updated album (frontend issue #937)
        if isinstance(new_dict, bool):
            new_dict = self._trovebox.get("/album/%s/view.json" %
                                           self.id)["result"]

        self._replace_fields(new_dict)
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
