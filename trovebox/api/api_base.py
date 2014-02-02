"""
api_base.py: Base class for all API classes
"""
try:
    from urllib.parse import quote # Python3
except ImportError:
    from urllib import quote # Python2


class ApiBase(object):
    """ Base class for all API objects """
    def __init__(self, client):
        self._client = client

    def _build_option_string(self, options):
        """
        :param options: dictionary containing the options
        :returns: option_string formatted for an API endpoint
        """
        option_string = ""
        if options is not None:
            for key in options:
                option_string += "/%s-%s" % (key, options[key])
        return self._quote_url(option_string)

    @staticmethod
    def _extract_id(obj):
        """ Return obj.id, or obj if the object doesn't have an ID """
        try:
            return obj.id
        except AttributeError:
            return obj

    @staticmethod
    def _quote_url(string):
        """ Make a string suitable for insertion into a URL """
        return quote(string.encode('utf-8'))

    @staticmethod
    def _result_to_list(result):
        """ Handle the case where the result contains no items """
        if not result:
            return []
        if "totalRows" in result[0] and result[0]["totalRows"] == 0:
            return []
        else:
            return result
