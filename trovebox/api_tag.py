"""
api_tag.py : Trovebox Tag API Classes
"""
from .objects import Tag

class ApiTags(object):
    def __init__(self, client):
        self._client = client

    def list(self, **kwds):
        """ Returns a list of Tag objects """
        results = self._client.get("/tags/list.json", **kwds)["result"]
        return [Tag(self._client, tag) for tag in results]

class ApiTag(object):
    def __init__(self, client):
        self._client = client

    def create(self, tag, **kwds):
        """
        Create a new tag.
        The API returns true if the tag was sucessfully created
        """
        return self._client.post("/tag/create.json", tag=tag, **kwds)["result"]

    def delete(self, tag, **kwds):
        """
        Delete a tag.
        Returns True if successful.
        Raises an TroveboxError if not.
        """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        return tag.delete(**kwds)

    def update(self, tag, **kwds):
        """ Update a tag """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        tag.update(**kwds)
        return tag
