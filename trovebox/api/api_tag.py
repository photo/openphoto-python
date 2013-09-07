"""
api_tag.py : Trovebox Tag API Classes
"""
from trovebox import http
from trovebox.objects.tag import Tag
from .api_base import ApiBase

class ApiTags(ApiBase):
    """ Definitions of /tags/ API endpoints """
    def list(self, **kwds):
        """
        Endpoint: /tags/list.json

        Returns a list of Tag objects.
        """
        tags = self._client.get("/tags/list.json", **kwds)["result"]
        tags = http.result_to_list(tags)
        return [Tag(self._client, tag) for tag in tags]

class ApiTag(ApiBase):
    """ Definitions of /tag/ API endpoints """
    def create(self, tag, **kwds):
        """
        Endpoint: /tag/create.json

        Creates a new tag.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        return self._client.post("/tag/create.json", tag=tag, **kwds)["result"]

    def delete(self, tag, **kwds):
        """
        Endpoint: /tag/<id>/delete.json

        Deletes a tag.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        return tag.delete(**kwds)

    def update(self, tag, **kwds):
        """
        Endpoint: /tag/<id>/update.json

        Updates a tag with the specified parameters.
        Returns the updated tag object.
        """
        if not isinstance(tag, Tag):
            tag = Tag(self._client, {"id": tag})
        tag.update(**kwds)
        return tag

    # def view(self, tag, **kwds):
