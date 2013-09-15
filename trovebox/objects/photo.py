"""
Representation of a Photo object
"""
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
        result = self._client.photo.delete(self, **kwds)
        self._delete_fields()
        return result

    def delete_source(self, **kwds):
        """
        Endpoint: /photo/<id>/source/delete.json

        Deletes the source files of this photo.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        return self._client.photo.delete_source(self, **kwds)

    def replace(self, photo_file, **kwds):
        """
        Endpoint: /photo/<id>/replace.json

        Uploads the specified photo file to replace this photo.
        """
        result = self._client.photo.replace(self, photo_file, **kwds)
        self._replace_fields(result.get_fields())

    def replace_encoded(self, photo_file, **kwds):
        """
        Endpoint: /photo/<id>/replace.json

        Base64-encodes and uploads the specified photo file to
        replace this photo.
        """
        result = self._client.photo.replace_encoded(self, photo_file,
                                                    **kwds)
        self._replace_fields(result.get_fields())

    def replace_from_url(self, url, **kwds):
        """
        Endpoint: /photo/<id>replace.json

        Import a photo from the specified URL to replace this photo.
        """
        result = self._client.photo.replace_from_url(self, url, **kwds)
        self._replace_fields(result.get_fields())

    def update(self, **kwds):
        """
        Endpoint: /photo/<id>/update.json

        Updates this photo with the specified parameters.
        """
        result = self._client.photo.update(self, **kwds)
        self._replace_fields(result.get_fields())

    def view(self, options=None, **kwds):
        """
        Endpoint: /photo/<id>[/<options>]/view.json

        Requests all properties of this photo.
        Can be used to obtain URLs for the photo at a particular size,
          by using the "returnSizes" parameter.
        Updates the photo's fields with the response.
        The options parameter can be used to pass in additional options.
        Eg: options={"token": <token_data>}
        """
        result = self._client.photo.view(self, options, **kwds)
        self._replace_fields(result.get_fields())

    def next_previous(self, options=None, **kwds):
        """
        Endpoint: /photo/<id>/nextprevious[/<options>].json

        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned).
        """
        return self._client.photo.next_previous(self, options, **kwds)

    def transform(self, **kwds):
        """
        Endpoint: /photo/<id>/transform.json

        Performs the specified transformations.
          eg. transform(photo, rotate=90)
        Updates the photo's fields with the response.
        """
        result = self._client.photo.transform(self, **kwds)
        self._replace_fields(result.get_fields())
