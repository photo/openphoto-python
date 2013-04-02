from errors import *
from objects import Tag

class ApiTags:
    def __init__(self, client):
        self._client = client

    def list(self, **kwds):
        """ Returns a list of Tag objects """
        results = self._client.get("/tags/list.json", **kwds)["result"]
        return [Tag(self._client, tag) for tag in results]

class ApiTag:
    def __init__(self, client):
        self._client = client

    def create(self, tag, **kwds):
        """ Create a new tag and return it """
        result = self._client.post("/tag/create.json", tag=tag, **kwds)["result"]
        return Tag(self._client, result)

    def delete(self, tag, **kwds):
        """ Delete a tag """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        tag.delete(**kwds)

    def update(self, tag, **kwds):
        """ Update a tag """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        tag.update(**kwds)
        return tag
