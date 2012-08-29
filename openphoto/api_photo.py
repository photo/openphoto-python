import base64

from openphoto_http import OpenPhotoHttp, OpenPhotoError
from objects import Photo

class ApiPhoto(OpenPhotoHttp):
    def photo_delete(self, photo_id, **kwds):
        """ Delete a photo """
        photo = Photo(self, {"id": photo_id})
        photo.delete(**kwds)

    def photo_edit(self, photo_id, **kwds):
        """ Returns an HTML form to edit a photo """
        photo = Photo(self, {"id": photo_id})
        return photo.edit(**kwds)

    def photo_replace(self, photo_id, photo_file, **kwds):
        raise NotImplementedError()

    def photo_replace_encoded(self, photo_id, photo_file, **kwds):
        raise NotImplementedError()

    def photo_update(self, photo_id, **kwds):
        """ 
        Update a photo with the specified parameters.
        Returns the updated photo object
        """
        photo = Photo(self, {"id": photo_id})
        photo.update(**kwds)
        return photo

    def photo_view(self, photo_id, **kwds):
        """ 
        Used to view the photo at a particular size. 
        Returns the requested photo object
        """
        photo = Photo(self, {"id": photo_id})
        photo.view(**kwds)
        return photo

    def photos_list(self, **kwds):
        """ Returns a list of Photo objects """
        photos = self.get("/photos/list.json", **kwds)["result"]
        photos = self._result_to_list(photos)
        return [Photo(self, photo) for photo in photos]

    def photos_update(self, photo_ids, **kwds):
        """ Updates a list of photos """
        if not self.post("/photos/update.json", ids=photo_ids, **kwds)["result"]:
            raise OpenPhotoError("Update response returned False")

    def photos_delete(self, photo_ids, **kwds):
        """ Deletes a list of photos """
        if not self.post("/photos/delete.json", ids=photo_ids, **kwds)["result"]:
            raise OpenPhotoError("Delete response returned False")

    def photo_upload(self, photo_file, **kwds):
        raise NotImplementedError("Use photo_upload_encoded instead.")

    def photo_upload_encoded(self, photo_file, **kwds):
        """ Base64-encodes and uploads the specified file """
        encoded_photo = base64.b64encode(open(photo_file, "rb").read())
        result = self.post("/photo/upload.json", photo=encoded_photo, 
                           **kwds)["result"]
        return Photo(self, result)

    def photo_dynamic_url(self, photo_id, **kwds):
        raise NotImplementedError()

    def photo_next_previous(self, photo_id, **kwds):
        """ 
        Returns a dict containing the next and previous photo objects, 
        given a photo in the middle.
        """
        photo = Photo(self, {"id": photo_id})
        return photo.next_previous(**kwds)

    def photo_transform(self, photo_id, **kwds):
        raise NotImplementedError()
