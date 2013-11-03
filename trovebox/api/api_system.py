"""
api_system.py : Trovebox System API Classes
"""
from .api_base import ApiBase

class ApiSystem(ApiBase):
    """ Definitions of /system/ API endpoints """
    def version(self, **kwds):
        """
        Endpoint: /system/version.json

        Returns a dictionary containing the various server version strings
        """
        return self._client.get("/system/version.json", **kwds)["result"]

    def diagnostics(self, **kwds):
        """
        Endpoint: /system/diagnostics.json

        Runs a set of diagnostic tests on the server.
        Returns a dictionary containing the results.
        """
        # Don't process the result automatically, since this raises an exception
        # on failure, which doesn't provide the cause of the failure
        self._client.get("/system/diagnostics.json", process_response=False,
                         **kwds)
        return self._client.last_response.json()["result"]
