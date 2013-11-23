"""
Base object supporting the storage of custom fields as attributes
"""
class TroveboxObject(object):
    """ Base object supporting the storage of custom fields as attributes """
    _type = "None"
    def __init__(self, client, json_dict):
        self.id = None
        self.name = None
        self._client = client
        self._json_dict = json_dict
        self._set_fields(json_dict)

    def _set_fields(self, json_dict):
        """ Set this object's attributes specified in json_dict """
        for key, value in json_dict.items():
            if not key.startswith("_"):
                setattr(self, key, value)

    def _replace_fields(self, json_dict):
        """
        Delete this object's attributes, and replace with
        those in json_dict.
        """
        for key in self._json_dict.keys():
            if not key.startswith("_"):
                delattr(self, key)
        self._json_dict = json_dict
        self._set_fields(json_dict)

    def _delete_fields(self):
        """
        Delete this object's attributes, including name and id
        """
        for key in self._json_dict.keys():
            if not key.startswith("_"):
                delattr(self, key)
        self._json_dict = {}
        self.id = None
        self.name = None

    def __repr__(self):
        if self.name is not None:
            return "<%s name='%s'>" % (self.__class__.__name__, self.name)
        elif self.id is not None:
            return "<%s id='%s'>" % (self.__class__.__name__, self.id)
        else:
            return "<%s>" % (self.__class__.__name__)

    def get_fields(self):
        """ Returns this object's attributes """
        return self._json_dict

    def get_type(self):
        """ Return this object's type (eg. "photo") """
        return self._type
