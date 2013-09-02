"""
api_action.py : Trovebox Action API Classes
"""
from trovebox.objects.action import Action
from trovebox.objects.photo import Photo

class ApiAction(object):
    """ Definitions of /action/ API endpoints """
    def __init__(self, client):
        self._client = client

    def create(self, target, target_type=None, **kwds):
        """
        Create a new action and return it.
        If the target_type parameter isn't specified, it is automatically
        generated.
        """
        if target_type is None:
            # Determine the target type
            if isinstance(target, Photo):
                target_type = "photo"
            else:
                raise NotImplementedError("Unsupported target type")
        # Extract the ID from the target
        try:
            target_id = target.id
        except AttributeError:
            # Assume the ID was passed in directly
            target_id = target

        result = self._client.post("/action/%s/%s/create.json" %
                                   (target_id, target_type),
                                   **kwds)["result"]
        return Action(self._client, result)

    def delete(self, action, **kwds):
        """
        Delete an action.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        if not isinstance(action, Action):
            action = Action(self._client, {"id": action})
        return action.delete(**kwds)

    def view(self, action, **kwds):
        """
        View an action's contents.
        Returns the requested action object.
        """
        if not isinstance(action, Action):
            action = Action(self._client, {"id": action})
        action.view(**kwds)
        return action
