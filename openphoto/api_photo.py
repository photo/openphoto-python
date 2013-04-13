import base64

from errors import *
from objects import Photo

class ApiPhotos:
    def __init__(self, client):
        self._client = client

    def list(self, **kwds):
        """ Returns a list of Photo objects """
        photos = self._client.get("/photos/list.json", **kwds)["result"]
        photos = self._client._result_to_list(photos)
        return [Photo(self._client, photo) for photo in photos]

    def update(self, photos, **kwds):
        """
        Updates a list of photos.
        Returns True if successful.
        Raises OpenPhotoError if not.
        """
        if not self._client.post("/photos/update.json", ids=photos, **kwds)["result"]:
            raise OpenPhotoError("Update response returned False")
        return True

    def delete(self, photos, **kwds):
        """
        Deletes a list of photos.
        Returns True if successful.
        Raises OpenPhotoError if not.
        """
        if not self._client.post("/photos/delete.json", ids=photos, **kwds)["result"]:
            raise OpenPhotoError("Delete response returned False")
        return True

class ApiPhoto:
    def __init__(self, client):
        self._client = client

    def delete(self, photo, **kwds):
        """
        Delete a photo.
        Returns True if successful.
        Raises an OpenPhotoError if not.
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        return photo.delete(**kwds)

    def edit(self, photo, **kwds):
        """ Returns an HTML form to edit a photo """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        return photo.edit(**kwds)

    def replace(self, photo, photo_file, **kwds):
        raise NotImplementedError()

    def replace_encoded(self, photo, photo_file, **kwds):
        raise NotImplementedError()

    def update(self, photo, **kwds):
        """ 
        Update a photo with the specified parameters.
        Returns the updated photo object
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        photo.update(**kwds)
        return photo

    def view(self, photo, **kwds):
        """ 
        Used to view the photo at a particular size. 
        Returns the requested photo object
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        photo.view(**kwds)
        return photo

    def upload(self, photo_file, **kwds):
        result = self._client.post("/photo/upload.json", files={'photo': photo_file}, 
                                   **kwds)["result"]
        return Photo(self._client, result)

    def upload_encoded(self, photo_file, **kwds):
        """ Base64-encodes and uploads the specified file """
        encoded_photo = base64.b64encode(open(photo_file, "rb").read())
        result = self._client.post("/photo/upload.json", photo=encoded_photo, 
                                   **kwds)["result"]
        return Photo(self._client, result)

    def dynamic_url(self, photo, **kwds):
        raise NotImplementedError()

    def next_previous(self, photo, **kwds):
        """ 
        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned). 
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        return photo.next_previous(**kwds)

    def transform(self, photo, **kwds):
        """
        Performs transformation specified in **kwds 
        Example: transform(photo, rotate=90)
        """
        if not isinstance(photo, Photo):
            photo = Photo(self._client, {"id": photo})
        photo.transform(**kwds)
        # The API doesn't currently return the transformed photo
        # Uncomment the below once frontend issue #955 is resolved
#        return photo
