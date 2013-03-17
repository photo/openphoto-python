import oauth2 as oauth
import urlparse
import urllib
import httplib2
try:
    import json
except ImportError:
    import simplejson as json

from objects import OpenPhotoObject
from errors import *
from multipart_post import encode_multipart_formdata

DUPLICATE_RESPONSE = {"code": 409,
                      "message": "This photo already exists"}

class OpenPhotoHttp:
    """ Base class to handle HTTP requests to an OpenPhoto server """
    def __init__(self, host, consumer_key='', consumer_secret='',
                 token='', token_secret=''):
        self._host = host
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._token = token
        self._token_secret = token_secret

        # Remember the most recent HTTP request and response
        self.last_url = None
        self.last_params = None
        self.last_response = None

    def get(self, endpoint, process_response=True, **params):
        """
        Performs an HTTP GET from the specified endpoint (API path),
        passing parameters if given.
        Returns the decoded JSON dictionary, and raises exceptions if an 
        error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        url = urlparse.urlunparse(('http', self._host, endpoint, '',
                                   urllib.urlencode(params), ''))
        if self._consumer_key:
            consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
            token = oauth.Token(self._token, self._token_secret)
            client = oauth.Client(consumer, token)
        else:
            client = httplib2.Http()

        _, content = client.request(url, "GET")

        self.last_url = url
        self.last_params = params
        self.last_response = content

        if process_response:
            return self._process_response(content)
            return response
        else:
            return content

    def post(self, endpoint, process_response=True, files = {}, **params):
        """
        Performs an HTTP POST to the specified endpoint (API path),
        passing parameters if given.
        Returns the decoded JSON dictionary, and raises exceptions if an 
        error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        url = urlparse.urlunparse(('http', self._host, endpoint, '', '', ''))
        
        if not self._consumer_key:
            raise OpenPhotoError("Cannot issue POST without OAuth tokens")

        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        token = oauth.Token(self._token, self._token_secret)
        client = oauth.Client(consumer, token)

        if files:
            headers, body = encode_multipart_formdata(params, files)
        else:
            headers = {}
            body = urllib.urlencode(params)

        _, content = client.request(url, "POST", body, headers)

        self.last_url = url
        self.last_params = params
        self.last_response = content

        if process_response:
            return self._process_response(content)
        else:
            return content

    @staticmethod
    def _process_params(params):
        """ Converts Unicode/lists/booleans inside HTTP parameters """
        processed_params = {}
        for key, value in params.items():
            # Extract IDs from objects
            if isinstance(value, OpenPhotoObject):
                value = value.id

            # Use UTF-8 encoding
            if isinstance(value, unicode):
                value = value.encode('utf-8')

            # Handle lists
            if isinstance(value, list):
                # Make a copy of the list, to avoid overwriting the original
                new_list = list(value)
                # Extract IDs from objects in the list
                for i, item in enumerate(new_list):
                    if isinstance(item, OpenPhotoObject):
                        new_list[i] = item.id
                # Convert list to unicode string
                value = u','.join([unicode(item) for item in new_list])

            # Handle booleans
            if isinstance(value, bool):
                value = 1 if value else 0
            processed_params[key] = value

        return processed_params

    @staticmethod
    def _process_response(content):
        """ 
        Decodes the JSON response, returning a dict.
        Raises an exception if an invalid response code is received.
        """
        response = json.loads(content)

        if response["code"] >= 200 and response["code"] < 300:
            # Valid response code
            return response

        error_message = "Code %d: %s" % (response["code"],
                                         response["message"])

        # Special case for a duplicate photo error
        if (response["code"] == DUPLICATE_RESPONSE["code"] and 
               DUPLICATE_RESPONSE["message"] in response["message"]):
            raise OpenPhotoDuplicateError(error_message)
        
        raise OpenPhotoError(error_message)

    @staticmethod
    def _result_to_list(result):
        """ Handle the case where the result contains no items """
        if result[0]["totalRows"] == 0:
            return []
        else:
            return result
