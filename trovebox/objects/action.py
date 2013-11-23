"""
Representation of an Action object
"""
from .trovebox_object import TroveboxObject
from .photo import Photo

class Action(TroveboxObject):
    """ Representation of an Action object """
    _type = "action"

    def __init__(self, client, json_dict):
        self.target = None
        self.target_type = None
        TroveboxObject.__init__(self, client, json_dict)
        self._update_fields_with_objects()

    def _update_fields_with_objects(self):
        """ Convert dict fields into objects, where appropriate """
        # Update the photo target with photo objects
        if self.target is not None:
            if self.target_type == "photo":
                self.target = Photo(self._client, self.target)
            else:
                raise NotImplementedError("Actions can only be assigned to "
                                          "Photos")

    def delete(self, **kwds):
        """
        Endpoint: /action/<id>/delete.json

        Deletes this action.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._client.action.delete(self, **kwds)
        self._delete_fields()
        return result

    def view(self, **kwds):
        """
        Endpoint: /action/<id>/view.json

        Requests the full contents of the action.
        Updates the action object's fields with the response.
        """
        result = self._client.action.view(self, **kwds)
        self._replace_fields(result.get_fields())
        self._update_fields_with_objects()
