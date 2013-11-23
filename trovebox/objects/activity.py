"""
Representation of an Activity object
"""
from .trovebox_object import TroveboxObject
from .photo import Photo

class Activity(TroveboxObject):
    """ Representation of an Activity object """
    _type = "activity"

    def __init__(self, client, json_dict):
        self.data = None
        self.type = None
        TroveboxObject.__init__(self, client, json_dict)
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the data with photo objects
        if self.type is not None:
            if self.type.startswith("photo"):
                self.data = Photo(self._client, self.data)
            else:
                raise NotImplementedError("Unrecognised activity type: %s"
                                          % self.type)

    def view(self, **kwds):
        """
        Endpoint: /activity/<id>/view.json

        Requests the full contents of the activity.
        Updates the activity's fields with the response.
        """
        result = self._client.activity.view(self, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()

