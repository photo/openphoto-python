import oauth2 as oauth
import urlparse
import urllib
import httplib2
try:
    import json
except ImportError:
    import simplejson as json

class OpenPhotoError(Exception):
    """ Indicates that an OpenPhoto operation failed """
    pass

class OpenPhotoDuplicateError(OpenPhotoError):
    """ Indicates that an upload operation failed due to a duplicate photo """
    pass

class NotImplementedError(OpenPhotoError):
    """ Indicates that the API function has not yet been coded - please help! """
    pass

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

    def get(self, endpoint, **params):
        """
        Performs an HTTP GET from the specified endpoint (API path),
        passing parameters if given.
        Returns the decoded JSON dictionary, and 
        raises exceptions if an error code is received.
        """
        response = json.loads(self.get_raw(endpoint, **params))
        self._process_response(response)
        return response

    def post(self, endpoint, **params):
        """
        Performs an HTTP POST to the specified endpoint (API path),
        passing parameters if given.
        Returns the decoded JSON dictionary, and 
        raises exceptions if an error code is received.
        """
        response = json.loads(self.post_raw(endpoint, **params))
        self._process_response(response)
        return response

    def get_raw(self, endpoint, **params):
        """
        Performs an HTTP GET from the specified endpoint (API path),
        passing parameters if given.
        Returns the raw HTTP content string.
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
        return content

    def post_raw(self, endpoint, **params):
        """
        Performs an HTTP POST to the specified endpoint (API path),
        passing parameters if given.
        Returns the raw HTTP content string.
        """
        params = self._process_params(params)
        url = urlparse.urlunparse(('http', self._host, endpoint, '', '', ''))
        
        if not self._consumer_key:
            raise OpenPhotoError("Cannot issue POST without OAuth tokens")

        consumer = oauth.Consumer(self._consumer_key, self._consumer_secret)
        token = oauth.Token(self._token, self._token_secret)

        client = oauth.Client(consumer, token)
        body = urllib.urlencode(params)
        _, content = client.request(url, "POST", body)
        return content

    @staticmethod
    def _process_params(params):
        """ Converts Unicode/lists/booleans inside HTTP parameters """
        processed_params = {}
        for key, value in params.items():
            # Use UTF-8 encoding
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            # Handle lists
            if isinstance(value, list):
                value = ",".join(value)
            # Handle booleans
            if isinstance(value, bool):
                value = 1 if value else 0
            processed_params[key] = value
        return processed_params

    @staticmethod
    def _process_response(response):
        """ Raises an exception if an invalid response code is received """
        if response["code"] >= 200 and response["code"] < 300:
            return

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
