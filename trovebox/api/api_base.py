"""
api_base.py: Base class for all API classes
"""

class ApiBase(object):
    def __init__(self, client):
        self._client = client

