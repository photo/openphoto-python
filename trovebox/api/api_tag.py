"""
api_tag.py : Trovebox Tag API Classes
"""
try:
    from urllib.parse import quote # Python3
except ImportError:
    from urllib import quote # Python2

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
        tags = self._result_to_list(tags)
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
        return self._client.post("/tag/%s/delete.json" %
                                 quote(self._extract_id(tag)),
                                 **kwds)["result"]

    def update(self, tag, **kwds):
        """
        Endpoint: /tag/<id>/update.json

        Updates a tag with the specified parameters.
        Returns the updated tag object.
        """
        result = self._client.post("/tag/%s/update.json" %
                                   quote(self._extract_id(tag)),
                                   **kwds)["result"]
        return Tag(self._client, result)

    # def view(self, tag, **kwds):
