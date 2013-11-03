"""
http.py : Trovebox HTTP Access
"""
from __future__ import unicode_literals
import sys
import requests
import requests_oauthlib
import logging
try:
    from urllib.parse import urlparse, urlunparse # Python3
except ImportError:
    from urlparse import urlparse, urlunparse # Python2

from trovebox.objects.trovebox_object import TroveboxObject
from .errors import TroveboxError, Trovebox404Error, TroveboxDuplicateError
from .auth import Auth

if sys.version < '3':
    TEXT_TYPE = unicode
else: # pragma: no cover
    TEXT_TYPE = str

DUPLICATE_RESPONSE = {"code": 409,
                      "message": "This photo already exists"}

class Http(object):
    """
    Base class to handle HTTP requests to a Trovebox server.
    If no parameters are specified, auth config is loaded from the
        default location (~/.config/trovebox/default).
    The config_file parameter is used to specify an alternate config file.
    If the host parameter is specified, no config file is loaded and
        OAuth tokens (consumer*, token*) can optionally be specified.
    """

    _CONFIG_DEFAULTS = {"api_version" : None,
                        "ssl_verify" : True,
                        }

    def __init__(self, config_file=None, host=None,
                 consumer_key='', consumer_secret='',
                 token='', token_secret='', api_version=None):

        self.config = dict(self._CONFIG_DEFAULTS)

        if api_version is not None: # pragma: no cover
            print("Deprecation Warning: api_version should be set by "
                  "calling the configure function")
            self.config["api_version"] = api_version

        self._logger = logging.getLogger("trovebox")

        self.auth = Auth(config_file, host,
                         consumer_key, consumer_secret,
                         token, token_secret)

        self.host = self.auth.host

        # Remember the most recent HTTP request and response
        self.last_url = None
        self.last_params = None
        self.last_response = None

    def configure(self, **kwds):
        """
        Update Trovebox HTTP client configuration.

        :param api_version: Include a Trovebox API version in all requests.
            This can be used to ensure that your application will continue
            to work even if the Trovebox API is updated to a new revision.
            [default: None]
        :param ssl_verify: If true, HTTPS SSL certificates will always be
            verified [default: True]
        """
        for item in kwds:
            self.config[item] = kwds[item]

    def get(self, endpoint, process_response=True, **params):
        """
        Performs an HTTP GET from the specified endpoint (API path),
            passing parameters if given.
        The api_version is prepended to the endpoint,
            if it was specified when the Trovebox object was created.

        Returns the decoded JSON dictionary, and raises exceptions if an
            error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        url = self._construct_url(endpoint)

        if self.auth.consumer_key:
            auth = requests_oauthlib.OAuth1(self.auth.consumer_key,
                                            self.auth.consumer_secret,
                                            self.auth.token,
                                            self.auth.token_secret)
        else:
            auth = None

        with requests.Session() as session:
            session.verify = self.config["ssl_verify"]
            response = session.get(url, params=params, auth=auth)

        self._logger.info("============================")
        self._logger.info("GET %s" % url)
        self._logger.info("---")
        self._logger.info(response.text[:1000])
        if len(response.text) > 1000: # pragma: no cover
            self._logger.info("[Response truncated to 1000 characters]")

        self.last_url = url
        self.last_params = params
        self.last_response = response

        if process_response:
            return self._process_response(response)
        else:
            if 200 <= response.status_code < 300:
                return response.text
            else:
                raise TroveboxError("HTTP Error %d: %s" %
                                    (response.status_code, response.reason))

    def post(self, endpoint, process_response=True, files=None, **params):
        """
        Performs an HTTP POST to the specified endpoint (API path),
            passing parameters if given.
        The api_version is prepended to the endpoint,
            if it was specified when the Trovebox object was created.

        Returns the decoded JSON dictionary, and raises exceptions if an
            error code is received.
        Returns the raw response if process_response=False
        """
        params = self._process_params(params)
        url = self._construct_url(endpoint)

        if not self.auth.consumer_key:
            raise TroveboxError("Cannot issue POST without OAuth tokens")

        auth = requests_oauthlib.OAuth1(self.auth.consumer_key,
                                        self.auth.consumer_secret,
                                        self.auth.token,
                                        self.auth.token_secret)
        with requests.Session() as session:
            session.verify = self.config["ssl_verify"]
            if files:
                # Need to pass parameters as URL query, so they get OAuth signed
                response = session.post(url, params=params,
                                        files=files, auth=auth)
            else:
                # Passing parameters as URL query doesn't work
                # if there are no files to send.
                # Send them as form data instead.
                response = session.post(url, data=params, auth=auth)

        self._logger.info("============================")
        self._logger.info("POST %s" % url)
        self._logger.info("params: %s" % repr(params))
        if files:
            self._logger.info("files:  %s" % repr(files))
        self._logger.info("---")
        self._logger.info(response.text[:1000])
        if len(response.text) > 1000: # pragma: no cover
            self._logger.info("[Response truncated to 1000 characters]")

        self.last_url = url
        self.last_params = params
        self.last_response = response

        if process_response:
            return self._process_response(response)
        else:
            if 200 <= response.status_code < 300:
                return response.text
            else:
                raise TroveboxError("HTTP Error %d: %s" %
                                    (response.status_code, response.reason))

    def _construct_url(self, endpoint):
        """Return the full URL to the specified endpoint"""
        parsed_url = urlparse(self.host)
        scheme = parsed_url[0]
        host = parsed_url[1]
        # Handle host without a scheme specified (eg. www.example.com)
        if scheme == "":
            scheme = "http"
            host = self.host

        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        if self.config["api_version"] is not None:
            endpoint = "/v%d%s" % (self.config["api_version"], endpoint)
        return urlunparse((scheme, host, endpoint, '', '', ''))

    @staticmethod
    def _process_params(params):
        """ Converts Unicode/lists/booleans inside HTTP parameters """
        processed_params = {}
        for key, value in params.items():
            # Extract IDs from objects
            if isinstance(value, TroveboxObject):
                value = value.id

            # Ensure value is UTF-8 encoded
            if isinstance(value, TEXT_TYPE):
                value = value.encode("utf-8")

            # Handle lists
            if isinstance(value, list):
                # Make a copy of the list, to avoid overwriting the original
                new_list = list(value)
                # Extract IDs from objects in the list
                for i, item in enumerate(new_list):
                    if isinstance(item, TroveboxObject):
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
        if response.status_code == 404:
            raise Trovebox404Error("HTTP Error %d: %s" %
                                   (response.status_code, response.reason))
        try:
            json_response = response.json()
            code = json_response["code"]
            message = json_response["message"]
        except (ValueError, KeyError):
            # Response wasn't Trovebox JSON - check the HTTP status code
            if 200 <= response.status_code < 300:
                # Status code was valid, so just reraise the exception
                raise
            else:
                raise TroveboxError("HTTP Error %d: %s" %
                                    (response.status_code, response.reason))

        if 200 <= code < 300:
            return json_response
        elif (code == DUPLICATE_RESPONSE["code"] and
               DUPLICATE_RESPONSE["message"] in message):
            raise TroveboxDuplicateError("Code %d: %s" % (code, message))
        else:
            raise TroveboxError("Code %d: %s" % (code, message))
