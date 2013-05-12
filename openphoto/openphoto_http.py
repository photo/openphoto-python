from __future__ import unicode_literals
import sys
import os
try:
    from urllib.parse import urlunparse # Python3
except ImportError:
    from urlparse import urlunparse # Python2
import requests
import requests_oauthlib
import logging
try:
    import io # Python3
except ImportError:
    import StringIO as io # Python2
try:
    from configparser import ConfigParser # Python3
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser # Python2

if sys.version < '3':
    text_type = unicode # Python2
else:
    text_type = str # Python3

from .objects import OpenPhotoObject
from .errors import *

if sys.version < '3':
	# requests_oauth needs to decode to ascii for Python2
    _oauth_decoding = "utf-8"
else:
	# requests_oauth needs to use (unicode) strings for Python3
    _oauth_decoding = None # Python3

DUPLICATE_RESPONSE = {"code": 409,
                      "message": "This photo already exists"}

class OpenPhotoHttp:
    """
    Base class to handle HTTP requests to an OpenPhoto server.
    If no parameters are specified, config is loaded from the default
        location (~/.config/openphoto/default).
    The config_file parameter is used to specify an alternate config file.
    If the host parameter is specified, no config file is loaded and
        OAuth tokens (consumer*, token*) can optionally be specified.
    All requests will include the api_version path, if specified.
    This should be used to ensure that your application will continue to work
        even if the OpenPhoto API is updated to a new revision.
    """
    def __init__(self, config_file=None, host=None,
                 consumer_key='', consumer_secret='',
                 token='', token_secret='', api_version=None):
        self._api_version = api_version

        self._logger = logging.getLogger("openphoto")

        if host is None:
            self.config_path = self._get_config_path(config_file)
            config = self._read_config(self.config_path)
            self._host = config['host']
            self._consumer_key = config['consumerKey']
            self._consumer_secret = config['consumerSecret']
            self._token = config['token']
            self._token_secret = config['tokenSecret']
        else:
            self._host = host
            self._consumer_key = consumer_key
            self._consumer_secret = consumer_secret
            self._token = token
            self._token_secret = token_secret

        if host is not None and config_file is not None:
            raise ValueError("Cannot specify both host and config_file")

        # Remember the most recent HTTP request and response
        self.last_url = None
        self.last_params = None
        self.last_response = None

    def get(self, endpoint, process_response=True, **params):
        """
        Performs an HTTP GET from the specified endpoint (API path),
            passing parameters if given.
        The api_version is prepended to the endpoint,
            if it was specified when the OpenPhoto object was created.

        Returns the decoded JSON dictionary, and raises exceptions if an
            error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        if self._api_version is not None:
            endpoint = "/v%d%s" % (self._api_version, endpoint)
        url = urlunparse(('http', self._host, endpoint, '', '', ''))

        if self._consumer_key:
            auth = requests_oauthlib.OAuth1(self._consumer_key, self._consumer_secret,
                                            self._token, self._token_secret,
                                            decoding=_oauth_decoding)
        else:
            auth = None

        with requests.Session() as s:
            response = s.get(url, params=params, auth=auth)

        self._logger.info("============================")
        self._logger.info("GET %s" % url)
        self._logger.info("---")
        self._logger.info(response.text)

        self.last_url = url
        self.last_params = params
        self.last_response = response

        if process_response:
            return self._process_response(response)
        else:
            return response.text

    def post(self, endpoint, process_response=True, files = {}, **params):
        """
        Performs an HTTP POST to the specified endpoint (API path),
            passing parameters if given.
        The api_version is prepended to the endpoint,
            if it was specified when the OpenPhoto object was created.

        Returns the decoded JSON dictionary, and raises exceptions if an
            error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        if self._api_version is not None:
            endpoint = "/v%d%s" % (self._api_version, endpoint)
        url = urlunparse(('http', self._host, endpoint, '', '', ''))

        if not self._consumer_key:
            raise OpenPhotoError("Cannot issue POST without OAuth tokens")

        auth = requests_oauthlib.OAuth1(self._consumer_key, self._consumer_secret,
                                        self._token, self._token_secret,
                                        decoding=_oauth_decoding)
        with requests.Session() as s:
            if files:
                # Need to pass parameters as URL query, so they get OAuth signed
                response = s.post(url, params=params, files=files, auth=auth)
            else:
                # Passing parameters as URL query doesn't work if there are no files to send.
                # Send them as form data instead.
                response = s.post(url, data=params, auth=auth)

        self._logger.info("============================")
        self._logger.info("POST %s" % url)
        self._logger.info("params: %s" % repr(params))
        if files:
            self._logger.info("files:  %s" % repr(files))
        self._logger.info("---")
        self._logger.info(response.text)

        self.last_url = url
        self.last_params = params
        self.last_response = response

        if process_response:
            return self._process_response(response)
        else:
            return response.text

    @staticmethod
    def _process_params(params):
        """ Converts Unicode/lists/booleans inside HTTP parameters """
        processed_params = {}
        for key, value in params.items():
            # Extract IDs from objects
            if isinstance(value, OpenPhotoObject):
                value = value.id

            # Ensure value is UTF-8 encoded
            if isinstance(value, text_type):
                value = value.encode("utf-8")

            # Handle lists
            if isinstance(value, list):
                # Make a copy of the list, to avoid overwriting the original
                new_list = list(value)
                # Extract IDs from objects in the list
                for i, item in enumerate(new_list):
                    if isinstance(item, OpenPhotoObject):
                        new_list[i] = item.id
                # Convert list to string
                value = ','.join([str(item) for item in new_list])

            # Handle booleans
            if isinstance(value, bool):
                value = 1 if value else 0
            processed_params[key] = value

        return processed_params

    @staticmethod
    def _process_response(response):
        """
        Decodes the JSON response, returning a dict.
        Raises an exception if an invalid response code is received.
        """
        try:
            json_response = response.json()
            code = json_response["code"]
            message = json_response["message"]
        except (ValueError, KeyError):
            # Response wasn't OpenPhoto JSON - check the HTTP status code
            if 200 <= response.status_code < 300:
                # Status code was valid, so just reraise the exception
                raise
            elif response.status_code == 404:
                raise OpenPhoto404Error("HTTP Error %d: %s" % (response.status_code, response.reason))
            else:
                raise OpenPhotoError("HTTP Error %d: %s" % (response.status_code, response.reason))

        if 200 <= code < 300:
            return json_response
        elif (code == DUPLICATE_RESPONSE["code"] and
               DUPLICATE_RESPONSE["message"] in message):
            raise OpenPhotoDuplicateError("Code %d: %s" % (code, message))
        else:
            raise OpenPhotoError("Code %d: %s" % (code, message))

    @staticmethod
    def _result_to_list(result):
        """ Handle the case where the result contains no items """
        if not result:
            return []
        if result[0]["totalRows"] == 0:
            return []
        else:
            return result

    @staticmethod
    def _get_config_path(config_file):
        config_path = os.getenv('XDG_CONFIG_HOME')
        if not config_path:
            config_path = os.path.join(os.getenv('HOME'), ".config")
        if not config_file:
            config_file = "default"
        return os.path.join(config_path, "openphoto", config_file)

    def _read_config(self, config_file):
        """
        Loads config data from the specified file.
        If config_file doesn't exist, returns an empty authentication config for localhost.
        """
        section = "DUMMY"
        defaults = {'host': 'localhost',
                    'consumerKey': '', 'consumerSecret': '',
                    'token': '', 'tokenSecret':'',
                    }
        # Insert an section header at the start of the config file, so ConfigParser can understand it
        buf = io.StringIO()
        buf.write('[%s]\n' % section)
        with io.open(config_file, "r") as f:
            buf.write(f.read())

        buf.seek(0, os.SEEK_SET)
        parser = ConfigParser()
        parser.optionxform = str # Case-sensitive options
        try:
            parser.read_file(buf) # Python3
        except AttributeError:
            parser.readfp(buf) # Python2

        # Trim quotes
        config = parser.items(section)
        config = [(item[0].replace('"', ''), item[1].replace('"', '')) for item in config]
        config = [(item[0].replace("'", ""), item[1].replace("'", "")) for item in config]
        config = dict(config)

        # Apply defaults
        for key in defaults:
            if key not in config:
                config[key] = defaults[key]

        return config
