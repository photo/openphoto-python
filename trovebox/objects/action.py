"""
Representation of an Action object
"""
from trovebox.errors import TroveboxError
from .trovebox_object import TroveboxObject
from .photo import Photo

class Action(TroveboxObject):
    """ Representation of an Action object """
    def __init__(self, trovebox, json_dict):
        self.target = None
        self.target_type = None
        TroveboxObject.__init__(self, trovebox, json_dict)
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the photo target with photo objects
        if self.target is not None:
            if self.target_type == "photo":
                self.target = Photo(self._trovebox, self.target)
            else:
                raise NotImplementedError("Actions can only be assigned to "
                                          "Photos")

    def delete(self, **kwds):
        """
        Delete this action.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._trovebox.post("/action/%s/delete.json" %
                                     self.id, **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    def view(self, **kwds):
        """
        Requests the full contents of the action.
        Updates the action's fields with the response.
        """
        result = self._trovebox.get("/action/%s/view.json" %
                                    self.id, **kwds)["result"]
        self._replace_fields(result)
        self._update_fields_with_objects()
