"""
api_base.py: Base class for all API classes
"""

class ApiBase(object):
    def __init__(self, client):
        self._client = client

    @staticmethod
    def _build_filter_string(filters):
        """
        :param filters: dictionary containing the filters
        :returns: filter_string formatted for an API endpoint
        """
        filter_string = ""
        for filter in filters:
            filter_string += "%s-%s/" % (filter, filters[filter])
        return filter_string
