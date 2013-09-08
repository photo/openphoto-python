"""
Representation of an Activity object
"""
import json

from .trovebox_object import TroveboxObject
from .photo import Photo

class Activity(TroveboxObject):
    """ Representation of an Activity object """
    def __init__(self, trovebox, json_dict):
        self.data = None
        self.type = None
        TroveboxObject.__init__(self, trovebox, json_dict)
        self._type = "activity"
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the data with photo objects
        if self.type is not None:
            if self.type.startswith("photo"):
                self.data = Photo(self._trovebox, self.data)
            else:
                raise NotImplementedError("Unrecognised activity type: %s"
                                          % self.type)

    def view(self, **kwds):
        """
        Endpoint: /activity/<id>/view.json

        Requests the full contents of the activity.
        Updates the activity's fields with the response.
        """
        result = self._trovebox.get("/activity/%s/view.json" %
                                    self.id, **kwds)["result"]

        # TBD: Why is the result enclosed/encoded like this?
        result = result["0"]
        result["data"] = json.loads(result["data"])

        self._replace_fields(result)
        self._update_fields_with_objects()
