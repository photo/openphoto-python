"""
Representation of a Tag object
"""
try:
    from urllib.parse import quote # Python3
except ImportError:
    from urllib import quote # Python2

from trovebox.errors import TroveboxError
from .trovebox_object import TroveboxObject

class Tag(TroveboxObject):
    """ Representation of a Tag object """
    def delete(self, **kwds):
        """
        Delete this tag.
        Returns True if successful.
        Raises a TroveboxError if not.
        """
        result = self._trovebox.post("/tag/%s/delete.json" %
                                     quote(self.id), **kwds)["result"]
        if not result:
            raise TroveboxError("Delete response returned False")
        self._delete_fields()
        return result

    def update(self, **kwds):
        """ Update this tag with the specified parameters """
        new_dict = self._trovebox.post("/tag/%s/update.json" % quote(self.id),
                                       **kwds)["result"]
        self._replace_fields(new_dict)
