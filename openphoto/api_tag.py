from openphoto_http import OpenPhotoHttp, OpenPhotoError
from objects import Tag

class ApiTag(OpenPhotoHttp):
    def tag_create(self, tag_id, **kwds):
        """ Create a new tag and return it """
        result = self.post("/tag/create.json", tag=tag_id, **kwds)["result"]
        return Tag(self, result)

    def tag_delete(self, tag_id, **kwds):
        """ Delete a tag """
        tag = Tag(self, {"id": tag_id})
        tag.delete(**kwds)

    def tag_update(self, tag_id, **kwds):
        """ Update a tag """
        tag = Tag(self, {"id": tag_id})
        tag.update(**kwds)
        return tag

    def tags_list(self, **kwds):
        """ Returns a list of Tag objects """
        results = self.get("/tags/list.json", **kwds)["result"]
        return [Tag(self, tag) for tag in results]

