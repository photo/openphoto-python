"""
Representation of a Photo object
"""
from trovebox.errors import TroveboxError
from .trovebox_object import TroveboxObject

class Photo(TroveboxObject):
    """ Representation of a Photo object """
    def delete(self, **kwds):
        """
        Delete this photo.
        Returns True if successful.
        Raises a TroveboxError if not.
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
        result = self._trovebox.post("/photo/%s/update.json" %
                                     self.id, **kwds)["result"]
        self._replace_fields(result)

    def view(self, **kwds):
        """
        Used to view the photo at a particular size.
        Updates the photo's fields with the response.
        """
        result = self._trovebox.get("/photo/%s/view.json" %
                                    self.id, **kwds)["result"]
        self._replace_fields(result)

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
            if not isinstance(result["next"], list): # pragma: no cover
                result["next"] = [result["next"]]

            value["next"] = []
            for photo in result["next"]:
                value["next"].append(Photo(self._trovebox, photo))

        if "previous" in result:
            # Workaround for APIv1
            if not isinstance(result["previous"], list): # pragma: no cover
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
        result = self._trovebox.post("/photo/%s/transform.json" %
                                     self.id, **kwds)["result"]

        # APIv1 doesn't return the transformed photo (frontend issue #955)
        if isinstance(result, bool): # pragma: no cover
            result = self._trovebox.get("/photo/%s/view.json" %
                                        self.id)["result"]

        self._replace_fields(result)
