"""
api_action.py : Trovebox Action API Classes
"""
from trovebox.objects.action import Action
from .api_base import ApiBase

class ApiAction(ApiBase):
    """ Definitions of /action/ API endpoints """
    def create(self, target, target_type=None, **kwds):
        """
        Endpoint: /action/<target_id>/<target_type>/create.json

        Creates a new action and returns it.
        The target parameter can either be an id or a Trovebox object.
        If a Trovebox object is used, the target type is inferred
        automatically.
        """
        # Extract the target type
        if target_type is None:
            target_type = target.get_type()

        # Extract the target ID
        try:
            target_id = target.id
        except AttributeError:
            target_id = target

        result = self._client.post("/action/%s/%s/create.json" %
                                   (target_id, target_type),
                                   **kwds)["result"]
        return Action(self._client, result)

    def delete(self, action, **kwds):
        """
        Endpoint: /action/<id>/delete.json

        Deletes an action.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        return self._client.post("/action/%s/delete.json" %
                                 self._extract_id(action),
                                 **kwds)["result"]

    def view(self, action, **kwds):
        """
        Endpoint: /action/<id>/view.json

        Requests all properties of an action.
        Returns the requested action object.
        """
        result = self._client.get("/action/%s/view.json" %
                                  self._extract_id(action),
                                  **kwds)["result"]
        return Action(self._client, result)
