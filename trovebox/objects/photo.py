"""
Representation of a Photo object
"""
from trovebox.errors import TroveboxError
from .trovebox_object import TroveboxObject

class Photo(TroveboxObject):
    """ Representation of a Photo object """
    _type = "photo"

    def delete(self, **kwds):
        """
        Endpoint: /photo/<id>/delete.json

        Deletes this photo.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._client.post("/photo/%s/delete.json" %
                                   self.id, **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    # def delete_source(self, **kwds):

    def replace(self, photo_file, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def replace_encoded(self, photo_file, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    def update(self, **kwds):
        """
        Endpoint: /photo/<id>/update.json

        Updates this photo with the specified parameters.
        """
        result = self._client.post("/photo/%s/update.json" %
                                   self.id, **kwds)["result"]
        self._replace_fields(result)

    # TODO: Add options
    def view(self, **kwds):
        """
        Endpoint: /photo/<id>/view.json

        Requests all properties of this photo.
        Can be used to obtain URLs for the photo at a particular size,
          by using the "returnSizes" parameter.
        Updates the photo's fields with the response.
        """
        result = self._client.get("/photo/%s/view.json" %
                                  self.id, **kwds)["result"]
        self._replace_fields(result)

    def dynamic_url(self, **kwds):
        """ Not implemented yet """
        raise NotImplementedError()

    # TODO: Add options
    def next_previous(self, **kwds):
        """
        Endpoint: /photo/<id>/nextprevious.json

        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned).
        """
        result = self._client.get("/photo/%s/nextprevious.json" %
                                  self.id, **kwds)["result"]
        value = {}
        if "next" in result:
            # Workaround for APIv1
            if not isinstance(result["next"], list): # pragma: no cover
                result["next"] = [result["next"]]

            value["next"] = []
            for photo in result["next"]:
                value["next"].append(Photo(self._client, photo))

        if "previous" in result:
            # Workaround for APIv1
            if not isinstance(result["previous"], list): # pragma: no cover
                result["previous"] = [result["previous"]]

            value["previous"] = []
            for photo in result["previous"]:
                value["previous"].append(Photo(self._client, photo))

        return value

    def transform(self, **kwds):
        """
        Endpoint: /photo/<id>/transform.json

        Performs the specified transformations.
          eg. transform(photo, rotate=90)
        Updates the photo's fields with the response.
        """
        result = self._client.post("/photo/%s/transform.json" %
                                   self.id, **kwds)["result"]

        # APIv1 doesn't return the transformed photo (frontend issue #955)
        if isinstance(result, bool): # pragma: no cover
            result = self._client.get("/photo/%s/view.json" %
                                      self.id)["result"]

        self._replace_fields(result)
