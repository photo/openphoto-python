"""
api_base.py: Base class for all API classes
"""

class ApiBase(object):
    """ Base class for all API objects """
    def __init__(self, client):
        self._client = client

    @staticmethod
    def _build_option_string(options):
        """
        :param options: dictionary containing the options
        :returns: option_string formatted for an API endpoint
        """
        option_string = ""
        if options is not None:
            for key in options:
                option_string += "/%s-%s" % (key, options[key])
        return option_string

    @staticmethod
    def _extract_id(obj):
        """ Return obj.id, or obj if the object doesn't have an ID """
        try:
            return obj.id
        except AttributeError:
            return obj

    @staticmethod
    def _result_to_list(result):
        """ Handle the case where the result contains no items """
        if not result:
            return []
        if "totalRows" in result[0] and result[0]["totalRows"] == 0:
            return []
        else:
            return result
