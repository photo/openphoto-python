"""
api_photo.py : Trovebox Photo API Classes
"""
import base64

from trovebox.objects.photo import Photo
from .api_base import ApiBase

class ApiPhotos(ApiBase):
    """ Definitions of /photos/ API endpoints """
    def list(self, options=None, **kwds):
        """
        Endpoint: /photos[/<options>]/list.json

        Returns a list of Photo objects.
        The options parameter can be used to narrow down the list.
        Eg: options={"album": <album_id>}
        """
        option_string = self._build_option_string(options)
        photos = self._client.get("/photos%s/list.json" % option_string,
                                  **kwds)["result"]
        photos = self._result_to_list(photos)
        return [Photo(self._client, photo) for photo in photos]

    def share(self, options=None, **kwds):
        """
        Endpoint: /photos[/<options>/share.json

        Not currently implemented.
        """
        option_string = self._build_option_string(options)
        return self._client.post("/photos%s/share.json" % option_string,
                                 **kwds)["result"]

    def delete(self, photos, **kwds):
        """
        Endpoint: /photos/delete.json

        Deletes a list of photos.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        ids = [self._extract_id(photo) for photo in photos]
        return self._client.post("/photos/delete.json", ids=ids,
                                 **kwds)["result"]

    def update(self, photos, **kwds):
        """
        Endpoint: /photos/<id>/update.json

        Updates a list of photos with the specified parameters.
        Returns True if successful.
        Raises TroveboxError if not.
        """
        ids = [self._extract_id(photo) for photo in photos]
        return self._client.post("/photos/update.json", ids=ids,
                                 **kwds)["result"]

class ApiPhoto(ApiBase):
    """ Definitions of /photo/ API endpoints """
    def delete(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/delete.json

        Deletes a photo.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        return self._client.post("/photo/%s/delete.json" %
                                 self._extract_id(photo),
                                 **kwds)["result"]

    def delete_source(self, photo, **kwds):
        """
        Endpoint: /photo/<id>/source/delete.json

        Delete the source files of a photo.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        return self._client.post("/photo/%s/source/delete.json" %
                                 self._extract_id(photo),
                                 **kwds)["result"]

    def replace(self, photo, photo_file, **kwds):
        """
        Endpoint: /photo/<id>/replace.json

        Uploads the specified photo file to replace an existing photo.
        """
        with open(photo_file, 'rb') as in_file:
            result = self._client.post("/photo/%s/replace.json" %
                                       self._extract_id(photo),
                                       files={'photo': in_file},
                                       **kwds)["result"]
        return Photo(self._client, result)

    def replace_encoded(self, photo, photo_file, **kwds):
        """
        Endpoint: /photo/<id>/replace.json

        Base64-encodes and uploads the specified photo filename to
        replace an existing photo.
        """
        with open(photo_file, "rb") as in_file:
            encoded_photo = base64.b64encode(in_file.read())
        result = self._client.post("/photo/%s/replace.json" %
                                   self._extract_id(photo),
                                   photo=encoded_photo,
                                   **kwds)["result"]
        return Photo(self._client, result)

    def replace_from_url(self, photo, url, **kwds):
        """
        Endpoint: /photo/<id>replace.json

        Import a photo from the specified URL to replace an existing
        photo.
        """
        result = self._client.post("/photo/%s/replace.json" %
                                   self._extract_id(photo),
                                   photo=url,
                                   **kwds)["result"]
        return Photo(self._client, result)


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

    def view(self, photo, options=None, **kwds):
        """
        Endpoint: /photo/<id>[/<options>]/view.json

        Requests all properties of a photo.
        Can be used to obtain URLs for the photo at a particular size,
          by using the "returnSizes" parameter.
        Returns the requested photo object.
        The options parameter can be used to pass in additional options.
        Eg: options={"token": <token_data>}
        """
        option_string = self._build_option_string(options)
        result = self._client.get("/photo/%s%s/view.json" %
                                  (self._extract_id(photo), option_string),
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

    def upload_from_url(self, url, **kwds):
        """
        Endpoint: /photo/upload.json

        Import a photo from the specified URL
        """
        result = self._client.post("/photo/upload.json", photo=url,
                                   **kwds)["result"]
        return Photo(self._client, result)

    def next_previous(self, photo, options=None, **kwds):
        """
        Endpoint: /photo/<id>/nextprevious[/<options>].json

        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned).
        The options parameter can be used to narrow down the photos
        Eg: options={"album": <album_id>}
        """
        option_string = self._build_option_string(options)
        result = self._client.get("/photo/%s/nextprevious%s.json" %
                                  (self._extract_id(photo), option_string),
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
