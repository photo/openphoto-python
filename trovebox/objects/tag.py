"""
Representation of a Tag object
"""
from .trovebox_object import TroveboxObject

class Tag(TroveboxObject):
    """ Representation of a Tag object """
    _type = "tag"

    def delete(self, **kwds):
        """
        Endpoint: /tag/<id>/delete.json

        Deletes this tag.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._client.tag.delete(self, **kwds)
        self._delete_fields()
        return result

    def update(self, **kwds):
        """
        Endpoint: /tag/<id>/update.json

        Updates this tag with the specified parameters.
        Returns the updated tag object.
        """
        result = self._client.tag.update(self, **kwds)
        self._replace_fields(result.get_fields())

    # def view(self, **kwds):
