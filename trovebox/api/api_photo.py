"""
api_photo.py : Trovebox Photo API Classes
"""
import base64

from trovebox.errors import TroveboxError
from trovebox.objects.photo import Photo
from .api_base import ApiBase

class ApiPhotos(ApiBase):
    """ Definitions of /photos/ API endpoints """
    # TODO: Add options
    def list(self, **kwds):
        """
        Endpoint: /photos/list.json

        Returns a list of Photo objects.
        """
        photos = self._client.get("/photos/list.json", **kwds)["result"]
        photos = self._result_to_list(photos)
        return [Photo(self._client, photo) for photo in photos]

    # def share(self, **kwds):

    def delete(self, photos, **kwds):
        """
        Endpoint: /photos/delete.json

        Deletes a list of photos.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        ids = [self._extract_id(photo) for photo in photos]
        if not self._client.post("/photos/delete.json", ids=ids,
                                 **kwds)["result"]:
            raise TroveboxError("Delete response returned False")
        return True

    def update(self, photos, **kwds):
        """
        Endpoint: /photos/<id>/update.json

        Updates a list of photos with the specified parameters.
        Returns True if successful.
        Raises TroveboxError if not.
        """
        ids = [self._extract_id(photo) for photo in photos]
        if not self._client.post("/photos/update.json", ids=ids,
                                 **kwds)["result"]:
            raise TroveboxError("Update response returned False")
        return True

class ApiPhoto(ApiBase):
    """ Definitions of /photo/ API endpoints """
    def delete(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/delete.json

        Deletes a photo.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._client.post("/photo/%s/delete.json" %
                                   self._extract_id(photo),
                                   **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        return result

    # def delete_source(self, photo, **kwds):

    def replace(self, photo, photo_file, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def replace_encoded(self, photo, photo_file, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    def update(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/update.json

        Updates a photo with the specified parameters.
        Returns the updated photo object.
        """
        result = self._client.post("/photo/%s/update.json" %
                                   self._extract_id(photo),
                                   **kwds)["result"]
        return Photo(self._client, result)

    # TODO: Add options
    def view(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/view.json

        Requests all properties of a photo.
        Can be used to obtain URLs for the photo at a particular size,
          by using the "returnSizes" parameter.
        Returns the requested photo object.
        """
        result = self._client.get("/photo/%s/view.json" %
                                  self._extract_id(photo),
                                  **kwds)["result"]
        return Photo(self._client, result)

    def upload(self, photo_file, **kwds):
        """
        Endpoint: /photo/upload.json

        Uploads the specified photo filename.
        """
        with open(photo_file, 'rb') as in_file:
            result = self._client.post("/photo/upload.json",
                                       files={'photo': in_file},
                                       **kwds)["result"]
        return Photo(self._client, result)

    def upload_encoded(self, photo_file, **kwds):
        """
        Endpoint: /photo/upload.json

        Base64-encodes and uploads the specified photo filename.
        """
        with open(photo_file, "rb") as in_file:
            encoded_photo = base64.b64encode(in_file.read())
        result = self._client.post("/photo/upload.json", photo=encoded_photo,
                                   **kwds)["result"]
        return Photo(self._client, result)

    def dynamic_url(self, photo, **kwds):
        """ Not yet implemented """
        raise NotImplementedError()

    # TODO: Add options
    def next_previous(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/nextprevious.json

        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned).
        """
        result = self._client.get("/photo/%s/nextprevious.json" %
                                  self._extract_id(photo),
                                  **kwds)["result"]
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

    def transform(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/transform.json

        Performs the specified transformations.
          eg. transform(photo, rotate=90)
        Returns the transformed photo.
        """
        result = self._client.post("/photo/%s/transform.json" %
                                   self._extract_id(photo),
                                   **kwds)["result"]

        # APIv1 doesn't return the transformed photo (frontend issue #955)
        if isinstance(result, bool): # pragma: no cover
            result = self._client.get("/photo/%s/view.json" %
                                      self._extract_id(photo))["result"]

        return Photo(self._client, result)
