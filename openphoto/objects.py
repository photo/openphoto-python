from errors import *

class OpenPhotoObject:
    """ Base object supporting the storage of custom fields as attributes """
    def __init__(self, openphoto, json_dict):
        self._openphoto = openphoto
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

    def __repr__(self):
        if hasattr(self, "name"):
            return "<%s name='%s'>" % (self.__class__, self.name)
        elif hasattr(self, "id"):
            return "<%s id='%s'>" % (self.__class__, self.id)
        else:
            return "<%s>" % (self.__class__)

    def get_fields(self):
        """ Returns this object's attributes """
        return self._json_dict


class Photo(OpenPhotoObject):
    def delete(self, **kwds):
        """
        Delete this photo.
        Returns True if successful.
        Raises an OpenPhotoError if not.
        """
        result = self._openphoto.post("/photo/%s/delete.json" % self.id, **kwds)["result"]
        self._replace_fields({})
        return result

    def edit(self, **kwds):
        """ Returns an HTML form to edit the photo """
        result = self._openphoto.get("/photo/%s/edit.json" % self.id, 
                                     **kwds)["result"]
        return result["markup"]

    def replace(self, photo_file, **kwds):
        raise NotImplementedError()

    def replace_encoded(self, encoded_photo, **kwds):
        raise NotImplementedError()

    def update(self, **kwds):
        """ Update this photo with the specified parameters """
        new_dict = self._openphoto.post("/photo/%s/update.json" % self.id, 
                                        **kwds)["result"]
        self._replace_fields(new_dict)

    def view(self, **kwds):
        """ 
        Used to view the photo at a particular size. 
        Updates the photo's fields with the response.
        """
        new_dict = self._openphoto.get("/photo/%s/view.json" % self.id, 
                                       **kwds)["result"]
        self._replace_fields(new_dict)

    def dynamic_url(self, **kwds):
        raise NotImplementedError()

    def next_previous(self, **kwds):
        """ 
        Returns a dict containing the next and previous photo lists
        (there may be more than one next/previous photo returned). 
        """
        result = self._openphoto.get("/photo/%s/nextprevious.json" % self.id, 
                                     **kwds)["result"]
        value = {}
        if "next" in result:
            value["next"] = []
            for photo in result["next"]:
                value["next"].append(Photo(self._openphoto, photo))
        if "previous" in result:
            value["previous"] = []
            for photo in result["previous"]:
                value["previous"].append(Photo(self._openphoto, photo))
        return value

    def transform(self, **kwds):
        """
        Performs transformation specified in **kwds
        Example: transform(rotate=90)
        """
        new_dict = self._openphoto.post("/photo/%s/transform.json" % self.id,
                                        **kwds)["result"]
        self._replace_fields(new_dict)

class Tag(OpenPhotoObject):
    def delete(self, **kwds):
        """
        Delete this tag.
        Returns True if successful.
        Raises an OpenPhotoError if not.
        """
        result = self._openphoto.post("/tag/%s/delete.json" % self.id, **kwds)["result"]
        self._replace_fields({})
        return result

    def update(self, **kwds):
        """ Update this tag with the specified parameters """
        new_dict = self._openphoto.post("/tag/%s/update.json" % self.id, 
                                        **kwds)["result"]
        self._replace_fields(new_dict)


class Album(OpenPhotoObject):
    def __init__(self, openphoto, json_dict):
        OpenPhotoObject.__init__(self, openphoto, json_dict)
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the cover with a photo object
        if hasattr(self, "cover") and isinstance(self.cover, dict):
            self.cover = Photo(self._openphoto, self.cover)
        # Update the photo list with photo objects
        if hasattr(self, "photos") and isinstance(self.photos, list):
            for i, photo in enumerate(self.photos):
                if isinstance(photo, dict):
                    self.photos[i] = Photo(self._openphoto, photo)

    def delete(self, **kwds):
        """
        Delete this album.
        Returns True if successful.
        Raises an OpenPhotoError if not.
        """
        result = self._openphoto.post("/album/%s/delete.json" % self.id, **kwds)["result"]
        self._replace_fields({})
        return result

    def form(self, **kwds):
        raise NotImplementedError()

    def add_photos(self, **kwds):
        raise NotImplementedError()
    
    def remove_photos(self, **kwds):
        raise NotImplementedError()

    def update(self, **kwds):
        """ Update this album with the specified parameters """
        new_dict = self._openphoto.post("/album/%s/update.json" % self.id, 
                                        **kwds)["result"]

        # Since the API doesn't give us the modified album, we need to
        # update our fields based on the kwds that were sent
        self._set_fields(kwds)

        # Replace the above line with the below once frontend issue #937 is resolved
#        self._set_fields(new_dict)
#        self._update_fields_with_objects()
        
    def view(self, **kwds):
        """ 
        Requests the full contents of the album.
        Updates the album's fields with the response.
        """
        result = self._openphoto.get("/album/%s/view.json" % self.id, 
                                     **kwds)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()
